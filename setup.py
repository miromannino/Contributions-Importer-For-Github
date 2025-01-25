from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setup(
    name='git-import-contributions',
    version='2.0.0-rc1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
      'gitpython'
    ],
    entry_points={
        'console_scripts': [
            'git-import-contributions=src.cli:main',
        ],
    },
    author='Miro Mannino',
    description='This tool helps users to import contributions to GitHub from private git repositories, or from public repositories that are not hosted in GitHub',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/miromannino/Contributions-Importer-For-Github',
)
