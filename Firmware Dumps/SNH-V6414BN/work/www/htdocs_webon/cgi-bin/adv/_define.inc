<?php
set_time_limit(60);
require_once('modelinfo.cgi');
define('CMD_NTP_SETTING',						6);
define('CMD_DDNS_SETTING',						7);
define('CMD_INTERFACE_SETTING',				8);
define('CMD_PROTOCOL_SETTING',				9);
define('CMD_ZERO_CONFIGURATION',				11);
define('CMD_IPADDRESS_FILTER',				12);
define('CMD_SMTP_SETTING',						13);
define('CMD_FTP_SETTING',						14);
define('CMD_NETWORK_CONFIGURATION',			15);
define('CMD_NETWORK_TEST',						16);
define('CMD_DATETIME',							18);
define('CMD_TIMEZONE_INFORMATION',			19);
define('CMD_FACTORY_DEFAULT',					20);
define('CMD_REBOOT',								21);
define('CMD_SYSTEM_CONFIGURATION',			24);
define('CMD_USER',								25);
define('CMD_CERTIFICATE',						26);
define('CMD_CERTIFICATE_STATE',				27);
define('CMD_SECURITY_CONFIGURATION',		29);
define('CMD_RELAY_OUTPUT_CONFIGURATION',	30);
define('CMD_RELAY_OUTPUT_STATE',				31);
define('CMD_SENSOR_CONFIGURATION',			32);
define('CMD_SENSOR_STATE',						33);
define('CMD_IO_CONFIGURATION',				34);
define('CMD_IMAGING',							35);
define('CMD_PROFILE',							36);
define('CMD_PROFILE_CONFIGURATION',			37);
define('CMD_MEDIA_CONFIGURATION',			38);
define('CMD_IV_CONFIGURATION',				43);
define('CMD_STORAGE_INFORMATION',			45);
define('CMD_RECORD_CONFIGURATION',			46);
define('CMD_RECORD_SEARCH',					47);
define('CMD_PLAYBACK',							48);
define('CMD_RECORD_BACKUP',					49);
define('CMD_STORAGE_FORMAT',					50);
define('CMD_OSD_CONTROL',						51);
define('CMD_LOG_BACKUP',						52);
define('CMD_CONFIGURATION_BACKUP',			53);
define('CMD_CONFIGURATION_RESTORE',			54);
define('CMD_MEDIA_DATA',						58);
define('CMD_RECORD_SEARCH_DETAIL',			59);
define('CMD_TIMER_CONFIGURATION',			60);
define('CMD_LOG_SEARCH',						61);
define('CMD_LOG_SEARCH_DETAIL',				62);
define('CMD_HTTPS_DATA',						63);
define('CMD_SYS_REGINFO',						66);
define('CMD_SYS_REGDATA',						67);
define('CMD_SNAPSHOT_URI',						76);
define('CMD_MULTICAST_STREAMING',			77);
define('CMD_FACTORY',							78);
define('CMD_EVENT_DATA',						79);
define('CMD_IMAGE_CONFIGURATION',			80);
define('CMD_SERIAL',								81);
define('CMD_OSD_TIME',							82);
define('CMD_VIDEO_SOURCE_SELECTION',		84);
define('CMD_SMARTCODEC',						85);
define('CMD_802_1X_CONFIGURATION',			86);
define('CMD_802_1X_DATA',						87);
define('CMD_MD_CONFIGURATION',				88);
define('CMD_VA_CONFIGURATION',				89);
define('CMD_NETWORK_EVENT',					91);
define('CMD_QOS_CONFIGURATION',				92);
define('CMD_SNMP_CONFIGURATION',				93);
define('CMD_CONTINUOUS_RECORDING',			94);
define('CMD_FD_CONFIGURATION',				95);
define('CMD_TAMPERING_CONFIGURATION',		97);
define('CMD_NAS_CONFIGURATION',				98);
define('CMD_EVENT_CONFIGURATION',			99);
define('CMD_VIDEO_SOURCE_3120',				101);
define('CMD_PRIVACY_MASK',						103);
define('CMD_PRIVACY_AREA',						104);
define('CMD_VIDEO_ANALYSIS',					105);
define('CMD_VAMASK_AREA',						106);
define('CMD_PTZ_HOMEPOSITION',				107);
define('CMD_PTZ_PRESET',						108);
define('CMD_PTZ_PRESET_ATTR_POSITION',		109);
define('CMD_PTZ_PRESET_ATTR_ZOOMFOCUS',	110);
define('CMD_PTZ_PRESET_ATTR_WHITEBAL',		111);
define('CMD_PTZ_PRESET_ATTR_EXPOSURE',		112);
define('CMD_PTZ_PRESET_ATTR_BLC',			113);
define('CMD_PTZ_PRESET_ATTR_DAYNIGHT',		114);
define('CMD_PTZ_PRESET_ATTR_AGC',			115);
define('CMD_PTZ_PRESET_ATTR_OTHER',			116);
define('CMD_PTZ_PRESET_ATTR_INTELLIGENCE',117);
define('CMD_PTZ_LIMIT',							118);
define('CMD_PTZ_SWING',							119);
define('CMD_PTZ_GROUP',							120);
define('CMD_PTZ_TOUR',							121);
define('CMD_PTZ_TRACE',							122);
define('CMD_PTZ_AUTORUN',						123);
define('CMD_PTZ_STATUS',						124);
define('CMD_PTZ_ABSMOVE',						125);
define('CMD_PTZ_STOP',							126);
define('CMD_PTZ_AUXILIARY',					129);
define('CMD_PTZ_RELMOVE',						136);
define('CMD_PTZ_CONTMOVE',						137);
define('CMD_PTZ_PRESET_ATTR',					138);
define('CMD_PTZ_INSTANT_AF',					139);
define('CMD_MOTORIZED_LENS_SETUP',			140);
define('CMD_APPEAR_DISAPPEAR_CONFIGURATION',	141);
define('CMD_TRACKING_PRESET',					142);
define('CMD_TRACKING_TARGETLOCK',			143);
define('CMD_TRACKING_TRACEZONE',				144);
define('CMD_TRACKING_STOP',					145);
define('CMD_TRACKING_EVENT_CONFIGURATION', 146);
define('CMD_TRACKING_TRACEZONE_PROPER',   147);
define('CMD_PTZ_PRESET_VA',			   	148);
define('CMD_AD_CONFIGURATION',				149);
define('CMD_AD_DATA',							150);
define('CMD_AUDIO_OUTPUT_CONFIGURATION',	151);
define('CMD_TIME_SEARCH',						152);
define('CMD_TIME_SEARCH_DETAIL',				153);
define('CMD_STREAMMING_DISCONNECTION',		154);
define('CMD_NETWORK_PORT_CONFIG',			198);
define('CMD_QUICK_CONNECT_SETTING',			199);
define('CMD_SIMPLE_PROFILE',					200);
define('CMD_ATC_INFORMATION',					201);
define('CMD_PROFILE_ACCESS_INFORMATION',	202);
define('CMD_ONVIF_CONFIGURATION',			203);
define('CMD_MANUAL_RECORDING',				204);
define('CMD_ISCSI_DISCOVERY',					298);
define('CMD_ISCSI_CONFIGURATION',			299);
define('CMD_BONJOUR',							300);
define('CMD_UPNP_DISCOVERY',					301);
define('CMD_SNMP_TRAP_CONFIGURATION',		303);
define('CMD_CHINESE_OSD',						327);
define('CMD_PTZ_PRESETEDIT',					328);
define('CMD_RESOLUTION_INFO',					330);
define('CMD_PTZ_AZIMUTHPOSITION',			331);
define('CMD_PTZ_SIMPLE_PRESET',				332);
define('CMD_NETWORK_CONFIGURATION_V2',		1008);
define('CMD_NETWORK_IF_EXTENSION',			1009);
define('CMD_DOT11_STATUS',						1014);
define('CMD_INFORMATION',						8888);
define('CMD_MONITORING_INFO',					9000);
define('CMD_ONVIF_INFO',						9999);
//OPENSDK COMMANDS
define('CMD_OPENSDK_APP',						13000);
define('CMD_OPENSDK_APP_DEBUG',	        		13002);
define('CMD_SDK_SEARCH_DETAIL',				14000);
define('CMD_SDK_APP_ATTRIBUTES',				15000);
define('CMD_SDK_TASK_MANAGER',				15001);
//OPENSDK 3RD PARTY COMMANDS
define('CMD_SDK_APP_DATA',			        	16000);
define('CMD_SDK_MARKET',			        	16001);
define('CMD_RUN_CONFORMANCE',					16006);
define('CMD_OPENSDK_APP_EVENT',			        	13006);

