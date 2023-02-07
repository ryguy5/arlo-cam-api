from arlo.camera import Camera, DEVICE_PREFIXES as CAM_PFIXES
from arlo.audio_doorbell import AudioDoorbell, DEVICE_PREFIXES as AUD_DBELL_PFIXES

import threading


class DeviceFactory:
    sqliteLock = threading.Lock()

    @staticmethod
    def createDevice(ip, registration):
        serial_number = registration['SystemModelNumber']
        if serial_number.startswith(tuple(CAM_PFIXES)):
            device = Camera(ip, registration)
        elif serial_number.startswith(tuple(AUD_DBELL_PFIXES)):
            device = AudioDoorbell(ip, registration)
        else:
            return None

        device.status = {}
        device.friendly_name = serial_number
        return device
