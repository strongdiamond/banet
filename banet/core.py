# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/00_core.ipynb (unless otherwise specified).

__all__ = ['filter_files', 'ls', 'hdf_attr_check', 'dict2json', 'monthlen', 'InOutPath']

# Cell
import numpy as np
import json
from pathlib import Path

# Cell
def filter_files(files, include=[], exclude=[]):
    "Filter list of files using a list of strings to inculde and/or exclude"
    for incl in include:
        files = [f for f in files if incl in f.name]
    for excl in exclude:
        files = [f for f in files if excl not in f.name]
    return sorted(files)

def ls(x, recursive=False, include=[], exclude=[]):
    "List files in folder, if recursive is True also list subfolders"
    if not recursive:
        out = list(x.iterdir())
    else:
        out = [o for o in x.glob('**/*')]
    out = filter_files(out, include=include, exclude=exclude)
    return sorted(out)

Path.ls = ls

def hdf_attr_check(attr, hdf, default):
    "Check if attribute is in hdf_attr_dict and return default"
    return default if not hasattr(hdf, attr) else hdf.__getattr__(attr)

def dict2json(data:dict, file):
    "Writes json file from dict"
    with open(file, 'w') as f:
        f.write(json.dumps(data))

# Cell
def monthlen(year, month):
    "Gives lenght of the month"
    base = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if (year % 4) == 0:
        if (year % 100) == 0:
            if (year % 400) == 0:
                base[1] += 1
        else:
            base[1] += 1
    return base[month-1]

# Cell
class InOutPath():
    """Keeps track of an input and a output path. Creates paths if they don't exist and mkdir=True"""
    def __init__(self, input_path:str, output_path:str, mkdir=True):
        if isinstance(input_path, str): input_path = Path(input_path)
        if isinstance(output_path, str): output_path = Path(output_path)
        self.input_path = input_path
        self.output_path = output_path
        if mkdir: self.mkdirs()

    @property
    def src(self):
        "Shortcut to input_path"
        return self.input_path

    @property
    def dst(self):
        "Shortcut to output_path"
        return self.output_path

    def mkdirs(self):
        self.input_path.mkdir(exist_ok=True, parents=True)
        self.output_path.mkdir(exist_ok=True, parents=True)

    def __truediv__(self, s):
        return InOutPath(self.src/s, self.dst/s)

    def __repr__(self):
        return '\n'.join([f'{i}: {o}' for i, o in self.__dict__.items()]) + '\n'