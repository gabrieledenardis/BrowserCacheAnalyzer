# -*- coding: utf-8 -*-
# !/usr/bin/env python

# PyQt4 imports
from PyQt4 import QtGui

# Python imports
import sys

# Project imports
import browser_cache_analyzer


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    application_main_window = browser_cache_analyzer.BrowserCacheAnalyzer()
    application_main_window.show()
    sys.exit(app.exec_())
