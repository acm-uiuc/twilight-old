import importlib.util
import os
import time
import twilight
import threading
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
        """Helper function to retrieve plugin and filter scripts. Returns array of possible plugins

        Args:
            location: the relative path where plugin or filter files are located
        """
        files = []
        for plugin_folder in os.listdir(location):
            plugin_files = os.listdir(location+plugin_folder)
            if "__init__.py" in plugin_files:
                files.append(plugin_folder)
        return files

    def get_available_plugins(self):
        """List all plugins located in the folder given in the config PLUGINS_FOLDER.
        Returns dict of plugin attributes. Throws ValueError if plugin not in plugins.yml
        """
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
                raise ValueError("{0} does not match any plugin stored in plugins.yml.".format(plugin_folder))
        return available_plugins

    def get_available_filters(self):
        """List all filters located in the folder given in the config FILTERS_FOLDER
        Returns dict of filter attributes. Throws ValueError if filter not in plugins.yml
        """
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
                raise ValueError("{0} does not match any filter stored in plugins.yml.".format(filter_folder))
        return available_filters
        # TODO: Reduce code duplication

    def load_plugin(self, plugin_name):
        """Loads plugin named plugin_name from plugins folder. Returns true if successful, else false"""
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
                    return True
            self.loaded_plugins.append(plugin_obj)
            return True
        return False

    def load_filter(self, filter_name):
        """Loads filter named filter_name from filters folder. Returns true if successful, else false"""
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
                    return True
            self.loaded_filters.append(filter_obj)
            return True
        return False
        # TODO: Reduce code duplication

    def load_next_plugin(self):
        """Retrieve the next plugin from the queue. Returns next plugin or None if queue is empty"""
        for plugin in self.loaded_plugins:
            if not plugin["persistent"]:
                self.loaded_plugins.remove(plugin)
                del self.blocked[plugin["name"]]  # allow this plugin to be re-added
            # Dynamically import Python module
            # http://stackoverflow.com/a/41595552
            spec = importlib.util.spec_from_file_location(plugin['name'], plugin['path'])
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            current_plugin = mod.plugin()
            return current_plugin
        return None

    def start(self):
        """Begins cycling through plugins"""
        player = PluginPlayerThread(self)
        player.run()


class PluginPlayerThread(threading.Thread):

    """Helper class for playing plugins in a separate thread from the manager"""
    def __init__(self, manager):
        threading.Thread.__init__(self)
        self.manager = manager
        self.plugin = None
        self.start_time = None
        self.last_fps_display_time = time.time()  # Keep track of when we last displayed FPS.

    def run(self):
        while True:
            if time.time() > self.start_time + self.manager.config["PLUGIN_CYCLE_LENGTH"]:
                next_plugin = self.manager.load_next_plugin()
                if next_plugin is None:
                    raise NotImplementedError
                if not self.plugin == next_plugin:
                    self.plugin = next_plugin
                    self.plugin.set_tile_matrix(twilight.interface.tile_matrix)
                    twilight.interface.clear_fps_data()
            # Wait for the plugin to be ready
            while not self.plugin.ready():
                time.sleep(self.manager.config['RATE_LIMIT_TIME']/1000.0)

            # Get and write the next frame
            tile_matrix = self.plugin.get_next_frame()

            # Apply filters to frame
            for current_filter in self.manager.loaded_filters:
                spec = importlib.util.spec_from_file_location(current_filter['name'], current_filter['path'])
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                filter_plugin = mod.filter_plugin()
                tile_matrix = filter_plugin.apply_to_frame(tile_matrix)
                if tile_matrix is None:  # filter dropped frame
                    break

            if tile_matrix is not None:
                for pixel in tile_matrix:
                    if isinstance(tile_matrix[pixel], tuple):
                        twilight.interface.set_unit_color(pixel, tile_matrix[pixel])
                    else:
                        twilight.interface.write_to_unit(pixel, tile_matrix[pixel])

            # Compute effective FPS
            if time.time() - self.last_fps_display_time > 1.0:
                generated_fps = twilight.interface.get_generated_fps()
                rendered_fps = twilight.interface.get_rendered_fps()
                print('FPS (generated/rendered):')

                for unit_id in generated_fps:
                    print('%s: %f/%f FPS' % (unit_id, generated_fps[unit_id], rendered_fps[unit_id]))
                self.last_fps_display_time = time.time()
