<?php
set_time_limit(60);
require_once('modelinfo.cgi');

define('CMD_IPADDRESS_FILTER', 12);
define('CMD_SMTP_SETTING', 13);
define('CMD_FTP_SETTING', 14);
define('CMD_NETWORK_TEST', 16);
define('CMD_USER', 25);
define('CMD_CERTIFICATE', 26);
define('CMD_CERTIFICATE_STATE', 27);
define('CMD_SENSOR_CONFIGURATION', 32);
define('CMD_SENSOR_STATE', 33);
define('CMD_MEDIA_CONFIGURATION', 38);
define('CMD_IV_CONFIGURATION', 43);
define('CMD_TIMER_CONFIGURATION', 60);
define('CMD_HTTPS_DATA', 63);
define('CMD_IMAGE_CONFIGURATION', 80);
define('CMD_VIDEO_SOURCE_SELECTION', 84);
define('CMD_SMARTCODEC', 85);
define('CMD_802_1X_CONFIGURATION', 86);
define('CMD_802_1X_DATA', 87);
define('CMD_MD_CONFIGURATION', 88);
define('CMD_VA_CONFIGURATION', 89);
define('CMD_NETWORK_EVENT', 91);
define('CMD_FD_CONFIGURATION', 95);
define('CMD_TAMPERING_CONFIGURATION', 97);
define('CMD_EVENT_CONFIGURATION', 99);
define('CMD_VIDEO_SOURCE_3120', 101);
define('CMD_PRIVACY_MASK', 103);
define('CMD_PRIVACY_AREA', 104);
define('CMD_PTZ_INSTANT_AF',		139);
define('CMD_MOTORIZED_LENS_SETUP',	140);
define('CMD_TRACKING_PRESET', 142);
define('CMD_TRACKING_TARGETLOCK', 143);
define('CMD_TRACKING_TRACEZONE', 144);
define('CMD_TRACKING_STOP', 145);
define('CMD_AD_CONFIGURATION', 149);
define('CMD_AD_DATA', 150);
define('CMD_POP_SETTING', 306);
define('CMD_HTTP_SETTING', 307);
define('CMD_INFORMATION', 8888);
//OPENSDK COMMANDS
define('CMD_OPENSDK_APP',						13000);
define('CGI_CMD_OPENSDK_APP_DEBUG',			13002);
define('CMD_SDK_SEARCH_DETAIL',				14000);
define('CMD_SDK_APP_ATTRIBUTES',				15000);
define('CMD_SDK_TASK_MANAGER',				15001);
define('CMD_SDK_UPDATE_LICENSE', 			16007);
//OPENSDK 3RD PARTY COMMANDS
define('CMD_SDK_APP_DATA',			        	16000);
define('CMD_SDK_MARKET',			        	16001);
define('CMD_OPENSDK_APP_EVENT',			   13006);

////////////////////////////////////////////////////////////////////////////////
// Actions
define('ACTION_GET', 0);
define('ACTION_GET_ALL', 1);
define('ACTION_SET', 4);
define('ACTION_ADD', 5);
define('ACTION_REMOVE', 6);
define('ACTION_START', 7);
define('ACTION_STOP', 8);
define('ACTION_MOVE_MASK',		15);
define('ACTION_ZOOM_THRESHOLD',		16);
////////////////////////////////////////////////////////////////////////////////
// Defines
define('MAX_USER', 7);
define('MAX_USER_10', 12);

////////////////////////////////////////////////////////////////////////////////
// ModelInfo ID Defines

define('IRIS_NO_SUPPORT', 		0x00);
define('IRIS_SUPPORT', 		0x01);
define('PIRIS_SUPPORT',	 	0x02);
define('IRIS_FNO_SUPPORT', 0x04);
define('DOME_PIRIS_SUPPORT', 0x08);

define('MOTORIZE_FOCUS_ONLY_SUPPORT', 1);
define('MOTORIZE_FOCUS_ZOOM_SUPPORT', 2);

define('VA_NOT_SUPPORT', 	0x00);
define('MD_SUPPORT', 		0x01);
define('IV_SUPPORT', 		0x02);

define('PTZ_NOT_SUPPORT', 0);
define('ZOOM_ONLY_SUPPORT', 1);
define('PT_ONLY_SUPPORT', 2);
define('PTZ_SUPPORT', 3);

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
define('ISP_TYPE_HISILICON', 	8);
define('ISP_TYPE_WN3_PTZ', 		9);

define('MAX_PRIVACY_AREA_COUNT',			32);
define('N2_PRIVACY_RECTANGLE_COUNT',	16);
define('N2_PRIVACY_POLYGON_COUNT',		1);	//(N2_PRIVACY_AREA_COUNT - N2_PRIVACY_RECTANGLE_COUNT)
define('WN1_PRIVACY_RECTANGLE_COUNT',	12);
define('WN1_PRIVACY_POLYGON_COUNT',		0);
define('NEW1_PRIVACY_RECTANGLE_COUNT',	0);
define('NEW1_PRIVACY_POLYGON_COUNT',	32);
define('A1_PRIVACY_RECTANGLE_COUNT',	0);
define('A1_PRIVACY_POLYGON_COUNT',		12	);// modified by sj0428.ko, 2011.08.19 : privacy area max is 12

