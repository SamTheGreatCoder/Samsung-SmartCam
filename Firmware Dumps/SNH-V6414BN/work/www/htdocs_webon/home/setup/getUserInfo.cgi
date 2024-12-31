<?php
require_once ('../../cgi-bin/adv/_define.inc');

require_once ('../../cgi-bin/adv/info.class');
$classInstances = array();
	$GLOBALS['SOCKET_MANAGER'] = new SocketManager();
$classInstances['Information'] = $GLOBALS['SOCKET_MANAGER']->Connection(new Information());
$data = '<?xml version="1.0" encoding="utf-8" ?>'."\n";
	$data .= '<GetUserInfo>'."\n";
	$data .= '<MEGAMODE>'.$GLOBALS['MEGAMODE'].'</MEGAMODE>'."\n";
	$data .= '<VIDEOTYPE>'.$GLOBALS['VIDEOTYPE'].'</VIDEOTYPE>'."\n";
	$data .= '<USERNAME>'.$GLOBALS['USERINFO']['encname'].'</USERNAME>'."\n";
	$data .= '<PWD>'.$GLOBALS['USERINFO']['encpw'].'</PWD>'."\n";
	$data .= '<LEVEL>'.$GLOBALS['USERINFO']['level'].'</LEVEL>'."\n";
	$data .= '<PROFILE>'.$GLOBALS['USERINFO']['profile'].'</PROFILE>'."\n";
	$data .= '<DEVICEPORT>'.$classInstances['Information']->dataInfo['DevicePort']['value'].'</DEVICEPORT>'."\n";
	$data .= '<AUDIOIN>'.$GLOBALS['USERINFO']['audioin'].'</AUDIOIN>'."\n";
	$data .= '<RELAY>'.$GLOBALS['USERINFO']['relay'].'</RELAY>'."\n";
	$data .= '<PTZ>'.$GLOBALS['USERINFO']['ptz'].'</PTZ>'."\n";
	$data .= '<LANGINDEX>'.$GLOBALS['LANGINDEX'].'</LANGINDEX>'."\n";
	$data .= '<LANGSTRING>'.$GLOBALS['LANGSTRING'].'</LANGSTRING>'."\n";
	$data .= '<JPEGUUID>'.$GLOBALS['JPEGUUID'].'</JPEGUUID>'."\n";
	$data .= '<SNAPUUID>'.$GLOBALS['SNAPUUID'].'</SNAPUUID>'."\n";
$data .= '</GetUserInfo>';

echo $data;
exit;
?>