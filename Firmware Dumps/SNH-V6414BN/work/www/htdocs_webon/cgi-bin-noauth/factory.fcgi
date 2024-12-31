<?php
require_once ('../cgi-bin/adv/_define.inc');
CheckAdminAccount(FALSE);

//프리셋 모션기능 없음 -> 있을 가능성있음(다른 모델에)
//알람출력 제어기능 삭제됨

$setFactoryClearCmd = "set_setup.security.factory_clear";

$apiCmd = $_GET["api"];

if($apiCmd == NULL){
	ResponseText(FALSE);
}
else{
	switch ($apiCmd){
		case $setFactoryClearCmd:
			SetFactoryClear();
			break;
		default:
			ResponseText(FALSE);
			break;
	}
}

function SetFactoryClear(){
	
	$classInstances= GetClassInstance('factoryclear');
	header("Content-Type: text/plain");
	$authtoken = $_GET['authtoken'];
	$authpass = $_GET['authpass'];

	if(strlen($authpass) > 16){
		echo "result="."false"."\r\n";		
		echo "authuser=".$classInstances['Factoryclear']->dataInfo['AuthUser']['value']."\r\n";
		echo "macaddr=".$classInstances['Factoryclear']->dataInfo['MacAddr']['value']."\r\n";
		return;
	}
	
	$classInstances['Factoryclear']->dataInfo['AuthToken']['value'] = $authtoken;
	$classInstances['Factoryclear']->dataInfo['AuthPass']['value'] = $authpass;
	$classInstances['Factoryclear']->headerInfo['Action'] = ACTION_SET;
	$classInstances['Factoryclear']->SetPayload();
	$GLOBALS['SOCKET_MANAGER']->Connection($classInstances['Factoryclear']);
	if ($GLOBALS['SOCKET_MANAGER']->dataInfo['ErrorCode']['value'] != 1) {
		echo "result="."false"."\r\n";		
	}
	else {
		echo "result="."true"."\r\n";
	}
	echo "authuser=".$classInstances['Factoryclear']->dataInfo['AuthUser']['value']."\r\n";
	echo "macaddr=".$classInstances['Factoryclear']->dataInfo['MacAddr']['value']."\r\n";
}

?>