import setuptools

import mackup.main


setuptools.setup(
    name = 'Mackup',
    version = mackup.main.VERSION,
    author = 'Laurent Raufaste',
    author_email = 'analogue@glop.org',
    description = 'Keep your application settings in sync (OS X/Linux)',
    license = 'GPLv3',
    keywords = 'mackup application settings sync',
    url = 'https://github.com/lra/mackup',
    packages = setuptools.find_packages(),
    scripts=['bin/mackup'],
)
