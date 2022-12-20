import os
import libvirt
from jinja2 import Template
import random
import uuid
KIB = 1048576

def get_ips(instance: libvirt.virDomain) -> tuple:
    querytype = libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT
    ipversion = libvirt.VIR_IP_ADDR_TYPE_IPV4
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

def get_uuid():
    return uuid.uuid1()


def render_xml_config(source, params):
    with open(f"{os.getcwd()}/kvmp/templates/{source}", 'r') as file:
        tpl = file.read()

    template = Template(tpl)
    return template.render(params)

def connect(uri=''):
    if len(uri) == 0:
        conn = libvirt.open()
        if conn == None:
            print('Failed to connect to the hypervizor')
            exit(1)
        else:
            return conn
    else:
        conn = libvirt.open(uri)
        if conn == None:
            print('Failed to connect to the hypervizor')
            exit(1)
        else:
            return conn

# get system info of the host
# https://libvirt.org/docs/libvirt-appdev-guide-python/en-US/html/ch03s04s17.html
# conn.getSysinfo()



def create_instance(conn, xmlconfig) -> tuple:
    instance = conn.defineXML(xmlconfig)
    result = instance.create()
    if instance == None:
      return('OK', 'Failed to define the instance')

    if instance.isActive() == 1:
        return ('OK', "Running", instance)
    else:
        return ('error', "Not Running", None)

    # instances = conn.listDefinedDomains()
    # print('Defined instances: {}'.format(instances))


# state, reason = instance.state()
# instance_info = {
#     "name": instance.name(),
#     "is_active": instance.isActive(),
#     "info": instance.info(),
#     "max_memory": instance.maxMemory(),
#     "OS_Type": instance.OSType(),
#     "state": state,
#     "reason": reason,
#     "cpu_stats": instance.getCPUStats(0)
# }
#
#
#
def destroy(instance) -> tuple:
    result_destroy = instance.destroy()
    result_undefine = instance.undefine()

    if result_destroy == 0 and result_undefine == 0:
        return ('OK', "Destroyed")
    else:
        return ("error", "Not Destroyed")

# conn.close()
#
#
def get_instance_table(conn) -> tuple:
    instance_table = []
    conn = connect()
    for i in conn.listAllDomains():
        mydict = {            
                "name": i.name(),
                "id": i.ID(),
                "os_type": i.OSType(),
                "ram": i.maxMemory() / 1024 / 1024 # GiB of RAM
            }

        if i.isActive():
            mydict["cpus"] = i.maxVcpus()
            mydict["power"] = "on"
        else:
            mydict["cpus"] = 0
            mydict["power"] = "off"
        instance_table.append(mydict)

    return ('OK', instance_table)
