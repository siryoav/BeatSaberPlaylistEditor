import os
import json

from ppadb.client import Client as AdbClient


class ADBClient(object):
    def __init__(self):
        os.system('adb start-server')
        self.client = AdbClient(host="127.0.0.1", port=5037)
        self.device = None
        for device in self.client.devices():
            properties = device.get_properties()
            if properties['ro.product.manufacturer'] == 'Oculus' and properties['ro.product.model'] == 'Quest':
                self.device = device
        if self.device is None:
            raise RuntimeError("No Oculus Quest Found attached to this PC")

    def get_player_data(self):
        return json.loads(self.device.shell('cat /sdcard/Android/data/com.beatgames.beatsaber/files/PlayerData.dat'))

    def save_player_data(self, dst='PlayerData.dat.json'):
        self.device.pull('/sdcard/Android/data/com.beatgames.beatsaber/files/PlayerData.dat', dst)

    def get_custom_songs_dir_content(self):
        return list(map(lambda x: x[1:] if x[0] == '\n' else x,self.device.shell('ls -m /sdcard/BMBFData/CustomSongs').split(',')))
