<?php
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";

function gettingServerFWVersion()
{
	require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/xmlParser.php";

	$fwVer = '';

	$parser = new xmlParser("http://www.samsungsmartcam.com/firmware/firmware.xml");
	if($parser->result)
	{
		$models = $parser->getData("FIRMWARE/MODEL");
		if($models != null && is_array($models))
		{
			foreach($models as $model)
			{
				if($model["NAME"] == "SNH-E6440BN")
				{
					$lastMajor = trim($model["MAJOR"]);
					$lastMinor = trim($model["MINOR"]);
					$lastMinor = (strlen($lastMinor) < 2)? $lastMinor . "0" : $lastMinor;
					$lastDate = trim($model["DATE"]);
					$fwVer = $lastMajor . "." . $lastMinor . "_" . $lastDate;
					break;
				}
			}
		}
	}

	return $fwVer;
}

function submenu_deviceinfo()
{
	if($_SERVER['REQUEST_METHOD'] == "GET")
	{
		$result_device = requestToCamera(CMD_SYSTEM_CONFIGURATION, ACTION_GET, TYPE_REQUEST, null);

		if($result_device[0] == "OK")
		{
			global $CLASS_PATH;
			require_once($CLASS_PATH . "system.class");

			$sysConf['SystemConfiguration'] = new SystemConfiguration();
			$sysConf['SystemConfiguration']->PayloadToArray($result_device[2]);

			$fwVer = explode('_', $sysConf['SystemConfiguration']->deviceInfo->dataInfo['FirmwareVer']['value']);

			$buildDate = "20" . substr($fwVer[1], 0, 2) .
						 "." . substr($fwVer[1], 2, 2) .
						 "." . substr($fwVer[1], 4, 2);

			$mac = substr($sysConf['SystemConfiguration']->deviceInfo->dataInfo['HardwareID']['value'], 0, 2) .
					":" . substr($sysConf['SystemConfiguration']->deviceInfo->dataInfo['HardwareID']['value'], 2, 2) .
					":" . substr($sysConf['SystemConfiguration']->deviceInfo->dataInfo['HardwareID']['value'], 4, 2) .
					":" . substr($sysConf['SystemConfiguration']->deviceInfo->dataInfo['HardwareID']['value'], 6, 2) .
					":" . substr($sysConf['SystemConfiguration']->deviceInfo->dataInfo['HardwareID']['value'], 8, 2) .
					":" . substr($sysConf['SystemConfiguration']->deviceInfo->dataInfo['HardwareID']['value'], 10, 2);

			$data = array("Model"=>$sysConf['SystemConfiguration']->deviceInfo->dataInfo['Model']['value'],
							"SerialNumber"=>$sysConf['SystemConfiguration']->deviceInfo->dataInfo['SerialNum']['value'],
							"FirmwareVersion"=>$sysConf['SystemConfiguration']->deviceInfo->dataInfo['FirmwareVer']['value'],
							"BuildDate"=>$buildDate,
							"DeviceType"=>"NWC",
							"ConnectedMACAddress"=>$mac);

			header("Content-type: application/json");
			echo json_encode($data);
		}
		else
		{
			header("HTTP/1.1 500 Internal Server Error");
		}
	}
	else
	{
		header("HTTP/1.1 405 Method Not Allowed");
	}
}

