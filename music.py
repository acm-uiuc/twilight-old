#!/usr/bin/env python

import atexit
import os
import sys
import alsaaudio as aa

import colorsys
import audioread
import numpy as np

import serial

import fft

import queue
import threading

_MIN_FREQUENCY = 20
_MAX_FREQUENCY = 8000

_CUSTOM_CHANNEL_FREQUENCIES = 0
_CUSTOM_CHANNEL_MAPPING = 0

CHUNK_SIZE = 2048

NUM_LEDS = 140
NUM_CHANNELS = NUM_LEDS // 2

MAX_BRIGHTNESS = 1.0

UPDATE_HZ = 24

serial_port = None
serial_port_2 = None
serial_port_3 = None

light_queue = queue.Queue()
light_queue_2 = queue.Queue()
light_queue_3 = queue.Queue()


def end_early():
    # hc.clean_up()
    serial_port.close()
    serial_port_2.close()
    serial_port_3.close()
    pass


atexit.register(end_early)


def update_lights_helper(my_light_queue, my_serial_port):
    while True:
        lights = my_light_queue.get()
        while not my_light_queue.empty():
            lights = my_light_queue.get()
        my_serial_port.write(lights)


def calculate_channel_frequency(min_frequency, max_frequency):

    channel_length = NUM_CHANNELS

    print("Calculating frequencies for %d channels." % channel_length)
    octaves = (np.log(max_frequency / min_frequency)) / np.log(2)
    print("octaves in selected frequency range ... %s" % octaves)
    octaves_per_channel = octaves / channel_length
    frequency_limits = []
    frequency_store = []

    frequency_limits.append(min_frequency)

    for pin in range(1, NUM_CHANNELS + 1):
        frequency_limits.append(frequency_limits[-1] * 10 ** (0.3 * octaves_per_channel))
    for pin in range(0, channel_length):
        frequency_store.append((frequency_limits[pin], frequency_limits[pin + 1]))
        print("channel %d is %6.2f to %6.2f " % (pin, frequency_limits[pin],
                                                 frequency_limits[pin + 1]))

    return frequency_store


def update_lights(matrix, mean, std):
    """Update the state of all the lights

    Update the state of all the lights based upon the current
    frequency response matrix

    :param matrix: row of data from cache matrix
    :type matrix: list

    :param mean: standard mean of fft values
    :type mean: list

    :param std: standard deviation of fft values
    :type std: list
    """
    colors = [(0, 0, 0) for i in range(NUM_LEDS)]
    colors_2 = [(0, 0, 0) for i in range(NUM_LEDS)]
    colors_3 = [(0, 0, 0) for i in range(NUM_LEDS)]

    for pin in range(0, NUM_CHANNELS):
        hue = matrix[pin] - mean[pin] + 0.5 * std[pin]
        hue /= 1.25 * std[pin]
        hue = int(360.0 * hue)

        red, green, blue = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        red = int(255 * red)
        green = int(255 * green)
        blue = int(255 * blue)

        if red >= 255:
            red = 254
        elif red < 0:
            red = 0

        if green >= 255:
            green = 254
        elif green < 0:
            green = 0

        if blue >= 255:
            blue = 254
        elif blue < 0:
            blue = 0

        colors[pin] = (red, green, blue)
        colors_2[pin] = (red, green, blue)
        colors_3[pin] = (red, green, blue)

        colors[pin + NUM_LEDS // 2] = (red, green, blue)
        colors_2[pin + NUM_LEDS // 2] = (red, green, blue)
        colors_3[pin + NUM_LEDS // 2] = (red, green, blue)

    light_queue.put(b'\xFF' + bytes(list(sum(colors, ()))))
    light_queue_2.put(b'\xFF' + bytes(list(sum(colors_2, ()))))
    light_queue_3.put(b'\xFF' + bytes(list(sum(colors_3, ()))))


def play_song(song_filename):

    # Initialize Lights
    # hc.initialize()

    # Ensure play_now is reset before beginning playback

    # Set up audio
    music_file = audioread.audio_open(song_filename)

    sample_rate = music_file.samplerate
    num_channels = music_file.channels
    output = aa.PCM(aa.PCM_PLAYBACK, aa.PCM_NORMAL)
    output.setchannels(num_channels)
    output.setrate(sample_rate)
    output.setformat(aa.PCM_FORMAT_S16_LE)
    output.setperiodsize(CHUNK_SIZE)

    print("Playing: " + song_filename + " (" + str(music_file.duration)
          + " sec)")

    # Output a bit about what we're about to play to the logs
    song_filename = os.path.abspath(song_filename)

    # The values 12 and 1.5 are good estimates for first time playing back
    # (i.e. before we have the actual mean and standard deviations
    # calculated for each channel).
    mean = [12.0 for _ in range(NUM_CHANNELS)]
    std = [1.5 for _ in range(NUM_CHANNELS)]

    # Process audio song_filename
    row = 0
    frequency_limits = calculate_channel_frequency(_MIN_FREQUENCY, _MAX_FREQUENCY)
    frames_played = 0
    update_rate = sample_rate / UPDATE_HZ
    last_update_spec = 0

    for data in music_file:
        output.write(data)

        # Control lights with cached timing values if they exist
        # No cache - Compute FFT in this chunk, and cache results
        matrix = fft.calculate_levels(data, CHUNK_SIZE, sample_rate, frequency_limits,
                                      NUM_CHANNELS)

        frames_played += len(data) / 4

        if last_update_spec + update_rate < frames_played:
            update_lights(matrix, mean, std)
            last_update_spec = frames_played

        # Read next chunk of data from music song_filename
        row += 1


if __name__ == "__main__":
    serial_port = serial.Serial('/dev/ttyACM0', 460800)
    serial_port_2 = serial.Serial('/dev/ttyACM1', 460800)
    serial_port_3 = serial.Serial('/dev/ttyACM4', 460800)
    t = threading.Thread(target=update_lights_helper, daemon=True, args=(light_queue, serial_port))
    t2 = threading.Thread(target=update_lights_helper, daemon=True, args=(light_queue_2, serial_port_2))
    t3 = threading.Thread(target=update_lights_helper, daemon=True, args=(light_queue_3, serial_port_3))
    t.start()
    t2.start()
    t3.start()
    light_queue.put(b'xFF' + b'x00' * 3 * NUM_LEDS)
    light_queue_2.put(b'xFF' + b'x00' * 3 * NUM_LEDS)
    light_queue_3.put(b'xFF' + b'x00' * 3 * NUM_LEDS)
    play_song(sys.argv[1])
