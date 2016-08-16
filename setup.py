from setuptools import setup
import os


def _read(fn):
    path = os.path.join(os.path.dirname(__file__), fn)

    return open(path).read()


setup(
    name='dothebackup',
    version='0.2.1',
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
        'attrs>=16.0.0',
        'Click>=6.0.0',
        'pyyaml>=3',
        'arrow>=0.8.0',
        'requests>=2.0.0'
    ],
    entry_points={
        'console_scripts': [
            'dothebackup = dothebackup.ui:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Topic :: System :: Archiving :: Backup'
    ]
)
