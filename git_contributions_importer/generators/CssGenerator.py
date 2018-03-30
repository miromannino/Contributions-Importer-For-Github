#!/usr/bin/python3

from . import Generator
import random


class CssGenerator(Generator):
    # one day this will generate awesome random code

    properties = ['line-height', 'border-top-width', 'border-bottom-width', 'border-left-width', 'border-right-width',
                  'margin-top', 'margin-bottom', 'margin-left', 'margin-right', 'padding-top', 'padding-bottom',
                  'padding-left', 'padding-right', 'font-size']

    min_content_size = 2

    def __init__(self):
        pass

    def insert(self, content, num):
        if len(content) <= self.min_content_size:
            content.clear()
            content.append('.' + self.random_string(5) + ' { ')
            content.append('}')
        for i in range(num):
            content.insert(-1, '  ' + self.properties[int(random.random() * len(self.properties))]
                           + ': ' + str(int(random.random() * 100)) + 'px;')

    def delete(self, content, num):
        for i in range(min(num, len(content) - self.min_content_size)):
            content.pop(-2)
