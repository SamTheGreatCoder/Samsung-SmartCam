<?php
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_menu.cgi');
require_once ('../language/language_av_ptz.cgi');

$classInstances = GetClassInstance('ptzlimit');
$ptzlimit = $classInstances['PTZLimit'];
$event_name = "ptzlimit";
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
	<script type="text/javascript" src="../js/jquery-1.9.1.js"></script>
	<script type="text/javascript" src="../js/jquery-ui.js"></script>
	<script type="text/javascript" src="../js/lnb.js"></script>
	<script type="text/javascript" src="../js/common_function.js"></script>
	<script type="text/javascript" src="../js/pluginCheck.js"></script>
	<script type="text/javascript" src="../js/pluginControl.js"></script>
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

	var panLimitVal = <?php echo $ptzlimit->dataInfo["PanLimit"]["value"]; ?>;
	var tiltLimitVal = <?php echo $ptzlimit->dataInfo["TiltLimit"]["value"]; ?>;
	var tiltLimitRange = <?php echo $ptzlimit->dataInfo["TiltLimitRange"]["value"]; ?>;
	var propotionalPT = <?php echo $ptzlimit->dataInfo["PropotionalMode"]["value"]; ?>;
	
	$(document).ready(function(){
		lnbonoff("lnb_av");		

		$("#LimitStartBtn").attr('href','#');
		$("#LimitStartBtn").attr('class','btn_type01');
		$("#LimitStartBtn").css('color','#fff');
		$("#LimitStartBtn").bind("click", LimitStartHandler);

		$("#LimitEnterBtn").removeAttr('href');	
		$("#LimitEnterBtn").attr('class','btn_disable');
		$("#LimitEnterBtn").css('color','gray');
		$("#LimitEnterBtn").unbind("click");
		
		$("#LimitExitBtn").removeAttr('href');
		$("#LimitExitBtn").attr('class','btn_disable');
		$("#LimitExitBtn").css('color','gray');
		$("#LimitExitBtn").unbind("click");
		
		ModeSet();
		$("#Tilt_Limit_Range").val(tiltLimitRange);
		ShowLimitUI(0);
		
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
	
	function LimitStartHandler(){
		$(this).removeAttr('href');
		$(this).attr('class','btn_disable');
		$(this).css('color','gray');
		$(this).unbind('click');
		
		$("#LimitEnterBtn").attr('href','#');
		$("#LimitEnterBtn").attr('class','btn_type01');
		$("#LimitEnterBtn").css('color','#fff');
		$("#LimitEnterBtn").bind("click", LimitEnterHandler);

		$("#LimitExitBtn").attr('href','#');	
		$("#LimitExitBtn").attr('class','btn_type01');
		$("#LimitExitBtn").css('color','#fff');
		$("#LimitExitBtn").bind("click", LimitEndHandler);

		ShowLimitUI(1);
		PtLimitRun($("#PanTiltLimit").val());
	}
	
	var isClickedEnter = false;
	function LimitEnterHandler(){
		if(isClickedEnter){				
			$(this).removeAttr('href');	
			$(this).attr('class','btn_disable');
			$(this).css('color','gray');
			$(this).unbind('click');		

			$("#LimitStartBtn").attr('href','#');
			$("#LimitStartBtn").attr('class','btn_type01');
			$("#LimitStartBtn").css('color','#fff');
			$("#LimitStartBtn").bind("click", LimitStartHandler); 		

			$("#LimitExitBtn").removeAttr('href');
			$("#LimitExitBtn").attr('class','btn_disable');
			$("#LimitExitBtn").css('color','gray');
			$("#LimitExitBtn").unbind('click');
			
			ShowLimitUI(0);
			isClickedEnter = false;
		}
		else{
			ShowLimitUI(2);
			isClickedEnter = true;
		}
		PtLimitRun(2);
	}

	function LimitEndHandler(){
		$(this).removeAttr('href');	
		$(this).attr('class','btn_disable');
		$(this).css('color','gray');
		$(this).unbind('click');			

		$("#LimitEnterBtn").removeAttr('href');	
		$("#LimitEnterBtn").attr('class','btn_disable');
		$("#LimitEnterBtn").css('color','gray');
		$("#LimitEnterBtn").unbind('click');	

		$("#LimitStartBtn").attr('href','#');
		$("#LimitStartBtn").attr('class','btn_type01');
		$("#LimitStartBtn").css('color','#fff');
		$("#LimitStartBtn").bind("click", LimitStartHandler);

		ShowLimitUI(0);
		PtLimitRun(3);
		isClickedEnter = false;
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
	}

	function ModeSet()
	{
		if ($("#PanTiltLimit").val() == 0) {
			$("#LimitEnable").val(panLimitVal);
		}
		else {
			$("#LimitEnable").val(tiltLimitVal);
		}
	}

	function LimitSet()
	{
		if($("#PanTiltLimit").val() == 0 ) {
			panLimitVal = $("#LimitEnable").val();
		}
		else {
			tiltLimitVal = $("#LimitEnable").val();
		}
		OnClickPTLimit();
	}

	function TiltRangeLimitSet()
	{
		tiltLimitRange =  $("#Tilt_Limit_Range").val();
		OnClickPTLimit();
	}

	function PropotionalModeSet()
	{
		propotionalPT = $("#propotionalMode").val();
		OnClickPTLimit();
	}

	function OnClickPTLimit()
	{
		var msg = "";
		msg += '<SetPTZLimit>';
		msg += '<Use>1</Use>';
		msg += '<PanLimit>'+panLimitVal+'</PanLimit>';
		msg += '<TiltLimit>'+tiltLimitVal+'</TiltLimit>';
		msg += '<TiltLimitRange>'+tiltLimitRange+'</TiltLimitRange>';
		msg += '<PropotionalMode>'+propotionalPT+'</PropotionalMode>';
		msg += '</SetPTZLimit>';
		RequestAjaxMsg(msg, "<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>","<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, "NO_REFRESH");
		localSeq++;
	}

	function PtLimitRun(param)
	{
		var msg = "";
		msg += "<StartPTZLimit>"
		msg += "<Cmd>"+param+"</Cmd>";
		msg += "</StartPTZLimit>";
		RequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, "NO_REFRESH");
		localSeq++;
	}

	function DrawLinHor( x, y, size, color, arrow){
		if (typeof arrow == "undefined")	arrow = 0;
		
		var str;
		if (x>=0 && y>=0 && size>0)
		{
			str = '<div id="LineHor" style="position:absolute; left:' + x + 'px; top:' + y + 'px;width:' + size + 'px; height:1px;background-color:' + color + '"><table height=1 width=' + size + '></table></div>\n';
			if (arrow == 1) // right
			{
				str += '<div id="LineHorArrow" style="position:absolute;left:' + (x+size-5) + 'px; top:' + (y-10) + 'px;width:10px;height:10px;background-color:transparent">&gt;</div>';
			}
			else if (arrow == 2) // left
			{
				str += '<div id="LineHorArrow" style="position:absolute;left:' + (x-size+22) + 'px; top:' + (y-10) + 'px;width:10px;height:10px;background-color:transparent">&lt;</div>';
			}
		} else {
			str = '';
		}
		$('#PtzLimitGuide').append(str);
	}

	function DrawLinVert( x, y, size, color){
		var str;
		if (x>=0 && y>=0 && size>0)
		{
			str = '<div id="LineVert" style="position:absolute; left:' + x + 'px; top:' + y + 'px;width:1px; height:' + size + 'px;background-color:' + color + '"><table height=' + size + ' width=1></table></div>\n';
		} else {
			str = '';
		}
		$('#PtzLimitGuide').append(str);
	}

	function DrawLine( x1, y1, x2, y2, color ){
		deltax=Math.abs(x2-x1);
		deltay=Math.abs(y2-y1);
		if (deltax>=deltay){
			if (y2<y1) {
				help=x1;
				x1=x2;
				x2=help;
				help=y1;
				y1=y2;
				y2=help;
			}

			deltax=x2-x1;
			deltay=y2-y1;
			dstep=deltax/(deltay+1);

			x=x1;
			if (dstep<0){
				x=x+dstep;
			}

			for (y=y1;y<=y2;y++){
				size=((x+dstep)-(x));
				if (dstep<0) {
					DrawLinHor( (x)-(dstep)+(size),(y),Math.abs(size),color );
				} else {
					DrawLinHor( (x),(y),Math.abs(size),color );
				}
				x=x+dstep;
			}
		}
		else {
			if (x2<x1) {
				help=x1;
				x1=x2;
				x2=help;
				help=y1;
				y1=y2;
				y2=help;
			}

			deltax=x2-x1;
			deltay=y2-y1;
			dstep=deltay/(deltax+1);

			y=y1;
			if (dstep<0){
				y=y+dstep;
			}

			for (x=x1;x<=x2;x++){
				size=((y+dstep)-(y))
				if (dstep<0){
					DrawLinVert( (x),(y)-(dstep)+(size),Math.abs(size),color );
				} else {
					DrawLinVert( (x),(y),Math.abs(size),color );
				}
				y=y+dstep;
			}
		}
	}

	function ShowLimitUI(mode)
	{
		var PanTiltMode = $("#PanTiltLimit").val();
		$("#PtzLimitGuide").empty();
		var divStr = "<span id='PtzLimitGuide_stepText'></span><?php for($i=0;$i<(<?php echo $GLOBALS['VIEWER_RESOLUTION']['height']; ?>/20);$i++) { ?><br/><?php } ?><span id='PtzLimitGuide_keyText'></span>"
		if (mode == 0)
		{
			$("#PtzLimitGuide").hide();
		}
		else if (mode == 1)
		{
			$("#PtzLimitGuide").show();
			$("#PtzLimitGuide").append(divStr);
			$("#PtzLimitGuide_stepText").text("Start Limit");
			$("#PtzLimitGuide_keyText").text("Enter : Set  Esc : Exit");

			DrawLinVert(320, (viewerHeight/2)-60, 150, "white");
			if (PanTiltMode == 0)
				DrawLinHor(320, viewerHeight/2, 30, "white", 1);
			else
				DrawLinHor(260, viewerHeight/2, 120, "white");
		}
		else if (mode == 2)
		{
			$("#PtzLimitGuide").show();
			$("#PtzLimitGuide").append(divStr);
			$("#PtzLimitGuide_stepText").text("End Limit");
			$("#PtzLimitGuide_keyText").text("Enter : Set  Esc : Exit");
			DrawLinVert(320, (viewerHeight/2)-60, 150, "white");
			if (PanTiltMode == 0)
				DrawLinHor(290, viewerHeight/2, 30, "white", 2);
			else
				DrawLinHor(260, viewerHeight/2, 120, "white");
		}
	}
	</script>
</head>

<body onload="OnLoad()" ononselectstart="return false">
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
					<h3 class="wid320"><?php echo $t_panTiltLimit[$GLOBALS["LANGINDEX"]]; ?></h3>
				</div>
				<table class="data_write">
					<colgroup>
						<col style="width:170px;" />
						<col />
					</colgroup>
					<tbody>
						<tr>
							<th><?php echo $t_mode[$GLOBALS["LANGINDEX"]]; ?></th>
							<td>
								<select id="PanTiltLimit" class="selectbox_style_wid250" onchange="ModeSet()">
									<option value="0"><?php echo $t_panLimit[$GLOBALS["LANGINDEX"]]; ?></option>
									<option value="1"><?php echo $t_tiltLimit[$GLOBALS["LANGINDEX"]]; ?></option>
								</select>
							</td>
						</tr>
						<tr>
							<th> <?php echo $t_use[$GLOBALS["LANGINDEX"]]; ?> </th>
							<td>
								<select id="LimitEnable" class="selectbox_style_wid250" onchange="LimitSet()">
									<option value="0"><?php echo $t_off[$GLOBALS["LANGINDEX"]]?></option>
									<option value="1"><?php echo $t_on[$GLOBALS["LANGINDEX"]]?></option>
				 				</select>
							</td>
						</tr>
						<tr>
							<th> <?php echo $t_tiltAngle[$GLOBALS["LANGINDEX"]]; ?></th>
							<td>
								<select id="Tilt_Limit_Range" class="selectbox_style_wid250" onchange="TiltRangeLimitSet()">
									<option value="1"> -5 ~ 185 </option>
									<option value="0"> -15 ~ 195 </option>
								</select>
							</td>
						</tr>
						<tr>
							<th> <?php echo $t_action[$GLOBALS["LANGINDEX"]]; ?> </th>
							<td>
								<a class="btn_type01" id="LimitStartBtn" type="button"><?php echo $t_start[$GLOBALS["LANGINDEX"]]; ?></a>
								<a class="btn_type01" id="LimitEnterBtn" type="button"><?php echo $t_enter[$GLOBALS["LANGINDEX"]]; ?></a>
								<a class="btn_type01" id="LimitExitBtn" type="button"><?php echo $t_exit[$GLOBALS["LANGINDEX"]]; ?></a>
							</td>
						</tr>
					</tbody>
				</table>
				<div class="h3_tit">
					<h3 class="wid320"><?php echo $t_proportionalPT[$GLOBALS["LANGINDEX"]]; ?></h3>
				</div>
				<table class="data_write">
					<colgroup>
						<col style="width:170px;" />
						<col />
					</colgroup>
					<tbody>
						<tr>
							<th><?php echo $t_mode[$GLOBALS["LANGINDEX"]]; ?></th>
							<td>
								<select id="propotionalMode" class="selectbox_style_wid250" onchange="PropotionalModeSet()">
									<option value="0" <?php if ($ptzlimit->dataInfo["PropotionalMode"]["value"] == 0) echo "selected=\"selected\""; ?>><?php echo $t_off[$GLOBALS["LANGINDEX"]]; ?></option>
									<option value="1" <?php if ($ptzlimit->dataInfo["PropotionalMode"]["value"] == 1) echo "selected=\"selected\""; ?>><?php echo $t_slow[$GLOBALS["LANGINDEX"]]; ?></option>
									<option value="2" <?php if ($ptzlimit->dataInfo["PropotionalMode"]["value"] == 2) echo "selected=\"selected\""; ?>><?php echo $t_normal[$GLOBALS["LANGINDEX"]]; ?></option>
									<option value="3" <?php if ($ptzlimit->dataInfo["PropotionalMode"]["value"] == 3) echo "selected=\"selected\""; ?>><?php echo $t_fast[$GLOBALS["LANGINDEX"]]; ?></option>
								</select>
							</td>
						</tr>
					</tbody>
				</table>
  			</div> <!-- end contents-->
		</div>
	</div>
</body>
</html>
