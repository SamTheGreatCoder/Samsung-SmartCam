# SmartCam Control Endpoints - Image Settings (image.php)

All submenus only accept `GET`/`PUT` requests, unless otherwise noted. All others return a 405 error.

Each camera has only 1 "channel" (image sensor), and it starts counting from 0. Setting `Channel` for each `PUT` request is **required** and **must** be set to `0`, otherwise it will be the first case to fail, returning a 400 error.

## Camera submenu

### `/stw-cgi-rest/image/camera` example GET request

```json
{"Channel.0.CompensationMode":"Off","Channel.0.DayNightMode":"Auto"}
```

WDR (Wide dynamic range) is set to `Off` and forced day/night exposure mode is set to `Auto`.

---

Set `CompensationMode` to `"Off"` or `0` to disable WDR, `"WDR"` will enable it.

**Note the quotes around the string, and the lack of quotes for an integer. Setting the value to `3`/`"3"` for WDR does not seem to work.**

Set `DayNightMode` to `"Color"` and force the camera to color mode only, entirely disabling night vision. Setting to `"Auto"` will tell the camera to automatically switch between color and B/W infared night vision.

**Using the php array number does not seem to work for this case.**

### `/stw-cgi-rest/image/camera` example PUT Requests

```json
{"Channel":"0","CompensationMode":"WDR","DayNightMode":"Color"}
```

This will enable WDR while also disabling night vision.

```json
{"Channel":"0","CompensationMode":0}
```

This will disable WDR without making any changes to `DayNightMode`.

## Image Enhancements submenu

### `/stw-cgi-rest/image/imageenhancements` example GET request

```json
{"Channel.0.Brightness":60}
```

Camera exposure (brightness) is currently set to 60%

---

`Brightness` values must be greater than or equal to 1, and less than or equal to 100. Exposure changes do not appear to be absolute, but rather relative targets, and are not guaranteed based on lighting conditions.

### `/stw-cgi-rest/image/imageenhancements` example PUT request

```json
{"Channel":"0","Brightness":"72"}
```

The `Brightness` value seems to be able to be processed whether it is set as an integer (`"Brightness":60`), or a string (`"Brightness":"60"`). In my personal testing and experimentation, the 50-70 range is a good value to work with, at least with WDR enabled.

## Flip submenu

### `/stw-cgi-rest/image/flip` example GET request

```json
{"Channel.0.HorizontalFlipEnable":false,"Channel.0.VerticalFlipEnable":false}
```

Horizontal (mirror) flip is disabled, and vertical (upside down) flip is also disabled, intended to be used when the camera is looking directly at the subject surveilance area, standing up.

---

### `/stw-cgi-rest/image/flip` example PUT requests

Flip values are evaluated as booleans, and must be in lowercase. Invalid examples are `"True"` and `False`.

```json
{"Channel":"0","HorizontalFlipEnable":true,"VerticalFlipEnable":false}
```

Flips the image horizontally (mirror), and orients the view right side up. (For viewing through the reflection of a mirror?)

```json
{"Channel":"0","VerticalFlipEnable":true}
```

Turns the view upside down (mounted from above), while not changing the horizontal view.

**TODO: Does it also invert the PTZ controls on the SNH-V6410BN?**

## Overlay submenu

### `/stw-cgi-rest/image/overlay` example GET request

```json
{"Channel.0.TimeEnable":true}
```

Date and time will be overlayed in the video stream, and subsequently, any local SD card recordings.

---

Setting `TimeEnable` to `true` will overlay the date and time in the video streams, while setting to `false` will not overlay the date and time.

### `/stw-cgi-rest/image/overlay` example PUT request

The `TimeEnable` value is evaluated as a boolean, and must be in lowercase. Invalid examples are `"True"` and `False`.

```json
{"Channel":"0","TimeEnable":false}
```

Disables overlaying the date and time in the video streams.

## Extra information

Line 30 is commented out in the php file, giving an option to force a B/W infared night vision mode:

```php
$DayNightMode = array(
  0 => 'Color',
//  1 => 'BW',
  2 => 'Auto'
 );

$CompensationMode = array(
  0 => "Off",
  3 => "WDR"
 );
```

Line 70 through 95 shows the shutter speed for the image sensor depending on the `CompensationMode` set. Default shutter speed range is 1/5 of a second up to 1/12000. Enabling WDR changes the range to 1/5 up to 1/240 of a second. (Could the sensor be reading at a higher bit-depth and the camera ISP is handling the tonemapping?). It is not clear what each `ShutterSpeed` value means in regards to real shutter speed.

```php
case 'CompensationMode':
    {
        $newValue = array_search($value, $CompensationMode);
            if ($newValue === FALSE)
            {
                header("HTTP/1.1 400 Bad Request");
                return;
            }

            if ($newValue == 3) // WDR
            {
                $imgSet['ImageSetting']->imageExposure->dataInfo['LongShutterSpeed']['value'] = 4; //MinShutter = 1/5
                $imgSet['ImageSetting']->imageExposure->dataInfo['ShortShutterSpeed']['value'] = 16; //MaxShutter = 1/240
            }
            else
            {
                if ($imgSet['ImageSetting']->imageBackLight->dataInfo['Mode']['value'] == 3)
                {
                    $imgSet['ImageSetting']->imageExposure->dataInfo['LongShutterSpeed']['value'] = 4; //MinShutter = 1/5
                    $imgSet['ImageSetting']->imageExposure->dataInfo['ShortShutterSpeed']['value'] = 29; //MaxShutter = 1/12000
                }
            }

        $imgSet['ImageSetting']->imageBackLight->dataInfo['Mode']['value'] = $newValue;
    }
    break;
```
