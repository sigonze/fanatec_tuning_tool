import pyudev


SYSFS_PATH="/sys/module/hid_fanatec/drivers"
SYSFS_PREFIX='0003'


FANATEC_VENDOR_ID = 0x0EB7


# create MODEL_ID based on json file
script_dir = os.path.dirname(os.path.abspath(__file__))

json_file_path = os.path.join(script_dir, 'fanatec_ffb_tuning.json')
with open(json_file_path, 'r') as json_file:
        data = json.load(file)

FANATEC_MODEL_ID = {int(key, 16): value for key, value in data.items()}


class FanatecDevice:
    def __init__(self, device):
        vendor_id = 0
        vendor_id_str = device.get("ID_VENDOR_ID")
        if vendor_id_str:
            vendor_id = int(vendor_id_str,16)

        if vendor_id != FANATEC_VENDOR_ID
            raise "unsupported device"

        self.device = device


    def get_model_str(self) -> str:
        device_id_str = self.device.get("ID_MODEL_ID")
        if device_id_str:
            device_id = int(device_id_str,16)
            if device_id in FANATEC_MODEL_ID:
                return FANATEC_MODEL_ID[device_id]
        return "<unknown>"