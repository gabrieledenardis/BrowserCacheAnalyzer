# -*- coding: utf-8 -*-
# !/usr/bin/env python

# PyQt4 imports
from PyQt4 import QtGui
from PyQt4 import QtCore

# Python imports
import platform
import os
import datetime
import shutil

# Project imports
from gui import bca_converted_gui
from operating_systems import windows
from utilities import utils, browsers_utils
import browsers
from gui import browsers_dialogs


class BrowserCacheAnalyzer(QtGui.QMainWindow, bca_converted_gui.Ui_BrowserCacheAnalyzerGuiClass):
    """
    Main class for Browser Cache Analyzer
    """

    def __init__(self, parent=None):
        super(BrowserCacheAnalyzer, self).__init__(parent)

        # Setting up the application user interface from converted gui
        self.setupUi(self)

        # Frameless window
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)


##########################################
# SECTION: APPLICATION ELEMENTS SETTINGS #
##########################################

        # "GroupBox_system_info"
        self.groupBox_system_info.setStyleSheet("QLineEdit { background-color: transparent }")
        for line in self.groupBox_system_info.findChildren(QtGui.QLineEdit):
            line.setFocusPolicy(QtCore.Qt.ClickFocus)
            line.installEventFilter(self)
            line.setReadOnly(True)
            line.setFrame(False)

        # "GroupBox_selected_browser_info"
        self.groupBox_selected_browser_info.setStyleSheet("QLineEdit { background-color: transparent }")
        for line in self.groupBox_selected_browser_info.findChildren(QtGui.QLineEdit):
            line.setFocusPolicy(QtCore.Qt.ClickFocus)
            line.installEventFilter(self)
            line.setReadOnly(True)
            line.setFrame(False)

        #########################################
        # ********** Browsers screen ********** #

        # "GroupBox_installed_browsers"
        self.groupBox_installed_browsers.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.groupBox_installed_browsers.installEventFilter(self)

        # "Table_installed_browsers"
        self.table_installed_browsers.setColumnCount(4)
        self.table_installed_browsers.setHorizontalHeaderLabels(['', 'Browser Name', 'Version', 'Installation Path'])
        self.table_installed_browsers.setColumnWidth(0, len("Icon") + 50)
        self.table_installed_browsers.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.Stretch)
        self.table_installed_browsers.horizontalHeader().setResizeMode(3, QtGui.QHeaderView.Stretch)
        self.table_installed_browsers.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table_installed_browsers.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.table_installed_browsers.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table_installed_browsers.setAlternatingRowColors(True)
        self.table_installed_browsers.setToolTip("Click on a row to select a browser")

        #############################################
        # ********** Input folder screen ********** #

        # "GroupBox_input_folder"
        self.groupBox_input_folder.setStyleSheet("QLineEdit {background-color: transparent}")
        for line in self.groupBox_input_folder.findChildren(QtGui.QLineEdit):
            if "line_input_path_folder_screen" != line.objectName():
                line.setFrame(False)
            line.setFocusPolicy(QtCore.Qt.ClickFocus)
            line.installEventFilter(self)
            line.setReadOnly(True)

        # "GroupBox_input_folder_preview"
        self.groupBox_input_folder_preview.setStyleSheet("color: rgb(70, 70, 70)")
        self.list_input_folder_preview.setStyleSheet("background-color: transparent")
        self.list_input_folder_preview.setToolTip("Select a file to show info")
        for line in self.groupBox_input_folder_preview.findChildren(QtGui.QLineEdit):
            line.setStyleSheet("background-color: transparent")
            line.installEventFilter(self)
            line.setReadOnly(True)
            line.setFrame(False)

        #########################################
        # ********** Analysis screen ********** #

        # "GroupBox_analysis_preview"
        self.line_input_path_analysis.setStyleSheet("background-color: transparent")
        self.line_input_path_analysis.installEventFilter(self)
        self.line_input_path_analysis.setReadOnly(True)
        self.line_input_path_analysis.setFrame(False)

        #  "Table_analysis_preview"
        self.table_analysis_preview.setColumnCount(4)
        self.table_analysis_preview.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.table_analysis_preview.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.table_analysis_preview.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table_analysis_preview.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table_analysis_preview.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.table_analysis_preview.setToolTip("Right click for options")
        self.table_analysis_preview.setAlternatingRowColors(True)
        self.table_analysis_preview.setSortingEnabled(True)

        ##########################################
        # ********** Exporting screen ********** #

        # "GroupBox_export"
        for line in self.groupBox_export.findChildren(QtGui.QLineEdit):
            line.setStyleSheet("background-color: transparent")
            line.installEventFilter(self)
            line.setReadOnly(True)
            line.setFrame(False)

        #############################################
        # ********** Application buttons ********** #

        # Application buttons
        for item in self.findChildren(QtGui.QPushButton):
            item.setStyleSheet(
                "QPushButton {background-color: transparent; border: 1px solid darkgray}"
                "QPushButton:hover {background-color: rgb(208,208,208)}"
            )


#######################
# SECTION: ATTRIBUTES #
#######################

        # Mouse cursor coordinates
        self.mouse_press_position = None
        # List of installed browsers in the system
        self.list_installed_browsers = []
        # Selection from "table_installed_browsers"
        self.selection_table_installed_browsers = None
        # Matching key for selected browser
        self.matching_browser_key = None
        # Default cache path for selected browser
        self.default_cache_path = None
        # Current selected path to analyze and current export path
        self.current_input_path = None
        self.current_export_path = None
        # List containing cache entries found in "chrome cache"
        self.list_found_cache_entries = []
        # Clipboard to store copied values
        self.clipboard = None
        # QDialog for advanced info on items in "table_analysis_preview"
        self.browser_preview_dialog = None
        # Context menu on "table_analysis_preview" during analysis
        self.context_menu_enabled = False
        # Selected browser is portable
        self.browser_is_portable = False

        # Threads
        self.chrome_analyzer_thread = None
        self.chrome_analyzer_worker = None
        self.chrome_exporter_thread = None
        self.chrome_exporter_worker = None

        self.firefox_analyzer_thread = None
        self.firefox_analyzer_worker = None
        self.firefox_exporter_thread = None
        self.firefox_exporter_worker = None

        self.opera_analyzer_thread = None
        self.opera_analyzer_worker = None
        self.opera_exporter_thread = None
        self.opera_exporter_worker = None

        self.current_analyzer_thread = None
        self.current_analyzer_worker = None
        self.current_exporter_thread = None
        self.current_exporter_worker = None


