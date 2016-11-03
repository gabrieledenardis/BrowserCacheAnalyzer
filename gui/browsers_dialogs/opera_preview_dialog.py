# -*- coding: utf-8 -*-
# !/usr/bin/env python

# PyQt4 imports
from PyQt4 import QtGui, QtCore

# Project imports
import opd_converted_gui


class OperaPreviewDialog(QtGui.QDialog, opd_converted_gui.Ui_OperaPreviewDialog):

    def __init__(self, parent=None, entry=None):
        super(OperaPreviewDialog, self).__init__(parent)

        # Setting up the application user interface from python converted gui
        self.setupUi(self)


##########################################
# SECTION: APPLICATION ELEMENTS SETTINGS #
##########################################

        # QDialog and buttons
        self.setStyleSheet("background-color: rgb(225,225,225) ")
        self.label_dialog_title.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        for button in self.findChildren(QtGui.QPushButton):
            button.setStyleSheet("QPushButton {background-color: transparent; border: 1px solid darkgray}"
                                 "QPushButton:hover {background-color: rgb(192,192,192)}")

        # Lines edit
        for line in self.findChildren(QtGui.QLineEdit):
            line.installEventFilter(self)
            line.setReadOnly(True)
            line.setFrame(False)


#######################
# SECTION: ATTRIBUTES #
#######################

        # Values for selected item
        self.label_dialog_title.setText(str(entry.key_hash))
        self.line_key_hash.setText(str(entry.key_hash))
        self.line_next_entry_address.setText(str(entry.next_entry_address))
        self.line_reuse_count.setText(str(entry.reuse_count))
        self.line_refetch_count.setText(str(entry.refetch_count))
        self.line_entry_state.setText(str(entry.entry_state))
        self.line_creation_time.setText(str(entry.creation_time))
        self.line_key_data_size.setText(str(entry.key_data_size))
        self.line_long_key_address.setText(str(entry.long_key_data_address))
        self.line_cache_entry_flags.setText(str(entry.cache_entry_flags))
        self.line_key_data.setText(str(entry.key_data))
        self.line_key_data.home(False)

        # Mouse cursor coordinates on left click over the dialog
        self.mouse_press_position = None

        # Frameless window
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # Closing QDialog on "button close" click
        self.button_close_dialog.clicked.connect(self.close)


######################################################################
# SECTION: MOUSE METHODS OVERRIDE (Application window drag and drop) #
######################################################################

    def mousePressEvent(self, event):

        """
        Override for QtGui.QWidget.mousePressEvent to calculate mouse position at click.
        Event position is relative to the application window.
        :param event: QtGui.QMouseEvent
        :return:
        """

        # Mouse cursor coordinates relative to the application window
        self.mouse_press_position = event.pos()

    def mouseMoveEvent(self, event):
        """
        Override for QtGui.QWidget.mouseMoveEvent to drag the application window.
        Event buttons indicates the button state when the event was generated.
        Event position is the global position of the mouse cursor at the time of the event.
        :param event: QtGui.QMouseEvent
        :return:
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
            if q_object in self.findChildren(QtGui.QLineEdit):
                QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))

        # Mouse hover leave event
        elif q_event.type() == QtCore.QEvent.HoverLeave:
            QtGui.QApplication.restoreOverrideCursor()

        elif q_event.type() == QtCore.QEvent.MouseButtonRelease:
            QtGui.QApplication.restoreOverrideCursor()

        # Pass the event on to the parent class
        return QtGui.QMainWindow.eventFilter(self, q_object, q_event)
