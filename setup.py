import sys
from setuptools import setup, find_packages

setup(
    name='tinc_graphs',
    version='0.3.11',

    description='Create Graphs from tinc Stats',
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    license='WTFPL',
    url='http://krebsco.de/',
    download_url='https://pypi.python.org/pypi/tinc_graphs/',
    author='krebs',
    author_email='spam@krebsco.de',
    # you will also need graphviz and imagemagick
    install_requires = [ 'pygeoip' ],
    scripts = ['scripts/all-the-graphs', 'scripts/build-graphs'],
    packages=['tinc_graphs'],
    package_data = {'tinc_graphs': ['static/*/*.html',
                                    'static/*/css/*.css' ]},
    entry_points={
        'console_scripts' : [
            'tinc-stats2json = tinc_graphs.Log2JSON:main',
            'tinc-build-graph = tinc_graphs.Graph:main',
            'tincstats-static-dir = tinc_graphs.Geo:get_static_dir',
            'add-geodata = tinc_graphs.Geo:main',
            'tinc-availability-stats = tinc_graphs.Availability:generate_stats',
            ]
        },

    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
)

