import json

from BMBFConfigFile import BMBFConfigFile
from EditorConfig import EditorConfig


def main():
    e = EditorConfig()
    with open('config.json', 'rb') as f:
        data = json.load(f)
        b = BMBFConfigFile(data)




if __name__ == '__main__':
    main()
