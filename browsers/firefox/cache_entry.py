# -*- coding: utf-8 -*-
# !/usr/bin/env python

# Python imports
import os

# Project imports
import cache_resource


class CacheEntry(object):

    def __init__(self, entries_path=None, url_hash=None, frequency=None, expire_date=None, app_id=None, flags=None,
                 file_size=None):
        """Complete entity stored in cache.
        :param entries_path: path to sub folder in Firefox folder containing entries
        :param url_hash: hash for url (name of the entry)
        :param frequency:
        :param expire_date:
        :param app_id:
        :param flags:
        :param file_size: Dimension for the entry
        """

        self.entries_path = entries_path
        self.url_hash = url_hash
        self.entry_file_path = os.path.join(self.entries_path, self.url_hash)
        self.frequency = frequency
        self.expire_date = expire_date
        self.app_id = app_id
        self.flags = flags
        self.file_size = file_size

        # Values for the resource pointed by the entry
        self.resource_uri = ""
        self.resource_http_header = ""
        self.resource_content_type = ""

        # Resource
        self.cache_resource_instance = cache_resource.CacheResource(
            entries_path=self.entries_path,
            url_hash=self.url_hash
        )

        # Values from resource
        self.resource_uri = self.cache_resource_instance.uri
        self.resource_http_header = self.cache_resource_instance.raw_http_header
        self.resource_content_type = self.cache_resource_instance.header_content_type
