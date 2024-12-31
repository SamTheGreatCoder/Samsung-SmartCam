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
			$xw->startElement ('Users');
			$xw->startElement ('User');
			$xw->writeElement ('id', $id);
			$xw->writeElement ('password', $password);
			$xw->writeElement ('level', $level);
			$xw->endElement();
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
