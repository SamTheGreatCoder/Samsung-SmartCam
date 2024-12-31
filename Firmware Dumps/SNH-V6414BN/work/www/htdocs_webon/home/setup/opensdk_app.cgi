<?php
// Application Status
define('OPENSDK_APP_INSTALL_FAILED', 		-1);  // Currently not handled
define('OPENSDK_APP_UN_INSTALLED', 		0);   // Currently not handled
define('OPENSDK_APP_UN_INSTALLING', 		1);
define('OPENSDK_APP_INSTALLED', 		2);
define('OPENSDK_APP_INSTALLING', 		3);
define('OPENSDK_APP_STARTED_NOT_RUNNING', 	4);
define('OPENSDK_APP_RUNNING', 			5);
define('OPENSDK_APP_STOPPED', 			6);

define('OPENSDK_MAX_SIZE_APP_NAME', 	        60);
define('OPENSDK_MAX_SIZE_INSTALLED_DATE', 	40);

require_once ('../../cgi-bin/adv/_define.inc');

        $classInstances = GetClassInstance('sdk');
	$sdkSearchConf = $classInstances['SDKInfoRequest'];

	$sdkSearchConf->SetHeaderCommand(CMD_SDK_SEARCH_DETAIL);
	$sdkSearchConf->SetCGIPayload();

        $GLOBALS['SOCKET_MANAGER']->Connection($sdkSearchConf);
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
			lnbonoff(1);
	});
        </script>

<script type="text/javascript">

var APP_NAME = "";
var APP_STATUS = -2;
var SELECTED_PROFILE = -1;
var APP_INSTALLED_DATE = "";
var APP_VERSION = "";

var INSTALLED_APPLICATIONS_COUNT = parseInt("<?php echo $sdkSearchConf->dataInfo['max_apps_count']['value'];?>");
var MAX_SIZE_INSTALLED_DATE = parseInt("<?php echo OPENSDK_MAX_SIZE_INSTALLED_DATE;?>");

// Define ERROR CODES map here
var SDK_ERROR_CODES_MAP = {
                                66: 'OPERATION TEMPORARILY UNAVAILABLE',
                                67: 'APP. ALREADY RUNNING',
                                68: 'APP. START FAILED',
                                69: 'APP. STOP FAILED',
                                70: 'APP. UPLOAD FAIL',
                                71: 'ENOUGH APP. SPACE UNAVAILABLE',
                                72: 'INVALID APPLICATION PACKAGE',
                                73: 'HIGHER OR SIMILAR VERSION IS ALREADY AVAILABLE',
                                74: 'APP. INSTALL FAIL',
                                75: 'APP. NOT FOUND',
                                77: 'APP. is NOT RUNNING'
                          };

var MAX_APP_PERMISSIONS = 32; // 32 bits
// Define Permissions map here
var APP_PERMISSION_CODES = {
                                0: 'OPENSDK CAPABILITY NONE',  // NONE
                                1: 'MEDIA',                    // Bit 0(LSB) is set
                                2: 'PTZ-CONTROL',              // Bit 1 is set
                                4: 'PROFILE CONFIG',           // Bit 2 is set
                                8: 'SD CARD',                  // Bit 3 is set
                                16: 'VIDEO ANALYTICS',         // Bit 4 is set
                                32: 'VIDEO SETUP',             // Bit 5 is set
                                64: 'DEVICE'                   // Bit 6 is set
                           };

function startUpload()
{
   //alert("In startUpload");
   document.getElementById('f1_upload_process').style.visibility = 'visible';
   document.getElementById('f1_upload_form').style.visibility = 'hidden';

   return true;
}
function SDKUploadRequestAjaxMsg(msg, alertMsg, reqUrl, command, asyncVal)
{
        //alert("in Ajax upload");
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
		success: OnSuccessUpload
                });
}

function SDKInstallRequestAjaxMsg(msg, alertMsg, reqUrl, command, asyncVal)
{
        //alert("in Ajax install");
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
		success: OnSuccessInstall
                });
}

function SDKHealthRequestAjaxMsg(msg, alertMsg, reqUrl, command, asyncVal)
{
        //alert("in Ajax install");
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
		success: OnSuccessHealth
                });
}

function SDKUpdateSettingsRequestAjaxMsg(msg, alertMsg, reqUrl, command, asyncVal)
{
        //alert("in Ajax update setings");
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
		success: OnSuccessUpdateSettings
                });
}

