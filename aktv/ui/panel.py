import wx
from wxPython.lib.scrolledpanel import wxScrolledPanel
import threading, time

from aktv import heartbeat
from aktv.ui import control


class MainPanel(wxScrolledPanel):
    '''I am the main panel which contains the RoomWidgets.  I hold
    2 other threads, a recorder thread for recording heartbeat sent by
    the client, and a gui update thread for updating the RoomWidgets
    according to the heartbeat.
    '''
    def __init__(self, parent, id, c):
        wxScrolledPanel.__init__(self, parent, id, style=wx.TAB_TRAVERSAL)
        self.SetBackgroundColour(wx.WHITE)
        self._widgets = {}
        self._heartbeats = heartbeat.HeartBeatDict()
        sizer = wx.BoxSizer(wx.VERTICAL)
       
        for endpoint in c['endpoints']:
            roomwidget = control.RoomWidget(self, -1,
                                            endpoint[1],
                                            endpoint[0],
                                            c['endpoint_port'],
                                            c['wait'])
            sizer.Add(roomwidget, 0, wx.ALIGN_RIGHT|wx.ALL, 3)            
            self._widgets[endpoint[0]] = roomwidget
            self._heartbeats[endpoint[0]] = 0 #initialize last_access_time to
                                              #long time ago
       
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        #self.SetScrollRate(5, 5) for wx.ScrolledWindow
        self.SetupScrolling(rate_x=5, rate_y=5)
        self.SetSize(self.GetBestSize())
        
        self._recorder_thread = heartbeat.Recorder(self._heartbeats.update,
                                                   c['hb_listening_port'])
        self._guiupdate_thread = GuiUpdate(c['inactive_time_length'],
                                           self._heartbeats,
                                           self._widgets)

        self._recorder_thread.start()
        self._guiupdate_thread.start()
        

class GuiUpdate(threading.Thread):
    '''I check the whole BeatDict to see if any client
    hasn't been updated in a certain time period (because
    it hasn't sent a heart beat to the listener).
    '''
    def __init__(self, inactive_period, heartbeats, widgets):
        threading.Thread.__init__(self)
        self._inactive_period = inactive_period
        self._heartbeats = heartbeats
        self._widgets = widgets

    def run(self):
        while self._go:
            when = time.time() - self._inactive_period
            pairs = self._heartbeats.iteritems()
            self.update_widgets(when, pairs)
            time.sleep(self._inactive_period)

    def update_widgets(self, when, pairs):
        #pair[0] is ipaddr, pair[1] is last_access_time
        for pair in pairs:
            w = self._widgets[pair[0]]
            if pair[1] < when:
                w.set_state(w.OFF)
                print '%s is off' % pair[0]
            else:
                w.set_state(w.ON)
                print '%s is on' % pair[0]
    
    def start(self):
        self._go = True
        threading.Thread.start(self)

    def stop(self):
        self._go = False


##class ResultPanel(wx.TextCtrl):
##    def __init__(self, parent, id):
##        wx.TextCtrl.__init__(self, parent, id,
##                             style=wx.TE_MULTILINE|
##                             wx.TE_READONLY|wx.HSCROLL)

        