define ('PRIVACY_COLOR_TYPE_EVERY', 0);
define ('PRIVACY_COLOR_TYPE_EACH', 1);

define ('PRIVACY_AREA_TYPE_MASK_RECTANGLE', 1);
define ('PRIVACY_AREA_TYPE_MASK_POLYGON', 2);

define('BACKLIGHT_MASK_HLC', 		0x01);
define('BACKLIGHT_MASK_WDR',	 	0x02);
define('BACKLIGHT_MASK_WDR_LIMIT', 0x04);

////////////////////////////////////////////////////////////////////////////////
// STATUS ERROR CODES

define('STATUS_OK', 1);
define('STATUS_SUBMENU_NOT_FOUND', 600);
define('STATUS_ACTION_NOT_FOUND', 601);
define('STATUS_INVALID_PARAMETER', 602);
define('STATUS_MISSING_PARAMETER', 603);
define('STATUS_INVALID_VALUE', 604);
define('STATUS_LIST_FULL', 605);
define('STATUS_DUPLICATE_VALUE', 606);
define('STATUS_UNKNOWN_ERROR', 607);
define('STATUS_NOT_IMPLEMENTED', 608);
define('STATUS_NOT_AUTHORIZED', 609);
define('STATUS_INVALID_FILE', 611);
define('STATUS_TAG_NOT_FOUND', 700);
define('STATUS_INVALID_XML', 701);

////////////////////////////////////////////////////////////////////////////////
// Response Status and Text Class Defintion 
class ResponseOutput
{

    //put your code here
    public $errCode;
    public $outputMsg;

    function __construct()
    {
        $this->errCode = STATUS_OK;
        $this->outputMsg = '';
    }

}

////////////////////////////////////////////////////////////////////////////////
// Globals

$boolArray = array(
	0 => 'False',
	1 => 'True'
);

$Sensitivity = array(
	1 => 'VeryLow',
	2 => 'Low',
	3 => 'Medium',
	4 => 'High',
	5 => 'VeryHigh'
);

$EventAreaMode = array(
	0 => 'Outside',
	1 => 'Inside'
);

$DetectionType = array(
	0 => 'MotionDetection',
	1 => 'IntelligentVideo',
	2 => 'MDAndIV',
	3 => 'Off'
);

$LineDetectionMode = array(
	0 => 'RightSide',
	1 => 'LeftSide',
	2 => 'LeftSide,RightSide',
	3 => 'RightSide,LeftSide' //'AnySide'
);

$EntireAreaMode = array(
    0 => 'Off',
    1 => 'AppearDisappear',
    2 => 'Scenechange'
);

$DefinedAreaMode = array(
    1 => 'AppearDisappear',
    2 => 'Entering',
    3 => 'Exiting',
    4 => 'Entering,Exiting',
    5 => 'Exiting,Entering'
);

