import git
from src import *
import shutil
from tests.tests_commons import import_commits
import pytest
import os

def test_collapse_changes_smaller_filesizes():
  repos_path = ['tests/repo1', 'tests/repo2']
  repos = [git.Repo(repo_path) for repo_path in repos_path]

  mock_repo_path_collapsed = 'tests/mockrepoc'
  mock_repo_collapsed = git.Repo.init(mock_repo_path_collapsed)
  importer = Importer(repos, mock_repo_collapsed)
  importer.set_collapse_multiple_changes_to_one(True)
  importer.set_keep_commit_messages(True)
  importer.import_repository()

  mock_repo_path = 'tests/mockrepo'
  mock_repo = git.Repo.init(mock_repo_path)
  importer = Importer(repos, mock_repo)
  importer.set_collapse_multiple_changes_to_one(False)
  importer.set_keep_commit_messages(True)
  importer.import_repository()

  files_collapsed = os.listdir(mock_repo_path_collapsed)
  files_collapsed = list(filter(lambda f: os.path.isfile(f), files_collapsed))
  files_non_collapsed = os.listdir(mock_repo_path)
  files_non_collapsed = list(filter(lambda f: os.path.isfile(f), files_non_collapsed))
  assert len(files_collapsed) == len(files_non_collapsed)

  for file in files_collapsed:
    assert file in files_non_collapsed
    lines_of_code_collapsed = 0
    lines_of_code_non_collapsed = 0
    with open(os.path.join(mock_repo_path_collapsed, file), 'r') as f:
      lines_of_code_collapsed = len(f.readlines())
    with open(os.path.join(mock_repo_path, file), 'r') as f:
      lines_of_code_non_collapsed = len(f.readlines())
    assert lines_of_code_collapsed <= lines_of_code_non_collapsed

  # shutil.rmtree(mock_repo_collapsed, ignore_errors=True)
  # shutil.rmtree(mock_repo_path, ignore_errors=True)
