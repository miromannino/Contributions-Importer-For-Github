#!/usr/bin/python3

from typing import Optional
import git
import time
import os
import shutil
from .commons import Author


class Committer:

  def __init__(self, mock_repo_path, content):
    self.mock_repo_path = mock_repo_path
    self.content = content
    self.mock_repo = self._initialize_repo()

  def _initialize_repo(self):
    """Ensure the mock repository exists and is initialized."""
    if not os.path.exists(self.mock_repo_path):
      os.makedirs(self.mock_repo_path)
    try:
      return git.Repo(self.mock_repo_path)
    except git.exc.InvalidGitRepositoryError:
      return git.Repo.init(self.mock_repo_path)

  def _check_readme(self):
    readme_path = os.path.dirname(__file__) + '/README.md'
    mockrepo_readme_path = self.mock_repo_path + '/README.md'
    shutil.copyfile(readme_path, mockrepo_readme_path)
    self.mock_repo.git.add('README.md')

  def get_last_commit_date(self):
    ''' returns the last commit date in ms from epoch'''
    last_commit_date = 0
    for b in self.mock_repo.branches:
      for c in self.mock_repo.iter_commits(b.name):
        if c.committed_date > last_commit_date:
          last_commit_date = c.committed_date
    return last_commit_date

  def commit(self, date: int, message: str, author: Optional[Author] = None):
    ''' performs the commit. date is in seconds from epoch '''
    self._check_readme()
    for file in self.content.get_files():
      self.mock_repo.git.add(file)
    date_iso_format = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(date))
    if author:
      if isinstance(author, list):
        author = author[0]
      os.environ["GIT_AUTHOR_NAME"] = author.name
      os.environ["GIT_AUTHOR_EMAIL"] = author.email
    os.environ['GIT_AUTHOR_DATE'] = date_iso_format
    os.environ['GIT_COMMITTER_DATE'] = date_iso_format
    try:
      self.mock_repo.git.commit('-m', message, '--allow-empty')
    except git.exc.GitError as e:
      print('Error in commit: ' + str(e))
