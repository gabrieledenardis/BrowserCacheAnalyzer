# -*- coding: utf-8 -*-
# !/usr/bin/env python

# PyQt4 imports
from PyQt4 import QtGui
from PyQt4 import QtCore

# Python imports
import platform
import os


# Project imports
from gui import bca_converted_gui
from operating_systems import windows
from utilities import utils, browsers_utils


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

        # ********** Browsers screen ********** #

        # "Table_found_browsers"
        self.table_found_browsers.setColumnCount(4)
        self.table_found_browsers.setHorizontalHeaderLabels(['', 'Browser Name', 'Version', 'Installation Path'])
        self.table_found_browsers.setColumnWidth(0, len("Icon") + 50)
        self.table_found_browsers.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.Stretch)
        self.table_found_browsers.horizontalHeader().setResizeMode(3, QtGui.QHeaderView.Stretch)
        self.table_found_browsers.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table_found_browsers.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.table_found_browsers.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table_found_browsers.setAlternatingRowColors(True)
        self.table_found_browsers.setToolTip("Click on a row to select a browser")


#######################
# SECTION: ATTRIBUTES #
#######################

        # Mouse cursor coordinates
        self.mouse_press_position = None
        # List of found browsers in the system
        self.list_found_browsers = []
        # Selection from "table_found_browsers"
        self.found_browsers_table_selection = None
        # Matching key for selected browser
        self.matching_browser_key = None
        # Default cache path for selected browser
        self.default_cache_path = None
        # Current selected path to analyze and current output path
        self.current_input_path = None
        self.current_output_path = None


##########################################
# SECTION: SIGNALS AND SLOTS CONNECTIONS #
##########################################

        # Connections for "minimize_application" and "close_application" buttons
        self.button_minimize_application.clicked.connect(self.showMinimized)
        self.button_close_application.clicked.connect(self.close_application)

        # Connections for other application elements
        self.button_search_browsers.clicked.connect(self.set_browsers_screen)
        self.table_found_browsers.itemClicked.connect(self.show_installation_folder_info)
        self.button_browsers_screen_select.clicked.connect(self.set_input_folder_screen)
        self.button_analyze_default_path.clicked.connect(self.select_input_path)
        self.button_analyze_other_path.clicked.connect(self.select_input_path)
        self.list_input_folder_preview.itemClicked.connect(self.get_file_info)
        self.button_input_folder_screen_back.clicked.connect(self.set_browsers_screen)


###########################
# SECTION: WELCOME SCREEN #
###########################

        # Welcome screen settings
        self.stackedWidget.setCurrentIndex(0)
        self.groupBox_selected_browser_info.setVisible(False)
        self.label_application_title.setVisible(False)
        self.label_application_icon.setVisible(False)
        self.groupBox_system_info.setVisible(False)


