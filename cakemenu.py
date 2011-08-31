#!/usr/bin/python2
import pygtk; pygtk.require('2.0')
import pangocairo
import gobject
import cairo
import pango
import gtk

import sys

from conf import conf

class CakeMenu(gtk.DrawingArea):
    __gsignals__ = {"expose-event": "override"}

    def __init__(self):
        gtk.DrawingArea.__init__(self)

        self.layout = None
        self.cr = None
        self.pc = None
        self.px = None
        self.w  = 0
        self.h  = 0

        self.size = 0
        self.pad  = 0

        self.input         = ""
        self.selected_num  = 0
        self.all_choices   = sys.stdin.readlines()
        self.all_choices   = map(lambda s: s.rstrip("\n"), self.all_choices)
        self.all_choices   = list(set(self.all_choices))
        self.choices       = self.all_choices
        self.choices_limit = 999

        conf.bg_sel = self.hex_to_color(conf.bg_sel)
        conf.fg_sel = self.hex_to_color(conf.fg_sel)

        conf.bg_norm = self.hex_to_color(conf.bg_norm)
        conf.fg_norm = self.hex_to_color(conf.fg_norm)

    def hex_to_color(self, hex_str):
        hex_str = hex_str.lstrip("#")
        r = hex_str[0:2]
        g = hex_str[2:4]
        b = hex_str[4:6]
        r = int(r, 16)
        g = int(g, 16)
        b = int(b, 16)
        r /= 255.0
        g /= 255.0
        b /= 255.0

        return (r, g, b)

    def do_expose_event(self, event):
        self.cr = self.window.cairo_create()
        self.pc = pangocairo.CairoContext(self.cr)
        self.px = self.get_pango_context()

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

        desc = pango.FontDescription(conf.font)
        self.layout = self.pc.create_layout()
        self.layout.set_font_description(desc)
        metrics = self.px.get_metrics(desc)
        ascent  = metrics.get_ascent()
        descent = metrics.get_descent()
        self.text_size_px = pango.PIXELS(ascent + descent)
        self.size = self.text_size_px + self.pad + self.pad
        self.pad  = pango.PIXELS(descent)
        self.choices_limit = (h / self.size) - 1

        self.draw_bg()
        self.draw_text()
        self.draw_sel()
        self.draw_sel_text()
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

        self.cr.translate(0, (1 + self.selected_num) * self.size)
        self.cr.set_source_rgb(*conf.bg_sel)
        self.cr.rectangle(
            0, 0,
            w, self.size,
        )
        self.cr.fill()
        self.cr.translate(0, -(1 + self.selected_num) * self.size)

    def draw_text(self):
        w = self.w
        h = self.h

        self.cr.set_source_rgb(*conf.fg_norm)
        for choice, y in zip(self.choices, xrange(self.size, h, self.size)):
            self.cr.translate(self.pad, self.pad + y)
            self.layout.set_text(choice)
            self.pc.update_layout(self.layout)
            self.pc.show_layout(self.layout)
            self.cr.translate(-self.pad, -(self.pad + y))

    def draw_sel_text(self):
        if self.selected_num < 0:
            return

        w = self.w
        h = self.h

        self.cr.set_source_rgb(*conf.fg_sel)
        choice = self.choices[self.selected_num]
        y      = self.size + self.selected_num * self.size
        self.cr.translate(self.pad, self.pad + y)
        self.layout.set_text(choice)
        self.pc.update_layout(self.layout)
        self.pc.show_layout(self.layout)
        self.cr.translate(-self.pad, -(self.pad + y))

    def draw_input(self):
        w = self.w
        h = self.h

        self.cr.translate(self.pad, self.pad)
        if self.selected_num < 0:
            self.cr.set_source_rgb(*conf.fg_sel)
        else:
            self.cr.set_source_rgb(*conf.fg_norm)
        self.layout.set_text(self.input)
        self.pc.update_layout(self.layout)
        self.pc.show_layout(self.layout)
        self.cr.translate(-self.pad, -self.pad)

    def search(self):
        self.choices = filter(
            lambda choice: self.input in choice,
            self.all_choices
        )
        self.choices = self.choices[:self.choices_limit]
        self.selected_num = 0
        if self.choices == []:
            self.selected_num = -1

    def on_key_press(self, widget, event):
        k = event.keyval
        # Printing ASCII range
        if 32 <= k <= 126:
            if not event.state & gtk.gdk.CONTROL_MASK:
                self.input += event.string
                self.search()
        elif k == gtk.keysyms.Escape:
            self.input = ""
            self.finish()
        elif k == gtk.keysyms.Return:
            self.finish()
        elif k == gtk.keysyms.BackSpace:
            self.input = self.input[0:-1]
            self.search()
        elif k == gtk.keysyms.Tab or k == gtk.keysyms.ISO_Left_Tab:
            if event.state & gtk.gdk.SHIFT_MASK:
                self.selected_num -= 1
            else:
                self.selected_num += 1

            self.input = self.choices[self.selected_num]

        self.queue_draw()

    def finish(self):
        if self.input != "":
            if self.selected_num == -1:
                print self.input
            else:
                print self.choices[self.selected_num]
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
