from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
    name='series_list',
    version=version,
    description="List of series with subtitles",
    long_description="""\
""",
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='Vladimir Iakovlev',
    author_email='nvbn.rm@gmail.com',
    url='',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'pyside',
        'requests',
        'BeautifulSoup,'
        'sure',
        'nose',
        'mock',
        'decorator',
        'gevent',
    ],
    entry_points={
        'gui_scripts': [
            'series_list=series_list.app:main'
        ]
    },
)
