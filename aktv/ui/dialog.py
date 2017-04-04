import wx
import wx.html
import wx.lib.wxpTag


class AboutBox(wx.Dialog):
    text = '''
    <html>
    <body bgcolor="#ffffff">
    <table border="0">
    <tr><td colspan="3" align="center"><h4>%s</h4></td></tr>
    <tr><td align="right"><strong>Version:</strong></td>
        <td colspan="2" align="left">%s</td></tr>
    <tr><td align="right"><strong>Author:</strong></td>
        <td colspan="2" align="left">%s</td></tr>
    <tr><td align="right"><strong>Copyright:</strong></td>
        <td colspan="2" align="left">%s</td></tr>
    <tr><td align="right"><strong>Contact Info:</strong></td>
        <td colspan="2" align="left">%s</td></tr>
    <tr><td colspan="3">&nbsp;</td></tr>
    <tr><td colspan="3" align="center">
        <wxp module="wx" class="Button">
            <param name="label" value="OK">
            <param name="id" value="ID_OK">
        </wxp>
        </td></tr>
    </table>
    </body>
    </html>
    '''
    
    def __init__(self, parent, program_name, program_version, program_author,
                 program_copyright, program_contact):
        wx.Dialog.__init__(self, parent, -1, 'About %s' % program_name,
                           style=wx.TAB_TRAVERSAL)
        html = wx.html.HtmlWindow(self, -1, size=(420, -1))
        html.SetPage(self.text % (program_name, program_version,
                                  program_author,
                                  program_copyright, program_contact))
        btn = html.FindWindowById(wx.ID_OK)
        btn.SetDefault()
        btn.SetFocus() #this set the focus to the button when dialog pops up
        ir = html.GetInternalRepresentation()
        html.SetSize((ir.GetWidth()+25, ir.GetHeight()+25))
        self.SetClientSize(html.GetSize())
        self.CentreOnParent(wx.BOTH)
