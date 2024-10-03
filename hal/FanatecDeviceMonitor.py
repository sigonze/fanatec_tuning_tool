import pyudev

from typing import Callable

from .FanatecDevice import FanatecDevice
from .FanatecDevice import InvalidDevice


class FanatecDeviceMonitor:
    def __init__(self):
        self.is_started = False

        self.callbacks = {
            "device-connected": None,
            "device-disconnected": None
        }

        self.context = pyudev.Context()

        self.devices = {}
        self.__list_devices()

        self.monitor = pyudev.Monitor.from_netlink(self.context)
        self.monitor.filter_by(subsystem='hid')
        self.observer = pyudev.MonitorObserver(self.monitor, self.__on_device_event)


    def start(self):
        if not self.is_started:
            self.observer.start()
            self.is_started = True


    def stop(self):
        if self.is_started:
            self.observer.stop()
            self.is_started = False


    def connect(self, event_name, callback: Callable[[str], None]):
        assert event_name in self.callbacks.keys()
        self.callbacks[event_name]=callback


    def __list_devices(self):
        devices = self.context.list_devices(subsystem='hid')
        for device in devices:
            self.__device_added(device)



    def __on_device_event(self, event, device):
        if event == 'add':
            self.__device_added(device)
        elif event == 'remove':
            self.__device_removed(device)


    def __device_added(self, device):
        try:
            fanatec_device = FanatecDevice(device)
            device_id = fanatec_device.get_id()
            device_info = fanatec_device.info()
            self.devices[device_id] = device
        
            if self.callbacks["device-connected"]:
                device_info.update( {"Status": "connected"} )
                self.callbacks["device-connected"](device_info)

        except InvalidDevice as e:
            pass


    def __device_removed(self, device):
        try:
            fanatec_device = FanatecDevice(device)
            device_id = fanatec_device.get_id()
            device_info = fanatec_device.info()
            del self.devices[device_id]

            if self.callbacks["device-disconnected"]:
                device_info.update( {"Status": "disconnected"} )
                self.callbacks["device-disconnected"](device_info)

        except ValueError:
            pass
