from setuptools import setup, find_packages


version = '7.3'

setup(
    name='series_list',
    version=version,
    description="List of series with subtitles",
    long_description="""\
""",
    classifiers=[],
    keywords='',
    author='Vladimir Iakovlev',
    author_email='nvbn.rm@gmail.com',
    url='https://github.com/nvbn/series_list',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    package_data={
        '': ['*.ui'],
    },
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'pyside',
        'requests',
        'BeautifulSoup',
        'sure',
        'nose',
        'mock',
        'decorator',
        'gevent',
        'subliminal >= 0.7',
    ],
    entry_points={
        'gui_scripts': [
            'series_list=series_list.app:main'
        ]
    },
    data_files=[
        ('share/icons/hicolor/128x128/apps', [
            'data/series_list_icon.png',
        ]),
        ('share/icons/hicolor/16x16/actions', [
            'data/fallback_icons/16/series-list-refresh.svg',
        ]),
        ('share/icons/hicolor/24x24/actions', [
            'data/fallback_icons/24/series-list-download.svg',
            'data/fallback_icons/24/series-list-open.svg',
            'data/fallback_icons/24/series-list-pause.svg',
            'data/fallback_icons/24/series-list-stop.svg',
        ]),
        ('share/applications', ['data/series_list.desktop']),
    ]
)
