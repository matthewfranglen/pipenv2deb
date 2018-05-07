from tempfile import mkdtemp
import os
import pkg_resources
from os import mkdir
from os.path import join
from shutil import copy, copytree, rmtree
from jinja2 import Template
import sh


def create_debian_package(settings):
    with Directory() as directory:
        directory.prepare(settings)
        return directory.create()


class Directory:

    def __init__(self):
        self.path = mkdtemp()
        mkdir(join(self.path, 'DEBIAN'))

    def __enter__(self):
        return self

    def __exit__(self, exception_type, value, traceback):
        self.clean()

    def prepare(self, settings):
        self.copy_project(settings)
        self.install_pyenv()
        self.install_python(settings)
        self.install_dependencies(settings)
        self.configure_dpkg(settings)

    def create(self):
        sh.dpkg_deb('--build', self.path, 'build.deb')

    def clean(self):
        if not self.path:
            raise ValueError('Clean invoked on cleaned directory')
        rmtree(self.path)
        self.path = None

    def copy_project(self, settings):
        copytree(settings.project, join(self.path, 'project'))

    def install_pyenv(self):
        sh.git.clone('https://github.com/pyenv/pyenv.git', join(self.path, 'pyenv'))

    def install_python(self, settings):
        pyenv = sh.Command(join(self.path, 'pyenv', 'bin', 'pyenv'))
        pyenv.install(settings.python_version)

    def install_dependencies(self, settings):
        env = os.environ.copy()
        env['PIPENV_VENV_IN_PROJECT'] = True
        sh.bash('-c', 'cd {project} && pipenv install', _env=env)

    def configure_dpkg(self, settings):
        template = Template(pkg_resources.resource_string(__name__, 'templates/control.jinja'))
        content = template.render(**settings)
        with open(join(self.path, 'DEBIAN', 'control'), 'w') as handle:
            handle.write(content)
