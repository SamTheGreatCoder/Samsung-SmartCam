<?php
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_menu.cgi');
require_once ('../language/language_av_videosetup.cgi');

$classInstances = GetClassInstance('videosrc');
$videosourceConf 	= $classInstances['VideoSource'];
$privacyMaskConf	= $classInstances['PrivacyMask'];
$mediaconfigurationconf = $classInstances['MediaConfiguration'];
$imageExposure 			= $classInstances["ImageSetting"]->imageExposure;
$blcMode						= $classInstances["ImageSetting"]->imageBackLight->dataInfo["Mode"]["value"];

// DEV_S1WEBVIEWER Start
$userClassInstance = GetClassInstance('user');
$userConf	= $userClassInstance['UserConfiguration'];
// DEV_S1WEBVIEWER End
$event_name = 'videosetup';
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
		#container{
			position:relative;
			overflow:visible;
			width:1600px;
		}
		#lnb-list {
			height:1300px;
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
		.ui-dialog .ui-dialog-buttonpane{ border: none;	padding: 20px 0}
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
		.ui-dialog-titlebar-close{float:right;}
		
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
			height:160px;
			opacity:0;filter:alpha(opacity=0);
			background:gray;
		}
		#poly-dialog{
			min-height: 0px !important;
		}
		#poly-dialog p{
		}#poly-dialog p label{
			line-height:20px;
			height:20px;
		}#poly-dialog p input,#poly-dialog p select{
			margin-left:10px;background:#fff;border:1px solid #EEE;
			width:140px;
		}
		#DeleteArea{
			background: none repeat scroll 0 0 #1B2029;
		//	border: 1px solid #1B2029;
			color: #FFFFFF;
			display: inline-block;
			font-weight: bold;
		/*	height: 25px;
			margin-left: 29px;
			margin-top: 8px;
			padding-top: 0;
			text-align: center;
			vertical-align: middle;
			width: 120px;
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
	<script type="text/javascript" src="../js/video_setup.js"></script>
	<!--[if lt IE 9]><script type="text/javascript" src="../js/excanvas.js"></script><![endif]-->	
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
	
	var buttonLang 			= ["<?php echo $t_ok[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $t_cancel[$GLOBALS['LANGINDEX']]; ?>"];
	var title		 			= "<?php echo $t_add[$GLOBALS['LANGINDEX']]; ?>";	
	var nameCheck	 			= "<?php echo $msg_validName[$GLOBALS['LANGINDEX']]; ?>";
	var isOnload				= false;

	<?php if($GLOBALS['M_SUPPORT_ROTATE']) { ?>
	var oldRotate = <?php echo $mediaconfigurationconf->dataInfo["Rotate"]["value"]; ?>;
	<?php } ?>

	$(document).ready(function(){ 
		lnbonoff("lnb_av"); 
		
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
		<?php if($GLOBALS['M_SUPPORT_PRIVACY_AREA'] == 32){ ?>
			videoSetup.msg_max_Privacyarea = "<?php echo $msg_max_Privacyarea_32[$GLOBALS['LANGINDEX']]; ?>";
		<?php }else if($GLOBALS['M_SUPPORT_PRIVACY_AREA'] == 12){ ?>
			videoSetup.msg_max_Privacyarea = "<?php echo $msg_max_Privacyarea_12[$GLOBALS['LANGINDEX']]; ?>";
		<?php }else if($GLOBALS['M_SUPPORT_PRIVACY_AREA'] == 6){ ?>
			videoSetup.msg_max_Privacyarea = "<?php echo $msg_max_Privacyarea_6[$GLOBALS['LANGINDEX']]; ?>";
		<?php } ?>
		window.setTimeout(function(){
			isOnload = true;
			ReqPrivacyArea();
		}, 1000);

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
		if(videoSetup.firstDrawClick && videoSetup.isDrawDragging){
			$("#imgTemp").trigger("mouseup");
		}
	});

	function OnLoad()
	{
		<?php if($blcMode == 3){ ?>			
			ChangeOption("sensor_mode", 0, 'Disable');		//sensor_tab.cgi
			ChangeOption("sensor_mode", 1, 'Disable');		//sensor_tab.cgi
		<?php } ?>
		if($("#privacy_off").is(':checked')) {
			$("#polyDraw").css("display","none"); 
			$("#DeleteArea").hide();
			$("#DeleteArea_disable").show();
			$(".DisableAreaList").css("display","");
		}		
	}

	function GetFilpMirrorStatus(){	
		var flip_mirror = 0;
		<?php if($videosourceConf->dataInfo['Flip']['value'] == 1 && $videosourceConf->dataInfo['Mirror']['value'] == 0) { ?>
			flip_mirror=1;
		<?php }else if($videosourceConf->dataInfo['Flip']['value'] == 0 && $videosourceConf->dataInfo['Mirror']['value'] == 1) { ?>
			flip_mirror=2;
		<?php }else if($videosourceConf->dataInfo['Flip']['value'] == 1 && $videosourceConf->dataInfo['Mirror']['value'] == 1) { ?>
			flip_mirror=3;
		<?php }else{ ?>
			flip_mirror=0;
		<?php } ?>
		
		return flip_mirror;
	}

	function GetRotateStatus(){	
		var rotate = 0;
		<?php if($mediaconfigurationconf->dataInfo["Rotate"]["value"] == 0) { ?>
			rotate=0;
		<?php }else if($mediaconfigurationconf->dataInfo["Rotate"]["value"] == 1) { ?>
			rotate=1;
		<?php }else if($mediaconfigurationconf->dataInfo["Rotate"]["value"] == 3) { ?>
			rotate=3;		
		<?php } ?>
		
		return rotate;
	}	

	function ApplyMaskPolygon(msg,isTest)
	{
	  	<?php if($GLOBALS['M_SUPPORT_PRIVACY_COLOR'] != PRIVACY_COLOR_TYPE_EVERY) { ?>
	  		$("input[name='privacyMaskStatus']").removeAttr("disabled");
	  	<?php } else {?>			
			$("#privacy_color").attr("disabled", "disabled");
			$("input[name='privacyMaskStatus']").attr("disabled", "disabled");
	  	<?php } ?>

		<?php if($GLOBALS['M_SUPPORT_PRIVACY_PATTERN']) { ?>
			$("#privacy_pattern").attr("disabled", "disabled");
		<?php } ?>
		
		$("#DisableVideoSetup").css("display","block");
		//$("#polyDraw").css("display","none");

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
	  			if(isTest){
					OnSuccessTest(req);
	  			}
	  			else{
					OnSuccessMask(req,true);
	  			}
	  		},
	  		error: null
	  	});
  }
  
	function ApplyPrivacyIndex(msg)
  	{  		
	  	<?php if($GLOBALS['M_SUPPORT_PRIVACY_COLOR'] != PRIVACY_COLOR_TYPE_EVERY) { ?>
	  		$("input[name='privacyMaskStatus']").removeAttr("disabled");
	  	<?php } else {?>			
			$("#privacy_color").attr("disabled", "disabled");
			$("input[name='privacyMaskStatus']").attr("disabled", "disabled");
	  	<?php } ?>

		<?php if($GLOBALS['M_SUPPORT_PRIVACY_PATTERN']) { ?>
			$("#privacy_pattern").attr("disabled", "disabled");
		<?php } ?>
		
		$("#DisableVideoSetup").css("display","block");
	  	
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
	  			OnSuccessMask(req,false);
	  		},
	  		error: function(){
				ReqPrivacyArea();
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
	  		//success: OnSuccessMask,
	  		error: function(){
				ReqPrivacyArea();
			}
	  	});
  }
  
  function OnSuccessTest(req)
  {
		if(req == "0")
		{
			alert("<?php echo $msg_areaSettingError[$GLOBALS['LANGINDEX']];?>");
		}else if(req == "58"){
			videoSetup.cleanViewer();
			$("input[name='privacyMaskStatus']").removeAttr("disabled");
			$("#privacy_color").removeAttr("disabled");
			<?php if($GLOBALS['M_SUPPORT_PRIVACY_PATTERN']) { ?>
			$("#privacy_pattern").removeAttr("disabled");
			<?php } ?>
			<?php if ($GLOBALS['M_MAX_ZOOM_RATIO'] == 43) { ?>
			alert("<?php echo $msg_privacy_Zoom_43x[$GLOBALS['LANGINDEX']];?>");
			<?php } else { ?>
			alert("<?php echo $msg_privacy_Zoom_32x[$GLOBALS['LANGINDEX']];?>");
			<?php } ?>
		}
		else
		{
			var xml_data=$.parseXML(req);

			var x1=$(xml_data).find("Point0 X").text(),x2=$(xml_data).find("Point1 X").text(),x3=$(xml_data).find("Point2 X").text(),x4=$(xml_data).find("Point3 X").text();
			var y1=$(xml_data).find("Point0 Y").text(),y2=$(xml_data).find("Point1 Y").text(),y3=$(xml_data).find("Point2 Y").text(),y4=$(xml_data).find("Point3 Y").text();
			<?php if($GLOBALS['M_SUPPORT_ZOOM_THRESHOLD']){ ?>
				$("#currentIndex").html($(xml_data).find("Index").text());
			<?php } ?>
			$('#polyName').val("");

			videoSetup.setAreaPoly(x1,y1,x2,y2,x3,y3,x4,y4);
	
			$("#poly-dialog").dialog("open");	
			$(".DisableAreaList" ).css("display","block");

			$("#DisableVideoSetup").css("display","none");

		<?php if($GLOBALS['M_SUPPORT_PRIVACY_COLOR'] & PRIVACY_COLOR_TYPE_EVERY) { ?>
			$("input[name='privacyShapeStatus']").removeAttr("disabled");
			//$('#privacy_color').removeAttr('disabled');
		<?php } ?>

		<?php if( $privacyMaskConf->dataInfo['Use']['value'] == 0){ ?>
			<?php if ($GLOBALS['M_SUPPORT_PRIVACY_COLOR'] == PRIVACY_COLOR_TYPE_EVERY) { ?>
			 $("input[name='privacyShapeStatus']").attr("disabled","disabled");
			 $('#privacy_color').attr('disabled', 'disabled');
			<?php } ?>

			<?php if($GLOBALS['M_SUPPORT_PRIVACY_PATTERN']) { ?>
			 $("#privacy_pattern").attr('disabled', 'disabled');
			<?php } ?>
		<?php } ?>
		}

		localSeq++;
  }
  function OnSuccessMask(req, isAreaSet)
  {
	  	if(req == "0")
	  	{
	  		alert("<?php echo $msg_areaSettingError[$GLOBALS['LANGINDEX']];?>");
	  	}else if(req == "58"){
			<?php if ($GLOBALS['M_MAX_ZOOM_RATIO'] == 43) { ?>
			alert("<?php echo $msg_privacy_Zoom_43x[$GLOBALS['LANGINDEX']];?>");
			<?php } else { ?>
			alert("<?php echo $msg_privacy_Zoom_32x[$GLOBALS['LANGINDEX']];?>");
			<?php } ?>
			
			<?php if($GLOBALS['M_SUPPORT_ZOOM_THRESHOLD']){ ?>
				if($("#zoom_threshold_on").length > 0){		//detect zoom_threshold_on obj
					$('#zoom_threshold_off').prop("checked", true);
					if(!isAreaSet){
						$(".DisableAreaList").css("display","block");
						$("#zoomThreshold-dialog").dialog("open");
					}
				}				
			<?php } ?>
		}

	  	setTimeout("ReqPrivacyArea()", 100);
		localSeq++;
  }

	function ReqPrivacyArea()
	{
	  	var msg = "<GetAllPrivacyArea />";

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
  		videoSetup.getAreaXML=req;		
		videoSetup.getArea();
		
		if(isOnload == true){
			if(BrowserDetect.browser == "Explorer" && getIEVersion() <= 8){
				var intervalId = window.setInterval(function(){
					var isFirstDecoding = SISOPlugin.getRelayStatus(90);
					if(isFirstDecoding == 1){
						window.clearInterval(intervalId);
						<?php if($GLOBALS['M_SUPPORT_PTZ'] == PTZ_SUPPORT) { ?> 
							videoSetup.init(viewerWidth,viewerHeight,maxResolution.width,maxResolution.height,"<?php echo $GLOBALS['M_SUPPORT_PRIVACY_AREA'] ?>", videoSetup.TYPE_RECT, 0, true,0);
						<?php }else if($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_HISILICON){ ?>
							videoSetup.init(viewerWidth,viewerHeight,maxResolution.width,maxResolution.height,"<?php echo $GLOBALS['M_SUPPORT_PRIVACY_AREA'] ?>", videoSetup.TYPE_RECT, GetFilpMirrorStatus(), false, GetRotateStatus());
						<?php }else{ ?>
							videoSetup.init(viewerWidth,viewerHeight,maxResolution.width,maxResolution.height,"<?php echo $GLOBALS['M_SUPPORT_PRIVACY_AREA'] ?>", videoSetup.TYPE_POLY, GetFilpMirrorStatus(), false,0);
						<?php } ?>
						<?php if ($privacyMaskConf->dataInfo['Use']['value'] == 1) { ?>
							$("#DisableVideoSetup").css("display","none");
						<?php } ?>
					}
				},100);
			}else{
				<?php if($GLOBALS['M_SUPPORT_PTZ'] == PTZ_SUPPORT) { ?> 
					videoSetup.init(viewerWidth,viewerHeight,maxResolution.width,maxResolution.height,"<?php echo $GLOBALS['M_SUPPORT_PRIVACY_AREA'] ?>", videoSetup.TYPE_RECT, 0, true,0);
				<?php }else if($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_HISILICON){ ?>
					videoSetup.init(viewerWidth,viewerHeight,maxResolution.width,maxResolution.height,"<?php echo $GLOBALS['M_SUPPORT_PRIVACY_AREA'] ?>", videoSetup.TYPE_RECT, GetFilpMirrorStatus(), false, GetRotateStatus());
				<?php }else{ ?>
					videoSetup.init(viewerWidth,viewerHeight,maxResolution.width,maxResolution.height,"<?php echo $GLOBALS['M_SUPPORT_PRIVACY_AREA'] ?>", videoSetup.TYPE_POLY, GetFilpMirrorStatus(), false,0);
				<?php } ?>
				<?php if ($privacyMaskConf->dataInfo['Use']['value'] == 1) { ?>
					$("#DisableVideoSetup").css("display","none");
				<?php } ?>
			}
			isOnload = false;
		}else{
			<?php if ($privacyMaskConf->dataInfo['Use']['value'] == 1) { ?>
				videoSetup.cleanViewer();
				<?php if($GLOBALS['M_SUPPORT_ZOOM_THRESHOLD']){ ?>
					if($("#zoom_threshold_on").length > 0){		//detect zoom_threshold_on obj
						if($("#zoom_threshold_on").is(":checked")){
							$(".DisableAreaList").css("display","block");
							$("#zoomThreshold-dialog").dialog("open");
							$('#zoom_threshold_off').prop("checked", true);
						}
					}
				<?php } ?>
			<?php } ?>
		}
	
	<?php if($GLOBALS['M_SUPPORT_PRIVACY_COLOR'] == PRIVACY_COLOR_TYPE_EVERY) { ?>
		$("input[name='privacyMaskStatus']").removeAttr("disabled");
		if ($('#privacy_on').is(':checked')) {
		  	$("input[name='privacyShapeStatus']").removeAttr("disabled");
			$('#privacy_color').removeAttr('disabled');
		}
		else {
			$("input[name='privacyShapeStatus']").attr("disabled","disabled");
  			$('#privacy_color').attr('disabled', 'disabled');
		}
	<?php } ?>

	<?php if($GLOBALS['M_SUPPORT_PRIVACY_PATTERN']) { ?>
		if ($('#privacy_on').is(':checked')) {
			$("#privacy_pattern").removeAttr("disabled");
		}
		else {
			$("#privacy_pattern").attr('disabled', 'disabled');
		}
	<?php } ?>

		localSeq++;
  }

  function DisableShapeSelect(val)
  {
	<?php if($privacyMaskConf->dataInfo['Use']['value'] == 0){ ?>
	return;
	<?php } ?>

  	<?php if ($GLOBALS['M_SUPPORT_PRIVACY_COLOR'] & PRIVACY_COLOR_TYPE_EVERY) { ?>
  	if(val == 1) {
  		$("input[name='privacyShapeStatus']").attr("disabled","disabled");
  	  	$('#privacy_color').attr('disabled', 'disabled');
  	}
  	else if(val == 0) {
  		$("input[name='privacyShapeStatus']").removeAttr("disabled");
  	  	$('#privacy_color').removeAttr('disabled');
  	}
  	<?php } ?>

	<?php if ($GLOBALS['M_SUPPORT_PRIVACY_PATTERN']) { ?>
  	if(val == 1) {
  	  	$('#privacy_pattern').attr('disabled', 'disabled');
  	}
  	else if(val == 0) {
  	  	$('#privacy_pattern').removeAttr('disabled');
  	}
  	<?php } ?>
	/*
	var list = $("#MaskList").get(0);
	if(val == 1) {
		list.content.MaskListControl.DisabledRemoveBtn("On");
  	}
  	else if(val == 0) {
		list.content.MaskListControl.DisabledRemoveBtn("Off");
  	}
  	*/
  }

	function validateName() {
	   var name = $("#polyName").val();	   	   
	   var trimChars = [ ' ', '=', '\\', '/', ';', ':', ',', '+', '*', '@', '!', '#', '$', '%', '^', '&', '*', '(', ')', '[', ']', '{', '}', '\'', '\"', '_', '~', '`', '?', '<', '>', '|' ];
	   for(var i=0; i < trimChars.length; i++) {
	   	name = name.replace(trimChars[i], "");	
	   }
	   
	   $("#polyName").val(name);
	   
	   var regexp = /^[a-zA-Z0-9]+$/;
	   if (name && certName.search(regexp) == -1)
	       { 
		  alert("<?php echo $msg_validName[$GLOBALS['LANGINDEX']];?>");
		  return false;
	       }
	       
	   return true;    
			
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

	function OnClickPrivacyUse()
	{
		if ($('#privacy_on').is(':checked')) {
			$('#privacy_color').removeAttr('disabled');
			<?php if($GLOBALS['M_SUPPORT_PRIVACY_PATTERN']) { ?>
			$('#privacy_pattern').removeAttr('disabled');
			<?php }?>
		}
		else {
			$('#privacy_color').attr('disabled', 'disabled');
			<?php if($GLOBALS['M_SUPPORT_PRIVACY_PATTERN']) { ?>
			$('#privacy_pattern').attr('disabled', 'disabled');
			<?php }?>
		}
  	}
	
	function OnClickApply()
  	{	
	 	var msg = "";
		var isChangedRotate = 0;
		var isS1model = <?php echo $GLOBALS['M_SPECIAL_TYPE']; ?>;
	  	
	  	msg += "<SetVideoOutput>";
		<?php if($GLOBALS['M_SUPPORT_ANALOG'] & ANALOG_ONOFF_CONFIGURABLE) { ?>
	  	msg += "<Enabled>"+($('#videoOutput_on').is(':checked') ? 1 : 0)+"</Enabled>";
		<?php } if ($GLOBALS['M_SUPPORT_ANALOG'] & ANALOG_NTPAL_CONFIGURABLE) {?>
	  	msg += "<VideoType>"+($('#videoType_pal').is(':checked') ? 1 : 0)+"</VideoType>";
	  	<?php } if($GLOBALS['M_SUPPORT_AUTOFLIP']){?>
	  	msg += "<AutoFlipEnable>"+($('#autoflip_on').is(':checked') ? 1 : 0)+"</AutoFlipEnable>";
	  	<?php } if($GLOBALS['M_SUPPORT_ROTATE']){?>
	  	msg += "<Rotate>"+$("#rotate").val()+"</Rotate>";
		if (oldRotate != $("#rotate").val()) {
			isChangedRotate = 1;
		}
	  	<?php }?>
	  	msg += "</SetVideoOutput>";
	  	RequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, 'NO_REFRESH'); // NOT REFRESH
		localSeq++;

	  	msg = '';
	  	msg += "<SetPrivacyMask>";
	  	msg += "<Use>"+($('#privacy_on').is(':checked') ? 1 : 0)+"</Use>";
	  	<?php if($GLOBALS['M_SUPPORT_PRIVACY_COLOR'] == PRIVACY_COLOR_TYPE_EVERY) { ?>
	  		msg += "<Color>"+ ($('#privacy_color').val())+"</Color>";
	  	<?php } ?>
		<?php if($GLOBALS['M_SUPPORT_PRIVACY_PATTERN']) { ?>
		msg += "<Pattern>" + ($('#privacy_pattern').val()) + "</Pattern>";
		<?php } ?>
	  	msg += "</SetPrivacyMask>";
	  	RequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, 'NO_REFRESH'); // NOT REFRESH
		localSeq++;

	  	msg = '';
		<?php if(($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ) && $GLOBALS['M_SUPPORT_SENSOR_FRAMEMODE']){ ?>
		msg += "<SetImageSetting>";
	  	msg += "<TestCmd>0</TestCmd>";
	  	msg += "<ImageExposure>";
	  	msg += "<SensorFrameMode>" + $("#sensor_mode").val() + "</SensorFrameMode>";		//sensor_tab.cgi
	  	msg += "</ImageExposure>";
	  	msg += "</SetImageSetting>";
	  	RequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, 'NO_REFRESH'); // NOT REFRESH
		localSeq++;
	  	<?php } ?>
	  	msg = '';
	  	msg += "<SetVideoSource>";
		<?php if($GLOBALS['M_SUPPORT_PTZ']){ ?>
	  	msg += "<Flip>"+($('#flip_on').is(':checked') ? 1 : 0)+"</Flip>";
	  	msg += "<Mirror>"+($('#flip_on').is(':checked') ? 1 : 0)+"</Mirror>";
		<?php } else { ?>
		msg += "<Flip>"+($('#flip_on').is(':checked') ? 1 : 0)+"</Flip>";
  		msg += "<Mirror>"+($('#mirror_on').is(':checked') ? 1 : 0)+"</Mirror>";
		<?php } ?>
	  	msg += "</SetVideoSource>";

		if (isChangedRotate == 1 && isS1model != 1) {
			SISOPlugin.stop();
			RequestAjaxMsg(msg, "<?php echo $t_apply[$GLOBALS['LANGINDEX']];?>", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, 'NO_REFRESH'); // NO_REFRESH
			alert("<?php echo $msg_windowClose[$GLOBALS['LANGINDEX']]; ?>");
			window.open('about:blank', '_self').close();
		}
		else
		{
	  		RequestAjaxMsg(msg, "<?php echo $t_apply[$GLOBALS['LANGINDEX']];?>", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, 'PrivacyMask'); // REFRESH
		}
  	}
	function OnchangeSensor(){
		<?php if($blcMode == 3){ ?>
			if($("#sensor_mode").val() < 2){
				$("#sensor_mode").val(old_sensor);
			}
			old_sensor = $("#sensor_mode").val();
		<?php } ?>
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
			<div id="contents">
			  	<div class="h3_tit mgt0" >
					<h3><?php echo $t_videosrc[$GLOBALS['LANGINDEX']];?></h3>
				</div>
				<table class="data_write">
					<colgroup>
						<col style="width:190px;" />
						<col style="width:160px;" />
						<col style="width:330px;" />
					</colgroup>
					<tbody>
					<?php if($GLOBALS['M_SUPPORT_PTZ']){ ?>
						<tr>
							<th scope="row"><?php echo $t_filpMirror[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<label><input type="radio" name="flip" id="flip_on" <?php if ($videosourceConf->dataInfo['Flip']['value'] == 1) echo 'checked=\'checked\''; ?> style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_on[$GLOBALS['LANGINDEX']];?></label>
							</td>
							<td>
								<label><input type="radio" name="flip" id="flip_off" <?php if ($videosourceConf->dataInfo['Flip']['value'] == 0) echo 'checked=\'checked\''; ?>/><?php echo $t_off[$GLOBALS['LANGINDEX']];?></label>
							</td>
						</tr>
					<?php } else { ?>
						<tr>
							<th scope="row"><?php echo $t_flip[$GLOBALS['LANGINDEX']];?></th>
							<td>
								<label><input type="radio" name="flip" id="flip_on" <?php if ($videosourceConf->dataInfo['Flip']['value'] == 1) echo 'checked=\'checked\''; ?> style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/>&nbsp;<?php echo $t_on[$GLOBALS['LANGINDEX']];?></label>
							</td>
							<td>
								<label><input type="radio" name="flip" id="flip_off" <?php if ($videosourceConf->dataInfo['Flip']['value'] == 0) echo 'checked=\'checked\''; ?>/>&nbsp;<?php echo $t_off[$GLOBALS['LANGINDEX']];?></label>
							</td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_mirror[$GLOBALS['LANGINDEX']];?></th>
							<td>
								<label><input type="radio" name="mirror" id="mirror_on" <?php if ($videosourceConf->dataInfo['Mirror']['value'] == 1) echo 'checked=\'checked\''; ?> style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/>&nbsp;<?php echo $t_on[$GLOBALS['LANGINDEX']];?></label>
							</td>
							<td>
								<label><input type="radio" name="mirror" id="mirror_off" <?php if ($videosourceConf->dataInfo['Mirror']['value'] == 0) echo 'checked=\'checked\''; ?>/>&nbsp;<?php echo $t_off[$GLOBALS['LANGINDEX']];?></label>
							</td>
						</tr>
					<?php } ?>
					<?php if($GLOBALS['M_SUPPORT_AUTOFLIP']){ ?>
						<tr>
							<th scope="row"><?php echo $t_digitalFlip[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<label><input type="radio" name="autoflip" id="autoflip_on" <?php if ($mediaconfigurationconf->dataInfo['AutoFlipEnable']['value'] == 1) echo 'checked=\'checked\''; ?> style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_on[$GLOBALS['LANGINDEX']];?></label>
							</td>
							<td>
								<label><input type="radio" name="autoflip" id="autoflip_off" <?php if ($mediaconfigurationconf->dataInfo['AutoFlipEnable']['value'] == 0) echo 'checked=\'checked\''; ?>/><?php echo $t_off[$GLOBALS['LANGINDEX']];?></label>
							</td>
						</tr>
					<?php } ?>
					<?php if($GLOBALS['M_SUPPORT_ROTATE'] && $GLOBALS['M_SPECIAL_TYPE'] != 1){ ?>
						<tr>
							<th scope="row"><?php echo $t_hallwayView[$GLOBALS['LANGINDEX']]; ?></th>
							<td colspan="2">
								<select name="select" id="rotate" class="selectbox_style_width160" >
									<option value="0" <?php if ($mediaconfigurationconf->dataInfo["Rotate"]["value"] == 0) echo "selected=\"selected\""; ?>>0 <?php echo $t_degree[$GLOBALS['LANGINDEX']]; ?></option>
									<option value="1" <?php if ($mediaconfigurationconf->dataInfo["Rotate"]["value"] == 1) echo "selected=\"selected\""; ?>>90 <?php echo $t_degree[$GLOBALS['LANGINDEX']]; ?></option>
									<option value="3" <?php if ($mediaconfigurationconf->dataInfo["Rotate"]["value"] == 3) echo "selected=\"selected\""; ?>>270 <?php echo $t_degree[$GLOBALS['LANGINDEX']]; ?></option>
							  </select>
							</td>
						</tr>
					<?php } ?>
					<?php
						if ($GLOBALS['M_SUPPORT_ANALOG'] & ANALOG_AVAILABLE) {
					?>
						<tr>
							<td colspan="3" style="height:30px;">
							</td>
						</tr>
						<tr>
							<td style="border-bottom:1px solid #737c8f;">
		  						<h3 style="color:#54afff;font-size:13px; margin-left:-8px"><?php echo $t_videoOutput[$GLOBALS['LANGINDEX']];?></h3>
							</td>
							<td style="border-bottom:1px solid #737c8f;">
								<label><input type="radio" name="videooutput" id="videoOutput_on" <?php if ($classInstances['MediaConfiguration']->videoOutput->dataInfo['Enabled']['value'] == 1) echo 'checked=\'checked\''; ?> style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_on[$GLOBALS['LANGINDEX']];?></label>
							</td>
							<td style="border-bottom:1px solid #737c8f;">
								<label><input type="radio" name="videooutput" id="videoOutput_off" <?php if ($classInstances['MediaConfiguration']->videoOutput->dataInfo['Enabled']['value'] == 0) echo 'checked=\'checked\''; ?>/><?php echo $t_off[$GLOBALS['LANGINDEX']];?></label>
							</td>
						</tr>
				<?php
					}
				?>
				<?php if($GLOBALS['M_SUPPORT_ANALOG'] & ANALOG_NTPAL_CONFIGURABLE) { ?>
						<tr>
							<td colspan="3" style="height:30px;">
							</td>
						</tr>

						<tr>
							<td style="border-bottom:1px solid #737c8f;">
								<h3 style="color:#54afff;font-size:13px; margin-left:-8px"><?php echo $t_videoType[$GLOBALS['LANGINDEX']];?></h3>
							</td>
							<td style="border-bottom:1px solid #737c8f;">
								<label><input type="radio" name="videotype" id="videoType_ntsc" <?php if ($classInstances['MediaConfiguration']->dataInfo['VideoType']['value'] == 0) echo 'checked=\'checked\''; ?> style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/>NTSC</label>
							</td>
							<td style="border-bottom:1px solid #737c8f;">
								<label><input type="radio" name="videotype" id="videoType_pal" <?php if ($classInstances['MediaConfiguration']->dataInfo['VideoType']['value'] == 1) echo 'checked=\'checked\''; ?>/>PAL</label>
							</td>
						</tr>
					<?php }?>
					<?php if(($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ) && $GLOBALS['M_SUPPORT_SENSOR_FRAMEMODE']){ ?>
						<tr>
							<td colspan="3" style="height:30px;">
							</td>
						</tr>
						<tr>
							<td colspan="3" style="border-bottom:1px solid #737c8f;">
								<h3 style="color:#54afff;font-size:13px; margin-left:-8px"><?php echo $t_sensor[$GLOBALS["LANGINDEX"]]; ?></h3>
							</td>
						</tr>
						<tr height="20px">	</tr>
						<tr>
							<th scope="row"> <?php echo $t_mode[$GLOBALS['LANGINDEX']];?> </th>
							<td colspan="2">
								<select name="select" id="sensor_mode" class="selectbox_style_width160" >
									<?php if ($GLOBALS['M_MAX_SERSORFRAME'] == 60) { ?>
									<option value="0" <?php if ($imageExposure->dataInfo["SensorFrameMode"]["value"] == 0) echo "selected=\"selected\""; ?>>60 fps</option>
									<option value="1" <?php if ($imageExposure->dataInfo["SensorFrameMode"]["value"] == 1) echo "selected=\"selected\""; ?>>50 fps</option>
									<?php } ?>
									<option value="2" <?php if ($imageExposure->dataInfo["SensorFrameMode"]["value"] == 2) echo "selected=\"selected\""; ?>>30 fps</option>
									<option value="3" <?php if ($imageExposure->dataInfo["SensorFrameMode"]["value"] == 3) echo "selected=\"selected\""; ?>>25 fps</option>
							  </select>
							</td>
						</tr>
						<tr>
							<td colspan="3">
								<?php 
								if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ) {
									echo $msg_sensorchange[$GLOBALS["LANGINDEX"]];
								}else{
									echo $msg_sensorchange_nowdr[$GLOBALS["LANGINDEX"]];
								}
								?>
							</td>
						</tr>
					<?php } ?>
						<tr>
							<td colspan="3" style="height:30px;">
							</td>
						</tr>
						<tr>
							<td colspan="3" style="border-bottom:1px solid #737c8f;">
								<h3 style="color:#54afff;font-size:13px; margin-left:-8px"><?php echo $t_privacy[$GLOBALS['LANGINDEX']];?></h3>
							</td>
						</tr>
						<tr height="20px">	</tr>
						<tr>
							<th scope="row">
								<?php echo $t_enable[$GLOBALS['LANGINDEX']];?>
							</th>
							<td>
								<label><input type="radio" name="privacyMaskStatus" id="privacy_on" onclick="OnClickPrivacyUse();" <?php if ($privacyMaskConf->dataInfo['Use']['value'] == 1) echo 'checked=\'checked\''; ?> style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_on[$GLOBALS['LANGINDEX']];?></label>
							</td>
							<td>
								<label><input type="radio" name="privacyMaskStatus" id="privacy_off" onclick="OnClickPrivacyUse();" <?php if ($privacyMaskConf->dataInfo['Use']['value'] == 0) echo 'checked=\'checked\''; ?>/><?php echo $t_off[$GLOBALS['LANGINDEX']];?></label>
							</td>
						</tr>
					<?php if($GLOBALS['M_SUPPORT_PRIVACY_PATTERN']) { ?>
						<tr>
							<th scope="row">
								<?php echo $t_pattern[$GLOBALS['LANGINDEX']];?>
							</th>
							<td colspan="2">
								<select name="select" id="privacy_pattern" class="selectbox_style_width160" style="" <?php if ($privacyMaskConf->dataInfo['Use']['value'] == 0) echo "disabled=\"disabled\""; ?>>
	        						<option value = "0" <?php if ($privacyMaskConf->dataInfo['Pattern']['value'] == 0) echo 'selected=\'selected\''; ?>><?php echo $t_solid[$GLOBALS['LANGINDEX']];?></option>
	        						<option value = "1" <?php if ($privacyMaskConf->dataInfo['Pattern']['value'] == 1) echo 'selected=\'selected\''; ?>><?php echo $t_mosaic[$GLOBALS['LANGINDEX']];?> 1</option>
	        						<option value = "2" <?php if ($privacyMaskConf->dataInfo['Pattern']['value'] == 2) echo 'selected=\'selected\''; ?>><?php echo $t_mosaic[$GLOBALS['LANGINDEX']];?> 2</option>
	        						<option value = "3" <?php if ($privacyMaskConf->dataInfo['Pattern']['value'] == 3) echo 'selected=\'selected\''; ?>><?php echo $t_mosaic[$GLOBALS['LANGINDEX']];?> 3</option>
	        						<option value = "4" <?php if ($privacyMaskConf->dataInfo['Pattern']['value'] == 4) echo 'selected=\'selected\''; ?>><?php echo $t_mosaic[$GLOBALS['LANGINDEX']];?> 4</option>
							  </select>
							</td>
						</tr>
					<?php } ?>
					<?php if($GLOBALS['M_SUPPORT_PRIVACY_COLOR'] & PRIVACY_COLOR_TYPE_EVERY) { ?>
						<tr>
							<th scope="row">
								<?php echo $t_polygonType[$GLOBALS['LANGINDEX']];?>
							</th>
							<td>
								<label><input type="radio" name="privacyShapeStatus" id="privacy_area_rectangle" checked="checked" onclick="DoRectangle();" <?php if ($privacyMaskConf->dataInfo['Use']['value'] == 0) echo "disabled=\"disabled\""; ?> style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_rectangle[$GLOBALS['LANGINDEX']];?></label>
							</td>
							<td>
								<label><input type="radio" name="privacyShapeStatus" id="privacy_area_quadrilateral" onclick="DoQuadrilateral();" <?php if ($privacyMaskConf->dataInfo['Use']['value'] == 0) echo "disabled=\"disabled\""; ?>/><?php echo $t_quadrilateral[$GLOBALS['LANGINDEX']];?></label>
							</td>
						</tr>
					<?php } ?>
					<?php if($GLOBALS['M_SUPPORT_PRIVACY_COLOR'] == PRIVACY_COLOR_TYPE_EVERY) { ?>
						<tr>
							<th scope="row"> <?php echo $t_color[$GLOBALS['LANGINDEX']];?> </th>
							<td colspan="2">
								<select name="select" id="privacy_color" class="selectbox_style_width160" style="" <?php if ($privacyMaskConf->dataInfo['Use']['value'] == 0) echo "disabled=\"disabled\""; ?>>
							    	<option value = "5" <?php if ($privacyMaskConf->dataInfo['Color']['value'] == 5) echo 'selected=\'selected\''; ?>><?php echo $t_gray[$GLOBALS['LANGINDEX']];?></option>
	        						<option value = "0" <?php if ($privacyMaskConf->dataInfo['Color']['value'] == 0) echo 'selected=\'selected\''; ?>><?php echo $t_green[$GLOBALS['LANGINDEX']];?></option>
	        						<option value = "1" <?php if ($privacyMaskConf->dataInfo['Color']['value'] == 1) echo 'selected=\'selected\''; ?>><?php echo $t_red[$GLOBALS['LANGINDEX']];?></option>
	        						<option value = "2" <?php if ($privacyMaskConf->dataInfo['Color']['value'] == 2) echo 'selected=\'selected\''; ?>><?php echo $t_blue[$GLOBALS['LANGINDEX']];?></option>
	        						<option value = "3" <?php if ($privacyMaskConf->dataInfo['Color']['value'] == 3) echo 'selected=\'selected\''; ?>><?php echo $t_black[$GLOBALS['LANGINDEX']];?></option>
	        						<option value = "4" <?php if ($privacyMaskConf->dataInfo['Color']['value'] == 4) echo 'selected=\'selected\''; ?>><?php echo $t_white[$GLOBALS['LANGINDEX']];?></option>
							  </select>
							</td>
						</tr>
					<?php } ?>
					<?php if($GLOBALS['M_SUPPORT_PTZ'] == PTZ_SUPPORT && $GLOBALS['M_MAX_ZOOM_RATIO'] == 43) { ?> 
						<tr><td colspan="3"><?php echo $msg_privacy_Zoom_43x[$GLOBALS['LANGINDEX']];?></td></tr>
					<?php } else if($GLOBALS['M_SUPPORT_PTZ'] == PTZ_SUPPORT) { ?> 
						<tr><td colspan="3"><?php echo $msg_privacy_Zoom_32x[$GLOBALS['LANGINDEX']];?></td></tr>
					<?php } ?>
						<tr height="30px">	</tr>
					</tbody>
				</table>
				<?php
					require_once ('plugin_ui.cgi');
				?>
				<div id="poly-dialog" title="Enter Polygon Area Name" style="display:none;" >
					<p><label for="polyName" style="width:50px"><?php echo $t_name[$GLOBALS['LANGINDEX']]; ?></label> <input type="text" name="polyName" id="polyName" onkeypress='NoKorean(event);OnCheckValue(event)' onkeydown='NoKorean(event)' ></p>
					<p>
					<?php if($GLOBALS['M_SUPPORT_PRIVACY_COLOR'] == PRIVACY_COLOR_TYPE_EACH) { ?>
						<label for="polyColor" style="width:50px"><?php echo $t_color[$GLOBALS['LANGINDEX']]; ?></label> 
						<select  name="polyColor" id="polyColor" >
							<option value="5"><?php echo $t_gray[$GLOBALS['LANGINDEX']];?></option>
							<option value="2"><?php echo $t_green[$GLOBALS['LANGINDEX']];?></option>	
							<option value="1"><?php echo $t_red[$GLOBALS['LANGINDEX']];?></option>	
							<option value="3"><?php echo $t_blue[$GLOBALS['LANGINDEX']];?></option>	
							<option value="4"><?php echo $t_black[$GLOBALS['LANGINDEX']];?></option>
							<option value="0"><?php echo $t_white[$GLOBALS['LANGINDEX']];?></option>	
						</select>
					<?php } ?>
					</p>
					<?php if($GLOBALS['M_SUPPORT_ZOOM_THRESHOLD']){ ?>
					<p style="position:relative; margin-top:10px">
						<label style="width:240px"><?php echo $t_zoomThreshold[$GLOBALS['LANGINDEX']]; ?></label>
					</p>
					<p>
						<div>
							<div style="float:left; width:100px">
								<label><input id="zoom_threshold_on" type="radio" name="zoom_threshold" /><?php echo $t_on[$GLOBALS['LANGINDEX']];?></label>
							</div>
							<div style="float:left; left:10px; width:100px">
								<label><input id="zoom_threshold_off" type="radio" name="zoom_threshold" checked="checked"/><?php echo $t_off[$GLOBALS['LANGINDEX']];?></label>
							</div>
						</div>
					</p>
					<?php } ?>
				</div>
				<?php if($GLOBALS['M_SUPPORT_ZOOM_THRESHOLD']){ ?>
				<div id="zoomThreshold-dialog" title="<?php echo $t_setZoomThreshold[$GLOBALS['LANGINDEX']]; ?>" style="display:none;" >
					<p style="position:relative; margin-top:10px">
						<label style=""><?php echo $msg_zoomThreshold[$GLOBALS['LANGINDEX']]; ?></label>
						<label id="currentIndex" style="display:none"></label>
					</p>					
				</div>
				<?php } ?>
				<div class="btn_right" style="clear:both; width:680px">
					<a href="javascript:OnClickApply()" class="btn_apply"><?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?></a>
				</div>
			</div>
		</div>
	</div>
</body>
</html>
