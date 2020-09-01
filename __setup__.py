#!/usr/bin/env python
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='abatools',
    version='1.0.0',
    entry_points={
        'console_scripts': [
            'abatools = abatools:main',
        ],
    },
    install_requires=[
        'argparse',
        'pathlib',
        'PIL',
    ],
    packages=['abatools'],
    url='https://github.com/threadreaper/abatools',
    license='Apache License 2.0',
    author='Michael Podrybau',
    author_email='threadreaper@gmail.com',
    description='Utility for working with Android boot animations',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Natural Language :: English",
        "Intended Audience :: End Users/Desktop",
    ],
    python_requires='>=3.6',
)