if($GLOBALS['M_SPECIAL_TYPE'] == 1) {
// DEV_S1LOGIN
define('CMD_USER_LOGIN',				10004);
// DEV_S1SMS
define('CMD_SMS_SETTING', 				10006);
}

define('ACTION_GET', 			0);
define('ACTION_GET_ALL', 		1);
define('ACTION_SET', 			4);
define('ACTION_ADD', 			5);
define('ACTION_REMOVE', 		6);
define('ACTION_START', 			7);
define('ACTION_STOP', 			8);
define('ACTION_MOVE_MASK',		15);
define('ACTION_ZOOM_THRESHOLD',	16);

define('VIDEOTYPE_NTSC',		0);
define('VIDEOTYPE_PAL',			1);
define('MAX_USER',				7);
define('MAX_USER_10',			12);
define('MAX_PROFILE',			10);
define('MAX_RESOLUTION_COUNT',	20);
define('MAX_VIDEO_ENCODER', 	10);
define('MAX_PTZ_PRESET12',		12);
define('MAX_PTZ_PRESET128',	128);
define('MAX_PTZ_PRESET255',	255);
define('gFIRMWAREUPGRADE',		'FirmwareUpgrade-1.0.0-100820.xap');
define('gSDBACKUP', 				'SDBackup-1.0.0-100820.xap');

define('MAX_GROUP_LIST_255',				255);
define('AUDIOCODEC_MASK_G726', 			0x02);
define('AUDIOCODEC_MASK_AAC', 			0x04);
define('AUDIOSOURCE_MASK_LINEIN',	0x01);
define('AUDIOSOURCE_MASK_INTERAL_MIC',	0x02);
define('AUDIOSOURCE_MASK_EXTERAL_MIC',	0x04);
define('VIDEOCODEC_MASK_MPEG4', 			0x04);

define('ANALOG_AVAILABLE', 			0x01);
define('ANALOG_ONOFF_CONFIGURABLE', 0x02);
define('ANALOG_NTPAL_CONFIGURABLE', 0x04);

define('IRIS_NOT_SUPPORT',	0x00);
define('IRIS_SUPPORT', 		0x01);
define('PIRIS_SUPPORT',	 	0x02);
define('IRIS_FNO_SUPPORT', 0x04);
define('DOME_PIRIS_SUPPORT', 0x08);

define('MOTORIZE_FOCUS_ONLY_SUPPORT', 1);
define('MOTORIZE_FOCUS_ZOOM_SUPPORT', 2);

define('VA_NOT_SUPPORT', 	0x00);
define('MD_SUPPORT', 		0x01);
define('IV_SUPPORT', 		0x02);

define('MAX_VGA', 	0);
define('MAX_4CIF', 	1);
define('MAX_SVGA', 	2);
define('MAX_1_MEGA', 3);
define('MAX_2_MEGA', 4);
define('MAX_3_MEGA', 5);

define('MF_5000', 1);
define('MF_7000', 2);
define('MF_6200', 3);
define('MF_1001', 4);
define('MF_3002', 5);
define('MF_5001', 6);
define('MF_7001', 7);
define('MF_7002', 8);
define('MF_5300', 9);
define('MF_6004', 10);
define('MF_5004', 11);
define('MF_7010FE', 12);
define('MF_7004', 13);
define('MF_6321', 14);
define('MF_5321', 15);
define('MF_6320', 16);
define('MF_5430', 17);
define('MF_5200', 18);
define('MF_3371', 19);
define('MF_3120', 20);
define('MF_6201', 21);
define('MF_6110', 22);
define('MF_8010', 23);
define('MF_3516', 24);
define('MF_6400', 25);

define('ISP_TYPE_WN1', 		0);
define('ISP_TYPE_WN2', 		1);
define('ISP_TYPE_WN2_REV', 2);
define('ISP_TYPE_WN2_PTZ', 3);
define('ISP_TYPE_NEW1', 	4);
define('ISP_TYPE_A1', 		5);
define('ISP_NO_TYPE', 		6);
define('ISP_TYPE_WN3', 		7);
define('ISP_TYPE_HISILICON',  8);
define('ISP_TYPE_WN3_PTZ',   	9);


define('MAX_PTZ_SWING',						3);
define('MAX_PRIVACY_AREA_COUNT',			32);
define('N2_PRIVACY_RECTANGLE_COUNT',	16);
define('N2_PRIVACY_POLYGON_COUNT',		1);	//(N2_PRIVACY_AREA_COUNT - N2_PRIVACY_RECTANGLE_COUNT)
define('WN1_PRIVACY_RECTANGLE_COUNT',	12);
define('WN1_PRIVACY_POLYGON_COUNT',		0);
define('NEW1_PRIVACY_RECTANGLE_COUNT',	0);
define('NEW1_PRIVACY_POLYGON_COUNT',	32);
define('A1_PRIVACY_RECTANGLE_COUNT',	0);
define('A1_PRIVACY_POLYGON_COUNT',		12	);// modified by sj0428.ko, 2011.08.19 : privacy area max is 12

define('PTZ_NOT_SUPPORT', 0);
define('ZOOM_ONLY_SUPPORT', 1);
define('PT_ONLY_SUPPORT', 2);
define('PTZ_SUPPORT', 3);

define ('PRIVACY_COLOR_TYPE_EVERY', 0);
define ('PRIVACY_COLOR_TYPE_EACH', 1);

define ('BACKLIGHT_MASK_HLC', 0x01);
define ('BACKLIGHT_MASK_WDR', 0x02);
define ('BACKLIGHT_MASK_WDR_LIMIT', 0x04);

if($GLOBALS['M_SPECIAL_TYPE'] == 1) {
// DEV_S1FACTORY
define('CMD_FACTORY_CLEAR', 10007);
//DEV_S1PWD_CHANGE_TIME
define('CMD_PW_CHANGE_TIME'	,			10001);
// DEV_S1PWRESTORE
define('CMD_PASSWORD_RESTORE',			10005);
}
$XMLArray = '';
$VIDEOTYPE = '';
$MEGAMODE = 3;
$VIEWER_WIDTH = '';
$VIEWER_HEIGHT = '';
$VIEWER_RESOLUTION = array('width'=>640, 'height'=>480);
$MAX_RESOLUTION = array('width'=>0, 'height'=>0);
$FLIP = 0;
$MIRROR = 0;
$JPEGUUID = '';
$SNAPUUID = '';
$LANGINDEX = 0;
$LANGSTRING = '';
$SOCKET_MANAGER = NULL;
$REQUEST_URI = '';

// DEV_S1PWRESTORE
if($GLOBALS['M_SPECIAL_TYPE'] == 1) {
	$USERINFO = array('name'=>'', 'pw'=>'', 'pw_js'=>'', 'level'=>1, 'profile'=>0, 'audioin'=>0, 'audioout'=>0, 'relay'=>0, 'ptz'=>0, 'encname'=>'', 'encpw'=>'', 's1'=>false);
}
else {
	$USERINFO = array('name'=>'', 'pw'=>'', 'level'=>1, 'profile'=>0, 'audioin'=>0, 'audioout'=>0, 'relay'=>0, 'ptz'=>0, 'encname'=>'', 'encpw'=>'');
}
// OPEN SDK PARAMETERS
$SDK_APP_CONFIG_FILE = "IPCameraManifest.xml";
$SDK_APP_INSTALL_DIRECTORY = "/mnt/opensdk/apps/";
$SDK_APP_DOWNLOAD_DIRECTORY = "/tmp/opensdk/downloaded/";
$SDK_APP_EXTRACTED_DIRECTORY = "/tmp/opensdk/extracted/";
$SDK_APP_IPC_DIRECTORY = "/tmp/opensdk_ipcs/";
$SDK_MARKET_APP_DIRECTORY = "/tmp/opensdk/downloaded/";
$SDK_MARKET_APP_CONFIG_FILE = "AppMarket.xml";
$SDK_MARKET_APP_CONFIG_FILE_DIR = "/mnt/opensdk/";

if ($GLOBALS['M_SPECIAL_TYPE'] != 1)	//DEV_S1LOGIN
{
	session_start();
	if (!isset($_SESSION['count']))
		$_SESSION['count'] = rand(1,10000);
}

