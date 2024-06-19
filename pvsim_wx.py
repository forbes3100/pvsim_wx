# PVSim wxPython draw test -- image based, with non-scrolling headers

import os
import wx

class PVSimWindow(wx.Frame):
    def __init__(self, parent, title):
        super(PVSimWindow, self).__init__(parent, title=title, size=(800, 600))

        self.scrolled_window = wx.ScrolledWindow(self, style=wx.HSCROLL | wx.VSCROLL)
        self.ds = 14  # scroll by row-height increments
        self.scrolled_window.SetScrollRate(self.ds, self.ds)

        # Load images
        self.top_image = wx.Image("test_timing_times.png", wx.BITMAP_TYPE_PNG)
        self.left_image = wx.Image("test_timing_names.png", wx.BITMAP_TYPE_PNG)
        self.main_image = wx.Image("test_timing.png", wx.BITMAP_TYPE_PNG)

        # Scale images to half size
        top_width = self.top_image.GetWidth() // 2
        self.top_height = self.top_image.GetHeight() // 2
        self.left_width = self.left_image.GetWidth() // 2
        left_height = self.left_image.GetHeight() // 2
        main_width = self.main_image.GetWidth() // 2
        main_height = self.main_image.GetHeight() // 2
        self.top_image = self.top_image.Scale(top_width, self.top_height).ConvertToBitmap()
        self.left_image = self.left_image.Scale(self.left_width, left_height).ConvertToBitmap()
        self.main_image = self.main_image.Scale(main_width, main_height).ConvertToBitmap()

        # Bind events
        self.scrolled_window.Bind(wx.EVT_PAINT, self.OnPaint)
        self.scrolled_window.Bind(wx.EVT_SCROLLWIN, self.OnScroll)

        # Set virtual size based on scaled images
        v_size = (main_width + self.left_width, main_height + self.top_height)
        self.scrolled_window.SetVirtualSize(v_size)

        self.Show()

    def OnPaint(self, event):
        dc = wx.PaintDC(self.scrolled_window)
        self.scrolled_window.PrepareDC(dc)

        # Get the current scroll positions
        x_scroll, y_scroll = self.scrolled_window.GetViewStart()
        top = self.top_height + y_scroll * self.ds
        left = self.left_width + x_scroll * self.ds
        right, bottom = self.scrolled_window.GetVirtualSize()

        # Blank rectangle in upper right where cursor time will be drawn
        dc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))
        dc.SetPen(wx.Pen(wx.Colour(255, 255, 255)))
        dc.DrawRectangle(0, 0, left, top)

        # Draw the top image, undoing any y scrolling
        # Clip each area to prevent overlap with other images
        dc.SetClippingRegion(left, 0, right, top)
        dc.DrawBitmap(self.top_image, self.left_width, y_scroll * self.ds, True)
        dc.DestroyClippingRegion()

        # Draw the left image, undoing any x scrolling
        dc.SetClippingRegion(0, top, left, bottom)
        dc.DrawBitmap(self.left_image, x_scroll * self.ds, self.top_height, True)
        dc.DestroyClippingRegion()

        # Draw the main image, normal scrolling
        dc.SetClippingRegion(left, top, right, bottom)
        dc.DrawBitmap(self.main_image, self.left_width, self.top_height, True)
        dc.DestroyClippingRegion()

    def OnScroll(self, event):
        self.scrolled_window.Refresh()
        event.Skip()

if __name__ == "__main__":
    app = wx.App(False)
    frame = PVSimWindow(None, "PVSim_wx.app")
    app.MainLoop()
    os._exit(0)    # to keep wx from seg-faulting with Python 3.12
