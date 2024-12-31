<?php
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_menu.cgi');
require_once ('../language/language_event_common.cgi');

$event_name 	= 'fd';
$classInstances= GetClassInstance($event_name);
$event_class	= $classInstances['FDConfiguration'];

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
	<script type="text/javascript" src="../js/faceDetection.js"></script>
	<script type="text/javascript" language="javascript">
	<?php if (!$GLOBALS['M_SUPPORT_EVENT_FD']) { ?>
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
		
	var detectMode = <?php echo $event_class->dataInfo['ObjectMode']['value']; ?>;
	var polyCanvas = document.getElementById("myCanvas");	
	var deleteLang				= "<?php echo $t_delete[$GLOBALS['LANGINDEX']]; ?>";
	
	$(document).ready(function(){
		lnbonoff("lnb_event");
		var t	= setTimeout("OnLoad()", 500);
		
		$("#fd_tabs").tabs();
	});
	
	function OnClickApply()
	{
		if (CheckScheduleSetting("<?php echo $event_name; ?>") == 0) {
			alert("<?php echo $msg_checkthetable[$GLOBALS['LANGINDEX']]; ?>");
			return; 
		} 
		var msg = '';
		msg += "<SetFDConfiguration>";
		msg += "<Enabled>"+($("#event_<?php echo $event_name; ?>_use_on").is(':checked') ? 1 : 0 )+"</Enabled>";
		msg += "<FDBoxDisplay>"+($('#event_<?php echo $event_name; ?>_overlay_motion').is(':checked')?1:0)+"</FDBoxDisplay>";
		msg += "<ObjectMode>"+($('#event_<?php echo $event_name; ?>_detection_mode_on').is(':checked')?1:0)+"</ObjectMode>";
		msg += "<Sensitivity>"+$('#event_<?php echo $event_name; ?>_sensitivity').val()+"</Sensitivity>";
		msg += FaceDetection.drawings.setPolygonData();
		<?php if($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>	
		msg += MakeScheduleAndActionSetupXML_S1("<?php echo $event_name; ?>");
		<?php } else { ?>
		msg += MakeScheduleAndActionSetupXML("<?php echo $event_name; ?>");	
		<?php } ?> 		
		msg += "</SetFDConfiguration>";
		RequestAjaxMsg(msg, "<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $GLOBALS['REQUEST_URI'].'?seq='.$_SESSION['count'] ?>");
	}

	function OnLoad()
	{
		<?php if($GLOBALS['M_SUPPORT_PTZ'] == PTZ_NOT_SUPPORT) { ?>
		FaceDetection.drawings.polygon("<?php echo MAX_FD_OBJECT; ?>",viewerWidth,viewerHeight,maxResolution.width,maxResolution.height,GetFilpMirrorStatus());
		<?php }else{ ?>
		FaceDetection.drawings.polygon("<?php echo MAX_FD_OBJECT; ?>",viewerWidth,viewerHeight,maxResolution.width,maxResolution.height,0);
		<?php } ?>
		var flip = <?php echo $classInstances['Information']->dataInfo['Flip']['value']; ?>;
		var mirror = <?php echo $classInstances['Information']->dataInfo['Mirror']['value']; ?>;

		var msg = "";
		msg += "<GetFDArea>\r\n";
			
	<?php 
		for ($index=0; $index<MAX_FD_OBJECT; ++$index) { 
			if ($event_class->objectConf[$index]->dataInfo['NumPoint']['value'] >= 1 ) {
	?>
			msg +="<ObjectArea>\r\n";
			msg += "<Index>" + <?php echo $index; ?> + "</Index>\r\n";
			msg += "<NumPoint>" + <?php echo $event_class->objectConf[$index]->dataInfo['NumPoint']['value']; ?> + "</NumPoint>\r\n";

			var posX = new Array();
			var posY = new Array();
			posX[0] = <?php echo $event_class->objectConf[$index]->fdPoint[0]->dataInfo['PosX']['value']; ?>;
			posY[0] = <?php echo $event_class->objectConf[$index]->fdPoint[0]->dataInfo['PosY']['value']; ?>;
			posX[1] = <?php echo $event_class->objectConf[$index]->fdPoint[1]->dataInfo['PosX']['value']; ?>;
			posY[1] = <?php echo $event_class->objectConf[$index]->fdPoint[1]->dataInfo['PosY']['value']; ?>;
			posX[2] = <?php echo $event_class->objectConf[$index]->fdPoint[2]->dataInfo['PosX']['value']; ?>;
			posY[2] = <?php echo $event_class->objectConf[$index]->fdPoint[2]->dataInfo['PosY']['value']; ?>;
			posX[3] = <?php echo $event_class->objectConf[$index]->fdPoint[3]->dataInfo['PosX']['value']; ?>;
			posY[3] = <?php echo $event_class->objectConf[$index]->fdPoint[3]->dataInfo['PosY']['value']; ?>;
			<?php if(($GLOBALS['M_MAX_RESOLUTION'] == MAX_3_MEGA &&  $GLOBALS['MEGAMODE'] == 2)) { ?>
				var halfX = 1920/2;
				var halfY = 1080/2;
			<?php }else{ ?>
				var halfX = maxResolution.width/2;
				var halfY = maxResolution.height/2;
			<?php } ?>
			<?php if($GLOBALS['M_SUPPORT_PTZ'] == PTZ_NOT_SUPPORT) { ?>
				for(i=0;i<=3;i++){
					if (mirror) {
						if (posX[i] >= halfX)
							posX[i] = halfX - (posX[i] - halfX);
						else
							posX[i] = halfX + (halfX - posX[i]);
					}

					if (flip) {
						if (posY[i] >= halfY)
							posY[i] = halfY - (posY[i] - halfY);
						else
							posY[i] = halfY + (halfY - posY[i]);
					}
				}
			<?php } ?>
			for(i=0;i<=3;i++)
			{
				msg += "<Point"+i+">\r\n";
				msg += "<X>" + posX[i] + "</X>\r\n";
				msg += "<Y>" + posY[i] + "</Y>\r\n";
				msg += "</Point"+i+">\r\n";
			}

			msg +="</ObjectArea>\r\n";
	<?php 
			}
		} 
	?>
		msg +="</GetFDArea>\r\n";
		FaceDetection.getRectagnleXML= msg;
		FaceDetection.drawings.getPolygon(msg);
		
		OnClickFdTabs('sense');

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
	
	function OnClickFdTabs(name)
	{
		if (name == 'sense') {
			$("#FDPolyDraw").css("display","none");
		}
		else if (name == 'area') {
			$("#FDPolyDraw").css("display","");			
		}
	}

	function OnClickDetectionMode()
	{
		FaceDetection.drawings.updatePolygon();
	}

	function OnClickDetectionModeImage(mode)
	{
		if(mode == 'on'){
			$("#event_<?php echo $event_name; ?>_detection_mode_on").prop("checked", true);
		}
		else{
			$("#event_<?php echo $event_name; ?>_detection_mode_none").prop("checked", true);
		}
		OnClickDetectionMode();
	}
		</script>
	</head>
	<body onselectstart="return false">
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
				<?php
					require_once('plugin_ui.cgi');
				?>
				<div class="h3_tit">
					<h3 class="wid320"><?php echo $menu_facedetection[$GLOBALS['LANGINDEX']]; ?></h3>
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
								<label><input type="radio" name="event_<?php echo $event_name; ?>_use" id="event_<?php echo $event_name; ?>_use_on"  <?php if ($event_class->dataInfo['Enabled']['value'] == 1) echo "checked=\"checked\""; ?> style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_on[$GLOBALS['LANGINDEX']]; ?></label>
								<label><input type="radio" name="event_<?php echo $event_name; ?>_use" id="event_<?php echo $event_name; ?>_use_off" <?php if ($event_class->dataInfo['Enabled']['value'] == 0) echo "checked=\"checked\""; ?> /><?php echo $t_off[$GLOBALS['LANGINDEX']]; ?></label>
							</td>
						</tr>
					</tbody>
				</table>
				<div id="fd_tabs" style="margin-top:20px; margin-bottom:10px; margin-left:9px">
					<ul>
						<li style="text-align:center;"><a href="#fd_tabs-1" onClick="OnClickFdTabs('sense')"><?php echo $t_sensitivity[$GLOBALS['LANGINDEX']]; ?></a></li>
						<li style="text-align:center;"><a href="#fd_tabs-2" onClick="OnClickFdTabs('area')"><?php echo $t_area[$GLOBALS['LANGINDEX']]; ?></a></li>
					</ul>
					<div id="fd_tabs-1">
						<table class="data_write mgt10 mgl-20 pdl15" style="width:670px;" border=0>
							<colgroup>
								<col style="width:162px;"/>
								<col />
							</colgroup>
							<tr>
								<th class="top_txt"><?php echo $t_sensitivity[$GLOBALS['LANGINDEX']]; ?></th> 					
								<td>
									<select id="event_<?php echo $event_name; ?>_sensitivity" class="selectbox_style">					
										<option value="1" <?php if ($event_class->dataInfo['Sensitivity']['value'] == 1) echo "selected=\"selected\""; ?> ><?php echo '1('.$t_very_low[$GLOBALS['LANGINDEX']].')'; ?></option>
										<?php
											$sens_list = '';
											for($i=2; $i<10; $i++) {
												$sens_list .= '<option value='.$i;
												if ($event_class->dataInfo['Sensitivity']['value'] == $i) $sens_list .= " selected=\"selected\"";
												$sens_list .= '>'.$i.'</option>'."\r\n";
				
											}
											echo $sens_list;
										?>
										<option value="10" <?php if ($event_class->dataInfo['Sensitivity']['value'] == 10) echo "selected=\"selected\""; ?> ><?php echo '10('.$t_very_high[$GLOBALS['LANGINDEX']].')'; ?></option>
									</select>
								</td>
							</tr>
						</table> 					
					</div>
					<div id="fd_tabs-2">
						<table class="data_write mgt10 mgl-20 pdl15" style='width:670px;'>
							<colgroup>
								<col style="width:162px;"/>
								<col />
							</colgroup>
							<tbody>
								<tr>
									<th class="top_txt"><?php echo $t_area[$GLOBALS['LANGINDEX']]; ?></th>
									<td>
										<input type="radio" name="event_<?php echo $event_name; ?>_detection_mode" id="event_<?php echo $event_name; ?>_detection_mode_on" onclick='OnClickDetectionMode()' <?php if($event_class->dataInfo['ObjectMode']['value'] == 1) echo "checked=\"checked\""; ?> style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><img id="detect_img" src="../images/common/detection.png" onclick="OnClickDetectionModeImage('on')" /><label style="vertical-align: top;" > <?php echo $t_detectionArea[$GLOBALS['LANGINDEX']]; ?></label>
									</td>
								</tr>
								<tr>
									<td></td>
									<td>
										<input type="radio" name="event_<?php echo $event_name; ?>_detection_mode" id="event_<?php echo $event_name; ?>_detection_mode_none" onclick='OnClickDetectionMode()' <?php if($event_class->dataInfo['ObjectMode']['value'] == 0) echo "checked=\"checked\""; ?> style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><img id="nonDetect_img" src="../images/common/non_detection.png" onclick="OnClickDetectionModeImage('none')" /><label style="vertical-align: top;" > <?php echo $t_nondetectionArea[$GLOBALS['LANGINDEX']]; ?></label>
									</td>
								</tr> 
							</tbody>
						</table>
					</div>
					<div id="DisableFDSelectLayer" style="position:absolute; width:670px; height:135px; left: 0px; top: 0px; background-color:#000000; display:none; z-index:1000; filter:alpha(opacity=0.3); opacity:0.3; -moz-opacity:0.3; -ms-filter: 'progid:DXImageTransform.Microsoft.Alpha(Opacity=30)';">
					</div>
				</div>
				<table class="data_write">
					<tbody>
						<tr>
							<th><?php echo $t_overlay[$GLOBALS['LANGINDEX']]; ?></th>
						</tr>
						<tr>
							<td style="padding-left:20px">
								<label><input type='checkbox' id='event_<?php echo $event_name; ?>_overlay_motion' <?php if ($event_class->dataInfo['FDBoxDisplay']['value']==1) echo "checked=\"checked\""; ?> style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_detection_result_overlay[$GLOBALS['LANGINDEX']] ; ?></label>
							</td>
						</tr> 
					</tbody>
				</table>
				<?php					
					require_once ('eventsetup_ui.cgi');
				?>
				<div class="btn_right">
					<a id="mid_ok_btn" class="btn_apply" href="javascript:OnClickApply()"><?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?></a>
				</div>
				</div>
			</div>
		</div>
	</body>
</html>

