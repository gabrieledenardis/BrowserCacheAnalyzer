# -*- coding: utf-8 -*-
# !/usr/bin/env python

# PyQt4 imports
from PyQt4 import QtCore
from PyQt4 import QtGui

# Python imports
import platform
import os


# Project imports
from gui import bca_converted_gui
from operating_systems import windows
from utilities import general_utils


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
        self.table_found_browsers.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.Stretch)
        self.table_found_browsers.horizontalHeader().setResizeMode(3, QtGui.QHeaderView.Stretch)
        self.table_found_browsers.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.table_found_browsers.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table_found_browsers.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table_found_browsers.setToolTip("Click on a row to select a browser")
        self.table_found_browsers.setColumnWidth(0, len("Icon") + 50)
        self.table_found_browsers.setAlternatingRowColors(True)

        # "Button_browsers_screen_select"
        self.button_browsers_screen_select.setEnabled(False)

#######################
# SECTION: ATTRIBUTES #
#######################

        # Mouse cursor coordinates on left click over the application window
        self.mouse_press_position = None
        # List of found browsers in the system
        self.list_found_browsers = []
        # Selection from "table_found_browsers"
        self.found_browsers_table_selection = None


##########################################
# SECTION: SIGNALS AND SLOTS CONNECTIONS #
##########################################

        # Connections for "minimize_application" and "close_application" buttons
        self.button_close_application.clicked.connect(self.close_application)
        self.button_minimize_application.clicked.connect(self.showMinimized)

        # Connections for other application elements
        self.button_search_browsers.clicked.connect(self.set_browsers_screen)
        self.table_found_browsers.itemClicked.connect(self.show_installation_folder_info)


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
        """Slot for "button_search_browsers" in "welcome screen".
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
        """ Slot for selection on "found_browsers_table".
        Showing installation folder info for selected browser and enabling "button_browsers_screen_select".
        :return: nothing
        """

        # Getting selection from table and enabling button
        self.found_browsers_table_selection = self.table_found_browsers.selectedItems()
        if self.found_browsers_table_selection:
            self.button_browsers_screen_select.setEnabled(True)

        # Installation folder info for selected browser
        folder_path = str(self.found_browsers_table_selection[2].text())
        folder_info = general_utils.get_folder_info(folder_path)

        self.line_inst_folder_dimension.setText(str(folder_info['folder_dimension']))
        self.line_inst_folder_elements.setText(str(folder_info['folder_elements']))
        self.line_inst_folder_creation_time.setText(str(folder_info['folder_creation_time']))
        self.line_inst_folder_modified_time.setText(str(folder_info['folder_last_modified_time']))
        self.line_inst_folder_access_time.setText(str(folder_info['folder_last_access_time']))


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
        icon_path = os.path.join(general_utils.ICONS_PATH, "{name}.png".format(name=icon_name))
        browser_icon = QtGui.QPixmap(icon_path)
        self.setPixmap(browser_icon)
