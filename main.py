import argparse

import yaml

import EditorConfig
from PlaylistEditor import PlaylistEditor


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', action='store_true', help='Print editor default config')
    parser.add_argument('-a', action='store_true', help='Print song authors')
    parser.add_argument('-c', action='store_true', help='Capital letters in author\'s name')
    parser.add_argument('-r', action='store_true', help='Transform all capital letters to only first if possible')
    parser.add_argument('-s', action='store_true', help='Strip whitespaces from author\'s name')
    parser.add_argument('-l', action='store_true', help='Print lists in yaml')
    parser.add_argument('-g', action='store_true', help='Try to guess song author if not available')
    parser.add_argument('--fix-the', action='store_true', help='Add "The" if possible')
    parser.add_argument('--song-name', action='store_true', help='Print song\'s name')
    parser.add_argument('--song-id', action='store_true', help='Print song\'s id')
    parser.add_argument('-p', action='store_true', help='Print new config file')
    parser.add_argument('--count', action='store_true', help='Print number of playlists and number of songs')
    parser.add_argument('--cover-image', action='store_true', help='Create cover image for playlists')
    parser.add_argument('--all-playlists', action='store_true', help='Read from all playlists')
    parser.add_argument('--auto-trash', action='store_true', help='Auto add items to your trash using ADB')
    parser.add_argument('--auto-trash-source', action='store', type=str, help='File path to get favorites from', default=None)
    parser.add_argument('--trash-overwrite', action='store_true', help='Auto add items to your trash using ADB')
    parser.add_argument('--favorite-whitelist', action='store_true', help='Auto add items to your trash using ADB')
    parser.add_argument('file', nargs='?', action='store', type=str, help='Config file path', default=None)
    parser.add_argument('playlist', nargs='?', action='store', type=str, help='Playlist name to read from',
                        default=None)
    args = parser.parse_args()

    if args.e:
        print(yaml.dump(yaml.load(EditorConfig.default_config)))
        return

    if args.file is None:
        parser.print_help()
        return

    playlist_editor = PlaylistEditor(args)
    if args.a:
        playlist_editor.print_song_authors()
    elif args.l:
        playlist_editor.print_playlists()
    elif args.p:
        playlist_editor.print_new_config_file()
    elif args.count:
        playlist_editor.print_count()
    elif args.auto_trash:
        playlist_editor.auto_get_bookmarked_to_trash()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
