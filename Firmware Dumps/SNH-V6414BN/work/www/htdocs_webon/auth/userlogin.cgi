<?php
require_once ('../cgi-bin/adv/_define.inc');

switch(@$_REQUEST['msubmenu'])
{
	case 'user':
	{
		if ($_REQUEST['action'] == 'userlogin')
		{
			//$pass = urldecode($_REQUEST['pass']);
			$pass = $_REQUEST['pass'];
			$pass = str_replace('\\\\', '\\', $pass );
			$pass = str_replace('\\\'', '\'', $pass );
			$pass = str_replace("\\\"", "\"", $pass );

			ResponseLoginResult(UserLogin($_REQUEST['id'], $_REQUEST['lastAuthTime'], '', 1, $pass));
		}
	}
		break;
}

ResponseLoginResult(FALSE);
?>