if ($GLOBALS['M_SPECIAL_TYPE'] == 1)	//DEV_S1LOGIN
{
	// for session manage
	$session_url = $_SERVER['PHP_SELF'];

	// skip cgi-bin, cgi-bin-noauth urls
	$cgi_bin_pattern = '/^\/cgi-bin\//';
	$cgi_bin_noauth_pattern = '/^\/cgi-bin-noauth\//';
	if (preg_match($cgi_bin_pattern, $session_url, $matches1, PREG_OFFSET_CAPTURE) == 1 || preg_match($cgi_bin_noauth_pattern, $session_url, $matches2, PREG_OFFSET_CAPTURE) == 1){
		// no include session
	}else{
		session_save_path('/tmp/websess');	// session path
		//session_cache_expire(60); // 세션 유효시간 : 분
		session_cache_limiter ("nocache, must-revalidate");
		ini_set("session.cookie_lifetime", 0); // 세션 쿠키가 작동하는 시간 : 초
		ini_set("session.cache_expire", 60); // 세션 유효시간 : 분
		ini_set("session.gc_maxlifetime", 3600); // 세션 가비지 컬렉션(로그인시 세션지속 시간) : 초
		session_start();	// session start
		if (!isset($_SESSION['count']))
			$_SESSION['count'] = rand(1,10000);
		require_once ('_session.inc');
	}

}

function CheckXMLMessage()
{
	$xmlData = str_replace('&_=', '', urldecode(trim(@file_get_contents('php://input'))));
	$xml_parser = xml_parser_create();
	if (xml_parse($xml_parser, $xmlData, true)) {
		$GLOBALS['XMLArray'] = simplexml_load_string($xmlData);
	}
	else {
		ResponseText('XML error'.xml_error_string(xml_get_error_code($xml_parser)).'at line '.xml_get_current_line_number($xml_parser));
	}
	$xmlRootName = $GLOBALS['XMLArray']->GetName();
	$actionList = array('Get', 'Set', 'Add', 'Stop', 'Start', 'Remove', 'GetAll', 'Backup', 'Restore', 'Move', 'Threshold');
	for ($index=9; $index>2; --$index) {
		$action = substr($xmlRootName, 0, $index);
		for ($index2=0; $index2<count($actionList); ++$index2) {
			if ($action == $actionList[$index2]) {
				$menu = substr($xmlRootName, $index);
				$actionCmd = array('Add'=>ACTION_ADD, 'Set'=>ACTION_SET, 'Get'=>ACTION_GET, 'Start'=>ACTION_START, 'Stop'=>ACTION_STOP, 'Remove'=>ACTION_REMOVE, 'GetAll'=>ACTION_GET_ALL, 'Backup'=>ACTION_GET, 'Restore'=>ACTION_SET, 'Move'=>ACTION_MOVE_MASK, 'Threshold'=>ACTION_ZOOM_THRESHOLD);
				return array('menu'=>$menu, 'action'=>$actionCmd[$action]);
			}
		}
	}
	ResponseText(FALSE);
}

function SetData(&$_dataInfo, &$_payload, $_dataArray, $_dataFormat='')
{
	if ($_dataFormat == '') $_dataFormat = MakeDataFormat($_dataInfo);
	if (is_string($_dataArray)) {
		if ($_dataFormat == '') return;
		$_dataArray = unpack($_dataFormat, $_dataArray);
	}
	foreach($_dataArray as $name=>$value) {
		if (substr($_dataInfo[$name]['type'], 0, 1) == 'A') $value = stripslashes(trim($value));
		if ($name == 'BitrateLimit') $value = (int)$value * 1024;
		$_dataInfo[$name]['value'] = $value;
	}
	$_payload = MakePayload($_dataInfo);

}

// For S1 function(user.class)
function SetDataNoTrim(&$_dataInfo, &$_payload, $_dataArray, $_dataFormat='')
{
	if ($_dataFormat == '') $_dataFormat = MakeDataFormat($_dataInfo);
	if (is_string($_dataArray)) {
		if ($_dataFormat == '') return;
		$_dataArray = unpack($_dataFormat, $_dataArray);
	}
	foreach($_dataArray as $name=>$value) {
		if (substr($_dataInfo[$name]['type'], 0, 1) == 'A') $value = str_replace("\0", "", $value);
		if ($name == 'BitrateLimit') $value = (int)$value * 1024;
		$_dataInfo[$name]['value'] = $value;
	}
	$_payload = MakePayloadNoTrim($_dataInfo);

}
function CheckConnection($_className)
{
	if (!$GLOBALS['M_SUPPORT_EVENT_FD']							&& $_className == 'FDConfiguration') 		return FALSE;
	if (!$GLOBALS['M_SUPPORT_EVENT_AD']							&& $_className == 'ADConfiguration') 		return FALSE;
	if ($GLOBALS['M_MAX_RESOLUTION'] != MAX_3_MEGA			&& $_className == 'VideoSourceSelection')	return FALSE;
	if ($GLOBALS['M_ALARMOUT_COUNT'] == 0 						&& $_className == 'RelayOutputStates')		return FALSE;
	if (($GLOBALS['M_SUPPORT_EVENT_VA'] & IV_SUPPORT == 0)	&& $_className == 'VAConfiguration')		return FALSE;
	if ($GLOBALS['M_SUPPORT_PTZ_TRACKING'] == 0 				&& $_className == 'TrackingPreset') 		return FALSE;
	if ($GLOBALS['M_AUX_COUNT'] == 0 								&& $_className == 'PTZAuxiliary')			return FALSE;
	if (($GLOBALS['M_SUPPORT_SD'] == 0 && $GLOBALS['M_SUPPORT_NAS'] == 0)	 && $_className == 'ManualRecording') return FALSE;
	if (($GLOBALS['M_SUPPORT_PTZ'] == 0 && $GLOBALS['M_SUPPORT_EXTERNAL_PTZ'] == 0)	 && $_className == 'PTZPreset') return FALSE;
	if (($GLOBALS['M_SUPPORT_ISCSI'] == 0)	 && $_className == 'ISCSIConfiguration') return FALSE;
	return TRUE;
}

