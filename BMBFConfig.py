from BMBFPlaylists import BMBFPlaylists


class BMBFConfig(object):
    def __init__(self, data):
        self.playlists = BMBFPlaylists(data['Playlists'])
        self.saber = data['Saber']
        self.left_color = data['LeftColor']
        self.right_color = data['RightColor']
        self.text_changes = data['TextChanges']

    def get_song_authors(self):
        return self.playlists.get_song_authors()
