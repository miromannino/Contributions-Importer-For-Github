import csv
import os
import subprocess

import git
import pytest

from .tests_commons import MOCK_REPO_PATH

MOCK_REPO_PATH_STATS = f"{MOCK_REPO_PATH}_stats"


def test_cli_stats():
    cli_command = [
        "python",
        "src/cli.py",
        "stats",
        "--csv",
        "tests/stats_1.csv",
        "--mock_repo",
        MOCK_REPO_PATH_STATS,
        "--generator",
        ".ts",
        "--author",
        "Test Name <test@example.com>",
    ]

    subprocess.run(cli_command, check=True)

    # Extract the expected dates from the CSV file
    unique_csv_dates = set()
    expanded_csv_dates = []
    with open("tests/stats_1.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            contributions = int(row["contributions"])
            if contributions > 0:
                unique_csv_dates.add(row["date"])
                for _ in range(contributions):
                    expanded_csv_dates.append(row["date"])

    # Validate that the mock repository contains commits with dates matching the CSV
    mock_repo = git.Repo(MOCK_REPO_PATH_STATS)
    unique_commit_dates = {
        commit.committed_datetime.strftime("%Y-%m-%d") for commit in mock_repo.iter_commits()
    }
    assert sorted(unique_commit_dates) == sorted(
        unique_csv_dates
    ), f"Commit dates do not match. Expected: {sorted(unique_csv_dates)}, Got: {sorted(unique_commit_dates)}"

    # Validates that the amount of commits is as described in the csv
    mock_repo = git.Repo(MOCK_REPO_PATH_STATS)
    commit_dates = [
        commit.committed_datetime.strftime("%Y-%m-%d") for commit in mock_repo.iter_commits()
    ]
    assert sorted(commit_dates) == sorted(
        expanded_csv_dates
    ), f"Commit dates do not match. Expected: {sorted(expanded_csv_dates)}, Got: {sorted(commit_dates)}"
