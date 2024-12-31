<?php
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/datetime_constant.php";

switch ($_SERVER['REQUEST_METHOD']) {
	case "GET":

		$result = requestToCamera(CMD_VA_CONFIGURATION, ACTION_GET, TYPE_REQUEST, null);

		$motion = array_fill(0, 2113, 0x00);
		$motion_enable = 0; $motion_sens = 2; $time_act = 0; $audio_enable = 0; $audio_sens = 2;
		if($result[0] == "OK"){

			$motion = $result[1];

			$motion_sens = $motion[4];				//Motion-Sensitivity
			$audio_sens = ($motion[2056] + 1);		//Audio-Sensitivity

			$motion_enable = $motion[1]; 			//Motion-Enabled
			if($motion_enable == 0){
				$motion_sens = 0;
			}
			$audio_enable = $motion[2055];  		//Audio-Enabled
			if($audio_enable == 0){
				$audio_sens = 0;
			}
			
			$xw = new xmlWriter();
			$xw->openMemory();
			$xw->startDocument('1.0','UTF-8');
			$xw->startElement ('Detection');
			$xw->writeElement ('audioSensitivity', $audio_sens);
			$xw->writeElement ('motionSensitivity', $motion_sens);
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
		$audioSensitivity = $parser->document->audiosensitivity[0]->tagData;
		$motionSensitivity = $parser->document->motionsensitivity[0]->tagData;
	
		echo "audiosensitivity : ".$audioSensitivity."\n";
		echo "motionsensitivity : ".$motionSensitivity."\n";
	

		$motion = array_fill(0, 2113, 0x00);
		$result = requestToCamera(CMD_VA_CONFIGURATION, ACTION_GET, TYPE_REQUEST, null);
		$motion = $result[1];

		$motion_enable = $motion[1]; 			//Motion-Enabled
		$audio_enable = $motion[2055];  		//Audio-Enabled
		
		if($audioSensitivity == null && $audio_enable != 0){
			$audioSensitivity = ($motion[2056] + 1);	
		}
		
		if($motionSensitivity == null && $motion_enable != 0){
			$motionSensitivity = $motion[4];	
		}
		
		//CGI Data set
		if($audioSensitivity != 0){
			$motion[2055] = 1;	//Audio-Enabled
			$audioSensitivity = ($audioSensitivity > 5)? 5 : $audioSensitivity;
			$motion[2056]  = $audioSensitivity-1;	//Audio-Sensitivity
		}else if($audioSensitivity == 0){
			$motion[2055] = 0;	//Audio-Enabled
		}
		
		if($motionSensitivity != 0){
			$motion[1] = 1;	//Motion-Enabled
			$motionSensitivity = ($motionSensitivity > 5)? 5 : $motionSensitivity;
			$motion[4] = $motionSensitivity;	//Motion-Sensitivity
		}else if($motionSensitivity == 0){
			$motion[1] = 0;	//Motion-Enabled
		}

		$result = requestToCamera(CMD_VA_CONFIGURATION, ACTION_SET, TYPE_REQUEST, $motion);
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
