class Stats:
  """
  A class that represents statistics for code changes.

  Attributes:
    insertions (dict): A dictionary that stores the number of insertions per file extension.
    deletions (dict): A dictionary that stores the number of deletions per file extension.
    max_changes_per_file (int): The maximum number of changes allowed per file.
  """

  def __init__(self, max_changes_per_file=-1):
    self.insertions = {}
    self.deletions = {}
    self.max_changes_per_file = max_changes_per_file

  def add_insertions(self, ext: str, num: int):
    """
    Adds the number of insertions for a specific file extension.

    Args:
      ext (str): The file extension.
      num (int): The number of insertions.
    """
    if ext not in self.insertions:
      self.insertions[ext] = num
    else:
      self.insertions[ext] = self.insertions[ext] + num
    if 0 < self.max_changes_per_file < self.insertions[ext]:
      self.insertions[ext] = self.max_changes_per_file

  def add_deletions(self, ext, num):
    """
    Adds the number of deletions for a specific file extension.

    Args:
      ext (str): The file extension.
      num (int): The number of deletions.
    """
    if ext not in self.deletions:
      self.deletions[ext] = num
    else:
      self.deletions[ext] = self.deletions[ext] + num
    if 0 < self.max_changes_per_file < self.deletions[ext]:
      self.deletions[ext] = self.max_changes_per_file

  def iterate_insertions(self, max_changes=-1):
    """
    Iterates over the insertions in the Stats object, breaking them down into smaller chunks.

    Args:
      max_changes (int, optional): The maximum number of changes allowed in each chunk. Defaults to -1, which means no limit.

    Yields:
      Stats: A new Stats object with a subset of the insertions.
    """
    if max_changes <= 0:
      yield self
      return
    broken_stats = Stats()
    acc = 0
    for k, v in self.insertions.items():
      while v > 0:
        changes = min(max_changes - acc, v)
        v -= changes
        broken_stats.insertions[k] = changes
        acc += changes
        if acc >= max_changes:
          yield broken_stats
          broken_stats.insertions = {}
          acc = 0
    for k, v in self.deletions.items():
      while v > 0:
        changes = min(max_changes - acc, v)
        v -= changes
        broken_stats.deletions[k] = changes
        acc += changes
        if acc >= max_changes:
          yield broken_stats
          broken_stats.deletions = {}
          acc = 0
    if len(broken_stats.insertions) > 0 or len(broken_stats.deletions) > 0:
      yield broken_stats

  def __str__(self):
    """
    Returns a string representation of the Stats object.
    """
    return 'insertions: ' + str(self.insertions) \
        + ' deletions: ' + str(self.deletions)
