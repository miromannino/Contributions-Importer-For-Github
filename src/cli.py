import argparse
import sys
import datetime
import git
from src.ImporterFromStats import ImporterFromStats
from src.ImporterFromRepository import ImporterFromRepository


def handle_stats_action(args):
  manager = ImporterFromStats(
      mock_repo_path=args.mock_repo,
      generator_type=args.generator,
      max_commits_per_day=args.max_commits_per_day,
  )

  if args.author:
    manager.set_author(args.author)

  manager.process_csv(args.csv)


def handle_repo_action(args):
  repos = [git.Repo(repo_path) for repo_path in args.repos]
  mock_repo = git.Repo.init(args.mock_repo)
  importer = ImporterFromRepository(repos, mock_repo)

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

  importer.import_repository()


def main():
  parser = argparse.ArgumentParser(description="Unified CLI for Contribution Importer")

  subparsers = parser.add_subparsers(dest="action", required=True)

  # region 'stats' action
  stats_parser = subparsers.add_parser(
    "stats",
    help="Generate commits based on contribution stats."
  )
  stats_parser.add_argument(
    "--csv",
    required=True,
    help="Path to the CSV file containing contributions data."
  )
  stats_parser.add_argument(
    "--mock_repo",
    required=True,
    help="Path to the mock repository."
  )
  stats_parser.add_argument(
    "--generator",
    required=True,
    help="File type for the generator (e.g., '.ts')."
  )
  stats_parser.add_argument(
    "--max-commits-per-day",
    type=int,
    default=10,
    help="Maximum number of commits per day (default: 10)."
  )
  stats_parser.add_argument(
    "--author",
    nargs="+",
    help="Emails of the author to filter commits by."
  )
  # endregion

  # region 'repo' action
  repo_parser = subparsers.add_parser(
    "repo",
    help="Import contributions from repositories."
  )
  repo_parser.add_argument(
    "--repos",
    nargs="+",
    help="Paths to the repositories to import from."
  )
  repo_parser.add_argument(
    "--mock_repo",
    help="Path to the mock repository."
  )
  repo_parser.add_argument(
    "--author",
    nargs="+",
    help="Emails of the author to filter commits by."
  )
  repo_parser.add_argument(
    "--max-commits-per-day",
    nargs=2,
    type=int,
    help="Max commits per day as a range (min max)."
  )
  repo_parser.add_argument(
    "--commit-max-amount-changes",
    type=int,
    help="Max number of changes allowed per commit."
  )
  repo_parser.add_argument(
    "--changes-commits-max-time-backward",
    type=int,
    help="Max time backward for splitting commits (in seconds)."
  )
  repo_parser.add_argument(
    "--ignored-file-types",
    nargs="+",
    help="List of file types to ignore (e.g., .csv, .txt)."
  )
  repo_parser.add_argument(
    "--ignore-before-date",
    type=str,
    help="Ignore commits before this date (YYYY-MM-DD)."
  )
  repo_parser.add_argument(
    "--collapse-multiple-changes",
    action="store_true",
    help="Collapse multiple changes into one."
  )
  repo_parser.add_argument(
    "--keep-commit-messages",
    action="store_true",
    help="Keep original commit messages."
  )
  repo_parser.add_argument(
    "--start-from-last",
    action="store_true",
    help="Start importing from the last commit."
  )
  # endregion

  args = parser.parse_args()

  if args.action == "stats":
    handle_stats_action(args)
  elif args.action == "repo":
    handle_repo_action(args)


if __name__ == "__main__":
  print(sys.argv)
  main()
