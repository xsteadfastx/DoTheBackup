from setuptools import setup
from os import path


here = path.abspath(path.dirname(__file__))

try:
    from pypandoc import convert

    long_description = convert(path.join(here, 'README.md'), 'rst')

except ImportError:
    print(
        "ERROR: pypandoc module not found, could not convert Markdown to RST")

    with open(path.join(here, 'README.md'), 'r') as f:
        long_description = f.read()


setup(
    name='dothebackup',
    version='0.1',
    description='backup tool with plugins',
    author='Marvin Steadfast',
    author_email='marvin@xsteadfastx.org',
    url='https://github.com/xsteadfastx/DoTheBackup',
    license='MIT',
    platforms='ALL',
    long_description=long_description,
    packages=[
        'dothebackup',
        'dothebackup.plugs'
    ],
    include_package_data=True,
    install_requires=[
        'Click',
        'pyyaml',
        'arrow'
    ],
    entry_points={
        'console_scripts': [
            'dothebackup = dothebackup.ui:main'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Topic :: System :: Archiving :: Backup'
    ]
)
