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
import cache_resource


class FirefoxExporter(QtCore.QObject):
    """Exporter for Firefox cache.
    """

    # Signals
    signal_finished = QtCore.pyqtSignal()
    signal_update_export = QtCore.pyqtSignal(int, int)
    signal_enable_stop_button = QtCore.pyqtSignal()
    signal_disable_stop_button = QtCore.pyqtSignal()

    def __init__(self, parent=None, input_path=None, export_path=None, export_folder_name=None, entries_to_export=None,
                 browser_portable=None, browser_info=None, browser_def_path=None, export_md5=None, export_sha1=None):
        super(FirefoxExporter, self).__init__(parent)

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
        Creating an output main folder for the scan and two sub folders, one with an export report
        and another with export results. Also creating a "Entries_not_in_index" sub folder for entries in "entries"
        folder but not in "index" file.
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

        # Path to sub folder containing entries
        entries_path = os.path.join(self.input_path, "entries")

        # Number of elements in "entries" folder
        num_entries_in_entries_folder = len(os.listdir(entries_path))

        # Firefox cache folder info
        cache_folder_info = utils.get_folder_info(folder_path=self.input_path)
        entry_folder_info = utils.get_folder_info(folder_path=entries_path)

        # Firefox "index" file info
        firefox_index_file = os.path.join(self.input_path, "index")
        firefox_index_header = index_header_reader.read_index_header(index_file=firefox_index_file)
        firefox_index_info = utils.get_file_info(file_path=firefox_index_file)


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
        <h2 class='sub_title'> Cache entry folder info </h2>
        <p class='analysis_item'> <b> Cache folder dimension (bytes): </b> {entry_folder_dimension} </p>
        <p class='analysis_item'> <b> Cache folder elements: </b> {entry_folder_elements} </p>
        <p class='analysis_item'> <b> Cache folder creation time: </b> {entry_folder_creation_time} </p>
        <p class='analysis_item'> <b> Cache folder last modified time: </b> {entry_folder_modified_time} </p>
        <p class='analysis_item'> <b> Cache folder last access: </b> {entry_folder_last_access} </p>
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
            cache_last_access=cache_folder_info['folder_last_access_time'],
            entry_folder_dimension=entry_folder_info['folder_dimension'],
            entry_folder_elements=entry_folder_info['folder_elements'],
            entry_folder_creation_time=entry_folder_info['folder_creation_time'],
            entry_folder_modified_time=entry_folder_info['folder_last_modified_time'],
            entry_folder_last_access=entry_folder_info['folder_last_access_time']
        )

        # Firefox "index" file values
        html_string_report_firefox_index = """
        <h2 class='sub_title'> index </h2>
        <p class='analysis_item'> <b> Index : </b> {index_file} </p>
        <p class='analysis_item'> <b> Index version: </b> {index_version} </p>
        <p class='analysis_item'> <b> Index last modified time: </b> {index_last_modified_time} </p>
        <p class='analysis_item'> <b> Index dirty flag: </b> {index_dirty_flag} </p>
        <p class='analysis_item'> <b> Index md5: </b> {md5} </p>
        <p class='analysis_item'> <b> Index sha1: </b> {sha1} </p>
        <p class='analysis_item'> <b> Dimension (bytes) (from OS): </b> {dimension} </p>
        <p class='analysis_item'> <b> Creation time (from OS): </b> {os_creation_time} </p>
        <p class='analysis_item'> <b> Last modified time (from OS): </b> {os_last_modified_time} </p>
        <p class='analysis_item'> <b> Last access time (from OS): </b> {os_last_access_time} </p>
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

        # Info for file in "entries" folder
        html_string_report_firefox_entry_file = ""
        for entry in os.listdir(entries_path):
            # Info for current f_ file
            entry_file_path = os.path.join(entries_path, entry)
            firefox_entry_file_info = utils.get_file_info(file_path=entry_file_path)
            html_string_report_firefox_entry_file += """
            <h2 class='sub_title'> {f_file}  </h2>
            <p class='analysis_item'> <b> Dimension (bytes) (from OS): </b> {dimension} </p>
            <p class='analysis_item'> <b> Creation time (from OS): </b> {os_creation_time} </p>
            <p class='analysis_item'> <b> Last modified time (from OS): </b> {os_last_modified_time} </p>
            <p class='analysis_item'> <b> Last access time (from OS): </b> {os_last_access_time} </p>
            <p class='analysis_item'> <b> {f_file} md5: </b> {md5} </p>
            <p class='analysis_item'> <b> {f_file} sha1: </b> {sha1} </p>
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
                html_string_report_firefox_index +
                html_string_report_firefox_entry_file +
                html_string_report_close
            )


