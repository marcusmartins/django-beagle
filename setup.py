# -*- encoding: utf-8 -*-
"""
Python setup file for the beagle app.
"""
from setuptools import setup, find_packages
import beagle


dev_requires = [
    'flake8',
]

install_requires = [
    'django>=1.5',
    'dogapi>=1.8'
]

with open('README.rst', 'r') as f:
    readme = f.read()

setup(
    name=beagle.__title__,
    version=beagle.__version__,
    description="A reusable app to send metrics to the datadog service.",
    long_description=readme,
    license=beagle.__license__,
    platforms=['OS Independent'],
    keywords='beagle, django, app, reusable, metrics, datadog',
    author=beagle.__author__,
    author_email='marcusdiasm@gmail.com',
    url="https://github.com/marcusmartins/django-beagle",
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    extras_require={
        'dev': dev_requires,
    },
)
