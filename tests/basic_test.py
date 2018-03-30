import sys
import git
from git_contributions_importer import *

repo_path = sys.argv[1]
repo = git.Repo(repo_path)

mock_repo_path = sys.argv[2]
mock_repo = git.Repo.init(mock_repo_path)

importer = Importer(repo, mock_repo)
importer.import_repository()