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
    def message_to_intervals(self, message: str, base: int, delay: int = 50) -> List[int]:
        """Converts a message into a set of time intervals. 
        Conversion is done by taking the base 8 ascii value of each character in the message.
        Args:
            message (String): The message that is converted to intervals.
        Returns:
            List: List of integers representing the intervals.
        """
        message = np.array(list(message.lower().replace(" ", ""))) # Convert to lower and remove whitespace
        message_int = message.view(np.int32) # Convert to ascii
        message_int = message_int - 97 # Subtract 97 from each ascii value
        message_base_7 = np.array([np.base_repr(c, base=base) for c in message_int]) # Convert to base 7
        message_base_7 = np.array(['0' + c if len(c) == 1 else c for c in message_base_7]) # Prepend 0 in case of len 1
        message_intervals_str = np.array([list(s) for s in message_base_7]).flatten() # Flatten array
        message_intervals_int = message_intervals_str.astype(np.int) # Convert to int

        return ((message_intervals_int - (base // 2)) * delay) / 1000 + 1


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
    message = "test"
    intervals = simple_sender.send_message(message, 7)
    print(intervals) # Print for debugging.
