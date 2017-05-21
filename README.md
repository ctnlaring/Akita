# arch installer thingy
A graphical arch linux installer in python/pygtk

The idea of this is that every screen will have multiple options which 
will change variables for that screen. When you hit the next button it 
puts those variables together into a command which it appends to a file 
"install" which is just a bash script that will run at the end.

# testing
this current version is obviously super early and doesn't work at all. Right now there's a checkbox on first screen and depending on whether or not it's checked when you hit next it will add a line to the output script to install firefox. This only works if you have gnome-terminal and dnf installed at the moment.

Ex:

On the partitioning screen you chose to partition /dev/sda1 as ext4. It 
will set a varible for the partition type and one for the partition 
you're formatting then when you hit next it 
will add the command "mkfs.ext4 /dev/sda1" to the install script. 
Everything is done in python/pygtk so it can be material with Liri's gtk 
theme/flat-plat


