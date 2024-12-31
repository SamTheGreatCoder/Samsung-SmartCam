<?php
require_once '/mnt/custom/iwatch/include/php/util.php';
require_once '/mnt/custom/iwatch/include/php/logger.php';
require_once '/mnt/custom/iwatch/include/php/config.php';
require_once '/mnt/custom/iwatch/include/php/iWLServiceAPI.php';
require_once '/mnt/custom/iwatch/include/php/iWLCamera.php';

/**
 * iWatch Installation Script 
 *
 * The contents of this file are considered proprietary information 
 * for the use of iWatchLife employees only.
 *
 * Unauthorized use of these files is an infringement of Canadian and
 * International copyright laws.  For full  copyright and license information, please
 * view the LICENSE file that was distributed with this platform.
 *
 * iWatchInstaller class
 * 
 * @package         
 * @creation-date	2015-12-01 
 * @revision        1.0.0.0
 */
class iWatchInstaller
{
	const IWL_INSTALLER_ACTIVATE="ACTIVATION";
	const IWL_INSTALLER_UPDATE="UPDATE";
	
	private $logger;
	protected $_options = array();
	/**
	 * Enumerates file types
	 * @var array _fileTypes
	 */
	protected $_fileTypes = array( "tgz", "bin" );


	// credentials
	protected $_credentials = array();
	
	protected $_mode;

	protected $_server;

	/**********************************************************************
	 * run - Executes validation and installation routines
	 *
	 * @param string $mode installer mode
	 * @param array $file $_FILES data
	 * @param array $data $_POST data
	 */
    public function __construct( $mode = iWatchInstaller::IWL_INSTALLER_ACTIVATE, $creds = array() )
    {
		$this->_credentials = $creds;
		$this->_mode = $mode;
		$this->logger = new iWatchLogger();
       	$this->logger->logfile = iWatchConfig::LOGGER;
    }

	/**********************************************************************
	 * run - Executes validation and installation routines
	 *
	 * @param string $mode installer mode
	 * @param array $file $_FILES data
	 * @param array $data $_POST data
	 */
	public function run( $data = null )
	{
		// establish source file
		$success = false;
		$this->setOptions( $data );

		//get server end-points
		$this->_server = iWatchConfig::getServer($this->_options["firmware_type"]); 

		// source firmware bundle
		$sourceFile = iWatchConfig::BASE_PATH . "/install".md5(time()).".bin";
		if (file_exists($sourceFile)) unlink ($sourceFile);
		//obtain firmware from server
		$deviceinfo = iWatchCamera::getDeviceInformation( iWatchConfig::CAM_MODEL, $this->_credentials );

		// process runtime data and execute firmware update
		if (($data) && ($deviceinfo)){
			
			// Change the admin password if the camera is in default state
			if (empty($this->_credentials["password"])) $this->updateRootPass($this->_options["cam_pass"]);
		
			// Request the firmware
			$firmware = $this->requestFirmare( $deviceinfo->Model, $deviceinfo->SerialNumber );
			if ( is_array( $firmware ) ){
				// move contents to source install file
				file_put_contents( $sourceFile, $firmware['data'] );
				// validate the integrity of the upload
				if ( $this->validateFirmware($sourceFile, $sourceFile, $firmware['checksum'] )) {
					// Add camera to core (skip this if update)
					if ($this->activateCamera()){
						// deploy stack
						$success = $this->installFirmware( $sourceFile );	
					} else {
						unlink( $sourceFile );
					}
				} 
			}
		}
		return $success;
	}

	/**********************************************************************
	 * setOptions
	 *
	 */
	private function setOptions( $options ){
		if ($options){
			$this->_options["cam_pass"] = (isset($options->cam_pass) && (!empty($options->cam_pass))) ? trim($options->cam_pass) : $this->_credentials["password"];
			$this->_options["pin"] = isset($options->pin) ? trim($options->pin) : "";
			$this->_options["tz"] = isset($options->tz) ? trim($options->tz) : "";
			$this->_options["name"] = isset($options->name) ? trim($options->name) : "";
			$this->_options["firmware_type"] = isset($options->firmware_type) ? $options->firmware_type : 0; 
		}
	}
	
	/**********************************************************************
	 * updateRootPass
	 *
	 */
	private function updateRootPass( $rootpass ){
		$this->logger->write("Installer - Updating root user");
		if (empty($rootpass)) {
			$rootpass = strtoupper("SC".substr( md5(rand()), 0, 4)."PS");
			$this->_options["cam_pass"] = $rootpass;
		}
		if (iWatchCamera::editUser(iWatchConfig::CAM_MODEL, $this->_credentials,array("index"=>"0","username"=>'admin',"password"=>$rootpass))){	
			// persist the root user/pass to iwl conf
			file_put_contents(iWatchConfig::IWL_ROOT_PATH."/conf/admin.user", 'admin:'.$rootpass);
			$this->_credentials = iWatchUtils::loadCredentials();

			return true;
		} else {
			return false;
		}

	}

	/**********************************************************************
	 * validateFirmware - Validate File
	 *
	 * @param string $fileContents
	 * @param string $fileName
	 * @param string $checksum
	 */
	private function validateFirmware( $fileContents, $fileName, $checksum )
	{
		//extract extension	
		$ext_array = explode(".", $fileName);
		$extension = end($ext_array);
		// verify file type and checksum
		if ( in_array($extension, $this->_fileTypes) && $this->verifyChecksum($fileContents,$checksum) ){
			return true;
		} 
		return false;		
	}

