<?php
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";

function submenu_interface()
{
	if($_SERVER['REQUEST_METHOD'] != "GET" && $_SERVER['REQUEST_METHOD'] != "PUT")
	{
		header("HTTP/1.1 405 Method Not Allowed");
	}
	
	$type = array("Manual", "DHCP");

	$result_network_config_v2 = requestToCamera(CMD_NETWORK_CONFIGURATION_V2, ACTION_GET, TYPE_REQUEST, null);
	if($result_network_config_v2[0] == "OK")
	{
		global $CLASS_PATH;
		require_once($CLASS_PATH . "network_v2.class");

		$netV2Conf['NetworkConfigurationV2'] = new NetworkConfigurationV2();
		$netV2Conf['NetworkConfigurationV2']->PayloadToArray($result_network_config_v2[2]);
	}
	else
	{
		header("HTTP/1.1 500 Internal Server Error");
		return;
	}
	
	if($_SERVER['REQUEST_METHOD'] == "GET")
	{
		require_once($CLASS_PATH . "interface_detail.class");
		$result_network_detail = requestToCamera(CMD_NETWORK_INTERFACE_DETAIL, ACTION_GET, TYPE_REQUEST, null);

		if($result_network_detail[0] == "OK")
		{
			$netDetail['InterfaceDetailConf'] = new InterfaceDetailConfiguration();
			$netDetail['InterfaceDetailConf']->PayloadToArray($result_network_detail[2]);
		}
		else
		{
			header("HTTP/1.1 500 Internal Server Error");
			return;
		}

		if($netV2Conf['NetworkConfigurationV2']->interface[0]->ipv4AddrConf->dataInfo['Type']['value'] == 1) //DHCP
		{
			$data = array("InterfaceName"=>"Network1", 
							"MACAddress"=>$netV2Conf['NetworkConfigurationV2']->interface[0]->dataInfo['HWAddress']['value'], 
							"LinkStatus"=>"Connected", 
							"InterfaceType"=>"Ethernet", 
							"BroadcastAddress"=>$netDetail['InterfaceDetailConf']->dataInfo['BroadCastIPv4Addr']['value'], 
							"IPv4Type"=>$type[$netV2Conf['NetworkConfigurationV2']->interface[0]->ipv4AddrConf->dataInfo['Type']['value']], 
							"IPv4Address"=>$netV2Conf['NetworkConfigurationV2']->interface[0]->ipv4AddrConf->dynamicAddr->dataInfo['Address']['value'], 
							"IPv4PrefixLength"=>$netV2Conf['NetworkConfigurationV2']->interface[0]->ipv4AddrConf->dynamicAddr->dataInfo['Prefix']['value'], 
							"IPv4Gateway"=>$netV2Conf['NetworkConfigurationV2']->gateway->ipv4Addr[0]);
		}
		else //Manual
		{
			$data = array("InterfaceName"=>"Network1", 
							"MACAddress"=>$netV2Conf['NetworkConfigurationV2']->interface[0]->dataInfo['HWAddress']['value'], 
							"LinkStatus"=>"Connected", 
							"InterfaceType"=>"Ethernet", 
							"BroadcastAddress"=>$netDetail['InterfaceDetailConf']->dataInfo['BroadCastIPv4Addr']['value'], 
							"IPv4Type"=>$type[$netV2Conf['NetworkConfigurationV2']->interface[0]->ipv4AddrConf->dataInfo['Type']['value']], 
							"IPv4Address"=>$netV2Conf['NetworkConfigurationV2']->interface[0]->ipv4AddrConf->staticAddr[0]->dataInfo['Address']['value'], 
							"IPv4PrefixLength"=>$netV2Conf['NetworkConfigurationV2']->interface[0]->ipv4AddrConf->staticAddr[0]->dataInfo['Prefix']['value'], 
							"IPv4Gateway"=>$netV2Conf['NetworkConfigurationV2']->gateway->ipv4Addr[0]);
		}

		header("Content-type: application/json");
		echo json_encode($data);
	}
	else if($_SERVER['REQUEST_METHOD'] == "PUT")
	{
		$put_data = json_decode(file_get_contents("php://input"));

		$typeValue = $netV2Conf['NetworkConfigurationV2']->interface[0]->ipv4AddrConf->dataInfo['Type']['value'];
		if(isset($put_data->{'IPv4Type'}))
		{
			if(!in_array($put_data->{'IPv4Type'}, $type))
			{
				header("HTTP/1.1 400 Bad Request");
				return;
			}

			$typeValue = array_search($put_data->{'IPv4Type'}, $type);
		}

		if($typeValue == 1 && (isset($put_data->{'IPv4Address'}) || isset($put_data->{'IPv4PrefixLength'}) || isset($put_data->{'IPv4Gateway'})))
		{
			header("HTTP/1.1 400 Bad Request");
			return;
		}

		if($typeValue == 0 && (!isset($put_data->{'IPv4Address'}) || !isset($put_data->{'IPv4PrefixLength'}) || !isset($put_data->{'IPv4Gateway'})))
		{
			header("HTTP/1.1 400 Bad Request");
			return;
		}

		if($put_data != null)
		{
			foreach ($put_data as $name => $value)
			{
				switch ($name)
	            {
	            	case 'IPv4Type':
	            		{
	            			$netV2Conf['NetworkConfigurationV2']->interface[0]->ipv4AddrConf->dataInfo['Type']['value'] = $typeValue;
	            		}
	            		break;
	            	case 'IPv4Address':
	            		{
	            			$netV2Conf['NetworkConfigurationV2']->interface[0]->ipv4AddrConf->staticAddr[0]->dataInfo['Address']['value'] = $value;
	            		}
	            		break;
	            	case 'IPv4Gateway':
		            	{
		            		$netV2Conf['NetworkConfigurationV2']->gateway->ipv4Addr[0] = $value;
		            	}
		            	break;
		            case 'IPv4PrefixLength':
			            {
			            	if($value < 1 || $value > 24)
							{
								header("HTTP/1.1 400 Bad Request");
								return;
							}
							
							$netV2Conf['NetworkConfigurationV2']->interface[0]->ipv4AddrConf->staticAddr[0]->dataInfo['Prefix']['value'] = (int)$value;
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

		$netV2Conf['NetworkConfigurationV2']->interface[0]->ipv4AddrConf->staticAddr[0]->payload = MakePayload($netV2Conf['NetworkConfigurationV2']->interface[0]->ipv4AddrConf->staticAddr[0]->dataInfo);			
		$netV2Conf['NetworkConfigurationV2']->interface[0]->ipv4AddrConf->SetPayload();
		$netV2Conf['NetworkConfigurationV2']->interface[0]->SetPayload();
		$netV2Conf['NetworkConfigurationV2']->gateway->SetPayload();
		$netV2Conf['NetworkConfigurationV2']->SetPayload();

		$result = requestToCamera(CMD_NETWORK_CONFIGURATION_V2, ACTION_SET, TYPE_REQUEST, unpack('c*', $netV2Conf['NetworkConfigurationV2']->payload));
		if($result[0] != "OK")
		{
			header("HTTP/1.1 500 Internal Server Error");
		}
	}
}

function wifiScan()
{
	ini_set("max_execution_time", 3);
    $result = requestToCamera(CMD_WIRELESS_SCANNING_2, ACTION_GET, TYPE_REQUEST, null);

    $aplist = array();

    if($result[0] == "OK")
    {
    	global $CLASS_PATH;
		require_once($CLASS_PATH . "network_v2.class");
		
		if($result[2] != null && strlen($result[2]) >= 88)
		{
			$netV2Conf['WirelessScanning_2'] = new WirelessScanning_2();
			$netV2Conf['WirelessScanning_2']->PayloadToArray($result[2]);

			$secuMode = array("OPEN"=>"None", "WEP"=>"WEP", "WPA"=>"PSK");
			
			for($i = 0 ; $i < (int)$netV2Conf['WirelessScanning_2']->dataInfo['ap_cnt']['value'] ; $i++)
			{
				$preStr = "AvailableNetworks.".($i+1) . ".";

				array_push($aplist, array($preStr."SSID"=>$netV2Conf['WirelessScanning_2']->apInfo[$i]->dataInfo['ssid']['value'], 
											$preStr."SecurityMode"=>$secuMode[$netV2Conf['WirelessScanning_2']->apInfo[$i]->dataInfo['type']['value']],
											$preStr."SignalStrength"=>$netV2Conf['WirelessScanning_2']->apInfo[$i]->dataInfo['quality']['value']));
			}
		}

    }
    else
    {
    	header("HTTP/1.1 500 Internal Server Error");
    	return "NG";
    }

    return $aplist;
}

function submenu_wifi()
{
	if($_SERVER['REQUEST_METHOD'] != "GET" && $_SERVER['REQUEST_METHOD'] != "PUT")
	{
		header("HTTP/1.1 405 Method Not Allowed");
		return;
	}

	if(isset($_REQUEST["Scan"])) // wifi scan
	{
		if($_SERVER['REQUEST_METHOD'] != "GET")
		{
			header("HTTP/1.1 405 Method Not Allowed");
			return;
		}
		
		$data = wifiScan();
		if($data != "NG")
		{
			header("Content-type: application/json");
			echo json_encode($data);
		}
		
		return;
	}

	if(isset($_REQUEST['Connect']))
	{
		if($_SERVER['REQUEST_METHOD'] != "PUT")
		{
			header("HTTP/1.1 405 Method Not Allowed");
			return;
		}
	}

	$result_network_config_v2 = requestToCamera(CMD_NETWORK_CONFIGURATION_V2, ACTION_GET, TYPE_REQUEST, null);
	if($result_network_config_v2[0] == "OK")
	{
		global $CLASS_PATH;
		require_once($CLASS_PATH . "network_v2.class");

		$netV2Conf['NetworkConfigurationV2'] = new NetworkConfigurationV2();
		$netV2Conf['NetworkConfigurationV2']->PayloadToArray($result_network_config_v2[2]);
	}
	else
	{
		header("HTTP/1.1 500 Internal Server Error");
		return;
	}
	
	if($_SERVER['REQUEST_METHOD'] == "GET")
	{
		$result_network_if_extention = requestToCamera(CMD_NETWORK_IF_EXTENSION, ACTION_GET, TYPE_REQUEST, null);
		if($result_network_if_extention[0] == "OK")
		{
			$netExt['NetworkInterfacesExtension'] = new NetworkInterfacesExtension();
			$netExt['NetworkInterfacesExtension']->PayloadToArray($result_network_if_extention[2]);
			
			$data = array("Enable"=>(bool)$netV2Conf['NetworkConfigurationV2']->interface[1]->dataInfo['Enabled']['value'], 
							"ConnectedSSID"=>$netExt['NetworkInterfacesExtension']->interfaceExtension[1]->dot11Conf->dataInfo['SSID']['value']);
		}
		else
		{
			header("HTTP/1.1 500 Internal Server Error");
			return;
		}

		header("Content-type: application/json");
		echo json_encode($data);
	}
	else if($_SERVER['REQUEST_METHOD'] == "PUT") // wifi connect
	{
		$put_data = json_decode(file_get_contents("php://input"));

		if(isset($_REQUEST['Connect'])) // wifi connection
		{
			if(!isset($put_data->{'SSID'}) || !isset($put_data->{'SecurityMode'}))
			{
				header("HTTP/1.1 400 Bad Request");
				return;
			}

			if($put_data->{'SecurityMode'} == "None")
			{
				if(isset($put_data->{'Password'}))
				{
					header("HTTP/1.1 400 Bad Request");
					return;
				}
			}
			else
			{
				if(!isset($put_data->{'Password'}))
				{
					header("HTTP/1.1 400 Bad Request");
					return;
				}
			}

			$secuMode = array("None", "WEP", "PSK");

			$result_network_if_extention = requestToCamera(CMD_NETWORK_IF_EXTENSION, ACTION_GET, TYPE_REQUEST, null);

			$netExt['NetworkInterfacesExtension'] = new NetworkInterfacesExtension();
			$netExt['NetworkInterfacesExtension']->PayloadToArray($result_network_if_extention[2]);

			foreach ($put_data as $name => $value)
			{
				switch ($name)
	            {
	            	case 'SSID':
	            		{
	            			$netExt['NetworkInterfacesExtension']->interfaceExtension[1]->dot11Conf->dataInfo['SSID']['value'] = $value;
	            		}
	            		break;
	            	case 'Password':
	            		{
	            			$netExt['NetworkInterfacesExtension']->interfaceExtension[1]->dot11Conf->dot11SecurityConf->dataInfo['PSK']['value'] = $value;
	            		}
	            		break;
	            	case 'SecurityMode':
	            		{
	            			if(!in_array($value, $secuMode))
							{
								header("HTTP/1.1 400 Bad Request");
								return;
							}
	            			$netExt['NetworkInterfacesExtension']->interfaceExtension[1]->dot11Conf->dot11SecurityConf->dataInfo['Mode']['value'] = array_search($value, $secuMode);
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

			$netExt['NetworkInterfacesExtension']->interfaceExtension[1]->dataInfo['InterfaceToken']['value'] = $netV2Conf['NetworkConfigurationV2']->interface[1]->dataInfo['Token']['value'];
			$netExt['NetworkInterfacesExtension']->interfaceExtension[1]->dot11Conf->dot11SecurityConf->payload = MakePayload($netExt['NetworkInterfacesExtension']->interfaceExtension[1]->dot11Conf->dot11SecurityConf->dataInfo);
			$netExt['NetworkInterfacesExtension']->interfaceExtension[1]->dot11Conf->SetPayload();
			$netExt['NetworkInterfacesExtension']->interfaceExtension[1]->SetPayload();
			$netExt['NetworkInterfacesExtension']->SetPayload();
			
			$result = requestToCamera(CMD_NETWORK_IF_EXTENSION, ACTION_SET, TYPE_REQUEST, unpack('c*', $netExt['NetworkInterfacesExtension']->payload));
			if($result[0] != "OK")
			{
				header("HTTP/1.1 500 Internal Server Error");
			}
		}
		else // wifi enable setting
		{
			if(!isset($put_data->{'Enable'}))
			{
				header("HTTP/1.1 400 Bad Request");
				return;
			}

			foreach ($put_data as $name => $value)
			{
				switch ($name)
	            {
	            	case 'Enable':
	            		{
	            			if(!is_bool($value))
							{
								header("HTTP/1.1 400 Bad Request");
								return;
							}

							$netV2Conf['NetworkConfigurationV2']->interface[1]->dataInfo['Enabled']['value'] = (int)$put_data->{'Enable'};
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

			$netV2Conf['NetworkConfigurationV2']->interface[2]->dataInfo['Enabled']['value'] = 0; // P2P disable
			
			$netV2Conf['NetworkConfigurationV2']->interface[1]->SetPayload();
			$netV2Conf['NetworkConfigurationV2']->interface[2]->SetPayload();
			
			$netV2Conf['NetworkConfigurationV2']->SetPayload();
			$result = requestToCamera(CMD_NETWORK_CONFIGURATION_V2, ACTION_SET, TYPE_REQUEST, unpack('c*', $netV2Conf['NetworkConfigurationV2']->payload));
			if($result[0] != "OK")
			{
				header("HTTP/1.1 500 Internal Server Error");
			}
		}
	}
}

switch (@$_REQUEST['msubmenu'])
{
    case 'interface': 
    case 'wifi':
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
