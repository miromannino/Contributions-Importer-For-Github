from .Generator import Generator


class CGenerator(Generator):

    min_content_size = 5

    def __init__(self):
        pass

    def insert(self, content, num):
        if len(content) <= self.min_content_size:
            content.clear()
            content.append("# include <stdio.h>")
            content.append("")
            content.append("int main() {")
            content.append("return 0;")
            content.append("}")
        for i in range(num):
            content.insert(-2, '        printf("' + self.random_string(5) + '");')

    def delete(self, content, num):
        for i in range(min(num, len(content) - self.min_content_size)):
            content.pop(-3)
