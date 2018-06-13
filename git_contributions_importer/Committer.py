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

    ''' performs the commit. date is in seconds from epoch '''
    def commit(self, date, message):
        self.check_readme()
        for file in self.content.get_files():
            self.mock_repo.git.add(os.path.join(self.mock_repo_path, file))
        date_iso_format = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(date))
        os.environ['GIT_AUTHOR_DATE'] = date_iso_format
        os.environ['GIT_COMMITTER_DATE'] = date_iso_format
        try:
            self.mock_repo.git.commit('-m', message, '--allow-empty')
        except git.exc.GitError as e:
            print('Error in commit: ' + str(e))
