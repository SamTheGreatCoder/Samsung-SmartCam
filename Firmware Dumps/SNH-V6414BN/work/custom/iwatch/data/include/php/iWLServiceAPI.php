<?php
/**
 * Service Wrapper
 *
 * The contents of this file are considered proprietary information 
 * for the use of iWatchLife employees only.
 *
 * Unauthorized use of these files is an infringement of Canadian and
 * International copyright laws.  For full  copyright and license information, please
 * view the LICENSE file that was distributed with this platform.
 *
 * IWLServiceAPI class
 * 
 * @package         
 * @creation-date   2015-12-05
 * @revision        1.0.0.0
 */

require_once '/mnt/custom/iwatch/include/php/curl.php';
require_once '/mnt/custom/iwatch/include/php/util.php';
require_once '/mnt/custom/iwatch/include/php/config.php';

class IWLServiceAPI {

/**********************************************************************
 * Add_User
 *
 */
public static function addCamera( $server, $pin, $camera = array() ){
	
	$httpclient = new Curl();
	$result = false;
	// Create JSON request
	$addCamRequest = array(
			'pin' => $pin,
			'camera' => $camera
			);	
	
	$httpclient->setHeader("Content-Type: application/json");
	$httpclient->postRaw($server . "/sapi/account/pin", iWatchUtils::encodeJSON($addCamRequest));
	
	$response = iWatchUtils::decodeJSON( $httpclient->getResponse() );
	if (($httpclient->getStatusCode() == "200") && ($response)){
			$result = true;
	} 
	return $result;
}

}