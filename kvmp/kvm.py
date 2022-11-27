import libvirt
import typing
from flask import render_template
import random
import uuid

def get_ips(instance: libvirt.virDomain) -> tuple:
    querytype = libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT
    ipversion   = libvirt.VIR_IP_ADDR_TYPE_IPV4
    try:
        ifaces = instance.interfaceAddresses(querytype)
    except Exception as e:
        return ('error', None)

    if 'lo' in ifaces.keys():
        ifaces.pop('lo', None)

    return (
        'OK',
        [addr['addr'] for addr in ifaces[key]['addrs'] for key in ifaces.keys()]
    )

def generate_mac_address():
    return "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255))

render_template(
    'ubuntu_22_04.xml',
    name='ubuntu2204-3',
    uuid=uuid.uuid1(),
    mem_kib=43434,
    current_mem_kib=434343,
    source_file="/var/lib/libvirt/images/ubuntu22.04-2.qcow2"
    mac_address=generate_mac_address
)

conn = libvirt.open('qemu:///system')
if conn == None:
  print('Failed to connecto to the hypervizor')
  exit(1)

# get system info of the host
# https://libvirt.org/docs/libvirt-appdev-guide-python/en-US/html/ch03s04s17.html
conn.getSysinfo()

instance = conn.defineXML(xmlconfig)
if instance == None:
  print('Failed to define the instance')
  exit(1)

instances = conn.listDefinedDomains()
print('Defined instances: {}'.format(instances))
result = instance.create()
if instance.isActive() == 1:
    print("Running")
else:
    print("Not Running")

state, reason = instance.state()
instance_info = {
    "name": instance.name(),
    "is_active": instance.isActive(),
    "info": instance.info(),
    "max_memory": instance.maxMemory(),
    "OS_Type": instance.OSType(),
    "state": state,
    "reason": reason,
    "cpu_stats": instance.getCPUStats(0)
}




result_destroy = instance.destroy()
result_undefine = instance.undefine()

if result_destroy == 0 and result_undefine == 0:
    print("Destroyed")
else:
    print("Not Destroyed")

conn.close()


instance_table = []

for instance_name in conn.listAllDomains():
    i = conn.lookupByName(instances[0])
    instance_table.add(
        {
            "name": instance_name,
            "id": i.ID(),
            "os_type": i.OSType(),
            "cpus": i.maxVcpus(),
            "ram": i.maxMemory() / 1024 / 1024 # GiB of RAM
        }
    )