#####################################################
# SECTION: EXPORT RESULTS (Entries in "index" file) #
#####################################################

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
        <h1 class='main_title'> <b> Browser Cache Analyzer <br> Results report [{export_date}]
        <br> Entries in "index" file </b>
        </h1>
        <h2 class='sub_title'> Export info </h2>
        <p class='analysis_item'> <b> Analysis folder: </b> {input_folder} </p>
        <p class='analysis_item'> <b> Export folder: </b> {export_folder} </p>
        <p class='analysis_item'> <b> Export date: </b> {export_date} </p>
        <p class='analysis_item'> <b> Export md5: </b> {export_md5} </p>
        <p class='analysis_item'> <b> Export sha1: </b> {export_sha1} </p>
        <p class='analysis_item'> <b> Number of entries in "entries" folder: </b> {num_entries} </p>
        <p class='analysis_item'> <b> Number of found entries: </b> {found_entries} </p>
        <hr>
        """.format(
            export_date=current_datetime_extended,
            input_folder=self.input_path,
            export_folder=os.path.join(self.export_path, self.export_folder_name),
            export_md5=self.export_md5,
            export_sha1=self.export_sha1,
            num_entries=len(os.listdir(entries_path)),
            found_entries=len(self.entries_to_export)
        )

        # Table header
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
                num_entries_in_entries_folder
            )

            # Name for current entry
            entry_name = "{number}{sep}{hash}".format(
                number=format(idx, "02"),
                sep="_",
                hash=entry.url_hash
            )

            # Table columns "#" and href for "Key Hash"
            html_string_results_table_row += """
            <tr>
            <td> {idx} </td> <td> <a href = {results_folder}/{file_entry_html} target=_blank> {hash} </td>
            """.format(
                idx=format(idx, "02"),
                results_folder=results_folder_name,
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

            # "Entry file"
            file_entry = os.path.join(export_results_path, entry_name)
            with open(file_entry + ".html", "w") as f_entry:
                html_string_file_entry_values = ""
                html_string_file_entry_container = ""
                html_string_file_entry_header = ""

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

                # Entry is in "entries" folder
                if entry.url_hash in os.listdir(entries_path):
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
                    <p class='analysis_item'> <b> Container file md5: </b> {entry_file_md5}  </p>
                    <p class='analysis_item'> <b> Container file sha1: </b> {entry_file_sha1} </p>
                    <hr>
                    """.format(
                        entry=entry.url_hash,
                        input_folder=self.input_path,
                        export_folder=os.path.join(self.export_path, self.export_folder_name),
                        export_date=current_datetime_extended,
                        export_md5=self.export_md5,
                        export_sha1=self.export_sha1,
                        entry_file=entry.entry_file_path,
                        entry_file_md5=utils.get_file_info(file_path=entry.entry_file_path)['file_md5'],
                        entry_file_sha1=utils.get_file_info(file_path=entry.entry_file_path)['file_sha1']
                    )

                    # Entry values
                    html_string_file_entry_values = """
                    <h2 class='sub_title'> Entry values </h2>
                    <p class='analysis_item'> <b> Data starting offset:  </b> {offset} </p>
                    <p class='analysis_item'> <b> Version:  </b> {version} </p>
                    <p class='analysis_item'> <b> Fetch count: </b> {fetch_count} </p>
                    <p class='analysis_item'> <b> Last fetched date:  </b> {last_fetched_date} </p>
                    <p class='analysis_item'> <b> Last modified date: </b> {last_modified_date} </b> </p>
                    <p class='analysis_item'> <b> Frequency: </b> {frequency} </p>
                    <p class='analysis_item'> <b> Expiration date: </b> {expiration_date} </p>
                    <p class='analysis_item'> <b> Key length:  </b> {key_length} </p>
                    <p class='analysis_item'> <b> URI: </b> {uri} </p>
                    <hr>
                    """.format(
                        offset=entry.cache_resource_instance.correct_data_starting_position,
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
                    <h2 class='sub_title'> Header </h2>
                    <p> {header} </p>
                    """.format(
                        header=entry.cache_resource_instance.raw_http_header
                    )

                    html_string_file_entry_header += """
                    <hr>
                    """

                    # File to save the header of the resource read
                    file_entry_header = os.path.join(export_results_path, entry_name + "-header")
                    with open(file_entry_header, "wb") as f_entry_header:
                        f_entry_header.write(str(entry.resource_http_header))

                    # File to save the data read from file in entries sub folder
                    file_entry_data = os.path.join(export_results_path, entry_name + "-data")
                    entries_file = os.path.join(entries_path, entry.url_hash)
                    with open(entries_file, "rb") as f_source:
                        source_data = f_source.read(entry.cache_resource_instance.correct_data_starting_position)
                        with open(file_entry_data, "wb") as file_entry_data:
                            file_entry_data.write(str(source_data))

                #  Closing "entry file"
                html_string_file_entry_close = """
                </body>
                </html>
                """

                # Writing "entry file"
                f_entry.write(html_string_file_entry_open +
                              html_string_file_entry_container +
                              html_string_file_entry_values +
                              html_string_file_entry_header +
                              html_string_file_entry_close
                              )

        # Closing "index_results""
        html_string_results_close = """
        </tbody>
        </table>
        </body>
        </html>
        """

        # Writing "export_results_index"
        with open(export_results_index, "w") as f_results_index:
            f_results_index.write(
                html_string_results_open +
                html_string_results_table_style +
                html_string_results_info +
                html_string_results_table_header +
                html_string_results_table_row +
                html_string_results_close
            )


#########################################################
# SECTION: EXPORT RESULTS (Entries NOT in "index" file) #
#########################################################

        # Disabling "button_stop_export"
        self.signal_disable_stop_button.emit()

        # Current number of entries exported (Entries in "self.entries_to_export")
        num_entries_in_index = len(self.entries_to_export)

        # "Not in index" folder name
        not_in_index_name = "Entries_not_in_index"

        # Path for export "not in index" folder
        entries_not_index_path = os.path.join(self.export_path, self.export_folder_name, not_in_index_name)

        # Creating export "not in index" folder
        os.makedirs(entries_not_index_path)

        # HTML "not_in_index" index in export folder
        export_results_index = os.path.join(self.export_path, self.export_folder_name, "index_entries_not_in_index.html")

        # Entries in "index" and in "entries" folder
        list_entry_ind_ent = []
        for idx, entry in enumerate(self.entries_to_export):
            if entry.url_hash in os.listdir(entries_path):
                list_entry_ind_ent.append(entry.url_hash)

        # Entries in "entries" folder but not in "index"
        num_only_entries = 0
        for url_hash in os.listdir(entries_path):
            if url_hash not in list_entry_ind_ent:
                num_only_entries += 1

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
        <h1 class='main_title'> <b> Browser Cache Analyzer <br> Results report [{export_date}]
        <br> Entries not in "index" file </b>
        </h1>
        <h2 class='sub_title'> Export info </h2>
        <p class='analysis_item'> <b> Analysis folder: </b> {input_folder} </p>
        <p class='analysis_item'> <b> Export folder: </b> {export_folder} </p>
        <p class='analysis_item'> <b> Export date: </b> {export_date} </p>
        <p class='analysis_item'> <b> Export md5: </b> {export_md5} </p>
        <p class='analysis_item'> <b> Export sha1: </b> {export_sha1} </p>
        <p class='analysis_item'> <b> Number of entries in "entries" folder: </b> {num_entries} </p>
        <p class='analysis_item'> <b> Number of found entries: </b> {found_entries} </p>
        <hr>
        """.format(
            export_date=current_datetime_extended,
            input_folder=self.input_path,
            export_folder=os.path.join(self.export_path, self.export_folder_name),
            export_md5=self.export_md5,
            export_sha1=self.export_sha1,
            num_entries=num_entries_in_entries_folder,
            found_entries=num_only_entries
        )

        # Table header
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

        # Enabling "button_stop_export"
        self.signal_enable_stop_button.emit()

        # Table rows (Entries in "entries" folder but not in "index")
        html_string_results_table_row = ""
        count = 0
        for url_hash in os.listdir(entries_path):
            if url_hash not in list_entry_ind_ent:
                count += 1
                cache_resource_instance = cache_resource.CacheResource(
                    entries_path=entries_path,
                    url_hash=url_hash
                )

                # "Button_stop_export" clicked
                if self.signal_stop.is_set():
                    self.stopped_by_user = True
                    self.worker_is_running = False
                    self.signal_finished.emit()
                    break

                # Updating "progressBar_analysis"
                self.signal_update_export.emit(
                    num_entries_in_index + count,
                    num_entries_in_entries_folder
                )

                # Name for current entry
                entry_name = "{number}{sep}{hash}".format(
                    number=format(count, "02"),
                    sep="_",
                    hash=url_hash
                )

                # Table columns "#" and href for "Key Hash"
                html_string_results_table_row += """
                <tr>
                <td> {idx} </td> <td> <a href = {not_in_index_folder}/{file_entry_html} target=_blank> {hash} </td>
                """.format(
                    idx=format(count, "02"),
                    not_in_index_folder=not_in_index_name,
                    file_entry_html=entry_name + ".html",
                    hash=unicode(url_hash)
                )

                # Table columns "Uri" and "Expire time"
                html_string_results_table_row += """
                <td> {uri} </td> <td> {expire_time} </td>
                </tr>
                """.format(
                    uri=unicode(cache_resource_instance.uri[:75]),
                    expire_time=cache_resource_instance.expire_date
                )

                # "Entry file"
                file_entry = os.path.join(entries_not_index_path, entry_name)
                with open(file_entry + ".html", "w") as f_entry:
                    html_string_file_entry_open = """
                    <html>
                    <head> <title> {entry_name} </title> </head>
                    <link rel="stylesheet" type="text/css" href="../{style_css}">
                    <body>
                    """.format(
                        entry_name=entry_name,
                        style_css=export_output_style_path
                    )

                    # "Entry" file container
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
                    <p class='analysis_item'> <b> Container file md5: </b> {entry_file_md5}  </p>
                    <p class='analysis_item'> <b> Container file sha1: </b> {entry_file_sha1} </p>
                    <hr>
                    """.format(
                        entry=url_hash,
                        input_folder=self.input_path,
                        export_folder=os.path.join(self.export_path, self.export_folder_name),
                        export_date=current_datetime_extended,
                        export_md5=self.export_md5,
                        export_sha1=self.export_sha1,
                        entry_file=cache_resource_instance.resource_file_path,
                        entry_file_md5=utils.get_file_info(
                            file_path=cache_resource_instance.resource_file_path
                        )['file_md5'],
                        entry_file_sha1=utils.get_file_info(
                            file_path=cache_resource_instance.resource_file_path
                         )['file_sha1']
                    )

                    # Entry values
                    html_string_file_entry_values = """
                    <h2 class='sub_title'> Entry values </h2>
                    <p class='analysis_item'> <b> Data starting offset:  </b> {offset} </p>
                    <p class='analysis_item'> <b> Version:  </b> {version} </p>
                    <p class='analysis_item'> <b> Fetch count: </b> {fetch_count} </p>
                    <p class='analysis_item'> <b> Last fetched date:  </b> {last_fetched_date} </p>
                    <p class='analysis_item'> <b> Last modified date: </b> {last_modified_date} </b> </p>
                    <p class='analysis_item'> <b> Frequency: </b> {frequency} </p>
                    <p class='analysis_item'> <b> Expiration date: </b> {expiration_date} </p>
                    <p class='analysis_item'> <b> Key length:  </b> {key_length} </p>
                    <p class='analysis_item'> <b> URI: </b> {uri} </p>
                    <hr>
                    """.format(
                        offset=cache_resource_instance.correct_data_starting_position,
                        version=cache_resource_instance.version,
                        fetch_count=cache_resource_instance.fetch_count,
                        last_fetched_date=cache_resource_instance.last_fetched_date,
                        last_modified_date=cache_resource_instance.last_modified_date,
                        frequency=cache_resource_instance.frequency,
                        expiration_date=cache_resource_instance.expire_date,
                        key_length=cache_resource_instance.key_length,
                        uri=cache_resource_instance.uri
                    )

                    # Entry header
                    html_string_file_entry_header = """
                    <h2 class='sub_title'> Header </h2>
                    <p> {header} </p>
                    """.format(
                        header=cache_resource_instance.raw_http_header
                    )

                    html_string_file_entry_header += """
                   <hr>
                   """

                    # File to save the header of the resource read
                    file_entry_header = os.path.join(entries_not_index_path, file_entry + "-header")
                    with open(file_entry_header, "wb") as f_entry_header:
                        f_entry_header.write(str(cache_resource_instance.raw_http_header))

                    # File to save the data read from file in entries sub folder
                    file_entry_data = os.path.join(entries_not_index_path, file_entry + "-data")
                    entries_file = os.path.join(entries_path, url_hash)
                    with open(entries_file, "rb") as f_source:
                        source_data = f_source.read(cache_resource_instance.correct_data_starting_position)
                        with open(file_entry_data, "wb") as file_entry_data:
                            file_entry_data.write(str(source_data))

                    #  Closing "entry file"
                    html_string_file_entry_close = """
                    </body>
                    </html>
                    """

                    # Writing "entry file"
                    f_entry.write(
                        html_string_file_entry_open +
                        html_string_file_entry_container +
                        html_string_file_entry_values +
                        html_string_file_entry_header +
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
