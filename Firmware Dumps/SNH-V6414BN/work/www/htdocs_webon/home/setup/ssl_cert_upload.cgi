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

function deleteCertificate()
{
   $certname = $_POST["certificateName"];
   //$msg = "<RemoveHTTPSData><PublicCertName>" . urlencode($certname) . "</PublicCertName></RemoveHTTPSData>";

   $socketManager = new SocketManager();
	$conf = new HTTPSData(ACTION_REMOVE);
	$conf->payload = pack('a32', $certname);

	$socketManager->Connection($conf);

   /*$myresult = sendStwRequest($msg);
    
	if ($myresult === false) {
	     echo "failure";
	} else {*/
	     echo "success";
	//}
}

function installCertificate()
{
	if ($_FILES["certificateFile"]["error"] > 0) {
		echo "Error: " . $_FILES["certificateFile"]["error"] . "<br>";
		return;
	} else {
		$name = $_FILES["certificateFile"]["name"];
       		$certificate_data = file_get_contents($_FILES['certificateFile']['tmp_name']);
	}
	
	if ($_FILES["keyFile"]["error"] > 0) {
		echo "Error: " . $_FILES["keyFile"]["error"] . "<br>";
		return;
	} else {
		$name = $_FILES["keyFile"]["name"];
		$keyFile_data = file_get_contents($_FILES['keyFile']['tmp_name']);
	}
	
	$certificateName = $_POST["certificateName"];

	$socketManager = new SocketManager();
	$conf = new HTTPSData(ACTION_SET);
	$conf->payload = pack('a32', $certificateName).
			pack('i1', strlen($certificate_data)).
			pack('A'.strlen($certificate_data), $certificate_data).
			pack('i1', strlen($keyFile_data)).
			pack('A'.strlen($keyFile_data), $keyFile_data);

	$socketManager->Connection($conf);
	
	/*$msg = "<SetHTTPSData><PublicCertName>" . urlencode($certificateName) . "</PublicCertName><CertLength>" . strlen($certificate_data) .
		"</CertLength><CertData>" . urlencode($certificate_data) . "</CertData>" . "<KeyLength>" . strlen($keyFile_data) .
		"</KeyLength><KeyData>" . urlencode($keyFile_data) . "</KeyData></SetHTTPSData>" ;
				
  	$myresult = sendStwRequest($msg);
    
	if ($myresult === false) {
	     echo "failure";
	} else {*/
	     echo "success";
	//}
}

?>
