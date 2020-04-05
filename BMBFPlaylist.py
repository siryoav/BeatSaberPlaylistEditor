from BMBFSongList import BMBFSongList


class BMBFPlaylist(object):
    def __init__(self, data):
        self.id = data['PlaylistID']
        self.name = data['PlaylistName']
        self.song_list = BMBFSongList(data['SongList'])
        self.cover_image_bytes = data['CoverImageBytes']
        self.is_cover_loaded = data['IsCoverLoaded']

    def get_song_authors(self):
        return self.song_list.get_song_authors()