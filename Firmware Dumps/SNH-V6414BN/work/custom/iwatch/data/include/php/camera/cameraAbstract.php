<?php
/**
 * API Wrapper
 *
 *
 * Unauthorized use of these files is an infringement of Canadian and
 * International copyright laws.  For full  copyright and license information, please
 * view the LICENSE file that was distributed with this platform.
 *
 * SNHCameraAPI class
 * 
 * @package         
 * @creation-date   2014-04-11
 * @revision        1.0.0.0
 */

require_once '/mnt/custom/iwatch/include/php/curl.php';
require_once '/mnt/custom/iwatch/include/php/util.php';

abstract class CameraInterface {

const DEFAULT_USER = "admin";
const DEFAULT_PASS = "";
const CAMERA_IP = "127.0.0.1";

protected  $_user = CameraInterface::DEFAULT_USER;
protected  $_pass = CameraInterface::DEFAULT_PASS;
protected  $_address = CameraInterface::CAMERA_IP;

abstract public function addUser($user);
abstract public function editUser($user);
abstract public function getUser($filter);
abstract public function getSystemDate();
abstract public function getDeviceInformation();
abstract public function getWirelessList();
abstract public function setWirelessState( $enabled );
abstract public function getWirelessState();
abstract public function getNetworkProfile();
abstract public function setWirelessProfile($wirelessInformation);
abstract public function getWirelessProfile();

/**********************************************************************
 * setCredentials
 *
 */
public function setCredentials ( $creds = array() ){
	$this->_user = trim($creds["username"]);
	$this->_pass = trim($creds["password"]);
}


/**********************************************************************
 * getHTTPClient 
 *
 */
protected function getHTTPClient($enableDisgest = true){

	$httpclient = new Curl();
	if ($enableDisgest) $httpclient->setOpt("digest","");
		$httpclient->setOpt("timeout","10");
		$httpclient->setOpt("maxtime","30");
	$httpclient->setBasicAuthentication($this->_user,$this->_pass);
	return $httpclient;
}

}