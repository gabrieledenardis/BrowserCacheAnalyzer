# -*- coding: utf-8 -*-
# !/usr/bin/env python

# Python imports
try:
    import _winreg
except ImportError:
    _winreg = None

import struct

# Project imports
from utilities import utils


def get_registry_time_info():
    """Reading in Windows Registry for info about system time last synchronization, ntp server and timezone.
    :return: last known good time, special polling interval, ntp server, synchronization type, timezone
    """

    # Time registry keys
    w32time_config = None
    w32time_parameters = None
    w32time_time_providers = None
    time_zone_information = None

    # Values to search
    last_known_time = None
    special_poll_interval = None
    ntp_server = None
    sync_type = None
    time_zone = None

    # W32TIME_CONFIG
    try:
        # Opening w32time_config key
        w32time_config = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, utils.W32TIME_CONFIG, 0, _winreg.KEY_READ)

        # Searching in key values
        for val in range(_winreg.QueryInfoKey(w32time_config)[1]):
            try:
                # Searching for "LastKnownGoodTime"
                value_name, value_data, value_data_type = _winreg.EnumValue(w32time_config, val)

                if value_name == "LastKnownGoodTime":
                    # Value expressed in units of 100 nanoseconds from 01 Jan 1601
                    last_known_time = struct.unpack('<Q', value_data)[0]

            except WindowsError as _:
                pass

    except WindowsError as _:
        pass

    finally:
        # Closing w32time_config key
        _winreg.CloseKey(w32time_config)

    # W32TIME_PARAMETERS
    try:
        # Opening w32time_parameters key
        w32time_parameters = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, utils.W32TIME_PARAMETERS, 0, _winreg.KEY_READ)

        # Searching in key values
        for val in range(_winreg.QueryInfoKey(w32time_parameters)[1]):
            try:
                # Searching for "NtpServer" and "Type"
                value_name, value_data, value_data_type = _winreg.EnumValue(w32time_parameters, val)

                if value_name == "NtpServer":
                    ntp_server = value_data

                elif value_name == "Type":
                    sync_type = value_data

            except WindowsError as _:
                pass

    except WindowsError as _:
        pass

    finally:
        # Closing w32time_parameters key
        _winreg.CloseKey(w32time_parameters)

    # W32TIME_TIME_PROVIDERS
    try:
        # Opening w32time_time_providers key
        w32time_time_providers = _winreg.OpenKey(
            _winreg.HKEY_LOCAL_MACHINE,
            utils.W32TIME_TIME_PROVIDERS,
            0,
            _winreg.KEY_READ
        )

        # Searching in key values
        for val in range(_winreg.QueryInfoKey(w32time_time_providers)[1]):
            try:
                # Searching for "SpecialPollInterval"
                value_name, value_data, value_data_type = _winreg.EnumValue(w32time_time_providers, val)

                if value_name == "SpecialPollInterval":
                    # Value expressed in seconds
                    special_poll_interval = value_data

            except WindowsError as _:
                pass

    except WindowsError as _:
        pass

    finally:
        # Closing w32time_time_providers key
        _winreg.CloseKey(w32time_time_providers)

    # TIME_ZONE_INFORMATION
    try:
        # Opening time_zone_information key
        time_zone_information = _winreg.OpenKey(
            _winreg.HKEY_LOCAL_MACHINE,
            utils.TIME_ZONE_INFORMATION,
            0,
            _winreg.KEY_READ
        )

        # Searching in key values
        for val in range(_winreg.QueryInfoKey(time_zone_information)[1]):
            try:
                # Searching for "TimeZoneKeyName"
                value_name, value_data, value_data_type = _winreg.EnumValue(time_zone_information, val)

                if value_name == "TimeZoneKeyName":
                    time_zone = value_data

            except WindowsError as _:
                pass

    except WindowsError as _:
        pass

    finally:
        # Closing time_zone_information key
        _winreg.CloseKey(time_zone_information)

    # Last known and next sync times in seconds
    last_known_time_sec = last_known_time / 10000000
    next_sync_time_sec = last_known_time_sec + special_poll_interval

    # Time format patterns
    format_last_known = utils.webkit_to_unix_timestamp(webkit_time=last_known_time_sec, source="windows_registry")
    format_next_sync = utils.webkit_to_unix_timestamp(webkit_time=next_sync_time_sec, source="windows_registry")

    results = {
        'last_known_time': format_last_known,
        'next_sync_time': format_next_sync,
        'ntp_server': ntp_server,
        'sync_type': sync_type,
        'time_zone': time_zone
    }

    return results
