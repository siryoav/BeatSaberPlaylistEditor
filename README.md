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
* BeatSaber 1.8 (because this is the only version I tested with)
### Trash management
For some of the features related to trash management (songs you don't want to have on your device anymore)
* ADB installed on the computer and in the `PATH` environment variable
## Installation
`pip install -r requirements.txt`
## Getting started
### Get the BMBF config file
Use `PlayList Editor Pro` to backup BMBF config file
### Editor configurations
You should create a new editor config file.
* Use `python main.py -e > config.yaml`

The application will read the configurations file from `config.yaml`
### Good to know
* This application will not touch any of the default BeatSaber playlists (OST1, OST2, etc.)
### Print song authors
To enable you to know where you stand you can print the list of song authors
Use `python main.py -a config.json`
#### Input playlist
The default input playlist is the custom songs playlist.
* Use `--all-playlists` to use all playlists (except default ones) as inputs
* Use the second positional argument (after input file) to give the name of the input playlist
    * For example `python main.py -a config.json my_playlist`
#### Basic changes
* Add `-c` to capitalize first letter in word
* Add `-s` to strip whitespaces from author's name
* Add `-r` to transform all capital letters to only first capital if possible - In case there are two song authors - one with the name in all capital  and one not (first letter capital or all not capital) - transfrom the all capital version to the other version - for example - `MUSE` will be transformed to `Muse` (given that some other song has the author `Muse`)
* Add `--fix-the` to add authors a missing "The". Depends on that some other song has the author with "The" - for example `Offspring` will be transformed into `The Offspring` (given that some other song has the author `The Offspring`)
### Print new playlists in yaml
To enable easy editing, and editor config editing - you can print the resulting playlists in `yaml`.

Use `python main.py -l --song-name config.json > playlists.yaml`

This will create playlists using author's name and will add to the playlists songs that have a matching author's name.
#### Input playlist
* Same as before - `--all-playlists` and the second positional argument are still available
#### Basic changes
* `-s`, `-c`, `-r` and `--fix-the` are still available
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
#### Input playlist
* Same as before - `--all-playlists` and the second positional argument are still available
#### Basic changes
* `-s`, `-c`, `-r`, `-g` and `--fix-the` are still available
* *Do not* use `--song-name` or `--song-id`
* `--cover-image` - Creates a cover image for the new playlists that contains a text with the playlist's name. Very useful for navigating between a lot of playlists
### Print counts of playlists and songs
`python main.py --count config.json`
### Trash
Trash configuration is where you can define song IDs that should be deleted from your playlists.

The application will not write the songs in the trash to playlists, no matter what (even if they are written elsewere in the configurations)
### Auto fill your trash
* You will need ADB installed on the computer. see [Prerequisites](https://github.com/siryoav/BeatSaberPlaylistEditor#trash-management)
    * You can copy relevant data from you Oculus Quest by your self, and this makes ADB unnecessary - more on this later.
* You should backup you config.yaml
* After filling your Trash - you should [Print new BMBF config](https://github.com/siryoav/BeatSaberPlaylistEditor#print-new-bmbf-config)
* Auto trash will also clean your configuration from previous usages of songs in the trash (for example - if you added it to a pre-defined list - it will remove it from there).
Use `python main.py --auto-trash config.json > config.yaml`
#### Input playlist
* Same as before - `--all-playlists` and the second positional argument are still available
#### Basic changes
* `--auto-trash-source` - replaces the need for ADB - you can supply your own `PlayerData.dat`
    * On the Oculus Quest - the `PlayerData.dat` is located at: `/sdcard/Android/data/com.beatgames.beatsaber/files/PlayerData.dat`
    * For example, if `PlayerData.dat` is in the current directory, `--auto-trash-source=PlayerData.dat`
* `--trash-overwrite` - Causes the new trash data to overwrite the old trash data, otherwise it appends.
* `--favorite-whitelist` - Causes the favorites list to be considered as whitelist - meaning all the songs *not* in the favorites list will go to trash
### Empty trash from Oculus Quest memory
Use Trash configuration and ADB to delete the songs in trash from the Oculus Quests' memory.
* You will need ADB installed on the computer. see [Prerequisites](https://github.com/siryoav/BeatSaberPlaylistEditor#trash-management)
* This *Cannot be reverted*
* I recommend doing 
Use `python main.py --empty-trash-from-device`
## You should know
* There are almost no checks for flag combinations - so this is your responsibility.
### Backup and restore
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
### Example editor config
* Example editor [config.yaml.txt](https://github.com/siryoav/BeatSaberPlaylistEditor/files/4464453/config.yam.txt)
### Recomannded workflow
* `python main.py -l -c -s -g -r --song-name --all-playlists --fix-the config.json > playlists.yaml`
* `python main.py -l -c -s -g -r --song-name --song-id --all-playlists --fix-the config.json > playlists.yaml`
* `python main.py -p -c -s -g -r --all-playlists --fix-the --cover-image config.json > new_config.json`

## FAQ
### Postfix SHA1 for playlists
Because the restore process of config.json is out of my hands, I found this to be a simple and reliable solution to the problem:
* The restore process does not respect the order of the playlists in the restored config.json. It will create new playlists in the correct order, but will add them at the end of the playlists list - meaning that every existing playlist will be before the newly added lists.
* As a result - upon using this tool for the second time and on - if you added songs from an author you didn't have before - this author will not be ordered alphabetically as the rest, but will be put in the end of playlists list.
* The recognition of existing playlists is done by a field in the playlist called `id`.
* To Solve the problem I added a SHA1 digest to the end of each playlist id, causing all the previous playlists to be deleted (because the same IDs are not existing in the new config.json) and the new ones to be created in the correct order
    * The use of SHA1 is a standard way to avoid collisions.
    * The hash is done on the resulting playlists - because I wanted this application to be deterministic.
