from scapy.all import *
import datetime

timings=[]

def handle_packet(packet):
    timings.append(datetime.datetime.now())

sniff(filter='icmp[icmptype] == icmp-echo', prn=handle_packet, store=0, timeout=10)

for i in range(len(timings) - 1):
    time_diff = timings[i+1] - timings[i]
    print(time_diff.total_seconds() * 1000 / 100)
