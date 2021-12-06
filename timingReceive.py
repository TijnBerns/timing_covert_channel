from scapy.all import *
from abc import ABC, abstractmethod
import time

class Receiver(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.timings = []

    def __handle_packet(self, packet) -> None:
        self.timings.append(time.time())

    def sniff_packet(self) -> None:
        sniff(filter='icmp[icmptype] == icmp-echo',
              prn=self.__handle_packet, store=False, quiet=True, iface="enp3s0", timeout=30)

    def decrypt_message(self, base=7, delay=30) -> List[int]:
        message_intervals_int = []
        for i in range(len(self.timings) - 1):
            time_diff_ms = (self.timings[i+1] - self.timings[i]) * 1000 - 1000
            intervals = delay * round(intervals / delay) 
            intervals = min(int(intervals / delay + (base // 2)), base-1)
            intervals = max(intervals, 0)
            message_intervals_int.append(intervals)
        
        print(message_intervals_int)

        base_7 = []
        for i in range(0, len(message_intervals_int) - 1, 2):
            base_7.append(str(message_intervals_int[i]) + str(message_intervals_int[i+1]))

        message = "".join([chr(int(base, 7) + 97) for base in base_7])

        print(message)

        return message_intervals_int


class SimpleReceiver(Receiver):
    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    sr = SimpleReceiver()
    sr.sniff_packet()
    sr.decrypt_message()