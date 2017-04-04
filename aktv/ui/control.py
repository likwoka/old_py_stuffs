import wx
from aktv.controller import logic


class RoomWidget(wx.Panel):
    '''I represent a Room.'''
    OFF = 0
    ON = 1
    def __init__(self, parent, id, machine_name, ipaddr, port, wait):
        wx.Panel.__init__(self, parent, id,
                          style=wx.SIMPLE_BORDER|wx.TAB_TRAVERSAL)
        self.SetBackgroundColour(wx.WHITE)
        self._label = machine_name
        self._ipaddr = ipaddr
        self._port = port
        self._state = self.OFF
        self._is_shutting_down = False
        self._wait = wait
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        #Label
        self._label = RoomLabel(self, wx.NewId(), machine_name)
        sizer.Add(self._label, 1, wx.ALIGN_CENTER|wx.ALL, 3)

        #Status
        self._status = RoomStatus(self, wx.NewId())          
        sizer.Add(self._status, 0, wx.ALIGN_CENTER|wx.ALL, 3)
   
        #Control
        control_id = wx.NewId()
        self._control = RoomControl(self, control_id)
        wx.EVT_BUTTON(self, control_id, self.on_click)
        sizer.Add(self._control, 0, wx.ALIGN_CENTER|wx.ALL, 3)

        self.SetSizerAndFit(sizer)
        self.Layout()
        self.SetAutoLayout(True)

    def on_click(self, event):
        '''On click event handling.

        This is only valid when the state is ON.  When the state is OFF,
        the control is DISABLED and therefore won't get any on click event.
        '''
        if self._state == self.ON and self._is_shutting_down == False:
            self._control.shutdown(self._ipaddr, self._port, self._wait)
            self._is_shutting_down = True
            self._status.shutting_down()
        elif self._state == self.ON and self._is_shutting_down == True:
            self._control.cancel_shutdown(self._ipaddr, self._port)
            self._is_shutting_down = False
            self._status.on()

    def set_state(self, state):
        '''Changes state.  Should be called by a GUI update thread.

        The other 2 cases: ON and ON, OFF and OFF, won't change anything,
        and therefore are ignored.'''
        if self._state == self.ON and state == self.OFF:
            self._status.off()
            self._control.disable()
        elif self._state == self.OFF and state == self.ON:
            self._status.on()
            self._control.enable()
        self._state = state


class RoomLabel(wx.StaticText):
    '''I display the Room identifier (ie, name).'''
    def __init__(self, parent, id, text):
        wx.StaticText.__init__(self, parent, id, text, size=(-1,22),
                               style=wx.ALIGN_CENTER|wx.ST_NO_AUTORESIZE
                               |wx.TAB_TRAVERSAL)
        self.SetFont(wx.Font(13,
                             family=wx.SWISS,
                             style=wx.NORMAL,
                             weight=wx.BOLD,
                             encoding=wx.FONTENCODING_SYSTEM))
        self.SetSize(self.GetBestSize())


class RoomStatus(wx.StaticText):
    '''I display the Room Status: ON or OFF.'''
    def __init__(self, parent, id):
        wx.StaticText.__init__(self, parent, id, label='', size=(130,22),
                               style=wx.ALIGN_CENTER|wx.ST_NO_AUTORESIZE|
                               wx.SIMPLE_BORDER|wx.TAB_TRAVERSAL)
        self.SetFont(wx.Font(12,
                             family=wx.SWISS,
                             style=wx.NORMAL,
                             weight=wx.BOLD,
                             encoding=wx.FONTENCODING_SYSTEM))
        self.off()

    def on(self):
        self.SetLabel('Occupied')
        self.SetBackgroundColour(wx.Colour(0,255,0))
        self.SetForegroundColour(wx.Colour(0,0,0))
        self.Refresh(True)

    def off(self):
        self.SetLabel('Off')
        self.SetBackgroundColour(wx.Colour(255,0,0))
        self.SetForegroundColour(wx.Colour(0,0,0))
        self.Refresh(True)

    def shutting_down(self):
        self.SetLabel('Shutting Down...')
        self.SetBackgroundColour(wx.Colour(255,255,0))
        self.SetForegroundColour(wx.Colour(0,0,0))        
        self.Refresh(True)
        
class RoomControl(wx.Button):
    '''I am the control.'''
    def __init__(self, parent, id):
        wx.Button.__init__(self, parent, id, label='', size=(110,22),
                           style=wx.SIMPLE_BORDER|wx.TAB_TRAVERSAL)
        self.disable()

    def shutdown(self, ipaddr, port, min):
        self.SetTitle('Cancel Shutdown')
        # XXX should be shutdown_machine, not shutdown_server_program
        logic('dummy', [ipaddr, port, 'shutdown_machine', min])
        
    def cancel_shutdown(self, ipaddr, port):
        self.SetTitle('Shutdown')
        logic('dummy', [ipaddr, port, 'cancel'])

    def disable(self):
        self.SetTitle('Shutdown')
        self.Enable(False)

    def enable(self):
        self.SetTitle('Shutdown')
        self.Enable(True)
    