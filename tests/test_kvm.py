# import os
# import pytest
# import libvirt
# from kvmp.kvm import generate_mac_address, render_xml_config, get_uuid, create_instance, destroy_instance, render_tmp_file
# from kvmp.ssh import run_command, run_ssh_command
# from pathlib import Path

# KEY_FILE = f"{Path.home()}/.ssh/id_rsa2"
# XMLCONFIG = render_xml_config(
#     'ubuntu_22_04.xml',
#     {
#         'name': 'ubuntu2204-34',
#         'uuid': get_uuid(),
#         'mem_kib': 1 * 1048576,
#         'current_mem_kib': 1 * 1048576,
#         'source_file': "/var/lib/libvirt/images/ubuntu22.04.qcow2",
#         'mac_address': generate_mac_address()
#     }
# )

# def test_create_ubuntu_xml():
#     assert render_xml_config(
#         'ubuntu_22_04.xml',
#         {
#             'name': 'ubuntu2204-3',
#             'uuid': get_uuid(),
#             'mem_kib': 4 * 1048576,
#             'current_mem_kib': 4 * 1048576,
#             'source_file': "/var/lib/libvirt/images/ubuntu22.04.qcow2",
#             'mac_address': generate_mac_address()
#         }
#     ).startswith("<domain type=\"kvm\">\n  <name>ubuntu2204-3</name>")

# def test_ssh_connect():
#     stdin, stdout, stderr = run_ssh_command('192.168.1.140', 'rtacconi', KEY_FILE, 'stat /root')
#     output = stdout.read()
#     output_string = output.decode('utf-8')
#     assert 'File: /root' in output_string

# def test_render_instance_remote_hypervisor():
#     r = create_instance(XMLCONFIG, 'rtacconi', '192.168.1.140')
#     assert "Domain 'ubuntu2204-34' created" in r[0]
#     r = destroy_instance('ubuntu2204-34', 'rtacconi', '192.168.1.140')
#     assert 'destroyed' in r[0]


# def test_local_command():
#     dir = os.path.abspath(__file__)
#     result = run_command(["ls", "-l", dir])
#     assert "test_kvm.py" in result[0]

# def test_render_file():
#     render_tmp_file('/tmp/ubuntu22.04.xml', XMLCONFIG)
#     with open('/tmp/ubuntu22.04.xml', 'r') as f:
#         file_contents = f.read()
#     assert '<address type="pci" domain="0x0000" bus="0x00"' in file_contents
