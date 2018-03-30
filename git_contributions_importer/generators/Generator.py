#!/usr/bin/python3

import random


class Generator:

    def __init__(self):
        pass

    def random_string(self, length=10):
        return ''.join([chr(int(random.random() * (ord('z') - ord('a'))) + ord('a')) for c in range(length)])

    def random_phrase(self, length=10, word_length=10):
        return ' '.join([self.random_string(length=int(word_length)) for _ in range(int(length))])

    ''' insert num lines of code/text inside content.
        content is a list of strings that represent the file '''
    def insert(self, content, num):
        for i in range(num):
            content.append(self.random_phrase(random.random() * 10 + 1))
    
    ''' delete num lines of code/text from content.
        content is a list of strings that represent the file '''
    def delete(self, content, num):
        for i in range(min(num, len(content))):
            content.pop()
