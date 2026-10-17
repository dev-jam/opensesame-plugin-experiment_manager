"""Experiment Manager plugin for OpenSesame"""

from importlib.metadata import PackageNotFoundError, version

# The name of the packages to check for updates on conda and pip
packages = ['opensesame-plugin-experiment-manager',
            'opensesame-plugin-experiment_manager']

# The version is set in pyproject.toml only; this reads it from the
# installed package
try:
    __version__ = version(packages[0])
except PackageNotFoundError:
    # Running from a source folder that is not installed
    __version__ = 'unknown'
