from BMBFConfig import BMBFConfig


class BMBFConfigFile(object):
    def __init__(self, data):
        is_committed = data['IsCommitted']
        config = BMBFConfig(data['Config'])
        sync_config = data['SyncConfig']
        beat_saber_version = data['BeatSaberVersion']