$systemErrorCodeMap = array(
    0 => STATUS_UNKNOWN_ERROR, 1 => STATUS_OK, 2 => STATUS_UNKNOWN_ERROR, 3 => STATUS_INVALID_VALUE, 4 => STATUS_INVALID_VALUE, 5 => STATUS_INVALID_VALUE,
    6 => STATUS_INVALID_VALUE, 7 => STATUS_INVALID_VALUE, 8 => STATUS_INVALID_VALUE, 9 => STATUS_UNKNOWN_ERROR, 10 => STATUS_UNKNOWN_ERROR,
    11 => STATUS_UNKNOWN_ERROR, 12 => STATUS_DUPLICATE_VALUE, 13 => STATUS_UNKNOWN_ERROR, 14 => STATUS_LIST_FULL, 15 => STATUS_UNKNOWN_ERROR,
    16 => STATUS_UNKNOWN_ERROR, 17 => STATUS_UNKNOWN_ERROR, 18 => STATUS_UNKNOWN_ERROR, 19 => STATUS_UNKNOWN_ERROR, 20 => STATUS_UNKNOWN_ERROR,
    21 => STATUS_UNKNOWN_ERROR, 22 => STATUS_UNKNOWN_ERROR, 23 => STATUS_UNKNOWN_ERROR, 24 => STATUS_UNKNOWN_ERROR, 25 => STATUS_UNKNOWN_ERROR,
    26 => STATUS_NOT_IMPLEMENTED, 27 => STATUS_INVALID_VALUE, 28 => STATUS_UNKNOWN_ERROR, 29 => STATUS_UNKNOWN_ERROR, 30 => STATUS_UNKNOWN_ERROR,
    31 => STATUS_UNKNOWN_ERROR, 32 => STATUS_UNKNOWN_ERROR, 33 => STATUS_UNKNOWN_ERROR, 34 => STATUS_UNKNOWN_ERROR, 35 => STATUS_UNKNOWN_ERROR,
    36 => STATUS_LIST_FULL, 37 => STATUS_UNKNOWN_ERROR, 38 => STATUS_UNKNOWN_ERROR, 39 => STATUS_UNKNOWN_ERROR, 40 => STATUS_UNKNOWN_ERROR,
    41 => STATUS_UNKNOWN_ERROR, 42 => STATUS_UNKNOWN_ERROR, 43 => STATUS_DUPLICATE_VALUE, 44 => STATUS_INVALID_VALUE, 45 => STATUS_INVALID_VALUE,
    46 => STATUS_INVALID_VALUE, 47 => STATUS_LIST_FULL, 48 => STATUS_UNKNOWN_ERROR, 49 => STATUS_UNKNOWN_ERROR, 50 => STATUS_INVALID_VALUE,
    51 => STATUS_UNKNOWN_ERROR, 52 => STATUS_UNKNOWN_ERROR, 53 => STATUS_INVALID_VALUE, 54 => STATUS_UNKNOWN_ERROR, 55 => STATUS_UNKNOWN_ERROR,
    56 => STATUS_UNKNOWN_ERROR, 57 => STATUS_UNKNOWN_ERROR, 58 => STATUS_UNKNOWN_ERROR, 59 => STATUS_UNKNOWN_ERROR, 60 => STATUS_UNKNOWN_ERROR,
    61 => STATUS_UNKNOWN_ERROR, 62 => STATUS_UNKNOWN_ERROR, 63 => STATUS_UNKNOWN_ERROR, 64 => STATUS_UNKNOWN_ERROR, 65 => STATUS_UNKNOWN_ERROR,
    66 => STATUS_NOT_IMPLEMENTED, 67 => STATUS_UNKNOWN_ERROR, 68 => STATUS_UNKNOWN_ERROR, 100 => STATUS_UNKNOWN_ERROR, 101 => STATUS_UNKNOWN_ERROR, 
	102 => STATUS_UNKNOWN_ERROR, 103 => STATUS_UNKNOWN_ERROR, 104 => STATUS_UNKNOWN_ERROR, 105 => STATUS_UNKNOWN_ERROR, 106 => STATUS_UNKNOWN_ERROR, 
	107 => STATUS_UNKNOWN_ERROR, 108 => STATUS_UNKNOWN_ERROR, 109 => STATUS_UNKNOWN_ERROR, 110 => STATUS_UNKNOWN_ERROR, 111 => STATUS_UNKNOWN_ERROR, 
	112 => STATUS_UNKNOWN_ERROR, 113 => STATUS_UNKNOWN_ERROR, 114 => STATUS_UNKNOWN_ERROR, 115 => STATUS_UNKNOWN_ERROR, 116 => STATUS_UNKNOWN_ERROR, 
	117 => STATUS_UNKNOWN_ERROR, 118 => STATUS_UNKNOWN_ERROR, 119 => STATUS_UNKNOWN_ERROR
);

////////////////////////////////////////////////////////////////////////////////

$XMLArray = '';
$SOCKET_MANAGER = NULL;
$USERINFO = array('name' => '', 'pw' => '', 'level' => 1, 'profile' => 0, 'audioin' => 0, 'audioout' => 0, 'relay' => 0, 'ptz' => 0);
// OPEN SDK PARAMETERS
$SDK_APP_CONFIG_FILE = "IPCameraManifest.xml";
$SDK_APP_INSTALL_DIRECTORY = "/mnt/opensdk/apps/";
$SDK_APP_DOWNLOAD_DIRECTORY = "/tmp/opensdk/downloaded/";
$SDK_APP_EXTRACTED_DIRECTORY = "/tmp/opensdk/extracted/";
$SDK_APP_IPC_DIRECTORY = "/tmp/opensdk_ipcs/";
$SDK_MARKET_APP_DIRECTORY = "/tmp/opensdk/downloaded/";
$SDK_MARKET_APP_CONFIG_FILE = "AppMarket.xml";
$SDK_MARKET_APP_CONFIG_FILE_DIR = "/mnt/opensdk/";

