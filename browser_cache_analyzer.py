# -*- coding: utf-8 -*-
# !/usr/bin/env python

# PyQt4 imports
from PyQt4 import QtGui
from PyQt4 import QtCore

# Project imports
from gui import bca_converted_gui


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


#######################
# SECTION: ATTRIBUTES #
#######################

        # Mouse cursor coordinates on left click over the application window
        self.mouse_press_position = None


##########################################
# SECTION: SIGNALS AND SLOTS CONNECTIONS #
##########################################

        # Application "minimize" and "close" buttons
        self.button_close_application.clicked.connect(self.close_application)
        self.button_minimize_application.clicked.connect(self.showMinimized)


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
