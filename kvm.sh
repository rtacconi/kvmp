#!/bin/bash

apt install -y bridge-utils libvirt-clients libvirt-daemon-system qemu-system-x86 ssh-askpass virt-manager
systemctl stop libvirtd
usermod -aG kvm $USER
chown :kvm /var/lib/libvirt/images
chmod g+rw /var/lib/libvirt/images
systemctl restart libvirtd
