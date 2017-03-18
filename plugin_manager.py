import importlib.util
import os
import time
import twilight
from config_loader import config_loader

PLUGIN_FILE_NAME = 'plugins.yml'


class PluginManager:

    """Service for switching between plugins for Twilight"""
    def __init__(self):

        default_config = {
            # Plugin and filter data, priority in range 0-9 inclusive, persistent only for plugins
            'PLUGINS': {},
            'FILTERS': {}
        }

        config_loader.register_config('plugin', PLUGIN_FILE_NAME, default_config)
        self.plugins = config_loader.load_config('plugin')
        self.loaded_plugins = []
        self.loaded_filters = []
        self.blocked = {}  # Dictionary to prevent multiple additions of same plugin/filter to queue
        self.config = config_loader.load_config('twilight')

    def get_files(self, location):
        """Helper function to retrieve plugin and filter scripts"""
        files = []
        for plugin_folder in os.listdir(location):
            plugin_files = os.listdir(location+plugin_folder)
            if "__init__.py" in plugin_files:
                files.append(plugin_folder)
        return files

    def get_available_plugins(self):
        """List all plugins located in the folder given in the config PLUGINS_FOLDER"""
        available_plugins = {}
        location = "." + self.config["PLUGINS_FOLDER"]
        for plugin_folder in self.get_files(location):
            if plugin_folder in self.plugins["PLUGINS"]:
                available_plugins[plugin_folder] = {
                    "name": plugin_folder,
                    "path": location+plugin_folder+"/__init__.py",
                    "priority": self.plugins["PLUGINS"][plugin_folder]['priority'],
                    "persistent": self.plugins["PLUGINS"][plugin_folder]['persistent']
                }
            else:
                available_plugins[plugin_folder] = {
                    "name": plugin_folder,
                    "path": location+plugin_folder+"/__init__.py",
                    "priority": 0,
                    "persistent": False
                }
        return available_plugins

    def get_available_filters(self):
        """List all filters located in the folder given in the config FILTERS_FOLDER"""
        available_filters = {}
        location = "." + self.config["FILTERS_FOLDER"]
        for filter_folder in self.get_files(location):
            if filter_folder in self.plugins["FILTERS"]:
                available_filters[filter_folder] = {
                    "name": filter_folder,
                    "path": location+filter_folder+"/__init__.py",
                    "priority": self.plugins["FILTERS"][filter_folder]["priority"]
                }
            else:
                available_filters[filter_folder] = {
                    "name": filter_folder,
                    "path": location+filter_folder+"/__init__.py",
                    "priority": 0
                }
        return available_filters

    def load_plugin(self, plugin_name):
        """Loads plugin named plugin_name from plugins folder. Returns 0 if successful, else 1"""
        plugins = self.get_available_plugins()
        if plugin_name in plugins and plugin_name not in self.blocked:
            plugin_obj = {
                "name": plugin_name,
                "path": plugins[plugin_name]["path"],
                "priority": plugins[plugin_name]["priority"],
                "persistent": plugins[plugin_name]["persistent"],
            }
            self.blocked[plugin_name] = True
            for index in range(len(self.loaded_plugins)):
                if self.loaded_plugins[index]["priority"] < plugin_obj["priority"]:
                    self.loaded_plugins.insert(index, plugin_obj)
                    return 0
            self.loaded_plugins.append(plugin_obj)
            return 0
        return 1

    def load_filter(self, filter_name):
        """Loads filter named filter_name from filters folder. Returns 0 if successful, else 1"""
        filters = self.get_available_filters()
        if filter_name in filters and filter_name not in self.blocked:
            filter_obj = {
                "name": filter_name,
                "path": filters[filter_name]["path"],
                "priority": filters[filter_name]["priority"]
            }
            self.blocked[filter_name] = True
            for index in range(len(self.loaded_filters)):
                if self.loaded_filters[index]["priority"] < filter_obj["priority"]:
                    self.loaded_filters.insert(index, filter_obj)
                    return 0
            self.loaded_filters.append(filter_obj)
            return 0
        return 1

    def get_next_plugin(self):
        """Retrieve the next plugin from the queue or return error if queue is empty"""
        for plugin in self.loaded_plugins:
            if not plugin["persistent"]:
                self.loaded_plugins.remove(plugin)
                del self.blocked[plugin["name"]]  # allow this plugin to be re-added
            return plugin
        return None

    def start(self):
        """Begins cycling through plugins"""
        current_module = None  # TODO (warut-vijit): replace with default module
        current_plugin = None

        # Keep track of when we last displayed FPS.
        last_fps_display_time = time.time()

        while True:
            start_time = time.time()  # gets time when current plugin starts
            next_module = self.get_next_plugin()
            if next_module and not next_module == current_module:
                # Load the next plugin and give it the current panel layout
                current_module = next_module

                # Dynamically import Python module
                # http://stackoverflow.com/a/41595552
                spec = importlib.util.spec_from_file_location(next_module['name'], next_module['path'])
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                current_plugin = mod.plugin()

                current_plugin.setTileMatrix(twilight.interface.tile_matrix)
            # only raise error if nothing is playing and queue is empty
            elif not next_module and current_module is None:
                raise NotImplementedError

            # Reset FPS data since we're changing plugins
            twilight.interface.clear_fps_data()

            while time.time() < start_time + self.config["PLUGIN_CYCLE_LENGTH"]:
                # Wait for the plugin to be ready
                while not current_plugin.ready():
                    time.sleep(self.config['RATE_LIMIT_TIME']/1000.0)

                # Get and write the next frame
                tile_matrix = current_plugin.getNextFrame()

                # Apply filters to frame
                for current_filter in self.loaded_filters:
                    filter_class = imp.load_source("__init__", current_filter["path"]).filter()
                    tile_matrix = filter_class.applyToFrame(tile_matrix)

                for pixel in tile_matrix:
                    if isinstance(tile_matrix[pixel], tuple):
                        twilight.interface.set_unit_color(pixel, tile_matrix[pixel])
                    else:
                        twilight.interface.write_to_unit(pixel, tile_matrix[pixel])

                if time.time() - last_fps_display_time > 1.0:
                    generated_fps = twilight.interface.get_generated_fps()
                    rendered_fps = twilight.interface.get_rendered_fps()
                    print('FPS (generated/rendered):')

                    for unit_id in generated_fps:
                        print('%s: %f/%f FPS' % (unit_id, generated_fps[unit_id], rendered_fps[unit_id]))
                    last_fps_display_time = time.time()
