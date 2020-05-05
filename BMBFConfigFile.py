from BMBFConfig import BMBFConfig
from BMBFPlaylists import BMBFPlaylists


class BMBFConfigFile(object):
    def __init__(self, is_committed, config, sync_config, beat_saber_version):
        self.is_committed = is_committed
        self.config = config
        self.sync_config = sync_config
        self.beat_saber_version = beat_saber_version

    @classmethod
    def load(cls, data):
        return cls(
            data['IsCommitted'],
            BMBFConfig.load(data['Config']),
            data['SyncConfig'],
            data['BeatSaberVersion'],
        )

    @classmethod
    def dump(cls, data):
        return {
            'IsCommitted': data.is_committed,
            'Config': BMBFConfig.dump(data.config),
            'SyncConfig': data.sync_config,
            'BeatSaberVersion': data.beat_saber_version,
        }

    def get_song_authors(self, playlist_filter):
        return self.config.get_song_authors(playlist_filter)

    def get_playlists(self):
        return self.config.get_playlists()

    def get_new_playlists(self, new_pre_defined_playlists, new_playlists, cover_image):
        self.config.get_new_playlists(new_pre_defined_playlists, new_playlists, cover_image)

    def get_songs(self, playlist_filter):
        return self.config.get_songs(playlist_filter)
