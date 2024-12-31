<?php
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_menu.cgi');
require_once ('../language/language_system_upgrade.cgi');

$classInstances= GetClassInstance('system');
$productInfo 	= $classInstances['SystemConfiguration']->deviceInfo;
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="kr" xml:lang="kr">
<head>
	<title>iPOLiS NETWORK CAMERA WEBVIEWER</title>
	<meta http-equiv="X-UA-Compatible" content="IE=Edge; requiresActiveX=true">
	<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
	<link rel="stylesheet" type="text/css" href="../css/techwin.css" />
	<link rel="stylesheet" type="text/css" href="../css/jquery-ui.css" />
	<link rel="stylesheet" type="text/css" href="../css/jquery.ui.dialog.css" />

	
	<script type="text/javascript" src="../js/jquery-1.9.1.js"></script>
 	<script type="text/javascript" src="../js/lnb.js"></script>
	<script type="text/javascript" src="../js/jquery-ui.js"></script>
	<script type="text/javascript" src="../js/jquery.ui.dialog.js"></script>
 	<script type="text/javascript" src="../js/jquery.form.js"></script>
 	<script type="text/javascript" src="../js/jquery.fileDownload.js"></script>
 	<script type="text/javascript" src="../js/jquery.cookie.js"></script>
	<script type="text/javascript" src="../js/common_function.js"></script>
	<script type="text/javascript" src="../js/pluginCheck.js"></script>
	<script type="text/javascript" src="../js/pluginControl.js"></script>
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
	$(document).ready(function(){ 	lnbonoff("lnb_system"); });

	var isBackup = false;	
	var encName 				= "<?php echo $GLOBALS['USERINFO']['encname']; ?>";
	var encPW					= "<?php echo $GLOBALS['USERINFO']['encpw']; ?>";
	var installMsg				= new Array();
	installMsg[0] 				= "<?php echo $msg_plugin_install[$GLOBALS['LANGINDEX']]; ?>";
	installMsg[1] 				= "<?php echo $msg_plugin_install2[$GLOBALS['LANGINDEX']]; ?>";
	installMsg[2] 				= "<?php echo $msg_notsupport_plugin[$GLOBALS['LANGINDEX']]; ?>";

	function OnClickReboot(type)
	{
		$("#upgrade_reset").attr('disabled', 'disabled');
		$("#upgrade_restart").attr('disabled', 'disabled');

		var confirmMsg = "<?php echo $msg_restart[$GLOBALS['LANGINDEX']]; ?>";
		if (type == "Reset") confirmMsg = "<?php echo $msg_factoryDefault[$GLOBALS['LANGINDEX']]; ?>";

		if (confirm(confirmMsg)) {
			
			alert("<?php echo $msg_reconnect[$GLOBALS['LANGINDEX']];?>");
			var msg = "<SetReboot/>";
			if (type == "Reset") {
				InitCookie();				
				msg = "<SetReset><Type>"+($('#upgrade_reset_all').is(':checked') ? 1 : 0)+"</Type></SetReset>";
			}

			RequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI'].'?seq='.$_SESSION['count'] ?>", "PAGE_CLOSE");
		}
		$("#upgrade_reset").removeAttr('disabled');
		$("#upgrade_restart").removeAttr('disabled');
	}

	function InitCookie()
	{
		SetCookie("PresetStatus",1);
		SetCookie("SequenceSetupStatus",1);
		SetCookie("AutorunStatus", 0);
		SetCookie("SwingStatus",0);
		SetCookie("GroupStatus",1);
		SetCookie("TourGroupStatus",0)
	}
	
	function OnClickBackup()
	{
		isBackup = false;
		alert("<?php echo $msg_reconnect[$GLOBALS['LANGINDEX']]; ?>");
		window.open('about:blank', '_self').close();
	}

	function OnClickRestore()
	{
		alert("<?php echo $msg_reconnect[$GLOBALS['LANGINDEX']]; ?>");
		window.open('about:blank', '_self').close();
	}

	function OnRestoreFailure()
	{
		relocate_page = "/home/system_upgrade.cgi";
		window.setTimeout("RefreshPage(relocate_page, 1)", 2000);
	}

	function RefreshPage(relocate_page, state)
	{
		window.location.href = relocate_page;
		if (state) window.location.reload(true);
	}

	function SetBackup()
	{
		isBackup = true;
	}

	function OnUnload()
	{
		RequestAjaxMsg("<SetReboot/>", "<?php echo $msg_reconnect[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $GLOBALS['REQUEST_URI'].'?seq='.$_SESSION['count'] ?>", "PAGE_CLOSE");
	}

	function OnClickUpgradeStart()
	{
		document.location = "./upgrade.cgi";
	}
	function OnClickBackupButton() {
		backupForm.submit();		
		$("#infoMsg").css("visibility", "visible");
	}
	
	var isRestoreDone = 0;
	function restoreFileOnChange() {
		var element = document.getElementById("restoreFile");		        
 		var i = 0, img, reader, file;		
		var fileName = element.value.split('/').pop().split('\\').pop();
		var ext = fileName.split('.').pop();

		//Check for file extension validity.
		if (ext != "bin") {
		  alert("<?php echo $msg_wrong_file[$GLOBALS['LANGINDEX']]; ?>");
		  $("#restoreForm").get(0).reset();
		  element.focus();
		  return;
		}

		// adding file name to text box
		var fullPath=$('#restoreFile').val();
		var filename = fullPath.replace(/^.*[\\\/]/, '')
		$('#RestoreText').val(filename);

		setTimeout(function () {
			if (isRestoreDone == 0) {
				$("#restoreForm").get(0).reset();
				alert("<?php echo $msg_recoverFileError[$GLOBALS['LANGINDEX']]; ?>");
			}
		}, 10000);
		
		 $('#restoreForm').ajaxSubmit({
		 	success : function (res) {
			        if(res == 'success') {
					  isRestoreDone = 1;
			          OnClickRestore();	
			        } else if(res == 'failure') {
						isRestoreDone = 1;
   					 $("#restoreForm").get(0).reset();    
			          alert("<?php echo $msg_sendRequestError[$GLOBALS['LANGINDEX']]; ?> <?php echo $msg_tryAgain[$GLOBALS['LANGINDEX']]; ?>");
			        } else if(res == 'filesizelimitexceeded') {
						isRestoreDone = 1;
			        	 $("#restoreForm").get(0).reset();
			          alert("<?php echo $msg_wrong_file[$GLOBALS['LANGINDEX']]; ?>");
			        } else {
						isRestoreDone = 1;
			        	 $("#restoreForm").get(0).reset();
			          alert("<?php echo $msg_recoverFileError[$GLOBALS['LANGINDEX']]; ?>");
			        }
				},
			 error: function (xhr, ajaxOptions, thrownError) {
				isRestoreDone = 1;
				$("#restoreForm").get(0).reset();
			    alert("<?php echo $msg_recoverFileError[$GLOBALS['LANGINDEX']]; ?>");
			  },
			 timeout: 10000
		 });

		return;	
	}
	
	function OnLoad()
	{
		// draw plugin area
		SISOPlugin.init(installMsg, 0, 0);
	}
	
	function onDownloadClick() {
		$("#infoMsg").css("visibility", "visible");	
		var url;
		if (  window.location.protocol == 'https:' ) {
			url = "https://" + location.host;
		}
		else
		{
			url = "http://" + location.host;
		}
		var result = SISOPlugin.onClickBackupConfiguration(url,encName,encPW);
		
		if(result == 1)		// Success
		{
				alert("<?php echo $msg_reconnect[$GLOBALS['LANGINDEX']]; ?>");
				window.open('about:blank', '_self').close();
		}
		else					// fail
		{
				$("#infoMsg").css("visibility", "hidden");
		}
	}

	</script>
	
	<style type="text/css">

	.FileUpload {
	   position:relative;
	}

	.FileField {
	   width:155px;
	   height:15px;
	   margin-right:85px;
	   border:solid 1px #CFD2D9;
	   font-size:16px;
		background:#CFD2D9;
		width:200px;
		margin-top: 1px;
		float: left;	
	}