function CheckXMLMessage()
{
    $responseOutput = new ResponseOutput();

    $xmlData = str_replace('&_=', '', urldecode(trim(@file_get_contents('php://input'))));
    $xml_parser = xml_parser_create();
    if (xml_parse($xml_parser, $xmlData, true))
    {
        $GLOBALS['XMLArray'] = simplexml_load_string($xmlData);
    }
    else
    {
        $responseOutput->errCode = STATUS_INVALID_XML;
        SendResponse($responseOutput);
    }
    $xmlRootName = $GLOBALS['XMLArray']->GetName();
    $actionList = array('Get', 'Set', 'Add', 'Stop', 'Start', 'Remove', 'GetAll', 'Backup', 'Restore');
    for ($index = 7; $index > 2; --$index)
    {
        $action = substr($xmlRootName, 0, $index);
        for ($index2 = 0; $index2 < count($actionList); ++$index2)
        {
            if ($action == $actionList[$index2])
            {
                $menu = substr($xmlRootName, $index);
                $actionCmd = array('Add' => ACTION_ADD, 'Set' => ACTION_SET, 'Get' => ACTION_GET, 'Start' => ACTION_START, 'Stop' => ACTION_STOP, 'Remove' => ACTION_REMOVE, 'GetAll' => ACTION_GET_ALL, 'Backup' => ACTION_GET, 'Restore' => ACTION_SET, 'Move'=>ACTION_MOVE_MASK, 'Zoom'=>ACTION_ZOOM_THRESHOLD);
                return array('menu' => $menu, 'action' => $actionCmd[$action]);
            }
        }
    }
    $responseOutput->errCode = STATUS_UNKNOWN_ERROR;
    SendResponse($responseOutput);
}

function SetData(&$_dataInfo, &$_payload, $_dataArray, $_dataFormat = '')
{
    if ($_dataFormat == '')			$_dataFormat = MakeDataFormat($_dataInfo);        
    if (is_string($_dataArray))	$_dataArray = unpack($_dataFormat, $_dataArray);
    foreach ($_dataArray as $name => $value)
    {
        foreach ($_dataInfo as $key => $data)
        {
            if ($key != $name) continue;
            if (substr($_dataInfo[$name]['type'], 0, 1) == 'A') $value = stripslashes(trim($value));                
            $_dataInfo[$name]['value'] = $value;
            break;
        }
    }
    $_payload = MakePayload($_dataInfo);
}

function CheckConnection($_pageName, $_className)
{
	if (!$GLOBALS['M_SUPPORT_EVENT_FD'] && $_className == 'FDConfiguration')	return FALSE;
	if (!$GLOBALS['M_SUPPORT_EVENT_AD'] && $_className == 'ADConfiguration')	return FALSE;
	return TRUE;
}

function GetClassInstance($_pageName = '', $_noInfo = '')
{
	$classInstances = array();
	$GLOBALS['SOCKET_MANAGER'] = new SocketManager();
	$classList = array(	'user' 		=> array('user' => 'UserConfiguration'),
								'alarm' 		=> array('alarm' => 'SensorConfiguration'),
								'va' 			=> array('va' => 'VAConfiguration'),
								'fd' 			=> array('fd' => 'FDConfiguration'),
								'tampering' => array('tampering' => 'TamperingConfiguration'),
								'ad' 			=> array('ad' => 'ADConfiguration'),				
								'netdiscon'	=> array('netdiscon'=>'NetworkDisconnectConfiguration'),
								'timesched' => array('timesched' => 'TimeScheduleConfiguration'),
								'tracking' 	=> array('tracking' => 'TrackingPreset'),				
								'image' 		=> array('imagesetting' => 'ImageSetting', 'media' => 'MediaConfiguration', 'videosource' => 'VideoSource'),
								'smartcodec'=> array('fd' => array('SmartCodecConfiguration', 'FDConfiguration')),
								'privacy' 	=> array('videosource' => 'PrivacyMask'),
								'ipfilter' 	=> array('ipfilter' => 'IPFilterConfiguration', 'info'=>'Information'),
								'8021x' 		=> array('https' => 'Configuration802Dot1x'),            
								'https' 		=> array('https' => 'HTTPSConfiguration'),
								'ftpemail' 	=> array('network_ftp' => 'FTPSetting', 'network_smtp' => 'SMTPSetting', 'network_test' => 'NetworkTestConfiguration'),
								'sdk'			=> array('sdk'=>'SDKInfoRequest'));
	foreach ($classList[$_pageName] as $require => $className)
	{
		require_once ($require . '.class');
		if (is_array($className))
		{
		    for ($index = 0; $index < count($className); ++$index)
		    {
		        $cName = $className[$index];
		        if (CheckConnection($_pageName, $cName) == FALSE)	continue;                     
		        $classInstances[$cName] = $GLOBALS['SOCKET_MANAGER']->Connection(new $cName());
		    }
		}
		else
		{
		    if (CheckConnection($_pageName, $className) == FALSE) continue;
		    $classInstances[$className] = new $className();
		    $GLOBALS['SOCKET_MANAGER']->Connection($classInstances[$className]);
		}
	}
	return $classInstances;
}

