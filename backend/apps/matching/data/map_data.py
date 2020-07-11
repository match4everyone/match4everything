import json
from os.path import abspath, dirname, join

current_location = dirname(abspath(__file__))

with open(join(current_location, "../data/zipcodes_merged.json")) as f:
    zipcodes = json.loads(f.read())
