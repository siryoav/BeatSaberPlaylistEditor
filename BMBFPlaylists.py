from BMBFPlaylist import BMBFPlaylist
from EditorConfig import EditorConfig


class BMBFPlaylists(object):
    default_playlists = [
        'OstVol1',
        'OstVol2',
        'OstVol3',
        'Extras',
        'Camellia',
    ]
    custom_playlist = 'CustomSongs'
    
    def __init__(self, data):
        self.playlists = []
        self.song_authors = set()
        [self.add_playlist(playlist_data)
         for playlist_data
         in data]
        [self.song_authors.add(song_author)
         for playlist
         in self.playlists
         for song_author
         in playlist.get_song_authors()
         if playlist.id not in BMBFPlaylists.default_playlists]
        [self.song_authors.add(song_author)
         for song_author
         in EditorConfig().config['PreDefinedSongAuthors']]
        self.song_authors.remove('')

    def add_playlist(self, playlist_data):
        self.playlists.append(BMBFPlaylist(playlist_data))

    def get_song_authors(self):
        return self.song_authors