function SendResponse($responseOutput, $headerOpt = 1, $boundary = "")
{
    $http_protocol = "HTTP/1.0";
    if (isset($_SERVER['SERVER_PROTOCOL']) && stripos($_SERVER['SERVER_PROTOCOL'], "HTTP") >= 0)
    {
        $http_protocol = $_SERVER['SERVER_PROTOCOL'];
    }

    // Status Codes Used in STW Cameras
    $errorMessage = array(
        STATUS_SUBMENU_NOT_FOUND => 'NG' . "\r\n" . 'Error Code: ' . STATUS_SUBMENU_NOT_FOUND . "\r\n" . 'Error Details: ' . "\r\n" . 'Submenu Not Found',
        STATUS_ACTION_NOT_FOUND => 'NG' . "\r\n" . 'Error Code: ' . STATUS_ACTION_NOT_FOUND . "\r\n" . 'Error Details: ' . "\r\n" . 'Action Not Found',
        STATUS_INVALID_PARAMETER => 'NG' . "\r\n" . 'Error Code: ' . STATUS_INVALID_PARAMETER . "\r\n" . 'Error Details: ' . "\r\n" . 'Invalid Parameter(s)',
        STATUS_MISSING_PARAMETER => 'NG' . "\r\n" . 'Error Code: ' . STATUS_MISSING_PARAMETER . "\r\n" . 'Error Details: ' . "\r\n" . 'Missing Required Parameter(s)',
        STATUS_INVALID_VALUE => 'NG' . "\r\n" . 'Error Code: ' . STATUS_INVALID_VALUE . "\r\n" . 'Error Details: ' . "\r\n" . 'Invalid Input Value(s)',
        STATUS_LIST_FULL => 'NG' . "\r\n" . 'Error Code: ' . STATUS_LIST_FULL . "\r\n" . 'Error Details: ' . "\r\n" . 'List Full',
        STATUS_DUPLICATE_VALUE => 'NG' . "\r\n" . 'Error Code: ' . STATUS_DUPLICATE_VALUE . "\r\n" . 'Error Details: ' . "\r\n" . 'Duplicate Value In List',
        STATUS_UNKNOWN_ERROR => 'NG' . "\r\n" . 'Error Code: ' . STATUS_UNKNOWN_ERROR . "\r\n" . 'Error Details: ' . "\r\n" . 'Unknown Error',
        STATUS_NOT_IMPLEMENTED => 'NG' . "\r\n" . 'Error Code: ' . STATUS_NOT_IMPLEMENTED . "\r\n" . 'Error Details: ' . "\r\n" . 'Feature(s) Not Implemented OR Not Supported',
        STATUS_NOT_AUTHORIZED => 'NG' . "\r\n" . 'Error Code: ' . STATUS_NOT_AUTHORIZED . "\r\n" . 'Error Details: ' . "\r\n" . 'Not Authorized',
		STATUS_INVALID_FILE => 'NG' . "\r\n" . 'Error Code: ' . STATUS_INVALID_FILE . "\r\n" . 'Error Details: ' . "\r\n" . 'Invalid File',
        STATUS_TAG_NOT_FOUND => 'NG' . "\r\n" . 'Error Code: ' . STATUS_TAG_NOT_FOUND . "\r\n" . 'Error Details: ' . "\r\n",
        STATUS_INVALID_XML => 'NG' . "\r\n" . 'Error Code: ' . STATUS_INVALID_XML . "\r\n" . 'Error Details: ' . "\r\n" . 'Invalid XML'
    );

	if($headerOpt != 3)
	{
		header($http_protocol . ' 200 OK');
	}

    if ($headerOpt == 1)
    {
        header("Content-Type: text/plain");
    }
	else if($headerOpt == 2)
	{
		header('Content-Type: text/xml; charset=utf-8');
	}
	else if($headerOpt == 3)
	{
		// header was already sent (multipart/x-mixed-replace with boundary)
	}
    else // headerOpt == 0
    {
		header("Content-Type: multipart/form-data;");  //multipart/x-mixed-replace
    }

    if ($responseOutput->errCode != STATUS_OK) // error occurs
    {
        $mesg = $errorMessage[$responseOutput->errCode];

        if (strlen($responseOutput->outputMsg) > 0 && $responseOutput->errCode == STATUS_TAG_NOT_FOUND) // only if error code = 700
        {
            $mesg .= $responseOutput->outputMsg . ': Not Found';
        }
    }
    else
    {
        $mesg = $responseOutput->outputMsg;
    }

	if($headerOpt != 3)
	{
		header("Content-Length:" . strlen($mesg));
	}
	else
	{
		$mesg .= "\r\n--{$boundary}\r\n"; // boundary tail
	}
		
    echo $mesg;

	exit;
}

function MakeUnpackFormat($_name, $_length, $_maxValue)
{
    $unpackFormat = '';
    for ($index = 0; $index < $_maxValue; ++$index)
        $unpackFormat .= 'A' . $_length . $_name . $index . '/';
    return $unpackFormat;
}

