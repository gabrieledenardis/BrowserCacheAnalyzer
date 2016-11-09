# -*- coding: utf-8 -*-
# !/usr/bin/env python

# PyQt4 imports
from PyQt4 import QtCore

# Python imports
from threading import Event
import datetime
import struct
import time
import os

# Project imports
import cache_entry


class FirefoxAnalyzer(QtCore.QObject):
    """Analyzer for Firefox cache.
    """

    # Signals
    signal_update_table_preview = QtCore.pyqtSignal(int, int, str, str, str, str)
    signal_finished = QtCore.pyqtSignal()

    def __init__(self, parent=None, input_path=None):
        super(FirefoxAnalyzer, self).__init__(parent)

        # Input path to analyze
        self.input_path = input_path
        # List of all cache entries found
        self.list_cache_entries = []

        # Thread stopped by user
        self.stopped_by_user = False
        # Analysis running
        self.worker_is_running = True

        # Signal from "button_stop_analysis"
        self.signal_stop = Event()

    def analyze_cache(self):
        """Analyzing a Firefox cache input path updating a list with all entries found.
       Also sending signals to update "table_analysis_preview" with values for found entries.
       :return: nothing
       """

        index_file = os.path.join(self.input_path, "index")
        index_file_dimension = os.path.getsize(index_file)

        # Path to sub folder containing entries
        entries_path = os.path.join(self.input_path, "entries")

        header_dimension = 12
        record_dimension = 36
        tot_elem = (index_file_dimension-header_dimension)/record_dimension

        with open(index_file, "rb") as f_index:
            # Skipping header
            f_index.seek(header_dimension)

            # Cache file records
            while True:
                record = f_index.read(record_dimension)
                if not record:
                    break

                # "Button_stop_analysis" clicked
                if self.signal_stop.is_set():
                    self.stopped_by_user = True
                    self.worker_is_running = False
                    break

                # Current position inside the file
                current_pos = f_index.tell()

                # Read file if not reminder (Remaining file dimension could be less than record dimension)
                if (index_file_dimension - current_pos) % record_dimension != 0:

                    # Record values
                    url_hash = ""
                    for i in range(20):
                        start = i
                        stop = i + 1
                        url_hash += format(struct.unpack(">B", record[start:stop])[0], "X").zfill(2)

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

                    # Avoiding not continuously updating effect on "table_analysis_preview"
                    time.sleep(0.02)

                    # Values from resource
                    resource_uri = cache_entry_instance.resource_uri
                    resource_content_type = cache_entry_instance.resource_content_type

                    # URI in resource
                    if resource_uri:
                        self.signal_update_table_preview.emit(
                            len(self.list_cache_entries),
                            tot_elem,
                            cache_entry_instance.url_hash,
                            resource_uri,
                            resource_content_type,
                            cache_entry_instance.expire_date
                        )

                    # URI not in resource
                    else:
                        self.signal_update_table_preview.emit(
                            len(self.list_cache_entries),
                            tot_elem,
                            cache_entry_instance.url_hash,
                            "-",
                            "-",
                            cache_entry_instance.expire_date
                        )

                    # Updating "list_cache_entries"
                    self.list_cache_entries.append(cache_entry_instance)

        # Analysis terminated
        self.worker_is_running = False
        self.signal_finished.emit()
