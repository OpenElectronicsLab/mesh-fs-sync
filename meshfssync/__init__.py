from pathlib import Path

import hashlib

def sha256_for_file(fp, blocksize = (4 * 1024 * 1024)):
    hasher = hashlib.sha256()
    buf = fp.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = fp.read(blocksize)
    return hasher.hexdigest()

def get_path_state(path):
    if path.is_file():
        with open(path, 'rb') as fp:
            return {
                'type': 'file',
                'sha256': sha256_for_file(fp),
            }
    else:
        return {
            'type': 'directory',
            'dir_state': {
                subpath.name: get_path_state(subpath)
                    for subpath in path.iterdir() },
        }
