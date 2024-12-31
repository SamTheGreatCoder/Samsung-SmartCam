<?php
require_once ('../cgi-bin/adv/_define.inc');
require_once ('./language/language_menu.cgi');
require_once ('./language/language_monitoring.cgi');
require_once ('./language/language_tooltip.cgi');

$classInstances = GetClassInstance('monitoring');
$ivConf = NULL;
$relayConf = NULL;
$auxConf = NULL;
$presetConf = NULL;

if ($GLOBALS['M_ALARMOUT_COUNT'] != 0)		 			$relayConf = $classInstances['RelayOutputStates'];
if ($GLOBALS['M_SUPPORT_EVENT_VA'] & IV_SUPPORT)	$ivConf = $classInstances['VAConfiguration']->ivConf;
if ($GLOBALS['M_AUX_COUNT'] != 0)		 					$auxConf = $classInstances['PTZAuxiliary'];
if ($GLOBALS['M_SUPPORT_PTZ'] || $GLOBALS['M_SUPPORT_EXTERNAL_PTZ']) $presetConf = $classInstances['PTZPreset'];
if ($GLOBALS['M_SPECIAL_TYPE'] == 1)
{
// DEV_S1PWD_CHANGE_TIME 
$timeClassInstances = GetClassInstance('time_password');
$timepwd	= $timeClassInstances['time_password'];
$userClassInstance = GetClassInstance('user');
$userConf	= $userClassInstance['UserConfiguration'];
$period = $userConf->dataInfo['Period']['value'] * 30;
// DEV_S1PWD_CHANGE_TIME -
}
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="kr" xml:lang="kr">
<head>
	<meta http-equiv="X-UA-Compatible" content="IE=Edge; requiresActiveX=true">
	<META http-equiv="Expires" content="-1">
	<META http-equiv="Pragma" content="no-cache">
	<META http-equiv="Cache-Control" content="No-Cache">
	<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
	<title>iPOLiS NETWORK CAMERA WEBVIEWER</title>
	<link rel="stylesheet" type="text/css" href="./css/techwin.css" />	
	<link rel="stylesheet" type="text/css" href="./css/jquery.ui.slider.css" />
	<link rel="stylesheet" type="text/css" href="./css/jquery.ui.tabs.css"/>	
	<link rel="stylesheet" type="text/css" href="./css/event_canvas.css" />
	<style>
		#container {
		  	overflow:hidden;
	   }
	   #lnb {
	  	 height:1100px;
	   }
	   #lnb-list {
	      height:1100px;
	   }	   
		a.pluginInstall:link, a.pluginInstall:visited, a.pluginInstall:focus, a.pluginInstall:hover, a.pluginInstall:active {
	  		color:#FFFFFF;
	  		text-decoration:underline;
	  		font-size:16px;
	  	}
	  	a:focus { outline: none; }

		div.gnb-tab {
			width: 560px;
		}

	  	div.gnb-tab div.profile {
			float:left;
			margin-top:17px;
			padding-left:5px;
		}
		.ptzbtn {
			position: absolute;
			left: 10px;
			top: 5px;
		}
		.areabtn {
			position: absolute;
			left: 18px;
			top: 28px;
		}

		.ui-tabs .ui-tabs-nav li a 
		{
		   background-color: #1b2029;
		   border-bottom-width: 0px;
		}
			.ui-tabs .ui-tabs-nav li a:hover
			{
			   background-color: #36567b;
			   border-bottom-width: 0px;
			}
		.ui-tabs .ui-tabs-nav .ui-tabs-active a
		{
			background-color: #0087ef;
			border-bottom-width: 0px;
			font-weight: bold; 
		}
			.ui-tabs .ui-tabs-nav .ui-tabs-active a:hover
			{
				background-color: #0087ef;
				border-bottom-width: 0px;
				font-weight: bold; 
			}
		.ui-tabs .ui-tabs-panel
		{
			border-bottom-right-radius:0px;
			border-bottom-left-radius:0px;
			border: 1px solid #40495a;
		}
		.ptztitle {
			margin-left: 0px;
			margin-bottom: 5px;
		}
		.ui-slider-vertical .ui-slider-range{
			background: #000000;
		}
		img {
			cursor:pointer;
		}
		.sequence_btn {
			position:absolute;
		}
		#IEoverlay{
			background: rgba(0,0,0,.1);
			background:#000;
			z-index:99999;
			width: 4000px;
			position: absolute;
			top: 2px;
			left: 0px;
			height: 2500px;
			display:none;
		}
  	</style>

	<script type="text/javascript" src="./js/jquery-1.9.1.js"></script>
  	<script type="text/javascript" src="./js/jquery-ui.js"></script>  	
	<script type="text/javascript" src="./js/jquery.cookie.js"></script>
	<script type="text/javascript" src="./js/lnb_monitoring.js"></script>
	<script type="text/javascript" src="./js/board.js"></script>
	<script type="text/javascript" src="./js/common_function.js"></script>
	<script type="text/javascript" src="./js/fullscreenApi.js"></script>
	<script type="text/javascript" src="./js/pluginCheck.js"></script>
	<script type="text/javascript" src="./js/pluginControl.js"></script>
	<script type="text/javascript">	
<?php
	if ($classInstances['Information']->dataInfo['PasswordCheck']['value'] == 1) {
?>
		window.location.href = './pw_change.cgi';
<?php
	}
	else if ($classInstances['Information']->dataInfo['PasswordCheck']['value'] == 2) {
?>
		alert("<?php echo $msg_change_weak_password[$GLOBALS['LANGINDEX']]; ?>");
<?php
	}
?>	
	$(document).ready(function(){
		$(document).tooltip({
			open: function (event, ui) {
				setTimeout(function () {
					$(ui.tooltip).hide();
				}, 1000);
			}
		});
		<?php if (($GLOBALS['M_SUPPORT_PTZ']) && $GLOBALS['USERINFO']['ptz'] == 1) { ?>
			SetSavePresetDialog();
		<?php } ?>
		$("#sequence-tabs").tabs();
		$("#Plus-Btn, #Minus-Btn, #btnHomeStart, #btnFit").tooltip({
			position: {
        		my: "right+30 center", 
        		at: "left bottom+25"
			},
			open: function (event, ui) {
				setTimeout(function () {
					$(ui.tooltip).hide();
				}, 1000);
			}
		 });

		// Slider
		$('#slider-vol').slider({
			orientation: "horizontal",
			value:3,
			min: 0,
			max: 5,
			range: "min",
			slide: function( event, ui ) {
			  SISOPlugin.setVolume(ui.value);
			  volumeVal = ui.value;
			}
		});
		$('#slider-vol-disable').slider({
			orientation: "horizontal",
			value:0,
			min: 0,
			max: 0,
			range: "min",
			slide: function( event, ui ) {
			}
		});

   	$( ".profileAccess" ).mouseup(function() {
     		window.open('./monitoring_info.cgi', 'popup', 'top=150, left=420, width=960, height=500, location=no, status=no, scrollbars=yes, resizable=no');
  		});
	});

	var browserName = "<?php echo GetBrowserName(); ?>";
	var ieVer = <?php echo ieversion(); ?>;

	var localSeq				= <?php echo $_SESSION['count']; ?>;
	var ajaxReqUrl				= "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq;
	var currentUserLevel		= "<?php echo $GLOBALS['USERINFO']['level']; ?>";
	var userRightVideo 		= "<?php echo $GLOBALS['USERINFO']['profile']; ?>";
	var userRightCtrl   		= "<?php echo $GLOBALS['USERINFO']['relay']; ?>";
	var userRightAudioIn  	= "<?php echo $GLOBALS['USERINFO']['audioin']; ?>";
	var userRightAudioOut	= "<?php echo $GLOBALS['USERINFO']['audioout']; ?>";
	var userRightPTZ   		= "<?php echo $GLOBALS['USERINFO']['ptz']; ?>";
	var recordingEnable		= <?php echo $classInstances['Information']->dataInfo['RecordingEnable']['value']; ?>;
	var recordingStatus 		= <?php echo $classInstances['Information']->dataInfo['ManualRecordingStatus']['value']; ?>;
	var installMsg				= new Array();
	installMsg[0] = "<?php echo $msg_plugin_install[$GLOBALS['LANGINDEX']]; ?>";
	installMsg[1] = "<?php echo $msg_plugin_install2[$GLOBALS['LANGINDEX']]; ?>";
	installMsg[2] = "<?php echo $msg_notsupport_plugin[$GLOBALS['LANGINDEX']]; ?>";

	var ValidProfileNum 	= new Array();
	var profilename 		= new Array();
	var encoding 			= new Array();
	var resolWidth 		= new Array();
	var resolHeight 		= new Array();
	var constantBitrate 	= new Array();
	var bitrateLimit 		= new Array();
	var frameRateLimit 	= new Array();
	var compression 		= new Array();
	var constantBitrate 	= new Array();
	var DrawProfileList 	= new Array();
	var audioIn				= new Array();
	var useCropEncoding 	= new Array();
	var cropX = new Array();
	var cropY = new Array();
	var cropWidth = new Array();
	var cropHeight = new Array();

	var relayStatus = new Array();
	var auxStatus = 0;
	var OriginalStatus = 0;
	var FullScreenStatus = 0;
	var FittStatus = 0;
	var DigitPTZStatus;
	var TalkStatus = 0;
	var ListenStatus = 0;
	var defaultProfile;
	var isWide = 0;
	var isConnectFail = 0;
	var presetIndex 	= 1;

	var viewportWidth;
	var viewportHeight;

	var volumeVal = 3;

	var audioTalkTimeoutValue = 0;	
	
	var LockOnPosX = 0;
	var LockOnPosY = 0;

	var doit;

	var isShowing = 0;
	var isShowingInstantRecord = 0;

	var localRecordingTimeout = 0;

<?php if($GLOBALS['M_SUPPORT_LOCAL_RECORDING']) { ?>
	recordingEnable = 1;
<?php } ?>

	var isEnabledRotate = 0;
<?php if($GLOBALS['M_SUPPORT_ROTATE'] && $classInstances['Information']->dataInfo['Rotate']['value'] > 0){?>
	isEnabledRotate = 1;
<?php } ?>

	var presetCnt = 0;	
	var MAX_PRESET_CNT 		= <?php echo MAX_PTZ_PRESET255; ?>;
	
	var selectPresetEnable	= new Array();
	var selectPresetNum 	= new Array();
	var selectPresetName	= new Array();
<?php if($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>	
	// DEV_S1PWD_CHANGE_TIME
	var is_time = <?=$timepwd->dataInfo['IsTime']?>;
	var msg_pwdchange = "<?=sprintf ( $msg_pwdchange[$GLOBALS['LANGINDEX']], $period )?>";
<?php } ?>
<?php
  	if ($GLOBALS['M_ALARMOUT_COUNT'] > 0) {
  		for ($index=0; $index<4; ++$index) {
?>
  			relayStatus[<?php echo $index; ?>] = <?php echo $relayConf->relayOutputState[$index]->dataInfo['LogicalState']['value']; ?>;
<?php
  		}
  	}

  	if ($GLOBALS['M_AUX_COUNT'] > 0) {
?>
		auxStatus = <?php echo $auxConf->dataInfo['Value']['value']; ?>;
<?php
	}
	
  	for ($index=0; $index<10; ++$index) {
?>
		ValidProfileNum[<?php echo $index; ?>] = "valid";
		profilename[<?php echo $index; ?>] 		= "<?php echo $classInstances['VideoProfile']->profile[$index]->dataInfo['Name']['value']; ?>";
		encoding[<?php echo $index; ?>]			= <?php echo $classInstances['VideoProfile']->profile[$index]->dataInfo['Encoding']['value']; ?>;
		resolWidth[<?php echo $index; ?>]		= <?php echo $classInstances['VideoProfile']->profile[$index]->dataInfo['ResolWidth']['value']; ?>;
		resolHeight[<?php echo $index; ?>]		= <?php echo $classInstances['VideoProfile']->profile[$index]->dataInfo['ResolHeight']['value']; ?>;
		constantBitrate[<?php echo $index; ?>]	= <?php echo $classInstances['VideoProfile']->profile[$index]->dataInfo['ConstantBitrate']['value']; ?>;
		bitrateLimit[<?php echo $index; ?>]		= <?php echo ($classInstances['VideoProfile']->profile[$index]->dataInfo['BitrateLimit']['value']/1024); ?>;
		frameRateLimit[<?php echo $index; ?>]	= <?php echo $classInstances['VideoProfile']->profile[$index]->dataInfo['FrameRateLimit']['value']; ?>;
		compression[<?php echo $index; ?>]		= <?php echo $classInstances['VideoProfile']->profile[$index]->dataInfo['Compression']['value']; ?>;
		audioIn[<?php echo $index; ?>]			= <?php echo $classInstances['VideoProfile']->profile[$index]->dataInfo['UseAudioIn']['value']; ?>;
		useCropEncoding[<?php echo $index; ?>]	= <?php echo $classInstances['VideoProfile']->profile[$index]->dataInfo['UseCropEncoding']['value']; ?>;
		cropX[<?php echo $index; ?>]				= <?php echo $classInstances['VideoProfile']->profile[$index]->dataInfo['CropXpos']['value']; ?>;
		cropY[<?php echo $index; ?>]				= <?php echo $classInstances['VideoProfile']->profile[$index]->dataInfo['CropYpos']['value']; ?>;
		cropWidth[<?php echo $index; ?>]			= <?php echo $classInstances['VideoProfile']->profile[$index]->dataInfo['CropWidth']['value']; ?>;
		cropHeight[<?php echo $index; ?>]		= <?php echo $classInstances['VideoProfile']->profile[$index]->dataInfo['CropHeight']['value']; ?>;
		if (<?php echo $classInstances['VideoProfile']->profile[$index]->dataInfo['Default']['value']; ?> == 1) defaultProfile = <?php echo $index; ?>;

<?php if($GLOBALS['M_SUPPORT_ROTATE']){?>
		if (<?php echo $classInstances['Information']->dataInfo['Rotate']['value']; ?> == 1 || <?php echo $classInstances['Information']->dataInfo['Rotate']['value']; ?> == 3) {
			var swapVal = resolWidth[<?php echo $index; ?>];
			resolWidth[<?php echo $index; ?>] = resolHeight[<?php echo $index; ?>];
			resolHeight[<?php echo $index; ?>] = swapVal;
		}
<?php } ?>

<?php
  	}
