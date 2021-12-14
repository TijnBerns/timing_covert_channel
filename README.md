# ICMP Based Timing Covert Channel
This repository contains the code and descriptions of an implementation of a covert channel based on the time intervals between ICMP ping packets.

# Requirements
Python3 is required to execute the scripts.

# Usage
The file ``timingSend.py`` acts as a client for encoding and sending packets, while the ``timingReceive.py`` acts as an server for receiving and decoding the packets send by the client.

Use python3 to run both programs. The following arguments can be used:
1. --msg: Set by the client, the string to be send. The string is converted to lowercase, and stripped of any none ASCII values in the range a-z. Defaults to "AttackAtDawn".
2. --base: Set by both the client and server, must be equal. The base used to encode and decode the msg. Valid bases are 2-36. Defaults to base 7.
3. --delay: Set by both the client and server, must be equal. The delay in milliseconds used between the encoded packets, while still taking the 1 second delay into account. Must be greater than 0, defaults to 30.
4. --timeout: Set by server. How long the server will wait and listen for incoming packets in seconds. Defaults to 20.
5. --type: #TODO

Additionally a file called ``IPs.py`` must be created, and contain the string values for `dst` and `src`. These variables specifies the IP of the server and where the pongs must be send to respectively.

# Example
For instance to send the message "example" in base 2, using a delay of 40 ms the client executes:
```
python3 timingSend.py --msg "example" --base 2 --delay 40
```
And the server executes:
```
python3 timingReceive.py --base 2 --delay 40 --timeout 60 --type 1
```

The server would then, if all went right, print the message "example" and statistics about the received packets.
