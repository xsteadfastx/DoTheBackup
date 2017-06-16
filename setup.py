import os
import sys

from setuptools import setup


def _read(fn):
    path = os.path.join(os.path.dirname(__file__), fn)

    return open(path).read()


def main():
    if sys.version_info[:2] < (3, 3):
        sys.exit('dothebackup currently requires Python 3.3+')

    setup(
        name='dothebackup',
        version='1.1.0',
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
            'Click>=6.0.0',
            'pendulum>=1.2.0',
            'pyyaml>=3',
            'requests>=2.0.0',
        ],
        entry_points={
            'console_scripts': [
                'dothebackup = dothebackup.ui:main'
            ]
        },
        classifiers=[
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3 :: Only',
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: MIT License',
            'Topic :: System :: Archiving :: Backup'
        ]
    )


if __name__ == '__main__':
    main()
