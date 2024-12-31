<?php
//require_once ('authorization.cgi');
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../../cgi-bin/adv/backup.class');

require_once ('stw_util.cgi');

if  ($_FILES["restoreFile"]["error"] > 0) {
	echo "Error: " . $_FILES["restoreFile"]["error"] . "<br>";
	return;
} else {
	$name = $_FILES["restoreFile"]["name"];
	$file_data = file_get_contents($_FILES['restoreFile']['tmp_name']);
	
	$base64_encoded_data = base64_encode($file_data);        
	$string_len = strlen($base64_encoded_data);

	if($string_len > 1000000) {
	    echo "filesizelimitexceeded";
	    return;
	}
	$socketManager = new SocketManager();
	$backupConf = new ConfigurationData(ACTION_SET);
	$backupConf->payload = pack('A'.strlen($file_data), $file_data);

	$socketManager->Connection($backupConf);

	/*

	$url_encoded_data = urlencode($base64_encoded_data);  	
	$_sendrequest = "<RestoreConfiguration><Data>" . $url_encoded_data . "</Data></RestoreConfiguration>";	

	//echo "url " . $url;
	//print_r($requestHeaders);
	
	//echo "_sendrequest " . $_sendrequest;

	$result = sendStwRequest($_sendrequest);

	if ($result === false) {
	     echo "failure";
	} else {*/
	     echo "success";
	//}
}

?>
