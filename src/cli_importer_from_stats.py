import argparse
from src.ImporterFromStats import ImporterFromStats


def main():
  parser = argparse.ArgumentParser(description="Generate commits based on contribution stats.")

  parser.add_argument(
      "--repo",
      required=True,
      help="Path to the mock repository.",
  )
  parser.add_argument(
      "--csv",
      required=True,
      help="Path to the CSV file containing contributions data.",
  )
  parser.add_argument(
      "--generator",
      required=True,
      help="File type for the generator (e.g., '.ts').",
  )
  parser.add_argument(
      "--max-commits-per-day",
      type=int,
      default=10,
      help="Maximum number of commits per day (default: 10).",
  )

  args = parser.parse_args()

  manager = ImporterFromStats(
      mock_repo_path=args.repo,
      generator_type=args.generator,
      max_commits_per_day=args.max_commits_per_day,
  )

  manager.process_csv(args.csv)


if __name__ == "__main__":
  main()
