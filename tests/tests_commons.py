from git import Repo
import time

REPOS_PATHS = ['tests/repo1', 'tests/repo2']
MOCK_REPO_PATH = 'tests/mockrepo'

def import_commits(repo_path: str):
  repo = Repo(repo_path)
  commits_list = []

  for commit in repo.iter_commits(repo.head.ref.name):
    commit_date = commit.committed_date
    date_iso_format = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(commit_date))
    commits_list.append([date_iso_format, commit.message.strip()])

  return commits_list
