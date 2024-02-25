import git
from src import *
import shutil
from tests.tests_commons import REPOS_PATHS, MOCK_REPO_PATH
import pytest


def test_ignore_file_types():
  repos = [git.Repo(repo_path) for repo_path in REPOS_PATHS]
  shutil.rmtree(MOCK_REPO_PATH, ignore_errors=True)
  mock_repo = git.Repo.init(MOCK_REPO_PATH)

  ignored_filetypes = ['.csv', '.txt', '.pdf', '.xsl', '.sql']

  importer = Importer(repos, mock_repo)
  importer.set_ignored_file_types(ignored_filetypes)
  importer.set_keep_commit_messages(True)
  importer.import_repository()

  # check that there are no files of the ignored categories
  for file in mock_repo.git.ls_files().split('\n'):
    for ignored_filetype in ignored_filetypes:
      assert not file.endswith(ignored_filetype)
