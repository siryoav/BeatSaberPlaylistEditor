import bisect
import json
import re
import string
from collections import OrderedDict

import yaml

from ADBClient import ADBClient
from BMBFConfigFile import BMBFConfigFile
from BMBFPlaylists import BMBFPlaylists
from EditorConfig import EditorConfig


def ordered_dump(data, stream=None, Dumper=yaml.Dumper, **kwds):
    class OrderedDumper(Dumper):
        pass

    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            data.items())

    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    return yaml.dump(data, stream, OrderedDumper, **kwds)


class PlaylistEditor(object):
    def __init__(self, args):
        self.args = args
        self.reversed_song_author_map = {value: key
                                         for key
                                         in EditorConfig().config['SongAuthorMap']
                                         for value
                                         in EditorConfig().config['SongAuthorMap'][key]}
        self.normalized_reversed_song_author_map = {PlaylistEditor.normalize_song_author(value): key
                                                    for key
                                                    in EditorConfig().config['SongAuthorMap']
                                                    for value
                                                    in EditorConfig().config['SongAuthorMap'][key]}

        config_file_path = args.file

        with open(config_file_path, 'rb') as f:
            data = json.load(f)
            self.config_file = BMBFConfigFile.load(data)

    @staticmethod
    def correct_first_letter(m):
        """process regular expression match groups for word upper-casing problem"""
        return m.group(1) + m.group(2).upper()

    def transform_song_author(self, song_author):
        if self.args.c:
            song_author = re.sub(r"(^|\s)(\S)", PlaylistEditor.correct_first_letter, song_author)
        if self.args.s:
            song_author = song_author.strip()

        song_author = song_author if song_author not in self.reversed_song_author_map else \
            self.reversed_song_author_map[song_author]

        return song_author

    remove_non_alphabet = re.compile('[^a-zA-Z]')

    def get_playlist_filter(self):
        playlist_id = BMBFPlaylists.custom_playlist if not self.args.all_playlists else None
        playlist_name = self.args.playlist
        if playlist_id is None and playlist_name is None:  # All the lists (no touching the default ones)
            return lambda playlist: playlist.id not in BMBFPlaylists.default_playlists
        elif playlist_name is None:
            return lambda playlist: playlist.id == playlist_id
        else:
            return lambda playlist: playlist.name == playlist_name

    def get_song_authors(self):
        return self.config_file.get_song_authors(self.get_playlist_filter())

    @staticmethod
    def normalize_song_author(song_author):
        return PlaylistEditor.remove_non_alphabet.sub('', song_author.lower())

    def print_song_authors(self):
        song_authors_set = self.get_song_authors()

        song_authors_set = set(self.transform_song_authors_set(song_authors_set).values())

        song_authors = sorted(list(song_authors_set))
        print('\n'.join(song_authors))

    def add_safe_to_playlists(self, playlists, list_name, song):
        if list_name not in playlists:
            playlists[list_name] = []
        if self.args.song_name or self.args.song_id:
            if not self.args.song_name:
                song_data = song.id
            elif not self.args.song_id:
                song_data = song.name
            else:
                song_data = ('', '- {} # {} @ {}'.format(song.id, song.name, song.level_author_name))
        else:
            song_data = song
        bisect.insort(playlists[list_name], song_data)

    excluded_guesses = EditorConfig().config['ExcludedGuesses']

    def song_author_guesser(self, song, normalized_song_authors):
        song_author_guesses = set()
        for song_author, normalized_song_author in normalized_song_authors.items():
            if normalized_song_author in PlaylistEditor.excluded_guesses:
                continue
            if normalized_song_author in PlaylistEditor.normalize_song_author(song.name):
                song_author_guesses.add(song_author)
            if normalized_song_author in PlaylistEditor.normalize_song_author(song.level_author_name):
                song_author_guesses.add(song_author)

        for normalized_song_author, song_author in self.normalized_reversed_song_author_map.items():
            if normalized_song_author in PlaylistEditor.excluded_guesses:
                continue
            if normalized_song_author in PlaylistEditor.normalize_song_author(song.name):
                song_author_guesses.add(song_author)
            if normalized_song_author in PlaylistEditor.normalize_song_author(song.level_author_name):
                song_author_guesses.add(song_author)

        for song_author in song_author_guesses:
            found = True
            for other_song_author in song_author_guesses:
                if PlaylistEditor.normalize_song_author(song_author) not in PlaylistEditor.normalize_song_author(other_song_author):
                    found = False
            if found:
                song_author_guesses = {song_author}
                break
        return song_author_guesses

    def transform_song_authors_set(self, song_authors_set):
        song_authors_dict = {
            song_author: self.transform_song_author(song_author)
            for song_author
            in song_authors_set
        }

        if self.args.fix_the or self.args.r:
            complete_song_authors_set = song_authors_set.union(set(EditorConfig().config['PreDefinedSongAuthors'])).\
                union(set(EditorConfig().config['ForcedSongAuthor'].values()))
            for song_author in complete_song_authors_set:
                if self.args.fix_the:
                    if "the " in song_author[:4] or "The " in song_author[:4]:
                        song_authors_dict[song_author[4:]] = song_author
                if self.args.r:
                    if song_author.isupper() and string.capwords(song_author) in complete_song_authors_set:
                        song_authors_dict[song_author] = string.capwords(song_author)

        return song_authors_dict

    @staticmethod
    def resolve(song_author, song_authors_dict):
        i = 10  # limit search to avoid cycles
        while song_author in song_authors_dict and i > 0:
            song_author = song_authors_dict[song_author]
            i -= 1
        return song_author

    def order_playlists(self):
        song_authors_set = self.get_song_authors()

        song_authors_dict = self.transform_song_authors_set(song_authors_set)

        normalized_song_authors = {
            song_author: PlaylistEditor.normalize_song_author(song_author)
            for song_author
            in set(song_authors_dict.values())
            if len(PlaylistEditor.normalize_song_author(song_author)) >= 3
        }

        new_playlists = {
            'Unknown': [],
        }
        new_pre_defined_playlists = OrderedDict()
        for pre_defined_playlist in EditorConfig().config['PreDefinedPlaylists']:
            new_pre_defined_playlists[pre_defined_playlist] = []
        old_playlists = self.config_file.get_playlists()
        for old_playlist in old_playlists:
            song_list = old_playlist.get_song_list()
            for song in song_list.get_songs():
                found = False
                for pre_defined_playlist in EditorConfig().config['PreDefinedPlaylists']:
                    if song.id in EditorConfig().config['PreDefinedPlaylists'][pre_defined_playlist]:
                        self.add_safe_to_playlists(new_pre_defined_playlists, pre_defined_playlist, song)
                        found = True
                        break
                if found:
                    continue
                if song.id in EditorConfig().config['ForcedSongAuthor']:
                    self.add_safe_to_playlists(
                        new_playlists,
                        PlaylistEditor.resolve(EditorConfig().config['ForcedSongAuthor'][song.id], song_authors_dict),
                        song,
                    )
                    continue
                if self.args.g:
                    song_author_guesses = self.song_author_guesser(song, normalized_song_authors)
                    if len(song_author_guesses) == 1:
                        self.add_safe_to_playlists(
                            new_playlists,
                            PlaylistEditor.resolve(song_author_guesses.pop(), song_authors_dict),
                            song,
                        )
                        continue
                if song.song_author_name not in song_authors_dict:
                    if self.args.g:
                        song_author_guesses = self.song_author_guesser(song, normalized_song_authors)
                        if len(song_author_guesses) == 1:
                            self.add_safe_to_playlists(new_playlists, song_author_guesses.pop(), song)
                            continue
                    self.add_safe_to_playlists(new_playlists, 'Unknown', song)
                    continue
                self.add_safe_to_playlists(
                    new_playlists,
                    PlaylistEditor.resolve(song_authors_dict[song.song_author_name], song_authors_dict),
                    song,
                )
        if len(new_playlists['Unknown']) == 0:
            del new_playlists['Unknown']
        return new_pre_defined_playlists, new_playlists

    def print_playlists(self):
        new_pre_defined_playlists, new_playlists = self.order_playlists()
        print(ordered_dump(new_pre_defined_playlists, Dumper=yaml.SafeDumper))
        print(ordered_dump(new_playlists, Dumper=yaml.SafeDumper))

    def print_new_config_file(self):
        new_pre_defined_playlists, new_playlists = self.order_playlists()
        self.config_file.get_new_playlists(new_pre_defined_playlists, new_playlists, self.args.cover_image)
        print(json.dumps(BMBFConfigFile.dump(self.config_file), indent=4))

    def print_count(self):
        new_pre_defined_playlists, new_playlists = self.order_playlists()
        playlist_count = len(new_pre_defined_playlists) + len(new_playlists)
        song_count = sum([
            len(songs)
            for songs
            in list(new_pre_defined_playlists.values()) + list(new_playlists.values())
        ])
        print('Playlists: {}'.format(playlist_count))
        print('Songs: {}'.format(song_count))

    def get_songs(self):
        return self.config_file.get_songs(self.get_playlist_filter())

    def auto_get_bookmarked_to_trash(self):
        if self.args.auto_trash_source is not None:
            with open(self.args.auto_trash_source) as f:
                player_data = json.load(f)
        else:
            adb = ADBClient()
            player_data = adb.get_player_data()

        favorites_level_ids = set(player_data['localPlayers'][0]['favoritesLevelIds'])

        songs = self.get_songs()
        songs_dict = {
            song.id: song
            for song
            in songs
        }
        songs_ids = set(songs_dict.keys())

        trash_config = EditorConfig().config['Trash']
        if self.args.favorite_whitelist:
            new_trash = songs_ids - favorites_level_ids
        else:
            new_trash = favorites_level_ids
        if self.args.trash_overwrite:
            trash_config.clear()
            final_trash = new_trash
        else:
            old_trash = set(trash_config)
            final_trash = new_trash - old_trash

        for song_id in final_trash:
            trash_config.append(song_id)
            if song_id in songs_dict:
                trash_config.yaml_add_eol_comment(songs_dict[song_id].name, len(trash_config) - 1)

        # cleaning trash from configuration
        final_trash_set = set(trash_config)

        pre_defined_playlists = EditorConfig().config['PreDefinedPlaylists']
        for pre_defined_playlist in pre_defined_playlists:
            pre_defined_playlist_set = set(pre_defined_playlist)
            songs_to_delete = pre_defined_playlist_set.intersection(final_trash_set)
            for song_to_delete in songs_to_delete:
                pre_defined_playlist.remove(song_to_delete)

        forced_song_author = EditorConfig().config['ForcedSongAuthor']
        for song_to_delete in final_trash_set:
            if song_to_delete in forced_song_author:
                del forced_song_author[song_to_delete]

        EditorConfig().print()

