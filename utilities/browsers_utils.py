# -*- coding: utf-8 -*-
# !/usr/bin/env python

# Python imports
import os
import platform
import psutil

# List of user installed browsers, used to simplify browsers recognition.
# Browsers will be referred as in this list to avoid any mismatch with names within the application.
USER_INSTALLED_BROWSERS = ["chrome", "firefox", "opera"]

# Browsers cache default paths
BROWSERS_DEFAULT_CACHE_PATHS = {

    ("chrome", "windows", "10"): os.path.join(
        "C:", os.sep, "Users", unicode(os.environ['USERNAME']), "AppData", "Local", "Google", "Chrome", "User Data",
        "Default", "Cache"
    ),

    ("opera", "windows", "10"): os.path.join(
        "C:", os.sep, "Users", unicode(os.environ['USERNAME']), "AppData", "Local", "Opera Software", "Opera Stable",
        "Cache"
    )
}


def check_open_browser(browser=None):
    """Slot for "button_browsers_screen_select" in "browsers screen".
    Checking if selected browser is open.
    :param browser: Browser key for selected browser
    :return: dictionary with pids and names of matching processes for selected browser
    """

    # Empty dictionary to store matching processes for selected browser
    results = {}

    # Searching for browser process in open processes
    for process in psutil.process_iter():
        # Browser key found in a process name
        if browser in process.name():
            results["{pid}".format(pid=process.pid)] = process.name()

    return results


def get_default_cache_path(browser_name=None):
    """Get default cache path for a given browser.
    Checking if a key for a browser is stored in "BROWSERS_DEFAULT_CACHE_PATHS".
    :param browser_name: complete name for browser
    :return: matching_browser_key and default_cache_path
    """

    # Values for matching browser
    matching_browser_key = None
    default_cache_path = None

    # Default cache paths for supported browsers
    for k in BROWSERS_DEFAULT_CACHE_PATHS.keys():
        # A key in dictionary matches browser name
        if k[0] in str(browser_name).lower():
            matching_browser_key = k[0]
            # Default path in dictionary
            default_cache_path = BROWSERS_DEFAULT_CACHE_PATHS.get(
                (matching_browser_key, platform.system().lower(), platform.release()),
                "Missing default cache path for selected browser")

    results = {
        'matching_browser_key': matching_browser_key,
        'default_cache_path': default_cache_path,
    }

    return results


def check_valid_cache_path(browser=None, cache_path=None):
    """Checking if a selected cache path is valid for selected browser.
    To be considered valid, a path must contain specific files (according to the browser).
    :param browser: Selected browser
    :param cache_path: Cache path for selected browser
    :return: True or false for valid or not not cache path
    """

    # Existing path
    if os.path.exists(cache_path):
        # Google Chrome
        if browser == "chrome":
            # Chrome index and data_ files
            chrome_files = ["index", "data_0", "data_1", "data_2", "data_3"]
            # All files in "chrome_files" are in cache folder
            if set(chrome_files).issubset(os.listdir(cache_path)):
                return True
            # Not all files in "chrome_files" are in cache folder
            return False

        # Opera
        elif browser == "opera":
            # Chrome index and data_ files
            chrome_files = ["index", "data_0", "data_1", "data_2", "data_3"]
            # All files in "chrome_files" are in cache folder
            if set(chrome_files).issubset(os.listdir(cache_path)):
                return True
            # Not all files in "chrome_files" are in cache folder
            return False
    # Not existing path
    else:
        return False
