class BMBFSong(object):
    def __init__(self, id, name, sub_name, song_author_name, level_author_name, custom_song_path):
        self.id = id
        self.name = name
        self.sub_name = sub_name
        self.song_author_name = song_author_name
        self.level_author_name = level_author_name
        self.custom_song_path = custom_song_path

    @classmethod
    def load(cls, data):
        return cls(
            data['SongID'],
            data['SongName'],
            data['SongSubName'],
            data['SongAuthorName'],
            data['LevelAuthorName'],
            data['CustomSongPath'],
        )

    def get_song_author(self):
        return self.song_author_name
