from BMBFPlaylists import BMBFPlaylists


class BMBFConfig(object):
    def __init__(self, data):
        playlists = BMBFPlaylists(data['Playlists'])
        saber = data['Saber']
        left_color = data['LeftColor']
        right_color = data['RightColor']
        text_changes = data['TextChanges']
