import json

class Message:
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def __getitem__(self,key):
        return self.dictionary[key]

    def __setitem__(self,key,value):
        self.dictionary[key] = value

    def __contains__(self,item):
        return item in self.dictionary

    def toNetworkMessage(self):
        msgJson = json.dumps(self.dictionary,separators=(',', ':'))
        length = len(msgJson)
        final = f"L:{length} {msgJson}"
        return str.encode(final)

    def toJSON(self):
        return json.dumps(self.dictionary,separators=(',', ':'))

    def __repr__(self):
        return json.dumps(self.dictionary,separators=(',', ':'))

    def __str__(self):
        return json.dumps(self.dictionary, indent=4) 

    @staticmethod
    def from_json(json_data):
        if (json_data is not None and json_data != "None"):
            return Message(json.loads(json_data))
        else:
            return None

    @staticmethod
    def fromNetworkMessage(data):
        if data.startswith("L:"):
            delimiter = data.index(" ")
            dataLength = int(data[2:delimiter])
            json_data = data[delimiter+1:delimiter+1+dataLength]
            return Message(json.loads(json_data))
        else:
            return None

# ID is an incrementing number
#FROM CAMERA
REGISTRATION = {
        "Type":"registration",
        "ID":1,
        "SystemSerialNumber":"YOURSERIAL",
        "SystemModelNumber":"VMC4030P",
        "SystemFirmwareVersion":"1.125.15.0_35_1191",
        "UpdateSystemModelNumber":"VMC4030P",
        "CommProtocolVersion":1,
        "BatPercent":89,
        "SignalStrengthIndicator":4,
        "LogFrequency":2,
        "BatTech":"Rechargeable",
        "ChargerTech":"None",
        "ChargingState":"Off",
        "ThermalShutdownRechargeMaxTemp":60,
        "Temperature":20,
        "InterfaceVersion":1,
        "Capabilities":["IRLED","PirMotion","NightVision","Temperature","BatteryLevel","Microphone","Speaker","SignalStrength","Solar","BatteryCharging","H.264Streaming","JPEGSnapshot","AutomatedStop","BEC","RaParams"],
        "HardwareRevision":"H3",
        "Sync":False,
        "BattChargeMinTemp":0,
        "BattChargeMaxTemp":60,
        "ThermalShutdownMinTemp":-20,
        "ThermalShutdownMaxTemp":74,
        "BootSeconds":4
        }
#FROM CAMERA
STATUS = {
        "Type":"status",
        "ID":2,
        "SystemFirmwareVersion":"1.125.15.0_35_1191",
        "HardwareRevision":"H3",
        "SystemSerialNumber":"YOURSERIAL",
        "UpdateSystemModelNumber":"VMC4030P",
        "BatPercent":89,
        "BatTech":"Rechargeable",
        "ChargerTech":"None",
        "ChargingState":"Off",
        "WifiCountryDetails":"AT/36",
        "Bat1Volt":7.814,
        "Temperature":20,
        "Battery1CaliVoltage":7.814,
        "SignalStrengthIndicator":4,
        "Streamed":0,
        "UserStreamed":0,
        "MotionStreamed":0,
        "IRLEDsOn":0,
        "PoweredOn":17,
        "CameraOnline":1,
        "CameraOffline":16,
        "WifiConnectionCount":1,
        "WifiConnectionAttempts":1,
        "PIREvents":0,
        "FailedStreams":0,
        "FailedUpgrades":0,
        "SnapshotCount":0,
        "LogFrequency":2,
        "CriticalBatStatus":0,
        "ISPOn":15,"TimeAtPlug":0,
        "TimeAtUnPlug":0,
        "PercentAtPlug":0,
        "PercentAtUnPlug":0,
        "ISPWatchdogCount":0,
        "ISPWatchdogCount2":0,
        "SecsPerPercentCurr":0,
        "SecsPerPercentAvg":0,
        "DdrFailCnt":0,
        "RtcpDiscCnt":0,
        "DhcpFCnt":48,
        "RegFCnt":340,
        "TxErr":0,
        "TxFail":0,
        "TxPhyE1":0,
        "TxPhyE2":0
        }

