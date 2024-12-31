<?php
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";

define("OFF_EMAIL"			, 3660);
define("OFF_EMAIL_LIST"		, 128);
define("OFF_EMAIL_SERVER"	, 1408);
define("OFF_NETWORK_CHANGED", 	11709);

switch ($_SERVER['REQUEST_METHOD']) {
	case "GET":

		$result_youtube = requestToCamera(CMD_YOUTUBE_CONFIGURATION, ACTION_GET, TYPE_REQUEST, null);
		$youtube = array();

		$result_picasa = requestToCamera(CMD_PICASA_CONFIGURATION, ACTION_GET, TYPE_REQUEST, null);
		$picasa = array();

		$result_xmmp = requestToCamera(CMD_GOOGLE_CONFIGURATION, ACTION_GET, TYPE_REQUEST, null);
		$xmpp = array(); $google_users = array();

		$result_twitter = requestToCamera(CMD_TWITTER_CONFIGURATION, ACTION_GET, TYPE_REQUEST, null);
		$twitter = array();

		$result_email = requestToCamera(CMD_NETWORK_CONFIGURATION, ACTION_GET, TYPE_REQUEST, null);
		$email = array();  $email_users = array();

		if($result_youtube[0] == "OK" && $result_picasa[0] == "OK" && $result_xmmp[0] =="OK" && $result_twitter[0] == "OK" && $result_email[0] == "OK"){
			//youtube
			$youtube = $result_youtube[1];
			$youtube_enable = $youtube[0];	//Enable
			$youtube_ID = byte2str($youtube, 2, 128);	//ID
			$youtube_PW = byte2str($youtube, 130, 128);	//Password
			$youtube_mode = $youtube[258];	//Access
			//picasa
			$picasa = $result_picasa[1];
			$picasa_enable = $picasa[0];	//Enable
			$picasa_ID = byte2str($picasa, 2, 128);	//ID
			$picasa_PW = byte2str($picasa, 130, 128);	//Password
			$picasa_mode = $picasa[514];	//Access
			//google xmpp
			$xmpp = $result_xmmp[1];
			$xmpp_enable = $xmpp[0];	//Enable
			//twitter
			$twitter = $result_twitter[1];
			$twitter_enable = $twitter[0];	//Enable
			$twitter_accessToken = byte2str($twitter, 130, 128); //acessToken?????

			$email = $result_email[1];
			$email_sender = byte2str($email, OFF_EMAIL, 128);	//Sender
			$email_server = byte2str($email, (OFF_EMAIL + OFF_EMAIL_SERVER), 128);	//Server
			$email_port = byte2int($email, (OFF_EMAIL + OFF_EMAIL_SERVER + 128));	//Port
			$email_auth = $email[OFF_EMAIL + OFF_EMAIL_SERVER + 132];		//UserAuthenication
			$email_ID = byte2str($email, (OFF_EMAIL + OFF_EMAIL_SERVER + 133), 64);	//ID
			$email_PW = byte2str($email, (OFF_EMAIL + OFF_EMAIL_SERVER + 197), 64);	//Password
			$email_useSSL = $email[OFF_EMAIL + 2949];	//Use SSL
			$email_SSLport = byte2int($email, (OFF_EMAIL + 2950));		//SSL Port
			for($i=0, $j=(OFF_EMAIL + OFF_EMAIL_LIST), $k=0; $i<10; $i++, $j+=128){
				$user = byte2str($email, $j, 128);
				if($user != null && $user != ""){
					$email_users[$k++] = $user;
				}
			}

			switch ($youtube_enable){
				case "0":
					$youtube_enable = "False";
					break;
				case "1":
					$youtube_enable = "True";
					break;
				default;
				break;
			}
			switch ($youtube_mode){
				case "0":
					$youtube_mode = "public";
					break;
				case "1":
					$youtube_mode = "private";
					break;
				default;
				break;
			}

			switch ($picasa_enable){
				case "0":
					$picasa_enable = "False";
					break;
				case "1":
					$picasa_enable = "True";
					break;
				default;
				break;
			}
			switch ($picasa_mode){
				case "0":
					$picasa_mode = "public";
					break;
				case "1":
					$picasa_mode = "private";
					break;
				default;
				break;
			}

			switch ($xmpp_enable){
				case "0":
					$xmpp_enable = "False";
					break;
				case "1":
					$xmpp_enable = "True";
					break;
				default;
				break;
			}

			switch ($twitter_enable){
				case "0":
					$twitter_enable = "False";
					break;
				case "1":
					$twitter_enable = "True";
					break;
				default;
				break;
			}
				
			switch ($email_useSSL){
				case "0":
					$email_useSSL = "False";
					break;
				case "1":
					$email_useSSL = "True";
					break;
				default;
				break;
			}
			switch ($email_auth){
				case "0":
					$email_auth = "Off";
					break;
				case "1":
					$email_auth = "On";
					break;
				default;
				break;
			}
				
			$xw = new xmlWriter();
			$xw->openMemory();
			$xw->startDocument('1.0','UTF-8');
			$xw->startElement ('SNSNotification');
			$xw->startElement ('Youtube');
			$xw->writeElement ('enable', $youtube_enable);
			$xw->writeElement ('id', $youtube_ID);
			$xw->writeElement ('password', $youtube_PW);
			$xw->writeElement ('mode', $youtube_mode);
			$xw->endElement();
			$xw->startElement ('Picasa');
			$xw->writeElement ('enable', $picasa_enable);
			$xw->writeElement ('id', $picasa_ID);
			$xw->writeElement ('password', $picasa_PW);
			$xw->writeElement ('mode', $picasa_mode);
			$xw->endElement();
			$xw->startElement ('XMPP');
			$xw->writeElement ('enable', $xmpp_enable);
			$xw->endElement();
			$xw->startElement ('Twitter');
			$xw->writeElement ('enable', $twitter_enable);
			$xw->writeElement ('accessToken', $twitter_accessToken);
			$xw->endElement();
			$xw->startElement ('Email');
			$xw->writeElement ('serverAddress', $email_server);
			$xw->writeElement ('useSSL', $email_useSSL);
			if($email_useSSL == "True"){
				$xw->writeElement ('port', $email_SSLport);
			}else{
				$xw->writeElement ('port', $email_port);
			}
			$xw->writeElement ('useAuthentication', $email_auth);
			$xw->writeElement ('id', $email_ID);
			$xw->writeElement ('password', $email_PW);
			$xw->writeElement ('sender', $email_sender);
			$xw->startElement ('recipients');
			for ($i = 0; $i < count($email_users); $i++) {
				$xw->writeElement ('recipient', $email_users[$i]);
			}
			$xw->endElement();
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
		
		$youtube_enable = $parser->document->youtube[0]->enable[0]->tagData;
		$youtube_id = $parser->document->youtube[0]->id[0]->tagData;
		$youtube_password = $parser->document->youtube[0]->password[0]->tagData;
		$youtube_mode = $parser->document->youtube[0]->mode[0]->tagData;
		
		$picasa_enable = $parser->document->picasa[0]->enable[0]->tagData;
		$picasa_id = $parser->document->picasa[0]->id[0]->tagData;
		$picasa_password = $parser->document->picasa[0]->password[0]->tagData;
		$picasa_mode = $parser->document->picasa[0]->mode[0]->tagData;
		
		$xmpp_enable = $parser->document->xmpp[0]->enable[0]->tagData;
		
		$email_serverAddress = $parser->document->email[0]->serveraddress[0]->tagData;
		$email_useSSL = $parser->document->email[0]->usessl[0]->tagData;
		$email_port = $parser->document->email[0]->port[0]->tagData;
		$email_useAuthentication = $parser->document->email[0]->useauthentication[0]->tagData;
		$email_id = $parser->document->email[0]->id[0]->tagData;
		$email_password = $parser->document->email[0]->password[0]->tagData;
		$email_sender = $parser->document->email[0]->sender[0]->tagData;
		
		$email_recipient1 = $parser->document->email[0]->recipients[0]->recipient[0]->tagData;
		$email_recipient2 = $parser->document->email[0]->recipients[0]->recipient[1]->tagData;
		$email_recipient3 = $parser->document->email[0]->recipients[0]->recipient[2]->tagData;
		$email_recipient4 = $parser->document->email[0]->recipients[0]->recipient[3]->tagData;
		$email_recipient5 = $parser->document->email[0]->recipients[0]->recipient[4]->tagData;
		
		switch ($youtube_enable){
			case "False":
				$youtube_enable = 0;
				break;
			case "True":
				$youtube_enable = 1;
				break;
			default;
			break;
		}
		switch ($youtube_mode){
			case "public":
				$youtube_mode = 0;
				break;
			case "private":
				$youtube_mode = 1;
				break;
			default;
			break;
		}
		
		switch ($picasa_enable){
			case "False":
				$picasa_enable = 0;
				break;
			case "True":
				$picasa_enable = 1;
				break;
			default;
			break;
		}
		switch ($picasa_mode){
			case "public":
				$picasa_mode = 0;
				break;
			case "private":
				$picasa_mode = 1;
				break;
			default;
			break;
		}
		
		switch ($xmpp_enable){
			case "False":
				$xmpp_enable = 0;
				break;
			case "True":
				$xmpp_enable = 1;
				break;
			default;
			break;
		}
		
		switch ($email_useSSL){
			case "False":
				$email_useSSL = 0;
				break;
			case "True":
				$email_useSSL = 1;
				break;
			default;
			break;
		}
		switch ($email_useAuthentication){
			case "Off":
				$email_useAuthentication = 0;
				break;
			case "On":
				$email_useAuthentication = 1;
				break;
			default;
			break;
		}
/*
		echo "youtube_enable : ".$youtube_enable."\n";
		echo "youtube_id : ".$youtube_id."\n";
		echo "youtube_password : ".$youtube_password."\n";
		echo "youtube_mode : ".$youtube_mode."\n";
		
		echo "picasa_enable : ".$picasa_enable."\n";
		echo "picasa_id : ".$picasa_id."\n";
		echo "picasa_password : ".$picasa_password."\n";
		echo "picasa_mode : ".$picasa_mode."\n";
		
		echo "xmpp_enable : ".$xmpp_enable."\n";
		
		echo "email_serverAddress : ".$email_serverAddress."\n";
		echo "email_useSSL : ".$email_useSSL."\n";
		echo "email_port : ".$email_port."\n";
		echo "email_useAuthentication : ".$email_useAuthentication."\n";
		echo "email_id : ".$email_id."\n";
		echo "email_password : ".$email_password."\n";
		echo "email_sender : ".$email_sender."\n";
		echo "email_recipient1 : ".$email_recipient1."\n";
		echo "email_recipient2 : ".$email_recipient2."\n";
		echo "email_recipient3 : ".$email_recipient3."\n";
		echo "email_recipient4 : ".$email_recipient4."\n";
		echo "email_recipient5 : ".$email_recipient5."\n";
*/		
		//CGI Data set
		$youtube = array_fill(0, 331, 0x00);
		$picasa = array_fill(0, 579, 0x00);
		$xmpp = array_fill(0, 3529, 0x00);
		$email = array_fill(0, 11728, 0x00);

		$result_youtube = requestToCamera(CMD_YOUTUBE_CONFIGURATION, ACTION_GET, TYPE_REQUEST, null);
		$result_picasa = requestToCamera(CMD_PICASA_CONFIGURATION, ACTION_GET, TYPE_REQUEST, null);
		$result_xmmp = requestToCamera(CMD_GOOGLE_CONFIGURATION, ACTION_GET, TYPE_REQUEST, null);
		$result_email = requestToCamera(CMD_NETWORK_CONFIGURATION, ACTION_GET, TYPE_REQUEST, null);
		$memList = array();

		$youtube = $result_youtube[1];
		$youtube[0] = $youtube_enable;
		str2byte($youtube, $youtube_id, 2, 128);		//ID
		str2byte($youtube, $youtube_password, 130, 128);		//Password
		$youtube[258] = $youtube_mode;
		
		$picasa = $result_picasa[1];
		$picasa[0] = $picasa_enable;
		str2byte($picasa, $picasa_id, 2, 128);		//ID
		str2byte($picasa, $picasa_password, 130, 128);		//Password
		$picasa[514] = $picasa_mode;
		
		$xmpp = $result_xmmp[1];
		$xmpp[0] = $xmpp_enable;
		
		$email = $result_email[1];
		str2byte($email, $email_sender, OFF_EMAIL, 128);									//Sender
		str2byte($email, $email_serverAddress, (OFF_EMAIL + OFF_EMAIL_SERVER), 128);				//Server
		
		$email[OFF_EMAIL + OFF_EMAIL_SERVER + 132] = $email_useAuthentication;				//UserAuthenication
		str2byte($email, $email_id, (OFF_EMAIL + OFF_EMAIL_SERVER + 133), 64);		//ID
		str2byte($email, $email_password, (OFF_EMAIL + OFF_EMAIL_SERVER + 197), 64);		//Password
		$email[OFF_EMAIL + 2949] = $email_useSSL;									//Use SSL
		if($email_useSSL == 0){
			int2byte($email, $email_port, (OFF_EMAIL + OFF_EMAIL_SERVER + 128));	//Port
		}else{
			int2byte($email, $email_port, (OFF_EMAIL + 2950));						//SSL Port
		}
		for($i=0, $j=(OFF_EMAIL + OFF_EMAIL_LIST); $i<10; $i++, $j+=128){					//Members
			str2byte($email, "", $j, 128);
		}
		
		$memList[0] = $email_recipient1;
		$memList[1] = $email_recipient2;
		$memList[2] = $email_recipient3;
		$memList[3] = $email_recipient4;
		$memList[4] = $email_recipient5;
		
		for($i=0, $j=(OFF_EMAIL + OFF_EMAIL_LIST); $i<count($memList); $i++, $j+=128){
			if($memList[$i] != null&& trim($memList[$i]) != ""){
				str2byte($email, $memList[$i], $j, 128);
			}
		}
		
		$email[OFF_NETWORK_CHANGED] = 1; //20120207_lcy added change field
		
		$result_youtube = requestToCamera(CMD_YOUTUBE_CONFIGURATION, ACTION_SET, TYPE_REQUEST, $youtube);
		$result_picasa = requestToCamera(CMD_PICASA_CONFIGURATION, ACTION_SET, TYPE_REQUEST, $picasa);
		$result_xmpp = requestToCamera(CMD_GOOGLE_CONFIGURATION, ACTION_SET, TYPE_REQUEST, $xmpp);
		$result_email = requestToCamera(CMD_NETWORK_CONFIGURATION, ACTION_SET, TYPE_REQUEST, $email);
		
		if($result_youtube[0] == "OK" && $result_picasa[0] == "OK" && $result_xmpp[0] == "OK" && $result_email[0] == "OK"){
			//echo "OK";
		}else{
			//echo "NOK;" . $result_email[1];
			header("HTTP/1.1 501 Not Implemented");
		}
		break;

	default:
		header("HTTP/1.1 404 Not Found");
		break;
}

?>
