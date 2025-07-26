#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name="browser_automation-python",
    version="0.1.0",
    author="Silvio Antunes",
    author_email="silvioantunes1@hotmail.com",
    description="Browser automation in python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="GPL-3.0",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "cryptography>=38.0.0",
    ],
    entry_points={
        "console_scripts": [
            "check_exists_cred=credentials.commands.check_exists_cred:main",
            "check_exists_cred_bin=credentials.commands.check_exists_cred_bin:main",
            "check_exists_cred_json=credentials.commands.check_exists_cred_json:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Security :: Cryptography",
    ],
)