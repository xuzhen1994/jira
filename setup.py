#!/usr/bin/env python

import setuptools
from setuptools.command.test import test as TestCommand
import sys
from pip import req

# In python < 2.7.4, a lazy loading of package `pbr` will break
# setuptools if some other modules registered functions in `atexit`.
# solution from: http://bugs.python.org/issue15881#msg170215
try:
    import multiprocessing  # noqa
except ImportError:
    pass

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_requires = [str(r.req) for r in req.parse_requirements('requirements.txt', session=False)]
tests_require = [str(r.req) for r in req.parse_requirements('requirements-dev.txt', session=False)]


class PyTest(TestCommand):

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

setuptools.setup(
    setup_requires=['pbr>=1.9', 'setuptools>=17.1', 'pytest-runner', 'pip'],
    install_requires=install_requires,
    tests_require=tests_require,
    pbr=True,
    cmdclass={'test': PyTest},
    test_suite='tests')
