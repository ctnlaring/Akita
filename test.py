import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
gi.require_version('Vte', '2.91')
from gi.repository import Vte, GLib
import os 

class test(gtk.Window):

	def __init__(self):
		gtk.Window.__init__(self, title="test")
		box = gtk.Box(orientation=gtk.Orientation.VERTICAL)
		self.add(box)
		testlabel = gtk.Label()
		testlabel.set_markup("There should be an embedded terminal here\n\n")
		box.pack_start(testlabel, True, True, padding=0)
		terminal = Vte.Terminal()
		terminal.spawn_sync(Vte.PtyFlags.DEFAULT, os.environ['HOME'], ["/bin/bash"], [], GLib.SpawnFlags.DO_NOT_REAP_CHILD, None, None)
		command="hi"
		terminal.feed_child(command, len(command))
		box.pack_start(terminal, True, True, padding=0)
		
win = test()
gtk.Window.resize(win,800,500)
win.connect("delete-event", gtk.main_quit)
win.show_all()
gtk.main()
