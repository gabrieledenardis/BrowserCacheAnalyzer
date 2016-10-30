# -*- coding: utf-8 -*-
# !/usr/bin/env python

# Python imports
try:
    import _winreg
except ImportError:
    _winreg = None

# Project imports
from utilities import utils, browsers_utils

# # Uninstall registry key (For user installed browsers)
# UNINSTALL_KEY = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"


def finder():
    """ Looking in system registry for installed browsers.
    For user installed browsers, if values in "utils.USER_INSTALLED_BROWSERS" are also in "uninstall" key
    in system registry, retrieving values and adding in "list_found browsers"
    :return: list of found browsers in the system
    """

    # Uninstall key (For user installed browsers)
    uninstall_key = None

    # Attributes for found browsers
    browser_name = None
    browser_version = None
    browser_path = None

    # List of found browsers in the system
    list_found_browsers = []

    try:
        # Opening uninstall key
        uninstall_key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, utils.UNINSTALL_KEY, 0, _winreg.KEY_READ)

        # Searching in sub keys of uninstall key for user installed browsers
        for s_k in range(_winreg.QueryInfoKey(uninstall_key)[0]):
            try:
                # Sub key name
                uninstall_sub_key_name = _winreg.EnumKey(uninstall_key, s_k)
                for browser in browsers_utils.USER_INSTALLED_BROWSERS:
                    # A browser in "user installed browsers" matches a sub key name
                    if browser in uninstall_sub_key_name.lower():
                        # Matching browser key name
                        browser_key_name = "\\".join([utils.UNINSTALL_KEY, uninstall_sub_key_name])
                        try:
                            # Opening matching browser key
                            browser_key = _winreg.OpenKey(
                                _winreg.HKEY_LOCAL_MACHINE,
                                browser_key_name,
                                0,
                                _winreg.KEY_READ
                            )
                            # Searching in matching browser key values
                            for val in range(_winreg.QueryInfoKey(browser_key)[1]):
                                try:
                                    # Browser key values
                                    value_name, value_data, value_data_type = _winreg.EnumValue(browser_key, val)
                                    # Name, version and installation path values
                                    if value_name == "DisplayName":
                                        browser_name = value_data
                                    elif value_name == "DisplayVersion":
                                        browser_version = value_data
                                    elif value_name == "InstallLocation":
                                        browser_path = value_data
                                except WindowsError as _:
                                    pass
                            # Updating "list_found_browsers"
                            list_found_browsers.append([browser, browser_name, browser_version, browser_path])
                        except WindowsError as _:
                            pass
                        finally:
                            # Closing matching browser key
                            _winreg.CloseKey(browser_key)
            except WindowsError as _:
                pass
    except WindowsError as _:
        pass
    finally:
        # Closing uninstall key
        _winreg.CloseKey(uninstall_key)

    # Returning results list with all found browsers values
    return list_found_browsers
