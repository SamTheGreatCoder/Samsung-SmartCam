<?php
/**
 * iWatch General Script Utils
 *
 * Unauthorized use of these files is an infringement of Canadian and
 * International copyright laws.  For full  copyright and license information, please
 * view the LICENSE file that was distributed with this platform.
 *
 * 
 * @package         
 * @creation-date   2014-04-11
 * @revision        1.0.0.0
 */

require_once '/mnt/custom/iwatch/include/php/config.php';

class iWatchCamera {

const SNH6414 = "SNH6414";
	
/**********************************************************************
 * loadCamera
 *
 */
protected static function loadCamera( $camera, $creds = null ){
		require_once '/mnt/custom/iwatch/include/php/camera/SNH6414.php';
		switch($camera){
			case iWatchCamera::SNH6414:
			 	$cam = new SNH6414Camera();
			 	if ( ($creds) && (is_array($creds)) ) $cam->setCredentials($creds);
			 	return $cam;
				break;
			default:
				return null;
			
		}

}

/**********************************************************************
 * editUser
 *
 */
public static function editUser( $camera, $creds, $user ){
        $cam = self::loadCamera($camera, $creds);
        $result =  ($cam) ? $cam->editUser($user) : false;
		return $result;

}

/**********************************************************************
 * getSystemDate
 *
 */
public static function getSystemDate( $camera, $creds ){
        $cam = self::loadCamera($camera, $creds);
        $result =  ($cam) ? $cam->getSystemDate() : false;
        return $result;

}

/**********************************************************************
 * getWirelessList
 *
 */
public static function getWirelessList( $camera, $creds ){
        $cam = self::loadCamera($camera, $creds);
        $result =  ($cam) ? $cam->getWirelessList() : null;
		return $result;

}

/**********************************************************************
 * getDeviceInformation
 *
 */
public static function getDeviceInformation( $camera, $creds ){
	$cam = self::loadCamera($camera, $creds);
	$result =  ($cam) ? $cam->getDeviceInformation() : null;
	return $result;

}

/**********************************************************************
 * getNetworkProfile
 *
 */
public static function getNetworkProfile( $camera, $creds ){
	$cam = self::loadCamera($camera, $creds);
	$result =  ($cam) ? $cam->getNetworkProfile() : null;
	return $result;

}

/**********************************************************************
 * getWirelessState
 *
 */
public static function getWirelessState( $camera, $creds ){
	$cam = self::loadCamera($camera, $creds);
	$result =  ($cam) ? $cam->getWirelessState() : false;
	return $result;

}

/**********************************************************************
 * setWirelessState
 *
 */
public static function setWirelessState( $camera, $creds, $wirelessState ){
	$cam = self::loadCamera($camera, $creds);
	$result =  ($cam) ? $cam->setWirelessState( $wirelessState ) : null;
	return $result;

}

/**********************************************************************
 * getWirelessProfile
 *
 */
public static function getWirelessProfile( $camera, $creds ){
	$cam = self::loadCamera($camera, $creds);
	$result =  ($cam) ? $cam->getWirelessProfile() : null;
	return $result;

}

/**********************************************************************
 * setWirelessProfile
 *
 */
public static function setWirelessProfile( $camera, $creds, $wirelessInformation ){
	$cam = self::loadCamera($camera, $creds);
	$result =  ($cam) ? $cam->setWirelessProfile( $wirelessInformation ) : null;
	return $result;

}

/**********************************************************************
 * setOutputVolume
 *
 */
public static function setOutputVolume( $camera, $creds, $volume ){
	$cam = self::loadCamera($camera, $creds);
	$result =  ($cam) ? $cam->setOutputVolume( $volume ) : null;
	return $result;

}

/**********************************************************************
 * playAudioFile
 *
 */
public static function playAudioFile( $camera, $creds, $file ){
	$cam = self::loadCamera($camera, $creds);
	$result =  ($cam) ? $cam->playAudioFile( $file ) : null;
	return $result;

}

}