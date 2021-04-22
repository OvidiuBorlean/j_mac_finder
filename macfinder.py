from netmiko import ConnectHandler
import time
import pathlib
import yaml

def connect(device, c_hostname, c_username, c_password, c_mac_address, c_delay):

    jnet = {
        'device_type': device,
        'host':   c_hostname,
        'username': c_username,
        'password': c_password,
        'port' : 22,
    }
    try:
        net_connect = ConnectHandler(**jnet)
        j_command = "show ethernet-switching table | match " + c_mac_address
        sndcommand = net_connect.send_command(j_command)
        print(sndcommand)
        if "c_mac_address" in sndcommand:
            print("Found in " + c_hostname)
        net_connect.disconnect()
        time.delay(c_delay)
    except:
        print("Unavailable device detected: " + c_hostname)
        unavailable_file = open("unavailable.txt","a")
        unavailable_file.write("Error connecting to " + c_hostname)
        unavailable_file.close()
if __name__ == '__main__':

    print("J-MacFinder Tool v0.10 \n")
    
    config_file = pathlib.Path("macfinder.yaml")
    if config_file.exists ():
        with open('macfinder.yaml') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            if "device" in data:
                c_device = data["device"]
            else:
                print("No <device> found in config file")
            
            if "c_username" in data:
                c_username = data["c_username"]
            else:
                print("No <username> found in config file")
            if "c_password" in data:
                c_password = data["c_password"]
            else:
                print("No <password> defined in config file")
            
            if "mac-address" in data:
                c_mac_address = data["mac-address"]
            else:
                print("No <mac-address> found in config file")
            
            if "delay" in data:
                c_delay = data["delay"]
            else:
                print("No <delay> found in config file")

    hostsdb = open("hosts.db","r")
    hostline = hostsdb.read()
    host_item = hostline.split("\n")
    for i in host_item:
        print("Checking the device: " + i)
        connect(c_device, i, c_username, c_password, c_mac_address, c_delay)
        