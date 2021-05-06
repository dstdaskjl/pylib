import collections
import json
import os
import pathlib
import shutil
import sys
from zipfile import ZipFile

from log import Log


logger = Log()

def args_valid(func):
    def decorate(*args, **kwargs):
        if not 'path' in kwargs:
            logger.error('Pass a path using kwargs')
        return func(*args, **kwargs)
    return decorate

def exists(func):
    @args_valid
    def decorate(*args, **kwargs):
        if not Path().exists(path=kwargs['path']):
            logger.error(kwargs['path'] + ' does not exist')
        return func(*args, **kwargs)
    return decorate

def is_file(func):
    @exists
    def decorate(*args, **kwargs):
        if not Path().is_file(kwargs['path']):
            logger.error(kwargs['path'] + ' is not a file')
        return func(*args, **kwargs)
    return decorate

def is_dir(func):
    @exists
    def decorate(*args, **kwargs):
        if not Path().is_dir(kwargs['path']):
            logger.error(kwargs['path'] + ' is not a directory')
        return func(*args, **kwargs)
    return decorate

def apply_to_all(func):
    def decorate(cls):
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)):
                setattr(cls, attr, func(getattr(cls, attr)))
        return cls
    return decorate


class Path:
    def create(self, path):
        if self.is_dir(path=path):
            os.makedirs(path)
        elif self.is_file(path=path):
            dirname = File().get_dirname(path=path)
            if not self.exists(dirname):
                os.makedirs(path)
            with open(path, 'w'): pass
        else:
            logger.error(path + ' is neither a directory nor file')

    def exists(self, path: str) -> bool:
        return os.path.exists(path)

    def home_path(self) -> str:
        return str(pathlib.Path.home())

    def is_dir(self, path: str) -> bool:
        return os.path.isdir(path)

    def is_file(self, path: str) -> bool:
        return os.path.isfile(path)

    def join(self, *args):
        return os.path.join(*args)


@apply_to_all(is_file)
class Compression:
    def zip(self, path: str, dest: str):
        try:
            with ZipFile(dest, 'w') as z:
                z.write(path)
        except Exception as e:
            logger.error(e)


@apply_to_all(is_dir)
class Directory:
    def filenames(self, path, nested=False):
        p = Path()

        # Search sub-directory as well
        if nested:
            filepaths = list()
            for dirpath, dirnames, filenames in os.walk(path):
                filepaths.extend(filenames)
            return filepaths
        # Current directory level only
        else:
            return [filename for filename in os.listdir(path) if p.is_file(p.join(path, filename))]

    def filepaths(self, path, nested=False):
        p = Path()

        # Search sub-directory as well
        if nested:
            filepaths = list()
            for dirpath, dirnames, filenames in os.walk(path):
                filepaths.extend([p.join(dirpath, filename) for filename in filenames])
            return filepaths
        # Current directory level only
        else:
            return [p.join(path, filename) for filename in os.listdir(path) if p.is_file(p.join(path, filename))]

    def is_empty(self, path):
        dirs = os.listdir(path)
        return len(dirs) == 0

    def remove(self, path):
        shutil.rmtree(path)


@apply_to_all(is_file)
class File:
    def basename(self, path: str) -> str:
        return os.path.basename(path)

    def count_chars(self, path: str) -> int:
        with open(path, 'r') as infile:
            count = 0
            for idx, line in enumerate(infile):
                count += len(line)
        return count

    def count_lines(self, path: str) -> int:
        with open(path, 'r') as infile:
            for idx, line in enumerate(infile):
                pass
        return idx + 1

    def dirname(self, path: str) -> str:
        return os.path.dirname(path)

    def size(self, path: str) -> int:
        return os.path.getsize(path)

    def remove(self, path: str):
        os.remove(path)


@apply_to_all(is_file)
class Read:
    def all(self, path: str) -> str:
        with open(path, 'r') as infile:
            content = infile.read()
        return content

    def first_n_chars(self, path: str, n: int) -> str:
        try:
            with open(path, 'r') as infile:
                content = infile.read(n)
            return content

        except Exception as e:
            logger.error(e)


    def first_n_lines(self, path: str, n: int) -> str:
        try:
            with open(path, 'r') as infile:
                content = ''
                for idx, line in enumerate(infile):
                    if idx == n:
                        break
                    content += line
            return content

        except Exception as e:
            logger.error(e)

    def last_n_chars(self, path: str, n: int) -> str:
        try:
            with open(path, 'r') as infile:
                queue = collections.deque(maxlen=n)
                for idx, line in enumerate(infile):
                    queue.extend(list(line))
            return ''.join(queue)

        except Exception as e:
            logger.error(e)


    def last_n_lines(self, path: str, n: int) -> str:
        try:
            with open(path, 'r') as infile:
                queue = collections.deque(maxlen=n)
                for idx, line in enumerate(infile):
                    queue.append(line)
            return ''.join(queue)

        except Exception as e:
            logger.error(e)


    def json(self, path: str) -> dict:
        with open(path, 'r') as infile:
            json_obj = json.load(infile)
        return json_obj


class Write:
    def data(self, path: str, data: str, overwrite = True):
        with open(path, 'w' if overwrite else 'a') as outfile:
            outfile.write(data)

    def json(self, path: str, data: dict, overwrite = True):
        json_obj = json.dumps(data, indent=4)
        with open(path, 'w' if overwrite else 'a') as outfile:
            outfile.write(json_obj)