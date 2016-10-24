# -*- coding: utf-8 -*-
# !/usr/bin/env python

# Python imports
import os
import datetime
import hashlib

# Uninstall registry key (For user installed browsers)
UNINSTALL_KEY = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"

# Icons path
ICONS_PATH = os.path.join(os.path.dirname(__file__), "..", "gui", "icons")


def get_folder_info(folder_path=None):
    """Retrieving folder information.
    :param folder_path: path to a selected folder.
    :return: folder dimension, elements, creation time and last access time.
    """

    folder_dimension = 0
    for dir_path, dir_names, file_names in os.walk(folder_path):
        for f in file_names:
            fp = os.path.join(dir_path, f)
            folder_dimension += os.path.getsize(fp)

    # Other values for selected folder
    folder_elements = len(os.listdir(folder_path))
    folder_creation_time = os.stat(folder_path).st_ctime
    folder_last_modified_time = os.stat(folder_path).st_mtime
    folder_last_access_time = os.stat(folder_path).st_atime

    readable_creation_time = datetime.datetime.fromtimestamp(folder_creation_time) \
        .strftime("%A - %d %B %Y - %H:%M:%S")

    readable_last_modified_time = datetime.datetime.fromtimestamp(folder_last_modified_time) \
        .strftime("%A - %d %B %Y - %H:%M:%S")

    readable_last_access_time = datetime.datetime.fromtimestamp(folder_last_access_time) \
        .strftime("%A - %d %B %Y - %H:%M:%S")

    results = {
        'folder_dimension': folder_dimension,
        'folder_elements': folder_elements,
        'folder_creation_time': readable_creation_time,
        'folder_last_access_time': readable_last_access_time,
        'folder_last_modified_time': readable_last_modified_time
    }

    return results


def get_file_info(file_path):
    """Retrieving file information.
    :param file_path: path to a selected file.
    :return: nothing
    """

    # File info
    file_dimension = os.stat(file_path).st_size
    creation_time = os.stat(file_path).st_ctime
    last_modified_time = os.stat(file_path).st_mtime
    last_access_time = os.stat(file_path).st_atime

    # Readable times
    readable_creation_time = datetime.datetime.fromtimestamp(creation_time)\
        .strftime("%A - %d %B %Y - %H:%M:%S")

    readable_last_modified_time = datetime.datetime.fromtimestamp(last_modified_time) \
        .strftime("%A - %d %B %Y - %H:%M:%S")

    readable_last_access_time = datetime.datetime.fromtimestamp(last_access_time)\
        .strftime("%A - %d %B %Y - %H:%M:%S")

    # Hash
    hash_md5 = hashlib.md5()
    hash_sha1 = hashlib.sha1()
    buf_dimension = 65536

    with open(file_path, 'rb') as f:
        while True:
            buf = f.read(buf_dimension)
            if not buf:
                break
            hash_md5.update(buf)
            hash_sha1.update(buf)
    md5 = hash_md5.hexdigest()
    sha1 = hash_sha1.hexdigest()

    results = {
        'file_dimension': file_dimension,
        'file_creation_time': readable_creation_time,
        'file_last_modified_time': readable_last_modified_time,
        'file_last_access_time': readable_last_access_time,
        'file_md5': md5,
        'file_sha1': sha1}

    return results


def webkit_to_unix_timestamp(webkit_time):
    """Convert from webkit timestamp to unix time stamp.
    :param webkit_time: webkit time read from a chrome cache file
    :return: Time in readable format
    """
    # From webkit time in microseconds to webkit time in seconds
    microsec_in_sec = float(1000000)
    webkit_time_microsec = float(int(webkit_time, 0))
    webkit_time_sec = webkit_time_microsec / microsec_in_sec

    # Webkit and unix starting date
    webkit_time_start = datetime.datetime(1601, 1, 1)
    unix_time_start = datetime.datetime(1970, 1, 1)

    # Delta time in seconds between webkit and unix starting date
    delta_starting_dates_seconds = (unix_time_start - webkit_time_start).total_seconds()

    # Correct timestamp in unix time
    correct_timestamp = webkit_time_sec - delta_starting_dates_seconds

    # Unix timestamp in readable time
    readable_time = datetime.datetime.fromtimestamp(correct_timestamp).strftime("%A - %d %B %Y - %H:%M:%S")

    return readable_time