function GetClassInstance($_pageName='', $_noInfo='')
{
	$classInstances = array();
	$GLOBALS['SOCKET_MANAGER'] = new SocketManager();
	if ($_pageName == '' || (substr($_pageName, 0, 3) != 'cgi' && $_noInfo == '')) {
		require_once ('info.class');
		$classInstances['Information'] = $GLOBALS['SOCKET_MANAGER']->Connection(new Information());
	}

	if (substr($_pageName, 0, 3) == 'cgi') $_pageName = substr($_pageName, 4);
	if ($_pageName != '') {
		if ($GLOBALS['M_SPECIAL_TYPE'] == 1) {
		$classList = array(	'monitoring'		=>	array('profile'=>'VideoProfile', 'relay'=>array('RelayOutputStates', 'PTZAuxiliary', 'ManualRecording'), 'va'=>'VAConfiguration', 'record'=>array('StorageInfo', 'RecordConfiguration'), 'nas'=>'NasConfiguration', 'preset'=>'PTZPreset', 'media'=>'MediaConfiguration'),
									'ddns'				=> array('ddns'=>array('DDNSConfiguration', 'QuickConnectConfiguration')),
									'protocol'			=> array('network_protocol'=>'NetworkProtocols'),
									'https'				=>	array('https'=>'HTTPSConfiguration', 'network_protocol'=>'NetworkProtocols'),
									'system'				=> array('system'=>'SystemConfiguration'),
									//'ftpemail'			=> array('network_ftp'=>'FTPSetting', 'network_smtp'=>'SMTPSetting'),
									'ftpemail'			=> array('network_ftp'=>'FTPSetting', 'network_smtp'=>'SMTPSetting', 'network_sms'=>'SMSSetting'),
									'videoprofile'		=> array('profile'=>array('VideoProfile', 'StreammingDisconnection'), 'imagesetting'=>'ImageSetting', 'info'=>'ResolutionInfo'),
									'video'				=> array('media'=>'MediaConfiguration', 'av'=>array('Profiles', 'ProfileConfiguration', 'VideoSourceSelection'), 'profile'=>array('VideoProfile', 'StreammingDisconnection')),
									'videosrc'			=> array('media'=>'MediaConfiguration','videosource'=>array('VideoSource', 'PrivacyMask'),'imagesetting'=>'ImageSetting'),
									'audio'				=> array('media'=>'MediaConfiguration'),
									'smartcodec'		=>	array('fd'=>array('SmartCodecConfiguration', 'FDConfiguration')),
									'storage' 			=> array('record'=>array('StorageInfo', 'RecordConfiguration'), 'continuous_record'=>'ContinuousRecord', 'nas'=>array('NasConfiguration', 'ISCSIConfiguration')),
									'8021x'				=>	array('https'=>'Configuration802Dot1x'),
									'image' 				=> array('imagesetting'=>'ImageSetting', 'media'=>'MediaConfiguration', 'videosource'=>'VideoSource'),
									'serial'				=>	array('serial'=>'SerialConfiguration'),
									'QoS'					=>	array('qos'=>'QoSConfiguration'),
									'SNMP'				=> array('network_snmp'=>array('SNMPConfiguration', 'SNMPTrapConfiguration')),
									'ipfilter'			=> array('ipfilter'=>'IPFilterConfiguration'),
									'interface'			=> array('interface'=>'InterfaceConfiguration'),
									'datetime'			=> array('ntp'=>'NTPConfiguration', 'datetime'=>'DateTimeConfiguration'),
									'event_setup'		=> array('event'=>'EventConfiguration', 'va'=>'VAConfiguration', 'fd'=>'FDConfiguration', 'ad'=>'ADConfiguration'),
									'event_list'		=> array('event'=>'EventConfiguration'),
									'alarm'				=> array('alarm'=>'SensorConfiguration'),
									'md'					=> array('va'=>'MDConfiguration'),
									'va'					=> array('va'=>'VAConfiguration', 'preset'=>'PTZPreset'),
									'timesched'			=> array('timesched'=>'TimeScheduleConfiguration'),
									'network'			=> array('network'=>'NetworkConfiguration'),
									'netdiscon'			=> array('netdiscon'=>'NetworkDisconnectConfiguration'),
									'fd'					=> array('fd'=>'FDConfiguration'),
									'tampering'			=> array('tampering'=>'TamperingConfiguration'),
									'opensdk'			=> array('opensdk'=>'OpenSDKConfiguration'),
									'ad'					=> array('ad'=>'ADConfiguration'),
									// DEV_S1FACTORY
									'factoryclear'		=> array('factoryclear'=>'Factoryclear'),
									 // DEV_S1LOGIN
									'userlogin'			=> array('userlogin'=>'UserLogin'),
									'user'				=> array('user'=>'UserConfiguration'),
									//DEV_S1PWD_CHANGE_TIME
									'time_password' => array('time_password'=>'time_password'),
									'privacy'			=> array('videosource'=>'PrivacyMask'),
									'profileaccess'	=> array('profileaccess'=>'ProfileAccessInformation'),
									'directosd' 		=> array('imagesetting'=>'ImageSetting', 'preset'=>'PTZPreset'),
									'osdtime'			=> array('osd'=>'OSDTime'),
									'sdrecord' 			=> array('profile'=>'VideoProfile', 'record'=>array('StorageInfo', 'RecordConfiguration'), 'continuous_record'=>'ContinuousRecord'),
									'bonjour'			=> array('autodiscovery'=>'BonjourConfiguration'),
									'upnp'				=> array('autodiscovery'=>'UPNPConfiguration'),
									'zeroconfig'		=> array('autodiscovery'=>'ZeroConfiguration'),
									'sdk'					=> array('sdk'=>'SDKInfoRequest'),
									'ptzsetup'			=>	array('serial'=>'SerialConfiguration', 'preset'=>'PTZPreset'),
									'ptz'					=>	array('ptz'=> array('PTZTour', 'PTZGroup', 'PTZSwing', 'PTZAutorun'), 'preset'=>'PTZPreset', 'presetedit'=>array('PresetImageConfiguration','PresetVAConfiguration'),'event'=>'EventConfiguration'),
									'ptzsequence'		=> array('ptz'=> array('PTZTour', 'PTZGroup', 'PTZSwing', 'PTZAutorun'), 'simplepreset'=>'PresetList'),
									'tracking'			=>	array('tracking'=>'TrackingPreset'),
									'ptztracking'		=>	array('preset'=>'PTZPreset', 'tracking'=>'TrackingPreset', 'videosource'=>'PrivacyMask'),
									'trackingEvent'	=>	array('trackingEvent'=>'TrackingConfiguration'),
									'relaySetting'		=>	array('relay_setting'=>'RelayOutputConfiguration'),
									'chineseosd'		=>	array('osd'=>'ChineseOSDConfiguration'),
									'tour'				=>	array('ptz'=> 'PTZTour'),
									'group'				=>	array('ptz'=> 'PTZGroup'),
									'swing'				=>	array('ptz'=> 'PTZSwing'),
									'autorun'			=>	array('ptz'=> 'PTZAutorun'),
									'presetedit'		=>	array('presetedit'=>array('PresetImageConfiguration','PresetVAConfiguration')),
									'ptzlimit'			=>	array('ptzlimit'=>'PTZLimit','tracking'=>'TrackingPreset'),
									'presetlist'		=>	array('simplepreset'=>'PresetList'),
									'autoipconfig'		=> array('autodiscovery'=>array('UPNPConfiguration', 'BonjourConfiguration', 'ZeroConfiguration')),
									'account_temp'			=> array('user'=>'UserConfiguration', 'https'=>'Configuration802Dot1x', 'network_snmp'=>array('SNMPConfiguration', 'SNMPTrapConfiguration'), 'nas'=>'NasConfiguration', 'ddns'=>array('DDNSConfiguration', 'QuickConnectConfiguration'), 'network_ftp'=>'FTPSetting', 'network_smtp'=>'SMTPSetting'));
			}
		else {
$classList = array(	'monitoring'		=>	array('profile'=>'VideoProfile', 'relay'=>array('RelayOutputStates', 'PTZAuxiliary', 'ManualRecording'), 'va'=>'VAConfiguration', 'record'=>array('StorageInfo', 'RecordConfiguration'), 'nas'=>'NasConfiguration', 'preset'=>'PTZPreset', 'media'=>'MediaConfiguration'),
									'ddns'				=> array('ddns'=>array('DDNSConfiguration', 'QuickConnectConfiguration')),
									'protocol'			=> array('network_protocol'=>'NetworkProtocols'),
									'https'				=>	array('https'=>'HTTPSConfiguration', 'network_protocol'=>'NetworkProtocols'),
									'system'				=> array('system'=>'SystemConfiguration'),
									'ftpemail'			=> array('network_ftp'=>'FTPSetting', 'network_smtp'=>'SMTPSetting'),
									'videoprofile'		=> array('profile'=>array('VideoProfile', 'StreammingDisconnection'), 'imagesetting'=>'ImageSetting', 'info'=>'ResolutionInfo'),
									'video'				=> array('media'=>'MediaConfiguration', 'av'=>array('Profiles', 'ProfileConfiguration', 'VideoSourceSelection'), 'profile'=>array('VideoProfile', 'StreammingDisconnection')),
									'videosrc'			=> array('media'=>'MediaConfiguration','videosource'=>array('VideoSource', 'PrivacyMask'),'imagesetting'=>'ImageSetting'),
									'audio'				=> array('media'=>'MediaConfiguration'),
									'smartcodec'		=>	array('fd'=>array('SmartCodecConfiguration', 'FDConfiguration')),
									'storage' 			=> array('record'=>array('StorageInfo', 'RecordConfiguration'), 'continuous_record'=>'ContinuousRecord', 'nas'=>array('NasConfiguration', 'ISCSIConfiguration')),
									'8021x'				=>	array('https'=>'Configuration802Dot1x'),
									'image' 				=> array('imagesetting'=>'ImageSetting', 'media'=>'MediaConfiguration', 'videosource'=>'VideoSource'),
									'serial'				=>	array('serial'=>'SerialConfiguration'),
									'QoS'					=>	array('qos'=>'QoSConfiguration'),
									'SNMP'				=> array('network_snmp'=>array('SNMPConfiguration', 'SNMPTrapConfiguration')),
									'ipfilter'			=> array('ipfilter'=>'IPFilterConfiguration'),
									'interface'			=> array('interface'=>'InterfaceConfiguration'),
									'datetime'			=> array('ntp'=>'NTPConfiguration', 'datetime'=>'DateTimeConfiguration'),
									'event_setup'		=> array('event'=>'EventConfiguration', 'va'=>'VAConfiguration', 'fd'=>'FDConfiguration', 'ad'=>'ADConfiguration'),
									'event_list'		=> array('event'=>'EventConfiguration'),
									'alarm'				=> array('alarm'=>'SensorConfiguration'),
									'md'					=> array('va'=>'MDConfiguration'),
									'va'					=> array('va'=>'VAConfiguration', 'preset'=>'PTZPreset'),
									'timesched'			=> array('timesched'=>'TimeScheduleConfiguration'),
									'network'			=> array('network'=>'NetworkConfiguration'),
									'netdiscon'			=> array('netdiscon'=>'NetworkDisconnectConfiguration'),
									'fd'					=> array('fd'=>'FDConfiguration'),
									'tampering'			=> array('tampering'=>'TamperingConfiguration'),
									'opensdk'			=> array('opensdk'=>'OpenSDKConfiguration'),
									'ad'					=> array('ad'=>'ADConfiguration'),
									// DEV_S1FACTORY
									'factoryclear'		=> array('factoryclear'=>'Factoryclear'),
									 // DEV_S1LOGIN
									'userlogin'			=> array('userlogin'=>'UserLogin'),
									'user'				=> array('user'=>'UserConfiguration'),
									//DEV_S1PWD_CHANGE_TIME
									'user'				=> array('user'=>'UserConfiguration'),
									'privacy'			=> array('videosource'=>'PrivacyMask'),
									'profileaccess'	=> array('profileaccess'=>'ProfileAccessInformation'),
									'directosd' 		=> array('imagesetting'=>'ImageSetting', 'preset'=>'PTZPreset'),
									'osdtime'			=> array('osd'=>'OSDTime'),
									'sdrecord' 			=> array('profile'=>'VideoProfile', 'record'=>array('StorageInfo', 'RecordConfiguration'), 'continuous_record'=>'ContinuousRecord'),
									'bonjour'			=> array('autodiscovery'=>'BonjourConfiguration'),
									'upnp'				=> array('autodiscovery'=>'UPNPConfiguration'),
									'zeroconfig'		=> array('autodiscovery'=>'ZeroConfiguration'),
									'sdk'					=> array('sdk'=>'SDKInfoRequest'),
									'ptzsetup'			=>	array('serial'=>'SerialConfiguration', 'preset'=>'PTZPreset'),
									'ptz'					=>	array('ptz'=> array('PTZTour', 'PTZGroup', 'PTZSwing', 'PTZAutorun'), 'preset'=>'PTZPreset', 'presetedit'=>array('PresetImageConfiguration','PresetVAConfiguration'),'event'=>'EventConfiguration'),
									'ptzsequence'		=> array('ptz'=> array('PTZTour', 'PTZGroup', 'PTZSwing', 'PTZAutorun'), 'simplepreset'=>'PresetList'),
									'tracking'			=>	array('tracking'=>'TrackingPreset'),
									'ptztracking'		=>	array('preset'=>'PTZPreset', 'tracking'=>'TrackingPreset', 'videosource'=>'PrivacyMask'),
									'trackingEvent'	=>	array('trackingEvent'=>'TrackingConfiguration'),
									'relaySetting'		=>	array('relay_setting'=>'RelayOutputConfiguration'),
									'chineseosd'		=>	array('osd'=>'ChineseOSDConfiguration'),
									'tour'				=>	array('ptz'=> 'PTZTour'),
									'group'				=>	array('ptz'=> 'PTZGroup'),
									'swing'				=>	array('ptz'=> 'PTZSwing'),
									'autorun'			=>	array('ptz'=> 'PTZAutorun'),
									'presetedit'		=>	array('presetedit'=>array('PresetImageConfiguration','PresetVAConfiguration')),
									'ptzlimit'			=>	array('ptzlimit'=>'PTZLimit','tracking'=>'TrackingPreset'),
									'presetlist'		=>	array('simplepreset'=>'PresetList'),
									'autoipconfig'		=> array('autodiscovery'=>array('UPNPConfiguration', 'BonjourConfiguration', 'ZeroConfiguration')),
									'account_temp'			=> array('user'=>'UserConfiguration', 'https'=>'Configuration802Dot1x', 'network_snmp'=>array('SNMPConfiguration', 'SNMPTrapConfiguration'), 'nas'=>'NasConfiguration', 'ddns'=>array('DDNSConfiguration', 'QuickConnectConfiguration'), 'network_ftp'=>'FTPSetting', 'network_smtp'=>'SMTPSetting'));
		}
		foreach ($classList[$_pageName] as $require=>$className) {
			require_once ($require.'.class');
			if (is_array($className)) {
				for ($index=0; $index<count($className); ++$index) {
					$cName = $className[$index];
					if (CheckConnection($cName) == FALSE) continue;
					$classInstances[$cName] = $GLOBALS['SOCKET_MANAGER']->Connection(new $cName());
				}
			}
			else {
				if (CheckConnection($className) == FALSE) continue;
				$classInstances[$className] = new $className();
				$GLOBALS['SOCKET_MANAGER']->Connection($classInstances[$className]);
			}
		}
	}
	return $classInstances;
}
function ResponseSDKText($_errorCode)
{
	$_msg = "";
	$_msg = '<?xml version="1.0" encoding="utf-8" ?>'."\n";
	$_msg .= '<ErrorCode>'."\n";
	$_msg .= $_errorCode."\n";
	$_msg .= '</ErrorCode>'."\n";
	header('Content-Type: text/xml; charset=utf-8');
	header('Content-Length: '.strlen($_msg));
	echo $_msg;
	exit;
}

