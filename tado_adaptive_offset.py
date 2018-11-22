#!/usr/bin/env python

import requests
import sys
import json

# tado credentials
USERNAME = ""
PASSWORD = ""

OFFSET_CONFIG = {"VA3516008704": {"base_temp": 12.0, "offset_factor": 0.1},
                 "VA3146778880": {"base_temp": 12.0, "offset_factor": 0.12}}

ME_URL = "https://my.tado.com/api/v2/me"
WEATHER_URL = "https://my.tado.com/api/v2/homes/{}/weather"
DEVICES_URL = "https://my.tado.com/api/v2/homes/{}/devices"
OFFSET_URL = "https://my.tado.com/api/v2/devices/{}/temperatureOffset"


class TadoAPICallException(Exception):
    def __init__(self, message, errors):

        # Call the base class constructor with the parameters it needs
        super(TadoAPICallException, self).__init__(message)

        # Now for your custom code...
        self.errors = errors


def api_call(endpoint, r_type="GET", data=None):
    GET_AUTH = "?username={}&password={}".format(USERNAME, PASSWORD)

    if r_type not in ["GET", "PUT"]:
        raise TadoAPICallException("request type {} not supported".format(r_type), 1)

    url = "".join([endpoint, GET_AUTH])
    if r_type == "GET":
        r = requests.get(url)
    elif r_type == "PUT":
        r = requests.put(url, data=json.dumps(data))

    if r.status_code != 200:
        raise TadoAPICallException("", r.status_code)

    return r.json()


def home_id():
    return api_call(ME_URL)["homes"][0]["id"]


def home_outside_temp(home_id):
    return api_call(WEATHER_URL.format(home_id))["outsideTemperature"]["celsius"]


def set_offset_temp(device_id, target_offset):
    payload = {"celsius": target_offset}
    return api_call(OFFSET_URL.format(device_id), "PUT", payload)


def thermostat_device_ids(hid):
    def capable(x):
        caps = x["characteristics"]["capabilities"]
        return "INSIDE_TEMPERATURE_MEASUREMENT" in caps

    return [x["serialNo"] for x in api_call(DEVICES_URL.format(hid)) if capable(x)]


if __name__ == '__main__':
    hid = home_id()
    outside_temp = home_outside_temp(hid)
    print("Outside temp is: ", outside_temp)

    for did in thermostat_device_ids(hid):
        if did not in OFFSET_CONFIG:
            continue

        c = OFFSET_CONFIG[did]
        target_offset = min(0.0, (outside_temp - c["base_temp"]) * c["offset_factor"])
        offset = set_offset_temp(did, target_offset)
        print("Offset for {}".format(did), offset)

    sys.exit(0)
