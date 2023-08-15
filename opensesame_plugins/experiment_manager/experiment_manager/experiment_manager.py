#-*- coding:utf-8 -*-

"""
Author: Bob Rosbag
2022

This plug-in is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This software is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this plug-in.  If not, see <http://www.gnu.org/licenses/>.
"""
import os
import subprocess

from libopensesame.py3compat import *
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from libopensesame.exceptions import OSException
from libopensesame.oslogging import oslogger


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
        log_file_name = exp_file_name + '_-_' + 'subject-' + str(subject_nr) + '.csv'

        exp_file_path = os.path.join(home_path, exp_file_name)
        log_file_path = os.path.join(home_path, log_file_name)

        command = 'opensesamerun'
        subject_arg = '--subject=' + str(subject_nr)
        log_arg = '--logfile=' + log_file_path
        screen_arg = '--fullscreen'

        args = [command, exp_file_path, subject_arg, log_arg, screen_arg]
        self._show_message(args)
        self.set_item_onset()

        if self.dummy_mode == 'no':
            try:
                subprocess.call(args)
            except Exception as e:
                raise OSException('Could not execute experiment\n\nMessage: %s' % e)
        elif self.dummy_mode == 'yes':
            self._show_message('Dummy mode enabled, run phase')
        else:
            self._show_message('Error with dummy mode, mode is: %s' % self.dummy_mode)

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
