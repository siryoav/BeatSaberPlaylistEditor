from BMBFPlaylists import BMBFPlaylists


class BMBFConfig(object):
    def __init__(self, playlists, saber, left_color, right_color, text_changes):
        self.playlists = playlists
        self.saber = saber
        self.left_color = left_color
        self.right_color = right_color
        self.text_changes = text_changes

    @classmethod
    def load(cls, data):
        return cls(
            BMBFPlaylists.load(data['Playlists']),
            data['Saber'],
            data['LeftColor'],
            data['RightColor'],
            data['TextChanges'],
        )

    @classmethod
    def dump(cls, data):
        return {
            'Playlists': BMBFPlaylists.dump(data.playlists),
            'Saber': data.saber,
            'LeftColor': data.left_color,
            'RightColor': data.right_color,
            'TextChanges': data.text_changes,
        }

    def get_song_authors(self, playlist_id=BMBFPlaylists.custom_playlist):
        return self.playlists.get_song_authors(playlist_id)

    def get_playlists(self):
        return self.playlists.get_playlists()

    def get_new_playlists(self, new_pre_defined_playlists, new_playlists):
        self.playlists = self.playlists.get_new_playlists(new_pre_defined_playlists, new_playlists)
