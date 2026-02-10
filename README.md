# Samsung SmartCam Local Control

> [!NOTE]
> Documentation is currently being migrated to the [wiki](https://github.com/SamTheGreatCoder/Samsung-SmartCam/wiki).

Samsung announced the discontinuation of the SmartCam line of mobile applications on December 31, 2024. Since then, camera models sold under this line are now EOL (End-of-life), I still have a collection of these fullly functional cameras actively in use, and I do not plan on discarding working devices.

## Goals (in no particular order)

- [ ] Documentation for past, present, and future work regarding these devices
- [ ] Allow cameras to be locally controlled, "Network-of-Things" devices, at minimum without reliance on the original SmartCam servers.
- [ ] Reverse engineer firmware for means discovering available control/setting endpoints for the cameras
- [ ] Archive any related information towards any of the listed goals here
- [ ] Create a REST API to MQTT bridge for integration with other software (including smart home controllers such as Home Assistant)
- [ ] Modify firwmare for devices, (such as restoring locked out functionality like ONVIF PTZ control on the SNH-V6410BN)

> [!WARNING]
> Everything is in still in a very early state, currently documenting the currently found API controls. (See 'Camera Control').

## What works? (primarily tested on SNH-V6410BN/SNH-V6414BN/SNH-V6430BN)

- Connecting the device to Wi-Fi from a factory default state (WPA(2) security with DHCP is the only tested method right now. None/WEP should work like normal, additionally, static IP address assignment may be possible.) **(TODO: Document)**
- Setting the `admin` user account password after successfully joining the camera to Wi-Fi. (RTSP server and streams become active after this) **(TODO: Document)**
- Controlling settings of the camera (this includes Pan/Tilt on included models) **(TODO: Document/Build list)**
- Multiple quality streams from the cameras over RTSP **(TODO: Document)**
- Two-way audio through RTSP/ONVIF Profile T (Tested with [go2rtc](https://github.com/AlexxIT/go2rtc?tab=readme-ov-file#two-way-audio) **(TODO: Document/Instruct)**

## What may not work?

- Controlling SD card recording (at least with the current amount of work looking through the extracted firmware)
- Viewing recorded media on the SD Card (partially because controlling SD card recording does not seem possible. This also might have been a feature that only works when relayed through SmartCam servers. I did find a couple REST API endpoints relating to browsing through media on the SD Card, but if you cannot enable recording then it is ultimately useless)

## What does not work?

- Only time will tell.
