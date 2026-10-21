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

from libopensesame.item import Item
from libopensesame.exceptions import OSException
from libopensesame.oslogging import oslogger

from .run_experiment import ExitCode

RUN_EXPERIMENT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   'run_experiment.py')


# The GUI class (QtExperimentManager) is created by OpenSesame from this class
class ExperimentManager(Item):

    def reset(self):
        self.var.filename = 'example.osexp'
        self.var.dummy_mode = 'no'
        self.var.verbose = 'no'

    def prepare(self):
        super().prepare()
        self._init_var()

    def run(self):
        # The filename is read in the run phase, so that an earlier item can
        # select the experiment, for example based on input from the user
        filename = str(self.var.filename)
        exp_file_path = self._experiment_file_path(filename)
        log_file_path = os.path.join(
            self._log_folder(),
            f"{filename}_-_subject-{self.var.subject_nr}.csv")

        # The experiment is started with the Python interpreter that runs
        # OpenSesame, because opensesamerun no longer works in OpenSesame 4.1
        args = [sys.executable, RUN_EXPERIMENT_PATH, exp_file_path,
                f"--subject={self.var.subject_nr}",
                f"--logfile={log_file_path}", '--fullscreen']
        self._show_message(args)
        # Also in dummy mode, so that a dummy run fails like a real one
        if not os.path.isfile(exp_file_path):
            raise OSException(f"Experiment file not found: {exp_file_path}")
        self.set_item_onset()

        if self.dummy_mode:
            self._show_message('Dummy mode enabled, run phase')
        else:
            self._run_experiment(args, os.path.basename(exp_file_path))

    def _init_var(self):
        """Reads the settings in the prepare phase, so that changes made by
        other items during the run phase do not affect them.
        """
        dummy_mode = self.var.dummy_mode
        # Any other value would start the experiment, which 3.2.0 did not do
        if dummy_mode not in ('yes', 'no'):
            raise OSException(
                f"Dummy mode must be 'yes' or 'no', not '{dummy_mode}'")
        self.dummy_mode = dummy_mode == 'yes'
        self.verbose = self.var.verbose == 'yes'

    def _experiment_file_path(self, filename):
        """Looks up the experiment in the folder of the log file, as in
        earlier versions. If it is not there, the file pool is used, which
        also covers the folder of the current experiment.
        """
        path = os.path.join(self._log_folder(), filename)
        if os.path.isfile(path) or filename not in self.experiment.pool:
            return path
        return self.experiment.pool[filename]

    def _log_folder(self):
        return os.path.dirname(self.experiment.logfile)

    def _run_experiment(self, args, exp_file_name):
        try:
            returncode = subprocess.run(args).returncode
        except OSError as e:
            raise OSException(
                f"Could not execute experiment\n\nMessage: {e}") from e
        if returncode == ExitCode.USER_ABORTED:
            oslogger.warning(f"Experiment was aborted: {exp_file_name}")
        elif returncode != ExitCode.OK:
            raise OSException(
                f"Experiment failed with exit code {returncode}: "
                f"{exp_file_name}\n\nSee the debug window or console for "
                "details")

    def _show_message(self, message):
        oslogger.debug(message)
        if self.verbose:
            print(message)
