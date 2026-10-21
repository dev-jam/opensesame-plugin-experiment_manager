# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

- fixed: since 4.0.0, a dummy mode value other than 'yes' or 'no' (e.g. from
  a variable) started the experiment; 3.2.0 did not start it and only logged
  a message. Now it raises an error
- fixed: since 4.0.0, when the participant aborted the started experiment
  (Escape, then Q) during a key wait in an inline script, the main experiment
  stopped with an error instead of logging a warning and continuing
- remove a note about the parallel port trigger plug-in from the item, which
  was copied from that plug-in
- describe the file lookup, the log file, errors and the use of
  run_experiment.py on its own in the readme; links use https
- code cleanup
- run_experiment.py passes subject, fullscreen and log file to the
  Experiment constructor, as OpenSesame's own runner does, and no longer
  seeds random itself (Experiment.run() already does)
- the main experiment no longer has to run windowed: fullscreen works with
  the PsychoPy backend; with the legacy backend, windowed is still advised,
  because the main experiment may not get the keyboard back
- dummy mode also checks that the experiment file exists, so a dummy run
  fails like a real run

## [4.0.3] - 2026-10-18

- the experiment is looked up in the log file folder first again, as in 3.2.0,
  and only then in the file pool and the experiment folder
- the started experiment logs `experiment_file` again, as with opensesamerun

## [4.0.2] - 2026-10-17

- the version label in the item is read from the installed package, so the
  version is only set in `pyproject.toml`

## [4.0.1] - 2026-10-17

- fixed license in package metadata (was shown as proprietary on PyPI)
- fix dependency

## [4.0.0] - 2026-10-16

- fix running experiments on OpenSesame 4.1, where opensesamerun was removed:
  experiments are now started with run_experiment.py and the Python
  interpreter that runs OpenSesame
- run_experiment.py can also be used on its own as a replacement for
  opensesamerun, with the same options (--subject, --logfile, --fullscreen)
- raise an error when the started experiment fails, instead of silently
  continuing; when it is aborted by the user, log a warning and continue
- raise an error when the experiment file does not exist
- look up the experiment in the file pool and the experiment folder first,
  and then in the log file folder as before
- remove the unused qtExperimentManager class; OpenSesame creates the GUI
  class itself, so the runtime part no longer imports Qt
- read dummy mode and verbose mode in the prepare phase, so that changes
  made by other items during the run phase do not affect them; the filename
  is still read in the run phase, so that an earlier item can select the
  experiment
- replace the placeholder plugin description
- code cleanup

## [3.2.0] - 2025-09-05

- convert string handling to f-strings

## [3.1.0] - 2025-07-17

- license cleanup

## [3.0.1] - 2023-08-30

- fixed dependencies
    
## [3.0.0] - 2023-08-15

- new style api OpenSesame 4.0
- lots of small fixes and code cleanup
    
## [2.4.0] - 2023-08-13

Final release for OpenSesame 3 API

- small bugfixes
    
## [v2.3.0] - 2022-11-25

- new plugin code style
- debian packaging fixed
    
## [v2.0] - 2016-01-22

- Opensesame 3 style


## v1.0 - 2015-03-16



[Unreleased]: https://github.com/dev-jam/opensesame-plugin-experiment_manager/compare/4.0.3...HEAD
[4.0.3]: https://github.com/dev-jam/opensesame-plugin-experiment_manager/compare/4.0.2...4.0.3
[4.0.2]: https://github.com/dev-jam/opensesame-plugin-experiment_manager/compare/4.0.1...4.0.2
[4.0.1]: https://github.com/dev-jam/opensesame-plugin-experiment_manager/compare/4.0.0...4.0.1
[4.0.0]: https://github.com/dev-jam/opensesame-plugin-experiment_manager/compare/3.2.0...4.0.0
[3.2.0]: https://github.com/dev-jam/opensesame-plugin-experiment_manager/compare/3.1.0...3.2.0
[3.1.0]: https://github.com/dev-jam/opensesame-plugin-experiment_manager/compare/3.0.1...3.1.0
[3.0.1]: https://github.com/dev-jam/opensesame-plugin-experiment_manager/compare/3.0.0...3.0.1
[3.0.0]: https://github.com/dev-jam/opensesame-plugin-experiment_manager/compare/2.4.0...3.0.0
[2.4.0]: https://github.com/dev-jam/opensesame-plugin-experiment_manager/compare/v2.3.0...2.4.0
[v2.3.0]: https://github.com/dev-jam/opensesame-plugin-experiment_manager/compare/v2.0...v2.3.0
[v2.0]: https://github.com/dev-jam/opensesame-plugin-experiment_manager/compare/v1.0...v2.0
