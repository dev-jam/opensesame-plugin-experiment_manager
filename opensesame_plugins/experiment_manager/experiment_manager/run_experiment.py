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
opensesamerun command, which was removed in OpenSesame 4.1, and accepts the
same options.

Usage: python run_experiment.py experiment.osexp [--subject=N]
       [--logfile=FILE] [--fullscreen]

Exit codes: 0 = finished, 1 = error, 2 = invalid arguments, 3 = aborted by
the user
"""

__author__ = "Bob Rosbag"
__license__ = "GPLv3"

import os
import sys
import random
import argparse
import traceback

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_USER_ABORTED = 3


def parse_args(argv):
    parser = argparse.ArgumentParser(
        prog='run_experiment.py',
        description='Run an OpenSesame experiment without the GUI '
                    '(replacement for opensesamerun)')
    parser.add_argument('experiment', help='Experiment file (.osexp)')
    parser.add_argument('-s', '--subject', type=int, default=0,
                        help='Subject number (default: 0)')
    parser.add_argument('-l', '--logfile',
                        help='Log file (default: subject-<nr>.csv)')
    parser.add_argument('-f', '--fullscreen', action='store_true',
                        help='Run fullscreen')
    args = parser.parse_args(argv)
    if args.logfile is None:
        args.logfile = f"subject-{args.subject}.csv"
    return args


def main(argv):
    args = parse_args(argv)
    exp_file_path = os.path.abspath(args.experiment)
    if not os.path.isfile(exp_file_path):
        print(f"Experiment file not found: {exp_file_path}", file=sys.stderr)
        return EXIT_ERROR

    from libopensesame.experiment import Experiment
    from libopensesame.exceptions import UserAborted

    exp = Experiment('Experiment', exp_file_path,
                     experiment_path=os.path.dirname(exp_file_path))
    exp.set_subject(args.subject)
    exp.var.fullscreen = 'yes' if args.fullscreen else 'no'
    exp.logfile = os.path.abspath(args.logfile)
    random.seed()
    try:
        # run() calls end() itself when the experiment finishes normally
        exp.run()
    except UserAborted as e:
        _end(exp)
        print(f"Experiment aborted by the user: {e}", file=sys.stderr)
        return EXIT_USER_ABORTED
    except Exception:
        _end(exp)
        traceback.print_exc()
        return EXIT_ERROR
    finally:
        exp.pool.clean_up()
    return EXIT_OK


def _end(exp):
    try:
        exp.end()
    except Exception:
        traceback.print_exc()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
