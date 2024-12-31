<?php
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_menu.cgi');
require_once ('../language/language_av_ptz.cgi');

$classInstances = GetClassInstance('ptzsetup');
$presetConf 	= $classInstances['PTZPreset'];
$serialConf 	= $classInstances['SerialConfiguration'];

// DEV_S1WEBVIEWER Start
$userClassInstance = GetClassInstance('user');
$userConf	= $userClassInstance['UserConfiguration'];
// DEV_S1WEBVIEWER End
define('MAX_PTZ_PRESET_SAMSUNG_T',		255);
define('MAX_PTZ_PRESET_SAMSUNG_E',		128);
define('MAX_PTZ_PRESET_PELCO_D',			255);
define('MAX_PTZ_PRESET_PELCO_P',			255);
define('MAX_PTZ_PRESET_SUNGJIN',			128);

$event_name = 'externalPTZ';
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="kr" xml:lang="kr">
<head>
	<title>iPOLiS NETWORK CAMERA WEBVIEWER</title>
	<meta http-equiv="X-UA-Compatible" content="IE=Edge; requiresActiveX=true" />
	<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
	<link rel="stylesheet" type="text/css" href="../css/techwin.css" />
	<link rel="stylesheet" type="text/css" href="../css/jquery.ui.slider.css"/>
	<link rel="stylesheet" type="text/css" href="../css/jquery.ui.tabs.css"/>
	<style>
	#container {
	  	position:relative,
  		float:left;
	  	overflow:hidden;
	  	color:#fff;
	  	min-height:900px;
	}
	#lnb-list {
		height:1200px;
	}
	</style>
	<script type="text/javascript" src="../js/jquery-1.9.1.js"></script>
	<script type="text/javascript" src="../js/jquery-ui.js"></script>
	<script type="text/javascript" src="../js/lnb.js"></script>
	<script type="text/javascript" src="../js/common_function.js"></script>
	<script type="text/javascript" src="../js/pluginCheck.js"></script>
	<script type="text/javascript" src="../js/pluginControl.js"></script>
	<script type="text/javascript" language="javascript">
	<?php if (!$GLOBALS['M_SUPPORT_EXTERNAL_PTZ']) { ?>
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

	var PRESETNUM		= new Array();
  	var PRESETNAME		= new Array();
  	var PRESETENABLE	= new Array();
  	var gActionCmd 		= "";

	$(document).ready(function(){ 
		lnbonoff("lnb_av");
		
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

  <?php
	  $maxPresetVal = MAX_PTZ_PRESET128; // 128
	  for($index=0; $index<$maxPresetVal; ++$index){
		  if (strlen($presetConf->preset[$index]['Name']['value']) == 0) continue;
  ?>
		  PRESETNAME[<?php echo ($index+1); ?>]  = "<?php echo trim($presetConf->preset[$index]['Name']['value']); ?>";
		  PRESETENABLE[<?php echo ($index+1); ?>]   = <?php echo $presetConf->preset[$index]['Enabled']['value']; ?>;
  <?php
	  }
  ?>

	function DrawPresetList()
	{
		var msgtxt = "";
		var maxPresetVal = 0;
		var test = 1;

		switch(test) {
			case "0":		maxPresetVal = <?php echo MAX_PTZ_PRESET_SAMSUNG_T; ?>;	break;
			case "1":		maxPresetVal = <?php echo MAX_PTZ_PRESET_SAMSUNG_E; ?>;	break;
			case "2":		maxPresetVal = <?php echo MAX_PTZ_PRESET_PELCO_D; ?>;		break;
			case "3":		maxPresetVal = <?php echo MAX_PTZ_PRESET_PELCO_P; ?>;		break;
			case "4":		maxPresetVal = <?php echo MAX_PTZ_PRESET_SUNGJIN; ?>;		break;
			default:		maxPresetVal = <?php echo MAX_PTZ_PRESET_SAMSUNG_T; ?>;	break;
		}
		
		<?php if($GLOBALS['M_SUPPORT_EXTERNAL_PTZ']){ ?>
				maxPresetVal = <?php echo MAX_PTZ_PRESET128; ?>;
		<?php } ?>

		msgtxt = "<select class=\"selectbox_style\" id=\"PresetList\" >";
		for(var i=1; i<=maxPresetVal; ++i){
			if(PRESETENABLE[i] == 1){
				msgtxt += "<option value="+i+">"+i+":"+PRESETNAME[i]+"</option>";
			}
			else {
				msgtxt += "<option value="+i+">"+i+":"+"</option>";
			}
		}
		msgtxt +="</select>";
		$("#PresetListText").html(msgtxt);
	}

	function OnClickPresetCmd(actionCmd)
	{
		var msg = "";
		var name = '';
		gActionCmd = actionCmd;
		if(actionCmd == "Add" ){

			if(!TypeCheck($('#PresetName').val(), NUM+ALPHA) || CheckSpace($('#PresetName').val())) {
				alert("<?php echo $msg_validPresetName[$GLOBALS['LANGINDEX']]; ?>");
				$('Preset.Name').focus();
				return;
			}

			if(parseInt($("#PresetList").val()) < 1 || parseInt($("#PresetList").val()) > <?php echo MAX_PTZ_PRESET255; ?> ){
				alert("<?php echo $msg_selValidPresetNumber[$GLOBALS['LANGINDEX']]; ?>");
				return;
			}
		}

		if(actionCmd == "Start" &&   PRESETENABLE[$("#PresetList").val()] != 1){
			alert("<?php echo $msg_selValidPresetNumber[$GLOBALS['LANGINDEX']]; ?>");
			return;
		}

		if(actionCmd == "Remove" &&   PRESETENABLE[$("#PresetList").val()] != 1){
			alert("<?php echo $msg_selValidPresetNumber[$GLOBALS['LANGINDEX']]; ?>");
			return;
		}

		//Add,Remove,Start
		msg += "<"+actionCmd+"PTZPreset>";
		msg += "<Index>"+$("#PresetList").val()+"</Index>";
		if (actionCmd == "Add") {
			msg += "<Name>"+$('#PresetName').val()+"</Name>";
		}
		msg += "</"+actionCmd+"PTZPreset>";

		var reqUrl = "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq;
		if (BrowserDetect.browser == "Explorer" || (BrowserDetect.browser == 'Safari' && reqUrl.search('.local') != -1)) {
			reqUrl = "../.."+reqUrl.substr(reqUrl.indexOf("/cgi"));
		}

		$.ajax({
			type: "POST",
			async: false,
			cache: false,
			url: reqUrl,
			dataType: "text",
			data: encodeURIComponent(msg),
			success: OnSuccessPresetCmd
		});
	}

	function OnSuccessPresetCmd(req)
	{
		if(gActionCmd == "Add") {
			alert("<?php echo $t_add[$GLOBALS['LANGINDEX']]; ?>");
		}
		else if(gActionCmd == "Remove") {
			alert("<?php echo $t_delete[$GLOBALS['LANGINDEX']]; ?>");
		}
		else if(gActionCmd == "Apply") {
			alert("<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>");
		}

		if (gActionCmd != "Start") {
			location.reload(true);
		}
		else
		{
			localSeq++;
		}
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
		
		DrawPresetList();
	}

	function OnClickApply()
	{
		var msg = "";
		msg += "<SetSerial>";
		msg += "<BaudRate>"+$('#baudRate').val()+"</BaudRate>";
		msg += "<ParityBit>"+$('#parityBit').val()+"</ParityBit>";
		msg += "<StopBit>"+$('#stopBit').val()+"</StopBit>";
		msg += "<DataBit>"+$('#dataBit').val()+"</DataBit>";
		msg += "<Protocol>"+$('#protocol').val()+"</Protocol>";
		msg += "<CameraID>"+1+"</CameraID>";
<?php 
	if ($GLOBALS['M_SUPPORT_MOTORIZE'] != 0) {
?>
		msg += "<FocusControl>"+$('#focusControl').val()+"</FocusControl>";
<?php
	}
?>
		msg += "</SetSerial>";
		gActionCmd = "Apply";
		RequestAjaxMsg(msg, "<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq);
	}

	</script>
</head>
<body onload="OnLoad()" onselectstart="return false">

	<div id="wrap">
		<?php
			require_once ('left_menu.cgi');
			require_once ('top_menu.cgi');
		?>
		<div id="container">
		<?php
			PrintLeftMenu($_SERVER['SCRIPT_NAME']);
		?>
			<div id="contents" >
			  	<?php
					require_once ('plugin_ui.cgi');
				?>
  				<div class="h3_tit" >
					<h3 class="wid320"><?php echo $t_presetSetup[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>
				<table class="data_write" border="0">
					<colgroup>
						<col style="width:160px;" />
						<col />
					</colgroup>
					<tbody>
						<tr>
							<th scope="row"><?php echo $t_number[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<span id="PresetListText"></span>
							</td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_name[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<input type="text" class="text" id="PresetName" maxlength ="12" onkeypress="IsNumChar(event);" style="width:191px;" >
							</td>
						</tr>
						<tr>
							<th></th>
							<td>
								<a class="btn_setup" href="javascript:OnClickPresetCmd('Start');" style="color:#fff"> <?php echo $t_go[$GLOBALS['LANGINDEX']]; ?> </a>
								<a class="btn_setup" href="javascript:OnClickPresetCmd('Add');" style="color:#fff"> <?php echo $t_add[$GLOBALS['LANGINDEX']]; ?> </a>
								<a class="btn_setup" href="javascript:OnClickPresetCmd('Remove');" style="color:#fff"> <?php echo $t_remove[$GLOBALS['LANGINDEX']]; ?> </a>
							</td>
						</tr>
					</tbody>
				</table>
				<div class="h3_tit" >
					<h3 class="wid220"><?php echo $t_serialSetup[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>
				<table class="data_write" border="0">
					<colgroup>
						<col style="width:160px;" />
						<col />
					</colgroup>
					<tbody>
						<tr>
							<th scope="row"><?php echo $t_protocol[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<select  id="protocol" class="selectbox_style">
									<option value="0" <?php if ($serialConf->dataInfo['Protocol']['value'] == 0) echo 'selected'; ?>>SAMSUNG-T</option>
									<option value="1" <?php if ($serialConf->dataInfo['Protocol']['value'] == 1) echo 'selected'; ?>>SAMSUNG-E</option>
									<option value="2" <?php if ($serialConf->dataInfo['Protocol']['value'] == 2) echo 'selected'; ?>>PELCO-D</option>
									<option value="3" <?php if ($serialConf->dataInfo['Protocol']['value'] == 3) echo 'selected'; ?>>PELCO-P</option>
									<?php if($GLOBALS['M_SUPPORT_EXTERNAL_PTZ']){ ?>
									<option value="4" <?php if ($serialConf->dataInfo['Protocol']['value'] == 4) echo 'selected'; ?>>SUNGJIN</option>
									<option value="5" <?php if ($serialConf->dataInfo['Protocol']['value'] == 5) echo 'selected'; ?>>PANASONIC</option>
									<option value="6" <?php if ($serialConf->dataInfo['Protocol']['value'] == 6) echo 'selected'; ?>>HONEYWELL</option>
									<option value="7" <?php if ($serialConf->dataInfo['Protocol']['value'] == 7) echo 'selected'; ?>>AD</option>
									<option value="8" <?php if ($serialConf->dataInfo['Protocol']['value'] == 8) echo 'selected'; ?>>VICON</option>
									<option value="9" <?php if ($serialConf->dataInfo['Protocol']['value'] == 9) echo 'selected'; ?>>GE</option>
									<option value="10" <?php if ($serialConf->dataInfo['Protocol']['value'] == 10) echo 'selected'; ?>>BOSCH</option>
									<?php } ?>
								</select>
							</td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_cameraID[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<select id="cameraID"  disabled='disabled' class="selectbox_style">
									<option value="1"> 1 </option>
								</select>
							</td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_baudRate[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<select id="baudRate" class="selectbox_style">
									<option value="0" <?php if ($serialConf->dataInfo['BaudRate']['value']  == 0) echo 'selected'; ?>>1200</option>
									<option value="1" <?php if ($serialConf->dataInfo['BaudRate']['value'] == 1) echo 'selected'; ?>>2400</option>
									<option value="2" <?php if ($serialConf->dataInfo['BaudRate']['value'] == 2) echo 'selected'; ?>>4800</option>
									<option value="3" <?php if ($serialConf->dataInfo['BaudRate']['value'] == 3) echo 'selected'; ?>>9600</option>
									<option value="4" <?php if ($serialConf->dataInfo['BaudRate']['value'] == 4) echo 'selected'; ?>>19200</option>
									<option value="5" <?php if ($serialConf->dataInfo['BaudRate']['value'] == 5) echo 'selected'; ?>>38400</option>
									<option value="6" <?php if ($serialConf->dataInfo['BaudRate']['value'] == 6) echo 'selected'; ?>>57600</option>
									<option value="7" <?php if ($serialConf->dataInfo['BaudRate']['value'] == 7) echo 'selected'; ?>>115200</option>
								</select>
							</td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_dataBit[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<select id="dataBit" class="selectbox_style">
									 <option value="0" <?php if ($serialConf->dataInfo['DataBit']['value'] == 0) echo 'selected'; ?>>7</option>
									 <option value="1" <?php if ($serialConf->dataInfo['DataBit']['value'] == 1) echo 'selected'; ?>>8</option>
								</select>
							</td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_parityBit[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<select id="parityBit" class="selectbox_style">
									 <option value="0"  <?php if ($serialConf->dataInfo['ParityBit']['value'] == 0) echo 'selected'; ?>>None</option>
									 <option value="1"  <?php if ($serialConf->dataInfo['ParityBit']['value'] == 1) echo 'selected'; ?>>Even</option>
									 <option value="2"  <?php if ($serialConf->dataInfo['ParityBit']['value'] == 2) echo 'selected'; ?>>Odd</option>
								</select>
							</td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_stopBit[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<select id="stopBit"  class="selectbox_style">
									 <option value="0" <?php if ($serialConf->dataInfo['StopBit']['value'] == 0) echo 'selected'; ?>>1</option>
									 <option value="1" <?php if ($serialConf->dataInfo['StopBit']['value'] == 1) echo 'selected'; ?>>2</option>
								</select>
							</td>
						</tr>
					<?php 
						if ($GLOBALS['M_SUPPORT_MOTORIZE'] != 0) {
					?>
						<tr>
							<th scope="row"><?php echo $t_onvifFocusMove[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<select id="focusControl"  class="selectbox_style">
									 <option value="0" <?php if ($serialConf->dataInfo['FocusControl']['value'] == 0) echo 'selected'; ?>><?php echo  $t_off[$GLOBALS['LANGINDEX']]; ?></option>
									 <option value="1" <?php if ($serialConf->dataInfo['FocusControl']['value'] == 1) echo 'selected'; ?>><?php echo  $t_on[$GLOBALS['LANGINDEX']]; ?></option>
								</select>
							</td>
						</tr>
					<?php
						}
					?>
					</tbody>
				</table>
				<div class="btn_right">
					<a id="mid_ok_btn" class="btn_apply" href="javascript:OnClickApply()"><?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?></a>
				</div>
				</div>
			</div>
		</div>
	</div>
</body>
</html>
