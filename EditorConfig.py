import os
import yaml

from Singleton import Singleton

config_file_path = 'config.yaml'
default_config = '''
PreDefinedPlaylists: []
PreDefinedSongAuthors: []
SongAuthorMap: {}
'''


class EditorConfig(object, metaclass=Singleton):
    def __init__(self):
        if os.path.exists(config_file_path):
            with open(config_file_path, 'r') as f:
                self.config = yaml.load(f)
        else:
            self.config = yaml.load(default_config)

    def save(self):
        with open(config_file_path, 'w') as f:
            yaml.dump(self.config, f)
