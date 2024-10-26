import argparse
import datetime
import git
from src.ImporterFromRepository import ImporterFromRepository


def main():
  parser = argparse.ArgumentParser(description="Contributions Importer for Git CLI")

  parser.add_argument(
      "repos",
      nargs="+",
      help="Paths to the repositories to import from."
  )

  parser.add_argument(
      "mock_repo_path",
      help="Path to the mock repository."
  )

  # Optional arguments
  parser.add_argument(
      "--author",
      nargs="+",
      help="Emails of the author to filter commits by."
  )
  parser.add_argument(
      "--max-commits-per-day",
      nargs=2,
      type=int,
      help="Max commits per day as a range (min max)."
  )
  parser.add_argument(
      "--commit-max-amount-changes",
      type=int,
      help="Max number of changes allowed per commit."
  )
  parser.add_argument(
      "--changes-commits-max-time-backward",
      type=int,
      help="Max time backward for splitting commits (in seconds)."
  )
  parser.add_argument(
      "--ignored-file-types",
      nargs="+",
      help="List of file types to ignore (e.g., .csv, .txt)."
  )
  parser.add_argument(
      "--ignore-before-date",
      type=str,
      help="Ignore commits before this date (YYYY-MM-DD)."
  )
  parser.add_argument(
      "--collapse-multiple-changes",
      action="store_true",
      help="Collapse multiple changes into one."
  )
  parser.add_argument(
      "--keep-commit-messages",
      action="store_true",
      help="Keep original commit messages."
  )
  parser.add_argument(
      "--start-from-last",
      action="store_true",
      help="Start importing from the last commit."
  )

  args = parser.parse_args()

  # Initialize repositories
  repos = [git.Repo(repo_path) for repo_path in args.repos]
  mock_repo = git.Repo.init(args.mock_repo_path)

  # Initialize Importer
  importer = ImporterFromRepository(repos, mock_repo)

  # Apply settings
  if args.author:
    importer.set_author(args.author)
  if args.max_commits_per_day:
    importer.set_max_commits_per_day([int(v) for v in args.max_commits_per_day])
  if args.commit_max_amount_changes is not None:
    importer.set_commit_max_amount_changes(args.commit_max_amount_changes)
  if args.changes_commits_max_time_backward is not None:
    importer.set_changes_commits_max_time_backward(args.changes_commits_max_time_backward)
  if args.ignored_file_types:
    importer.set_ignored_file_types(args.ignored_file_types)
  if args.ignore_before_date:
    ignore_date = datetime.datetime.strptime(args.ignore_before_date, "%Y-%m-%d")
    importer.set_ignore_before_date(ignore_date.timestamp())
  importer.set_collapse_multiple_changes_to_one(args.collapse_multiple_changes)
  importer.set_keep_commit_messages(args.keep_commit_messages)
  importer.set_start_from_last(args.start_from_last)

  # Start import
  importer.import_repository()


if __name__ == "__main__":
  main()
