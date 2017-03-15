"""
Loads configurations from config file.
Please keep docstrings in sync with config.yaml
"""

import ruamel.yaml


class Config:

    def __init__(self):
        self.config_files = {}
        self.config_dicts = {}

    def register_config(self, config_name, filename, my_dict):
        if config_name not in self.config_files:
            self.config_files[config_name] = filename
            self.config_dicts[config_name] = my_dict

    def load_config(self, my_config_key=None):
        for config_key in self.config_files:
            filename = self.config_files[config_key]
            my_dict = self.config_dicts[config_key]
            """Read file and set values"""
            with open(filename, 'r') as f:
                config_dict = ruamel.yaml.load(f.read(), ruamel.yaml.RoundTripLoader)
                for key in config_dict:
                    if key not in my_dict:
                        raise RuntimeError("%s has not been declared in %s plugin" % (key, config_key))
                    my_dict[key] = config_dict[key]

        return self.config_dicts[my_config_key] if my_config_key else None


config_loader = Config()
