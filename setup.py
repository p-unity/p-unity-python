#!/usr/bin/env python3
# encoding: utf-8

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

long_description += "\n\n"

with open("LICENSE.md", "r") as fh:
    long_description += fh.read()

setuptools.setup(
    name="p-unity",
    version="0.42.202104180000",
    author="Scott McCallum (https://sr.ht/~scott91e1)",
    author_email="262464@195387.com",
    description="{ Programming : Unity }",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/p-unity",
    packages=setuptools.find_packages(),

    install_requires=[
        "simplejson",
    ],

    entry_points={
       "console_scripts": ["p-forth=p_unity.cli:ide_stdio"]
    },

    classifiers=[
        "License :: Free To Use But Restricted",

        "Development Status :: 3 - Alpha",

        "Environment :: Console",
        "Environment :: Console :: Curses",
        "Environment :: Win32 (MS Windows)",
        "Environment :: No Input/Output (Daemon)",

        "Framework :: Trio",

        "Operating System :: OS Independent",

        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",

        "Natural Language :: English",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: SQL",
        "Programming Language :: Forth",
        "Programming Language :: Basic",
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
