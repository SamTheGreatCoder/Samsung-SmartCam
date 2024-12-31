<?php
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";

switch ($_SERVER['REQUEST_METHOD']) {
	case "GET":
		
		$result = requestToCamera(CMD_SYSTEM_CONFIGURATION, ACTION_GET, TYPE_REQUEST, null);

		$error = "";
		if($result[0] == "OK"){
			
			$manufacturer = byte2str($result[1], 0, 64);	//Manufacturer
			$modelID = byte2str($result[1], 64, 32); //Model
			$swVersion = byte2str($result[1], 96, 16); //FirmwareVersion
			$SerialNumber = byte2str($result[1], 176, 32); //SerialNumber
			
			$xw = new xmlWriter();
			$xw->openMemory();
			$xw->startDocument('1.0','UTF-8');
			$xw->startElement ('Information');
			$xw->writeElement ('modelID', $modelID);
			$xw->writeElement ('SerialNumber', $SerialNumber);
			$xw->endElement();
			$xw->endDocument();
			
			header("Content-type: application/xml");
			echo $xw->outputMemory(true);
		}else{ 
			header("HTTP/1.1 501 Not Implemented");
		}
	break;
	
	default:
		header("HTTP/1.1 404 Not Found");
	break;
}
?>
