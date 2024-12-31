<?php
//-------------------------------------------------------------------------------------------------------------
/* Structure - tPicasaConfiguration
	Enabled				bool		0
	Status				Byte		1
	ID					char[128]	2 ~ 129
	PW					char[128]	130 ~ 257
	AlbumTitle			char[128]	258 ~ 385
	AlbumSummary		char[128]	386 ~ 513
	Private				Byte		514
	Reserved			char[64]	515 ~ 578
*/

require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";	

$pageData = explode(";", $_POST["data"]); //0:recvData, 1:Enabled, 2:ID, 3:PWD, 4:Private
$sendData = explode(",", $pageData[0]);

$sendData[0] = intval($pageData[1]);
str2byte($sendData, $pageData[2], 2, 128);
str2byte($sendData, $pageData[3], 130, 128);
$sendData[514] = intval($pageData[4]);

$result = requestToCamera(getNewCmd(CMD_PICASA_CONFIGURATION), ACTION_SET, TYPE_REQUEST, $sendData);
if($result[0] == "OK"){
	echo "OK";
}else{
	echo "NOK;" . $result[1];
}

?>