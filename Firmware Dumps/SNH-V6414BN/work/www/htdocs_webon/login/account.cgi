<?php
require_once ('../cgi-bin/adv/_define.inc');

$classInstances= GetClassInstance('user');
$securityConf	= $classInstances['UserConfiguration'];

// 암호변경 요청 
function ChangePwd()
{
	if (!isset($_REQUEST['name']) || !isset($_REQUEST['pass']))	{
		return FALSE;
	}

	foreach($_REQUEST as $name=>$value)
	{
		switch($name)
		{
			case 'name':	
			case 'pass':
				{
					// DEV_S1PWRESTORE
					//if (strlen(urldecode($value)) > 16) {
					$value = str_replace('\\\\', '\\', $value);
					$value = str_replace('\\\'', '\'', $value);
					$value = str_replace("\\\"", "\"", $value);
					if (strlen($value) > 16) {
						return FALSE;
					}
				}
				break;
		}
	}

	$classInstances= GetClassInstance('user');

	$isMatch = FALSE;

	if(CheckModelName('All1001')) $max_user = MAX_USER_10;
	else $max_user = MAX_USER;

	for ($index=0; $index<($max_user-1); ++$index)
	{
		$userConf = $classInstances['UserConfiguration']->user[$index];
		if ($userConf->dataInfo['Name']['value'] == $_REQUEST['name'])
		{
			// DEV_S1PWRESTORE
			//$userConf->dataInfo['Password']['value'] = urldecode($_REQUEST['pass']);
			$pass = $_REQUEST['pass'];
			$pass = str_replace('\\\\', '\\', $pass);
			$pass = str_replace('\\\'', '\'', $pass);
			$pass = str_replace("\\\"", "\"", $pass);
			$userConf->dataInfo['Password']['value'] = $pass;

			if (isset($_REQUEST['enabled']))
			{
				if ($_REQUEST['enabled'] < 0 || $_REQUEST['enabled'] > 1) return FALSE;
				$userConf->dataInfo['Enabled']['value'] = $_REQUEST['enabled'];
			}
			// DEV_S1PWRESTORE
			//$userConf->payload = MakePayload($userConf->dataInfo);
			$userConf->payload = MakePayloadNoTrim($userConf->dataInfo);

			$isMatch = TRUE;
			break;
		}
	}

	if ($isMatch == FALSE) ResponseText(FALSE);

	$classInstances['UserConfiguration']->headerInfo['Action'] = ACTION_SET;
	$classInstances['UserConfiguration']->SetPayload();
	$GLOBALS['SOCKET_MANAGER']->Connection($classInstances['UserConfiguration']);
	$GLOBALS['SOCKET_MANAGER']->CheckErrorCode();

	return TRUE;
}


///////////////////////////////////////////////
// CGI Command
///////////////////////////////////////////////
switch(@$_REQUEST['msubmenu'])
{
	case 'user':
		{
			if 	($_REQUEST['action'] == 'chgpwd')	 
			{ 
// 				CheckAdminAccount(FALSE);	 
				ResponseText(ChangePwd()); 
			}
			else if ($_REQUEST['action'] == 'isenabled')	// admin account
			{
				header("Content-Type: text/plain");
				echo $securityConf->user[0]->dataInfo['Enabled']['value'];
				exit;
			}
		}
		break;
}

ResponseText(FALSE);
?>

