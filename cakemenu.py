#!/usr/bin/python2
import pygtk; pygtk.require('2.0')
import gtk
import gobject
import cairo
import pango
import pangocairo

import random
import string

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
        self.selected_num = 1

    def do_expose_event(self, event):
        self.cr = self.window.cairo_create()
        self.pc = pangocairo.CairoContext(self.cr)

        #a = event.area
        #self.cr.rectangle(
        #    a.x,
        #    a.y,
        #    a.width,
        #    a.height
        #)
        #self.cr.clip()

        self.w, self.h = self.window.get_size()
        self.draw()

    def random_string(self):
        times = xrange(random.randrange(4, 30))
        src   = string.ascii_letters
        ret   = [random.choice(src) for x in times]
        return "".join(ret)

    def draw(self):
        w  = self.w
        h  = self.h
        cr = self.cr
        pc = self.pc

        random.seed(0xdeadbeef)

        desc   = pango.FontDescription(conf.font)
        layout = pc.create_layout()
        layout.set_font_description(desc)

        # Draw background
        cr.set_source_rgb(*conf.bg_norm)
        cr.rectangle(0, 0, w, h)
        cr.fill()

        # Draw fake selected item
        cr.translate(0, self.selected_num * conf.size)
        cr.set_source_rgb(*conf.bg_sel)
        cr.rectangle(
            0, 0,
            w, conf.size,
        )
        cr.fill()
        cr.translate(0, -self.selected_num * conf.size)

        # Draw the text
        cr.set_source_rgb(*conf.fg_norm)
        for y in xrange(conf.size, h, conf.size):
            cr.translate(conf.pad, conf.pad + y)
            layout.set_text(self.random_string())
            pc.update_layout(layout)
            pc.show_layout(layout)
            cr.translate(-conf.pad, -(conf.pad + y))

        # Draw current input
        cr.translate(conf.pad, conf.pad)
        cr.set_source_rgb(*conf.fg_norm)
        layout.set_text(self.input)
        pc.update_layout(layout)
        pc.show_layout(layout)
        cr.translate(-conf.pad, -conf.pad)

    def on_key_press(self, widget, event):
        k = event.keyval
        # Printing ASCII range
        if 32 <= k <= 126:
            if not event.state & gtk.gdk.CONTROL_MASK:
                self.input += event.string
        elif k == gtk.keysyms.Escape:
            self.input = ""
            self.finish()
        elif k == gtk.keysyms.Return:
            self.finish()
        elif k == gtk.keysyms.BackSpace:
            self.input = self.input[0:-1]
        elif k == gtk.keysyms.Tab or k == gtk.keysyms.ISO_Left_Tab:
            if event.state & gtk.gdk.SHIFT_MASK:
                self.selected_num -= 1
            else:
                self.selected_num += 1

        self.queue_draw()

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
