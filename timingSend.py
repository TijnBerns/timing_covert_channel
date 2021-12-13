from scapy.all import Ether, IP, ICMP, raw, conf
from abc import ABC
from typing import List
import numpy as np
import time
import IPs
from args import parser

class MessageConverter(ABC):
    def message_to_intervals(self, msg: str, base: int) -> List[int]:
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
        return intervals_str.astype(int)


class SimpleMessageConverter(MessageConverter):
    def message_to_intervals(self, msg: str, base: int, delay: int) -> List[int]:
        """Converts a message into a set of time intervals.
        Adds a standard interval of 1 sec, and centers computed intervals around 1 sec.

        Args:
            message (String): The message that is converted to intervals.
        Returns:
            List: List of integers representing the intervals in seconds.
        """
        intervals_int = super().message_to_intervals(msg, base)
        # In case of an even base, evenly distribute the intervals around 1.
        if (base % 2 == 1):
            return ((intervals_int - (base // 2)) * delay) / 1000 + 1
        else:
            return ((intervals_int - (base // 2)) * delay) / 1000 + 1 + delay / 2000

class NoIntervalMessageConverter(MessageConverter):
    def message_to_intervals(self, msg: str, base: int, delay: int) -> List[int]:
        """Converts a message into a set of time intervals.
        Adds a standard interval of 1 ms * delay (without centering).

        Args:
            message (String): The message that is converted to intervals.
        Returns:
            List: List of integers representing the intervals in seconds.
        """
        intervals_int = super().message_to_intervals(msg, base)
        return (intervals_int + 1) * delay / 1000

class Sender(object):
    def __init__(self, message_converter: MessageConverter) -> None:
        super().__init__()
        self.message_converter = message_converter

    def send_message(self, message: str, base: int, delay: int) -> None:
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
        intervals = self.message_converter.message_to_intervals(
            message, base, delay)
        s.send(frame)
        for interval in intervals:
            time.sleep(interval)
            s.send(frame)
        s.close()
        return intervals

if __name__ == "__main__":
    args = parser()

    # Initialize sender
    if args.type == 1:
        mc = SimpleMessageConverter()
    elif args.type == 2:
        mc = NoIntervalMessageConverter()
    else:
        raise NotImplementedError

    # Send message
    simple_sender = Sender(mc)
    message = args.msg
    intervals = simple_sender.send_message(message, args.base, args.delay)

    # Print info
    print(f"Message: {message}\n" +
          f"Ping at intervals (ms): {intervals * 1000}")
