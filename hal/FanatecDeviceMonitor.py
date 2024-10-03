import pyudev


class FanatecDeviceMonitor:
    def __init__(self):
        self.devices = []
        self.__list_devices()

        self.context = pyudev.Context()
        self.monitor = pyudev.Monitor.from_netlink(self.context)
        self.monitor.filter_by(subsystem='input')  # Filter for input devices

        self.start_monitoring()


    def __del__(self):
        self.stop_monitoring()


    def __list_devices(self):
        devices = context.list_devices(subsystem='input')
        for device in devices:
            self.__device_added(device)


    def start_monitoring(self):
        self.observer = pyudev.MonitorObserver(self.monitor, self.device_event)
        self.observer.start()


    def stop_monitoring(self):
        self.observer.stop()


    def __device_event(self, event, device):
        if is_fanatec_device(device):
            if event=='add':
                self.__device_added(device)
            elif event == 'remove':
                self.devices.remove(device)


    def __device_added(self, device):
        try:
            fanatec_device = FanatecDevice(device)
            self.devices.append(fanatec_device)
        except:
            pass


    def __device_removed(self, device):
        try:
            fanatec_device = FanatecDevice(device)
            self.devices.append(fanatec_device)
        except:
            pass
