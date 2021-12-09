from scapy.all import *
from abc import ABC, abstractmethod
import time
import numpy as np


class Receiver(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.timings = []

    def sniff_packet(self, timeout: int = 15) -> None:
        """Sniffs ping packets for 'timeout' seconds

        Args:
            timeout (int, optional): Time the network is sniffed (s). Defaults to 15.
        """
        sniff(filter='icmp[icmptype] == icmp-echo',
              prn=self.__handle_packet, store=False, quiet=True, iface="enp3s0", timeout=timeout)

    def get_time_diff_ms(self) -> np.array(float):
        """Computes the timing difference between each pair of sequentially received ping packets

        Returns:
            np.array(float): Numpy array containing the time difference between all received ping packets
        """
        message_intervals_ms = []
        for i in range(len(self.timings) - 1):
            message_intervals_ms.append(
                (self.timings[i+1] - self.timings[i]) * 1000)

        return np.array(message_intervals_ms)

    def __handle_packet(self, packet) -> None:
        self.timings.append(time.time())

    @abstractmethod
    def decrypt_message(self, base=20, delay=30) -> str:
        pass


class SimpleReceiver(Receiver):
    def __init__(self) -> None:
        super().__init__()

    def decrypt_message(self, base: int = 7, delay: int = 50) -> str:
        # Get the intervals between pings in ms
        msg_enc = self.get_time_diff_ms() - 1000

        # Ronud intervals based on delay
        msg_enc = delay * np.round(msg_enc / delay)

        # Convert to different base
        msg_enc = msg_enc / delay + (base // 2)

        # Clip to valid range
        msg_enc = np.clip(msg_enc, 0, base-1).astype('int')

        # Convert to array of characters
        msg_enc_str = msg_enc.astype(str)

        # Compute the max length of a single character in given base
        max_len = len(np.base_repr(26, base=base))

        # Take slices of msg_enc_str with length of max_len
        msg_base = ["".join(msg_enc_str[i:max_len+i])
                    for i in range(0, len(msg_enc_str) - 1, max_len)]

        # Convert to base 10, then to ascii, then to characters
        msg_dec = "".join([chr(int(msg, base) + 97) for msg in msg_base])
        return msg_dec


if __name__ == "__main__":
    sr = SimpleReceiver()
    sr.sniff_packet(60)
    msg = sr.decrypt_message()
    intervals = sr.get_time_diff_ms()

    if len(intervals) > 0:
        print(f"REVEIVED MESSAGE: {msg}\n")

        print(f"STATISTICS OF RECEIVED PINGS\n" +
              f"Count: {len(intervals)}\n" +
              f"Total time: {np.sum(intervals)}\n" +
              f"Min interval: {np.min(intervals)}\n" +
              f"Max interval: {np.max(intervals)}\n"
              f"Mean: {np.average(intervals)}\n" +
              f"Variance: {np.var(intervals)}\n")
