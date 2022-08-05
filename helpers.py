import os
import numpy as np
import aplpy
import warnings
from astropy.io import fits
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import rc as rc
from itertools import cycle
rc('text', usetex=True)

# custom settings import
from . import settings as settings

def _set_up_figure(**kwargs):
    """Returns main figure environment

    Returns
    -------
    matplotlib.figure
        Top level container containing all plot elements.
    """
    figsize = kwargs.get('figsize', (8.267, 11.692)) # A4 in inches
    main_fig = plt.figure(figsize=figsize, constrained_layout=True)
    
    return main_fig


def _set_up_panels(main_fig, fitsfiles, shape, colorbar, **kwargs):
    """Constructs the GridSpec environment onto which images will be plotted. Also returns information about the panels that will be plotted.

    Parameters
    ----------
    main_fig : matplotlib.figure
        Top level container for all plot elements.
    fitsfiles : list
        contains filepaths pointing to the FITS images
    shape : tuple
        Used by Gridspec to construct the desired grid shape.
    colorbar : str
        Used by GridSpec to determine if an extra column for the colorbar is needed.

    Returns
    -------
    panels : list
        each entry in the list corresponds to a dictionary of information about the particular panel
    gs : matplotlib.gridspec.GridSpec
        Grid layout to place the subplots
    """
    # default properties for whitespace
    wspace = kwargs.get('wspace', 0.15)
    hspace = kwargs.get('hspace', 0.05)
    
    # turn fitsfiles and titles into iterators
    fitsfiles_iterator = cycle(fitsfiles)
    
    panels = []
    if colorbar == 'all' or colorbar == 'none':
        gs = gridspec.GridSpec(shape[0],
                               shape[1],
                               figure=main_fig,
                               wspace=wspace,
                               hspace=hspace)
    elif colorbar == 'shared':
        width_ratios = [1] * shape[1]
        width_ratios.append(0.05)
        gs = gridspec.GridSpec(shape[0],
                               shape[1]+1,
                               figure=main_fig,
                               wspace=wspace,
                               hspace=hspace,
                               width_ratios=width_ratios)
        
    # add in properties of each panel into panels
    for row in range(shape[0]):
        for col in range(shape[1]):
            
            # load fits file in to gather vmin and vmax values
            fitsfile = next(fitsfiles_iterator)
            with fits.open(fitsfile) as hdul:
                data = hdul[0].data
                vmin = np.nanmin(data)
                vmax = np.nanmax(data)
            
            panels.append({'fitsfile': fitsfile,
                            'row': row,
                            'col': col,
                            'gs': gs[row, col],
                            'vmin': vmin,
                            'vmax': vmax})
            
    return panels, gs
        

def _set_up_panel(fitsfile, main_fig, gs, **kwargs):
    """Plots the fitsfile using aplpy's FITSFigure environment, on the specific gridspec element.

    Parameters
    ----------
    fitsfile : str
        Filepath pointing to the FITS file.
    main_fig : matplotlib.figure
        Top level container for all plot elements.
    gs : matplotlib.gridspec.SubplotSpec
        Specific subplotspec to draw the FITS image onto.

    Returns
    -------
    aplpy.FITSFigure
        Figure environment created by aplpy.
    """
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore')
        fig = aplpy.FITSFigure(fitsfile,
                               figure=main_fig,
                               subplot=list(gs.get_position(main_fig).bounds))
    return fig


def _show_map(fig, vmin_val, vmax_val, **kwargs):
    """Displays the colorscale map for the input aplpy figure, according to the input vmin and vmax bounds."""
    cmap = kwargs.get('cmap', 'viridis')
    stretch = kwargs.get('stretch', 'linear')
    aspect = kwargs.get('aspect', 'equal')
    
    fig.show_colorscale(cmap=cmap, vmin=vmin_val, vmax=vmax_val, stretch=stretch, aspect=aspect)


def _show_title(fig, title):
    """Sets the title for the aplpy figure environment."""
    fig.set_title(title)

   
