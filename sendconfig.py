'''
Python - Netmiko library to connect to network devices via ssh
MANUALLY ENTER CREDS
CONNECT TO DEVICES LISTED IN EXTERNAL FILE
SEND CONFIGURATIONS FROM EXTERNAL FILE
SCRIPT PERFORM ERROR HANDLING BEFORE AUTHENTICATING TO IP AND IF FILE DOES NOT EXIST
'''
from netmiko import ConnectHandler
from getpass import getpass
from netmiko import ConnectHandler
from netmiko.exceptions import NetMikoTimeoutException
from netmiko.exceptions import AuthenticationException
from netmiko.exceptions import SSHException
import time
import ipaddress

def main():
    while True:
        file1 = input("\nConfiguration File Name: ")
        try:
            with open(file1) as f:
                commands_to_send = f.read().splitlines()
        except FileNotFoundError as fnf_error:
            print('')
            print(fnf_error, "...try again...")
            continue
        else:
            while True:
                file2 = input("\nIP Address File Name: ")
                try:
                    with open(file2) as f:
                        devicelist = f.read().splitlines()
                except FileNotFoundError as fnf_error:
                    print('')
                    print(fnf_error, "...try again...")
                    continue
                else: 
                    break
            break

    username = input("\nEnter SSH Username: ")
    password = getpass()
    enable = input("Enter enable secret (if required, or hit enter): ") # if device requires enable secret password

    with open("Output_Report.txt", "a") as saveoutput:
        for device_ip in devicelist:
            print('\n\n---- Veryfing if ' + str(device_ip) + ' is a valid IP...')
            time.sleep(1)
            try:
                ipaddress.ip_address(device_ip)
                print("\n---- IP address {} is valid...".format(device_ip))
                time.sleep(1)    
            except ValueError:
                print("\n---- IP address {} is not valid".format(device_ip))
                access_issue = (device_ip + ' invalid IP')
                saveoutput.write(access_issue + ("\n"))
                saveoutput.write(' ')
                time.sleep(1)
                continue       
            print('\n---- Connecting to IP: ' + str(device_ip) + '...')
            time.sleep(1)
            ios_device = {
            'device_type': 'cisco_ios',
            'ip': device_ip,
            'username': username,
            'password': password,
            'secret': enable # if device requires enable secret password
            }
        #Script to perform error handling before attempting a connection to the device listed in Device_File file:
            try:
                net_connect = ConnectHandler(**ios_device)
                net_connect.enable()  # if device requires enable secret password
            except (AuthenticationException):
                access_issue = (device_ip + ' Authentication failure')
                print ('\n---- Authentication issue\n')
                saveoutput.write(access_issue + ("\n"))
                saveoutput.write(' ')
                continue
            except (NetMikoTimeoutException):
                access_issue = (device_ip + ' Timeout')
                print('---- Timeout\n')
                saveoutput.write(access_issue + ("\n"))
                saveoutput.write(' ')
                continue
            except (EOFError):
                access_issue = (device_ip + ' Access Error')
                print('---- End of file while attempting access')
                saveoutput.write(access_issue + ("\n"))
                saveoutput.write(' ')
                continue
            except (SSHException):
                access_issue = (device_ip + ' SSH not enable')
                print('---- SSH Issue. Check SSH settings')
                saveoutput.write(access_issue + ("\n"))
                saveoutput.write(' ')
                continue
            except Exception as unknown_error:
                access_issue = (device_ip + ' Unknown error')
                print ('---- Cannot connect. Unknown error')
                print ('---- Unknown error: ' + str(unknown_error))
                saveoutput.write(access_issue + ("\n"))
                saveoutput.write(' ')
                continue
            
            print ('\n---- Successfully connected ')
            time.sleep(1)
            saveoutput.write(str(device_ip) + (' connected' + ("\n")))
            print ('\n---- Sending configurations.... \n')
            output1 = net_connect.send_config_set(commands_to_send)
            print (output1)
            #saveoutput.write(" ")
            #saveoutput.write(output1)
            #saveoutput.write(" ")
            print('\n---- Successfully configured: ' + str(device_ip))
            saveoutput.write(str(device_ip) + 'configured' +  ('\n'))
            print('\n======================================')
            saveoutput.write(" ")

if __name__ == "__main__":
    main()

