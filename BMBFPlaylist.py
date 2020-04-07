from BMBFSongList import BMBFSongList


class BMBFPlaylist(object):
    def __init__(self, id, name, song_list, cover_image_bytes, is_cover_loaded):
        self.id = id
        self.name = name
        self.song_list = song_list
        self.cover_image_bytes = cover_image_bytes
        self.is_cover_loaded = is_cover_loaded

    @classmethod
    def load(cls, data):
        return cls(
           data['PlaylistID'],
           data['PlaylistName'],
           BMBFSongList.load(data['SongList']),
           data['CoverImageBytes'],
           data['IsCoverLoaded']
        )

    @classmethod
    def dump(cls, data):
        return {
            'PlaylistID': data.id,
            'PlaylistName': data.name,
            'SongList': BMBFSongList.dump(data.song_list),
            'CoverImageBytes': data.cover_image_bytes,
            'IsCoverLoaded': data.is_cover_loaded,
        }

    def get_song_authors(self):
        return self.song_list.get_song_authors()

    def get_song_list(self):
        return self.song_list

    def add_song(self, song):
        self.song_list.add_song(song)
