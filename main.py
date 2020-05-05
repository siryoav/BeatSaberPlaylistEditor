import argparse
import yaml

import EditorConfig
from PlaylistEditor import PlaylistEditor

trash_script = """@ECHO OFF
setlocal
for /f "usebackq delims=" %%t in (`powershell -noprofile -c "[Console]::Title.Replace(' - '+[Environment]::CommandLine,'') -replace '(.+) - .+','$1'"`) do set thisTitle=%%t
setlocal EnableDelayedExpansion
set n=0

set count=0
for /D %%j in (*) do set /A count+=1

rem Fill "bar" variable with 70 characters
set "bar="
for /L %%j in (1,1,70) do set "bar=!bar!#"

rem Fill "space" variable with filler spaces
set "space="
for /L %%i in (1,1,98) do set "space=!space!_"
set k=0

FOR /D %%i IN (*) DO (

	set /A k+=1, percent=k*100/count, barLen=70*percent/100
	set /A spaceLen=100-percent
	set /A spaceLen=98*spaceLen/100
	for %%a in (!barLen!) do set completed=!bar:~0,%%a!
	for %%a in (!spaceLen!) do set not_completed=!space:~0,%%a!
	title !percent!%% !completed!!not_completed!

	FOR %%f IN (
{}
	) DO (
		ECHO %%i | FINDSTR /C:"%%f" >nul & IF ERRORLEVEL 1 (
			REM FALSE
		) else (
			set vector[!n!]=%%i
			set /A n+=1
		)
	)
)


set /A n-=1
for /L %%i in (0,1,%n%) do (
	set j=!vector[%%i]!
	echo !j!
	RMDIR /s /Q "!j!"
)
title !thisTitle!
"""


def print_trash_script():
    print(trash_script.format(
        '\n'.join(map(lambda f: '\t\t{}'.format(f[13:]), EditorConfig.EditorConfig().config['Trash']))))


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
    parser.add_argument('-t', action='store_true', help='Print trash script')
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

    if args.t:
        print_trash_script()
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
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
