from setuptools import setup


setup(
    name='gzip-stream',
    version='1.2.0',

    py_modules=['gzip_stream'],
    provides=['gzip_stream'],

    description='Compress stream by GZIP on the fly.',
    long_description=open('README.rst').read(),
    keywords=['gzip', 'compression'],

    url='https://github.com/leenr/gzip-stream',
    author='leenr',
    author_email='i@leenr.me',
    maintainer='leenr',
    maintainer_email='i@leenr.me',

    platforms=['posix'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries'
    ],

    python_requires='~=3.5',
    extras_require={
        'develop': [
            'pytest~=5.0',
            'pytest-cov~=2.7',
            'pylama~=7.7',
            'faker~=2.0'
        ]
    }
)
