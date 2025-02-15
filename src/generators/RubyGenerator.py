from .Generator import Generator


class RubyGenerator(Generator):

    def __init__(self):
        pass

    def insert(self, content, num):
        for i in range(num):
            content.append('puts("' + self.random_string(5) + '")')
