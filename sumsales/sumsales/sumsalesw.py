'''
A GUI.
'''

import wx
import wx.wizard as wiz
import os, sys
from sumsales import core


#---------------------------------------------------------------------------
class TitledPage(wiz.PyWizardPage):

    def __init__(self, parent, title):
        wiz.PyWizardPage.__init__(self, parent)
        self.parent = parent
        self.prev = None
        self.next = None
        self._setTitle(title)


    def _setTitle(self, title):
        t = wx.StaticText(self, -1, title)
        t.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.AddWindow(t, 0, wx.ALIGN_LEFT|wx.ALL, 5)
        self.sizer.AddWindow(wx.StaticLine(self, -1),
                             0, wx.EXPAND|wx.ALL, 5)

        self.SetSizer(self.sizer)


    def SetPrev(self, prev):
        self.prev = prev


    def SetNext(self, next):
        self.next = next


    def GetPrev(self):
        return self.prev


    def GetNext(self):
        return self.next


#--------------------------------------------------------------------------- 
class ChooseFolderPage(TitledPage):
    "Step 1 of 3: Choose a folder."
    
    def __init__(self, parent):
        TitledPage.__init__(self, parent, self.__doc__)
        
        # A textbox to show the result from the directory dialog,
        # or the user can type in the path directly.
        self.textctl = wx.TextCtrl(self, -1,
                                   value='',
                                   size=(300, -1))

        # Add a "Browse" button which pops up the directory dialog
        id = wx.NewId()
        self.button = wx.Button(self, id, "Browse...")
        wx.EVT_BUTTON(self, id, self.onClick)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(wx.StaticText(self, -1, "Folder: "), 0,
                   wx.ALIGN_CENTER|wx.ALIGN_LEFT|wx.ALL, 3)
        hsizer.Add(self.textctl, 0, wx.ALIGN_RIGHT|wx.ALL, 3)

        self.sizer.Add(hsizer)
        self.sizer.Add(self.button, 0, wx.ALIGN_RIGHT|wx.ALL, 3)


    def _read_inifile(self, inifile):
        '''
        Return the initial path info from the ini file.
        The ini file is python code.
        '''
        result = {}
        try:
            execfile(inifile, result)
        except IOError:
            return None
        return result.get('path', None)


    def onClick(self, event):
        '''
        When click, pop up the directory dialog.
        '''
        path = self.parent.data.get('path', '')
        dlg = wx.DirDialog(self, "Choose a folder.", defaultPath=path)

        if dlg.ShowModal() == wx.ID_OK:
            self.textctl.SetValue(dlg.GetPath())
        dlg.Destroy()


    def _changedToThisPage(self, event):
        # Read the initial path from the ini file.
        # This allows the user to prevent starting the directory
        # dialog from the "root" everytime to run this program.
        inifile = os.path.join(os.path.abspath(''), 'sumsales.ini')
        path = self._read_inifile(inifile)
        if path is not None:
            self.parent.data['path'] = path
            self.textctl.SetValue(path)
 

    def _changingToNextPage(self, event):
        # Before moving to next page, let's get the path value
        # from the text box to see if it is valid.
        path = self.textctl.GetValue()
        if len(path.strip()) > 0:
            path = os.path.abspath(path)
             
        if not os.path.isdir(path):
            wx.MessageBox("This is not a valid folder.  "
                          "May be you made a typo?")            
            event.Veto()
            return

        # Up to now, the path is a valid path, but is it
        # the path that we want?
        try:
            month, year = core.get_month_year(path)
            self.parent.data['path'] = path            
            self.parent.data['month'] = month
            self.parent.data['year'] = year
        except ValueError:
            wx.MessageBox("Cannot infer the MONTH and YEAR from the folder "
                          "name.  If you are sure this is the folder "
                          "we want, please rename it in MMM_YY format.")
            event.Veto()