def _show_colorbar_all(fig, **kwargs):
    """Displays the colorbar to the side of the aplpy FITSFigure."""
    fig.add_colorbar()
    fig.colorbar.set_location(settings.colorbar_location)
    #fig.colorbar.set_axis_label_text()
    fig.colorbar.set_axis_label_pad(settings.colorbar_labelpad)
    fig.colorbar.set_font(size=settings.colorbar_label_fontsize)
    fig.colorbar.set_axis_label_font(size=settings.colorbar_label_fontsize)
    fig.colorbar.set_frame_color(settings.frame_color)

   
def _show_colorbar_shared(main_fig, gs, vmin_val, vmax_val, **kwargs):
    """Adds a shared colorbar to the given subplotspec environment passed in.

    Parameters
    ----------
    main_fig : matplotlib.Figure
        Top level container.
    gs : matplotlib.gridspec.SubplotSpec
        Location where colorbar will display.
    vmin_val : float
        Minimum value of the colorbar.
    vmax_val : float
        Maximum value of the colorbar.
    """
    # grab a cmap object
    cmap = kwargs.get('cmap', 'viridis')
    if isinstance(cmap, str):
        cmap = plt.get_cmap(cmap)
    
    # create new axes on the gridspec object given
    ax1 = main_fig.add_axes(list(gs.get_position(main_fig).bounds))
    
    # implementing colorbar
    sm = mpl.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin_val, vmax=vmax_val))
    cb = plt.colorbar(sm, cax=ax1)
    

def _show_ticksNlabels(fig, gs, trim, **kwargs):
    """Sets the ticks, tick labels, and axis label settings. Rids of internal x and y ticks, tick labels, and axis labels when appropriate."""
    fig.tick_labels.set_xformat(settings.tick_label_xformat)
    fig.tick_labels.set_yformat(settings.tick_label_yformat)
    fig.tick_labels.set_font(size=settings.tick_label_fontsize)
    #fig.ticks.set_xspacing((settings.ticks_xspacing).to(u.degree).value)
    #fig.ticks.set_yspacing((settings.ticks_yspacing).to(u.degree).value)
    fig.ticks.set_minor_frequency(settings.ticks_minor_frequency)
    fig.ticks.set_length(settings.tick_length)
    fig.ticks.set_color(settings.ticks_color)
    fig.frame.set_color(settings.frame_color)
    fig.axis_labels.set_font(size=settings.tick_label_fontsize)
    
    # check for trim flag and trim appropriately
    if trim == 'inner':
        if not gs.is_first_col():
            fig.axis_labels.hide_y()
        if not gs.is_last_row():
            fig.axis_labels.hide_x()

    elif trim == 'all':
        if not gs.is_first_col():
            fig.axis_labels.hide_y()
            fig.tick_labels.hide_y()
            fig.ticks.hide_y() 
        if not gs.is_last_row():
            fig.axis_labels.hide_x()
            fig.tick_labels.hide_x()
            fig.ticks.hide_x()
    
    elif trim == 'full':
        fig.axis_labels.hide_x()
        fig.tick_labels.hide_x()
        fig.ticks.hide_x()
        fig.axis_labels.hide_y()
        fig.tick_labels.hide_y()
        fig.ticks.hide_y()
    
def _save_figure(fitsfile, main_fig, **kwargs):
    """Saves the figure.

    Parameters
    ----------
    fitsfile : str
        Used to set output location if `title` is not given in `**kwargs`.
    main_fig : matplotlib.figure
        Figure environment to save.
    """
    out = kwargs.get('out', os.path.splitext(fitsfile)[0]+'.png')
    if isinstance(out, str):
        main_fig.savefig(out, dpi=300, transparent=False, bbox_inches='tight')
    elif out == None:
        plt.show()
    else:
        plt.show()


def _setup_map(main_fig, fitsfile):
    fig = aplpy.FITSFigure(fitsfile,
                           figure=main_fig)
    
    return fig