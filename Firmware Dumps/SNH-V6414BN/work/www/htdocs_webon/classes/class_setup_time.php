<?php
//-------------------------------------------------------------------------------------------------------------
/*	Structure - tSystemDateTime
	Type				byte 		0
	DaylightSavings		bool		1
	TimeZone			char[64]	2 ~ 65
	UTC_Year			int			66 ~ 69
	UTC_Month			int			70 ~ 73
	UTC_Day				int			74 ~ 77
	UTC_Hour			int			78 ~ 81
	UTC_Minute			int			82 ~ 85
	UTC_Second			int			86 ~ 89
	Local_Year			int			90 ~ 93
	Local_Month			int			94 ~ 97
	Local_Day			int			98 ~ 101
	Local_Hour			int			102 ~ 105
	Local_Minute		int			106 ~ 109
	Local_Second		int			110 ~ 113
	Msec				int			114 ~ 117
	CurrTimezoneIdx		byte		118
*/
	
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";	

$pageData = explode(";", $_POST["data"]); //0:recvData, 1:zone, 2:zone_name, 3:summer
$sendData = explode(",", $pageData[0]);

$sendData[118] = intval($pageData[1]);
str2byte($sendData, $pageData[2], 2, 64);
$sendData[1] = intval($pageData[3]);

$result = requestToCamera(CMD_DATETIME, ACTION_SET, TYPE_REQUEST, $sendData);
if($result[0] != "OK"){
	echo "NOK;" . $result[1];
	return;
}

if($pageData[4] != null){ // 4: timeOSD data 5: enable/disable 6:platform type
	$sendData = explode(",", $pageData[4]);
	if($pageData[6] == 'WR3.0'){
		$sendData[362] = intval($pageData[5]);           // enable
		$sendData[363] = 0;           // date format
		int2byte($sendData, 1, 364);  // date pos x
		int2byte($sendData, 1, 368);  // data pos y
		$sendData[399] = 0;           // display weekand
		$sendData[402] = 0;           // osd size
	} else {
		$sendData[373] = intval($pageData[5]);           // enable
		$sendData[374] = 0;           // date format
		int2byte($sendData, 1, 375);  // date pos x
		int2byte($sendData, 1, 379);  // data pos y
		$sendData[410] = 0;           // display weekand
		$sendData[413] = 0;           // osd size
	}
	$sendData[$sendData.length] = 0;

	$result = requestToCamera(CMD_IMAGE_CONFIGURATION, ACTION_SET, TYPE_REQUEST, $sendData);
	if($result[0] == "OK"){
		echo "OK";
	} else {
		echo "NOK;" . $result[1];
	}
}
?>