function SetUserInfo($_userConf = NULL)
{
    if ($_userConf == NULL)
    {
        $classInstances = GetClassInstance('user');
        $_userConf = $classInstances['UserConfiguration']->user;
    }
    $digest = '';
    preg_match_all('/(\w+)="([\w\s\~\`\!\@\$\^\*\(\)\_\-\|\{\}\[\]\;\,\.\?\/]+)"/', $_SERVER['PHP_AUTH_DIGEST'], $digest);
    for ($index = 0; $index < count($digest[1]); ++$index)
    {
        if ($digest[1][$index] == 'username')
        {
            $GLOBALS['USERINFO']['name'] = $digest[2][$index];
            break;
        }
    }
    for ($index = 0; $index < MAX_USER; ++$index)
    {
        if ($GLOBALS['USERINFO']['name'] == $_userConf[$index]->dataInfo['Name']['value'])
        {
            $GLOBALS['USERINFO']['pw'] = $_userConf[$index]->dataInfo['Password']['value'];
            $GLOBALS['USERINFO']['level'] = $_userConf[$index]->dataInfo['Level']['value'];
            $GLOBALS['USERINFO']['profile'] = $_userConf[$index]->dataInfo['UserRightProfile']['value'];
            $GLOBALS['USERINFO']['audioin'] = $_userConf[$index]->dataInfo['UserRightAudioIn']['value'];
            $GLOBALS['USERINFO']['audioout'] = $_userConf[$index]->dataInfo['UserRightAudioOut']['value'];
            $GLOBALS['USERINFO']['relay'] = $_userConf[$index]->dataInfo['UserRightRelay']['value'];
            $GLOBALS['USERINFO']['ptz'] = $_userConf[$index]->dataInfo['UserRightPTZ']['value'];
            break;
        }
    }
}

function CheckAdminAccount($_state = TRUE)
{
    $digest = '';
    preg_match_all('/(\w+)="([\w\s\~\`\!\@\$\^\*\(\)\_\-\|\{\}\[\]\;\,\.\?\/]+)"/', $_SERVER['PHP_AUTH_DIGEST'], $digest);
    for ($index = 0; $index < count($digest[1]); ++$index)
    {
        if ($digest[1][$index] == 'username')
        {
            if ($digest[2][$index] != 'admin')
            {
                if ($_state == FALSE)
                {
                    $responseOutput = new ResponseOutput();
                    $responseOutput->errCode = STATUS_NOT_AUTHORIZED;
                    SendResponse($responseOutput);
                }
                echo "<meta http-equiv='refresh' content='0; url=http://" . trim($_SERVER['HTTP_HOST']) . "/index.htm'>";
                exit;
            }
        }
    }
}

function CheckGuestAccount($_state = TRUE)
{
    $digest = '';
    preg_match_all('/(\w+)="([\w\s\~\`\!\@\$\^\*\(\)\_\-\|\{\}\[\]\;\,\.\?\/]+)"/', $_SERVER['PHP_AUTH_DIGEST'], $digest);
    for ($index = 0; $index < count($digest[1]); ++$index)
    {
        if ($digest[1][$index] == 'username')
        {
            if ($digest[2][$index] == 'guest')
            {
                if ($_state)
                {
                    echo "<meta http-equiv='refresh' content='0; url=http://" . trim($_SERVER['HTTP_HOST']) . "/index.htm'>";
                    exit;
                }
                else
                {
                    $responseOutput = new ResponseOutput();
                    $responseOutput->errCode = STATUS_NOT_AUTHORIZED;
                    SendResponse($responseOutput);
                }
            }
        }
    }
}

function MakeDataFormat($_dataInfo)
{
    $dataFormat = '';
    while ($data = current($_dataInfo))
    {
        $dataFormat .= $data['type'] . key($_dataInfo) . "/";
        next($_dataInfo);
    }
    return $dataFormat;
}

function MakePayload($_dataInfo)
{
    $payload = '';
    foreach ($_dataInfo as $data)
    {
        $payload .= pack(strtolower($data['type']), trim($data['value']));
    }
    return $payload;
}

function GetPayloads($_dataClass, $_max)
{
    $payloads = '';
    for ($index = 0; $index < $_max; ++$index)
    {
        $payloads .= $_dataClass[$index]->payload;
    }
    return $payloads;
}

function GetDataInfoLength($_dataInfo)
{
    $totalLength = 0;
    foreach ($_dataInfo as $data)
    {
        $length = (int) substr($data['type'], 1);
        $type = substr($data['type'], 0, 1);
        if ($type == 'i' || $type == 'I')
            $length *= 4;
        $totalLength += $length;
    }
    return $totalLength;
}

function CheckModelName($_param)
{
	switch($_param) {
		case 'CHECK_MD_POLY_SUPPORT':
		{
			if($GLOBALS['M_SUPPORT_PRIVACY_AREA_TYPE'] == PRIVACY_AREA_TYPE_MASK_POLYGON)
				return TRUE; 
		} break;
		case 'CHECK_IV_ENTIREAREA_MODE':
		{
			if($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3) /** need to add condition for old Box/Dome models, when support them */
				return TRUE;
		}
	}
	return FALSE;
}

