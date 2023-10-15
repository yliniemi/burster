#!/usr/bin/env python3

"""
    Burst receiver
    Copyright (C) 2023 Antti Yliniemi
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


from argparse import ArgumentParser
from collections import namedtuple
from sys import exit
import socket
import struct
import time


argparser = ArgumentParser(prog='BDR - Burst Data Receiver',
                           description='Receive data bursts.',
                           )

argparser.add_argument('-p',
                       '--port',
                       help='Target port.',
                       type=int,
                       metavar='PORT',
                       default='5005',
                       )

argparser.add_argument('-d',
                       '--debug-interval',
                       help='Interval for debug logging in seconds.',
                       type=int,
                       metavar='INT',
                       default=10,
                       )

args = argparser.parse_args()

print(args)


UDP_IP = "0.0.0.0"
# UDP_IP = "127.0.0.1"
# UDP_IP = "192.168.69.101"


sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, args.port))


Message = namedtuple('Message', 'packet_index burst_index packet_number_total burst_length interval packet_size')
new_message = Message(0, -1, 0, 0, 0, 0)
old_message = new_message
packets_caugth_total = 0
packets_caugth_in_burst = 0
late_packets = 0
intact_bursts_caugth = 0
incomplete_bursts_number = 0
debug_time = time.time() + args.debug_interval

print()

while True:
    data_raw, addr = sock.recvfrom(10240) # buffer size is 1024 bytes
    if data_raw.startswith(b"BurstTester 0.01"):
        # print(f"received message length: {len(data_raw)}")
        try:
            new_message = Message(*struct.unpack("<LLLLLL", data_raw[16:40]))
            # print(message)
            if new_message.burst_index < old_message.burst_index:
                late_packets += 1
            elif new_message.burst_index == old_message.burst_index:
                packets_caugth_total += 1
                old_packets_caugth_total = packets_caugth_total
                packets_caugth_in_burst += 1
                old_message = new_message
            else:  # new_message.burst_index > old_message.burst_index:
                if time.time() > debug_time:
                    debug_time += args.debug_interval
                    print(f'packets caugth/late/total = {old_packets_caugth_total}/{late_packets}/{old_message.packet_number_total}, bursts intact/incomplete/total = {intact_bursts_caugth}/{incomplete_bursts_number}/{old_message.burst_index + 1}, packet length = {len(data_raw)}')
                if packets_caugth_in_burst < old_message.burst_length:
                    incomplete_bursts_number += 1
                else:
                    intact_bursts_caugth += 1
                packets_caugth_in_burst = 1
                packets_caugth_total += 1
                old_packets_caugth_total = packets_caugth_total
                old_message = new_message
            
        except struct.error as e:
            print(e)
    else:
        print(f"Invalid protocol. Packet length = {len(data_raw)}")



