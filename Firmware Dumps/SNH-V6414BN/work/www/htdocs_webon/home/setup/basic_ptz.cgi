<?php
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_menu.cgi');
require_once ('../language/language_av_ptz.cgi');
require_once ('../language/language_av_camera.cgi');
require_once ('../language/language_event_common.cgi');
require_once ('../language/language_event_videoanalytics.cgi');

$event_name = 'presetedit';

if (isset($_REQUEST['presetNo'])) {
	require_once ('../../cgi-bin/adv/presetedit.class');
	require_once ('../../cgi-bin/adv/info.class');

	$GLOBALS['SOCKET_MANAGER'] = new SocketManager();
	$classInstances['Information'] = $GLOBALS['SOCKET_MANAGER']->Connection(new Information());
	
	$presetImageConf = new PresetImageConfiguration();
	$presetImageConf->payload = pack('i1', $_REQUEST['presetNo']);
	$GLOBALS['SOCKET_MANAGER']->Connection($presetImageConf);

	$presetVaConf = new PresetVAConfiguration();
	$presetVaConf->payload = pack('i1', $_REQUEST['presetNo']);
	$GLOBALS['SOCKET_MANAGER']->Connection($presetVaConf);

	$msg = '';
	$msg .= "<PresetEditConfiguration>\r\n";
	$msg .= "<Information>\r\n";
	$msg .= "<SensorFrameMode>".$classInstances['Information']->dataInfo['SensorFrameMode']['value']."</SensorFrameMode>\r\n";
	$msg .= "<LongShutterSpeed>".$classInstances['Information']->dataInfo['LongShutterSpeed']['value']."</LongShutterSpeed>\r\n"; 
	$msg .= "<BlcMode>".$classInstances['Information']->dataInfo['BlcMode']['value']."</BlcMode>\r\n"; 
	$msg .= "<TamperingEnable>".$classInstances['Information']->dataInfo['TamperingEnable']['value']."</TamperingEnable>\r\n"; 	
	$msg .= "<MDEnable>".$classInstances['Information']->dataInfo['MDEnable']['value']."</MDEnable>\r\n"; 	
	$msg .= "<IVEnable>".$classInstances['Information']->dataInfo['IVEnable']['value']."</IVEnable>\r\n"; 	
	$msg .= "</Information>\r\n";	
	$msg .= $presetImageConf->GetXMLData();
	$msg .= $presetVaConf->GetXMLData();	
	$msg .= "</PresetEditConfiguration>\r\n";
	echo $msg;
	exit;
}

$classInstances	= GetClassInstance('ptz');
$presetConf 		= $classInstances['PTZPreset'];
$groupsConf 		= $classInstances['PTZGroup'];
$autorunConf  		= $classInstances['PTZAutorun'];
$swingsConf    	= $classInstances['PTZSwing'];
$tourConf     	 	= $classInstances['PTZTour'];
$trackingpreset 	= $classInstances['TrackingPreset'];
$presetImageConf	= $classInstances['PresetImageConfiguration'];
$presetVaConf		= $classInstances['PresetVAConfiguration'];
$imageSSDR 			= $presetImageConf->imageConf->imageSSDR;
$imageWhiteBalance= $presetImageConf->imageConf->imageWhiteBalance;
$imageBackLight 	= $presetImageConf->imageConf->imageBackLight;
$imageExposure 	= $presetImageConf->imageConf->imageExposure;
$imageSpecial 		= $presetImageConf->imageConf->imageSpecial;
$imageFocus 		= $presetImageConf->imageConf->imageFocus;
$imageTracking		= $presetImageConf->imageConf->imageTracking;

