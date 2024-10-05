import csv
import datetime as dt
import git
import time
import random

from .commons import is_valid_git_repo

from .Committer import Committer
from .Content import Content
from .generators import apply_generator
from .Stats import Stats

DEFAULT_TIME_RANGE = (9, 18)
DEFAULT_MAX_COMMITS_PER_DAY = 10
DEFAULT_MAX_CHANGES_PER_FILE = 10
DEFAULT_JITTER = (((DEFAULT_TIME_RANGE[1] - DEFAULT_TIME_RANGE[0]
                    ) / DEFAULT_MAX_COMMITS_PER_DAY) * 60 * 60) / 2


class ImporterFromStats:

  def __init__(
          self, mock_repo_path,
          generator_type,
          max_changes_per_file=DEFAULT_MAX_CHANGES_PER_FILE,
          max_commits_per_day=DEFAULT_MAX_COMMITS_PER_DAY,
          commit_time_range=DEFAULT_TIME_RANGE,
          jitter=DEFAULT_JITTER):
    """
    :param mock_repo_path: Path to the mock repository.
    :param generator_type: File type for the generator (e.g., ".ts").
    :param max_changes_per_file: Number of max changes per file on each commit
    :param max_commits_per_day: max commits per day.
    """
    if is_valid_git_repo(mock_repo_path):
      self.repo = git.Repo(mock_repo_path)
    else:
      raise Exception(f"The path {mock_repo_path} is not a valid Git repository.")
    self.content = Content(self.repo.working_tree_dir)
    self.committer = Committer(self.repo, self.content)
    self.generator_type = generator_type
    self.max_changes_per_file = max_changes_per_file
    self.max_commits_per_day = max_commits_per_day
    self.commit_time_range = commit_time_range
    self.jitter = jitter

  def count_commits_for_date(self, date):
    """
    Count the number of commits for a given date.
    :param date: Date in 'YYYY-MM-DD' format.
    :return: Number of commits for the given date.
    """
    try:
      log_output = self.repo.git.log('--pretty=format:%ad', '--date=short')
      committed_dates = log_output.split('\n')
      return committed_dates.count(date)
    except BaseException:
      return 0

  def parse_date(self, date_str):
    try:
      date = dt.datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
      raise ValueError(f"Invalid date format: {date_str}. Expected 'YYYY-MM-DD'.")
    return date

  def process_csv(self, file_path):
    """
    Process a CSV file and create commits based on the contributions data.
    :param file_path: Path to the CSV file.
    """
    with open(file_path, "r") as file:
      reader = csv.reader(file)
      next(reader)  # Skip the header

      # Read all rows to calculate max_commits_in_stats
      rows = [row for row in reader]
      max_commits_in_stats = max(int(row[0]) for row in rows)

      for row in rows:
        target_commits = int(row[0])  # Target number of commits for the date
        date_str = row[1]
        print(target_commits, "commits at", date_str)
        date = self.parse_date(date_str)

        # Normalize the number of commits for the day
        scaled_commits = int(
            (target_commits / max_commits_in_stats) * self.max_commits_per_day
        )
        scaled_commits = max(
            0, min(
                scaled_commits, self.max_commits_per_day))

        # Count existing commits for the date
        existing_commits = self.count_commits_for_date(date_str)

        # Calculate missing commits
        missing_commits = scaled_commits - existing_commits
        if missing_commits > 0:
          print(f"Creating {missing_commits} commits for {date_str}")
          self.create_commits(date, missing_commits)
        else:
          print(f"No additional commits needed for {date_str}")

  def create_commits(self, date, count):
    """
    Create the specified number of commits for a given date, generating content using apply_generator.
    :param date: Date for the commits (datetime object).
    :param count: Number of commits to create.
    """
    # Define the commit time hours (for example working hours)
    start_time = dt.datetime.combine(date, dt.time(self.commit_time_range[0], 0, 0))
    end_time = dt.datetime.combine(date, dt.time(self.commit_time_range[1], 0, 0))

    # Calculate the time interval between commits
    working_seconds = (end_time - start_time).total_seconds()
    interval = working_seconds // count if count > 0 else 0

    current_time = start_time
    for i in range(count):
      # Generate stats and apply generator
      stats = Stats()
      stats.insertions[self.generator_type] = random.randint(1, self.max_changes_per_file)
      stats.deletions[self.generator_type] = random.randint(1, self.max_changes_per_file)
      apply_generator(self.content, stats)
      self.content.save()

      # Convert current_time to a Unix timestamp
      commit_date = int(time.mktime(current_time.timetuple()) + random.randint(0, int(self.jitter)))

      # Commit changes
      message = (
          f"Add code in files of type: {','.join(stats.insertions.keys())}\n"
          f"Remove code in files of type: {','.join(stats.deletions.keys())}"
      )
      self.committer.commit(commit_date, message)
      print(
        f"Commit created for {current_time.strftime('%Y-%m-%d')} with message:\n{message}")

      # Increment current_time by the interval
      current_time += dt.timedelta(seconds=interval)
