import pyudev
import json
import os
import re


SYSFS_PATH="/sys/module/hid_fanatec/drivers"

DEVICE_PREFIX="0003:"


FANATEC_VENDOR_ID = 0x0EB7


# create MODEL_ID based on json file
script_dir = os.path.dirname(os.path.abspath(__file__))

json_file_path = os.path.join(script_dir, 'fanatec_devices.json')
with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

FANATEC_MODEL_ID = {int(key, 16): value for key, value in data["MODEL_ID"].items()}
FANATEC_WHEEL_ID = {int(key, 16): value for key, value in data["WHEEL_ID"].items()}


class InvalidDevice(Exception):
    pass


class FanatecDevice:
    def __init__(self, device):
        device_id = os.path.basename(device.get('DEVPATH'))
        if device_id.startswith(DEVICE_PREFIX):
            parts = device_id.split(':')
            vendor_id = parts[1]
            model_id = parts[2].split('.')[0]
            instance_number = parts[2].split('.')[-1]
        else:
            raise InvalidDevice(f"Cannot identify device {device_id}")

        vendor_id_value = int(vendor_id,16)
        if vendor_id_value != FANATEC_VENDOR_ID:
            raise InvalidDevice(f"Unsupported device {vendor_id_value:04X}")

        self.device_id = device_id
        self.model_id  = model_id


    def get_id(self):
        return self.device_id


    def info(self):
        info = {}
        base = self.__get_model_str()
        if base:
            info.update({ "Base": base })
        if self.device_id:
            info.update({ "Id": self.device_id })
        # wheel = self.__get_wheel_str()
        # if wheel:
        #     info.update({ "Wheel": wheel })
        return info


    def __get_model_str(self) -> str:
        model_id = int(self.model_id, 16)
        if model_id in FANATEC_MODEL_ID.keys():
            return FANATEC_MODEL_ID[model_id]
        return "<unknown>"