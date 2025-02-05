import os
import shutil
import git
import pytest
from src.ImporterFromRepository import ImporterFromRepository
from tests.tests_commons import REPOS_PATHS, MOCK_REPO_PATH


@pytest.fixture
def setup_mock_repos():
    # Cleanup existing mock repos
    shutil.rmtree(MOCK_REPO_PATH, ignore_errors=True)
    shutil.rmtree(MOCK_REPO_PATH + "_c", ignore_errors=True)
    yield
    # Cleanup after the test
    shutil.rmtree(MOCK_REPO_PATH, ignore_errors=True)
    shutil.rmtree(MOCK_REPO_PATH + "_c", ignore_errors=True)


def test_collapse_changes_smaller_filesizes(setup_mock_repos):
    # Initialize repositories
    repos = [git.Repo(repo_path) for repo_path in REPOS_PATHS]

    # Test with collapse enabled
    mock_repo_collapsed = git.Repo.init(MOCK_REPO_PATH + "_c")
    importer_collapsed = ImporterFromRepository(repos, mock_repo_collapsed)
    importer_collapsed.set_collapse_multiple_changes_to_one(True)
    importer_collapsed.set_keep_commit_messages(True)
    importer_collapsed.import_repository()

    # Test with collapse disabled
    mock_repo = git.Repo.init(MOCK_REPO_PATH)
    importer_non_collapsed = ImporterFromRepository(repos, mock_repo)
    importer_non_collapsed.set_collapse_multiple_changes_to_one(False)
    importer_non_collapsed.set_keep_commit_messages(True)
    importer_non_collapsed.import_repository()

    # Get lists of files in each mock repo, excluding README.md
    files_collapsed = [
        f
        for f in os.listdir(MOCK_REPO_PATH + "_c")
        if os.path.isfile(os.path.join(MOCK_REPO_PATH + "_c", f)) and not f.endswith(".md")
    ]
    files_non_collapsed = [
        f
        for f in os.listdir(MOCK_REPO_PATH)
        if os.path.isfile(os.path.join(MOCK_REPO_PATH, f)) and not f.endswith(".md")
    ]

    # Assert same number of files
    assert len(files_collapsed) == len(files_non_collapsed)

    # Compare line counts for each file
    for file in files_collapsed:
        assert file in files_non_collapsed
        with open(os.path.join(MOCK_REPO_PATH + "_c", file), "r") as collapsed_file:
            lines_collapsed = len(collapsed_file.readlines())
        with open(os.path.join(MOCK_REPO_PATH, file), "r") as non_collapsed_file:
            lines_non_collapsed = len(non_collapsed_file.readlines())
        assert lines_collapsed < lines_non_collapsed
