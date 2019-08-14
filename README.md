# Contributions Importer for GitHub

This tool helps users to import contributions to GitHub from private git repositories, or from public repositories that are not hosted in GitHub.

<p style="margin: 20px" align="center">
<img src="https://github.com/miromannino/contributions-importer-for-github/blob/resources/fig1.png" />
</p>


## How it Works

In its simplest case, this tools copies all commits from a source git repository to a mock git repository. Each copied commit will report the same commit date, but the original code is not copied, neither the commit message.

<p style="margin: 20px" align="center">
<img src="https://github.com/miromannino/contributions-importer-for-github/blob/resources/fig0.png" />
</p>

_Contributions Importer_ will create instead mock code in order to report which languages have been used in the source repository.

You can also have multiple source git repository as well in order to report activities from several private git repositories.

## Reasons

GitHub shows contributions statistics of its users. There are [several reasons](https://github.com/isaacs/github/issues/627) why this feature could be debatable.

Moreover, this mechanism only rewards developers that work on GitHub maintained repositories.

Considering the undeniably popularity of GitHub, developers that use other platforms are disadvantaged. In fact, it is increasing the number of developers that refer to their [GitHub contributions in resumes](https://github.com/resume/resume.github.com). Similarly, recruiters [may use GitHub to find talents](https://www.socialtalent.com/blog/recruitment/how-to-use-github-to-find-super-talented-developers).

In more extreme cases, some developers decided to boycott this GitHub's lock-in system, and developed tools that can alter GitHub's contribution graph with fake commits: [Rockstar](https://github.com/avinassh/rockstar) and [Vanity text for GitHub](https://github.com/ihabunek/github-vanity) are good examples.

Instead, the aim of [Contributions Importer for GitHub](https://github.com/miromannino/contributions-importer-for-github) is to generate an overall realistic activity overview.


## How to Use

_Contributions Importer_ is for developers. No UI, nor simple command line tools. This tool can be used by writing a simple Python script:

    import git
    from git_contributions_importer import *

    repo = git.Repo("path/to/your/private/repo")
    mock_repo = git.Repo("path/to/your/mock/repo")

    importer = Importer([repo], mock_repo)
    importer.set_author('email@domain.com')

    importer.import_repository()

If the mock repository folder could be an empty git repository as well as a repository that has already other commits.


## Protecting your private repository

_Contributions Importer_ has few features to protect your  private code.

### Masking the real commit time  

    importer.set_commit_time_max_past(value)

Maximum amount in the past that the commit can be shifted for. The values are in seconds.

### Maximum number of changes per file  

    importer.set_max_changes_per_file(max_amount)

Maximum number of changes per file. By default for each change (line of code changed, added or removed) a line of mock code is changed. Instead, `set_max_changes_per_file()` would limit the number of generated mock code for extreme cases where too many lines of codes are changes (e.g. SQL database dump). The default is 5.

### Collapse multiple changes into one

    importer.set_collapse_multiple_changes_to_one(true)

It allows the importer to collapse several lines of changes to just one per commit, and one per type of file. This allows avoiding excessive growth of files size. The default is set to True.

### Maximum number of changes per commit  

    importer.set_commit_max_amount_changes(max_amount)

The maximum number of changes (line of code changed, added or removed) that a commit can have. Commits with many changes are disadvantaged in GitHub. Most likely these large commits could have been split in many smaller ones. GitHub users that know how contributions are calculated are prone to do several smaller commits instead, while in private repository this could not be necessary, especially in smaller teams. The default is -1, and it is to indicate no limits.

### Maximum time backward

    importer.set_changes_commits_max_time_backward(max_amount)

If `set_commit_max_amount_changes()` has been used, a commit could be split. In that case this value decides how long these commits could go in the past. The idea is that a big commit is likely composed by several features that could have been committed in different commits. These changes would have been some time before the actual real commit. The time is in seconds, the default is 4 days (good in simpler projects where there is a "backup" commit every week).

### Ignore Before Date

    importer.set_ignore_before_date(value)

Importer will ignore all commits before this date (number of seconds from 1970-01-01 UTC)

### Just last commit

    importer.set_start_from_last(false)

The importer will fetch last commited date from mock_repo and will ignore all commits before this date. If `ignore_before_date` is set all commits before the most recent date between last commit and `ignore_before_date` will be ignored. Useful to do incremental imports.

### Set Author

    importer.set_author(email)

Author to analyse. If not set, commits from any author will be imported. Author is given as email. This could also be an array in case the author uses different emails.

## Blog Posts about this project

- [How I Restored My Git Contributions](https://medium.com/@razan.joc/how-i-restored-my-git-contributions-7ddb27f06d4e) by Rajan Joshi

## Contributing

#### Code style
Regarding code style like indentation and whitespace, **follow the conventions you see used in the source already.**

### Submitting pull requests

- Create a new branch, please don't work in your `master` branch directly.
- Add failing tests for the change you want to make.
- Fix stuff.
- Ensure that the written tests don't fail anymore, as well as the other tests.
- Update the documentation to reflect any changes.
- Push to your fork and submit a pull request.

## License

MIT License

Copyright (c) 2018 Miro Mannino

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
