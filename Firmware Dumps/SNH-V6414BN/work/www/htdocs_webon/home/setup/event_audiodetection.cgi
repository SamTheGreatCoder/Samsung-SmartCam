<?php
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_menu.cgi');
require_once ('../language/language_event_common.cgi');
require_once ('../language/language_event_audiodetection.cgi');

$event_name 	= 'ad';
$classInstances= GetClassInstance($event_name);
$event_class	= $classInstances['ADConfiguration'];
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
	<link rel="stylesheet" type="text/css" href="../css/jquery.ui.theme.css"/>
	<link rel="stylesheet" type="text/css" href="../css/event_canvas.css" />
	
	<style>
		#lnb-list {
			height:1000px;
		}
	</style>
	<script type="text/javascript" src="../js/jquery-1.9.1.js"></script>
	<script type="text/javascript" src="../js/lnb.js"></script>
	<script type="text/javascript" src="../js/common_function.js"></script>
	<script type="text/javascript" src="../js/jquery-ui.js"></script>
	<script type="text/javascript" src="../js/jquery.ui.dialog.js"></script>
	<script type="text/javascript" src="../js/timeSchedule.js"></script>
	<script type="text/javascript" src="../js/eventcontrol.js"></script>
	<script type="text/javascript" language="javascript">
	<?php if (!$GLOBALS['M_SUPPORT_EVENT_AD']) { ?>
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

	var gTimerAD = "";
	var gReqCount = 1;
	var gCurPlayStatus = 0;
	var gCurThreadsHoldVal = 0;
	var lastSeqOfLevel = 0;
	var adSeqArray = new Array(5);
	var adLevelArray = new Array(5);
	
	$(document).ready(function(){
		lnbonoff("lnb_event");

		$("#slider-vertical").slider({
			orientation: "vertical",
			range: "min",
			min: 1,
			max: 100,
			value: <?php echo $event_class->dataInfo['Sensitivity']['value']; ?>,
			slide: function(event, ui) {
				if (ui.value < 1) {
					ui.value = 1;
				}
				$("#event_<?php echo $event_name; ?>_sensitivity").val(ui.value);
				$("#ad_threadshold_bar").animate({
					marginTop : 100-ui.value+"px"
				}, 0);
				gCurThreadsHoldVal = ui.value;
			},
			change : function (event, ui) {
				ChangeGraphColorAsThreadhold();
			}
		});
		$("#event_<?php echo $event_name; ?>_sensitivity").val(parseInt($("#slider-vertical").slider("value")));
		$("#ad_threadshold_bar").animate({
			marginTop : (100-parseInt($("#event_<?php echo $event_name; ?>_sensitivity").val()))+"px"
		}, 0);
		gCurThreadsHoldVal = parseInt($("#event_<?php echo $event_name; ?>_sensitivity").val());
	});
	
	function OnClickApply()
	{
		if (CheckScheduleSetting("<?php echo $event_name; ?>") == 0) {
			alert("<?php echo $msg_checkthetable[$GLOBALS['LANGINDEX']]; ?>");
			return; 
		}
			
		if (!(parseInt($('#event_<?php echo $event_name; ?>_sensitivity').val()) > 0 && parseInt($('#event_<?php echo $event_name; ?>_sensitivity').val()) < 101)) {
			alert("<?php echo $msg_check_level[$GLOBALS['LANGINDEX']]; ?>");
			return;
		}

		var msg = '';
		msg += "<SetADConfiguration>";
		msg += "<Enabled>"+($("#event_<?php echo $event_name; ?>_use_on").is(':checked') ? 1 : 0 )+"</Enabled>";
		msg += "<Sensitivity>"+$("#event_<?php echo $event_name; ?>_sensitivity").val()+"</Sensitivity>";
		<?php if($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>	
		msg += MakeScheduleAndActionSetupXML_S1("<?php echo $event_name; ?>");
		<?php } else { ?>
		msg += MakeScheduleAndActionSetupXML("<?php echo $event_name; ?>");
		<?php } ?>
		msg += "</SetADConfiguration>";
		RequestAjaxMsg(msg, "<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $GLOBALS['REQUEST_URI'].'?seq='.$_SESSION['count'] ?>");
	}

	function GetADLevel(data)
	{
		var dataArr = data.split(" ");
		var val = '';
		var curLevel = 0;
		var isDetect = false;
		for (var index=0; index<5; ++index) {
			val = dataArr[index].split(":");
			adSeqArray[index] = val[0];
			if (val[1] > 100) val[1] = 100;
			if (val[1] < 0) 	val[1] = 0;
			adLevelArray[index] = val[1];
			if (parseInt(gCurThreadsHoldVal) - adLevelArray[index] <= 0 && lastSeqOfLevel < adSeqArray[index]) {
				isDetect = true;
				lastSeqOfLevel = adSeqArray[index];
				curLevel = adLevelArray[index];
				break;
			}
		}

		if (isDetect == false) {
			lastSeqOfLevel = adSeqArray[4];
			curLevel = adLevelArray[4];
		}

		return curLevel;
	}

	function RequestADStatus()
	{
		var reqUrl = "<?php echo GetMyRequestURI($_SERVER['SCRIPT_NAME']); ?>";
		reqUrl = reqUrl.replace("home/setup/event_audiodetection.cgi", "cgi-bin/control.cgi");
		if (BrowserDetect.browser == "Explorer" || (BrowserDetect.browser == 'Safari' && reqUrl.search('.local') != -1)) {
			reqUrl = "../.."+reqUrl.substr(reqUrl.indexOf("/cgi-bin/"));
		}
		$.ajax({
			type: "GET",
			dataType: "text",
			url: reqUrl,
			data: "msubmenu=adlevel&action=check&pctz="+(new Date()).getTime(),
			success: OnSuccessADResult,
			error: OnFailADResult,
			timeout: OnFailADResult
		});
	}

	function OnFailADResult(req)
	{
		gCurPlayStatus = 0;
		clearInterval(gTimerAD);
	}

	function OnSuccessADResult(req)
	{
		if (parseInt(gReqCount) >= 160) {
			$("#ad_graph_table tr:first > td:first").remove();
		}
		else {
			$("#ad_graph_table tr:first > td:first").width(480-((parseInt(gReqCount))*3));
		}

		var colorVal = GetADLevel(req);
		var imsgSrc = '../images/common/leveBarOn.png';

		// detection audio
		if (parseInt(gCurThreadsHoldVal) > colorVal) imsgSrc = '../images/common/leveBarOff.png';

		$("#ad_graph_table tr:first > td:last").after(
			"<td>\
				<img src='"+imsgSrc+"' width='3' height='"+colorVal+"' style='margin-top:"+(100-colorVal)+"px'/>\
			</td>"
		);
		gReqCount++;
	}

	function ChangeGraphColorAsThreadhold()
	{
		$("#ad_graph_table tr:first > td").each(function() {
			var oldColorHeight = $(this).children().attr('height');
			if (oldColorHeight == null) return;
			if (parseInt(gCurThreadsHoldVal) > parseInt(oldColorHeight)) {	// down threadhold
				$(this).children().attr('src', '../images/common/leveBarOff.png');
			}
			else {	// up threadhold
				$(this).children().attr('src', '../images/common/leveBarOn.png');
			}
		});
	}

	function OnClickThreadHoldPlusOrMinus(type)
	{
		if (type == 'plus') {
			gCurThreadsHoldVal = parseInt(gCurThreadsHoldVal) + 1;
		}
		else {
			gCurThreadsHoldVal = parseInt(gCurThreadsHoldVal) - 1;
		}
		if (parseInt(gCurThreadsHoldVal) > 100) gCurThreadsHoldVal = 100;
		if (parseInt(gCurThreadsHoldVal) < 1) gCurThreadsHoldVal = 1;
		MoveSlider();
	}

	function OnKeyDownAdThreadshold(event)
	{
		var keyCode;
		if (window.event) {  //ie,crome, safari
			keyCode = event.keyCode;
		}
		else {  //firefox
			keyCode = event.which;
		}

		if (keyCode == 13) {
			if (parseInt($('#event_<?php echo $event_name; ?>_sensitivity').val()) < 1 || parseInt($('#event_<?php echo $event_name; ?>_sensitivity').val()) > 100) return;
			gCurThreadsHoldVal = $('#event_<?php echo $event_name; ?>_sensitivity').val();
			MoveSlider();
		}
	}

	function MoveSlider()
	{
		$("#event_<?php echo $event_name; ?>_sensitivity").val(gCurThreadsHoldVal);
		$("#slider-vertical").slider("option", "value", gCurThreadsHoldVal);
		$("#ad_threadshold_bar").animate({
			marginTop : parseInt(100-gCurThreadsHoldVal)+"px"
		}, 0);
		ChangeGraphColorAsThreadhold();
	}

	function OnLoad() 
	{
		gCurPlayStatus = 1;
		gTimerAD = setInterval('RequestADStatus()', 400);
	}

		</script>
	</head>
	<body onload="OnLoad()" onselectstart="return false">
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
				<div class="h3_tit mgt0">
					<h3 class="wid320"><?php echo $menu_audiodetection[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>
				<table class="data_write" >
					<colgroup>
						<col style="width:100px;"/>
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
				<table style="width:670px; height:100px; margin-top:10px; margin-left:10px" border=0>
					<colgroup>
						<col style="width:100px;"/>
						<col style="width:480px;"/>
						<col style="width:20px;"/>
						<col style="width:30px;"/>
						<col style="width:30px;"/>
					</colgroup> 
					<tr>
						<th style="vertical-align:top; text-align:left"><?php echo $t_level[$GLOBALS['LANGINDEX']]; ?></th>
						<td>
							<img id="ad_threadshold_bar" src="../images/common/ad_bar.png" alt="" width="480px" style="height:1px; position: absolute" />
							<div style="width:480px; height:100px; background-color:#666f7a">
								<table id="ad_graph_table">
									<tbody>
										<tr>
											<td width="480px"></td>
										</tr>
									</tbody>
								</table>
							</div>
						</td>
						<td><img src="../images/setup/ad_levelbar.png" ></td>
						<td align="left">
							<div id="slider-vertical" style="height:100px; margin-left:6px"></div>
						</td>
						<td style="vertical-align:bottom;" align="left">
							<input type="text" class="text" id="event_<?php echo $event_name; ?>_sensitivity" maxlength="3" style="width:25px; padding-left:5px" onKeyPress='return IsNum(event)' onKeyDown="OnlyNUm(event); OnKeyDownAdThreadshold(event);" />
						</td>
					</tr>
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


