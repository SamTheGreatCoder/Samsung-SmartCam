<?php
/**
 * iWatch General Config
 *
 * Unauthorized use of these files is an infringement of Canadian and
 * International copyright laws.  For full  copyright and license information, please
 * view the LICENSE file that was distributed with this platform.
 *
 * iWatchConfig class
 * 
 * @package         
 * @creation-date	2015-12-01 
 * @revision        1.0.0.0
 */
class iWatchConfig {

	/* constants */
	const BASE_PATH = "/tmp";
	const CAM_MODEL = "SNH6414";
	const AN_SUCCESS = "/mnt/custom/iwatch/audio/success.wav";
	const AN_FAIL = "/mnt/custom/iwatch/audio/fail.wav";
	const AN_PROCESSING = "/mnt/custom/iwatch/audio/processing.wav";
	const LOGGER = "/tmp/logs/iwl.installer.log";
	const IWL_ROOT_PATH  = '/mnt/custom/iwatch';
	const IWL_LOGGING_PATH  = '/tmp/logs';
	const IWL_CAMERA_DATA_PATH  = '/tmp/camera_data';
	const IWL_ACTIVATION_DATA = '/tmp/iwl.activation.dat';
	const IWL_FW_KEY_PLACEHOLDER = '<REPLACE_WITH_FIRMWARE_KEY>'; // Do not hardcode keys — load from environment or secrets file at runtime
	const IWL_DEFAULT_CREDS = '/tmp/daemon/cfg/lighttpd.user';
	const MAX_FW_RETRIES = 4;

	// Define server end-points for each environment
    public static function getServer( $installType = 0 ){
            $_servers  = array(
	                        array("index"=>0,"sapi"=>"https://api.mysmartcamcloud.com","fw"=>"https://updates.mysmartcamcloud.com/firmware/"), // production
	                        array("index"=>1,"sapi"=>"https://preprodapi.smartcamcloud.ca","fw"=>"https://updates.smartcamcloud.ca/firmware/"), // preprod
	                        array("index"=>2,"sapi"=>"https://testapi.smartcamcloud.ca","fw"=>"https://updates.smartcamcloud.ca/firmware/"),  // test
	                        array("index"=>3,"sapi"=>"https://devapi.smartcamcloud.ca","fw"=>"https://updates.smartcamcloud.ca/firmware/")  // dev
                            );
            // determine if the value is out of range...if so set default
            $installType = (isset($_servers[$installType]))?$installType:0;
            return $_servers[$installType];
    }

}
