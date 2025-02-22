from .Generator import Generator


class SqlGenerator(Generator):

    def __init__(self):
        pass

    def insert(self, content, num):
        for i in range(num):
            content.append("SELECT * from " + self.random_string(5) + ";")
