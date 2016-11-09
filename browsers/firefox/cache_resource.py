# -*- coding: utf-8 -*-
# !/usr/bin/env python

# Python imports
import datetime
import binascii
import struct
import urllib
import os
import re


class CacheResource(object):

    def __init__(self, entries_path=None, url_hash=None):
        """Resource for Firefox cache
        Contains the data pointed by the entry.
        :param entries_path: path to sub folder in cache folder containing entries
        :param url_hash: hash for url (name for file containing the entry)
        """

        self.entries_path = entries_path
        self.url_hash = url_hash
        self.resource_file_path = os.path.join(self.entries_path, self.url_hash)
        self.correct_data_starting_position = None
        self.version = None
        self.fetch_count = None
        self.last_fetched_date = None
        self.last_modified_date = None
        self.frequency = None
        self.expire_date = ""
        self.key_length = None
        self.uri = ""
        self.raw_http_header = ""
        self.header_content_type = ""

        chunk_size_bytes = 262144
        hash_bytes = 4

        # Hash (file name) in cache directory
        if self.url_hash in os.listdir(self.entries_path):
            # Opening cache file
            file_to_open = os.path.join(self.entries_path, self.url_hash)
            with open(file_to_open, "rb") as f_hash:

                # Calculating starting offset for data
                f_hash.seek(-4, 2)
                data_starting_offset = struct.unpack(">I", f_hash.read(4))[0]

                # Number of chunks
                if data_starting_offset % chunk_size_bytes:
                    num_of_chunks = (data_starting_offset/chunk_size_bytes)+1

                else:
                    num_of_chunks = data_starting_offset/chunk_size_bytes

                # Right starting location for data
                self.correct_data_starting_position = data_starting_offset + hash_bytes + (num_of_chunks * 2)
                f_hash.seek(self.correct_data_starting_position)

                # Values
                self.version = struct.unpack(">I", f_hash.read(4))[0]
                self.fetch_count = struct.unpack(">I", f_hash.read(4))[0]

                last_fetched_date_unix = struct.unpack(">I", f_hash.read(4))[0]
                if last_fetched_date_unix != 0:
                    self.last_fetched_date = datetime.datetime.fromtimestamp(last_fetched_date_unix)\
                        .strftime("%A - %d %B %Y - %H:%M:%S")

                else:
                    self.last_fetched_date = datetime.datetime.fromtimestamp(last_fetched_date_unix)\
                        .strftime("%A - %d %B %Y - %H:%M:%S")

                last_modified_date_unix = struct.unpack(">I", f_hash.read(4))[0]
                if last_modified_date_unix != 0:
                    self.last_modified_date = datetime.datetime.fromtimestamp(last_modified_date_unix)\
                        .strftime("%A - %d %B %Y - %H:%M:%S")

                else:
                    self.last_modified_date = datetime.datetime.fromtimestamp(last_modified_date_unix)\
                        .strftime("%A - %d %B %Y - %H:%M:%S")

                self.frequency = struct.unpack(">I", f_hash.read(4))[0]

                expire_date_unix = struct.unpack(">I", f_hash.read(4))[0]
                if expire_date_unix != 0:
                    self.expire_date = datetime.datetime.fromtimestamp(expire_date_unix)\
                        .strftime("%A - %d %B %Y - %H:%M:%S")

                else:
                    self.expire_date = datetime.datetime.fromtimestamp(expire_date_unix)\
                        .strftime("%A - %d %B %Y - %H:%M:%S")

                self.key_length = struct.unpack(">I", f_hash.read(4))[0]

                # Finding header starting location (skipping raw data)
                while True:
                    c = f_hash.read(1)
                    # Stop if char is "h" of "http"
                    if c == "h":
                        f_hash.seek(-1, 1)
                        break

                uri_raw = f_hash.read(self.key_length)
                self.uri = urllib.unquote(uri_raw)

                self.raw_http_header = binascii.b2a_qp(f_hash.read())
                self.header_content_type = get_content_type(self.raw_http_header)


def get_content_type(raw_header=None):
    """Reading a raw header from resource looking for "Content-Type".
    :param raw_header: raw header from resource data
    :return: Content-Type
    """

    pattern = r'(?<=Content-Type:\s)[ -~]+?(?=;?\s)'
    res = re.search(pattern, raw_header)

    if res is not None:
        return res.group(0)
    else:
        return "-"