function ResponseText($_msg)
{
	if 		(is_bool($_msg) && $_msg == FALSE)	$_msg = 'NG';
	else if 	(is_bool($_msg) && $_msg == TRUE) 	$_msg = 'OK';
	header("Content-Type: text/plain");
	header("Content-Length:".strlen($_msg));
	echo $_msg;
	exit;
}

function ResponseResult($_value)
{
	$msgType = array('NG', 'OK');
	header("Content-Type: text/plain");
	header("Content-Length: 2");
	echo $msgType[$_value];
	exit;
}

function ResponseXML($_dataClass, $_menu, $_xmlMsg='')
{
	$actionName = 'Get';
	if ($_dataClass->headerInfo['Action'] == ACTION_GET_ALL) $actionName = 'GetAll';
	$msg = '<?xml version="1.0" encoding="utf-8" ?>'."\r\n";
	$msg .= '<'.$actionName.$_menu.'Response>'."\r\n";
	if ($_xmlMsg == '') {
		if (method_exists($_dataClass, 'GetXMLData')) {
			$msg .= $_dataClass->GetXMLData($_menu);
		}
		else {
			$msg .= MakeXMLData($_dataClass->dataInfo);
		}
	}
	else {
		$msg .= $_xmlMsg;
	}
	$msg .= '</'.$actionName.$_menu.'Response>'."\r\n";
	header('Content-Type: text/xml; charset=utf-8');
	header('Content-Length: '.strlen($msg));
	echo $msg;
	exit;
}

function MakeXMLData($_dataInfo, $_name='')
{
	$msg = '';
	$tabVal = '';
	if (strlen($_name) != 0) {
		$tabVal = "\t";
		$msg .= $tabVal.'<'.$_name.'>';
	}
	foreach ($_dataInfo as $name=>$value) {
		if ($name == 'Reserved') continue;
		$msg .= "\t".$tabVal.'<'.$name.'>'.$value['value'].'</'.$name.'>';
	}
	if (strlen($_name) != 0)	$msg .= $tabVal.'</'.$_name.'>';
	return $msg;
}

function MakeUnpackFormat($_name, $_length, $_maxValue)
{
	$unpackFormat = '';
	for ($index=0; $index<$_maxValue; ++$index)
		$unpackFormat .= 'A'.$_length.$_name.$index.'/';
	return $unpackFormat;
}