function SDKGetSettingsRequestAjaxMsg(msg, alertMsg, reqUrl, command, asyncVal)
{
        //alert("in Ajax fetch settings request");
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
		success: OnSuccessGetSettings
                });
}

function OnSuccessUpload(ack)
{
	var msg = "";
	var result ='';

        var xml = $.parseXML(ack);
        var Is_valid_error_code = $(xml).find("ErrorCode").text();

        if(Is_valid_error_code != "")
        {
              var error_code = parseInt(Is_valid_error_code);
              msg += "ERROR in File Upload : "+SDK_ERROR_CODES_MAP[error_code];
              result = '<span class="emsg">There was an error during file upload!<\/span><br/><br/>';
              alert(msg);
        }
	else
        {
                var xml = $.parseXML(ack);
                var permissions = parseInt($(xml).find("AddResult").text());
                var permissionsMsg = "Installing this application might access the below permissions from your Camera : "+ "\n";
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
                permissionsMsg += "Press \"OK\" button if you wish to Install the application.";

		var confirm_result;

		confirm_result = confirm(permissionsMsg);
		if (confirm_result == true)
	  	{
			document.getElementById("f1_upload_process").innerHTML='Installation in Progress. Please wait...<img src="../images/opensdk/loader.gif" /><br/>';

                        msg += "<SetSDK>";
			msg += "<AppName>"+ APP_NAME +"</AppName>";
			//msg += "<AppUploadPath>" + app_downloaded_directory + "</AppUploadPath>";
			msg += "</SetSDK>";
			//alert("You have selected \""+ APP_NAME +"\" to install on the IP camera device.");
     	  	        SDKInstallRequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>", 'SDK', 'undefined');
      	  	        //RequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>", 'SDK', 'undefined');
      	  	        return;
		}
		else
		{
			msg="User pressed Cancel!";
			result = '<span class="emsg">Installation Error: User pressed Cancel!<\/span><br/><br/>';
			alert(msg);

		}
	}
        document.getElementById('f1_upload_process').style.visibility = 'hidden';
	document.getElementById('f1_upload_form').innerHTML = result + '<label>File: <input id="file_id" name="myfile" type="file" size="30" /><\/label><label><input type="submit" name="submitBtn" class="sbtn" value="Upload" /><\/label>';
	document.getElementById('f1_upload_form').style.visibility = 'visible';
}

function OnSuccessInstall(ack)
{
        var msg = "";
        var result = '';

        var xml = $.parseXML(ack);
        var Is_valid_error_code = $(xml).find("ErrorCode").text();

        if(Is_valid_error_code != "")
        {
              var error_code = parseInt(Is_valid_error_code);
              msg += "ERROR in Installation : "+SDK_ERROR_CODES_MAP[error_code];
              result = '<span class="emsg">Error in Installing Application.!<\/span><br/><br/>';
              alert(msg);
        }
	else
        {
               msg += "Application installed successfully.";
               result = '<span class="emsg">Application installed successfully.<\/span><br/><br/>';
               alert(msg);
               window.location.reload(true);
        }
        document.getElementById('f1_upload_process').style.visibility = 'hidden';
	document.getElementById('f1_upload_form').innerHTML = result + '<label>File: <input id="file_id" name="myfile" type="file" size="30" /><\/label><label><input type="submit" name="submitBtn" class="sbtn" value="Upload" /><\/label>';
	document.getElementById('f1_upload_form').style.visibility = 'visible';
}

function postUploadDetails(success, appName, app_downloaded_directory, error_message_str)
{
        var result = '';

      	if (success == 1)
      	{
      		//console.log("the app cap is: " +appName+" Downloaded to Device Path: "+app_downloaded_directory);
      		result = '<span class="msg">The file was uploaded successfully!<\/span><br/><br/>';
                APP_NAME = appName;
      		//console.log("The app name is " +APP_NAME);
      		var msg = "";
      		msg += "<AddSDK>";
      		msg += "<AppName>"+ APP_NAME +"</AppName>";
      		msg += "<AppUploadPath>" + app_downloaded_directory + "</AppUploadPath>";
      		msg += "</AddSDK>";
      		//console.log(msg);
      		SDKUploadRequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>", 'SDK', 'undefined');

                document.getElementById('f1_upload_process').style.visibility = 'visible';
	        return true;
      	}
      	else
      	{
                alert(error_message_str); // Upload failed Alert
                result = '<span class="emsg">There was an error during file upload!<\/span><br/><br/>';
      	}
	document.getElementById('f1_upload_process').style.visibility = 'hidden';
	document.getElementById('f1_upload_form').innerHTML = result + '<label>File: <input id="file_id" name="myfile" type="file" size="30" /><\/label><label><input type="submit" name="submitBtn" class="sbtn" value="Upload" /><\/label>';
	document.getElementById('f1_upload_form').style.visibility = 'visible';
	return true;
}

