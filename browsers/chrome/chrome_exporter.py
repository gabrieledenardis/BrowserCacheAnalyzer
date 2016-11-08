# -*- coding: utf-8 -*-
# !/usr/bin/env python

# PyQt4 imports
from PyQt4 import QtCore

# Python imports
from threading import Event
import platform
import datetime
import shutil
import os

# Project imports
from operating_systems import windows
from utilities import utils
import index_header_reader
import data_header_reader


class ChromeExporter(QtCore.QObject):
    """Exporter for Google Chrome cache.
    """

    # Signals
    signal_finished = QtCore.pyqtSignal()
    signal_update_export = QtCore.pyqtSignal(int, int)
    signal_enable_stop_button = QtCore.pyqtSignal()

    def __init__(self, parent=None, input_path=None, export_path=None, export_folder_name=None, entries_to_export=None,
                 browser_portable=None, browser_info=None, browser_def_path=None, export_md5=None, export_sha1=None):
        super(ChromeExporter, self).__init__(parent)

        # Signal from "button_stop_export"
        self.signal_stop = Event()

        self.input_path = input_path
        self.export_path = export_path
        self.export_folder_name = export_folder_name
        self.entries_to_export = entries_to_export
        self.export_md5 = export_md5
        self.export_sha1 = export_sha1
        self.stopped_by_user = False
        self.worker_is_running = False

        if browser_portable:
            self.browser = browser_info[0]
            self.browser_version = browser_info[1]
            self.browser_inst_path = browser_info[2]
            self.browser_def_path = browser_def_path
        else:
            self.browser = browser_info[0].text()
            self.browser_version = browser_info[1].text()
            self.browser_inst_path = browser_info[2].text()
            self.browser_def_path = browser_def_path

    def exporter(self):
        """Exporting all cache entries found in analysis.
        Creating an output main folder for the scan and two sub folders. One with an export report
        and another with export results.
        :return: nothing
        """

        # Current time
        current_datetime = datetime.datetime.now().strftime("%d-%b-%Y-%H_%M_%S")
        current_datetime_extended = datetime.datetime.now().strftime("%A - %d %B %Y - %H:%M:%S")

        # Export folders
        report_folder_name = "Export_report"
        results_folder_name = "Export_results"

        # Paths for export folder
        export_report_path = os.path.join(self.export_path, self.export_folder_name, report_folder_name)
        export_results_path = os.path.join(self.export_path, self.export_folder_name, results_folder_name)

        # Creating "export_report_path"
        try:
            os.makedirs(export_report_path)
        except:
            pass

        # Creating "export_results_path"
        try:
            os.makedirs(export_results_path)
        except:
            pass

        # HTML index in scan report folders
        export_report_index = os.path.join(export_report_path, "index_report.html")
        export_results_index = os.path.join(export_results_path, "index_results.html")

        # Chrome "index" file info
        chrome_index_file = os.path.join(self.input_path, "index")
        chrome_index_header = index_header_reader.read_index_header(index_file=chrome_index_file)
        chrome_index_info = utils.get_file_info(file_path=chrome_index_file)

        # Chrome cache folder info
        folder_info = utils.get_folder_info(folder_path=self.input_path)