function CheckAdminAccount($_state=TRUE)
{
	// DEV_S1LOGIN
	if ($_SESSION['sess_auth_type'] == 1) {
		if ($_SESSION['sess_user_id'] != 'admin') {
			if ($_state) {
				echo "<meta http-equiv='refresh' content='0; url=http://".trim($_SERVER['HTTP_HOST'])."/index.htm'>";
				exit;
			}
			else {
				ResponseText(FALSE);
			}
		}
	}
	else
	{
		$digest = '';
		preg_match_all('/(\w+)="([\w\s\~\`\!\@\$\^\*\(\)\_\-\|\{\}\[\]\;\,\.\?\/]+)"/', $_SERVER['PHP_AUTH_DIGEST'], $digest);
		for ($index=0; $index<count($digest[1]); ++$index) {
			if ($digest[1][$index] == 'username') {
				if ($digest[2][$index] != 'admin') {
					if ($_state == FALSE) ResponseText(FALSE);
					echo "<meta http-equiv='refresh' content='0; url=http://".trim($_SERVER['HTTP_HOST'])."/index.htm'>";
					exit;
				}
			}
		}
	}
}
function CheckGuestAccount($_state=TRUE)
{
	// DEV_S1LOGIN
	if ($_SESSION['sess_auth_type'] == 1) {
		if ($_SESSION['sess_user_id'] == 'guest') {
			if ($_state) {
				echo "<meta http-equiv='refresh' content='0; url=http://".trim($_SERVER['HTTP_HOST'])."/index.htm'>";
				exit;
			}
			else {
				ResponseText(FALSE);
			}
		}
	}
	else
	{
		$digest = '';
		preg_match_all('/(\w+)="([\w\s\~\`\!\@\$\^\*\(\)\_\-\|\{\}\[\]\;\,\.\?\/]+)"/', $_SERVER['PHP_AUTH_DIGEST'], $digest);
		for ($index=0; $index<count($digest[1]); ++$index) {
			if ($digest[1][$index] == 'username') {
				if ($digest[2][$index] == 'guest') {
					if ($_state) {
						echo "<meta http-equiv='refresh' content='0; url=http://".trim($_SERVER['HTTP_HOST'])."/index.htm'>";
						exit;
					}
					else {
						ResponseText(FALSE);
					}
				}
			}
		}
	}
}
function MakeDataFormat($_dataInfo)
{
	$dataFormat = '';
	while($data = current($_dataInfo)) {
		if (is_array($data) && array_key_exists('type', $data)) {
			$dataFormat .= $data['type'].key($_dataInfo)."/";
			next($_dataInfo);
		}
	}
	return $dataFormat;
}

function MakePayload($_dataInfo)
{
	$payload = '';
	foreach($_dataInfo as $data)
	{
		if (is_array($data) && array_key_exists('type', $data) && array_key_exists('value', $data)) {
			$payload .= pack(strtolower($data['type']), trim($data['value']));
		}
	}
	return $payload;
}

// For S1 function(user.class)
function MakePayloadNoTrim($_dataInfo)
{
	$payload = '';
	foreach($_dataInfo as $data)
	{
		if (is_array($data) && array_key_exists('type', $data) && array_key_exists('value', $data)) {
			$payload .= pack(strtolower($data['type']), $data['value']);
		}
	}
	return $payload;
}

function GetPayloads($_dataClass, $_max)
{
	$payloads = '';
	for ($index=0; $index<$_max; ++$index)
	{

		$payloads .= $_dataClass[$index]->payload;
	}
	return $payloads;
}

function GetDataInfoLength($_dataInfo)
{
	$totalLength = 0;
	foreach ($_dataInfo as $data) {
		$length = (int)substr($data['type'], 1);
		$type = substr($data['type'], 0, 1);
		if ($type == 'i' ||  $type == 'I') $length *= 4;
		$totalLength += $length;
	}
	return $totalLength;
}

function CheckModelName($_param)
{
	$model = $_SERVER['MODELNAME'];
	if (strlen($model) < 2) {
		require_once ('system.class');
		$GLOBALS['SOCKET_MANAGER'] = new SocketManager();
		$systemConf = $GLOBALS['SOCKET_MANAGER']->Connection(new SystemConfiguration());
		$model = $systemConf->deviceInfo->dataInfo['Model']['value'];
	}

	switch($_param) {
///////////////////////////////////////
////////////// MODEL
///////////////////////////////////////
		case 'All7001':							{	if ($model == 'SNB-7001'		|| $model == 'SND-7061'	|| 	$model == 'SND-7011') 	return TRUE;	}  break;
		case 'All5001':							{	if ($model == 'SNB-5001'		|| $model == 'SND-5061'	|| 	$model == 'SND-5011'	|| 	$model == 'SND-5010') 	return TRUE;	}  break;
		case 'All7002':							{	if ($model == 'SNB-7002'		|| $model == 'SND-7082' 	|| 	$model == 'SNV-7082'	|| 	$model == 'SNO-7082R')	return TRUE;	}  break;
		case 'All3002':							{	if ($model == 'SNB-3002'		|| $model == 'SND-3082'	|| 	$model == 'SNV-3082')		return TRUE;	}	break;
		case 'All5000':							{	if ($model == 'SNB-5000'		|| $model == 'SND-5080'	|| 	$model == 'SND-5080F'	||	$model == 'SNV-5080' 	||	$model == 'SNB-5000A'  	|| 	$model == 'SNB-5000TJ')  return TRUE;		}	break;
		case 'All7000':							{	if	($model == 'SNB-7000'		|| $model == 'SNV-7080' 	||	$model == 'SND-7080'	|| 	$model == 'SNV-7080R'	|| 	$model == 'SNO-7080R') return TRUE;		}	break;
		case 'All1001':	 						{	if ($model == 'SNB-1001' 	|| $model == 'SND-1011' 	|| 	$model == 'SND-1080'	|| 	$model == 'SNV-1080' 	|| 	$model == 'SNO-1080R'		||	$model == 'SNV-1080R') 				return TRUE;	}	break;
		case 'MEGA':	 							{	if ($model == 'SNV-5010'		|| $model == 'SNB-5000A'	|| 	$model == 'SNO-5080R'	|| 	$model == 'SNV-5080R'	|| 	$model == 'SNB-5000TJ' 	|| CheckModelName('All5000')) 		return TRUE;	}	break;
		case 'AllS202':							{	if	($model == 'SNB-S202'		|| $model == 'SNB-S201'	||	$model == 'SND-S202'	|| $model == 'SND-S201'	|| 	$model == 'SNO-S202R'		|| 	$model == 'SND-S202R') 				return TRUE;	}	break;
		case 'All6004':							{	if	($model == 'SNB-6004'		|| $model == 'SNB-6003'	||	$model == 'SND-6084'	|| $model == 'SND-6083'	|| 	$model == 'SNV-6012M'	|| 	$model == 'SNO-6084R'		|| 	$model == 'SNV-6084R'	||	$model == 'SND-6084R' || CheckModelName('AllS202') || $model == 'SNP-6320') return TRUE;		}	break;
///////////////////////////////////////
////////////// FEATURE
///////////////////////////////////////
		case 'HLC':								{	if (CheckModelName('All7002') || CheckModelName('MEGA')  || CheckModelName('All7000')) return TRUE; } break;
		case 'WDR':								{	if (CheckModelName('All7002') || CheckModelName('All7000') || CheckModelName('All3002') || CheckModelName('All6004')) return TRUE; }break;
		case 'CAR':								{	if	(CheckModelName('AllS202')) return TRUE;	} break;
		case 'LENS_SHADING':					{ 	if	($model == 'SNO-6011R'	||	$model == 'SND-6011R'	||	$model == 'SNV-6012M')	return TRUE; } break;
	}
	return FALSE;
}

function ArrayPop(&$_array, $_value)
{
	unset($_array[array_search($_value, $_array)]);
	$_array = array_values($_array);
}

function GetBrowserName()
{
	$browser = '';
	$useragent = $_SERVER['HTTP_USER_AGENT'];
	if (preg_match('|MSIE ([0-9]{1,2}.[0-9]{1,2})|', $useragent, $matched) || preg_match('|Trident/.*rv:([0-9]{1,}[\.0-9]{0,})|', $useragent, $matched)) {
		$browser = 'IE';
	}
	else if(preg_match('/Chrome/i',$useragent))
	{
		$browser = 'Google Chrome';
	}
	else if(preg_match('/Safari/i',$useragent))
	{
		$browser = 'Apple Safari';
   }
	else if(preg_match('/Firefox/i',$useragent))
	{
		$browser = 'Mozilla Firefox';
	}
	return $browser;
}

function ieversion()
{
 	ereg('MSIE ([0-9]{1,2}.[0-9])',$_SERVER['HTTP_USER_AGENT'],$reg);
	if(!isset($reg[1])){
		ereg('Trident/.*rv:([0-9]{1,}[\.0-9]{0,})',$_SERVER['HTTP_USER_AGENT'],$reg);
		if(isset($reg[1])){
			return floatval($reg[1]);
		}else{
			return -1;
		}
	}
	else return floatval($reg[1]);
}

