

class SiteMap(object):
    """
    """
    def __init__(self, name):
        self.name = name


class BreadCrumb(object):

    link_html = '<a href="%s" title="%s">%s</a>'

    def __init__(self, sitemap_obj, separator, encoding):
        self.sitemap = sitemap_obj
        self.separator = separator
        self.encoding = encoding

    def breadcrumb(self, request):
        return                 
