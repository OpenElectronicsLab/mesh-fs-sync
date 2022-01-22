from pathlib import Path

def get_dir_state(dirpath):
    ds = {}
    for x in dirpath.iterdir():
        ds[x.name] = {}
    return ds
