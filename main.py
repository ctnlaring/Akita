#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# Akita
# Copyright (C) 2017 Collin Norwood <cnorwood7641@stu.neisd.net>

import gi, os
gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')
from gi.repository import Gtk, Vte, GdkPixbuf, GLib
from subprocess import call
os.system("rm out.sh")
os.system("echo 'echo installing' > out.sh")
print("Welcome to Akita")
print("This terminal will show some debug output")

class installer(Gtk.Window):

	def __init__(self):

		Gtk.Window.__init__(self, title="Akita")
		self.set_border_width(10)
		self.set_icon_from_file("data/icon.png")
		self.set_wmclass ("Akita", "Akita")
		box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.add(box)
		global mainbook
		mainbook = Gtk.Notebook()
		box.pack_start(mainbook, True, True, padding=0)


		buttonbox = Gtk.Box()
		box.pack_end(buttonbox, False, False, padding=5)

		button = Gtk.Button.new_with_label("Exit")
		button.connect("clicked", self.quitbutton)
		buttonbox.pack_start(button, False, False, padding=5)
		
		button = Gtk.Button.new_with_label("Next")
		button.connect("clicked", self.nextbutton)
		buttonbox.pack_end(button, False, False, padding=5)

		button = Gtk.Button.new_with_label("Back")
		button.connect("clicked", self.backbutton)
		buttonbox.pack_end(button, False, False, padding=5)


		welcomepage = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		topbox = Gtk.Box()
		welcomepage.add(topbox)
		icon = Gtk.Image()
		icon.set_from_file("data/icon.png")
		topbox.add(icon)
		welcomelabel = Gtk.Label()
		welcomelabel.set_markup("<span font_size='x-large'><b>   Welcome to Akita</b> - v0.6</span>")
		topbox.add(welcomelabel)
		label = Gtk.Label(margin=8)
		label.set_markup("<span font_size='large'><b>\n\nThis is pre-release software. It's not ready for use on systems with installations you care about. For now it won't run 'out.sh' automatically. Do so manually only after you've verified it's correct. I'm not responsible if it breaks anything\n\n</b></span>")
		label.set_line_wrap(True)
		welcomepage.add(label)
		interfaces = os.listdir("/sys/class/net")
		print("List of network cards: " + str(interfaces))
		for interface in interfaces:
			print("Checking network card:")
			print(interface)
			cards = open("/sys/class/net/" + interface + "/operstate", "r")
			if cards.read().strip() == "up":
				print("Found a working connection!")
				print("\n")
				label = Gtk.Label()
				label.set_markup("You're connected to the internet. Hooray.")
				break
			if cards.read().strip() != "up":
				print("it appears to be down :(")
				label = Gtk.Label()
				label.set_markup("<b>You don't appear to be connected to the internet.</b>")
		welcomepage.add(label)
		cards.close()
		helpbox = Gtk.Box()
		welcomepage.pack_end(helpbox, True, False, padding=6)
		help = Gtk.LinkButton("https://github.com/collinthegeek/Akita/issues/new", label="Help!")
		helpbox.pack_start(help, True, False, padding=6)
		github = Gtk.LinkButton("https://github.com/collinthegeek/Akita", label="Github")
		helpbox.pack_end(github, True, False, padding=6)



		partitionpage = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		welcomelabel = Gtk.Label(margin=6)
		welcomelabel.set_markup("<span font_size='x-large'><b>Choose where to install:</b></span>")
		partitionpage.add(welcomelabel)
		partbox = Gtk.Box()
		partitionpage.pack_end(partbox, True, True, padding=5)
		drivebox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		schemebox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
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
					firstdrive = Gtk.RadioButton(margin=5,label = "/dev/" + drive)
					drivebox.add(firstdrive)
				else:
					parts["/dev/" + drive] = Gtk.RadioButton(margin=5, group=firstdrive, label = "/dev/" + drive)
					drivebox.add(parts["/dev/" + drive])


		global ext3
		ext3 = Gtk.RadioButton(margin=6, label="ext3")
		schemebox.add(ext3)
		global ext4
		ext4 = Gtk.RadioButton(margin=5, group=ext3, label="ext4")
		schemebox.add(ext4)



		timezonepage = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)	
		global zone
		"""zone = Gtk.ComboBoxText(margin_right=500, margin_left=12, margin_top=12)
		excludedirs = set(['posix', 'right', 'Etc'])
		excludefiles = set(['MET', 'W-SU', 'zone.tab', 'PRC', 'posixrules', 'iso3166.tab', 'zone1970.tab'])
		for root, directories, filenames in os.walk('/usr/share/zoneinfo/', topdown=True):
			directories[:] = [d for d in directories if d not in excludedirs]
			filenames[:] = [f for f in filenames if f not in excludefiles]
			for filename in filenames:
				zone.append_text(os.path.join(root[20:], filename))
		zone.set_active(0)
		timezonepage.add(zone)"""
		
		
		pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename="data/map.png", width=550, height=550, preserve_aspect_ratio=True)
		zonemap = Gtk.Image.new_from_pixbuf(pixbuf)
		timezonepage.add(zonemap)
		
		namelabel = Gtk.Label(margin_right=500, margin_top=24, label="Enter a hostname:")
		timezonepage.add(namelabel)
		global hostname
		hostname = Gtk.Entry(margin_right=500, margin_left=12, margin_top=12)
		hostname.set_placeholder_text("arch")
		timezonepage.add(hostname)



		userpage = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		welcomelabel = Gtk.Label(margin=6)
		welcomelabel.set_markup("<span font_size='x-large'><b>User setup</b></span>")
		userpage.add(welcomelabel)
		info = Gtk.Label(margin_right=24, margin_left=24, margin_top=12, label="Root password:")
		userpage.add(info)
		global rootpassword
		rootpassword = Gtk.Entry(margin_right=24, margin_left=24, margin_top=12)
		userpage.add(rootpassword)
		info = Gtk.Label(margin_right=24, margin_left=24, margin_top=12, label="Administrator:")
		userpage.add(info)
		userbox = Gtk.Box()
		userpage.add(userbox)
		global username
		username = Gtk.Entry(margin_right=12, margin_left=12, margin_top=12)
		username.set_placeholder_text("username")
		userbox.pack_start(username, True, True, padding=0)
		global password
		password = Gtk.Entry(margin_right=12, margin_left=12, margin_top=12)
		password.set_placeholder_text("password")
		userbox.pack_end(password, True, True, padding=0)



		global media
		media = {
		'vlc': Gtk.CheckButton("VLC")
		}

		global internet
		internet = {
		'firefox': Gtk.CheckButton("Firefox"),
		'tor': Gtk.CheckButton("Tor"),
		'chrome': Gtk.CheckButton("Chrome"),
		'pidgin': Gtk.CheckButton("Pidgin"),
		'hangouts': Gtk.CheckButton("Hangouts"),
		'dropbox': Gtk.CheckButton("Dropbox"),
		'drive': Gtk.CheckButton("Google Drive"),
		'thunderbird': Gtk.CheckButton("Thunderbird"),
		'polari': Gtk.CheckButton("Polari"),
		'transmission': Gtk.CheckButton("Transmission")
		}
		global productivity
		productivity = {
		'libreoffice': Gtk.CheckButton("LibreOffice"),
		'abiword': Gtk.CheckButton("AbiWord"),
		'lyx': Gtk.CheckButton("LyX"),
		}
		global games
		games = {
		'supertuxkart': Gtk.CheckButton("SuperTuxKart"),
		'frozen-bubble': Gtk.CheckButton("Fozen Bubble"),
		'battle-for-wesnoth': Gtk.CheckButton("Battle for Wesnoth")
		}
		global graphics
		graphics = {
		'gimp': Gtk.CheckButton("Gimp")
		}
		global development
		development = {
		'emacs': Gtk.CheckButton("Emacs"),
		'nano': Gtk.CheckButton("Nano")
		}
		global education
		education = {
		'celestia': Gtk.CheckButton("Celestia Space Simulator")
		}
		global utilities
		utilities = {
		'synapse': Gtk.CheckButton("Synapse"),
		'autokey': Gtk.CheckButton("Autokey"),
		'shotwell': Gtk.CheckButton("Shotwell"),
		'wine': Gtk.CheckButton("Wine"),
		'virtualbox': Gtk.CheckButton("Virtualbox")
		}



		softwarepage = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		global packages
		packages = [];
		softwarebook = Gtk.Notebook()
		softwarebook.set_tab_pos(Gtk.PositionType.LEFT)
		softwarepage.pack_end(softwarebook, True, True, padding=5)

		mediatab = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		tablabel = Gtk.Label(margin_top=6, label="Media")
		mediatab.add(tablabel)
		for app in media:
			mediatab.add(media[app])

		nettab = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		tablabel = Gtk.Label(margin_top=6, label="Internet")
		nettab.add(tablabel)
		for app in internet:
			nettab.add(internet[app])

		productivitytab = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		tablabel = Gtk.Label(margin_top=6, label="Productivity")
		productivitytab.add(tablabel)
		for app in productivity:
			productivitytab.add(productivity[app])

		gamestab = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		tablabel = Gtk.Label(margin_top=6, label="Games")
		gamestab.add(tablabel)
		for app in games:
			gamestab.add(games[app])

		graphicstab = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		tablabel = Gtk.Label(margin_top=6, label="Graphics")
		graphicstab.add(tablabel)
		for app in graphics:
			graphicstab.add(graphics[app])

		devtoolstab = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		tablabel = Gtk.Label(margin_top=6, label="Developer Tools")
		devtoolstab.add(tablabel)
		for app in development:
			devtoolstab.add(development[app])

		educationtab = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		tablabel = Gtk.Label(margin_top=6, label="Education")
		educationtab.add(tablabel)
		for app in education:
			educationtab.add(education[app])

		utilitiestab = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		tablabel = Gtk.Label(margin_top=6, label="Utilites")
		utilitiestab.add(tablabel)
		for app in utilities:
			utilitiestab.add(utilities[app])

		media = Gtk.Label("Media")
		net = Gtk.Label("Internet")
		productivity = Gtk.Label("Productivity")
		games = Gtk.Label("Games")
		graphics= Gtk.Label("Graphics")
		devtools = Gtk.Label("Dev Tools")
		education = Gtk.Label("Education")
		utilites = Gtk.Label("Utilites")
		softwarebook.append_page(mediatab, media)
		softwarebook.append_page(nettab, net)
		softwarebook.append_page(productivitytab, productivity)
		softwarebook.append_page(gamestab, games)
		softwarebook.append_page(graphicstab, graphics)
		softwarebook.append_page(devtoolstab, devtools)
		softwarebook.append_page(educationtab, education)
		softwarebook.append_page(utilitiestab, utilites)



		summarypage = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		welcomelabel = Gtk.Label(margin=6)
		welcomelabel.set_markup("<span font_size='x-large'><b>Summary:</b></span>")
		summarypage.add(welcomelabel)
		summarylabel = Gtk.Label()
		summarylabel.set_markup("Here's what I'm going to do:\n\nMake an XXX filesystem on XXX\nPut Arch on it\nSet up your hostname, passwords, user, GRUB, etc.\nInstall the following applications:\n")
		summarypage.add(summarylabel)



		finalpage = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		welcomelabel = Gtk.Label()
		welcomelabel.set_markup("I'm now going to attempt to generate an install script based on the options you selected.\nI won't run it automatically for now. Do so manually only after <b>careful</b> review.")
		finalpage.add(welcomelabel)
		gobutton = Gtk.Button("GO!")
		gobutton.connect("clicked", self.write)
		finalpage.pack_end(gobutton, False, False, padding=5)
		terminal = Vte.Terminal()
		terminal.spawn_sync(Vte.PtyFlags.DEFAULT, ".", ["/bin/bash"], [], GLib.SpawnFlags.DO_NOT_REAP_CHILD, None, None)
		command="hi"
		#terminal.feed_child(command, len(command))
		finalpage.add(terminal)

		#Tabs
		welcome = Gtk.Label("Welcome")
		disks = Gtk.Label("Disks")
		timezone = Gtk.Label("Time Zone")
		users = Gtk.Label("Users")
		software = Gtk.Label("Software")
		summary = Gtk.Label("Summary")
		finish = Gtk.Label("Finish")
		mainbook.append_page(welcomepage, welcome)
		mainbook.append_page(partitionpage, disks)
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
							out.write("mkfs.ext4 " + firstdrive.get_label() + "\n")
							out.write("mount " + firstdrive.get_label() + " /mnt\n")
					runs = 2
				else:
					if parts[part].get_active():
						out.write("mkfs.ext4 " + part + "\n")
						out.write("mount " + part + " /mnt\n")


		out.write("echo ''\necho ''\necho '################################################################################'\necho ''\necho ''\n")

		out.write("pacstrap -i /mnt base base-devel\n")

		out.write("echo ''\necho ''\necho '################################################################################'\necho ''\necho ''\n")

		out.write("genfstab -U -p /mnt >> /mnt/etc/fstab\n")
		out.write("arch-chroot /mnt echo 'en_US.UTF-8 UTF-8' > /etc/locale.gen\n")
		out.write("arch-chroot /mnt locale-gen\n")

		out.write("echo ''\necho ''\necho '################################################################################'\necho ''\necho ''\n")

		out.write("arch-chroot /mnt echo LANG=en_US.UTF-8 > /etc/locale.conf\n")
		out.write("arch-chroot /mnt EXPORT LANG=en_US.UTF-8\n")
		out.write("arch-chroot /mnt rm /etc/localtime\n")
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
			out.write("arch-chroot /mnt yes " + rootpassword.get_text().strip() + " | passwd root\n")

		out.write("echo ''\necho ''\necho '################################################################################'\necho ''\necho ''\n")

		out.write("arch-chroot /mnt pacman -S grub\n")

		out.write("echo ''\necho ''\necho '################################################################################'\necho ''\necho ''\n")

		out.write("arch-chroot /mnt grub-install --target=i386-pc --recheck /dev/sda\n")

		out.write("echo ''\necho ''\necho '################################################################################'\necho ''\necho ''\n")

		out.write("arch-chroot /mnt grub-mkconfig -o /boot/grub/grub.cfg\n")

		out.write("echo ''\necho ''\necho '################################################################################'\necho ''\necho ''\n")

		out.write("arch-chroot /mnt pacman -S xorg-apps\n")
		out.write("arch-chroot /mnt pacman -S xorg-server xorg-xinit mesa\n")
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
				out.write("pacman -S install " + internet[app].get_label() + "\n")
				out.write("echo ''\necho ''\necho '################################################################################'\necho ''\necho ''\n")


		out.write("echo 'Done!'")

		out.close()
		#os.system("bash out.sh")
		print("\n\n")
		print("Now open 'out.sh' in your favorite editor and make sure it's correct before running it. AS ROOT!")
		print("You've been warned")
		Gtk.main_quit()

	def backbutton(self, button):
		mainbook.prev_page()

	def quitbutton(self, button):
		Gtk.main_quit()

win = installer()
Gtk.Window.resize(win,800,500)
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
