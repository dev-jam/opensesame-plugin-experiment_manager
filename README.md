OpenSesame Plugin: Experiment Manager
==========

*An OpenSesame plugin for running other OpenSesame experiments within an experiment.*  

Copyright (C) 2015-2026 Bob Rosbag  


## About

This plugin runs a standalone OpenSesame experiment as an item of a main
experiment, in a separate process. As an item in a loop or sequence, it can
run a number of experiments in a fixed or random order, and each experiment
can have its own backend.

The item has three settings:

- *Dummy Mode*: the experiment file is checked, but the experiment is not
  started; for testing the main experiment.
- *Verbose Mode*: prints what the item does, e.g. the command that starts
  the experiment.
- *Experiment file name*: a filename or a full path (see below where the
  file is looked up).

The started experiment runs fullscreen. The main experiment can also run
fullscreen with the PsychoPy backend. With the legacy backend, run the main
experiment windowed: in fullscreen it may not get the keyboard back after the
started experiment ends (seen on Linux). The experiment file is looked up in the folder of the log file
first, and then in the file pool (which includes the folder of the main
experiment). The filename may be a variable, for example set by an earlier
item. The started experiment uses the subject number of the main experiment
and writes its log file to `<filename>_-_subject-<nr>.csv` in the folder of
the main log file (with a full path as filename: in the folder of the
experiment file).

If the started experiment fails, or its file does not exist, the main
experiment stops with an error. If the participant aborts the started
experiment (Escape, then Q), a warning is logged and the main experiment
continues.


## Running an experiment without the GUI

The experiment is started with `run_experiment.py`, which is part of this
plugin. It can also be used on its own, as a replacement for
`opensesamerun` (which no longer works in OpenSesame 4.1). Use the Python
interpreter of OpenSesame:

    python run_experiment.py experiment.osexp --subject=3 --logfile=log.csv --fullscreen

Exit codes: 0 = finished, 1 = error, 2 = invalid arguments, 3 = aborted by
the user.


## Installation

Install the plugin with pip, in the Python environment of OpenSesame:

    pip install opensesame-plugin-experiment_manager


## License

This plugin is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version (GPL-3.0-or-later).

The full license text is in the file `COPYING`, and is also available at <https://www.gnu.org/licenses/gpl-3.0.html>.
  
  
## Documentation

Installation instructions and documentation on OpenSesame are available on the documentation website:

- <https://osdoc.cogsci.nl/>
