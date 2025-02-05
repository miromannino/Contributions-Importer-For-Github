from . import Generator


class PyGenerator(Generator):

    def __init__(self):
        pass

    def insert(self, content, num):
        for i in range(num):
            content.append('print("' + self.random_string(5) + '")')
