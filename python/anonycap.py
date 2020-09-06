#!/usr/bin/env python3

from scapy.all import *
import os
import sys


ETHER_COUNT = 0
IP_COUNT = 0


def next_ether():
    global ETHER_COUNT
    ether_id = ETHER_COUNT
    ETHER_COUNT += 1
    ether_str = '%012x' % (ether_id,)
    return ':'.join([ether_str[i:i+2] for i in range(0, len(ether_str), 2)])


def next_ip():
    global IP_COUNT
    ip_id = IP_COUNT
    IP_COUNT += 1
    return '.'.join([str(o) for o in [ip_id >> 24, (ip_id >> 16) & 0xFF, (ip_id >> 8) & 0xFF, ip_id & 0xFF]])


ETHER_MAP = defaultdict(next_ether)
IP_MAP = defaultdict(next_ip)
START_TIME = None


def process_pkt(pkt):
    global ETHER_MAP
    global IP_MAP
    global START_TIME

    if pkt.haslayer(TCP):
        if not START_TIME:
            START_TIME = pkt.time
        pkt.time -= START_TIME
        pkt_ether = pkt.getlayer(Ether)
        pkt_ether.dst = ETHER_MAP[pkt_ether.dst]
        pkt_ether.src = ETHER_MAP[pkt_ether.src]
        pkt_ip = pkt.getlayer(IP)
        pkt_ip.dst = IP_MAP[pkt_ip.dst]
        pkt_ip.src = IP_MAP[pkt_ip.src]
        pkt_tcp = pkt.getlayer(TCP)
        pkt_tcp.remove_payload()
    return pkt


def main():
    global SNIFF_IFACE
    
    if len(sys.argv) < 3:
        print("usage: {} <in.pcap> <out.pcap>".format(sys.argv[0]))
        sys.exit(1)

    pcap_in = PcapReader(sys.argv[1])
    if not pcap_in:
        print("{}: failed to open PcapReader for {}".format(sys.argv[0], sys.argv[1]))
        sys.exit(1)

    pcap_out = PcapWriter(sys.argv[2])
    if not pcap_out:
        print("{}: failed to open PcapWriter for {}".format(sys.argv[0], sys.argv[2]))
        sys.exit(1)

    pkt = pcap_in.read_packet()
    while pkt:
        pcap_out.write(process_pkt(pkt))
        pkt = pcap_in.read_packet()

    pcap_in.close()
    pcap_out.close()


if __name__ == '__main__':
    main()

