import paramiko
import subprocess

def run_ssh_command(hostname, username, key_path, command):
    # Set up the SSH client
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    private_key = paramiko.RSAKey.from_private_key_file(key_path)
    # Connect to the remote host
    client.connect(hostname=hostname, username=username, pkey=private_key)
    # Execute the command
    stdin, stdout, stderr = client.exec_command(command)
    # Close the connection
    stdin.close()

    return stdin, stdout, stderr

def run_command(command):
    result = subprocess.run(
        command, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )
    return result.stdout.decode('utf-8'), result.stderr.decode('utf-8')
