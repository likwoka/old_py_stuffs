from kid import Template

from quixote.directory import Resolving, Directory
from quixote.util import StaticDirectory
from quixote import get_publisher

from bookie.controllers.bookmarks import BookmarksDirectory


        
class RootDirectory(Resolving, Directory):
    
    _q_exports = [""]
    def _q_index(self):
        return Template(name="bookie.views.root").serialize()


    _q_exports += ["test"]
    def test(self):
        """
        For testing the kid template.
        """
        return Template(name="bookie.views.test").serialize()


    _q_exports += ["qtest"]
    def qtest(self):
        """
        For testing quixote.
        """
        from quixote.util import dump_request
        return dump_request()


    _q_exports += ["login"]
    def login(self):
        return Template(name="bookie.views.login").serialize()


    _q_exports += ["logout"]
    def logout(self):
        return Template(name="bookie.views.login").serialize()


    def _q_lookup(self, component):
        user_mgr = get_publisher().context.user_mgr
        
        if user_mgr.has_user(component):
            return BookmarksDirectory(component)
        else:
            return None


    _q_exports += ["static"]
    def _q_resolve(self, name):
        if name == "static":
            return StaticDirectory(
                   get_publisher().context.app_options.get(
                   "server", "static_content"))
  



