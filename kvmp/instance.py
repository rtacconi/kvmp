from kvmp.kvm import get_instance_table, connect

instances = get_instance_table(connect())[1]