
from netmiko import ConnectHandler

with open('devices.txt') as routers:
    for IP in routers:
        Router = {
            'device_type': 'cisco_ios',
            'ip': IP,
            'username': 'tes',
            'password': 'test'

        }

        net_connect = ConnectHandler(**Router)

        print ('Connecting to ' + IP)
        print('-'*79)
        output = net_connect.send_command('sh int description | e  down|Employee|Guest|Mesh|Printer|WAP')
        print(output)
        output = net_connect.send_command('sh cdp nei')
        print(output)
        output = net_connect.send_command('sh lldp nei')
        print(output)
        print()
        print('-'*79)
net_connect.disconnect()

