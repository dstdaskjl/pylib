import os
import shutil
import pathlib
import json
import traceback
from zipfile import ZipFile


def handle_exception(func):
    def decorate(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            print(traceback.format_exc())
    return decorate


def apply_to_all(func):
    def decorate(cls):
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)):
                setattr(cls, attr, func(getattr(cls, attr)))
        return cls
    return decorate


class Path:
    def basename(self, *args: str) -> str:
        return os.path.basename(self.join(*args))

    def join(self, *args: str) -> str:
        return os.path.join(*args)

    def list_dir(self, *args: str) -> list:
        return os.listdir(self.join(*args))

    def split(self, path: str) -> list:
        return os.path.normpath(path).split(os.sep)


@apply_to_all(handle_exception)
class File(Path):
    def copy(self, src: str, dst: str) -> None:
        shutil.copy(src, dst)

    def create(self, *args: str) -> None:
        open(self.join(*args), 'w')

    def delete(self, *args: str) -> None:
        os.remove(self.join(*args))

    def exists(self, *args: str) -> bool:
        return os.path.exists(self.join(*args))

    def read_text(self, filepath: str) -> list:
        with open(filepath, 'r') as f:
            contents = f.read().splitlines()
        return contents

    def read_json(self, path: str) -> dict:
        with open(path, 'r') as f:
            json_obj = json.load(f)
        return json_obj

    def rename(self, src: str, dst: str) -> None:
        os.rename(src=src, dst=dst)

    def write_binary(self, filepath: str, content: bytes, mode='wb') -> None:
        with open(filepath, mode=mode) as f:
            f.write(content)

    def write_json(self, filepath: str, data: dict, mode='a', indent=4) -> None:
        json_obj = json.dumps(data, indent=indent)
        with open(filepath, mode=mode) as f:
            f.write(json_obj)

    def write_nothing(self, filepath:str) -> None:
        with open(filepath, 'w') as f:
            pass

    def write_text(self, filepath: str, content: str, mode='a') -> None:
        with open(filepath, mode=mode) as f:
            f.write(content)

    def zip(self, src: str, dst: str) -> None:
        with ZipFile(dst, 'w') as z:
            z.write(src)

    def unzip(self, src: str, dst: str) -> None:
        with ZipFile(src, 'r') as z:
            z.extractall(dst)


@apply_to_all(handle_exception)
class Directory(Path):
    def copy(self, src: str, dst: str) -> None:
        shutil.copytree(src, dst)

    def create(self, *args: str) -> None:
        os.mkdir(self.join(*args))

    def delete(self, *args: str) -> None:
        shutil.rmtree(self.join(*args))

    def exists(self, *args: str) -> bool:
        return os.path.exists(self.join(*args))

    def home(self) -> str:
        return str(pathlib.Path.home())

    def is_empty(self, *args: str) -> bool:
        return len(self.listdir(*args)) == 0

    def rename(self, src: str, dst: str) -> None:
        os.rename(src=src, dst=dst)

    def zip(self, src: str, dst: str) -> None:
        shutil.make_archive(base_name=dst, format='zip', root_dir=src)

    def unzip(self, src: str, dst: str) -> None:
        shutil.unpack_archive(filename=src, format='zip', extract_dir=dst)
