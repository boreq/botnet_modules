import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='botnet_modules',
    version='0.1.0',
    author='boreq',
    author_email='boreq@sourcedrops.com',
    description = ('Additional modules for an IRC bot.'),
    license='BSD',
    packages=['botnet_modules'],
    long_description=read('README.md'),
    install_requires=[
        'botnet>=0.1.0',
        'requests',
    ]
)
