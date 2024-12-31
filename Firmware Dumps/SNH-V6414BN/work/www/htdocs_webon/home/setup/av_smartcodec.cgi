<?php
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_menu.cgi');
require_once ('../language/language_av_smartcodec.cgi');

$classInstances= GetClassInstance('smartcodec');
$imageConf		= $classInstances['SmartCodecConfiguration'];
$fdConf			= $classInstances['FDConfiguration'];

// DEV_S1WEBVIEWER Start
$userClassInstance = GetClassInstance('user');
$userConf	= $userClassInstance['UserConfiguration'];
// DEV_S1WEBVIEWER End
$event_name = 'smartcodec';
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="kr" xml:lang="kr">
<head>
	<title>iPOLiS NETWORK CAMERA WEBVIEWER</title>
	<meta http-equiv="X-UA-Compatible" content="IE=Edge; requiresActiveX=true">
	<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
	<link rel="stylesheet" type="text/css" href="../css/techwin.css" />
	<link rel="stylesheet" type="text/css" href="../css/jquery.ui.slider.css"/>	
	<style>
	#lnb-list {
		height:950px;
	}	
	</style>
	<script type="text/javascript" src="../js/jquery-1.9.1.js"></script>
	<script type="text/javascript" src="../js/jquery-ui.js"></script>
	<script type="text/javascript" src="../js/lnb.js"></script>
	<script type="text/javascript" src="../js/common_function.js"></script>
	<script type="text/javascript" src="../js/pluginCheck.js"></script>
	<script type="text/javascript" src="../js/pluginControl.js"></script>
	<!--[if lt IE 9]><script type="text/javascript" src="../js/excanvas.js"></script><![endif]-->	
	<script type="text/javascript" src="../js/smartCodec.js"></script>
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
	
	var viewerWidth                         = <?php echo $GLOBALS['VIEWER_RESOLUTION']['width']; ?>;
	var viewerHeight                        = <?php echo $GLOBALS['VIEWER_RESOLUTION']['height']; ?>;
	var maxResolution                       = {width: <?php echo $GLOBALS['MAX_RESOLUTION']['width'] ?>, height: <?php echo $GLOBALS['MAX_RESOLUTION']['height'] ?>};

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
	
	function OnClickApply()
	{
		var msg = "<SetSmartCodecConfiguration>";
		<?php if ($GLOBALS['M_SUPPORT_EVENT_FD'] && ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2 || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3 || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ)) { ?>
		msg += "<Mode>"+($("#roi_area_manual").is(':checked') ? 1 : 0)+"</Mode>";
		<?php } else { ?>
		msg += "<Mode>1</Mode>";
		<?php } ?>
	  	msg += "<QualityLevel>"+($("#roi_quality").val())+"</QualityLevel>";
		<?php if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2) { ?>
		msg += "<FDSensitivity>"+($("#roi_sensitivity").val())+"</FDSensitivity>";
		<?php } ?>
		msg += smartCodec.drawings.setArea_xml();
	  	msg += "</SetSmartCodecConfiguration>";

	  	// ** width/height value must not be more than or equal to video source's max width/height!
	  	<?php if ($GLOBALS['MEGAMODE'] == 2) { ?>
	  		msg = msg.replaceAll("1920", "1919");
	  		msg = msg.replaceAll("1080", "1079");
	  	<?php } else { ?>
	  		msg = msg.replaceAll("2048", "2047");
	  		msg = msg.replaceAll("1536", "1535");
	  	<?php } ?>

		RequestAjaxMsg(msg, "<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, "Audio");
	}
	function OnClickRoiMode(mode){
		<?php if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2 || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3 || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ) { ?>
		if(mode == 'manual'){
			$('#roi_sensitivity').attr('disabled', 'disabled');
			$("#roi_clear_btn").attr('href',"javascript:OnClickClearBtn();");
			$("#roi_clear_btn").attr('class','btn_type01');
			$("#DisableVideoSetup").css("display","none");

		}
		else{
			$('#roi_sensitivity').removeAttr('disabled');
			$("#roi_clear_btn").removeAttr('href');
			$("#roi_clear_btn").attr('class','btn_disable');
			$("#DisableVideoSetup").css("display","block");
		}
		<?php } ?>
	}

	function OnClickClearBtn(){
		smartCodec.drawings.clearArea();
	}

	function InitSmartCodecArea(){
		<?php if($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3){ ?>
		smartCodec.drawings.rectangle(viewerWidth,viewerHeight,maxResolution.width,maxResolution.height,GetFilpMirrorStatus(), false);
		<?php }else if($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ){ ?>
		smartCodec.drawings.rectangle(viewerWidth,viewerHeight,maxResolution.width,maxResolution.height, 0, true);		
		<?php } ?>
		var xmlData = "<?php echo $imageConf->GetXMLData(); ?>";
		smartCodec.drawings.getArea(xmlData);
		
		if(!$("#roi_area_fd").is(":checked")){
			$("#DisableVideoSetup").css("display","none");
		}else{
			$("#DisableVideoSetup").css("display","block");
		}
		
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
					InitSmartCodecArea();
				}
			}, 100);
		}else{
			InitSmartCodecArea();
		}
  				
		<?php if($imageConf->dataInfo['Mode']['value'] == 1){ ?>
			OnClickRoiMode('manual');
		<?php }else{ ?>
			OnClickRoiMode('fd');
		<?php } ?>
  	}
 
	</script>
