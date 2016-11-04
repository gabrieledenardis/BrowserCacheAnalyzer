# -*- coding: utf-8 -*-
# !/usr/bin/env python

# Python imports
import os
import struct
import urllib
import datetime

# Project imports
import cache_resource


class CacheEntry(object):

    def __init__(self, entries_path=None, url_hash=None, frequency=None, expire_date=None, app_id=None, flags=None,
                 file_size=None):

        self.entries_path = entries_path
        self.url_hash = url_hash
        self.entry_file_path = os.path.join(self.entries_path, self.url_hash)
        self.frequency = frequency
        self.expire_date = expire_date
        self.app_id = app_id
        self.flags = flags
        self.file_size = file_size

        self.resource_uri = None

        # Resource

        self.cache_resource_instance = cache_resource.CacheResource(
            entries_path=self.entries_path,
            url_hash=self.url_hash
        )

        self.resource_uri = self.cache_resource_instance.uri
        self.resource_http_header = self.cache_resource_instance.http_header