<?php
define('OPENSDK_MAX_SIZE_APP_NAME', 	        60);
define('OPENSDK_MAX_SIZE_INSTALLED_DATE', 	40);

require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_system_appmarket.cgi');
require_once ('../language/language_menu.cgi');
require_once ('SDKErrorCodes.cgi');

session_start();

$username = $_SESSION["marketUserName"];
$password = $_SESSION["marketPassword"];
$ServerIp = $_SESSION["MARKET_SERVER_IP"];
$ServerPort = $_SESSION["MARKET_SERVER_PORT"];

$classInstances = GetClassInstance('sdk');
$sdkSearchConf = $classInstances['SDKInfoRequest'];
$sdkSearchConf->SetHeaderCommand(CMD_SDK_SEARCH_DETAIL);
$sdkSearchConf->SetCGIPayload();

$GLOBALS['SOCKET_MANAGER']->Connection($sdkSearchConf);

if($username == null && $password == null){
		header("Location: ./auth_system_market.cgi");
}
	
function cURLcheckBasicFunctions()
{
  if( !function_exists("curl_init") &&
      !function_exists("curl_setopt") &&
      !function_exists("curl_exec") &&
      !function_exists("curl_close") ) return false;
  else return true;
}

function getAppsInfo()
{
    
    //$url="http://".$_SESSION["MARKET_SERVER_IP"].":".$_SESSION["MARKET_SERVER_PORT"]."/market/spring/appservice/allapps";
	$url="http://".$_SESSION["MARKET_SERVER_IP"].":".$_SESSION["MARKET_SERVER_PORT"]."/market/spring/appservice/allapps";
	
	//$url="http://107.108.212.43:8081/market/spring/appservice/allapps";
	
	$marketUsername=$_SESSION["marketUserName"];
	//$marketUsername="admin";
	$marketPassword=$_SESSION["marketPassword"];
	//$marketPassword="admin";
	
	// Make the request
	$response = null;
	if($marketUsername != null && $marketPassword != null){
		$context = stream_context_create(array(
				'http' => array('header'  => "Authorization: Basic " . base64_encode("$marketUsername:$marketPassword")
		)));
		$response = @file_get_contents($url,false,$context);
	}
	//syslog(LOG_INFO,$http_response_header);	
	// Retrieve HTTP status code
	list($version,$status_code,$msg) = explode(' ',$http_response_header[0], 3);

	// Check the HTTP Status code
	switch($status_code) {
		case 200:
			$json_array = array("status" => $status_code,"msg" => $response);
			return json_encode($json_array);
			break;
		default:
			$_SESSION["marketUserName"] = null;
			$_SESSION["marketPassword"] = null;
			$json_array = array("status" => $status_code,"msg" => $msg);
			return json_encode($json_array);
	}
}

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
	<script type="text/javascript" src="../js/jquery.raty.js"></script>
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
	lnbonoff("lnb_system");
	var MAX_APP_PERMISSIONS = 32; // 32 bits
	// Define ERROR CODES map here
	var SDK_ERROR_CODES_MAP = <?php echo json_encode($SDK_ERROR_CODES_MAP);?>;
	
	// Define Permissions map here
	var APP_PERMISSION_CODES = 
	{
		0: 'Permissions None',  // NONE
		1: 'Device',            // Bit 0(LSB) is set
		2: 'PTZ',               // Bit 1 is set
		4: 'Network',           // Bit 2 is set
		8: 'SDCard'             // Bit 3 is set
	};
	var APP_NAME = "";
	var MARKET_SERVER_IP = "";
	var MARKET_SERVER_PORT = "";

	
	var response= <?php echo getAppsInfo();?>;

	console.log("Response:: ",response);
	
	if(response["status"] == "200"){

		var oTable = $('#installed_apps_list').dataTable( {
			"aaData": JSON.parse(response["msg"]),
			"bProcessing": true,
			"bAutoWidth": false,
			"bFilter": false,
			"bPaginate": false,
			"sScrollY": "520px",
			"aoColumns": [
				{
					"mDataProp": "name",
					"sTitle": "<?php echo $t_appName[$GLOBALS['LANGINDEX']]?>",
					"sClass": "left",
					"sWidth": "150px",
				},
				{
					"mDataProp": "description",
					"sTitle": "<?php echo $t_description[$GLOBALS['LANGINDEX']]?>",
					"sClass": "center",
				},
				{
					"mDataProp": "rating",
					"sTitle": "<?php echo $t_rating[$GLOBALS['LANGINDEX']]?>",
					"sWidth": "100px",
					"sClass": "left",
					"fnRender": function(obj) {
						var sReturn = obj.aData[ "rating" ];
						console.log("sReturn " , sReturn, " obj ", obj);
						var returnButton = '<div class="rateit" data-rateit-value="'+sReturn+'" ></div>';
						return returnButton;
					}
				},
				{
					"mDataProp": "id", 
					"sTitle": "",
					"sClass": "left",
					"fnRender": function(obj) {
									  
						console.log("obj",obj );

						var version= obj.aData["version"];
						//version=version.toFixed(1);
						var appNameCheck = obj.aData["name"];
						var flag = false;
						<?php
							for ($index=0; $index < $sdkSearchConf->dataInfo['max_apps_count']['value']; $index++){
								$rawAppName = $sdkSearchConf->sdk_app[$index]->dataInfo['app_name']['value'];
								//$version = $sdkSearchConf->sdk_app[$index]->dataInfo['app_major_version']['value'].".".$sdkSearchConf->sdk_app[$index]->dataInfo['app_minor_version']['value'];
							        $version = $sdkSearchConf->sdk_app[$index]->dataInfo['app_version']['value'];
								$version = trim($version);
								$AppNameLength = 0;
								for ($i = 0; $i < OPENSDK_MAX_SIZE_APP_NAME; $i++){
									/* below code is commented as ctype is not available /*
									/*if(substr($rawAppName, $i, 1) == "_" || ctype_space(substr($rawAppName, $i, 1)) || ctype_alnum(substr($rawAppName, $i, 1))){
										$AppNameLength += 1;
										continue;
									}*/
									break;
								}
								//$AppName = substr($rawAppName, 0, $AppNameLength);
								//$AppName = substr($rawAppName, 0);
								$AppName = trim($rawAppName);

						?>
						var App_Name1 = "<?php echo $AppName;?>";
						var App_Version1 = <?php echo $version;?>;
						if(appNameCheck ==   App_Name1){
							flag=true;
							if(parseFloat( version) > parseFloat(App_Version1) ){							 
								return '<input class="downloadButton" type="button" style="width:75px" value="<?php echo $t_upgrade[$GLOBALS['LANGINDEX']]?>" appId='+obj.aData[ "id" ]+' appName='+obj.aData[ "name" ]+' />';
							}else if( parseFloat(App_Version1) == parseFloat( version)){
								return '<input class="downloadButton" type="button" style="width:75px" value="<?php echo $t_install[$GLOBALS['LANGINDEX']]?>" appId='+obj.aData[ "id" ]+' appName='+obj.aData[ "name" ]+' disabled/>';
							}else{
								return '<input class="downloadButton" type="button" style="width:75px" value="<?php echo $t_install[$GLOBALS['LANGINDEX']]?>" appId='+obj.aData[ "id" ]+' appName='+obj.aData[ "name" ]+' />';
							}
						}else{
							flag=false;
						}
						<?php
						}
						?>
						if(flag==false)
							 return   '<input class="downloadButton" type="button" style="width:75px" value="<?php echo $t_install[$GLOBALS['LANGINDEX']]?>" appId='+obj.aData[ "id" ]+' appName='+obj.aData[ "name" ]+' />';
					}
				}
			]
		} );
	}else{
		if(response["status"]==null){
			alert("<?php echo $msg_err[$GLOBALS['LANGINDEX']]?> "+"<?php echo $msg_comm_err[$GLOBALS['LANGINDEX']]?>");
		}else{
			alert("<?php echo $msg_err[$GLOBALS['LANGINDEX']]?> "+response["status"]+":"+response["msg"]);
			parent.window.location.reload(true);
		}
	}

	$('.rateit').raty({
		path:"../images/setup",
		readOnly:true,
		score:function(){
			return $(this).attr("data-rateit-value");
		}
	});

	$("body").delegate("#logoutbutton","click",function(){
		window.location="remove_market_session.cgi";
	});

	$("body").delegate(".downloadButton", "click", function() {
		var msg ="";
		var appId=$(this).attr("appId");
		APP_NAME = $(this).attr("appName");
	

		
	var val = $(this).val();
	
	var labelVal='';
	
	if(val=='install'){
	labelVal="installing..";
	}else if(val=='upgrade'){
	labelVal="updating..";
	}

	var meterHead= document.getElementById("installHead");
	meterHead.innerHTML=labelVal;

		//alert('Appname '+appName);
		//alert('AppId '+appId);
		msg += "<SetCMD_SDK_MARKET>";
		msg += "<AppName>"+APP_NAME+"</AppName>";
		//msg += "<Data>"+"http://107.108.205.195:8080/market/spring/appservice/download/"+appId+"</Data>";
		//msg += "<Data>"+"http://107.108.212.43:8081/market/spring/appservice/download/"+appId+"</Data>";
		msg += "<Data>"+"http://"+"<?php echo $_SESSION["MARKET_SERVER_IP"]?>"+":"+"<?php echo $_SESSION["MARKET_SERVER_PORT"]?>"+"/market/spring/appservice/download/"+appId+"</Data>";
		msg += "</SetCMD_SDK_MARKET>";
		//alert(msg);

		SDKMarket_DownloadAppRequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>", 'CMD_SDK_MARKET', 'undefined');
	});
	function SDKMarket_DownloadAppRequestAjaxMsg(msg, alertMsg, reqUrl, command, asyncVal)
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
			data: encodeURIComponent(msg),
			success: function(successMsg){
				var xml = $.parseXML(successMsg);
				//console.log(xml);
				APP_NAME = $(xml).find("AppName").text();
				//console.log(appName);
				if($(xml).find("Status").text() == "OK")
                                {
					var msg = "";
					msg += "<AddSDK>";
					msg += "<AppName>"+APP_NAME+"</AppName>";
					msg += "<AppUploadPath>" + "<?php echo $GLOBALS['SDK_MARKET_APP_DIRECTORY']; ?>" + "</AppUploadPath>";
					msg += "</AddSDK>";
					SDKUploadRequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>", 'SDK', 'undefined');
				}
                                else
                                {
					alert($(xml).find("ErrorString").text());
				}
			},
			error: function(errorMsg)
                        {
        			var xml = $.parseXML(errorMsg);
        			console.log(xml);
			}
		});
	}
	
	function SDKUploadRequestAjaxMsg(msg, alertMsg, reqUrl, command, asyncVal)
	{
		if (typeof command == "undefined")	command = "";
		if (typeof asyncVal == "undefined")	asyncVal = false;
		gAlertMsg = alertMsg;
		if (BrowserDetect.browser == "Explorer" || BrowserDetect.browser == 'Firefox') {
			reqUrl = "../.."+reqUrl.substr(reqUrl.indexOf("/cgi"));
		}
	var meter= document.getElementById("meter");
	
	
	var buttonElm= document.getElementsByClassName('downloadButton');
	console.log('buttonElm',buttonElm);

	
	meter.style.display="block";
	
		$.ajax({
			type: "POST",
			async: asyncVal,
			cache: false,
			url: reqUrl,
			dataType: "text",
			data: encodeURIComponent(msg),
			success: OnSuccessUpload
		});
	}

	function OnSuccessUpload(successMsg)
	{
		var msg = "";
		var xml = $.parseXML(successMsg);
		var Is_valid_error_code = $(xml).find("ErrorCode").text();
		
			
			

		if(Is_valid_error_code != "")
		{
		var meter= document.getElementById("meter");
		meter.style.display="none";
		  var error_code = parseInt(Is_valid_error_code);
		  msg += "<?php echo $msg_upload_err[$GLOBALS['LANGINDEX']]?> : "+SDK_ERROR_CODES_MAP[error_code];
		  alert(msg);
		}
		else
		{
			var xml = $.parseXML(successMsg);
			var permissions = parseInt($(xml).find("AddResult").text());
			var permissionsMsg = "<?php echo $msg_permission[$GLOBALS['LANGINDEX']]?> : "+ "\n";
			var result = 0;
			if(0 == permissions)
			{
			  permissionsMsg += (APP_PERMISSION_CODES[result] + "\n");
			}
			else
			{
				for(i=0; i<MAX_APP_PERMISSIONS; i++)
				{
				   result = permissions & (1<<i);
				   if(0 == result)
						continue;

				  permissionsMsg += (APP_PERMISSION_CODES[result] + "\n");
				}
			}
			permissionsMsg += "<?php echo $msg_permissiontail[$GLOBALS['LANGINDEX']]?>";

			var confirm_result;
			confirm_result = confirm(permissionsMsg);
			if (confirm_result == true)
			{
				msg += "<SetSDK>";
				msg += "<AppName>"+APP_NAME+"</AppName>";
				msg += "</SetSDK>";
				SDKInstallRequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>", 'SDK', 'undefined');
				//return;
			}else{
				var meter= document.getElementById("meter");
				meter.style.display="none";
			}
			
		}
	}

	function SDKInstallRequestAjaxMsg(msg, alertMsg, reqUrl, command, asyncVal)
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
			data: encodeURIComponent(msg),
			success: function(successMsg){
				var msg = "";
				var xml = $.parseXML(successMsg);
				var Is_valid_error_code = $(xml).find("ErrorCode").text();
				var meter= document.getElementById("meter");
				meter.style.display="none";
				if(Is_valid_error_code != ""){
				
					  var error_code = parseInt(Is_valid_error_code);
					  msg += "<?php echo $msg_install_err[$GLOBALS['LANGINDEX']]?> : "+SDK_ERROR_CODES_MAP[error_code];
					  alert(msg);
				}
				else{
					   msg += "<?php echo $msg_install_success[$GLOBALS['LANGINDEX']]?>";
					   alert(msg);
					   location.reload();
				}
				
			}
		});
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
						<img src="../images/opensdk/loader.gif" />	
					</div>
					<?php
						if($_SESSION["marketUserName"]!=null && $_SESSION["marketPassword"]!=null){
					?>
					<div style="float:right"><button type="button" style="width:75px;height:30px" id="logoutbutton"><?php echo $t_logout[$GLOBALS['LANGINDEX']]; ?></button></div>
					<?php
					}
					?>
					<br/><br/>
					<table id="installed_apps_list">
					</table>
				</div>
			</div>
		</div>
	</div>
	
</body>
</html>
