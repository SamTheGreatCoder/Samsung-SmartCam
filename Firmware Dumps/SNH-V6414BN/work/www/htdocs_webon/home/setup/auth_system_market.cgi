<?php
define('OPENSDK_MAX_SIZE_APP_NAME', 	        60);
define('OPENSDK_MAX_SIZE_INSTALLED_DATE', 	40);

require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_menu.cgi');
require_once ('../language/language_system_authmarket.cgi');

session_start();

	$classInstances = GetClassInstance('sdk');
	$sdkSearchConf = $classInstances['SDKInfoRequest'];
	$sdkSearchConf->SetHeaderCommand(CMD_SDK_SEARCH_DETAIL);
	$sdkSearchConf->SetCGIPayload();

	$GLOBALS['SOCKET_MANAGER']->Connection($sdkSearchConf);
	
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="kr" xml:lang="kr">
<head>
	<title>iPOLiS NETWORK CAMERA WEBVIEWER</title>
	<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
	<link rel="stylesheet" type="text/css" href="../css/techwin.css" />
	<link rel="stylesheet" type="text/css" href="../css/jquery.dataTables.css">
	<style type="text/css">
	@import url("../css/jquery-ui.css");
	#dia1 .ui-dialog,#dia1 .ui-dialog,#dia1 .ui-widget, #dia1 .ui-widget-content, #dia1 .ui-corner-all, #dia1 .foo, #dia1 .ui-draggable, #dia1 .ui-resizable {background:white !important}
	#dia1 .ui-dialog .ui-dialog-titlebar{background:#3598DD !important}
	</style>

	<script type="text/javascript" src="../js/jquery-1.5.1.min.js"></script>
	<script type="text/javascript" src="../js/jquery-ui-1.8.16.custom.min.js "></script>
	<script type="text/javascript" src="../js/lnb.js"></script>
	<script type="text/javascript" src="../js/common_function.js"></script>
	<script src="../js/jquery.dataTables.min.js"></script>

	

	<script type="text/javascript" language="javascript">
<?php
	if ($classInstances['Information']->dataInfo['PasswordCheck']['value'] == 1) {
?>
		window.location.href = '../pw_change.cgi';
<?php
	}
	else if ($classInstances['Information']->dataInfo['PasswordCheck']['value'] == 2) {
?>
		alert("<?php echo $msg_change_weak_password[$GLOBALS['LANGINDEX']]; ?>");
<?php
	}
?>

	$(document).ready(function(){
	lnbonoff("lnb_event");
	SDK_APP_GetAppMarketSettings();
	
	function SDK_APP_GetAppMarketSettings()
	{
	    // get the Market Server Ip and port number from server
		var FILE_PATH = "<?php echo $GLOBALS['SDK_MARKET_APP_CONFIG_FILE_DIR'].$GLOBALS['SDK_MARKET_APP_CONFIG_FILE']; ?>";
		var msg = "";
            msg += "<GetCMD_SDK_MARKET_SERVERSETTINGS>";
            msg += "<SettingsPath>"+ FILE_PATH +"</SettingsPath>";
            msg += "</GetCMD_SDK_MARKET_SERVERSETTINGS>";
            SDKMarketGetSettingsRequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>", 'SDK', 'undefined');
	}
	function SDKMarketGetSettingsRequestAjaxMsg(msg, alertMsg, reqUrl, command, asyncVal)
	{
		if (typeof command == "undefined")	command = "";
        if (typeof asyncVal == "undefined")	asyncVal = false;
        gAlertMsg = alertMsg;
        if (BrowserDetect.browser == "Explorer" || BrowserDetect.browser == 'Firefox') {
        	reqUrl = "../.."+reqUrl.substr(reqUrl.indexOf("/cgi"));
        }
		$.ajax({
        	type: "POST",
        	async: asyncVal,
        	cache: false,
        	url: reqUrl,
        	dataType: "text",
        	data: encodeURI(msg),
        	success: OnSuccessMarketSettings
            });
	}
    function OnSuccessMarketSettings(ack)
	{
		var xml = $.parseXML(ack);
		if($(xml).find("ErrorString").text())
		{
			alert($(xml).find("ErrorString").text());
			return;
		}
		if($(xml).find("MARKETAPP").text())
		{
			var ServerIP = $(xml).find("SERVERIP").text();
			var ServerPort = $(xml).find("PORTNO").text();
			document.getElementById("marketServerIP").value = ServerIP;
			document.getElementById("marketPortNumber").value = ServerPort;

		    $.ajax({
        	type: "POST",
        	async: false,
        	cache: false,
        	url: "get_market_settings.cgi",
        	data: {'MARKET_SERVER_IP':ServerIP,'MARKET_SERVER_PORT':ServerPort}
            });
		}
	}
		$("#UpdateSettings").click(function(){

			// get the Market Server Ip and port number from server
			var FILE_PATH = "<?php echo $GLOBALS['SDK_MARKET_APP_CONFIG_FILE_DIR'].$GLOBALS['SDK_MARKET_APP_CONFIG_FILE']; ?>";
			var Market_ServerIP=document.getElementById("marketServerIP").value;
			var Market_ServerPort=document.getElementById("marketPortNumber").value;
			var msg = "";
				msg += "<SetCMD_SDK_MARKET_SERVERSETTINGS>";
				msg += "<SettingsPath>"+ FILE_PATH +"</SettingsPath>";
				msg += "<SERVERIP>"+ Market_ServerIP +"</SERVERIP>";
				msg += "<PORTNO>"+ Market_ServerPort +"</PORTNO>";
				msg += "</SetCMD_SDK_MARKET_SERVERSETTINGS>";

			if(!CheckIPv4Address()) {
			    alert("Check the Server IP");
                       	    return false;
                        }

		        if ($('#marketPortNumber').val() == "" || $('#marketPortNumber').val() == 3702 || ($('#marketPortNumber').val() > -1 && $('#marketPortNumber').val() < 80) || ($('#marketPortNumber').val() > 80 && $('#marketPortNumber').val() < 1024) || $('#marketPortNumber').val() > 65535 || !TypeCheck($('#marketPortNumber').val(), NUM)) {
		         	alert("Check the port Number.\nThe port range is between 1024 and 65535, or port 80 is also available.");
		        	return;
		        }

			SDKMarketUpdateSettingsRequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>", 'SDK', 'undefined');
		});
		
		function SDKMarketUpdateSettingsRequestAjaxMsg(msg, alertMsg, reqUrl, command, asyncVal)
		{
			if (typeof command == "undefined")	command = "";
			if (typeof asyncVal == "undefined")	asyncVal = false;
			gAlertMsg = alertMsg;
			if (BrowserDetect.browser == "Explorer" || BrowserDetect.browser == 'Firefox') {
				reqUrl = "../.."+reqUrl.substr(reqUrl.indexOf("/cgi"));
			}

			$.ajax({
				type: "POST",
				async: asyncVal,
				cache: false,
				url: reqUrl,
				dataType: "text",
				data: encodeURI(msg),
				success: OnSuccessUpdateMarketSettings
				});
		}
		
		function OnSuccessUpdateMarketSettings(ack)
		{
			alert("Update Success!");
		}

        function CheckIPv4Address()
        {
            var ipPattern = /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/;
            var ipArray 	= $('#marketServerIP').val().match(ipPattern);
        
        	if(ipArray == null) {
        		return false;
        	}
        
        	var ip_num 		= ((ipArray[1]&0xFF)<<24) + ((ipArray[2]&0xFF)<<16) + ((ipArray[3]&0xFF)<<8) + ((ipArray[4]&0xFF)<<0);
        	var thisSegment 	= ipArray[1];
        
        	if(thisSegment<1 || thisSegment>223) {
        		return false;
        	}
        
        	for(i=2; i<5; i++) {
        		thisSegment = ipArray[i];
        		if(thisSegment>255) {
        			return false;
        		}
        	}
        
        	
        
        	return true;
        }
	});	
	</script>

