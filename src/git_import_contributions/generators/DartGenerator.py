from .Generator import Generator


class DartGenerator(Generator):
    min_content_size = 4

    def __init__(self):
        pass

    def insert(self, content, num):
        if len(content) <= self.min_content_size:
            content.clear()
            content.append("void main() {")
            content.append("  // Generated Dart code")
            content.append("}")
        for i in range(num):
            content.insert(-1, '  print("' + self.random_string(5) + '");')

    def delete(self, content, num):
        for i in range(min(num, len(content) - self.min_content_size)):
            content.pop(-2)