function OnSuccessHealth(ack)
{
        var msg = "";

        var xml = $.parseXML(ack);
        var Is_valid_error_code = $(xml).find("ErrorCode").text();

        if(Is_valid_error_code != "")
        {
              var error_code = parseInt(Is_valid_error_code);
              msg += "ERROR in Health status Disply : "+SDK_ERROR_CODES_MAP[error_code];
              alert(msg);
        }
	else
        {
                var xml = $.parseXML(ack);
                var app_cpu_usage_percent = $(xml).find("cpuPercent").text();
                var app_mem_usage_percent = $(xml).find("memPercent").text();
                var threads_count = $(xml).find("threadsCnt").text();
                var duration = parseInt($(xml).find("Duration").text());  // Time in seconds

                var hours = parseInt( duration / 3600 );     // Time in hours
                var min_balance =  parseInt( duration % 3600 )
                var minutes = parseInt( min_balance / 60 ); // Time in minutes
                var seconds = min_balance % 60;             // Time in seconds

                var result = hours+" Hrs"+" : "+minutes+" Min"+" : "+seconds+" Sec";

                msg += "APPLICATION HEALTH : "+"\n";
                msg += "CPU Usage : "+app_cpu_usage_percent+" %"+"\n";
                msg += "Memory Usage : "+app_mem_usage_percent+" %"+"\n";
                msg += "Threads Count : "+threads_count+"\n";
                msg += "Application Running Since (Duration) :   "+result+"\n";

                alert(msg);
	}
}

function OnSuccessUpdateSettings(ack)
{
      alert("Settings Saved.");
      document.getElementById('settings_menu').style.visibility = 'hidden';
}

function OnSuccessGetSettings(ack)
{
        var xml = $.parseXML(ack);
        var Is_valid_error_code = $(xml).find("ErrorCode").text();

        if(Is_valid_error_code != "")
        {
              var error_code = parseInt(Is_valid_error_code);
              msg += "ERROR in Health status Disply : "+SDK_ERROR_CODES_MAP[error_code];
              alert(msg);
        }
	else
        {
             var xml = $.parseXML(ack);
             var priority = parseInt($(xml).find("Priority").text());
             var autoStart = parseInt($(xml).find("IsAutoStart").text());

             document.getElementById('settings_menu').style.visibility = 'visible';

             switch(priority)
             {
                   case 0 : document.getElementById('priority_low').checked = true; break;

                   case 1 : document.getElementById('priority_medium').checked = true; break;

                   case 2 : document.getElementById('priority_high').checked = true; break;

                   default : break;
             }
             if(autoStart == 1)
             {
                   document.getElementById('auto_start').checked = true;
             }
             else
             {
                  document.getElementById('auto_start').checked = false;
             }
	}
}

function isProfileSelected()
{
   if(SELECTED_PROFILE == -1)
   {
        alert("Please selct the Application to continue");
        return false;
   }
   return true;
}

function onStartBtnClk()
{
   if(!isProfileSelected())
        return;

   var msg = "";
   msg += "<StartSDK>";
   msg += "<AppName>"+ APP_NAME +"</AppName>";
   msg += "</StartSDK>";

   RequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>", 'SDK', 'undefined');
}

function onStopBtnClk()
{
   if(!isProfileSelected())
        return;

   var msg = "";
   msg += "<StopSDK>";
   msg += "<AppName>"+ APP_NAME +"</AppName>";
   msg += "</StopSDK>";

   RequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>", 'SDK', 'undefined');
}

