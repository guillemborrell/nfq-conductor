#!/usr/bin/env python

from setuptools import setup

setup(
    name="nfq-conductor",
    description="NFQ Solutions process manager",
    version="0.1.2",
    author="NFQ Solutions",
    author_email="solutions@nfq.es",
    packages=[
        'nfq',
        'nfq.conductor'
        ],
    zip_safe=False,
    install_requires=[nfq-logwrapper, psutil],
    include_package_data=True,
    setup_requires=[],
    tests_require=[]
    )
