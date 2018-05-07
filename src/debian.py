from tempfile import mkdtemp
from os.path import join
from shutil import copy, copytree, rmtree
from jinja2 import Template
from sh import (
    dpkg_architecture,
    git,
)


def create_debian_package(settings):
    with Directory() as directory:
        directory.prepare(settings)
        return directory.create()


class Directory:

    def __init__(self):
        self.path = mkdtemp()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, value, traceback):
        self.clean()

    def prepare(self, settings):
        self.copy_project(settings)
        self.install_pyenv(settings)
        self.install_python(settings)
        self.install_dependencies(settings)
        self.configure_dpkg(settings)

    def create(self):
        pass

    def clean(self):
        if not self.path:
            raise ValueError('Clean invoked on cleaned directory')
        rmtree(self.path)
        self.path = None

    def copy_project(self, settings):
        copytree(settings.project, join(self.path, 'project'))

    def install_pyenv(self):
        git('clone', 'https://github.com/pyenv/pyenv.git', join(self.path, 'pyenv')) # pylint: disable=too-many-function-args

    def install_python(self, settings):
        pass
        # call pyenv install settings python version

    def install_dependencies(self, settings):
        pass

    def configure_dpkg(self, settings):
        pass
