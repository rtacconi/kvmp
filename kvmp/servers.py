from kvmp.kvm import generate_mac_address, render_xml_config, get_uuid, connect, create_instance, destroy

servers = {
    "1": {
        "name":"aleks",
        "URI":"aleks@192.168.1.140"
    },
    "2": {
        "name": "aleks-rog",
        "URI":""
    }
}
