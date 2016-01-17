"""Setup file to automate the install of Mackup in the Python environment."""
from setuptools import setup
from mackup.constants import VERSION


setup(
    name='mackup',
    version=VERSION,
    author='Laurent Raufaste',
    author_email='analogue@glop.org',
    url='https://github.com/lra/mackup',
    description='Keep your application settings in sync (OS X/Linux)',
    keywords='configuration config dotfiles sync backup dropbox gdrive box',
    license='GPLv3',
    packages=['mackup'],
    install_requires=['docopt'],
    entry_points={
        'console_scripts': [
            'mackup=mackup.main:main',
        ],
    },
    package_data={'mackup': ['applications/*.cfg']},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        ('License :: OSI Approved :: '
         'GNU General Public License v3 or later (GPLv3+)'),
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
)