// DEV_S1WEBVIEWER Start
$userClassInstance = GetClassInstance('user');
$userConf	= $userClassInstance['UserConfiguration'];
// DEV_S1WEBVIEWER End
if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ) {
	$isp_name = 'wn2_ptz';
}
else if($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ){
	$isp_name = 'wn3_ptz';
}
else{
	$isp_name = 'wn3_ptz';
}
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
	<link rel="stylesheet" type="text/css" href="../css/jquery.ui.tabs.css"/>
	<link rel="stylesheet" type="text/css" href="../css/jquery.ui.theme.css"/>
	<link rel="stylesheet" type="text/css" href="../css/jquery.ui.spinner.css"/>
	<link rel="stylesheet" type="text/css" href="../css/event_canvas.css" />
	<link rel="stylesheet" type="text/css" href="../css/camerasetup.css" />
	<style>
		#lnb-list {
			height:1400px;
		}
		#ptz_tabs {
			width:695px;
			margin-top:20px;
		}
		#sequence_tabs {
			width:658px;
		}
		#presetedit_tabs {
			width:658px;
		}
		#tabs-camerasetup .btn_right {
			margin-top:9px;
			width:658px;
		}
		#tabs-va .btn_right {
			margin-top:183px;
			margin-left:8px;
			width:658px;
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
	<script type="text/javascript" src="../js/md_va.js"></script>
	<script type="text/javascript" src="../js/board.js"></script>
	<script type="text/javascript" src="../js/autorunSchedule.js"></script>
	<script type="text/javascript" src="../js/camerasetup_function.js"></script>
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
	<?php if($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ) { ?>
	previewProfileNo++;
	<?php } ?>
	var installMsg				= new Array();
	installMsg[0] 				= "<?php echo $msg_plugin_install[$GLOBALS['LANGINDEX']]; ?>";
	installMsg[1] 				= "<?php echo $msg_plugin_install2[$GLOBALS['LANGINDEX']]; ?>";
	installMsg[2] 				= "<?php echo $msg_notsupport_plugin[$GLOBALS['LANGINDEX']]; ?>";
	
	var viewerWidth			= <?php echo $GLOBALS['VIEWER_RESOLUTION']['width']; ?>;
	var viewerHeight			= <?php echo $GLOBALS['VIEWER_RESOLUTION']['height']; ?>;
	var maxResolution			= {width: <?php echo $GLOBALS['MAX_RESOLUTION']['width'] ?>, height: <?php echo $GLOBALS['MAX_RESOLUTION']['height'] ?>};

	var okLang 					= "<?php echo $t_ok[$GLOBALS['LANGINDEX']]; ?>";
	var cancelLang				= "<?php echo $t_cancel[$GLOBALS['LANGINDEX']]; ?>";
	var deleteLang				= "<?php echo $t_delete[$GLOBALS['LANGINDEX']]; ?>";
	var titleLang				=["<?php echo $t_virtual_line_based[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $t_defined_area[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $t_entire_area[$GLOBALS['LANGINDEX']]; ?>"];
	var directionLang			=["<?php echo $t_right[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $t_left[$GLOBALS['LANGINDEX']]; ?>"];
		
	var timer;
 	var setupState = 1;
 	var isOnloading = true; 	
 	var isApplying = 0;
	var oldDN = <?php echo $imageSpecial->dataInfo["DayNightMode"]["value"]; ?>;
	var oldBlc_mode = <?php echo $imageBackLight->dataInfo["Mode"]["value"]; ?>;
	var pirisVal = <?php echo $imageExposure->dataInfo["PIrisPosition"]["value"]; ?>;
	var blc_top = 0;
	var blc_bottom = 0;
	var blc_right = 0;
	var blc_left = 0;
	var TEST = 1;
	var SAVE = 0;
	var SENSOR_MODE = 0;
	var LONG_SHUTTER_SPEED = 0;
	var TAMPERING_ENABLE = 0;
	var MD_ENABLE = 0;
	var IV_ENABLE = 0;
	var BLC_MODE = 0;
	
	var currentTabName = 'sequence';
	var MAX_PRESET_CNT = <?php echo MAX_PTZ_PRESET255; ?>;
	var MAX_PRESET_OF_PRESETLIST = <?php echo MAX_PRESET_OF_PRESETLIST; ?>;	//128
	var MAX_GROUP_OF_TOUR_CNT = <?php echo MAX_GROUP_OF_TOUR; ?>;

	var prevGroupNo = 1;
	var groupSetStatus = new Array(<?php echo MAX_PTZ_GROUP+1; ?>);
	
	var tourSetStatus = false;
	var PRESETENABLE		= new Array();
	var curPresetNo = 0;
	var curSeqenceName = '';
	var buttonInfo = { // apply, cancel
	};

	var presetCnt = 0;

	$(document).ready(function(){
		lnbonoff("lnb_basic");
		$("#ptz_tabs").tabs();
		$("#sequence_tabs").tabs();
		
		$(".preset-camera").css("width", "auto");
		$(".ptz_tabs").css({
							"width" : 347,
							"text-align": "center",
							"padding-left": ".0em"});
		$(".inner-first").css({
							"width" : 135,
							"text-align": "center"});
		$("#va_tabs").css({
							"text-align": "center",
							"padding-left": ".0em"});
		$("#md_tabs").css({
							"text-align": "center",
							"padding-left": ".0em"});				

		$("#sequence_tabs").removeClass("ui-tabs");
		$("#presetedit_tabs").removeClass("ui-tabs");
		$("#sequence_tabs .ui-tabs-panel").css("height", "520px");
		
		if(BrowserDetect.browser == 'Chrome') {
			$(window).on('beforeunload', function(){
				RequestStartStopPresetEdit('Stop');
			});
		}
		else {
			$(window).on('unload', function() {
				RequestStartStopPresetEdit('Stop');
			});
		}
		
	});

	$(document).mouseup(function() {
		if(firstDrawClick && isDrawDragging){		
			switch(EventSetup.viewStatus){
				case VIEW_MODE["MD"] : $("#MDPolyTemp").trigger("mouseup"); break;
				case VIEW_MODE["MD_OBJSIZE"] : $("#maxMinCover").trigger("mouseup"); break;
				case VIEW_MODE["VA_PASSING"] : ; break;
				case VIEW_MODE["VA_ENTERING"] : ; break;
				case VIEW_MODE["VA_APPEAR"] : $("#myCanvasRectTmp").trigger("mouseup"); break;
				//default : ;
			}
			$("#imgTemp").trigger("mouseup");
		}
	});

	function OnClickPresetCmd(actionCmd)
	{
		var msg = "";
		var cmdMsg = "";

		if ($("#PresetList").val() == 0) {
			alert("<?php echo $msg_selValidPresetNumber[$GLOBALS['LANGINDEX']]; ?>");
			return;
		}

		if(actionCmd == "Add") {
			if($('#PresetName').val() == "" || !TypeCheck($('#PresetName').val(), NUM+ALPHA)) {
				alert("<?php echo $msg_validPresetName[$GLOBALS['LANGINDEX']]; ?>");
				return;
			}			
		}
		else if(actionCmd == "Remove") {
			var selPresetName = $("#PresetList option[value='"+$("#PresetList").val()+"']").text().split(':');
			if(selPresetName[1] == "") {
				alert("<?php echo $msg_selValidPresetNumber[$GLOBALS['LANGINDEX']]; ?>");
				return;
			}
		}

		msg += "<"+actionCmd+"PTZPreset>";
		msg += "<Index>"+$("#PresetList").val()+"</Index>";
		if (actionCmd == "Add") {
			msg += "<Name>"+$('#PresetName').val()+"</Name>";
		}
		msg += "</"+actionCmd+"PTZPreset>";

		if(actionCmd == "Set") {
			applyMsg = "<?php echo $t_set[$GLOBALS['LANGINDEX']]; ?>";
		}
		else if(actionCmd == "Remove") {
			applyMsg = "<?php echo $t_remove[$GLOBALS['LANGINDEX']]; ?>";
		}
		else if(actionCmd == "Add") {
			applyMsg = "<?php echo $t_add[$GLOBALS['LANGINDEX']]; ?>";			
		}
		else if (actionCmd == "Start") {
			applyMsg = '';
			cmdMsg = 'NO_REFRESH';
		}
		
		SetPTZCookie('Preset');
		RequestAjaxMsg(msg, applyMsg, "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, cmdMsg, false);
		if (actionCmd == "Start") {
			localSeq++;
		}
	}

	function OnChangePresetList()
	{
		var selPresetName = $("#PresetList option[value='"+$("#PresetList").val()+"']").text().split(':');
		if (selPresetName[1] == "" || parseInt($("#PresetList").val()) == 0) {
			$("#ptz_tabs").tabs("disable", 1);			
		}
		else {
			$("#ptz_tabs").tabs("enable", 1);
			if (currentTabName == 'presetedit') {
				OnClickPtzTabs('sequence');
			}
		}
		$("#ptz_tabs").tabs("option", "active", 0);
		EventSetup.VA.view("");
	}

	function SetPTZCookie(seqName)
	{
		switch(seqName) {
			case 'Preset':
				SetCookie("PresetStatus", $("#PresetList").val());
				break;
			case 'Group':
				SetCookie("SequenceSetupStatus", 2);
				SetCookie("GroupStatus", $("#GroupNo").val());
				break;
			case 'Tour':
				SetCookie("SequenceSetupStatus", 3);
				SetCookie("TourGroupStatus", $("#TourGroupNo").val());
				break;
			case 'Autorun':
				SetCookie("SequenceSetupStatus", 4);
				break;
			case 'Swing': default:
				SetCookie("SequenceSetupStatus",1);
				SetCookie("SwingStatus", $("#SwingMode").val());
				break;				
		}
	}

	function GetPTZCookie()
	{
		var presetStatus 			= GetCookie("PresetStatus");
		var sequenceSetupStatus = GetCookie("SequenceSetupStatus");
		var swingStatus 			= GetCookie("SwingStatus");
		var groupStatus 			= GetCookie("GroupStatus");
		var tourGroupStatus 		= GetCookie("TourGroupStatus");

		if (presetStatus != ""){
			$("#PresetList").val(presetStatus);
		}
		if (sequenceSetupStatus != "") {
			if (swingStatus != "") {
				$("#SwingMode").val(swingStatus);
			}		
			if (groupStatus != "") {
				$("#GroupNo").val(groupStatus);
				
			}
			if (tourGroupStatus != "") {
				var i = 0;
				var status = false;
				for(i = 0 ; i < $("#TourGroupNo option").size() ; i ++ ) {
					if(parseInt($("#TourGroupNo option:eq("+i+")").val()) == tourGroupStatus) {
						status = true;
						break;
					}
				}
				
				if(status == true) {
					$("#TourGroupNo").val(tourGroupStatus);
				} else {
					$("#TourGroupNo").val($("#TourGroupNo option:eq(0)").val());
				}		
			}
			$("#sequence_tabs").tabs("option", "active", parseInt(sequenceSetupStatus)-1);	
		}		
		OnChangePresetList();		
		RedrawSwingArea();
		OnChangeGroupNo();
	}
	

	function OnClickPtzTabs(tabName)
	{
		currentTabName = tabName;
		var selPresetName = $("#PresetList option[value='"+$("#PresetList").val()+"']").text().split(':');
		if (tabName == 'presetedit') {
			if (curPresetNo != parseInt($("#PresetList").val())) {
				curPresetNo = $("#PresetList").val();
			}
			isOnloading = true;
			RequestGetPresetEdit();	
			isOnloading = false;
			RequestStartStopPresetEdit('Start');
			$("#presetEditType").val(0);
			OnChangePresetEditType();
			SetPTZCookie('Preset');
			if(selPresetName[1] != "")	ChangeHomePositionImage();			
			$("#camera_tabs .ui-tabs-panel").css("height", "400px"); 	
		}
		else {
			clearTimeout(timer);
			RequestStartStopPresetEdit('Stop');
			EventSetup.VA.view("");
			ChangeHomePositionImage();
		}
		ChangePresetButtonStatus();
	}

	function DisplayPtzTab()
	{
		$("#ptz_tabs").show();
		$("#ptz_tabs").tabs("disable", 1);
		GetPTZCookie();
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

		setTimeout("DisplayPtzTab()", 300);
		CheckGroupList(false);
		OnClickTourList();
		OnChangeAutoRunMode();
		OnChangeAutoRunMode('Schedule');
		RedrawSwingArea();
		ChangeHomePositionImage();
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
		if (currentTabName == 'sequence') {		
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
		else if(currentTabName == 'presetedit') {
			$("#home-start").attr('src', '../images/common/PTZ/gohome_disable.png');
			$("#home-start").hover(function(){ ChangeImage('home-start','../images/common/PTZ/gohome_disable.png');
							}, function(){ ChangeImage('home-start','../images/common/PTZ/gohome_disable.png');
							}).unbind('click');
			$("#home-start").css('cursor', 'default');
			
			$("#home-set").attr('src', '../images/common/PTZ/sethome_disable.png');
			$("#home-set").hover(function(){ ChangeImage('home-set','../images/common/PTZ/sethome_disable.png');
							}, function(){ ChangeImage('home-set','../images/common/PTZ/sethome_disable.png');
							}).unbind('click');
			$("#home-set").css('cursor', 'default');
		}
	}

	function ChangePresetButtonStatus()
	{
		if (currentTabName == 'sequence') {	
			$('#PresetList').removeAttr('disabled');
			$('#PresetName').removeAttr('disabled');
			$('.presetBtnEnable').show();
			$('.presetBtnDisable').hide();
		}
		else {			
			var selPresetName = $("#PresetList option[value='"+$("#PresetList").val()+"']").text().split(':');
			if(selPresetName[1] == ""){
				$('#PresetList').removeAttr('disabled');
				$('#PresetName').removeAttr('disabled');
				$('.presetBtnEnable').show();
				$('.presetBtnDisable').hide();
			} else {
				$('#PresetList').attr('disabled', 'disabled');
				$('#PresetName').attr('disabled', 'disabled');
				$('.presetBtnEnable').hide();
				$('.presetBtnDisable').show();
			}
			
		}
	}

/////////////////////////////////////////
/////// 		PRESET EDIT
/////////////////////////////////////////	
		
	function RequestGetPresetEdit()
	{
		var reqUrl = "<?php echo GetMyRequestURI($_SERVER['SCRIPT_NAME']); ?>";
		if (BrowserDetect.browser == "Explorer" || (BrowserDetect.browser == 'Safari' && reqUrl.search('.local') != -1)) {
			reqUrl = ".."+reqUrl.substr(reqUrl.indexOf("/setup/"));
		}
		
	  	$.ajax({
	  		type: "POST",
	  		data: "presetNo="+$("#PresetList").val()+"&pctz="+(new Date()).getTime(),
	  		async: false,
	  		cache: false,
	  		url: reqUrl,
	  		dataType: "xml",
	  		success: OnSuccessPresetEdit,
	  		error: null
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
	}

	function OnSuccessPresetEdit(xml)
	{
		<?php if($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ) { ?>
		var dataList = ["Information", "ImageSSDR", "ImageWhiteBalance", "ImageExposure", "ImageSpecial", "ImageFocus", "ImageTracking", "VAConfiguration"];
		<?php }else{ ?>
		var dataList = ["Information", "ImageSSDR", "ImageWhiteBalance", "ImageBackLight", "ImageExposure", "ImageSpecial", "ImageFocus", "ImageTracking", "VAConfiguration"];
		<?php } ?>
		for (var i=0; i<dataList.length; ++i) {
			$(xml).find(dataList[i]).each(function() {
				eval("ParsingXML_"+dataList[i]+"($(this));");
			});
		}
		InitCameraSetup();
	}
	
	function ParsingXML_Information(xmlData)
	{
		SENSOR_MODE = xmlData.find('SensorFrameMode').text();
		LONG_SHUTTER_SPEED = xmlData.find('LongShutterSpeed').text();
		TAMPERING_ENABLE = xmlData.find('TamperingEnable').text();
		//MD_ENABLE = xmlData.find('MDEnable').text();
		//IV_ENABLE = xmlData.find('IVEnable').text();
		BLC_MODE = parseInt(xmlData.find('BlcMode').text(),10);
	}

	function OnChangePresetEditType()
	{
		if ($("#presetEditType").val() == 0) {	// Camera setup
			$("#tabs-camerasetup").show();
			$("#camera_tabs").tabs();
			$("#tabs-va").hide();	
			$("#camera_tabs").tabs("option", "active", 0);
			if($("#after_action").val() == 3 || TAMPERING_ENABLE == 1){
				$("#dis").attr("disabled", "disabled");
			}else{
				$("#dis").removeAttr("disabled");
			}
			EventSetup.VA.view("");
		}
		else {	// MD/VA setup
			$("#tabs-camerasetup").hide();
			$("#tabs-va").show();
			OnClickVaMode();
		}
	}

	function InitCameraSetup()
	{
		if (SENSOR_MODE == 0 || SENSOR_MODE == 1) {
			$('#blc_mode :eq(3)').html("- - -");
			$('#wdr_level').attr("disabled","disabled");
		}
		else {
			$('#blc_mode :eq(3)').html("<?php echo $t_wdr[$GLOBALS["LANGINDEX"]]; ?>");
		}	
		OnClickSsdrMode();
		OnChangeWhitebalnaceMode();
		<?php if(!($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ)) { ?>
		OnChangeBlcMode();
		<?php } ?>
		OnChangeExposure();
		OnChangeFocus();
		OnChangeSpecial();
	}

	function OnClickApply(mode)
	{
		var msg = "";
	  	msg += "<SetPresetImageConfiguration>";
	  	msg += "<TestCmd>"+mode+"</TestCmd>";
	  	msg += "<Index>"+$("#PresetList").val()+"</Index>";	  
	  	msg += "<ImageSetting>";	  	
	  	msg += MakeSsdrXml(); 				//ssdr_tab.cgi
		msg += MakeWhitebalanceXml();	//whitebalance_tab.cgi
		<?php if(!($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ)) { ?>
		msg += MakeBacklightXml(mode);		//backlight_tab.cgi
		<?php } ?>
		msg += MakeExposureXml();			//exposure_tab.cgi
		msg += MakeFocusXml();				//focus_tab.cgi
	 	msg += MakeSpecialXml();
		msg += "</ImageSetting>";
		msg += "</SetPresetImageConfiguration>";

		clearTimeout(timer);
		if(mode == TEST) {
			timer = setTimeout("FailTestCommand()",240000);
			RequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, "NO_REFRESH", true, OnSuccessTest);
			localSeq++;
		}
		else {
			RequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, "NO_REFRESH", false);
			localSeq++;
			SetPresetEditVaCommand();
		}
	}
	
	function OnClickInit()
	{
	  	var msg;
	  	msg = "<SetPresetImageConfiguration>";
	  	msg += "<TestCmd>"+2+"</TestCmd>";
		msg += "<Index>"+$("#PresetList").val()+"</Index>";	  
		msg += "</SetPresetImageConfiguration>";

		RequestAjaxMsg(msg, "<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, "Camera");
	}

	function OnSuccessTest(req)
	{
	  	<?php if($GLOBALS['M_MAX_RESOLUTION'] == MAX_3_MEGA) { ?>
	  	if(req == "66" && isApplying == 0)
	  	{
	  		isApplying = 1;
	  		alert("<?php echo $msg_applying[$GLOBALS['LANGINDEX']]; ?>");
	  		window.location.reload(true);
	  	}
	  	<?php } ?>
	  	if(setupState == 2){
	  		setupState = 1;
	  	} else if (setupState == 3){
	  		setupState = 2;
	  		OnClickApply(TEST);;
	  	}
	}
	
	function SetPresetEditVaCommand()
	{
		var msg = "";
		msg += "<SetPresetVAConfiguration>";
		msg += "<Index>"+$("#PresetList").val()+"</Index>";
		msg += MakeVideoAnalyticsXml();
		msg += "</SetPresetVAConfiguration>";
		RequestAjaxMsg(msg, "<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $GLOBALS['REQUEST_URI']; ?>", "NO_REFRESH");
		localSeq++;
	}

	function FailTestCommand()
	{
		alert("<?php echo $t_timeout[$GLOBALS['LANGINDEX']]; ?>");
	  	window.location.reload(true);
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
					?>
	  				<div class="h3_tit">
						<h3 class="wid320"><?php echo $t_presetSetup[$GLOBALS['LANGINDEX']]; ?></h3>
					</div>
					<table class="data_write">
						<colgroup>
							<col style="width:160px;" />
							<col />
						</colgroup>
						<tbody>
							<tr>
								<th scope="row"><?php echo $t_number[$GLOBALS['LANGINDEX']]; ?></th>
								<td>
									<select class="selectbox_style" id="PresetList" onchange="OnChangePresetList()">
							<?php
								for($index=1; $index<=MAX_PTZ_PRESET255; ++$index){
							?>
										<option value="<?php echo $index; ?>" ><?php echo $index.':'.trim($presetConf->preset[$index-1]['Name']['value']); ?></option>
							<?php
								
									if ($presetConf->preset[$index-1]['Enabled']['value'] == 1) {
										$presetCnt = 1;
									}
								}
							?>
							
							<script>
								presetCnt = "<?php echo $presetCnt ?>";
							</script>
									</select>
								</td>
							</tr>
							<tr>
								<th scope="row"><?php echo $t_name[$GLOBALS['LANGINDEX']]; ?></th>
								<td>
									<input type="text" class="text" id="PresetName" maxlength ="12" onkeypress="IsNumChar(event); NoKorean(event)" onkeydown='NoKorean(event);' style="width:191px;" >
								</td>
							</tr>
							<tr class="presetBtnEnable">
								<th></th>
								<td>
									<a class="btn_setup" href="javascript:OnClickPresetCmd('Start');" style="color:#fff"> <?php echo $t_go[$GLOBALS['LANGINDEX']]; ?> </a>
									<a class="btn_setup" href="javascript:OnClickPresetCmd('Add');" style="color:#fff"> <?php echo $t_add[$GLOBALS['LANGINDEX']]; ?> </a>
									<a class="btn_setup" href="javascript:OnClickPresetCmd('Remove');" style="color:#fff"> <?php echo $t_remove[$GLOBALS['LANGINDEX']]; ?> </a>
								</td>
							</tr>
							<tr class="presetBtnDisable" style="display:none">
								<th></th>
								<td>
									<a class="btn_setup_disable"> <?php echo $t_go[$GLOBALS['LANGINDEX']]; ?> </a>
									<a class="btn_setup_disable"> <?php echo $t_add[$GLOBALS['LANGINDEX']]; ?> </a>
									<a class="btn_setup_disable"> <?php echo $t_remove[$GLOBALS['LANGINDEX']]; ?> </a>
								</td>
							</tr>
						</tbody>
					</table>
					<div id="ptz_tabs" style="display:none;">
						<ul>
							<li class="ptz_tabs"><a href="#sequence_tabs" style="width:347px;padding-left:0em;padding-right:0em;" onClick="OnClickPtzTabs('sequence')"><?php echo $t_sequenceSetup[$GLOBALS["LANGINDEX"]]; ?></a></li>
							<li class="ptz_tabs"><a href="#presetedit_tabs" style="width:347px;padding-left:0em;padding-right:0em;" onClick="OnClickPtzTabs('presetedit')"><?php echo $t_preseteditSetup[$GLOBALS["LANGINDEX"]]; ?></a></li>
						</ul>
						<div id="sequence_tabs" style="padding-top:20px; height:575px">
							<ul>
								<li class="inner-first"><a href="#tabs-swing" style="width:135px;"><?php echo $t_swing[$GLOBALS["LANGINDEX"]]; ?></a></li>
								<li class="inner-first"><a href="#tabs-group" style="width:135px;"><?php echo $t_group[$GLOBALS["LANGINDEX"]]; ?></a></li>
								<li class="inner-first"><a href="#tabs-tour" style="width:135px;"><?php echo $t_tour[$GLOBALS["LANGINDEX"]]; ?></a></li>
								<li style="width:246px; text-align:center"><a href="#tabs-autorun" style="width:246px;"><?php echo $t_traceAutorun[$GLOBALS["LANGINDEX"]]; ?></a></li>
							</ul>
						<?php
							require_once('./ptz_tab/swing_tab.cgi');
							require_once('./ptz_tab/group_tab.cgi');
							require_once('./ptz_tab/tour_tab.cgi');
							require_once('./ptz_tab/trace_autorun_tab.cgi');
						?>						
						</div>
						<div id="presetedit_tabs" style="height:600px">
							<table class="data_write" style="padding-top:20px">
								<colgroup>
									<col style="width:142px;" />
									<col />
								</colgroup>
								<tbody>
									<tr>
										<th scope="row" style="padding-left:0px"><?php echo $t_type[$GLOBALS["LANGINDEX"]]; ?></th>
										<td>
											<select class="selectbox_style_wid230" id="presetEditType" onchange="OnChangePresetEditType()">
												<option value='0'><?php echo $menu_camera[$GLOBALS["LANGINDEX"]]; ?></option>
												<option value='1'><?php echo $menu_videoanalytics[$GLOBALS["LANGINDEX"]]; ?></option>
											</select>
										</td>
									</tr>
								</tbody>
							</table>
							<div id="tabs-camerasetup" style="height:560px">	
								<div id="camera_tabs" style="margin-top:20px;">
									<ul class="preset-camera">
										<li class="preset-camera" id="li-ssdr"><a class="preset-camera" href="#tabs-ssdr">SSDR</a></li>
										<li class="preset-camera" id="li-wb"><a class="preset-camera" href="#tabs-wb"><?php echo $t_whitebalance[$GLOBALS["LANGINDEX"]]; ?></a></li>
										<?php if(!($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ)) { ?>
										<li class="preset-camera" id="li-backlight" onclick="javascript:SISOPlugin.ptzControl.onClickBLCStatus();"><a class="preset-camera" href="#tabs-backlight"><?php echo $t_backlight[$GLOBALS["LANGINDEX"]]; ?></a></li>
										<?php } ?>
										<li class="preset-camera" id="li-exposure"><a class="preset-camera" href="#tabs-exposure"><?php echo $t_exposure[$GLOBALS["LANGINDEX"]]; ?></a></li>
										<li class="preset-camera" id="li-special"><a class="preset-camera" href="#tabs-special"><?php echo $t_special[$GLOBALS["LANGINDEX"]]; ?></a></li>
										<li class="preset-camera" id="li-focus"><a class="preset-camera" href="#tabs-focus"><?php echo $t_focus[$GLOBALS["LANGINDEX"]]; ?></a></li>
									</ul>
									<div id="tabs-ssdr"><?php require_once('./camera_tab/'.$isp_name.'/ssdr_tab.cgi'); ?></div>
									<div id="tabs-wb"><?php require_once('./camera_tab/'.$isp_name.'/whitebalance_tab.cgi'); ?></div>
									<?php if(!($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ)) { ?>
									<div id="tabs-backlight"><?php require_once('./camera_tab/'.$isp_name.'/backlight_tab.cgi'); ?></div>
									<?php } ?>
									<?php if($isp_name == 'wn2_ptz'){ ?>
										<?php if($GLOBALS["M_MODEL_GROUP"] == MF_6320) { ?>
										<div id="tabs-exposure"><?php require_once('./camera_tab/'.$isp_name.'/exposure_tab_6320.cgi'); ?></div>
										<?php }else{ ?>
										<div id="tabs-exposure"><?php require_once('./camera_tab/'.$isp_name.'/exposure_tab_5430.cgi'); ?></div>
										<?php } ?>										
									<?php }else{ ?>
									<div id="tabs-exposure"><?php require_once('./camera_tab/'.$isp_name.'/exposure_tab.cgi'); ?></div>
									<?php } ?>
									<div id="tabs-special"><?php require_once('./camera_tab/'.$isp_name.'/special_tab.cgi'); ?></div>			
									<div id="tabs-focus"><?php require_once('./camera_tab/'.$isp_name.'/focus_tab.cgi'); ?></div>
								</div>
								<div class="btn_right">
									<a class="btn_apply" href="javascript:OnClickApply(SAVE)" style="color:#fff"> <?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?> </a>
								</div>
							</div>
							<div id="tabs-va" style="display:none; height:0px; margin-left:-8px">
								<?php
									$vaConf = $presetVaConf;
									require_once('./ptz_tab/presetedit_va.cgi');
								?>
								<div class="btn_right">
									<a class="btn_apply" href="javascript:OnClickApply(SAVE)" style="color:#fff"> <?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?> </a>
								</div>
							</div>						
							<div id="DisableIVSelectLayer" style="position:absolute; width:695px; height:580px; left: 0px; top: 0px; background-color:#000000; display:none; z-index:1000; filter:alpha(opacity=0.3); opacity:0.3; -moz-opacity:0.3; -ms-filter: 'progid:DXImageTransform.Microsoft.Alpha(Opacity=30)';"></div>
						</div>
					</div>			
				</div>
			</div>
		</div>
	</body>
</html>
