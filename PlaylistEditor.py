import bisect
import json
import re
from collections import OrderedDict

import yaml

from BMBFConfigFile import BMBFConfigFile
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

    @staticmethod
    def normalize_song_author(song_author):
        return PlaylistEditor.remove_non_alphabet.sub('', song_author.lower())

    def print_song_authors(self):
        song_authors_set = self.config_file.get_song_authors()

        song_authors_set = set([
            self.transform_song_author(song_author)
            for song_author
            in song_authors_set
        ])

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

        return song_author_guesses

    def order_playlists(self):
        song_authors_set = self.config_file.get_song_authors()

        song_authors_dict = {
            song_author: self.transform_song_author(song_author)
            for song_author
            in song_authors_set
        }
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
                    self.add_safe_to_playlists(new_playlists, EditorConfig().config['ForcedSongAuthor'][song.id], song)
                    continue
                if self.args.g:
                    song_author_guesses = self.song_author_guesser(song, normalized_song_authors)
                    if len(song_author_guesses) == 1:
                        self.add_safe_to_playlists(new_playlists, song_author_guesses.pop(), song)
                        continue
                if song.song_author_name not in song_authors_dict:
                    if self.args.g:
                        song_author_guesses = self.song_author_guesser(song, normalized_song_authors)
                        if len(song_author_guesses) == 1:
                            self.add_safe_to_playlists(new_playlists, song_author_guesses.pop(), song)
                            continue
                    self.add_safe_to_playlists(new_playlists, 'Unknown', song)
                    continue
                self.add_safe_to_playlists(new_playlists, song_authors_dict[song.song_author_name], song)
        return new_pre_defined_playlists, new_playlists

    def print_playlists(self):
        new_pre_defined_playlists, new_playlists = self.order_playlists()
        print(ordered_dump(new_pre_defined_playlists, Dumper=yaml.SafeDumper))
        print(ordered_dump(new_playlists, Dumper=yaml.SafeDumper))

    def print_new_config_file(self):
        new_pre_defined_playlists, new_playlists = self.order_playlists()
        self.config_file.set_new_playlists(new_pre_defined_playlists, new_playlists)
        print(self.config_file.dump())
