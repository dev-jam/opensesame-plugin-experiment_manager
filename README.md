OpenSesame Plug-in: Experiment Manager
==========

*An OpenSesame plug-in for managing/executing multiple OpenSesame experiments.*  

Copyright, 2015-2026, Bob Rosbag  


## About

This plug-in can insert standalone OpenSesame Experiments within a main experiment. 
It can run within a loop or sequence as an item. This makes it possible to run a number 
of experiments in sequence (random or fixed order) and also it gives the possibility to 
give each experiment its own (different) backend. 

This plug-in has three options:

- *Dummy mode* for testing experiments.
- *Verbose mode* for testing experiments.
- *Experiment filename* full path or filename.

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
plug-in. It can also be used on its own, as a replacement for
`opensesamerun` (which no longer works in OpenSesame 4.1). Use the Python
interpreter of OpenSesame:

    python run_experiment.py experiment.osexp --subject=3 --logfile=log.csv --fullscreen

Exit codes: 0 = finished, 1 = error, 2 = invalid arguments, 3 = aborted by
the user.


## License

This software is distributed under the terms of the GNU General Public License 3. The full license should be included in the file `COPYING`, or can be obtained from:

- <https://www.gnu.org/licenses/gpl.txt>
  
  
## Documentation

Installation instructions and documentation on OpenSesame are available on the documentation website:

- <https://osdoc.cogsci.nl/>
