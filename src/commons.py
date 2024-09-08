
import git

def is_valid_git_repo(path):
    try:
      _ = git.Repo(path).git_dir  # Attempt to access the .git directory
      return True
    except git.exc.InvalidGitRepositoryError:
      return False
    except git.exc.NoSuchPathError:
      return False
