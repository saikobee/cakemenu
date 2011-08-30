#!/usr/bin/python2
import pygtk; pygtk.require('2.0')
import pangocairo
import gobject
import cairo
import pango
import gtk

import random
import string

from conf import conf

class CakeMenu(gtk.DrawingArea):
    __gsignals__ = {"expose-event": "override"}


    def __init__(self):
        gtk.DrawingArea.__init__(self)

        self.layout = None
        self.cr = None
        self.pc = None
        self.w  = 0
        self.h  = 0

        self.input = ""
        self.selected_num = 1

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

    def random_string(self):
        times = xrange(random.randrange(4, 30))
        src   = string.ascii_letters
        ret   = [random.choice(src) for x in times]
        return "".join(ret)

    def draw(self):
        w  = self.w
        h  = self.h

        random.seed(0xdeadbeef)

        desc = pango.FontDescription(conf.font)
        self.layout = self.pc.create_layout()
        self.layout.set_font_description(desc)

        self.draw_bg()
        self.draw_sel()
        self.draw_text()
        self.draw_input()

    def draw_bg(self):
        w  = self.w
        h  = self.h

        self.cr.set_source_rgb(*conf.bg_norm)
        self.cr.rectangle(0, 0, w, h)
        self.cr.fill()

    def draw_sel(self):
        w  = self.w
        h  = self.h

        self.cr.translate(0, self.selected_num * conf.size)
        self.cr.set_source_rgb(*conf.bg_sel)
        self.cr.rectangle(
            0, 0,
            w, conf.size,
        )
        self.cr.fill()
        self.cr.translate(0, -self.selected_num * conf.size)

    def draw_text(self):
        w = self.w
        h = self.h

        self.cr.set_source_rgb(*conf.fg_norm)
        for y in xrange(conf.size, h, conf.size):
            self.cr.translate(conf.pad, conf.pad + y)
            self.layout.set_text(self.random_string())
            self.pc.update_layout(self.layout)
            self.pc.show_layout(self.layout)
            self.cr.translate(-conf.pad, -(conf.pad + y))

    def draw_input(self):
        w = self.w
        h = self.h

        self.cr.translate(conf.pad, conf.pad)
        self.cr.set_source_rgb(*conf.fg_norm)
        self.layout.set_text(self.input)
        self.pc.update_layout(self.layout)
        self.pc.show_layout(self.layout)
        self.cr.translate(-conf.pad, -conf.pad)

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
