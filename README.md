# Samsung SmartCam Maintainence Project
Samsung/Hanwha Techwin announced they'd be discontinuing the Samsung SmartCam and Samsung SmartCam+ line of mobile applications on December 31, 2024. While these camera models are all considered EOL (End-of-life), these are still usable cameras in the current day and age, and I don't intend on discarding perfectly good devices.

## NOTE: THIS PROJECT IS IN A VERY EARLY STAGE. MANY ASPECTS OF THIS REPOSITORY ARE UNFINISHED AND WILL BE MERELY DATA "DUMPS".

## What works?
- Connecting the device to Wi-Fi from a factory default state (WPA security with DHCP is the only tested method right now. None/WEP should be possible, and possibly static addressing too)
- Setting the `admin` user account password after joining the device to Wi-Fi. (RTSP server and streams become active after this)
- Controlling various settings of the camera (TODO: Build list)

## What may not work?
- Two-way audio (despite the Android app for SmartCam+ making use of STUN for a connection to the camera, the two-way audio might still be relayed in a way that I have not been able to packet capture and understand yet. I am also unsure if two-way audio works through RTSP backchannel connections, though I doubt it.)
- Viewing recorded media on the SD Card (this also might have been a feature that only works when relayed through SmartCam servers, though I did find a couple REST API endpoints relating to browsing through media on the SD Card)

## What doesn't work?
- Unknown