function onUnistallBtnClk()
{
   if(!isProfileSelected())
        return;

   var conf_message = "Do you really want to uninstall the application : "+APP_NAME+" ?"+"\n"+"Press \"OK\" to uninstall.";
   var confirm_status;
   confirm_status = confirm(conf_message);

   if (confirm_status == true)
   {
       var msg = "";
       msg += "<RemoveSDK>";
       msg += "<AppName>"+ APP_NAME +"</AppName>";
       msg += "</RemoveSDK>";

       RequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>", 'SDK', 'undefined');
   }
}
function onHealthBtnClk()
{
   if(!isProfileSelected())
        return;

   var msg = "";
   msg += "<GetSDK>";
   msg += "<AppName>"+ APP_NAME +"</AppName>";
   msg += "</GetSDK>";

   SDKHealthRequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>", 'SDK', 'undefined');
}

function onSettingsBtnClk()
{
   if(!isProfileSelected())
        return;
     //window.open("window-child.html","Ratting","width=550,height=170,left=150,top=200,toolbar=0,status=0,");
     var msg ="";
     msg += "<GetSDKAppAttributes>";
     msg += "<AppName>"+ APP_NAME +"</AppName>"+"\n";
     msg += "</GetSDKAppAttributes>";

     SDKGetSettingsRequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>", 'SDKAppAttributes', 'undefined');
}

function onUpdateSettingsBtnClk()
{
    var priority = -1;
    var isAutoStart = 0;

    if(document.getElementById('priority_low').checked)
    {
       priority = document.getElementById('priority_low').value;
    }
    else if(document.getElementById('priority_medium').checked)
    {
       priority = document.getElementById('priority_medium').value;
    }
    else if(document.getElementById('priority_high').checked)
    {
       priority = document.getElementById('priority_high').value;
    }

    if(document.getElementById('auto_start').checked)
    {
       isAutoStart = 1;
    }

    var msg ="";
    msg += "<SetSDKAppAttributes>";
    msg += "<AppName>"+ APP_NAME +"</AppName>"+"\n";
    msg += "<IsAutoStart>"+ isAutoStart +"</IsAutoStart>"+"\n";
    msg += "<Priority>"+ priority +"</Priority>"+"\n";
    msg += "</SetSDKAppAttributes>";

    SDKUpdateSettingsRequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>", 'SDKAppAttributes', 'undefined');
}

function onDetailsBtnClk()
{
    if(!isProfileSelected())
        return;

    var msg = "";
    msg = "App. Name: "+ APP_NAME + "\n"+"Installed Date: "+ APP_INSTALLED_DATE + "\n"+"Version : "+ APP_VERSION;
    alert(msg);
}

function onAppPageBtnClk()
{
    window.open("../setup/opensdk/"+APP_NAME+"/"+"index.cgi?AppName="+APP_NAME);
}

function onBtnClk(BTN_ID)
{
    if(!isProfileSelected())
        return;

    switch(BTN_ID)
    {
         case 'BTN_START_STOP' :
         {
            if(APP_STATUS == 2 || APP_STATUS == 6)
            {
                onStartBtnClk();
            }
            else if(APP_STATUS == 4 || APP_STATUS == 5)
            {
                onStopBtnClk();
            }
         } break;

         case 'BTN_UNINSTALL' :
         {
            onUnistallBtnClk();
         } break;

         case 'BTN_HEALTH' :
         {
            onHealthBtnClk();
         } break;

         case 'BTN_SETTINGS' :
         {
            onSettingsBtnClk();
         } break;

         case 'BTN_DETAILS' :
         {
            onDetailsBtnClk();
         } break;

         case 'BTN_APP_PAGE' :
         {
            onAppPageBtnClk();
         } break;

         default : break;
    }
}

