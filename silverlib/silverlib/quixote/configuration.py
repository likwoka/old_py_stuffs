from silverlib.configuration import configure as _configure


_schema = {"server" : {"host" : ("str", "localhost"),
                       "port" : ("int", 8080),},
           "session" : {"storage" : ("str", "ram"),
                        "timeout" : ("int", 60),
                        "cleanup_delay" : ("int", 30),},
           "static_content" : {},
           }


def configure(path, app_schema=None):
    if app_schema is not None:
        _schema.update(app_schema)
    
    return _configure(path, _schema)

