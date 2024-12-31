<?php
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";

function submenu_smtp()
{
	if($_SERVER['REQUEST_METHOD'] != "GET" && $_SERVER['REQUEST_METHOD'] != "PUT")
	{
		header("HTTP/1.1 405 Method Not Allowed");
		return;
	}

	$result_smtp = requestToCamera(CMD_SMTP_SETTING, ACTION_GET, TYPE_REQUEST, null);
	if($result_smtp[0] == "OK")
	{
		global $CLASS_PATH;
		require_once($CLASS_PATH . "network_smtp.class");

		$smtp['SMTPSetting'] = new SMTPSetting();
		$smtp['SMTPSetting']->PayloadToArray($result_smtp[2]);
	}
	else
	{
		header("HTTP/1.1 500 Internal Server Error");
		return;
	}
	
	if($_SERVER['REQUEST_METHOD'] == "GET")
	{
		$data = array("Sender"=>$smtp['SMTPSetting']->dataInfo['Sender']['value'], 
						"Recipient"=>$smtp['SMTPSetting']->dataInfo['Recipient']['value'], 
						"Server"=>"smtp.gmail.com", 
						"Port"=>465, 
						"AuthNeeded"=>(bool)$smtp['SMTPSetting']->dataInfo['AuthNeeded']['value'], 
						"Username"=>$smtp['SMTPSetting']->dataInfo['UserName']['value'], 
						"Password"=>$smtp['SMTPSetting']->dataInfo['Password']['value'], 
						"Subject"=>$smtp['SMTPSetting']->dataInfo['Subject']['value'], 
						"Body"=>$smtp['SMTPSetting']->dataInfo['Body']['value'], 
						"SSLEnabled"=>(bool)$smtp['SMTPSetting']->dataInfo['SSLEnabled']['value'], 
						"SSLPort"=>$smtp['SMTPSetting']->dataInfo['SSLPort']['value']);

		header("Content-type: application/json");
		echo json_encode($data);
	}
	else if($_SERVER['REQUEST_METHOD'] == "PUT")
	{
		$put_data = json_decode(file_get_contents("php://input"));

		if($put_data != null)
		{
			foreach ($put_data as $name => $value)
			{
				switch ($name)
	            {
	            	case 'AuthNeeded':
		            	{
		            		if(!is_bool($value))
		            		{
		            			header("HTTP/1.1 400 Bad Request");
		            			return;
		            		}
		            		
		            		$smtp['SMTPSetting']->dataInfo['AuthNeeded']['value'] = (int)$value;
		            	}
		            	break;
		            case 'Sender':
		            case 'Recipient':
		            {
		            	if(strlen($value) > 127)
		            	{
		            		header("HTTP/1.1 400 Bad Request");
	            			return;
		            	}
		            }
		            case 'Username':
		            case 'Password':
		            case 'Subject':
		            case 'Body':
		            	{
		            		$dataNameList = array('Sender' => 'Sender', 'Recipient' => 'Recipient', 'Username' => 'UserName', 'Password' => 'Password', 
	                        						'Subject' => 'Subject', 'Body' => 'Body');
	                        						
		            		$smtp['SMTPSetting']->dataInfo[$dataNameList[$name]]['value'] = $value;
		            	}
		            	break;
		            case 'SSLEnabled':
		            	{
		            		if(!is_bool($value))
		            		{
		            			header("HTTP/1.1 400 Bad Request");
		            			return;
		            		}
		            		$smtp['SMTPSetting']->dataInfo['SSLEnabled']['value'] = (int)$value;
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
		}

		$smtp['SMTPSetting']->dataInfo['Server']['value'] = "smtp.gmail.com";
		$smtp['SMTPSetting']->dataInfo['Port']['value'] = 465;
						
		$smtp['SMTPSetting']->payload = MakePayload($smtp['SMTPSetting']->dataInfo);
		$result = requestToCamera(CMD_SMTP_SETTING, ACTION_SET, TYPE_REQUEST, unpack('c*', $smtp['SMTPSetting']->payload));
		if($result[0] != "OK")
		{
			header("HTTP/1.1 500 Internal Server Error");
		}
	}
}

function checkSubscriptionID($SubList, $input, &$index, &$emptyIdx)
{
	for($i = 0 ; $i < MAX_SUBSCRIPTION ; $i++)
	{
		if($SubList->subscription[$i]->dataInfo['enable']['value'] == 1)
		{
			if($SubList->subscription[$i]->dataInfo['subID']['value'] == $input)
			{
				$index = $i;
			}
		}
		else
		{
			if($emptyIdx < 0)
			{
				$emptyIdx = $i;
			}
		}
	}
}

function submenu_subscription()
{
	if($_SERVER['REQUEST_METHOD'] != "GET" && $_SERVER['REQUEST_METHOD'] != "POST" && $_SERVER['REQUEST_METHOD'] != "PUT" && $_SERVER['REQUEST_METHOD'] != "DELETE")
	{
		header("HTTP/1.1 405 Method Not Allowed");
		return;
	}

	$result_httpnoti = requestToCamera(CMD_HTTP_NOTIFICATION, ACTION_GET, TYPE_REQUEST, null);
	if($result_httpnoti[0] == "OK")
	{
		global $CLASS_PATH;
		require_once($CLASS_PATH . "network_httpnoti.class");

		$http['HTTPNoti'] = new HTTPNotificationSetting();
		$http['HTTPNoti']->PayloadToArray($result_httpnoti[2]);
	}
	else
	{
		header("HTTP/1.1 500 Internal Server Error");
		return;
	}

	$eventType = array(
					0 => "None", 
					1 => "Motion", 
					2 => "Audio", 
					3 => "All");
	
	if($_SERVER['REQUEST_METHOD'] == "GET")
	{
		$subList = array();

		for($i = 0 ; $i < MAX_SUBSCRIPTION ; $i++)
		{
			if($http['HTTPNoti']->subscription[$i]->dataInfo['enable']['value'] == 1)
			{
				array_push($subList, array("NotificationURL"=>$http['HTTPNoti']->subscription[$i]->dataInfo['URL']['value'], 
													"EventType"=>$eventType[$http['HTTPNoti']->subscription[$i]->dataInfo['eventType']['value']], 
													"SubscriptionID"=>$http['HTTPNoti']->subscription[$i]->dataInfo['subID']['value']));
			}
		}
		
		$data = array("CameraID"=>$http['HTTPNoti']->dataInfo['cameraID']['value'],
							"SubscriptionList"=>$subList);

		header("Content-type: application/json");
		echo json_encode($data);
	}
	else if($_SERVER['REQUEST_METHOD'] == "POST" || $_SERVER['REQUEST_METHOD'] == "PUT")
	{
		$put_data = json_decode(file_get_contents("php://input"));

		if(!isset($put_data->{'SubscriptionID'}))
		{
			header("HTTP/1.1 400 Bad Request");
			return;
		}

		$index = -1;	$emptyIdx = -1;
		checkSubscriptionID($http['HTTPNoti'], $put_data->{'SubscriptionID'}, &$index, &$emptyIdx);

		if($_SERVER['REQUEST_METHOD'] == "POST") // add
		{
			if(!isset($put_data->{'NotificationURL'}) || !isset($put_data->{'EventType'}))
			{
				header("HTTP/1.1 400 Bad Request");
				return;
			}
			
			if($index >= 0 || $emptyIdx < 0)
			{
				header("HTTP/1.1 400 Bad Request");
				return;
			}

			$idx = $emptyIdx;
		}
		else // modify
		{
			if($index < 0)
			{
				header("HTTP/1.1 400 Bad Request");
				return;
			}

			$idx = $index;
		}
		
		foreach ($put_data as $name => $value)
		{
			switch ($name)
            {
            	case 'NotificationURL':
	            	{
	            		if(strlen($value) > 511)
		            	{
		            		header("HTTP/1.1 400 Bad Request");
	            			return;
		            	}

		            	if(preg_match('~^http(s)?\:\/\/[a-z0-9]([a-z0-9\-]\.+)*~i', $value) != 1)
						{
							header("HTTP/1.1 400 Bad Request");
	            			return;
						}

						$http['HTTPNoti']->subscription[$idx]->dataInfo['URL']['value'] = $value;
	            	}
	            	break;
	            case 'SubscriptionID':
		            {
		            	if(strlen($value) > 511)
		            	{
		            		header("HTTP/1.1 400 Bad Request");
	            			return;
		            	}

		            	$http['HTTPNoti']->subscription[$idx]->dataInfo['subID']['value'] = $value;
		            }
		            break;
	            case 'EventType':
	            	{
	            		$newValue = array_search($value, $eventType);
			        	if($newValue === FALSE)
			        	{
			                header("HTTP/1.1 400 Bad Request");
							return;
			            }
                        						
	            		$http['HTTPNoti']->subscription[$idx]->dataInfo['eventType']['value'] = $newValue;
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

		$http['HTTPNoti']->subscription[$idx]->dataInfo['enable']['value'] = 1;
		$http['HTTPNoti']->subscription[$idx]->SetPayload();
		$http['HTTPNoti']->SetPayload();

		if($_SERVER['REQUEST_METHOD'] == "POST")
		{
			$result = requestToCamera(CMD_HTTP_NOTIFICATION, ACTION_ADD, TYPE_REQUEST, unpack('c*', $http['HTTPNoti']->subscription[$idx]->payload));
		}
		else
		{
			$result = requestToCamera(CMD_HTTP_NOTIFICATION, ACTION_SET, TYPE_REQUEST, unpack('c*', $http['HTTPNoti']->payload));
		}
		
		if($result[0] != "OK")
		{
			header("HTTP/1.1 500 Internal Server Error");
		}
	}
	else if($_SERVER['REQUEST_METHOD'] == "DELETE")
	{
		$put_data = json_decode(file_get_contents("php://input"));
		
		if(!isset($put_data->{'SubscriptionID'}))
		{
			header("HTTP/1.1 400 Bad Request");
			return;
		}

		$index = -1;	$emptyIdx = -1;
		checkSubscriptionID($http['HTTPNoti'], $put_data->{'SubscriptionID'}, &$index, &$emptyIdx);

		if($index < 0)
		{
			header("HTTP/1.1 400 Bad Request");
			return;
		}

		$result = requestToCamera(CMD_HTTP_NOTIFICATION, ACTION_REMOVE, TYPE_REQUEST, unpack('c*', $http['HTTPNoti']->subscription[$index]->payload));
		if($result[0] != "OK")
		{
			header("HTTP/1.1 500 Internal Server Error");
		}
	}
}

switch (@$_REQUEST['msubmenu'])
{
    case 'smtp': 
    //case 'subscription': 
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
