import sys
sys.path.append('../')

import os
import shutil
import json
import inspect
import traceback
from pylib.path import path
from zipfile import ZipFile


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
    shutil.copy(src, dst)

def create(*args: str) -> None:
    open(path.join(*args), 'w')

def delete(*args: str) -> None:
    os.remove(path.join(*args))

def exists(*args: str) -> bool:
    return os.path.exists(path.join(*args))

def read_text(filepath: str) -> list:
    with open(filepath, 'r') as f:
        contents = f.read().splitlines()
    return contents

def read_json(path: str) -> dict:
    with open(path, 'r') as f:
        json_obj = json.load(f)
    return json_obj

def rename(src: str, dst: str) -> None:
    os.rename(src=src, dst=dst)

def write_binary(filepath: str, content: bytes, mode='wb') -> None:
    with open(filepath, mode=mode) as f:
        f.write(content)

def write_json(filepath: str, data: dict, mode='a', indent=4) -> None:
    json_obj = json.dumps(data, indent=indent)
    with open(filepath, mode=mode) as f:
        f.write(json_obj)

def write_nothing(filepath: str) -> None:
    with open(filepath, 'w') as f:
        pass

def write_text(filepath: str, content: str, mode='a') -> None:
    with open(filepath, mode=mode) as f:
        f.write(content)

def zip(src: str, dst: str) -> None:
    with ZipFile(dst, 'w') as z:
        z.write(src)

def unzip(src: str, dst: str) -> None:
    with ZipFile(src, 'r') as z:
        z.extractall(dst)

decorate_module(sys.modules[__name__], handle_exception)