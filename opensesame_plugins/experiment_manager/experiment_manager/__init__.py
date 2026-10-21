"""Runs another OpenSesame experiment"""

from .. import __version__

# The category determines the group for the plugin in the item toolbar
category = "control"
# Defines the GUI controls
controls = [
    {
        "label": "Dummy Mode",
        "name": "checkbox_dummy",
        "tooltip": "Run in dummy mode",
        "type": "checkbox",
        "var": "dummy_mode"
    }, {
        "label": "Verbose Mode",
        "name": "checkbox_verbose",
        "tooltip": "Show actions in debug window",
        "type": "checkbox",
        "var": "verbose"
    }, {
        "label": "Experiment file name",
        "name": "filepool_experiment_file_name",
        "tooltip": "File name of the experiment",
        "type": "filepool",
        "var": "filename"
    }, {
        "label": "<b>Note:</b> With the legacy backend, start the main "
        "experiment in windowed mode: in fullscreen mode it may not get the "
        "keyboard back after the started experiment. With the PsychoPy "
        "backend, fullscreen mode works.\n",
        "type": "text"
    }, {
        "label": f"<small>Experiment Manager version {__version__}</small>\n",
        "type": "text"
    }
]