class ReadyPage(TitledPage):
    "Step 2 of 3: Ready to generate the report."
    
    def __init__(self, parent):
        TitledPage.__init__(self, parent, self.__doc__)

        self.willtext = wx.StaticText(self, -1, '')
        text = 'Click Next to create the report.  This may take a while.' 

        self.sizer.Add(self.willtext, 0, wx.ALIGN_LEFT|wx.ALL, 5)
        self.sizer.Add(wx.StaticText(self, -1, text), 0,
                       wx.ALIGN_LEFT|wx.ALL, 5)


    def _changedToThisPage(self, event):
        month = self.parent.data.get('month')
        year = self.parent.data.get('year')
        self.willtext.SetLabel('Will create the %s 20%s '
                               'Monthly Sales Report now.' % (month, year))

                               
    def _changingToNextPage(self, event):
        # Capture the stdout log.
        self.parent.logname = os.path.join(os.path.abspath(''), 'log.tmp')
        sys.stdout = sys.stderr = file(self.parent.logname, 'w')

        try:
            # Do the summarization work.
            core.sum(self.parent.data['path'])
            self.parent.data['isOk'] = True
        except:
            self.parent.data['isOk'] = False

        sys.stdout.close()

          

class FeedbackPage(TitledPage):
    "Step 3 of 3: Verify the report."

    def __init__(self, parent):
        TitledPage.__init__(self, parent, self.__doc__)

        self.resulttext = wx.StaticText(self, -1, '')
        self.sizer.Add(self.resulttext, 0, wx.ALIGN_LEFT|wx.ALL, 5)
        self.sizer.Add(wx.StaticText(self, -1, ''), 0,
                       wx.ALIGN_LEFT|wx.ALL, 5)

        self.sizer.Add(wx.StaticText(self, -1,
                       'Action Log:'), 0, wx.ALIGN_LEFT|wx.ALL, 5)

        self.log = wx.TextCtrl(self, -1, value='', size=(320, 220),
                style=wx.TE_MULTILINE|wx.TE_DONTWRAP|wx.TE_READONLY)
        self.sizer.Add(self.log, 0, wx.ALIGN_LEFT|wx.ALL, 5)

        
    def _changedToThisPage(self, event):
        # Display the detailed log messages.
        self.log.SetValue(file(self.parent.logname, 'r').read())
        # We remove the log file after every run, so that
        # it won't be mixed up with the next run.
        os.remove(self.parent.logname)

        # Also display a one-line summary.
        if self.parent.data['isOk']:
            month = self.parent.data.get('month')
            year = self.parent.data.get('year')
            result = 'The %s 20%s Monthly Sales Report ' \
                     'is created successfully :)' % (month, year)
        else:
            result = 'Somethings wrong happened.  You may have to run ' \
                     'the program again.'
            
        self.resulttext.SetLabel(result)


#---------------------------------------------------------------------------
def onPageChanging(event):

    if event.GetDirection():
        # True means moving forward.
        page = event.GetPage()
        try:
            page._changingToNextPage(event)
        except AttributeError:
            pass


def onPageChanged(event):

    if event.GetDirection():
        # True means moving forward.
        page = event.GetPage()
        try:
            page._changedToThisPage(event)
        except AttributeError:
            pass
    

if __name__ == '__main__':  
    app = wx.PySimpleApp()

    id = wx.NewId()
    wizard = wiz.Wizard(None, id, "Summarize Sales For A Month")
    wizard.data = {}
    
    page1 = ChooseFolderPage(wizard)
    page2 = ReadyPage(wizard)
    page3 = FeedbackPage(wizard)

    page1.SetNext(page2)
    page2.SetPrev(page1)
    page2.SetNext(page3)
    
    wiz.EVT_WIZARD_PAGE_CHANGING(app, id, onPageChanging)
    wiz.EVT_WIZARD_PAGE_CHANGED(app, id, onPageChanged)

    wizard.FitToPage(page1)
    wizard.RunWizard(page1)
    wizard.Destroy()

    app.MainLoop()
