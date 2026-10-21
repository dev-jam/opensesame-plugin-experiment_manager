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

Runs a single OpenSesame experiment without the GUI. This replaces the
opensesamerun command, which no longer works in OpenSesame 4.1, and accepts
its options --subject, --logfile and --fullscreen.

Usage: python run_experiment.py experiment.osexp [--subject=N]
       [--logfile=FILE] [--fullscreen]
"""

__author__ = "Bob Rosbag"
__license__ = "GPLv3"

import os
import sys
import argparse
import traceback
from enum import IntEnum


class ExitCode(IntEnum):
    OK = 0
    ERROR = 1
    INVALID_ARGUMENTS = 2  # also used by argparse and by Python itself
    USER_ABORTED = 3


def run_experiment(exp_file_path, subject_nr=0, log_file_path=None,
                   fullscreen=False):
    """Runs an experiment and returns an ExitCode.

    libopensesame is imported here, so that importing this module (for
    ExitCode) and printing the help text stay fast.
    """
    from libopensesame.experiment import Experiment

    exp_file_path = os.path.abspath(exp_file_path)
    if not os.path.isfile(exp_file_path):
        print(f"Experiment file not found: {exp_file_path}", file=sys.stderr)
        return ExitCode.ERROR
    if log_file_path is None:
        log_file_path = f"subject-{subject_nr}.csv"

    # As opensesamerun did, pass the file path: this also sets experiment_file
    exp = Experiment('Experiment', exp_file_path,
                     experiment_path=exp_file_path, fullscreen=fullscreen,
                     subject_nr=subject_nr,
                     logfile=os.path.abspath(log_file_path))
    try:
        # run() seeds the random generators and calls end() itself when the
        # experiment finishes normally
        exp.run()
        return ExitCode.OK
    except Exception as e:
        user_aborted = _user_aborted(e)
        if user_aborted is None:
            traceback.print_exc()
            exit_code = ExitCode.ERROR
        else:
            print(f"Experiment aborted by the user: {user_aborted}",
                  file=sys.stderr)
            exit_code = ExitCode.USER_ABORTED
        _end(exp)
        return exit_code
    finally:
        exp.pool.clean_up()


def _user_aborted(e):
    """Returns the UserAborted exception that caused e, or None.

    An inline_script wraps every exception in a PythonError, so an abort
    with Escape during keyboard.get_key() in an inline script only shows up
    in the chain of causes.
    """
    from libopensesame.exceptions import UserAborted

    while e is not None:
        if isinstance(e, UserAborted):
            return e
        e = e.__cause__ or e.__context__
    return None


def _end(exp):
    """Closes the display, sound and log after an experiment was
    interrupted.
    """
    try:
        exp.end()
    except Exception:
        traceback.print_exc()


def parse_args(argv):
    parser = argparse.ArgumentParser(
        prog='run_experiment.py',
        description='Run an OpenSesame experiment without the GUI '
                    '(replacement for opensesamerun)',
        epilog='Exit codes: 0 = finished, 1 = error, 2 = invalid arguments, '
               '3 = aborted by the user')
    parser.add_argument('experiment', help='experiment file (.osexp)')
    parser.add_argument('-s', '--subject', type=int, default=0,
                        help='subject number (default: 0)')
    parser.add_argument('-l', '--logfile',
                        help='log file (default: subject-<nr>.csv)')
    parser.add_argument('-f', '--fullscreen', action='store_true',
                        help='run fullscreen')
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    return run_experiment(args.experiment, args.subject, args.logfile,
                          args.fullscreen)


if __name__ == '__main__':
    sys.exit(main())
