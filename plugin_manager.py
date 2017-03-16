import imp
import os
import time
import twilight
from config_loader import config_loader

PLUGIN_FILE_NAME = 'plugins.yml'


class PluginManager:

    """Service for switching between plugins for Twilight"""
    def __init__(self):

        default_config = {
            # Plugin data, priority in range 0-9 inclusive, persistent is boolean
            'PLUGINS': {}
        }

        config_loader.register_config('plugin', PLUGIN_FILE_NAME, default_config)
        self.plugins = config_loader.load_config('plugin')
        self.loaded_plugins = []
        self.blocked = {}  # Dictionary to prevent multiple additions of same plugin to queue
        self.config = config_loader.load_config('twilight')

    def get_available_plugins(self):
        """List all plugins located in the folder given in the config PLUGINS_FOLDER"""
        available_plugins = {}
        location = "." + self.config["PLUGINS_FOLDER"]
        for plugin_folder in os.listdir(location):
            plugin_files = os.listdir(location+plugin_folder)
            if "__init__.py" in plugin_files:
                try:
                    available_plugins[plugin_folder] = {
                        "name": plugin_folder,
                        "path": location+plugin_folder+"/__init__.py",
                        "priority": self.plugins["PLUGINS"][plugin_folder]['priority'],
                        "persistent": self.plugins["PLUGINS"][plugin_folder]['persistent']
                    }
                except KeyError:
                    # config.json not correctly formatted
                    pass
            else:
                # incorrectly formatted plugin
                pass
        return available_plugins

    def load_plugin(self, plugin_name):
        """Loads plugin named plugin_name from plugins folder"""
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
                    return
            self.loaded_plugins.append(plugin_obj)
        else:
            # plugin not found
            pass

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
        while True:
            start_time = time.time()  # gets time when current plugin starts
            next_module = self.get_next_plugin()
            if next_module and not next_module == current_module:
                # Load the next plugin and give it the current panel layout
                current_module = next_module
                current_plugin = imp.load_source("__init__", next_module["path"]).plugin()
                current_plugin.setTileMatrix(twilight.interface.tile_matrix)
            elif not next_module:
                raise NotImplementedError
            while time.time() < start_time + self.config["PLUGIN_CYCLE_LENGTH"]:
                # Wait for the plugin to be ready
                while not current_plugin.ready():
                    time.sleep(self.config['RATE_LIMIT_TIME']/1000.0)

                # Get and write the next frame
                tile_matrix = current_plugin.getNextFrame()
                for pixel in tile_matrix:
                    if isinstance(tile_matrix[pixel], tuple):
                        twilight.interface.set_unit_color(pixel, tile_matrix[pixel])
                    else:
                        twilight.interface.write_to_unit(pixel, tile_matrix[pixel])
