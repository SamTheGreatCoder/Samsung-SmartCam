<?php
/**
 * iWatch General Script Utils
 *
 * Unauthorized use of these files is an infringement of Canadian and
 * International copyright laws.  For full  copyright and license information, please
 * view the LICENSE file that was distributed with this platform.
 *
 * iWatchUtils class
 * 
 * @package         
 * @creation-date   2014-04-11
 * @revision        1.0.0.0
 */
class iWatchUtils {

/**********************************************************************
 * jsonDecode
 *
 */
public static function decodeJSON( $data ){
		require_once '/mnt/custom/iwatch/include/php/JSON.php';
		$json = new Services_JSON();
        return $json->decode($data);
}

/**********************************************************************
 * jsonEncode
 *
 */
public static function encodeJSON( $data ){
		require_once '/mnt/custom/iwatch/include/php/JSON.php';
		$json = new Services_JSON();
        return $json->encode($data);

}


/**********************************************************************
 * sanitizeJSON
 *
 */
public static function sanitizeJSON( $data, $maxLength = 256){
  $dataOut = new stdClass();
  if (strlen($data) <= $maxLength) {
    $dataIn  = iWatchUtils::decodeJSON($data);
    // only persist valid fields
    if ($dataIn){
      if ( (isset($dataIn->cam_pass)) && (strlen($dataIn->cam_pass) <= 15 )) $dataOut->cam_pass = $dataIn->cam_pass;
      if ( (isset($dataIn->pin)) && (preg_match("/^[a-zA-Z0-9]+$/", $dataIn->pin))) $dataOut->pin = $dataIn->pin;
      if ( (isset($dataIn->name)) && (preg_match("/^[a-zA-Z0-9]+$/", $dataIn->name))) $dataOut->name = $dataIn->name;
      if ( (isset($dataIn->tz)) && (preg_match("/^[a-zA-Z0-9]+$/", $dataIn->tz))) $dataOut->tz = $dataIn->tz;
      if ( (isset($dataIn->firmware_type)) && (preg_match("/^[0-9]{1}$/", $dataIn->firmware_type))) $dataOut->firmware_type = $dataIn->firmware_type;
      if (isset($dataIn->wireless)){
        $dataOut->wireless = new stdClass();
        if ( (isset($dataIn->wireless->ssid)) && (strlen($dataIn->wireless->ssid) <= 32 )) $dataOut->wireless->ssid = $dataIn->wireless->ssid;
        if ( (isset($dataIn->wireless->passphrase)) && (strlen($dataIn->wireless->passphrase) <= 64 )) $dataOut->wireless->passphrase = $dataIn->wireless->passphrase;        
      }    
    }  
  }  
  return iWatchUtils::encodeJSON($dataOut);

}

/**********************************************************************
 * md5_check
 *
 */
public static function md5_check( $source_file ){
        ob_start();
        system("/usr/bin/md5sum ". escapeshellarg($source_file)." | cut -d' ' -f1",$ret);
        $data = ob_get_contents();
        ob_end_clean();
		return $data;

}

/**********************************************************************
 * get_token
 *
 */
public static function get_token( $fw_token, $serial ){
    ob_start();
    system("/mnt/custom/iwatch/bin/get_token ". escapeshellarg($serial)." ".escapeshellarg($fw_token));
    $data = ob_get_contents();
    ob_end_clean();
    return $data;

}

/**********************************************************************
 * ping
 *
 */
public static function ping($host,$port=80,$timeout=10)
{
		$result = array('result'=>true,'errdesc'=>'','errcode'=>0);
		if ($port == 0){
			$pingresult = exec("/bin/ping -c1 -w". escapeshellarg($timeout). " " . escapeshellarg($host), $output, $status);  
   			if ($status!=0) {
	        	$result['result'] = false;
	        	$result['errdesc'] = "Unable to ping host";
	        	$result['errcode'] = "E_INTERFACE_DOWN";
   			}			
		} else {
	        $fsock = @fsockopen($host, $port, $errno, $errstr, $timeout);
	        if ( ! $fsock )
	        {
	        	$result['result'] = false;
	        	$result['errdesc'] = $errstr;
	        	$result['errcode'] = $errno;	
	            
	        }
    	}
        return $result;
}

/**********************************************************************
 * loadCredentials
 *
 */
public static function loadCredentials( $path ){

	// grab alternate creds from file
	$credentials = array();
	$credentials["username"] = "admin";
	$credentials["password"] = "";
	
	if (empty($path)) $path = iWatchConfig::IWL_DEFAULT_CREDS;
	
	if (file_exists( $path )){	
		$creds = explode(":",file_get_contents($path));
		$credentials["username"] = trim($creds[0]);
		$credentials["password"] = trim($creds[1]);
	} 

	return $credentials;
}

/**********************************************************************
 * getTimeZone
 *
 */
public static function getTimeZone( $camera_timezone ){
$result = "America/New_York";

$timezones =  array(
  "GMT-12:00" => array ("Default"=>"Etc/GMT+12"),
  "GMT-11:00" => array ("Default"=>"Etc/GMT+11","Coordinated Universal Time-11"=>"Pacific/Midway"),
  "GMT-10:00" => array ("Default"=>"Etc/GMT+10","Hawaii"=>"America/Adak"),
  "GMT-09:00" => array ("Default"=>"Etc/GMT+9","Alaska"=>"America/Anchorage"),
  "GMT-08:00" => array ("Default"=>"Etc/GMT+8","Baja California"=>"America/Ensenada","Pacific Time"=>"America/Los_Angeles"),
  "GMT-07:00" => array ("Default"=>"Etc/GMT+7","Chihuahua, La Paz, Mazatlan"=>"America/Chihuahua","Mountain Time"=>"America/Denver","Arizona"=>"America/Dawson_Creek"),
  "GMT-06:00" => array ("Default"=>"Etc/GMT+6","Central Time"=>"America/Chicago","Saskatchewan"=>"America/Belize","Guadalajara, Mexico City, Monterrey"=>"America/Cancun","Central America"=>"America/Belize"),
  "GMT-05:00" => array ("Default"=>"America/New_York","Eastern Time"=>"America/New_York","Bogota, Lima, Quito"=>"America/Bogota"),
  "GMT-04:30" => array ("Default"=>"America/Caracas"),
  "GMT-04:00" => array ("Default"=>"America/Glace_Bay","Cuiaba"=>"America/Cuiaba","Santiago"=>"America/Santiago","Asuncion"=>"America/Asuncion"),
  "GMT-03:30" => array ("Default"=>"America/St_Johns"),
  "GMT-03:00" => array ("Default"=>"America/Araguaina","Buenos Aires"=>"America/Argentina/Buenos_Aires","Brasilia"=>"America/Sao_Paulo","Montevideo"=>"America/Montevideo","Greenland"=>"America/Godthab"),
  "GMT-02:00" => array ("Default"=>"America/Noronha"),
  "GMT-01:00" => array ("Default"=>"America/Azores","Cape Verde Is."=>"Atlantic/Cape_Verde"),
  "GMT" => array ("Default"=>"Europe/London","Monrovia, Reykjavik"=>"Africa/Abidjan"),
  "GMT+01:00" => array ("Default"=>"Europe/Belgrade","Amsterdam, Berlin, Bern, Rome, Stockholm, Vienna"=>"Europe/Amsterdam","Brussels, Copenhagen, Madrid, Paris"=>"Europe/Brussels","West Central Africa"=>"Africa/Algiers","Windhoek"=>"Africa/Windhoek"),
  "GMT+02:00" => array ("Default"=>"Europe/Minsk","Cairo"=>"Africa/Cairo","Jerusalem"=>"Asia/Jerusalem","Beirut"=>"Asia/Beirut","Damascus"=>"Asia/Damascus","Istanbul"=>"Asia/Gaza"),
  "GMT+03:00" => array ("Default"=>"Europe/Moscow","Nairobi"=>"Africa/Addis_Ababa"),
  "GMT+03:30" => array ("Default"=>"Asia/Tehran"),
  "GMT+04:00" => array ("Default"=>"Asia/Dubai","Yerevan"=>"Asia/Yerevan","Moscow, St. Petersburg, Volgograd"=>"Europe/Moscow"),
  "GMT+04:30" => array ("Default"=>"Asia/Kabul"),
  "GMT+05:00" => array ("Default"=>"Asia/Yekaterinburg","Tashkent"=>"Asia/Tashkent"),
  "GMT+05:30" => array ("Default"=>"Asia/Kolkata"),
  "GMT+05:45" => array ("Default"=>"Asia/Kathmandu"),
  "GMT+06:00" => array ("Default"=>"Asia/Dhaka"),
  "GMT+06:30" => array ("Default"=>"Asia/Rangoon"),
  "GMT+07:00" => array ("Default"=>"Asia/Bangkok","Novosibirsk"=>"Asia/Novosibirsk"),
  "GMT+08:00" => array ("Default"=>"Asia/Hong_Kong","Ulaanbaatar"=>"Asia/Irkutsk","Perth"=>"Australia/Perth"),
  "GMT+09:00" => array ("Default"=>"Asia/Yakutsk","Irkutsk"=>"Asia/Irkutsk","Seoul"=>"Asia/Seoul"),
  "GMT+09:30" => array ("Default"=>"Australia/Adelaide","Darwin"=>"Australia/Darwin"),
  "GMT+10:00" => array ("Default"=>"Asia/Vladivostok","Brisbane"=>"Australia/Brisbane","Hobart"=>"Australia/Hobart"),
  "GMT+11:00" => array ("Default"=>"Asia/Magadan","Solomon Is., New Caledonia"=>"Etc/GMT-11"),
  "GMT+12:00" => array ("Default"=>"Etc/GMT-12","Auckland, Wellington"=>"Pacific/Auckland"),
  "GMT+13:00" => array ("Default"=>"Pacific/Tongatapu")
);

    $timezone = trim(substr($camera_timezone, strpos($camera_timezone, ':') + 1));
    if (preg_match_all('#\((([^()]+|(?R))*)\)#', $timezone, $zone)) {
             $tz = trim(preg_replace('#\s*\(.+\)\s*#U', ' ', $timezone));
             $tz_offset = $zone[1][0];
             if (isset($timezones[$tz_offset])){
               $result = isset( $timezones[$tz_offset][$tz] ) ? $timezones[$tz_offset][$tz] : $timezones[$tz_offset]["Default"];
             }
    }

    return $result;
}


}