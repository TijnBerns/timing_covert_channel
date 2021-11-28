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
              prn=self.__handle_packet, store=False, quiet=True, iface="enp3s0", timeout=5)

    @abstractmethod
    def decrypt_message(self) -> str:
        pass


class SimpleReceiver(Receiver):
    def decrypt_message(self) -> str:
        for i in range(len(self.timings) - 1):
            time_diff = self.timings[i+1] - self.timings[i]
            print(time_diff * 1000 / 5)
        return ""


if __name__ == "__main__":
    sr = SimpleReceiver()
    sr.sniff_packet()
    sr.decrypt_message()
