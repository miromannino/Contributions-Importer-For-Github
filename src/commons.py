from collections import namedtuple
import git
import re

Author = namedtuple("Author", ["name", "email"])


def is_valid_git_repo(path):
  try:
    _ = git.Repo(path).git_dir  # Attempt to access the .git directory
    return True
  except git.exc.InvalidGitRepositoryError:
    return False
  except git.exc.NoSuchPathError:
    return False


def extract_name_email(author_string):
  """
  Extracts the name and email from a string in the format 'My Name <email>'.
  Returns:
    Author: An object with 'name' and 'email' fields, or None if the format is invalid.
  """
  print("extract", author_string)
  match = re.match(r"^(.+?)\s*<([^<>]+)>$", author_string)
  print(match)
  if match:
    name, email = match.groups()
    return Author(name=name.strip(), email=email.strip())
  return None