function CheckAllowedParams($_param)
{
	foreach ($_GET as $name => $value)
	{	
		if(array_search($name, $_param) === FALSE)
		{
			return FALSE;
		}
	}

	return TRUE;
}

function debug($output) {	echo "<pre>";	print_r($output);	echo "</pre>\n";	}

class SocketManager
{

    public $socket;
    public $ipcAddr;
    public $payload;
    public $dataInfo;
	 public	$dataInfo_sdk_app;
    public $ipcAction;
    public $ipcCommand;

    function __construct($_ipcAddr = '')
    {
        $this->ipcAddr = '/tmp/ipc_path';
        if ($_ipcAddr != '')
            $this->ipcAddr = $_ipcAddr;
    }

    function SetHeaderValue($_dataClass)
    {
        $account = (strlen($GLOBALS['USERINFO']['name']) < 1 ? "admin" : $GLOBALS['USERINFO']['name']);
        $this->dataInfo = array('MagicNumber' => array('value' => (int) 0xFFFEFFFE, 'type' => 'i1'),
            'IPCMajorVersion' => array('value' => 0, 'type' => 'c1'),
            'IPCMinorVersion' => array('value' => 6, 'type' => 'c1'),
            'Command' => array('value' => $_dataClass->headerInfo['Command'], 'type' => 'i1'),
            'Action' => array('value' => $_dataClass->headerInfo['Action'], 'type' => 'c1'),
            'Type' => array('value' => 0, 'type' => 'c1'),
            'ErrorCode' => array('value' => 0, 'type' => 'c1'),
            'PayloadLength' => array('value' => strlen($_dataClass->payload), 'type' => 'i1'),
            'PeerIP' => array('value' => '127.0.0.1', 'type' => 'A40'),
            'PeerPort' => array('value' => 80, 'type' => 'i1'),
            'PeerAccount' => array('value' => $account, 'type' => 'A16'),
            'Reserved' => array('value' => 'WEB', 'type' => 'A8'));
        $this->payload = MakePayload($this->dataInfo);
        $this->ipcAction = $_dataClass->headerInfo['Action'];
        $this->ipcCommand = $_dataClass->headerInfo['Command'];
    }

    function CreateSocket()
    {
        $this->socket = @socket_create(AF_UNIX, SOCK_STREAM, 0);
        if ($this->socket < 0)
            return FALSE;
        socket_set_option($this->socket, SOL_SOCKET, SO_SNDTIMEO, array('sec' => 10, 'usec' => 0));
        socket_set_option($this->socket, SOL_SOCKET, SO_RCVTIMEO, array('sec' => 1, 'usec' => 0));

        $retryCnt = 0;
        $sleepVal = array(1, 1, 1);
        do
        {
            $retVal = @socket_connect($this->socket, $this->ipcAddr);
            if ($retVal === FALSE)
            {
                if ($retryCnt > 2)
                {
                    if ($this->socket > 0)
                    {
                        socket_shutdown($this->socket);
                        socket_close($this->socket);
                    }
                    $this->socket = NULL;
                    exit;
                }
                usleep($sleepVal[$retryCnt++] * 1000000); //ms
            }
        }
        while (!$retVal);
        return TRUE;
    }

