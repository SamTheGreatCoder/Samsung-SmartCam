<?php
require_once ('../cgi-bin/adv/_define.inc');

$classInstances= GetClassInstance('time_password');
$time_pw	=	$classInstances['time_password'];
$time_pw->headerInfo["Action"] = ACTION_SET;
$time_pw->SetPayload();	
$socketManager = new SocketManager();
$socketManager->Connection($time_pw);
ResponseText(True);
?>

