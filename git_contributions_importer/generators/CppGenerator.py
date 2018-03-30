#!/usr/bin/python3

from . import Generator


class CppGenerator(Generator):
    # one day this will generate awesome random code

    min_content_size = 6

    def __init__(self):
        pass

    def insert(self, content, num):
        if len(content) <= self.min_content_size:
            content.clear()
            content.append('# include <iostream>')
            content.append('using namespace std;')
            content.append('')
            content.append('int main() {')
            content.append('return 0;')
            content.append('}')
        for i in range(num):
            content.insert(-2, '        cout << "' + self.random_string(5) + '";')

    def delete(self, content, num):
        for i in range(min(num, len(content) - self.min_content_size)):
            content.pop(-3)
