<?php
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_menu.cgi');
require_once ('../language/language_event_common.cgi');
require_once ('../language/language_event_alarminput.cgi');

$alarmIndex 	= 0;
if (isset($_REQUEST['inputNo'])) {
	$alarmIndex 	= $_REQUEST['inputNo'];
}
$event_name 	= 'alarm';
$classInstances= GetClassInstance($event_name);
$event_class	= $classInstances['SensorConfiguration']->alarmInput[$alarmIndex];
$dnMode = $classInstances['Information']->dataInfo['DayNightMode']['value'];
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="kr" xml:lang="kr">
<head>
	<title>iPOLiS NETWORK CAMERA WEBVIEWER</title>
	<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
	<meta http-equiv="X-UA-Compatible" content="IE=Edge; requiresActiveX=true" />
	<link rel="stylesheet" type="text/css" href="../css/techwin.css" />
	<link rel="stylesheet" type="text/css" href="../css/jquery.ui.core.css"/>
	<link rel="stylesheet" type="text/css" href="../css/jquery.ui.theme.css"/>
	<link rel="stylesheet" type="text/css" href="../css/event_canvas.css" />
	<style>
		#lnb-list {
			height:900px;
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
	<?php if ($GLOBALS['M_ALARMIN_COUNT'] == 0 || $dnMode == 3) { ?>
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
	$(document).ready(function(){
		lnbonoff("lnb_event");;
	});
	
	function OnClickApply()
	{
		if (CheckScheduleSetting("<?php echo $event_name; ?>") == 0) {
			alert("<?php echo $msg_checkthetable[$GLOBALS['LANGINDEX']]; ?>");
			return; 
		} 
		var msg = '';
		msg += "<SetAlarmInput>";
		msg += "<AlarmInput>";
		msg += "<No><?php echo $alarmIndex+1; ?></No>";
		msg += "<Enabled>"+($("#event_<?php echo $event_name; ?>_use_on").is(':checked') ? 1 : 0 )+"</Enabled>";
		msg += "<Type>"+($("#event_<?php echo $event_name; ?>_type_nc").is(':checked') ? 1 : 0 )+"</Type>";		
		<?php if($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>	
		msg += MakeScheduleAndActionSetupXML_S1("<?php echo $event_name; ?>");
		<?php } else { ?>
		msg += MakeScheduleAndActionSetupXML("<?php echo $event_name; ?>");
		<?php } ?>	
		msg += "</AlarmInput>";
		msg += "</SetAlarmInput>";
		RequestAjaxMsg(msg, "<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $GLOBALS['REQUEST_URI'].'?seq='.$_SESSION['count'] ?>");
	}

	function OnChangeAlarmInputNo()
	{
		document.location = "event_alarminput.cgi?inputNo="+$("#alarmInputNo").val();
	}

	function OnLoad() {}

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
		<?php
			if ($GLOBALS['M_ALARMIN_COUNT'] > 1) {
		?>
					<h3 class="wid320"><?php echo $t_alarmInputNo[$GLOBALS['LANGINDEX']]; ?>	</h3> 		
				</div>	
				<table style="position:absolute; top:113px;">
					<colgroup>
						<col style="width:200px;"/>
						<col />
					</colgroup>
					<tbody>
						<tr>
							<td></td>
							<td>
							<select id="alarmInputNo" class="selectbox_style" onChange="OnChangeAlarmInputNo()" style="width:50px">
						<?php
							for ($index=0; $index<$GLOBALS['M_ALARMIN_COUNT']; ++$index) {
						?>
								<option value="<?php echo $index; ?>" <?php if ($alarmIndex == $index) echo "selected=\"selected\"";?>><?php echo $index+1; ?></option>
						<?php
							}
						?>
							</select>
							</td>
						</tr>
					</tbody>
				</table>
				<div class="h3_tit">
		<?php
			}
		?>
					<h3 class="wid320"><?php echo $t_inputDeviceSetup[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>
				<table class="data_write" >
					<colgroup>
						<col style="width:190px;"/>
						<col style="width:170px;"/>
						<col />
					</colgroup>
					<tbody>
						<tr>
							<th scope="row"><?php echo $t_enable[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<label><input type="radio" name="event_<?php echo $event_name; ?>_use" id="event_<?php echo $event_name; ?>_use_on"  <?php if ($event_class->dataInfo['Enabled']['value'] == 1) echo "checked=\"checked\""; ?> style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_on[$GLOBALS['LANGINDEX']]; ?></label>
							</td>
							<td>
								<label><input type="radio" name="event_<?php echo $event_name; ?>_use" id="event_<?php echo $event_name; ?>_use_off" <?php if ($event_class->dataInfo['Enabled']['value'] == 0) echo "checked=\"checked\""; ?> /><?php echo $t_off[$GLOBALS['LANGINDEX']]; ?></label>
							</td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_type[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<label style="margin-right: 0px;"><input type="radio" name="event_<?php echo $event_name; ?>_type" id="event_<?php echo $event_name; ?>_type_no" <?php if ($event_class->dataInfo['Type']['value'] == 0) echo "checked=\"checked\""; ?> style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_normal_open[$GLOBALS['LANGINDEX']]; ?></label>
							</td>
							<td>
								<label><input type="radio" name="event_<?php echo $event_name; ?>_type" id="event_<?php echo $event_name; ?>_type_nc" <?php if ($event_class->dataInfo['Type']['value'] == 1) echo "checked=\"checked\""; ?> /><?php echo $t_normal_close[$GLOBALS['LANGINDEX']]; ?></label>
							</td>
						</tr>
					</tbody>
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
