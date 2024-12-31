<?php
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";
//require_once('../cgi-bin/adv/_define.inc');

function submenu_otheroutputs()
{
	if($_SERVER['REQUEST_METHOD'] != "GET" && $_SERVER['REQUEST_METHOD'] != "PUT")
	{
		header("HTTP/1.1 405 Method Not Allowed");
		return;
	}
	
	$state = array("Off", "On");

	global $CLASS_PATH;
	require_once($CLASS_PATH . "io_extention.class");

	$led['IoLED'] = new IoLED();
	
	if($_SERVER['REQUEST_METHOD'] == "GET")
	{
		$result_led = requestToCamera(CMD_LED, ACTION_GET, TYPE_REQUEST, null);
		if($result_led[0] == "OK")
		{
			$led['IoLED']->PayloadToArray($result_led[2]);

			$data = array("StatusLED.State"=>$state[(int)$led['IoLED']->dataInfo['Enabled']['value']]);

			header("Content-type: application/json");
			echo json_encode($data);
		}
		else
		{
			header("HTTP/1.1 500 Internal Server Error");
		}
	}
	else if($_SERVER['REQUEST_METHOD'] == "PUT")
	{
		$put_data = json_decode(file_get_contents("php://input"));

		if(!isset($put_data->{'StatusLED.State'}))
		{
			header("HTTP/1.1 400 Bad Request");
			return;
		}

		foreach ($put_data as $name => $value)
		{
			switch ($name)
            {
            	case 'StatusLED.State':
            		{
            			if(!in_array($value, $state))
						{
							header("HTTP/1.1 400 Bad Request");
							return;
						}

						$led['IoLED']->dataInfo['Enabled']['value'] = array_search($value, $state);
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
		
		$led['IoLED']->SetPayload();
		$result = requestToCamera(CMD_LED, ACTION_SET, TYPE_REQUEST, unpack('c*', $led['IoLED']->payload));
		if($result[0] != "OK")
		{
			header("HTTP/1.1 500 Internal Server Error");
		}
	}
}

function submenu_lullaby()
{
	if($_SERVER['REQUEST_METHOD'] == "PUT")
	{
		$put_data = json_decode(file_get_contents("php://input"));

		foreach ($put_data as $name => $value)
		{
			switch ($name)
            {
            	case 'Mode':
            	case 'FileName':
            		break;
            	default:
	            	{
	            		header("HTTP/1.1 400 Bad Request");
	            		return;
	            	}
	            	break;
            }
		}

		if(!isset($put_data->{'Mode'}))
		{
			header("HTTP/1.1 400 Bad Request");
			return;
		}

		if($put_data->{'Mode'} == "Start")
		{
			if(!isset($put_data->{'FileName'}))
			{
				header("HTTP/1.1 400 Bad Request");
				return;
			}

			$value = $put_data->{'FileName'};

			if($value != "Alarm-Siren.wav" && $value != "Dog-barking.wav" && 
    	        $value != "police-siren.wav")
			{
				header("HTTP/1.1 400 Bad Request");
				return;
			}

			global $CLASS_PATH;
			require_once($CLASS_PATH . "io_extention.class");

			$lullaby['IoLullaby'] = new IoLullaby();
			$lullaby['IoLullaby']->dataInfo['fileName']['value'] = $value;
			$lullaby['IoLullaby']->SetPayload();
			
			$result = requestToCamera(CMD_LULLABY, ACTION_START, TYPE_REQUEST, unpack('c*', $lullaby['IoLullaby']->payload));
			if($result[0] != "OK")
			{
				header("HTTP/1.1 500 Internal Server Error");
			}
		}
		else if($put_data->{'Mode'} == "Stop")
		{
			$result = requestToCamera(CMD_LULLABY, ACTION_STOP, TYPE_REQUEST, null);
			if($result[0] != "OK")
			{
				header("HTTP/1.1 500 Internal Server Error");
			}
		}
		else
		{
			header("HTTP/1.1 400 Bad Request");
			return;
		}
	}
	else
	{
		header("HTTP/1.1 405 Method Not Allowed");
	}
}

switch (@$_REQUEST['msubmenu'])
{
    case 'otheroutputs': 
    case 'lullaby': 
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
