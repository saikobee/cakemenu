#!/usr/bin/python2
import pygtk; pygtk.require('2.0')
import gtk
import gobject
import cairo
import pango
import pangocairo

from conf import conf

class CakeMenu(gtk.DrawingArea):
    __gsignals__ = {"expose-event": "override"}


    def __init__(self):
        gtk.DrawingArea.__init__(self)

        self.cr = None
        self.pc = None
        self.w  = 0
        self.h  = 0

        self.input = ""

    def do_expose_event(self, event):
        self.cr = self.window.cairo_create()
        self.pc = pangocairo.CairoContext(self.cr)

        a = event.area
        self.cr.rectangle(
            a.x,
            a.y,
            a.width,
            a.height
        )
        self.cr.clip()

        self.w, self.h = self.window.get_size()
        self.draw()

    def draw(self):
        w  = self.w
        h  = self.h
        cr = self.cr
        pc = self.pc

        # Draw background
        cr.set_source_rgb(*conf.bg_norm)
        cr.rectangle(0, 0, w, h)
        cr.fill()

        # Draw dividing lines
        cr.set_source_rgb(*conf.hl)
        for y in xrange(conf.size, h, conf.size):
            #cr.move_to(0,     y)
            #cr.line_to(w - 1, y)
            #cr.stroke()
            cr.rectangle(
                0, y,
                w, 1
            )
            cr.fill()

        # Draw fake selected item
        cr.set_source_rgb(*conf.bg_sel)
        cr.rectangle(
            0, 4 * conf.size + 1,
            w,     conf.size - 1
        )
        cr.fill()

    def on_key_press(self, widget, event):
        # Printing ASCII range
        k = event.keyval
        if 32 <= k <= 126:
            self.input += event.string
        elif k == gtk.keysyms.Escape:
            self.input = ""
            self.finish()
        elif k == gtk.keysyms.Return:
            self.finish()
        elif k == gtk.keysyms.BackSpace:
            self.input = self.input[0:-1]

    def finish(self):
        if self.input != "":
            print self.input
        gtk.main_quit()

    def on_delete(self, widget, event):
        self.finish()

# GTK mumbo-jumbo to show the widget in a window and quit when it's closed
def main():
    window = gtk.Window()
    widget = CakeMenu()
    window.connect("delete_event",    widget.on_delete)
    window.connect("key_press_event", widget.on_key_press)
    widget.show()
    window.add(widget)
    window.present()
    window.fullscreen()
    gtk.main()

if __name__ == "__main__":
    main()
