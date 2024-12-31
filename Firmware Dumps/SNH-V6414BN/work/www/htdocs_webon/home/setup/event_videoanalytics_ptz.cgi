<?php
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_menu.cgi');
require_once ('../language/language_event_common.cgi');
require_once ('../language/language_event_videoanalytics.cgi');

$event_name = 'va';
$msg = '';
$presetNo = 1;
$mdvaSetupMode = 'global';
if (isset($_REQUEST['presetNo']) && $_REQUEST['presetNo'] > 0) {
	$presetNo = $_REQUEST['presetNo'];
	require_once ('../../cgi-bin/adv/presetedit.class');

	$GLOBALS['SOCKET_MANAGER'] = new SocketManager();
	$presetVaConf = new PresetVAConfiguration();
	$presetVaConf->payload = pack('i1', $_REQUEST['presetNo']);
	$GLOBALS['SOCKET_MANAGER']->Connection($presetVaConf);
	$msg = $presetVaConf->GetXMLData();
	$mdvaSetupMode = 'preset';
	if (isset($_REQUEST['inner'])) {
		echo $msg;
		exit;
	}
}
else if (isset($_REQUEST['mdva'])) {
	require_once ('../../cgi-bin/adv/va.class');
	
	$GLOBALS['SOCKET_MANAGER'] = new SocketManager();
	$vaConf = new VAConfiguration();
	$GLOBALS['SOCKET_MANAGER']->Connection($vaConf);
	$msg = $vaConf->GetXMLData();
	$mdvaSetupMode = 'global';
	echo $msg;
	exit;
}

$classInstances= GetClassInstance($event_name);
$event_class	= $classInstances['VAConfiguration'];
if ($mdvaSetupMode == 'global') {
	$msg = $event_class->GetXMLData();
}
$presetConf 	= $classInstances['PTZPreset'];

