#!/usr/bin/env python3
# encoding: utf-8

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("LICENSE.md", "r") as fh:
    long_description += fh.read()

setuptools.setup(
    name="p-unity",
    version="0.10.42",
    author="Scott McCallum (https://sr.ht/~scott91e1)",
    author_email="262464@195387.com",
    description="{ Programming : Unity }",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/p-unity",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: Free To Use But Restricted",
        "License :: Programming Unity License 10.42",
        "License :: SPDX License Identifier :: Programming-Unity-10.42",

        "Development Status :: 3 - Alpha",

        "Environment :: Console",
        "Environment :: Console :: Curses",
        "Environment :: Win32",
        "Environment :: No Input/Output (Daemon)",

        "Framework :: Trio",
        "Framework :: Quart",

        "Operating System :: OS Independent",

        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Administrators",
        "Intended Audience :: Developers",

        "Natural Language :: English",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: cPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: SQL",
        "Programming Language :: Forth",
        "Programming Language :: BASIC",
        "Programming Language :: JavaScript",
        "Programming Language :: Other Scripting Engines",

        "Topic :: Education",
        "Topic :: Multimedia",
        "Topic :: Internet",
        "Topic :: Software Development",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Bug Tracking",
        "Topic :: Software Development :: Interpreters",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Pre-processors",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Software Development :: Version Control",
        "Topic :: System :: Software Distribution",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Markup :: Markdown",
    ],
    python_requires=">=3.7",
)
