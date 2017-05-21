#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# main.py
# Copyright (C) 2017 Collin Norwood <cnorwood7641@stu.neisd.net>


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from subprocess import call
import os
os.system("rm out.sh")
os.system("echo 'echo installing' > out.sh")
class installer(gtk.Window):

	def __init__(self):
		gtk.Window.__init__(self, title="Arch installer")
		self.set_border_width(10)
		box = gtk.Box(orientation=gtk.Orientation.VERTICAL)
		self.add(box)
		mainbook = gtk.Notebook()
		box.pack_start(mainbook, True, True, padding=0)
		
		
		buttonbox = gtk.Box()
		box.pack_end(buttonbox, False, False, padding=5)
		
		button = gtk.Button.new_with_label("Exit")
		button.connect("clicked", self.quitbutton)
		buttonbox.pack_start(button, False, False, padding=5)

		button = gtk.Button.new_with_label("Next")
		button.connect("clicked", self.nextbutton)
		buttonbox.pack_end(button, False, False, padding=5)

		button = gtk.Button.new_with_label("Back")
		button.connect("clicked", self.backbutton)
		buttonbox.pack_end(button, False, False, padding=5)
		button.set_sensitive(False)



		#Page 1
		page1 = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=6)
		welcomelabel = gtk.Label("Welcome to this unnamed thingy. Hopefully this will let you install arch linux at some point. As you chose options and click next on each page it will basically make a script based on what options you selected.")
		page1.add(welcomelabel)

		#Page 2
		page2 = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=6)
		welcomelabel = gtk.Label("hello again")
		page2.add(welcomelabel)
		

		#Tabs
		tab1label = gtk.Label("tab1")
		tab2label = gtk.Label("tab2")
		tab3label = gtk.Label("tab3")
		tab4label = gtk.Label("tab4")
		tab5label = gtk.Label("tab5")
		mainbook.append_page(page1, tab1label)
		mainbook.append_page(page2, tab2label)


	def nextbutton(self, button):
		print("running")
		os.system("gnome-terminal -x sh -c 'bash out.sh; exec bash'")

	def backbutton(self, button):
 		print("back")
		
	def quitbutton(self, button):
		gtk.main_quit()

win = installer()
gtk.Window.resize(win,800,800)
win.connect("delete-event", gtk.main_quit)
win.show_all()
gtk.main()
