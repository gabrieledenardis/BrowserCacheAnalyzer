# -*- coding: utf-8 -*-
# !/usr/bin/env python

# PyQt4 imports
from PyQt4 import QtCore

# Python imports
from threading import Event
import os
import struct
import datetime
import time

# Project imports
import cache_entry


class FirefoxAnalyzer(QtCore.QObject):
    """
    Analyzer for Firefox cache.
    """

    # Signals
    signal_update_table_preview = QtCore.pyqtSignal(int, int, str, str, str)
    signal_finished = QtCore.pyqtSignal()

    def __init__(self, parent=None, input_path=None):
        super(FirefoxAnalyzer, self).__init__(parent)

        # Signal from "button_stop_analysis"
        self.signal_stop = Event()
        # Thread stopped by user
        self.stopped_by_user = False
        # Analysis running
        self.worker_is_running = True
        # Input path to analyze
        self.input_path = input_path
        # List of all cache entries found
        self.list_cache_entries = []

    def analyze_cache(self):

        index_file = os.path.join(self.input_path, "index")
        index_file_dimension = os.path.getsize(index_file)

        entries_path = os.path.join(self.input_path, "entries")

        header_dimension = 12
        record_dimension = 36
        tot_elem = (index_file_dimension-header_dimension)/record_dimension

        with open(index_file, "rb") as f_index:

            f_index.seek(header_dimension)

            # Cache file records
            while True:

                record = f_index.read(record_dimension)
                if not record:
                    break

                if self.signal_stop.is_set():
                    self.stopped_by_user = True
                    self.worker_is_running = False
                    break

                current_pos = f_index.tell()

                if (index_file_dimension - current_pos) % record_dimension != 0:

                    url_hash = ""
                    for i in range(0, 20, 4):
                        start = i
                        stop = i + 4
                        url_hash += format(struct.unpack(">I", record[start:stop])[0], "X")

                    frequency = struct.unpack(">I", record[20:24])[0]

                    expire_date_unix = struct.unpack(">I", record[24:28])[0]
                    expire_date = datetime.datetime.fromtimestamp(expire_date_unix).strftime("%A - %d %B %Y - %H:%M:%S")

                    app_id = struct.unpack(">I", record[28:32])[0]
                    flags = ord(struct.unpack(">c", record[32:33])[0])
                    file_size = struct.unpack(">I", "\0" + record[33:])[0]

                    cache_entry_instance = cache_entry.CacheEntry(
                        entries_path=entries_path,
                        url_hash=url_hash,
                        frequency=frequency,
                        expire_date=expire_date,
                        app_id=app_id,
                        flags=flags,
                        file_size=file_size
                    )

                    time.sleep(0.01)

                    resource_uri = cache_entry_instance.resource_uri
                    if resource_uri:
                        # start = resource_uri.index("h")
                        # resource_uri = resource_uri[start:]
                        self.signal_update_table_preview.emit(
                            len(self.list_cache_entries),
                            tot_elem,
                            cache_entry_instance.url_hash,
                            resource_uri,
                            cache_entry_instance.expire_date
                        )
                    else:
                        self.signal_update_table_preview.emit(
                            len(self.list_cache_entries),
                            tot_elem,
                            cache_entry_instance.url_hash,
                            "-",
                            cache_entry_instance.expire_date
                        )

                    self.list_cache_entries.append(cache_entry_instance)

        # Analysis terminated
        self.worker_is_running = False
        self.signal_finished.emit()
        print len (self.list_cache_entries)
