<?php	
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";
define("OFF_EMAIL"			, 	3660);
define("OFF_EMAIL_LIST"		, 	128);
define("OFF_EMAIL_SERVER"	, 	1408);
define("OFF_NETWORK_CHANGED", 	11709);

$pageData = explode(";", $_POST["data"]); //0:recvData, 1:Server, 2:Port, 3:Needed, 4:User Name, 5:Password, 6:Use SSL, 7:SSL Port, 8:Members, 9:Sender

if($pageData[0] == "IPCV0.6"){	
	$sendData = explode(",", $pageData[1]);
	str2byte($sendData, $pageData[10], OFF_EMAIL, 128);									//Sender
	str2byte($sendData, $pageData[2], (OFF_EMAIL + OFF_EMAIL_SERVER), 128);				//Server
	int2byte($sendData, intval($pageData[3]), (OFF_EMAIL + OFF_EMAIL_SERVER + 128));	//Port
	$sendData[OFF_EMAIL + OFF_EMAIL_SERVER + 132] = intval($pageData[4]);				//Needed
	str2byte($sendData, $pageData[5], (OFF_EMAIL + OFF_EMAIL_SERVER + 133), 64);		//User Name
	str2byte($sendData, $pageData[6], (OFF_EMAIL + OFF_EMAIL_SERVER + 197), 64);		//Password
	$sendData[OFF_EMAIL + 2949] = intval($pageData[7]);									//Use SSL
	int2byte($sendData, intval($pageData[8]), (OFF_EMAIL + 2950));						//SSL Port
	for($i=0, $j=(OFF_EMAIL + OFF_EMAIL_LIST); $i<10; $i++, $j+=128){					//Members
		str2byte($sendData, "", $j, 128);
	}
	
	$memList = explode(",", $pageData[9]);
	for($i=0, $j=(OFF_EMAIL + OFF_EMAIL_LIST); $i<count($memList); $i++, $j+=128){
		if($memList[$i] != null && trim($memList[$i]) != ""){
			str2byte($sendData, $memList[$i], $j, 128);
		}
	}
	$sendData[OFF_NETWORK_CHANGED] = 1; //20120207_lcy added change field
	
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
		return;
	}
	$sendData=null;
	$memList = explode(",", $pageData[2]);
	int2byte($sendData, 5, 0);
	for($i=1, $j=4; $i<=5; $i++){
		if($memList[$i] != null && trim($memList[$i]) != ""){
			str2byte($sendData, $memList[$i], $j, 128);
		}else{
			str2byte($sendData, "", $j, 128);
		}
		$j+=128;
	}
	$result = requestToCamera(CMD_SMTP_EXT_CONFIG, ACTION_SET, TYPE_REQUEST, $sendData);
	if($result[0] == "OK"){
		echo "OK";
	}else{
		echo "NOK;" . $result[1];
	}
}


?>