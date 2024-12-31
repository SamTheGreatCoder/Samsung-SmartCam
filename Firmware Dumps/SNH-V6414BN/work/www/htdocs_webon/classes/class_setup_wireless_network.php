<?php
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";
define("OFF_WLAN", 				909);
define("OFF_NETWORK_CHANGED", 	11709);

$pageData = explode(";", $_POST["data"]); //action
if($pageData[0] == "SCAN"){	
	ini_set("max_execution_time", 3);
	$result = requestToCamera(getNewCmd(CMD_WIRELESS_SCANNING), ACTION_GET, TYPE_REQUEST, null);	
	if($result[0] == "OK"){
		$list = "";
		if($result[1] != null && count($result[1]) >= 88){
			$count = byte2int($result[1], 0);
			$level = 0;
			$apName = "";
			for($i=0,$j=4; $i<$count; $i++,$j+=84){
				$apName = rawurlencode(byte2str($result[1], $j, 64)) . ",";
				$list .= $apName;
				$list .= byte2str($result[1], $j+64, 16) . ",";
				$level = byte2int($result[1], $j+80);
				if($level == 0){
					$list .= "0";
				}else if(($level >= 1) && ($level <= 20)){
					$list .= "1";
				}else if(($level >= 21) && ($level <= 40)){
					$list .= "2";
				}else if(($level >= 41) && ($level <= 60)){
					$list .= "3";
				}else if(($level >= 61) && ($level <= 80)){
					$list .= "4";
				}else{
					$list .= "5";
				}
				if($i < ($count - 1)){
					$list .= ";";
				}
			}
		}
		if($list == ""){
			echo "OK; ";
		}else{
			echo "OK;". $list;
		}
	}else{
		echo "NOK;" . $result[1];
	}
}else if($pageData[0] == "SET"){  //0:action, 1:recvData, 2:use, 3:type, 4:ssid, 5:psk
	ini_set("max_execution_time", 20);
	$sendData = explode(",", $pageData[1]);
	$sendData[OFF_WLAN+64] = intval($pageData[2]);
	if(trim($pageData[3]) != ""){
		str2byte($sendData, $pageData[3], OFF_WLAN+343, 16);
	}
	if(trim($pageData[4]) != ""){
		str2byte($sendData, $pageData[4], OFF_WLAN+359, 64);
	}
	if(trim($pageData[5]) != ""){
		str2byte($sendData, $pageData[5], OFF_WLAN+423, 128);
	}
	$sendData[OFF_NETWORK_CHANGED] = 0; //20120207_lcy added change field

	$result = requestToCamera(CMD_NETWORK_CONFIGURATION, ACTION_SET, TYPE_REQUEST, $sendData);
	if($result[0] == "OK"){
		echo "OK";
	}else{
		echo "NOK;" . $result[1];
	}
}else if($pageData[0] == "IPCV0.7"){
	$sendData = explode(",", $pageData[1]);
	$result = requestToCamera(getNewCmd(CMD_NETWORK_CONFIGURATION), ACTION_SET, TYPE_REQUEST, $sendData);
	if($result[0] == "OK"){
		echo "OK";
	}else{
		echo "NOK;" . $result[1];
	}
	$sendData = explode(",", $pageData[2]);
	$result = requestToCamera(getNewCmd(CMD_NETWORK_IF_EXTENSION), ACTION_SET, TYPE_REQUEST, $sendData);
	if($result[0] == "OK"){
		echo "OK";
	}else{
		echo "NOK;" . $result[1];
	}
}

?>