##########################################
# SECTION: SIGNALS AND SLOTS CONNECTIONS #
##########################################

        # Connections for "minimize_application" and "close_application" buttons
        self.button_minimize_application.clicked.connect(self.showMinimized)
        self.button_close_application.clicked.connect(self.close_application)

        # Connections for other application elements
        self.button_search_installed_browsers.clicked.connect(self.set_browsers_screen)
        self.table_installed_browsers.itemClicked.connect(self.enable_button_browsers_screen_select)
        self.button_installed_select_cache.clicked.connect(self.set_input_folder_screen)
        self.button_analyze_default_path.clicked.connect(self.select_input_path)
        self.button_analyze_other_path.clicked.connect(self.select_input_path)
        self.list_input_folder_preview.itemClicked.connect(self.get_file_info)
        self.button_input_folder_screen_back.clicked.connect(self.set_browsers_screen)
        self.button_confirm_analysis.clicked.connect(self.set_analysis_screen)
        self.button_stop_analysis.clicked.connect(self.stop_analysis)
        self.button_analysis_screen_back.clicked.connect(self.set_input_folder_screen)
        self.button_quit_analysis_screen.clicked.connect(self.close_application)
        self.table_analysis_preview.customContextMenuRequested.connect(self.table_analysis_preview_context_menu)
        self.button_export_to_html.clicked.connect(self.export_to_html)
        self.button_show_folder.clicked.connect(self.show_export_folder)
        self.button_stop_export.clicked.connect(self.stop_export)
        self.button_quit_export_screen.clicked.connect(self.close_application)
        self.button_home.clicked.connect(self.set_welcome_screen)

        self.button_portable_versions.clicked.connect(self.set_browsers_screen)
        self.button_back_portable_versions.clicked.connect(self.set_welcome_screen)
        self.button_portable_chrome.clicked.connect(self.enable_button_browsers_screen_select)
        self.button_portable_firefox.clicked.connect(self.enable_button_browsers_screen_select)
        self.button_portable_opera.clicked.connect(self.enable_button_browsers_screen_select)
        self.button_portable_select_cache.clicked.connect(self.set_input_folder_screen)
        self.button_back_installed_browsers.clicked.connect(self.set_welcome_screen)

        self.set_welcome_screen()


###########################
# SECTION: WELCOME SCREEN #
###########################

    def set_welcome_screen(self):

        # Welcome screen settings
        self.stackedWidget.setCurrentIndex(0)
        self.groupBox_selected_browser_info.setVisible(False)
        self.label_application_title.setVisible(False)
        self.label_application_icon.setVisible(False)
        self.groupBox_system_info.setVisible(False)

        self.browser_is_portable = False

############################
# SECTION: BROWSERS SCREEN #
#############################

    def set_browsers_screen(self):
        """Slot for "button_search_browsers" in "welcome screen" and "button_input_folder_screen_back"
        in "input folder screen" .
        "Browsers screen": stacked widget index = 1, visible "groupBox_system_info" with system values,
        not visible "groupBox_selected_browser_info" and "table_installed_browsers" containing installed browsers
        in the system.
        :return: nothing
        """

        # for item in self.groupBox_selected_browser_info.findChildren((QtGui.QLineEdit, QtGui.QLabel)):
        #     item.clear()
        self.groupBox_selected_browser_info.setVisible(False)

        self.label_application_title.setVisible(True)
        self.label_application_icon.setVisible(True)
        self.groupBox_system_info.setVisible(True)
        self.groupBox_selected_browser_info.setVisible(False)

        # System values
        self.line_system_os_name.setText(platform.system())
        self.line_system_release.setText(platform.release())
        self.line_system_release_version.setText(platform.version())
        self.line_system_hostname.setText(platform.node())

        # Detecting clicked button
        clicked_button = self.sender().objectName()

        if clicked_button == "button_portable_versions":

            self.browser_is_portable = True

            # Welcome screen settings
            self.stackedWidget.setCurrentIndex(1)
            self.button_portable_select_cache.setEnabled(False)
            self.label_selected_portable.clear()

        elif clicked_button == "button_search_installed_browsers":

            # Browsers screen settings
            self.stackedWidget.setCurrentIndex(2)

            self.button_installed_select_cache.setEnabled(False)

            # If back from "input folder screen"
            self.table_installed_browsers.setRowCount(0)

            # Searching for browsers (depending on OS)
            # Microsoft Windows
            if "windows" in platform.system().lower():
                self.list_installed_browsers = windows.browsers_finder.finder()
            # TODO: Code for other OSs

            # "Table_installed_browsers"
            for idx, brw in enumerate(self.list_installed_browsers):
                self.table_installed_browsers.insertRow(idx)

                # Browser values
                icon_name = brw[0]
                browser_name = brw[1]
                version = brw[2]
                browser_inst_path = brw[3]

                self.table_installed_browsers.setCellWidget(idx, 0, BrowserIconWidget(icon_name=icon_name))
                self.table_installed_browsers.setItem(idx, 1, QtGui.QTableWidgetItem(browser_name))
                self.table_installed_browsers.setItem(idx, 2, QtGui.QTableWidgetItem(version))
                self.table_installed_browsers.setItem(idx, 3, QtGui.QTableWidgetItem(browser_inst_path))

        elif clicked_button == "button_input_folder_screen_back":

            if self.browser_is_portable:
                self.stackedWidget.setCurrentIndex(1)
            else:
                self.stackedWidget.setCurrentIndex(2)

    def enable_button_browsers_screen_select(self):

        if self.browser_is_portable:
            # Detecting clicked button
            clicked_button = self.sender().objectName()

            # "Button_browsers_screen_select" button in "browser screen"
            if clicked_button == "button_portable_chrome":
                self.matching_browser_key = "chrome"
                self.label_selected_portable.setText(self.matching_browser_key)
            elif clicked_button == "button_portable_firefox":
                self.matching_browser_key = "firefox"
                self.label_selected_portable.setText(self.matching_browser_key)
            elif clicked_button == "button_portable_opera":
                self.matching_browser_key = "opera"
                self.label_selected_portable.setText(self.matching_browser_key)

            if clicked_button:
                self.button_portable_select_cache.setEnabled(True)

        else:

            # Getting selection from table and enabling button
            self.selection_table_installed_browsers = self.table_installed_browsers.selectedItems()
            if self.selection_table_installed_browsers:
                self.button_installed_select_cache.setEnabled(True)


