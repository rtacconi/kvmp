# kvmp

## Development
Start by entering the venv with:
poetry shell

Run the flask app in dev mode:
poetry run flask --debug --app kvmp.control_panel run

Run pytest:
pytest

https://testdriven.io/blog/flask-htmx-tailwind/

## Migrations
To manage the database schema we use (dbmate)[https://github.com/amacneil/dbmate]

## virsh notes

(base) rtacconi@ubuntu1:~$ virsh dominfo 4
Id:             4
Name:           ubuntu2204-34
UUID:           76566b94-91e4-11ed-90ec-acde48001122
OS Type:        hvm
State:          running
CPU(s):         2
CPU time:       2.7s
Max memory:     1048576 KiB
Used memory:    1048576 KiB
Persistent:     no
Autostart:      disable
Managed save:   no
Security model: apparmor
Security DOI:   0
Security label: libvirt-76566b94-91e4-11ed-90ec-acde48001122 (enforcing)

(base) rtacconi@ubuntu1:~$ virsh domifaddr 4
 Name       MAC address          Protocol     Address
-------------------------------------------------------------------------------

(base) rtacconi@ubuntu1:~$ virsh net-list
 Name      State    Autostart   Persistent
--------------------------------------------
 default   active   yes         yes

(base) rtacconi@ubuntu1:~$ virsh net-info network
error: failed to get network 'network'
error: Network not found: no network with matching name 'network'

(base) rtacconi@ubuntu1:~$ virsh net-info default
Name:           default
UUID:           19f84246-1843-44ad-ac99-0deb7fef4ee1
Active:         yes
Persistent:     yes
Autostart:      yes
Bridge:         virbr0

## Marketing

Hosting control panel virtualization

KVM stands for Kernel-based Virtual Machine, which is a virtualization technology that allows users to run multiple operating systems on one physical server. This helps you save money by avoiding the cost of purchasing additional hardware.

Hosting control panel virtualization

The hosting control panel offers features that allow you to manage your website and domain names, create email accounts, set up databases and more.

[company name] is a SaaS provider of hosting control panel virtualization. We help you manage your servers and data, so you can focus on what matters to you.

Our dedicated teams are experienced in the industry and know exactly what it takes to deliver reliable, high-performance services. We're passionate about working with our customers and providing them with the tools they need to succeed.

The [company name] is a SaaS hosting control panel that allows you to manage your servers remotely and easily. With a friendly, intuitive interface, you can manage your servers from anywhere in the world.

There are no hardware requirements—you can use any computer or device to access your servers. No installation is required; simply log in and start using it immediately!

Virtualization is the future of hosting—and [company name] is here to help you take advantage of it.

With our control panel, you can configure your virtualization environment in seconds and be up and running within minutes. We offer a range of hosting options from basic cloud servers to fully managed dedicated server clusters: all you have to do is choose what works for your business and budget, then set it up with the click of a button.

Our team of experts will be there every step of the way to make sure your virtualization platform is running smoothly and efficiently, so that you can focus on what really matters: growing your business!
