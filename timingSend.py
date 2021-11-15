import numpy as np
import time
from scapy.all import *
import os

hidden_message_str = "TestString"
hidden_message_base_8 = [oct(ord(c)) for c in hidden_message_str]
hidden_message_intervals_str = np.array([list(s[2:]) for s in hidden_message_base_8]).flatten()
hidden_message_intervals_int = [int(c) for c in hidden_message_intervals_str]
print(hidden_message_intervals_int)

# packet =  Ether() / IP(dst='www.google.com') / ICMP() / "XXXXXXXXXXX"
# sendp(packet, iface=interface)
# Warmup
os.system("ping -c 1 www.google.com")
os.system("ping -c 1 www.google.com")
os.system("ping -c 1 www.google.com")
os.system("ping -c 1 www.google.com")
os.system("ping -c 1 www.google.com")

for interval in hidden_message_intervals_int:
    time.sleep((interval*100) / 1000)
    os.system("ping -c 1 www.google.com")

