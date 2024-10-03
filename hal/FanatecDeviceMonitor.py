import pyudev


from .FanatecDevice import FanatecDevice
from .FanatecDevice import InvalidDevice


class FanatecDeviceMonitor:
    def __init__(self):
        self.context = pyudev.Context()

        self.devices = {}
        self.__list_devices()

        self.context = pyudev.Context()
        self.monitor = pyudev.Monitor.from_netlink(self.context)
        self.monitor.filter_by(subsystem='hid')
        self.observer = pyudev.MonitorObserver(self.monitor, self.__on_device_event)


    def __list_devices(self):
        devices = self.context.list_devices(subsystem='hid')
        for device in devices:
            self.__device_added(device)


    def start(self):
        # Start the observer
        self.observer.start()
        print("Device monitoring started...")


    def stop(self):
        # Stop the observer
        self.observer.stop()
        print("Device monitoring stopped.")


    def __on_device_event(self, event, device):
        if event == 'add':
            self.__device_added(device)
        elif event == 'remove':
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