	/**********************************************************************
	 * installFirmware - Unpack and install the firmware
	 *
	 * @param string $file
	 */
	private function installFirmware( $file ){

		$success = false;	
		$this->logger->write("Installer - Installing Firmware");
		if ( file_exists($file) ){				
			exec( iWatchConfig::IWL_ROOT_PATH . "/scripts/install.sh " . escapeshellarg($file) . " >> /tmp/logs/iwl.firmware.log &");
			$success = true;		  
		}
		return $success;
	}

	/**********************************************************************
	 * verifyChecksum - Unpack and install the firmware
	 *
	 * @param string $file - source file
	 * @param string $checksum - source file checksum from server
	 */
	private function activateCamera( ){	

		$success = true;

		 // add to core if this is an activation
		 if ($this->_mode == iWatchInstaller::IWL_INSTALLER_ACTIVATE){
		 	$this->logger->write("Installer - Adding Camera to Core");
		 	$deviceinfo = iWatchCamera::getDeviceInformation( iWatchConfig::CAM_MODEL, $this->_credentials );
		 	// if device info doesn't return exit installer
		 	if (!$deviceinfo) return false;
		 	$deviceName = (!empty($this->_options["name"])) ? $this->_options["name"] : $deviceinfo->SerialNumber;
                        $dateinfo = iWatchCamera::getSystemDate( iWatchConfig::CAM_MODEL, $this->_credentials );
                        $tz = ((isset($dateinfo)) && (isset($dateinfo->timezone))) ? $dateinfo->timezone : "";
                        $timezone = iWatchUtils::getTimeZone($tz);
			 // Prepare the camera structure
			 if (!IWLServiceAPI::addCamera($this->_server["sapi"], $this->_options["pin"], array(
									"username"=> "admin",
									"password"=>  $this->_options["cam_pass"],
									"timezone"=> $timezone,
									"name"=>$deviceName,
									"serial"=> $deviceinfo->SerialNumber,
									"manufacturer"=> $deviceinfo->Model
									))) {
										$success = false;																								
										$this->logger->write("Installer - Failed to add to core");
			} 
		 } 
					
		return $success;
	}

	/**********************************************************************
	 * verifyChecksum - Unpack and install the firmware
	 *
	 * @param string $file - source file
	 * @param string $checksum - source file checksum from server
	 */
	private function verifyChecksum($file, $checksum){	
		return (trim(iWatchUtils::md5_check($file)) == trim($checksum));
	}


	/**********************************************************************
	 * requestFirmare - Request firmware from remote service
	 *
	 * @param string $xauth_token - core firmware authtoken
	 * @param string $camera_model - defaults to samsung SNH101x 
	 */
	private function requestFirmare( $camera_model = 'SNH6414', $serial = '00000000000' ){
		$retries = 1;

		//temp buffer for firmware request
		$tmp_buffer = iWatchConfig::BASE_PATH . "/iwl".md5(time()).".tmp";
		
		// verify server URL
		$url = parse_url( $this->_server["fw"] );
		$pingresult = iWatchUtils::ping($url['host'],80,30);
		if (!$pingresult['result']){
			$this->logger->write("Installer - Failed to ping server [". $pingresult['errdesc'] . " - ". $pingresult['errcode'] ."] - setting retries");
			$retries = iWatchConfig::MAX_FW_RETRIES;
		}

		$success = false;		

		// build request query string		
		$installType = http_build_query( array( 'type' => $this->_server["index"] ) );
		$token = iWatchUtils::get_token(iWatchConfig::IWL_FW_KEY, $serial);
		$reqStr = "/usr/bin/curl '" . $this->_server["fw"] . "/index.php?" .$installType. "' -k -s -H 'X-Auth-Token:".$token. "'  -H 'X-Camera-Serial:".$serial."' -H 'X-Camera-Model:".$camera_model."' -o " . $tmp_buffer;
		$this->logger->write("Installer -  downloading firmware: " . $reqStr);

		for ($i = 0; $i < $retries; $i++){
			// request firmware
			passthru( $reqStr , $result );
			
			// if passthru returns anything other than 0, the action was a failure and we should exit
			if ($result == 0){
				$success = true;
				break;	
			} else {
				$this->logger->write("Installer - Failed to obtain firmware - retrying");
				unlink( $tmp_buffer );
				sleep(5);
			}
		}

		// check to see if we were successful obtaining firmware
		if (!$success) return false;

		// basic parsing of the buffer contents
		$fh = @fopen($tmp_buffer, "r");
		if ($fh) {

			// read the first line from buffer. This will always be the checksum
			$result = array( "checksum" => "", "data" => "" );
			$checksum = fgets($fh, 1024); 
			$result['checksum'] = trim(substr($checksum, strlen("X-File-Checksum:") )); // extract checksum from buffer
			// copy firmware contents into memory
			while(!feof($fh)) {
				// reset to prevent timeouts	
				set_time_limit(0);			
				# read data into file buffer
				$result['data'] .= fread($fh, 1024);			
				@flush();
			}			
			
			fclose($fh);			
			unlink( $tmp_buffer );	
			
			return $result;
		}
		return false;
	} 
}