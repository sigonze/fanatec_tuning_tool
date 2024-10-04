import pyudev
import json
import os
import re
import threading
import time

from typing import Callable

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
    def __init__(self, device, interval=0.5):
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

        self.callbacks = {
            "device-settings": None
        }

        self.device_id = device_id
        self.model_id  = model_id
        self.wheel_id  = self.__get_wheel_id()

        sysfs_path = [ SYSFS_PATH, device_id, "ftec_tuning", device_id ]
        self.sysfs_path = os.path.join(*sysfs_path)

        self.settings={}


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
            time.sleep(self.interval)
            settings = self.read_settings()
            if settings != self.settings:
                differences = {key: settings[key] for key in settings if settings[key] != self.settings.get(key)}
                self.settings=settings
                if self.callbacks["device-settings"]:
                    self.callbacks["device-settings"](differences)


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


    def connect(self, event_name, callback: Callable[[str], None]):
        assert event_name in self.callbacks.keys()
        self.callbacks[event_name]=callback


    def read_settings(self):
        settings = {}
        pattern = re.compile(r'^[A-Z]{2,3}$|^SLOT$')

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


    def set_settings(self,new_settings):
        for setting, value in new_settings.items():
            try:
                file_path = os.path.join(self.sysfs_path, setting)
                if value > 0:    # to handle SLOT case (0 => no change)
                    with open(file_path, 'w') as file:
                        file.write(f"{value}")
                    self.settings.update({setting: value})
            except (FileNotFoundError,OSError):
                pass


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