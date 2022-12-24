from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(
    name='gisp',
    version='1.0.1',
    description='Generalized Interval-extended Sequential Pattern mining',
    author='wu0306109',
    author_email='t110598007@ntut.org.tw',
    url = 'https://github.com/wu0306109/gisp',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    requires=[],
    classifiers=[
        "Programming Language :: Python :: 3"],
)