import shutil
import sys

import git

from git_import_contributions.ImporterFromRepository import ImporterFromRepository
from src import *

from .tests_commons import MOCK_REPO_PATH, REPOS_PATHS, import_commits


def test_obfuscation():
    repos = [git.Repo(repo_path) for repo_path in REPOS_PATHS]
    shutil.rmtree(MOCK_REPO_PATH, ignore_errors=True)
    mock_repo = git.Repo.init(MOCK_REPO_PATH)
    importer = ImporterFromRepository(repos, mock_repo)
    importer.set_keep_commit_messages(False)
    importer.import_repository()

    repos_commits = []
    for repo_path in REPOS_PATHS:
        repos_commits += import_commits(repo_path)
    repos_commits.sort(key=lambda c: c[0])

    mock_commits = import_commits(MOCK_REPO_PATH)
    mock_commits.sort(key=lambda c: c[0])

    # test that these are the same list
    assert len(repos_commits) == len(mock_commits)
    for i in range(len(repos_commits)):
        assert repos_commits[i][0] == mock_commits[i][0]
        assert repos_commits[i][1] != mock_commits[i][1]


def test_no_obfuscation():
    repos = [git.Repo(repo_path) for repo_path in REPOS_PATHS]
    shutil.rmtree(MOCK_REPO_PATH, ignore_errors=True)
    mock_repo = git.Repo.init(MOCK_REPO_PATH)
    importer = ImporterFromRepository(repos, mock_repo)
    importer.set_keep_commit_messages(True)
    importer.import_repository()

    repos_commits = []
    for repo_path in REPOS_PATHS:
        repos_commits += import_commits(repo_path)
    repos_commits.sort(key=lambda c: c[0])

    mock_commits = import_commits(MOCK_REPO_PATH)
    mock_commits.sort(key=lambda c: c[0])

    # test that these are the same list
    assert len(repos_commits) == len(mock_commits)
    for i in range(len(repos_commits)):
        assert repos_commits[i][0] == mock_commits[i][0]
        assert repos_commits[i][1] == mock_commits[i][1]
