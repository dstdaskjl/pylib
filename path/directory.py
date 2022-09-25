import sys
sys.path.append('../')

import os
import inspect
import traceback
import shutil
import pathlib
from pylib.path import path


# Module Decorators
def decorate_module(module, decorator):
    for name, member in inspect.getmembers(module):
        if inspect.getmodule(member) == module and callable(member):
            if member == decorate_module or member == handle_exception:
                continue
            module.__dict__[name] = decorator(member)


def handle_exception(func):
    def decorate(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            print(traceback.format_exc())
    return decorate
# Module Decorators

def copy(src: str, dst: str) -> None:
    shutil.copytree(src, dst)

def create(*args: str) -> None:
    os.mkdir(path.join(*args))

def delete(*args: str) -> None:
    shutil.rmtree(path.join(*args))

def exists(*args: str) -> bool:
    return os.path.exists(path.join(*args))

def home() -> str:
    return str(pathlib.Path.home())

def is_empty(*args: str) -> bool:
    return len(path.listdir(*args)) == 0

def rename(src: str, dst: str) -> None:
    os.rename(src=src, dst=dst)

def zip(src: str, dst: str) -> None:
    shutil.make_archive(base_name=dst, format='zip', root_dir=src)

def unzip(src: str, dst: str) -> None:
    shutil.unpack_archive(filename=src, format='zip', extract_dir=dst)

decorate_module(sys.modules[__name__], handle_exception)