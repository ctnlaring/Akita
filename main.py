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
		global mainbook
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



		#Page 1
		page1 = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=6)
		welcomelabel = gtk.Label("Welcome to this unnamed thingy. Hopefully this will let you install arch linux at some point.\nAs you chose options and click next on each page it will make a script based on what options you selected.")
		page1.add(welcomelabel)
		testcheck = gtk.CheckButton("Install Firefox?")
		page1.add(testcheck)
		radio1 = gtk.RadioButton("radio1")
		radio2 = gtk.RadioButton(group=radio1, label="radio2")
		page1.add(radio1)
		page1.add(radio2)

		#Page 2
		page2 = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=6)
		welcomelabel = gtk.Label("hello again")
		page2.add(welcomelabel)
		
		#Page 3
		page3 = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=6)
		if testcheck.get_active() == True:
			print("fire")
		welcomelabel = gtk.Label("I'm now going to attempt to generate an install script based on the options you selected.\nYou Should review it very, very carefully. It will almost certainly destroy your machine otherwise.")
		page3.add(welcomelabel)
		gobutton = gtk.Button("GO!")
		page3.pack_end(gobutton, False, False, padding=5)

		#Tabs
		tab1label = gtk.Label("tab1")
		tab2label = gtk.Label("tab2")
		tab3label = gtk.Label("Fin")
		tab4label = gtk.Label("tab4")
		tab5label = gtk.Label("tab5")
		mainbook.append_page(page1, tab1label)
		mainbook.append_page(page2, tab2label)
		mainbook.append_page(page3, tab3label)


	def nextbutton(self, button):
		#os.system("gnome-terminal -x sh -c 'bash out.sh; exec bash'")
		mainbook.next_page()


	def backbutton(self, button):
		mainbook.prev_page()
		
	def quitbutton(self, button):
		gtk.main_quit()

win = installer()
gtk.Window.resize(win,800,500)
win.connect("delete-event", gtk.main_quit)
win.show_all()
gtk.main()
