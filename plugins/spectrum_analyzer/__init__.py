import colorsys
import multiprocessing
import queue
import time

import alsaaudio as aa
import audioread
import pyaudio
import numpy as np
from numpy import sum as npsum
from numpy import abs as npabs
from numpy import log10, frombuffer, empty, hanning, fft, delete, int16, zeros
from pylru import lrudecorator

from config_loader import config_loader
from plugin_base import Plugin

CONFIG_FILE_NAME = 'spectrum_analyzer.yml'

default_config = {
    # The minimum and maximum frequencies in Hz to use for spectrum analysis
    'MIN_FREQ': 20,
    'MAX_FREQ': 8000,

    # Number of audio frames to read/write at a time
    'CHUNK_SIZE': 2048,

    # Refresh rate of the spectrum analyzer in Hz
    'UPDATE_HZ': 24,

    # Starting LED hue, from 0.0 to 1.0
    'INITIAL_HUE': 0.0,

    # How much weight to put towards the current color frame
    # A fade factor of 1.0 disables fading
    'FADE_FACTOR': 0.7,

    # How fast to scroll the LEDs around the panel, in LEDs per frame
    # A negative speed scrolls backwards and 0 disables scrolling
    'SCROLL_SPEED': 1.0,

    # How much to shift LED hues per frame
    # A negative speed shifts backwards and 0 disables shifting
    'HUE_SHIFT_FACTOR': 0.025,

    # List of audio files to play, in order
    'PLAYLIST': [],

    # Use microphone input instead of songs
    'USE_MIC': True
}

config_loader.register_config('spectrum_analyzer', CONFIG_FILE_NAME, default_config)
config = config_loader.load_config('spectrum_analyzer')
twilight_config = config_loader.load_config('twilight')


def play_music(song_filename, music_frame_queue):

    if song_filename is not None:
        # Open music file and get its characteristics
        music_file = audioread.audio_open(song_filename)

        num_channels = music_file.channels
        sample_rate = music_file.samplerate

        # Set up audio playback
        output = aa.PCM(aa.PCM_PLAYBACK, aa.PCM_NORMAL)
        output.setchannels(num_channels)
        output.setrate(sample_rate)
        output.setformat(aa.PCM_FORMAT_S16_LE)
        output.setperiodsize(config['CHUNK_SIZE'])

        # Pass song information to parent process
        music_info = {
            'music_filename': song_filename,
            'num_channels': music_file.channels,
            'sample_rate': music_file.samplerate,
            'duration': music_file.duration
        }
        music_frame_queue.put(music_info)

        # Start playing
        for data in music_file:
            output.write(data)
            music_frame_queue.put(data)

    else:
        # Use microphone input
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=2,
            rate=44100,
            input=True,
            frames_per_buffer=config['CHUNK_SIZE']
        )

        music_info = {
            'music_filename': 'microphone',
            'num_channels': 2,
            'sample_rate': 44100,
            'duration': None
        }
        music_frame_queue.put(music_info)

        while True:
            data = stream.read(config['CHUNK_SIZE'])
            music_frame_queue.put(data)