################################
# SECTION: INPUT FOLDER SCREEN #
################################

    def set_input_folder_screen(self):
        """Slot for "button_browsers_screen_select" in "browsers screen".
        "Input folder screen": stacked widget index = 2, visible "groupBox_selected_browser_info" and
        selection for an input folder to analyze.
        :return: nothing
        """


        # Detecting clicked button
        clicked_button = self.sender().objectName()

        if clicked_button == "button_portable_select_cache":
            # Processes for selected browser
            browser_process = browsers_utils.check_open_browser(self.matching_browser_key)

            # If selected browser is open
            if len(browser_process):
                # String with pids and names from "browser_process_list"
                browser_processes_string = ""

                for pid, name in browser_process.iteritems():
                    browser_processes_string += "pid: {pid} \t name: {name}\n".format(pid=pid, name=name)

                QtGui.QMessageBox.warning(
                    QtGui.QMessageBox(), "Open browser",
                    "{browser} seems to be open. Please close it.\n\n{processes}".format(
                        browser=self.matching_browser_key.capitalize(),
                        processes=browser_processes_string
                    ),
                    QtGui.QMessageBox.Ok
                )
            # Selected browser is not open
            else:
                # Input screen settings"
                self.stackedWidget.setCurrentIndex(3)
                self.groupBox_selected_browser_info.setVisible(True)
                self.button_analyze_default_path.setEnabled(False)
                self.button_confirm_analysis.setEnabled(False)

                self.line_browser_selected.setText(self.matching_browser_key.capitalize())
                self.line_browser_version.setText("Not available")
                self.line_browser_default_cache_path.setText("Not available")
                self.line_browser_install_path.setText("Not available")
                self.label_browser_mark_path.clear()

                # Selected browser icon
                icon_path = os.path.join(utils.ICONS_PATH, "{icon}.png".format(icon=self.matching_browser_key))
                browser_icon = QtGui.QPixmap(icon_path)
                self.label_browser_icon.setPixmap(browser_icon)

                # Already visited "input screen" from "browser screen"
                self.current_input_path = None
                for line in self.groupBox_input_folder.findChildren(QtGui.QLineEdit):
                    line.clear()
                for item in self.groupBox_input_folder_preview.findChildren((QtGui.QListWidget, QtGui.QLineEdit)):
                    item.clear()

        # "Button_browsers_screen_select" button in "browser screen"
        elif clicked_button == "button_installed_select_cache":

            self.button_confirm_analysis.setEnabled(False)

            # Values for selection from table
            browser_name = self.selection_table_installed_browsers[0].text()
            browser_version = self.selection_table_installed_browsers[1].text()
            browser_install_path = self.selection_table_installed_browsers[2].text()

            # Matching key for selected browser
            browser_info_path = browsers_utils.get_default_cache_path(browser_name=browser_name)
            self.matching_browser_key = browser_info_path['matching_browser_key']
            self.default_cache_path = browser_info_path['default_cache_path']

            # Processes for selected browser
            browser_process = browsers_utils.check_open_browser(self.matching_browser_key)

            # If selected browser is open
            if len(browser_process):
                # String with pids and names from "browser_process_list"
                browser_processes_string = ""

                for pid, name in browser_process.iteritems():
                    browser_processes_string += "pid: {pid} \t name: {name}\n".format(pid=pid, name=name)

                QtGui.QMessageBox.warning(
                    QtGui.QMessageBox(), "Open browser",
                    "{browser} seems to be open. Please close it.\n\n{processes}".format(
                        browser=browser_name,
                        processes=browser_processes_string
                    ),
                    QtGui.QMessageBox.Ok
                )

            # Selected browser is not open
            else:
                # Input screen settings"
                self.stackedWidget.setCurrentIndex(3)
                self.groupBox_selected_browser_info.setVisible(True)

                # Already visited "input screen" from "browser screen"
                self.current_input_path = None
                for line in self.groupBox_input_folder.findChildren(QtGui.QLineEdit):
                    line.clear()
                for item in self.groupBox_input_folder_preview.findChildren((QtGui.QListWidget, QtGui.QLineEdit)):
                    item.clear()

                # Selected browser values
                self.line_browser_selected.setText(browser_name)
                self.line_browser_version.setText(browser_version)
                self.line_browser_install_path.setText(browser_install_path)
                self.line_browser_default_cache_path.setText(self.default_cache_path)
                self.line_browser_default_cache_path.home(False)
                self.line_browser_install_path.home(False)

                # Selected browser icon
                icon_path = os.path.join(utils.ICONS_PATH, "{icon}.png".format(icon=self.matching_browser_key))
                browser_icon = QtGui.QPixmap(icon_path)
                self.label_browser_icon.setPixmap(browser_icon)

                # Checking if default cache path for selected browser is valid
                valid_default_path = browsers_utils.check_valid_cache_path(
                    browser=self.matching_browser_key,
                    cache_path=self.default_cache_path
                )

                # Valid default cache path
                if valid_default_path:
                    mark_path = os.path.join(utils.ICONS_PATH, "mark_valid.png")
                    self.label_browser_mark_path.setToolTip("Path is valid for selected browser")
                    self.button_analyze_default_path.setEnabled(True)

                # Not valid default cache path
                else:
                    mark_path = os.path.join(utils.ICONS_PATH, "mark_not_valid.png")
                    self.label_browser_mark_path.setToolTip("Path is not valid for selected browser")
                    self.button_analyze_default_path.setEnabled(False)

                # Mark for default path
                mark_icon = QtGui.QPixmap(mark_path)
                self.label_browser_mark_path.setPixmap(mark_icon)

        # "Button_analysis_screen_back" button in "analysis screen"
        elif clicked_button == "button_analysis_screen_back":
            # Input screen settings"
            self.stackedWidget.setCurrentIndex(3)

    def select_input_path(self):
        """Slot for "button_analyze_default_path" and "button_analyze_other_path".
        Selecting a path to analyze and checking it to be valid for selected browser.
        :return: nothing
        """
        # Clicked button ("default" or "other path")
        clicked_button = self.sender().objectName()

        # "Default" path button
        if clicked_button == "button_analyze_default_path":
            # Setting "current input path" as "default path"
            self.current_input_path = self.default_cache_path

            self.line_input_path_folder_screen.setText(self.current_input_path)
            self.line_input_path_folder_screen.home(False)

        # "Other path" button
        elif clicked_button == "button_analyze_other_path":
            # Selecting an input path to analyze
            dialog_input_path = QtGui.QFileDialog().getExistingDirectory(
                self, "Select a cache folder to analyze",
                os.path.join("C:", os.sep, "Users", unicode(os.environ['USERNAME']), "Desktop"),
                QtGui.QFileDialog.DontUseNativeDialog | QtGui.QFileDialog.ShowDirsOnly | QtGui.QFileDialog.ReadOnly
            )

            dialog_input_path = unicode(dialog_input_path)

            # Checking if selected path is valid for selected browser
            valid_other_path = browsers_utils.check_valid_cache_path(
                browser=self.matching_browser_key,
                cache_path=dialog_input_path
            )

            # Selected path to analyze is correct
            if valid_other_path:
                # Setting "current input path" as selected path from QDialog
                self.current_input_path = dialog_input_path

                self.line_input_path_folder_screen.setText(self.current_input_path.replace("/", "\\"))
                self.line_input_path_folder_screen.home(False)
            # Selected path to analyze is not correct

            else:
                # Path is selected but not correct
                if dialog_input_path:

                    if self.browser_is_portable:
                        browser_name = self.matching_browser_key.capitalize()
                    else:
                        # Browser name from table
                        browser_name = self.selection_table_installed_browsers[0].text()

                    QtGui.QMessageBox.warning(
                        QtGui.QMessageBox(), "Wrong input path",
                        "{path} <br> is not correct for ''{browser}''".format(
                            path=dialog_input_path.replace("/", "\\"),
                            browser=browser_name
                        ),
                        QtGui.QMessageBox.Ok
                    )

                # No selected path to analyze
                else:
                    QtGui.QMessageBox.information(
                        QtGui.QMessageBox(), "No selected path",
                        "Seems you did not select an input folder. <br> Please selected one",
                        QtGui.QMessageBox.Ok
                    )

        # Selected cache path info
        if self.current_input_path:
            # Info for current selected input path
            folder_info = utils.get_folder_info(folder_path=self.current_input_path)

            self.line_folder_dimension.setText(str(folder_info["folder_dimension"]))
            self.line_folder_elements.setText(str(folder_info["folder_elements"]))
            self.line_folder_creation_time.setText(str(folder_info["folder_creation_time"]))
            self.line_folder_last_modified_time.setText(str(folder_info["folder_last_modified_time"]))
            self.line_folder_last_access_time.setText(str(folder_info["folder_last_access_time"]))

            for item in self.groupBox_input_folder_preview.findChildren((QtGui.QListWidget, QtGui.QLineEdit)):
                item.clear()
            self.list_input_folder_preview.addItems(os.listdir(self.current_input_path))

            self.button_confirm_analysis.setEnabled(True)

    def get_file_info(self):
        """Slot for "list_input_folder_preview" in "folder choice screen".
        Retrieving info about selected file from the list widget.
        :return: nothing
        """

        # Selected item from "list_input_folder" list widget
        selected_item = unicode(self.list_input_folder_preview.selectedItems()[0].text())
        file_path = os.path.join(self.current_input_path, selected_item)

        try:
            # Selected file info
            file_info = utils.get_file_info(file_path=file_path)

            self.line_file_selected.setText(selected_item)
            self.line_file_dimension.setText(str(file_info["file_dimension"]))
            self.line_file_md5.setText(str(file_info["file_md5"]))
            self.line_file_sha1.setText(str(file_info["file_sha1"]))
            self.line_file_creation_time.setText(str(file_info["file_creation_time"]))
            self.line_file_last_modified.setText(str(file_info["file_last_modified_time"]))
            self.line_file_last_access.setText(str(file_info["file_last_access_time"]))

        except Exception as _:
            QtGui.QMessageBox.critical(
                QtGui.QMessageBox(), "Error", "Unable to open file <br> ''{item}''".format(item=selected_item),
                QtGui.QMessageBox.Ok
            )


