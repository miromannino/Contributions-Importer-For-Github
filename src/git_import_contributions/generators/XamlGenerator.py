from .Generator import Generator


class XamlGenerator(Generator):
    min_content_size = 6

    def __init__(self):
        pass

    def insert(self, content, num):
        if len(content) <= self.min_content_size:
            content.clear()
            content.append('<Window x:Class="GeneratedWindow"')
            content.append(
                '        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"'
            )
            content.append('        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">')
            content.append("    <Grid>")
            content.append("    </Grid>")
            content.append("</Window>")
        for i in range(num):
            content.insert(-2, '        <TextBlock Text="' + self.random_string(8) + '" />')

    def delete(self, content, num):
        for i in range(min(num, len(content) - self.min_content_size)):
            content.pop(-3)
