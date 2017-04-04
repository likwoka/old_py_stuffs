from quixote.directory import AccessControlled, Directory
from quixote import get_publisher, get_session
from quixote.errors import AccessError

from bookie.models.bookmarks import Folder, Bookmark, Bookmarks



class BookmarksDirectory(AccessControlled, Directory):

    def __init__(self, username):
        bookmarksdb = get_publisher().context.bookmarksdb
        self.bookmarks = bookmarksdb[username]
    
    
    _q_exports = [""]
    def _q_index(self):
        return "this is the bookmark list"


    def _q_access(self):
        session = get_session()
        if not session.user:
            raise AccessError


    _q_exports += ["options"]
    def options(self):
        return "set options"


    _q_exports += ["addfolder"]
    def addfolder(self):
        return "form"
        

    _q_exports += ["addbookmark"]
    def addbookmark(self):
        return "form"


    def _q_lookup(self, component):
        if component in self.bookmarks:
            return FolderDirectory(self.bookmarks[component], component)
        else:
            return None
            
        

class FolderDirectory(Directory):

    def __init__(self, bookmarks, component):
        self.bookmarks = bookmarks
        self.name = component


    _q_exports = [""]
    def _q_index(self):
        return "list of directory"    


    _q_exports += ["edit"]
    def edit(self):
        return "form"


    _q_exports += ["move"]
    def move(self):
        return "form"

    
    _q_exports += ["delete"]
    def delete(self):
        return "form"


    _q_exports += ["addbookmark"]
    def addbookmark(self):
        return "form"


    _q_exports += ["addfolder"]
    def addfolder(self):
        return "form"


    def _q_lookup(self, component):
        if component in self.bookmarks:
            return FolderDirectory(self.bookmarks[component], component)
        else:
            return None
        


class BookmarkDirectory(Directory):
    
    def __init__(self):
        pass


