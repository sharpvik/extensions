import json
from path import File

def decode(file):
    contents = file.read('r')
    return json.loads(contents)