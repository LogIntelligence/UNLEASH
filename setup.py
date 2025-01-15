from os.path import join, dirname, abspath
from setuptools import setup
from unleash import __version__

# Get the long description from the README file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

# Get requirements from requirements.txt
with open('requirements.txt', encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(
    name='icse-unleash',
    version=__version__,
    description='UNLEASH: Unleashing the True Potential of Semantic-based Log Parsing with Pre-trained Language Models',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['unleash'],
    install_requires=requirements
)