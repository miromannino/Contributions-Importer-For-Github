from . import Generator


class KotlinGenerator(Generator):

    def __init__(self):
        pass

    def insert(self, content, num):
        for i in range(num):
            content.append('println("' + self.random_string(5) + '")')
