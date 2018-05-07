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
    parser.add_argument(
        '--script',
        action='append',
        help='Script for the tool. Can be read from the setup.py file'
    )
    parser.add_argument(
        '--name', help='Name of the tool. Can be read from the setup.py file'
    )
    parser.add_argument(
        '--version',
        help='Version of the tool. Can be read from setup.py file'
    )
    parser.add_argument(
        '--project',
        help=
        'Root folder for project. Defaults to the folder containing the Pipfile'
    )
    parser.add_argument(
        '--python-version', default='3.6.5', help='Python version to install'
    )
    parser.add_argument('pipfile', help='Path to the Pipfile for the project')
    parser.add_argument(
        'setup',
        required=False,
        help=
        'Optional path to the setup.py file. Will read settings from this file'
    )
    args = parser.parse_args()

    pipfile = abspath(args.pipfile)
    project = args.project or dirname(pipfile)

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
        pipfile=pipfile,
        python_version=args.python_version,
        architecture=architecture,
    )


Settings = namedtuple(
    'Settings',
    ['project', 'name', 'version', 'scripts', 'pipfile', 'python_version', 'architecture']
)
