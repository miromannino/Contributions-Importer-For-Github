import os
import shutil
import subprocess

from setuptools import find_packages, setup


def get_version_from_git():
    try:
        git_path = shutil.which("git")
        if git_path is None:
            raise ValueError("Git is not installed")

        result = subprocess.run(
            [git_path, "describe", "--tags", "--abbrev=0"],
            text=True,
            capture_output=True,
            check=True,
        )
        return result.stdout.strip()
    except Exception:
        return "0.0.0"


version = os.getenv("RELEASE_VERSION", get_version_from_git())

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="git-import-contributions",
    version=version,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={
        "git_import_contributions": ["README.md"],
    },
    install_requires=["gitpython"],
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "git-import-contributions=git_import_contributions.cli:main",
        ],
    },
    author="Miro Mannino",
    description="This tool helps users to import contributions to GitHub from private git repositories, or from public repositories that are not hosted in GitHub",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/miromannino/Contributions-Importer-For-Github",
)