##########################
# SECTION: EXPORT REPORT #
##########################

        # Opening HTML "export_report"
        html_string_export_report_open = """
        <html>
        <head> <title> {scan_date} </title> </head>
        <body>
        """.format(
            scan_date=current_datetime
        )

        # Report info
        time_info = windows.registry_system_time.get_registry_time_info()
        html_string_report_info = """
        <h1> <b> Browser Cache Analyzer <br> Export report [{analysis_date}] </b> </h1>
        <p> <b> Analysis folder: </b> {input_folder} </p>
        <p> <b> Export folder: </b> {export_folder} </p>
        <p> <b> Export md5: </b> {export_md5} </p>
        <p> <b> Export sha1: </b> {export_sha1} </p>
        <hr>
        <h2> System info </h2>
        <p> <b> System / Os name: </b> {os_name} </p>
        <p> <b> Release: </b> {release} </p>
        <p> <b> Release version: </b> {release_version} </p>
        <p> <b> Hostname: </b> {hostname} </p>
        <hr>
        <h2> System time info </h2>
        <p> <b> Last known good time: </b> {last_known} </p>
        <p> <b> Next synchronization time: </b> {next_sync} </p>
        <p> <b> Ntp server: </b> {ntp_server} </p>
        <p> <b> Synchronization type: </b> {sync_type} </p>
        <p> <b> Time zone: </b> {time_zone} </p>
        <hr>
        <h2> Browser info </h2>
        <p> <b> Browser: </b> {browser} </p>
        <p> <b> Browser version: </b> {browser_version} </p>
        <p> <b> Browser installation path: </b> {browser_inst_path} </p>
        <p> <b> Browser default cache path: </b> {browser_def_path} </p>
        <hr>
        <h2> Cache folder info </h2>
        <p> <b> Cache folder dimension (bytes): </b> {dimension} </p>
        <p> <b> Cache folder elements: </b> {elements} </p>
        <p> <b> Cache folder creation time: </b> {creation_time} </p>
        <p> <b> Cache folder last modified time: </b> {modified_time} </p>
        <p> <b> Cache folder last access: </b> {last_access} </p>
        <hr>
        """.format(
            analysis_date=current_datetime_extended,
            input_folder=self.input_path,
            export_folder=os.path.join(self.export_path, self.export_folder_name),
            export_md5=self.export_md5,
            export_sha1=self.export_sha1,
            last_known=time_info['last_known_time'],
            next_sync=time_info['next_sync_time'],
            ntp_server=time_info['ntp_server'],
            sync_type=time_info['sync_type'],
            time_zone=time_info['time_zone'],
            os_name=platform.system(),
            release=platform.release(),
            release_version=platform.version(),
            hostname=platform.node(),
            browser=self.browser,
            browser_version=self.browser_version,
            browser_inst_path=self.browser_inst_path,
            browser_def_path=self.browser_def_path,
            dimension=folder_info['folder_dimension'],
            elements=folder_info['folder_elements'],
            creation_time=folder_info['folder_creation_time'],
            modified_time=folder_info['folder_last_modified_time'],
            last_access=folder_info['folder_last_access_time']
        )

        # Chrome "index" file values
        html_string_report_chrome_index = """
        <h2> index </h2>
        <p> <b> Index : </b> {index_file} </p>
        <p> <b> Signature: </b> {signature} </p>
        <p> <b> Minor version: </b> {minor_version} </p>
        <p> <b> Major version: </b> {major_version} </p>
        <p> <b> Number of entries: </b> {entries} </p>
        <p> <b> Stored data size (bytes): </b> {stored_data} </p>
        <p> <b> Last created f_ file: </b> f_{last_f_file} </p>
        <p> <b> Address table size: </b> {table_size} </p>
        <p> <b> Creation time: </b> {creation_time} </p>
        <p> <b> Index md5: </b> {md5} </p>
        <p> <b> Index sha1: </b> {sha1} </p>
        <p> <b> Dimension (bytes) (from OS): </b> {dimension} </p>
        <p> <b> Creation time (from OS): </b> {os_creation_time} </p>
        <p> <b> Last modified time (from OS): </b> {os_last_modified_time} </p>
        <p> <b> Last access time (from OS): </b> {os_last_access_time} </p>
        <hr>
        """.format(
            index_file=chrome_index_file,
            signature=format(chrome_index_header['signature'], "X"),
            minor_version=chrome_index_header['minor_version'],
            major_version=chrome_index_header['major_version'],
            entries=chrome_index_header['number_of_entries'],
            stored_data=chrome_index_header['stored_data_size'],
            last_f_file=format(chrome_index_header['last_created_file_f'], "06"),
            table_size=chrome_index_header['table_size'],
            creation_time=chrome_index_header['creation_time'],
            md5=chrome_index_info['file_md5'],
            sha1=chrome_index_info['file_sha1'],
            dimension=chrome_index_info['file_dimension'],
            os_creation_time=chrome_index_info['file_creation_time'],
            os_last_modified_time=chrome_index_info['file_last_modified_time'],
            os_last_access_time=chrome_index_info['file_last_access_time']
        )

        # Data_ file info
        html_string_report_chrome_data = ""
        for data_file in os.listdir(self.input_path):
            if "data_" in data_file:
                # Values for current data_# file
                data_num = str(data_file).split("_")[1]
                data_file_path = os.path.join(self.input_path, "data_{num}".format(num=data_num))
                chrome_data_header = data_header_reader.read_data_header(data_to_open=data_file_path)
                chrome_data_info = utils.get_file_info(file_path=data_file_path)

                html_string_report_chrome_data += """
                <h2> {data_file} </h2>
                <p> <b> Signature:  </b> {signature} </p>
                <p> <b> Minor version:  </b> {minor_version} </p>
                <p> <b> Major version:  </b> {major_version} </p>
                <p> <b> File number:  </b> {file_number} </p>
                <p> <b> Next file number:  </b> {next_file_number} </p>
                <p> <b> Block size (bytes):  </b> {block_size} </p>
                <p> <b> Number of entries:  </b> {num_entries} </p>
                <p> <b> Max number of entries:  </b> {max_num_entries} </p>
                <p> <b> {data_file} md5:  </b> {md5} </p>
                <p> <b> {data_file} sha1:  </b> {sha1} </p>
                <p> <b> Dimension (bytes) (from OS): </b> {dimension} </p>
                <p> <b> Creation time (from OS): </b> {os_creation_time} </p>
                <p> <b> Last modified time (from OS): </b> {os_last_modified_time} </p>
                <p> <b> Last access time (from OS): </b> {os_last_access_time} </p>
                <hr>
                """.format(
                    data_file=data_file,
                    signature=format(chrome_data_header['signature'], "X"),
                    minor_version=chrome_data_header['minor_version'],
                    major_version=chrome_data_header['major_version'],
                    file_number=chrome_data_header['file_number'],
                    next_file_number=chrome_data_header['next_file_number'],
                    block_size=chrome_data_header['block_size'],
                    num_entries=chrome_data_header['num_entries'],
                    max_num_entries=chrome_data_header['max_num_entries'],
                    md5=chrome_data_info['file_md5'],
                    sha1=chrome_data_info['file_sha1'],
                    dimension=chrome_data_info['file_dimension'],
                    os_creation_time=chrome_data_info['file_creation_time'],
                    os_last_modified_time=chrome_data_info['file_last_modified_time'],
                    os_last_access_time=chrome_data_info['file_last_access_time']
                )

        # F_ file info
        html_string_report_chrome_f_ = ""
        for sep_file in os.listdir(self.input_path):
            if "f_" in sep_file:
                # Values for current f_ file
                f_file_path = os.path.join(self.input_path, sep_file)
                chrome_f_info = utils.get_file_info(file_path=f_file_path)

                html_string_report_chrome_f_ += """
                <h2> {f_file}  </h2>
                <p> <b> Dimension (bytes) (from OS): </b> {dimension} </p>
                <p> <b> Creation time (from OS): </b> {os_creation_time} </p>
                <p> <b> Last modified time (from OS): </b> {os_last_modified_time} </p>
                <p> <b> Last access time (from OS): </b> {os_last_access_time} </p>
                <p> <b> {f_file} md5: </b> {md5} </p>
                <p> <b> {f_file} sha1: </b> {sha1} </p>
                <hr>
                """.format(
                    f_file=sep_file,
                    dimension=chrome_f_info['file_dimension'],
                    os_creation_time=chrome_f_info['file_creation_time'],
                    os_last_modified_time=chrome_f_info['file_last_modified_time'],
                    os_last_access_time=chrome_f_info['file_last_access_time'],
                    md5=chrome_f_info['file_md5'],
                    sha1=chrome_f_info['file_sha1']
                )

        # Closing HTML "export_report"
        html_string_export_report_close = """
                </body >
                </html >
                """

        # Creating "export_report_index"
        with open(export_report_index, "w") as f_report_index:
            f_report_index.write(
                html_string_export_report_open +
                html_string_report_info +
                html_string_report_chrome_index +
                html_string_report_chrome_data +
                html_string_report_chrome_f_ +
                html_string_export_report_close
            )


