from itertools import cycle

# load helper functions
from _helpers import (
    _set_up_figure, _set_up_panels, _set_up_panel,
    _show_map, _save_figure,
    _show_ticksNlabels, _show_title,
    _show_colorbar_shared, _show_colorbar_all
)

# plot a grid of maps
#####################
def grid(fitsfiles, shape, colorbar='all', colorbar_bounds='auto', titles=None, plot_title=None, trim='inner', **kwargs):
    """Provides a simple interface to APLpy plots. This function generates a single image output, of a series of images in a grid, given by the desired input shape.

    Parameters
    ----------
    fitsfiles : list
        List of filepath strings which point to the FITS images to be plotted.
    shape : tuple
        Constructs a `shape[0] x shape[1]` grid of images. Total number of grids must match length of `fitsfiles` inputted.
    colorbar : str, optional
        Sets the number of colorbars drawn., by default 'all'.
            - 'all' will draw a colorbar beside each grid image.
            - 'shared' will draw a shared colorbar on the right hand side of the grid layout.
            - 'none' will bypass all colorbar drawing.
    colorbar_bounds : str, optional
        Sets whether the colorbar minimum and maximum values are automatically computed, or grabbed from vmin and vmax arguments by default 'auto'.
            - 'auto' will either set the scale per image (`colorbar='all'`) or set the scale globally (`colorbar='shared')
            - 'manual' will set the scale either per image or globally via the input `vmin` and `vmax` keyword arguments.
    titles : list, optional
        List of subplot titles. `None` will skip drawing titles, by default None.
    plot_title : str, optional
        Sets the overall figure title, by default None.
    trim_inner " str, optional
        Sets how much trimming occurs for ticks, tick labels and axis labels, by default 'inner'. 
            - 'inner' will only trim the inner axis labels, but leave ticks and tick labels. 
            - 'all' will trim all inner axis labels, ticks, and tick labels.
            - 'full' will trim all aforementioned inner properties, and outer axis labels, tick and tick labels.
        

    Optional Keyword Parameters - **kwargs
    ----------
    figsize : tuple
        Sets the figure size by matplotlib.figure call, default is `(8.267, 11.692)`. Advisable to keep as equal aspect as possible.
    wspace : float
        Sets the horizontal padding between grid elements by matplotlib.gridspec.GridSpec call, default is 0.15.
    hspace : float
        Sets the vertical padding between grid elements by matplotlib.gridspec.GridSpec call, default is 0.05.
    cmap : str
        Sets the colormap type used by aplpy FITSFigure show_colorscale call, default is 'viridis'.
    stretch : str
        Sets the stretch used by aplpy FITFigure show_colorscale call, default is 'linear'. No other options supported.
    aspect : str
        Sets the aspect used by aplpy FITFigure show_colorscale call, default is 'equal. No other options supported.
    out : str
        Sets the output filename for the matplotlib.figure.savefig call, default is set to the location of the input FITS image.
        

    Returns
    -------
    main_fig : matplotlib.figure
        Top level container.
    subfigs : list of aplpy.FITSFigure
        Contains aplpy.FITSFigures that are drawn to the grid.
    gs : matplotlib.gridspec.GridSpec
        Conatins the GridSpec object used to place FITS images.
    """
    # start of plotting
    main_fig = _set_up_figure(**kwargs)
    panels, gs = _set_up_panels(main_fig, fitsfiles, shape, colorbar, **kwargs)
    
    # grabbing global vmin and vmax if needed
    if colorbar == 'shared' and colorbar_bounds == 'auto':
        
        # grab global vmin and vmax values for all panels
        global_vmin = 100
        global_vmax = -100
        for panel in panels:
            if panel['vmin'] < global_vmin:
                global_vmin = panel['vmin']
            if panel['vmax'] > global_vmax:
                global_vmax = panel['vmax']
                
    # creating title iterator if given
    if titles is not None:
        titles_iterator = cycle(titles) # create iterator
    
    # plotting grids
    subfigs = []
    for panel in panels:
        # pull out fitsfile and current gridspec
        fitsfile = panel['fitsfile']
        gs_current = panel['gs']
        
        # construct the panel
        fig = _set_up_panel(fitsfile, main_fig, gs_current, **kwargs)
        
        # show the image
        if colorbar_bounds == 'auto':
            if colorbar == 'all' or colorbar == 'none':
                _show_map(fig, None, None, **kwargs)
            elif colorbar == 'shared':
                _show_map(fig, global_vmin, global_vmax, **kwargs)
        elif colorbar_bounds == 'manual':
            _show_map(fig, kwargs['vmin'], kwargs['vmax'], **kwargs)
        
        # add in tick and label properties
        _show_ticksNlabels(fig, gs_current, trim, **kwargs)
        
        # individual colorbar
        if colorbar == 'all':
            _show_colorbar_all(fig, **kwargs)

        # add in titles
        if titles is not None:
            _show_title(fig, next(titles_iterator))
        
        # append the panels to the list of subfigures
        subfigs.append(fig)

    # shared colorbar
    if colorbar == 'shared':
        if colorbar_bounds == 'auto':
            _show_colorbar_shared(main_fig, gs[:, -1], global_vmin, global_vmax, **kwargs)
        elif colorbar_bounds == 'manual':
            _show_colorbar_shared(main_fig, gs[:, -1], kwargs['vmin'], kwargs['vmax'], **kwargs)

    # add in plot title if given
    if isinstance(plot_title, str):
        main_fig.suptitle(plot_title)

    # saving plot
    _save_figure(fitsfile, main_fig, **kwargs)

    return main_fig, subfigs, gs
