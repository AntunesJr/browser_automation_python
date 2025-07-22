#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name="browser_automation",
    version="0.1.0",
    author="Silvio Antunes",
    author_email="silvioantunes1@hotmail.com",
    description="Browser automation",
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
            "check_cred=authenticator.commands.check_cred:main",
            "check_cred_bin=authenticator.commands.check_cred_bin:main",
            "check_cred_json=authenticator.commands.check_cred_json:main",
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