import hashlib
import json

from BMBFPlaylist import BMBFPlaylist
from BMBFSongList import BMBFSongList
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

    id_separator = '#@#'

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

    @classmethod
    def dump(cls, data):
        return [
            BMBFPlaylist.dump(playlist)
            for playlist
            in data.playlists
        ]

    def add_playlist(self, playlist):
        self.playlists.append(playlist)

    def get_playlist_index(self, id):
        for index, playlist in enumerate(self.playlists):
            if playlist.id == id:
                return index
        return -1

    def get_playlist(self, id):
        index = self.get_playlist_index(id)
        if index > -1:
            return self.playlists[index]
        return None

    def get_song_authors(self, playlist_filter):
        song_authors = set()
        [
            song_authors.add(song_author)
            for playlist
            in filter(playlist_filter, self.playlists)
            for song_author
            in playlist.get_song_authors()
         ]
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

    def get_new_playlists(self, new_pre_defined_playlists, new_playlists, cover_image):
        playlists_res = BMBFPlaylists()
        sha1 = hashlib.sha1()
        sha1.update(json.dumps(new_pre_defined_playlists, default=lambda o: o.__dict__).encode())
        sha1.update(json.dumps(new_playlists, default=lambda o: o.__dict__).encode())
        postfix = BMBFPlaylists.id_separator + sha1.hexdigest()

        # Insert default playlists
        for playlist_id in BMBFPlaylists.default_playlists:
            playlists_res.add_playlist(self.get_playlist(playlist_id))

        # Insert predefined playlists
        for playlist_id, songs in new_pre_defined_playlists.items():
            new_song_list = BMBFSongList()
            for song in songs:
                new_song_list.add_song(song)
            new_playlist = BMBFPlaylist(
                playlist_id + postfix,  # explanation about postfix in README
                playlist_id,
                new_song_list,
                None,  # defaults I saw in real configurations
                True,  # defaults I saw in real configurations
            )
            if cover_image:
                new_playlist.create_cover_image()
            playlists_res.add_playlist(new_playlist)

        # Insert rest of new playlists
        for playlist_id in sorted(new_playlists.keys()):
            songs = new_playlists[playlist_id]
            new_song_list = BMBFSongList()
            for song in songs:
                new_song_list.add_song(song)
            new_playlist = BMBFPlaylist(
                playlist_id + postfix,   # explanation about postfix in README
                playlist_id,
                new_song_list,
                None,  # defaults I saw in real configurations
                True,  # defaults I saw in real configurations
            )
            if cover_image:
                new_playlist.create_cover_image()
            playlists_res.add_playlist(new_playlist)

        ###########################################

        song_ids_in_playlists_res = {
            song.id
            for playlist
            in playlists_res.playlists
            for song
            in playlist.get_song_list().get_songs()
        }

        # Add songs from existing playlists with the same id as new playlists
        for playlist in self.playlists:
            if playlist.id in BMBFPlaylists.default_playlists:
                continue
            playlist_id = playlist.id
            if BMBFPlaylists.id_separator in playlist_id:
                playlist_id = playlist_id.split(BMBFPlaylists.id_separator)[0]
            playlist_in_playlists_res = playlists_res.get_playlist(playlist_id + postfix)
            if playlist_in_playlists_res is None:
                continue
            for song in playlist.get_song_list().get_songs():
                if song.id in song_ids_in_playlists_res:
                    continue
                playlist_in_playlists_res.add_song(song)

        # Add songs from existing playlists that did not get into the new playlists
        for playlist in self.playlists:
            if playlist.id in BMBFPlaylists.default_playlists:
                continue
            remaining_songs = []
            for song in playlist.get_song_list().get_songs():
                if song.id not in song_ids_in_playlists_res:
                    remaining_songs.append(song)
            if len(remaining_songs) > 0:
                new_song_list = BMBFSongList()
                for song in remaining_songs:
                    new_song_list.add_song(song)
                playlist_id = playlist.id
                if BMBFPlaylists.id_separator in playlist_id:
                    playlist_id = playlist_id.split(BMBFPlaylists.id_separator)[0]
                new_playlist = BMBFPlaylist(
                    playlist_id + postfix,
                    playlist.name,
                    new_song_list,
                    playlist.cover_image_bytes,
                    playlist.is_cover_loaded,
                )
                playlists_res.add_playlist(new_playlist)

        # Insert custom_playlist if missing
        if playlists_res.get_playlist(BMBFPlaylists.custom_playlist) is None:
            old_custom_playlist = self.get_playlist(BMBFPlaylists.custom_playlist)
            if old_custom_playlist is None:
                new_song_list = BMBFSongList()
                new_custom_playlist = BMBFPlaylist(
                    BMBFPlaylists.custom_playlist,
                    BMBFPlaylists.custom_playlist,
                    new_song_list,
                    None,  # defaults I saw in real configurations
                    True,  # defaults I saw in real configurations
                )
                playlists_res.add_playlist(new_custom_playlist)
            else:
                new_song_list = BMBFSongList()
                new_custom_playlist = BMBFPlaylist(
                    BMBFPlaylists.custom_playlist,
                    old_custom_playlist.name,
                    new_song_list,  # if missing, new playlist must be empty, because all of it's songs were handled
                    old_custom_playlist.cover_image_bytes,
                    old_custom_playlist.is_cover_loaded
                )
                playlists_res.add_playlist(new_custom_playlist)

        return playlists_res
