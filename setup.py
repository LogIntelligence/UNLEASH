from os.path import join, dirname, abspath
from setuptools import setup

# Get the long description from the README file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

# Get requirements from requirements.txt
with open('requirements.txt', encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(
    name='unleash',
    version='0.1.0',
    description='Log parsing and evaluation tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['unleash'],
    install_requires=requirements
)