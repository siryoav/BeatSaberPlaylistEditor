# BeatSaberPlaylistEditor
The goal of this project is to allow auto ordering of custom songs into playlists (packs) based on song author (artist).

Written in python3.

This project is based on the ability to backup and restore BMBF config, using [PlayList Editor Pro](http://beatsaberquest.com/playlisteditorpro/)
## Terminology
* `BMBF`: the mechanism that controls custom songs in BeatSaber on Oculus platform. previously known as `BeatsOn`
* `default playlists` - The default BeatSaber playlists (OST1, OST2, etc.)
## Prerequisites
* BMBF config file - A `json` file containing BMBF configuration - can be obtained using `PlayList Editor Pro`. This guide will assume you have this file in the same folder with the application with the name `config.json`
* `PlayList Editor Pro` - a project that enables offline playlist editing for BMBF [PlayList Editor Pro](http://beatsaberquest.com/playlisteditorpro/)
* Python 3
* `pillow` python library - `pip install pillow`
* BeatSaber 1.8 (because this is the only version I tested with)
## Getting started
### Get the BMBF config file
Use `PlayList Editor Pro` to backup BMBF config file
### Editor configurations
You should create a new editor config file.
* Use `python main.py -e config.json > config.yaml`

The application will read the configurations file from `config.yaml`
### Good to know
* This application will not touch any of the default BeatSaber playlists (OST1, OST2, etc.)
* It will try to organize only songs in the custom song list (for now, with a little change it will be more dynamic)
### Print song authors
To enable you to know where you stand you can print the list of song authors
Use `python main.py -a config.json`

#### Basic changes
* Add `-c` to capitalize first letter in word
* Add `-s` to strip whitespaces from author's name

### Print new playlists in yaml
To enable easy editing, and editor config editing - you can print the resulting playlists in `yaml`.

Use `python main.py -l --song-name config.json > playlists.yaml`

This will create playlists using author's name and will add to the playlists songs that have a matching author's name.
#### Basic changes
* `-s` and `-c` are still available
* You should add `--song-name` or `--song-id`
    * Without them you would get the python str of internal object
    * With both you will get also song level author, and all of this will be printed in a very convenient format to help you change editor config
#### Guessing song author
A simple algorithm to try and guess the song author.

Many times the BeatSaber community does not write the song author in the right field.

Use `-g` to search the author's name in the song's name, in the song's level author field etc.

If the guessing algorithm could find a single author - it will prefer it over the data included in song author field.

The guessing algorithm normalizes all known authors (from: author field, pre-defined authors and song author map) to lower case letters with only alphabet characters, excludes less then 3 characters results and also excluded guesses, then search for the normalized author's name in a normalized song name field and in normalized level author field.
#### Editor config
* `PreDefinedPlaylists` - A dictionary of where each value is a list of song IDs. Pre-defined playlists will always go at the top of the new playlists (after default playlists)
* `PreDefinedSongAuthors` - A list of user defined authors. This helps the guessing algorithm by adding authors to look for, except the author names embedded in the songs' author field.
* `SongAuthorMap` - A dictionary where each value is a list of song authors. Sometimes we can see author's name written in a non-standard manner - for example `AC/DC` is sometimes written `ACDC`.
    * The keys are the correct form, and the values under the key will be translated to the key form
* `ForcedSongAuthor` - A dictionary from song ID to author's name. With this you can force a specific author to a specific song.
* `ExcludedGuesses` - A list of normalized form author's name, that does not participate in guessing algorithm
### Print new BMBF config
To get the resulting config file
Use `python main.py -p config.json > new_config.json`
#### Basic changes
* `-s`, `-c` and `-g` are still available
* *Do not* use `--song-name` or `--song-id`
* `--cover-image` - Creates a cover image for the new playlists that contains a text with the playlist's name. Very useful for navigating between a lot of playlists

## You should know
* There are almost no checks for flag combinations - so this is your responsibility.
* Backup and restore:
    * BMBF should be open.
    * Use The backup button in `PlayList Editor Pro` to save you current config to the computer.
    * Use the backup file to utilize as input to this application.
    * Close `PlayList Editor Pro`
    * Replace the file that you used with your new config
    * Open `PlayList Editor Pro`
    * Select the config file
    * Click the restore button.
    * Be aware that you should wait for BMBF to finish processing the new config, sometimes I had to wait for the "Sync BeatSaber" red button to show up and let it finish.
    * Also, many times I had `PlayList Editor Pro` throw an error (connection timeout for example) - just click continue.
* Example editor [config.yaml.txt](https://github.com/siryoav/BeatSaberPlaylistEditor/files/4446111/config.yaml.txt)