function SafePassword($_password,$_id)
{
	$pattern_num=0;
	$pattern_upper_alpha=0;
	$pattern_lower_alpha=0;
	$pattern_simbol=0;
	$check = 0;

	$passwordlength = strlen($_password);
	if( $passwordlength < 8)
		return 1;
	if ($_password == $_id)
	{
		return 2;
	}
	for($index = 0;$index < $passwordlength;$index++){
		$ch = substr($_password,$index,1);

		if ( $ch >= 'a' && $ch <= 'z' ){
			$pattern_lower_alpha++;
		}else if( $ch >= 'A' && $ch <= 'Z' ){
			$pattern_upper_alpha++;
		}else if( $ch >= '0' && $ch <= '9' ){
			$pattern_num++;
		}else if( $ch == '~' || $ch == '`' || $ch == '!' || $ch == '@' || $ch == '#' || $ch == '$' || $ch == '%' || $ch == '^' || $ch == '*' ||
				$ch == '(' || $ch == ')' || $ch == '_' || $ch == '-' || $ch == '+' || $ch == '=' || $ch == '|' ||
				$ch == '{' || $ch == '}' || $ch == '[' || $ch == ']' || $ch == '.' || $ch == '?' || $ch == '/' ){
			$pattern_simbol++;
		}
	}

	if ($pattern_lower_alpha != 0)	$check++;
	if ($pattern_upper_alpha != 0)	$check++;
	if ($pattern_num != 0)	$check++;
	if ($pattern_simbol != 0)	$check++;

	if($passwordlength < 10)
	{
		if($check < 3) return 3;
	}
	else
	{
		if($check < 2) return 4;
	}


	return 0;

}


function debug($output)							{	echo "<pre>";	print_r($output);	echo "</pre>\n";	}
function GetMyRequestURI($_scriptName)	{
	if ($GLOBALS['M_SPECIAL_TYPE'] == 1) {
		return (str_replace('/cgi-bin-stw/stw.cgi', $_scriptName, $GLOBALS['REQUEST_URI']));
	}
	else {
		return (str_replace('/cgi-bin/stw.cgi', $_scriptName, $GLOBALS['REQUEST_URI']));
	}
}

// fix the system log backup issue for S1
function GetMyRequestURIS1($_scriptName)	{
	$requestURI = str_replace('/cgi-bin-stw/stw.cgi', $_scriptName, $GLOBALS['REQUEST_URI']);

	$startPos = strpos($requestURI, "//");
	// next to position "//"
	$startPos += 2;

	$endPos = strpos($requestURI, "@");
	// next to position "@"
	$endPos += 1;

	$replace_str = substr($requestURI, $startPos, ($endPos - $startPos));

	return str_replace($replace_str, "", $requestURI);
}

class SocketManager
{
	public 	$socket;
	public	$ipcAddr;
	public	$payload;
	public	$dataInfo;
	public	$dataInfo_sdk_app;
	public	$ipcAction;
	public	$ipcCommand;

	function __construct($_ipcAddr = '')
	{
		$this->ipcAddr = '/tmp/ipc_path';
		if ($_ipcAddr != '')	$this->ipcAddr = $_ipcAddr;
	}

	function SetHeaderValue($_dataClass)
	{
		$account = (strlen($GLOBALS['USERINFO']['name']) < 1 ? "admin" : $GLOBALS['USERINFO']['name']);
		$this->dataInfo = array('MagicNumber' 		=> array('value'=>(int)0xFFFEFFFE,							'type'=>'i1'),
										'IPCMajorVersion' => array('value'=>0, 												'type'=>'c1'),
										'IPCMinorVersion' => array('value'=>6, 												'type'=>'c1'),
										'Command'			=>	array('value'=>$_dataClass->headerInfo['Command'], 	'type'=>'i1'),
										'Action'				=>	array('value'=>$_dataClass->headerInfo['Action'],	'type'=>'c1'),
										'Type'				=>	array('value'=>0, 												'type'=>'c1'),
										'ErrorCode' 		=> array('value'=>0, 												'type'=>'c1'),
										'PayloadLength'	=>	array('value'=>strlen($_dataClass->payload), 			'type'=>'i1'),
										'PeerIP' 			=> array('value'=>'127.0.0.1', 								'type'=>'A40'),
										'PeerPort' 			=> array('value'=>80, 											'type'=>'i1'),
										'PeerAccount' 		=> array('value'=>$account, 									'type'=>'A16'),
										'Reserved' 			=> array('value'=>'WEB', 										'type'=>'A8'));
		$this->payload 		= MakePayload($this->dataInfo);
		$this->ipcAction 	= $_dataClass->headerInfo['Action'];
		$this->ipcCommand 	= $_dataClass->headerInfo['Command'];
	}

	function CreateSocket()
	{
		$this->socket = @socket_create(AF_UNIX, SOCK_STREAM, 0);
		if ($this->socket < 0)	return FALSE;
		socket_set_option($this->socket, SOL_SOCKET, SO_SNDTIMEO, array('sec'=>10, 'usec'=>0));
		if ($this->ipcCommand == CMD_RECORD_BACKUP || $this->ipcCommand == CMD_CONFIGURATION_BACKUP) {
			socket_set_option($this->socket, SOL_SOCKET, SO_RCVTIMEO, array('sec'=>3, 'usec'=>0));
		}
		else {
			socket_set_option($this->socket, SOL_SOCKET, SO_RCVTIMEO, array('sec'=>1, 'usec'=>0));
		}

		$retryCnt = 0;
		$sleepVal = array(1, 1, 1);
		do {
			$retVal = @socket_connect($this->socket, $this->ipcAddr);
			if ($retVal === FALSE) {
				if ($retryCnt > 2) {
					if($this->socket > 0) {
						socket_shutdown($this->socket);
						socket_close($this->socket);
					}
					$this->socket = NULL;
					exit;
				}
				usleep($sleepVal[$retryCnt++]*1000000);	//ms
			}
		} while (!$retVal);
		return TRUE;
	}

	function SendPacket($_packet)
	{
		$retVal = @socket_write($this->socket, $_packet, strlen($_packet));
		if ($retVal === FALSE) {
			if($this->socket > 0) {
				socket_shutdown($this->socket);
				socket_close($this->socket);
			}
			$this->socket = NULL;
			return FALSE;
		}
		return TRUE;
	}

	function ReceivePacket($_packetSize)
	{
		$retryCnt = 0;
		$sleepVal = array(1, 3, 5);
		$recvPacketSize = 0;
		$totalRecvPacket = '';
		do {
			$recvPacket = @socket_read($this->socket, ($_packetSize-$recvPacketSize));			//  receive header (68 byte)
			if ($recvPacket == FALSE || strlen($recvPacket) == 0) {
				if ($retryCnt < 10) {
					usleep(1000000);	//ms
					$retryCnt++;
					if ($recvPacketSize < $_packetSize) 			continue;	// not complete recv data
					if (socket_last_error($this->socket) == 0) 	continue;	// Success
					if (socket_last_error($this->socket) == 4) 	continue;	// ??
					if (socket_last_error($this->socket) == 11) 	continue;	// EAGAIN
				}
				else {
					if($this->socket > 0) {
						socket_shutdown($this->socket);
						socket_close($this->socket);
					}
					$this->socket = NULL;
					exit;
				}
			}
			$totalRecvPacket .= $recvPacket;
			$recvPacketSize = strlen($totalRecvPacket);
		} while($_packetSize != $recvPacketSize);
		return $totalRecvPacket;
	}

