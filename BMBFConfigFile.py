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

    def get_song_authors(self, playlist_id=BMBFPlaylists.custom_playlist):
        return self.config.get_song_authors(playlist_id)

    def get_playlists(self):
        return self.config.get_playlists()

    def set_new_playlists(self, new_pre_defined_playlists, new_playlists):
        self.config.set_new_playlists(new_pre_defined_playlists, new_playlists)
