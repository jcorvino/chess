from setuptools import setup, find_packages


with open('README.md', 'r') as fo:
    readme = fo.read()

requires = []

setup(
    name='chess',
    version='1.0',
    description='A simple chess game engine',
    long_description=readme,
    author='Joe Corvino',
    url='https://github.com/jcorvino/chess',
    keywords='chess',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=False,
    install_requires=requires,
    license='GNU GPL 3.0',
)
