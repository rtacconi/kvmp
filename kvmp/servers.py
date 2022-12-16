from kvmp.kvm import generate_mac_address, render_xml_config, get_uuid, connect, create_instance, destroy

servers = {
    "1": {
        "name":"aleks",
        "URI":"aleks@192.168.1.187"
    },
    "2": {
        "name": "aleks-rog",
        "URI":""
    }
}

# connection = connect(servers["2"]["URI"])
connection2 = connect(f"qemu+ssh://{servers['1']['URI']}/system")
# print(connection)
print(connection2)