<?php
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";

define("OFF_NETWORK"	, 230);

switch ($_SERVER['REQUEST_METHOD']) {
	case "GET":
		
		$result_device = requestToCamera(CMD_SYSTEM_CONFIGURATION, ACTION_GET, TYPE_REQUEST, null);
		$result_time = requestToCamera(CMD_DATETIME, ACTION_GET, TYPE_REQUEST, null);
		$result_network = requestToCamera(CMD_NETWORK_CONFIGURATION, ACTION_GET, TYPE_REQUEST, null);
		$fromdhcp = 0; $dns1 = array(); $dns2 = array(); $ipAddress = array(); $dhcp_static = 0;

		$error = "";
		if($result_device[0] == "OK" && $result_time[0] == "OK" && $result_network[0] == "OK"){
			
			$device = byte2str($result_device[1], 224, 32);	//Device Name
			
			$utc_year = byte2int($result_time[1], 66);		//year
			$utc_month = byte2int($result_time[1], 70); 	//month
			$utc_day = byte2int($result_time[1], 	74);			//day
			$utc_hour = byte2int($result_time[1], 78);		//hour
			$utc_minute = byte2int($result_time[1], 82);	//minute
						
			$utc_date = new DateTime($utc_year . "-" . $utc_month . "-" . $utc_day . " " . $utc_hour . ":" . $utc_minute);
			$utc_date = $utc_date->format("ymdHi");
			
			$fromdhcp = $result[1][OFF_NETWORK+84]; //DHCP?
			$ipAddress[0] = byte2str($result_network[1], OFF_NETWORK+85, 16);	//Static ip
			$ipAddress[1] = byte2str($result_network[1], OFF_NETWORK+105, 16);	//DHCP ip
			
			if($fromdhcp == 1){
				$dhcp_static = 0;
			}else{
				$dhcp_static = 1;
			}
			
			$xw = new xmlWriter();
			$xw->openMemory();
			$xw->startDocument('1.0','UTF-8');
			$xw->startElement ('Device');
			$xw->writeElement ('id', "0");
			$xw->writeElement ('type', "IP-Camera");
			$xw->writeElement ('time', $utc_date);
			$xw->writeElement ('description', $device);
			$xw->writeElement ('InformationLink', "http://$ipAddress[$dhcp_static]/information");
			$xw->writeElement ('UsersLink', "http://$ipAddress[$dhcp_static]/users");
			$xw->endElement();
			$xw->endDocument();
			
			header("Content-type: application/xml");
			echo $xw->outputMemory(true);
		}else{ 
			header("HTTP/1.1 501 Not Implemented");
		}
	break;
	
	case "PUT":
		header("HTTP/1.1 501 Not Implemented");
	break;
	
	default:
		header("HTTP/1.1 404 Not Found");
	break;
}

?>