#FROM CAMERA
ALERT = {
        "Type":"alert",
        "ID":7,
        "AlertType":"pirMotionAlert",
        "PIRMotion":{
            "Triggered":True,
            "TriggerLevel":7970,
            "TriggerRtpTime":0,
            "TriggerSysTime":1,
            "zones":[],
            "MdZones":0,
            "MdPrevZones":0,
            "PirTrigger":0,
            "z0Intensity":0,
            "z0Counter":0,
            "z1Intensity":0,
            "z1Counter":0,
            "z2Intensity":0,
            "z2Counter":0,
            "z3Intensity":0,
            "z3Counter":0
            }
        }

#FROM CAMERA
ALERT_TIMEOUT = {
        "Type":"alert",
        "ID":9,
        "AlertType":"motionTimeoutAlert",
        "StreamDuration":18
        }

#FROM CAMERA
ALERT_AUDIO = {
        "Type":"alert",
        "ID":-1,
        "AlertType":"audioAlert",
        "AudioDetect":{
            "AudioTriggered":True,
            "AudioTriggerLevel":2672,
            "AudioTriggerRtpTime":0,
            "AudioTriggerSysTime":0
            }
        }

#FROM CAMERA
ALERT_AUDIO_TIMEOUT = {
        "Type":"alert",
        "ID":-1,
        "AlertType":"audioTimeoutAlert",
        "StreamDuration":10
        }

STATUS_REQUEST = {"Type":"statusRequest","ID":19}

RA_PARAMS_LOW_QUALITY = {
        "Type":"raParams",
        "ID":-1,
        "Params":{
            "1080p":{
                "minbps":102400,
                "maxbps":532480,
                "minQP":24,
                "maxQP":38,
                "vbr":True,
                "targetbps":409600,
                "cbrbps":409600
                },
            "360p":{
                "minbps":51200,
                "maxbps":307200,
                "minQP":24,
                "maxQP":38,
                "vbr":True,
                "targetbps":102400,
                "cbrbps":102400
                },
            "480p":{
                "minbps":51200,
                "maxbps":409600,
                "minQP":24,
                "maxQP":38,
                "vbr":True,
                "targetbps":307200,
                "cbrbps":307200
                },
            "720p":{
                "minbps":51200,
                "maxbps":532480,
                "minQP":24,
                "maxQP":38,
                "vbr":True,
                "targetbps":409600,
                "cbrbps":409600
                }
            }
        }

RA_PARAMS_MEDIUM_QUALITY = {
        "Type":"raParams",
        "ID":-1,
        "Params":{
            "1080p":{
                "minbps":102400,
                "maxbps":640000,
                "minQP":24,
                "maxQP":38,
                "vbr":True,
                "targetbps":512000,
                "cbrbps":512000
                },
            "360p":{
                "minbps":51200,
                "maxbps":409600,
                "minQP":24,
                "maxQP":38,
                "vbr":True,
                "targetbps":204800,
                "cbrbps":204800
                },
            "480p":{
                "minbps":51200,
                "maxbps":409600,
                "minQP":24,
                "maxQP":38,
                "vbr":True,
                "targetbps":409600,
                "cbrbps":409600
                },
            "720p":{
                "minbps":51200,
                "maxbps":599040,
                "minQP":24,
                "maxQP":38,
                "vbr":True,
                "targetbps":460800,
                "cbrbps":460800
                }
            }
        }