############################
# SECTION: ANALYSIS SCREEN #
############################

    def set_analysis_screen(self):
        """Slot for "button_confirm_analysis" in "input folder screen".
        "Analysis screen": stacked widget index = 3, "table_analysis_preview" with preview of results from scan.
        :return: nothing
        """

        self.stackedWidget.setCurrentIndex(4)

        # Already visited "analysis screen"
        self.progressBar_analysis.reset()
        self.table_analysis_preview.setRowCount(0)

        self.line_input_path_analysis.setText(self.current_input_path.replace("/", "\\"))
        self.button_export_to_html.setEnabled(False)
        self.button_analysis_screen_back.setEnabled(False)
        self.button_stop_analysis.setEnabled(True)
        self.button_quit_analysis_screen.setEnabled(False)

        # Clipboard to store copied values from "table_analysis_preview"
        self.clipboard = QtGui.QApplication.clipboard()

        # Chrome threads
        if self.matching_browser_key == "chrome":
            # Columns and header for "table_analysis_preview"
            self.table_analysis_preview.setHorizontalHeaderLabels(
                ['Key Hash', 'Key URL', 'Content Type', 'Creation Time'])

            # Analyzer thread and worker
            self.chrome_analyzer_thread = QtCore.QThread()
            self.chrome_analyzer_worker = browsers.chrome.chrome_analyzer.ChromeAnalyzer(
                input_path=self.current_input_path
            )
            self.chrome_analyzer_worker.moveToThread(self.chrome_analyzer_thread)

            # Analyzer thread and worker signals connections
            self.chrome_analyzer_thread.started.connect(self.chrome_analyzer_worker.analyze_cache)
            self.chrome_analyzer_worker.signal_finished.connect(self.chrome_analyzer_thread.quit)
            self.chrome_analyzer_worker.signal_finished.connect(self.chrome_analyzer_worker.deleteLater)
            self.chrome_analyzer_thread.finished.connect(self.chrome_analyzer_thread.deleteLater)
            self.chrome_analyzer_thread.finished.connect(self.analysis_terminated)
            self.chrome_analyzer_worker.signal_update_table_preview.connect(self.update_table_preview)
            self.current_analyzer_thread = self.chrome_analyzer_thread
            self.current_analyzer_worker = self.chrome_analyzer_worker
            self.current_analyzer_thread.start()

        # Firefox threads
        elif self.matching_browser_key == "firefox":
            # Columns and header for "table_analysis_preview"
            self.table_analysis_preview.setHorizontalHeaderLabels(['Key Hash', 'URI', 'Content-Type', 'Expire Date'])

            # Analyzer thread and worker
            self.firefox_analyzer_thread = QtCore.QThread()
            self.firefox_analyzer_worker = browsers.firefox.firefox_analyzer.FirefoxAnalyzer(
                input_path=self.current_input_path
            )
            self.firefox_analyzer_worker.moveToThread(self.firefox_analyzer_thread)

            # Analyzer thread and worker signals connections
            self.firefox_analyzer_thread.started.connect(self.firefox_analyzer_worker.analyze_cache)
            self.firefox_analyzer_worker.signal_finished.connect(self.firefox_analyzer_thread.quit)
            self.firefox_analyzer_worker.signal_finished.connect(self.firefox_analyzer_worker.deleteLater)
            self.firefox_analyzer_thread.finished.connect(self.firefox_analyzer_thread.deleteLater)
            self.firefox_analyzer_thread.finished.connect(self.analysis_terminated)
            self.firefox_analyzer_worker.signal_update_table_preview.connect(self.update_table_preview)
            self.current_analyzer_thread = self.firefox_analyzer_thread
            self.current_analyzer_worker = self.firefox_analyzer_worker
            self.current_analyzer_thread.start()

        # Opera threads
        elif self.matching_browser_key == "opera":
            # Columns and header for "table_analysis_preview"
            self.table_analysis_preview.setHorizontalHeaderLabels(
                ['Key Hash', 'Key URL', 'Content Type', 'Creation Time'])

            # Analyzer thread and worker
            self.opera_analyzer_thread = QtCore.QThread()
            self.opera_analyzer_worker = browsers.opera.opera_analyzer.OperaAnalyzer(
                input_path=self.current_input_path
            )
            self.opera_analyzer_worker.moveToThread(self.opera_analyzer_thread)

            # Analyzer thread and worker signals connections
            self.opera_analyzer_thread.started.connect(self.opera_analyzer_worker.analyze_cache)
            self.opera_analyzer_worker.signal_finished.connect(self.opera_analyzer_thread.quit)
            self.opera_analyzer_worker.signal_finished.connect(self.opera_analyzer_worker.deleteLater)
            self.opera_analyzer_thread.finished.connect(self.opera_analyzer_thread.deleteLater)
            self.opera_analyzer_thread.finished.connect(self.analysis_terminated)
            self.opera_analyzer_worker.signal_update_table_preview.connect(self.update_table_preview)
            self.current_analyzer_thread = self.opera_analyzer_thread
            self.current_analyzer_worker = self.opera_analyzer_worker
            self.current_analyzer_thread.start()

    def update_table_preview(self, idx_elem, tot_elem, key_hash, key_url, content_type, time):
        """Slot for "signal_update_table_preview" from "chrome_analyzer_worker".
        Updating table with results from "chroma_analyzer_worker"
        :param idx_elem: position of the element in list of found cache entry instances
        :param tot_elem: number of entries in "index" file header
        :param key_hash: hash of the key in found cache entry
        :param key_data: data in cache entry
        :param content_type: content type for the data in cache entry
        :param creation_time: cache entry creation time
        :return: nothing
        """
        # Cache entry values in "table analysis preview"
        self.table_analysis_preview.insertRow(idx_elem)
        self.table_analysis_preview.setItem(idx_elem, 0, QtGui.QTableWidgetItem(key_hash))
        self.table_analysis_preview.setItem(idx_elem, 1, QtGui.QTableWidgetItem(key_url))
        self.table_analysis_preview.setItem(idx_elem, 2, QtGui.QTableWidgetItem(content_type))
        self.table_analysis_preview.setItem(idx_elem, 3, QtGui.QTableWidgetItem(time))

        self.table_analysis_preview.scrollToBottom()

        # Copying "cache_entries_list" from "chrome_analyzer_thread" to avoid rescan for html export (if any)
        self.list_found_cache_entries = self.current_analyzer_worker.list_cache_entries[:]

        # "ProgressBar_analysis" value
        value = float(100 * len(self.list_found_cache_entries)) / float(tot_elem)
        self.progressBar_analysis.setValue(value)

    def table_analysis_preview_context_menu(self, position):
        """Slot for "customContextMenuRequested" on "table_analysis_preview".
        Right mouse click on table to open a context menu for advanced options.
        :param position: event position on the "table_analysis_preview
        :return:
        """

        # Context menu enabled
        if self.context_menu_enabled:
            # Context menu
            menu = QtGui.QMenu()
            action_copy_to_clipboard = menu.addAction("Copy item to clipboard")
            action_advanced_results = menu.addAction("Show advanced results")
            action = menu.exec_(self.table_analysis_preview.mapToGlobal(position))

            # Copy element
            if action == action_copy_to_clipboard:
                selection = self.table_analysis_preview.currentItem().text()
                self.clipboard.clear()
                self.clipboard.setText(selection)
                QtGui.QMessageBox.information(
                    QtGui.QMessageBox(), "Clipboard",
                    "{selection}\n\nElement copied to clipboard".format(selection=selection),
                    QtGui.QMessageBox.Ok
                )

            # Advanced results
            if action == action_advanced_results:
                # Retrieving selected item from "table_analysis_preview"
                # Position in results list = table row
                current_table_row = self.table_analysis_preview.currentRow()
                current_result_item = self.list_found_cache_entries[current_table_row]

                # Entry preview
                if self.matching_browser_key == "chrome":
                    self.browser_preview_dialog = browsers_dialogs.chrome_preview_dialog.ChromePreviewDialog(
                        entry=current_result_item
                    )

                elif self.matching_browser_key == "firefox":
                    self.browser_preview_dialog = browsers_dialogs.firefox_preview_dialog.FirefoxPreviewDialog(
                        entry=current_result_item
                    )
                elif self.matching_browser_key == "opera":
                    self.browser_preview_dialog = browsers_dialogs.opera_preview_dialog.OperaPreviewDialog(
                        entry=current_result_item
                    )

                self.browser_preview_dialog.exec_()

    def stop_analysis(self):
        """Slot for "button_stop_analysis" in "analysis screen".
        Setting a stop signal for "chrome_analyzer_worker".
        :return: nothing
        """

        self.current_analyzer_worker.signal_stop.set()

    def analysis_terminated(self):
        """Slot for signal "finished" from "chrome_analyzer_thread".
        A message box will confirm if analysis normally terminated or stopped by user.
        :return: nothing
        """

        # Enabling context menu on "table_analysis_preview"
        self.context_menu_enabled = True

        if self.browser_is_portable:
            browser_name = self.matching_browser_key.capitalize()
        else:
            # Browser name from selection in "table_installed_browsers"
            browser_name = self.selection_table_installed_browsers[0].text()

        # Analysis stopped by user
        if self.current_analyzer_worker.stopped_by_user:
            QtGui.QMessageBox.warning(
                QtGui.QMessageBox(), "Analysis stopped",
                "Analysis for {browser} stopped by user".format(browser=browser_name),
                QtGui.QMessageBox.Ok
            )

            # "Analysis screen" buttons settings
            self.button_analysis_screen_back.setEnabled(True)
            self.button_stop_analysis.setEnabled(False)
            self.button_quit_analysis_screen.setEnabled(True)

        # Analysis normal termination
        else:
            QtGui.QMessageBox.information(
                QtGui.QMessageBox(), "Analysis terminated",
                "Analysis for {browser} successfully terminated".format(browser=browser_name),
                QtGui.QMessageBox.Ok
            )

            # "Analysis screen" buttons settings
            self.button_analysis_screen_back.setEnabled(True)
            self.button_stop_analysis.setEnabled(False)
            self.button_export_to_html.setEnabled(True)
            self.button_quit_analysis_screen.setEnabled(True)


