#!/usr/bin/python3

from . import Generator
import random


class JsonGenerator(Generator):
    # one day this will generate awesome random code

    min_content_size = 3

    def __init__(self):
        pass

    def insert(self, content, num):
        if len(content) <= self.min_content_size:
            content.clear()
            content.append('{')
            content.append('  "last-prop": 42')
            content.append('}')
        for i in range(num):
            content.insert(-2, '  "' + self.random_string(5) + '": ' + str(int(random.random() * 100)) + ',')

    def delete(self, content, num):
        for i in range(min(num, len(content) - self.min_content_size)):
            content.pop(-3)
