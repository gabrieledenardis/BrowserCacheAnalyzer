# -*- coding: utf-8 -*-
# !/usr/bin/env python

# PyQt4 imports
from PyQt4 import QtCore

# Python imports
from threading import Event
import os
import struct

# Project imports
import index_header_reader
import cache_address
import cache_entry


class ChromeAnalyzerWorker(QtCore.QObject):
    """
    Analyzer for Google Chrome cache and Opera cache.
    """

    signal_update_table_preview = QtCore.pyqtSignal(int, int, str, str, str, str)
    signal_finished = QtCore.pyqtSignal()

    def __init__(self, parent=None, input_path=None):
        super(ChromeAnalyzerWorker, self).__init__(parent)

        # Signal from "button_stop_analysis"
        self.signal_stop = Event()
        # Thread stopped by user
        self.stopped_by_user = False
        # Input path to analyze
        self.input_path = input_path
        # List of all cache entries found
        self.cache_entries_list = []

    def analyze_cache(self):

        # Chrome "index" file
        index_file = os.path.join(self.input_path, "index")

        # Address table size adn number of entries in "index" file
        table_size = index_header_reader.read_index_header(index_file)["table_size"]
        num_entries = index_header_reader.read_index_header(index_file)["number_of_entries"]

        # Header for "index" file
        index_header_dimension = 368

        with open(index_file, "rb") as f_index:
            # Skipping header
            f_index.seek(index_header_dimension)

            for addresses in range(table_size):
                # "Button_stop_analysis" clicked
                if self.signal_stop.is_set():
                    self.stopped_by_user = True
                    break

                # Binary address (32 bits)
                bin_address_in_index = format(struct.unpack("<I", f_index.read(4))[0], "032b")

                # # Existing and valid entry
                if bin_address_in_index and bin_address_in_index[0] == "1":
                    # Entry location
                    cache_file_instance = cache_address.CacheAddress(
                        binary_address=bin_address_in_index,
                        cache_path=self.input_path
                    )

                    cache_entry_instance = cache_entry.CacheEntry(
                        cache_path=self.input_path,
                        entry_file=cache_file_instance.file_path,
                        block_dimension=cache_file_instance.block_dimension,
                        block_number=cache_file_instance.block_number
                    )

                    # If an entry has a valid next entry address (an entry with the same hash),
                    # adding it to the entries list. Those entries are not in index table addresses
                    while cache_entry_instance.next_entry_address != 0:
                        # Updating "table_analysis_preview"
                        if (cache_entry_instance.data_stream_addresses[0] and
                                isinstance(cache_entry_instance.data_stream_addresses[0].resource_data, dict)):

                            if "Content-Type" in cache_entry_instance.data_stream_addresses[0].resource_data:
                                self.signal_update_table_preview.emit(
                                    len(self.cache_entries_list) - 1,
                                    num_entries,
                                    str(cache_entry_instance.key_hash),
                                    cache_entry_instance.key_data,
                                    cache_entry_instance.data_stream_addresses[0].resource_data['Content-Type'],
                                    cache_entry_instance.creation_time
                                )
                            else:
                                self.signal_update_table_preview.emit(
                                    len(self.cache_entries_list)-1,
                                    num_entries,
                                    str(cache_entry_instance.key_hash),
                                    cache_entry_instance.key_data,
                                    " - ",
                                    cache_entry_instance.creation_time
                                )
                        else:
                            self.signal_update_table_preview.emit(
                                len(self.cache_entries_list)-1,
                                num_entries,
                                str(cache_entry_instance.key_hash),
                                cache_entry_instance.key_data,
                                " - ",
                                cache_entry_instance.creation_time
                            )

                        # Adds cache entry to cache entries list
                        self.cache_entries_list.append(cache_entry_instance)

                        # Next entry address (from current entry)
                        bin_next_entry_address = format(cache_entry_instance.next_entry_address, "032b")

                        # Corresponding entry location (from next entry address)
                        cache_next_file_instance = cache_address.CacheAddress(
                            binary_address=bin_next_entry_address,
                            cache_path=self.input_path
                        )

                        cache_entry_instance = cache_entry.CacheEntry(
                            cache_path=self.input_path,
                            entry_file=cache_next_file_instance.file_path,
                            block_dimension=cache_next_file_instance.block_dimension,
                            block_number=cache_next_file_instance.block_number
                        )

                    # Adding cache entry to cache entries list
                    self.cache_entries_list.append(cache_entry_instance)

                    if (cache_entry_instance.data_stream_addresses[0] and
                            isinstance(cache_entry_instance.data_stream_addresses[0].resource_data, dict)):

                            if "Content-Type" in cache_entry_instance.data_stream_addresses[0].resource_data:
                                self.signal_update_table_preview.emit(
                                    len(self.cache_entries_list)-1,
                                    num_entries,
                                    str(cache_entry_instance.key_hash),
                                    cache_entry_instance.key_data,
                                    cache_entry_instance.data_stream_addresses[0].resource_data['Content-Type'],
                                    cache_entry_instance.creation_time
                                )
                            else:
                                self.signal_update_table_preview.emit(
                                    len(self.cache_entries_list)-1,
                                    num_entries,
                                    str(cache_entry_instance.key_hash),
                                    cache_entry_instance.key_data,
                                    " - ",
                                    cache_entry_instance.creation_time
                                )
                    else:
                        self.signal_update_table_preview.emit(
                            len(self.cache_entries_list)-1,
                            num_entries,
                            str(cache_entry_instance.key_hash),
                            cache_entry_instance.key_data,
                            " - ",
                            cache_entry_instance.creation_time
                        )

        self.signal_finished.emit()