###########################
# SECTION: EXPORT TO HTML #
###########################

    def export_to_html(self):
        """Slot for button_export_to_html" in analysis screen.
        Export screen = stacked widget index = 4 and showing progress of exporting.
        :return: nothing
        """

        # Output path for export
        dialog_output_path = QtGui.QFileDialog().getExistingDirectory(
            self, "Select an output folder for export",
            os.path.join("C:", os.sep, "Users", unicode(os.environ['USERNAME']), "Desktop"),
            QtGui.QFileDialog.ShowDirsOnly
        )

        # Convert QString from QDialog to unicode
        self.current_export_path = unicode(dialog_output_path)

        # Selected output path for export
        if self.current_export_path:

            self.stackedWidget.setCurrentIndex(5)

            # Export screen settings
            self.button_home.setEnabled(False)
            self.button_show_folder.setEnabled(False)
            self.button_quit_export_screen.setEnabled(False)
            self.button_stop_export.setEnabled(False)
            self.progressBar_export.reset()

            current_datetime = datetime.datetime.now().strftime("%d-%b-%Y-%H_%M_%S")
            export_folder_name = "BrowserCacheAnalyzer-Export[{date}]".format(date=current_datetime)
            self.export_folder_path = os.path.join(self.current_export_path, export_folder_name)

            # Creating export main folder
            try:
                os.makedirs(self.export_folder_path)
            except:
                QtGui.QMessageBox.warning(
                    QtGui.QMessageBox(), "Export folder",
                    "Unable to create \n{folder}".format(folder=self.export_folder_path),
                    QtGui.QMessageBox.Ok
                )

            self.line_input_path_export.setText(self.current_input_path.replace("/", "\\"))
            self.line_output_path_export.setText(self.export_folder_path)

            # Generating random MD5 and SHA1 for the export
            export_md5 = utils.create_random_hash()['random_md5']
            export_sha1 = utils.create_random_hash()['random_sha1']

            if self.browser_is_portable:
                browser_info = [self.matching_browser_key.capitalize(), "Not available", "Not available", "Not available"]
                browser_default_path = "Not available"
            else:
                browser_info = self.selection_table_installed_browsers
                browser_default_path = self.default_cache_path

            # Chrome threads
            if self.matching_browser_key == "chrome":
                # Exporter thread and worker
                self.chrome_exporter_thread = QtCore.QThread()
                self.chrome_exporter_worker = browsers.chrome.chrome_exporter.ChromeExporter(
                    input_path=self.current_input_path,
                    export_path=self.current_export_path,
                    export_folder_name=export_folder_name,
                    entries_to_export=self.list_found_cache_entries,
                    browser_portable=self.browser_is_portable,
                    browser_info=browser_info,
                    browser_def_path=browser_default_path,
                    export_md5=export_md5,
                    export_sha1=export_sha1
                )

                self.chrome_exporter_worker.moveToThread(self.chrome_exporter_thread)

                # Exporter thread and worker signals connections
                self.chrome_exporter_thread.started.connect(self.chrome_exporter_worker.exporter)
                self.chrome_exporter_worker.signal_finished.connect(self.chrome_exporter_thread.quit)
                self.chrome_exporter_worker.signal_finished.connect(self.chrome_exporter_worker.deleteLater)
                self.chrome_exporter_thread.finished.connect(self.chrome_exporter_thread.deleteLater)
                self.chrome_exporter_worker.signal_update_export.connect(self.update_export_progress)
                self.chrome_exporter_thread.finished.connect(self.export_terminated)
                self.chrome_exporter_worker.signal_enable_stop_button.connect(self.enable_stop_export_button)
                self.current_exporter_thread = self.chrome_exporter_thread
                self.current_exporter_worker = self.chrome_exporter_worker
                self.current_exporter_thread.start()

            elif self.matching_browser_key == "firefox":
                # Exporter thread and worker
                self.firefox_exporter_thread = QtCore.QThread()
                self.firefox_exporter_worker = browsers.firefox.firefox_exporter.FirefoxExporter(
                    input_path=self.current_input_path,
                    export_path=self.current_export_path,
                    export_folder_name=export_folder_name,
                    entries_to_export=self.list_found_cache_entries,
                    browser_portable=self.browser_is_portable,
                    browser_info=browser_info,
                    browser_def_path=browser_default_path,
                    export_md5=export_md5,
                    export_sha1=export_sha1
                )

                self.firefox_exporter_worker.moveToThread(self.firefox_exporter_thread)

                # Exporter thread and worker signals connections
                self.firefox_exporter_thread.started.connect(self.firefox_exporter_worker.exporter)
                self.firefox_exporter_worker.signal_finished.connect(self.firefox_exporter_thread.quit)
                self.firefox_exporter_worker.signal_finished.connect(self.firefox_exporter_worker.deleteLater)
                self.firefox_exporter_thread.finished.connect(self.firefox_exporter_thread.deleteLater)
                self.firefox_exporter_worker.signal_update_export.connect(self.update_export_progress)
                self.firefox_exporter_thread.finished.connect(self.export_terminated)
                self.firefox_exporter_worker.signal_enable_stop_button.connect(self.enable_stop_export_button)
                self.current_exporter_thread = self.firefox_exporter_thread
                self.current_exporter_worker = self.firefox_exporter_worker
                self.current_exporter_thread.start()

            # Opera threads
            elif self.matching_browser_key == "opera":
                # Exporter thread and worker
                self.opera_exporter_thread = QtCore.QThread()
                self.opera_exporter_worker = browsers.opera.opera_exporter.OperaExporter(
                    input_path=self.current_input_path,
                    export_path=self.current_export_path,
                    export_folder_name=export_folder_name,
                    entries_to_export=self.list_found_cache_entries,
                    browser_portable=self.browser_is_portable,
                    browser_info=browser_info,
                    browser_def_path=browser_default_path,
                    export_md5=export_md5,
                    export_sha1=export_sha1
                )

                self.opera_exporter_worker.moveToThread(self.opera_exporter_thread)

                # Exporter thread and worker signals connections
                self.opera_exporter_thread.started.connect(self.opera_exporter_worker.exporter)
                self.opera_exporter_worker.signal_finished.connect(self.opera_exporter_thread.quit)
                self.opera_exporter_worker.signal_finished.connect(self.opera_exporter_worker.deleteLater)
                self.opera_exporter_thread.finished.connect(self.opera_exporter_thread.deleteLater)
                self.opera_exporter_worker.signal_update_export.connect(self.update_export_progress)
                self.opera_exporter_thread.finished.connect(self.export_terminated)
                self.opera_exporter_worker.signal_enable_stop_button.connect(self.enable_stop_export_button)
                self.current_exporter_thread = self.opera_exporter_thread
                self.current_exporter_worker = self.opera_exporter_worker
                self.current_exporter_thread.start()

        # Not selected output path for export
        else:
            QtGui.QMessageBox.information(
                QtGui.QMessageBox(), "No selected folder",
                "Seems you did not select an output folder. <br> Please selected one", QtGui.QMessageBox.Ok
            )

    def enable_stop_export_button(self):
        """Slot for "signal_enable_stop_button" in "chrome_exporter_worker".
        Enabling stop button if export started.
        :return: nothing
        """
        self.button_stop_export.setEnabled(True)

    def update_export_progress(self, exported_entries=None, tot_entries=None):
        """Slot for "signal_update_export" in "chrome_exporter_worker".
        Updating export progress.
        :param exported_entries: entries exported
        :param tot_entries: total extries to export
        :return: nothing
        """

        value = float(100 * exported_entries) / float(tot_entries)
        self.progressBar_export.setValue(value)

    def stop_export(self):
        """Slot for "button_stop_export" in "export screen".
        Setting a stop signal for "chrome_exporter_worker".
        :return: nothing
        """

        self.current_exporter_worker.signal_stop.set()

    def export_terminated(self):
        """Slot for signal "finished" from "chrome_exporter_thread".
        A message box will confirm if export normally terminated or stopped by user.
        :return: nothing
        """

        if self.browser_is_portable:
            browser_name = self.matching_browser_key.capitalize()
        else:
            # Browser name from selection in "table_installed_browsers"
            browser_name = self.selection_table_installed_browsers[0].text()

        # Analysis stopped by user
        if self.current_exporter_worker.stopped_by_user:
            QtGui.QMessageBox.warning(
                QtGui.QMessageBox(), "Export stopped",
                "Export for {browser} stopped by user".format(browser=browser_name),
                QtGui.QMessageBox.Ok
            )

            # Deleting export folder
            shutil.rmtree(self.export_folder_path, ignore_errors=True)
            QtGui.QMessageBox.information(
                QtGui.QMessageBox(), "Deleted folder",
                "{folder} deleted after stop export".format(folder=self.export_folder_path),
                QtGui.QMessageBox.Ok
            )

            # "Export screen" buttons settings
            self.button_home.setEnabled(True)
            self.button_stop_export.setEnabled(False)
            self.button_quit_export_screen.setEnabled(True)

        # Export normal termination
        else:
            QtGui.QMessageBox.information(
                QtGui.QMessageBox(), "Export terminated",
                "Export for {browser} successfully terminated".format(browser=browser_name),
                QtGui.QMessageBox.Ok
            )

            # "Export screen" buttons settings
            self.button_home.setEnabled(True)
            self.button_stop_export.setEnabled(False)
            self.button_quit_export_screen.setEnabled(True)
            self.button_show_folder.setEnabled(True)

    def show_export_folder(self):
        """Slot for "button_show_folder" in export screen.
        Opening export folder after export termination.
        :return: nothing
        """

        os.startfile(self.export_folder_path)


