<?php
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";

switch ($_SERVER['REQUEST_METHOD']) {
	case "GET":

		$result = requestToCamera(CMD_MEDIA_CONFIGURATION, ACTION_GET, TYPE_REQUEST, null);

		$media = array_fill(0, 414, 0x00);
		$audio_mic = 3; $audio_spk = 5;
		if($result[0] == "OK"){
			$media = $result[1];
			$audio_mic = byte2int($media, 212);		//Audio_mic
			$audio_mic = ($audio_mic > 3)? 3 : $audio_mic;
			$audio_spk = byte2int($media, 282);		//Audio_spk
				
			$xw = new xmlWriter();
			$xw->openMemory();
			$xw->startDocument('1.0','UTF-8');
			$xw->startElement ('Audio');
			$xw->writeElement ('microphone', $audio_mic);
			$xw->writeElement ('speaker', $audio_spk);
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
		$microphone = $parser->document->microphone[0]->tagData;
		$speaker = $parser->document->speaker[0]->tagData;

		//echo "microphone : ".$microphone."\n";
		//echo "speaker : ".$speaker."\n";

		//CGI Data set
		$media = array_fill(0, 414, 0x00);

		$result = requestToCamera(CMD_MEDIA_CONFIGURATION, ACTION_GET, TYPE_REQUEST, null);

		$media = $result[1];
		if($microphone != null){
			$media[212] = $microphone;
		}
		if($speaker != null){
			$media[282] = $speaker;
		}

		$result = requestToCamera(CMD_MEDIA_CONFIGURATION, ACTION_SET, TYPE_REQUEST, $media);
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