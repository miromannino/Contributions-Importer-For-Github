#!/usr/bin/python3

import os
import pathlib
from .generators import available_generators


class Content:
    FILENAME = 'content'

    def __init__(self, folder_path):
        self.contents = {}
        self.folder_path = folder_path
        self.load()

    def loadFile(self, ext, path):
        if ext not in available_generators: return
        with open(path, 'r') as t:
            lines = []
            for l in t:
                lines.append(l.replace('\n', ''))
            self.contents[ext] = lines

    def load(self):
        for path in os.listdir(self.folder_path):
            full_path = os.path.join(self.folder_path, path)
            if os.path.isfile(full_path):
                self.loadFile(pathlib.Path(full_path).suffix, full_path)

    def save(self):
        for k, v in self.contents.items():
            full_path = os.path.join(self.folder_path, Content.FILENAME + k)
            with open(full_path, 'w') as f:
                for l in v:
                    f.write(l)
                    f.write('\n')

    def get_files(self):
        return map(lambda fn: Content.FILENAME + fn, self.contents.keys())

    def get(self, ext): 
        if ext not in self.contents:
            self.contents[ext] = []
        return self.contents[ext]
