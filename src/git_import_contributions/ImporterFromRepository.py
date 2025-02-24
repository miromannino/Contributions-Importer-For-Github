#!/usr/bin/python3

import pathlib
import random
import time

from git_import_contributions.Committer import Committer
from git_import_contributions.commons import extract_name_email
from git_import_contributions.Content import Content
from git_import_contributions.generators import apply_generator
from git_import_contributions.Stats import Stats


class ImporterFromRepository:

    def __init__(self, repos, mock_repo):

        # Maximum amount in the past that the commit can be shifted for. The values are in seconds.
        self.commit_time_max_past = 0

        # The maximum number of changes (line of code changed, added or removed) that a commit can have. Commits with
        # many changes are disadvantaged in GitHub. Most likely these large commits could have been split in many
        # smaller ones. GitHub users that know how contributions are calculated are prone to do several smaller commits
        # instead, while in private repository this could not be necessary, especially in smaller teams.
        # The default is -1, and it is to indicate no limits.
        self.commit_max_changes = -1

        # Maximum number of changes per file. By default for each change (line of code changed, added or removed) a
        # line of mock code is changed. This would limit the number of generated mock code for extreme cases where too
        # many lines of codes are changes (e.g. SQL database dump).
        self.max_changes_per_file = 100

        # If commit_max_changes is a positive number, a commit could be break in several ones.
        # In that case this value decides how long these commits could go in the past. The idea
        # is that a big commit is likely composed by several features that could have been
        # committed in different commits. These changes would have been some time before the actual
        # big commit. The time is in seconds.
        self.changes_commits_max_time_backward = 60 * 60 * 24 * 4  # 4 days as default

        # It allows the importer to collapse several lines of changes to just one per commit,
        # and one per type of file. This allows avoiding excessive growth of files size.
        self.collapse_multiple_changes_to_one = True

        # It allows some types of files to be ignored. For example ['.csv',
        # '.txt', '.pdf', '.log', '.sql', '.json']
        self.ignored_file_types = []

        # In case the settings above are too crazy it doesn't commit too much (the
        # array is to have a random value instead of a specific one)
        self.max_commits_per_day = [10, 15]

        # Ignore all the commits before this date, in order to analyze same repositories over time
        self.ignore_before_date = None

        # Ignore all the commits before last commit
        self.start_from_last = False

        # Author to analyze. If None commits from any author will be imported. Author is given as email
        # This could be an array of email in case, depending on the repository,
        # the author has different emails.
        self.author = None

        # Keep the original commit message if true
        self.keep_commit_messages = False

        self.repos = repos
        self.mock_repo = mock_repo
        self.content = Content(mock_repo.working_tree_dir)
        self.committer = Committer(mock_repo.working_tree_dir, self.content)

    def import_repository(self):
        commits_for_last_day = 0

        if self.start_from_last:
            last_committed_date = self.committer.get_last_commit_date()
            print(
                "\nStarting from last commit: "
                + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(last_committed_date))
            )
        else:
            print("\nStarting")
            last_committed_date = 0

        author_emails = (
            (
                [a.email for a in self.author]
                if isinstance(self.author, list)
                else [self.author.email]
            )
            if self.author
            else []
        )

        for c in self.get_all_commits(last_committed_date + 1):
            print(
                "Analyze commit at "
                + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(c.committed_date))
            )
            print('  msg:" ' + c.message + '"')

            if len(author_emails) > 0 and c.author.email not in author_emails:
                print("    Commit skipped because the author is: " + c.author.email)
                continue

            committed_date = c.committed_date
            if self.commit_time_max_past > 0:
                committed_date -= int(random.random() * self.commit_time_max_past)
                print(
                    "    Commit date changed to: "
                    + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(c.committed_date))
                )

            stats = Stats(self.max_changes_per_file)
            self.get_changes(c, stats)
            print("    Commit changes: " + str(stats))
            for broken_stats in stats.iterate_insertions(self.commit_max_changes):
                if self.collapse_multiple_changes_to_one:
                    for k in broken_stats.insertions.keys():
                        broken_stats.insertions[k] = 1
                    for k in broken_stats.deletions.keys():
                        broken_stats.deletions[k] = 1
                print("    Apply changes: " + str(broken_stats))
                apply_generator(self.content, broken_stats)
                self.content.save()
                break_committed_date = committed_date
                if broken_stats != stats:
                    max_past = self.changes_commits_max_time_backward
                    if last_committed_date != 0:
                        max_past = min(break_committed_date - last_committed_date, max_past)
                    break_committed_date -= int(
                        random.random() * (max_past / 3) + (max_past / 3 * 2)
                    )
                if time.strftime("%Y-%m-%d", time.localtime(last_committed_date)) == time.strftime(
                    "%Y-%m-%d", time.localtime(break_committed_date)
                ):
                    commits_for_last_day += 1
                    if (
                        commits_for_last_day
                        > random.random()
                        * (self.max_commits_per_day[1] - self.max_commits_per_day[0])
                        + self.max_commits_per_day[0]
                    ):
                        print(
                            "    Commit skipped because the maximum amount of commit for "
                            + time.strftime("%Y-%m-%d", time.localtime(last_committed_date))
                            + " exceeded"
                        )
                        continue
                else:
                    commits_for_last_day = 1
                print(
                    "    Commit at: "
                    + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(break_committed_date))
                )
                print("keep commit messages" + str(self.keep_commit_messages))
                if self.keep_commit_messages:
                    message = c.message
                else:
                    message = (
                        "add code in files types: "
                        + ",".join(broken_stats.insertions.keys())
                        + "\nremove code in files types: "
                        + ",".join(broken_stats.deletions.keys())
                    )
                self.committer.commit(break_committed_date, message, self.author)
                last_committed_date = break_committed_date

    def get_all_commits(self, ignore_before_date):
        """iter commits coming from any branch"""
        commits = []
        s = set()  # to remove duplicated commits from other branches
        for repo in self.repos:
            for b in repo.branches:
                for c in repo.iter_commits(b.name):
                    if c.committed_date < ignore_before_date or (
                        self.ignore_before_date is not None
                        and c.committed_date < self.ignore_before_date
                    ):
                        continue
                    if c.hexsha not in s:
                        s.add(c.hexsha)
                        commits.append(c)
        commits.sort(key=lambda c: c.committed_date)
        return commits

    def get_changes(self, commit, stats):
        """for a specific commit it gets all the changed files"""
        for k, v in commit.stats.files.items():
            ext = pathlib.Path(k).suffix
            if ext in self.ignored_file_types:
                continue
            if v["insertions"] > 0:
                stats.add_insertions(ext, v["insertions"])
            if v["deletions"] > 0:
                stats.add_deletions(ext, v["deletions"])

    def set_commit_time_max_past(self, value):
        self.commit_time_max_past = value

    def set_commit_max_amount_changes(self, max_amount):
        self.commit_max_changes = max_amount

    def set_changes_commits_max_time_backward(self, max_amount):
        self.changes_commits_max_time_backward = max_amount

    def set_collapse_multiple_changes_to_one(self, value):
        self.collapse_multiple_changes_to_one = value

    def set_ignored_file_types(self, file_types):
        self.ignored_file_types = file_types

    def set_max_changes_per_file(self, value):
        self.max_changes_per_file = value

    def set_max_commits_per_day(self, value):
        self.max_commits_per_day = value

    def set_ignore_before_date(self, value):
        self.ignore_before_date = value

    def set_start_from_last(self, value):
        self.start_from_last = value

    def set_author(self, author: str | list):
        """
        Set author from a string "Some Name <some.email@example.com>" or a list of such strings.
        """
        if isinstance(author, list):
            self.author = [
                extract_name_email(a) for a in author if extract_name_email(a) is not None
            ]
        else:
            self.author = extract_name_email(author)

    def set_keep_commit_messages(self, value):
        self.keep_commit_messages = value
