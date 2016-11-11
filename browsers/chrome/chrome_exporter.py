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

        self.input_path = input_path
        self.export_path = export_path
        self.export_folder_name = export_folder_name
        self.entries_to_export = entries_to_export
        self.export_md5 = export_md5
        self.export_sha1 = export_sha1

        # Portable browser
        if browser_portable:
            self.browser = browser_info[0]
            self.browser_version = browser_info[1]
            self.browser_inst_path = browser_info[2]
            self.browser_def_path = browser_def_path

        # Installed browser
        else:
            self.browser = browser_info[0].text()
            self.browser_version = browser_info[1].text()
            self.browser_inst_path = browser_info[2].text()
            self.browser_def_path = browser_def_path

        # Signal from "button_stop_export"
        self.signal_stop = Event()

        # Exporter state
        self.stopped_by_user = False
        self.worker_is_running = True

    def exporter(self):
        """Exporting all cache entries found in analysis.
        Creating an output main folder for the scan and two sub folders. One with an export report
        and another with export results.
        :return: nothing
        """

        # Current time
        current_datetime = datetime.datetime.now().strftime("%d-%b-%Y-%H_%M_%S")
        current_datetime_extended = datetime.datetime.now().strftime("%A - %d %B %Y - %H:%M:%S")

        # Results folder name
        results_folder_name = "Export_results"

        # Path for export results folder
        export_results_path = os.path.join(self.export_path, self.export_folder_name, results_folder_name)

        # Creating export folder
        os.makedirs(export_results_path)

        # HTML indexes in export folder
        export_report_index = os.path.join(self.export_path, self.export_folder_name, "index_report.html")
        export_results_index = os.path.join(self.export_path, self.export_folder_name, "index_results.html")

        # Static folder (for jquery and css)
        static_folder = os.path.join(self.export_path, self.export_folder_name, "_static")
        shutil.copytree(utils.STATIC_FOLDER, static_folder)
        export_output_style_path = "/".join(("_static", "application_css", "export_output_style.css"))
        jquery_path = "/".join(("_static", "js", "jquery-3.1.1.min.js"))
        jquery_datatables_path = "/".join(("_static", "js", "jquery.dataTables.js"))
        jquery_datatables_css_path = "/".join(("_static", "jquery_datatables_css", "jquery.dataTables.css"))

        # Chrome "index" file info
        chrome_index_file = os.path.join(self.input_path, "index")
        chrome_index_header = index_header_reader.read_index_header(index_file=chrome_index_file)
        chrome_index_info = utils.get_file_info(file_path=chrome_index_file)

        # Chrome cache folder info
        cache_folder_info = utils.get_folder_info(folder_path=self.input_path)

        # Number of entries found
        num_entries_found = len(self.entries_to_export)


