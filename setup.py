import io
import os

from setuptools import find_packages, setup, Command

NAME = 'City Info'
DESCRIPTION = 'Homework Assignment from Cayuse'
EMAIL = 'mikelane@gmail.com'
AUTHOR = 'Michael Lane'
REQUIRES_PYTHON = '>=3.6.0'

REQUIRED = ['requests']

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f'\n {f.read()}'
except FileNotFoundError:
    long_description = DESCRIPTION

setup(
    name=NAME,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    py_modules=['city_info'],
    entry_points={
        'console_scripts': ['city-info=city_info:main'],
    },
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
