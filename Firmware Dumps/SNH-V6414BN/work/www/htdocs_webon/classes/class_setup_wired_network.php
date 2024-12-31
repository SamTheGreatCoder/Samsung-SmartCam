<?php	
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";	
define("OFF_DNS", 				65);
define("OFF_NETWORK", 			230);
define("OFF_GATEWAY", 			1588);
define("OFF_NETWORK_CHANGED", 	11709);

$pageData = explode(";", $_POST["data"]); //0:recvData, 1:type, 2:IP, 3:Subnet, 4:Gateway, 5:DNS1, 6:DNS2

if($pageData[0] == "IPCV0.6"){
	$sendData = explode(",", $pageData[1]);
	
	$sendData[OFF_NETWORK+84] = intval($pageData[2]);
	if($pageData[2] == "0"){
		str2byte($sendData, $pageData[6], OFF_DNS+2, 40);		//DNS 1
		str2byte($sendData, $pageData[7], OFF_DNS+43, 40);		//DNS 2
		str2byte($sendData, $pageData[3], OFF_NETWORK+85, 16);	//IP Address
		str2byte($sendData, $pageData[5], OFF_GATEWAY, 16);		//Gateway
	}
	$sendData[OFF_NETWORK_CHANGED] = 0; //20120207_lcy added change field
	
	$result = requestToCamera(CMD_NETWORK_CONFIGURATION, ACTION_SET, TYPE_REQUEST, $sendData, true);
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
}




?>