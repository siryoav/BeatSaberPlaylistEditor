import argparse

from PlaylistEditor import PlaylistEditor


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', action='store_true', help='Print song authors')
    parser.add_argument('-c', action='store_true', help='Capital letters in author\'s name')
    parser.add_argument('-s', action='store_true', help='Strip whitespaces from author\'s name')
    parser.add_argument('-l', action='store_true', help='Print lists in yaml')
    parser.add_argument('-g', action='store_true', help='Try to guess song author if not available')
    parser.add_argument('--song-name', action='store_true', help='Print song\'s name')
    parser.add_argument('--song-id', action='store_true', help='Print song\'s id')
    parser.add_argument('-p', action='store_true', help='Print new config file')
    parser.add_argument('file', action='store', type=str, help='Config file path')
    args = parser.parse_args()

    playlist_editor = PlaylistEditor(args)

    if args.a:
        playlist_editor.print_song_authors()
    elif args.l:
        playlist_editor.print_playlists()
    elif args.p:
        playlist_editor.print_new_config_file()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
