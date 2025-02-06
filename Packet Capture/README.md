# Packet Capture
As it currently stands, the only useful part for packet capture, was to reverse engineer the inital setup process the SmartCam app uses to send the Wi-Fi credentials to the device. It appears that once the camera is connected to the internet, the Smartcam app switches to communicating with the camera through the Smartcam servers, using the XMPP protocol, which is encrypted. At the moment I have been unsuccessful in trying to decrypt the XMPP TLS traffic.

## TL:DR Version
### Tested on SNH-V6414BN
SmartCam devices use WPA with TKIP for the setup wireless network. The PSK password is `smartcam`. The wireless driver seems to only allow one station to associate at a time. Once connected to the camera's setup Wi-Fi network, the app sends out a HTTP 1.1 GET Request to `http://192.168.123.1/information` *(TODO: is it getting sent there because it's hardcoded in the app or because it's the router/gateway address advertised?)*. The camera returns the model number and serial number in XML format.
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Information>
    <modelID>SNH-V6414BN</modelID>
    <SerialNumber>**(REDACTED)**</SerialNumber>
</Information>
```
My assumption then is that the app checks the `modelID` value to see if it is eligible to be setup. <br>
Following that, the SmartCam sends out another HTTP 1.1 GET request to `http://192.168.123.1/device/network/aplist`. This appears to hang for a moment as the camera performs a scan of nearby access points, before returning another XML formatted response.
### TODO: What does WEP and None look like in the security field?
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Network>
    <aplist>
        <id>1</id>
        <ssid>Network1</ssid>
        <rssi>100</rssi>
        <security>WPA</security>
    </aplist>
    <aplist>
        <id>2</id>
        <ssid>Network2</ssid>
        <rssi>100</rssi>
        <security>WPA</security>
    </aplist>
    <aplist>
        <id>3</id>
        <ssid>Network3</ssid>
        <rssi>82</rssi>
        <security>WPA</security>
    </aplist>
</Network>
```
At this stage in the SmartCam app, the user is prompted to choose the Wi-Fi network they want to connect the camera to, and to enter the encryption password for it. Once the user confirms to connect, the mobile device sends an XML formatted, HTTP 1.1 PUT request to `http://192.168.123.1/device/network`, with the wireless credentials. **Security alert: This is sent in plain text, with no authentication on the web server, and over a WPA/TKIP connection with a guessable dictionary encryption password.**
### TODO: What do WEP and None look like in the security field? If `fromDHCP` is set to false, is it possible to send a static IP configuration?
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<Network>
    <selectedNetwork>Wireless</selectedNetwork>
    <wireless>
        <fromDHCP>True</fromDHCP>
        <ssid>**(REDACTED)**</ssid>
        <password>**(REDACTED)**</password>
        <security>WPA</security>
    </wireless>
