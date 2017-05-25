#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# Akita
# Copyright (C) 2017 Collin Norwood <cnorwood7641@stu.neisd.net>

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
gi.require_version('Vte', '2.91')
from gi.repository import Vte as vte
from subprocess import call
import os
os.system("rm out.sh")
os.system("echo 'echo installing' > out.sh")
print("Welcome to Akita")
print("This terminal will show some debug output")

class installer(gtk.Window):

	def __init__(self):

		gtk.Window.__init__(self, title="Akita")
		self.set_border_width(10)
		self.set_icon_from_file("./icon.png")
		self.set_wmclass ("Akita", "Akita")
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


		welcomepage = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=6)
		welcomelabel = gtk.Label()
		welcomelabel.set_markup("<b>Welcome to Akita</b>")
		welcomepage.add(welcomelabel)
		langlabel = gtk.Label("Please choose a language for use during the installation (currently english only)")
		welcomepage.add(langlabel)
		lang = gtk.ComboBoxText()
		lang.append_text("English")
		lang.set_active(0)
		welcomepage.add(lang)
		label = gtk.Label()
		label.set_markup("<b>\n\nThis is pre-release software. It's not ready for use on systems with installations you care about.\nFor now it won't run 'out.sh' automatically. Do so manually only after you've verified it's correct\nI'm not responsible if it breaks anything\n\n</b>")
		welcomepage.add(label)
		interfaces = os.listdir("/sys/class/net")
		print("List of network cards: " + str(interfaces))
		for interface in interfaces:
			print("Checking network card:")
			print interface
			cards = open("/sys/class/net/" + interface + "/operstate", "r")
			if cards.read().strip() == "up":
				print("Found a working connection")
				label = gtk.Label()
				label.set_markup("<b>You're connected to the internet. Hooray.</b>")
				break
			if cards.read().strip() != "up":
				print ("it appears to be down")
				label = gtk.Label()
				label.set_markup("<b>You don't appear to be connected to the internet.</b>")
		welcomepage.add(label)
		cards.close()
		

		keyboardpage = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=6)
		welcomelabel = gtk.Label()
		welcomelabel.set_markup("<b>This will let you pick keyboard layouts</b>")
		keyboardpage.add(welcomelabel)

		softwarepage = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=10)
		welcomelabel = gtk.Label()
		welcomelabel.set_markup("<b>Chose some packages:</b>")
		softwarepage.add(welcomelabel)
		global packages
		packages = [];
		softwarebook = gtk.Notebook()
		softwarebook.set_tab_pos(gtk.PositionType.LEFT)
		softwarepage.pack_end(softwarebook, True, True, padding=5)
		
		page01 = gtk.Box()
		pagelabel = gtk.Label("Page 1")
		page01.add(pagelabel)
		
		page02 = gtk.Box()
		pagelabel = gtk.Label("Page 2")
		page02.add(pagelabel)
		
		page03 = gtk.Box()
		pagelabel = gtk.Label("Page 3")
		page03.add(pagelabel)
		
		page04 = gtk.Box()
		pagelabel = gtk.Label("Page 4")
		page04.add(pagelabel)
		
		page05 = gtk.Box()
		pagelabel = gtk.Label("Page 5")
		page05.add(pagelabel)
		
		page1 = gtk.Label("page1")
		page2 = gtk.Label("page2")
		page3 = gtk.Label("page3")
		page4 = gtk.Label("page4")
		page5 = gtk.Label("page5")
		softwarebook.append_page(page01, page1)
		softwarebook.append_page(page02, page2)
		softwarebook.append_page(page03, page3)
		softwarebook.append_page(page04, page4)
		softwarebook.append_page(page05, page5)

		
		'''global firefox
		firefox = gtk.CheckButton("firefox")
		softwarepage.add(firefox)
		packages.append(firefox)
		
		global gedit
		gedit = gtk.CheckButton("gedit")
		softwarepage.add(gedit)
		packages.append(gedit)
		
		global steam
		steam = gtk.CheckButton("steam")
		softwarepage.add(steam)
		packages.append(steam)
		
		global kdenlive
		kdenlive = gtk.CheckButton("kdenlive")
		softwarepage.add(kdenlive)
		packages.append(kdenlive)'''


		partitionpage = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=6)
		welcomelabel = gtk.Label()
		welcomelabel.set_markup("<b>Choose your partitions:</b>")
		partitionpage.add(welcomelabel)
		partbox = gtk.Box()
		partitionpage.pack_end(partbox, True, True, padding=5)
		drivebox = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=6)
		schemebox = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=6)
		partbox.add(drivebox)
		partbox.add(schemebox)
		
		global drive1
		drive1 = gtk.RadioButton("/dev/sda")
		drivebox.add(drive1)
		
		global drive2
		drive2 = gtk.RadioButton(group=drive1, label="/dev/sdb")
		drivebox.add(drive2)
		
		global ext3
		ext3 = gtk.RadioButton("ext3")
		schemebox.add(ext3)
		
		global ext4
		ext4 = gtk.RadioButton(group=ext3, label="ext4")
		schemebox.add(ext4)
		
		
		timezonepage = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=6)
		welcomelabel = gtk.Label("Pick a time zone:")
		timezonepage.add(welcomelabel)
		global zone
		zone = gtk.ComboBoxText()
		zone.append_text("US/Pacific")
		zone.append_text("US/Central")
		zone.append_text("US/Eastern")
		zone.append_text("gmt")
		zone.set_active(0)
		timezonepage.add(zone)
		namelabel = gtk.Label("Enter a hostname:")
		timezonepage.add(namelabel)
		global hostname
		hostname = gtk.Entry()
		hostname.set_text("arch")
		timezonepage.add(hostname)
		
		userpage = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=6)
		welcomelabel = gtk.Label("Root password:")
		userpage.add(welcomelabel)
		global rootpassword
		rootpassword = gtk.Entry()
		userpage.add(rootpassword)
		info = gtk.Label("Username:")
		userpage.add(info)
		global username
		username = gtk.Entry()
		userpage.add(username)
		info = gtk.Label("Password:")
		userpage.add(info)
		global password
		password = gtk.Entry()
		userpage.add(password)


		summarypage = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=6)
		welcomelabel = gtk.Label()
		welcomelabel.set_markup("<b>Here's what I'm going to do:</b>\n\nImagine a list of all the commands")
		summarypage.add(welcomelabel)
		
	

		finalpage = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=6)
		welcomelabel = gtk.Label()
		welcomelabel.set_markup("I'm now going to attempt to generate an install script based on the options you selected.\nI won't run it automatically for now. Do so manually only after <b>careful</b> review.")
		finalpage.add(welcomelabel)
		gobutton = gtk.Button("GO!")
		gobutton.connect("clicked", self.write)
		finalpage.pack_end(gobutton, False, False, padding=5)
		terminal = vte.Terminal()
		terminal.connect ("child-exited", lambda term: gtk.main_quit())
		terminal.feed_child("echo hi", True)
		finalpage.add(terminal)

		#Tabs
		welcome = gtk.Label("Welcome")
		software = gtk.Label("Software")
		displaymanager = gtk.Label("Display Manager")
		disks = gtk.Label("Disks")
		users = gtk.Label("Users")
		finish = gtk.Label("Finish")
		timezone = gtk.Label("Time Zone")
		summary = gtk.Label("Summary")
		keyboard = gtk.Label("Keyboard layout")
		mainbook.append_page(welcomepage, welcome)
		mainbook.append_page(partitionpage, disks)
		mainbook.append_page(softwarepage, software)
		mainbook.append_page(keyboardpage, keyboard)
		mainbook.append_page(timezonepage, timezone)
		mainbook.append_page(userpage, users)
		mainbook.append_page(summarypage, summary)
		mainbook.append_page(finalpage, finish)


	def nextbutton(self, button):
		mainbook.next_page()
		
	def write(self, button):
		print("generating install script")
		out = open("out.sh", "a");
		
		#Format the drive
		if ext3.get_active() & drive1.get_active():
			out.write("sudo mkfs.ext3 NO NO /dev/sda\n")
		if ext3.get_active() & drive2.get_active():
			out.write("sudo mkfs.ext3 NO NO /dev/sdb\n")
		if ext4.get_active() & drive1.get_active():
			out.write("sudo mkfs.ext4 NO NO /dev/sda\n")
		if ext4.get_active() & drive2.get_active():
			out.write("sudo mkfs.ext4 NO NO /dev/sdb\n")
		
		out.write("echo ''\necho ''\necho '################################################################################'\necho ''\necho ''\n")
		
		#Mount
		if drive1.get_active():
			out.write("mount /dev/sda1 /mnt\n")
		if drive2.get_active():
			out.write("mount /dev/sdb1 /mnt\n")
			
		out.write("echo ''\necho ''\necho '################################################################################'\necho ''\necho ''\n")

		#Arch stuff
		out.write("pacstrap -i /mnt base base-devel\n")

		out.write("echo ''\necho ''\necho '################################################################################'\necho ''\necho ''\n")

		out.write("genfstab -U -p /mnt >> /mnt/etc/fstab\n")
		out.write("arch-chroot /mnt echo 'en_US.UTF-8 UTF-8' > /etc/locale.gen\n")
		out.write("arch-chroot /mnt locale-gen\n")
		
		out.write("echo ''\necho ''\necho '################################################################################'\necho ''\necho ''\n")

		out.write("arch-chroot /mnt echo LANG=en_US.UTF-8 > /etc/locale.conf\n")
		out.write("arch-chroot /mnt EXPORT LANG=en_US.UTF-8\n")
		out.write("arch-chroot /mnt ln -s /usr/share/zoneinfo/" + str(zone.get_active_text()) + " /etc/localtime\n")
		
		out.write("echo ''\necho ''\necho '################################################################################'\necho ''\necho ''\n")

		out.write("arch-chroot /mnt hwclock --systohc --utc\n")
		
		out.write("echo ''\necho ''\necho '################################################################################'\necho ''\necho ''\n")

		out.write("arch-chroot /mnt echo " + hostname.get_text().strip()+ " > /etc/hostname\n")
		#out.write("arch-chroot /mnt echo 'A MAGICAL COMMAND THAT PUTS THE HOSTNAME IN /ETC/HOSTS'\n")

		out.write("echo ''\necho ''\necho '################################################################################'\necho ''\necho ''\n")
		
		#Make sure a root password was entered
		if rootpassword.get_text().strip() == "":
			raise ValueError("You didn't enter a root password")
		else:
			out.write("arch-chroot /mnt passwd root " + rootpassword.get_text().strip() + "\n")

		out.write("echo ''\necho ''\necho '################################################################################'\necho ''\necho ''\n")
			
		out.write("arch-chroot /mnt pacman -S grub\n")
		
		out.write("echo ''\necho ''\necho '################################################################################'\necho ''\necho ''\n")

		out.write("arch-chroot /mnt grub-install --target=i386-pc --recheck /dev/sda\n")
		
		out.write("echo ''\necho ''\necho '################################################################################'\necho ''\necho ''\n")

		out.write("arch-chroot /mnt grub-mkconfig -o /boot/grub/grub.cfg\n")

		out.write("echo ''\necho ''\necho '################################################################################'\necho ''\necho ''\n")

		#out.write("arch-chroot /mnt pacman -S liri-*\n")
		out.write("arch-chroot /mnt pacman -S xorg-server xorg-xinit xorg-server-utils mesa\n")
		out.write("arch-chroot /mnt pacman -S xorg-twm xorg-xclock xterm\n")
		out.write("arch-chroot /mnt pacman -S lxde\n")
		out.write("arch-chroot /mnt systemctl enable lxdm\n")
				
		out.write("echo ''\necho ''\necho '################################################################################'\necho ''\necho ''\n")
				
		if username.get_text().strip() == "":
			raise ValueError("You didn't enter a username")
		else:
			out.write("arch-chroot /mnt useradd -m -G wheel -s /bin/bash " + username.get_text().strip()+ "\n")
		
		out.write("echo ''\necho ''\necho '################################################################################'\necho ''\necho ''\n")

		if password.get_text().strip() == "":
			raise ValueError("You didn't enter a user password")
		else:
			out.write("arch-chroot /mnt passwd " + username.get_text().strip()+  " " + password.get_text().strip()+ "\n")
		
		out.write("echo ''\necho ''\necho '################################################################################'\necho ''\necho ''\n")
		
		#out.write("arch-chroot /mnt visudo things\n")
		
		for package in packages:
			if package.get_active() == True:
				out.write("sudo pacman -S install " + package.get_label() + "\n")
				out.write("echo ''\necho ''\necho '################################################################################'\necho ''\necho ''\n")
			else:
				out.write("echo 'skipping " + package.get_label() + "'\n")
				out.write("echo ''\necho ''\necho '################################################################################'\necho ''\necho ''\n")
		
		out.write("echo ''\necho ''\necho '################################################################################'\necho ''\necho ''\n")

		out.write("echo 'Done!'")
			
		out.close()
		#os.system("bash out.sh")
		gtk.main_quit()

	def backbutton(self, button):
		mainbook.prev_page()
		
	def quitbutton(self, button):
		gtk.main_quit()

win = installer()
gtk.Window.resize(win,800,500)
win.connect("delete-event", gtk.main_quit)
win.show_all()
gtk.main()