?>

  	window.onkeydown = document.onkeydown = bodyOnkeydown;

  	function bodyOnkeydown(event)
  	{
  		var event = event?event:window.event?window.event:null;
  		if(event.keyCode == 27 && FullScreenStatus == 1)
  		{
  			SISOPlugin.makeBrowserFullScreen(0);
  			var ProfileStatus = $('#liveProfile').val();
  			FullScreenStatus = 0;
  			OriginalStatus = 0;
  			FittStatus = 0;
  			SISOPlugin.setResolution(parseInt(resolWidth[ProfileStatus], 10), parseInt(resolHeight[ProfileStatus], 10));
  			$('#contents').offset(offset);
  			$('#contents').offset({top:5, left:300});
  			$('#head').show();
  			document.getElementById('contents').style.padding = "20px 100px 20px 19px";
  			$("body").css("overflow","auto");
  			document.body.scroll = 'yes';
  			GetIVOverlay();
			$("#IEoverlay").css("display", "none");
  		}
		else if(event.keyCode == 9 && FullScreenStatus == 1)
		{
			return false;
		}
  	}
  	

	function OnLoad()
	{
		InitPresetList()
		DrawPresetList(0);
		openlnbMenu(1);
		SISOPlugin.init(installMsg, 0, 0);
	<?php 
		if (($GLOBALS['M_SUPPORT_PTZ']) && $GLOBALS['USERINFO']['ptz'] == 1) {
	?>
		GetPTZCookie();
	<?php
		}
	?>
	  	// draw profile list selectbox
	  	DrawProfileSelectList();
	  	$('#liveProfile').val(defaultProfile);
	  	DrawCurrentProfileInfo();
	  	StartPlugin();

		GetIVOverlay();

		<?php if($GLOBALS['M_ALARMOUT_COUNT'] > 0 && !($GLOBALS['USERINFO']['relay'] == 0 || $GLOBALS['USERINFO']['level'] == 3)) { ?>
		window.setInterval("CheckRelay()", 500);
		SISOPlugin.setRelayStatus(relayStatus);
		<?php } ?>

		// =========== DEV_S1PWD_CHANGE_TIME ================
<?php
if ($GLOBALS['M_SPECIAL_TYPE'] == 1)
{		
?>
		if ( is_time && currentUserLevel == 0){
			if (confirm(msg_pwdchange)){
				location.href = "/home/setup/basic_user.cgi";
				return;
			}else{
				$.ajax({
				  type: 'POST',
				  url: '/home/passwordtime.cgi',
				  data: { nonce : (new Date()).getTime() },
				  success:  function(data){
								console.log(data);
							},
				  dataType: 'text'
				});
			}
		}
		// ============== DEV_S1PWD_CHANGE_TIME // ===============
<?php 
} 
?>
	<?php 
		if($GLOBALS['M_AUX_COUNT'] > 0 && !($GLOBALS['USERINFO']['relay'] == 0 || $GLOBALS['USERINFO']['level'] == 3)) { 
	?>			
			if (auxStatus == 1) {
				relayStatus[<?php echo $GLOBALS['M_ALARMOUT_COUNT'] + 1; ?>] = 1;
			}
			else {
				relayStatus[<?php echo $GLOBALS['M_ALARMOUT_COUNT'] + 1; ?>] = 0;
			}
			//AuxBtnColorChange('monitoring');
			SISOPlugin.setRelayStatus(relayStatus);
	<?php	
		} 

		if ($GLOBALS['M_SUPPORT_LOCAL_RECORDING'] == 0 && $GLOBALS['USERINFO']['level'] == 0 && ($GLOBALS['M_SUPPORT_SD'] || $GLOBALS['M_SUPPORT_NAS'])) {
	?>
			SISOPlugin.ptzControl.manualRecordingBtnColorChange(recordingStatus);
	<?php
		}
	?>
		//window.setInterval("CheckPTZMove()", 100);

		OnFittClick();
		window.onresize = function(event) {
			clearTimeout(doit);
																																																																																																																																																																doit = window.setTimeout("OnResizeEvent()", 100);
		}

		<?php if($GLOBALS['M_SUPPORT_LOCAL_RECORDING']) { ?>
		if (BrowserDetect.OS == 'Mac') {
			$("#btnManualRecordingSpan").html("<img id=\"btnManualRecording\" src=\"./images/common/VIEW/rec_disable.png\" title=\"<?php echo $t_instantRecording[$GLOBALS['LANGINDEX']]; ?>\" style=\"cursor:default;\" class=\"mgr2\" />");
		}
		<?php } ?>
	}

	function OnResizeEvent(){
		var winWidth = window.innerWidth;
		var winHeight = window.innerHeight;

		if(document.getElementById('plugin').width == 1 || document.getElementById('plugin').height == 1)
			return;

  		var CurrProfile;
 		CurrProfile = $('#liveProfile').val();

		if(FittStatus == 1)
		{
		 	SetViewportSize();
		 	var widthVal = parseInt(viewportWidth) - 345;
		 	var heightVal = parseInt(viewportHeight) - 135;
		 	var ratio = resolWidth[CurrProfile] / resolHeight[CurrProfile];
			var viewportRatio = widthVal / heightVal;

			viewportRatio = viewportRatio.toFixed(1);
			ratio = ratio.toFixed(1);

			if (isEnabledRotate > 0) {
				if(ratio == 0.6){				// 16:9
					if(viewportRatio < ratio)
						heightVal = (widthVal * 25 / 9) - widthVal;
					else
						widthVal = (heightVal * 25 / 16) - heightVal;

					if(widthVal < 180 || heightVal < 320)
					{
						widthVal = 180;
						heightVal = 320;
					}
				}
				else if(ratio == 0.8 && resolHeight[CurrProfile] != 1280 && resolWidth[CurrProfile] != 1024 && resolHeight[CurrProfile] != 720 && resolWidth[CurrProfile] != 576){		//4//4:3
					if(viewportRatio < ratio)
						heightVal = (widthVal * 7 / 3) - widthVal;
					else
						widthVal = (heightVal * 7 / 4) - heightVal;

					if(widthVal < 240 || heightVal < 320)
					{
						widthVal = 240;
						heightVal = 320;
					}
				}
				else{								//5:4
					if(viewportRatio < ratio)
						heightVal = (widthVal * 9 / 4) - widthVal;
					else
						widthVal = (heightVal * 9 / 5) - heightVal;

					if(widthVal < 320 || heightVal < 256)
					{
						widthVal = 320;
						heightVal = 256;
					}
				}
			}
			else
			{
				if(ratio == 1.8){				// 16:9
					if(viewportRatio < ratio)
						heightVal = (widthVal * 25 / 16) - widthVal;
					else
						widthVal = (heightVal * 25 / 9) - heightVal;

					if(widthVal < 320 || heightVal < 180)
					{
						widthVal = 320;
						heightVal = 180;
					}
				}
				else if(ratio == 1.3 && resolHeight[CurrProfile] != 1024 && resolHeight[CurrProfile] != 576){		//4//4:3
					if(viewportRatio < ratio)
						heightVal = (widthVal * 7 / 4) - widthVal;
					else
						widthVal = (heightVal * 7 / 3) - heightVal;

					if(widthVal < 320 || heightVal < 240)
					{
						widthVal = 320;
						heightVal = 240;
					}
				}
				else{								//5:4
					if(viewportRatio < ratio)
						heightVal = (widthVal * 9 / 5) - widthVal;
					else
						widthVal = (heightVal * 9 / 4) - heightVal;

					if(widthVal < 320 || heightVal < 256)
					{
						widthVal = 320;
						heightVal = 256;
					}
				}
			}

		 	SISOPlugin.setResolution(parseInt(widthVal), parseInt(heightVal));
		  	//document.getElementById('plugin').width = widthVal;
		  	//document.getElementById('plugin').height = heightVal;

		  	if(BrowserDetect.browser != 'Firefox')
		   {
		  	  //document.body.style.overflow = 'hidden';
		  	}

			GetIVOverlay();
		}

		<?php	if (GetBrowserName() == 'Google Chrome') { ?>
		if (FullScreenStatus == 1) {
			window.setTimeout('DoChromeFullScreen()', 500);
		}
		<?php } ?>

		//window.scrollTo( 20, 0);
		window.scrollTo( 0, 0);		
	}

	function CheckRelay()
	{
		<?php 
			$relayCount = $GLOBALS['M_ALARMOUT_COUNT'];
			if ($GLOBALS['M_AUX_COUNT'] > 0) {
				$relayCount++;
			}
		?>

		<?php for ($index = 1; $index <= $relayCount; $index++) { ?>

		<?php if($GLOBALS['M_AUX_COUNT'] > 0 && $index == $relayCount) { ?>
		var val<?php echo $index;?> = SISOPlugin.getRelayStatus(<?php echo $relayCount;?>); // aux index is max alarm count + 1
		<?php } else { ?>
		var val<?php echo $index;?> = SISOPlugin.getRelayStatus(<?php echo $index-1;?>);
		<?php } ?>

		if (val<?php echo $index;?> == 1)
		{
			<?php if($GLOBALS['M_AUX_COUNT'] > 0 && $index == $relayCount) { ?>
			$('#btnAux').get(0).style.background = "#e65757";
			auxStatus = 1;
			<?php } else { ?>
			$('#btnRelay<?php echo $index;?>').get(0).style.background = "#e65757";
			<?php } ?>
			relayStatus[<?php echo $index-1;?>] = 1;
		}
		else
		{
			<?php if($GLOBALS['M_AUX_COUNT'] > 0 && $index == $relayCount) { ?>
			$('#btnAux').get(0).style.background = "#1b2029";
			auxStatus = 0;
			<?php } else { ?>
			$('#btnRelay<?php echo $index;?>').get(0).style.background = "#1b2029";
			<?php } ?>
			relayStatus[<?php echo $index-1;?>] = 0;
		}
		<?php } ?>
	}

	function DrawProfileSelectList()
	{
		$('#liveProfile').empty();
		for(var i = 0 ; i < 10 ; i++) {
			if(profilename[i].length > 0 && encoding[i] != 1)
			{
			  $('#liveProfile').append("<option value=\"" + i + "\">" + profilename[i] + "</option>");
			}
		}

		if(userRightVideo == 0 || currentUserLevel == 3)
		  $('#liveProfile').attr('disabled', 'disabled');
	}

	function DrawCurrentProfileInfo()
	{
		var h = parseInt($('#liveProfile').val());
	  	if(ValidProfileNum[h] == "valid") {
			var codecType = ["MJPEG", "MPEG4", "H.264"];
	  		$("#liveProfileCodec").html(codecType[parseInt(encoding[h])]);	  		
	  		$("#liveProfileName").html(profilename[h]);
	  		$("#liveProfileResol").html(resolWidth[h] + "X" + resolHeight[h]);
	  		$("#liveProfileFramerate").html((frameRateLimit[h]/1000) + "fps");
	  		<?php if ($GLOBALS['M_SUPPORT_COMPRESSION']) { ?> 	
			if (constantBitrate[h] == 0 || encoding[h] == 0) // if MJPEG or VBR, compression has to be shown!
	  		{
	  			if(compression[h] == 1) {
	  				$("#liveProfileCompression").html("<?php echo $t_best[$GLOBALS['LANGINDEX']]; ?>");
	  			} 
	  			else if (compression[h] == 20) {
	  				$("#liveProfileCompression").html("<?php echo $t_worst[$GLOBALS['LANGINDEX']]; ?>");
	  			} 
	  			else {
	  				$("#liveProfileCompression").html(compression[h]);
	  			}
	  		}
	  		else
	  		{
	  		  $("#liveProfileCompression").html("---");
	  		}
	  		<?php } ?>

			var bitrateControlMenu = ["<?php echo $t_max_bitrate[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $t_targetBitrate[$GLOBALS['LANGINDEX']]; ?>"];
			$("#liveProfileBitrateText").html(bitrateControlMenu[parseInt(constantBitrate[h])]);
			if (parseInt(encoding[h]) == 0) {
				$("#liveProfileBitrate").html((bitrateLimit[h]/1024) + "Kbps");
			}
			else {				
				var bitrateControlMsg = ["VBR", "CBR"];				
				$("#liveProfileBitrate").html((bitrateLimit[h]/1024) + "Kbps, " + bitrateControlMsg[parseInt(constantBitrate[h])]);
			}
		}
	}

	function StartPlugin()
	{
		$('#liveProfile').attr('disabled', 'disabled');
		var CurrProfile = $('#liveProfile').val();
		var userName = "<?php echo $GLOBALS['USERINFO']['encname']; ?>";
		var userPW = "<?php echo $GLOBALS['USERINFO']['encpw']; ?>";
		if (userName == "") {
			userName = "guest";
			userPW= "guest";
		}

  	// Notice : change resolution after liveplay!
		SISOPlugin.setSecurityEnhancement();
		// DEV_S1WEBVIEWER start
		//SISOPlugin.livePlay(location.hostname, <?php echo $classInstances['Information']->dataInfo['DevicePort']['value']; ?>, parseInt(CurrProfile), userName, userPW);
		<?php if ($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>
			SISOPlugin.setIsNoVideoEncrypt(<?php echo $userConf->dataInfo['IsEnableNoEncrypt']['value']; ?>);
			SISOPlugin.livePlay(location.hostname, <?php echo $classInstances['Information']->dataInfo['DevicePort']['value']; ?>, parseInt(CurrProfile), userName, userPW);
		<?php } else { ?>
			SISOPlugin.livePlay(location.hostname, <?php echo $classInstances['Information']->dataInfo['DevicePort']['value']; ?>, parseInt(CurrProfile), userName, userPW);
		<?php } ?>
		// DEV_S1WEBVIEWER end
		//SISOPlugin.setPTZExtension(1);
		SISOPlugin.setResolution(parseInt(resolWidth[CurrProfile]), parseInt(resolHeight[CurrProfile]));
		//document.getElementById('plugin').width = resolWidth[CurrProfile];
		//document.getElementById('plugin').height = resolHeight[CurrProfile];

		if((frameRateLimit[CurrProfile]/1000) <= 2)
			window.setTimeout('CheckResCode()', 7000);
		else if ((frameRateLimit[CurrProfile]/1000) <= 10)
			window.setTimeout('CheckResCode()', 5000);
		else
			window.setTimeout('CheckResCode()', 2000);

		if(userRightAudioIn == 1 && audioIn[CurrProfile] == 0)
		{
			$("#btnListenSpan").html("<img src='./images/common/btn/btn_sound_disable.png' alt='' />");
		}
		else if(userRightAudioIn == 1 && audioIn[CurrProfile] == 1)
		{
			$("#btnListenSpan").html("<a href='javascript:OnListenClick()' class='btn_type02a btn_type02_03' id='btnListen' ><img src='./images/common/btn/btn_sound.png' alt='' /></a>");
		}
	}

	function CheckResCode()
	{
	  var res = parseInt(SISOPlugin.getVNPResCode());

	  if(res != 0 && res >= 0) // == 4355 || a == 4110)
	  {
		isConnectFail = 1;
		SISOPlugin.stop();
		SISOPlugin.setResolution(1, 1);
		alert("<?php echo $msg_login_error[$GLOBALS['LANGINDEX']]; ?> (" + res + ")");
	  }
	  else if (res < 0)
	  {
		window.setTimeout('CheckResCode()', 1000);
		return;
	  }
	  else
	  {
		isConnectFail = 0;
	  }

	  $("#liveProfile").removeAttr('disabled');

	  if(userRightVideo == 0 || currentUserLevel == 3) // check again
		$('#liveProfile').attr('disabled', 'disabled');
	}

	function OnChangeProfile()
	{
	  	var CurrProfile;
  		CurrProfile = $('#liveProfile').val();

	  	DrawCurrentProfileInfo();

		if(isConnectFail == 1)
		{
			isConnectFail = 0;
			StartPlugin();
			GetIVOverlay();
			return;
		}
	  	SISOPlugin.changeProfile(parseInt(CurrProfile));

	  	if(FittStatus == 1){
	  		FittStatus = 0;
			OnFittClick();
	  	}
	  	else{
	  		if(OriginalStatus == 1){
				OriginalStatus = 0;
				OnOriginalClick();
	  		}
	  		else{
		  		SISOPlugin.setResolution(parseInt(resolWidth[CurrProfile]), parseInt(resolHeight[CurrProfile]));
				//document.getElementById('plugin').width = resolWidth[CurrProfile];
				//document.getElementById('plugin').height = resolHeight[CurrProfile];
			}
	  	}

		if((frameRateLimit[CurrProfile]/1000) <= 2)
			window.setTimeout('CheckResCode()', 7000);
		else if ((frameRateLimit[CurrProfile]/1000) <= 10)
			window.setTimeout('CheckResCode()', 5000);
		else
			window.setTimeout('CheckResCode()', 2000);

		$("#liveProfile").attr('disabled', 'disabled');

		if(BrowserDetect.browser == 'Safari') // defense code for wrong image display in Safari
		{
			window.scrollTo( 20, 0);
			window.scrollTo( 0, 0);
		}
		GetIVOverlay();

		if(userRightAudioIn == 1 && audioIn[CurrProfile] == 0)
		{
			$("#btnListenSpan").html("<img src='./images/common/btn/btn_sound_disable.png' alt='' />");
			SISOPlugin.stopAudio();
			ListenStatus = 0;
		}
		else if(userRightAudioIn == 1 && audioIn[CurrProfile] == 1)
		{
			$("#btnListenSpan").html("<a href='javascript:OnListenClick()' class='btn_type02a btn_type02_03' id='btnListen' ><img src='./images/common/btn/btn_sound.png' alt='' /></a>");
			if(ListenStatus == 0)
			{
				$('#btnListen').get(0).style.backgroundColor = '#656e83';
			}
			else
			{
				$('#btnListen').get(0).style.backgroundColor = '#0b76d5';
			}
		}
	}

	function OnSnapshotClick()
	{
		if(document.getElementById('plugin').width == 1 || document.getElementById('plugin').height == 1)
			return;

		var date = new Date();
		var defaultFilename = "<?php echo $_SERVER['MODELNAME']; ?>" + "_";
		defaultFilename += leadingZeros(date.getFullYear(), 4) + leadingZeros(date.getMonth() + 1, 2) + leadingZeros(date.getDate(), 2) + leadingZeros(date.getHours(), 2) + leadingZeros(date.getMinutes(), 2) + leadingZeros(date.getSeconds(), 2);

		SISOPlugin.saveSnapShotNoDialog(defaultFilename);
		//SISOPlugin.SaveSnapShot("11");

		$('#snapshotCompleted').get(0).style.display = "block";
		
		if (isShowing == 0) {
			setTimeout(function () {
				isShowing = 0;
				$('#snapshotCompleted').get(0).style.display = "none";
			}, 1000);
		}

		isShowing = 1;
	}

	function OnFittClick()
	{
		if(document.getElementById('plugin').width == 1 || document.getElementById('plugin').height == 1)
			return;

  		var CurrProfile;
 		CurrProfile = $('#liveProfile').val();

	  if(FittStatus == 0)
	  {
	    	SetViewportSize();
	    	var widthVal = parseInt(viewportWidth) - 345;
	    	var heightVal = parseInt(viewportHeight) - 135;
	    	var ratio = resolWidth[CurrProfile] / resolHeight[CurrProfile];
			var viewportRatio = widthVal / heightVal;

			viewportRatio = viewportRatio.toFixed(1);
			ratio = ratio.toFixed(1);

			if (isEnabledRotate > 0) {
				if(ratio == 0.6){				// 16:9
					if(viewportRatio < ratio)
						heightVal = (widthVal * 25 / 9) - widthVal;
					else
						widthVal = (heightVal * 25 / 16) - heightVal;

					if(widthVal < 180 || heightVal < 320)
					{
						widthVal = 180;
						heightVal = 320;
					}
				}
				else if(ratio == 0.8 && resolHeight[CurrProfile] != 1280 && resolWidth[CurrProfile] != 1024 && resolHeight[CurrProfile] != 720 && resolWidth[CurrProfile] != 576){		//4//4:3
					if(viewportRatio < ratio)
						heightVal = (widthVal * 7 / 3) - widthVal;
					else
						widthVal = (heightVal * 7 / 4) - heightVal;

					if(widthVal < 240 || heightVal < 320)
					{
						widthVal = 240;
						heightVal = 320;
					}
				}
				else{								//5:4
					if(viewportRatio < ratio)
						heightVal = (widthVal * 9 / 4) - widthVal;
					else
						widthVal = (heightVal * 9 / 5) - heightVal;

					if(widthVal < 320 || heightVal < 256)
					{
						widthVal = 320;
						heightVal = 256;
					}
				}
			}
			else
			{
				if(ratio == 1.8){				// 16:9
					if(viewportRatio < ratio)
						heightVal = (widthVal * 25 / 16) - widthVal;
					else
						widthVal = (heightVal * 25 / 9) - heightVal;

					if(widthVal < 320 || heightVal < 180)
					{
						widthVal = 320;
						heightVal = 180;
					}
				}
				else if(ratio == 1.3 && resolHeight[CurrProfile] != 1024 && resolHeight[CurrProfile] != 576){		//4//4:3
					if(viewportRatio < ratio)
						heightVal = (widthVal * 7 / 4) - widthVal;
					else
						widthVal = (heightVal * 7 / 3) - heightVal;

					if(widthVal < 320 || heightVal < 240)
					{
						widthVal = 320;
						heightVal = 240;
					}
				}
				else{								//5:4
					if(viewportRatio < ratio)
						heightVal = (widthVal * 9 / 5) - widthVal;
					else
						widthVal = (heightVal * 9 / 4) - heightVal;

					if(widthVal < 320 || heightVal < 256)
					{
						widthVal = 320;
						heightVal = 256;
					}
				}
			}

	    	SISOPlugin.setResolution(parseInt(widthVal), parseInt(heightVal));
		  	//document.getElementById('plugin').width = widthVal;
		  	//document.getElementById('plugin').height = heightVal;
		  	FittStatus = 1;
		  	OriginalStatus = 0;
		  	if(BrowserDetect.browser != 'Firefox')
	      {
		  	  //document.body.style.overflow = 'hidden';
		  	}
		}
		else
		{
		  	SISOPlugin.setResolution(parseInt(resolWidth[CurrProfile]), parseInt(resolHeight[CurrProfile]));
		  	//document.getElementById('plugin').width = resolWidth[CurrProfile];
		  	//document.getElementById('plugin').height = resolHeight[CurrProfile];
		  	FittStatus = 0;
		  	if(BrowserDetect.browser != 'Firefox')
	       {
		  	  //document.body.style.overflow = 'auto';
		  	}
		}
		GetIVOverlay();

		if(BrowserDetect.browser == 'Safari') // defense code for wrong image display in Safari
		{
			window.scrollTo( 20, 0);
			window.scrollTo( 0, 0);
		}
	}

	function AspectRatioOnFullScreen()
	{
  		var CurrProfile;
 		CurrProfile = $('#liveProfile').val();
    	var widthVal = parseInt(viewportWidth);
		var heightVal = parseInt(viewportHeight);
		var ratio = resolWidth[CurrProfile] / resolHeight[CurrProfile];
		var viewportRatio = widthVal / heightVal;

		viewportRatio = viewportRatio.toFixed(1);
		ratio = ratio.toFixed(1);

		if (isEnabledRotate > 0) {
			if(ratio == 0.6){				// 16:9
				if(viewportRatio < ratio)
					heightVal = (widthVal * 25 / 9) - widthVal;
				else
					widthVal = (heightVal * 25 / 16) - heightVal;

				if(widthVal < 180 || heightVal < 320)
				{
					widthVal = 180;
					heightVal = 320;
				}
			}
			else if(ratio == 0.8 && resolHeight[CurrProfile] != 1280 && resolWidth[CurrProfile] != 1024 && resolHeight[CurrProfile] != 720 && resolWidth[CurrProfile] != 576){		//4//4:3
				if(viewportRatio < ratio)
					heightVal = (widthVal * 7 / 3) - widthVal;
				else
					widthVal = (heightVal * 7 / 4) - heightVal;

				if(widthVal < 240 || heightVal < 320)
				{
					widthVal = 240;
					heightVal = 320;
				}
			}
			else{								//5:4
				if(viewportRatio < ratio)
					heightVal = (widthVal * 9 / 4) - widthVal;
				else
					widthVal = (heightVal * 9 / 5) - heightVal;

				if(widthVal < 320 || heightVal < 256)
				{
					widthVal = 320;
					heightVal = 256;
				}
			}
		}
		else
		{
			if (Math.abs(viewportRatio - ratio) > 0.2) {

				if(ratio == 1.8){				// 16:9
					if(viewportRatio < ratio)
						heightVal = (widthVal * 25 / 16) - widthVal;
					else
						widthVal = (heightVal * 25 / 9) - heightVal;

					if(widthVal < 320 || heightVal < 180)
					{
						widthVal = 320;
						heightVal = 180;
					}
				}
				else if(ratio == 1.3 && resolHeight[CurrProfile] != 1024 && resolHeight[CurrProfile] != 576){		//4//4:3
					if(viewportRatio < ratio)
						heightVal = (widthVal * 7 / 4) - widthVal;
					else
						widthVal = (heightVal * 7 / 3) - heightVal;

					if(widthVal < 320 || heightVal < 240)
					{
						widthVal = 320;
						heightVal = 240;
					}
				}
				else{								//5:4
					if(viewportRatio < ratio)
						heightVal = (widthVal * 9 / 5) - widthVal;
					else
						widthVal = (heightVal * 9 / 4) - heightVal;

					if(widthVal < 320 || heightVal < 256)
					{
						widthVal = 320;
						heightVal = 256;
					}
				}

			}
		}
		viewportWidth = parseInt(widthVal);
		viewportHeight = parseInt(heightVal);
	}


  var offset = $('#contents').offset();
  
	function DoChromeFullScreen()
	{
		if (!fullScreenApi.isFullScreen()) {
			var CurrProfile;
			CurrProfile = $('#liveProfile').val();
			SISOPlugin.setResolution(parseInt(resolWidth[CurrProfile]), parseInt(resolHeight[CurrProfile]));
			  //document.getElementById('plugin').width = resolWidth[CurrProfile];
			  //document.getElementById('plugin').height = resolHeight[CurrProfile];
			  document.getElementById('contents').style.padding = '20px';
			  GetIVOverlay();
			  FullScreenStatus = 0;
			  $("#IEoverlay").css("display", "none");
			  return;
		}
		SetViewportSize();
		AspectRatioOnFullScreen();
		SISOPlugin.setResolution(viewportWidth, viewportHeight);
		//document.getElementById('plugin').width = viewportWidth;
		 //document.getElementById('plugin').height = viewportHeight;
		 document.getElementById('contents').style.padding = '0px';
		 GetIVOverlay();
		 FullScreenStatus = 1;
		 $("#IEoverlay").css("display", "block");
	}

	function OnFullScreenClick()
	{
		if(FittStatus == 1)
			FittStatus = 0;

		if(document.getElementById('plugin').width == 1 || document.getElementById('plugin').height == 1)
			return;

		if(!(BrowserDetect.browser == "Explorer")) {
			window.scrollTo( 0, 0);
			if(FullScreenStatus == 0) {
				var element = $('#contents').get(0);

				if (fullScreenApi.supportsFullScreen) {
					fullScreenApi.requestFullScreen(element);
					element.addEventListener(fullScreenApi.fullScreenEventName, function() {
						if (fullScreenApi.isFullScreen()) {
							window.setTimeout('DoChromeFullScreen()', 500);
						} else {
							var CurrProfile;
							CurrProfile = $('#liveProfile').val();
							SISOPlugin.setResolution(parseInt(resolWidth[CurrProfile]), parseInt(resolHeight[CurrProfile]));
							  //document.getElementById('plugin').width = resolWidth[CurrProfile];
							  //document.getElementById('plugin').height = resolHeight[CurrProfile];
							  document.getElementById('contents').style.padding = '20px';
							  GetIVOverlay();
							  FullScreenStatus = 0;
							  $("#IEoverlay").css("display", "none");
						}
					}, true);
				}
  			}
  		}
  		else {
  			if(FullScreenStatus == 0) {
  				SISOPlugin.makeBrowserFullScreen(1);
  				FullScreenStatus = 1;

				$("body").css("overflow","hidden");
				document.body.scroll = 'no';
  				SetViewportSize();
				var screenWidth = viewportWidth;
				var screenHeight = viewportHeight;
				var widthDiff = 0;
				var heightDiff = 0;
				AspectRatioOnFullScreen();
				
				if(viewportWidth<=screenWidth)
					widthDiff = parseInt((screenWidth - viewportWidth) / 2);
				
  				$('#contents').offset({top:90, left:widthDiff});
  				document.getElementById('contents').style.padding = '0px';
  				$('#head').hide();
  				window.scrollTo( 0, 0);

				SISOPlugin.setResolution(viewportWidth, viewportHeight);
  				GetIVOverlay();
				$("#IEoverlay").css("display", "block");
  			}
		}
	}

	function OnOriginalClick()
	{
		if(document.getElementById('plugin').width == 1 || document.getElementById('plugin').height == 1)
			return;

	  var CurrProfile;
  	  CurrProfile = $('#liveProfile').val();

	  if(OriginalStatus == 0)
	  {
		  if (isEnabledRotate > 0) {
			  SISOPlugin.setResolution(480, 640);
		  }
		  else
		  {
			  SISOPlugin.setResolution(640, 480);
		  }
		  //document.getElementById('plugin').width = 640;
		  //document.getElementById('plugin').height = 480;
		  OriginalStatus = 1;
		  FittStatus = 0;
		}
		else
		{
		  SISOPlugin.setResolution(parseInt(resolWidth[CurrProfile]), parseInt(resolHeight[CurrProfile]));
		  //document.getElementById('plugin').width = resolWidth[CurrProfile];
		  //document.getElementById('plugin').height = resolHeight[CurrProfile];
		  OriginalStatus = 0;
		}
		GetIVOverlay();

		if(BrowserDetect.browser == 'Safari') // defense code for wrong image display in Safari
		{
			window.scrollTo( 20, 0);
			window.scrollTo( 0, 0);
		}
	}

	function OnTalkClick()
	{
	  if (audioTalkTimeoutValue == 1) return;

	  if(TalkStatus == 0)
	  {
	    SISOPlugin.startTalk();
	    TalkStatus = 1;
		$('#btnMic').get(0).style.backgroundColor = '#0b76d5';
	  }
	  else
	  {
	    SISOPlugin.stopTalk();
	    TalkStatus = 0;
		$('#btnMic').get(0).style.backgroundColor = '#656e83';
	  }

	  audioTalkTimeoutValue = 1;
	  window.setTimeout('ResetAudioTalkTimeoutValue()', 500);
	}

	function OnListenClick()
	{
	  if(ListenStatus == 0)
	  {
		<?php if($GLOBALS['M_ISP_TYPE'] != ISP_TYPE_WN3 && $GLOBALS['M_ISP_TYPE'] != ISP_TYPE_WN3_PTZ && $GLOBALS['M_ISP_TYPE'] != ISP_TYPE_HISILICON) { ?>
		SISOPlugin.enableLowAudioBuffer(); // only enabled in DM8127
		<?php } ?>
	    SISOPlugin.startAudio();
	    ListenStatus = 1;
		$('#btnListen').get(0).style.backgroundColor = '#0b76d5';
		//window.setTimeout('SISOPlugin.SetVolume(volumeVal)', 1000);
	  }
	  else
	  {
	    SISOPlugin.stopAudio();
	    ListenStatus = 0;
		$('#btnListen').get(0).style.backgroundColor = '#656e83';
	  }
	}

	function OnClickRelay(relayno)
	{
	  var  msg;
		var  command;

		if (relayStatus[relayno] == 1) {
			relayStatus[relayno] = 0;
			command = 0;
		}
		else if (relayStatus[relayno] == 0) {
			relayStatus[relayno] = 1;
			command = 1;
		}

		msg = "<SetRelayOutputState>";
		if(relayno == 0)
			msg += "<Token>"+"<?php echo $relayConf->relayOutputState[0]->dataInfo['Token']['value']; ?>"+"</Token>";
		else if(relayno == 1)
			msg += "<Token>"+"<?php echo $relayConf->relayOutputState[1]->dataInfo['Token']['value']; ?>"+"</Token>";
		else if(relayno == 2)
			msg += "<Token>"+"<?php echo $relayConf->relayOutputState[2]->dataInfo['Token']['value']; ?>"+"</Token>";
		else if(relayno == 3)
			msg += "<Token>"+"<?php echo $relayConf->relayOutputState[3]->dataInfo['Token']['value']; ?>"+"</Token>";
		msg += "<LogicalState>"+command+"</LogicalState>";
		msg += "</SetRelayOutputState>";

		RequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, 'NO_REFRESH');
		localSeq++;
	}

	function OnClickManualRecording()
	{
		var actionCmd = '';
		if(recordingEnable == 1) { 
			if (recordingStatus == 1) {					
				actionCmd = 'Stop';													
				recordingStatus = 0;
				<?php if($GLOBALS['M_SUPPORT_LOCAL_RECORDING']) { ?>
				SISOPlugin.stopLocalRecording();
				clearTimeout(localRecordingTimeout);
				<?php } ?>
			}
			else if (recordingStatus == 0) {	
				actionCmd = 'Start';					
				recordingStatus = 1;
				<?php if($GLOBALS['M_SUPPORT_LOCAL_RECORDING']) { ?>
				var date = new Date();
				var defaultFilename = "<?php echo $_SERVER['MODELNAME']; ?>" + "_";
				defaultFilename += leadingZeros(date.getFullYear(), 4) + leadingZeros(date.getMonth() + 1, 2) + leadingZeros(date.getDate(), 2) + leadingZeros(date.getHours(), 2) + leadingZeros(date.getMinutes(), 2) + leadingZeros(date.getSeconds(), 2);
				var res = SISOPlugin.startLocalRecording(defaultFilename);
				if (res == 0) {
					actionCmd = 'Stop';													
					recordingStatus = 0;
					return;
				} // Cancelled
				localRecordingTimeout = window.setTimeout('OnTimeoutLocalRecording()', 1000 * 60 * 5);
				<?php } ?>
			}		
			SISOPlugin.ptzControl.manualRecordingBtnColorChange(recordingStatus);
			<?php if($GLOBALS['M_SUPPORT_LOCAL_RECORDING']) { ?>
			// disable SD manual recording!!!
			<?php } else { ?>
			RequestAjaxMsg("<"+actionCmd+"ManualRecording/>", "", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, 'NO_REFRESH');
			localSeq++;
			<?php } ?>
		} 
		else {
			alert("<?php echo $msg_checkStorageStatus[$GLOBALS['LANGINDEX']]; ?>");
			return;
		}
	}

	function OnTimeoutLocalRecording()
	{
		var actionCmd = 'Stop';													
		recordingStatus = 0;
		SISOPlugin.stopLocalRecording();
		clearTimeout(localRecordingTimeout);
		SISOPlugin.ptzControl.manualRecordingBtnColorChange(recordingStatus);
	}

	function OnClickAux()
	{
		var msg = "";		
		auxStatus = (auxStatus ? 0 : 1);
		msg = "<SetPTZAuxiliary>";
		msg +="<Value>"+auxStatus+"</Value>";
		msg += "</SetPTZAuxiliary>";
		RequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, 'NO_REFRESH');
		localSeq++;
	}

	function OnClickTargetLockOn(posX, posY)
	{
		var msg = "";
		msg += "<StartTrackingTargetlock>";
		msg += "<Mode>1</Mode>";
		msg += "<PosX>"+posX+"</PosX>";
		msg += "<PosY>"+posY+"</PosY>";
		msg += "<AutoTrack>1</AutoTrack>";
		msg += "</StartTrackingTargetlock>";
		RequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, 'NO_REFRESH');
		localSeq++;
	}

	function SetLockOnPosX(val)
	{
		LockOnPosX = val;
	}
	
	function SetLockOnPosY(val)
	{
		LockOnPosY = val;
	}
	
	function DoLockOn()
	{
		OnClickTargetLockOn(LockOnPosX, LockOnPosY);
	}
	
  function SetViewportSize()
  {
  	if (typeof document.documentElement.clientWidth != 'undefined' && document.documentElement.clientWidth != 0 && typeof document.documentElement != 'undefined')
  	{
  		viewportWidth = document.documentElement.clientWidth;
  		viewportHeight = document.documentElement.clientHeight;
  	}

	else if (typeof window.innerWidth != 'undefined')
  	{
  		viewportWidth = window.innerWidth;
  		viewportHeight = window.innerHeight;
  	}

  	else
  	{
  		viewportWidth = document.getElementsByTagName('body')[0].clientWidth;
  		viewportHeight = document.getElementsByTagName('body')[0].clientHeight;
  	}
  }

  function GetIVOverlay()
{
<?php
	if(($GLOBALS['M_SUPPORT_EVENT_VA'] & IV_SUPPORT) && ($GLOBALS['M_SUPPORT_PTZ'] == PTZ_NOT_SUPPORT))
	{
?>
		<?php if($classInstances['VAConfiguration']->dataInfo['Mode']['value'] == 0){ ?>
			return;
		<?php } ?>

		var AXPosX1 = new Array();
		var AXPosY1 = new Array();
		var AXPosX2 = new Array();
		var AXPosY2 = new Array();
		var AXAreaPosX = new Array();
		var AXAreaPosY = new Array();
		var AXArrowDirection = new Array();
		var profileStatus = $('#liveProfile').val();
		
		SISOPlugin.doOverlay(0);
		SISOPlugin.doOverlay(1);

		var mirror = <?php echo $classInstances['Information']->dataInfo['Mirror']['value']; ?>;
		var flip = <?php echo $classInstances['Information']->dataInfo['Flip']['value']; ?>;

		var halfX = 640;
		var halfY = 512;
		var originalWidth = 1280;
		var originalHeight = 1024;
		<?php if($GLOBALS['M_MAX_RESOLUTION'] == MAX_3_MEGA && $GLOBALS['MEGAMODE'] == 3) { ?>
			halfX = 2048/2;
			halfY = 1536/2;
			originalWidth = 2048;
			originalHeight = 1536;
		<?php } ?>
		<?php if(($GLOBALS['M_MAX_RESOLUTION'] == MAX_3_MEGA &&  $GLOBALS['MEGAMODE'] == 2) || $GLOBALS['M_MAX_RESOLUTION'] == MAX_2_MEGA) { ?>
			halfX = 1920/2;
			halfY = 1080/2;
			originalWidth = 1920;
			originalHeight = 1080;
		<?php } ?>
		<?php if($GLOBALS['M_MAX_RESOLUTION'] == MAX_4CIF && $classInstances['Information']->dataInfo['VideoType']['value'] == 1) { ?>
			halfX = 704/2;
			halfY = 576/2;
			originalWidth = 704;
			originalHeight = 576;
		<?php } ?>
		<?php if($GLOBALS['M_MAX_RESOLUTION'] == MAX_4CIF && $classInstances['Information']->dataInfo['VideoType']['value'] == 0) { ?>
			halfX = 704/2;
			halfY = 480/2;
			originalWidth = 704;
			originalHeight = 480;
		<?php } ?>

		var offsetX, offsetY;
		var disRatio = 1;
		var is4to3 = 0;
		var cropRatioX = 1;
		var cropRatioY = 1;
		<?php if($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3) { ?>
		offsetX = 0;
		offsetY = 0;
		if (useCropEncoding[profileStatus] == 0)
		{
			<?php if(($GLOBALS['M_MAX_RESOLUTION'] == MAX_3_MEGA &&  $GLOBALS['MEGAMODE'] == 2) || $GLOBALS['M_MAX_RESOLUTION'] == MAX_2_MEGA) { ?>
			if (resolHeight[profileStatus] == 240 || resolHeight[profileStatus] == 480 || resolHeight[profileStatus] == 600
			|| resolHeight[profileStatus] == 768 || resolHeight[profileStatus] == 960)
			{
				originalWidth = 1440;
				offsetX = 240;
				is4to3 = 1;
			}
			else if (resolHeight[profileStatus] == 1024)
			{
				originalWidth = 1350;
				offsetX = 285;
				is4to3 = 1;
			}
			<?php } ?>

			<?php if($GLOBALS['M_MAX_RESOLUTION'] == MAX_3_MEGA && $GLOBALS['MEGAMODE'] == 3) { ?>
			if (resolHeight[profileStatus] == 180 || resolHeight[profileStatus] == 360 || resolHeight[profileStatus] == 450
			|| resolHeight[profileStatus] == 720 || resolHeight[profileStatus] == 1080)
			{
				originalHeight = 1152;
				offsetY = 192;
			}
			else if (resolHeight[profileStatus] == 1024)
			{
				originalWidth = 1920;
				offsetX = 64;
			}
			<?php } ?>

			<?php if($classInstances['Info']->videoInfo['DIS']['value'] == 1) { ?>
			disRatio = 1.2;
			offsetX = ((originalWidth - (originalWidth / disRatio)) / 2) + offsetX;
			offsetY = ((originalHeight - (originalHeight / disRatio)) / 2) + offsetY;
			<?php } ?>
		}

		if (useCropEncoding[profileStatus] > 0)
		{
			var cropOffsetX = cropX[profileStatus];
			var cropOffsetY = cropY[profileStatus];

			var X1 = cropOffsetX;
			var Y1 = cropOffsetY;
			var X2 = cropOffsetX + cropWidth[profileStatus];
			var Y2 = cropOffsetY + cropHeight[profileStatus];
			if (mirror)
			{
				if (X1 >= halfX)
					X1 = halfX - (X1 - halfX);
				else
					X1 = halfX + (halfX - X1);

				if (X2 >= halfX)
					X2 = halfX - (X2 - halfX);
				else
					X2 = halfX + (halfX - X2);
			}
			if (flip)
			{
				if (Y1 >= halfY)
					Y1 = halfY - (Y1 - halfY);
				else
					Y1 = halfY + (halfY - Y1);

				if (Y2 >= halfY)
					Y2 = halfY - (Y2 - halfY);
				else
					Y2 = halfY + (halfY - Y2);
			}

			if (mirror)
			{
				var tmp = X1;
				X1 = X2;
				X2 = tmp;
			}
			if (flip)
			{
				var tmp = Y1;
				Y1 = Y2;
				Y2 = tmp;
			}
			var width = X2 - X1;
			var height = Y2 - Y1;

			cropRatioX = originalWidth / width;
			cropRatioY = originalHeight / height;

			<?php if($classInstances['Info']->videoInfo['DIS']['value'] == 1) { ?>
			disRatio = 1.2;
			offsetX = ((originalWidth - (originalWidth / disRatio)) / 2) + (X1 / disRatio);
			offsetY = ((originalHeight - (originalHeight / disRatio)) / 2) + (Y1 / disRatio);
			<?php } else { ?>
			offsetX += X1;
			offsetY += Y1;
			<?php } ?>
		}

		<?php } ?>

		var viewerWidth = SISOPlugin.pluginObj.width;
		var viewerHeight = SISOPlugin.pluginObj.height;
		if(BrowserDetect.OS == 'Mac')
		{
			viewerWidth = parseInt(resolWidth[profileStatus]);
			viewerHeight = parseInt(resolHeight[profileStatus]);
		}

		<?php if ($GLOBALS['M_MAX_RESOLUTION'] == MAX_1_MEGA) { ?>
		if(resolHeight[profileStatus] == 720)
		{
			isWide = 1;
			originalHeight = 720;
		}
		else
		{
			isWide = 0;
		}
		<?php } ?>

		<?php if ($ivConf->dataInfo['Enabled']['value'] == 1 && $ivConf->dataInfo['Overlay']['value'] == 1)
		{
		?>
			var msg;
			<?php
				$vlinecount = 0;
				for ($index=0; $index<MAX_IV_OBJECT; ++$index) {
					if ($ivConf->objectRule[$index]->type == 1) $vlinecount++;
				}
			?>
			msg = "<IVLineObject count=\"" + <?php echo $vlinecount; ?> + "\">\r\n";
			<?php
				$vlineindex=0;
				for ($index=0; $index<MAX_IV_OBJECT; ++$index) {
					$pointcount = 0;
					if ($ivConf->objectRule[$index]->type == 1) //LINE
					{
						for ($j=0;$j<11;++$j)
						{
							if ($ivConf->objectRule[$index]->point[$j]->dataInfo['Valid']['value'] == true)
								$pointcount++;
						}
						?>
						msg += "<LineObject index=\"" + <?php echo $vlineindex;?> + "\">\r\n";
						msg += "<PointCount>" + <?php echo $pointcount;?> + "</PointCount>\r\n";
						msg += "<LineRule>" + <?php echo $ivConf->objectRule[$index]->dataInfo['LineRule']['value'];?> + "</LineRule>\r\n";
						AXArrowDirection[<?php echo $index;?>] = <?php echo $ivConf->objectRule[$index]->dataInfo['LineRule']['value'];?>;
						<?php
						for ($k=0;$k<$pointcount;++$k)
						{
							?>
							var posx = <?php echo $ivConf->objectRule[$index]->point[$k]->dataInfo['PosX']['value'];?>;
							var posy = <?php echo $ivConf->objectRule[$index]->point[$k]->dataInfo['PosY']['value'];?>;
							if (mirror)
	                        {
	                            if (posx >= halfX)
	                                posx = halfX - (posx - halfX);
	                            else
	                                posx = halfX + (halfX - posx);
	                        }
	                        if (flip)
	                        {
	                            if (posy >= halfY)
	                                posy = halfY - (posy - halfY);
	                            else
	                                posy = halfY + (halfY - posy);
	                        }
							msg += "<Point index =\"" +<?php echo $k; ?>+ "\">\r\n";
							msg += "<X>" + posx + "</X>\r\n";
							msg += "<Y>" + posy + "</Y>\r\n";

							<?php if ($k == 0) { ?>
								if(isWide == 0)
								{
									AXPosX1[<?php echo $index;?>] = (posx - offsetX) / ((originalWidth / viewerWidth) / (disRatio * cropRatioX));
									AXPosY1[<?php echo $index;?>] = (posy - offsetY) / ((originalHeight / viewerHeight) / (disRatio * cropRatioY));
								}
								else
								{
									AXPosX1[<?php echo $index;?>] = posx / ((originalWidth / viewerWidth) / (disRatio * cropRatioX));
									AXPosY1[<?php echo $index;?>] = (posy-152)/ ((originalHeight / viewerHeight) / (disRatio * cropRatioY));
								}
							<?php } else { ?>
								if(isWide == 0)
								{
									AXPosX2[<?php echo $index;?>] = (posx - offsetX)  / ((originalWidth / viewerWidth) / (disRatio * cropRatioX));
									AXPosY2[<?php echo $index;?>] = (posy - offsetY) / ((originalHeight / viewerHeight) / (disRatio * cropRatioY));
								}
								else
								{
									AXPosX2[<?php echo $index;?>] = posx / ((originalWidth / viewerWidth) / (disRatio * cropRatioX));
									AXPosY2[<?php echo $index;?>] = (posy-152) / ((originalHeight / viewerHeight) / (disRatio * cropRatioY));
								}
							<?php } ?>

							msg += "</Point>\r\n";
						<?php } ?>
						msg += "</LineObject>\r\n";
					<?php } ?>
				<?php
				$vlineindex++;
				} ?>
			msg += "</IVLineObject>\r\n";

			for(i=0;i<AXArrowDirection.length;i++)
			{
				var right, left;
				if(AXArrowDirection[i] == 0)
				{
					right = 1;
					left = 0;
				}
				else if (AXArrowDirection[i] == 1) {
					right = 0;
					left = 1;
				}
				else if (AXArrowDirection[i] == 2) {
					right = 1;
					left = 1;
				}

					if (AXPosX1[i] < 0)
					{
						var slope = (AXPosY2[i] - AXPosY1[i]) / (AXPosX2[i] - AXPosX1[i]);
						var modY = slope * (0 - AXPosX2[i]) + AXPosY2[i];
						AXPosX1[i] = 0;
						AXPosY1[i] = modY;
					}
					if (AXPosX2[i] < 0)
					{
						var slope = (AXPosY2[i] - AXPosY1[i]) / (AXPosX2[i] - AXPosX1[i]);
						var modY = slope * (0 - AXPosX1[i]) + AXPosY1[i];
						AXPosX2[i] = 0;
						AXPosY2[i] = modY;
					}

					if (AXPosY1[i] < 0)
					{
						var slope = (AXPosY2[i] - AXPosY1[i]) / (AXPosX2[i] - AXPosX1[i]);
						var modX = AXPosX2[i] - (AXPosY2[i] / slope);
						AXPosY1[i] = 0;
						AXPosX1[i] = modX;
					}
					if (AXPosY2[i] < 0)
					{
						var slope = (AXPosY2[i] - AXPosY1[i]) / (AXPosX2[i] - AXPosX1[i]);
						var modX = AXPosX1[i] - (AXPosY1[i] / slope);
						AXPosY2[i] = 0;
						AXPosX2[i] = modX;
					}

				if (mirror) {
					if(AXPosY1[i] > AXPosY2[i])
					{
						SISOPlugin.drawIVLine(parseInt(AXPosX1[i],10), parseInt(AXPosY1[i],10), parseInt(AXPosX2[i],10), parseInt(AXPosY2[i],10), right, left);
					}
					else
					{
						SISOPlugin.drawIVLine(parseInt(AXPosX1[i],10), parseInt(AXPosY1[i],10), parseInt(AXPosX2[i],10), parseInt(AXPosY2[i],10), left, right);
					}
				}
				else
				{
					if(AXPosY1[i] > AXPosY2[i])
					{
						SISOPlugin.drawIVLine(parseInt(AXPosX1[i],10), parseInt(AXPosY1[i],10), parseInt(AXPosX2[i],10), parseInt(AXPosY2[i],10), left, right);
					}
					else
					{
						SISOPlugin.drawIVLine(parseInt(AXPosX1[i],10), parseInt(AXPosY1[i],10), parseInt(AXPosX2[i],10), parseInt(AXPosY2[i],10), right, left);
					}
				}
			}

			//---------area-------------
			<?php
				$areacount = 0;
				$AXpointcount = 0;
				for ($index=0; $index<MAX_IV_OBJECT; ++$index) {
					if ($ivConf->objectRule[$index]->type == 2) $areacount++;
				}
			?>
			msg = "<IVAreaObject count=\"" + <?php echo $areacount; ?> + "\">\r\n";
			<?php
				$areaindex=0;
				for ($index=0; $index<MAX_IV_OBJECT; ++$index) {
					$pointcount = 0;
					if ($ivConf->objectRule[$index]->type == 2) //LINE
					{
						for ($j=0;$j<11;++$j)
						{
							if ($ivConf->objectRule[$index]->point[$j]->dataInfo['Valid']['value'] == true)
								$pointcount++;
						}
						?>
						msg += "<LineObject index=\"" + <?php echo $areaindex;?> + "\">\r\n";
						msg += "<PointCount>" + <?php echo $pointcount;?> + "</PointCount>\r\n";
						msg += "<AreaEnter>" + <?php echo $ivConf->objectRule[$index]->dataInfo['AreaEnter']['value'];?> + "</AreaEnter>\r\n";
						msg += "<AreaExit>" + <?php echo $ivConf->objectRule[$index]->dataInfo['AreaExit']['value'];?> + "</AreaExit>\r\n";
						msg += "<AreaAppear>" + <?php echo $ivConf->objectRule[$index]->dataInfo['AreaAppear']['value'];?> + "</AreaAppear>\r\n";
						msg += "<AreaDisappear>" + <?php echo $ivConf->objectRule[$index]->dataInfo['AreaDisappear']['value'];?> + "</AreaDisappear>\r\n";
						<?php
						for ($k=0;$k<$pointcount;++$k)
						{
							?>
							var posx = <?php echo $ivConf->objectRule[$index]->point[$k]->dataInfo['PosX']['value'];?>;
							var posy = <?php echo $ivConf->objectRule[$index]->point[$k]->dataInfo['PosY']['value'];?>;
							if (mirror)
	                        {
	                            if (posx >= halfX)
	                                posx = halfX - (posx - halfX);
	                            else
	                                posx = halfX + (halfX - posx);
	                        }
	                        if (flip)
	                        {
	                            if (posy >= halfY)
	                                posy = halfY - (posy - halfY);
	                            else
	                                posy = halfY + (halfY - posy);
	                        }
							msg += "<Point index =\"" +<?php echo $k ?>+ "\">\r\n";
							msg += "<X>" + posx + "</X>\r\n";
							msg += "<Y>" + posy + "</Y>\r\n";

							if(isWide == 0)
							{
								AXAreaPosX[<?php echo $AXpointcount;?>] = (posx - offsetX) / ((originalWidth / viewerWidth) / (disRatio * cropRatioX));
								AXAreaPosY[<?php echo $AXpointcount;?>] = (posy - offsetY) / ((originalHeight / viewerHeight) / (disRatio * cropRatioY));
							}
							else
							{
								AXAreaPosX[<?php echo $AXpointcount;?>] = posx / ((originalWidth / viewerWidth) / (disRatio * cropRatioX));
								AXAreaPosY[<?php echo $AXpointcount;?>] = (posy-152) / ((originalHeight / viewerHeight) / (disRatio * cropRatioY));
							}
							<?php $AXpointcount++;  ?>

							msg += "</Point>\r\n";
						<?php } ?>
						msg += "</LineObject>\r\n";
				<?php
						$areaindex++;
					}
				?>
			<?php

				}
			?>
			msg += "</IVAreaObject>\r\n";

			var j;

			for(i=0;i<(AXAreaPosX.length)/4;i++)
			{
				j = i*4;

				if (AXAreaPosX[j] < 0)
				{
					AXAreaPosX[j] = 0;
				}
				if (AXAreaPosX[j+1] < 0)
				{
					AXAreaPosX[j+1] = 0;
				}
				if (AXAreaPosX[j+2] < 0)
				{
					AXAreaPosX[j+2] = 0;
				}
				if (AXAreaPosX[j+3] < 0)
				{
					AXAreaPosX[j+3] = 0;
				}

				if (AXAreaPosY[j] < 0)
				{
					AXAreaPosY[j] = 0;
				}
				if (AXAreaPosY[j+1] < 0)
				{
					AXAreaPosY[j+1] = 0;
				}
				if (AXAreaPosY[j+2] < 0)
				{
					AXAreaPosY[j+2] = 0;
				}
				if (AXAreaPosY[j+3] < 0)
				{
					AXAreaPosY[j+3] = 0;
				}


				SISOPlugin.drawIVArea(parseInt(AXAreaPosX[j],10), parseInt(AXAreaPosY[j],10), parseInt(AXAreaPosX[j+1],10), parseInt(AXAreaPosY[j+1],10), parseInt(AXAreaPosX[j+2],10), parseInt(AXAreaPosY[j+2],10),parseInt(AXAreaPosX[j+3],10), parseInt(AXAreaPosY[j+3],10));
			}
<?php
		}
	}
?>
}

