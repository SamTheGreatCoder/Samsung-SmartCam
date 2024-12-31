<?php
require_once ('_define.inc');
CheckAdminAccount(FALSE);

define ("CMD_PHOTO_VALUE", 	1017);
define ("CMD_SPEAKER_TEST", 	1018);
define ("MODE_NONE",	0);
define ("MODE_WEP",	1);
define ("MODE_WPA",	2);
define ("MODE_INFRASTRUCTURE", 1);

class SHC_MODEL_FACTORY_TEST
{
	public 	$payload;
	public 	$dataInfo;
	public 	$headerInfo;

	function __construct($_action = ACTION_GET)
	{
		$this->headerInfo	= array( 'Command'=>'', 'Action'=>$_action);
	}

	function PayloadToArray($_payload)
	{
		if ($this->headerInfo['Action'] == ACTION_GET) {
			$dataArray = unpack('i1Value', $_payload);
			$msg = 'level:'.$dataArray['Value']."\r\n";
			ResponseText($msg);
		}
	}
}

if (!isset($_REQUEST['action']) || !isset($_REQUEST['msubmenu']))	ResponseText(FALSE);

$retVal = FALSE;
$factory = new SHC_MODEL_FACTORY_TEST();
if ($_REQUEST['msubmenu'] == 'speaker') {
	if ($_REQUEST['action'] == 'start' || $_REQUEST['action'] == 'stop') {	//http://<ip>/cgi-bin/adv/shc.cgi?msubmenu=speaker&action=start(stop)
		$factory->headerInfo['Command'] = CMD_SPEAKER_TEST;
		if ($_REQUEST['action'] == 'start') {
			$factory->headerInfo['Action'] = 	ACTION_START;
		}
		else {
			$factory->headerInfo['Action'] = 	ACTION_STOP;
		}
		$socketManager = new SocketManager();
		$socketManager->Connection($factory);
		$retVal = TRUE;
	}
}
else if ($_REQUEST['msubmenu'] == 'phototr') {	//http://<ip>/cgi-bin/adv/shc.cgi?msubmenu=phototr&action=view
	if ($_REQUEST['action'] == 'view') {
		$factory->headerInfo['Command'] = CMD_PHOTO_VALUE;
		$factory->headerInfo['Action'] = 	ACTION_GET;
		$socketManager = new SocketManager();
		$socketManager->Connection($factory);
	}

}
else if ($_REQUEST['msubmenu'] == 'wireless') {
	if ($_REQUEST['action'] != 'apply') ResponseText(FALSE);
	if (!isset($_REQUEST['ssid']) || !isset($_REQUEST['mode']) || !isset($_REQUEST['password'])) ResponseText(FALSE);
	require_once ('network_v2.class');
	$socketManager = new SocketManager();

	$networkV2Conf = $socketManager->Connection(new NetworkConfigurationV2());

        $networkV2Conf->interface[1]->dataInfo['Enabled']['value'] = 1;
        $networkV2Conf->interface[1]->SetPayload();
        $networkV2Conf->SetPayload();
        $networkV2Conf->headerInfo['Action'] = ACTION_SET;
        $socketManager->Connection($networkV2Conf);

	$interfacesExtensionConf = $socketManager->Connection(new NetworkInterfacesExtension());

	$interfacesExtensionConf->interfaceExtension[0]->dataInfo['InterfaceToken']['value'] = $networkV2Conf->interface[1]->dataInfo['Token']['value'];

	$interfacesExtensionConf->interfaceExtension[0]->dot11Conf->dataInfo['SSID']['value'] = $_REQUEST['ssid'];
	$interfacesExtensionConf->interfaceExtension[0]->dot11Conf->dataInfo['Mode']['value'] = MODE_INFRASTRUCTURE;
	if ($_REQUEST['mode'] == 'NONE' || $_REQUEST['mode'] == 'none')
	$interfacesExtensionConf->interfaceExtension[0]->dot11Conf->dot11SecurityConf->dataInfo['Mode']['value'] = MODE_NONE;
	if ($_REQUEST['mode'] == 'WEP' || $_REQUEST['mode'] == 'wep')
	$interfacesExtensionConf->interfaceExtension[0]->dot11Conf->dot11SecurityConf->dataInfo['Mode']['value'] = MODE_WEP;
	if ($_REQUEST['mode'] == 'WPA' || $_REQUEST['mode'] == 'wpa')
	$interfacesExtensionConf->interfaceExtension[0]->dot11Conf->dot11SecurityConf->dataInfo['Mode']['value'] = MODE_WPA;

	$interfacesExtensionConf->interfaceExtension[0]->dot11Conf->dot11SecurityConf->dataInfo['PSK']['value'] = $_REQUEST['password'];
	$interfacesExtensionConf->interfaceExtension[0]->dot11Conf->dot11SecurityConf->payload = MakePayload($interfacesExtensionConf->interfaceExtension[0]->dot11Conf->dot11SecurityConf->dataInfo);
	$interfacesExtensionConf->interfaceExtension[0]->dot11Conf->SetPayload();
	$interfacesExtensionConf->interfaceExtension[0]->SetPayload();
	$interfacesExtensionConf->SetPayload();
	$interfacesExtensionConf->headerInfo['Action'] = ACTION_SET;
	$socketManager->Connection($interfacesExtensionConf);
	$retVal = TRUE;
}
else if ($_REQUEST['msubmenu'] == 'network') {
	if ($_REQUEST['action'] != 'off' && $_REQUEST['action'] != 'on') ResponseText(FALSE);
	require_once ('network_v2.class');
	$socketManager = new SocketManager();
	$networkV2Conf = $socketManager->Connection(new NetworkConfigurationV2());

	$networkV2Conf->interface[0]->dataInfo['Enabled']['value'] = ($_REQUEST['action'] == 'off' ? 0 : 1); // wired off -> wireless on , wired on -> wireless off

        $networkV2Conf->interface[1]->dataInfo['Enabled']['value'] = ($_REQUEST['action'] == 'on' ? 0 : 1);

	$networkV2Conf->interface[0]->SetPayload();
	$networkV2Conf->interface[1]->SetPayload();
	$networkV2Conf->SetPayload();
	$networkV2Conf->headerInfo['Action'] = ACTION_SET;
	$socketManager->Connection($networkV2Conf);
	$retVal = TRUE;
}
else if ($_REQUEST['msubmenu'] == 'wireless_status') {
	if ($_REQUEST['action'] != 'view') ResponseText(FALSE);
	require_once ('network_v2.class');
	$socketManager = new SocketManager();
	$networkV2Conf = $socketManager->Connection(new NetworkConfigurationV2());

	$dot11Status = new Dot11Status();
	$dot11Status->headerInfo['Action'] = ACTION_GET;
	$dot11Status->payload = pack('a64', $networkV2Conf->interface[1]->dataInfo['Token']['value']);
	$socketManager->Connection($dot11Status);
}
ResponseText($retVal);
?>
