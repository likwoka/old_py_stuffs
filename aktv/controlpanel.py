'''
Control Panel for aktvcontroller.py
1,2) Read data file (contains room_name:ip pair)
3) ping each of the ip to see if they are on/off (occupied/not-occupied)
4) link the logic to the gui

1 App contains 1 Frame contains 1 splitterWindow contains 2 panels...
1 panel contains all rooms, another 1 contains the action result.
'''

__AUTHOR__ = 'Alex Li <likwoka@yahoo.com>'
__COPYRIGHT__ = 'Copyright (c) Alex Li 2003.'
__VERSION__ = '0.1'
__NAME__ = 'AKTV Control Panel'
__CONTACT__ = 'Polygon Production 416-754-0880'

import wx
import os, sys, thread
from aktv import configurator, heartbeat
from aktv import image
from aktv.ui import dialog, panel

        
class MyFrame(wx.Frame):
    '''I am the main Frame.'''  
    def __init__(self, config_param):
        wx.Frame.__init__(self, parent=None, id=-1,
                          title=__NAME__,
                          pos=wx.DefaultPosition,
                          style=wx.DEFAULT_FRAME_STYLE|
                          wx.NO_FULL_REPAINT_ON_RESIZE)
        self._c = config_param
        self.CreateStatusBar(1, wx.ST_SIZEGRIP)
        self.create_menubar()
        self.create_panels()
        self.set_sane_size()
        wx.InitAllImageHandlers()
        self.SetIcon(image.getIcon())
        self.Show(True)

    def create_menubar(self):
        self._main_menu = wx.MenuBar()
        # Make a File menu
        exitId = wx.NewId()
        menu = wx.Menu()
        menu.Append(exitId, 'E&xit\tAlt-F4', 'Exits the program.')
        wx.EVT_MENU(self, exitId, self.on_file_exit)
        wx.App_SetMacExitMenuItemId(exitId)
        self._main_menu.Append(menu, '&File')
        # Make a Help menu
        helpId = wx.NewId()
        menu = wx.Menu()
        menu.Append(helpId, '&About %s' % __NAME__,
                    'Displays program information, version number, '
                    'and copyright.')
        wx.App_SetMacAboutMenuItemId(helpId)
        wx.EVT_MENU(self, helpId, self.on_help_about)
        self._main_menu.Append(menu, '&Help')
        # Add this menu bar to self 
        self.SetMenuBar(self._main_menu)        

    def create_panels(self):
        self._main_panel = panel.MainPanel(self, -1, self._c)

    def set_sane_size(self):
        screen = wx.ScreenDC().GetSize()
        this = self._main_panel.GetBestSize()
        # 10 is approx. width of vert. scrollbar,
        # 85 is approx. height of titlebar, menubar, statusbar combined.
        sane = wx.Size(this.GetX()+10, this.GetY()+85) 
        if sane.GetY() < screen.GetY()-60:  # 60 is approx. height of taskbar
            self.SetSize(sane)
        else:
            self.SetSize((sane.GetX(), screen.GetY()-60))
            
##    def createSplitteredPanels(self):
##        '''XXX Not used.  create_panels() is used instead.'''
##        splitter = wx.SplitterWindow(self, -1)
##        self._clp = MainPanel(splitter, -1, self._c['endpoints'])
##        self._log = ResultPanel(splitter, -1)
##        wx.Log_SetActiveTarget(wx.LogTextCtrl(self._log))
##        splitter.SetMinimumPaneSize(20)
##        splitter.SplitHorizontally(self._clp, self._log, 350)

    def on_file_exit(self, event):
        self.Close()

    def on_help_about(self, event):
        about = dialog.AboutBox(self, __NAME__, __VERSION__,
                                __AUTHOR__, __COPYRIGHT__,
                                __CONTACT__)
        about.ShowModal()
        about.Destroy()
        

class MyApp(wx.App):
    def OnInit(self):
        c = configurator.get_param(os.path.join(sys.path[0], 'aktvcp.ini'))

        self.frame = MyFrame(c)
        self.frame.Show()
        self.SetTopWindow(self.frame)
        self.SetExitOnFrameDelete(True)
        return True

    def OnExit(self):
        #remember to clean up all resource first
        #(like close log file object, save config file...etc)
        os._exit(0)

if __name__ == '__main__':
    app = MyApp(0)
    app.MainLoop()


