<?php
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";

function submenu_audioinput()
{
	if($_SERVER['REQUEST_METHOD'] != "GET" && $_SERVER['REQUEST_METHOD'] != "PUT")
	{
		header("HTTP/1.1 405 Method Not Allowed");
		return;
	}

	$result_media = requestToCamera(CMD_MEDIA_CONFIGURATION, ACTION_GET, TYPE_REQUEST, null);
	if($result_media[0] == "OK")
	{
		global $CLASS_PATH;
		require_once($CLASS_PATH . "media.class");

		$media['MediaConfiguration'] = new MediaConfiguration();
		$media['MediaConfiguration']->PayloadToArray($result_media[2]);
	}
	else
	{
		header("HTTP/1.1 500 Internal Server Error");
		return;
	}
	
	if($_SERVER['REQUEST_METHOD'] == "GET")
	{
		if($media['MediaConfiguration']->audioInput->dataInfo['Enabled']['value'] == 0)
		{
			$data = array("Channel.0.Gain"=>0);
		}
		else
		{
			$data = array("Channel.0.Gain"=>($media['MediaConfiguration']->audioInput->dataInfo['Gain']['value']/3));
		}

		header("Content-type: application/json");
		echo json_encode($data);
	}
	else if($_SERVER['REQUEST_METHOD'] == "PUT")
	{
		$put_data = json_decode(file_get_contents("php://input"));

		if(!isset($put_data->{'Gain'}))
		{
			header("HTTP/1.1 400 Bad Request");
			return;
		}

		foreach ($put_data as $name => $value)
		{
			switch ($name)
            {
            	case 'Channel':
            		{
            			if($value != 0)
            			{
		            		header("HTTP/1.1 400 Bad Request");
		            		return;
		            	}
	            	}
	            	break;
            	case 'Gain':
            		{
            			$gain = (int)$value;
            			if($gain < 0 || $gain > 3)
						{
							header("HTTP/1.1 400 Bad Request");
							return;
						}	
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
		
		if($gain == 0)
		{
			$media['MediaConfiguration']->audioInput->dataInfo['Enabled']['value'] = 0;
		}
		else
		{
			$media['MediaConfiguration']->audioInput->dataInfo['Enabled']['value'] = 1;
			$media['MediaConfiguration']->audioInput->dataInfo['Gain']['value'] = $gain * 3;
		}
		
		$media['MediaConfiguration']->audioInput->payload = MakePayload($media['MediaConfiguration']->audioInput->dataInfo);
		$media['MediaConfiguration']->SetPayload();

		$result = requestToCamera(CMD_MEDIA_CONFIGURATION, ACTION_SET, TYPE_REQUEST, unpack('c*', $media['MediaConfiguration']->payload));
		if($result[0] != "OK")
		{
			header("HTTP/1.1 500 Internal Server Error");
		}
	}
}

function submenu_audiooutput()
{
	if($_SERVER['REQUEST_METHOD'] != "GET" && $_SERVER['REQUEST_METHOD'] != "PUT")
	{
		header("HTTP/1.1 405 Method Not Allowed");
		return;
	}

	$result_media = requestToCamera(CMD_MEDIA_CONFIGURATION, ACTION_GET, TYPE_REQUEST, null);
	if($result_media[0] == "OK")
	{
		global $CLASS_PATH;
		require_once($CLASS_PATH . "media.class");

		$media['MediaConfiguration'] = new MediaConfiguration();
		$media['MediaConfiguration']->PayloadToArray($result_media[2]);
	}
	else
	{
		header("HTTP/1.1 500 Internal Server Error");
		return;
	}
	
	if($_SERVER['REQUEST_METHOD'] == "GET")
	{
		if($media['MediaConfiguration']->audioOutput->dataInfo['Enabled']['value'] == 0)
		{
			$data = array("Channel.0.Gain"=>0);
		}
		else
		{
			$data = array("Channel.0.Gain"=>$media['MediaConfiguration']->audioOutput->dataInfo['Gain']['value']);
		}

		header("Content-type: application/json");
		echo json_encode($data);
	}
	else if($_SERVER['REQUEST_METHOD'] == "PUT")
	{
		$put_data = json_decode(file_get_contents("php://input"));

		if(!isset($put_data->{'Gain'}))
		{
			header("HTTP/1.1 400 Bad Request");
			return;
		}

		foreach ($put_data as $name => $value)
		{
			switch ($name)
            {
            	case 'Channel':
            		{
            			if($value != 0)
            			{
		            		header("HTTP/1.1 400 Bad Request");
		            		return;
		            	}
	            	}
	            	break;
            	case 'Gain':
            		{
            			$gain = (int)$value;
            			if($gain < 0 || $gain > 10)
						{
							header("HTTP/1.1 400 Bad Request");
							return;
						}	
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

		if($gain == 0)
		{
			$media['MediaConfiguration']->audioOutput->dataInfo['Enabled']['value'] = 0;
		}
		else
		{
			$media['MediaConfiguration']->audioOutput->dataInfo['Enabled']['value'] = 1;
			$media['MediaConfiguration']->audioOutput->dataInfo['Gain']['value'] = $gain;
		}
		
		$media['MediaConfiguration']->audioOutput->payload = MakePayload($media['MediaConfiguration']->audioOutput->dataInfo);
		$media['MediaConfiguration']->SetPayload();

		$result = requestToCamera(CMD_MEDIA_CONFIGURATION, ACTION_SET, TYPE_REQUEST, unpack('c*', $media['MediaConfiguration']->payload));
		if($result[0] != "OK")
		{
			header("HTTP/1.1 500 Internal Server Error");
		}
	}
	else
	{
		header("HTTP/1.1 405 Method Not Allowed");
	}
}

switch (@$_REQUEST['msubmenu'])
{
    case 'audioinput': 
    case 'audiooutput': 
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
