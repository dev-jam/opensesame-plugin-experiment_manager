#-*- coding:utf-8 -*-

"""
Author: Bob Rosbag
2017

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
from libopensesame import debug
from libopensesame.item import item
from libqtopensesame.items.qtautoplugin import qtautoplugin
from libopensesame.exceptions import osexception

VERSION = u'2017.11-1'

class experiment_manager(item):

    """
    Experiment Manager class handles the basic functionality of the item.
    It does not deal with GUI stuff.
    """

    # Provide an informative description for your plug-in.
    description = u'Experiment Manager: start a opensesame experiment.'

    def __init__(self, name, experiment, string=None):

        item.__init__(self, name, experiment, string)
        self.verbose = u'no'


    def reset(self):

        """Resets plug-in to initial values."""

        # Set default experimental variables and values
        self.var.filename = u'example.osexp'
        self.var.dummy_mode = u'no'
        self.var.verbose = u'no'

        self.show_message(u'Experiment Manager plug-in has been initialized!')


    def init_var(self):

        """Set en check variables."""

        self.verbose = self.var.verbose
        self.dummy_mode = self.var.dummy_mode



    def prepare(self):

        """Preparation phase"""

        # Call the parent constructor.
        item.prepare(self)

        self.init_var()


    def run(self):

        """Run phase"""

        self.subject_nr = self.var.subject_nr
        self.filename = self.experiment.pool[self.var.filename]
        self.experiment.var.filename = self.experiment.pool[self.var.filename]

        ## get variables
        subject_nr    = self.subject_nr
        home_path     = os.path.dirname(self.experiment.logfile)

        ## create file names
        exp_file_name = self.filename
        log_file_name = exp_file_name + u'_-_' + u'subject-' + str(subject_nr) + u'.csv'

        ## create paths
        exp_file_path = os.path.join(home_path, exp_file_name)
        log_file_path = os.path.join(home_path, log_file_name)

        ## create cmds and args
        command       = u'opensesamerun'
        subject_arg   = u'--subject=' + str(subject_nr)
        log_arg       = u'--logfile=' + log_file_path
        screen_arg    = u'--fullscreen'

        args = [command, exp_file_path, subject_arg, log_arg, screen_arg]
        self.show_message(args)
        self.set_item_onset()

        if self.dummy_mode == u'no':
            try:
                subprocess.call(args)
            except Exception as e:
                raise osexception(u'Could not execute experiment', exception=e)
        elif self.dummy_mode == u'yes':
            self.show_message(u'Dummy mode enabled, run phase')
        else:
            self.show_message(u'Error with dummy mode, mode is: %s' % self.dummy_mode)

    def show_message(self, message):
        """
        desc:
            Show message.
        """

        debug.msg(message)
        if self.verbose == u'yes':
            print(message)


class qtexperiment_manager(experiment_manager, qtautoplugin):

    def __init__(self, name, experiment, script=None):

        """Experiment Manager plug-in GUI"""

        experiment_manager.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)
        self.text_version.setText(
        u'<small>Parallel Port Trigger version %s</small>' % VERSION)
