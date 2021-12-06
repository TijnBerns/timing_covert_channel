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

        # Group adjacent numbers based on the base
        # TODO: This depends on which based is used, e.g. in case of base 2 we need to group 26 adjacecent numbers instead of 2
        msg_base = []
        for i in range(0, len(msg_enc) - 1, 2):
            msg_base.append(str(msg_enc[i]) + str(msg_enc[i+1]))

        # Convert to base 10, then to ascii, then to characters
        msg_dec = "".join([chr(int(base, 7) + 97) for base in msg_base])
        return msg_dec


if __name__ == "__main__":
    sr = SimpleReceiver()
    sr.sniff_packet()
    msg = sr.decrypt_message()
    intervals = sr.get_time_diff_ms()

    print(f"REVEIVED MESSAGE:\t{msg}\n")
    # TODO: Add a bunch of statistics of the intervals
    print(f"STATISTICS OF RECEIVED PINGS\n" +
          f"Mean: {np.average(intervals)}\n" + 
          f"Variance: {np.var(intervals)}\n")
