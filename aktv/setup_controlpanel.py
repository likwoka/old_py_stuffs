from distutils.core import setup
import py2exe
setup(name='controlpanel',
      version='0.1',
      description='AKTV Control Panel',
      author='Alex Li',
      author_email='likwoka@yahoo.com',
      scripts=['controlpanel.py'],
      data_files=[('', ['aktvcp.ini'])])