from . import Generator


class TerraformGenerator(Generator):
  
  def __init__(self):
    pass

  def insert(self, content, num):
    for i in range(num):
      content.append('resource "random_string" "' + self.random_string(5) + '" { length = 10 }')
