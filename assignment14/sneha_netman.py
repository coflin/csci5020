#!/usr/bin/python

"""
Assignment 14: NETWORK MANAGEMENT AUTOMATION.
Gives the following options to the user:
1: Configure a network device
2: Ping an IP from a network device
3: Save the network device config to a file
Pre-req: A network topology configured on GNS3
"""

from netmiko import ConnectHandler
from loguru import logger
import sys

def config_router(net_connect):
    fa00ip = input("Enter the IP address & subnet mask for Fa0/0 interface (ex: 10.0.0.1 255.255.255.0): ")
    fa00desc = input("Enter the description for Fa0/0: ")
    lo0ip = input("Enter the IP address & subnet mask for Loopback 0 (ex: 11.0.0.1 255.255.255.0): ")
    lo0desc = input("Enter the description for Loopback 0: ")

    commands = ["int Fa0/0",f"description {fa00desc}",f"ip address {fa00ip}","int Lo0",f"description {lo0desc}",f"ip address {lo0ip}"]
    try:
        output = net_connect.send_config_set(commands)
        logger.info("Successfully configured the router with the provided configuration\n")
        print("show ip interface brief")
        print(net_connect.send_command("show ip interface brief"))
        print("\nshow interface description")
        print(net_connect.send_command("show interface description"))
    except Exception as e:
        logger.error(f"Unable to configure the router: {e}")
        sys.exit()

def ping_check(net_connect,routerip):
    pingip = input(f"Enter an IP address to ping from {routerip}: ")
    output = net_connect.send_command(f"ping {pingip}",read_timeout=20)
    if "Success rate is 0 percent" in output.splitlines()[4]:
        print(output)
        logger.error(f"{pingip} is not reachable from {routerip}. Please check the configuration and try again")
    else:
        print(output)
        logger.info(f"{pingip} is reachable from {routerip}. {output.splitlines()[4].split(',')[0]}")

    yn = input("Ping another IP? [y/n]: ")
    while yn == "y" or yn == "Y":
        ping_check(net_connect,routerip)
    else:
        sys.exit()

def save_config(net_connect):
    try:
        output = net_connect.send_command("show running-config")
        with open("config.txt","w") as file:
            file.write(output)
        logger.info("Saved configuration to config.txt")
    except:
        logger.error("Unable to write to file config.txt")

def main():
    print("1: Configure a device\n2: Ping a device to check IP connectivity\n3: Save the configuration")
    option = input("Select an option (1 or 2 or 3): ")

    routerip = input("Enter the IP address of the router you want to check/configure: ")
    username = input("Enter the username to login to the device: ")
    password = input("Enter the password of the device: ")

    ios = {
        'device_type':'cisco_ios',
        'ip':routerip,
        'username':username,
        'password':password,
    }

    try:
        net_connect = ConnectHandler(**ios)
        logger.info(f"Successfully connected to {routerip} as '{username}' with password '{password}'\n")
    except:
        logger.error(f"Unable to connect to {routerip} as {username}. Please try again.")
        sys.exit()

    if option == "1":
        config_router(net_connect)

    elif option == "2":
        ping_check(net_connect,routerip)

    elif option == "3":
        save_config(net_connect)

if __name__ == "__main__":
    main()