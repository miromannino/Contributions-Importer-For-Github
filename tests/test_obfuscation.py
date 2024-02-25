import sys
import git
from src import *
import shutil
from tests.tests_commons import import_commits
import pytest


def test_obfuscation():
  repos_path = ['tests/repo1', 'tests/repo2']
  repos = [git.Repo(repo_path) for repo_path in repos_path]
  mock_repo_path = 'tests/mockrepo'
  shutil.rmtree(mock_repo_path, ignore_errors=True)
  mock_repo = git.Repo.init(mock_repo_path)
  importer = Importer(repos, mock_repo)
  importer.set_keep_commit_messages(False)
  importer.import_repository()

  repos_commits = []
  for repo_path in repos_path:
    repos_commits += import_commits(repo_path)
  repos_commits.sort(key=lambda c: c[0])

  mock_commits = import_commits(mock_repo_path)
  mock_commits.sort(key=lambda c: c[0])

  # test that these are the same list
  assert len(repos_commits) == len(mock_commits)
  for i in range(len(repos_commits)):
    assert repos_commits[i][0] == mock_commits[i][0]
    assert repos_commits[i][1] != mock_commits[i][1]


@pytest.mark.skip()
def test_no_obfuscation():
  repos_path = ['tests/repo1', 'tests/repo2']
  repos = [git.Repo(repo_path) for repo_path in repos_path]
  mock_repo_path = 'tests/mockrepo'
  shutil.rmtree(mock_repo_path, ignore_errors=True)
  mock_repo = git.Repo.init(mock_repo_path)
  importer = Importer(repos, mock_repo)
  importer.set_keep_commit_messages(True)
  importer.import_repository()

  repos_commits = []
  for repo_path in repos_path:
    repos_commits += import_commits(repo_path)
  repos_commits.sort(key=lambda c: c[0])

  mock_commits = import_commits(mock_repo_path)
  mock_commits.sort(key=lambda c: c[0])

  # test that these are the same list
  assert len(repos_commits) == len(mock_commits)
  for i in range(len(repos_commits)):
    assert repos_commits[i][0] == mock_commits[i][0]
    assert repos_commits[i][1] == mock_commits[i][1]
