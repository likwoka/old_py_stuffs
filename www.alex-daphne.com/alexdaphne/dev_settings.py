from alexdaphne.settings import *

from os import path
root = 'd:/alex/sandbox/_my_/www.alex-daphne.com/'

DEBUG          = True
TEMPLATE_DEBUG = DEBUG
DATABASE_NAME  = path.join(root, 'database.db')
MEDIA_ROOT     = path.join(root, 'public_html/media/')
TEMPLATE_DIRS += (
    path.join(root, 'alexdaphne/templates/'),
)
