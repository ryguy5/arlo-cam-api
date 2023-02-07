import time
from helpers.safe_print import s_print
from webhooks import webhook
from webhooks.senders import targeted


class WebHookManager:
    def __init__(self, config):
        self.config = config

    ### REGISTRATION RECEIVED ###

    def registration_received(self, ip, friendly_name, hostname, serial_number, registration):
        r = self.__registration(ip, friendly_name, hostname, serial_number, registration, time.time(),
                              url=self.config['RegistrationWebHookUrl'], encoding="application/json", timeout=5)
        s_print(str(r))

    @webhook(sender_callable=targeted.sender)
    def __registration(self, ip, friendly_name, hostname, serial_number, registration, _time, url, encoding, timeout):
        return {"ip": ip, "friendly_name": friendly_name, "hostname": hostname, "serial_number": serial_number, "registration": registration, "time": _time}

    ### STATUS RECEIVED ###

    def status_received(self, ip, friendly_name, hostname, serial_number, status):
        r = self.__status(ip, friendly_name, hostname, serial_number, status, time.time(),
                        url=self.config['StatusUpdateWebHookUrl'], encoding="application/json", timeout=5)
        s_print(str(r))

    @webhook(sender_callable=targeted.sender)
    def __status(self, ip, friendly_name, hostname, serial_number, status, _time, url, encoding, timeout):
        return {"ip": ip, "friendly_name": friendly_name, "hostname": hostname, "serial_number": serial_number, "status": status, "time": _time}

    ### MOTION DETECTED ###

    def motion_detected(self, ip, friendly_name, hostname, serial_number, zone, file_name):
        r = self.__motion(ip, friendly_name, hostname, serial_number, zone, file_name, time.time(),
                        url=self.config['MotionRecordingWebHookUrl'], encoding="application/json", timeout=5)
        s_print(str(r))

    @webhook(sender_callable=targeted.sender)
    def __motion(self, ip, friendly_name, hostname, serial_number, zone, file_name, _time, url, encoding, timeout):
        return {"ip": ip, "friendly_name": friendly_name, "hostname": hostname, "serial_number": serial_number, "zone": zone, "file_name": file_name, "time": _time}

    ### BUTTON PRESSED ###

    def button_pressed(self, ip, friendly_name, hostname, serial_number, triggered):
        r = self.__button_press(ip, friendly_name, hostname, serial_number, triggered, time.time(),
                              url=self.config['ButtonPressWebHookUrl'], encoding="application/json", timeout=5)
        s_print(str(r))

    @webhook(sender_callable=targeted.sender)
    def __button_press(self, ip, friendly_name, hostname, serial_number, triggered, _time, url, encoding, timeout):
        return {"ip": ip, "friendly_name": friendly_name, "hostname": hostname, "serial_number": serial_number, "triggered": triggered, "time": _time}
