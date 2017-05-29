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
		self.set_icon_from_file("icon.png")
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
		topbox = gtk.Box()
		welcomepage.add(topbox)
		icon = gtk.Image()
		icon.set_from_file("icon.png")
		topbox.add(icon)
		welcomelabel = gtk.Label()
		welcomelabel.set_markup("<span font_size='x-large'><b>   Welcome to Akita</b> - v0.6</span>")
		topbox.add(welcomelabel)
		label = gtk.Label(margin=8)
		label.set_markup("<span font_size='large'><b>\n\nThis is pre-release software. It's not ready for use on systems with installations you care about. For now it won't run 'out.sh' automatically. Do so manually only after you've verified it's correct. I'm not responsible if it breaks anything\n\n</b></span>")
		label.set_line_wrap(True)
		welcomepage.add(label)
		interfaces = os.listdir("/sys/class/net")
		print("List of network cards: " + str(interfaces))
		for interface in interfaces:
			print("Checking network card:")
			print interface
			cards = open("/sys/class/net/" + interface + "/operstate", "r")
			if cards.read().strip() == "up":
				print("Found a working connection!")
				print("")
				label = gtk.Label()
				label.set_markup("You're connected to the internet. Hooray.")
				break
			if cards.read().strip() != "up":
				print ("it appears to be down :(")
				label = gtk.Label()
				label.set_markup("<b>You don't appear to be connected to the internet.</b>")
		welcomepage.add(label)
		cards.close()
		helpbox = gtk.Box()
		welcomepage.pack_end(helpbox, True, False, padding=6)
		help = gtk.LinkButton("https://github.com/collinthegeek/Akita/issues/new", label="Help!")
		helpbox.pack_start(help, True, False, padding=6)
		github = gtk.LinkButton("https://github.com/collinthegeek/Akita", label="Github")
		helpbox.pack_end(github, True, False, padding=6)
		
	
		
		partitionpage = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=6)
		welcomelabel = gtk.Label(margin=6)
		welcomelabel.set_markup("<span font_size='x-large'><b>Choose where to install:</b></span>")
		partitionpage.add(welcomelabel)
		partbox = gtk.Box()
		partitionpage.pack_end(partbox, True, True, padding=5)
		drivebox = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=6)
		schemebox = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=6)
		partbox.add(drivebox)
		partbox.add(schemebox)

		drives = os.listdir("/dev")
		runs = 1
		global parts
		parts = {}
		
		for drive in drives:
			if drives[drives.index(drive)][0]=="s" and drives[drives.index(drive)][1]=="d":
				if runs == 1:
					runs = 2
					global firstdrive
					firstdrive = gtk.RadioButton(margin=5,label = "/dev/" + drive)
					drivebox.add(firstdrive)
				else:
					parts["/dev/" + drive] = gtk.RadioButton(margin=5, group=firstdrive, label = "/dev/" + drive)
					drivebox.add(parts["/dev/" + drive])


		global ext3
		ext3 = gtk.RadioButton(margin=6, label="ext3")
		schemebox.add(ext3)
		global ext4
		ext4 = gtk.RadioButton(margin=5, group=ext3, label="ext4")
		schemebox.add(ext4)
		


		keyboardpage = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=6)
		welcomelabel = gtk.Label(margin=6)
		welcomelabel.set_markup("<span font_size='x-large'><b>This will let you pick keyboard layouts</b></span>")
		keyboardpage.add(welcomelabel)



		timezonepage = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=6)
		welcomelabel = gtk.Label(margin_right=600, margin_top=12, label="Pick a time zone:")
		timezonepage.add(welcomelabel)
		global zone
		zone = gtk.ComboBoxText(margin_right=600, margin_left=12, margin_top=12)
		zone.append_text("US/Pacific")
		zone.append_text("US/Central")
		zone.append_text("US/Eastern")
		zone.append_text("gmt")
		zone.set_active(0)
		timezonepage.add(zone)
		namelabel = gtk.Label(margin_right=600, margin_top=24, label="Enter a hostname:")
		timezonepage.add(namelabel)
		global hostname
		hostname = gtk.Entry(margin_right=600, margin_left=12, margin_top=12)
		hostname.set_placeholder_text("arch")
		timezonepage.add(hostname)

		
		
		userpage = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=6)
		welcomelabel = gtk.Label(margin=6)
		welcomelabel.set_markup("<span font_size='x-large'><b>User setup</b></span>")
		userpage.add(welcomelabel)
		info = gtk.Label(margin_right=24, margin_left=24, margin_top=12, label="Root password:")
		userpage.add(info)
		global rootpassword
		rootpassword = gtk.Entry(margin_right=24, margin_left=24, margin_top=12)
		userpage.add(rootpassword)
		info = gtk.Label(margin_right=24, margin_left=24, margin_top=12, label="Administrator:")
		userpage.add(info)
		userbox = gtk.Box()
		userpage.add(userbox)
		global username
		username = gtk.Entry(margin_right=12, margin_left=12, margin_top=12)
		username.set_placeholder_text("username")
		userbox.pack_start(username, True, True, padding=0)
		global password
		password = gtk.Entry(margin_right=12, margin_left=12, margin_top=12)
		password.set_placeholder_text("password")
		userbox.pack_end(password, True, True, padding=0)
		
		
		
		global media
		media = {
		'vlc': gtk.CheckButton("VLC")
		}
		
		global internet
		internet = {
		'firefox': gtk.CheckButton("Firefox"),
		'tor': gtk.CheckButton("Tor"),
		'chrome': gtk.CheckButton("Chrome"),
		'pidgin': gtk.CheckButton("Pidgin"),
		'hangouts': gtk.CheckButton("Hangouts"),
		'dropbox': gtk.CheckButton("Dropbox"),
		'drive': gtk.CheckButton("Google Drive")
		}
		global productivity
		productivity = {
		'libreoffice': gtk.CheckButton("LibreOffice")
		}
		global games
		games = {

		}
		global graphics
		graphics = {
		'gimp': gtk.CheckButton("Gimp")
		}
		global development
		development = {
		'emacs': gtk.CheckButton("Emacs"),
		'nano': gtk.CheckButton("Nano")
		}
		global education
		education = {

		}
		global utilities
		utilities = {
		'synapse': gtk.CheckButton("Synapse"),
		'autokey': gtk.CheckButton("Autokey"),
		'shotwell': gtk.CheckButton("Shotwell"),
		'wine': gtk.CheckButton("Wine"),
		'virtualbox': gtk.CheckButton("Virtualbox")
		}



		softwarepage = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=6)
		global packages
		packages = [];
		softwarebook = gtk.Notebook()
		softwarebook.set_tab_pos(gtk.PositionType.LEFT)
		softwarepage.pack_end(softwarebook, True, True, padding=5)
		
		mediatab = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=6)
		tablabel = gtk.Label(margin_top=6, label="Media")
		mediatab.add(tablabel)
		for app in media:
			mediatab.add(media[app])
		
		nettab = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=6)
		tablabel = gtk.Label(margin_top=6, label="Internet")
		nettab.add(tablabel)
		for app in internet:
			nettab.add(internet[app])
		
		productivitytab = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=6)
		tablabel = gtk.Label(margin_top=6, label="Productivity")
		productivitytab.add(tablabel)
		for app in productivity:
			productivitytab.add(productivity[app])
		
		gamestab = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=6)
		tablabel = gtk.Label(margin_top=6, label="Games")
		gamestab.add(tablabel)
		for app in games:
			gamestab.add(games[app])
		
		graphicstab = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=6)
		tablabel = gtk.Label(margin_top=6, label="Graphics")
		graphicstab.add(tablabel)
		for app in graphics:
			graphicstab.add(graphics[app])
		
		devtoolstab = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=6)
		tablabel = gtk.Label(margin_top=6, label="Developer Tools")
		devtoolstab.add(tablabel)
		for app in development:
			devtoolstab.add(development[app])
		
		educationtab = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=6)
		tablabel = gtk.Label(margin_top=6, label="Education")
		educationtab.add(tablabel)
		for app in education:
			educationtab.add(education[app])
		
		utilitiestab = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=6)
		tablabel = gtk.Label(margin_top=6, label="Utilites")
		utilitiestab.add(tablabel)
		for app in utilities:
			utilitiestab.add(utilities[app])
		
		media = gtk.Label("Media")
		net = gtk.Label("Internet")
		productivity = gtk.Label("Productivity")
		games = gtk.Label("Games")
		graphics= gtk.Label("Graphics")
		devtools = gtk.Label("Dev Tools")
		education = gtk.Label("Education")
		utilites = gtk.Label("Utilites")
		softwarebook.append_page(mediatab, media)
		softwarebook.append_page(nettab, net)
		softwarebook.append_page(productivitytab, productivity)
		softwarebook.append_page(gamestab, games)
		softwarebook.append_page(graphicstab, graphics)
		softwarebook.append_page(devtoolstab, devtools)
		softwarebook.append_page(educationtab, education)
		softwarebook.append_page(utilitiestab, utilites)
		



		summarypage = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=6)
		welcomelabel = gtk.Label(margin=6)
		welcomelabel.set_markup("<span font_size='x-large'><b>Summary:</b></span>")
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
		disks = gtk.Label("Disks")
		keyboard = gtk.Label("Keyboard layout")
		timezone = gtk.Label("Time Zone")
		users = gtk.Label("Users")
		software = gtk.Label("Software")
		summary = gtk.Label("Summary")
		finish = gtk.Label("Finish")
		mainbook.append_page(welcomepage, welcome)
		mainbook.append_page(partitionpage, disks)
		mainbook.append_page(keyboardpage, keyboard)
		mainbook.append_page(timezonepage, timezone)
		mainbook.append_page(userpage, users)
		mainbook.append_page(softwarepage, software)
		mainbook.append_page(summarypage, summary)
		mainbook.append_page(finalpage, finish)


	def nextbutton(self, button):
		mainbook.next_page()
		
	def write(self, button):
		print("generating install script")
		out = open("out.sh", "a");
		runs = 1
		drives = os.listdir("/dev")
		for drive in drives:
			if drives[drives.index(drive)][0]=="s" and drives[drives.index(drive)][1]=="d":
				part = "/dev/" + drive

				if runs == 1:
					if firstdrive.get_active():
							out.write("sudo mkfs.ext4 " + firstdrive.get_label() + "\n")
							out.write("sudo mount " + firstdrive.get_label() + " /mnt\n")
					runs = 2
				else:
					if parts[part].get_active():
						out.write("sudo mkfs.ext4 " + part + "\n")
						out.write("sudo mount " + part + " /mnt\n")

			
		out.write("echo ''\necho ''\necho '################################################################################'\necho ''\necho ''\n")

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
		
		if hostname.get_text().strip() == "":
			out.write("arch-chroot /mnt echo 'arch' > /etc/hostname\n")
		else:
			out.write("arch-chroot /mnt echo " + hostname.get_text().strip()+ " > /etc/hostname\n")
			#out.write("arch-chroot /mnt echo 'A MAGICAL COMMAND THAT PUTS THE HOSTNAME IN /ETC/HOSTS'\n")

		out.write("echo ''\necho ''\necho '################################################################################'\necho ''\necho ''\n")
		
		#Make sure a root password was entered
		if rootpassword.get_text().strip() == "":
			raise ValueError("You didn't enter a root password")
			os.system("rm out.sh")
			os.system("echo 'echo installing' > out.sh")
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
			os.system("rm out.sh")
			os.system("echo 'echo installing' > out.sh")
		else:
			out.write("arch-chroot /mnt useradd -m -G wheel -s /bin/bash " + username.get_text().strip()+ "\n")
		
		out.write("echo ''\necho ''\necho '################################################################################'\necho ''\necho ''\n")

		if password.get_text().strip() == "":
			raise ValueError("You didn't enter a user password")
			os.system("rm out.sh")
			os.system("echo 'echo installing' > out.sh")
		else:
			out.write("arch-chroot /mnt passwd " + username.get_text().strip()+  " " + password.get_text().strip()+ "\n")
		
		out.write("echo ''\necho ''\necho '################################################################################'\necho ''\necho ''\n")
		
		#out.write("arch-chroot /mnt visudo things\n")
		
		for app in internet:
			if internet[app].get_active() == True:
				out.write("sudo pacman -S install " + internet[app].get_label() + "\n")
				out.write("echo ''\necho ''\necho '################################################################################'\necho ''\necho ''\n")
			else:
				out.write("echo 'skipping " + internet[app].get_label() + "'\n")
				out.write("echo ''\necho ''\necho '################################################################################'\necho ''\necho ''\n")
		
		out.write("echo ''\necho ''\necho '################################################################################'\necho ''\necho ''\n")

		out.write("echo 'Done!'")
			
		out.close()
		#os.system("bash out.sh")
		print("")
		print("Now open 'out.sh' in your favorite editor and make sure it's correct before running it.")
		print("You've been warned")
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
