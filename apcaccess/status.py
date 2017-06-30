"""
apcaccess.status

Contains functions to extract and parse the status of the apcupsd NIS.
"""

from __future__ import print_function

import socket
from collections import OrderedDict


CMD_STATUS = "\x00\x06status".encode()
EOF = "  \n\x00\x00"
SEP = ":"
BUFFER_SIZE = 1024
ALL_UNITS = (
    "Minutes",
    "Seconds",
    "Percent",
    "Volts",
    "Watts",
    "Amps",
    "Hz",
    "C",
    "VA",
    "Percent Load Capacity"
)


def get(host="localhost", port=3551, timeout=30):
    """
    Connect to the APCUPSd NIS and request its status.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    sock.connect((host, port))
    sock.send(CMD_STATUS)
    buffr = ""
    while not buffr.endswith(EOF):
        buffr += sock.recv(BUFFER_SIZE).decode()
    sock.close()
    return buffr


def split(raw_status):
    """
    Split the output from get_status() into lines, removing the length and
    newline chars.
    """
    # Remove the EOF string, split status on the line endings (\x00), strip the
    # length byte and newline chars off the beginning and end respectively.
    return [x[1:-1] for x in raw_status[:-len(EOF)].split("\x00") if x]


def parse(raw_status, strip_units=False):
    """
    Split the output from get_status() into lines, clean it up and return it as
    an OrderedDict.
    """
    lines = split(raw_status)
    if strip_units:
        lines = strip_units_from_lines(lines)
    # Split each line on the SEP character, strip extraneous whitespace and
    # create an OrderedDict out of the keys/values.
    return OrderedDict([[x.strip() for x in x.split(SEP, 1)] for x in lines])


def strip_units_from_lines(lines):
    """
    Removes all units from the ends of the lines.
    """
    for line in lines:
        for unit in ALL_UNITS:
            if line.endswith(" %s" % unit):
                line = line[:-1-len(unit)]
        yield line


def print_status(raw_status, strip_units=False):
    """
    Print the status to stdout in the same format as the original apcaccess.
    """
    lines = split(raw_status)
    if strip_units:
        lines = strip_units_from_lines(lines)
    for line in lines:
        print(line)
