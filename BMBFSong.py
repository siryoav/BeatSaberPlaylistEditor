class BMBFSong(object):
    def __init__(self, data):
        self.id = data['SongID']
        self.name = data['SongName']
        self.sub_name = data['SongSubName']
        self.song_author_name = data['SongAuthorName']
        self.level_author_name = data['LevelAuthorName']
        self.custom_song_path = data['CustomSongPath']

    def get_song_author(self):
        return self.song_author_name