###########################
# SECTION: EXPORT RESULTS #
###########################

        # Opening HTML "export_results"
        html_string_export_results_open = """
        <html>
        <head> <title> {scan_date} </title>
        """.format(
            scan_date=current_datetime
        )

        html_string_results_table_style = """
        <script type="text/javascript" charset="utf8" src=file://{jquery}></script>
        <script type="text/javascript" charset="utf8" src=file://{jquery_tables}></script>
        <link rel="stylesheet" type="text/css" href="file://{jquery_datatables_css}">

        <script>
        $(function() {{
        $("#recap_table").DataTable();
        }});
        </script>
        </head>
        <body>
        """.format(
            jquery=utils.JQUERY_PATH,
            jquery_tables=utils.JQUERY_TABLES_PATH,
            jquery_datatables_css=utils.JQUERY_DATATABLES_CSS_PATH
        )

        html_string_results_info = """
        <h1> <b> Browser Cache Analyzer <br> Results report [{analysis_date}] </b> </h1>
        <p> <b> Analysis folder: </b> {input_folder} </p>
        <p> <b> Export folder: </b> {export_folder} </p>
        <p> <b> Export md5: </b> {export_md5} </p>
        <p> <b> Export sha1: </b> {export_sha1} </p>
        <hr>
        <p> <b> Number of entries in index header: </b> {index_entries} </p>
        <p> <b> Number of found entries: </b> {found_entries} </p>
        <hr>
        """.format(
            analysis_date=current_datetime_extended,
            input_folder=self.input_path,
            export_folder=os.path.join(self.export_path, self.export_folder_name),
            export_md5=self.export_md5,
            export_sha1=self.export_sha1,
            index_entries=chrome_index_header['number_of_entries'],
            found_entries=len(self.entries_to_export)
        )

        html_string_results_table_header = """
        <table id="recap_table" class="display" cellspacing="0" width="100%">
        <thead>
        <tr>
        <th> # </th>
        <th> Key Hash </th>
        <th> Content Type </th>
        <th> Key Url (preview) </th>
        <th> Creation Time </th>
        </tr>
        </thead>
        <tbody>
        """

        # Starting export
        self.worker_is_running = True

        html_string_results_table_row = ""
        for idx, entry in enumerate(self.entries_to_export, 1):

            # Enabling "button_stop_export"
            if idx > 1:
                self.signal_enable_stop_button.emit()

            # "Button_stop_export" clicked
            if self.signal_stop.is_set():
                self.stopped_by_user = True
                self.worker_is_running = False
                break

            # Updating "progressBar_analysis"
            self.signal_update_export.emit(
                idx,
                len(self.entries_to_export)
            )

            # Name for current entry
            entry_name = "{number}{sep}{hash}".format(
                number=format(idx, "02"),
                sep="_",
                hash=entry.key_hash
            )

            # Table columns "#" and href for "Key Hash"
            html_string_results_table_row += """
            <tr>
            <td> {idx} </td> <td> <a href = ./{file_entry_html} target=_blank> {hash} </td>
            """.format(
                idx=format(idx, "02"),
                file_entry_html=entry_name + ".html",
                hash=entry.key_hash
            )

            # Columns "Content Type" and "Creation Time"
            if (entry.data_stream_addresses[0] and
                    isinstance(entry.data_stream_addresses[0].resource_data, dict)):

                # "Content-Type" in HTTP header
                if "Content-Type" in entry.data_stream_addresses[0].resource_data:
                    html_string_results_table_row += """
                    <td> {content_type} </td> <td> {key_data} </td> <td> {creation_time} </td>
                    </tr>
                    """.format(
                        content_type=entry.data_stream_addresses[0].resource_data.get('Content-Type', "-"),
                        key_data=entry.key_data[:75],
                        creation_time=entry.creation_time
                    )

            # Not HTTP Header
            else:
                html_string_results_table_row += """
                <td> - </td> <td> {key_data} </td> <td> {creation_time} </td>
                </tr>
                """.format(
                    key_data=entry.key_data[:75],
                    creation_time=entry.creation_time
                )

            # Creating HTML file with entry info
            file_entry = os.path.join(export_results_path, entry_name)
            with open(file_entry + ".html", "w") as f_entry:
                # Opening HTML file for the entry
                html_string_file_entry_open = """
                <html>
                <head> <title> {entry_name} </title> </head>
                <body>
                """.format(
                    entry_name=entry_name
                )

                # Container file info
                offset = 8192 + (entry.block_dimension * entry.block_number)
                html_string_file_entry_container = """
                <h2> Report for entry: {entry} </h2>
                <hr>
                <h3> Export info </h3>
                <p> <b> Export date: </b> {export_date} </p>
                <p> <b> Export md5: </b> {export_md5} </p>
                <p> <b> Export sha1: </b> {export_sha1} </p>
                <hr>
                <h3> Container file </h3>
                <p> <b> Container file: </b> {entry_file} </p>
                <p> <b> Container file block dimension: </b> {block_dimension} </p>
                <p> <b> Container file block number: </b> {block_number} </p>
                <p> <b> Container file offset: </b> {offset} </p>
                <p> <b> Container file md5: </b> {entry_file_md5}  </p>
                <p> <b> Container file sha1: </b> {entry_file_sha1} </p>
                <hr>
                """.format(
                    entry=entry.key_hash,
                    export_date=current_datetime_extended,
                    export_md5=self.export_md5,
                    export_sha1=self.export_sha1,
                    entry_file=entry.entry_file,
                    block_dimension=entry.block_dimension,
                    block_number=entry.block_number,
                    offset=offset,
                    entry_file_md5=utils.get_file_info(entry.entry_file)['file_md5'],
                    entry_file_sha1=utils.get_file_info(entry.entry_file)['file_sha1'],
                )

                # Entry values
                html_string_file_entry_values = """
                <h3> Entry values </h3>
                <p> <b> Key hash:  </b> {hash} </p>
                <p> <b> Next entry address: </b> {next_addr} </p>
                <p> <b> Reuse count:  </b> {reuse_count} </p>
                <p> <b> Refetch count: </b> {refetch_count} </b> </p>
                <p> <b> Cache entry state: </b> {entry_state} </p>
                <p> <b> Creation time: </b> {creation_time} </p>
                <p> <b> Key data size:  </b> {key_data_size} </p>
                <p> <b> Long key cache data address: </b> {long_key_addr} </p>
                <p> <b> Cache entry flags:  </b> {flags} </b> <br>
                <p> <b> Key data:  </b> {key_data} </b> </p>
                <hr>
                """.format(
                    hash=entry.key_hash,
                    next_addr=entry.next_entry_address,
                    reuse_count=entry.reuse_count,
                    refetch_count=entry.refetch_count,
                    entry_state=entry.entry_state,
                    creation_time=entry.creation_time,
                    key_data_size=entry.key_data_size,
                    long_key_addr=entry.long_key_data_address,
                    flags=entry.cache_entry_flags,
                    key_data=entry.key_data
                )

                # Entry HTTP header
                html_string_file_http_header = ""

                # Resource values
                html_string_resource_values = ""
                for str_add, item in enumerate(entry.data_stream_addresses):
                    # HTTP Header
                    if str_add == 0 and item:
                        file_entry_data = "".join((file_entry, "-header"))
                        header_dimension = 8192
                        resource_file = item.resource_file
                        block_dimension = item.block_dimension
                        block_number = item.block_number
                        resource_size = item.resource_size
                        resource_offset = header_dimension + (block_dimension * block_number)

                        # Values for the resource
                        html_string_resource_values += """
                        <h3> Resource values (Header) </h3>
                        <p> <b> Resource file:  </b> {resource_file} </p>
                        <p> <b> File header dimension:  </b> {header_dimension} </p>
                        <p> <b> Block dimension:  </b> {block_dimension} </p>
                        <p> <b> Block number:  </b> {block_number} </p>
                        <p> <b> Resource size:  </b> {resource_size} </p>
                        <p> <b> Resource offset:  </b> {offset} </p>
                        <hr>
                        """.format(
                            resource_file=resource_file,
                            header_dimension=8192,
                            block_dimension=block_dimension,
                            block_number=block_number,
                            resource_size=resource_size,
                            offset=resource_offset
                        )

                        # Reading file containing the resource
                        with open(resource_file, "rb") as f_resource:
                            f_resource.seek(resource_offset)
                            resource_data = f_resource.read(resource_size)

                            # Creating file to save the resource read
                            with open(file_entry_data, "wb") as f_entry_data:
                                f_entry_data.write(resource_data)

                        # Resource is HTTP Header
                        if item and isinstance(item.resource_data, dict):
                            # Values for the HTTP Header
                            html_string_file_http_header += """
                            <h3> Header </h3>
                            """

                            # Header keys (tags) and values
                            for key, key_value in item.resource_data.iteritems():
                                html_string_file_http_header += """
                                <p> <b> {key}: </b> {key_value} </p>
                                """.format(
                                    key=key,
                                    key_value=key_value
                                )

                            html_string_file_http_header += """
                            <hr>
                            """

                    # Not HTTP Header
                    elif str_add != 0 and item:
                        if not item.is_http_header or item.is_http_header == "Unknown":
                            file_entry_data = "".join((file_entry, "-data{num}".format(num=str_add)))

                            # Key data not in separate file
                            if item.file_type != "000":

                                header_dimension = 8192
                                resource_file = item.resource_file
                                block_dimension = item.block_dimension
                                block_number = item.block_number
                                resource_size = item.resource_size
                                resource_offset = header_dimension + (block_dimension * block_number)

                                # Values for the resource
                                html_string_resource_values += """
                                <h3> Resource values (Data) </h3>
                                <p> <b> Resource file:  </b> {resource_file} </p>
                                <p> <b> File header dimension:  </b> {header_dimension} </p>
                                <p> <b> Block dimension:  </b> {block_dimension} </p>
                                <p> <b> Block number:  </b> {block_number} </p>
                                <p> <b> Resource size:  </b> {resource_size} </p>
                                <p> <b> Resource offset:  </b> {offset} </p>
                                <hr>
                                """.format(
                                    resource_file=resource_file,
                                    header_dimension=8192,
                                    block_dimension=block_dimension,
                                    block_number=block_number,
                                    resource_size=resource_size,
                                    offset=resource_offset
                                )

                                # Creating file to save the resource read
                                with open(file_entry_data, "wb") as f_entry_data:
                                    f_entry_data.write(str(item.resource_data))

                            # Copying separate file if key data is in a separate file
                            else:
                                shutil.copy(item.resource_file, file_entry_data)

                #  Closing HTML file for the entry
                html_string_file_entry_close = """
                                </body>
                                </html>
                                """

                # Writing file for the entry
                f_entry.write(html_string_file_entry_open +
                              html_string_file_entry_container +
                              html_string_file_entry_values +
                              html_string_resource_values +
                              html_string_file_http_header +
                              html_string_file_entry_close
                              )

        # Closing HTML "export_results"
        html_string_results_close = """
                </tbody>
                </table>
                </body>
                </html>
                """

        # Creating "export_results_index"
        with open(export_results_index, "w") as f_scan_index:
            f_scan_index.write(
                html_string_export_results_open +
                html_string_results_table_style +
                html_string_results_info +
                html_string_results_table_header +
                html_string_results_table_row +
                html_string_results_close
            )

        # Export terminated
        self.worker_is_running = False
        self.signal_finished.emit()
