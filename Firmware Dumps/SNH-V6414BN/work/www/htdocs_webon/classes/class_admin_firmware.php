<?php	
//-------------------------------------------------------------------------------------------------------------
/* Structure - tDeviceInformation
	Manufacturer		char[64]	0 ~ 63
	Model				char[32]	64 ~ 95
	FirmwareVersion		char[16]	96 ~ 111
	ModuleVersion		char[16]	112 ~ 127
	PTZVersion			char[16]	128 ~ 143
	LastUpdate			char[32]	144 ~ 175
	SerialNumber		char[32]	176 ~ 207
	HardwareId			char[16]	208 ~ 223
	DeviceName			char[32]	224 ~ 255
	Location			char[64]
	Description			char[64]
	Memo				char[128]
	Language			byte
	VideoType			int
	IfBoardVersion		char[16]
*/
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";
session_start();

$pageData = explode(";", $_POST["data"]); //0:action, 1:recvData, 2:lang
if($pageData[0] == "LANGUAGE"){
	$sendData = explode(",", $pageData[1]);
	$sendData[512] = intval($pageData[2]);
	$result = requestToCamera(CMD_SYSTEM_CONFIGURATION, ACTION_SET, TYPE_REQUEST, $sendData);
	if($result[0] == "OK"){
		$_SESSION["LANGUAGE"] = $pageData[2];
		echo "OK";
	}else{
		echo "NOK;" . $result[1];
	}
}else{
	$sendData = array();
	for($i=0; $i<256; $i++){
		$sendData[$i] = 0x00;
	}
	$result = requestToCamera(getNewCmd(CMD_FIRMWARE_UPGRADE), ACTION_SET, TYPE_REQUEST, $sendData);
}
?>