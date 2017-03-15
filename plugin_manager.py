import imp
import os
import json
import time
from config_loader import config_loader


class PluginManager:

    """Service for switching between plugins for Twilight"""
    def __init__(self):
        self.loaded_plugins = []
        self.blocked = {}
        self.config = config_loader.load_config('twilight')

    def getAvailablePlugins(self):
        available_plugins = {}
        location = "." + self.config["PLUGINS_FOLDER"]
        for plugin_folder in os.listdir(location):
            plugin_files = os.listdir(location+plugin_folder)
            if "__init__.py" in plugin_files and "config.json" in plugin_files:
                try:
                    config_json = json.loads(open(location+plugin_folder+"/config.json").read())
                    available_plugins[plugin_folder] = {
                        "name": plugin_folder,
                        "path": location+plugin_folder+"/__init__.py",
                        "priority": config_json["priority"],
                        "persistent": config_json["persistent"]
                    }
                except KeyError:
                    # config.json not correctly formatted
                    pass
            else:
                # incorrectly formatted plugin
                pass
        return available_plugins

    def loadPlugin(self, plugin_name):
        plugins = self.getAvailablePlugins()
        if plugin_name in plugins and plugin_name not in self.blocked:
            plugin_obj = {
                "name": plugin_name,
                "path": plugins[plugin_name]["path"],
                "priority": plugins[plugin_name]["priority"],
                "persistent": plugins[plugin_name]["persistent"]
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

    def getNextPlugin(self):
        for plugin in self.loaded_plugins:
            module = imp.load_source("__init__", plugin["path"])
            if module.ready():
                if not plugin["persistent"]:
                    self.loaded_plugins.remove(plugin)
                    del self.blocked[plugin["name"]]  # allow this plugin to be re-added
                return module
        return None

    def start(self):
        current_module = None  # TODO: replace with default module
        current_plugin = None
        while True:
            current_time = time.time()
            next_module = self.getNextPlugin()
            if next_module and not next_module == current_module:
                current_module = next_module
                current_plugin = current_module.Plugin()
            while time.time() < current_time + self.config["PLUGIN_CYCLE_LENGTH"]:
                current_plugin.getNextFrame()
                time.sleep(0.1)


if __name__ == "__main__":
    manager = PluginManager()
    manager.loadPlugin("mood")
    manager.loadPlugin("epilepsy")
    manager.start()