function submenu_date()
{
	$syncType = array("Manual", "NTP");

	if($_SERVER['REQUEST_METHOD'] == "GET")
	{
		if(isset($_REQUEST["TimeZoneList"]))
		{
			require_once($_SERVER["DOCUMENT_ROOT"] . "/utils/timezone_list.cgi");

			$list = array();

			for($i = 0 ; $i < count($TIME_ZONE_LIST_SET); $i++)
			{
				$timezone_value = sprintf("%02d:%s", $i, $TIME_ZONE_LIST_SET[$i][0]);
				array_push($list, $timezone_value);
			}

			$data = array("TimeZoneList"=>$list);
		}
		else
		{
			$result_date = requestToCamera(CMD_DATETIME, ACTION_GET, TYPE_REQUEST, null);
			if($result_date[0] == "OK")
			{
				global $CLASS_PATH;
				require_once($CLASS_PATH . "datetime.class");

				$datetime['DateTimeConfiguration'] = new DateTimeConfiguration();
				$datetime['DateTimeConfiguration']->PayloadToArray($result_date[2]);

				$localTimestamp = mktime($datetime['DateTimeConfiguration']->localDateTime->dataInfo['Hour']['value'],
											$datetime['DateTimeConfiguration']->localDateTime->dataInfo['Min']['value'],
											$datetime['DateTimeConfiguration']->localDateTime->dataInfo['Sec']['value'],
											$datetime['DateTimeConfiguration']->localDateTime->dataInfo['Month']['value'],
											$datetime['DateTimeConfiguration']->localDateTime->dataInfo['Day']['value'],
											$datetime['DateTimeConfiguration']->localDateTime->dataInfo['Year']['value']);

				$utcTimestamp = mktime($datetime['DateTimeConfiguration']->utcDateTime->dataInfo['Hour']['value'],
											$datetime['DateTimeConfiguration']->utcDateTime->dataInfo['Min']['value'],
											$datetime['DateTimeConfiguration']->utcDateTime->dataInfo['Sec']['value'],
											$datetime['DateTimeConfiguration']->utcDateTime->dataInfo['Month']['value'],
											$datetime['DateTimeConfiguration']->utcDateTime->dataInfo['Day']['value'],
											$datetime['DateTimeConfiguration']->utcDateTime->dataInfo['Year']['value']);

				$data = array("LocalTime"=>date('Y-m-d H:i:s', $localTimestamp),
								"UTCTime"=>date('Y-m-d H:i:s', $utcTimestamp),
								"SyncType"=>$syncType[$datetime['DateTimeConfiguration']->dataInfo['Type']['value']],
								"DSTEnable"=>(bool)$datetime['DateTimeConfiguration']->dataInfo['DaylightSavings']['value'],
								"TimeZoneIndex"=>(int)$datetime['DateTimeConfiguration']->currTimezoneIdx,
								"POSIXTimeZone"=>$datetime['DateTimeConfiguration']->dataInfo['TimeZone']['value']);
			}
			else
			{
				header("HTTP/1.1 500 Internal Server Error");
				return;
			}
		}

		header("Content-type: application/json");
		echo json_encode($data);
	}
	else if($_SERVER['REQUEST_METHOD'] == "PUT")
	{
		if(isset($_REQUEST["TimeZoneList"]))
		{
			header("HTTP/1.1 405 Method Not Allowed");
			return;
		}

		$put_data = json_decode(file_get_contents("php://input"));

		$result_date = requestToCamera(CMD_DATETIME, ACTION_GET, TYPE_REQUEST, null);
		if($result_date[0] == "OK")
		{
			global $CLASS_PATH;
			require_once($CLASS_PATH . "datetime.class");

			$datetime['DateTimeConfiguration'] = new DateTimeConfiguration();
			$datetime['DateTimeConfiguration']->PayloadToArray($result_date[2]);

			if(!isset($put_data->{'SyncType'}))
			{
				header("HTTP/1.1 400 Bad Request");
				return;
			}

			foreach ($put_data as $name => $value)
			{
				switch ($name)
	            {
	            	case 'SyncType':
	            		{
	            			if($value != "NTP")
							{
								header("HTTP/1.1 400 Bad Request");
								return;
							}
	            		}
	            		break;
	            	case 'DSTEnable':
		            	{
		            		if(!is_bool($value))
		            		{
		            			header("HTTP/1.1 400 Bad Request");
		            			return;
		            		}

		            		$datetime['DateTimeConfiguration']->dataInfo['DaylightSavings']['value'] = (int)$value;
		            	}
		            	break;
		            case 'TimeZoneIndex':
			            {
			            	if($value < 0 || $value > 100)
							{
								header("HTTP/1.1 400 Bad Request");
								return;
							}

							$datetime['DateTimeConfiguration']->currTimezoneIdx = $value;
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

			$datetime['DateTimeConfiguration']->SetPayload();
			$result = requestToCamera(CMD_DATETIME, ACTION_SET, TYPE_REQUEST, unpack('c*', $datetime['DateTimeConfiguration']->payload));
			if($result[0] != "OK")
			{
				header("HTTP/1.1 500 Internal Server Error");
			}
		}
		else
		{
			header("HTTP/1.1 500 Internal Server Error");
		}
	}
	else
	{
		header("HTTP/1.1 405 Method Not Allowed");
	}
}

function submenu_factoryreset()
{
	if($_SERVER['REQUEST_METHOD'] == "PUT")
	{
		$put_data = json_decode(file_get_contents("php://input"));

		global $CLASS_PATH;
		require_once($CLASS_PATH . "reset.class");

		$factoryReset['FactoryDefaultConf'] = new FactoryDefaultConfiguration();

		if($put_data != null)
		{
			foreach ($put_data as $name => $value)
			{
				switch ($name)
	            {
	            	case 'ExcludeSettings':
	            		{
	            			if($value != "Network")
							{
								header("HTTP/1.1 400 Bad Request");
								return;
							}

							$factoryReset['FactoryDefaultConf']->dataInfo['Type']['value'] = 0;
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

		if(!isset($put_data->{'ExcludeSettings'}))
		{
			$factoryReset['FactoryDefaultConf']->dataInfo['Type']['value'] = 1;
		}

		$factoryReset['FactoryDefaultConf']->payload = MakePayload($factoryReset['FactoryDefaultConf']->dataInfo);
		$result = requestToCamera(CMD_FACTORY_DEFAULT, ACTION_SET, TYPE_REQUEST, unpack('c*', $factoryReset['FactoryDefaultConf']->payload));
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

function submenu_power()
{
	if($_SERVER['REQUEST_METHOD'] == "PUT")
	{
		$put_data = json_decode(file_get_contents("php://input"));
		if($put_data != null)
		{
			foreach ($put_data as $name => $value)
			{
				switch ($name)
	            {
	            	case 'Type':
	            		{
	            			if($value != "Restart")
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
		}

		global $CLASS_PATH;
		require_once($CLASS_PATH . "reset.class");

		$reboot['rebootConfig'] = new RebootConfiguration();
		$reboot['rebootConfig']->dataInfo['Message']['value'] = "Camera Reboot Requested";

		$reboot['rebootConfig']->payload = MakePayload($reboot['rebootConfig']->dataInfo);
		$result = requestToCamera(CMD_REBOOT, ACTION_SET, TYPE_REQUEST, unpack('c*', $reboot['rebootConfig']->payload));
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

function submenu_firmwareupdate()
{
	if($_SERVER['REQUEST_METHOD'] == "GET")
	{
		$data = array("ServerFirmwareVersion"=>gettingServerFWVersion());

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
	            	case 'Type':
	            		{
	            			if($value != "Normal")
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
		}

		global $CLASS_PATH;
		require_once($CLASS_PATH . "fwupdate.class");

		$fwConf['firmwareConfig'] = new FirmwareUpdateConfiguration_HSS();
		$result = requestToCamera(CMD_FIRMWARE_UPGRADE_2, ACTION_SET, TYPE_REQUEST, unpack('c*', $fwConf['firmwareConfig']->payload));

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
    case 'deviceinfo':
    case 'date':
    case 'factoryreset':
    case 'power':
    case 'firmwareupdate':
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
