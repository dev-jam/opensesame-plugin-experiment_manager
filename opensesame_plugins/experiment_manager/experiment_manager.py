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

VERSION = u'2.1.0'


class experiment_manager(item):
    """Experiment Manager class handles the basic
    functionality of the item. It does not deal with GUI stuff.
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
        """Show message."""
        debug.msg(message)
        if self.verbose == u'yes':
            print(message)


class qtexperiment_manager(experiment_manager, qtautoplugin):
    """This class handles the GUI aspect of the plug-in. By using qtautoplugin,
    we usually need to do hardly anything, because the GUI is defined in
    info.json.
    """

    def __init__(self, name, experiment, script=None):

        """Constructor.

        Arguments:
        name       -- Experiment Manager plug-in.
        experiment -- The experiment object.

        Keyword arguments:
        script     -- A definition script. (default=None)
        """
        # We don't need to do anything here, except call the parent
        # constructors.
        experiment_manager.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)

    def init_edit_widget(self):
        """Constructs the GUI controls. Usually, you can omit this function
        altogether, but if you want to implement more advanced functionality,
        such as controls that are grayed out under certain conditions, you need
        to implement this here.
        """
        # First, call the parent constructor, which constructs the GUI controls
        # based on info.json.
        qtautoplugin.init_edit_widget(self)
        # If you specify a 'name' for a control in info.json, this control will
        # be available self.[name]. The type of the object depends on the
        # control. A checkbox will be a QCheckBox, a line_edit will be a
        # QLineEdit. Here we connect the stateChanged signal of the QCheckBox,
        # to the setEnabled() slot of the QLineEdit. This has the effect of
        # disabling the QLineEdit when the QCheckBox is uncheckhed. We also
        # explictly set the starting state.
        self.line_edit_widget.setEnabled(self.checkbox_widget.isChecked())
        self.checkbox_widget.stateChanged.connect(
            self.line_edit_widget.setEnabled)