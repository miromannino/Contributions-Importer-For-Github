import sys
import git
import datetime
from src import *

repos_path = [
    '/Users/miro/Desktop/Light-1/raadsat-firmware',
]
repos = []
for repo_path in repos_path:
    repos.append(git.Repo(repo_path))

mock_repo_path = '/Users/miro/Dropbox/Dev/repos-contribs/light-1'
mock_repo = git.Repo.init(mock_repo_path)

importer = Importer(repos, mock_repo)
# importer.set_author(['miro.mannino@gmail.com', 'miro.mannino@nyu.edu'])
# importer.set_commit_max_amount_changes(30)
importer.set_max_commits_per_day([9,13])
importer.set_changes_commits_max_time_backward(60*60*24*30)
# importer.set_max_changes_per_file(300)
importer.set_ignored_file_types(['.csv', '.txt', '.pdf', '.log', '.sql', '', '.json'])
importer.set_ignore_before_date(datetime.datetime(2019, 4, 7).timestamp())
importer.set_collapse_multiple_changes_to_one(True)
importer.import_repository()