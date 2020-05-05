import argparse
import functools

import yaml

import EditorConfig
from ADBClient import ADBClient
from PlaylistEditor import PlaylistEditor


def trash_path_filter(trash_ids, song_path):
    for trash_id in trash_ids:
        if trash_id in song_path:
            return True
    return False


def empty_trash_from_device():
    trash_ids = set(map(lambda f: f[13:], EditorConfig.EditorConfig().config['Trash']))
    adb_client = ADBClient()
    existing_songs_paths = adb_client.get_custom_songs_dir_content()
    songs_paths_to_delete = filter(functools.partial(trash_path_filter, trash_ids), existing_songs_paths)
    adb_client.delete_songs(list(songs_paths_to_delete))


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
    parser.add_argument('--empty-trash-from-device', action='store_true', help='Using ADB, delete all trash songs')
    parser.add_argument('file', nargs='?', action='store', type=str, help='Config file path', default=None)
    parser.add_argument('playlist', nargs='?', action='store', type=str, help='Playlist name to read from',
                        default=None)
    args = parser.parse_args()

    if args.e:
        print(yaml.dump(yaml.load(EditorConfig.default_config)))
        return

    if args.empty_trash_from_device:
        empty_trash_from_device()
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
