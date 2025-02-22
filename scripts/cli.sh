export PYTHONPATH=".:$PYTHONPATH"
pipenv run python src/git_import_contributions/cli.py "$@"
