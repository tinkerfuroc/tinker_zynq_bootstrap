#!/usr/bin/env python

import mmap
import argparse
import struct
import sys


class PWMotorController: 
    FREQ = 100000000
    RATE = 50
    def __init__(self, dev_name):
        self.io_file = open(dev_name, 'rb+')
        self.reg_map = mmap.mmap(self.io_file.fileno(), 8)
        self.reg_map[0:4] = struct.pack('<I', Loader.FREQ / Loader.RATE)

    def set_duty_rate(self, duty_rate):
        duty_width = int(duty_rate * Loader.FREQ / Loader.RATE)
        self.reg_map[4:8] = struct.pack('<I', duty_width)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dev', required=True)
    args = parser.parse_args()
    controller = PWMotorController(args.dev)
    for l in sys.stdin():
        controller.set_duty_rate(float(l))
    
