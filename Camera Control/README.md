# SmartCam Control Endpoints

Current working directory: `/work/www/htdocs_webon/stw-cgi-rest/`

This appears to be the directory where are all of the available control endpoints are documented. You can look for yourself under the extracted firmwre dump in the `Firmware Dumps` folder in the repository.

Each `php` file has multiple submenus you'll need to separetely query in order to GET/PUT configuration.

Eg. `http://192.168.0.243/stw-cgi-rest/image/overlay` to GET/PUT the configuration for overlaying the camera time and date on the video stream.

The list of files in the working directory are as shows:

`eventsources.php` - Controls for motion/audio detection

`image.php` - Image settings (brightness, flip modes, day/night, etc)

`io.php` - Status LED and built-in audio playback

`media.php` - Microphone/Speaker volume

`network.php` - DHCP/Static address, Wi-Fi scanning/change

`security.php` - Changing password (length less than 15 chars.)

`system.php` - Device information, date/time, factory reset, device reboot, firmware update

`transfer.php` - Email notifications, subscription(???)

## Using `curl` to GET/PUT from the camera

### *EXAMPLE:* Enable automatic night vision, without changing the WDR setting

**Note:** Change the IP address to the IP address of your camera, and change password to the admin password set on your camera. The username of admin should not need to changed as the camera does not seemingly permit other user IDs except admin.

```shell
curl -X PUT -d '{"Channel":"0","DayNightMode":"Auto"}' --digest -u admin:password http://192.168.0.243/stw-cgi-rest/image/camera
```

### *EXAMPLE:* Retrieve the camera's model and serial number string

```shell
curl -X GET --digest -u admin:password http://192.168.0.243/information
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Information><modelID>SNH-V6414BN</modelID><SerialNumber>[REDACTED]</SerialNumber></Information>
```

## Using `python` to GET/PUT from the camera

*Disclaimer: This code was written in assistance from an AI LLM system. Operation of this script appears to be sane, but always remember to personally inspect code before executing it.*

**Note:** Change the IP address to the IP address of your camera, and change password to the admin password set on your camera. The username of admin should not need to changed as the camera does not seemingly permit other user IDs except admin.

### *EXAMPLE:* Reset camera to factory defaults

```python
import requests
from requests.auth import HTTPDigestAuth

# Change 192.168.0.243 of the actual IP address of your camera
url = 'http://192.168.0.243/stw-cgi-rest/system/factoryreset'

# Your PUT request data is set here
data = {"ExcludeSettings":"0"}

# Connect to the camera, use digest authentication, and PUT the payload
response = requests.put(url, auth=HTTPDigestAuth('admin', 'password'), data=data)

# Print the result
print(response.status_code)
print(response.headers)
print(response.text)
```

### *EXAMPLE:* Retrieve the exposure setting

```python
import requests
from requests.auth import HTTPDigestAuth

# Change 192.168.0.243 of the actual IP address of your camera
url = 'http://192.168.0.243/stw-cgi-rest/image/imageenhancements'

# Connect to the camera, use digest authentication, and GET the payload
response = requests.get(url, auth=HTTPDigestAuth('admin', 'password'))

print(response.status_code)
print(response.headers)
print(response.text)
```

Status code:

```text
200
```

Headers:

```json
{'X-Powered-By': 'PHP/5.2.17', 'Content-type': 'application/json', 'Transfer-Encoding': 'chunked', 'Date': 'Wed, 09 Apr 2025 02:28:04 GMT', 'Server': 'SmartCamWebService'}
```

Text (returned values):

```json
{"Channel.0.Brightness":60}
```

### *EXAMPLE:* Connect the camera to a Wi-Fi network, with WPA/WPA2 security, and get an IP address from DHCP

***TODO: Is it necessary to add the `Content-Type` header?***

```python
import requests

# You should not need to change the IP address in this instance, since the camera is in setup mode, and is self-assigned by the camera
url = 'http://192.168.123.1/device/network'

xml_data = '''<?xml version="1.0" encoding="UTF-8" ?>
<Network>
    <selectedNetwork>Wireless</selectedNetwork>
    <wireless>
        <fromDHCP>True</fromDHCP>
        <ssid>MyWiFiName</ssid>
        <password>MyWiFiPassword</password>
        <security>WPA</security>
    </wireless>
</Network>
'''

headers = {
    'Content-Type': 'application/xml'
}

# Connect to the camera, do not authenticate (not required), and PUT the payload, also marking it as XML content
response = requests.put(url, data=xml_data, headers=headers)

print(response.status_code)
print(response.headers)
print(response.text)
```

### *EXAMPLE:* Set the admin password for the camera after the inital Wi-Fi setup

***TODO: Is `passwor` REALLY the default password for the camera??? - It's been a while since I last worked on this, so I am not sure.***

```python
import requests
from requests.auth import HTTPDigestAuth

# Change 192.168.0.243 of the actual IP address of your camera
url = 'http://192.168.0.243/stw-cgi-rest/security/users'

# There is only one user ID allowed, keep the Index set to 0, and UserID to admin, while setting the password for that user, to "password".
data = {"Index":"0","UserID":"admin","Password":"password"}

# Connect to the camera, use digest authentication, and PUT the payload
response = requests.put(url, auth=HTTPDigestAuth('admin', 'passwor'), data=data)

print(response.status_code)
print(response.headers)
print(response.text)
```
