#!/usr/bin/python3

import git
import time
import os
import shutil


class Committer:

    def __init__(self, mock_repo, content):
        self.mock_repo = mock_repo
        self.mock_repo_path = self.mock_repo.working_tree_dir
        self.content = content

    def check_readme(self):
        readme_path = os.path.dirname(__file__) + '/README.md'
        mockrepo_readme_path = self.mock_repo_path + '/README.md'
        shutil.copyfile(readme_path, mockrepo_readme_path)
        self.mock_repo.git.add(self.mock_repo_path + '/README.md')

    ''' returns the last commit date in ms from epoch'''
    def get_last_commit_date(self):
        last_commit_date = 0
        for b in self.mock_repo.branches:
            for c in self.mock_repo.iter_commits(b.name):
                if c.committed_date > last_commit_date:
                    if (c.message.startswith("add code in files types:")
                            or c.message.startswith("removed code in files types:")
                            or c.message.startswith("remove code in files types:")):
                        last_commit_date = c.committed_date
        return last_commit_date

    ''' performs the commit. date is in seconds from epoch '''
    def commit(self, date, message):
        self.check_readme()
        for file in self.content.get_files():
            self.mock_repo.git.add(os.path.join(self.mock_repo_path, file))
        date_iso_format = time.strftime("%Y-%m-%d %H:%M:%S +0000", time.gmtime(date))
        os.environ['GIT_AUTHOR_DATE'] = date_iso_format
        os.environ['GIT_COMMITTER_DATE'] = date_iso_format
        try:
            self.mock_repo.git.commit('-m', message, '--allow-empty')
        except git.exc.GitError as e:
            print('Error in commit: ' + str(e))