$isDIS = $classInstances['Information']->dataInfo['DIS']['value'];
// DEV_S1WEBVIEWER Start
$userClassInstance = GetClassInstance('user');
$userConf	= $userClassInstance['UserConfiguration'];
// DEV_S1WEBVIEWER End
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="kr" xml:lang="kr">
<head>
	<title>iPOLiS NETWORK CAMERA WEBVIEWER</title>
	<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
	<meta http-equiv="X-UA-Compatible" content="IE=Edge; requiresActiveX=true" />
	<link rel="stylesheet" type="text/css" href="../css/techwin.css" />
	<link rel="stylesheet" type="text/css" href="../css/jquery.ui.slider.css"/>
	<link rel="stylesheet" type="text/css" href="../css/jquery.ui.core.css"/>
	<link rel="stylesheet" type="text/css" href="../css/jquery.ui.tabs.css"/>
	<link rel="stylesheet" type="text/css" href="../css/jquery.ui.theme.css"/>
	<link rel="stylesheet" type="text/css" href="../css/jquery.ui.spinner.css"/>
	<link rel="stylesheet" type="text/css" href="../css/event_canvas.css" />
	<style>
		#lnb-list {
			height:1750px;
		}
		
		.ui-tabs .ui-tabs-nav li 
		{
		  border: 0px;
		}
		.ui-tabs .ui-tabs-nav li a 
		{
		   background-color: #868fa3;
		   border: 1px solid #5e6472;
		   border-bottom-width: 0px;
		   color: #212121;
			padding: .2em .5em;
		}
		.ui-tabs .ui-tabs-nav .ui-tabs-active a
		{
			background-color: #0087ef;
			border: 1px solid #5e6472;
			border-bottom-width: 0px;
			color: #ffffff;
			font-weight: bold; 
		}
		.ui-tabs .ui-tabs-panel
		{
			border-bottom-right-radius:0px;
			border-bottom-left-radius:0px;
			border: 1px solid #5e6472;
		}
		#tmMinute .ui-dialog-content{
			margin-left: 20px;
		}
	</style>
	<script type="text/javascript" src="../js/jquery-1.9.1.js"></script>
	<script type="text/javascript" src="../js/lnb.js"></script>
	<script type="text/javascript" src="../js/common_function.js"></script>
	<script type="text/javascript" src="../js/jquery-ui.js"></script>
	<script type="text/javascript" src="../js/jquery.cookie.js"></script>
	<script type="text/javascript" src="../js/jquery.ui.dialog.js"></script>
	<script type="text/javascript" src="../js/timeSchedule.js"></script>
	<script type="text/javascript" src="../js/eventcontrol.js"></script>
	<script type="text/javascript" src="../js/pluginCheck.js"></script>
	<script type="text/javascript" src="../js/pluginControl.js"></script>
	<!--[if lt IE 9]><script type="text/javascript" src="../js/excanvas.js"></script><![endif]-->
	<script type="text/javascript" src="../js/md_va.js"></script>
	<script type="text/javascript" src="../js/videoanalytics_function.js"></script>
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
	var ajaxReqUrl 			= "<?php echo $GLOBALS['REQUEST_URI']; ?>";
	var encName 				= "<?php echo $GLOBALS['USERINFO']['encname']; ?>";
	var encPW					= "<?php echo $GLOBALS['USERINFO']['encpw']; ?>";
	var devicePort 			= <?php echo $classInstances['Information']->dataInfo['DevicePort']['value']; ?>;
	var previewProfileNo 	= <?php echo $classInstances['Information']->dataInfo['PreviewProfileNo']['value']; ?>;
	var installMsg				= new Array();
	installMsg[0] 				= "<?php echo $msg_plugin_install[$GLOBALS['LANGINDEX']]; ?>";
	installMsg[1] 				= "<?php echo $msg_plugin_install2[$GLOBALS['LANGINDEX']]; ?>";
	installMsg[2] 				= "<?php echo $msg_notsupport_plugin[$GLOBALS['LANGINDEX']]; ?>";
	
	var viewerWidth			= <?php echo $GLOBALS['VIEWER_RESOLUTION']['width']; ?>;
	var viewerHeight			= <?php echo $GLOBALS['VIEWER_RESOLUTION']['height']; ?>;
	var maxResolution			= {width: <?php echo $GLOBALS['MAX_RESOLUTION']['width'] ?>, height: <?php echo $GLOBALS['MAX_RESOLUTION']['height'] ?>};
	var FLIP						= parseInt(<?php echo $classInstances['Information']->dataInfo['Flip']['value']; ?>);
	var MIRROR					= parseInt(<?php echo $classInstances['Information']->dataInfo['Mirror']['value']; ?>);
	var okLang 					= "<?php echo $t_ok[$GLOBALS['LANGINDEX']]; ?>";
	var cancelLang				= "<?php echo $t_cancel[$GLOBALS['LANGINDEX']]; ?>";
	var deleteLang				= "<?php echo $t_delete[$GLOBALS['LANGINDEX']]; ?>";
	var titleLang				=["<?php echo $t_virtual_line_based[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $t_defined_area[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $t_entire_area[$GLOBALS['LANGINDEX']]; ?>"]
	var directionLang			=["<?php echo $t_right[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $t_left[$GLOBALS['LANGINDEX']]; ?>"]
	var currentVaMode 		= '';
	var mdvaXmlMsg 			= "<?php echo $msg; ?>";
	var event_name				= "<?php echo $event_name; ?>";
	
	var presetCnt = 0;	
	var currentPresetNo = <?php echo $presetNo; ?>;
	var currentMdVaSetupType = "<?php echo $mdvaSetupMode; ?>";
	
	$(document).ready(function(){
		lnbonoff("lnb_event");
		
		SISOPlugin.init(installMsg, viewerWidth, viewerHeight);

		// DEV_S1WEBVIEWER start
		//SISOPlugin.startPluginPlay(devicePort,previewProfileNo,encName,encPW);
		<?php if ($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>
			SISOPlugin.startS1PluginPlay(devicePort,previewProfileNo,encName,encPW,<?php echo $userConf->dataInfo['IsEnableNoEncrypt']['value']; ?>);
		<?php } else { ?>
			SISOPlugin.startPluginPlay(devicePort,previewProfileNo,encName,encPW);
		<?php } ?>
		// DEV_S1WEBVIEWER end

		if(BrowserDetect.browser == 'Chrome'){
			$(window).on('beforeunload', function(){
			if (currentMdVaSetupType == 'preset') {
				RequestStartStopPresetEdit('Stop');
			}
			});
		}
		else{
			$(window).on('unload', function(){
			if (currentMdVaSetupType == 'preset') {
				RequestStartStopPresetEdit('Stop');
			}
			});
		}	
	});
	
	function OnClickApply()
	{
		if (CheckScheduleSetting("<?php echo $event_name; ?>") == 0) {
			alert("<?php echo $msg_checkthetable[$GLOBALS['LANGINDEX']]; ?>");
			return; 
		}

		var msg = "";
		if (currentMdVaSetupType == 'global') {
			msg += "<SetVAConfiguration>";
			msg += MakeVideoAnalyticsXml();			//event_va.cgi
			msg += "</SetVAConfiguration>";
		}
		else {	
			msg += "<SetVAConfiguration>";
			msg += "<MDConfiguration>";
			<?php if($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>	
			msg += MakeScheduleAndActionSetupXML_S1("<?php echo $event_name; ?>");
			<?php } else { ?>
			msg += MakeScheduleAndActionSetupXML("<?php echo $event_name; ?>");	
			<?php } ?>
			msg += "</MDConfiguration>";
			msg += "</SetVAConfiguration>";
			RequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI'].'?seq='.$_SESSION['count'] ?>", "NO_REFRESH");

			msg = "";
			msg += "<SetPresetVAConfiguration>";
			msg += "<Index>"+$("#PresetList").val()+"</Index>";
			msg += MakeVideoAnalyticsXml();
			msg += "</SetPresetVAConfiguration>";
		}
		RequestAjaxMsg(msg, "<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $GLOBALS['REQUEST_URI'].'?seq='.$_SESSION['count'] ?>", "NO_REFRESH");
	}

	function OnClickMdVaType(type)
	{
		currentMdVaSetupType = type;
		if (currentMdVaSetupType == 'global') {
			$('#PresetList').hide();
			RequestGetMdVaSetup();
			RequestStartStopPresetEdit('Stop');
		}
		else {
			$('#PresetList').show();
			OnChangePresetList();
		}
		$("#md_tabs").tabs("option", "active", 0);
		$("#va_tabs").tabs("option", "active", 0);
	}

	function OnChangePresetList()
	{
		RequestGetMdVaSetup();
		RequestStartStopPresetEdit('Start');		
	}

	function RequestGetMdVaSetup()
	{
		var reqUrl = "<?php echo GetMyRequestURI($_SERVER['SCRIPT_NAME']); ?>";
		if (BrowserDetect.browser == "Explorer" || (BrowserDetect.browser == 'Safari' && reqUrl.search('.local') != -1)) {
			reqUrl = ".."+reqUrl.substr(reqUrl.indexOf("/setup/"));
		}

		var reqMsg = '';
		if (currentMdVaSetupType == 'global') {
			reqMsg = "mdva=1&pctz="+(new Date()).getTime();
		}
		else {
			if($("#PresetList").val() == null){
				var firstVal = $("#PresetList option :eq(0)").attr("value");
				$("#PresetList").val(parseInt(firstVal,10));
			}
		
			reqMsg = "presetNo="+$("#PresetList").val()+"&inner=1&pctz="+(new Date()).getTime();
		}
		
	  	$.ajax({
	  		type: "POST",
	  		data: reqMsg,
	  		async: false,
	  		cache: false,
	  		url: reqUrl,
	  		dataType: "xml",
	  		success: OnSuccessMdVaSetup,
	  		error: null
	  	});
	}

	function OnSuccessMdVaSetup(xml)
	{
		$(xml).find("VAConfiguration").each(function() {
			ParsingXML_VAConfiguration($(this));
		});
	}

	function RequestStartStopPresetEdit(actionMsg)
	{
		if ($("#PresetList").val() < 1)	return;
		var msg = '';
		msg += "<"+actionMsg+"PTZPreseEdit>";
		msg += "<Index>"+$("#PresetList").val()+"</Index>";
		msg += "</"+actionMsg+"PTZPreseEdit>";
	  	RequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, "NO_REFRESH");
		localSeq++;

		SetCookie("PresetStatus", $("#PresetList").val());
	}
	
	function OnLoad()
	{
		if (currentMdVaSetupType == 'global') {
			$('#event_md_va_type_global').prop("checked", true);
			if (presetCnt == 0) {
				$('#event_md_va_type_preset').attr("disabled", "disabled");
			}
			else {
				$("#PresetList").val(currentPresetNo);
			}
			currentVaMode = ($('#event_<?php echo $event_name; ?>_mode_md').is(":checked") ? 'md' : 'va');
			InitIVConfiguration($($.parseXML(mdvaXmlMsg)));			//event_va.cgi
		}
		else {
			$('#event_md_va_type_preset').prop("checked", true);
			$("#PresetList").val(currentPresetNo);
			$('#PresetList').show();
			OnSuccessMdVaSetup($.parseXML(mdvaXmlMsg));
			RequestStartStopPresetEdit('Start');
			SetCookie("PresetStatus", $("#PresetList").val());
		}
	}
