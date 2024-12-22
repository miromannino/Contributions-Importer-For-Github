rm -rf dist build *.egg-info
pipenv run python setup.py sdist bdist_wheel
ls dist/
pipenv run twine upload --repository testpypi dist/*
pipenv run pip install --index-url https://test.pypi.org/simple/ git-import-contributions
