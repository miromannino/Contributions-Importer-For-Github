#!/usr/bin/python3

from . import Generator


class PhpGenerator(Generator):
    # one day this will generate awesome random code

    min_content_size = 2

    def __init__(self):
        pass

    def insert(self, content, num):
        if len(content) <= self.min_content_size:
            content.clear()
            content.append('<?php')
            content.append('?>')
        for i in range(num):
            content.insert(-1, '        echo "' + self.random_string(5) + '";')

    def delete(self, content, num):
        for i in range(min(num, len(content) - self.min_content_size)):
            content.pop(-2)
