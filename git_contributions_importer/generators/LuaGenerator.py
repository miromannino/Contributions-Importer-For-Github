#!/usr/bin/python3

from . import Generator


class LuaGenerator(Generator):
    # one day this will generate awesome random code

    def __init__(self):
        pass

    def insert(self, content, num):
        for i in range(num):
            content.append("print '" + self.random_string(5) + "'")

