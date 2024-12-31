<?php
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/datetime_constant.php";

define("OFF_DNS"		, 65);
define("OFF_NETWORK"	, 230);
define("OFF_GATEWAY"	, 1588);
define("OFF_WLAN", 909);
define("OFF_NETWORK"	, 230);

switch ($_SERVER['REQUEST_METHOD']) {
	case "GET":

		$result_network = requestToCamera(CMD_NETWORK_CONFIGURATION, ACTION_GET, TYPE_REQUEST, null);
		if($result_network[0] == "OK"){

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
			$xw->startElement ('AV');
			$xw->writeElement ('rtspSupported', "true");
			$xw->writeElement ('supportrdResolutions', "320,240;640,480");
			$xw->writeElement ('resolution', "640,480");
			$xw->writeElement ('supportrdCodes', "MJPEG;H.264");
			$xw->writeElement ('codec', "H.264");
			$xw->writeElement ('AVProfilesLink', "http://$ipAddress[$dhcp_static]/device/av/avprofiles");
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
