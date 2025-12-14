import os

def block_ip(ip):
    command = f"netsh advfirewall firewall add rule name='Block {ip}' dir=in action=block remoteip={ip}"
    os.system(command)
