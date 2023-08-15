"""A docstring with a description of the plugin"""

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
        "label": "<b>IMPORTANT:</b> The experiment should be started in "
        "windowed mode!\n",
        "type": "text"
    }, {
        "label": "<small><b>Note:</b> Parallel Port Trigger Init item "
        "at the begin of the experiment is needed for "
        "initialisation of the parallel port</small>\n",
        "type": "text"
    }, {
        "label": "<small>Experiment Manager version 3.0.0</small>\n",
        "type": "text"
    }
]