</script>

	</head>
	<body onload="OnLoad()" onselectstart="return false">
		<div id="wrap">	
		<?php
			require_once ('left_menu.cgi');
			require_once ('top_menu.cgi');
		?>
		<div id="container" style='width:1400px;'>
		<?php
			PrintLeftMenu($_SERVER['SCRIPT_NAME']);
		?>
			<div id="contents"  style="width:680px;">							
				<?php
					require_once('plugin_ui.cgi');
				?>
					<div class="h3_tit">
							<h3 class="wid400"><?php echo $t_md_va[$GLOBALS['LANGINDEX']]; ?></h3>
					</div>				
					<table class="data_write">
						<colgroup>
							<col style="width:180px;"/>
							<col />
						</colgroup>
						<tbody>	
							<tr>
								<th scope="row"><?php echo $t_type[$GLOBALS['LANGINDEX']]; ?></th>
								<td>
									<label><input type="radio" name="event_md_va_type" id="event_md_va_type_global" onclick="OnClickMdVaType('global')" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_global[$GLOBALS['LANGINDEX']]; ?></label>
								</td>
							</tr>
							<tr height="35px">
								<th></th>
								<td style="vertical-align:top">
									<label><input type="radio" name="event_md_va_type" id="event_md_va_type_preset" onclick="OnClickMdVaType('preset')" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"><?php echo $t_preset[$GLOBALS['LANGINDEX']]; ?></label>
									<select class="selectbox_style" id="PresetList" onchange="OnChangePresetList()" style="display:none; float:none;">
							<?php
								$presetCnt = 0;
								for($index=1; $index<=MAX_PTZ_PRESET255; ++$index){
									if ($presetConf->preset[$index-1]['Enabled']['value'] == 0) continue;
									$presetCnt++;
							?>
										<option value="<?php echo $index; ?>" ><?php echo $index.':'.trim($presetConf->preset[$index-1]['Name']['value']); ?></option>
							<?php
								}
							?>
									</select>
									<script>
										presetCnt = <?php echo $presetCnt; ?>;
									</script>
								</td>
							</tr>
							<tr>
								<th scope="row"><?php echo $t_enable[$GLOBALS['LANGINDEX']]; ?></th>
								<td>
									<label><input type="radio" name="event_<?php echo $event_name; ?>_use" id="event_<?php echo $event_name; ?>_use_on"  value="1" <?php if ($classInstances['VAConfiguration']->mdConf->dataInfo['Enabled']['value'] == 1 || $classInstances['VAConfiguration']->ivConf->dataInfo['Enabled']['value'] == 1) echo "checked=\"checked\""; ?> style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_on[$GLOBALS['LANGINDEX']]; ?></label>
									<label><input type="radio" name="event_<?php echo $event_name; ?>_use" id="event_<?php echo $event_name; ?>_use_off" value="0" <?php if ($classInstances['VAConfiguration']->mdConf->dataInfo['Enabled']['value'] == 0 && $classInstances['VAConfiguration']->ivConf->dataInfo['Enabled']['value'] == 0) echo "checked=\"checked\""; ?> /><?php echo $t_off[$GLOBALS['LANGINDEX']]; ?></label>
								</td>
							</tr>
							<tr>
								<th><?php echo $t_mode[$GLOBALS['LANGINDEX']] ?></th>
								<td>
									<label><input type="radio" name="event_<?php echo $event_name; ?>_mode" id="event_<?php echo $event_name; ?>_mode_md" value="0" onClick="OnClickVaMode('md')" <?php if ($classInstances['VAConfiguration']->dataInfo['Mode']['value'] == 0) echo "checked=\"checked\""; ?> style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_md[$GLOBALS['LANGINDEX']]; ?></label>
								</td>
							</tr>
							<tr>
								<th></th>
								<td>
									<label><input type="radio" name="event_<?php echo $event_name; ?>_mode" id="event_<?php echo $event_name; ?>_mode_va" value="1" onClick="OnClickVaMode('va')" <?php if ($classInstances['VAConfiguration']->dataInfo['Mode']['value'] == 1) echo "checked=\"checked\""; ?> style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_videoAnalytics[$GLOBALS['LANGINDEX']]; ?></label>
								</td>
							</tr>	
						</tbody>
					</table>	
					<?php
						$vaConf = $classInstances['VAConfiguration'];
						require_once('./event_setup/event_va_ptz.cgi');
						$event_class = $classInstances['VAConfiguration']->mdConf;
						require_once('eventsetup_ui.cgi');
					?>
					<div class="btn_right">
						<a id="mid_ok_btn" class="btn_apply" href="javascript:OnClickApply()"><?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?></a>
					</div>
				</div>
			</div>
		</div>
	</body>
</html>
