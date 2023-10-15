#!/usr/bin/env python3

"""
    Burst sender
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
import logging
import socket
import struct
import time


argparser = ArgumentParser(prog='BDS - Burst Data Sender',
                           description='Send data bursts.',
                           )

argparser.add_argument('--ip',
                       help='Target IP.',
                       type=str,
                       metavar='IPv4 Addr.',
                       default='127.0.0.1',
                       )

argparser.add_argument('-p',
                       '--port',
                       help='Target port.',
                       type=int,
                       metavar='PORT',
                       default='5005',
                       )

argparser.add_argument('-b',
                       '--burst-length',
                       help='Length of a single burst.',
                       type=int,
                       metavar='INT',
                       default=53,
                       )

argparser.add_argument('-n',
                       '--bursts-to-send',
                       help='Amount of bursts to send before exiting.',
                       type=int,
                       metavar='INT',
                       default=-1,
                       )

argparser.add_argument('-i',
                       '--interval',
                       help='Time interval between bursts in microseconds.',
                       type=int,
                       metavar='INT',
                       default=16666,
                       )

argparser.add_argument('-s',
                       '--packet-size',
                       help='Packet size in bytes.',
                       type=int,
                       metavar='INT',
                       default=532,
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


# UDP_IP = "192.168.69.176"
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
protocol_id = b"BurstTester 0.01"
padding_length = args.packet_size - len(protocol_id) - 4 * 6
if padding_length < 0:
    print('Minimum packet size is {len(protocol_id) + 4 * 6}')
    padding_length = 0
padding = b"." * padding_length

# data_raw = protocol_id + data + padding
print("UDP target IP: %s" % args.ip)
print("UDP target port: %s" % args.port)
# print(f"Packet length: {len(data_raw)}")


sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

delta_min = 10000000000000
delta_max = 0
debug_bursts_sent = 0
ignore_delta = 2

data = struct.pack("<LLLLLL", 0, 0, 0, args.burst_length, args.interval, args.packet_size)
data_raw = protocol_id + data + padding

desired_time = time.time()
old_time = time.time()
old_time_debug = time.time()
debug_time = time.time() + args.debug_interval
packet_number_total = 0
burst_index = 0

print()

while burst_index != args.bursts_to_send:
    new_time_debug = time.time()
    delta_time_debug = new_time_debug - old_time_debug
    if delta_time_debug < delta_min:
        delta_min = delta_time_debug
    if delta_time_debug > delta_max:
        delta_max = delta_time_debug
    old_time_debug = new_time_debug
    for packet_index in range(args.burst_length):
        packet_number_total += 1
        data = struct.pack("<LLLLLL", packet_index, burst_index, packet_number_total, args.burst_length, args.interval, args.packet_size)
        data_raw = protocol_id + data + padding
        sock.sendto(data_raw, (UDP_IP, UDP_PORT))
    if time.time() > debug_time:
        print(f'Bursts = {debug_bursts_sent}, delta_min = {int(delta_min * 1_000_000)}, delta_max = {int(delta_max * 1_000_000)}, total packets {packet_number_total}, burst_index {burst_index}')
        delta_min = 10000000000000
        delta_max = 0
        debug_bursts_sent = 0
        debug_time += args.debug_interval
    burst_index += 1
    debug_bursts_sent += 1
    desired_time = desired_time + args.interval / 1_000_000
    new_time = time.time()
    sleep_this_long = desired_time - new_time
    old_time = new_time
    # print(f"Time delta = {time_delta * 1000000} us")
    if sleep_this_long > 0:
        time.sleep(sleep_this_long)
    


