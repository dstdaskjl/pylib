import os


def basename(*args: str) -> str:
    return os.path.basename(join(*args))

def join(*args: str) -> str:
    return os.path.join(*args)

def list_dir(*args: str) -> list:
    return os.listdir(join(*args))

def split(path: str) -> list:
    return os.path.normpath(path).split(os.sep)