/*
	#restoreFile {
	   position:relative;
		width: 125px;
		height: 21px;
	   text-align: right;
	   -moz-opacity:0;
	   filter:alpha(opacity: 0);
	   opacity: 0;
	   z-index: 2;
		float: left;
	}
*/
	.btn_restore {
		display:inline-block;
		width:145px;
		height:19px;
		margin-top:1px;
		padding-top:2px;
		background:#1b2029;
		text-align:center;
		vertical-align:middle;
		font-weight:bold;
	}

	.btn_restore:hover {
		background:#0b76d5;
		text-decoration:none;
	}

	.btn_restore input {
		position: absolute;
		left: 0;
		top: 0;
		width:145px;
		opacity: 0;
		filter: alpha(opacity=0);
		direction: ltr;
		cursor: pointer;
	}

	</style>
	</head>
	<body onselectstart="return false" onload="OnLoad()">
		<div id="wrap">
			<div id="head">
			<?php
				require_once ('left_menu.cgi');
				require_once ('top_menu.cgi');
			?>
			<div id="container">
			<?php
				PrintLeftMenu($_SERVER['SCRIPT_NAME']);
			?>
			<div id="contents" >
				<div class="h3_tit mgt0" >
					<h3><?php echo $t_upgrade[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>
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
						<tr>
							<td colspan="2">
								<a id="upgrade_btn" class="btn_type01 btn_type01_11" href="javascript:OnClickUpgradeStart()"><?php echo $t_upgrade[$GLOBALS['LANGINDEX']]; ?></a>
							</td>
						</tr>
					</tbody>
				</table>
				<div class="h3_tit">
					<h3 class="wid280"><?php echo $t_factoryDefault[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>
				<table class="data_write">
					<colgroup>
						<col />
					</colgroup>
					<tbody>
						<tr>
							<td>
								<label><input type="radio" name="upgrade_reset_type" id="upgrade_reset_except" checked="checked" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/>
									<?php 
										if ($GLOBALS['M_SUPPORT_OPENSDK']){
											echo $t_resetExceptNetwork_SDK[$GLOBALS['LANGINDEX']];
										}else{
											echo $t_resetExceptNetwork[$GLOBALS['LANGINDEX']];
										}
									?>
								</label>
								<label><input type="radio" name="upgrade_reset_type" id="upgrade_reset_all"/><?php echo $t_resetAll[$GLOBALS['LANGINDEX']]; ?></label>
							</td>
						</tr>
						<tr>
							<td>
								<a id="upgrade_reset" class="btn_type01 btn_type01_11" href="javascript:OnClickReboot('Reset')"><?php echo $t_reset[$GLOBALS['LANGINDEX']]; ?></a>
							</td>
						</tr>
					</tbody>
				</table>
				<div class="h3_tit">
					<h3 class="wid400"><?php echo $t_configurationBackupRestore[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>
            <div id="backup_area">
               <a id="backup_button" style="float:left;margin-left:10px" class="btn_type01 btn_type01_11" href="javascript:onDownloadClick();" > <?php echo $btn_backup[$GLOBALS['LANGINDEX']]; ?> </a>
					<div style="position:absolute; left:495px">
						<form method="POST" name="restoreForm" id="restoreForm" action="config_restore.cgi" enctype="multipart/form-data" > 
							<div class="FileUpload">
								<span class = "btn_restore">
									<input type="file" name="restoreFile" id="restoreFile" accept=".bin" onchange="restoreFileOnChange();" style="font-size:20px; right:0; height:22px;"/>
									<span><?php echo $btn_restore[$GLOBALS['LANGINDEX']]; ?></span>
								</span>
							</div>
						</form>	
					</div>
               <form method="POST" name="backupForm" target="backupFormResult" action="config_backup.cgi" style="visibility:hidden"> </form>
               <iframe id="backupFormResult" style="display:none"> </iframe>               
            </div>
            <br/>
            <div id="infoMsg" class="style7" style="display:none; color:red;"><b><?php echo $t_time_wait[$GLOBALS['LANGINDEX']]; ?></b></div>
            <br/>
				<div class="h3_tit">
					<h3 class="wid400"><?php echo $t_restart[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>
				<div id="statusDialog1" style="display:none">
					<?php echo $msg_reconnect[$GLOBALS['LANGINDEX']]; ?>
				</div>
				<div>
					<a id="upgrade_restart" class="btn_type01 btn_type01_11" style="float:left;margin-left:10px" href="javascript:OnClickReboot('Reboot')"><?php echo $t_restart[$GLOBALS['LANGINDEX']];?></a>
				</div>
			</div>
		</div>
	</div>
	</div>
	<span id="pluginArea" style="width:0;height:0;"></span>
</body>
</html>
