import pyudev
import json
import os
import re
import threading
import time


SYSFS_PATH="/sys/module/hid_fanatec/drivers/hid:fanatec"

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
    def __init__(self, device, interval=0.1):
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

        self.interval = interval
        self._running = False
        self._thread = None

        self.device_id = device_id
        self.model_id  = model_id
        self.wheel_id  = self.__get_wheel_id()

        sysfs_path = [ SYSFS_PATH, device_id, "ftec_tuning", device_id ]
        self.sysfs_path = os.path.join(*sysfs_path)

        self.settings=self.read_settings()


    def start_monitoring(self):
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._check_setting_updated)
            self._thread.start()


    def stop_monitoring(self):
        if self._running:
            self._running = False
            self._thread.join()


    def _check_setting_updated(self):
        while self._running:
            settings = self.read_settings()
            if settings != self.settings:
                print(settings)
                time.sleep(self.interval)


    def get_id(self):
        return self.device_id


    def info(self):
        info = {}
        base = self.__get_model_id_str()
        if base:
            info.update({ "Base": base })
        wheel = self.__get_wheel_id_str()
        if wheel:
            info.update({ "Wheel": wheel })
        if self.device_id:
            info.update({ "Id": self.device_id })
        return info


    def read_settings(self):
        settings = {}
        pattern = re.compile(r'^[A-Z]{2,3}$')

        for filename in os.listdir(self.sysfs_path):
            if pattern.match(filename):
                try:
                    file_path = os.path.join(self.sysfs_path,filename)
                    with open(file_path, 'r') as file:
                        value_str = file.read().strip()
                        value = int(value_str)
                    settings.update({filename: value})
                except (ValueError, FileNotFoundError):
                    pass
        return settings


    def get_settings(self):
        return self.settings


    def __get_wheel_id(self):
        sysfs_path = [ SYSFS_PATH, self.device_id, "wheel_id" ]
        file_path = os.path.join(*sysfs_path)

        try:
            with open(file_path, 'r') as file:
                value = file.read().strip()
                wheel_id = int(value,16)
        except (ValueError, FileNotFoundError):
            wheel_id = 0
        return wheel_id


    def __get_model_id_str(self) -> str:
        model_id = int(self.model_id, 16)
        if model_id in FANATEC_MODEL_ID.keys():
            return FANATEC_MODEL_ID[model_id]
        return "<unknown>"


    def __get_wheel_id_str(self) -> str:
        if self.wheel_id:
            if self.wheel_id in FANATEC_WHEEL_ID.keys():
                return FANATEC_WHEEL_ID[self.wheel_id]
        return None