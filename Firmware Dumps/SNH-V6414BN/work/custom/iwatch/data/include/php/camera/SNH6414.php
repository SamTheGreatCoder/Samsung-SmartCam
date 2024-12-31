<?php
/**
 * API Wrapper
 *
 * Unauthorized use of these files is an infringement of Canadian and
 * International copyright laws.  For full  copyright and license information, please
 * view the LICENSE file that was distributed with this platform.
 *
 * SNH6414Camera class
 * 
 * @package         
 * @creation-date   2015-12-04
 * @revision        1.0.0.0
 */

require_once '/mnt/custom/iwatch/include/php/camera/cameraAbstract.php';

class SNH6414Camera extends CameraInterface {

/**********************************************************************
 * Add User
 *
 */
public function addUser($user){
	return false;
}	

/**********************************************************************
 * Edit_User
 *
 */
public function editUser( $user){
	$result = false;
	$httpclient = $this->getHTTPClient();
	$user = iWatchUtils::encodeJSON( array("Index"=>$user["index"],"UserID"=>$user["username"],"Password"=>$user["password"]));
	$http_ret = $httpclient->putRaw('http://'.$this->_address.'/stw-cgi-rest/security/users',$user);
	if ($http_ret){
		if ($httpclient->getStatusCode() == "200"){
			$result = true;
		}
	}
	return $result;
}

/**********************************************************************
 * Get User
 *
 */
public function getUser( $filter ){
	$result = null;
	$httpclient = $this->getHTTPClient();
	$http_ret = $httpclient->get('http://'.$this->_address.'/stw-cgi-rest/security/users');
	if ($http_ret){
			$index=0;
			$userList = iWatchUtils::decodeJSON( $httpclient->getResponse() );
			if ($userList){
				
				$user = new stdClass();
				$user->index = 0;
				$user->id = $userList->{"Users.$index.UserID"};
				$user->password = $userList->{"Users.$index.Password"};
				$user->enabled = $userList->{"Users.$index.Enable"};
				$user->VideoProfileAccess = $userList->{"Users.$index.VideoProfileAccess"};
				$user->AudioInAccess = $userList->{"Users.$index.AudioInAccess"};
				$user->AudioOutAccess = $userList->{"Users.$index.AudioOutAccess"};
				$result =  $user;
			}
			
	}

	return $result;
}

/**********************************************************************
 * getSystemDate
 *
 */
public function getSystemDate(){
	$result = null;
	$httpclient = $this->getHTTPClient();
	$http_ret = $httpclient->get('http://'.$this->_address.'/stw-cgi-rest/system/date');
	if ($http_ret){
		$date = iWatchUtils::decodeJSON( $httpclient->getResponse() );		
		if ($date){
		    // Get string representation of timezone
			$tz_ret = $httpclient->get('http://'.$this->_address.'/stw-cgi-rest/system/date/timezonelist');
			if ($tz_ret){
				$tz = iWatchUtils::decodeJSON( $httpclient->getResponse() );
				if ($tz){
				  $date->timezonelist = $tz->TimeZoneList;	
				  $date->timezone = $tz->TimeZoneList[$date->TimeZoneIndex];
				}		
			}
			$result = $date;
		} 
	}
	return $result;
}

/**********************************************************************
 * getDeviceInformation - Obtain the model and serial
 *
 */
public function getDeviceInformation(){

	//default to a generic camera
	$result = null;
	$httpclient = $this->getHTTPClient();
	$http_ret = $httpclient->get('http://'.$this->_address.'/stw-cgi-rest/system/deviceinfo');
	if ($http_ret){
		$device = iWatchUtils::decodeJSON( $httpclient->getResponse() );
		if ($device){
			$result = $device;
		}

	}
	return $result;
}

/**********************************************************************
 * getWirelessList
 *
 */
public function getWirelessList(){
	$result = null;
	$httpclient = $this->getHTTPClient();
	$http_ret = $httpclient->get('http://'.$this->_address.'/stw-cgi-rest/network/wifi/scan');
	if ($http_ret){
		$wirelessList = iWatchUtils::decodeJSON($httpclient->getResponse());
		$index=0;
		$result = array();
		foreach ($wirelessList as $network){
			$index++;
			$availableNetwork = new stdClass();
			$availableNetwork->ssid = $network->{"AvailableNetworks.$index.SSID"};
			$availableNetwork->mode = $network->{"AvailableNetworks.$index.SecurityMode"};
			$availableNetwork->strength = $network->{"AvailableNetworks.$index.SignalStrength"};
			$result[] =  $availableNetwork;
		}		 
	}

	return $result;
}

/**********************************************************************
 * setWirelessStatus
 *
 */
public function setWirelessState( $enabled ){

	$result = false;
	$httpclient = $this->getHTTPClient();
	$wirelessState = iWatchUtils::encodeJSON( array("Enable"=>$enabled));
	$http_ret = $httpclient->putRaw('http://'.$this->_address.'/stw-cgi-rest/network/wifi',$wirelessState);
	if ($http_ret){
		if ($httpclient->getStatusCode() == "200"){
			$result = true;
		}
	}
	return $result;
}

/**********************************************************************
 * getWirelessStatus
 *
 */
public function getWirelessState(){

	$result = false;
	$httpclient = $this->getHTTPClient();
	$http_ret = $httpclient->get('http://'.$this->_address.'/stw-cgi-rest/network/wifi');
	if ($http_ret){
		$profile = iWatchUtils::decodeJSON( $httpclient->getResponse() );
		if ($profile){
			$result = $profile->Enable;
		} 
	}
	return $result;
}

/**********************************************************************
 * getNetworkProfiles
 *
 */
public function getNetworkProfile(){

	$result = null;
	$httpclient = $this->getHTTPClient();
	$http_ret = $httpclient->get('http://'.$this->_address.'/stw-cgi-rest/network/interface');
	if ($http_ret){
		$network = iWatchUtils::decodeJSON( $httpclient->getResponse() );
		if ($network){
			$result = $network;
		} 
	}
	return $result;
}

/**********************************************************************
 * setWirelessProfile 
 *
 */
public function setWirelessProfile( $wirelessInformation ){

	$result = false;
	$httpclient = $this->getHTTPClient();
	$wirelessProfile = iWatchUtils::encodeJSON( array("SSID"=>$wirelessInformation["ssid"],"Password"=>$wirelessInformation["passphrase"],"SecurityMode"=>$wirelessInformation["mode"]));
	$http_ret = $httpclient->putRaw('http://'.$this->_address.'/stw-cgi-rest/network/wifi/connect',$wirelessProfile);
	if ($http_ret){
		if ($httpclient->getStatusCode() == "200"){
			$result = true;
		}
	}
	return $result;

}


/**********************************************************************
 * getWirelessProfile
 *
 */
public function getWirelessProfile( ){
	$result = null;
	$httpclient = $this->getHTTPClient();
	$http_ret = $httpclient->get('http://'.$this->_address.'/stw-cgi-rest/network/wifi');
	if ($http_ret){
		$profile = iWatchUtils::decodeJSON( $httpclient->getResponse() );
		if ($profile){
			$result = $profile;
		} 
	}

	return $result;
}

/**********************************************************************
 * setOutputVolume
 *
 */
public function setOutputVolume( $volume ){
	$result = false;
	$httpclient = $this->getHTTPClient();
	$outputVolume = iWatchUtils::encodeJSON( array("Channel"=>0,"Gain"=>$volume) );
	$http_ret = $httpclient->putRaw('http://'.$this->_address.'/stw-cgi-rest/media/audiooutput',$outputVolume);
	if ($http_ret){
		if ($httpclient->getStatusCode() == "200"){
			$result = true;
		}
	}
	return $result;
}

/**********************************************************************
 * playAudioFile
 *
 */
public function playAudioFile( $audioFile ){
	$result = false;
	if (file_exists($audioFile)) {
		exec( "/usr/bin/aplay ". escapeshellarg($audioFile) . " &");
	}

	return $result;
}

}