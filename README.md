# Samsung SmartCam Local Control Project
Samsung/Hanwha Techwin announced the discontinuation of the Samsung SmartCam and Samsung SmartCam+ line of mobile applications on December 31, 2024. While these camera models are all considered EOL (End-of-life), I still have a collection of these fullly functional cameras actively in use, and I don't intend on discarding working devices.

## Goals (in no particular order)
- [ ] Provide documentation recreating past, present, and future progress and work regarding these devices
- [ ] Prevent the cameras from accessing the internet, turning them into locally controlled, NOT (Network of Things) devices.
- [ ] Reverse engineer any available firmware for means of discovering available control/setting endpoints for the cameras
- [ ] Archive any related information towards any of the listed goals here
- [ ] Create a REST API to MQTT bridge for ease of integration into smart home controllers (such as Home Assistant)
- [ ] Create modified firwmare for the devices, restoring locked out functionality (such as ONVIF PTZ control on the SNH-V6410BN)

## NOTE: THIS PROJECT IS IN A VERY EARLY STAGE. MANY ASPECTS OF THIS REPOSITORY ARE UNFINISHED AND WILL BE MERELY DATA "DUMPS".

## What works? (primarily tested on SNH-V6410BN/SNH-V6414BN/SNH-V6430BN)
- Connecting the device to Wi-Fi from a factory default state (WPA security with DHCP is the only tested method right now. None/WEP should be possible, and possibly static addressing too) **(TODO: Document)**
- Setting the `admin` user account password after joining the device to Wi-Fi. (RTSP server and streams become active after this) **(TODO: Document)**
- Controlling various settings of the camera **(TODO: Document/Build list)**
- Multiple quality streams from the cameras over RTSP **(TODO: Document)**

## What may not work?
- Two-way audio (despite the Android app for SmartCam+ making use of STUN for a connection to the camera, the two-way audio might still be relayed in a way that I have not been able to packet capture and understand yet. I am also unsure if two-way audio works through RTSP backchannel connections, though I doubt it.)
- Viewing recorded media on the SD Card (this also might have been a feature that only works when relayed through SmartCam servers, though I did find a couple REST API endpoints relating to browsing through media on the SD Card)

## What doesn't work?
- Unknown
