from BMBFSong import BMBFSong


class BMBFSongList(object):
    def __init__(self, data):
        self.songs = []
        self.song_ids = set()
        [self.add_song(song_data) for song_data in data]

    def add_song(self, data):
        song = BMBFSong(data)
        if song.id not in self.song_ids:
            self.song_ids.add(song.id)
            self.songs.append(song)

    def get_song_authors(self):
        return [song.get_song_author()
                for song
                in self.songs]
