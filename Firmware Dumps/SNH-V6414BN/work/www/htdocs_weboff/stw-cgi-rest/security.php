<?php
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";

function submenu_users()
{
	if($_SERVER['REQUEST_METHOD'] != "GET" && $_SERVER['REQUEST_METHOD'] != "PUT")
	{
		header("HTTP/1.1 405 Method Not Allowed");
		return;
	}

	$result_users = requestToCamera(CMD_USER, ACTION_GET_ALL, TYPE_REQUEST, null);
	if($result_users[0] == "OK")
	{
		global $CLASS_PATH;
		require_once($CLASS_PATH . "user.class");

		$users['UserConfiguration'] = new UserConfiguration();
		$users['UserConfiguration']->PayloadToArray($result_users[2]);
	}
	else
	{
		header("HTTP/1.1 500 Internal Server Error");
		return;
	}

	if($_SERVER['REQUEST_METHOD'] == "GET")
	{
		$pwdBlock = '';
		for($i = 0 ; $i < strlen($users['UserConfiguration']->user[0]->dataInfo['Password']['value']) ; $i++)
		{
			$pwdBlock .= '*';
		}
		
		$data = array("Users.0.UserID"=>$users['UserConfiguration']->user[0]->dataInfo['Name']['value'], 
						"Users.0.Enable"=>(bool)$users['UserConfiguration']->user[0]->dataInfo['Enabled']['value'], 
						"Users.0.VideoProfileAccess"=>(bool)$users['UserConfiguration']->user[0]->dataInfo['UserRightProfile']['value'], 
						"Users.0.AudioInAccess"=>(bool)$users['UserConfiguration']->user[0]->dataInfo['UserRightAudioIn']['value'], 
						"Users.0.AudioOutAccess"=>(bool)$users['UserConfiguration']->user[0]->dataInfo['UserRightAudioOut']['value'], 
						"Users.0.Password"=>$pwdBlock); //$users['UserConfiguration']->user[0]->dataInfo['Password']['value']

		header("Content-type: application/json");
		echo json_encode($data);
	}
	else if($_SERVER['REQUEST_METHOD'] == "PUT")
	{
		$put_data = json_decode(file_get_contents("php://input"));

		if(!isset($put_data->{'Index'}) || !isset($put_data->{'UserID'}) || !isset($put_data->{'Password'}))
		{
			header("HTTP/1.1 400 Bad Request");
			return;
		}

		foreach ($put_data as $name => $value)
		{
			switch ($name)
            {
            	case 'Index':
            		{
            			if($value != 0)
						{
							header("HTTP/1.1 400 Bad Request");
							return;
						}
            		}
            		break;
            	case 'UserID':
            		{
            			if($value != "admin")
						{
							header("HTTP/1.1 400 Bad Request");
							return;
						}
            		}
            		break;
            	case 'Password':
            		{
            			if(strlen($value) > 15)
						{
							header("HTTP/1.1 400 Bad Request");
							return;
						}
						$users['UserConfiguration']->user[0]->dataInfo['Password']['value'] = $value;
            		}
            		break;
            	default:
	            	{
	            		header("HTTP/1.1 400 Bad Request");
	            		return;
	            	}
	            	break;
            }
		}

		$users['UserConfiguration']->user[0]->payload = MakePayload($users['UserConfiguration']->user[0]->dataInfo);
		$users['UserConfiguration']->SetPayload();
		
		$result = requestToCamera(CMD_USER, ACTION_SET, TYPE_REQUEST, unpack('c*', $users['UserConfiguration']->payload));
		if($result[0] != "OK")
		{
			header("HTTP/1.1 500 Internal Server Error");
		}
	}
}

function submenu_ssl()
{
	if($_SERVER['REQUEST_METHOD'] != "GET" && $_SERVER['REQUEST_METHOD'] != "PUT")
	{
		header("HTTP/1.1 405 Method Not Allowed");
		return;
	}

	$result_ssl = requestToCamera(CMD_CERTIFICATE, ACTION_GET, TYPE_REQUEST, null);
	if($result_ssl[0] == "OK")
	{
		global $CLASS_PATH;
		require_once($CLASS_PATH . "https.class");

		$ssl['HTTPSConfiguration'] = new HTTPSConfiguration();
		$ssl['HTTPSConfiguration']->PayloadToArray($result_ssl[2]);
	}
	else
	{
		header("HTTP/1.1 500 Internal Server Error");
		return;
	}

	$PolicyArr = array(0 => 'HTTP', 1 => 'HTTPSProprietary'/*, 2 => 'HTTPSPublic'*/);

	if($_SERVER['REQUEST_METHOD'] == "GET")
	{
		$data = array("Policy"=>$PolicyArr[$ssl['HTTPSConfiguration']->dataInfo['Mode']['value']]);

		header("Content-type: application/json");
		echo json_encode($data);
	}
	else if($_SERVER['REQUEST_METHOD'] == "PUT")
	{
		$put_data = json_decode(file_get_contents("php://input"));

		if(!isset($put_data->{'Policy'}))
		{
			header("HTTP/1.1 400 Bad Request");
			return;
		}

		foreach ($put_data as $name => $value)
		{
			switch ($name)
            {
            	case 'Policy':
            		{
            			if(!in_array($value, $PolicyArr))
						{
							header("HTTP/1.1 400 Bad Request");
							return;
						}
            			$ssl['HTTPSConfiguration']->dataInfo['Mode']['value'] = array_search($value, $PolicyArr);
            		}
            		break;
            	default:
	            	{
	            		header("HTTP/1.1 400 Bad Request");
	            		return;
	            	}
	            	break;
            }
		}

		$ssl['HTTPSConfiguration']->payload = MakePayload($ssl['HTTPSConfiguration']->dataInfo);

		$result = requestToCamera(CMD_CERTIFICATE, ACTION_SET, TYPE_REQUEST, unpack('c*', $ssl['HTTPSConfiguration']->payload));
		if($result[0] != "OK")
		{
			header("HTTP/1.1 500 Internal Server Error");
		}
	}
}

switch (@$_REQUEST['msubmenu'])
{
    case 'users': 
    //case 'ssl': 
        {
            $funcName = 'submenu_' . $_REQUEST['msubmenu'];
            $funcName();
        }
        break;
    default:
    	header("HTTP/1.1 501 Not Implemented");
		break;
}
?>
