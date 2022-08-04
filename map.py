# load helper functions
from _helpers import (
    _set_up_figure, _setup_map,
    _show_map, _show_title,
    _show_colorbar_all, _save_figure
)

# plot a map
def map(fitsfile, colorbar=True, title=None, **kwargs):
    
    main_fig = _set_up_figure(**kwargs)
    fig = _setup_map(main_fig, fitsfile)
    _show_map(fig, None, None)
    
    if title is not None:
        _show_title(fig, title)

    _show_colorbar_all(fig)
    _save_figure(fitsfile, main_fig)
    
    return main_fig, fig
    