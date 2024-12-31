<?php
//-------------------------------------------------------------------------------------------------------------
/* Structure - tTwitterConfiguration
	Enabled					bool		0
	Status					Byte		1
	Reserved				char[64]	2 ~ 65
	
	AuthURL					char[128]	0 ~ 127
	
	PinCode					char[64]	0 ~ 63
*/

require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";

$pageData = explode(";", $_POST["data"]); //0:action, 1:data
if($pageData[0] == "GET"){
	$result = requestToCamera(getNewCmd(CMD_TWITTER_AUTH_URL), ACTION_GET, TYPE_REQUEST, null);
	if($result[0] == "OK"){
		echo "OK;" . byte2str($result[1], 0, 128);
	}else{
		echo "NOK;" . $result[1];
	}
}else if($pageData[0] == "SET"){
	$sendData = array();
	str2byte($sendData, $pageData[1], 0, 64);
	$result = requestToCamera(getNewCmd(CMD_TWITTER_ACCESS_TOKEN), ACTION_SET, TYPE_REQUEST, $sendData);
	if($result[0] == "OK"){
		echo "OK";
	}else{
		echo "NOK;" . $result[1];
	}
}else if($pageData[0] == "LIVE"){
	$sendData = explode(",", $pageData[1]);
	$sendData[0] = intval($pageData[2]);
	$result = requestToCamera(getNewCmd(CMD_TWITTER_CONFIGURATION), ACTION_SET, TYPE_REQUEST, $sendData);
	if($result[0] == "OK"){
		echo "OK";
	}else{
		echo "NOK;" . $result[1];
	}
}

?>