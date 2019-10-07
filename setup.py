from setuptools import setup, find_packages
import os
try:
    with open(os.path.join(os.path.dirname(__file__)), 'README.md') as f:
        long_description = f.read()
except:
    long_description = None
print(
    """
Currently ssh cloning of a remote is not supported by setuptools.
To fix this run "pip install -e git+git://<repo_url>"
or "pip install -e git+ssh://git@bitbucket.org/rshanker779/rshanker779_common.git#egg=rshanker779_common"
"""
)
setup(
    name=postcode_map,
    version="1.0.0",
    author=rshanker779,
    author_email=rshanker779@gmail.com,
    description=Generation and plotting of UK postcodes from partial matches,
    long_description=long_description if long_description is not None else Generation and plotting of UK postcodes from partial matches
    license="MIT",
    python_requires=">=3.5",
    install_requires=[
        "black",
        "pre-commit",
        "rshanker779_common",
        "coverage",
    ],
    packages=find_packages(),
    entry_points={},
    test_suite="tests",
    dependency_links=[
        "git+https://rshanker779@bitbucket.org/rshanker779/rshanker779_common.git#egg=rshanker779_common"
    ],
)
