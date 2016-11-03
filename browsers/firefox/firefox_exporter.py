# -*- coding: utf-8 -*-
# !/usr/bin/env python

# PyQt4 imports
from PyQt4 import QtCore

# Python imports
from threading import Event
import datetime
import os
import platform
import shutil

# Project imports
from utilities import utils
import index_header_reader
from operating_systems import windows


class FirefoxExporter(QtCore.QObject):
    """
    Exporter forMozilla Firefox cache.
    """

    # Signals
    signal_finished = QtCore.pyqtSignal()
    signal_update_export = QtCore.pyqtSignal(int, int)
    signal_enable_stop_button = QtCore.pyqtSignal()

    def __init__(self, parent=None, input_path=None, export_path=None, export_folder_name=None, entries_to_export=None,
                 browser_info=None, browser_def_path=None, export_md5=None, export_sha1=None):
        super(FirefoxExporter, self).__init__(parent)

        # Signal from "button_stop_export"
        self.signal_stop = Event()

        # Attributes
        self.input_path = input_path
        self.export_path = export_path
        self.export_folder_name = export_folder_name
        self.entries_to_export = entries_to_export
        self.browser = browser_info[0].text()
        self.browser_version = browser_info[1].text()
        self.browser_inst_path = browser_info[2].text()
        self.browser_def_path = browser_def_path
        self.export_md5 = export_md5
        self.export_sha1 = export_sha1
        self.stopped_by_user = False
        self.worker_is_running = True


    def exporter(self):

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

        # HTML index in scan report folder
        export_report_index = os.path.join(export_report_path, "index_report.html")
        export_results_index = os.path.join(export_results_path, "index_results.html")

        # Firefox "index" file info
        firefox_index_file = os.path.join(self.input_path, "index")
        firefox_index_header = index_header_reader.read_index_header(index_file=firefox_index_file)
        firefox_index_info = utils.get_file_info(file_path=firefox_index_file)

        entries_path = os.path.join(self.input_path, "entries")

        # Firefox cache folder info
        cache_folder_info = utils.get_folder_info(folder_path=self.input_path)
        entry_folder_info = utils.get_folder_info(folder_path=entries_path)


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
        <p> <b> Cache folder dimension (bytes): </b> {cache_dimension} </p>
        <p> <b> Cache folder elements: </b> {cache_elements} </p>
        <p> <b> Cache folder creation time: </b> {cache_creation_time} </p>
        <p> <b> Cache folder last modified time: </b> {cache_modified_time} </p>
        <p> <b> Cache folder last access: </b> {cache_last_access} </p>
        <hr>
        <h2> Cache entry folder info </h2>
        <p> <b> Cache folder dimension (bytes): </b> {entry_folder_dimension} </p>
        <p> <b> Cache folder elements: </b> {entry_folder_elements} </p>
        <p> <b> Cache folder creation time: </b> {entry_folder_creation_time} </p>
        <p> <b> Cache folder last modified time: </b> {entry_folder_modified_time} </p>
        <p> <b> Cache folder last access: </b> {entry_folder_last_access} </p>
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
            release_version= platform.version(),
            hostname=platform.node(),
            browser=self.browser,
            browser_version=self.browser_version,
            browser_inst_path=self.browser_inst_path,
            browser_def_path=self.browser_def_path,
            cache_dimension=cache_folder_info['folder_dimension'],
            cache_elements=cache_folder_info['folder_elements'],
            cache_creation_time=cache_folder_info['folder_creation_time'],
            cache_modified_time=cache_folder_info['folder_last_modified_time'],
            cache_last_access=cache_folder_info['folder_last_access_time'],
            entry_folder_dimension=entry_folder_info['folder_dimension'],
            entry_folder_elements=entry_folder_info['folder_elements'],
            entry_folder_creation_time=entry_folder_info['folder_creation_time'],
            entry_folder_modified_time=entry_folder_info['folder_last_modified_time'],
            entry_folder_last_access=entry_folder_info['folder_last_access_time'],
        )

        # Chrome "index" file values
        html_string_report_firefox_index = """
        <h2> index </h2>
        <p> <b> Index : </b> {index_file} </p>
        <p> <b> Index version: </b> {index_version} </p>
        <p> <b> Index last modified time: </b> {index_last_modified_time} </p>
        <p> <b> Index dirty flag: </b> {index_dirty_flag} </p>
        <p> <b> Index md5: </b> {md5} </p>
        <p> <b> Index sha1: </b> {sha1} </p>
        <p> <b> Dimension (bytes) (from OS): </b> {dimension} </p>
        <p> <b> Creation time (from OS): </b> {os_creation_time} </p>
        <p> <b> Last modified time (from OS): </b> {os_last_modified_time} </p>
        <p> <b> Last access time (from OS): </b> {os_last_access_time} </p>
        <hr>
        """.format(
            index_file=firefox_index_file,
            index_version=firefox_index_header['version'],
            index_last_modified_time=firefox_index_header['last_modified_time'],
            index_dirty_flag=firefox_index_header['dirty_flag'],
            md5=firefox_index_info['file_md5'],
            sha1=firefox_index_info['file_sha1'],
            dimension=firefox_index_info['file_dimension'],
            os_creation_time=firefox_index_info['file_creation_time'],
            os_last_modified_time=firefox_index_info['file_last_modified_time'],
            os_last_access_time=firefox_index_info['file_last_access_time']
        )

        # Cache file info
        html_string_report_firefox_entry_file = ""
        for entry in os.listdir(entries_path):

            # Info for current f_ file
            entry_file_path = os.path.join(entries_path, entry)
            firefox_entry_file_info = utils.get_file_info(file_path=entry_file_path)
            html_string_report_firefox_entry_file += """
            <h2> {f_file}  </h2>
            <p> <b> Dimension (bytes) (from OS): </b> {dimension} </p>
            <p> <b> Creation time (from OS): </b> {os_creation_time} </p>
            <p> <b> Last modified time (from OS): </b> {os_last_modified_time} </p>
            <p> <b> Last access time (from OS): </b> {os_last_access_time} </p>
            <p> <b> {f_file} md5: </b> {md5} </p>
            <p> <b> {f_file} sha1: </b> {sha1} </p>
            <hr>
            """.format(
                f_file=entry,
                dimension=firefox_entry_file_info['file_dimension'],
                os_creation_time=firefox_entry_file_info['file_creation_time'],
                os_last_modified_time=firefox_entry_file_info['file_last_modified_time'],
                os_last_access_time=firefox_entry_file_info['file_last_access_time'],
                md5=firefox_entry_file_info['file_md5'],
                sha1=firefox_entry_file_info['file_sha1']
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
                html_string_report_firefox_index +
                html_string_report_firefox_entry_file +
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
        <p> <b> Number of entries in entries_folder: </b> {num_entries} </p>
        <p> <b> Number of found entries: </b> {found_entries} </p>
        <hr>
        """.format(
            analysis_date=current_datetime_extended,
            input_folder=self.input_path,
            export_folder=os.path.join(self.export_path, self.export_folder_name),
            export_md5=self.export_md5,
            export_sha1=self.export_sha1,
            num_entries=len(os.listdir(entries_path)),
            found_entries=len(self.entries_to_export)
        )

        html_string_results_table_header = """
        <table id="recap_table" class="display" cellspacing="0" width="100%">
        <thead>
        <tr>
        <th> # </th>
        <th> Key Hash </th>
        <th> URI (preview) </th>
        <th> Expire Time </th>
        </tr>
        </thead>
        <tbody>
        """

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

            entry_name = "{number}{sep}{hash}".format(
                number=format(idx, "02"),
                sep="_",
                hash=entry.url_hash
            )

            # Table columns "#" and href for "Key Hash"
            html_string_results_table_row += """
            <tr>
            <td> {idx} </td> <td> <a href = ./{file_entry_html} target=_blank> {hash} </td>
            """.format(
                idx=format(idx, "02"),
                file_entry_html=entry_name + ".html",
                hash=unicode(entry.url_hash)
            )

            # Table columns "Uri" and "Expire time"
            html_string_results_table_row += """
            <td> {uri} </td> <td> {expire_time} </td>
            </tr>
            """.format(
                uri=unicode(entry.resource_uri[:75]),
                expire_time=entry.expire_date
            )

            # Creating a HTML file with entry info
            file_entry = os.path.join(export_results_path, entry_name)

            with open(file_entry + ".html", "w") as f_entry:
                # Opening HTML file for the entry
                html_string_file_entry_values = ""
                html_string_file_entry_container = ""
                html_string_file_entry_header = ""
                html_string_file_entry_open = """
                <html>
                <head> <title> {entry_name} </title> </head>
                <body>
                """.format(
                    entry_name=entry_name
                )

                # entry.entry_file_path not found for function "utils.get_file_info".
                # "entry.url_hash" in "os.listdir(entries_path)" avoids this problem

                if entry.url_hash in os.listdir(entries_path):
                    # shutil.copy(os.path.join(entries_path, entry.url_hash) , file_entry + "-data")
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
                    <p> <b> Container file md5: </b> {entry_file_md5}  </p>
                    <p> <b> Container file sha1: </b> {entry_file_sha1} </p>
                    <hr>
                    """.format(
                        entry=entry.url_hash,
                        export_date=current_datetime_extended,
                        export_md5=self.export_md5,
                        export_sha1=self.export_sha1,
                        entry_file=entry.entry_file_path,
                        entry_file_md5=utils.get_file_info(file_path=entry.entry_file_path)['file_md5'],
                        entry_file_sha1=utils.get_file_info(file_path=entry.entry_file_path)['file_sha1'],
                    )

                    # Entry values

                    html_string_file_entry_values = """
                    <h3> Entry values </h3>
                    <p> <b> Version:  </b> {version} </p>
                    <p> <b> Fetch count: </b> {fetch_count} </p>
                    <p> <b> Last fetched date:  </b> {last_fetched_date} </p>
                    <p> <b> Last modified date: </b> {last_modified_date} </b> </p>
                    <p> <b> Frequency: </b> {frequency} </p>
                    <p> <b> Expiration date: </b> {expiration_date} </p>
                    <p> <b> Key length:  </b> {key_length} </p>
                    <p> <b> URI: </b> {uri} </p>
                    <hr>
                    """.format(
                        version=entry.cache_resource_instance.version,
                        fetch_count=entry.cache_resource_instance.fetch_count,
                        last_fetched_date=entry.cache_resource_instance.last_fetched_date,
                        last_modified_date=entry.cache_resource_instance.last_modified_date,
                        frequency=entry.cache_resource_instance.frequency,
                        expiration_date=entry.cache_resource_instance.expire_date,
                        key_length=entry.cache_resource_instance.key_length,
                        uri=entry.cache_resource_instance.uri
                    )

                    html_string_file_entry_header = """
                    <h3> Header </h3>
                    <p> {header} </p>
                    """.format(
                        header=entry.cache_resource_instance.header
                    )

                    # Copying resource
                    entry_to_copy = os.path.join(entries_path, entry.url_hash)

                    # print  entry_name + "-data"
                    shutil.copy(os.path.join(entries_path, entry.url_hash), file_entry + "-data")

                #  Closing HTML file for the entry
                html_string_file_entry_close = """
                                            </body>
                                            </html>
                                            """
                # Writing file for the entry
                f_entry.write(html_string_file_entry_open +
                              html_string_file_entry_container +
                              html_string_file_entry_values +
                              html_string_file_entry_header +
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
