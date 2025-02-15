from .Generator import Generator


class JsGenerator(Generator):

    def __init__(self):
        pass

    def insert(self, content, num):
        for i in range(num):
            content.append('console.log("' + self.random_string(5) + '")')
