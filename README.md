# Samsung SmartCam Local Control Project

Samsung announced the discontinuation of the SmartCam line of mobile applications on December 31, 2024. Since then, camera models sold under this line are now EOL (End-of-life), I still have a collection of these fullly functional cameras actively in use, and I do not plan on discarding working devices.

## Goals (in no particular order)

- [ ] Provide documentation recreating past, present, and future progress and work regarding these devices
- [ ] Prevent the cameras from accessing the internet, turning them into locally controlled, NOT (Network of Things) devices.
- [ ] Reverse engineer any available firmware for means of discovering available control/setting endpoints for the cameras
- [ ] Archive any related information towards any of the listed goals here
- [ ] Create a REST API to MQTT bridge for ease of integration into smart home controllers (such as Home Assistant)
- [ ] Create modified firwmare for the devices, restoring locked out functionality (such as ONVIF PTZ control on the SNH-V6410BN)

## NOTE: THIS PROJECT IS IN A VERY EARLY STAGE. MANY ASPECTS OF THIS REPOSITORY ARE UNFINISHED AND WILL BE MERELY DATA "DUMPS"

- Currently in progress: documenting all possible camera API endpoint controls. (See `Camera Control`).

## What works? (primarily tested on SNH-V6410BN/SNH-V6414BN/SNH-V6430BN)

- Connecting the device to Wi-Fi from a factory default state (WPA security with DHCP is the only tested method right now. None/WEP should be possible, and possibly static addressing too) **(TODO: Document)**
- Setting the `admin` user account password after joining the device to Wi-Fi. (RTSP server and streams become active after this) **(TODO: Document)**
- Controlling various settings of the camera (this includes Pan/Tilt on included models) **(TODO: Document/Build list)**
- Multiple quality streams from the cameras over RTSP **(TODO: Document)**
- Two-way audio through RTSP/ONVIF Profile T (https://github.com/AlexxIT/go2rtc?tab=readme-ov-file#two-way-audio) **(TODO: Document/Instruct)**

## What may not work?

- Controlling SD card recording (at least with the current amount of work looking through the extracted firmware)
- Viewing recorded media on the SD Card (partially because controlling SD card recording does not seem possible. This also might have been a feature that only works when relayed through SmartCam servers. I did find a couple REST API endpoints relating to browsing through media on the SD Card, but if you cannot enable recording then it is ultimately useless)

## What does not work?

- Only time will tell.