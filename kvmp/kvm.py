import os
from jinja2 import Template
import random
import uuid
from kvmp.ssh import run_command
import kvmp.db as db
import tempfile
import subprocess

KIB = 1048576

def run_command(command):
    result = subprocess.run(
        command, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )
    return result.stdout.decode('utf-8'), result.stderr.decode('utf-8')

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
    with tempfile.NamedTemporaryFile(mode='w', dir='/tmp', delete=False) as f:
        f.write(xmlconfig)
        xml_file = f.name

    result = run_command([
        "virsh", "-c", f"qemu+ssh://{username}@{host}/system", 
        "create", xml_file
    ])
    return result

def parse_vm_info(name, username, host) -> dict:
    result = run_command([
        "virsh", "-c", f"qemu+ssh://{username}@{host}/system", 
        "dominfo", name
    ])
    
    output = []
    for line in result[0].strip().split("\n"):
        columns = line.strip().split()
        output.append({"name": columns[0], "state": ' '.join(columns[1:])})

    keys = [d['name'] for d in output]
    values = [d['state'] for d in output]

    return dict(zip(keys, values))

def store_vm_info(name, data, server_id, user_id, xmlconfig, username, host):
    vm_info_id = db.add_vm_info(data, server_id, user_id)
    xml_data = parse_vm_info(name, xmlconfig, username, host)
    db.add_xml_template(name, user_id, vm_info_id, xml_data)

def create_instance_workflow(name, ram, source_file, server_id, user_id, username, host):
    xmlconfig = render_xml_config(
        'ubuntu_22_04.xml',
        {
            'name': name,
            'uuid': get_uuid(),
            'mem_kib': 4 * ram,
            'current_mem_kib': 4 * ram,
            'source_file': source_file,
            'mac_address': generate_mac_address()
        }
    )
    # create an instance with virsh
    create_instance(xmlconfig, username, host)
    # get instance info and parse it to a dict
    data = parse_vm_info(name, xmlconfig, username, host)
    # store instaince info and XML template to their relative tables 
    # with user and server info
    store_vm_info(name, data, server_id, user_id, xmlconfig, username, host)
    # TODO: return a more informative result then True
    return True

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
