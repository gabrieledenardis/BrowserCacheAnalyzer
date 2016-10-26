# -*- coding: utf-8 -*-
# !/usr/bin/env python

# PyQt4 imports
from PyQt4 import QtGui, QtCore

# Project imports
import cpd_converted_gui


class ChromePreviewDialog(QtGui.QDialog, cpd_converted_gui.Ui_ChromePreviewDialog):

    def __init__(self, parent=None, item=None):
        super(ChromePreviewDialog, self).__init__(parent)

        # Setting up the application user interface from python converted gui
        self.setupUi(self)

        # Values for selected item
        self.label_dialog_title.setText(str(item.key_hash))
        self.line_key_hash.setText(str(item.key_hash))
        self.line_next_entry_address.setText(str(item.next_entry_address))
        self.line_reuse_count.setText(str(item.reuse_count))
        self.line_refetch_count.setText(str(item.refetch_count))
        self.line_entry_state.setText(str(item.entry_state))
        self.line_creation_time.setText(str(item.creation_time))
        self.line_key_data_size.setText(str(item.key_data_size))
        self.line_long_key_address.setText(str(item.long_key_data_address))
        self.line_cache_entry_flags.setText(str(item.cache_entry_flags))
        self.line_key_data.setText(str(item.key_data))
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
