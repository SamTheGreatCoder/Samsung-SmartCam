<?php
require_once '/mnt/custom/iwatch/include/php/installer.php';
require_once '/mnt/custom/iwatch/include/php/wirelessManager.php';
require_once '/mnt/custom/iwatch/include/php/config.php';
require_once '/mnt/custom/iwatch/include/php/iWLCamera.php';

// surpess errors and notices
error_reporting(0);

/**
 * Installation Script 
 *
 * Unauthorized use of these files is an infringement of Canadian and
 * International copyright laws.  For full  copyright and license information, please
 * view the LICENSE file that was distributed with this platform.
 *
 * @package         
 * @creation-date	2015-12-01 
 * @revision        1.0.0.0
 */

define("SET_WIRELESS_RETRY",3);
define("CHECK_WIRELESS_RETRY",9);

// Ensure request method is POST
if ($_SERVER['REQUEST_METHOD'] != 'POST') {
	header('HTTP/1.0 405 Method not supported', true, 405);
	exit;
}

// Verify mode and exit if not correct
if ( (isset($_POST["mode"]))  &&  ( ($_POST["mode"] != iWatchInstaller::IWL_INSTALLER_ACTIVATE) &&  ($_POST["mode"] != iWatchInstaller::IWL_INSTALLER_UPDATE)) ){
	header('HTTP/1.0 400 Bad Request', true, 400);
	exit;
}

$processActivation = true;
$logger = new iWatchLogger();
$logger->logfile = iWatchConfig::LOGGER;
$success = false;

if ( (file_exists(iWatchConfig::IWL_ACTIVATION_DATA)) && (isset($_POST["mode"]))){				
	// Instantiate iWatch Installer and run with data
	$contents = file_get_contents( iWatchConfig::IWL_ACTIVATION_DATA );
	$data = iWatchUtils::decodeJSON( iWatchUtils::sanitizeJSON( $contents ) );

	if($data){	

		// Check for valid activation request
		$credentials = iWatchUtils::loadCredentials();
		if ($_POST["mode"] == iWatchInstaller::IWL_INSTALLER_ACTIVATE){
			// if we don't have a pin exit
			if (isset($data->pin)){	
                   if (file_exists(iWatchConfig::IWL_ROOT_PATH . "/scripts/iwl_stop.sh")) {
                       // kill all the active IWL processes
                       $system_cmd = iWatchConfig::IWL_ROOT_PATH . "/scripts/iwl_stop.sh > /dev/null 2>&1 &" ;
		       		   exec($system_cmd) ;
                   }
                   iWatchCamera::playAudioFile(iWatchConfig::CAM_MODEL, $credentials,iWatchConfig::AN_PROCESSING);                   
            } else {
            	$processActivation = false;	
            	$logger->write("InstallManager - invalid pin");
            }		
		}	

		// validate credentials (if empty it is a new camera and this will be configured during activation)
		if ( ($processActivation) && (isset($data->cam_pass)) && (!empty($data->cam_pass)) && (!empty($credentials["password"]))){
			if (strcmp($credentials["password"], trim($data->cam_pass)) !== 0) {
				echo '{"result":"Failed"}';
				$processActivation = false;
				$logger->write("InstallManager - invalid credentials");
			}
		}

		// Set the wireless information assuming the profile was sent in
		// If the profile is not present, ignore and continue with the activation/update
		if ($processActivation && (isset($data->wireless))){
			$wirelessConfig = new wirelessManager( $credentials );
			$processActivation = $wirelessConfig->run( $data->wireless );
		}

		// iwatch stack activation, update and addition to service
		if ($processActivation){
			$iwlInstaller = new iWatchInstaller( $_POST["mode"], $credentials );
			// run with raw file content (not JSON decoded)
			if ($iwlInstaller->run( $data )) {
				// reload creds in case of a change
				$success = true;	
			} 
		}
		
		// Reload credentials and process results
		$credentials = iWatchUtils::loadCredentials();
		iWatchCamera::setOutputVolume(iWatchConfig::CAM_MODEL, $credentials,9);
		if ($success){
			echo '{"result":"OK"}';
			if ($_POST["mode"] == iWatchInstaller::IWL_INSTALLER_ACTIVATE){
				iWatchCamera::playAudioFile(iWatchConfig::CAM_MODEL, $credentials,iWatchConfig::AN_SUCCESS);
            }
		} else {
			echo '{"result":"Failed"}';			
			if ($_POST["mode"] == iWatchInstaller::IWL_INSTALLER_ACTIVATE){
				iWatchCamera::playAudioFile(iWatchConfig::CAM_MODEL, $credentials,iWatchConfig::AN_FAIL);
                $system_cmd = iWatchConfig::IWL_ROOT_PATH . "/scripts/start.sh > /dev/null 2>&1 &" ;
			    exec($system_cmd) ;
			}

		}
		// clean up activation file
		unlink(iWatchConfig::IWL_ACTIVATION_DATA);
	}
} else {
	header('HTTP/1.0 400 Bad Request', true, 400);
	$logger->write("InstallManager - No install data present");
	if ($_POST["mode"] == iWatchInstaller::IWL_INSTALLER_ACTIVATE){
        $system_cmd = iWatchConfig::IWL_ROOT_PATH . "/scripts/start.sh > /dev/null 2>&1 &" ;
	    exec($system_cmd) ;
	}	
}