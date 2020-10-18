#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="jex",
    version="0.1.4",
    description="JSON/YAML interactive explorer - no JQ",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Viet Hung Nguyen",
    author_email="hvn@familug.org",
    url="https://github.com/hvnsweeting/jex",
    license="MIT",
    classifiers=["Environment :: Console"],
    packages=find_packages(include=["jex"]),
    install_requires=['PyYAML>5'],
    entry_points={"console_scripts": ["jex=jex.cli:main"]},
)