##########################
# SECTION: EXPORT REPORT #
##########################

        # Opening "export_report"
        html_string_report_open = """
        <html>
        <head> <title> {export_date} </title>
        <link rel="stylesheet" type="text/css" href="{style_css}">
        </head>
        <body>
        """.format(
            export_date=current_datetime,
            style_css=export_output_style_path
        )

        # Report info
        time_info = windows.registry_system_time.get_registry_time_info()
        html_string_report_info = """
        <h1 class='main_title'> <b> Browser Cache Analyzer <br> Export report [{export_date}] </b> </h1>
        <h2 class='sub_title'> Export info </h2>
        <p class='analysis_item'> <b> Analysis folder: </b> {input_folder} </p>
        <p class='analysis_item'> <b> Export folder: </b> {export_folder} </p>
        <p class='analysis_item'> <b> Export md5: </b> {export_md5} </p>
        <p class='analysis_item'> <b> Export sha1: </b> {export_sha1} </p>
        <hr>
        <h2 class='sub_title'> System info </h2>
        <p class='analysis_item'> <b> System / Os name: </b> {os_name} </p>
        <p class='analysis_item'> <b> Release: </b> {release} </p>
        <p class='analysis_item'> <b> Release version: </b> {release_version} </p>
        <p class='analysis_item'> <b> Hostname: </b> {hostname} </p>
        <hr>
        <h2 class='sub_title'> System time info </h2>
        <p class='analysis_item'> <b> Last known good time: </b> {last_known} </p>
        <p class='analysis_item'> <b> Next synchronization time: </b> {next_sync} </p>
        <p class='analysis_item'> <b> Ntp server: </b> {ntp_server} </p>
        <p class='analysis_item'> <b> Synchronization type: </b> {sync_type} </p>
        <p class='analysis_item'> <b> Time zone: </b> {time_zone} </p>
        <hr>
        <h2 class='sub_title'> Browser info </h2>
        <p class='analysis_item'> <b> Browser: </b> {browser} </p>
        <p class='analysis_item'> <b> Browser version: </b> {browser_version} </p>
        <p class='analysis_item'> <b> Browser installation path: </b> {browser_inst_path} </p>
        <p class='analysis_item'> <b> Browser default cache path: </b> {browser_def_path} </p>
        <hr>
        <h2 class='sub_title'> Cache folder info </h2>
        <p class='analysis_item'> <b> Cache folder dimension (bytes): </b> {cache_dimension} </p>
        <p class='analysis_item'> <b> Cache folder elements: </b> {cache_elements} </p>
        <p class='analysis_item'> <b> Cache folder creation time: </b> {cache_creation_time} </p>
        <p class='analysis_item'> <b> Cache folder last modified time: </b> {cache_modified_time} </p>
        <p class='analysis_item'> <b> Cache folder last access: </b> {cache_last_access} </p>
        <hr>
        """.format(
            export_date=current_datetime_extended,
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
            cache_dimension=cache_folder_info['folder_dimension'],
            cache_elements=cache_folder_info['folder_elements'],
            cache_creation_time=cache_folder_info['folder_creation_time'],
            cache_modified_time=cache_folder_info['folder_last_modified_time'],
            cache_last_access=cache_folder_info['folder_last_access_time']
        )

        # Chrome "index" file values
        html_string_report_chrome_index = """
        <h2 class='sub_title'> index </h2>
        <p class='analysis_item'> <b> Index : </b> {index_file} </p>
        <p class='analysis_item'> <b> Signature: </b> {signature} </p>
        <p class='analysis_item'> <b> Minor version: </b> {minor_version} </p>
        <p class='analysis_item'> <b> Major version: </b> {major_version} </p>
        <p class='analysis_item'> <b> Number of entries: </b> {entries} </p>
        <p class='analysis_item'> <b> Stored data size (bytes): </b> {stored_data} </p>
        <p class='analysis_item'> <b> Last created f_ file: </b> f_{last_f_file} </p>
        <p class='analysis_item'> <b> Address table size: </b> {table_size} </p>
        <p class='analysis_item'> <b> Creation time: </b> {creation_time} </p>
        <p class='analysis_item'> <b> Index md5: </b> {md5} </p>
        <p class='analysis_item'> <b> Index sha1: </b> {sha1} </p>
        <p class='analysis_item'> <b> Dimension (bytes) (from OS): </b> {dimension} </p>
        <p class='analysis_item'> <b> Creation time (from OS): </b> {os_creation_time} </p>
        <p class='analysis_item'> <b> Last modified time (from OS): </b> {os_last_modified_time} </p>
        <p class='analysis_item'> <b> Last access time (from OS): </b> {os_last_access_time} </p>
        <hr>
        """.format(
            index_file=chrome_index_file,
            signature=chrome_index_header['signature'],
            minor_version=chrome_index_header['minor_version'],
            major_version=chrome_index_header['major_version'],
            entries=chrome_index_header['number_of_entries'],
            stored_data=chrome_index_header['stored_data_size'],
            last_f_file=chrome_index_header['last_created_file_f'],
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
                <h2 class='sub_title'> {data_file} </h2>
                <p class='analysis_item'> <b> Signature:  </b> {signature} </p>
                <p class='analysis_item'> <b> Minor version:  </b> {minor_version} </p>
                <p class='analysis_item'> <b> Major version:  </b> {major_version} </p>
                <p class='analysis_item'> <b> File number:  </b> {file_number} </p>
                <p class='analysis_item'> <b> Next file number:  </b> {next_file_number} </p>
                <p class='analysis_item'> <b> Block size (bytes):  </b> {block_size} </p>
                <p class='analysis_item'> <b> Number of entries:  </b> {num_entries} </p>
                <p class='analysis_item'> <b> Max number of entries:  </b> {max_num_entries} </p>
                <p class='analysis_item'> <b> {data_file} md5:  </b> {md5} </p>
                <p class='analysis_item'> <b> {data_file} sha1:  </b> {sha1} </p>
                <p class='analysis_item'> <b> Dimension (bytes) (from OS): </b> {dimension} </p>
                <p class='analysis_item'> <b> Creation time (from OS): </b> {os_creation_time} </p>
                <p class='analysis_item'> <b> Last modified time (from OS): </b> {os_last_modified_time} </p>
                <p class='analysis_item'> <b> Last access time (from OS): </b> {os_last_access_time} </p>
                <hr>
                """.format(
                    data_file=data_file,
                    signature=chrome_data_header['signature'],
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
                <h2 class='sub_title'> {f_file}  </h2>
                <p class='analysis_item'> <b> Dimension (bytes) (from OS): </b> {dimension} </p>
                <p class='analysis_item'> <b> Creation time (from OS): </b> {os_creation_time} </p>
                <p class='analysis_item'> <b> Last modified time (from OS): </b> {os_last_modified_time} </p>
                <p class='analysis_item'> <b> Last access time (from OS): </b> {os_last_access_time} </p>
                <p class='analysis_item'> <b> {f_file} md5: </b> {md5} </p>
                <p class='analysis_item'> <b> {f_file} sha1: </b> {sha1} </p>
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

        # Closing "export_report"
        html_string_report_close = """
        </body >
        </html >
        """

        # Writing "export_report_index"
        with open(export_report_index, "w") as f_report_index:
            f_report_index.write(
                html_string_report_open +
                html_string_report_info +
                html_string_report_chrome_index +
                html_string_report_chrome_data +
                html_string_report_chrome_f_ +
                html_string_report_close
            )


###########################
# SECTION: EXPORT RESULTS #
###########################

        # Opening "index_results"
        html_string_results_open = """
        <html>
        <head> <title> {export_date} </title>
        <link rel="stylesheet" type="text/css" href="{style_css}">
        """.format(
            export_date=current_datetime,
            style_css=export_output_style_path
        )

        # Table style
        html_string_results_table_style = """
        <script type="text/javascript" charset="utf8" src="{jquery}"></script>
        <script type="text/javascript" charset="utf8" src="{jquery_tables}"></script>
        <link rel="stylesheet" type="text/css" href="{jquery_datatables_css}">

        <script>
        $(function() {{
        $("#recap_table").DataTable();
        }});
        </script>
        </head>
        <body>
        """.format(
            jquery=jquery_path,
            jquery_tables=jquery_datatables_path,
            jquery_datatables_css=jquery_datatables_css_path
        )

        # Results info
        html_string_results_info = """
        <h1 class='main_title'> <b> Browser Cache Analyzer <br> Results report [{export_date}] </b> </h1>
        <h2 class='sub_title'> Export info </h2>
        <p class='analysis_item'> <b> Analysis folder: </b> {input_folder} </p>
        <p class='analysis_item'> <b> Export folder: </b> {export_folder} </p>
        <p class='analysis_item'> <b> Export date: </b> {export_date} </p>
        <p class='analysis_item'> <b> Export md5: </b> {export_md5} </p>
        <p class='analysis_item'> <b> Export sha1: </b> {export_sha1} </p>
        <p class='analysis_item'> <b> Number of entries in "index" header: </b> {index_entries} </p>
        <p class='analysis_item'> <b> Number of found entries: </b> {found_entries} </p>
        <hr>
        """.format(
            export_date=current_datetime_extended,
            input_folder=self.input_path,
            export_folder=os.path.join(self.export_path, self.export_folder_name),
            export_md5=self.export_md5,
            export_sha1=self.export_sha1,
            index_entries=chrome_index_header['number_of_entries'],
            found_entries=num_entries_found
        )

        # Table header
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

        # Enabling "button_stop_export"
        self.signal_enable_stop_button.emit()

        # Table rows
        html_string_results_table_row = ""
        for idx, entry in enumerate(self.entries_to_export, 1):

            # "Button_stop_export" clicked
            if self.signal_stop.is_set():
                self.stopped_by_user = True
                self.worker_is_running = False
                self.signal_finished.emit()
                break

            # Updating "progressBar_analysis"
            self.signal_update_export.emit(
                idx,
                num_entries_found
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
            <td> {idx} </td> <td> <a href = {results_folder}/{file_entry_html} target=_blank> {hash} </td>
            """.format(
                idx=format(idx, "02"),
                results_folder=results_folder_name,
                file_entry_html=entry_name + ".html",
                hash=entry.key_hash
            )

            # Table columns "Content Type" and "Creation Time"
            if (entry.data_stream_addresses[0] and
                    isinstance(entry.data_stream_addresses[0].resource_data, dict)):

                # "Content-Type" in HTTP header
                if "Content-Type" in entry.data_stream_addresses[0].resource_data:
                    html_string_results_table_row += """
                    <td> {content_type} </td> <td> {key_data} </td> <td> {creation_time} </td>
                    </tr>
                    """.format(
                        content_type=entry.data_stream_addresses[0].resource_data['Content-Type'],
                        key_data=entry.key_data[:75],
                        creation_time=entry.creation_time
                    )

                # "Content-Type" not in HTTP header
                else:
                    html_string_results_table_row += """
                    <td> - </td> <td> {key_data} </td> <td> {creation_time} </td>
                    </tr>
                    """.format(
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

            # "Entry file"
            file_entry = os.path.join(export_results_path, entry_name)
            with open(file_entry + ".html", "w") as f_entry:
                # Opening "entry file"
                html_string_file_entry_open = """
                <html>
                <head> <title> {entry_name} </title> </head>
                <link rel="stylesheet" type="text/css" href="../{style_css}">
                <body>
                """.format(
                    entry_name=entry_name,
                    style_css=export_output_style_path
                )

                # Container file info
                offset = 8192 + (entry.block_dimension * entry.block_number)
                html_string_file_entry_container = """
                <h2 class='main_title'> Report for entry: {entry} </h2>
                <h2 class='sub_title'> Export info </h2>
                <p class='analysis_item'> <b> Analysis folder: </b> {input_folder} </p>
                <p class='analysis_item'> <b> Export folder: </b> {export_folder} </p>
                <p class='analysis_item'> <b> Export date: </b> {export_date} </p>
                <p class='analysis_item'> <b> Export md5: </b> {export_md5} </p>
                <p class='analysis_item'> <b> Export sha1: </b> {export_sha1} </p>
                <hr>
                <h2 class='sub_title'> Container file </h2>
                <p class='analysis_item'> <b> Container file: </b> {entry_file} </p>
                <p class='analysis_item'> <b> Container file block dimension: </b> {block_dimension} </p>
                <p class='analysis_item'> <b> Container file block number: </b> {block_number} </p>
                <p class='analysis_item'> <b> Container file offset: </b> {offset} </p>
                <p class='analysis_item'> <b> Container file md5: </b> {entry_file_md5}  </p>
                <p class='analysis_item'> <b> Container file sha1: </b> {entry_file_sha1} </p>
                <hr>
                """.format(
                    entry=entry.key_hash,
                    input_folder=self.input_path,
                    export_folder=os.path.join(self.export_path, self.export_folder_name),
                    export_date=current_datetime_extended,
                    export_md5=self.export_md5,
                    export_sha1=self.export_sha1,
                    entry_file=entry.entry_file,
                    block_dimension=entry.block_dimension,
                    block_number=entry.block_number,
                    offset=offset,
                    entry_file_md5=utils.get_file_info(file_path=entry.entry_file)['file_md5'],
                    entry_file_sha1=utils.get_file_info(file_path=entry.entry_file)['file_sha1']
                )

                # Entry values
                html_string_file_entry_values = """
                <h2 class='sub_title'> Entry values </h2>
                <p class='analysis_item'> <b> Key hash:  </b> {hash} </p>
                <p class='analysis_item'> <b> Next entry address: </b> {next_addr} </p>
                <p class='analysis_item'> <b> Reuse count:  </b> {reuse_count} </p>
                <p class='analysis_item'> <b> Refetch count: </b> {refetch_count} </b> </p>
                <p class='analysis_item'> <b> Cache entry state: </b> {entry_state} </p>
                <p class='analysis_item'> <b> Creation time: </b> {creation_time} </p>
                <p class='analysis_item'> <b> Key data size:  </b> {key_data_size} </p>
                <p class='analysis_item'> <b> Long key cache data address: </b> {long_key_addr} </p>
                <p class='analysis_item'> <b> Cache entry flags:  </b> {flags} </b> <br>
                <p class='analysis_item'> <b> Key data:  </b> {key_data} </b> </p>
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
                        <h2 class='sub_title'> Resource values (Header) </h2>
                        <p class='analysis_item'> <b> Resource file:  </b> {resource_file} </p>
                        <p class='analysis_item'> <b> File header dimension:  </b> {header_dimension} </p>
                        <p class='analysis_item'> <b> Block dimension:  </b> {block_dimension} </p>
                        <p class='analysis_item'> <b> Block number:  </b> {block_number} </p>
                        <p class='analysis_item'> <b> Resource size:  </b> {resource_size} </p>
                        <p class='analysis_item'> <b> Resource offset:  </b> {offset} </p>
                        <hr>
                        """.format(
                            resource_file=resource_file,
                            header_dimension=8192,
                            block_dimension=block_dimension,
                            block_number=block_number,
                            resource_size=resource_size,
                            offset=resource_offset
                        )

                        # File containing the resource
                        with open(resource_file, "rb") as f_resource:
                            f_resource.seek(resource_offset)
                            resource_data = f_resource.read(resource_size)

                            # File to save the resource read
                            with open(file_entry_data, "wb") as f_entry_data:
                                f_entry_data.write(resource_data)

                        # Resource is HTTP Header
                        if item and isinstance(item.resource_data, dict) and item.resource_data:
                            # Values for the HTTP Header
                            html_string_file_http_header += """
                            <h2 class='sub_title'> Header </h2>
                            """

                            # Header keys (tags) and values
                            for key, key_value in item.resource_data.iteritems():
                                html_string_file_http_header += """
                                <p class='analysis_item'> <b> {key}: </b> {key_value} </p>
                                """.format(
                                    key=key,
                                    key_value=key_value
                                )

                            # Updating HTTP Header
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
                                <h2 class='sub_title'> Resource values (Data) </h2>
                                <p class='analysis_item'> <b> Resource file:  </b> {resource_file} </p>
                                <p class='analysis_item'> <b> File header dimension:  </b> {header_dimension} </p>
                                <p class='analysis_item'> <b> Block dimension:  </b> {block_dimension} </p>
                                <p class='analysis_item'> <b> Block number:  </b> {block_number} </p>
                                <p class='analysis_item'> <b> Resource size:  </b> {resource_size} </p>
                                <p class='analysis_item'> <b> Resource offset:  </b> {offset} </p>
                                <hr>
                                """.format(
                                    resource_file=resource_file,
                                    header_dimension=8192,
                                    block_dimension=block_dimension,
                                    block_number=block_number,
                                    resource_size=resource_size,
                                    offset=resource_offset
                                )

                                # File to save the resource read
                                with open(file_entry_data, "wb") as f_entry_data:
                                    f_entry_data.write(str(item.resource_data))

                            # Copying separate file if key data is in a separate file
                            else:
                                shutil.copy2(item.resource_file, file_entry_data)

                # Closing "entry file"
                html_string_file_entry_close = """
                                </body>
                                </html>
                                """

                # Writing "entry file"
                f_entry.write(html_string_file_entry_open +
                              html_string_file_entry_container +
                              html_string_file_entry_values +
                              html_string_resource_values +
                              html_string_file_http_header +
                              html_string_file_entry_close
                              )

        # Closing "index_results"
        html_string_results_close = """
        </tbody>
        </table>
        </body>
        </html>
        """

        # Writing "export_results_index"
        with open(export_results_index, "w") as f_export_index:
            f_export_index.write(
                html_string_results_open +
                html_string_results_table_style +
                html_string_results_info +
                html_string_results_table_header +
                html_string_results_table_row +
                html_string_results_close
            )

        # Export terminated
        self.worker_is_running = False
        self.signal_finished.emit()
