import pyudev


from .FanatecDevice import FanatecDevice
from .FanatecDevice import InvalidDevice


class FanatecDeviceMonitor:
    def __init__(self):
        self.context = pyudev.Context()

        self.devices = {}
        self.__list_devices()


    # def __del__(self):
    #     self.stop_monitoring()

    def __list_devices(self):
        devices = self.context.list_devices(subsystem='hid')
        for device in devices:
            self.__device_added(device)


    def start_monitoring(self):
        self.monitor = pyudev.Monitor.from_netlink(self.context)
        self.monitor.filter_by(subsystem='hid')  # Filter for input devices
        for action, device in self.monitor:
            if action == 'add':
                self.__device_added(device)
            elif action == 'remove':
                self.__device_removed(device)



    def __device_added(self, device):
        try:
            fanatec_device = FanatecDevice(device)
            print( f"{fanatec_device.info()} connected")
            device_id = fanatec_device.get_id()
            self.devices[device_id] = device
        except InvalidDevice as e:
            pass


    def __device_removed(self, device):
        try:
            fanatec_device = FanatecDevice(device)
            print( f"{fanatec_device.info()} disconnected")
            device_id = fanatec_device.get_id()
            del self.devices[device_id]
        except ValueError:
            pass
