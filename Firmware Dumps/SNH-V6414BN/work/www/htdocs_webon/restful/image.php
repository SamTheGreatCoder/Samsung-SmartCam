<?php
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";

switch ($_SERVER['REQUEST_METHOD']) {
	case "GET":

		$temp = array(0, 0, 0, 0);
		$result = requestToCamera(CMD_CMOS_CONFIGURATION, ACTION_GET, TYPE_REQUEST, $temp);

		$cmos = array_fill(0, 120, 0x00);
		//$brightness = 5; $flip_mode = 0; $flicker = 0; $ir_mode = 0; $error = "";
		$error = "";
		if($result[0] == "OK"){
				
			$cmos = $result[1];
			$brightness = byte2int($cmos, 24);		//Brightness
			$flip_mirror = byte2int($cmos, 72);		//FlipMode
			$dayNight = byte2int($cmos, 96);			//IrMode
			$flickerless = byte2int($cmos, 76);			//FlickerMode
				
			switch ($flip_mirror){
				case "0":
					$flip = "OFF"; $mirror  = "OFF"; //Normal
					break;
				case "1":
					$flip = "OFF"; $mirror  = "ON";	//Vertical
					break;
				case "2":
					$flip = "ON"; $mirror  = "OFF";	//Horizontal
					break;
				case "3":
					$flip = "ON"; $mirror  = "ON";	//Rotate 180
					break;
				default;
				break;
			}
				
			switch ($dayNight){
				case "0":
					$dayNight = "OFF";
					break;
				case "1":
					$dayNight = "ON";
					break;
				default;
				break;
			}

			switch ($flickerless){
				case "0":
					$flickerless = "Auto";
					break;
				case "1":
					$flickerless = "50";
					break;
				case "2":
					$flickerless = "60";
					break;
				default;
				break;
			}
				
			$xw = new xmlWriter();
			$xw->openMemory();
			$xw->startDocument('1.0','UTF-8');
			$xw->startElement ('Image');
			$xw->writeElement ('brightness', $brightness);
			$xw->writeElement ('flip', $flip);
			$xw->writeElement ('mirror', $mirror);
			$xw->writeElement ('dayNight', $dayNight);
			$xw->writeElement ('flickerless', $flickerless);
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
		$brightness = $parser->document->brightness[0]->tagData;
		$brightness = ($brightness > 10)? 10 : $brightness;
		$flip = $parser->document->flip[0]->tagData;
		$mirror = $parser->document->mirror[0]->tagData;
		$dayNight = $parser->document->daynight[0]->tagData;
		$flickerless = $parser->document->flickerless[0]->tagData;

		switch ($flip ) {
			case "OFF":
				if ($mirror == "OFF") {
					$flip_mirror = "0"; //flip OFF/mirror OFF Normal
				}else{
					$flip_mirror = "1"; //flip OFF/mirror ON Vertical
				}
				break;
			case "ON":
				if ($mirror == "OFF") {
					$flip_mirror = "2"; //flip ON/mirror OFF Horizontal
				}else{
					$flip_mirror = "3"; //flip ON/mirror ON Roatate 180
				}
				break;
			default:
				break;
		}

		switch ($dayNight){
			case "OFF":
				$dayNight = "0";
				break;
			case "ON":
				$dayNight = "1"; //Auto
				break;
			default;
			break;
		}

		switch ($flickerless){
			case "Auto":
				$flickerless = "0";
				break;
			case "50":
				$flickerless = "1";
				break;
			case "60":
				$flickerless = "2";
				break;
			default;
			break;
		}
		/*
		 echo "\nBefoe_brightness : ".$brightness."\n";
		echo "Befoe_flip_mirror : ".$flip_mirror."\n";
		echo "Befoe_dayNight : ".$dayNight."\n";
		echo "Befoe_flickerless : ".$flickerless."\n";
		*/
		//CGI Data set
		//$media = array_fill(0, 414, 0x00);

		//$result = requestToCamera(CMD_MEDIA_CONFIGURATION, ACTION_GET, TYPE_REQUEST, null);

		//$media = $result[1];
		$temp = array(0, 0, 0, 0);
		$cmos = array_fill(0, 120, 0x00);

		$result = requestToCamera(CMD_CMOS_CONFIGURATION, ACTION_GET, TYPE_REQUEST, $temp);

		$cmos = $result[1];

		if($brightness != null){
			$cmos[24] = $brightness;
		}
		if($flip_mirror != null){
			$cmos[72] = $flip_mirror;
		}
		if($dayNight != null){
			$cmos[96] = $dayNight;
		}
		if($flickerless != null){
			$cmos[76] = $flickerless;
		}

		$cmos[count($cmos)] = 0;
		$result = requestToCamera(CMD_CMOS_CONFIGURATION, ACTION_SET, TYPE_REQUEST, $cmos);

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
