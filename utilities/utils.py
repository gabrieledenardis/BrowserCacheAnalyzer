# -*- coding: utf-8 -*-
# !/usr/bin/env python

# Python imports
import datetime
import hashlib
import os


######################
# SECTION: UTILITIES #
######################

# Paths
ICONS_PATH = os.path.join(os.path.dirname(__file__), "..", "gui", "icons")
JQUERY_PATH = os.path.join(os.path.dirname(__file__), "..", "static", "js", "jquery-3.1.1.min.js")
JQUERY_TABLES_PATH = os.path.join(os.path.dirname(__file__), "..", "static", "js", "jquery.dataTables.js")
JQUERY_DATATABLES_CSS_PATH = os.path.join(os.path.dirname(__file__), "..", "static", "css", "jquery.dataTables.css")

# Uninstall registry key (For user installed browsers)
UNINSTALL_KEY = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"

# Windows registry keys for time info
W32TIME_CONFIG = r"SYSTEM\CurrentControlSet\Services\W32Time\Config"
W32TIME_PARAMETERS = r"SYSTEM\CurrentControlSet\Services\W32Time\Parameters"
W32TIME_TIME_PROVIDERS = r"SYSTEM\CurrentControlSet\Services\W32Time\TimeProviders\NtpClient"
TIME_ZONE_INFORMATION = r"SYSTEM\CurrentControlSet\Control\TimeZoneInformation"


######################
# SECTION: FUNCTIONS #
######################

def get_folder_info(folder_path=None):
    """Retrieving folder information.
    :param folder_path: path to a selected folder
    :return: folder dimension, elements, creation time, last modified time and last access time
    """

    # Folder dimension
    folder_dimension = 0
    for dir_path, dir_names, file_names in os.walk(folder_path):
        for f in file_names:
            fp = os.path.join(dir_path, f)
            folder_dimension += os.path.getsize(fp)

    # Other values for selected folder
    folder_elements = len(os.listdir(folder_path))
    creation_time = os.stat(folder_path).st_ctime
    last_modified_time = os.stat(folder_path).st_mtime
    last_access_time = os.stat(folder_path).st_atime

    # Time format patterns
    format_creation_time = datetime.datetime.fromtimestamp(creation_time).strftime("%A - %d %B %Y - %H:%M:%S")
    format_last_modified_time = datetime.datetime.fromtimestamp(last_modified_time).strftime("%A - %d %B %Y - %H:%M:%S")
    format_last_access_time = datetime.datetime.fromtimestamp(last_access_time).strftime("%A - %d %B %Y - %H:%M:%S")

    results = {
        'folder_dimension': folder_dimension,
        'folder_elements': folder_elements,
        'folder_creation_time': format_creation_time,
        'folder_last_access_time': format_last_modified_time,
        'folder_last_modified_time': format_last_access_time
    }

    return results


def get_file_info(file_path=None):
    """Retrieving file information.
    :param file_path: path to a selected file
    :return: file dimension, creation time, last modified time, last access time, MD5 and SHA1
    """

    # File info
    file_dimension = os.stat(file_path).st_size
    creation_time = os.stat(file_path).st_ctime
    last_modified_time = os.stat(file_path).st_mtime
    last_access_time = os.stat(file_path).st_atime

    # Time format patterns
    format_creation_time = datetime.datetime.fromtimestamp(creation_time).strftime("%A - %d %B %Y - %H:%M:%S")
    format_last_modified_time = datetime.datetime.fromtimestamp(last_modified_time).strftime("%A - %d %B %Y - %H:%M:%S")
    format_last_access_time = datetime.datetime.fromtimestamp(last_access_time).strftime("%A - %d %B %Y - %H:%M:%S")

    # Hash
    object_md5 = hashlib.md5()
    object_sha1 = hashlib.sha1()
    buf_dimension = 65536

    with open(file_path, 'rb') as f:
        while True:
            buf = f.read(buf_dimension)
            if not buf:
                break
            object_md5.update(buf)
            object_sha1.update(buf)
    md5 = object_md5.hexdigest()
    sha1 = object_sha1.hexdigest()

    results = {
        'file_dimension': file_dimension,
        'file_creation_time': format_creation_time,
        'file_last_modified_time': format_last_modified_time,
        'file_last_access_time': format_last_access_time,
        'file_md5': md5,
        'file_sha1': sha1}

    return results


def webkit_to_unix_timestamp(webkit_time=None, source=None):
    """Convert from webkit timestamp to unix time stamp.
    :param webkit_time: webkit time read from a chrome cache file or from Windows registry
    :param source: browser or windows registry
    :return: time in format pattern
    """

    # Webkit time in seconds
    webkit_time_sec = None

    # Time from chrome cache (microseconds)
    if source == "chrome" or source == "opera":
        # Conversion from microseconds to seconds
        microsec_in_sec = float(1000000)
        webkit_time_microsec = float(int(webkit_time, 0))
        webkit_time_sec = webkit_time_microsec / microsec_in_sec

    # Time from windows registry (seconds)
    elif source == "windows_registry":
        webkit_time_sec = webkit_time

    # Webkit and unix starting date
    webkit_time_start = datetime.datetime(1601, 1, 1)
    unix_time_start = datetime.datetime(1970, 1, 1)

    # Delta time in seconds between webkit and unix starting dates
    delta_starting_dates_sec = (unix_time_start - webkit_time_start).total_seconds()

    # Correct unix timestamp
    correct_unix_timestamp = webkit_time_sec - delta_starting_dates_sec

    # Time format pattern
    format_pattern_time = datetime.datetime.fromtimestamp(correct_unix_timestamp).strftime("%A - %d %B %Y - %H:%M:%S")

    return format_pattern_time


def create_random_hash():
    """Creating MD5 and SHA1 hash from a random number.
    Providing unique identifiers for every cache export session.
    :return: MD5 and SHA1
    """

    random_md5 = hashlib.md5(os.urandom(128)).hexdigest()
    random_sha1 = hashlib.sha1(os.urandom(128)).hexdigest()

    results = {
        'random_md5': random_md5,
        'random_sha1': random_sha1
    }

    return results
