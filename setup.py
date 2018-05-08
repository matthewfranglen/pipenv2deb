from setuptools import setup, find_packages

setup(
    name='pipenv2deb',
    version='0.0.1',
    description='Convert a Pipenv project into a Debian Package',
    author='Matthew Franglen',
    url='https://github.com/matthewfranglen/pipenv2deb',
    scripts=['pipenv2deb'],
    package_data={'src': ['templates/*.jinja']},
    packages=find_packages(),
    install_requires=[
        'jinja2',
        'sh',
    ]
)
