"""setuptools module for yomisplit.
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# adapted from https://coderwall.com/p/qawuyq/use-markdown-readme-s-in-python-modules
try:
       import pypandoc
       long_description = pypandoc.convert(path.join(here, 'README.md'), 'rst', format='markdown')
except (IOError, ImportError):
    with open(path.join(here, 'README.md')) as f:
        long_description = f.read()

setup(
    name='yomisplit',

    # PEP440
    version='0.0.2',

    description='Split Japanese kanji string by readings',
    long_description=long_description,

    url='https://github.com/leoboiko/yomisplit',

    # Author details
    author='Leonardo Boiko',
    author_email='leoboiko@namakajiri.net',

    # Choose your license
    license='CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',

    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Software Development :: Localization',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Linguistic',

        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2', # probably?
        'Programming Language :: Python :: 3.3', # I hope...
        'Programming Language :: Python :: 3.4', # actually tested here

    ],

    keywords='japanese kanji han hiragana katakana readings yomi',

    # packages=find_packages(exclude=['contrib', 'docs', 'tests*', 'update']),
    packages=['yomisplit'],

    # cf. https://packaging.python.org/en/latest/requirements.html
    install_requires=[],

    extras_require={},

    package_data={},

    data_files=[],

    entry_points={},
)
