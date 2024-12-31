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
	const IWL_FW_KEY = 'b19fa6ecd52f0439dfdb7a123de6e04e'; 
	const IWL_DEFAULT_CREDS = '/tmp/daemon/cfg/lighttpd.user';
	const MAX_FW_RETRIES = 4;

	// Define server end-points for each environment
    public static function getServer( $installType = 0 ){
            $_servers  = array(
	                        array("index"=>0,"sapi"=>"https://api.mysmartcamcloud.com","fw"=>"https://updates.mysmartcamcloud.com/firmware/"), // production
	                        array("index"=>1,"sapi"=>"http://preprodapi.smartcamcloud.ca","fw"=>"http://updates.smartcamcloud.ca/firmware/"), // preprod
	                        array("index"=>2,"sapi"=>"http://testapi.smartcamcloud.ca","fw"=>"http://updates.smartcamcloud.ca/firmware/"),  // test
	                        array("index"=>3,"sapi"=>"http://devapi.smartcamcloud.ca","fw"=>"http://updates.smartcamcloud.ca/firmware/")  // dev
                            );
            // determine if the value is out of range...if so set default
            $installType = (isset($_servers[$installType]))?$installType:0;
            return $_servers[$installType];
    }

}