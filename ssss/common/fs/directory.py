import os
from pathlib import Path


def make_empty(dir_path, remove=False):
    [x if x.is_dir() and make_empty(x, True) else x.is_file() and x.unlink() for x in Path(dir_path).iterdir()]
    if remove:
        os.rmdir(dir_path)