# TODO: Extend plugin API to make this plugin more useful
class SpectrumAnalyzerPlugin(Plugin):

    def __init__(self):
        Plugin.__init__(self)
        self.playlist_index = 0
        self.last_frame_time = 0
        self.starting_led = 0.0
        self.starting_hue = config['INITIAL_HUE']

        self.music_info = None
        self.last_music_frame = None
        self.last_color_frame = [(0, 0, 0) for _ in range(twilight_config['NUM_LEDS_PER_STRIP'] // 2)]

        self.frequency_limits = None
        self.calculate_channel_frequency(
            config['MIN_FREQ'],
            config['MAX_FREQ'],
            twilight_config['NUM_LEDS_PER_STRIP'] // 2
        )

        self.music_queue = multiprocessing.Queue()
        if config['USE_MIC']:
            self.music_subprocess = multiprocessing.Process(
                target=play_music,
                kwargs={
                    'song_filename': None,
                    'music_frame_queue': self.music_queue
                },
                daemon=False
            )
        else:
            self.music_subprocess = multiprocessing.Process(
                target=play_music,
                kwargs={
                    'song_filename': config['PLAYLIST'][self.playlist_index],
                    'music_frame_queue': self.music_queue
                },
                daemon=True
            )
        self.music_subprocess.start()

    def calculate_channel_frequency(self, min_freq, max_freq, num_channels):
        """Calculate the frequency bands to separate the audio waveform into."""
        octaves = (np.log(max_freq / min_freq)) / np.log(2)
        octaves_per_channel = octaves / num_channels
        frequency_limits = []
        self.frequency_limits = []

        frequency_limits.append(min_freq)

        for pin in range(1, num_channels + 1):
            frequency_limits.append(frequency_limits[-1] * 10 ** (0.3 * octaves_per_channel))

        for pin in range(0, num_channels):
            self.frequency_limits.append((frequency_limits[pin], frequency_limits[pin + 1]))

    def get_next_music_frame(self):
        """Get the last frame of audio data played by the playback subprocess.
        If a new song just started playing, update the known characteristics of the song.
        Afterwards, if playback has finished, start playing the next song.

        Return True if a valid frame of audio data is available."""

        # Clear the audio frame queue and update our variables
        try:
            while not self.music_queue.empty():
                data = self.music_queue.get_nowait()
                if isinstance(data, dict):
                    self.music_info = data
                else:
                    self.last_music_frame = data
        except queue.Empty:
            pass

        # Check if current song ended and play next song if so
        if not self.music_subprocess.is_alive():
            # TODO: Have the plugin end when playlist is complete, instead of looping
            # Should also make this configurable

            # Advance playlist, then start song
            self.playlist_index = (self.playlist_index + 1) % len(config['PLAYLIST'])
            self.music_queue = multiprocessing.Queue()
            self.music_subprocess = multiprocessing.Process(
                target=play_music,
                kwargs={
                    'song_filename': config['PLAYLIST'](self.playlist_index),
                    'music_frame_queue': self.music_queue
                },
                daemon=True
            )
            self.music_subprocess.start()

        return self.last_music_frame is not None

    def ready(self):
        # Check if we have a valid audio frame and if enough time has passed
        return self.get_next_music_frame() and (time.time() - self.last_frame_time > (1.0 / config['UPDATE_HZ']))

    def getNextFrame(self):
        # Get an audio frame, then perform FFT
        self.get_next_music_frame()
        matrix = calculate_levels(
            self.last_music_frame,
            config['CHUNK_SIZE'],
            self.music_info['sample_rate'],
            self.frequency_limits,
            len(self.frequency_limits)
        )

        colors = [(0, 0, 0) for _ in self.frequency_limits]

        # Placeholder values for FFT mean and standard deviation
        # TODO: make these more meaningful
        mean = 12.0
        std = 1.5

        self.starting_hue += config['HUE_SHIFT_FACTOR']

        # This function divides the LEDs into two halves and maps each LED in a half to an audio channel
        for channel in range(0, len(colors)):
            # This hue calculation gets us a rainbow-like color distribution
            hue = self.starting_hue + (channel / len(self.frequency_limits))

            saturation = 1.0
            value = matrix[channel] - mean + 0.5 * std
            value /= 1.25 * std

            # Colorsys takes 0.0 - 1.0 for all 3 parameters
            red, green, blue = colorsys.hsv_to_rgb(hue, saturation, value)

            # Clamp our RGB values
            red = int(255 * red)
            green = int(255 * green)
            blue = int(255 * blue)

            if red > 255:
                red = 255
            elif red < 0:
                red = 0

            if green > 255:
                green = 255
            elif green < 0:
                green = 0

            if blue > 255:
                blue = 255
            elif blue < 0:
                blue = 0

            old_r, old_g, old_b = self.last_color_frame[channel]

            factor = config['FADE_FACTOR']
            opposite = 1.0 - factor

            colors[channel] = (
                int(factor * red + opposite * old_r),
                int(factor * green + opposite * old_g),
                int(factor * blue + opposite * old_b)
            )

        self.last_color_frame = colors

        self.starting_led += config['SCROLL_SPEED']
        if self.starting_led > len(colors) * 2:
            self.starting_led -= len(colors) * 2
        elif self.starting_led < 0:
            self.starting_led += len(colors) * 2

        # Duplicate our colors to the other half of the LED strip
        colors_doubled = colors * 2
        colors_doubled = colors_doubled[int(self.starting_led):] + colors_doubled[:int(self.starting_led)]

        frame = {}
        for row in self.tile_matrix:
            for tile in row:
                if tile is not None:
                    frame[tile['unit']] = colors_doubled

        # Clear our processed audio frame so we don't use stale data
        self.last_music_frame = None
        self.last_frame_time = time.time()
        return frame


#
# Licensed under the BSD license.  See full license in LICENSE file.
# http://www.lightshowpi.com/
#
# Author: Todd Giles (todd@lightshowpi.com)

"""FFT methods for computing / analyzing frequency response of audio.

This is simply a wrapper around FFT support in numpy.

Initial FFT code inspired from the code posted here:
http://www.raspberrypi.org/phpBB3/viewtopic.php?t=35838&p=454041

Optimizations from work by Scott Driscoll:
http://www.instructables.com/id/Raspberry-Pi-Spectrum-Analyzer-with-RGB-LED-Strip-/

Third party dependencies:

numpy: for FFT calculation - http://www.numpy.org/
"""


@lrudecorator(100)
def cached_hanning(size):
    return hanning(size)


def calculate_levels(data, chunk_size, sample_rate, frequency_limits, num_bins, input_channels=2):
    """Calculate frequency response for each channel defined in frequency_limits

    :param data: decoder.frames(), audio data for fft calculations
    :type data: decoder.frames

    :param chunk_size: chunk size of audio data
    :type chunk_size: int

    :param sample_rate: audio file sample rate
    :type sample_rate: int

    :param frequency_limits: list of frequency_limits
    :type frequency_limits: list

    :param num_bins: length of gpio to process
    :type num_bins: int

    :param input_channels: number of audio input channels to process for (default=2)
    :type input_channels: int

    :return:
    :rtype: numpy.array
    """

    # create a numpy array, taking just the left channel if stereo
    data_stereo = frombuffer(data, dtype=int16)
    if input_channels == 2:
        # data has 2 bytes per channel
        data = empty(int(len(data) / (2 * input_channels)))

        # pull out the even values, just using left channel
        data[:] = data_stereo[:len(data_stereo) - (len(data_stereo) % 2):2]
    elif input_channels == 1:
        data = data_stereo

    # if you take an FFT of a chunk of audio, the edges will look like
    # super high frequency cutoffs. Applying a window tapers the edges
    # of each end of the chunk down to zero.
    data = data * cached_hanning(len(data))

    # Apply FFT - real data
    fourier = fft.rfft(data)

    # Remove last element in array to make it the same size as chunk_size
    fourier = delete(fourier, len(fourier) - 1)

    # Calculate the power spectrum
    power = npabs(fourier) ** 2

    matrix = zeros(num_bins, dtype='float64')
    for pin in range(num_bins):
        # take the log10 of the resulting sum to approximate how human ears
        # perceive sound levels

        # Get the power array index corresponding to a particular frequency.
        idx1 = int(chunk_size * frequency_limits[pin][0] / sample_rate)
        idx2 = int(chunk_size * frequency_limits[pin][1] / sample_rate)

        # if index1 is the same as index2 the value is an invalid value
        # we can fix this by incrementing index2 by 1, This is a temporary fix
        # for RuntimeWarning: invalid value encountered in double_scalars
        # generated while calculating the standard deviation.  This warning
        # results in some channels not lighting up during playback.
        if idx1 == idx2:
            idx2 += 1

        npsums = npsum(power[idx1:idx2:1])

        # if the sum is 0 lets not take log10, just use 0
        # eliminates RuntimeWarning: divide by zero encountered in log10, does not insert -inf
        if npsums == 0:
            matrix[pin] = 0
        else:
            matrix[pin] = log10(npsums)

    return matrix


plugin = SpectrumAnalyzerPlugin
