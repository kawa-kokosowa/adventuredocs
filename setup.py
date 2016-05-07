from setuptools import setup
from adventuredocs import __version__


setup(
    name='AdventureDocs',
    version=__version__,
    description='Choose your own adventure style documentation!',
    url='https://github.com/lillian-gardenia-seabreeze/adventuredocs',
    author='Lillian Gardenia Seabreeze',
    author_email='lillian.gardenia.seabreeze@gmail.com',
    keywords='cli',
    packages=['adventuredocs', 'adventuredocs.plugins'],
    install_requires = ['docopt'],
    entry_points = {
        'console_scripts': [
            'adocs=adventuredocs.adocs:main',
        ],
    },
    include_package_data=True,
    package_dir={'adventuredocs': 'adventuredocs'},
    package_data={'adventuredocs': ['style.css']}
)
