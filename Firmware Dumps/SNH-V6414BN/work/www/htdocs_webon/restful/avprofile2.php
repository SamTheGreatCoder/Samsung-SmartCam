<?php
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";

define("OFF_NETWORK"	, 230);
define("OFF_VideoConfig"	, 402);
define("OFF_AudioConfig"	, 2980);

switch ($_SERVER['REQUEST_METHOD']) {
	case "GET":

		$result = requestToCamera(CMD_PROFILE_CONFIGURATION, ACTION_GET, TYPE_REQUEST, null);
		$result_name = requestToCamera(CMD_PROFILE, ACTION_GET, TYPE_REQUEST, null);
		$result_network = requestToCamera(CMD_NETWORK_CONFIGURATION, ACTION_GET, TYPE_REQUEST, null);
		$fromdhcp = 0; $dns1 = array(); $dns2 = array(); $ipAddress = array(); $dhcp_static = 0;
		if($result[0] == "OK" && $result_name[0] =="OK" && $result_network[0] =="OK"){

			$xw = new xmlWriter();
			$xw->openMemory();
			$xw->startDocument('1.0','UTF-8');


			$name = byte2str($result_name[1], 708, 64);

			$encoding = $result[1][OFF_VideoConfig+129+298];
			$x = byte2int($result[1], OFF_VideoConfig+130+298);
			$y = byte2int($result[1], OFF_VideoConfig+134+298);
			$framlate= byte2int($result[1], OFF_VideoConfig+139+298);
			$bitrate = byte2int($result[1], OFF_VideoConfig+147+298);

			$govLength = byte2int($result[1], OFF_VideoConfig+159+298);
			$codecProfile = $result[1][OFF_VideoConfig+163+298];

			$audio_encoding = $result[1][OFF_VideoConfig+OFF_AudioConfig+129];
			$audio_bitrate = byte2int($result[1], OFF_VideoConfig+OFF_AudioConfig+130);
			$audio_samplerate = byte2int($result[1], OFF_VideoConfig+OFF_AudioConfig+134);

			switch ($encoding){
				case "0":
					$encoding = "JPEG";
					break;
				case "1":
					$encoding = "MPEG4";
					break;
				case "2":
					$encoding = "H264";
					break;
				default;
				break;
			}
			switch ($codecProfile){
				case "0":
					$codecProfile = "Baseline";
					break;
				case "1":
					$codecProfile = "Main";
					break;
				case "2":
					$codecProfile = "Extended";
					break;
				case "3":
					$codecProfile = "High";
					break;
				default;
				break;
			}

			switch ($audio_encoding){
				case "0":
					$audio_encoding = "G711";
					break;
				case "1":
					$audio_encoding = "G726";
					break;
				case "2":
					$audio_encoding = "AAC";
					break;
				default;
				break;
			}

			$fromdhcp = $result[1][OFF_NETWORK+84]; //DHCP?
			$ipAddress[0] = byte2str($result_network[1], OFF_NETWORK+85, 16);	//Static ip
			$ipAddress[1] = byte2str($result_network[1], OFF_NETWORK+105, 16);	//DHCP ip

			if($fromdhcp == 1){
				$dhcp_static = 0;
			}else{
				$dhcp_static = 1;
			}

			$xw->startElement ('AVProfile');
			$xw->writeElement ('id', 2);
			$xw->writeElement ('name', $name);
			$xw->startElement ('Video');
			$xw->writeElement ('codec', $encoding);
			$xw->writeElement ('resolution', $x.",".$y);
			$xw->writeElement ('framRateLimit', $framlate/1000);
			$xw->writeElement ('bitRateLimit', $bitrate/1024);
			if ($encoding == "H264") {
				$xw->startElement ('H264');
				$xw->writeElement ('govLength', $govLength);
				$xw->writeElement ('profile', $codecProfile);
				$xw->endElement();
			}
			$xw->endElement();

			$xw->startElement ('Audio');
			$xw->writeElement ('codec', $audio_encoding);
			$xw->writeElement ('bitRate', $audio_bitrate/1024);
			$xw->writeElement ('sampleRate', $audio_samplerate);
			$xw->endElement();
			$xw->writeElement ('streamURI', "rtsp://$ipAddress[$dhcp_static]/profile2/media.smp");
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