	function Connection($_dataClass)
	{
		$this->SetHeaderValue($_dataClass);
		if ($this->socket == NULL && $this->CreateSocket() == FALSE)	exit;
		if (!$this->SendPacket($this->payload)) 	ResponseText(FALSE);	// Send Header
		if ($this->CheckConnect('Send') && !($this->SendPacket($_dataClass->payload))) ResponseText(FALSE);	// Send Payload
		$recvPacket = $this->ReceivePacket(strlen($this->payload));		// Receive Header
		SetData($this->dataInfo, $this->payload, $recvPacket);				// Unpack Header Data

		if ($this->dataInfo['ErrorCode']['value'] != 1)	$this->CheckErrorCode();	// Check ErrorCode
		if ($this->CheckConnect('Receive')){
         $recvPacket = $this->ReceivePacket($this->dataInfo['PayloadLength']['value']);	// Receive Payload
			if($this->ipcCommand == CMD_SDK_APP_DATA) {
				$_dataClass->PayloadToArray($recvPacket, $this->dataInfo['PayloadLength']['value']); // Unpack Payload Data - Dynamic receive length
			}
         else {
         	if ($this->dataInfo['Command']['value'] == CMD_PRIVACY_AREA || $this->dataInfo['Command']['value'] == CMD_TRACKING_TRACEZONE) {
					$_dataClass->SetErrorCode($this->dataInfo['ErrorCode']['value']);
				}
				$_dataClass->PayloadToArray($recvPacket);	// Unpack Payload Data
			}
		}
		if ($this->ipcAction == ACTION_GET && ($this->ipcCommand == CMD_RECORD_BACKUP || $this->ipcCommand == CMD_CONFIGURATION_BACKUP)) {
			do {	// Server-Push Type
				$recvPacket = $this->ReceivePacket(strlen($this->payload));	// Receive Header
				SetData($this->dataInfo, $this->payload, $recvPacket);
				$recvPacket = $this->ReceivePacket($this->dataInfo['PayloadLength']['value']);	// Receive Payload
            $isContinue = $_dataClass->PayloadToData($recvPacket, $this->dataInfo['PayloadLength']['value']);	// Unpack Payload Data
			} while($isContinue);
		}
		if($this->socket > 0) {
			socket_shutdown($this->socket);
			socket_close($this->socket);
		}
		$this->socket = NULL;
		return $_dataClass;
	}

	function CheckErrorCode()
	{
		if ($this->ipcCommand == CMD_FACTORY) return;
		if ($this->dataInfo['ErrorCode']['value'] != 1) 	{
			if ($this->ipcCommand == CMD_RECORD_BACKUP || $this->ipcCommand == CMD_CONFIGURATION_BACKUP) {	echo "0";	exit;	}
			else if ($this->ipcCommand == CMD_OPENSDK_APP ) {	ResponseSDKText($this->dataInfo['ErrorCode']['value']); }
			else if ($this->ipcCommand == CMD_PRIVACY_AREA || $this->ipcCommand == CMD_TRACKING_TRACEZONE) return;
			else if ($this->ipcCommand == CMD_OPENSDK_APP_DEBUG ) {
				$_error_msg = $this->dataInfo['ErrorCode']['value'];
				header("Content-Type: text/plain");
				header("Content-Length:".strlen($_error_msg));
				echo $_error_msg;
				exit;
			}
			else if ($GLOBALS['M_MAX_RESOLUTION'] == MAX_3_MEGA && $this->ipcCommand == CMD_IMAGE_CONFIGURATION && $this->dataInfo['ErrorCode']['value'] != 2) {
				header("Content-Type: multipart/form-data;"); 	//multipart/x-mixed-replace
				echo $this->dataInfo['ErrorCode']['value'];		// 66(not ready), 42(invalid set)
				exit;
			}
			// DEV_S1LOGIN
			else if ($this->ipcCommand == CMD_USER_LOGIN) {
				return;
			}
			ResponseText(FALSE);
		}
		else {
			if ($this->ipcAction != ACTION_GET && $this->ipcAction != ACTION_GET_ALL && ($this->ipcCommand != CMD_LOG_SEARCH && $this->ipcCommand != CMD_LOG_SEARCH_DETAIL)) ResponseText(TRUE);
		}
	}

	function CheckConnect($_type)
	{
		if ($_type == "Send") {
			switch ($this->ipcAction) {
				case ACTION_SET: case ACTION_ADD:	case ACTION_REMOVE:	return TRUE;
				case ACTION_GET: {
					switch ($this->ipcCommand) {
					case CMD_RECORD_BACKUP:	case CMD_IMAGING:	case CMD_IMAGE_CONFIGURATION:	case CMD_PTZ_PRESET:	case CMD_PTZ_PRESET_ATTR:	case CMD_INFORMATION:	 case CMD_ONVIF_INFO: case CMD_SDK_APP_ATTRIBUTES: case CMD_OPENSDK_APP: case CMD_RUN_CONFORMANCE:
							case CMD_SDK_SEARCH_DETAIL: case CMD_SDK_APP_DATA:  case CMD_SDK_TASK_MANAGER: case CMD_PTZ_PRESET_VA: case CMD_PTZ_SWING: case CMD_PTZ_GROUP: case CMD_PTZ_TOUR: case CMD_PTZ_TRACE: case CMD_PTZ_AUTORUN: case CMD_TRACKING_TARGETLOCK:
							case CMD_PTZ_AUXILIARY: case CMD_DOT11_STATUS:
							return TRUE;
					}
				} break;
				case ACTION_START: case ACTION_MOVE_MASK: {
					switch ($this->ipcCommand) {
						case CMD_FACTORY:		case CMD_RECORD_SEARCH:	case CMD_PTZ_PRESET:	case CMD_RECORD_SEARCH_DETAIL:	case CMD_MULTICAST_STREAMING:	case CMD_STORAGE_FORMAT:
						case CMD_PLAYBACK:		case CMD_NETWORK_TEST:	case CMD_LOG_SEARCH:	case CMD_LOG_SEARCH_DETAIL:		case CMD_IMAGE_CONFIGURATION:	case CMD_MOTORIZED_LENS_SETUP:
						case CMD_NAS_CONFIGURATION:	 case CMD_TIME_SEARCH: case CMD_TIME_SEARCH_DETAIL: case CMD_OPENSDK_APP: case CMD_PTZ_PRESET_ATTR: case CMD_OPENSDK_APP_DEBUG:
						case CMD_PTZ_SWING: case CMD_PTZ_GROUP: case CMD_PTZ_TOUR: case CMD_PTZ_TRACE: case CMD_PTZ_AUTORUN: case CMD_PTZ_HOMEPOSITION:
						case CMD_PTZ_INSTANT_AF: case CMD_TRACKING_TARGETLOCK: case CMD_PTZ_LIMIT: case CMD_PRIVACY_AREA: case CMD_PTZ_PRESETEDIT: case CMD_TRACKING_TRACEZONE:
						case CMD_ISCSI_CONFIGURATION: case CMD_ISCSI_DISCOVERY:	case CMD_RUN_CONFORMANCE:
						case CMD_PASSWORD_RESTORE: // DEV_S1PWRESTORE
							return TRUE;
					}
				} break;
				case ACTION_STOP: {
					switch ($this->ipcCommand) {
					case CMD_MULTICAST_STREAMING: case CMD_OPENSDK_APP: case CMD_PTZ_PRESET_ATTR: case CMD_PTZ_PRESETEDIT: case CMD_RUN_CONFORMANCE:
							return TRUE;
					}
				} break;
				case ACTION_GET_ALL:{
					switch ($this->ipcCommand) {
						case CMD_RUN_CONFORMANCE:
							return TRUE;
					}
				} break;
				case ACTION_ZOOM_THRESHOLD:{
					if($this->ipcCommand == CMD_PRIVACY_AREA)
					return TRUE;
				} break;
			}
		}
		else if ($_type == "Receive") {
			switch ($this->ipcAction) {
				case ACTION_START: {
					switch ($this->ipcCommand) {
						case CMD_LOG_SEARCH:	case CMD_LOG_SEARCH_DETAIL: case CMD_NETWORK_TEST: case CMD_RECORD_SEARCH:	case CMD_OPENSDK_APP:case CMD_OPENSDK_APP_DEBUG:
						case CMD_RECORD_SEARCH_DETAIL:	 case CMD_TIME_SEARCH: case CMD_TIME_SEARCH_DETAIL: case CMD_PRIVACY_AREA: case CMD_TRACKING_TRACEZONE:
						case CMD_ISCSI_DISCOVERY: case CMD_ISCSI_CONFIGURATION:
						case CMD_PASSWORD_RESTORE: // DEV_S1PWRESTORE
							return TRUE;
					}
				} break;
				case ACTION_ZOOM_THRESHOLD: { if($this->ipcCommand == CMD_PRIVACY_AREA) return TRUE; }
					break;
				case ACTION_SET: { if($this->ipcCommand == CMD_PRIVACY_AREA) return TRUE; }
					break;
				case ACTION_GET: case ACTION_GET_ALL:	return TRUE;
				case ACTION_ADD: { 	if ($this->ipcCommand == CMD_OPENSDK_APP) 	return TRUE;	} break;
				case ACTION_MOVE_MASK: { if($this->ipcCommand == CMD_TRACKING_TRACEZONE) return TRUE; }
			}
		}
		return FALSE;
	}
}
?>
