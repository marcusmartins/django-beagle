# -*- encoding: utf-8 -*-
"""
Python setup file for the datadog_metrics app.
"""
from setuptools import setup, find_packages
import datadog_metrics


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
    name=datadog_metrics.__title__,
    version=datadog_metrics.__version__,
    description="A reusable app to send metrics to the datadog service.",
    long_description=readme,
    license=datadog_metrics.__license__,
    platforms=['OS Independent'],
    keywords='django, app, reusable, metrics, datadog',
    author=datadog_metrics.__author__,
    author_email='marcusdiasm@gmail.com',
    url="https://github.com/marcusmartins/django-datadog-metrics",
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    extras_require={
        'dev': dev_requires,
    },
)
