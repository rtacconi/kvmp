import pytest
import libvirt
from kvmp.kvm import generate_mac_address, render_xml_config, get_uuid, connect, create_instance, destroy

def test_create_ubuntu_xml():
    assert render_xml_config(
        'ubuntu_22_04.xml',
        {
            'name': 'ubuntu2204-3',
            'uuid': get_uuid(),
            'mem_kib': 4 * 1048576,
            'current_mem_kib': 4 * 1048576,
            'source_file': "/var/lib/libvirt/images/ubuntu22.04.qcow2",
            'mac_address': generate_mac_address()
        }
    ).startswith("<domain type=\"kvm\">\n  <name>ubuntu2204-3</name>")

def test_connect():
    conn = connect()
    assert type(conn) == libvirt.virConnect, 'It is not a libvirt.virConnect type'
    assert conn.close() == 0

def test_render_instance():
    xmlconfig = render_xml_config(
        'ubuntu_22_04.xml',
        {
            'name': 'ubuntu2204-34',
            'uuid': get_uuid(),
            'mem_kib': 1 * 1048576,
            'current_mem_kib': 1 * 1048576,
            'source_file': "/var/lib/libvirt/images/ubuntu22.04.qcow2",
            'mac_address': generate_mac_address()
        }
    )
    ituple = create_instance(connect(), xmlconfig)
    assert ituple == ('OK', 'Running', ituple[2])
    # assert destroy(ituple[2]) == ('OK', "Destroyed") 