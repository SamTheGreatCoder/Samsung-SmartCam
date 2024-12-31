<?php
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";
session_start();

$pageData = explode(";", $_POST["data"]);
if($pageData[0] == "CHECK"){
	$result = requestToCamera(CMD_USER, ACTION_GET_ALL, TYPE_REQUEST, null);
	if($result[0] == "OK" && $result[1] != null){
		$recvData = $result[1];
		$privateKey = byte2str($recvData, 17, 16);
		if($privateKey == ""){
			echo "NOKEY";
		}else{
			if($pageData[1] == $privateKey){
				$_SESSION["LOGIN_STATUS"] = "TRUE";
				$_SESSION["PRIVATE_KEY"] = $pageData[1];
				echo "OK";
			}else{
				echo "NOK;Private key is wrong.";
			}
		}
	}else{
		echo "NOK;" . $result[1];
	}
}else if($pageData[0] == "SET"){
	$result = requestToCamera(CMD_USER, ACTION_GET_ALL, TYPE_REQUEST, null);
	if($result[0] == "OK" && $result[1] != null){
		$recvData = $result[1];
		//if(strcmp("SEC-6410", CAMERA_MODEL) != 0){
		if(CheckModelName_SNH('WR15')) {
			$sendData = array_slice($recvData, 0, 40);
		}else{
			$sendData = $recvData;
		}
		$currentKey = byte2str($sendData, 17, 16);
		if($pageData[1] == $currentKey){
			str2byte($sendData, $pageData[2], 17, 16);
			requestToCamera(CMD_USER, ACTION_SET, TYPE_REQUEST, $sendData);
			$_SESSION["PRIVATE_KEY"] = $pageData[2];
			echo "OK";
		}else{
			echo "NOK;Incorrect private key";
		}
	}else{
		echo "NOK;" . $result[1];
	}
}else if($pageData[0] == "NEW"){
	$result = requestToCamera(CMD_USER, ACTION_GET_ALL, TYPE_REQUEST, null);
	if($result[0] == "OK" && $result[1] != null){
		$recvData = $result[1];
		//if(strcmp("SEC-6410", CAMERA_MODEL) != 0){
		if(CheckModelName_SNH('WR15')) {
			$sendData = array_slice($recvData, 0, 40);
		}else{
			$sendData = $recvData;
		}

		str2byte($sendData, $pageData[1], 17, 16);
		requestToCamera(CMD_USER, ACTION_SET, TYPE_REQUEST, $sendData);
		$_SESSION["PRIVATE_KEY"] = $pageData[1];
		echo "OK";
	}else{
		echo "NOK;" . $result[1];
	}
}

?>