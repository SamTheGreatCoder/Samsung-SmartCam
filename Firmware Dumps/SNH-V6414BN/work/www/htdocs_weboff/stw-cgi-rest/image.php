<?php
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";

function submenu_camera()
{
	if($_SERVER['REQUEST_METHOD'] != "GET" && $_SERVER['REQUEST_METHOD'] != "PUT")
	{
		header("HTTP/1.1 405 Method Not Allowed");
		return;
	}

	global $CLASS_PATH;
	require_once($CLASS_PATH . "imagesetting.class");

	$imgSet['ImageSetting'] = new ImageSetting();
	
	$result_img = requestToCamera(CMD_IMAGE_CONFIGURATION, ACTION_GET, TYPE_REQUEST, unpack('c*', $imgSet['ImageSetting']->payload));
	if($result_img[0] == "OK")
	{		
		$imgSet['ImageSetting']->PayloadToArray($result_img[2]);
	}
	else
	{
		header("HTTP/1.1 500 Internal Server Error");
		return;
	}

	$DayNightMode = array(
		0 => 'Color',
//		1 => 'BW',
		2 => 'Auto'
	);

	$CompensationMode = array(
		0 => "Off",
		3 => "WDR"
	);
	
	if($_SERVER['REQUEST_METHOD'] == "GET")
	{
		$data = array("Channel.0.CompensationMode"=>$CompensationMode[$imgSet['ImageSetting']->imageBackLight->dataInfo['Mode']['value']], 
						"Channel.0.DayNightMode"=>$DayNightMode[$imgSet['ImageSetting']->imageSpecial->dataInfo['DayNightMode']['value']]);
		
		header("Content-type: application/json");
		echo json_encode($data);
	}
	else if($_SERVER['REQUEST_METHOD'] == "PUT")
	{
		$put_data = json_decode(file_get_contents("php://input"));

		if($put_data == null)
		{
			header("HTTP/1.1 400 Bad Request");
			return;
		}

		foreach($put_data as $name => $value)
		{
			switch($name)
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
				case 'CompensationMode':
					{
						$newValue = array_search($value, $CompensationMode);
						if ($newValue === FALSE)
						{
							header("HTTP/1.1 400 Bad Request");
							return;
						}

						if ($newValue == 3) // WDR
						{
							$imgSet['ImageSetting']->imageExposure->dataInfo['LongShutterSpeed']['value'] = 4; //MinShutter = 1/5
							$imgSet['ImageSetting']->imageExposure->dataInfo['ShortShutterSpeed']['value'] = 16; //MaxShutter = 1/240
						}
						else
						{
							if ($imgSet['ImageSetting']->imageBackLight->dataInfo['Mode']['value'] == 3)
							{
								$imgSet['ImageSetting']->imageExposure->dataInfo['LongShutterSpeed']['value'] = 4; //MinShutter = 1/5
								$imgSet['ImageSetting']->imageExposure->dataInfo['ShortShutterSpeed']['value'] = 29; //MaxShutter = 1/12000
							}
						}

						$imgSet['ImageSetting']->imageBackLight->dataInfo['Mode']['value'] = $newValue;
					}
					break;
				case 'DayNightMode':
					{
						if ($value == "Auto")
						{
							if ($imgSet['ImageSetting']->imageExposure->dataInfo['AGCMode']['value'] == 0 ||
									$imgSet['ImageSetting']->imageExposure->dataInfo['AGCMode']['value'] == 4)
							{
								header("HTTP/1.1 400 Bad Request");
								return;
							}
						}

						$newValue = array_search($value, $DayNightMode);
			        	if($newValue === FALSE)
			        	{
			                header("HTTP/1.1 400 Bad Request");
							return;
			            }

						$imgSet['ImageSetting']->imageSpecial->dataInfo['DayNightMode']['value'] = $newValue;
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

		$imgSet['ImageSetting']->SetPayload();
		$result = requestToCamera(CMD_IMAGE_CONFIGURATION, ACTION_SET, TYPE_REQUEST, unpack('c*', $imgSet['ImageSetting']->payload));
		if($result[0] != "OK")
		{
			header("HTTP/1.1 500 Internal Server Error");
		}
	}
}

function submenu_imageenhancements()
{
	if($_SERVER['REQUEST_METHOD'] != "GET" && $_SERVER['REQUEST_METHOD'] != "PUT")
	{
		header("HTTP/1.1 405 Method Not Allowed");
		return;
	}

	global $CLASS_PATH;
	require_once($CLASS_PATH . "imagesetting.class");

	$imgSet['ImageSetting'] = new ImageSetting();
	
	$result_img = requestToCamera(CMD_IMAGE_CONFIGURATION, ACTION_GET, TYPE_REQUEST, unpack('c*', $imgSet['ImageSetting']->payload));
	if($result_img[0] == "OK")
	{		
		$imgSet['ImageSetting']->PayloadToArray($result_img[2]);
	}
	else
	{
		header("HTTP/1.1 500 Internal Server Error");
		return;
	}
	
	if($_SERVER['REQUEST_METHOD'] == "GET")
	{
		$data = array("Channel.0.Brightness"=>(int)$imgSet['ImageSetting']->imageExposure->dataInfo['Brightness']['value']);
	
		header("Content-type: application/json");
		echo json_encode($data);
	}
	else if($_SERVER['REQUEST_METHOD'] == "PUT")
	{
		$put_data = json_decode(file_get_contents("php://input"));

		if(!isset($put_data->{'Brightness'}))
		{
			header("HTTP/1.1 400 Bad Request");
			return;
		}

		foreach($put_data as $name => $value)
		{
			switch($name)
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
				case 'Brightness':
					{
						if ($value < 1 || $value > 100)
						{
							header("HTTP/1.1 400 Bad Request");
		            		return;
						}
						$imgSet['ImageSetting']->imageExposure->dataInfo['Brightness']['value'] = (int)$value;
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

		$imgSet['ImageSetting']->SetPayload();
		$result = requestToCamera(CMD_IMAGE_CONFIGURATION, ACTION_SET, TYPE_REQUEST, unpack('c*', $imgSet['ImageSetting']->payload));
		if($result[0] != "OK")
		{
			header("HTTP/1.1 500 Internal Server Error");
		}
	}
}

function submenu_flip()
{
	if($_SERVER['REQUEST_METHOD'] != "GET" && $_SERVER['REQUEST_METHOD'] != "PUT")
	{
		header("HTTP/1.1 405 Method Not Allowed");
		return;
	}

	$result_flip = requestToCamera(CMD_VIDEO_SOURCE, ACTION_GET, TYPE_REQUEST, null);
	if($result_flip[0] == "OK")
	{		
		global $CLASS_PATH;
		require_once($CLASS_PATH . "videosource.class");

		$videoSrc['VideoSource'] = new VideoSource();
		$videoSrc['VideoSource']->PayloadToArray($result_flip[2]);
	}
	else
	{
		header("HTTP/1.1 500 Internal Server Error");
		return;
	}
	
	if($_SERVER['REQUEST_METHOD'] == "GET")
	{
		$data = array("Channel.0.HorizontalFlipEnable"=>(bool)$videoSrc['VideoSource']->dataInfo['Mirror']['value'], 
						"Channel.0.VerticalFlipEnable"=>(bool)$videoSrc['VideoSource']->dataInfo['Flip']['value']);
		
		header("Content-type: application/json");
		echo json_encode($data);
	}
	else if($_SERVER['REQUEST_METHOD'] == "PUT")
	{
		$put_data = json_decode(file_get_contents("php://input"));

		if($put_data != null)
		{
			foreach($put_data as $name=>$value)
			{
				switch($name)
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
					case 'HorizontalFlipEnable':
					case 'VerticalFlipEnable':
						{
							if(!is_bool($value))
							{
								header("HTTP/1.1 400 Bad Request");
			            		return;
							}

							$dataName = array('HorizontalFlipEnable'=>'Mirror', 'VerticalFlipEnable'=>'Flip');

							$videoSrc['VideoSource']->dataInfo[$dataName[$name]]['value'] = (int)$value;
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

			$videoSrc['VideoSource']->payload = MakePayload($videoSrc['VideoSource']->dataInfo);
			$result = requestToCamera(CMD_VIDEO_SOURCE, ACTION_SET, TYPE_REQUEST, unpack('c*', $videoSrc['VideoSource']->payload));
			if($result[0] != "OK")
			{
				header("HTTP/1.1 500 Internal Server Error");
			}
		}
		else
		{
			header("HTTP/1.1 400 Bad Request");
		}
	}
}

function submenu_overlay()
{
	if($_SERVER['REQUEST_METHOD'] != "GET" && $_SERVER['REQUEST_METHOD'] != "PUT")
	{
		header("HTTP/1.1 405 Method Not Allowed");
		return;
	}

	global $CLASS_PATH;
	require_once($CLASS_PATH . "imagesetting.class");

	$imgSet['ImageSetting'] = new ImageSetting();
	
	$result_img = requestToCamera(CMD_IMAGE_CONFIGURATION, ACTION_GET, TYPE_REQUEST, unpack('c*', $imgSet['ImageSetting']->payload));
	if($result_img[0] == "OK")
	{		
		$imgSet['ImageSetting']->PayloadToArray($result_img[2]);
	}
	else
	{
		header("HTTP/1.1 500 Internal Server Error");
		return;
	}
	
	if($_SERVER['REQUEST_METHOD'] == "GET")
	{
		$data = array("Channel.0.TimeEnable"=>(bool)$imgSet['ImageSetting']->imageOSD->dataInfo['DispDate']['value']);
		
		header("Content-type: application/json");
		echo json_encode($data);
	}
	else if($_SERVER['REQUEST_METHOD'] == "PUT")
	{
		$put_data = json_decode(file_get_contents("php://input"));

		if(!isset($put_data->{'TimeEnable'}))
		{
			header("HTTP/1.1 400 Bad Request");
			return;
		}

		foreach($put_data as $name=>$value)
		{
			switch($name)
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
				case 'TimeEnable':
					{
						if(!is_bool($value))
						{
							header("HTTP/1.1 400 Bad Request");
		            		return;
						}

						$imgSet['ImageSetting']->imageOSD->dataInfo['DispDate']['value'] = (int)$value;
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

		$imgSet['ImageSetting']->SetPayload();
		$result = requestToCamera(CMD_IMAGE_CONFIGURATION, ACTION_SET, TYPE_REQUEST, unpack('c*', $imgSet['ImageSetting']->payload));
		if($result[0] != "OK")
		{
			header("HTTP/1.1 500 Internal Server Error");
		}
	}
}

switch (@$_REQUEST['msubmenu'])
{
    case 'camera': 
    case 'imageenhancements': 
    case 'flip': 
    case 'overlay': 
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