##############################
# SECTION: CLOSE APPLICATION #
##############################

    def close_application(self):
        """Slot for "button_close_application".
        A message box will ask to confirm before quitting normally or during an analysis or export.
        :return: nothing
        """

        # Analysis is still running
        if self.current_analyzer_worker and self.current_analyzer_worker.worker_is_running:

            if self.browser_is_portable:
                browser_name = self.matching_browser_key.capitalize()
            else:
                browser_name = self.selection_table_installed_browsers[0].text()

            # Asking for closing on running analysis
            msg_quit_analysis = QtGui.QMessageBox.warning(
                QtGui.QMessageBox(), "Analysis running",
                "Analysis for {browser} is still running. Quit?".format(browser=browser_name),
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No
            )

            # Quitting application
            if msg_quit_analysis == QtGui.QMessageBox.Yes:
                self.deleteLater()

        # Export is still running
        elif self.current_exporter_worker and self.current_exporter_worker.worker_is_running:

            if self.browser_is_portable:
                browser_name = self.matching_browser_key.capitalize()
            else:
                browser_name = self.selection_table_installed_browsers[0].text()

            # Asking for closing on running export
            msg_quit_export = QtGui.QMessageBox.warning(
                QtGui.QMessageBox(), "Export running",
                "Export for {browser} is still running. Quit?".format(browser=browser_name),
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No
            )

            # Quitting application
            if msg_quit_export == QtGui.QMessageBox.Yes:
                self.deleteLater()

        # Analysis or export terminated or stopped by user
        else:
            # Confirmation before quitting
            msg_confirm_exit = QtGui.QMessageBox.question(
                QtGui.QMessageBox(), "Confirm", "Are you sure you want to quit?",
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                QtGui.QMessageBox.No)

            # Quitting application
            if msg_confirm_exit == QtGui.QMessageBox.Yes:
                self.deleteLater()


