import os
import yaml

from Singleton import Singleton

config_file_path = 'config.yml'


class EditorConfig(object, metaclass=Singleton):
    def __init__(self):
        if os.path.exists(config_file_path):
            with open(config_file_path, 'r') as f:
                config = yaml.load(f)
        else:
            config = yaml.load('')
