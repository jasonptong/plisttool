from pathlib import Path

import os.path


def exists(filename):
    return os.path.exists(filename)


def file_ext(type, filename, parser):
    ext = os.path.splitext(filename)[1][1:]
    if ext != type:
       parser.error("File doesn't end with {}".format(type))
    return filename


def new_filename(filename, dir=Path().absolute()):
    if os.path.isabs(filename):
        return filename
    return "%s/%s" % (dir, filename)
