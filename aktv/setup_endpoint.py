from distutils.core import setup
import py2exe
setup(name='endpoint',
      version='0.1',
      description='AKTV Endpoint',
      author='Alex Li',
      author_email='likwoka@yahoo.com',
      scripts=['endpoint.py'],
      data_files=[('', ['aktvendpoint.ini'])])