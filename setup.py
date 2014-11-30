#!/usr/bin/python

import os
from setuptools import setup

from evelink import __version__

try:
    __readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    __readme_contents = open(__readme_path).read()
except IOError:
    __readme_contents = ""

setup(
    name="EVELink",
    version=__version__,
    description="Python Bindings for the EVE Online API",
    long_description=__readme_contents,
    license="MIT License",
    author="Valkyries of Night",
    author_email="d-eve-lopment@googlegroups.com",
    maintainer="Amber Yust",
    maintainer_email="amber.yust@gmail.com",
    url="https://github.com/eve-val/evelink",
    download_url="https://github.com/eve-val/evelink/downloads",
    packages=[
        "evelink",
        "evelink.appengine",
        "evelink.cache",
        "evelink.parsing",
        "evelink.thirdparty",
    ],
    data_files=[
        ('', ['README.md', 'LICENSE']),
    ],
    scripts=["bin/evelink"],
    provides=["evelink"],
    requires=["six"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)

# vim: set et ts=4 sts=4 sw=4:
