from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')


setup(
    name='jupyterhub_client',
    version='0.1.0',
    description='Library and Client for managing, benchmarking, and interacting with jupyterhub',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/costrouc/jupyterhub_client',
    author='Christopher Ostrouchov',
    author_email='chris.ostrouchov@gmail.com',
     classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: BSD 3 License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='jupyterhub, jupyter',
    packages=find_packages(where='.'),
    install_requires=['aiohttp', 'yarl'],
    extras_require={
        'dev': ['pytest', 'pytest-asyncio'],
    },
    entry_points={
        'console_scripts': [
            'jhubctl=jupyterhub_client.__main__:main',
        ],
    },
)