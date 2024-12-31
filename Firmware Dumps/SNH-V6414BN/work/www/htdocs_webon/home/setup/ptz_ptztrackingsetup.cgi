<?php
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_menu.cgi');
require_once ('../language/language_av_ptztracking.cgi');

$classInstances	= GetClassInstance('ptztracking');
$presetConf 		= $classInstances['PTZPreset'];
$trackingpreset 	= $classInstances['TrackingPreset'];
$trackingMask    	= $classInstances['PrivacyMask'];
$event_name 		= 'ptztracking';

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
	<link rel="stylesheet" type="text/css" href="../css/jquery.ui.dialog.css"/>
	<link rel="stylesheet" type="text/css" href="../css/jquery.ui.theme.css"/>	
	<link rel="stylesheet" type="text/css" href="../css/jquery.ui.slider.css"/>
	<style>
		#lnb-list {
			height:950px;
		}
		.ui-tooltip { padding-top:2px; padding-bottom:2px; padding-left:5px; padding-right:5px; width:auto; position:absolute; z-index:9999; background: #ffffff; color: black; }
		.ui-dialog{
			background: #EFF1F3;
			position: absolute !important;
			width: 300px;
			//opacity: 0.5;
			//-ms-filter: "progid:DXImageTransform.Microsoft.Alpha(Opacity=50)"; /* IE 8 */
			display: block;
			z-index:1000;
		}
		.ui-dialog .ui-widget-header {
			background: #E4E7EA;
			color: #000;
			font-weight: bold;
			font-size: 11px;
			border: none;
			height: 20px;
			padding-left: 10px;
		}
		.ui-dialog .ui-dialog-titlebar-close{
			background: none;
			border: none;
		}
		.ui-dialog .ui-widget-content {background: #EFF1F3;
			border: none;
			margin-left: 0px;
			margin-top: 5px;
		}
		.ui-dialog .ui-dialog-buttonset button{ background: #EFF1F3; margin: 0 10px;}
		.ui-dialog .ui-dialog-buttonpane{ border: none;	/*padding: 20px 0*/}
		.ui-dialog .ui-resizable-handle{ display: none !important;}
		.ui-widget-overlay{
			background: none repeat scroll 0 0 #000000;
			opacity: 0;   
			filter:alpha(opacity=0);
			width: <?php echo $GLOBALS['VIEWER_RESOLUTION']['width']+40; ?>px;
			height: <?php echo $GLOBALS['VIEWER_RESOLUTION']['height']+20; ?>px;
			position: absolute;
			z-index: 1000;
		}
		.ui-dialog .ui-widget-content p{ display:block;clear: both;}
		.ui-dialog .ui-widget-content input,.ui-dialog .ui-widget-content label{float:left;margin-left:5px;color:#000;}
		.ui-dialog-titlebar-close .ui-button-text{display:none;}
		.ui-dialog-titlebar-close{ float:right; }
		.ui-dialog .ui-dialog-titlebar-close span.ui-button-text { display:none; }
		.ui-button.ui-state-default { color:#000;}
		
		#AreaList{
			background: none repeat scroll 0 0 #858ea1;
    		clear: right;
    		height: 138px;
    		overflow-y: auto;
    		width: 200px;
			margin-top:20px;
			margin-left:10px;
		}
		
		ul#AreaNames{
			list-style: none outside none;
    		margin: 0;
    		padding: 0;
    		text-align: left;
		}
		ul#AreaNames li a{
			color: #000000;
    		display: block;
    		padding: 2px 5px;
			text-decoration: none;
			font-size:11px;
			border:1px solid #858ea1;
 		}
		ul#AreaNames li a.selArea {
			background:#B1D1DE;
			border:1px solid #6DBDD1;
		}
		ul#AreaNames li a:hover{
			background:#98AABB;
			border:1px solid #98AABB;
		}
		.DisableAreaList{
			position:absolute;
			left:10px;
			top:20px;
			width:240px;
			height:180px;
			opacity:0;filter:alpha(opacity=0);
			background:gray;
		}
		#poly-dialog{
			min-height: 0px !important;
		}
		#poly-dialog p{
			height:30px;
		}#poly-dialog p label{
			line-height:20px;
			height:20px;
		}#poly-dialog p input,#poly-dialog p select{
			margin-left:10px;background:#fff;border:1px solid #EEE;
			width:140px;
		}
		#DeleteArea{
			background: none repeat scroll 0 0 #1B2029;
			//border: 1px solid #1B2029;
			color: #FFFFFF;
			display: inline-block;
			font-weight: bold;
		/*	height: 25px;
			margin-left: 29px;
			margin-top: 8px;
			padding-top: 0;
			text-align: center;
			vertical-align: middle;
			float:right; */
		}
	</style>
	<script type="text/javascript" src="../js/jquery-1.9.1.js"></script>
	<script type="text/javascript" src="../js/jquery-ui.js"></script>
	<script type="text/javascript" src="../js/lnb.js"></script>
	<script type="text/javascript" src="../js/common_function.js"></script>
	<script type="text/javascript" src="../js/jquery.ui.dialog.js"></script>
	<script type="text/javascript" src="../js/pluginCheck.js"></script>
	<script type="text/javascript" src="../js/pluginControl.js"></script>
	<!--[if lt IE 9]><script type="text/javascript" src="../js/excanvas.js"></script><![endif]-->	
	<script type="text/javascript" src="../js/tracking_setup.js"></script>
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
	var maxResolution			= {width: <?php echo $GLOBALS['MAX_RESOLUTION']['width'] ?>, height: <?php echo $GLOBALS['MAX_RESOLUTION']['height'] ?>};

	var MAX_PRESET_CNT 		= <?php echo MAX_PTZ_PRESET255; ?>;
	var PRESETENABLE			= new Array();

	var buttonLang 			= ["<?php echo $t_ok[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $t_cancel[$GLOBALS['LANGINDEX']]; ?>"];
	var title					= "<?php echo $t_add[$GLOBALS['LANGINDEX']]; ?>";	
	var nameCheck	 			= "<?php echo $msg_validName[$GLOBALS['LANGINDEX']]; ?>";
	var isOnload				= false;
	
	$(document).ready(function(){
		lnbonoff("lnb_ptz");
				
		$("#camera_height").slider({
			orientation: "horizontal",
			min: 250,
			max: 3000,
			value: <?php echo $trackingpreset->dataInfo['CameraHeight']['value']; ?>,
			range: "min",
			step:10,
			slide: function( event, ui ) {
				var val1 = parseInt(ui.value)/100;
				if (ui.value%100 == 0)
					val1 = val1+".0";
				$("#camera_height_value").html(val1+" m");
			}
		});
		var val1 = $("#camera_height").slider("value")/100;
		if ($("#camera_height").slider("value")%100 == 0)
			val1 = val1+".0";
		$("#camera_height_value").html(val1+" m");

		
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

	$(document).mouseup(function() {		
		if(firstDrawClick && isDrawDragging){
			$("#imgTemp").trigger("mouseup");
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

		$("#DisableVideoSetup").css("display","block");
		window.setTimeout(function(){
			isOnload = true;
			ReqTrackingMaskArea();
		},1000);
		
	}

	function OnClickSlider(name,cmd)
	{
		var id = "#" + name;
		var value = $(id).slider( "option", "value" );
		var maxVal =  $(id).slider( "option", "max" );
		var minVal = $(id).slider( "option", "min" );

		if(cmd == "left"){
			value -= 10;
		}
		else {
			value += 10;
		}

		if(value >= minVal && value <= maxVal){
			$(id).slider("option", "value", value);
			var val1 = parseInt($(id).slider("option", "value"))/100;
			if ($(id).slider("option", "value")%100 == 0)
				val1 = val1+".0";
			$(id + "_value").html(val1+" m");
		}
	}

	function OnClickTrackingZoom()
	{
		if ($('#zoom_enable').is(':checked') == 1) {
			$('#small').removeAttr('disabled');
			$('#medium').removeAttr('disabled');
			$('#large').removeAttr('disabled');
		}
		else {
			$('#small').attr('disabled', 'disabled');
			$('#medium').attr('disabled', 'disabled');
			$('#large').attr('disabled', 'disabled');
		}
	}

	function OnClickApply()
	{
		var msg ="";
		msg +="<SetTrackingPreset>";
		msg +="<CameraHeight>"+ ($("#camera_height").slider("option","value")) +"</CameraHeight>";
		msg +="<ZoomControl>"+($("#zoom_enable").is(':checked') ? 1 : 0) +"</ZoomControl>";
		var sizeVal = ($('#small').is(':checked') ? 1 : ($('#medium').is(':checked') ? 2 : 3));
		msg +="<ObjectSize>"+ sizeVal +"</ObjectSize>";
		msg +="<Indicator>"+ ($("#indicator_display_enable").is(':checked') ? 1 : 0) +"</Indicator>";
		msg +="<AreaActivation>"+($("#area_activation_enable").is(':checked') ? 1 : 0) +"</AreaActivation>";
		msg +="<AutoMode>"+ ($("#automode_lostend").is(':checked') ? 1 : 0) +"</AutoMode>";
		msg +="</SetTrackingPreset>";
		RequestAjaxMsg(msg, "<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq);
	}


	function ApplyMaskPolygon(msg,isTest)
	{
	  	var reqUrl = "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq;
	  	if (BrowserDetect.browser == "Explorer" || (BrowserDetect.browser == 'Safari' && reqUrl.search('.local') != -1)) {
	  		reqUrl = "../.."+reqUrl.substr(reqUrl.indexOf("/cgi"));
	  	}
		$("#DisableVideoSetup").css("display","block");
		$("#polyDraw").css("display","none");
		
	  	$.ajax({
	  		type: "POST",
	  		data: encodeURIComponent(msg),
	  		async: true,
	  		cache: false,
	  		url: reqUrl,
	  		dataType: "text",
	  		success: function(req){
	  			if(isTest){
					OnSuccessTest(req,isTest);
	  			}
	  			else{
					OnSuccessMask(req);
	  			}
	  		},
	  		error: null
	  	});
	}
  
	function ApplyDelete(msg)
	{
	  	var reqUrl = "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq;
	  	if (BrowserDetect.browser == "Explorer" || (BrowserDetect.browser == 'Safari' && reqUrl.search('.local') != -1)) {
	  		reqUrl = "../.."+reqUrl.substr(reqUrl.indexOf("/cgi"));
	  	}
		$("#DisableVideoSetup").css("display","block");
		$("#polyDraw").css("display","none");
		
	  	$.ajax({
	  		type: "POST",
	  		data: encodeURIComponent(msg),
	  		async: true,
	  		cache: false,
	  		url: reqUrl,
	  		dataType: "text",
	  		success: OnSuccessMask,
	  		error: function(){
				ReqTrackingMaskArea();
			}
	  	});
	}

	function ApplyMove(msg)
  	{
	  	var reqUrl = "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq;
	  	if (BrowserDetect.browser == "Explorer" || (BrowserDetect.browser == 'Safari' && reqUrl.search('.local') != -1)) {
	  		reqUrl = "../.."+reqUrl.substr(reqUrl.indexOf("/cgi"));
	  	}
	  	$.ajax({
	  		type: "POST",
	  		data: encodeURIComponent(msg),
	  		async: true,
	  		cache: false,
	  		url: reqUrl,
	  		dataType: "text",
	  		success: function(req){
				OnSuccessTest(req, false);
	  		},
	  		error: function(){
				ReqTrackingMaskArea();
			}
	  	});
  }
  

  function OnSuccessTest(req, isTest)
	 {  
		  if(req == "0")
		  {
			  alert("<?php echo $msg_areaSettingError[$GLOBALS['LANGINDEX']];?>");
		  }
		  else if(req == "58" && isTest)
		  {
				trackingSetup.drawings.cleanViewer();
		  }
		  else
		  {
				if(isTest){
					var xml_data=$.parseXML(req);
					
					var x1=$(xml_data).find("Point0 X").text(),x2=$(xml_data).find("Point1 X").text(),x3=$(xml_data).find("Point2 X").text(),x4=$(xml_data).find("Point3 X").text();
					var y1=$(xml_data).find("Point0 Y").text(),y2=$(xml_data).find("Point1 Y").text(),y3=$(xml_data).find("Point2 Y").text(),y4=$(xml_data).find("Point3 Y").text();
					
					trackingSetup.drawings.setAreaPoly(x1,y1,x2,y2,x3,y3,x4,y4);
				
					$('#polyName').val("");

					$("#poly-dialog").dialog("open");	
					$(".DisableAreaList" ).css("display","block");
					
					$("#DisableVideoSetup").css("display","none");
					$("#polyDraw").css("display","");
				}
		  }

		  localSeq++;
	 }

  	function OnSuccessMask(req)
	{
	  	setTimeout("ReqTrackingMaskArea()", 100);
	  	
	  	if(req == "0")
	  	{
	  		alert("<?php echo $msg_areaSettingError[$GLOBALS['LANGINDEX']];?>");
	  	}

		localSeq++;
	}

	function ReqTrackingMaskArea()
	{
	  	var msg = "<GetAllTrackingMaskArea />";

	  	var reqUrl = "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq;
	  	if (BrowserDetect.browser == "Explorer" || (BrowserDetect.browser == 'Safari' && reqUrl.search('.local') != -1)) {
	  		reqUrl = "../.."+reqUrl.substr(reqUrl.indexOf("/cgi"));
	  	}

	  	$.ajax({
	  		type: "POST",
	  		data: encodeURIComponent(msg),
	  		async: true,
	  		cache: false,
	  		url: reqUrl,
	  		dataType: "text",
	  		success: GetSuccess,
	  		error: null
	  	});
	}

	function GetSuccess(req)
	{
		trackingSetup.getAreaXML=req;
		trackingSetup.drawings.getArea();
		
		if(isOnload == true){
			if(BrowserDetect.browser == "Explorer" && getIEVersion() <= 8){
				var intervalId = window.setInterval(function(){
					var isFirstDecoding = SISOPlugin.getRelayStatus(90);
					if(isFirstDecoding == 1){
						window.clearInterval(intervalId);
						trackingSetup.drawings.rectangle(viewerWidth, viewerHeight, maxResolution.width, maxResolution.height);
						$("#DisableVideoSetup").css("display","none");
						$("#polyDraw").css("display","");
					}
				}, 100);
			}else{
				trackingSetup.drawings.rectangle(viewerWidth, viewerHeight, maxResolution.width, maxResolution.height);
				$("#DisableVideoSetup").css("display","none");
				$("#polyDraw").css("display","");
			}
			isOnload = false;
		}else{
			$("#DisableVideoSetup").css("display","none");
			$("#polyDraw").css("display","");		
		}

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
  	
	function OnCheckValue(event)
	{
		var keyCode = 0;
		if(window.event){ 	//ie,crome, safari
			keyCode = event.keyCode;
		} else { 				//firefox	
			keyCode = event.which;
		}
		if ((keyCode == 8) || (keyCode == 45) || (keyCode == 46) 
				|| (keyCode > 47 && keyCode < 58)
				|| (keyCode > 64 && keyCode < 91)
				|| (keyCode > 96 && keyCode < 123)) {
		}
		else {
			if(window.event){ //ie
				event.returnValue = false; 
				try{
					event.preventDefault();
				}catch(err){
				
				}
			}
			else{
				event.preventDefault();
			}
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
				?>
				<div id="poly-dialog" title="Enter Polygon Area Name" style="display:none;" >
					<p><label for="polyName"><?php echo $t_name[$GLOBALS['LANGINDEX']]; ?></label> <input type="text" name="polyName" id="polyName" onkeypress="NoKorean(event);OnCheckValue(event)" onkeydown="NoKorean(event);"></p>
				</div>
  				<div class="h3_tit">
					<h3 class="wid320"><?php echo $menu_ptztrackingsetup[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>
				<table class="data_write">
					<colgroup>
						<col style="width:180px;"/>
						<col style="width:35px;"/>
						<col style="width:165px;"/>
						<col style="width:35px;"/>
						<col />
					</colgroup>
					<tbody>
						<tr>
							<th> <?php echo $t_cameraHeight[$GLOBALS["LANGINDEX"]]; ?> </th>
							<td>
								<img id="camera_height_left" src="../images/common/btn/slider_-_normal.png" onclick="OnClickSlider('camera_height' , 'left');" 
									onMouseOver="ChangeImage('camera_height_left','../images/common/btn/slider_-_press.png');" 
									onMouseOut="ChangeImage('camera_height_left','../images/common/btn/slider_-_normal.png');"/>
							</td>
							<td>
								<div id="camera_height" class="slider_style_wid150">	</div>
							</td>
							<td>
								<img id="camera_height_right" src="../images/common/btn/slider_+_normal.png" onclick="OnClickSlider('camera_height' , 'right');" 
									onMouseOver="ChangeImage('camera_height_right','../images/common/btn/slider_+_press.png');" 
									onMouseOut="ChangeImage('camera_height_right','../images/common/btn/slider_+_normal.png');"/>
							</td>
							<td>
								<label id="camera_height_value"></label>
							</td>
						</tr>
						</tbody>
					</table>
					<table class="data_write">
						<colgroup>
							<col style="width:180px;"/>
							<col style="width:160px;"/>
							<col style="width:160px;"/>
							<col />
						</colgroup>
						<tbody>
							<tr>
								<th> <?php echo $t_zoom[$GLOBALS["LANGINDEX"]]; ?> </th>
								<td>
									<label><input type="radio" name="zoom" id="zoom_enable" value="Enable" onclick="OnClickTrackingZoom()" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" <?php if($trackingpreset->dataInfo['ZoomControl']['value'] == 1) echo "checked=\"checked\"" ?> /><?php echo $t_enable[$GLOBALS["LANGINDEX"]]; ?></label>
								</td>
								<td colspan=2>
									<label><input type="radio" name="zoom" id="zoom_disable" value="Disable" onclick="OnClickTrackingZoom()" <?php if($trackingpreset->dataInfo['ZoomControl']['value'] == 0) echo "checked=\"checked\"" ?>  /><?php echo $t_disable[$GLOBALS["LANGINDEX"]]; ?></label>
								</td>
							</tr>
							<tr>
								<th> <?php echo $t_maintainSize[$GLOBALS["LANGINDEX"]]; ?> </th>
								<td>
									<label style="margin-right:0px;"><input type="radio" name="size" id="small" value="small" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" <?php if($trackingpreset->dataInfo['ObjectSize']['value'] == 1) echo "checked=\"checked\""; if ($trackingpreset->dataInfo['ZoomControl']['value'] == 0) echo " disabled=\"disabled\""  ?> /><?php echo $t_small[$GLOBALS["LANGINDEX"]]; ?></label>
								</td>
								<td>
									<label><input type="radio" name="size" id="medium" value="medium" <?php if($trackingpreset->dataInfo['ObjectSize']['value'] == 2) echo "checked=\"checked\""; if ($trackingpreset->dataInfo['ZoomControl']['value'] == 0) echo " disabled=\"disabled\"" ?> /><?php echo $t_medium[$GLOBALS["LANGINDEX"]]; ?></label>
								</td>
								<td>
									<label><input type="radio" name="size" id="large" value="large" <?php if($trackingpreset->dataInfo['ObjectSize']['value'] == 3) echo "checked=\"checked\""; if ($trackingpreset->dataInfo['ZoomControl']['value'] == 0) echo " disabled=\"disabled\"" ?> /><?php echo $t_large[$GLOBALS["LANGINDEX"]]; ?></label>
								</td>
							</tr>
							<tr>
								<th> <?php echo $t_indicatorDisplay[$GLOBALS["LANGINDEX"]]; ?> </th>
								<td>
									<label><input type="radio" name="indicator_display" id="indicator_display_enable" value="Enable" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" <?php if($trackingpreset->dataInfo['Indicator']['value'] == 1) echo "checked=\"checked\"" ?> /><?php echo $t_enable[$GLOBALS["LANGINDEX"]]; ?></label>
								</td>
								<td colspan=2>
									<label><input type="radio" name="indicator_display" id="indicator_display_disable" value="Disable" <?php if($trackingpreset->dataInfo['Indicator']['value'] == 0) echo "checked=\"checked\"" ?>  /><?php echo $t_disable[$GLOBALS["LANGINDEX"]]; ?></label>
								</td>
							</tr>
							<tr>
								<th> <?php echo $t_areaActivation[$GLOBALS["LANGINDEX"]]; ?> </th>
								<td>
									<label><input type="radio" name="area_activation" id="area_activation_enable" value="Enable" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" <?php if($trackingpreset->dataInfo['AreaActivation']['value'] == 1) echo "checked=\"checked\"" ?> /><?php echo $t_enable[$GLOBALS["LANGINDEX"]]; ?></label>
								</td>
								<td colspan=2>
									<label><input type="radio" name="area_activation" id="area_activation_disable" value="Disable" <?php if($trackingpreset->dataInfo['AreaActivation']['value'] == 0) echo "checked=\"checked\"" ?>  /><?php echo $t_disable[$GLOBALS["LANGINDEX"]]; ?></label>
								</td>
							</tr>
							<tr>
								<th> <?php echo $t_automode[$GLOBALS["LANGINDEX"]]; ?> </th>
								<td colspan="3">
									<label><input type="radio" name="automode" id="automode_unlimited" value="Unlimited" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" <?php if($trackingpreset->dataInfo['AutoMode']['value'] == 0) echo "checked=\"checked\"" ?> /><?php echo $t_unlimited[$GLOBALS["LANGINDEX"]]; ?></label>
								</td>
							</tr>
							<tr>
								<td></td>
								<td colspan="3">
									<label><input type="radio" name="automode" id="automode_lostend" value="LostEnd" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" <?php if($trackingpreset->dataInfo['AutoMode']['value'] == 1) echo "checked=\"checked\"" ?> /><?php echo $t_lostend[$GLOBALS["LANGINDEX"]]; ?></label>
								</td>
							</tr>
						</table>
						<div class="btn_right" style="width:680px">
							<a id="mid_ok_btn" class="btn_apply" href="javascript:OnClickApply()"><?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?></a>
						</div>
					</div>
				</div>
			</div>
	</body>
</html>