function onProfileSelRadioBtnClk(Profile_No, App_Name, App_status, Installed_Date, Version)
{
    SELECTED_PROFILE = Profile_No;
    APP_NAME = App_Name;
    APP_STATUS = App_status;

    if(BrowserDetect.browser == "Explorer")
    {
        APP_INSTALLED_DATE = Installed_Date;
    }
    else
    {
        var end_position = 0;
        while(end_position < MAX_SIZE_INSTALLED_DATE)
        {
            if(Installed_Date.charCodeAt(end_position) == 65533)
            {
               break;
            }
            end_position+=1;
        }
        APP_INSTALLED_DATE = Installed_Date.slice(0,end_position);
    }

    APP_VERSION = Version;

    document.getElementById("BTN_HEALTH").style.color="SlateGray";
    document.getElementById('BTN_HEALTH').disabled=true;
    document.getElementById('settings_menu').style.visibility = 'hidden';

    if((APP_STATUS == 1) || (APP_STATUS == 3))
    {
          document.getElementById("BTN_START_STOP").style.color="SlateGray";
          document.getElementById('BTN_START_STOP').disabled=true;
          document.getElementById("BTN_UNINSTALL").style.color="SlateGray";
          document.getElementById('BTN_UNINSTALL').disabled=true;
          document.getElementById("BTN_SETTINGS").style.color="SlateGray";
          document.getElementById('BTN_SETTINGS').disabled=true;
          document.getElementById("BTN_DETAILS").style.color="SlateGray";
          document.getElementById('BTN_DETAILS').disabled=true;
          document.getElementById("BTN_APP_PAGE").style.color="SlateGray";
          document.getElementById('BTN_APP_PAGE').disabled=true;
          return;
    }

    if((APP_STATUS == 2) || (APP_STATUS == 6))
    {
         document.getElementById('BTN_START_STOP').innerHTML = "START";
    }
    else if((APP_STATUS == 4) || (APP_STATUS == 5))
    {
         document.getElementById('BTN_START_STOP').innerHTML = "STOP";
         document.getElementById("BTN_HEALTH").style.color="black";
         document.getElementById('BTN_HEALTH').disabled=false;
    }
    document.getElementById("BTN_START_STOP").style.color="black";
    document.getElementById('BTN_START_STOP').disabled=false;
    document.getElementById("BTN_UNINSTALL").style.color="black";
    document.getElementById('BTN_UNINSTALL').disabled=false;
    document.getElementById("BTN_SETTINGS").style.color="black";
    document.getElementById('BTN_SETTINGS').disabled=false;
    document.getElementById("BTN_DETAILS").style.color="black";
    document.getElementById('BTN_DETAILS').disabled=false;
    document.getElementById("BTN_APP_PAGE").style.color="black";
    document.getElementById('BTN_APP_PAGE').disabled=false;
}

</script>
</head>

<body>
<h1 align="center">iPOLiS NETWORK CAMERA - OPEN SDK [SISO]</h1>

<div id="main_page_align" style="margin-left:50px;width:100%;">
<br/><br/><br/>
<form action="opensdk_upload.cgi" method="post" enctype="multipart/form-data" target="upload_target" onsubmit="startUpload();" >
	<p id="f1_upload_process">File Upload in progress.Please wait ...!<br/><img src="../images/opensdk/loader.gif" /><br/></p>
	<p id="f1_upload_form" align="left"><br/>
	<label>File: <input name="myfile" type="file" size="30" /></label>
	<label><input type="submit" name="submitBtn" class="sbtn" value="Upload" /></label>
	</p>
	<iframe id="upload_target" name="upload_target" src="#" style="width:0;height:0;border:0px solid #fff;"></iframe>
</form>

<h2>OPEN SDK Installed Applications</h3>
<table border="2">
<!-- Table Headder -->
<tr>
<th style="color:LightSeaGreen;font: bold">App. Selection</th>
<th style="color:LightSeaGreen;font: bold">App. Name</th>
<th style="color:LightSeaGreen;font: bold">App. Status</th>
</tr>
<!-- Dynamic Creation of rows & populate Row data -->
<?php

