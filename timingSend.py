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
    def message_to_intervals(self, message: str) -> List[int]:
        """Converts a message into a set of time intervals. 
        Conversion is done by taking the base 8 ascii value of each character in the message.
        Args:
            message (String): The message that is converted to intervals.
        Returns:
            List: List of integers representing the intervals.
        """
        message_base_8 = [oct(ord(c)) for c in message]
        message_intervals_str = np.array(
            [list(s[2:]) for s in message_base_8]).flatten()
        hidden_message_intervals_int = [int(c) for c in message_intervals_str]
        return hidden_message_intervals_int


class StreamMessageConverter(MessageConverter):
    def message_to_intervals(self, message: str) -> List[int]:
        raise NotImplementedError

class Sender(object):
    def __init__(self, message_converter: MessageConverter) -> None:
        super().__init__()
        self.message_converter = message_converter

    def send_message(self, message: str) -> None:
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
        intervals = self.message_converter.message_to_intervals(message)
        for interval in intervals:
            time.sleep((interval*5) / 1000)
            s.send(frame)
        return intervals


if __name__ == "__main__":
    smc = SimpleMessageConverter()
    simple_sender = Sender(smc)
    message = "AttackAtDawn"
    intervals = simple_sender.send_message(message)
    print(intervals) # Print for debugging.
