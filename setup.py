from setuptools import setup
import os


def _read(fn):
    path = os.path.join(os.path.dirname(__file__), fn)

    return open(path).read()


setup(
    name='dothebackup',
    version='0.1.2',
    description='backup tool with plugins',
    author='Marvin Steadfast',
    author_email='marvin@xsteadfastx.org',
    url='https://github.com/xsteadfastx/DoTheBackup',
    license='MIT',
    platforms='ALL',
    long_description=_read('README.rst'),
    packages=[
        'dothebackup',
        'dothebackup.plugs'
    ],
    include_package_data=True,
    install_requires=[
        'Click',
        'pyyaml',
        'arrow',
        'requests'
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
