# -*- coding: utf-8 -*-
# !/usr/bin/env python

# Python imports
import binascii
import struct
import urllib
import re


class CacheResource(object):

    def __init__(self, resource_file=None, file_type=None, block_dimension=None, block_number=None,
                 resource_size=None, is_http_header=None):

        """Resource for chrome cache.
        Contains the data pointed by the entry.
        :param resource_file: file containing the resource
        :param file_type: data block file data_# or separate file f_######
        :param block_dimension: dimension of the block within the file (depending on data_# file)
        :param block_number: number of the block within the file
        :param resource_size: dimension of the resource
        :param is_http_header: True, False or Unknown if the resource is an HTTP header
        """

        # Data from entry address
        self.resource_file = resource_file
        self.file_type = file_type
        self.block_dimension = block_dimension
        self.block_number = block_number
        self.resource_size = resource_size
        self.is_http_header = is_http_header

        # Content of resource
        self.resource_data = ""

        # Offset for the resource
        data_header_dimension = 8192

        # Not a separate file
        if self.file_type != "000":
            with open(self.resource_file, "rb") as f_resource:
                # Resource offset
                f_resource.seek(data_header_dimension + (self.block_dimension * self.block_number))

                # Reading resource
                for chars in range(self.resource_size):
                    self.resource_data += binascii.b2a_qp(struct.unpack("c", f_resource.read(1))[0])

            # Resource is HTTP Header
            if self.is_http_header is True:
                # self.resource_data = http_header_values(raw_header=self.resource_data)
               print self.resource_data

            # Resource is not HTTP header
            else:
                self.resource_data = urllib.unquote(self.resource_data.replace("=2E", ".").replace("=20", " ")
                                                    .replace("=3D", "="))


def http_header_values(raw_header=None):
    """Reading a raw header from resource and separating tag and value.
    :param raw_header: raw header from resource data
    :return: HTTP header tag and values
    """

    headers_dict = {}

    # All string except before HTTP and after =00=00
    matched = re.search(r"(?<=(HTTP))(.+?)(?==00=00)", raw_header)

    if matched is not None:
        # =00 added as string termination to match last string value
        source = "".join(matched.groups()) + "=00"

        # HTTP response
        http = re.match(r"^(.+?)(?==00)", source)
        http = "".join(http.groups()).split("=20")

        # Keys and replacement for not standard percent-encoding escape sequences found in http header
        keys = re.findall(r"(?<==00).+?(?=:)", source)
        keys.append(http[0].replace("=2E", "."))

        # Values and replacement for not standard percent-encoding escape sequences found in http header
        values = map(lambda val: urllib.unquote(val.replace("=2E", ".").replace("=20", " ").replace("=3D", "=")
                                                .strip()), re.findall(r"(?<=:).+?(?==00)", source))
        values.append(" ".join(http[1:]))

        # Updating dictionary
        headers_dict.update(dict(zip(keys, values)))

    return headers_dict
