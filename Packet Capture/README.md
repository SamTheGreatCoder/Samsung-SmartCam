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
My assumption then is that the app checks the `modelID` value to see if it is able to be setup. <br>
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

## Fully Explained Version (including airmon-ng and Wireshark)
TODO