# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\browsers_dialogs\firefox_preview_dialog.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_FirefoxPreviewDialog(object):
    def setupUi(self, FirefoxPreviewDialog):
        FirefoxPreviewDialog.setObjectName(_fromUtf8("FirefoxPreviewDialog"))
        FirefoxPreviewDialog.resize(650, 300)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(FirefoxPreviewDialog.sizePolicy().hasHeightForWidth())
        FirefoxPreviewDialog.setSizePolicy(sizePolicy)
        FirefoxPreviewDialog.setMinimumSize(QtCore.QSize(650, 300))
        FirefoxPreviewDialog.setMaximumSize(QtCore.QSize(650, 300))
        self.gridLayout_3 = QtGui.QGridLayout(FirefoxPreviewDialog)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(FirefoxPreviewDialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ebrima"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.line_dialog_title = QtGui.QLineEdit(FirefoxPreviewDialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ebrima"))
        font.setPointSize(12)
        self.line_dialog_title.setFont(font)
        self.line_dialog_title.setObjectName(_fromUtf8("line_dialog_title"))
        self.gridLayout.addWidget(self.line_dialog_title, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.button_close_dialog = QtGui.QPushButton(FirefoxPreviewDialog)
        self.button_close_dialog.setMinimumSize(QtCore.QSize(24, 24))
        self.button_close_dialog.setMaximumSize(QtCore.QSize(24, 24))
        self.button_close_dialog.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/button_close.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_close_dialog.setIcon(icon)
        self.button_close_dialog.setIconSize(QtCore.QSize(24, 24))
        self.button_close_dialog.setObjectName(_fromUtf8("button_close_dialog"))
        self.gridLayout.addWidget(self.button_close_dialog, 0, 3, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_4 = QtGui.QLabel(FirefoxPreviewDialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ebrima"))
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 2, 0, 1, 1)
        self.line_frecency = QtGui.QLineEdit(FirefoxPreviewDialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ebrima"))
        font.setPointSize(9)
        self.line_frecency.setFont(font)
        self.line_frecency.setObjectName(_fromUtf8("line_frecency"))
        self.gridLayout_2.addWidget(self.line_frecency, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(FirefoxPreviewDialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ebrima"))
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_5 = QtGui.QLabel(FirefoxPreviewDialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ebrima"))
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_2.addWidget(self.label_5, 3, 0, 1, 1)
        self.line_expiration_date = QtGui.QLineEdit(FirefoxPreviewDialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ebrima"))
        font.setPointSize(9)
        self.line_expiration_date.setFont(font)
        self.line_expiration_date.setObjectName(_fromUtf8("line_expiration_date"))
        self.gridLayout_2.addWidget(self.line_expiration_date, 2, 1, 1, 1)
        self.line_app_id = QtGui.QLineEdit(FirefoxPreviewDialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ebrima"))
        font.setPointSize(9)
        self.line_app_id.setFont(font)
        self.line_app_id.setObjectName(_fromUtf8("line_app_id"))
        self.gridLayout_2.addWidget(self.line_app_id, 3, 1, 1, 1)
        self.line_file_size = QtGui.QLineEdit(FirefoxPreviewDialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ebrima"))
        font.setPointSize(9)
        self.line_file_size.setFont(font)
        self.line_file_size.setObjectName(_fromUtf8("line_file_size"))
        self.gridLayout_2.addWidget(self.line_file_size, 5, 1, 1, 1)
        self.label_6 = QtGui.QLabel(FirefoxPreviewDialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ebrima"))
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_2.addWidget(self.label_6, 4, 0, 1, 1)
        self.line_flags = QtGui.QLineEdit(FirefoxPreviewDialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ebrima"))
        font.setPointSize(9)
        self.line_flags.setFont(font)
        self.line_flags.setObjectName(_fromUtf8("line_flags"))
        self.gridLayout_2.addWidget(self.line_flags, 4, 1, 1, 1)
        self.line_url_hash = QtGui.QLineEdit(FirefoxPreviewDialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ebrima"))
        font.setPointSize(9)
        self.line_url_hash.setFont(font)
        self.line_url_hash.setObjectName(_fromUtf8("line_url_hash"))
        self.gridLayout_2.addWidget(self.line_url_hash, 0, 1, 1, 1)
        self.label_7 = QtGui.QLabel(FirefoxPreviewDialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ebrima"))
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_2.addWidget(self.label_7, 5, 0, 1, 1)
        self.label_8 = QtGui.QLabel(FirefoxPreviewDialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ebrima"))
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_2.addWidget(self.label_8, 6, 0, 1, 1)
        self.label_2 = QtGui.QLabel(FirefoxPreviewDialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ebrima"))
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.line_resource_uri = QtGui.QLineEdit(FirefoxPreviewDialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ebrima"))
        font.setPointSize(9)
        self.line_resource_uri.setFont(font)
        self.line_resource_uri.setObjectName(_fromUtf8("line_resource_uri"))
        self.gridLayout_2.addWidget(self.line_resource_uri, 6, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 2, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem1, 1, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem2, 3, 0, 1, 1)

        self.retranslateUi(FirefoxPreviewDialog)
        QtCore.QMetaObject.connectSlotsByName(FirefoxPreviewDialog)

    def retranslateUi(self, FirefoxPreviewDialog):
        FirefoxPreviewDialog.setWindowTitle(_translate("FirefoxPreviewDialog", "Dialog", None))
        self.label.setText(_translate("FirefoxPreviewDialog", "Advanced info for entry:", None))
        self.label_4.setText(_translate("FirefoxPreviewDialog", "Expiration date:", None))
        self.label_3.setText(_translate("FirefoxPreviewDialog", "Frecency:", None))
        self.label_5.setText(_translate("FirefoxPreviewDialog", "App Id:", None))
        self.label_6.setText(_translate("FirefoxPreviewDialog", "Flags:", None))
        self.label_7.setText(_translate("FirefoxPreviewDialog", "File size (bytes):", None))
        self.label_8.setText(_translate("FirefoxPreviewDialog", "Resource URI:", None))
        self.label_2.setText(_translate("FirefoxPreviewDialog", "Url hash:", None))

import icons_rc
