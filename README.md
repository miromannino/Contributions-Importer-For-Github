# Contributions Importer for GitHub

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/miromannino/Contributions-Importer-For-Github/blob/main/LICENSE) [![pypi version](https://img.shields.io/pypi/v/git-import-contributions.svg)](https://pypi.org/project/git-import-contributions/) [![Build and Tests](https://github.com/miromannino/Contributions-Importer-For-Github/actions/workflows/tests.yaml/badge.svg)](https://github.com/miromannino/Contributions-Importer-For-Github/actions/workflows/tests.yaml) [![Static Code Analysis](https://github.com/miromannino/Contributions-Importer-For-Github/actions/workflows/static-analysis.yaml/badge.svg)](https://github.com/miromannino/Contributions-Importer-For-Github/actions/workflows/static-analysis.yaml) [![Code Security Analysis](https://github.com/miromannino/Contributions-Importer-For-Github/actions/workflows/security.yaml/badge.svg)](https://github.com/miromannino/Contributions-Importer-For-Github/actions/workflows/security.yaml)

This tool helps users to import contributions to GitHub from private git repositories, or from public repositories that are not hosted in GitHub.

<p style="margin: 20px" align="center">
<img src="https://github.com/miromannino/contributions-importer-for-github/blob/resources/fig1.webp?raw=true" />
</p>

## How it Works

In its simplest case, this tool copies all commits from a source git repository to a mock git repository. Each copied commit will report the same commit date, but the original code is not copied, nor is the commit message.

<p style="margin: 20px" align="center">
<img src="https://github.com/miromannino/contributions-importer-for-github/blob/resources/fig0.png?raw=true" />
</p>

_Contributions Importer_ will create instead mock code to report which languages have been used in the source repository.

You can also have multiple source git repositories as well to report activities from several private git repositories.

## Reasons

GitHub shows contributions statistics of its users. There are [several reasons](https://github.com/isaacs/github/issues/627) why this feature could be debatable.

Moreover, this mechanism only rewards developers who work on GitHub-maintained repositories.

Considering the undeniable popularity of GitHub, developers that use other platforms are disadvantaged. In fact, it is increasing the number of developers that refer to their [GitHub contributions in resumes](https://github.com/resume/resume.github.com). Similarly, recruiters [may use GitHub to find talent](https://www.socialtalent.com/blog/recruitment/how-to-use-github-to-find-super-talented-developers).

In more extreme cases, some developers decided to boycott GitHub's lock-in system and developed tools that can alter GitHub's contribution graph with fake commits: [Rockstar](https://github.com/avinassh/rockstar) and [Vanity text for GitHub](https://github.com/ihabunek/github-vanity) are good examples.

Instead, [Contributions Importer for GitHub](https://github.com/miromannino/contributions-importer-for-github) aims to generate an overall realistic activity overview.

### Installation

To install using `pip`:

```bash
pip install git-import-contributions
```

Using `brew`:

```bash
brew tap miromannino/tap
brew install git-import-contributions
```

### Usage

The `git-import-contributions` CLI provides an interface for importing contributions into a mock Git repository using data from either a CSV file or other repositories. This tool is designed for developers and operates exclusively via the command line.

The `git-import-contributions` CLI has two main modes of operation: **stats** and **repo**.

#### General Syntax

```bash
git-import-contributions <action> [options]
```

### Actions

#### 1. Stats Mode

Generates commits in a mock repository based on a CSV file containing contribution statistics.

**Command:**

```bash
git-import-contributions stats \
    --csv <path-to-csv> \
    --mock_repo <mock-repo-path> \
    --generator <generator-type>
```

**Options:**

- `--csv <path>`: Path to the CSV file containing contribution statistics.
- `--mock_repo <path>`: Path to the mock Git repository.
- `--generator <file-extension>`: Type of generator to use for file creation (e.g., `.ts`).

**Other Optional Options:**

- `--max-commits-per-day <number>`: Maximum number of commits per day (default: 10).
- `--author <email>`: Filter commits by the specified author(s) (optional). Accepts multiple email addresses.

**Example:**

The contributions are saved in a CSV file `data.csv` as the following:

```csv
contributions,date
4,2024-08-05
2,2024-08-09
0,2024-08-10
0,2024-08-11
```

Let's import:

```bash
git-import-contributions stats \
    --csv data.csv \
    --mock_repo mock-repo \
    --generator .py \
    --max-commits-per-day 5 \
    --author "example@example.com"
```

#### 2. Repo Mode

Imports contributions into a mock repository by analyzing one or more existing repositories.

**Command:**

```bash
git-import-contributions repo \
    --repos <repo-paths> \
    --mock_repo <mock-repo-path>
```

**Options:**

- `--repos <paths>`: Paths to the repositories to analyze (required). Accepts multiple paths.
- `--mock_repo <path>`: Path to the mock Git repository (required).

**Other Optional Options:**

- `--author <email>`: Filter commits by the specified author(s) (optional). Accepts multiple email addresses.
- `--max-commits-per-day <min max>`: Set a range for the number of commits per day (optional).
- `--commit-max-amount-changes <number>`: Limit the number of changes per commit (optional).
- `--changes-commits-max-time-backward <seconds>`: Maximum time backward for splitting large commits (optional).
- `--ignored-file-types <types>`: List of file types to ignore (e.g., `.csv`, `.txt`) (optional).
- `--ignore-before-date <YYYY-MM-DD>`: Ignore commits before this date (optional).
- `--collapse-multiple-changes`: Collapse multiple changes into one per type of file (optional).
- `--keep-commit-messages`: Keep original commit messages instead of using mocked ones (optional).
- `--start-from-last`: Start importing from the last commit in the mock repository (optional).

**Example:**

The repositories to analyze are in folder `repo1` and `repo2`.
The mock repo is instead in the `mock-repo` folder.

```bash
git-import-contributions repo \
    --repos repo1 repo2 \
    --mock_repo mock-repo \
    --author "dev@example.com" \
    --max-commits-per-day 5 10 \
    --ignore-before-date 2020-01-01
```

### Advanced Features

The `repo` mode supports additional options to control how contributions are imported:

1. **Masking Commit Time**
   Commit times can be randomized using `--changes-commits-max-time-backward`.

2. **Limiting Changes per Commit**
   Use `--commit-max-amount-changes` to set a cap on the number of changes in a single commit.

3. **Incremental Imports**
   Use `--start-from-last` to import contributions incrementally starting from the most recent commit in the mock repository

4. **Ignoring Commits Before a Date**
   Use `--ignore-before-date` to skip commits older than a specific date.

### Help

To view the full list of commands and options:

```bash
git-import-contributions --help
```

For specific actions:

```bash
git-import-contributions stats --help
git-import-contributions repo --help
```

### Other good tutorials about this project

- [How I Restored My Git Contributions](https://medium.com/@razan.joc/how-i-restored-my-git-contributions-7ddb27f06d4e) by Rajan Joshi
- [Import Contributions from Bitbucket to GitHub](https://medium.com/@danielnmai/import-contributions-from-bitbucket-to-github-afd9160eaf6d) by Daniel Mai

## Contributing

We welcome contributions from the community. Please fork the repository, create a new branch, and submit a pull request with your changes.

Ensure all tests pass and update documentation as needed.

### Install dev dependencies

To install dev dependencies

```bash
pipenv install --dev
```

Install the pre-commit scripts with:

```bash
pipenv run pre-commit install
```

### Code style

Regarding code styles like indentation and whitespace, **follow the conventions you see used in the source already.**

The project uses `black` as auto formatter using the settings in `pyproject.toml`.

### Submitting pull requests

- Create a new branch; avoid working directly in the `master` branch.
- Write failing tests for the changes you plan to implement.
- Make the necessary changes to fix the issues.
- Ensure all tests, including the new ones, pass successfully.
- Update the documentation to reflect any modifications.
- Push your changes to your fork and submit a pull request.

### Use from source

Make sure you have first of all `pipenv` installed and install all required dependencies:

```bash
./scripts/install-dependencies.sh
```

You can then use the CLI with:

```bash
./scripts/cli.sh --help
```

### Tests

In order to run tests:

Make sure you have first of all `pipenv` installed and install all required dependencies:

```bash
./scripts/install-dependencies.sh
```

Start tests with:

```bash
./scripts/run-tests.sh
```

### Install from source

To install from source using `pip`:

```bash
pip install .
```

To uninstall

```bash
pip uninstall git-import-contributions
```
