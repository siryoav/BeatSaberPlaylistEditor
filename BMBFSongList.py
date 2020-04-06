from BMBFSong import BMBFSong


class BMBFSongList(object):
    def __init__(self):
        self.songs = []
        self.song_ids = set()

    def add_song(self, song):
        if song.id not in self.song_ids:
            self.song_ids.add(song.id)
            self.songs.append(song)

    @classmethod
    def load(cls, data):
        song_list = cls()
        [
            song_list.add_song(BMBFSong.load(song_data))
            for song_data
            in data
        ]
        return song_list

    def get_song_authors(self):
        return [
            song.get_song_author()
            for song
            in self.songs
        ]

    def get_songs(self):
        return self.songs