RA_PARAMS_HIGH_QUALITY = {
        "Type":"raParams",
        "ID":-1,
        "Params":{
            "1080p":{
                "minbps":102400,
                "maxbps":819200,
                "minQP":35,
                "maxQP":40,
                "vbr":True,
                "targetbps":614400,
                "cbrbps":614400
                },
            "360p":{
                "minbps":51200,
                "maxbps":512000,
                "minQP":24,
                "maxQP":38,
                "vbr":True,
                "targetbps":409600,
                "cbrbps":409600
                },
            "480p":{
                "minbps":51200,
                "maxbps":614400,
                "minQP":24,
                "maxQP":38,
                "vbr":True,
                "targetbps":512000,
                "cbrbps":512000
                },
            "720p":{
                "minbps":51200,
                "maxbps":665600,
                "minQP":24,
                "maxQP":38,
                "vbr":True,
                "targetbps":512000,
                "cbrbps":512000
                }
            }
        }

#  Destination URL includes serial number
# Camera will POST with a multipart form containing file parameter.
# Will not include temp.jpg in URL
SNAPSHOT = {
        "Type":"fullSnapshot",
        "ID":-1,
        "DestinationURL":"http://172.14.1.1/snapshot/YOURSERIAL_d293116d/temp.jpg"
        }

REGISTER_SET_USER_STREAM_ACTIVE = {
        "Type":"registerSet",
        "ID":-1,
        "SetValues":{
            "UserStreamActive":0  # 0 Active 1 Disabled
            }
        }
        
# Generic registerSet
REGISTER_SET = {
        "Type":"registerSet",
        "ID":-1,
        "SetValues":{
            }
        }

#Enable/Disable motion sensitivity
REGISTER_SET_PIR = {
        "Type":"registerSet",
        "ID":-1,
        "SetValues":{
            "PIREnableLED":True,
            "PIRLEDSensitivity":80
            }
        }

REGISTER_SET_ARMED = {
        "Type":"registerSet",
        "ID":-1,
        "SetValues":{
            "PIRTargetState":"Armed",
            "PIRStartSensitivity":80,
            "PIRAction":"Stream",
            "VideoMotionEstimationEnable":True,
            "VideoMotionSensitivity":80,
            "AudioTargetState":"Disarmed"
            }
        }

REGISTER_SET_DISARMED = {
        "Type":"registerSet",
        "ID":-1,
        "SetValues":{
            "PIRTargetState":"Disarmed",
            "AudioTargetState":"Disarmed",
            "VideoMotionEstimationEnable":False,
            "DefaultMotionStreamTimeLimit":10
            }
        }

REGISTER_SET_INITIAL = {
        "Type":"registerSet",
        "ID":-1,
        "SetValues":{
                "AudioMicVolume":4,
                "AudioSpkrEnable":False,
                "VideoExposureCompensation":0,
                "VideoMirror":False,
                "VideoFlip":False,
                "VideoWindowStartX":0,
                "VideoWindowStartY":0,
                "VideoWindowEndX":1280,
                "VideoWindowEndY":720,
                "MaxMissedBeaconTime":10,
                "MaxStreamTimeLimit":1800,
                "VideoAntiFlickerRate":50,
                "WifiCountryCode":"EU",
                "NightVisionMode":True,
                "HdrControl":"off",
                "MaxUserStreamTimeLimit":1800,
                "MaxMotionStreamTimeLimit":120,
                "VideoMode":"superWide",
                "JPEGOutputResolution":"",
                "ChargeNotificationLed":0,
                "AudioMicAGC":0,
                "VideoOutputResolution":"1080p",
                "VideoTargetBitrate":600,
                "Audio0EncodeFormat":0,
                "Audio1EncodeFormat":1,
                "ArloSmart":True,
                "AlertBackoffTime":0,
                "PIRTargetState":"Disarmed",
                "AudioTargetState":"Disarmed",
                "VideoMotionEstimationEnable":False,
                "DefaultMotionStreamTimeLimit":10
                }
        }

RESPONSE = {
        "Type":"response",
        "ID":-1,
        "Response":"Ack"
        }
