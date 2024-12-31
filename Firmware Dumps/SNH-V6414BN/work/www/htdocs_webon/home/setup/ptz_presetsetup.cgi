<?php
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_menu.cgi');
require_once ('../language/language_av_ptz.cgi');
require_once ('../language/language_av_camera.cgi');
require_once ('../language/language_event_common.cgi');
require_once ('../language/language_event_videoanalytics.cgi');

$event_name = 'presetedit';
$classInstances	= GetClassInstance('presetlist');
$presetConf 		= $classInstances['PresetList'];

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
	<link rel="stylesheet" type="text/css" href="../css/jquery.ui.core.css"/>
	<link rel="stylesheet" type="text/css" href="../css/jquery.ui.theme.css"/>
	<link rel="stylesheet" type="text/css" href="../css/jquery.ui.spinner.css"/>
	<link rel="stylesheet" type="text/css" href="../css/event_canvas.css" />
	<link rel="stylesheet" type="text/css" href="../css/camerasetup.css" />
	<style>
		#lnb-list {
			height:1400px;
		}
	</style>
	<script type="text/javascript" src="../js/jquery-1.9.1.js"></script>
	<script type="text/javascript" src="../js/jquery-ui.js"></script>
	<script type="text/javascript" src="../js/jquery.cookie.js"></script>
	<script type="text/javascript" src="../js/lnb.js"></script>
	<script type="text/javascript" src="../js/common_function.js"></script>
	<script type="text/javascript" src="../js/pluginCheck.js"></script>
	<script type="text/javascript" src="../js/pluginControl.js"></script>
	<!--[if lt IE 9]><script type="text/javascript" src="../js/excanvas.js"></script><![endif]-->
	<script type="text/javascript" src="../js/board.js"></script>
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

	var browserName = "<?php echo GetBrowserName(); ?>";
	var ieVer = <?php echo ieversion(); ?>;

	var localSeq				= <?php echo $_SESSION['count']; ?>;
	var ajaxReqUrl				= "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq;
	var encName 				= "<?php echo $GLOBALS['USERINFO']['encname']; ?>";
	var encPW					= "<?php echo $GLOBALS['USERINFO']['encpw']; ?>";
	var devicePort 			= <?php echo $classInstances['Information']->dataInfo['DevicePort']['value']; ?>;
	var previewProfileNo 	= <?php echo $classInstances['Information']->dataInfo['PreviewProfileNo']['value']; ?>;
	var installMsg				= new Array();
	installMsg[0] 				= "<?php echo $msg_plugin_install[$GLOBALS['LANGINDEX']]; ?>";
	installMsg[1] 				= "<?php echo $msg_plugin_install2[$GLOBALS['LANGINDEX']]; ?>";
	installMsg[2] 				= "<?php echo $msg_notsupport_plugin[$GLOBALS['LANGINDEX']]; ?>";
	
	var viewerWidth 			= <?php echo $GLOBALS['VIEWER_RESOLUTION']['width']; ?>;
	var viewerHeight 			= <?php echo $GLOBALS['VIEWER_RESOLUTION']['height']; ?>;
	var maxResolution			= {width: <?php echo $GLOBALS['MAX_RESOLUTION']['width'] ?>, height: <?php echo $GLOBALS['MAX_RESOLUTION']['height'] ?>};

	var alertLang				= ["<?php echo $msg_validPresetName[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $t_left[$GLOBALS['LANGINDEX']]; ?>"];
	var deleteLang				= "<?php echo $t_delete[$GLOBALS['LANGINDEX']]; ?>";
	var afterActionArr		= ["<?php echo $t_off[$GLOBALS["LANGINDEX"]]; ?>", "<?php echo $t_autotracking[$GLOBALS["LANGINDEX"]]; ?>", "<?php echo $t_autoRun[$GLOBALS["LANGINDEX"]]; ?>", "<?php echo $t_videoAnalytics[$GLOBALS["LANGINDEX"]]; ?>"]; 
	var MAX_PRESET_CNT 		= <?php echo MAX_PTZ_PRESET255; ?>;
	
	var presetCnt = 0;
	var initListCnt = 0;
	var selectPresetEnable	= new Array();
	var selectPresetNum 		= new Array();
	var selectPresetName		= new Array();
	var selectAfterAction	= new Array();
	var selectTrackingTime	= new Array();

	$(document).ready(function(){
		lnbonoff("lnb_ptz");
		SetSavePresetDialog();
	});

	
	function InitPresetList() 
	{
	<?php
		for($index = 0; $index<MAX_PTZ_PRESET255; $index++) {
			if(trim($presetConf->preset[$index]->dataInfo['Name']['value']) != "" && $presetConf->preset[$index]->dataInfo['Enabled']['value'] == 1) {
	?>
				selectPresetEnable[<?php echo $index; ?>] = <?php echo $presetConf->preset[$index]->dataInfo['Enabled']['value']; ?>;
				selectPresetNum[<?php echo $index; ?>] = <?php echo $presetConf->preset[$index]->dataInfo['Index']['value']; ?>;
				selectPresetName[<?php echo $index; ?>] = "<?php echo trim($presetConf->preset[$index]->dataInfo['Name']['value']); ?>";
				selectAfterAction[<?php echo $index; ?>] = <?php echo $presetConf->preset[$index]->dataInfo['AfterAction']['value']; ?>;	
				selectTrackingTime[<?php echo $index; ?>] = <?php echo $presetConf->preset[$index]->dataInfo['TrackingTime']['value']; ?>; 
				presetCnt++;			
	<?php
			}
			else {
	?> 
				selectPresetEnable[<?php echo $index; ?>] = 0;
				selectPresetNum[<?php echo $index; ?>] = <?php echo $index; ?>;
				selectPresetName[<?php echo $index; ?>] = "";
				selectAfterAction[<?php echo $index; ?>] = 0;
				selectTrackingTime[<?php echo $index; ?>] = 10;
	<?php
			}
		}
	?> 
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

		ChangeHomePositionImage();
		InitPresetList();
		DrawPresetList(0);	
		
		if(SISOPlugin.ptzControl.ptzSlideStatus == 0 && presetCnt != 0) SISOPlugin.ptzControl.onClickPTZSlide();
	}

	
	function OnClickHomePosition(actionCmd)
	{
		var msg = "";
		var applyMsg = "";
		msg = "<"+actionCmd+"PTZHomePosition>";
		if(actionCmd == "Set"){	//Set
			applyMsg = "<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>";
		}
		else { 		//Start
			msg += "<PanReal>100</PanReal>";
			msg += "<PanNorm>0</PanNorm>";
		}
		msg += "</"+actionCmd+"PTZHomePosition>";
		RequestAjaxMsg(msg, applyMsg, "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, 'NO_REFRESH', 'true');
		localSeq++;
	}

	function ChangeHomePositionImage()
	{
		$("#home-start").attr({
			src : "../images/common/PTZ/gohome_normal.png",
			title : "<?php echo $t_goHomePosition[$GLOBALS['LANGINDEX']]; ?>"
		});
		$("#home-start").hover(function(){ ChangeImage('home-start','../images/common/PTZ/gohome_press.png');
						}, function(){ ChangeImage('home-start','../images/common/PTZ/gohome_normal.png');
						}).click(function(){ 	OnClickHomePosition('Start'); });
		$("#home-start").css('cursor', 'pointer');

		$("#home-set").attr({
			src : "../images/common/PTZ/sethome_normal.png",
			title : "<?php echo $t_setHomePosition[$GLOBALS['LANGINDEX']]; ?>"
		});
		$("#home-set").hover(function(){ ChangeImage('home-set','../images/common/PTZ/sethome_press.png');
						}, function(){ ChangeImage('home-set','../images/common/PTZ/sethome_normal.png');
						}).click(function(){ 	OnClickHomePosition('Set'); });
		$("#home-set").css('cursor', 'pointer');
	}

	function OnFocusPresetAfterAction(id) {	
		var select = document.getElementById(id);
		var option_value = select.options[select.selectedIndex].value;
	
		document.getElementById(id).innerHTML = "";
		
		var afterAction = "<option value='0'><?php echo $t_off[$GLOBALS["LANGINDEX"]]; ?></option>\
						<?php 
							if ($GLOBALS['M_SUPPORT_PTZ_TRACKING']) {
						?>
						<option value='1'><?php echo $t_autotracking[$GLOBALS["LANGINDEX"]]; ?></option>\
						<?php
							}
						?>
						<option value='2'><?php echo $t_autoRun[$GLOBALS["LANGINDEX"]]; ?></option>\
						<option value='3'><?php echo $t_videoAnalytics[$GLOBALS["LANGINDEX"]]; ?></option>"
						
		$("#" + id).append(afterAction);			
		$("#" + id + " option[value = "+option_value+"]").attr("selected", true);
	}	
	
	function OnFocusPresetTrackingTime(id) {
		var select = document.getElementById(id);
		var option_value = select.options[select.selectedIndex].value;

		document.getElementById(id).innerHTML = "";
		
		var trackingTime = "	<option value='10'>10 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?> </option>\
									<option value='20'>20 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?> </option>\
									<option value='30'>30 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?> </option>\
									<option value='40'>40 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?> </option>\
									<option value='50'>50 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?> </option>\
									<option value='60'>1 <?php echo $t_minute[$GLOBALS['LANGINDEX']]; ?> </option>\
									<option value='120'>2 <?php echo $t_minute[$GLOBALS['LANGINDEX']]; ?> </option>\
									<option value='180'>3 <?php echo $t_minute[$GLOBALS['LANGINDEX']]; ?> </option>\
									<option value='240'>4 <?php echo $t_minute[$GLOBALS['LANGINDEX']]; ?> </option>\
									<option value='300'>5 <?php echo $t_minute[$GLOBALS['LANGINDEX']]; ?> </option>\
									<option value='600'>10 <?php echo $t_minute[$GLOBALS['LANGINDEX']]; ?> </option>"
		
		$("#" + id).append(trackingTime);
		$("#" + id + " option[value = "+option_value+"]").attr("selected", true);
	}

var oldSelNo;
	function OnClickPresetCmd(index) {
		var msg = "";
		var selNo = index;
		
		if (selNo != oldSelNo && typeof oldSelNo != "undefined") {
			$("#presetName_"+oldSelNo).css('color', '#374052');
			$("#presetName_"+oldSelNo).css('font-weight', 'normal');			
			$("#presetNum_"+oldSelNo).css('color', '#374052');
			$("#presetNum_"+oldSelNo).css('font-weight', 'normal');
		}
		$("#presetName_"+selNo).css('color', '#0087ef');
		$("#presetName_"+selNo).css('font-weight', 'bold');		
		$("#presetNum_"+selNo).css('color', '#0087ef');
		$("#presetNum_"+selNo).css('font-weight', 'bold');

		oldSelNo = selNo;
		
		msg += "<StartPTZPreset>";
		msg += "<Index>"+index+"</Index>";		
		msg += "</StartPTZPreset>";
		
		RequestAjaxMsg(msg, '', "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, 'NO_REFRESH', false);	
		localSeq++;
	}

	function DrawPresetList(mode, num, name) 
	{			
		var trackingTime="";
		
		if(mode == 1)	{
			selectPresetNum[num-1] = num;
			selectPresetName[num-1] = name;
		}
		
		for(var i=1; i<=MAX_PRESET_CNT; i++) {
			if(selectPresetName[i-1] != "") {
				switch(selectTrackingTime[i-1]) {
					case 10:		trackingTime = "10 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?>"; break;
					case 20:		trackingTime = "20 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?>"; break;
					case 30:		trackingTime = "30 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?>"; break;
					case 40:		trackingTime = "40 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?>"; break;
					case 50:		trackingTime = "50 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?>"; break;
					case 60:		trackingTime = "1 <?php echo $t_minute[$GLOBALS['LANGINDEX']]; ?>"; break;
					case 120:		trackingTime = "2 <?php echo $t_minute[$GLOBALS['LANGINDEX']]; ?>"; break;
					case 180:		trackingTime = "3 <?php echo $t_minute[$GLOBALS['LANGINDEX']]; ?>"; break;
					case 240:		trackingTime = "4 <?php echo $t_minute[$GLOBALS['LANGINDEX']]; ?>"; break;
					case 300:		trackingTime = "5 <?php echo $t_minute[$GLOBALS['LANGINDEX']]; ?>"; break;
					case 600:		trackingTime = "10 <?php echo $t_minute[$GLOBALS['LANGINDEX']]; ?>"; break;	
				}
				
				var presetList = "<li id='presetList_"+i+"' style='text-align:center; border-bottom:1px solid #8e939e; height:25px; padding-top:5px; color:black;'>\
											<span style='width:48px;float:left'><a href=\"javascript:OnClickPresetCmd("+i+");\" style='color:black' id='presetNum_"+i+"'>"+selectPresetNum[i-1]+"</a></span>\
											<span style='width:130px;float:left'><a href=\"javascript:OnClickPresetCmd("+i+");\" style='color:black' id='presetName_"+i+"'>"+selectPresetName[i-1]+"</a></span>\
											<span style='width:205px;float:left'>\
											<label>\
												<select id='presetAfterAction_"+i+"' name='presetAfterAction' class='presetAfterAction' style='width:204px;background-color:#b4b9c5;' onchange=\"OnFocusPresetAfterAction('presetAfterAction_"+i+"')\">\
													<option value='"+selectAfterAction[i-1]+"' selected='selected'>"+afterActionArr[selectAfterAction[i-1]]+"</option>\
												</select>\
											</label>\
											</span>\
										<?php 
											if ($GLOBALS['M_SUPPORT_PTZ_TRACKING']) {
										?>
											<span style='width:170px;float:left'>\
												<select id='presetTrackingTime_"+i+"' name='presetTrackingTime' style='width:169px;background-color:#b4b9c5' onchange=\"OnFocusPresetTrackingTime('presetTrackingTime_"+i+"');\"; >\
													<option value='"+selectTrackingTime[i-1]+"' selected='selected'>"+trackingTime+"</option>\
												</select>\
											</span>\
										<?php
											}
										?>
											<span style='float:left;width:160px;'>\
												<img id='cameraSetup_"+i+"' src='../images/common/PTZ/camerasetup_normal.png' onclick='javascript:document.location=\"av_camera.cgi?presetNo="+i+"&pctz="+(new Date()).getTime()+"\"'\
													onmouseover=\"ChangeImage('cameraSetup_"+i+"', '../images/common/PTZ/camerasetup_press.png');\" onmouseout=\"ChangeImage('cameraSetup_"+i+"', '../images/common/PTZ/camerasetup_normal.png');\" />\
											</span>\
											<span style='float:left;width:80px;'>\
												<img id='MdVa_"+i+"' src='../images/common/PTZ/mdva_normal.png' onclick='javascript:document.location=\"event_videoanalytics.cgi?presetNo="+i+"&pctz="+(new Date()).getTime()+"\"'\
													onmouseover=\"ChangeImage('MdVa_"+i+"', '../images/common/PTZ/mdva_press.png');\" onmouseout=\"ChangeImage('MdVa_"+i+"', '../images/common/PTZ/mdva_normal.png');\" />\
											</span>\
											<span style='width:30px;float:left'><input type='checkbox' class='presetCheck' id='"+selectPresetNum[i-1]+"' /></span>\
											</li>";	
				
				$("#preset_list").append(presetList);					
				$("#presetAfterAction_"+i).trigger('change');
				$("#presetTrackingTime_"+i).trigger('change')
			}
		}	
	}
	
	function OnClickPresetCheck(){
		if($("#presetCheckAll").is(":checked")) {
			$(".presetCheck").prop("checked", "checked");
		} else {
			$(".presetCheck").removeAttr("checked");
		}
	}	
	
	function OnClickApply()
	{
		var presetListCnt = $("#preset_list li").size();
		
		var msg = "";
	  	msg = "<SetPresetList>";
	  	for(var index=0; index<presetListCnt; index++) {
			var presetNum = $("#preset_list li:eq("+(index)+")").attr('id');
			var presetArr = presetNum.split('_');
			
		  	msg += "<PresetList"+ (presetArr[1]-1) +">";
		  	msg += "<Index>"+ presetArr[1] +"</Index>";	   	
		  	msg += "<Enabled>1</Enabled>";	  
		  	msg += "<Name>"+ $("#presetName_"+presetArr[1]).text() +"</Name>";	  
		  	msg += "<AfterAction>"+ $("#presetAfterAction_"+presetArr[1]).val() +"</AfterAction>";
		<?php if($GLOBALS['M_SUPPORT_PTZ_TRACKING']) { ?>
		 	msg += "<TrackingTime>"+ $("#presetTrackingTime_"+presetArr[1]).val() +"</TrackingTime>";	
		<? } ?>
		  	msg += "</PresetList"+ (presetArr[1]-1) +">"

	  	}
		msg += "</SetPresetList>";

		RequestAjaxMsg(msg, "<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, "", true);
		localSeq++;
	}

	function OnClickDelete() {
		var msg="";
		var checkPreset = $('.presetCheck:checked');		
		
		if($(".presetCheck").is(":checked") == false) {
			alert("<?php echo $msg_selValidPresetNumber[$GLOBALS['LANGINDEX']]; ?>");
		} else { 

			msg = "<SetPresetList>";
			for(var i =0; i<$('.presetCheck:checked').size(); i++) {
				var index = $('.presetCheck:checked:eq('+i+')').attr("id");
				msg += "<PresetList"+ (index-1) +">";
				msg += "<Index>"+index+"</Index>";
				msg += "<Enabled>0</Enabled>";	  
				msg += "<Name>"+ $("#presetName_"+index).val() +"</Name>";	 
				msg += "<AfterAction>0</AfterAction>";   
				msg += "<TrackingTime>10</TrackingTime>"; 
				msg += "</PresetList"+ (index-1) +">"
			}			
			msg += "</SetPresetList>";
			RequestAjaxMsg(msg, "<?php echo $t_delete[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq,"" , false);			//localSeq?
			localSeq++;
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
			<div id="container" style="width:1500px">
			<?php
				PrintLeftMenu($_SERVER['SCRIPT_NAME']);
			?>

				<div id="contents" >
					<?php
						require_once ('plugin_ui.cgi');
						require_once ('ptz_presetdialog.cgi');						
					?>	
										
					<div id="presetDetail" style=""> 
				<?php 
					if ($GLOBALS['M_SUPPORT_PTZ_TRACKING']) {
				?>			
						<div class="h3_tit" style="width:800px;">
				<?php 
					} else { 
				?>
						<div class="h3_tit" style="width:680px;">
				<?php
					} 
				?>
							<h3 class="wid320"><?php echo $t_presetSetup[$GLOBALS['LANGINDEX']]; ?></h3>
						</div>
						<div style="text-align:right;">
							<a id="mid_del_btn" class="btn_type01" href="javascript:OnClickDelete();"><?php echo $t_delete[$GLOBALS['LANGINDEX']]; ?></a>
						</div>

						<div>
							<h3 style="height:25px; background-color:#8e939e; color:black; margin-top:10px; text-align:center">						
								<span style="float:left; width:50px; margin-top:3px;"><?php echo $t_num[$GLOBALS['LANGINDEX']]; ?></span>	
								<span style="float:left; width:130px; margin-top:3px;"><?php echo $t_name[$GLOBALS['LANGINDEX']]; ?></span>
								<span style="float:left; width:200px; margin-top:3px;"><?php echo $t_afteraction[$GLOBALS['LANGINDEX']]; ?></span>		
							<?php 
								if ($GLOBALS['M_SUPPORT_PTZ_TRACKING']) {
							?>
								<span style="float:left; width:170px; margin-top:3px;"><?php echo $t_trackingTime[$GLOBALS['LANGINDEX']]; ?></span>
							<?php 
								}
							?>
								<span style="float:left; width:170px; margin-top:3px;"><?php echo $menu_camera[$GLOBALS['LANGINDEX']]; ?></span>						
								<span style="float:left; width:70px; margin-top:3px;"><?php echo $menu_videoanalytics[$GLOBALS['LANGINDEX']]; ?></span>
								<span style="float:left; width:51px; margin-top:3px;"><input type="checkbox" id="presetCheckAll" name="presetCheck" style="margin-left:-10px;" onclick="OnClickPresetCheck();"/> </span>

							</h3>
							<ul id="preset_list" style="overflow-y:scroll; overflow-x:hidden; height:310px; background-color:#b4b9c5">
								
							</ul>
						</div>
					</div>
					<div class="btn_right">
						<a id="mid_ok_btn" class="btn_apply" href="javascript:OnClickApply()"><?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?></a>
					</div>
				</div>
			</div>
		</div>
	</body>
</html>


