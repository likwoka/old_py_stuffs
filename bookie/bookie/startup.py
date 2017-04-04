from quixote.config import Config

from silverlib.configuration import configure
from silverlib.user import UserManager
from silverlib.objectstores.dirdb import CachingDirStore
from silverlib.quixote.session import FixedTimeoutSessionManager, SessionReaper
from silverlib.quixote.publish import ThreadedPublisher

from bookie.configuration import schema
from bookie.session import Session
from bookie.controllers.root import RootDirectory


class Context:
    """
    This class represents the context of the application.  
    It stores global resources for a publisher, as a result,
    other part of the system can access those global resources
    through the publisher.
    """
    pass


def run(server_start, quixote_conf, app_conf):
    """
    Run this application.
    
    server_start -- a function that starts a particular type of server.
                    Specifically, a quixote.server.xxx_server.run function.
    quixote_conf -- a string of path to the Quixote configuration file.
    app_conf -- a string of path to the application configuration file.
    """
    
    app_options = configure(app_conf, schema)

    ctx = Context()
    ctx.app_options = app_options
    ctx.user_mgr = UserManager(CachingDirStore(app_options.get(
                               "bookie", "user_store")))
    ctx.bookmarksdb = CachingDirStore(app_options.get(
                                      "bookie", "bookmarks_store"))

    # Sessions will timed out after 2 days.
    session_mgr = FixedTimeoutSessionManager(Session, {})
    session_mgr.timeout_in_min = 2880
    
    config_obj = Config()
    config_obj.read_file(quixote_conf)

    # A background thread to clean up expired session
    # every 60 mins.
    SessionReaper(60, session_mgr).start()

    # The publisher factory function.
    def create_publisher():
        publisher = ThreadedPublisher(RootDirectory(),
                                      session_manager=session_mgr,
                                      config=config_obj)
        publisher.context = ctx
        return publisher

    server_start(create_publisher,
                 host=app_options.get("server", "host"),
                 port=app_options.get("server", "port"))

