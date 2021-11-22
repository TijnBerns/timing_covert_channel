from scapy.all import *
from abc import ABC, abstractmethod
import datetime


class Receiver(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.timings = []

    def __handle_packet(self, packet) -> None:
        self.timings.append(datetime.datetime.now())

    def sniff_packet(self) -> None:
        sniff(filter='icmp[icmptype] == icmp-echo',
              prn=self.__handle_packet, store=0, timeout=10)

    @abstractmethod
    def decrypt_message(self) -> str:
        pass


class SimpleReceiver(Receiver):
    def decrypt_message(self) -> str:
        for i in range(len(self.timings) - 1):
            time_diff = self.timings[i+1] - self.timings[i]
            print(time_diff.total_seconds() * 1000 / 100)
        return ""


if __name__ == "__main__":
    sr = SimpleReceiver()
    sr.sniff_packet
    sr.decrypt_message
