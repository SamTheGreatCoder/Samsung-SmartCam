<?php
require_once '/mnt/custom/iwatch/include/php/wirelessManager.php';
require_once '/mnt/custom/iwatch/include/php/config.php';

/**
 * wireless configuration script 
 *
 * Unauthorized use of these files is an infringement of Canadian and
 * International copyright laws.  For full  copyright and license information, please
 * view the LICENSE file that was distributed with this platform.
 *
 * 
 * @package         
 * @creation-date	2015-12-01 
 * @revision        1.0.0.0
 */
// Ensure request method is POST
if ($_SERVER['REQUEST_METHOD'] != 'POST') {
	header('HTTP/1.0 405 Method not supported', true, 405);
	exit;
}

$content  = file_get_contents("php://input");
$data = iWatchUtils::decodeJSON( iWatchUtils::sanitizeJSON( $content ) );

if($data){	


		$credentials = iWatchUtils::loadCredentials();	
		iWatchCamera::playAudioFile(iWatchConfig::CAM_MODEL, $credentials,iWatchConfig::AN_PROCESSING);
		// Set the wireless information assuming the profile was sent in
		// If the profile is not present, ignore and continue with the activation/update

		if (isset($data->wireless)){
			$wirelessConfig = new wirelessManager( $credentials );
			if ($wirelessConfig->run( $data->wireless )){		
				echo '{"result":"OK"}';
				iWatchCamera::playAudioFile(iWatchConfig::CAM_MODEL, $credentials,iWatchConfig::AN_SUCCESS);
			} else {
	            header('HTTP/1.0 400 Bad request', true, 400);
				echo '{"result":"Failed"}';
				iWatchCamera::playAudioFile(iWatchConfig::CAM_MODEL, $credentials,iWatchConfig::AN_FAIL);
			}
		} else {
			echo '{"result":"Failed"}';
			iWatchCamera::playAudioFile(iWatchConfig::CAM_MODEL, $credentials,iWatchConfig::AN_FAIL);
		}

} else {
	header('HTTP/1.0 405 Method not supported', true, 405);
	exit;
}