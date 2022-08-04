# easy_aplpy_v2
Improved wrapper functions for the APLpy plotting package. Heavily inspired by GiantMolecularCloud's easy_aplpy package. Many portions of code, and entire files (like `_settings.py`) have been used from easy_aplpy.

For details on APLpy see https://aplpy.readthedocs.io/en/stable/#.

For details on GiantMolecularCloud/easy_aplpy see https://github.com/GiantMolecularCloud/easy_aplpy.

These wrapper functions work very similar to easy_aplpy's wrapper functions, but where as easy_aplpy's wrapper functions plot only one specific FITS file at a time, these wrapper functions take many FITS filepaths, and plot them in a grid.

# Available Wrappers:

## easy_aplypy_v2.grid

A one-liner to plot a grid of images that looks good by default. 

Also provides many keyword arguments to customize the plot, depending mainly on whether individual colorbars, or one shared colorbar is needed.

By default, inner x and y axis labels are trimmed, but ticks and tick labels are included. The `trim_fully` flag can be set to `True` if all inner properties are to be trimmed.

# Dependencies

This code was developed and only tested on the specific versions listed below:

* astropy == 5.1
* aplpy == 2.1.0
* matplotlib == 3.5.2

# Settings

Found in `_settings.py` is a list of default parameters, used by the plotting modules to customize the plots. This file is found in GiantMolecularCloud's repository. Slight changes have been made.
