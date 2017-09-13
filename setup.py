# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

install_requires = [
                    'dj_database_url',
]

extras_require = {
        'test': [
            'pytest>=3.0.0',
            'responses',
            'pytest-cov',
        ]
}

setup(
    name='vaultkeeper_adaptor',
    version='0.0.1',
    description=('A small library that '
                 'allows Django apps to '
                 'consume Vaultkeeper output '
                 'as resource secrets.'),
    long_description=readme,
    install_requires=install_requires,
    extras_require=extras_require,
    author='mracter',
    author_email='mary@praekelt.org',
    url='https://github.com/praekeltfoundation/vaultkeeper',
    license='BSD',
    packages=find_packages(),
)
