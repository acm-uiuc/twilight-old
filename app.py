from plugin_manager import PluginManager


def main():
    manager = PluginManager()
    manager.loadPlugin("mood")
    manager.loadPlugin("epilepsy")
    manager.start()


if __name__ == "__main__":
    main()
