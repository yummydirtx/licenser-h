from setuptools import setup, find_packages

setup(
    name='licenser',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'argparse',
        'InquirerPy',
    ],
    entry_points={
        'console_scripts': [
            'licenser = src.main:main',
        ],
    },
)
