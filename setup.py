#/usr/bin/env python
import os
from setuptools import setup

ROOT_DIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.join(ROOT_DIR)

test_requirements = []
setup(
    name="docker-AMI",
    version='0.0.1',
    description="Utility to build AMI images with docker pre-installed",
    packages=[
        'docker_ami',
        'docker_ami.utils'],
    install_requires=[
        'boto==2.9.6',
        'paramiko==1.10.1',
        'requests==1.2.3',] + test_requirements,
    scripts  = [
        'bin/build-docker-ami'
    ],
    zip_safe=False,
    classifiers=['Development Status :: 3 - Alpha',
                 'Environment :: Other Environment',
                 'Intended Audience :: Developers',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Topic :: Utilities'],
    )
