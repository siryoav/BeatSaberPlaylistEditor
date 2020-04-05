from BMBFConfig import BMBFConfig


class BMBFConfigFile(object):
    def __init__(self, data):
        self.is_committed = data['IsCommitted']
        self.config = BMBFConfig(data['Config'])
        self.sync_config = data['SyncConfig']
        self.beat_saber_version = data['BeatSaberVersion']

    def get_song_authors(self):
        return self.config.get_song_authors()

    def get_playlists(self):
        return self.config.get_playlists()
