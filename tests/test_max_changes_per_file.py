import git
from src import *
import shutil
from tests.tests_commons import import_commits, REPOS_PATHS, MOCK_REPO_PATH
import pytest


def test_max_changes_per_file():
  repos = [git.Repo(repo_path) for repo_path in REPOS_PATHS]
  shutil.rmtree(MOCK_REPO_PATH, ignore_errors=True)
  mock_repo = git.Repo.init(MOCK_REPO_PATH)

  importer = Importer(repos, mock_repo)
  importer.set_max_changes_per_file(5)
  importer.set_keep_commit_messages(True)
  importer.import_repository()

  # TODO next
