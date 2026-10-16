"""
This file is part of OpenSesame.

OpenSesame is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OpenSesame.  If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "Bob Rosbag"
__license__ = "GPLv3"

import os
import sys
import subprocess

from libopensesame.py3compat import *
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from libopensesame.exceptions import OSException
from libopensesame.oslogging import oslogger

from .run_experiment import EXIT_USER_ABORTED

RUNNER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           'run_experiment.py')


class ExperimentManager(Item):

    def reset(self):
        self.var.filename = 'example.osexp'
        self.var.dummy_mode = 'no'
        self.var.verbose = 'no'

    def prepare(self):
        super().prepare()
        self._init_var()

    def run(self):
        self.subject_nr = self.var.subject_nr
        self.filename = self.var.filename

        subject_nr = self.subject_nr
        home_path = os.path.dirname(self.experiment.logfile)

        exp_file_name = self.filename
        log_file_name = f"{exp_file_name}_-_subject-{subject_nr}.csv"

        exp_file_path = os.path.join(home_path, exp_file_name)
        log_file_path = os.path.join(home_path, log_file_name)

        # opensesamerun was removed in OpenSesame 4.1, so the experiment is
        # started with run_experiment.py and the Python interpreter that runs
        # OpenSesame
        command = [sys.executable, RUNNER_PATH]
        subject_arg = f"--subject={subject_nr}"
        log_arg = f"--logfile={log_file_path}"
        screen_arg = '--fullscreen'

        args = command + [exp_file_path, subject_arg, log_arg, screen_arg]
        self._show_message(args)
        self.set_item_onset()

        if self.dummy_mode == 'no':
            if not os.path.isfile(exp_file_path):
                raise OSException(f"Experiment file not found: {exp_file_path}")
            try:
                returncode = subprocess.call(args)
            except Exception as e:
                raise OSException(f"Could not execute experiment\n\nMessage: {e}")
            if returncode == EXIT_USER_ABORTED:
                oslogger.warning(f"Experiment was aborted: {exp_file_name}")
            elif returncode != 0:
                raise OSException(
                    f"Experiment failed with exit code {returncode}: "
                    f"{exp_file_name}\n\nSee the debug window or console "
                    "for details")
        elif self.dummy_mode == 'yes':
            self._show_message('Dummy mode enabled, run phase')
        else:
            self._show_message(f"Error with dummy mode, mode is: {self.dummy_mode}")

    def _init_var(self):
        self.verbose = self.var.verbose
        self.dummy_mode = self.var.dummy_mode

    def _show_message(self, message):
        oslogger.debug(message)
        if self.verbose == 'yes':
            print(message)


class qtExperimentManager(ExperimentManager, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):
        ExperimentManager.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)
