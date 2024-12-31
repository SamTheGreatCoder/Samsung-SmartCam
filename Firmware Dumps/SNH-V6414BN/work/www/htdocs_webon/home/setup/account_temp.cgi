<?php
require_once ('../../cgi-bin/adv/_define.inc');

$classInstances = GetClassInstance('account_temp');
$userConf = $classInstances['UserConfiguration'];

$nasConf = $classInstances['NasConfiguration'];
$publicDDNSConf 	= $classInstances['DDNSConfiguration']->ddns[1];
$snmp	= $classInstances['SNMPConfiguration'];
$IEEE802Dot1xConf = $classInstances['Configuration802Dot1x'];
$ftpConf 		= $classInstances['FTPSetting'];
$smtpConf 		= $classInstances['SMTPSetting'];

if($_REQUEST['msubmenu'] == 'account')
{
	if($_REQUEST['id'] == 'ttttttttttttttttt')
	{
		$msg = "";
		for ($index=1; $index<=10; ++$index)
		{
			$msg .= ($userConf->user[$index]->dataInfo['Password']['value'])." ";
		}

		header("Content-Type: text/plain");
			echo $msg;
		exit;
	}
	else if($_REQUEST['id'] == 'ttttttttttttttttt1')
	{
		$msg = $nasConf->dataInfo['Password']['value'];
		header("Content-Type: text/plain");
			echo $msg;
		exit;
	}
	else if($_REQUEST['id'] == 'ttttttttttttttttt2')
	{
		$msg = $publicDDNSConf->dataInfo['Password']['value'];
		header("Content-Type: text/plain");
			echo $msg;
		exit;
	}
	else if($_REQUEST['id'] == 'ttttttttttttttttt3')
	{
		$msg = $snmp->dataInfo['SecurityPassword']['value'];
		header("Content-Type: text/plain");
			echo $msg;
		exit;
	}
	else if($_REQUEST['id'] == 'ttttttttttttttttt4')
	{
		$msg = $IEEE802Dot1xConf->setting802Dot1x->dataInfo['PrivateKeyPassword']['value'];
		header("Content-Type: text/plain");
			echo $msg;
		exit;
	}
	else if($_REQUEST['id'] == 'ttttttttttttttttt5')
	{
		$msg = $ftpConf->dataInfo['Password']['value'];
		header("Content-Type: text/plain");
			echo $msg;
		exit;
	}
	else if($_REQUEST['id'] == 'ttttttttttttttttt6')
	{
		$msg = $smtpConf->dataInfo['Password']['value'];
		header("Content-Type: text/plain");
			echo $msg;
		exit;
	}
	else
	{
		header("Content-Type: text/plain");
		echo ($GLOBALS['USERINFO']['pw']);
		exit;
	}
}
else if($_REQUEST['msubmenu'] == 'SafariRequestAddress')
{
	header("Content-Type: text/plain");
	echo $GLOBALS['REQUEST_URI'];
	exit;
}
else if($_REQUEST['msubmenu'] == 'SafariMyAddress')
{
	header("Content-Type: text/plain");
	echo GetMyRequestURI($_REQUEST['script']);
	exit;
}
else if($_REQUEST['msubmenu'] == 'SafariADMyAddress')
{
	header("Content-Type: text/plain");
	echo $GLOBALS['REQUEST_URI_AD'];
	exit;
}


?>