######################################################################
# SECTION: MOUSE METHODS OVERRIDE (Application window drag and drop) #
######################################################################

    def mousePressEvent(self, event):
        """ Override for QtGui.QWidget.mousePressEvent to calculate mouse position at click.
        Event position is relative to the application window.
        :param event: QtGui.QMouseEvent
        :return: nothing
        """

        # Mouse cursor coordinates relative to the application window
        self.mouse_press_position = event.pos()

    def mouseMoveEvent(self, event):
        """ Override for QtGui.QWidget.mouseMoveEvent to drag the application window.
        Event buttons indicates the button state when the event was generated.
        Event position is the global position of the mouse cursor at the time of the event.
        :param event: QtGui.QMouseEvent
        :return: nothing
        """

        # Application window move (with mouse left button)
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.mouse_press_position)


#########################
# SECTION: EVENT FILTER #
#########################

    def eventFilter(self, q_object, q_event):
        """
        Filters events if this object has been installed as an event filter for the watched object.
        :param q_object: QObject
        :param q_event: QEvent
        :return: eventFilter(q_object, q_event)
        """

        # Mouse hover enter event
        if q_event.type() == QtCore.QEvent.HoverEnter:
            # "GroupBox_system_info"
            if q_object in self.groupBox_system_info.findChildren(QtGui.QLineEdit):
                QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
            # "GroupBox_selected_browser_info"
            elif q_object in self.groupBox_selected_browser_info.findChildren(QtGui.QLineEdit):
                QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
            # "GroupBox_installed_browsers"
            elif q_object == self.groupBox_installed_browsers:
                QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            # "Lines edit" in "groupBox_input_folder"
            elif q_object in self.groupBox_input_folder.findChildren(QtGui.QLineEdit):
                if not q_object.text().isEmpty():
                    QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
            # "Lines edit" in "groupBox_input_folder"
            elif q_object in self.groupBox_input_folder_preview.findChildren(QtGui.QLineEdit):
                if not q_object.text().isEmpty():
                    QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
            # "Line_input_path_analysis"
            elif q_object == self.line_input_path_analysis:
                QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
            # "Lines edit" in "groupBox_export"
            elif q_object == self.line_input_path_export or q_object == self.line_output_path_export:
                QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))

        # Mouse hover leave event
        elif q_event.type() == QtCore.QEvent.HoverLeave:
            QtGui.QApplication.restoreOverrideCursor()

        elif q_event.type() == QtCore.QEvent.MouseButtonRelease:
            QtGui.QApplication.restoreOverrideCursor()

        # Pass the event on to the parent class
        return QtGui.QMainWindow.eventFilter(self, q_object, q_event)


###############################################################################
# SECTION: BROWSER ICON WIDGET (Browsers icons in "table_installed_browsers") #
###############################################################################

class BrowserIconWidget(QtGui.QLabel):
    """
    Selection for browser icon in "table_installed_browsers".
    Setting a Browser Icon Widget for the first column of "table-installed_browsers", selecting the right icon
    according to the browser name.
    :param icon_name: browser name from "list_installed_browsers"
    """

    def __init__(self, parent=None, icon_name=None):
        super(BrowserIconWidget, self).__init__(parent)

        # Icon center alignment
        self.setAlignment(QtCore.Qt.AlignCenter)

        # Setting browser icon
        icon_path = os.path.join(utils.ICONS_PATH, "{name}.png".format(name=icon_name))
        browser_icon = QtGui.QPixmap(icon_path)
        self.setPixmap(browser_icon)
