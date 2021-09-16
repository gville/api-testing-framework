import pathlib

def read_file(file_name):
    file = open(str(pathlib.Path(__file__).parent.parent.absolute()) + f"/data/{file_name}", "r")
    return file
