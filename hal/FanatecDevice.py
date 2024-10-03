import pyudev
import os
import re


SYSFS_PATH="/sys/module/hid_fanatec/drivers"
SYSFS_PREFIX='0003'


FANATEC_VENDOR_ID = 0x0EB7


# create MODEL_ID based on json file
script_dir = os.path.dirname(os.path.abspath(__file__))

json_file_path = os.path.join(script_dir, 'fanatec_ffb_tuning.json')
with open(json_file_path, 'r') as json_file:
        data = json.load(file)

FANATEC_MODEL_ID = {int(key, 16): value for key, value in data["MODEL_ID"].items()}
FANATEC_WHEEL_ID = {int(key, 16): value for key, value in data["WHEEL_ID"].items()}


class FanatecDevice:
    def __init__(self, device):
        vendor_id = 0
        vendor_id_str = device.get("ID_VENDOR_ID")
        if vendor_id_str:
            vendor_id = int(vendor_id_str,16)

        if vendor_id != FANATEC_VENDOR_ID
            raise "unsupported device"

        self.device = device
        model_id_str = self.device.get("ID_MODEL_ID")
        self.model_id = int(device_id_str,16)

        expected_dir = f"{SYSFS_PREFIX}:{vendor_id:04X}:{self.model_id:04X}"


    # List all entries in the base path
    for dirname in os.listdir(base_path):
        # Check if the entry is a directory and matches the regex pattern
        full_path = os.path.join(base_path, dirname)
        if os.path.isdir(full_path) and regex_pattern.match(dirname):
            matching_dirs.append(full_path)

    return matching_dirs

    def get_id(self):



    def info(self):
        info = {}
        base = self.__get_model_str()
        if base:
            info.update({ "Base": base })
        wheel = self.__get_wheel_str()
        if wheel:
            info.update({ "Wheel": wheel })


    def __get_model_str(self) -> str:
        device_id_str = self.device.get("ID_MODEL_ID")
        if device_id_str:
            device_id = int(device_id_str,16)
            if device_id in FANATEC_MODEL_ID:
                return FANATEC_MODEL_ID[device_id]
        return "<unknown>"