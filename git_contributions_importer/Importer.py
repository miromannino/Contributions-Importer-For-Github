#!/usr/bin/python3

import pathlib
from random import random

import time

from .Committer import Committer
from .Content import Content
from .generators import apply


class Importer:

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
        # big commit. The time is in seconds. '''
        self.changes_commits_max_time_backward = 60*60*24*4  # 4 days as default

        # It allows the importer to collapse several lines of changes to just one per commit,
        # and one per type of file. This allows avoiding excessive growth of files size.
        self.collapse_multiple_changes_to_one = True

        # Author to analyse. If None commits from any author will be imported. Author is given as email
        # This could be an array of email in case, depending on the repository, the author has different emails.
        self.author = None

        self.repos = repos
        self.mock_repo = mock_repo
        self.content = Content(mock_repo.working_tree_dir)
        self.committer = Committer(mock_repo, self.content)

    def import_repository(self):
        last_committed_date = 0

        for c in self.get_all_commits():
            print('\nAnalysing commit at ' + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(c.committed_date)))

            if self.author is not None:
                if isinstance(self.author, list):
                    found = False
                    for a in self.author:
                        if c.author.email == a: found = True
                else:
                    found = c.author.email == self.author
                if not found:
                    print('    Commit skipped because the author is: ' + c.author.email)
                    continue

            committed_date = c.committed_date
            if self.commit_time_max_past > 0:
                committed_date -= int(random() * self.commit_time_max_past)
                print('    Commit date changed to: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(c.committed_date)))

            stats = Stats(self.max_changes_per_file)
            self.get_changes(c, stats)
            print('    Commit changes: ' + str(stats))
            for broken_stats in stats.iterate_insertions(self.commit_max_changes):
                if self.collapse_multiple_changes_to_one:
                    for k in broken_stats.insertions.keys():
                        broken_stats.insertions[k] = 1
                    for k in broken_stats.deletions.keys():
                        broken_stats.deletions[k] = 1
                print('    Apply changes: ' + str(broken_stats))
                apply(self.content, broken_stats)
                self.content.save()
                break_committed_date = committed_date
                if broken_stats != stats:
                    if last_committed_date == 0:
                        max_past = self.changes_commits_max_time_backward
                    else:
                        max_past = min(break_committed_date - last_committed_date,
                                       self.changes_commits_max_time_backward)
                    break_committed_date -= int(random() * (max_past / 3) + (max_past / 3 * 2))
                print('    Commit at: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(break_committed_date)))
                message = 'add code in files types: ' + ','.join(broken_stats.insertions.keys()) + \
                          '\nremoved code in files types: ' + ','.join(broken_stats.deletions.keys())
                self.committer.commit(break_committed_date, message)
                last_committed_date = break_committed_date

    ''' iter commits coming from any branch'''

    def get_all_commits(self):
        commits = []
        s = set()  # to remove duplicated commits form other branches
        for repo in self.repos:
            for b in repo.branches:
                for c in repo.iter_commits(b.name):
                    if c.hexsha not in s:
                        s.add(c.hexsha)
                        commits.append(c)
        commits.sort(key=lambda c: c.committed_date)
        return commits

    ''' for a specific commit it gets all the changed files '''

    def get_changes(self, commit, stats):
        for k, v in commit.stats.files.items():
            ext = pathlib.Path(k).suffix
            if v['insertions'] > 0:
                stats.add_insertions(ext, v['insertions'])
            if v['deletions'] > 0:
                stats.add_deletions(ext, v['deletions'])

    def set_commit_time_max_past(self, value):
        self.commit_time_max_past = value

    def set_commit_max_amount_changes(self, max_amount):
        self.commit_max_changes = max_amount

    def set_changes_commits_max_time_backward(self, max_amount):
        self.changes_commits_max_time_backward = max_amount

    def set_collapse_multiple_changes_to_one(self, value):
        self.collapse_multiple_changes_to_one = value

    def set_max_changes_per_file(self, value):
        self.max_changes_per_file = value

    def set_author(self, author):
        self.author = author


class Stats:

    def __init__(self, max_changes_per_file=-1):
        self.insertions = {}
        self.deletions = {}
        self.max_changes_per_file = max_changes_per_file

    def add_insertions(self, ext, num):
        if ext not in self.insertions:
            self.insertions[ext] = num
        else:
            self.insertions[ext] = self.insertions[ext] + num
        if 0 < self.max_changes_per_file < self.insertions[ext]:
            self.insertions[ext] = self.max_changes_per_file

    def add_deletions(self, ext, num):
        if ext not in self.deletions:
            self.deletions[ext] = num
        else:
            self.deletions[ext] = self.deletions[ext] + num
        if 0 < self.max_changes_per_file < self.deletions[ext]:
            self.deletions[ext] = self.max_changes_per_file

    def iterate_insertions(self, max_changes=-1):
        if max_changes <= 0:
            yield self
            return
        broken_stats = Stats()
        acc = 0
        for k, v in self.insertions.items():
            while v > 0:
                changes = min(max_changes - acc, v)
                v -= changes
                broken_stats.insertions[k] = changes
                acc += changes
                if acc >= max_changes:
                    yield broken_stats
                    broken_stats.insertions = {}
                    acc = 0
        for k, v in self.deletions.items():
            while v > 0:
                changes = min(max_changes - acc, v)
                v -= changes
                broken_stats.deletions[k] = changes
                acc += changes
                if acc >= max_changes:
                    yield broken_stats
                    broken_stats.deletions = {}
                    acc = 0
        if len(broken_stats.insertions) > 0 or len(broken_stats.deletions) > 0:
            yield broken_stats

    def __str__(self):
        return 'insertions: ' + str(self.insertions) \
               + ' deletions: ' + str(self.deletions)
