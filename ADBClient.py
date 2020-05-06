import os
import json

from ppadb.client import Client as AdbClient

custom_songs_path = '/sdcard/BMBFData/CustomSongs'
player_data_path = '/sdcard/Android/data/com.beatgames.beatsaber/files/PlayerData.dat'


class ADBClient(object):
    def __init__(self):
        os.system('adb start-server')
        self.client = AdbClient(host="127.0.0.1", port=5037)
        self.device = None
        for device in self.client.devices():
            properties = device.get_properties()
            if properties['ro.product.manufacturer'] == 'Oculus' and properties['ro.product.model'] == 'Quest':
                self.device = device
                break
        if self.device is None:
            raise RuntimeError("No Oculus Quest Found attached to this PC")

    def get_player_data(self):
        return json.loads(self.device.shell('cat {}'.format(player_data_path)))

    def save_player_data(self, dst='PlayerData.dat.json'):
        self.device.pull(player_data_path, dst)

    def get_custom_songs_dir_content(self):
        return list(map(lambda x: x[1:] if x[0] == '\n' else x,
                        self.device.shell('ls -m {}'.format(custom_songs_path)).split(',')))

    def delete_songs(self, songs_paths):
        print('Number of songs to delete: {}'.format(len(songs_paths)))
        full_path_songs = list(map(lambda song_path: '"{}/{}"'.format(custom_songs_path, song_path), songs_paths))
        count = 0
        for full_path_song in full_path_songs:
            print('Deleting {}'.format(full_path_song))
            command = 'rm -rf {}'.format(full_path_song)
            res = self.device.shell(command)
            if res is not None and len(res) > 0:
                print(res)
            else:
                count += 1
        print('Deleted: {}'.format(count))
