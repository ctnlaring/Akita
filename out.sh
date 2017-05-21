echo installing
mkfs.ext4 /dev/sdb1
mount /dev/sdb1 /mnt
pacstrap -i /mnt base base-devel
genfstab -U -p /mnt >> /mnt/etc/fstab
arch-chroot /mnt echo 'en_US.UTF-8 UTF-8' > /etc/locale.gen
arch-chroot /mnt locale-gen
arch-chroot /mnt echo LANG=en_US.UTF-8 > /etc/locale.conf
arch-chroot /mnt export LANG=en_US.UTF-8
arch-chroot /mnt ln -s /usr/share/zoneinfo/US/Central /etc/localtime
arch-chroot /mnt hwclock --systohc --utc
arch-chroot /mnt echo hostname > /etc/hostname
arch-chroot /mnt passwd 12345
arch-chroot /mnt pacman -S grub
arch-chroot /mnt grub-install --target=i386-pc --recheck /dev/sda
arch-chroot /mnt grub-mkconfig -o /boot/grub/grub.cfg
arch-chroot /mnt pacman -S xorg-server xorg-xinit xorg-server-utils mesa
arch-chroot /mnt pacman -S xorg-twm xorg-xclock xterm
arch-chroot /mnt pacman -S lxde
arch-chroot /mnt systemctl enable lxdm
arch-chroot /mnt useradd -m -G wheel -s /bin/bash collin
arch-chroot /mnt passwd collin 12345
echo 'Done!'