function ResetAudioTalkTimeoutValue()
{
	audioTalkTimeoutValue = 0;
}

function OnClickHomePosition()
{
	var msg = "";
	msg = "<StartPTZHomePosition>";
	msg += "<PanReal>100</PanReal>";
	msg += "<PanNorm>0</PanNorm>";
	msg += "</StartPTZHomePosition>";
	RequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, 'NO_REFRESH');
	localSeq++;
}


function OnClickSwing()
{
	var msg = "";
	msg += "<StartPTZSwing>";
	msg += "<Index>"+$("#SwingMode").val()+"</Index>";
	msg += "</StartPTZSwing>";
	RequestAjaxMsg(msg, '', "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, 'NO_REFRESH');
	localSeq++;
}

function OnClickGroup()
{
	var msg = "";
	msg += "<StartPTZGroup>";
	msg += "<Index>"+$("#ptzGroupNo").val()+"</Index>";
	msg += "</StartPTZGroup>";
	RequestAjaxMsg(msg, '', "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, 'NO_REFRESH');
	localSeq++;
}

function OnClickTour()
{
	RequestAjaxMsg("<StartPTZTour/>", '', "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, 'NO_REFRESH');
	localSeq++;
}

function OnClickTrace()
{
	var msg = "";
	msg += "<StartPTZTrace>";
	msg += "<Index>"+$("#ptzTraceNo").val()+"</Index>";
	msg += "<Mode>0</Mode>";
	msg += "</StartPTZTrace>";
	RequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, 'NO_REFRESH');
	localSeq++;
}

<?php if($GLOBALS['M_SUPPORT_EXTERNAL_PTZ']){ ?>	
function OnClickExternalPTZ(cmd){		//[cmd] : "stop":0, "up":1, "down":2, "left":3, "right":4, "upLeft":5, "upRight":6, "downLeft":7, "downRight":8, "zoomIn":9, "zoomOut":10, "near":11, "far":12
	var externSpeed = $("#externPtzSpeed").val();
	SISOPlugin.externalPtz.control(externSpeed,cmd);
}
<?php } ?>

function InitPresetList() {
	
//Preset list	
<?php
	for($index = 0; $index<$GLOBALS['M_PRESET_COUNT']; $index++) {
?> 
	selectPresetNum[<?php echo $index; ?>] = <?php echo trim($presetConf->preset[$index]['Index']['value']); ?>;
	selectPresetName[<?php echo $index; ?>] = '<?php echo trim($presetConf->preset[$index]['Name']['value']); ?>';
	
	presetCnt++;
<?php
	}
?> 	
} 

function DrawPresetList(mode, num, name) {
	if(mode == 1)	{
		selectPresetNum[num-1] = num;
		selectPresetName[num-1] = name;
	}

	var isEmpty = true;
	for(var index=1; index<=MAX_PRESET_CNT; index++) {		
		if(selectPresetName[index-1] != "") {
			$("#ptzPresetNo").append('<option value="'+index+'">'+index+':'+selectPresetName[index-1]+'</option>');			
			isEmpty = false;
		}
	}

	if(isEmpty) {
		$("#ptzPresetNo").append("<option value=0> --- </option>");
	}
	
	$("#ptzPresetNo option[value = "+selectPresetNum[num-1]+"]").attr('selected', true);
}

function GetPTZCookie()
{
	var presetStatus 			= GetCookie("PresetStatus");
	if (presetStatus != ""){
		$("#ptzPresetNo").val(presetStatus);
	}
}	

function SetPTZCookie(){
	SetCookie("PresetStatus", $("#ptzPresetNo").val());
}

function OnUnload()
{
	<?php if($GLOBALS['M_SUPPORT_LOCAL_RECORDING']) { ?>
	if (recordingStatus == 1) 
	{							
		SISOPlugin.stopLocalRecording();
		clearTimeout(localRecordingTimeout);
	}
	<?php } ?>
}

	</script>
</head>
<body onload="OnLoad()" onunload="OnUnload()" onselectstart="return false">
	<div id="IEoverlay"></div>
	<div id="wrap">
		<div id="head">
		<?php 
			if($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>
				<div class="head-top2">
				<h1><img src="./images/common/top_title_1.png" alt="S1" /></h1>
				<div class="logo"></div>
			<?php 
			} 
			else { ?>
			<div class="head-top">
				<h1><img src="./images/common/top_title.gif" alt="iPOLiS NETWORK CAMERA WEBVIEWER" /></h1>
				<div class="logo"><img src="./images/common/top_logo.gif" alt="SAMSUNG TECHWIN" /></div>
			<?php } ?>
			
			</div>
			<div class="gnb-tab">
				<ul style="margin-right:20px">
					<li class="selected">	<a href="./monitoring.cgi"><img src="./images/common/icon/icon_live.png" alt="live icon" class="fix" /><?php echo $GLOBALS['top_monitoring'][0]; ?></a></li>

			<?php
				if ((($GLOBALS['M_SUPPORT_SD'] || $GLOBALS['M_SUPPORT_NAS']) && $GLOBALS['USERINFO']['level'] == 0) && $GLOBALS['M_SPECIAL_TYPE'] != 1) {
			?>
					<li><a href="./setup/playback.cgi"><img src="./images/common/icon/icon_search.png" alt="search icon" class="fix" /><?php echo $GLOBALS['top_playback'][0]; ?></a></li>
			<?php
				} else {
			?>
					<li class="disable" style="color:gray;"><img src="./images/common/icon/icon_search.png" alt="search icon" class="fix" style="vertical-align:middle;"/><?php echo $GLOBALS['top_playback'][0]; ?></li>
			<?php
				}
			?>

			<?php
				if ($GLOBALS['USERINFO']['level'] == 0) {
			?>
					<li><a href="./setup/basic_videoprofile.cgi"><img src="./images/common/icon/icon_setup.png" alt="setup icon" class="fix" /><?php echo $GLOBALS['top_setup'][0]; ?></a></li>
			<?php
				} else {
			?>
					<li class="disable" style="color:gray;"><img src="./images/common/icon/icon_setup.png" alt="setup icon" class="fix" style="vertical-align:middle;" /> <?php echo $GLOBALS['top_setup'][0]; ?></li>
			<?php
				}
			?>

				</ul>
				<div>
					<div style="position:absolute; top:54px;left:430px;">
						<img src="./images/common/icon/user_icon.png">
					</div>
					<div style="position:absolute; top:58px;left:450px">					
					<h2>
			<?php
				// NO NEED to transrate, ONLY ENGLISH
				if 		($GLOBALS['USERINFO']['name'] == 'admin') echo 'ADMIN';
				else if 	($GLOBALS['USERINFO']['name'] == 'guest') echo 'GUEST';
				else																echo 'USER';
			?>
					</h2>
					</div>
					<div style="position:absolute; top:58px;left:510px">
						<img src="./images/common/PTZ/bar.png">
					</div>
					<div style="position:absolute; top:60px;left:520px">
					<?php
						if ($GLOBALS['USERINFO']['level'] == 0) {
					?>
						<img class="profileAccess" src="./images/common/icon/profileaccess.png" style="cursor:pointer" />
					<?php 
						} else {
					?>
						<img style="cursor:default;" src="./images/common/icon/profileaccess.png" />
					<?php 
						}
					?>
					</div>
					<div style="position:absolute; top:58px;left:545px;">
					<?php
						if ($GLOBALS['USERINFO']['level'] == 0) {
					?>
						<h2 class="profileAccess" style="cursor:pointer">Status</h2>					
					<?php
						} else {
					?>
						<h2 style="cursor:default;color:gray">Status</h2>										
					<?php
						}
					?>
					</div>
				</div>
			</div>
		</div>
		<div id="container">
			<div id="lnb2" style="display:none;">
				<div id="lnb-list-fold">
					<ul class="lnb-list-in2" style="display:none;">
						<li><a href="javascript:openlnbMenu(1)"><img src="./images/live/lnb_m01_off.gif" alt="profile" /></a></li>
						<li><a href="javascript:openlnbMenu(2)"><img src="./images/live/lnb_m02_off.gif" alt="view" /></a></li>
						<?php if (($GLOBALS['M_SUPPORT_PTZ'] || $GLOBALS['M_SUPPORT_EXTERNAL_PTZ']) && $GLOBALS['USERINFO']['level'] == 0) { ?> 		
							<li><a href="javascript:openlnbMenu(3)"><img src="./images/live/lnb_m03_off.gif" alt="PTZ" /></a></li>
						<?php } else if (($GLOBALS['M_SUPPORT_PTZ'] || $GLOBALS['M_SUPPORT_EXTERNAL_PTZ']) && $GLOBALS['USERINFO']['ptz'] == 1) { ?>
							<li><a href="javascript:openlnbMenu(3)"><img src="./images/live/lnb_m03_off.gif" alt="PTZ" /></a></li>
						<?php	} ?>
					</ul>
					<ul class="lnb-list-in2">
						<li><a href="javascript:openlnbMenu(1)"><img src="./images/live/lnb_m01_s.gif" alt="profile" /></a></li>
						<li><a href="javascript:openlnbMenu(2)"><img src="./images/live/lnb_m02_s.gif" alt="view" /></a></li>
						<?php if (($GLOBALS['M_SUPPORT_PTZ'] || $GLOBALS['M_SUPPORT_EXTERNAL_PTZ']) && $GLOBALS['USERINFO']['level'] == 0) { ?> 		
							<li><a href="javascript:openlnbMenu(3)"><img src="./images/live/lnb_m03_s.gif" alt="PTZ" /></a></li>
						<?php } else if (($GLOBALS['M_SUPPORT_PTZ'] || $GLOBALS['M_SUPPORT_EXTERNAL_PTZ']) && $GLOBALS['USERINFO']['ptz'] == 1) { ?>
							<li><a href="javascript:openlnbMenu(3)"><img src="./images/live/lnb_m03_s.gif" alt="PTZ" /></a></li>
						<?php } ?>
					</ul>
					<div class="lnb-open">
						<a href="#"><img src="./images/common/btn/btn_lnb_arrow02.gif" alt="lnb_arrow" /></a>
					</div>
				</div>
			</div>
			<div id="lnb">
				<div id="lnb-list">
					<ul class="lnb-list-in">
						<li id="lnb01">
							<a href="#"><img src="./images/live/lnb_m01_on.gif" alt="profile" /></a>
							
							<div class="hidden_box lnb_box">
								<select name="profile" id="liveProfile" class="selectbox_style_wid260" style="margin-left:10px" onchange="OnChangeProfile();">
								</select>
								<div class="profile-cont">
									<ul>
										<li>
											<em><?php echo $t_codec[$GLOBALS['LANGINDEX']]; ?></em> : <span id="liveProfileCodec"></span>
										</li>
										<li>
											<em><?php echo $t_name[$GLOBALS['LANGINDEX']]; ?></em> : <span id="liveProfileName"></span>
										</li>
										<li>
											<em><?php echo $t_resolution[$GLOBALS['LANGINDEX']]; ?></em> : <span id="liveProfileResol"></span>
										</li>
										<li>
											<em><?php echo $t_framerate[$GLOBALS['LANGINDEX']]; ?></em> : <span id="liveProfileFramerate"></span>
										</li>
										<?php if ($GLOBALS['M_SUPPORT_COMPRESSION']) { ?> 
										<li>
											<em><?php echo $t_compression[$GLOBALS['LANGINDEX']]; ?></em> : <span id="liveProfileCompression"></span>
										</li>
										<?php } ?>
										<li>
											<em><span id="liveProfileBitrateText"></span></em> : <span id="liveProfileBitrate"></span>
										</li>
									</ul>
								</div>
							</div>						
						</li>
					
						<li id="lnb02">
							<a href="#"><img src="./images/live/lnb_m02_off.gif" alt="view" /></a>
							<div class="hidden_box live-view" style="margin-bottom:-15px; padding-left:12px;">
								<div class="btn-view01">
						<?php 
						if($GLOBALS['M_SPECIAL_TYPE'] != 1) { ?>
							<div id="snapshotCompleted" style="position:absolute; width:270px; height:150px; left: 10px; top: 140px; background-color:#000000; display:none; z-index:1000">
								<p align="center">
									<br /> <br /> 
									<?php echo $msg_capturedImageFile[$GLOBALS['LANGINDEX']]; ?>
									<br />
									<script>
										var msg = "C:\\Users\\{Current User}\\Pictures\\";
										if (BrowserDetect.OS == 'Mac') {
											msg = "~/Pictures/";
										}
										document.write(msg);
									</script>
									
								</p>
							</div>

						<?php } ?>
						
							<div id="instantRecordStarted" style="position:absolute; width:270px; height:150px; left: 10px; top: 140px; background-color:#000000; display:none; z-index:1000">
								<p align="center">
									<br /> <br /> 
									<?php echo $msg_instantRecordStarted[$GLOBALS['LANGINDEX']]; ?>
									<br />
									<script>
										var msg = "C:\\Users\\{Current User}\\Videos\\";
										if (BrowserDetect.OS == 'Mac') {
											msg = "~/Movies/";
										}
										document.write(msg);
									</script>
									
								</p>
							</div>
				<?php 
				if($GLOBALS['M_SPECIAL_TYPE'] != 1) { ?>
                        	<img id="btnCapture" src="./images/common/VIEW/capture_normal.png" class="mgr2" 
                        		onclick="javascript:OnSnapshotClick()"
                        		onMouseOver="ChangeImage('btnCapture','./images/common/VIEW/capture_press.png');"
                        		onMouseOut="ChangeImage('btnCapture','./images/common/VIEW/capture_normal.png');"
                        		title="<?php echo $t_capture[$GLOBALS['LANGINDEX']]; ?>"/>
								<span id="btnManualRecordingSpan">
                 		<?php if(($GLOBALS['USERINFO']['level'] == 0 && ($GLOBALS['M_SUPPORT_SD'] || $GLOBALS['M_SUPPORT_NAS'])) || $GLOBALS['M_SUPPORT_LOCAL_RECORDING']) { ?>
									<img id="btnManualRecording" src="./images/common/VIEW/rec_normal.png" class="mgr2"
										onclick="javascript:OnClickManualRecording();"
										<?php if($GLOBALS['M_SUPPORT_LOCAL_RECORDING']) { ?>
										title="<?php echo $t_instantRecording[$GLOBALS['LANGINDEX']]; ?>"/>
										<?php } else { ?>
										title="<?php echo $t_manualRecording[$GLOBALS['LANGINDEX']]; ?>"/>
										<?php } ?>
								<?php } else { ?>
									<img id="btnManualRecording" src="./images/common/VIEW/rec_disable.png" title="<?php echo $t_manualRecording[$GLOBALS['LANGINDEX']]; ?>" style="cursor:default;" class="mgr2" />
                     <?php } ?>
								</span>
				<?php } ?>
								
                     <?php	if (GetBrowserName() == 'IE' || GetBrowserName() == 'Google Chrome') { ?>
                        	<img id="btnFullScreen" src="./images/common/VIEW/full_normal.png" class="mgr2"
                        		onclick="javascript:OnFullScreenClick()"
                        		onMouseOver="ChangeImage('btnFullScreen','./images/common/VIEW/full_press.png');"
                        		onMouseOut="ChangeImage('btnFullScreen','./images/common/VIEW/full_normal.png');"
                        		title="<?php echo $t_fullScreen[$GLOBALS['LANGINDEX']]; ?>"/>
                     <?php } else { ?>
                     		<img id="btnFullScreen" src="./images/common/VIEW/full_disable.png" class="mgr2" title="<?php echo $t_fullScreen[$GLOBALS['LANGINDEX']]; ?>" style="cursor:default"/>
                     <?php	} ?>
                        	<img id="btnOriginal" src="./images/common/VIEW/original_normal.png" class="mgr2"
                        		onclick="javascript:OnOriginalClick()"
                        		onMouseOver="ChangeImage('btnOriginal','./images/common/VIEW/original_press.png');"
                        		onMouseOut="ChangeImage('btnOriginal','./images/common/VIEW/original_normal.png');"
                        		title="1:1"/>
                        	<img id="btnFit" src="./images/common/VIEW/fit_normal.png" class="mgr2"
                        		onclick="javascript:OnFittClick()"
                        		onMouseOver="ChangeImage('btnFit','./images/common/VIEW/fit_press.png');"
                        		onMouseOut="ChangeImage('btnFit','./images/common/VIEW/fit_normal.png');"
                        		title="<?php echo $t_fit[$GLOBALS['LANGINDEX']]; ?>"/>
								</div>								
								<?php if($GLOBALS['M_SUPPORT_AUDIO']) { ?>
								
								<div style="margin-top:10px;"><h2 style="margin-left:0px;"><?php echo $t_audio[$GLOBALS['LANGINDEX']]; ?></h2></div>
								<div class="volume">
									<table style="width:255px">
										<colgroup>
											<col style="width:40px;"/>
											<col style="width:180px;"/>
											<?php if($GLOBALS['M_SUPPORT_AUDIO_OUT'] != 0) { ?>
											<col style="width:40px;"/>
											<?php } ?>
										</colgroup>
										<tr>
											<td>
												<span id="btnListenSpan">
												<?php if($GLOBALS['USERINFO']['audioin'] == 0 || $GLOBALS['USERINFO']['level'] == 3 || $GLOBALS['M_SUPPORT_AUDIO'] == 0) { ?>
												<img src="./images/common/btn/btn_sound_disable.png" alt="" />
												<?php } else { ?>
												<a href="javascript:OnListenClick()" class="btn_type02a btn_type02_03" id="btnListen" ><img src="./images/common/btn/btn_sound.png" alt="" /></a>
												<?php } ?>
												</span>
											</td>
											<td valign="center" style="height: 26px;">
												<?php if($GLOBALS['USERINFO']['audioin'] == 0 || $GLOBALS['USERINFO']['level'] == 3 || $GLOBALS['M_SUPPORT_AUDIO'] == 0) { ?>
												<div id="slider-vol-disable" style="width:160px; margin-left:8px; margin-top:-7px" ></div>
												<?php } else { ?>
												<div id="slider-vol" style="width:160px; margin-left:8px; margin-top:-7px" ></div>												
												<?php } ?>
											</td>
											<?php if($GLOBALS['M_SUPPORT_AUDIO_OUT'] != 0) { ?>
											<td align="right">
												<?php if($GLOBALS['USERINFO']['audioout'] == 0 || $GLOBALS['USERINFO']['level'] == 3 || $GLOBALS['M_SUPPORT_AUDIO'] == 0 || $classInstances['Information']->dataInfo['AudioOutputEnable']['value'] == 0 || $GLOBALS['M_SUPPORT_AUDIO_OUT'] == 0) { ?>
												<img src="./images/common/btn/btn_mike_disable.png" alt="" />
												<?php } else { ?>
												<a href="javascript:OnTalkClick()" class="btn_type02a btn_type02_02" id="btnMic"><img src="./images/common/btn/btn_mike.png" alt="" /></a>
												<?php } ?>
											</td>
											<?php } ?>
										</tr>
									</table>									
								</div>
								<?php if($GLOBALS['M_SUPPORT_AUDIO_OUT'] != 0) { ?>
								<div style="margin-top:-38px;">
									<span style="margin-left:45px;">-</span>
									<span style="margin-left:142px;">+</span>
								</div>
								<?php } else { ?>
								<div style="margin-top:-38px;">
									<span style="margin-left:55px;">-</span>
									<span style="margin-left:142px;">+</span>
								</div>
								<?php } ?>							
								<?php } ?>
								<?php if($GLOBALS['M_ALARMOUT_COUNT'] > 0) { ?>
								<div class="btn-view01" style="margin-top:40px">
									<h2 style="margin-left:0px"><?php echo $t_alarmOutput[$GLOBALS['LANGINDEX']]; ?><?php if($GLOBALS['M_AUX_COUNT'] > 0) { ?> / AUX <?php } ?></h2>
									<a id="btnRelay1" class="btn_type01_05_disable mgr3">1</a>
								<?php if($GLOBALS['M_ALARMOUT_COUNT'] > 1) { ?>
									<a id="btnRelay2" class="btn_type01_05_disable mgr3">2</a>
								<?php } ?>
								<?php if($GLOBALS['M_AUX_COUNT'] > 0) { ?>
									<a id="btnAux" class="btn_type01_05_disable btn_type01_05" style="margin-left:10px;">AUX</a>
									<div>
										<img src="./images/common/PTZ/bar.png" style="margin-top:7px; margin-left:-65px"/>
									</div>
								<?php } ?>									
								</div>
								<?php } ?>
								<script>
								<?php for ($index=1; $index <= $GLOBALS['M_ALARMOUT_COUNT']; $index++) { ?>
									<?php if(!($GLOBALS['USERINFO']['relay'] == 0 || $GLOBALS['USERINFO']['level'] == 3)) { ?>
										$("#btnRelay<?php echo $index;?>").attr('class','btn_type01 btn_type01_05 mgr3');
										$("#btnRelay<?php echo $index;?>").attr('href','javascript:OnClickRelay(<?php echo $index-1;?>)');
									<?php } ?>
									<?php if(!($GLOBALS['USERINFO']['relay'] == 0 || $GLOBALS['USERINFO']['level'] == 3) && $GLOBALS['M_AUX_COUNT'] > 0) { ?>
										$("#btnAux").attr('class','btn_type01 btn_type01_05');
										$("#btnAux").attr('href','javascript:OnClickAux()');
									<?php }?>
								<?php }?>
								</script>
								<br /><br />
							</div>
						</li>
						<?php if (($GLOBALS['M_SUPPORT_PTZ']) && $GLOBALS['USERINFO']['ptz'] == 1) { ?>
						<li id="lnb03">
							<a href="#"><img src="./images/live/lnb_m03_off.gif" alt="PTZ" /></a>
							
							<div id="PTZArea" class="hidden_box" style="width:240px;height:148px;position:relative; margin-left:auto; margin-right:auto; top:20px;" >
								<div id="MOVEArea" style="height:138px; width:190px; background: url(./images/common/PTZ/ptcontrol_bg.png); background-repeat: no-repeat; position:relative; left:4px; margin-left:auto; margin-right:auto;z-index:1; ">
									
								</div>
								<div style="position:absolute;top:57px;left:112px; z-index:100">
									<img id="Move-Btn" src="./images/common/PTZ/jog.png" />
								</div>
					<!-- Sequence --> 							
								<div class="profile-cont" style="width:260px;position:absolute;top:160px;left:-8px;">
									<h2 class="ptztitle"><?php echo $t_sequence[$GLOBALS['LANGINDEX']]; ?></h2>
									<div id="sequence-tabs" style="margin-bottom:10px; width:255px; height:80px">
										<ul>
											<li class="sequence-tabs" id="preset-Btn" style="border:0; top:0; width:51px; height:30px;">
												<a style="padding:0; width:51px; height:30px" href="#tabs-preset" title="<?php echo $t_preset[$GLOBALS['LANGINDEX']]; ?>"><img class="ptzbtn" src="./images/common/PTZ/preset.png"/></a>
											</li>
											<li class="sequence-tabs" id="swing-Btn" style="border:0; top:0; width:51px; height:30px;">
												<a style="padding:0; width:51px; height:30px" href="#tabs-swing" title="<?php echo $t_swing[$GLOBALS['LANGINDEX']]; ?>"><img class="ptzbtn" src="./images/common/PTZ/swing.png"/></a>
											</li>
											<li class="sequence-tabs" id="group-Btn" style="border:0; top:0; width:51px; height:30px;">
												<a style="padding:0; width:51px; height:30px" href="#tabs-group" title="<?php echo $t_group[$GLOBALS['LANGINDEX']]; ?>"><img class="ptzbtn" src="./images/common/PTZ/group.png"/></a>
											</li>
											<li class="sequence-tabs" id="tour-Btn" style="border:0; top:0; width:51px; height:30px;">
												<a style="padding:0; width:51px; height:30px" href="#tabs-tour" title="<?php echo $t_tour[$GLOBALS['LANGINDEX']]; ?>"><img class="ptzbtn" src="./images/common/PTZ/tour.png"/></a>
											</li>
											<li class="sequence-tabs" id="trace-Btn" style="border:0; top:0; width:51px; height:30px;">
												<a style="padding:0; width:51px; height:30px" href="#tabs-trace" title="<?php echo $t_trace[$GLOBALS['LANGINDEX']]; ?>"><img class="ptzbtn" src="./images/common/PTZ/trace.png"/></a>
											</li>
										</ul> 					
										<div id="tabs-preset" style="height:120px">
											<table class="data_write mgl-15" style="width:240px; position:<?php if (GetBrowserName()=='Mozilla Firefox') {echo 'absolute';} ?>; top:<?php if (GetBrowserName()=='Mozilla Firefox') {echo '30';} ?>px;">
												<colgroup>
												</colgroup>											
												<tbody>
												<tr>
													<td style="padding-bottom:0px; padding-left:2px;float:left"><?php echo $t_selectPreset[$GLOBALS['LANGINDEX']]; ?></td>
												</tr>
												<tr>
													<td style="padding-left:2px;float:left">
														<select id="ptzPresetNo" class="selectbox_style_wid240">															
														</select>
													</td>
												</tr>
												<tr>
													<td>
													<img id="btnPresetStart" src="./images/common/PTZ/go_normal.png" class="sequence_btn" style="left:6px" 
														onclick="javascript:SISOPlugin.ptzControl.onClickPresetMove();SetPTZCookie();"
														onMouseOver="ChangeImage('btnPresetStart','./images/common/PTZ/go_press.png');"
														onMouseOut="ChangeImage('btnPresetStart','./images/common/PTZ/go_normal.png');"
														title="<?php echo $t_start[$GLOBALS['LANGINDEX']]; ?>"/>
													<img id="btnHomeStart" src="./images/common/PTZ/home_normal.png" class="sequence_btn" style="left:60px"
														onclick="javascript:OnClickHomePosition();"
														onMouseOver="ChangeImage('btnHomeStart','./images/common/PTZ/home_press.png');"
														onMouseOut="ChangeImage('btnHomeStart','./images/common/PTZ/home_normal.png');"
														title="<?php echo $t_goHomePosition[$GLOBALS['LANGINDEX']]; ?>"/>													
													<img id="savePreset_btn" src="./images/common/PTZ/savepreset_normal.png" class="sequence_btn" style="left:198px"
														onclick="OnClickSavePreset();"
														onMouseOver="ChangeImage('savePreset_btn','./images/common/PTZ/savepreset_press.png');"
														onMouseOut="ChangeImage('savePreset_btn','./images/common/PTZ/savepreset_normal.png');"
														title="<?php echo $t_setPreset[$GLOBALS['LANGINDEX']]; ?>"/>
													<?php
														require_once('./setup/ptz_presetdialog.cgi');
													?>
													</td>
												</tr>
												</tbody>
											</table>
										</div>
										<div id="tabs-swing" style="height:120px">
											<table class="data_write mgl-15" style="width:230px; position:<?php if (GetBrowserName()=='Mozilla Firefox') {echo 'absolute';} ?>; top:<?php if (GetBrowserName()=='Mozilla Firefox') {echo '30';} ?>px;">	
												<tr>
													<td style="padding-bottom:0px; padding-left:2px;"><?php echo $t_selectMode[$GLOBALS['LANGINDEX']]; ?></td>
												</tr>
												<tr>
													<td style="padding-left:2px;">
														<select id="SwingMode" class="selectbox_style_wid240">
															<option value="0"><?php echo $t_pan[$GLOBALS['LANGINDEX']]; ?></option>
															<option value="1"><?php echo $t_tilt[$GLOBALS['LANGINDEX']]; ?></option>
															<option value="2"><?php echo $t_pantilt[$GLOBALS['LANGINDEX']]; ?></option>
														</select>
													</td>
												</tr>
												<tr>
													<td>
														<img id="swing-start" src="./images/common/PTZ/go_normal.png" class="sequence_btn" style="left:6px"
															onclick="javascript:OnClickSwing();"
															onMouseOver="ChangeImage('swing-start','./images/common/PTZ/go_press.png');"
															onMouseOut="ChangeImage('swing-start','./images/common/PTZ/go_normal.png');"
															title="<?php echo $t_start[$GLOBALS['LANGINDEX']]; ?>"/>
														<img id="swing-stop" src="./images/common/PTZ/stop_normal.png" class="sequence_btn" style="left:60px;" 
															onclick="javascript:SISOPlugin.ptzControl.onClickPtzStop('sequence');"
															onMouseOver="ChangeImage('swing-stop','./images/common/PTZ/stop_press.png');"
															onMouseOut="ChangeImage('swing-stop','./images/common/PTZ/stop_normal.png');"
															title="<?php echo $t_stop[$GLOBALS['LANGINDEX']]; ?>"/>
													</td>
												</tr>
											</table>
										</div>
										<div id="tabs-group" style="height:120px">
											<table class="data_write mgl-15" style="width:230px;position:<?php if (GetBrowserName()=='Mozilla Firefox') {echo 'absolute';} ?>; top:<?php if (GetBrowserName()=='Mozilla Firefox') {echo '30';} ?>px;">
												<tr>
													<td style="padding-bottom:0px; padding-left:2px;"><?php echo $t_selectGroup[$GLOBALS['LANGINDEX']]; ?></td>
												</tr>
												<tr>
													<td style="padding-left:2px;">
														<select id="ptzGroupNo" class="selectbox_style_wid240">
														<?php for($index=1; $index <= $GLOBALS['M_GROUP_IN_TOUR_COUNT']; $index++){ ?>
															<option value= <?php echo $index; ?> > <?php echo $index; ?> </option>
														<?php } ?>
														</select>
													</td>
												</tr>
												<tr>
													<td>
														<img id="group-start" src="./images/common/PTZ/go_normal.png" class="sequence_btn" style="left:6px;" 
															onclick="javascript:OnClickGroup();"
															onMouseOver="ChangeImage('group-start','./images/common/PTZ/go_press.png');"
															onMouseOut="ChangeImage('group-start','./images/common/PTZ/go_normal.png');"
															title="<?php echo $t_start[$GLOBALS['LANGINDEX']]; ?>"/>
														<img id="group-stop" src="./images/common/PTZ/stop_normal.png" class="sequence_btn" style="left:60px;" 
															onclick="javascript:SISOPlugin.ptzControl.onClickPtzStop('sequence');"
															onMouseOver="ChangeImage('group-stop','./images/common/PTZ/stop_press.png');"
															onMouseOut="ChangeImage('group-stop','./images/common/PTZ/stop_normal.png');"
															title="<?php echo $t_stop[$GLOBALS['LANGINDEX']]; ?>"/>
													</td>
												</tr>
											</table>
										</div>
										<div id="tabs-tour" style="height:120px">
											<table class="data_write mgl-15" style="width:230px; position:<?php if (GetBrowserName()=='Mozilla Firefox') {echo 'absolute';} ?>; top:<?php if (GetBrowserName()=='Mozilla Firefox') {echo '30';} ?>px;">
												<tr>
													<td style="padding-bottom:0px; padding-left:2px;"><?php echo $t_selectTour[$GLOBALS['LANGINDEX']]; ?></td>
												</tr>
												<tr>
													<td style="padding-left:2px;">
														<select id="ptzTourNo" class="selectbox_style_wid240">
															<option value="0">1</option>
														</select>
													</td>
												</tr>
												<tr>
													<td>
														<img id="tour-start" src="./images/common/PTZ/go_normal.png" class="sequence_btn" style="left:6px;" 
															onclick="javascript:OnClickTour();"
															onMouseOver="ChangeImage('tour-start','./images/common/PTZ/go_press.png');"
															onMouseOut="ChangeImage('tour-start','./images/common/PTZ/go_normal.png');"
															title="<?php echo $t_start[$GLOBALS['LANGINDEX']]; ?>"/>
														<img id="tour-stop" src="./images/common/PTZ/stop_normal.png" class="sequence_btn" style="left:60px;" 
															onclick="javascript:SISOPlugin.ptzControl.onClickPtzStop('sequence');"
															onMouseOver="ChangeImage('tour-stop','./images/common/PTZ/stop_press.png');"
															onMouseOut="ChangeImage('tour-stop','./images/common/PTZ/stop_normal.png');"
															title="<?php echo $t_stop[$GLOBALS['LANGINDEX']]; ?>"/>
													</td>
												</tr>
											</table>
										</div>
										<div id="tabs-trace" style="height:120px">
											<table class="data_write mgl-15" style="width:250px;position:<?php if (GetBrowserName()=='Mozilla Firefox') {echo 'absolute';} ?>; top:<?php if (GetBrowserName()=='Mozilla Firefox') {echo '30';} ?>px;">
												<tr>
													<td style="padding-bottom:0px; padding-left:2px;"><?php echo $t_selectTrace[$GLOBALS['LANGINDEX']]; ?></td>
												</tr>
												<tr>
													<td style="padding-left:2px;">
														<select id="ptzTraceNo" class="selectbox_style_wid240">
															<option value="1">1</option>
															<option value="2">2</option>
															<option value="3">3</option>
															<option value="4">4</option>
														</select>
													</td>
												</tr>
												<tr>
													<td>
														<img id="trace-start" src="./images/common/PTZ/go_normal.png" class="sequence_btn" style="left:6px;" 
															onclick="javascript:OnClickTrace();"
															onMouseOver="ChangeImage('trace-start','./images/common/PTZ/go_press.png');"
															onMouseOut="ChangeImage('trace-start','./images/common/PTZ/go_normal.png');"
															title="<?php echo $t_start[$GLOBALS['LANGINDEX']]; ?>"/>
														<img id="trace-stop" src="./images/common/PTZ/stop_normal.png" class="sequence_btn" style="left:60px;" 
															onclick="javascript:SISOPlugin.ptzControl.onClickPtzStop('sequence');"
															onMouseOver="ChangeImage('trace-stop','./images/common/PTZ/stop_press.png');"
															onMouseOut="ChangeImage('trace-stop','./images/common/PTZ/stop_normal.png');"
															title="<?php echo $t_stop[$GLOBALS['LANGINDEX']]; ?>"/>
													</td>
												</tr>
											</table>
										</div>
									</div>
								</div>

                  <!-- AREA ZOOM -->
                        <div style="position:absolute;top:320px;left:-8px;width:260px;cursor:pointer;">
                        	<h2 class="ptztitle"><?php echo $t_areaZoom[$GLOBALS['LANGINDEX']]; ?></h2>
										<a class="btn_type01" style="width:61px; height:30px" href="javascript:SISOPlugin.ptzControl.btnPtzAreazoomActive();" title="<?php echo $t_areaZoom[$GLOBALS['LANGINDEX']]; ?>">
											<img class="areabtn" src="./images/common/PTZ/areazoom.png"/>
										</a>
										<a class="btn_type01" style="width:61px; height:30px; position:absolute; left:64px; top:22px;" href="javascript:SISOPlugin.ptzControl.btnPtzAreazoomGoto1x();" title="<?php echo $t_goto1x[$GLOBALS['LANGINDEX']]; ?>">
											<img style="margin-top:3px" src="./images/common/PTZ/1x.png"/>
										</a>
										<a class="btn_type01" style="width:61px; height:30px; position:absolute; left:128px; top:22px;" href="javascript:SISOPlugin.ptzControl.btnPtzAreazoomPreview();" title="<?php echo $t_prev[$GLOBALS['LANGINDEX']]; ?>">
											<img style="margin-top:3px" src="./images/common/PTZ/prev.png"/>
										</a>									
										<a class="btn_type01" style="width:61px; height:30px; position:absolute; left:192px; top:22px;" href="javascript:SISOPlugin.ptzControl.btnPtzAreazoomForward();" title="<?php echo $t_next[$GLOBALS['LANGINDEX']]; ?>">
											<img style="margin-top:3px" src="./images/common/PTZ/next.png"/>
										</a>
								</div>
						<?php 
							if ($GLOBALS['M_SUPPORT_PTZ_TRACKING']) {
						?>
						<!-- AUTO TRACKING -->		
								<div style="position:absolute;top:380px;left:-8px;cursor:pointer;">
									<h2 class="ptztitle"><?php echo $t_autoTracking[$GLOBALS['LANGINDEX']]; ?></h2>						
										<a class="btn_type01" style="width:61px; height:30px" href="javascript:OnClickAutoTracking('1');" title="<?php echo $t_autotracking_on[$GLOBALS['LANGINDEX']]; ?>">
											<img class="areabtn" src="./images/common/PTZ/autotracking_on.png"/>
										</a>
										<a class="btn_type01" style="width:61px; height:30px; position:absolute; left:64px; top:22px;" href="javascript:OnClickAutoTracking('0');" title="<?php echo $t_autotracking_off[$GLOBALS['LANGINDEX']]; ?>">
											<img style="margin-top:3px" src="./images/common/PTZ/autotracking_off.png"/>
										</a>
                        </div>
						<?php
							}
						?>
                 <!-- FOCUS -->
                 			<div style="position:absolute;top:0px;left:-8px;cursor:pointer">
                 				<img id="btnAutoFocus" src="./images/common/PTZ/AF_normal.png"
                        		onclick="javascript:OnClickAutoFocus()"
                        		onMouseOver="ChangeImage('btnAutoFocus','./images/common/PTZ/AF_press.png');"
                        		onMouseOut="ChangeImage('btnAutoFocus','./images/common/PTZ/AF_normal.png');"
                        		title="<?php echo $t_autoFocus[$GLOBALS['LANGINDEX']]; ?>"/>
                 			</div>
                        <div style="position:absolute;top:70px;left:-8px;cursor:pointer">
									<img id="Near-Btn" src="./images/common/PTZ/near_normal.png"
										onMouseOver="ChangeImage('Near-Btn','./images/common/PTZ/near_press.png');"
										onMouseOut="SISOPlugin.ptzControl.onClickPtzStop(); ChangeImage('Near-Btn','./images/common/PTZ/near_normal.png');"
										onMouseDown="SISOPlugin.ptzControl.onClickFocus('Near');"
										onMouseUp = "SISOPlugin.ptzControl.onClickPtzStop();"
										title="<?php echo $t_near[$GLOBALS['LANGINDEX']]; ?>" />
                         </div>
                        <div style="position:absolute;top:108px;left:-8px;cursor:pointer">
                        	<img id="Far-Btn" src="./images/common/PTZ/far_normal.png"
                           	onMouseOver="ChangeImage('Far-Btn','./images/common/PTZ/far_press.png');"
                           	onMouseOut="SISOPlugin.ptzControl.onClickPtzStop(); ChangeImage('Far-Btn','./images/common/PTZ/far_normal.png');"
                           	onMouseDown="SISOPlugin.ptzControl.onClickFocus('Far');"
                           	onMouseUp = "SISOPlugin.ptzControl.onClickPtzStop();"
                           	title="<?php echo $t_far[$GLOBALS['LANGINDEX']]; ?>" />
                        </div>

                <!-- ZOOM -->
                        <div style="position:absolute;top:118px;left:226px;cursor:pointer">
									<img id="Minus-Btn" src="./images/common/PTZ/zoomout_normal.png"
										onMouseOver="ChangeImage('Minus-Btn','./images/common/PTZ/zoomout_press.png');"
										onMouseOut="SISOPlugin.ptzControl.onClickPtzStop(); ChangeImage('Minus-Btn','./images/common/PTZ/zoomout_normal.png');"
										onMouseDown="SISOPlugin.ptzControl.onClickZoom('Out', 'btn');"
										onMouseUp="SISOPlugin.ptzControl.onClickPtzStop();"
										title="<?php echo $t_zoomOut[$GLOBALS['LANGINDEX']]; ?>" />
									<img id="Minus-Btn-Disable" src="./images/common/PTZ/zoomout_normal.png" style="display:none; cursor:default;"/>
                        </div>
                        <div style="position:absolute;top:0px;left:226px;cursor:pointer">
									<img id="Plus-Btn" src="./images/common/PTZ/zoomin_normal.png"
										 onMouseOver="ChangeImage('Plus-Btn','./images/common/PTZ/zoomin_press.png');"
										 onMouseOut="SISOPlugin.ptzControl.onClickPtzStop(); ChangeImage('Plus-Btn','./images/common/PTZ/zoomin_normal.png');"
										 onMouseDown="SISOPlugin.ptzControl.onClickZoom('In', 'btn');"
										 onMouseUp = "SISOPlugin.ptzControl.onClickPtzStop();"
										 title="<?php echo $t_zoomIn[$GLOBALS['LANGINDEX']]; ?>" />
									<img id="Plus-Btn-Disable" src="./images/common/PTZ/zoomin_normal.png" style="display:none; cursor:default;"/>
                        </div>
                        
						<!-- SPEED -->
                        <div id="ptzSpeed" style="position:absolute;top:28px;left:234px;height:85px;"></div>
						<?php 
							if ($GLOBALS['M_SUPPORT_PTZ_TRACKING']) {
						?>
                        <div style="width:250px; position:absolute; left:-20px; top:450px; padding:15px; background:url(./images/common/PTZ/autotracking_bg.png); font-size:11px">
                        	<?php echo $msg_lockon_info[$GLOBALS['LANGINDEX']]; ?>
                        </div>
                  <?php
                  	}
                  ?>
							</div>
						</li>
						<?php }else if($GLOBALS['M_SUPPORT_EXTERNAL_PTZ'] && $GLOBALS['USERINFO']['ptz'] == 1) {?>						
						<li id="lnb03">
							<a href="#"><img src="./images/live/lnb_m03_off.gif" alt="PTZ" /></a>
							<div id="PTZArea" class="hidden_box" style="position:relative; background-repeat: no-repeat; margin-left:auto; margin-right:auto; top:20px;">
								<div id="MOVEArea" style="background: url(./images/common/ExternalPtz/BOX_bg.png); width:128px;height:128px; position:absolute;top:0px;left:70px;"></div>
								<div style="width:50px;position:absolute;top:-8px;left:107px;">
									<img id="Top-Btn" src="./images/common/ExternalPtz/top.png" usemap="#top" />
									<map name="top"
										onMouseOut="ChangeImage('Top-Btn','./images/common/ExternalPtz/top.png');OnClickExternalPTZ(0);"
										onMouseover="ChangeImage('Top-Btn','./images/common/ExternalPtz/top_press.png');"
										onDragstart=""
										onMouseDown="OnClickExternalPTZ(1);ChangeImage('Top-Btn','./images/common/ExternalPtz/top_press.png');"
										onMouseUp = "OnClickExternalPTZ(0);">
										<area shape="poly" coords="0,13 , 60,13, 52,42, 8,42 " />
									</map>
								</div>
								<div style="width:50px;position:absolute;top:4px;left:72px;">
									<img id="TopLeft-Btn" src="./images/common/ExternalPtz/top_left.png" usemap="#top_left" />
									<map name="top_left"
										onMouseOut="ChangeImage('TopLeft-Btn','./images/common/ExternalPtz/top_left.png');OnClickExternalPTZ(0);"
										onMouseover="ChangeImage('TopLeft-Btn','./images/common/ExternalPtz/top_left_press.png');"
										onDragstart=""
										onMouseDown="OnClickExternalPTZ(5);ChangeImage('TopLeft-Btn','./images/common/ExternalPtz/top_left_press.png');"
										onMouseUp = "OnClickExternalPTZ(0);">
										<area shape="poly" coords="2,40, 40,2, 52,25, 25,52" />
									</map>
								</div>
								<div style="width:50px;position:absolute;top:4px;left:144px;">
									<img id="TopRight-Btn" src="./images/common/ExternalPtz/top_right.png" usemap="#top_right" />
									<map name="top_right"
										onMouseOut="ChangeImage('TopRight-Btn','./images/common/ExternalPtz/top_right.png');OnClickExternalPTZ(0);"
										onMouseover="ChangeImage('TopRight-Btn','./images/common/ExternalPtz/top_right_press.png');"
										onDragstart=""
										onMouseDown="OnClickExternalPTZ(6);ChangeImage('TopRight-Btn','./images/common/ExternalPtz/top_right_press.png');"
										onMouseUp = "OnClickExternalPTZ(0);">
										<area shape="poly" coords="5,28, 17,3, 57,43, 32,55" />
									</map>
								</div>
								<div style="width:50px;position:absolute;top:39px;left:61px;">
									<img id="Left-Btn" src="./images/common/ExternalPtz/left.png" usemap="#left" />
									<map name="left"
										onMouseOut="ChangeImage('Left-Btn','./images/common/ExternalPtz/left.png');OnClickExternalPTZ(0);"
										onMouseover="ChangeImage('Left-Btn','./images/common/ExternalPtz/left_press.png');"
										onDragstart=""
										onMouseDown="OnClickExternalPTZ(3);ChangeImage('Left-Btn','./images/common/ExternalPtz/left_press.png');"
										onMouseUp = "OnClickExternalPTZ(0);" >
										<area shape="poly" coords="13,1, 40,12, 40,48, 13,59" />
									</map>
								</div>
								<div style="width:50px;position:absolute;top:40px;left:154px;">
									<img id="Right-Btn" src="./images/common/ExternalPtz/right.png" usemap="#right" />
									<map name="right"
										onMouseOut="ChangeImage('Right-Btn','./images/common/ExternalPtz/right.png');OnClickExternalPTZ(0);"
										onMouseover="ChangeImage('Right-Btn','./images/common/ExternalPtz/right_press.png');"
										onDragstart=""
										onMouseDown="OnClickExternalPTZ(4);ChangeImage('Right-Btn','./images/common/ExternalPtz/right_press.png');"
										onMouseUp = "OnClickExternalPTZ(0);">
										<area shape="poly" coords="15,12, 44,0, 44,59, 15,48" />
									</map>
								</div>
								<div style="width:50px;position:absolute;top:75px;left:73px;">
									<img id="DownLeft-Btn" src="./images/common/ExternalPtz/bottom_left.png" usemap="#down_left" />
									<map name="down_left"
										onMouseOut="ChangeImage('DownLeft-Btn','./images/common/ExternalPtz/bottom_left.png');OnClickExternalPTZ(0);"
										onMouseover="ChangeImage('DownLeft-Btn','./images/common/ExternalPtz/bottom_left_press.png');"
										onDragstart=""
										onMouseDown="OnClickExternalPTZ(7);ChangeImage('DownLeft-Btn','./images/common/ExternalPtz/bottom_left_press.png');"
										onMouseUp = "OnClickExternalPTZ(0);">
										<area shape="poly" coords="1,17, 26,7, 52,33, 41,58" />
									</map>
								</div>
								<div style="width:50px;position:absolute;top:75px;left:141px;">
									<img id="DownRight-Btn" src="./images/common/ExternalPtz/bottom_right.png" usemap="#down_right" />
									<map name="down_right"
										onMouseOut="ChangeImage('DownRight-Btn','./images/common/ExternalPtz/bottom_right.png');OnClickExternalPTZ(0);"
										onMouseover="ChangeImage('DownRight-Btn','./images/common/ExternalPtz/bottom_right_press.png');"
										onDragstart=""
										onMouseDown="OnClickExternalPTZ(8);ChangeImage('DownRight-Btn','./images/common/ExternalPtz/bottom_right_press.png');"
										onMouseUp = "OnClickExternalPTZ(0);">
										<area shape="poly" coords="7,30, 34,4, 59,16, 18,57" />
									</map>
								</div>
								<div style="width:50px;position:absolute;top:87px;left:107px;">
									<img id="Down-Btn" src="./images/common/ExternalPtz/bottom.png" usemap="#down" />
									<map name="down"
										onMouseOut="ChangeImage('Down-Btn','./images/common/ExternalPtz/bottom.png');OnClickExternalPTZ(0);"
										onMouseover="ChangeImage('Down-Btn','./images/common/ExternalPtz/bottom_press.png');"
										onDragstart=""
										onMouseDown="OnClickExternalPTZ(2);ChangeImage('Down-Btn','./images/common/ExternalPtz/bottom_press.png');"
										onMouseUp = "OnClickExternalPTZ(0);">
										<area shape="poly" coords="12,18, 47,18, 59,47, 0,47" />
									</map>
								</div>
								<div style="position:absolute;top:61px;left:15px;">
									<img id="Near-Btn" src="./images/common/PTZ/near_normal.png"
										onMouseOver="ChangeImage('Near-Btn','./images/common/PTZ/near_press.png');"
										onMouseOut="OnClickExternalPTZ(0); ChangeImage('Near-Btn','./images/common/PTZ/near_normal.png');"
										onMouseDown="OnClickExternalPTZ(11);" 
										onMouseUp = "OnClickExternalPTZ(0);" 
										title="<?php echo $t_near[$GLOBALS['LANGINDEX']]; ?>" />
								 </div>
								<div style="position:absolute;top:95px;left:15px;">
									<img id="Far-Btn" src="./images/common/PTZ/far_normal.png"
										onMouseOver="ChangeImage('Far-Btn','./images/common/PTZ/far_press.png');"
										onMouseOut="OnClickExternalPTZ(0); ChangeImage('Far-Btn','./images/common/PTZ/far_normal.png');" 
										onMouseDown="OnClickExternalPTZ(12);" 
										onMouseUp = "OnClickExternalPTZ(0);" 
										title="<?php echo $t_far[$GLOBALS['LANGINDEX']]; ?>" />
								</div>
								<div style="width:30px;position:absolute;top:37px;left:221px;">
									<img id="Minus-Btn" src="./images/common/ExternalPtz/zoom_in_normal.png"
										onMouseOver="ChangeImage('Minus-Btn','./images/common/ExternalPtz/zoom_in_press.png');"						
										onMouseOut="OnClickExternalPTZ(0);ChangeImage('Minus-Btn','./images/common/ExternalPtz/zoom_in_normal.png');"
										onMouseDown="OnClickExternalPTZ(10);"
										onMouseUp = "OnClickExternalPTZ(0);"
										title="<?php echo $t_zoomOut[$GLOBALS['LANGINDEX']]; ?>" />
								</div>
								<div style="width:30px;position:absolute;top:71px;left:221px;">
									<img id="Plus-Btn" src="./images/common/ExternalPtz/zoom_out_normal.png"
										onMouseOver="ChangeImage('Plus-Btn','./images/common/ExternalPtz/zoom_out_press.png');"
										onMouseOut="OnClickExternalPTZ(0);ChangeImage('Plus-Btn','./images/common/ExternalPtz/zoom_out_normal.png');"
										onMouseDown="OnClickExternalPTZ(9);"
										onMouseUp = "OnClickExternalPTZ(0);"
										title="<?php echo $t_zoomIn[$GLOBALS['LANGINDEX']]; ?>" />
								</div>
								<div style="width:40px;position:absolute;top:105px;left:221px;">
									<select id="externPtzSpeed" class="selectbox_style" style="width:40px;">
										<option value=1>1</option>
										<option value=2>2</option>
										<option value=3>3</option>
										<option value=4>4</option>
										<option value=5>5</option>
										<option value=6 selected="selected">6</option>
									</select>
								</div>					
							</div>
						</li>							
						<?php } ?>
					</ul>
					<div class="lnb-btn">
						<a href="#"><img src="./images/common/btn/btn_lnb_arrow.gif" alt="lnb_arrow" /></a>
					</div>
				</div>
			</div>
			<div id="contents" >
				<div class="ficture">
				  <span id="pluginArea"></span>
				</div>
			</div>
			<script type="text/javascript">
				var containerWidth = screen.width + 1000;
				if (containerWidth < 3000)
					containerWidth = 3000;
				document.getElementById('container').style.width = containerWidth + 'px';
			</script>
		</div>
	</div>
</body>
</html>

<style>
	.ui-dialog.scheduleTable {
		left: 10px !important;
		top: -660px !important;
	}
</style>