############################
# SECTION: BROWSERS SCREEN #
############################

    def set_browsers_screen(self):
        """Slot for "button_search_browsers" in "welcome screen" and "button_input_folder_screen_back"
        in "input folder screen" .
        "Browsers screen": stacked widget index = 1, visible "groupBox_system_info" with system values,
        not visible "groupBox_selected_browser_info" and "table_found_browsers" containing found browsers
        in the system.
        :return: nothing
        """

        # Browsers screen settings
        self.stackedWidget.setCurrentIndex(1)
        self.label_application_title.setVisible(True)
        self.label_application_icon.setVisible(True)
        self.groupBox_system_info.setVisible(True)
        self.groupBox_selected_browser_info.setVisible(False)
        self.button_browsers_screen_select.setEnabled(False)

        # If back from "input folder screen"
        self.table_found_browsers.setRowCount(0)
        for line in self.groupBox_install_folder_info.findChildren(QtGui.QLineEdit):
            line.clear()

        # System values
        self.line_system_os_name.setText(platform.system())
        self.line_system_release.setText(platform.release())
        self.line_system_release_version.setText(platform.version())
        self.line_system_hostname.setText(platform.node())

        # Searching for browsers (depending on OS)
        # Microsoft Windows
        if "windows" in platform.system().lower():
            self.list_found_browsers = windows.browsers_finder.finder()
        # TODO: Code for other OSs

        # "Table_found_browsers"
        for idx, brw in enumerate(self.list_found_browsers):
            self.table_found_browsers.insertRow(idx)

            # Browser values
            icon_name = brw[0]
            browser_name = brw[1]
            version = brw[2]
            browser_inst_path = brw[3]

            self.table_found_browsers.setCellWidget(idx, 0, BrowserIconWidget(icon_name=icon_name))
            self.table_found_browsers.setItem(idx, 1, QtGui.QTableWidgetItem(browser_name))
            self.table_found_browsers.setItem(idx, 2, QtGui.QTableWidgetItem(version))
            self.table_found_browsers.setItem(idx, 3, QtGui.QTableWidgetItem(browser_inst_path))

    def show_installation_folder_info(self):
        """Slot for selection on "found_browsers_table".
        Showing installation folder info for selected browser and enabling "button_browsers_screen_select".
        :return: nothing
        """

        # Getting selection from table and enabling button
        self.found_browsers_table_selection = self.table_found_browsers.selectedItems()
        if self.found_browsers_table_selection:
            self.button_browsers_screen_select.setEnabled(True)

        # Installation folder info for selected browser
        folder_path = str(self.found_browsers_table_selection[2].text())
        folder_info = utils.get_folder_info(folder_path=folder_path)

        self.line_inst_folder_dimension.setText(str(folder_info['folder_dimension']))
        self.line_inst_folder_elements.setText(str(folder_info['folder_elements']))
        self.line_inst_folder_creation_time.setText(str(folder_info['folder_creation_time']))
        self.line_inst_folder_modified_time.setText(str(folder_info['folder_last_modified_time']))
        self.line_inst_folder_access_time.setText(str(folder_info['folder_last_access_time']))


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

        # "Button_browsers_screen_select" button in "browser screen"
        if clicked_button == "button_browsers_screen_select":
            # Values for selection from table
            browser_name = self.found_browsers_table_selection[0].text()
            browser_version = self.found_browsers_table_selection[1].text()
            browser_install_path = self.found_browsers_table_selection[2].text()

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
                self.stackedWidget.setCurrentIndex(2)
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

            self.line_analysis_input_path.setText(self.current_input_path)
            self.line_analysis_input_path.home(False)
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

                self.line_analysis_input_path.setText(self.current_input_path.replace("/", "\\"))
                self.line_analysis_input_path.home(False)
            # Selected path to analyze is not correct
            else:
                # Path is selected but not correct
                if dialog_input_path:
                    # Browser name from table
                    browser = self.found_browsers_table_selection[0].text()

                    QtGui.QMessageBox.warning(
                        QtGui.QMessageBox(), "Wrong input path",
                        "{path} <br> is not correct for {browser}".format(
                            path=dialog_input_path.replace("/", "\\"),
                            browser=browser
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
                QtGui.QMessageBox(), "Error", "Unable to open file <br> {item}".format(item=selected_item),
                QtGui.QMessageBox.Ok
            )


##############################
# SECTION: CLOSE APPLICATION #
##############################

    def close_application(self):
        """Slot for "button_close_application".
        A message box will ask to confirm before quitting.
        :return: nothing
        """

        # Confirmation before quitting
        msg_confirm_exit = QtGui.QMessageBox.question(
            QtGui.QMessageBox(), "Confirm", "Are you sure you want to quit?",
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
            QtGui.QMessageBox.No)

        # Quitting application
        if msg_confirm_exit == QtGui.QMessageBox.Yes:
            self.close()


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


###########################################################################
# SECTION: BROWSER ICON WIDGET (Browsers icons in "table found browsers") #
###########################################################################

class BrowserIconWidget(QtGui.QLabel):
    """
    Selection for browser icon in "table found browsers".
    Setting a Browser Icon Widget for the first column of "table found browsers", selecting the right icon according
    to the browser name.
    :param icon_name: browser name from "found browser list"
    """

    def __init__(self, parent=None, icon_name=None):
        super(BrowserIconWidget, self).__init__(parent)

        # Icon center alignment
        self.setAlignment(QtCore.Qt.AlignCenter)

        # Setting browser icon
        icon_path = os.path.join(utils.ICONS_PATH, "{name}.png".format(name=icon_name))
        browser_icon = QtGui.QPixmap(icon_path)
        self.setPixmap(browser_icon)
