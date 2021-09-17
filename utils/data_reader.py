import pathlib
import json

def read_file(file_name):
    file = open(str(pathlib.Path(__file__).parent.parent.absolute()) + f"/data/{file_name}", "r")
    return file

def read_json_from_file(file_name):
    dictionary = json.load(read_file(file_name))
    return dictionary
