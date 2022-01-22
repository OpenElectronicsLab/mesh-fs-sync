from pathlib import Path

import hashlib

def sha256_for_path(fp, blocksize = (4 * 1024 * 1024)):
    hasher = hashlib.sha256()
    buf = fp.read(blocksize)
    # while len(buf) > 0:
    assert len(buf) < blocksize
    hasher.update(buf)
    #    buf = fp.read(blocksize)
    return hasher.hexdigest()

def get_dir_state(dirpath):
    ds = {}
    for path in dirpath.iterdir():
        with open(path, 'rb') as fp:
            ds[path.name] = { 'sha256': sha256_for_path(fp) }
    return ds
