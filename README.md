# Arlo Cam API

This project forks [Meatballs1/arlo-cam-api](https://github.com/Meatballs1/arlo-cam-api) which simulates the Arlo Basestation to communicate with cameras.

Based on reconstructing the communication between a VMB4000r3, Arlo Pro 2 cameras (VMC4030P), and Arlo Audio Doorbells.

It won't work with the mobile app, and there is no real plan to support this at present. However, it does allow you to use your Arlo cameras as normal RTSP camera sources for other media recorders, and your Audio Doorbell as a Wi-Fi motion and binary sensor.

We can either emulate the basestation using the same SSID and capture and re-use the WPA-PSK to make the cameras connect to us. Or we can try and use WPS to get the cameras to sync to our own basestation.

You can't use the camera's native direct-join-to-WiFi functionality; you must pair the camera as you would to a base station.

Finally, while you can use the API to control the camera (e.g. set quality, arm/disarm), there is NO state maintained; if the camera restarts, or falls off WiFi and rejoins/reregisters, it will be reprovisioned with the defaults, so you will need to issue your commands to the camera again.

## Tested Working Hardware

- Ultra (VMC5040)
- Pro 2 (VMC4030P)
- Essential Spotlight Camera (VMC2030B)
- Audio Doorbell (AAD1001)

## API Configuration

First, create a `config.yaml` file (available in this repo) that will be used to configure the server.

```
WifiCountryCode: "US"
VideoAntiFlickerRate: 60
NotifyOnMotionAlert: true
NotifyOnAudioAlert: false
NotifyOnButtonPressAlert: true
MotionRecordingWebHookUrl: "http://192.168.1.100:4321/endpoint/@scrypted/arlo-local/public/motionDetected"
AudioRecordingWebHookUrl: "http://192.168.1.100:4321/endpoint/@scrypted/arlo-local/public/"
UserRecordingWebHookUrl: "http://192.168.1.100:4321/endpoint/@scrypted/arlo-local/public/"
StatusUpdateWebHookUrl: "http://192.168.1.100:4321/endpoint/@scrypted/arlo-local/public/statusUpdated"
RegistrationWebHookUrl: "http://192.168.1.100:4321/endpoint/@scrypted/arlo-local/public/registered"
ButtonPressWebHookUrl: "http://192.168.1.100:4321/endpoint/@scrypted/arlo-local/public/buttonPressed"
```

You'll want to replace the `WifiCountryCode` with your two-letter ISO3166-1 alpha-2 code, and the `VideoAntiFlickerRate` with `50` or `60`—whatever electrical frequency your country uses (e.g. most of Europe uses 50 Hz, the US uses 60 Hz).

. If you want to use webhooks, currently only the following webhooks are functional:
- `RegistrationWebHookUrl`
- `StatusUpdateWebHookUrl`
- `MotionRecordingWebHookUrl`
- `ButtonPressWebHookUrl`

If you are using this server with Scrypted:
- Replace `RegistrationWebHookUrl` with the `Registration Webhook` from the Scrypted plugin configuration.
- Replace `StatusUpdateWebHookUrl` with the `Status Update Webhook` from the Scrypted plugin configuration.
- Replace `MotionRecordingWebHookUrl` with the `Motion Sensor Webhook` from the Scrypted plugin configuration.
- Replace `ButtonPressWebHookUrl` with the Status `Button Press Webhook` from the Scrypted plugin configuration.

## Run the Server

### Using Docker Compose (recommended)

1. Adjust the configuration below to point to your `config.yaml` file.
1. (Optional) Create a file to store the sqlite database used by the server and mount it.

```
version: '3.8'
services:
  arlo-cam-api:
    container_name: 'arlo-cam-api'
    image: 'bschrameck/arlo-cam-api'        
    ports:
      - 4000:4000
      - 4100:4100
      - 5000:5000
    volumes:
      - ./config.yaml:/opt/arlo-cam-api/config.yaml
      - ./arlo.db:/opt/arlo-cam-api/arlo.db
    restart: 'always'
```

### Using Docker

Similar guidance as the Docker Compose method as above:

```
touch arlo.db

docker run -d \
    -p 4000:4000 -p 4100:4100 -p 5000:5000 \
    --volume "$(pwd)"/config.yaml:/opt/arlo-cam-api/config.yaml \
    --volume "$(pwd)"/arlo.db:/opt/arlo-cam-api/arlo.db bschrameck/arlo-cam-api
```

### Manually

Clone the repository and install the necessary dependencies.
```
sudo apt install -y python3-pip
git clone https://github.com/brianschrameck/arlo-cam-api.git
cd arlo-cam-api
pip3 install -r requirements.txt
```

Modify the `config.yaml` file as above, then start the server:

```
python3 server.py
```

How you keep the server running/start it automatically at boot is an exercise left to the reader.

## Networking

The Arlo cameras assume that they will be talking with their Base Station server using port 4000 on *the default gateway* passed from the DHCP server (usually your router). Audio Doorbells use port 4100. Assuming you are not running the API software on your router, you'll need a way to redirect the camera's requests to your server host.

Below are a few ways to do that:

- Add a static lease to your DCHP server that also sets the default gateway to the host running the server software software (recommended) 
- Create a port forward on port 4000 and 4100 on the LAN side of your router to redirect traffic to the host running the server software software
- Run the cameras in a different VLAN and configure NAT rules to route traffic to the host running the server software software; this is a tested working scenario:

    Let's say you run a Ubiquiti UniFi network in your home, using a Unifi Security Gateway (a.k.a USG3P). Your cameras reside on VLAN 3 (192.168.3.0/24), while your server running the Arlo Cam API resides on the default untagged LAN at 192.168.1.100. The cameras will try to talk to 192.168.3.1 by default in this configuration. To forward the requests to your server, instead of the default gateway, you could use [Ubiquiti's instructions](https://help.ui.com/hc/en-us/articles/215458888-UniFi-USG-Advanced-Configuration-Using-config-gateway-json) to modify the `config.gateway.json` file to look something like this (repeating the same for port 4100):

    ```
    {
        "service": {
            "nat": {
                "rule": {
                    "1": {
                    "description": "Redirect Arlo camera traffic to arlo-cam-api",
                    "destination": {
                        "address": "192.168.3.1",
                        "port": "4000"
                    },
                    "inside-address": {
                        "address": "192.168.1.100"
                    },
                    "inbound-interface": "eth1.3",
                    "protocol": "tcp_udp",
                    "type": "destination",
                    "log": "enable"
                    }
                }
            }
        }
    }
    ```
- If your networking equipment doesn't allow for any of the above, you'll need to [set up a Linux computer](https://github.com/brianschrameck/arlo-cam-api#pairing-a-camera-to-your-own-basestation) to run the API and act as a base station. This requires you to configure `hostapd` and `dhcpcd` to turn your Linux machine into an access point. You would then need to configure a static route between your main network where you run your camera software (e.g. Scrypted), and the network subnet that the cameras would join. Alternatively, you could run the camera software on the same machine that hosts Arlo Cam API and your wireless access point to avoid setting up a static route.


## Capture Real Base Station WPA-PSK

The Arlo Base Station is really just a Wi-Fi router running some custom software and Arlo cameras are paired with the Base Station using Wi-Fi Protected Setup, or WPS. When you press the `SYNC` button on your camera and base station, the two devices authenticate and exchange the information necessary for the camera to connect to the Base Station.

The goal here is to trick the Arlo Base Station into thinking you are a camera so that it gives you the WPA-PSK (i.e. the Wi-Fi password for the base station). To do this, you'll need a Linux machine with a Wi-Fi card. We'll use that machine to connect to the Base Station, but we'll simulate a WPS Pushbutton Configuration (PBC) that will tell the Base Station to give us the WPA-PSK.

*These instructions were run on Ubuntu, but can likely be adapted to your Linux distro.*

1. Install dependencies:

```
apt install wpasupplicant wireless-tools
```

2. Create a `wpa.conf` file with the following information:

```
ctrl_interface=/var/run/wpa_supplicant
ctrl_interface_group=0
update_config=1
device_name=NTGRDEV
manufacturer=broadcom technology, Inc.
```

3. Run these commands, replacing `wlan0` with the interface name of your wireless card (can be obtained by looking at `ifconfig`.) For example, your card may be named `wlo1`. You'll also need the network name of your Arlo Base Station; for example `NETGEAR81`. Be sure to replace the `essid` argument with yours.

```
systemctl stop NetworkManager.service
wpa_supplicant -t -Dwext -i wlan0 -c wpa.conf
iwconfig wlan0 essid NETGEAR81
```

4. Put your Base Station into pairing mode by using the Arlo app or by pressing the `SYNC` button on it, then run this command (again, replacing `wlan0` as necessary):

```
wpa_cli -i wlan0 wps_pbc
```
If all goes well, your `wpa.conf` file should be updated with a section that contains the Wi-Fi network configuration, including the WPA-PSK.

## Set Up A Wi-Fi Network

You can now configure your own Wi-Fi network with that same information (same SSID, using WPA2 with the given PSK). This can be done using a separate wireless access point with a different SSID, or you may be able to broadcast additional SSIDs from your existing router/access point.

You may also have to set the Wi-Fi to the same channel that the Base Station was using for cameras to connect successfully. There are many apps on the market to view wireless networks and their channels around you. Or you can just try switching to each channel for several minutes to see if the cameras connect.

After setting up your Wi-Fi network, unplug your Arlo Base Station and give the cameras a few minutes to reconnect. You can tell when things are working when you tail your API server logs and can see registration and status messages for your camera.

# Appendix

## API

The service spins up a REST API on TCP port 5000. The api.postman_collection.json config
contains all of the functioning endpoints to import into Postman.

## Pairing a camera to your own basestation

The cameras seem fairly happy to connect to any basestation when they the `SYNC` button is pressed. With hostapd the following configuration in `/etc/hostapd/hostapd.conf` was used:

```
beacon_int=100
ssid=NETGEAR07
interface=wlan0
channel=1
ctrl_interface=/var/run/hostapd
wpa_passphrase=YOUR_PSK_HERE
ctrl_interface_group=0
eap_server=1
wps_pin_requests=/var/run/hostapd.pin-req
config_methods=label display push_button keypad
wps_state=2
ap_setup_locked=1
ieee80211n=1
ignore_broadcast_ssid=0
```

PBC can be activated using:

```
hostapd_cli wps_pbc
```

There is also a script to setup a Raspberry Pi with hostapd/dnsmasq and configure the server within systemd. Should work well on a fresh Raspberry Pi - remember to change the PSK, SSID, and WLAN interface first.

## Video streaming

The camera RTSP stream is available on `http://CAMERA_IP/live`. For 4K cameras, it seems to be served on port 555 instead of the standard 554.

The FFmpeg library doesn't send RTCP Response Received messages very often, and the camera seems to timeout the stream, and force itself to reauth to the wifi if this happens. This means FFmpeg and dependent apps seem to kill the camera after about 6seconds. libVLC seems to work, also Live555 - openRTSP.

Blocking ALL RTCP (by dropping all UDP) appears to allow FFMPEG to function, as the cameras dont mind if no RTCP responses are received. However, if the connection dies without a TEARDOWN from the client then the cameras may just keep sending RTP packets and may require a reboot as they don't know the client has disconnected.

## Audio Streaming to the Camera

The UDP port 5000 on the cameras constantly listens for RTP traffic with the following encoding:

Audio: pcm_mulaw, 8000 Hz, mono, s16, 64 kb/s

```
ffmpeg -re -i piano2.wav  -ar 8000 -sample_fmt s16 -ac 1 -f rtp rtp://172.14.1.194:5000
ffmpeg -f alsa -channels 1 -i hw:1  -ar 8000 -sample_fmt s16 -ac 1 -f rtp rtp://172.14.1.194:5000
```

Where hw:1 matches source input hardware device etc

Sending audio whilst the camera is streaming appears to kill audio...

## Temperature Sensor

A camera *on battery power* reports near ambient temperatures for it's temperature that seems to be accurate within a few degrees. This can be retrieved with a status request via the API.

## Other Gotchas

1. I coulnd't seem to get TCP connections to the RTSP stream to work; only UDP.

2. Always ensure your UDP connection sends the `TEARDOWN` request, otherwise the camera will just keep sending data.

3. If you have multiple Wi-Fi access points, the cameras tend to hold on to one. You may want to reboot your camera right next to the access point you want it to connect to. If you have the ability to modify the Minimum RSSI then you can also do that to try and force cameras onto the right access point. Or if you have the ability to lock a camera to an access point in your network software, that can work. However, like mentioned above, you may need to have whatever access points you want the cameras to use to all share the same Wi-Fi channel.

4. If you are getting `ECONNREFUSED` errors in the plugin/camera console, this means your camera is already sending a stream to another socket. This can happen if a client leaves the socket open for some reason, or doesn't send a `TEARDOWN` command. I've had success rebooting the camera in that situation (pulling the battery). Or you can bump them off the Wi-Fi for a few minutes, at which point they should give up and reset the stream.

5. The live stream can be pretty jittery. Make sure you have VERY strong Wi-Fi coverage for the cameras.

6. You can't control the cameras without using the REST API directly. They are defaulted to always "armed" which means they will always send a motion notification. Video quality is defaulted to "subscription".

7. The camera streams have no authentication mechanism, and they are sent unencrypted over the wire. Use them only on a network you own and trust, as anybody could theoretically listen to the traffic and reconstruct the video by sniffing the packets.
