<?php
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_menu.cgi');
require_once ('../language/language_event_common.cgi');
require_once ('../language/language_event_videoanalytics.cgi');

$event_name 	= 'va';
$classInstances= GetClassInstance($event_name);
$event_class	= $classInstances['VAConfiguration'];

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
			height:1650px;
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
	<script type="text/javascript" src="../js/jquery.ui.dialog.js"></script>
	<script type="text/javascript" src="../js/timeSchedule.js"></script>
	<script type="text/javascript" src="../js/eventcontrol.js"></script>
	<script type="text/javascript" src="../js/pluginCheck.js"></script>
	<script type="text/javascript" src="../js/pluginControl.js"></script>
	<!--[if lt IE 9]><script type="text/javascript" src="../js/excanvas.js"></script><![endif]-->
	<script type="text/javascript" src="../js/md_va.js"></script>
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
	var maxResolution			= {width:1920, height:1080};
	
	<?php if($GLOBALS['M_MAX_RESOLUTION'] == MAX_VGA){ ?>
		maxResolution.width = 704;
		maxResolution.height = 480;
	<?php }else if($GLOBALS['M_MAX_RESOLUTION'] == MAX_4CIF){  ?>
		maxResolution.width = 640;
		maxResolution.height = 480;
	<?php }else if($GLOBALS['M_MAX_RESOLUTION'] == MAX_1_MEGA){ ?>
		maxResolution.width = 1280;
		maxResolution.height = 1024; 	
	<?php }else if(($GLOBALS['M_MAX_RESOLUTION'] == MAX_3_MEGA && $GLOBALS['MEGAMODE'] == 2) || $GLOBALS['M_MAX_RESOLUTION'] == MAX_2_MEGA) { ?>
		maxResolution.width = 1920;
		maxResolution.height = 1080;		
	<?php }else if($GLOBALS['M_MAX_RESOLUTION'] == MAX_3_MEGA && $GLOBALS['MEGAMODE'] == 3) { ?>
		maxResolution.width = 2048;
		maxResolution.height = 1536;
	<?php } ?>
	
	var okLang 					= "<?php echo $t_ok[$GLOBALS['LANGINDEX']]; ?>";
	var cancelLang				= "<?php echo $t_cancel[$GLOBALS['LANGINDEX']]; ?>";
	var deleteLang				= "<?php echo $t_delete[$GLOBALS['LANGINDEX']]; ?>";
	var titleLang				=["<?php echo $t_virtual_line_based[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $t_defined_area[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $t_entire_area[$GLOBALS['LANGINDEX']]; ?>"]
	var directionLang			=["<?php echo $t_right[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $t_left[$GLOBALS['LANGINDEX']]; ?>"]

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
		<?php } ?>
		
		InitIVConfiguration();			//event_va.cgi
		
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
	
	function OnClickApply()
	{
		if (CheckScheduleSetting("<?php echo $event_name; ?>") == 0) {
			alert("<?php echo $msg_checkthetable[$GLOBALS['LANGINDEX']]; ?>");
			return; 
		}

		var msg = "";
		msg += "<SetVAConfiguration>";
		msg += MakeVideoAnalyticsXml();			//event_va.cgi
		msg += "</SetVAConfiguration>";
		RequestAjaxMsg(msg, "<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $GLOBALS['REQUEST_URI'].'?seq='.$_SESSION['count'] ?>");
	}
	
	function GetFilpMirrorStatus(){	
		var flip_mirror = 0;
		<?php if($classInstances['Information']->dataInfo['Flip']['value'] == 1 && $classInstances['Information']->dataInfo['Mirror']['value'] == 0) { ?>
			flip_mirror=1;
		<?php }else if($classInstances['Information']->dataInfo['Flip']['value'] == 0 && $classInstances['Information']->dataInfo['Mirror']['value'] == 1) { ?>
			flip_mirror=2;
		<?php }else if($classInstances['Information']->dataInfo['Flip']['value'] == 1 && $classInstances['Information']->dataInfo['Mirror']['value'] == 1) { ?>
			flip_mirror=3;
		<?php }else{ ?>
			flip_mirror=0;
		<?php } ?>
		
		return flip_mirror;
	}
	
	function OnLoad(){

	}
</script>
	</head>
	<body onload="OnLoad()" onselectstart="return false">
		<div id="wrap">	
		<?php
			require_once ('left_menu.cgi');
			require_once ('top_menu.cgi');
		?>
		<div id="container" <?php if($GLOBALS['M_SUPPORT_EVENT_VA'] & IV_SUPPORT) echo "style='width:1400px;'"; ?> >
		<?php
			PrintLeftMenu($_SERVER['SCRIPT_NAME']);
		?>
			<div id="contents"  style="width:680px;">
				<div class="h3_tit mgt0">
				<?php
					if ($GLOBALS['M_SUPPORT_EVENT_VA'] & IV_SUPPORT) {
				?>
						<h3 class="wid400"><?php echo $t_md_va[$GLOBALS['LANGINDEX']]; ?></h3>
				<?php
					}
					else {
				?>
						<h3 class="wid320"><?php echo $menu_motiondetection[$GLOBALS['LANGINDEX']]; ?></h3>
				<?php
					}
				?>
				</div>
				<table class="data_write" >
					<colgroup>
						<col style="width:180px;"/>
						<col />
					</colgroup>
					<tbody>
						<tr>
							<th scope="row"><?php echo $t_enable[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<label><input type="radio" name="event_<?php echo $event_name; ?>_use" id="event_<?php echo $event_name; ?>_use_on"  <?php if ($classInstances['VAConfiguration']->mdConf->dataInfo['Enabled']['value'] == 1 || $classInstances['VAConfiguration']->ivConf->dataInfo['Enabled']['value'] == 1) echo "checked=\"checked\""; ?> style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_on[$GLOBALS['LANGINDEX']]; ?></label>
								<label><input type="radio" name="event_<?php echo $event_name; ?>_use" id="event_<?php echo $event_name; ?>_use_off" <?php if ($classInstances['VAConfiguration']->mdConf->dataInfo['Enabled']['value'] == 0 && $classInstances['VAConfiguration']->ivConf->dataInfo['Enabled']['value'] == 0) echo "checked=\"checked\""; ?> /><?php echo $t_off[$GLOBALS['LANGINDEX']]; ?></label>
							</td>
						</tr>
					</tbody>
				</table>	
				
				<div class="h3_tit">
					<h3 class="wid320"><?php echo $t_area_configuration[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>
				<?php
					require_once('plugin_ui.cgi');
					$vaConf = $classInstances['VAConfiguration'];
					require_once('./event_setup/event_va.cgi');
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
