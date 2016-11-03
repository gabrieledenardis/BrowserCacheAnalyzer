# -*- coding: utf-8 -*-
# !/usr/bin/env python

# Python imports
import struct

# Project imports
from utilities import utils


def read_index_header(index_file=None):
    """Reading "index" file in chrome cache.
    :param index_file: path to file index
    :return: values read in chrome "index" file header
    """

    with open(index_file, "rb") as f_index:
        # Header
        version = struct.unpack(">I", f_index.read(4))[0]
        last_modified = struct.unpack(">I", f_index.read(4))[0]

        dirty_flag = struct.unpack(">I", f_index.read(4))[0]

    results = {'version': version,
               'last_modified_time': last_modified,
               'dirty_flag': dirty_flag
               }

    return results
