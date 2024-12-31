<?php
//-------------------------------------------------------------------------------------------------------------
/* Structure - tYoutubeConfiguration
	Enabled			bool		0
	Status			Byte		1
	ID				char[128]	2 ~ 129
	PW				char[128]	130 ~ 257
	Private			Byte		258
	PreRecTime		int			259 ~ 262
	RecTime			int			263 ~ 266
	Reserved		char[64]	267 ~ 330
*/

require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";	

$pageData = explode(";", $_POST["data"]); //0:recvData, 1:Enabled, 2:ID, 3:PWD, 4:Access, 5:Record Time
$sendData = explode(",", $pageData[0]);

$sendData[0] = intval($pageData[1]);
str2byte($sendData, $pageData[2], 2, 128);
str2byte($sendData, $pageData[3], 130, 128);
$sendData[258] = intval($pageData[4]);
int2byte($sendData, ((intval($pageData[5]) + 1) * 10), 263);

$result = requestToCamera(getNewCmd(CMD_YOUTUBE_CONFIGURATION), ACTION_SET, TYPE_REQUEST, $sendData);
if($result[0] == "OK"){
	echo "OK";
}else{
	echo "NOK;" . $result[1];
}
	
?>