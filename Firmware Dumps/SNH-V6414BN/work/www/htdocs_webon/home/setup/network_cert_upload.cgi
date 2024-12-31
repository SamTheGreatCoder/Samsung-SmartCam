<?php
//require_once ('authorization.cgi');
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../../cgi-bin/adv/https.class');
require_once ('stw_util.cgi');

$action = $_POST["action"];
if($action == "Install") {
 	//Call Install function.
 	installCertificate();
} else if ($action == "Delete") {
	//Call delete function.
	deleteCertificate();
}

function deleteCertificate() {
    $certtype = $_POST["certType"];
    
    //$msg = "<RemoveData802Dot1x><PublicCertType>" . $certtype . "</PublicCertType></RemoveData802Dot1x>";

	$socketManager = new SocketManager();
	$conf = new Data802Dot1x(ACTION_REMOVE);
	$conf->payload = pack('c1', $certtype);

	$socketManager->Connection($conf);
    
    /*$myresult = sendStwRequest($msg);
    
	if ($myresult === false) {
	     echo "failure";
	} else {*/
	     echo "success";
	//}
}

function installCertificate() {

	if  ($_FILES["certificateFile"]["error"] > 0) {
		echo "Error: " . $_FILES["certificateFile"]["error"] . "<br>";
		return;
	} else {
		$name = $_FILES["certificateFile"]["name"];
       		$certificate_data = file_get_contents($_FILES['certificateFile']['tmp_name']);
	}
	
	$certificateType = $_POST["certType"];

	$socketManager = new SocketManager();
	$conf = new Data802Dot1x(ACTION_SET);
	$conf->payload = 
			pack('c1', $certificateType).
			pack('i1', strlen($certificate_data)).
			pack('A'.strlen($certificate_data), $certificate_data);

	$socketManager->Connection($conf);
	
	/*$msg = "<SetData802Dot1x><PublicCertType>" . $certificateType . "</PublicCertType><CertLength>" . strlen($certificate_data) .
		"</CertLength><CertData>" . urlencode($certificate_data) . "</CertData>" . "</SetData802Dot1x>" ;
				
    	$myresult = sendStwRequest($msg);
    
	if ($myresult === false) {
	     echo "failure";
	} else {*/
	     echo "success";
	//}
}


?>
