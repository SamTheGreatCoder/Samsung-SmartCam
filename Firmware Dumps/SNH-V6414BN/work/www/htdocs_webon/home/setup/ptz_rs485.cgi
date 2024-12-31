<?php
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_menu.cgi');
require_once ('../language/language_av_ptz.cgi');

$classInstances = GetClassInstance('ptzsetup');
$presetConf 	= $classInstances['PTZPreset'];
$serialConf 	= $classInstances['SerialConfiguration'];

$event_name = "ptzlimit";

// DEV_S1WEBVIEWER Start
$userClassInstance = GetClassInstance('user');
$userConf	= $userClassInstance['UserConfiguration'];
// DEV_S1WEBVIEWER End
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="kr" xml:lang="kr">
<head>
	<title>iPOLiS NETWORK CAMERA WEBVIEWER</title>
	<meta http-equiv="X-UA-Compatible" content="IE=Edge; requiresActiveX=true" /> 
	<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
	<link rel="stylesheet" type="text/css" href="../css/techwin.css" />
	<link rel="stylesheet" type="text/css" href="../css/jquery.ui.slider.css"/>
	<script type="text/javascript" src="../js/jquery-1.9.1.js"></script>
	<script type="text/javascript" src="../js/jquery-ui.js"></script>
	<script type="text/javascript" src="../js/lnb.js"></script>
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

	var localSeq				= <?php echo $_SESSION['count']; ?>;
	var ajaxReqUrl				= "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq;
	var encName 				= "<?php echo $GLOBALS['USERINFO']['encname']; ?>";
	var encPW 					= "<?php echo $GLOBALS['USERINFO']['encpw']; ?>";
	var devicePort 			= <?php echo $classInstances['Information']->dataInfo['DevicePort']['value']; ?>;
	var previewProfileNo 	= <?php echo $classInstances['Information']->dataInfo['PreviewProfileNo']['value']; ?>;
	var installMsg				= new Array();
	installMsg[0] 				= "<?php echo $msg_plugin_install[$GLOBALS['LANGINDEX']]; ?>";
	installMsg[1] 				= "<?php echo $msg_plugin_install2[$GLOBALS['LANGINDEX']]; ?>";
	installMsg[2] 				= "<?php echo $msg_notsupport_plugin[$GLOBALS['LANGINDEX']]; ?>";

	var viewerWidth 			= <?php echo $GLOBALS['VIEWER_RESOLUTION']['width']; ?>;
	var viewerHeight 			= <?php echo $GLOBALS['VIEWER_RESOLUTION']['height']; ?>;
	
	$(document).ready(function(){
		lnbonoff("lnb_ptz");		
		
		if(BrowserDetect.browser == 'Chrome'){
			$(window).on('beforeunload', function(){
				SISOPlugin.onPluginUnload();
			});
		}
		else{
			$(window).on('unload', function(){
				SISOPlugin.onPluginUnload();
			});
		}
	});
	
	function OnLoad()
	{
		SISOPlugin.init(installMsg, viewerWidth, viewerHeight);

		// DEV_S1WEBVIEWER start
		//SISOPlugin.startPluginPlay(devicePort,previewProfileNo,encName,encPW);
		<?php if ($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>
			SISOPlugin.startS1PluginPlay(devicePort,previewProfileNo,encName,encPW,<?php echo $userConf->dataInfo['IsEnableNoEncrypt']['value']; ?>);
		<?php } else { ?>
			SISOPlugin.startPluginPlay(devicePort,previewProfileNo,encName,encPW);
		<?php } ?>
		// DEV_S1WEBVIEWER end

	}

	function OnClickApply()
	{
		var msg = "";
		msg += "<SetSerial>";
		msg += "<BaudRate>"+$('#baudRate').val()+"</BaudRate>";
		msg += "<Protocol>"+$('#protocol').val()+"</Protocol>";
		msg += "<CameraID>"+$('#cameraID').val()+"</CameraID>";
		msg += "</SetSerial>";
		gActionCmd = "Apply";
		RequestAjaxMsg(msg, "<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq);
	}

	</script>
</head>

<body onload="OnLoad()" ononselectstart="return false">
	<div id="wrap">
		<?php
			require_once ('left_menu.cgi');
			require_once ('top_menu.cgi');
		?>
		<div id="container" style="width:1500px">
		<?php
			PrintLeftMenu($_SERVER['SCRIPT_NAME']);
		?>
			<div id="contents" >
				<?php
					require_once ('plugin_ui.cgi');
				?>
				<div class="h3_tit">
					<h3 class="wid320"><?php echo $menu_rs485[$GLOBALS["LANGINDEX"]]; ?></h3>
				</div>
				<table class="data_write">
					<colgroup>
						<col style="width:170px;" />
						<col />
					</colgroup>
					<tbody>
						<tr>
							<th scope="row"><?php echo $t_protocol[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<select  id="protocol" class="selectbox_style">
									<option value="0" <?php if ($serialConf->dataInfo['Protocol']['value'] == 0) echo 'selected'; ?>>SAMSUNG-T</option>
									<option value="1" <?php if ($serialConf->dataInfo['Protocol']['value'] == 1) echo 'selected'; ?>>SAMSUNG-E</option>
									<option value="2" <?php if ($serialConf->dataInfo['Protocol']['value'] == 2) echo 'selected'; ?>>PELCO-D</option>
									<option value="3" <?php if ($serialConf->dataInfo['Protocol']['value'] == 3) echo 'selected'; ?>>PELCO-P</option>
									<!-- SUNGJIN not supported-->
									<option value="5" <?php if ($serialConf->dataInfo['Protocol']['value'] == 5) echo 'selected'; ?>>PANASONIC</option>
									<option value="6" <?php if ($serialConf->dataInfo['Protocol']['value'] == 6) echo 'selected'; ?>>HONEYWELL</option>
									<option value="7" <?php if ($serialConf->dataInfo['Protocol']['value'] == 7) echo 'selected'; ?>>AD</option>
									<option value="8" <?php if ($serialConf->dataInfo['Protocol']['value'] == 8) echo 'selected'; ?>>VICON</option>
									<option value="9" <?php if ($serialConf->dataInfo['Protocol']['value'] == 9) echo 'selected'; ?>>GE</option>
									<option value="10" <?php if ($serialConf->dataInfo['Protocol']['value'] == 10) echo 'selected'; ?>>BOSCH</option>
								</select>
							</td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_cameraID[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<select id="cameraID" value="<?php echo $serialConf->dataInfo['CameraID']['value']; ?>" class="selectbox_style">
									<?php 	
										$max_id = 255;
										for ($index=1; $index<=$max_id; $index++) { ?>
										<option value="<?php echo $index; ?>" <?php if ($serialConf->dataInfo["CameraID"]["value"] == $index) echo "selected=\"selected\""; ?>><?php echo $index; ?></option>
									<?php } ?>
								</select>
							</td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_baudRate[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<select id="baudRate" class="selectbox_style">
									<option value="1" <?php if ($serialConf->dataInfo['BaudRate']['value'] == 1) echo 'selected'; ?>>2400</option>
									<option value="2" <?php if ($serialConf->dataInfo['BaudRate']['value'] == 2) echo 'selected'; ?>>4800</option>
									<option value="3" <?php if ($serialConf->dataInfo['BaudRate']['value'] == 3) echo 'selected'; ?>>9600</option>
									<option value="4" <?php if ($serialConf->dataInfo['BaudRate']['value'] == 4) echo 'selected'; ?>>19200</option>
								</select>
							</td>
						</tr>
					</tbody>
				</table>
				<div class="btn_right">
					<a id="mid_ok_btn" class="btn_apply" href="javascript:OnClickApply()"><?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?></a>
				</div>
  			</div> <!-- end contents-->
		</div>
	</div>
</body>
</html>
