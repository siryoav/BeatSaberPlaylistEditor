import json
import argparse
import re

from BMBFConfigFile import BMBFConfigFile
from EditorConfig import EditorConfig


def correct_first_letter(m):
    """process regular expression match groups for word upper-casing problem"""
    return m.group(1) + m.group(2).upper()


def transform_song_author(song_author, args, reversed_song_author_map):
    if args.c:
        song_author = re.sub(r"(^|\s)(\S)", correct_first_letter, song_author)
    if args.s:
        song_author = song_author.strip()

    song_author = song_author if song_author not in reversed_song_author_map else reversed_song_author_map[song_author]

    return song_author


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', action='store_true', help='Print song authors')
    parser.add_argument('-c', action='store_true', help='Capital letters in author\'s name')
    parser.add_argument('-s', action='store_true', help='Strip whitespaces from author\'s name')
    parser.add_argument('file', action='store', type=str, help='Config file path')
    args = parser.parse_args()

    config_file_path = args.file

    with open(config_file_path, 'rb') as f:
        data = json.load(f)
        config_file = BMBFConfigFile(data)

    reversed_song_author_map = {value: key
                                for key
                                in EditorConfig().config['SongAuthorMap']
                                for value
                                in EditorConfig().config['SongAuthorMap'][key]}

    if args.a:
        song_authors_set = config_file.get_song_authors()

        song_authors_set = set([
            transform_song_author(song_author, args, reversed_song_author_map)
            for song_author
            in song_authors_set
        ])

        song_authors = sorted(list(song_authors_set))
        print('\n'.join(song_authors))


if __name__ == '__main__':
    main()
