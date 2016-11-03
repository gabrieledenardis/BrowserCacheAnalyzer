# -*- coding: utf-8 -*-
# !/usr/bin/env python

# Python imports
import os
import struct
import urllib
import datetime
import re
import binascii


class CacheResource(object):

    def __init__(self, entries_path=None, url_hash=None):

        self.entries_path = entries_path
        self.url_hash = url_hash
        self.version = None
        self.fetch_count = None
        self.last_fetched_date = None
        self.last_modified_date = None
        self.frequency = None
        self.expire_date = ""
        self.key_length = None
        self.uri = ""

        chunk_size_bytes = 262144
        num_of_chunks = 0
        hash_bytes = 4

        # Hash (file name) in cache directory
        if self.url_hash in os.listdir(self.entries_path):

            # Opening cache file
            file_to_open = os.path.join(self.entries_path, self.url_hash)
            with open(file_to_open, "rb") as f_hash:

                # Start offset for data
                f_hash.seek(-4, 2)
                data_start_offset = struct.unpack(">I", f_hash.read(4))[0]

                # Number of chunks
                if data_start_offset % chunk_size_bytes:
                    num_of_chunks = (data_start_offset/chunk_size_bytes)+1
                else:
                    num_of_chunks = data_start_offset/chunk_size_bytes

                # Right start location for data
                f_hash.seek(data_start_offset + hash_bytes + (num_of_chunks * 2))

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
                uri_raw = f_hash.read(self.key_length)
                start = uri_raw.index("h")
                uri_raw = uri_raw[start:]
                self.uri = urllib.unquote(uri_raw)

                raw_http_header = binascii.b2a_qp(f_hash.read())
                self.http_header = http_header_values(raw_http_header)


def http_header_values(raw_header=None):
    """Reading a raw header from resource and separating tag and value.
    :param raw_header: raw header from resource data
    :return: HTTP header tag and values
    """

    headers_dict = {}

    pattern_keys = r'(Server|Date|Content-Type|Content-Length|Connection|Keep-Alive|Last-Modified|Etag|Vary|Sid|' \
                   r'Expires|Cache-Control|Accept-Ranges|P3P|Transfer-Encoding|Access-Control-Allow-Origin|' \
                   r'Access-Control-Allow-Credentials|Access-Control-Allow-Methods|Access-Control-Max-Age|' \
                   r'Strict-Transport-Security|Content-Encoding|X-Cache-Status)'

    pattern_values = r'(?<=:\s)([A-Za-z0-9\/\-\=\"]+|[A-Za-z]{3},\s[\d]{2}\s[A-Za-z]{3}\s[\d]{4}\s[\d]{2}:' \
                     r'[\d]{2}:[\d]{2}\sGMT)(?=\s)'

    keys = re.findall(pattern_keys, raw_header)
    values = re.findall(pattern_values, raw_header)

    # Updating dictionary
    headers_dict.update(dict(zip(keys, values)))

    return headers_dict