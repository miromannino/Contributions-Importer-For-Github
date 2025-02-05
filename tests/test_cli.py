import subprocess
import git
import os
import pytest
from tests.tests_commons import REPOS_PATHS, MOCK_REPO_PATH


def test_cli_collapse_changes():
    cli_command_collapsed = [
        "python",
        "src/cli.py",
        "repo",
        "--repos",
        *REPOS_PATHS,
        "--mock_repo",
        MOCK_REPO_PATH + "_c",
        "--author",
        "Test Name <test@example.com>",
        "--collapse-multiple-changes",
        "--keep-commit-messages",
    ]

    cli_command_non_collapsed = [
        "python",
        "src/cli.py",
        "repo",
        "--repos",
        *REPOS_PATHS,
        "--mock_repo",
        MOCK_REPO_PATH,
        "--author",
        "Test Name <test@example.com>",
        "--keep-commit-messages",
    ]

    subprocess.run(cli_command_collapsed, check=True)
    subprocess.run(cli_command_non_collapsed, check=True)

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

    # Validate line count
    for file in files_collapsed:
        assert file in files_non_collapsed
        with open(os.path.join(MOCK_REPO_PATH + "_c", file), "r") as collapsed_file:
            lines_collapsed = len(collapsed_file.readlines())
        with open(os.path.join(MOCK_REPO_PATH, file), "r") as non_collapsed_file:
            lines_non_collapsed = len(non_collapsed_file.readlines())
        assert lines_collapsed < lines_non_collapsed


def test_cli_filter_by_author():
    cli_command = [
        "python",
        "src/cli.py",
        "repo",
        "--repos",
        *REPOS_PATHS,
        "--mock_repo",
        MOCK_REPO_PATH,
        "--author",
        "Test Name <test@example.com>",
    ]

    subprocess.run(cli_command, check=True)

    # Validate that the mock repository contains commits only by the specified author
    mock_repo = git.Repo(MOCK_REPO_PATH)
    for commit in mock_repo.iter_commits():
        assert "test@example.com" in commit.author.email
