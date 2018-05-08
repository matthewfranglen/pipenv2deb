import os
from os import mkdir
from os.path import join
from shutil import copytree, rmtree
from tempfile import mkdtemp

import pkg_resources
import sh
from jinja2 import Template


def create_debian_package(settings):
    with PackageBuildDirectory(settings) as directory:
        directory.prepare()
        return directory.create()


class PackageBuildDirectory:
    def __init__(self, settings):
        self.settings = settings
        self.path = mkdtemp()
        self.pyenv_root = join(self.path, 'pyenv')
        self.project_root = join(self.path, 'project')
        self.debian_root = join(self.path, 'DEBIAN')
        mkdir(self.debian_root)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, value, traceback):
        self.clean()

    def prepare(self):
        print('preparing...')
        self.copy_project()
        self.install_pyenv()
        self.install_python()
        self.install_dependencies()
        self.configure_dpkg()

    def create(self):
        print('creating...')
        sh.dpkg_deb('--build', self.path, 'build.deb')

    def clean(self):
        print('cleaning...')
        if not self.path:
            raise ValueError('Clean invoked on cleaned directory')
        rmtree(self.path)
        self.path = None

    def copy_project(self):
        print('copying project...')
        copytree(self.settings.project, self.project_root)

    def install_pyenv(self):
        print('installing pyenv...')
        sh.git.clone('https://github.com/pyenv/pyenv.git', self.pyenv_root)

    def install_python(self):
        print('installing python...')
        env = os.environ.copy()
        env['PYENV_ROOT'] = self.pyenv_root
        pyenv = sh.Command(join(self.path, 'pyenv', 'bin', 'pyenv'))
        pyenv.install(self.settings.python_version, _env=env)

    def install_dependencies(self):
        print('installing dependencies...')
        env = os.environ.copy()
        env['PYENV_ROOT'] = self.pyenv_root
        env['PIPENV_VENV_IN_PROJECT'] = '1'
        os.chdir(self.project_root)
        sh.pipenv('install', _env=env)

    def configure_dpkg(self):
        print('configuring debian metadata...')
        template = Template(
            pkg_resources.resource_string(
                __name__, '../templates/control.jinja'
            )
        )
        content = template.render(**self.settings)
        with open(join(self.path, 'DEBIAN', 'control'), 'w') as handle:
            handle.write(content)
