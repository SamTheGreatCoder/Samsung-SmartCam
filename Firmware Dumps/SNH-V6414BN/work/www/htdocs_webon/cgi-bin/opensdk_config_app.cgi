<?php
require_once ('./adv/_define.inc');
//CheckAdminAccount(FA);
//http://107.108.217.226/cgi-bin/opensdk_config_app.cgi?AppName=NWCameraSW


	if (!isset($_REQUEST['AppName'])) return FALSE;
	$app_name = $_REQUEST['AppName'];


	require_once ('./adv/sdk.class');
	$sdkSearchConf = new SDKInfoRequest(ACTION_GET);
	error_log("Appname from arguments list is".$app_name);
	$sdkSearchConf->dataInfo['AppName']['value'] = $app_name;
	$sdkSearchConf->payload = MakePayload($sdkSearchConf->dataInfo);
	$socketManager = new SocketManager();
	$socketManager->Connection($sdkSearchConf);
	
	error_log("App date ". $sdkSearchConf->sdk_app->dataInfo['installed_date']['value']); 

//ResponseText(TRUE);
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
	<title>iPOLiS NETWORK CAMERA</title>
	<link rel="stylesheet" type="text/css" href="../css/techwin.css" />

        <link href="style/style.css" rel="stylesheet" type="text/css" />
	<script type="text/javascript" src="../js/jquery-1.10.0.min.js"></script>
	<script type="text/javascript" src="../js/lnb.js"></script>
	<script type="text/javascript" src="../js/board.js"></script>
	<script type="text/javascript" src="../js/common_function.js"></script>
	<script type="text/javascript">
	$(document).ready(function(){
			lnbonoff(0);
	});
    </script>

    <script type="text/javascript">
    function OnLoad()
	{
		//alert("");
		alert("<?php echo $sdkSearchConf->sdk_app->dataInfo['installed_date']['value'];?>");
	}
    </script>
</head>
<body onload="OnLoad()">
	
	
</body>

