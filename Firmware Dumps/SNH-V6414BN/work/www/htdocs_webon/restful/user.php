<?php
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";

switch ($_SERVER['REQUEST_METHOD']) {
	case "GET":

		$result = requestToCamera(CMD_USER, ACTION_GET_ALL, TYPE_REQUEST, null);

		$error = "";
		if($result[0] == "OK"){

			$id = byte2str($result[1], 1, 16); //name
			$password = byte2str($result[1], 17, 16); //password
			$level = byte2int($result[1], 33); //level

			switch ($level){
				case "0":
					$level = "Admin";
					break;
				case "1":
					$level = "User";
					break;
				case "2":
					$level = "Guest";
					break;
				default;
				break;
			}

			$xw = new xmlWriter();
			$xw->openMemory();
			$xw->startDocument('1.0','UTF-8');
			$xw->startElement ('User');
			$xw->writeElement ('id', $id);
			$xw->writeElement ('password', $password);
			$xw->writeElement ('level', $level);
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
		$password = $parser->document->password[0]->tagData;

		//echo "microphone : ".$microphone."\n";
		//echo "speaker : ".$speaker."\n";

		//CGI Data set
		$users = array_fill(0, 280, 0x00);
		$user = array_fill(0, 280, 0x00);

		$result = requestToCamera(CMD_USER, ACTION_GET_ALL, TYPE_REQUEST, null);

		$users = $result[1];
		$user = array_slice($users, 0 , 40);

		if($password != null){
			str2byte($user, $password, 17, 16);
		}
		//echo count($result[1]);
		//echo count($user);
		$result = requestToCamera(CMD_USER, ACTION_SET, TYPE_REQUEST, $user);
			
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
