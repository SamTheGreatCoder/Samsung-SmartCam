<?php
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_av_ptz.cgi');
require_once ('../language/language_menu.cgi');

$classInstances= GetClassInstance('');

// DEV_S1WEBVIEWER Start
$userClassInstance = GetClassInstance('user');
$userConf	= $userClassInstance['UserConfiguration'];
// DEV_S1WEBVIEWER End
$event_name = 'focussetup';
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="kr" xml:lang="kr">
<head>
	<title>iPOLiS NETWORK CAMERA WEBVIEWER</title>
	<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
	<link rel="stylesheet" type="text/css" href="../css/techwin.css" />
	<script type="text/javascript" src="../js/jquery-1.9.1.js"></script>
	<script type="text/javascript" src="../js/jquery-ui.js"></script>
	<script type="text/javascript" src="../js/lnb.js"></script>
	<script type="text/javascript" src="../js/common_function.js"></script>
	<script type="text/javascript" src="../js/pluginCheck.js"></script>
	<script type="text/javascript" src="../js/pluginControl.js"></script>
	<!--[if lt IE 9]><script type="text/javascript" src="../js/excanvas.js"></script><![endif]-->	
	<script type="text/javascript" src="../js/focus_setup.js"></script>
	<script type="text/javascript" language="javascript">
	<?php if ($GLOBALS['M_SUPPORT_MOTORIZE'] == 0) { ?>
		document.location = "../../index.htm";
	<?php } ?>
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
	var maxResolution			= {width: <?php echo $GLOBALS['MAX_RESOLUTION']['width'] ?>, height: <?php echo $GLOBALS['MAX_RESOLUTION']['height'] ?>};
	
	$(document).ready(function(){ 
		lnbonoff("lnb_av"); 

		$(document).mouseup(function() {
			if(firstDrawClick && isDrawDragging){
				$("#imgTemp").trigger("mouseup");
			}
		});
		
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

	function OnClickMotorizedMove(ptzMode, value)
	{
		var msg="";
		msg += "<StartMotorizedLensSetup>";
		if (ptzMode == 'zoom') {
			msg += "<Mode>0</Mode>";
			msg += "<PTZ>";
			msg += "<ZoomReal>" + value + "</ZoomReal>";
		}
		else { 
			msg += "<Mode>1</Mode>";
			msg += "<PTZ>";
			msg += "<FocusReal>" + value + "</FocusReal>";
		}
		msg += "</PTZ>";
		msg += "<AF>0</AF>";
		msg += "</StartMotorizedLensSetup>";
		RequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, "NO_REFRESH");
		localSeq++;
	}

	function OnClickAutoFocus(value)
	{
		var msg="";
		msg += "<StartMotorizedLensSetup>";
		msg += "<Mode>2</Mode>";
		msg += "<AF>"+value+"</AF>";
		if (value == 1 && focusSetup.drawings.getWidth(0) > 0 && focusSetup.drawings.getHeight(0) > 0) 
		{
			msg += "<FocusArea>";
			msg += "<Enable>1</Enable>";
			msg += focusSetup.drawings.setArea_xml();
			msg += "</FocusArea>";
			focusSetup.drawings.clearArea();
		}
		else
		{
			msg += "<FocusArea>";
			msg += "<Enable>0</Enable>";
			msg += "</FocusArea>";
		}
		msg += "</StartMotorizedLensSetup>";
		RequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, "NO_REFRESH");
		localSeq++;
	}

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
		
		if(BrowserDetect.browser == "Explorer" && getIEVersion() <= 8){
			var intervalId = window.setInterval(function(){
				var isFirstDecoding = SISOPlugin.getRelayStatus(90);
				if(isFirstDecoding == 1){
					window.clearInterval(intervalId);
					InitFocusArea();
				}
			}, 100);
		}else{
			InitFocusArea();
		}
	}

	function InitFocusArea(){
		focusSetup.init(maxResolution.width,maxResolution.height);
		focusSetup.drawings.rectangle(viewerWidth,viewerHeight);	
	}

	</script>
</head>
<body onselectstart="return false" onload="OnLoad()">
	<div id="wrap">
		<?php
			require_once ('left_menu.cgi');
			require_once ('top_menu.cgi');
		?>
		<div id="container">
		<?php
			PrintLeftMenu($_SERVER['SCRIPT_NAME']);
		?>
			<div id="contents" style="width:680px;">
				<?php
					require_once ('plugin_ui.cgi');
				?>
				<div id="focus" style="margin-top:20px; width:680px">
				<table class="data_write" >
					<colgroup>
						<col style="width:250px;" />
						<col />
					</colgroup>
					<tbody>
						<tr>
							<th scope="row"><?php echo $t_focus[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<a class="btn_type02" style="width:60px;" href="javascript:OnClickMotorizedMove('focus', -100)">-100</a>
								<a class="btn_type02" style="width:60px;" href="javascript:OnClickMotorizedMove('focus', -10)">-10</a>
								<a class="btn_type02" style="width:60px;" href="javascript:OnClickMotorizedMove('focus', -1)">-1</a>
								<a class="btn_type02" style="width:60px;" href="javascript:OnClickMotorizedMove('focus', 1)">+1</a>
								<a class="btn_type02" style="width:60px;" href="javascript:OnClickMotorizedMove('focus', 10)">+10</a>
								<a class="btn_type02" style="width:60px;" href="javascript:OnClickMotorizedMove('focus', 100)">+100</a>
							</td>
						</tr>
						<?php if ($GLOBALS['M_SUPPORT_MOTORIZE'] == MOTORIZE_FOCUS_ZOOM_SUPPORT) { ?>
						<tr>
							<th scope="row"><?php echo $t_zoom[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<a class="btn_type02" style="width:60px;" href="javascript:OnClickMotorizedMove('zoom', -100)">-100</a>
								<a class="btn_type02" style="width:60px;" href="javascript:OnClickMotorizedMove('zoom', -10)">-10</a>
								<a class="btn_type02" style="width:60px;" href="javascript:OnClickMotorizedMove('zoom', -1)">-1</a>
								<a class="btn_type02" style="width:60px;" href="javascript:OnClickMotorizedMove('zoom', 1)">+1</a>
								<a class="btn_type02" style="width:60px;" href="javascript:OnClickMotorizedMove('zoom', 10)">+10</a>
								<a class="btn_type02" style="width:60px;" href="javascript:OnClickMotorizedMove('zoom', 100)">+100</a>
							</td>
						</tr>
						<?php } ?>
						<tr>
							<th scope="row"><?php echo $t_simpleFocus[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								&nbsp;<a id="af_btn" href="javascript:OnClickAutoFocus(1)" style="margin-left:0px"><img src="../images/common/btn/log_01.png"/></a>
							</td>
						</tr>
						<?php if ($GLOBALS['M_SUPPORT_MOTORIZE'] == MOTORIZE_FOCUS_ONLY_SUPPORT) { ?>
						<tr>
							<th scope="row"><?php echo $t_reset[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								&nbsp;<a id="af_btn" href="javascript:OnClickAutoFocus(0)" style="margin-left:0px"><img src="../images/common/btn/log_01.png"/></a>
							</td>
						</tr>
						<?php } ?>
					</tbody>
				</table>
				</div>
			</div>
		</div>
	</div>
</body>
</html>