</head>
<body onload="OnLoad();" onselectstart="return false">
	<div id="wrap">
		<?php
			require_once ('left_menu.cgi');
			require_once ('top_menu.cgi');
		?>
		<div id="container">
		<?php
			PrintLeftMenu($_SERVER['SCRIPT_NAME']);
		?>
			<div id="contents">
				<div class="h3_tit mgt0" >
					<h3 class="wid220"><?php echo $t_smartcodecSetup[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>
				<?php if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2) { ?>
				<table class="data_write" <?php if (GetBrowserName() == 'Apple Safari') {echo "style=\"width:539px\""; } else {echo "style=\"width:530px\"";}?>>
				<?php } else { ?>
				<table class="data_write" <?php if (GetBrowserName() == 'Apple Safari') {echo "style=\"width:539px\""; } else {echo "style=\"width:600px\"";}?>>
				<?php } ?>
					<colgroup>
						<col style="width:135px;" />
						<col style="width:110px;" />
						<col/>
					</colgroup>
					<tbody>
						<?php if ($GLOBALS['M_SUPPORT_EVENT_FD'] && ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2 || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3 || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ)) { ?>
						<tr>
							<th scope="row"><?php echo $t_roiArea[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<label style="margin-right:0px;"><input type="radio" name="roi_area" id="roi_area_manual" onclick="OnClickRoiMode('manual');" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" <?php if ($imageConf->dataInfo['Mode']['value'] == 1) echo 'checked=\'checked\''; ?> /><?php echo $t_manual[$GLOBALS['LANGINDEX']];?></label>
							</td>
							<td>
								<label style="margin-right:0px;width:250px;"><input type="radio" name="roi_area" id="roi_area_fd" onclick="OnClickRoiMode('fd');" <?php if ($imageConf->dataInfo['Mode']['value'] == 0) echo "checked=\"checked\""; if ($fdConf->dataInfo['Enabled']['value'] == 0) echo "disabled=\"disabled\""; ?> /><?php echo $t_faceDetection[$GLOBALS['LANGINDEX']];?></label>
							</td>
						</tr>
						<?php } ?>
					
						<tr>
							<th scope="row"><?php echo $t_quality[$GLOBALS['LANGINDEX']]; ?></th>
							<td colspan="2">
								<select name="roi_quality_select" id="roi_quality" style="width:150px; height:22px; background-color:#868fa3; color:#1c1c1c;">
								<?php if (!($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3 || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ)) { ?>
									<option value = "0" <?php if($imageConf->dataInfo['QualityLevel']['value'] == 0) echo "selected=\"selected\""; ?> ><?php echo $t_auto[$GLOBALS['LANGINDEX']]; ?></option>
								<?php } ?>
  									<option value = "1" <?php if($imageConf->dataInfo['QualityLevel']['value'] == 1) echo "selected=\"selected\""; ?> ><?php echo $t_low[$GLOBALS['LANGINDEX']]; ?></option>
  									<option value = "2" <?php if($imageConf->dataInfo['QualityLevel']['value'] == 2) echo "selected=\"selected\""; ?> ><?php echo $t_medium[$GLOBALS['LANGINDEX']]; ?></option>
  									<option value = "3" <?php if($imageConf->dataInfo['QualityLevel']['value'] == 3) echo "selected=\"selected\""; ?> ><?php echo $t_high[$GLOBALS['LANGINDEX']]; ?></option>
								</select>
							</td>
						</tr>
						
				<?php 
					if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2) { 
				?>
						<tr>
							<th scope="row"><?php echo $t_face_Sensitivity[$GLOBALS['LANGINDEX']]; ?></th>
							<td colspan="2">
								<select name="roi_sensitivity_select" id="roi_sensitivity" style="width:150px; height:22px; background-color:#868fa3; color:#1c1c1c;" >
									<option value = "1" <?php if($imageConf->dataInfo['FDSensitivity']['value'] == 1) echo "selected=\"selected\""; ?> >1</option>
  									<option value = "2" <?php if($imageConf->dataInfo['FDSensitivity']['value'] == 2) echo "selected=\"selected\""; ?> >2</option>
  									<option value = "3" <?php if($imageConf->dataInfo['FDSensitivity']['value'] == 3) echo "selected=\"selected\""; ?> >3</option>
  									<option value = "4" <?php if($imageConf->dataInfo['FDSensitivity']['value'] == 4) echo "selected=\"selected\""; ?> >4</option>
									<option value = "5" <?php if($imageConf->dataInfo['FDSensitivity']['value'] == 5) echo "selected=\"selected\""; ?> >5</option>
  									<option value = "6" <?php if($imageConf->dataInfo['FDSensitivity']['value'] == 6) echo "selected=\"selected\""; ?> >6</option>
  									<option value = "7" <?php if($imageConf->dataInfo['FDSensitivity']['value'] == 7) echo "selected=\"selected\""; ?> >7</option>
  									<option value = "8" <?php if($imageConf->dataInfo['FDSensitivity']['value'] == 8) echo "selected=\"selected\""; ?> >8</option>
									<option value = "9" <?php if($imageConf->dataInfo['FDSensitivity']['value'] == 9) echo "selected=\"selected\""; ?> >9</option>
  									<option value = "10" <?php if($imageConf->dataInfo['FDSensitivity']['value'] == 10) echo "selected=\"selected\""; ?> >10</option>
								</select>
							</td>
						</tr>
				<?php 
					} 
				?>
					</tbody>
				</table>
		<?php 
			if ($GLOBALS['M_SUPPORT_EVENT_FD'] && ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2 || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3 || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ)) { 
		?>
				<div id="roiMsg" style="padding:10px; width:680px;">
					<?php echo $t_roimsg[$GLOBALS['LANGINDEX']]; ?>
				</div>
		<?php
			}
		?>
				<div class="h3_tit mgt20">
					<h3 class="wid220"><?php echo $t_manualROIarea[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>
				<?php
					require_once ('plugin_ui.cgi');
				?>
				<div style="text-align:right; width:680px;margin-top: 10px;">
					<a class="btn_type01" href="javascript:OnClickClearBtn();" id="roi_clear_btn"><?php echo $t_clear[$GLOBALS['LANGINDEX']]; ?></a>
				</div>
				<div class="btn_right" style="width:680px">
					<a id="mid_ok_btn" class="btn_apply" href="javascript:OnClickApply()"><?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?></a>
				</div>
			</div>
		</div>
	</div>
</body>
</html>
