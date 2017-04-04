def get_param(filename):
    '''Return configuration parameters from config file.
    Config file is python code.
    '''
    config_vars = {}
    try:
        execfile(filename, config_vars)
    except IOError, exc:
        if exc.filename is None:    # execfile() loses filename
            exc.filename = filename
        raise exc
    return config_vars   