</Network>
```
Once the camera starts to connect to Wi-Fi, the Smartcam app switches to XMPP over SmartCam servers, waiting for the camera to register itself and the useful part of wireless monitoring/packet capture ends here. The next part of setup in the app for the name and admin password for the camera are not done locally.

## Detailed Version (including airmon-ng and Wireshark)
### Disclaimer: This is not an in-depth tutorial about how to use airmon-ng, Wireshark, or perform packet capturing. Ideally you should be already familar with the concepts demonstrated here.

#### Test system: Microsoft Surface Pro 8, Intel AX201 (CNVio), running on Manjaro, linux-surface kernel ```6.12.7-arch1-1-surface```, and `iw` version `6.9`

To start, you'll need a wireless NIC/driver in your packet capture system, capable of both at minimum 802.11b and running in monitor mode. Most mainline kernel drivers should support monitor mode, such as ```ath9k/ath10k/ath11k```, ```iwlwifi```, and ```mt76```. Broadcom/NDISWrapper users may need to explore the different (if possible) procedure to place the wireless card in monitor mode.
```
iw list
```
In the output list, look in the ``Supported interface modes:`` section, below the ``Supported Ciphers:`` and ``Available/Configured Antennas:`` section. Specifically, look for a mention of ``monitor`` being a supported mode.
<br>
```bash
* monitor
```
Now the wireless NIC can be put into monitor mode. <b>Replace ``wlp0s20f3`` with the name of your wireless interface from something like `ip a`.</b>
```bash
airmon-ng start wlp0s20f3
```
When I performed this, the wireless interface was renamed to `wlp0s20f3mon`. You'll need this updated interface name to actually start the capture with `airodump-ng` and to stop monitor mode when you're finished capturing packets.
<br>
<br>
To actually begin packet capturing, you'll need to find the broadcast SSID of the camera, the wireless channel it's being broadcast on, the name of wireless monitor interface, and a place to store the captured wireless packets.
#### NOTES:
1. The MAC address printed on the camera will not be the same mac address used for the setup access point network. Eg. (00:16:6C:xx:xx:xx) became (02:16:6C:xx:xx:xx). Use a wireless utility that can display the BSSID of an access point (Android, some Linux desktop environments, or some other means through CLI)
2. In my tests, the wireless channel was always 1 on the 2.4Ghz spectrum. Again, confirm this by your own utilities.
3. You can find the updated name of the monitoring wireless interface by rerunning `ip a` or equivalent depeding on your environment.
4. A short term packet capture should not require a significant amount of storage, though longer capture sessions can extend into multiple hundreds of megabytes.
5. Keep the camera, your setup device, your packet capture device, and your access point nearby (ideally in the same room or spread out in an open air environment). This helps keeps a smooth setup flow, and prevents lost or garbled packets on the capture system.
```bash
airodump-ng --bssid 02:16:6C:xx:xx:xx --channel 1 wlp0s20f3mon -w airodump.ng
```
Replace `02:16:6C:xx:xx:xx` with the BSSID of your camera, `wlp0s20f3mon` with the monitor interface of your wireless card, `1` with the actual channel your camera is operating on, and `airodump.ng` with the file name prefix you wish to use for the dump. ```airodump``` on it's own adds a numerical increment to the file name and puts a ```.cap``` extension at the end. In this running example I continued to use ```airodump.ng``` not knowing this.
<br><i>Extra note: you can also instead initiate a capture using the MAC address of the device you're using to connect to the camera, like your phone, tablet, or other device running the SmartCam app.</i>``airodump-ng --bssid 7C:10:C9:xx:xx:xx --channel 1 wlp0s20f3mon -w airodump.ng``
```
CH  1 ][ Elapsed: 1 hour 51 mins ][ 2024-12-31 02:38 ][ WPA handshake: 02:16:6C:xx:xx:xx

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

 02:16:6C:xx:xx:xx  -34 100    58123   192490    0   1   54e. WPA  TKIP   PSK  PGZNG1                       

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes

 02:16:6C:xx:xx:xx  7C:10:C9:xx:xx:xx  -49   54e-36e     0    21946                                         
 02:16:6C:xx:xx:xx  44:78:3E:FF:88:B1  -44   54e- 6e     0   175468  EAPOL  PGZNG1
```
Above is an example layout of what the `airodump-ng` program will display in the console during your packet capture session. In this example, I am capturing with the source being from the camera itself. Under station is where you can see the various destinations of those packets. The first address under station is the device I used to setup the camera, and the second station in the list is the AP the camera was instructed to connect to. Now that the capture process is underway at this point, connect your setup device to the camera and setup the camera like usual.<br>
<br>
Since after the camera connects to Wi-Fi and switches to communicating through the cloud over encrypted XMPP, the only neccessary part of setup to packet capture is connecting the camera to Wi-Fi. Once you have finished that part of setup in the app, you can stop the packet capture and move onto analyzing the captured packets in Wireshark.

### Analyzing the captured packets in Wireshark
1. Open the file created by ```airodump``` in Wireshark.
2. Right/secondary click the first 802.11 frame shown in the list (none of the properties about the packet apply here)
3. Choose ```Protocol preferences``` > ```IEEE 802.11 Wireless LAN``` > ```Decryption Keys```.
4. Add a new ```wpa-pwd``` key ```smartcam``` (matching the password for the SmartCam setup Wi-Fi network)
5. Repeat step 3, but ensure that ```Enable decryption``` is checked, above the ```Decryption Keys``` option.
6. Filter the Wireshark results with ```http```
7. Done.
<br>
<i>
The following screenshots assume that you have perfromed the initial Wi-Fi setup on a single camera only once. 
</i>
<br>
![Wireshark Filtered Results](https://github.com/user-attachments/assets/9fd99a96-7cd6-444a-95df-b973b4e88215)
<br>
The inital Wi-Fi setup process is a 6-step procedure.
1. Mobile device connects to camera getting for information.
2. Camera responds with model and serial number.<br>
![Information Query Response](https://github.com/user-attachments/assets/f8ed9ddc-6ed3-437b-a3ff-256bb99bb7fe)
3. Mobile device requests a list of visible access points from the camera.
4. Camera scans for nearby access points, then responds with XML-formatted list.<br>
![AP List Response](https://github.com/user-attachments/assets/94dbb45f-06b8-4157-a728-d5a7280ee14f)
5. Mobile device send the user-specified Wi-Fi credentials to the camera.<br>
![Network Config PUT](https://github.com/user-attachments/assets/c79b6aea-9416-47a1-9d5b-2f66b9f384b6)
6. Camera acknowledges and switches to station mode.
