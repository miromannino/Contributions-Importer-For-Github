from .Generator import Generator


class CsharpGenerator(Generator):
    min_content_size = 8

    def __init__(self):
        pass

    def insert(self, content, num):
        if len(content) <= self.min_content_size:
            content.clear()
            content.append("using System;")
            content.append("")
            content.append("namespace GeneratedCode")
            content.append("{")
            content.append("    class Program")
            content.append("    {")
            content.append("        static void Main(string[] args)")
            content.append("        {")
            content.append("        }")
            content.append("    }")
            content.append("}")
        for i in range(num):
            content.insert(-3, '            Console.WriteLine("' + self.random_string(5) + '");')

    def delete(self, content, num):
        for i in range(min(num, len(content) - self.min_content_size)):
            content.pop(-4)
