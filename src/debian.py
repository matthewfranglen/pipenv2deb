import os
from os import mkdir
from pathlib import Path
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
        self.path = self.pyenv_root = self.project_root = self.debian_root = self.env = None
        self.settings = settings

    def __enter__(self):
        self.path = Path(mkdtemp())
        self.pyenv_root = self.path / 'pyenv'
        self.project_root = self.path / 'project'
        self.debian_root = self.path / 'DEBIAN'
        mkdir(self.debian_root)

        env = os.environ.copy()
        env['PYENV_ROOT'] = self.pyenv_root
        env['PIPENV_VENV_IN_PROJECT'] = '1'
        self.env = env

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
        command_path = self.pyenv_root / 'bin' / 'pyenv'
        pyenv = sh.Command(command_path)
        pyenv.install(self.settings.python_version, _env=self.env)

    def install_dependencies(self):
        print('installing dependencies...')
        os.chdir(self.project_root)
        sh.pipenv('install', _env=self.env)

    def configure_dpkg(self):
        print('configuring debian metadata...')
        template_content = pkg_resources.resource_string(
            __name__, 'templates/control.jinja'
        ).decode('utf-8')
        template = Template(template_content)
        content = template.render(**self.settings._asdict())
        control_file = self.debian_root / 'control'
        control_file.write_text(content)
        print(content)
