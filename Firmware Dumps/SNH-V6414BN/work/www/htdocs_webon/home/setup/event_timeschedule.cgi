<?php
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_menu.cgi');
require_once ('../language/language_event_common.cgi');
require_once ('../language/language_event_timeschedule.cgi');

$event_name 	= 'timesched';
$classInstances= GetClassInstance($event_name);
$event_class	= $classInstances['TimeScheduleConfiguration'];

$intervalTime = 0;
$intervalUnit = 0;
$interval = $event_class->dataInfo['Interval']['value'];
if ($interval/600 <= 1) {
	$intervalUnit = 10;
	$intervalTime = $interval/10;
}
else {
	$intervalUnit = 600;
	$intervalTime = $interval/600;
}
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
	
	<script type="text/javascript" src="../js/jquery-1.9.1.js"></script>
	<script type="text/javascript" src="../js/lnb.js"></script>
	<script type="text/javascript" src="../js/common_function.js"></script>
	<script type="text/javascript" src="../js/jquery-ui.js"></script>
	<script type="text/javascript" src="../js/jquery.ui.dialog.js"></script>
	<script type="text/javascript" src="../js/timeSchedule.js"></script>
	<script type="text/javascript" src="../js/eventcontrol.js"></script>
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
	$(document).ready(function(){
		lnbonoff("lnb_event");
	});
	
	function OnClickApply()
	{
		if (CheckScheduleSetting("<?php echo $event_name; ?>") == 0) {
			alert("<?php echo $msg_checkthetable[$GLOBALS['LANGINDEX']]; ?>");
			return; 
		} 
		var msg = '';
		msg += "<SetTimeSchedule>";
		msg += "<Enabled>"+($("#event_<?php echo $event_name; ?>_use_on").is(':checked') ? 1 : 0 )+"</Enabled>";
		msg += "<Interval>"+parseInt($('#event_<?php echo $event_name; ?>_interval').val()) * parseInt($('#event_<?php echo $event_name; ?>_interval_unit').val()) +"</Interval>";
		<?php if($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>	
		msg += MakeScheduleAndActionSetupXML_S1("<?php echo $event_name; ?>");
		<?php } else { ?>		
		msg += MakeScheduleAndActionSetupXML("<?php echo $event_name; ?>");
		<?php } ?>
		msg += "</SetTimeSchedule>";
		RequestAjaxMsg(msg, "<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $GLOBALS['REQUEST_URI'].'?seq='.$_SESSION['count'] ?>");
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
					<h3 class="wid320"><?php echo $t_timerSetup[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>
				<table class="data_write" >
					<colgroup>
						<col style="width:180px;"/>
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
				<div class="h3_tit" style='overflow:auto;width:100%'>
					<h3 class="wid220"><?php echo $t_transferInterval[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>
				<table class="data_write" >
					<colgroup>
						<col style="width:180px;" />
						<col />
					</colgroup>
					<tbody>
						<tr>
							<th scope="row"><?php echo $t_oneImagePer[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<select name="select" id="event_<?php echo $event_name; ?>_interval" class="selectbox_style" style="width:46px; margin-right:10px">
					        		<option value="5"  <?php if ($intervalTime == 5)  echo "selected=\"selected\""; ?> >5</option>
									<option value="10" <?php if ($intervalTime == 10) echo "selected=\"selected\""; ?> >10</option>
									<option value="15" <?php if ($intervalTime == 15) echo "selected=\"selected\""; ?> >15</option>
									<option value="30" <?php if ($intervalTime == 30) echo "selected=\"selected\""; ?> >30</option>
				           		<option value="45" <?php if ($intervalTime == 45) echo "selected=\"selected\""; ?> >45</option>
				           		<option value="60" <?php if ($intervalTime == 60) echo "selected=\"selected\""; ?> >60</option>
				      		</select>
				      		<select name="select" id="event_<?php echo $event_name; ?>_interval_unit" class="selectbox_style" style="width:180px">
				           		<option value="10" <?php if ($intervalUnit == 10)  echo "selected=\"selected\""; ?> ><?php echo $t_seconds[$GLOBALS['LANGINDEX']]; ?></option>
				           		<option value="600" <?php if ($intervalUnit == 600)  echo "selected=\"selected\""; ?> ><?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
				   			</select>
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
