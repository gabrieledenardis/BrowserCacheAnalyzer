# -*- coding: utf-8 -*-
# !/usr/bin/env python

# Python imports
import platform
import psutil
import struct
import os

# List of user installed browsers, used to simplify browsers recognition.
# Browsers will be referred as in this list to avoid any mismatch with names within the application.
USER_INSTALLED_BROWSERS = ["chrome", "firefox", "opera"]

# Firefox profile folder (This folder contains an user folder with a random identifier name)
FIREFOX_PROFILE_FOLDER = "C:\\Users\\Gabriele\\AppData\\Local\\Mozilla\\Firefox\\Profiles"


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
    browser_key = str(browser_name).lower()
    current_system = platform.system().lower()
    current_release = platform.release()

    # Default cache paths for supported browsers
    for k in BROWSERS_DEFAULT_CACHE_PATHS.keys():
        # A key in dictionary matches browser name
        if k[0] in browser_key and k[1] == current_system and k[2] == current_release:
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


def get_firefox_default_cache_path():
    """Searching for Firefox "cache2" folder.
    The "cache2" contains both "index" file and "entries" sub folder.
    :return: path to firefox "cache2" folder
    """

    firefox_cache_path = ""

    # Searching for "cache2" folder
    for root, dirs, files in os.walk(FIREFOX_PROFILE_FOLDER):
        for subdir in dirs:
            if subdir == "cache2":
                firefox_cache_path = os.path.join(root, subdir)

    # "Cache2" folder not present
    if not firefox_cache_path:
        firefox_cache_path = "Not available"

    return firefox_cache_path


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
            # Chrome "index" and "data_#" files
            chrome_files = ["index", "data_0", "data_1", "data_2", "data_3"]
            index_signature = "C103CAC3"
            data_signature = "C104CAC3"

            # All files in "chrome_files" are in cache folder
            if set(chrome_files).issubset(os.listdir(cache_path)):
                for f in chrome_files:
                    file_to_open = os.path.join(cache_path, f)
                    # Checking signature for "index" file
                    if f == "index":
                        with open(file_to_open, "rb") as f_index:
                            try:
                                read_signature = format(struct.unpack("<I", f_index.read(4))[0], "X")

                            except Exception as _:
                                return False

                            # Not correct signature
                            if read_signature != index_signature:
                                return False

                    # Checking signature for "data_#" file
                    else:
                        with open(file_to_open, "rb") as f_data:
                            try:
                                read_signature = format(struct.unpack("<I", f_data.read(4))[0], "X")

                            except Exception as _:
                                return False

                            # Not correct signature
                            if read_signature != data_signature:
                                return False

                # All signatures correct
                else:
                    return True

            # Not all files in "chrome_files" are in cache folder
            return False

        # Firefox
        elif browser == "firefox":
            index_version = 1
            entries_folder_present = False

            # Searching "entries" folder
            for root, dirs, files in os.walk(cache_path):
                for subdir in dirs:
                    if subdir == "entries":
                        entries_folder_present = True
                        break

            # "Index" file and "entries" sub folder in cache folder
            if "index" in os.listdir(cache_path) and entries_folder_present:
                index_to_open = os.path.join(cache_path, "index")

                # Checking version for "index" file
                with open(index_to_open, "rb") as f_index:
                    try:
                        read_version = struct.unpack(">I", f_index.read(4))[0]

                    except Exception as _:
                        return False

                    # Not correct version
                    if read_version != index_version:
                        return False

                # Correct version
                return True

            # "Index" file and "entries" sub folder not in cache folder
            else:
                return False

        # Opera
        if browser == "opera":
            # Opera "index" and "data_#" files
            opera_files = ["index", "data_0", "data_1", "data_2", "data_3"]
            index_signature = "C103CAC3"
            data_signature = "C104CAC3"

            # All files in "opera_files" are in cache folder
            if set(opera_files).issubset(os.listdir(cache_path)):
                for f in opera_files:
                    file_to_open = os.path.join(cache_path, f)
                    # Checking signature for "index" file
                    if f == "index":
                        with open(file_to_open, "rb") as f_index:
                            try:
                                read_signature = format(struct.unpack("<I", f_index.read(4))[0], "X")

                            except Exception as _:
                                return False

                            # Not correct signature
                            if read_signature != index_signature:
                                return False

                    # Checking signature for "data_#" file
                    else:
                        with open(file_to_open, "rb") as f_data:
                            try:
                                read_signature = format(struct.unpack("<I", f_data.read(4))[0], "X")

                            except Exception as _:
                                return False

                            # Not correct signature
                            if read_signature != data_signature:
                                return False

                # All signatures correct
                else:
                    return True

            # Not all files in "opera_files" are in cache folder
            return False


# Browsers cache default paths
BROWSERS_DEFAULT_CACHE_PATHS = {

    ("chrome", "windows", "7"): os.path.join(
        "C:", os.sep, "Users", unicode(os.environ['USERNAME']), "AppData", "Local", "Google", "Chrome", "User Data",
        "Default", "Cache"
    ),

    ("firefox", "windows", "7"): get_firefox_default_cache_path(),

    ("opera", "windows", "7"): os.path.join(
        "C:", os.sep, "Users", unicode(os.environ['USERNAME']), "AppData", "Local", "Opera Software", "Opera Stable",
        "Cache"
    ),

    ("chrome", "windows", "8"): os.path.join(
        "C:", os.sep, "Users", unicode(os.environ['USERNAME']), "AppData", "Local", "Google", "Chrome", "User Data",
        "Default", "Cache"
    ),

    ("firefox", "windows", "8"): get_firefox_default_cache_path(),

    ("opera", "windows", "8"): os.path.join(
        "C:", os.sep, "Users", unicode(os.environ['USERNAME']), "AppData", "Local", "Opera Software", "Opera Stable",
        "Cache"
    ),

    ("chrome", "windows", "8.1"): os.path.join(
        "C:", os.sep, "Users", unicode(os.environ['USERNAME']), "AppData", "Local", "Google", "Chrome", "User Data",
        "Default", "Cache"
    ),

    ("firefox", "windows", "8.1"): get_firefox_default_cache_path(),

    ("opera", "windows", "8.1"): os.path.join(
        "C:", os.sep, "Users", unicode(os.environ['USERNAME']), "AppData", "Local", "Opera Software", "Opera Stable",
        "Cache"
    ),

    ("chrome", "windows", "10"): os.path.join(
        "C:", os.sep, "Users", unicode(os.environ['USERNAME']), "AppData", "Local", "Google", "Chrome", "User Data",
        "Default", "Cache"
    ),

    ("firefox", "windows", "10"): get_firefox_default_cache_path(),

    ("opera", "windows", "10"): os.path.join(
        "C:", os.sep, "Users", unicode(os.environ['USERNAME']), "AppData", "Local", "Opera Software", "Opera Stable",
        "Cache"
    )
}
