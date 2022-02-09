#!/usr/bin/python3

from . import Generator


class ScalaGenerator(Generator):
    # one day this will generate awesome random code

    min_content_size = 4

    def __init__(self):
        pass

    def insert(self, content, num):
        if len(content) <= self.min_content_size:
            content.clear()
            content.append('object Main' + self.random_string(5) + ' {')
            content.append('    def main(args: Array[String]): Unit = {')
            content.append('    }')
            content.append('}')
        for i in range(num):
            content.insert(-2, '        println("' + self.random_string(5) + '");')

    def delete(self, content, num):
        for i in range(min(num, len(content) - self.min_content_size)):
            content.pop(-3)
