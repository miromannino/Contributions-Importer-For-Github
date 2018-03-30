#!/usr/bin/python3

from . import Generator


class JavaGenerator(Generator):
    # one day this will generate awesome random code

    min_content_size = 4

    def __init__(self):
        pass

    def insert(self, content, num):
        if len(content) <= self.min_content_size:
            content.clear()
            content.append('public class C' + self.random_string(5) + ' {')
            content.append('    public static void main() {')
            content.append('    }')
            content.append('}')
        for i in range(num):
            content.insert(-2, '        System.out.println("' + self.random_string(5) + '");')

    def delete(self, content, num):
        for i in range(min(num, len(content) - self.min_content_size)):
            content.pop(-3)
