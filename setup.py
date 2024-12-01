from setuptools import setup, find_packages


setup(
    name='git-import-contributions',
    version='2.0.0',
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
    description='A brief description of your script.',
    url='https://github.com/miromannino/Contributions-Importer-For-Github',
)