for ($index=0; $index < $sdkSearchConf->dataInfo['max_apps_count']['value']; $index++)
{
  $AppStatus_Val = $sdkSearchConf->sdk_app[$index]->dataInfo['app_status']['value'];

  $Raw_AppName = $sdkSearchConf->sdk_app[$index]->dataInfo['app_name']['value'];
  $AppNameLength = 0;
  for ($i = 0; $i < OPENSDK_MAX_SIZE_APP_NAME; $i++)
  {
        if(substr($Raw_AppName, $i, 1) == "_" || ctype_space(substr($Raw_AppName, $i, 1)) || ctype_alnum(substr($Raw_AppName, $i, 1)))
        {
             $AppNameLength += 1;
             continue;
        }
        break;
  }
  $AppName = substr($Raw_AppName, 0, $AppNameLength);

  $InstalledDate = $sdkSearchConf->sdk_app[$index]->dataInfo['installed_date']['value'];
  $Version = $sdkSearchConf->sdk_app[$index]->dataInfo['app_major_version']['value'].".".$sdkSearchConf->sdk_app[$index]->dataInfo['app_minor_version']['value'];

  switch($AppStatus_Val)
  {
      //case OPENSDK_APP_INSTALL_FAILED:      $Color_code = "Yellow"; $AppStatus_Txt = "Install Failed"; break;

      //case OPENSDK_APP_UN_INSTALLED:        $Color_code = "Yellow"; $AppStatus_Txt = "UnInstalled"; break;

      case OPENSDK_APP_UN_INSTALLING:       $Color_code = "Yellow"; $AppStatus_Txt = "UnInstalation in Progress..."; break;

      case OPENSDK_APP_INSTALLED:           $Color_code = "Yellow"; $AppStatus_Txt = "Installed."; break;

      case OPENSDK_APP_INSTALLING:          $Color_code = "Yellow"; $AppStatus_Txt = "Instalation in Progress..."; break;

      case OPENSDK_APP_STARTED_NOT_RUNNING: $Color_code = "Yellow"; $AppStatus_Txt = "Started but not Running."; break;
  
      case OPENSDK_APP_RUNNING:             $Color_code = "Green"; $AppStatus_Txt = "Running."; break;
  
      case OPENSDK_APP_STOPPED:             $Color_code = "Red"; $AppStatus_Txt = "Stopped."; break;

      default :                             $Color_code = ""; $AppStatus_Txt = ""; break;
  }
?>
<tr>
<td style="color:black;font: bold" align="center"> <input type="radio" name="profile_select" id="profile_select_<?php echo $index; ?>" value='<?php echo $index; ?>' onclick="onProfileSelRadioBtnClk('<?php echo $index; ?>', '<?php echo $AppName; ?>', '<?php echo $AppStatus_Val; ?>', '<?php echo $InstalledDate; ?>', '<?php echo $Version; ?>');"/></td>
<td style="color:black;font: bold;font-size: 25px;" name="profile_name" id="profile_name_<?php echo $index; ?>"> <img src="../images/opensdk/img_sample_app.gif" width="40" height="30"/><?php echo $AppName; ?> </td>
<td style="color:<?php echo $Color_code; ?>;font: bold;font-size: 20px;" name="profile_status" id="profile_status_<?php echo $index; ?>"> <?php echo $AppStatus_Txt; ?> </td>
</tr>
<?php
}
?>
</table>

<br/><br/>
<button id="BTN_START_STOP" style="color:SlateGray;font: bold" disabled="disabled" onclick="onBtnClk('BTN_START_STOP');"> START/STOP </button>
<button id="BTN_UNINSTALL" style="color:SlateGray;font: bold" disabled="disabled" onclick="onBtnClk('BTN_UNINSTALL');"> UNINSTALL </button>
<button id="BTN_HEALTH" style="color:SlateGray;font: bold" disabled="disabled" onclick="onBtnClk('BTN_HEALTH');"> HEALTH </button>
<button id="BTN_SETTINGS" style="color:SlateGray;font: bold" disabled="disabled" onclick="onBtnClk('BTN_SETTINGS');"> SETTINGS </button>
<button id="BTN_DETAILS" style="color:SlateGray;font: bold" disabled="disabled" onclick="onBtnClk('BTN_DETAILS');"> DETAILS </button>
<button id="BTN_APP_PAGE" style="color:SlateGray;font: bold" disabled="disabled" onclick="onBtnClk('BTN_APP_PAGE');"> APP PAGE </button>
<br/><br/>

<div id="settings_menu" style="visibility: hidden">
<h4>APP. SETTINGS:</h4>
  <h5>PRIORITY:</h5>
  <input id="priority_low" name="priority" type="radio" value=0 /> LOW <br />
  <input id="priority_medium" name="priority" type="radio" value=1 /> MEDIUM <br />
  <input id="priority_high" name="priority" type="radio" value=2 /> HIGH <br />
  <h5>AUTO START:</h5>
  <input id="auto_start" name="autoStart" type="checkbox" /> AUTO START<br />
  <br/>
  <button id="BTN_UPDATE_SETTINGS" style="color:black;font: bold" onclick="onUpdateSettingsBtnClk();"> UPDATE </button>
  <br/>
</div>

</div>
</body>

