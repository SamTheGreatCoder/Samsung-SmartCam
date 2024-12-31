<?php
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/datetime_constant.php";

switch ($_SERVER['REQUEST_METHOD']) {
	case "GET":
		
		$result = requestToCamera(CMD_DATETIME, ACTION_GET, TYPE_REQUEST, null);
		
		$error = "";
		if($result[0] == "OK"){
			
			$utc_year = byte2int($result[1], 66);		//year
			$utc_month = byte2int($result[1], 70); 	//month
			$utc_day = byte2int($result[1], 	74);			//day
			$utc_hour = byte2int($result[1], 78);		//hour
			$utc_minute = byte2int($result[1], 82);	//minute
			$timezone = byte2str($result[1], 2, 64);	//timezone
			$timezoneIndex = byte2int($result[1], 118);	//timezoneIndex
			$dst = $result[1][1]; //summer
						
			$utc_date = new DateTime($utc_year . "-" . $utc_month . "-" . $utc_day . " " . $utc_hour . ":" . $utc_minute);
			$utc_date = $utc_date->format("ymdHi");
			
			switch ($dst){
				case "0":
					$dst = "OFF";
					break;
				case "1":
					$dst = "ON";
					break;
				default;
				break;
			}
			
			$xw = new xmlWriter();
			$xw->openMemory();
			$xw->startDocument('1.0','UTF-8');
			$xw->startElement ('Time');
			$xw->writeElement ('time', $utc_date);
			$xw->writeElement ('timezoneIndex', $timezoneIndex);
			$xw->writeElement ('timezone', $timezone);
			$xw->writeElement ('dst', $dst);
			for ($i = 0; $i < count($TIME_ZONE_LIST); $i++) {
				$xw->writeElement ('timezoneList', $i.",".$TIME_ZONE_LIST[$i][0].",".$TIME_ZONE[$i]);
			}
			$xw->endElement();
			$xw->endDocument();
			
			header("Content-type: application/xml");
			echo $xw->outputMemory(true);
		}else{ 
			header("HTTP/1.1 501 Not Implemented");
		}
	break;
	
	case "PUT":
	
		//input XML
		$xml = file_get_contents('php://input');
	
		//XML Parser
		require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/DMC_xmlParser.php";
	
		//echo($xml)."\n";
		$parser = new XMLParser($xml);
		$parser->Parse();
		$timezoneIndex = $parser->document->timezoneindex[0]->tagData;
		$timezone = $parser->document->timezone[0]->tagData;
		$dst = $parser->document->dst[0]->tagData;
	/*
		echo "timezone : ".$timezone."\n";
		echo "dst : ".$dst."\n";
	*/
			
		switch ($dst){
			case "OFF":
				$dst = "0";
				break;
			case "ON":
				$dst = "1"; 
				break;
			default;
			break;
		}
/*
		echo "\nBefoe_timezoneIndex : ".$timezoneIndex."\n";
		echo "Befoe_timezone : ".$timezone."\n";
		echo "Befoe_dst : ".$dst."\n";
*/	
		//CGI Data set
		$dateTime = array_fill(0, 118, 0x00);  
		$dateTime[118] = $timezoneIndex; //zone
		$dateTime[2] = $timezone;	//zone_name
		$dateTime[1] = $dst;	//summer
		
		//$cmos[count($cmos)] = 0;
		$result = requestToCamera(CMD_DATETIME, ACTION_SET, TYPE_REQUEST, $dateTime);
		if($result[0] == "OK"){
			//echo "OK";
		}else{
			//echo "NOK;" . $result[1];
			header("HTTP/1.1 501 Not Implemented");
		}
		break;
	
	default:
		header("HTTP/1.1 404 Not Found");
	break;
}
?>
