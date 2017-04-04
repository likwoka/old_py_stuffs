from distutils.core import setup
import py2exe

setup(name='sumsales',
      version='0.1',
      description='',
      author='Alex Li',
      author_email='ali@silverpeaksoftware.com',
      url = 'http://go-a.dyndns.org',
      windows = ['sumsales/sumsalesw.py'],
      console = ['sumsales/sumsalesc.py'],
      data_files=[('', ['sumsales/sumsales.ini'])],
      options = {'py2exe': {"compressed": 1, "optimize": 2}},
      
      # This is the Microsoft Excel 9.0 Object Library (EXCEL9.OLB).
      #options = {'py2exe': {'typelibs': [('{00020813-0000-0000-C000-000000000046}',0,1,3)]}},
      )