</head>
<body onselectstart="return false" id="dia1">

	<div id="wrap">
		<div id="head">
			<?php
				require_once ('left_menu.cgi');
				require_once ('top_menu.cgi');
			?>
			<div id="container" style="width:1500px" >
				<?php
					PrintLeftMenu($_SERVER['SCRIPT_NAME']);
				?>
				
				<div id="contents" style="width:800px" >
					<div class="h3_tit mgt0" >
						<h3 class="wid220"><?php echo $menu_market[$GLOBALS['LANGINDEX']]; ?></h3>
					</div>
					<br>
					<div style="background-color:white;width:40%;display:none;" id="meter">
						<h3 style="color:black" id='installHead'></h3>
						<meter value="0.6" Style="width:100%;" >60%</meter>	
					</div>
					<br/><br/>
					
					<form action="save_market_session.cgi" method="POST">
						<div>
							<table style="width:60%">
								<tr>
									<td style="width:30%"><?php echo $t_username[$GLOBALS['LANGINDEX']];?></td>
									<td><input type="text" id="marketUserName" name="marketUserName" class="text" style="width:80%;"/></td>
								</tr>
								<tr>
									<td style="width:30%"><?php echo $t_password[$GLOBALS['LANGINDEX']];?></td>
									<td><input type="password" id="marketPassword" name="marketPassword" class="text" style="width:80%;"/></td>
								</tr>
								<tr>
									<td style="width:30%">&nbsp;</td>
									<td style="padding-left:15%"><input type="submit" value="<?php echo $t_save[$GLOBALS['LANGINDEX']];?>" /><input type="reset" value="<?php echo $t_clear[$GLOBALS['LANGINDEX']];?>" id="clearMarketCredential" /></td>
								</tr>
							</table>
						</div>
					</form>
					
					
					<br>
					<br>
					<div class="h3_tit mgt0" >
						<h3 class="wid220"><?php echo $t_appmarketConfig[$GLOBALS['LANGINDEX']] ?></h3>
					</div>
					<br>
					<div style="background-color:white;width:40%;display:none;" id="meter">
						<h3 style="color:black" id='installHead'></h3>
						<meter value="0.6" Style="width:100%;" >60%</meter>	
					</div>
					
					<br>
					<!--<form action="save_market_session.cgi" method="POST">-->
						<div>
							<table style="width:60%">
								<tr>
									<td style="width:30%"><?php echo $t_serverIP[$GLOBALS['LANGINDEX']] ?></td>
									<td><input type="text" id="marketServerIP" name="marketServerIP" class="text" style="width:80%;" maxlength="15" onkeypress='CheckIPv4(event)' onkeydown='CheckIPv4(event)' /></td>
								</tr>
								<tr>
									<td style="width:30%"><?php echo $t_port[$GLOBALS['LANGINDEX']] ?></td>
									<td><input type="text" id="marketPortNumber" name="marketPortNumber" class="text" style="width:80%;" onkeypress="IsNum(event)" onkeydown="OnlyNUm(event);" maxlength="5"/></td>
								</tr>
								<tr>
									<td colspan="2" align="center"><input type="button" id="UpdateSettings" value="<?php echo $t_update[$GLOBALS['LANGINDEX']] ?>"/></td>
								</tr>
							</table>	
						</div>
					<!--</form>-->
					
				</div>
			</div>
		</div>
	</div>
	
</body>
</html>