    function SendPacket($_packet)
    {
        $retVal = @socket_write($this->socket, $_packet, strlen($_packet));
        if ($retVal === FALSE)
        {
            if ($this->socket > 0)
            {
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
        do
        {
            $recvPacket = @socket_read($this->socket, ($_packetSize - $recvPacketSize));   //  receive header (68 byte)
            if ($recvPacket == FALSE || strlen($recvPacket) == 0)
            {
                if ($retryCnt < 10)
                {
                    usleep(1000000); //ms
                    $retryCnt++;
                    if ($recvPacketSize < $_packetSize)
                        continue; // not complete recv data
                    if (socket_last_error($this->socket) == 0)
                        continue; // Success
                    if (socket_last_error($this->socket) == 4)
                        continue; // ??
                    if (socket_last_error($this->socket) == 11)
                        continue; // EAGAIN
                }
                else
                {
                    if ($this->socket > 0)
                    {
                        socket_shutdown($this->socket);
                        socket_close($this->socket);
                    }
                    $this->socket = NULL;
                    exit;
                }
            }
            $totalRecvPacket .= $recvPacket;
            $recvPacketSize = strlen($totalRecvPacket);
        }
        while ($_packetSize != $recvPacketSize);
        return $totalRecvPacket;
    }

    function Connection($_dataClass)
    {
        $responseOutput = new ResponseOutput();

        $this->SetHeaderValue($_dataClass);
        //var_dump($_REQUEST);
        if ($this->socket == NULL && $this->CreateSocket() == FALSE)
        {
            //exit;
            $responseOutput->errCode = STATUS_UNKNOWN_ERROR;
            SendResponse($responseOutput);
        }
        if (!$this->SendPacket($this->payload))
        {
            $responseOutput->errCode = STATUS_UNKNOWN_ERROR;
            SendResponse($responseOutput);
        }
        if ($this->CheckConnect('Send') && !($this->SendPacket($_dataClass->payload)))
        {
            $responseOutput->errCode = STATUS_UNKNOWN_ERROR;
            SendResponse($responseOutput);
        }
        $recvPacket = $this->ReceivePacket(strlen($this->payload));  // Receive Header
        SetData($this->dataInfo, $this->payload, $recvPacket);    // Unpack Header Data

        if ($this->dataInfo['ErrorCode']['value'] != 1)
            $this->CheckErrorCode(); // Check ErrorCode
        if ($this->CheckConnect('Receive'))
        {
            $recvPacket = $this->ReceivePacket($this->dataInfo['PayloadLength']['value']); // Receive Payload
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
        if ($this->socket > 0)
        {
            socket_shutdown($this->socket);
            socket_close($this->socket);
        }
        $this->socket = NULL;
        return $_dataClass;
    }

    function CheckErrorCode()
    {
        global $systemErrorCodeMap;
        $responseOutput = new ResponseOutput();

        if ($this->dataInfo['ErrorCode']['value'] != 1)
        {
            if ($this->ipcCommand == CMD_OPENSDK_APP ) {	
				$responseOutput->errCode = $systemErrorCodeMap[$this->dataInfo['ErrorCode']['value']];
				SendResponse($responseOutput);
			}
			else if ($this->ipcCommand == CMD_PRIVACY_AREA || $this->ipcCommand == CMD_TRACKING_TRACEZONE) return;
			else if ($this->ipcCommand == CGI_CMD_OPENSDK_APP_DEBUG ) {
				$responseOutput->errCode = $systemErrorCodeMap[$this->dataInfo['ErrorCode']['value']];
				SendResponse($responseOutput);
				exit;
			}
            else if ($GLOBALS['M_MAX_RESOLUTION'] == MAX_3_MEGA && $this->ipcCommand == CMD_IMAGE_CONFIGURATION && $this->dataInfo['ErrorCode']['value'] != 2)
            {
            	$responseOutput->errCode = $systemErrorCodeMap[$this->dataInfo['ErrorCode']['value']];
            	SendResponse($responseOutput, 0);
            }

            $responseOutput->errCode = $systemErrorCodeMap[$this->dataInfo['ErrorCode']['value']];
            SendResponse($responseOutput);
        }
        else
        {
            if ($this->ipcAction != ACTION_GET && $this->ipcAction != ACTION_GET_ALL)
            {
                $responseOutput->errCode = STATUS_UNKNOWN_ERROR;
                SendResponse($responseOutput);
            }
        }
    }

    function CheckConnect($_type)
    {
        if ($_type == "Send")
        {
            switch ($this->ipcAction)
            {
                case ACTION_SET: case ACTION_ADD: case ACTION_REMOVE: return TRUE;
                case ACTION_GET:
                    {
                        switch ($this->ipcCommand)
                        {
                            case CMD_IMAGING: case CMD_IMAGE_CONFIGURATION: case CMD_INFORMATION: case CMD_SMARTCODEC: 
							case CMD_SDK_APP_ATTRIBUTES: case CMD_OPENSDK_APP: case CMD_SDK_SEARCH_DETAIL: case CMD_SDK_APP_DATA: case CMD_SDK_TASK_MANAGER: case CMD_SDK_UPDATE_LICENSE: 
							return TRUE;
                        }
                    } break;
                case ACTION_START: case ACTION_MOVE_MASK: case ACTION_ZOOM_THRESHOLD:
                    {
                        switch ($this->ipcCommand)
                        {
                            case CMD_NETWORK_TEST: case CMD_IMAGE_CONFIGURATION: case CMD_TRACKING_TARGETLOCK: case CMD_TRACKING_TRACEZONE: case CMD_OPENSDK_APP: 
							case CMD_MOTORIZED_LENS_SETUP: case CMD_PTZ_INSTANT_AF: case CMD_PRIVACY_AREA:
                                return TRUE;
                        }
                    } break;
                case ACTION_STOP:
                    {
						switch ($this->ipcCommand) {
							case CMD_OPENSDK_APP: 
								return TRUE;
						}
                    } break;
            }
        }
        else if ($_type == "Receive")
        {
            switch ($this->ipcAction)
            {
                case ACTION_START:
                    {
                        switch ($this->ipcCommand)
                        {
                            case CMD_NETWORK_TEST: case CMD_TRACKING_TRACEZONE: case CMD_OPENSDK_APP: 
                                return TRUE;
                        }
                    } break;
                case ACTION_GET: case ACTION_GET_ALL: return TRUE;
				case ACTION_ADD: { 	if ($this->ipcCommand == CMD_OPENSDK_APP) 	return TRUE;	}break;
                case ACTION_MOVE_MASK: { if($this->ipcCommand == CMD_TRACKING_TRACEZONE) return TRUE;}
                
            }
        }
        return FALSE;
    }
}
?>
