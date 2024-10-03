import pyudev


FANATEC_VENDOR_ID = 0x0EB7
FANATEC_MODEL_ID = {
    0x0E03: 'CSL Elite',
    0x0005: 'CSL Elite PS4',
    0x0020: 'CSL DD',
    0x6204: 'CSL Elite Pedals',
    0x0001: 'ClubSport V2',
    0x0004: 'ClubSport V2.5',
    0x183B: 'ClubSport Pedals V3',
    0x0006: 'Podium DD1',
    0x0007: 'Podium DD2',
    0x0011: 'CSR Elite'
}


SYSFS_PATH="/sys/module/hid_fanatec/drivers"
SYSFS_PREFIX='0003'


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


    def is_fanatec_device(device) -> bool:
        vendor_id_str = device.get("ID_VENDOR_ID")
        if vendor_id_str:
            vendor_id = int(vendor_id_str,16)
            return vendor_id == FANATEC_VENDOR_ID
        return False


    def get_model_str(device) -> str:
        device_id_str = device.get("ID_MODEL_ID")
        if device_id_str:
            device_id = int(device_id_str,16)
            if device_id in FANATEC_MODEL_ID:
                return FANATEC_MODEL_ID[device_id]
        return "<unknown>"


    def __list_devices(self):
        devices = context.list_devices(subsystem='input')
        for device in devices:
            if is_fanatec_device(device):
                    self.devices.append(device)


    def start_monitoring(self):
        self.observer = pyudev.MonitorObserver(self.monitor, self.device_event)
        self.observer.start()


    def stop_monitoring(self):
        self.observer.stop()


    def __device_event(self, event, device):
        if is_fanatec_device(device):
            if event=='add':
                self.devices.append(device)
            elif event == 'remove':
                self.devices.remove(device)