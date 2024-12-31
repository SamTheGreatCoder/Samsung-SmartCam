<?php
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_menu.cgi');
require_once ('../language/language_av_ptz.cgi');
require_once ('../language/language_av_camera.cgi');
require_once ('../language/language_event_common.cgi');
require_once ('../language/language_event_videoanalytics.cgi');

$event_name = 'ptzsequence';

$classInstances	= GetClassInstance('ptzsequence');
$presetConf 		= $classInstances['PresetList'];
$groupsConf 		= $classInstances['PTZGroup'];
$autorunConf  		= $classInstances['PTZAutorun'];
$swingsConf    	= $classInstances['PTZSwing'];
$tourConf     	 	= $classInstances['PTZTour'];

if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ) {
	$isp_name = 'wn2_ptz';
}
else if($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ){
	$isp_name = 'wn3_ptz';
}
else{
	$isp_name = 'wn3_ptz';
}

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
	<link rel="stylesheet" type="text/css" href="../css/jquery.ui.tabs.css"/>
	<link rel="stylesheet" type="text/css" href="../css/jquery.ui.theme.css"/>
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
		.ui-tabs .ui-tabs-panel {
			height: 550px;
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

	var okLang 					= "<?php echo $t_ok[$GLOBALS['LANGINDEX']]; ?>";
	var cancelLang				= "<?php echo $t_cancel[$GLOBALS['LANGINDEX']]; ?>";
	var deleteLang				= "<?php echo $t_delete[$GLOBALS['LANGINDEX']]; ?>";
	var titleLang				=["<?php echo $t_virtual_line_based[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $t_defined_area[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $t_entire_area[$GLOBALS['LANGINDEX']]; ?>"];
	var directionLang			=["<?php echo $t_right[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $t_left[$GLOBALS['LANGINDEX']]; ?>"];
		
	var timer;
 	var setupState = 1;
 	var isOnloading = true; 	
 	var isApplying = 0;
	
	var MAX_PRESET_CNT = <?php echo MAX_PTZ_PRESET255; ?>;
	var MAX_PRESET_OF_PRESETLIST = <?php echo MAX_PRESET_OF_PRESETLIST; ?>;	//128
	var MAX_GROUP_OF_TOUR_CNT = <?php echo MAX_GROUP_OF_TOUR; ?>;
	var MAX_PTZ_GROUP = <?php echo MAX_PTZ_GROUP; ?>;

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
		lnbonoff("lnb_ptz");
		$("#ptz_tabs").tabs();
		
		$(".ptz_tabs").css({
							"width" : 347,
							"text-align": "center",
							"padding-left": ".0em"});
		$(".inner-first").css({
							"width" : 135,
							"text-align": "center"});

		if(BrowserDetect.browser == 'Chrome') {
			$(window).on('beforeunload', function(){
				//RequestStartStopPresetEdit('Stop');
			});
		}
		else {
			$(window).on('unload', function() {
				//RequestStartStopPresetEdit('Stop');
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

	function SetPTZCookie(seqName)
	{
		switch(seqName) {
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
		var sequenceSetupStatus = GetCookie("SequenceSetupStatus");
		var swingStatus 			= GetCookie("SwingStatus");
		var groupStatus 			= GetCookie("GroupStatus");
		var tourGroupStatus 		= GetCookie("TourGroupStatus");

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
			$("#ptz_tabs").tabs("option", "active", parseInt(sequenceSetupStatus)-1);	
		}
		RedrawSwingArea();
		OnChangeGroupNo();
	}
	
	function DisplayPtzTab()
	{
		$("#ptz_tabs").show();
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
		
		InitGroupList();
//		setTimeout("DisplayPtzTab()", 300);
		DisplayPtzTab();

		DrawTourList();
		OnChangeAutoRunMode();
		OnChangeAutoRunMode('Schedule');
		
	//	RedrawSwingArea();
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
					<div id="ptz_tabs" style="display:none;">
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
				</div>
			</div>
		</div>
	</body>
</html>
