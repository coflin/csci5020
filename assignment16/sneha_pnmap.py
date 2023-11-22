#!/usr/bin/python

"""
Assignment 16: Personal NMAP. Takes IP address, port range and protocol as an 
input and scans all open ports.
"""

import argparse
import ipaddress
from scapy.all import *
from loguru import logger
import concurrent.futures

def tcpsyn_scan(target, port, scan_results):
    logger.info(f"Scanning {target}:{port}/tcp")
    try:
        answers, unanswers = sr(IP(dst=str(target)) / TCP(flags="S", dport=port), verbose=0)
        for answer in answers:
            response_port = answer[1][TCP].sport
            try:
                service = scapy.data.TCP_SERVICES[response_port]
            except:
                service = "unknown"
            response_flag = str(answer[1][TCP].flags)
            if response_flag == "SA":
                result = (str(target), response_port, "open", f"{service}")
                scan_results.append(result)
    except Exception as e:
        logger.error(f"Error during TCP SYN scan on {target}:{port}: {e}")

def udp_scan(target, port, scan_results):
    logger.info(f"Scanning {target}:{port}/udp")
    try:
        answers, unanswers = sr(IP(dst=str(target)) / UDP(dport=port), verbose=0, timeout=2)
        for answer in answers:
            response_port = answer[1][UDP].sport
            try:
                service = scapy.data.UDP_SERVICES[response_port]
            except:
                service = "unknown"
            result = (str(target), response_port, "open", f"{service}")
            scan_results.append(result)
    except Exception as e:
        logger.error(f"Error during UDP scan on {target}:{port}: {e}")

def tcpack_scan(target, port, scan_results):
    logger.info(f"Scanning {target}:{port}/tcp")
    try:
        answers, unanswers = sr(IP(dst=str(target)) / TCP(flags="A", dport=port), verbose=0)
        for answer in answers:
            response_port = answer[1][TCP].sport
            try:
                service = scapy.data.TCP_SERVICES[response_port]
            except:
                service = "unknown"
            result = (str(target), response_port, "open", f"{service}")
            scan_results.append(result)
    except Exception as e:
        logger.error(f"Error during TCP ACK scan on {target}:{port}: {e}")

def print_results(results, protocol):
    print("IP\t\tPORT\tSTATE\tSERVICE")
    for result in results:
        print(f"{result[0]}\t{result[1]}/{protocol}\t{result[2]}\t{result[3]}")

def execute_script(args):
    ports = []

    if "-" in args.p:
        firstport = int(args.p.split("-")[0])
        endport = int(args.p.split("-")[1])
        ports = list(range(firstport, endport + 1))
    else:
        ports.append(int(args.p))

    scan_results = []

    if args.t == "tcp-syn":
        protocol = "tcp"
        target_ports = [(str(ip), port) for ip in ipaddress.IPv4Network(args.target, strict=False) for port in ports]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for target, port in target_ports:
                future = executor.submit(tcpsyn_scan, target, port, scan_results)
                futures.append(future)
            concurrent.futures.wait(futures)

    elif args.t == "udp":
        protocol = "udp"
        target_ports = [(str(ip), port) for ip in ipaddress.IPv4Network(args.target, strict=False) for port in ports]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for target, port in target_ports:
                future = executor.submit(udp_scan, target, port, scan_results)
                futures.append(future)
            concurrent.futures.wait(futures)

    elif args.t == "tcp-ack":
        protocol = "tcp-ack"
        target_ports = [(str(ip), port) for ip in ipaddress.IPv4Network(args.target, strict=False) for port in ports]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for target, port in target_ports:
                future = executor.submit(tcpack_scan, target, port, scan_results)
                futures.append(future)
            concurrent.futures.wait(futures)

    print_results(scan_results, protocol)

def main():
    parser = argparse.ArgumentParser(description="PNMAP - Personal NMAP. -h/--help for usage.")
    parser.add_argument("target", help="Target IP or CIDR block")
    parser.add_argument("-p", help="<port ranges>: Only scan specified ports. Ex: -p 22; -p 1-65535", required=True)
    parser.add_argument("-t", help="Type of protocol to use. Ex: -t tcp-syn; -t tcp-ack; -t udp;", default="tcp-syn")
    args = parser.parse_args()

    logger.info("Starting pnmap..")

    try:
        execute_script(args)
    except Exception as e:
        logger.error(f"Error during script execution: {e}")

if __name__ == "__main__":
    conf.verb = 0
    main()