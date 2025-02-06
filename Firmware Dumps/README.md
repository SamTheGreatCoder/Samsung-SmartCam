# Firmware Dumps
While not officially "dumps" these were publically (last downloaded December 31, 2024) available firmware update archives from the SmartCam servers.

## Download yourself (website fails DNS lookup as of 2/6/25 - this method no longer works):
http://www.samsungsmartcam.com/firmware/firmware.xml
(found in `/work/www/htdocs_webon/stw-cgi-rest/system.php`)

Download instructions: 
1. View XML file to find the file name for the model number (use either the one located in this folder or downloading from the URL above)
2. Replace `firmware.xml` in the link to the file name of your choosing
- Example: http://www.samsungsmartcam.com/firmware/snhv6410pn.tgz

## Extract firmware
### (Tested on a SNH-V6410PN)

## Note: Various cameras seem to make use of various firmware image layouts. Some firmware archives also don't appear to be openable by commonly used archive utilities (Ark/7-Zip)

### Linux:
1. Setup python virtual environment for ubi_reader
- ``python3 -m venv ./ubi_reader-venv``
- ``source ./ubi_reader-venv/bin/activate``
- ``pip install ubi-reader``
2. Use `ubi-reader` to extract the root filesystem from the `ubifs` image (run inside the directory for the extracted firmware image)
- ``ubireader_extract_files ./ubifs``
3. Extracted root file system is in `./ubifs-root/(numbers)/rootfs`
- `(numbers)` varies depending on the firmware image, it is not a variable
### Windows:
