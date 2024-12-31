<?php
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_system_upgrade.cgi');
require_once ('../language/language_menu.cgi');

$classInstances= GetClassInstance('system');
$productInfo 	= $classInstances['SystemConfiguration']->deviceInfo;
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="kr" xml:lang="kr">
	<head>
		<title>iPOLiS NETWORK CAMERA WEBVIEWER</title>
		<META HTTP-EQUIV="Pragma" CONTENT="no-cache">
		<META HTTP-EQUIV="Expires" CONTENT="-1">
		<meta http-equiv="X-UA-Compatible" content="IE=Edge; requiresActiveX=true">
		<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
		<link rel="stylesheet" type="text/css" href="../css/techwin.css" />
		<link rel="stylesheet" type="text/css" href="../css/jquery-ui.css" />
		<link rel="stylesheet" type="text/css" href="../css/jquery.ui.dialog.css" />


	<script type="text/javascript" src="../js/jquery-1.9.1.js"></script>
	<script type="text/javascript" src="../js/jquery-ui.js"></script>
	<script type="text/javascript" src="../js/common_function.js"></script>
	<script type="text/javascript" src="../js/pluginCheck.js"></script>
	<script type="text/javascript" src="../js/pluginControl.js"></script>
	<script type="text/javascript" src="../js/jquery.ui.dialog.js"></script>
	<style type="text/css">
	    html, body {
		    height: 800px;
		    overflow: hidden;
	    }
	    body {
		    padding: 0;
		    margin: 0;
	    }
	    #silverlightControlHost {
		    height: 100%;
		    text-align:center;
	    }
	  #messageList .ui-selecting { background: #cae4ed; }
	  #messageList .ui-selected { background: #cae4ed; }
	  #messageList { list-style-type: none; margin: 0; padding: 0; width: 60%; }
	  #messageList li { padding: 0.1em; }
	  .ui-draggable .ui-dialog-titlebar {
		background: #e3e6e8;
		padding: 0 5px;
		border: none;
		color: #000;
		font-size: 11px;
		margin: 0 5px;
		}
		.ui-dialog-titlebar-close{
			display:none;	
		}
		.ui-dialog{
			width: 400px !important;
		}
		.ui-widget-overlay{
			background: none repeat scroll 0 0 #000000
			height: 100%;
		}
		#message{
			height: 250px;
			border: 1px solid #657480;
			margin-bottom:10px;
			padding: 5px;
			color: #000;
			font-size: 11px;
			background: #fff;
		}
		.ui-dialog .ui-dialog-content {
			padding: .5em 0.5em;
		}
		.ui-dialog .ui-button-text-only .ui-button-text {
			padding: .2em 1em;
		}
		.ui-dialog .ui-dialog-buttonpane button {
			margin: 5px;
			cursor: pointer;
			font-weight: bold;
		}
		.ui-dialog .ui-dialog-buttonpane {
			margin-top: 0;
		}
		#progressbar{
			background: #fff;
			border: 1px solid #657480;
		}
		.ui-dialog.ui-widget-content {
			
			background: #e3e6e8;
			color: #000;
		}
		.ui-dialog .ui-dialog-buttonpane button {
			margin:0;
		}
		.ui-dialog-buttonpane.ui-widget-content{
			border:0;
			background: none
		}
		.upgrade_info{
			color: #FAFAFA;
			padding: 30px 0 0 29px;
			line-height: 1.5;
		}
		
		#upgradeFileSel{
			width: 323px;
			margin-top: 17x;
			padding: 0px;
			background: #FAFAFA;
			border: 0px;
			height: 20px;
			margin-left:10px;
		}
		.FileUpload {
			position:relative;
		}
		.btn_browse {
			position: absolute;
			top:-1px; 
			display:inline-block;
			width:105px;
			height:20px;
			margin-top:1px;
			padding-top:2px;
			background:#1b2029;
			text-align:center;
			vertical-align:middle;
			font-weight:bold;
			font-size: 13px;
			color:#fff;
		}
		.btn_browse:hover {
			background:#0b76d5;
			text-decoration:none;
			font-size: 13px;
			color:#fff;
		}
		.btn_browse input {
			position: absolute;
			top: 0;
			left: 0px;
			margin: 0;
			border: solid transparent;
			width:104px;
			/*border-width: 0 0 100px 200px;*/
			opacity: 0;
			filter: alpha(opacity=0);
			/*-moz-transform: translate(-300px, 0) scale(4);*/
			direction: ltr;
			cursor: pointer;
		}

	  </style>

	<script type="text/javascript">
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
	  var ajaxReqUrl			  = "<?php echo $GLOBALS['REQUEST_URI']; ?>";
	  var encName				  = "<?php echo $GLOBALS['USERINFO']['encname']; ?>";
	  var encPW 				  = "<?php echo $GLOBALS['USERINFO']['encpw']; ?>";
	  var devicePort			  = <?php echo $classInstances['Information']->dataInfo['DevicePort']['value']; ?>;
	  var previewProfileNo	  = <?php echo $classInstances['Information']->dataInfo['PreviewProfileNo']['value']; ?>;
	  var installMsg			  = new Array();
	  installMsg[0]			  = "<?php echo $msg_plugin_install[$GLOBALS['LANGINDEX']]; ?>";
	  installMsg[1]			  = "<?php echo $msg_plugin_install2[$GLOBALS['LANGINDEX']]; ?>";
	  installMsg[2]			  = "<?php echo $msg_notsupport_plugin[$GLOBALS['LANGINDEX']]; ?>";

	  var isUpgradeStart = 0;

function OnSetParameters()
{
	var model 		= "<?php echo $_SERVER['MODELNAME']; ?>";
	var upgradeVer = "<?php echo $productInfo->dataInfo['FirmwareVer']['value']; ?>";
	var moduleVer 	= "<?php echo $productInfo->dataInfo['ModuleVer']['value']; ?>";
	var lastupdate = "<?php echo $productInfo->dataInfo['LastUpdate']['value']; ?>";
	var devicePort = "<?php echo $classInstances['Information']->dataInfo['DevicePort']['value']; ?>";

	var tempVal = 0;
	while(tempVal <= 150000)
	{
		tempVal++;
	}

	var control 	= document.getElementById("firmwareUpgrade");
	control.content.FirmwareUpgradeControl.SetConnectionParameters(location.hostname, devicePort, "<?php echo $GLOBALS['USERINFO']['name']; ?>", "<?php echo $GLOBALS['USERINFO']['pw']; ?>");
	control.content.FirmwareUpgradeControl.SetUpgradeInformations(upgradeVer, moduleVer, lastupdate);

	if(model == 'SNP-3120V' || model == 'SNP-3120' || model == 'SNP-3120VH')
	{
		var ifVer 	= "<?php echo $productInfo->dataInfo['IfBoardVersion']['value']; ?>";
		var PTZVer 	= "<?php echo $productInfo->dataInfo['PtzVer']['value']; ?>";
		control.content.FirmwareUpgradeControl.SetUpgradeInformations_PTZ(ifVer, PTZVer);
	} else if(model == "SNP-5190H" || model == "SNP-5190" || model=="SNP-5200" || model == "SNP-5200H" ){
		var ifVer 	= "0.0";
		var PTZVer 	= "<?php echo $productInfo->dataInfo['PtzVer']['value']; ?>";
		control.content.FirmwareUpgradeControl.SetUpgradeInformations_PTZ(ifVer, PTZVer);
	}
}

function closeWindow()
{
	window.open('about:blank', '_self').close();
}

function doFirmwareUpgrade()
{
	if(isUpgradeStart > 0)
		return;

	var fileName = jQuery.trim(document.getElementById("upgradeFileSel").value);

	if(fileName.length < 1)
	{
		alert("<?php echo $msg_selectFirmwareError[$GLOBALS['LANGINDEX']]; ?>");
		return;
	}

	<?php if ($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>
		if (checkS1FileName(fileName) == 0)
		{
			alert("<?php echo $msg_invalid_firmware[$GLOBALS['LANGINDEX']]; ?>");
			return;
		}
	<?php } else { ?>
		if(checkModelName(fileName) < 1)
		{
			alert("<?php echo $msg_invalid_firmware[$GLOBALS['LANGINDEX']]; ?>");
			return;
		}
	<?php } ?>

	var userName = "<?php echo $GLOBALS['USERINFO']['name']; ?>";
	if (userName == "") {
		userName = "guest";
	}

	

	//var msg = SISOPlugin.firmwareUpgrade(location.hostname, devicePort, encName, encPW);
	isUpgradeStart = 1;
	var msg = SISOPlugin.firmwareUpgrade(location.hostname, devicePort, encName, encPW);
	if(parseInt(msg) == 1) {
		openStatusDialog();
	} 
	
}	

function checkS1FileName(file)
{
	var key = "S1_sndl6013";
	var result;
	
	result = file.search(key);

	if(result != -1)
	{
		return 1;
	}
	else
	{
		return 0;
	}

}

function checkModelName(file)
{
	var key;
	var result;
	var modelName = "<?php echo $_SERVER['MODELNAME']; ?>";
	var modelCode = modelName.substr(4, 4);

	if (modelCode == "6320") {
		key = "6320";
	}
	else if (modelCode == "7004" || modelCode == "7084") {
		key = "7004";
	}
	else if (modelCode == "6004" || modelCode == "6084" || modelCode == "6003" || modelCode == "6083") {
		key = "6004";
	}
	else if (modelCode == "5004" || modelCode == "5084" || modelCode == "5003" || modelCode == "5083") {
		key = "5004";
	}
	else if (modelCode == "S202" || modelCode == "S201") {
		key = "s202";
	}
	else if (modelCode == "S102" || modelCode == "S101") {
		key = "s102";
	}
	else if (modelCode == "6011") {
		key = "6011";
	}
	else if (modelCode == "6012") {
		key = "6012";
	}
	else if (modelCode == "7010") {
		key = "7010";
	}
	else if (modelName == "SND-L6013" || modelName == "SND-L6013R" || modelName == "SNO-L6013R") {
		if(file.search("S1_sndl6013") != -1)
			return 0;
		
		key = "l6013";
		result = file.search(key);
		if(result == -1){
			key = "l6083";
		}
		else{
			return 1;
		}
	}
	else if (modelName == "SND-L6083" || modelName == "SND-L6083R" || modelName == "SNO-L6083R" || modelName == "SNV-L6083R") {
		if(file.search("S1_sndl6013") != -1)
			return 0;
		
		key = "l6083";
		result = file.search(key);
		if(result == -1){
			key = "l6013";
		}
		else{
			return 1;
		}
	}
	else if (modelName == "SND-L5013" || modelName == "SND-L5013R" || modelName == "SNO-L5013R") {
		key = "l5013";
		result = file.search(key);
		if(result == -1){
			key = "l5083";
		}
		else{
			return 1;
		}
	}
	else if (modelName == "SND-L5083" || modelName == "SND-L5083R" || modelName == "SNO-L5083R" || modelName == "SNV-L5083R") {
		key = "l5083";
		result = file.search(key);
		if(result == -1){
			key = "l5013";
		}
		else{
			return 1;
		}
	}
	else if (modelCode == "5430") {
		key = "5430";
	}
	else if (modelCode == "6321") {
		key = "6321";
	}
	else if (modelCode == "5321") {
		key = "5321";
	}

	result = file.search(key);

	if(result != -1)
	{
		return 1;
	}
	else
	{
		return 0;
	}
}

function browseFirmwareImage()
{		
	if(isUpgradeStart > 0)
		return;

	SISOPlugin.browseFirmwareImage();
}

function displayMessage(message)
{
   //console.log("message ", message);	
   alert("<?php echo $msg_selectFirmwareError[$GLOBALS['LANGINDEX']]; ?>");
}

//  This function will be called when you select a file in the dialogue box.
function displayFirmwareFile(file)
{
// remove alert and add your code here to display file name
	var filename = file.replace(/^.*[\\\/]/, '')
	document.getElementById("upgradeFileSel").value = filename;	
}


//Function to open the dialog status.
function openStatusDialog(msg) {
	var progress = 0;

	$("#statusDialog").dialog({ 
	//	closeOnEscape: true,
		disabled: true,
		resizable: false,
		autoOpen: false,
		draggable: false,
		modal: true,
		title : "<?php echo $t_upgrade[$GLOBALS['LANGINDEX']]; ?>",
		
		buttons: [{
			disabled:"disabled",
			text: "<?php echo $t_close[$GLOBALS['LANGINDEX']]; ?>",
			click: function() { $(this).dialog("close"); }
			}]
	});

	$("#progressbar").progressbar({
      		value: progress
   });
   	 
   $("#messageList" ).selectable();
   	
  	if(msg) 
  		$("#messageList").append("<li class='ui-selected'> " + msg + " </li>");			
}

function getMessage(msg, type) {
	// Downloading was started
	// Downloading was succeeded
	// Downloading was ended
	// Upgrading was started
	// Kernel upgrading was succeeded
	// Application upgrading was skipped
	// Web upgrading was skipped
	// ISP upgrading was started
	// ISP upgrading was skipped
	// Upgrading was ended
	var messageStr = new Array();
	var progress;
	
	switch (msg) {
		case "NONE" :
			messageStr[0] = "<?php echo $msg_downloading_was_started[$GLOBALS['LANGINDEX']]; ?>";
			break;
		case "DOWNLOAD_OK" :
			progress = 100;
			messageStr[0] = "<?php echo $msg_downloading_was_succeeded[$GLOBALS['LANGINDEX']]; ?>";
			messageStr[1] = "<?php echo $msg_downloading_was_ended[$GLOBALS['LANGINDEX']]; ?>";
			break;
		case "DOWNLOAD_FAIL" :	
			messageStr[0] = "<?php echo $msg_downloading_was_failed[$GLOBALS['LANGINDEX']]; ?>";
			messageStr[1] = "<?php echo $msg_downloading_was_ended[$GLOBALS['LANGINDEX']]; ?>";
			break;
		case "UPGRADE_START" :
			progress = 0;
			messageStr[0] = "<?php echo $msg_upgrading_was_started[$GLOBALS['LANGINDEX']]; ?>";
			break;
			
		case "UPGRADE_END" :
			progress = 100;
			messageStr[0] = "<?php echo $msg_upgrading_was_ended[$GLOBALS['LANGINDEX']]; ?>";	
			break;
			
		case "UPGRADE_OK" :
			
			if(type == "KERNEL") {
				progress = 16;
				messageStr[0] = "<?php echo $msg_Kernel_upgrading_was_succeeded[$GLOBALS['LANGINDEX']]; ?>";
			 
			} else if(type == "APPLICATION") {
				progress = 32;
				messageStr[0] = "<?php echo $msg_application_upgrading_was_succeeded[$GLOBALS['LANGINDEX']]; ?>";
				
			} else if(type == "WEB") {
				progress = 48;
				messageStr[0] = "<?php echo $msg_web_upgrading_was_succeeded[$GLOBALS['LANGINDEX']]; ?>";
				
			} else {
				progress = 100;
				<?php if ($GLOBALS['M_ISP_TYPE'] != ISP_TYPE_WN3 && $GLOBALS['M_ISP_TYPE'] != ISP_NO_TYPE && $GLOBALS['M_ISP_TYPE'] != ISP_TYPE_HISILICON) { ?>
				messageStr[0] = "<?php echo $msg_isp_upgrading_was_succeeded[$GLOBALS['LANGINDEX']]; ?>";
				<?php } ?>
			}
			break;
			
		case "UPGRADE_SKIP" :
			if(type == "KERNEL") {
				progress = 16;
				messageStr[0] = "<?php echo $msg_Kernel_upgrading_was_skipped[$GLOBALS['LANGINDEX']]; ?>";
			 
			} else if(type == "APPLICATION") {
				progress = 32;
				messageStr[0] = "<?php echo $msg_application_upgrading_was_skipped[$GLOBALS['LANGINDEX']]; ?>";
				
			} else if(type == "WEB") {
				progress = 48;
				messageStr[0] = "<?php echo $msg_web_upgrading_was_skipped[$GLOBALS['LANGINDEX']]; ?>";
				
			} else {
				progress = 100;
				<?php if ($GLOBALS['M_ISP_TYPE'] != ISP_TYPE_WN3 && $GLOBALS['M_ISP_TYPE'] != ISP_NO_TYPE && $GLOBALS['M_ISP_TYPE'] != ISP_TYPE_HISILICON) { ?>
				messageStr[0] = "<?php echo $msg_isp_upgrading_was_skipped[$GLOBALS['LANGINDEX']]; ?>";
				<?php } ?>
			}
			break;
		case "UPGRADE_FAIL" :
			if(type == "KERNEL") {
				progress = 16;
				messageStr[0] = "<?php echo $msg_Kernel_upgrading_was_failed[$GLOBALS['LANGINDEX']]; ?>";
			 
			} else if(type == "APPLICATION") {
				progress = 32;
				messageStr[0] = "<?php echo $msg_application_upgrading_was_failed[$GLOBALS['LANGINDEX']]; ?>";
				
			} else if(type == "WEB") {
				progress = 48;
				messageStr[0] = "<?php echo $msg_web_upgrading_was_failed[$GLOBALS['LANGINDEX']]; ?>";
				
			} else {
				progress = 100;
				messageStr[0] = "<?php echo $msg_upgrading_was_failed[$GLOBALS['LANGINDEX']]; ?>";
			}
			break;

		case "FWUPGRADE_UPDATING_ISP" :
			progress = 50 + (type / 2);
			break;
	}
	
	return {"messageStr" : messageStr, "progress" : progress };	
}

//Function to update the dialog status.
function updateStatus(message) {
	
	var data = message.split("::");
	//console.log("message ", message);
			
	if(data[1]) {
		
		var data2 = data[1].split(":");		
		var currStatus = getMessage(data2[0], data2[1]);
		var currmsg = currStatus["messageStr"];
		var progress = currStatus["progress"];
		
		if(currmsg && currmsg.length != 0) {
		
			for(var i =0; i < currmsg.length; i++) {
			
				//Remove the curreny class.
				$("#messageList li").each(
					function() {
						$(this).removeClass("ui-selected");
						$(this).addClass("ui-unselected");
					}
				);

				$("#messageList").append("<li class='ui-selected'> " + currmsg[i] + " </li>");
			}
		}
		
		updateTitle(progress);
		
		if(data2[0] == "UPGRADE_END") {
			upgradeDone();
		}
		
	}	
	
	updateTitle(data[0]);
	
	$( "#messageList" ).selectable();
	return;
}

function updateTitle(progress) {
	if(progress != undefined && progress != null && progress.length != 0) {	
		$("#progressbar").progressbar({
			value: parseInt(progress)
		 });		

		 

		$("#statusDialog").dialog({
			resizable: false,
			draggable: false,
			modal: true,
			title : "<?php echo $t_upgrade[$GLOBALS['LANGINDEX']]; ?> - " + progress + "%", 
			buttons: [{
				disabled:"disabled",
				text: "<?php echo $t_close[$GLOBALS['LANGINDEX']]; ?>",
				click: function() { $(this).dialog("close"); }
				}]
		});
	}	
}

function upgradeDone() {
	
	$("#statusDialog").dialog({		
		resizable: false,
		draggable: false,
		modal: true,
		buttons: [
		{
			text: "<?php echo $t_close[$GLOBALS['LANGINDEX']]; ?>",
			click: function() { 
				$(this).dialog("close"); 
					alert("<?php echo $msg_reconnect[$GLOBALS['LANGINDEX']];?>");
					window.open('about:blank', '_self').close();
			}
		}]
	});	
}

//Closes the status dialog & browser window both.
function closeStatusDialog() {
	$("#statusDialog").dialog( "close" );
	
}

function OnLoad()
{
	SISOPlugin.init(installMsg, 0, 0);
	SISOPlugin.setSecurityEnhancement();
}

</script>
	
</head>

	<body onload="OnLoad();">
		<div id="wrap">
			<div id="head">
		<?php 
			
			if($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>
				<div class="head-top2">
				<h1><img src="../images/common/top_title_1.png" alt="S1" /></h1>
				<div class="logo"></div>
			<?php } 
				else { 
			?>
			<div class="head-top">

				<h1><img src="../images/common/top_title.gif" alt="iPOLiS NETWORK CAMERA WEBVIEWER" /></h1>
				<div class="logo"><img src="../images/common/top_logo.gif" alt="SAMSUNG TECHWIN" /></div>
			<?php } ?>

			</div>
			<div id="contents" style="visibility:hidden;position:absolute" >
				<div class="ficture" style="visibility:hidden">
					
				</div>	
			</div>
			
		</div>
		<div class='upgrade_info'>
			<table class="data_write">
				<colgroup>
					<col style="width:140px;" />
					<col />
				</colgroup>
				<tbody>
					<tr>
						<th scope="row">S/W</th>
						<td>
							<input type="text" class="text" style="width:180px;" value="<?php echo $productInfo->dataInfo['FirmwareVer']['value']; ?>" disabled="disabled"/>
						</td>							
					</tr>
					<?php if($GLOBALS['M_ISP_TYPE'] != ISP_NO_TYPE) { ?>
					<tr>
						<th scope="row">ISP</th>
						<td>
							<input type="text" class="text" style="width:180px;" value="<?php echo $productInfo->dataInfo['ModuleVer']['value']; ?>" disabled="disabled"/>
						</td>
						<td></td>
					</tr>
					<?php } ?>
					<?php if($GLOBALS['M_SUPPORT_PTZ_TRACKING']) { ?>
					<tr>
						<th scope="row"><?php echo $t_tracking[$GLOBALS['LANGINDEX']]; ?></th>
						<td>
							<input type="text" class="text" style="width:180px;" value="<?php echo $classInstances['SystemConfiguration']->dataInfo['TrackingBoardVersion']['value']; ?>" disabled="disabled"/>
						</td>
						<td></td>
					</tr>
					<?php } ?>
				</tbody>
			</table>
			<div id="contents" style="width:100%; padding-left:0px; padding-top:10px;">
				<div class="FileUpload">
					<input type="text" readonly id="upgradeFileSel" name="upgradeFileSel" class="FileField" />
				</div>
				<?php
				$browseBtnTop = 219;
				if($GLOBALS['M_ISP_TYPE'] == ISP_NO_TYPE) $browseBtnTop -= 30;
				if(!$GLOBALS['M_SUPPORT_PTZ_TRACKING']) $browseBtnTop -= 30;
				?>
				<a class="btn_browse" href="javascript:browseFirmwareImage();" style="top:<?php echo $browseBtnTop;?>px; left:380px;"><?php echo $t_browse[$GLOBALS['LANGINDEX']]; ?></a>
				<a class="btn_browse" href="javascript:doFirmwareUpgrade();" style="top:<?php echo $browseBtnTop;?>px; left:490px;"><?php echo $t_send[$GLOBALS['LANGINDEX']]; ?></a>
			</div>		
		</div>
		<div id="statusDialog" style="display:none;">
			<div id="message" style="overflow:auto;">
				<ul id="messageList" style="list-style-type:none;width:100%">
				</ul>	
			</div>	
			
			<div id="progressbar" style="height:10px">
			</div>
		</div>
		<span id="pluginArea" style="width:0;height:0;"></span>
	</body>
</html>
