def hide_UserWarning_DrawCall():
    try:
        import warnings
        warnings.filterwarnings(action='ignore',
                                category=UserWarning,
                                message='There are no gridspecs with layoutgrids.')
    except:
        print('easy_aplpy_v2: Could not suppress UserWarnings outputted by aplpy when calling .draw() method on FITSFigure.')