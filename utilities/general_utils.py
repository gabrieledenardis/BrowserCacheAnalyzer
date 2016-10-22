# -*- coding: utf-8 -*-
# !/usr/bin/env python

# Python imports
import os
import datetime

# Uninstall registry key (For user installed browsers)
UNINSTALL_KEY = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"

# Icons path
ICONS_PATH = os.path.join(os.path.dirname(__file__), "..", "gui", "icons")


def get_folder_info(folder_path):
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
    folder_last_access_time = os.stat(folder_path).st_atime
    folder_last_modified_time = os.stat(folder_path).st_mtime

    readable_creation_time = datetime.datetime.fromtimestamp(folder_creation_time) \
        .strftime("%A - %d %B %Y - %H:%M:%S")

    readable_last_access_time = datetime.datetime.fromtimestamp(folder_last_access_time) \
        .strftime("%A - %d %B %Y - %H:%M:%S")

    readable_last_modified_time = datetime.datetime.fromtimestamp(folder_last_modified_time) \
        .strftime("%A - %d %B %Y - %H:%M:%S")

    results = {
        'folder_dimension': folder_dimension,
        'folder_elements': folder_elements,
        'folder_creation_time': readable_creation_time,
        'folder_last_access_time': readable_last_access_time,
        'folder_last_modified_time': readable_last_modified_time
    }

    return results
