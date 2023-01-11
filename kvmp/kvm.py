import os
import libvirt
from jinja2 import Template
import random
import uuid
from kvmp.ssh import run_command

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

def create_instance(xmlconfig, username, host) -> tuple:
    result = run_command([
        "virsh", "-c", f"qemu+ssh://{username}@{host}/system", 
        "create", "/Users/riccardotacconi/ubuntu22.04.xml"
    ])
    print(result)
    return result

def destroy_instance(name, username, host) -> tuple:
    cmd = [
        "virsh", "-c", f"qemu+ssh://{username}@{host}/system", "list"
    ]
    result = run_command(cmd)
    last_line = [i for i in result[0].split("\n") if name in i][0].split(' ')
    id = [i for i in last_line if i != '' and i.isnumeric()][0]
    cmd = ["virsh", "-c", f"qemu+ssh://{username}@{host}/system", "destroy", id]
    result = run_command(cmd)

    return result

def render_tmp_file(name, content):
    with open(name, 'w') as f:
        f.write(content)
        f.close()
