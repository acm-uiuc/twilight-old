from plugin_manager import PluginManager


def main():
    manager = PluginManager()
    manager.load_plugin("spectrum_analyzer")
    manager.load_plugin("mood")
    manager.load_plugin("epilepsy")
    manager.start()


if __name__ == "__main__":
    main()
