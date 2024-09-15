import tarfile
import shutil
from tests_commons import REPOS_PATHS


def pytest_sessionstart(session):
  for repo in REPOS_PATHS:
    with tarfile.open(f"{repo}.tar.gz") as tar:
      shutil.rmtree(repo, ignore_errors=True)
      tar.extractall('tests')


def pytest_sessionfinish(session, exitstatus):
  for repo in REPOS_PATHS:
    shutil.rmtree(repo, ignore_errors=True)
  shutil.rmtree('tests/mockrepo', ignore_errors=True)
  shutil.rmtree('tests/mockrepo_c', ignore_errors=True)
