<?php
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_menu.cgi');
require_once ('../language/language_event_output.cgi');
$classInstances= GetClassInstance('relaySetting');
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="kr" xml:lang="kr">
<head>
	<title>iPOLiS NETWORK CAMERA WEBVIEWER</title>
	<meta http-equiv="X-UA-Compatible" content="IE=Edge; requiresActiveX=true">
	<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
	<link rel="stylesheet" type="text/css" href="../css/techwin.css" />
	<script type="text/javascript" src="../js/jquery-1.9.1.js"></script>
	<script type="text/javascript" src="../js/lnb.js"></script>
	<script type="text/javascript" src="../js/common_function.js"></script>
	<script type="text/javascript" language="javascript">
	<?php if ($GLOBALS['M_ALARMOUT_COUNT'] == 0) { ?>
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
	$(document).ready(function(){ lnbonoff("lnb_event"); });

	var oldDuration = new Array();	
	var alarmCnt = <?php echo $GLOBALS['M_ALARMOUT_COUNT']; ?>;

function OnClickApply()
{
  	var msg = "";
  	msg += "<SetRelaySetting>";
  	for (var index=0; index<alarmCnt; index++) {
  		msg += "<Outputlist"+index+">";
	  	msg += "<Mode>"+($('#pulse_'+index).is(':checked') ? 0 : 1)+"</Mode>";

		if($('#active_'+index).is(':checked')) { // active/inactive
	  		msg += "<Duration>0</Duration>";
	  	}
	  	else {
	  		msg += "<Duration>"+$('#output_duration_pulse_'+index).val()+"</Duration>";
	  	}
		msg += "<IdleState>"+($('#normal_open_'+index).is(':checked') ? 0 : 1)+"</IdleState>";
		msg += "</Outputlist"+index+">";
	}
  	msg += "</SetRelaySetting>";
	RequestAjaxMsg(msg, "<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $GLOBALS['REQUEST_URI'].'?seq='.$_SESSION['count'] ?>");
}

function OnClickOutputType(index)
{
	if($('#active_' + index).is(':checked') == 1) {
		oldDuration[index] = parseInt($('#output_duration_pulse_' + index).val());
		$('.output_duration_pulse_area_' + index).hide();
		$('.output_duration_active_area_' + index).show();
	}
	else {
		$('.output_duration_pulse_area_' + index).show();
		$('.output_duration_active_area_' + index).hide();
		if (oldDuration[index] == 0) oldDuration[index] = 15;	
		$('#output_duration_pulse_' + index).val(oldDuration[index]);
	}
}

function OnLoad() {}

	</script>
</head>

<body onload="OnLoad()" onselectstart="return false">
	<div id="wrap" >
		<?php
			require_once ('left_menu.cgi');
			require_once ('top_menu.cgi');
		?>
		<div id="container" >
		<?php
			PrintLeftMenu($_SERVER['SCRIPT_NAME']);
		?>
			<div id="contents">
		<?php
			for($index2=0; $index2<$GLOBALS['M_ALARMOUT_COUNT']; $index2++) {	
				$outputName = $t_alarmOutput[$GLOBALS['LANGINDEX']];
				if ($GLOBALS['M_ALARMOUT_COUNT'] > 1) {
					$outputName = $outputName.' '.($index2+1);
				}
		?>
				<div class="h3_tit mgt0" >
					<h3 class="wid220"><?php echo $outputName; ?></h3>
				</div>
				<table class="data_write" id="output_list">
					<colgroup>
						<col style="width:160px;" />
						<col style="width:160px;" />
						<col />
					</colgroup>
					<tbody>
						<tr>
							<th scope="row"><?php echo $t_type[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<label><input type="radio" name="output_type_<?php echo $index2; ?>" id="normal_open_<?php echo $index2; ?>" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" value="open" <?php if ($classInstances['RelayOutputConfiguration']->relayOutput[$index2]->dataInfo['IdleState']['value'] == 0) echo "checked=\"checked\""; ?> /><?php echo $t_normal_open[$GLOBALS['LANGINDEX']]; ?></label>
							</td>
							<td>
								<label><input type="radio" name="output_type_<?php echo $index2; ?>" id="normal_close_<?php echo $index2; ?>" value="close" <?php if ($classInstances['RelayOutputConfiguration']->relayOutput[$index2]->dataInfo['IdleState']['value'] == 1) echo "checked=\"checked\""; ?> /><?php echo $t_normal_close[$GLOBALS['LANGINDEX']]; ?></label>
							</td>
						</tr>
						<tr>
							<th colspan="3"> <?php echo $t_outputbutton[$GLOBALS['LANGINDEX']]; ?> </th>
						</tr>
						<tr>
							<td style="padding-left:20px"><?php echo $t_mode[$GLOBALS['LANGINDEX']]; ?></td>
							<td>
								<label><input type="radio" name="output_mode_<?php echo $index2; ?>" id="pulse_<?php echo $index2; ?>" value="pulse" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" onclick="OnClickOutputType(<?php echo $index2; ?>)" <?php if ($classInstances['RelayOutputConfiguration']->relayOutput[$index2]->dataInfo['Mode']['value'] == 0) echo "checked=\"checked\""; ?> /><?php echo $t_pulse[$GLOBALS['LANGINDEX']]; ?></label>
							</td>
							<td>
								<label><input type="radio" name="output_mode_<?php echo $index2; ?>" id="active_<?php echo $index2; ?>" value="active" onclick="OnClickOutputType(<?php echo $index2; ?>)" <?php if ($classInstances['RelayOutputConfiguration']->relayOutput[$index2]->dataInfo['Mode']['value'] == 1) echo "checked=\"checked\""; ?> /><?php echo $t_active_inactive[$GLOBALS['LANGINDEX']]; ?></label>
							</td>
						</tr>
						<tr>
							<td style="padding-left:20px"><?php echo $t_duration[$GLOBALS['LANGINDEX']]; ?></td>
							<td>
								<div class="output_duration_pulse_area_<?php echo $index2; ?>" <?php if ($classInstances['RelayOutputConfiguration']->relayOutput[$index2]->dataInfo['Mode']['value'] == 1) echo "style=\"display:none\""; ?> >
									<select name="select" id="output_duration_pulse_<?php echo $index2; ?>" class="selectbox_style">
									<?php
										for ($index=1; $index<=15; ++$index) {
									?>
										<option value="<?php echo $index; ?>" <?php if ($classInstances['RelayOutputConfiguration']->relayOutput[$index2]->dataInfo['Duration']['value'] == $index) echo " selected=\"selected\""; ?>><?php echo $index;?> <?php echo $t_seconds[$GLOBALS['LANGINDEX']]; ?></option>
		  							<?php
		  								}
		  							?>
									</select>
								</div>
								<div class="output_duration_active_area_<?php echo $index2; ?>" <?php if ($classInstances['RelayOutputConfiguration']->relayOutput[$index2]->dataInfo['Mode']['value'] == 0) echo "style=\"display:none\""; ?> >
									<select name="select" id="output_duration_active_<?php echo $index2; ?>" class="selectbox_style" disabled="disabled">
										<option value="0" selected="selected"><?php echo $t_always[$GLOBALS['LANGINDEX']];?></option>
									</select>
								</div>
							</td>
						</tr>
					</tbody>
				</table>		
				<script>
					oldDuration[<?php echo $index2; ?>] = <?php echo $classInstances['RelayOutputConfiguration']->relayOutput[$index2]->dataInfo['Duration']['value']; ?>;
				</script>
			<?php
				if ($index2 != ($GLOBALS['M_ALARMOUT_COUNT']-1)) {
			?>
					<br/>
			<?php 
				}
			}
		?>
				<div class="btn_right">
					<a id="mid_ok_btn" class="btn_apply" href="javascript:OnClickApply()"><?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?></a>
				</div>
			</div>
		</div>
	</div>
</body>
</html>
