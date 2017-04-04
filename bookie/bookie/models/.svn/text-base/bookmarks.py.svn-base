"""Bookmarks-handling classes."""


from silverlib.objectstores import dirdb
import os



class Bookmark(object):
    """Represent a link."""
    
    attrs = ["href",
             "add_date",
             "last_visit",
             "icon",
             "last_charset",
             "shortcuturl",]
    
    text = ["title", "comment"]


class Folder(object):
    """
    A list-like class represents a category of links.  Can contain 
    both sub-category or link instances.  Note that it is legal
    to have duplicate sub-catagories or links.
    """

    attrs = ["add_date",
             "last_modified",
             "folder_group",
             "id",
             "personal_toolbar_folder",]

    text = ["title", "comment"]


    def __init__(self):
        self.subcats = []
        self.links = []
        self.is_open = False


    def append(self, obj):
        if obj.__class__ == Bookmark:
            self.links.append(obj)
            self.sort_links()
        elif obj.__class__== Folder:
            self.subcats.append(obj)
            self.sort_subcats()
        else:
            raise TypeError('should be type <Bookmark> or <Folder>')


    def sort_subcats(self):
        self.subcats.sort(self._textcmp)


    def sort_links(self):
        self.links.sort(self._textcmp)


    def recur_sort(self):
        self.sort_links()
        self.sort_subcats()
        for subcat in self.subcats:
            subcat.recur_sort()


    def _textcmp(self, x, y):
        '''
        Return the result of the comparison on the title attributes
        of x and y objects.  Sort is case-insensitive.
        '''
        xrep = getattr(x, 'title', 'None').upper()
        yrep = getattr(y, 'title', 'None').upper()
        
        if xrep < yrep:
            return -1
        elif xrep == yrep:
            return 0
        else:
            return 1 


    def __iter__(self):
        return iter(self.subcats + self.links)


    def __len__(self):
        return (self.subcats + self.links).__len__()


    def index(self, item):
        return (self.subcats + self.links).index(item)


    def __contains__(self, item):
        return self.subcats.__contains__(item) or \
               self.links.__contains__(item)

    def __getitem__(self, index):
        return (self.subcats + self.links).__getitem__(index)


    def __setitem__(self, index, item):
        cats = len(self.subcats)
        if index < cats:
            self.subcats.__setitem__(index, item)
            self.sort_subcats()
        else:
            self.links.__setitem__(index - cats, item)
            self.sort_links()


    def __delitem__(self, index):
        cats = len(self.subcats)
        if index < cats:
            self.subcats.__delitem__(index)
        else:
            self.links.__delitem__(index - cats)


class Bookmarks(Folder):
    title = 'Bookmarks'


class BookmarksDB(dirdb.CachingDirStore):
    """
    The bookmark database.  Each key is a username (string),
    each item is a Bookmarks instance.
    """
    
    def __setitem__(self, key, value):
        # Do type checking.
        if not isinstance(value, Bookmarks):
            raise TypeError("Value has to an instance of "
                            "Bookmarks or its subclasses.")
        dirdb.CachingDirMapping.__setitem__(self, key, value)


#---------------------------------------------------------------------------
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


class BookmarkExporter:
    """
    Read a Bookmarks instance and output a bookmarks.html 
    (Mozilla boomark) file.
    """
    def __init__(self):
        self.reset()


    def reset(self):
        self._bm = None
        self._out = StringIO()
        self.output = None
        

    def close(self):
        self.output = self._out.getvalue()
        self._out.close()


    def parse(self, bookmark_instance):
        self._bm = bookmark_instance
        f = self._out
        f.write('<!DOCTYPE NETSCAPE-Bookmark-file-1>\n')
        f.write('<!-- This is an automatically generated file.\n')
        f.write('It will be read and overwritten.\n')
        f.write('Do Not Edit! -->\n')
        f.write('<META HTTP-EQUIV="Content-Type" CONTENT="text/html;'
                'charset=UTF-8">\n')
        f.write('<TITLE>Bookmarks</TITLE>\n')
        f.write('<H1>Bookmarks</H1>\n\n')
        self._walk(self._bm)


    def _walk(self, category):
        self._out.write('<DL><p>\n')
        
        for item in category:
            if item.__class__ == Folder:
                self._write_obj(item, 'H3')
                self._walk(item)
            elif item.__class__ == Bookmark:
                self._write_obj(item, 'A')
        
        self._out.write('</DL><p>\n')


    def _write_obj(self, obj, tag):
        attrs = []
        for k in obj.attrs:
            v = getattr(obj, k, None)
            if v is not None:
                attrs.append('%s="%s"' % (k, v))
            
        self._out.write('<DT><%s %s>%s</%s>\n' % (tag, ' '.join(attrs),
                                                  obj.title, tag))
        if 'comment' in obj.__dict__:
            self._out.write('<DD>%s\n' % obj.comment)
     
     
#---------------------------------------------------------------------------
from htmllib import HTMLParser
from formatter import NullFormatter


class _BookmarkParser(HTMLParser):
    
    def __init__(self):
        HTMLParser.__init__(self, NullFormatter())


    def reset(self):
        self._data_is_title = False
        self._data_is_comment = False
        self.output = None
        self._current = None
        self._container = []
        HTMLParser.reset(self)


    def start_h1(self, attrs):
        self._current = Bookmarks()
        self.output = self._current


    def start_dl(self, attrs):
        self._container.append(self._current)


    def end_dl(self):
        self._container.pop()


    def start_h3(self, attrs):
        self._parse_tag(attrs, Folder)


    def start_a(self, attrs):
        self._parse_tag(attrs, Bookmark)


    def _parse_tag(self, attrs, obj_class):
        self._current = obj_class()
        self._container[-1].append(self._current)
        self._data_is_title = True
        for k, v in attrs:
            setattr(self._current, k, v)


    def start_dd(self, attrs):
        self._data_is_comment = True
    

    def handle_data(self, data):
        if self._data_is_title:
            self._current.title = data
            self._data_is_title = False
        elif self._data_is_comment:
            self._current.comment = data
            self._data_is_comment = False
       
       
class BookmarkImporter:
    """
    Read and parse a bookmarks.html (Mozilla bookmark) 
    file and return a Bookmarks instance.
    """
    def __init__(self):
        self._parser = _BookmarkParser()
        self.reset()
    
    
    def reset(self):
        self.output = None
        self._parser.reset()
    
    
    def parse(self, path):
        data = file(path, 'r').read()
        self._parser.feed(data)


    def close(self):
        self._parser.close()
        self.output = self._parser.output

