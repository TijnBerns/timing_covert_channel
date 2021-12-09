from scapy.all import Ether, IP, ICMP, raw, conf
from abc import ABC, abstractmethod
from typing import List
import numpy as np
import time
import IPs

class MessageConverter(ABC):
    @abstractmethod
    def message_to_intervals(self, message: str) -> List[int]:
        pass

class SimpleMessageConverter(MessageConverter):
    def message_to_intervals(self, msg: str, base: int, delay: int = 20) -> List[int]:
        """Converts a message into a set of time intervals. 

        Args:
            message (String): The message that is converted to intervals.
        Returns:
            List: List of integers representing the intervals in seconds.
        """
        max_len = len(np.base_repr(26, base=base))
        
        # Convert to lower and remove whitespace
        msg = np.array(list(msg.lower().replace(" ", "")))
        
        # Convert to integers
        msg_int = msg.view(np.int32) - 97
        
        # Convert to specified base
        msg_base = np.array([np.base_repr(c, base=base) for c in msg_int])  
        
        # Prepend 0's to ensure equal lengths
        msg_base = np.array([((max_len - len(c)) * '0') + c for c in msg_base])
        
        # Convert strings to time intervals 
        intervals_str = np.array([list(s) for s in msg_base]).flatten() 
        intervals_int = intervals_str.astype(np.int)

        print(intervals_int)

        # In case of an even base, evenly distribute the intervals around 1.
        if (base % 2 == 1):
            return ((intervals_int - (base // 2)) * delay) / 1000 + 1
        else:
            return ((intervals_int - (base // 2)) * delay) / 1000 + 1 + delay / 2000

class StreamMessageConverter(MessageConverter):
    def message_to_intervals(self, message: str) -> List[int]:
        raise NotImplementedError

class Sender(object):
    def __init__(self, message_converter: MessageConverter) -> None:
        super().__init__()
        self.message_converter = message_converter

    def send_message(self, message: str, base: int) -> None:
        """Sends ping messages to receiver at corresponding time intervals.
        Args:
            message (String): The plaintext message that is send to the receiver.
            receiver (String): The IP-address of the receiver.
        """

        # Prepare both the raw ping message and a socket.
        packet = Ether() / IP(dst=IPs.dst, src=IPs.src) / ICMP()
        frame = bytearray(raw(packet))
        s = conf.L2socket()
        # Send pings at message intervals.
        intervals = self.message_converter.message_to_intervals(message, base)
        s.send(frame)
        for interval in intervals:
            time.sleep(interval)
            s.send(frame)
        s.close()
        return intervals

if __name__ == "__main__":
    smc = SimpleMessageConverter()
    simple_sender = Sender(smc)
    message = "testberichtditis"
    intervals = simple_sender.send_message(message, 2)
    print(intervals)  # Print for debugging.
