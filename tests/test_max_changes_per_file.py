import os
import shutil

import git

from git_import_contributions.ImporterFromRepository import ImporterFromRepository
from src import *

from .tests_commons import MOCK_REPO_PATH, REPOS_PATHS, import_commits


def test_max_changes_per_file():
    repos = [git.Repo(repo_path) for repo_path in REPOS_PATHS]
    shutil.rmtree(MOCK_REPO_PATH, ignore_errors=True)
    mock_repo = git.Repo.init(MOCK_REPO_PATH)

    shutil.rmtree(MOCK_REPO_PATH + "_c", ignore_errors=True)
    mock_repo_collapsed = git.Repo.init(MOCK_REPO_PATH + "_c")
    importer = ImporterFromRepository(repos, mock_repo_collapsed)
    importer.set_max_changes_per_file(1)
    importer.set_keep_commit_messages(True)
    importer.import_repository()

    shutil.rmtree(MOCK_REPO_PATH, ignore_errors=True)
    mock_repo = git.Repo.init(MOCK_REPO_PATH)
    importer = ImporterFromRepository(repos, mock_repo)
    importer.set_max_changes_per_file(1)
    importer.set_keep_commit_messages(True)
    importer.import_repository()

    files_collapsed = os.listdir(MOCK_REPO_PATH + "_c")
    files_collapsed = list(filter(lambda f: os.path.isfile(f), files_collapsed))
    files_collapsed.remove("README.md")
    files_non_collapsed = os.listdir(MOCK_REPO_PATH)
    files_non_collapsed = list(filter(lambda f: os.path.isfile(f), files_non_collapsed))
    files_non_collapsed.remove("README.md")
    assert len(files_collapsed) == len(files_non_collapsed)

    for file in files_collapsed:
        assert file in files_non_collapsed
        lines_of_code_collapsed = 0
        lines_of_code_non_collapsed = 0
        with open(os.path.join(MOCK_REPO_PATH + "_c", file)) as f:
            lines_of_code_collapsed = len(f.readlines())
        with open(os.path.join(MOCK_REPO_PATH, file)) as f:
            lines_of_code_non_collapsed = len(f.readlines())
        print(
            "Checking",
            file,
            "collapsed:",
            lines_of_code_collapsed,
            "non_collapsed:",
            lines_of_code_non_collapsed,
        )
        assert lines_of_code_collapsed < lines_of_code_non_collapsed
