import argparse
from collections import namedtuple
from os.path import abspath, basename, dirname
from sh import dpkg  # pylint: disable=no-name-in-module
from .parse import read_setup_details


def read_settings():
    parser = argparse.ArgumentParser(
        description=
        'Create a debian package out of a pipenv enabled python project'
    )
    parser.add_argument('--script', action='append')
    parser.add_argument('--name')
    parser.add_argument('--version')
    parser.add_argument('pipfile')
    parser.add_argument('setup', required=False)
    args = parser.parse_args()

    pipfile = abspath(args.pipfile)
    project = dirname(pipfile)

    if args.setup:
        with open(args.setup, 'r') as handle:
            name, version, scripts = read_setup_details(handle.read())

    if args.name:
        name = args.name
    if args.version:
        version = args.version
    if args.script:
        scripts = args.script

    if not name:
        name = basename(project)
    if not version:
        version = '0.0.0'
    if not scripts:
        scripts = []
    architecture = dpkg('--print-architecture')

    return Settings(
        project=project,
        name=name,
        version=version,
        scripts=scripts,
        architecture=architecture,
    )


Settings = namedtuple(
    'Settings', ['project', 'name', 'version', 'scripts', 'architecture']
)
