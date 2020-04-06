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
    
    def __init__(self):
        self.playlists = []

    @classmethod
    def load(cls, data):
        playlists = cls()
        [
            playlists.add_playlist(BMBFPlaylist.load(playlist_data))
            for playlist_data
            in data
        ]
        return playlists

    def add_playlist(self, playlist):
        self.playlists.append(playlist)

    def get_song_authors(self, playlist_id=custom_playlist):
        song_authors = set()
        if playlist_id is None: # All the lists (no touching the default ones)
            [song_authors.add(song_author)
             for playlist
             in self.playlists
             for song_author
             in playlist.get_song_authors()
             if playlist.id not in BMBFPlaylists.default_playlists]
        else:
            [song_authors.add(song_author)
             for playlist
             in self.playlists
             for song_author
             in playlist.get_song_authors()
             if playlist.id == playlist_id]
        [song_authors.add(song_author)
         for song_author
         in EditorConfig().config['PreDefinedSongAuthors']]
        song_authors.remove('')
        return song_authors

    def get_playlists(self):
        return [playlist
                for playlist
                in self.playlists
                if playlist.id not in BMBFPlaylists.default_playlists]

    def set_new_playlists(self, new_pre_defined_playlists, new_playlists):
        song_id_to_playlist_id = {
            song.id: playlist.id
            for playlist
            in self.playlists
            for song
            in playlist.get_song_list().get_songs()
        }

