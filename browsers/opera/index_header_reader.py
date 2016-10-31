# -*- coding: utf-8 -*-
# !/usr/bin/env python

# Python imports
import struct

# Project imports
from utilities import utils


def read_index_header(index_file=None):
    """Reading "index" file in Opera cache.
    :param index_file: path to file index
    :return: values read in chrome "index" file header
    """

    with open(index_file, "rb") as f_index:
        # Index file header fields
        signature = struct.unpack("<I", f_index.read(4))[0]
        minor_version = struct.unpack("<h", f_index.read(2))[0]
        major_version = struct.unpack("<h", f_index.read(2))[0]
        number_of_entries = struct.unpack("<I", f_index.read(4))[0]
        stored_data_size = struct.unpack("<I", f_index.read(4))[0]
        last_created_file_f = struct.unpack("<I", f_index.read(4))[0]
        dirty_flag = struct.unpack("<I", f_index.read(4))[0]
        usage_statistics = struct.unpack("<I", f_index.read(4))[0]
        table_size = struct.unpack("<I", f_index.read(4))[0]

        # Skipping fields (previous crash and ongoing test)
        f_index.seek(8, 1)

        # Creation time
        webkit_creation_time = hex(struct.unpack("<Q", f_index.read(8))[0])
        creation_time = utils.webkit_to_unix_timestamp(
            webkit_time=webkit_creation_time,
            source="opera_cache"
        )

    results = {'signature': signature,
               'minor_version': minor_version,
               'major_version': major_version,
               'number_of_entries': number_of_entries,
               'stored_data_size': stored_data_size,
               'last_created_file_f': last_created_file_f,
               'dirty_flag': dirty_flag,
               'usage_statistics': usage_statistics,
               'table_size': table_size,
               'creation_time': creation_time
               }

    return results
