import sys
import git
from git_contributions_importer import *

repos_path = [
    '/path/to/Project1',
    '/path/to/Project2',
    '/path/to/Project3',
]
repos = []
for repo_path in repos_path:
    repos.append(git.Repo(repo_path))

mock_repo_path = '/path/to/destination/private/repo'
mock_repo = git.Repo.init(mock_repo_path)

importer = Importer(repos, mock_repo)
importer.set_author(['your.email@domain.com', 'your.other.email@domain.com'])
importer.set_commit_max_amount_changes(15)
importer.set_changes_commits_max_time_backward(60*60*24*30)
importer.set_max_changes_per_file(60)
importer.ignore_file_types(['.csv', '.txt', '.pdf', '.xsl', '.sql'])
importer.set_collapse_multiple_changes_to_one(True)
importer.import_repository()