from plugin_manager import PluginManager


def load_plugin(plugin_name):
    print(manager)

def main():
    manager = PluginManager()
    manager.load_plugin("spectrum_analyzer")
    manager.load_plugin("mood")
    manager.load_plugin("epilepsy")
    manager.start()


if __name__ == "__main__":
    main()
    load_plugin("hi")
