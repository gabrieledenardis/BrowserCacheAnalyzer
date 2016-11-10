# -*- coding: utf-8 -*-
# !/usr/bin/env python

# Python imports
import struct


def read_data_header(data_to_open=None):
    """Reading "data_#" files in Opera cache.
    :param data_to_open: path to file index
    :return: values read in Opera "data_#" file header
    """

    with open(data_to_open, "rb") as f_data:
        # Data_header_fields
        signature = format(struct.unpack("<I", f_data.read(4))[0], "X")
        minor_version = struct.unpack("<h", f_data.read(2))[0]
        major_version = struct.unpack("<h", f_data.read(2))[0]
        file_number = struct.unpack("<h", f_data.read(2))[0]
        next_file_number = struct.unpack("<h", f_data.read(2))[0]
        block_size = struct.unpack("<I", f_data.read(4))[0]
        num_entries = struct.unpack("<I", f_data.read(4))[0]
        max_num_entries = struct.unpack("<I", f_data.read(4))[0]

        results = {'signature': signature,
                   'minor_version': minor_version,
                   'major_version': major_version,
                   'file_number': file_number,
                   'next_file_number': next_file_number,
                   'block_size': block_size,
                   'num_entries': num_entries,
                   'max_num_entries': max_num_entries
                   }

        return results
