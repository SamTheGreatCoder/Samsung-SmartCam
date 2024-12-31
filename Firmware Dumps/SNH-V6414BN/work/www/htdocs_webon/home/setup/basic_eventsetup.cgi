<?php
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_menu.cgi');
require_once ('../language/language_event_setup.cgi');

$classInstances= GetClassInstance('event_list');
$eventConf		= $classInstances['EventConfiguration'];
$event_class 	= array();
$dnMode = $classInstances['Information']->dataInfo['DayNightMode']['value'];

$presetValues 	= array($t_off[$GLOBALS['LANGINDEX']]);
for ($index=1; $index<=$GLOBALS['M_PRESET_COUNT']; ++$index) $presetValues[$index] = $index;
$event_list 	= array('alarm0','alarm1','alarm2','alarm3', 'timesched', 'tampering', 'md','va', 'fd', 'ad', 'netdiscon', 'trackingEvent', 'opensdk');
$event_index 	= array('alarm0'=>0, 'alarm1'=>1, 'alarm2'=>2, 'alarm3'=>3, 'md'=>4, 'va'=>5, 'timesched'=>6, 'netdiscon'=>7, 'fd'=>8, 'tampering'=>9, 'ad'=>10, 'trackingEvent'=>11,'opensdk'=>12);
$event_lang 	= array('alarm0'=>$t_alarm, 'md'=>$t_md, 'va'=>$t_md_va, 'timesched'=>$t_timesched, 'netdiscon'=>$t_netdiscon, 'fd'=>$t_fd, 'tampering'=>$t_tampering, 'ad'=>$t_ad, 'trackingEvent'=>$t_ptzTracking, 'opensdk'=>$t_appevent);
if ($GLOBALS['M_SPECIAL_TYPE'] == 1)
{
	// DEV_S1SMS
	$action_list 	= array('enable', 'ftp', 'email', 'sms', 'output0', 'output1', 'output2', 'output3','preset');
	$action_info 	= array('enable'=>'Enabled', 'output0'=>'RelayOutput0', 'output1'=>'RelayOutput1', 'output2'=>'RelayOutput2', 'output3'=>'RelayOutput3', 'ftp'=>'FTPSending', 'email'=>'SMTPSending', 'record'=>'Record', 'preset'=>'GotoPreset', 'sms'=>'SMSSending');
}
else
{
	$action_list 	= array('enable', 'ftp', 'email', 'record', 'output0', 'output1', 'output2', 'output3','preset');
	$action_info 	= array('enable'=>'Enabled', 'output0'=>'RelayOutput0', 'output1'=>'RelayOutput1', 'output2'=>'RelayOutput2', 'output3'=>'RelayOutput3', 'ftp'=>'FTPSending', 'email'=>'SMTPSending', 'record'=>'Record', 'preset'=>'GotoPreset');
}

$event_class 	= array('alarm'=>'Sensor', 'md'=>'MD', 'va'=>'VA', 'timesched'=>'TimeSchedule', 'netdiscon'=>'NetworkDisconnect', 'fd'=>'FD', 'tampering'=>'Tampering', 'ad'=>'AD', 'trackingEvent'=>'Tracking','opensdk'=>'OpenSDK');
if ($GLOBALS['M_SPECIAL_TYPE'] == 1)
{
	// DEV_S1SMS
$action_lang 	= array(	'enable'	=>array($t_off[$GLOBALS['LANGINDEX']], $t_on[$GLOBALS['LANGINDEX']]),
								'output'	=>array($t_off[$GLOBALS['LANGINDEX']], $t_always[$GLOBALS['LANGINDEX']], '5 '.$t_sec[$GLOBALS['LANGINDEX']], '10 '.$t_sec[$GLOBALS['LANGINDEX']], '15 '.$t_sec[$GLOBALS['LANGINDEX']]),
								'ftp'		=>array($t_off[$GLOBALS['LANGINDEX']], $t_on[$GLOBALS['LANGINDEX']]),
								'email'	=>array($t_off[$GLOBALS['LANGINDEX']], $t_on[$GLOBALS['LANGINDEX']]),
									'preset'	=>$presetValues,
									'sms'		=>array($t_off[$GLOBALS['LANGINDEX']], $t_on[$GLOBALS['LANGINDEX']]));
}
else
{
	$action_lang 	= array(	'enable'	=>array($t_off[$GLOBALS['LANGINDEX']], $t_on[$GLOBALS['LANGINDEX']]),
									'output'	=>array($t_off[$GLOBALS['LANGINDEX']], $t_always[$GLOBALS['LANGINDEX']], '5 '.$t_sec[$GLOBALS['LANGINDEX']], '10 '.$t_sec[$GLOBALS['LANGINDEX']], '15 '.$t_sec[$GLOBALS['LANGINDEX']]),
									'ftp'		=>array($t_off[$GLOBALS['LANGINDEX']], $t_on[$GLOBALS['LANGINDEX']]),
									'email'	=>array($t_off[$GLOBALS['LANGINDEX']], $t_on[$GLOBALS['LANGINDEX']]),
									'record'	=>array($t_off[$GLOBALS['LANGINDEX']], $t_on[$GLOBALS['LANGINDEX']]),
									'preset'	=>$presetValues);
}

if (!$GLOBALS['M_SUPPORT_EVENT_ND']) 						ArrayPop($event_list, 'netdiscon');
if (!$GLOBALS['M_SUPPORT_EVENT_FD'])							ArrayPop($event_list, 'fd');
if (!$GLOBALS['M_SUPPORT_EVENT_TD'])							ArrayPop($event_list, 'tampering');
if (!$GLOBALS['M_SUPPORT_EVENT_AD']) 						ArrayPop($event_list, 'ad');
if (!($GLOBALS['M_SUPPORT_EVENT_VA'] & IV_SUPPORT))		ArrayPop($event_list, 'va');
else 																	ArrayPop($event_list, 'md');
if (!$GLOBALS['M_SUPPORT_PTZ_TRACKING'])				ArrayPop($event_list, 'trackingEvent');
if (!$GLOBALS['M_SUPPORT_OPENSDK'])				ArrayPop($event_list, 'opensdk');

for ($index = 3; $index >= $GLOBALS['M_ALARMOUT_COUNT'] ; $index-- ) {
	ArrayPop($action_list, 'output'.$index);
	unset($action_info[array_search('output'.$index, $action_info)]);
}

for ($index = 3; $index >= $GLOBALS['M_ALARMIN_COUNT'] ; $index-- ) {
	ArrayPop($event_list, 'alarm'.$index);
}

if($dnMode == 3) {	
	for ($index = 0; $index <$GLOBALS['M_ALARMIN_COUNT']; $index++)	 {
		ArrayPop($event_list, 'alarm'.$index);		
	}
}

for ($index = 1; $index <$GLOBALS['M_ALARMIN_COUNT']; $index++)
	$event_lang['alarm'.$index]=$t_alarm;

if (!($GLOBALS['M_SUPPORT_SD'] || $GLOBALS['M_SUPPORT_NAS']) && $GLOBALS['M_SPECIAL_TYPE'] != 1) 		ArrayPop($action_list, 'record');
if (!($GLOBALS['M_SUPPORT_PTZ'] || $GLOBALS['M_SUPPORT_EXTERNAL_PTZ']))	ArrayPop($action_list, 'preset');
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="kr" xml:lang="kr">
<head>
	<title>iPOLiS NETWORK CAMERA WEBVIEWER</title>
	<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
	<meta http-equiv="X-UA-Compatible" content="IE=Edge; requiresActiveX=true" />
	<link rel="stylesheet" type="text/css" href="../css/techwin.css" />
	<script type="text/javascript" src="../js/jquery-1.9.1.js"></script>
	<script type="text/javascript" src="../js/lnb.js"></script>
	<script type="text/javascript" src="../js/common_function.js"></script>
	<script type="text/javascript" src="../js/jquery-ui.js"></script>
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
	var reqUrl = "<?php echo GetMyRequestURI($_SERVER['SCRIPT_NAME']); ?>";

	$(document).ready(function(){
		lnbonoff("lnb_basic");
	});
	
	function OnClickApply()
	{
		var msg = "<SetEventConfiguration>";
	<?php
		foreach ($event_list as $eventType) {
	?>
			<?php if(substr($eventType, 0, 5) == 'alarm') {?>
				msg += "<?php echo '<'.$event_class[substr($eventType, 0, 5)].substr($eventType, -1).'>'; ?>";
			<?php } else { ?>
				<?php if($eventType == 'va'){ ?>
					msg += "<MD>";
						msg += "<Enabled>"+ ($("#event_va_enable").is(':checked') ? 1 : 0 ) +"</Enabled>";
					msg += "</MD>";
				<?php } ?>			
				msg += "<?php echo '<'.$event_class[$eventType].'>'; ?>";
			<?php } ?>
	<?php
			foreach ($action_list as $actionType) {

				if(substr($actionType, 0, 6) == 'output' || $actionType == 'preset') {
	?>
					msg += "<?php echo '<'.$action_info[$actionType].'>'; ?>"+$("#event_<?php echo $eventType.'_'.$actionType; ?>").val()+"<?php echo '</'.$action_info[$actionType].'>'; ?>";
	<?php
				}
				else {
	?>
					msg += "<?php echo '<'.$action_info[$actionType].'>'; ?>"+($("#event_<?php echo $eventType.'_'.$actionType; ?>").is(':checked') ? 1 : 0 )+"<?php echo '</'.$action_info[$actionType].'>'; ?>";
	<?php
				}
			}
	?>
			
			<?php if(substr($eventType, 0, 5) == 'alarm') {?>
				msg += "<?php echo '</'.$event_class[substr($eventType, 0, 5)].substr($eventType, -1).'>'; ?>";
			<?php } else { ?>
				msg += "<?php echo '</'.$event_class[$eventType].'>'; ?>";
			<?php } ?>
	<?php
		}
	?>
		msg += "</SetEventConfiguration>"
		RequestAjaxMsg(msg, "<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $GLOBALS['REQUEST_URI'].'?seq='.$_SESSION['count'] ?>");
	}

	function OnClickEventType(eventName)
	{
			var eventSrc = {	'alarm0':'alarminput.cgi?inputNo=0',
				'alarm1':'alarminput.cgi?inputNo=1',
				'alarm2':'alarminput.cgi?inputNo=2',
				'alarm3':'alarminput.cgi?inputNo=3',
				'timesched':'timeschedule.cgi',
				'tampering':'tamperingdetection.cgi',
				'md':'videoanalytics.cgi',
				'va':'videoanalytics.cgi', 
				'fd':'facedetection.cgi', 
				'ad':'audiodetection.cgi', 
				'netdiscon':'networkdisconnect.cgi', 
				'trackingEvent':'ptztracking.cgi',
				'opensdk':'appevent.cgi'};
		
					document.location = "event_"+eventSrc[eventName];
	}
	
	function OnLoad() {}

		</script>
	</head>
	<body onload="OnLoad()" onunload="" onselectstart="return false">
		<div id="wrap">
		<?php
			require_once ('left_menu.cgi');
			require_once ('top_menu.cgi');
		?>
		<div id="container" style="width:1400px;">
		<?php
			PrintLeftMenu($_SERVER['SCRIPT_NAME']);
		?>
			<div id="contents"  style="width:680px;">
				<div class="h3_tit mgt0" style="overflow:auto;width:880px;">
					<h3 class="wid320"><?php echo $t_eventList[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>
				<table class="data_table" border="0" style="width:880px;overflow:auto;">
					<colgroup>
						<col style="width:20px;" />
						<col style="width:120px;" />
						<col style="width:100px;" />
				<!--
						<col style="width:100px;" />		// Output
						<col style="width:100px;" />		// FTP
						<col style="width:100px;" />		// E-mail
						<col style="width:100px;" />		// Record
						<col style="width:100px;" />		// Preset
				-->
				<?php
					if ($GLOBALS['M_SPECIAL_TYPE'] == 1)
					{
						// DEV_S1SMS
						$maxCol = 6;
					}
					else
					{
						$maxCol = 5;
					}
					if ($GLOBALS['M_ALARMOUT_COUNT'] == 0) 	$maxCol--;
					if ($GLOBALS['M_ALARMOUT_COUNT'] > 1) 	$maxCol += $GLOBALS['M_ALARMOUT_COUNT'] -1;
					if (!($GLOBALS['M_SUPPORT_SD'] || $GLOBALS['M_SUPPORT_NAS']) && $GLOBALS['M_SPECIAL_TYPE'] != 1) 	$maxCol--;
					if (!($GLOBALS['M_SUPPORT_PTZ'] || $GLOBALS['M_SUPPORT_EXTERNAL_PTZ']))		$maxCol--;
					for($index=0; $index<$maxCol; ++$index)
						echo "<col />";
				?>

					</colgroup>
					<thead>
						<tr>
							<th colspan="2"><?php echo $t_type[$GLOBALS['LANGINDEX']]; ?></th>
							<th><?php echo $t_enable[$GLOBALS['LANGINDEX']]; ?></th>

							<th>FTP</th>
							<th><?php echo $t_email[$GLOBALS['LANGINDEX']]; ?></th>
					<?php
					if ($GLOBALS['M_SPECIAL_TYPE'] == 1)
					{		
					?>
							<!-- DEV_S1SMS -->
							<th><?php echo $t_sms[$GLOBALS['LANGINDEX']]; ?></th>
					<?php 
					}
					?>
					<?php
						if ($GLOBALS['M_SPECIAL_TYPE'] != 1 && ($GLOBALS['M_SUPPORT_SD'] || $GLOBALS['M_SUPPORT_NAS'])) {
					?>
							<th><?php echo $t_record[$GLOBALS['LANGINDEX']]; ?></th>
					<?php
						}
						if($GLOBALS['M_ALARMOUT_COUNT'] > 0) {
							for ($index = 1; $index <=$GLOBALS['M_ALARMOUT_COUNT']; $index++)
							{
					?>
							<th><?php echo $t_alarmOutput[$GLOBALS['LANGINDEX']].($GLOBALS['M_ALARMOUT_COUNT'] > 1 ? $index : ''); ?></th>
							
					<?php
							}
						}
						if ($GLOBALS['M_SUPPORT_PTZ'] || $GLOBALS['M_SUPPORT_EXTERNAL_PTZ']) {
					?>
							<th><?php echo $t_gotoPreset[$GLOBALS['LANGINDEX']]; ?></th>
					<?php
						}
					?>
						</tr>
					</thead>
					<tbody>
				<?php
					
					foreach ($event_list as $eventType) {
				?>
						<tr>
							<td>
								<img id="event_<?php echo $eventType; ?>" src="../images/common/btn/event_normal.png" style="cursor:pointer;margin-left:4px;"
									onclick="javascript:OnClickEventType('<?php echo $eventType; ?>');"
									onmouseover="ChangeImage('event_<?php echo $eventType; ?>','../images/common/btn/event_press.png');"
									onmouseout="ChangeImage('event_<?php echo $eventType; ?>','../images/common/btn/event_normal.png');">
							</td>
							<td id="event_<?php echo $eventType; ?>_select_type" style="text-align:left;padding-left:10px"><a href="javascript:OnClickEventType('<?php echo $eventType; ?>');" style="color:black"><?php echo $event_lang[$eventType][$GLOBALS['LANGINDEX']]; if($GLOBALS['M_ALARMOUT_COUNT'] > 1 && substr($eventType, 0, 5) == 'alarm') echo substr($eventType, -1)+1;?></a></td>
					<?php
						foreach ($action_list as $actionType) {
							if(substr($actionType, 0, 6) == 'output') {
					?>
							<td id="event_<?php echo $eventType; ?>_select_<?php echo $actionType; ?>" style="width:120px;">
							<?php
								if($eventType !='timesched' && $eventType != 'opensdk') {
							?>
								<select id="event_<?php echo $eventType.'_'.$actionType;?>" style="width:120px;" >
								<?php
									for ($index=0; $index<count($action_lang['output']); ++$index) {
										$value = $index;
										if ($index == 1) $value = -1;
										else if ($index >= 2) $value = ($index-1)*5;
								?>
									<option value="<?php echo $value; ?>" <?php if ($eventConf->event[$event_index[$eventType]]->dataInfo[$action_info[$actionType]]['value'] == $value) echo "selected=\"selected\""; ?>><?php echo $action_lang['output'][$index]; ?></option>
								<?php
									}
								?>
								</select>
							<?php
								}
							?>	
							</td>							
							<script>
								$("#event_<?php echo $eventType.'_'.$actionType; ?>").styledSelect({innerClass:'selectbox_style_option'});
							</script>
						<?php
							}
							else if ($actionType == 'preset') {
						?>
							<td id="event_<?php echo $eventType; ?>_select_<?php echo $actionType; ?>" style="width:120px;">
								<?php 
									if (!($eventType =='timesched' || $eventType == 'opensdk')) {
										if (!($GLOBALS['M_SUPPORT_PTZ'] && ($eventType == 'va' || $eventType == 'fd' || $eventType == 'tampering' || $eventType == 'trackingEvent'))) {
								?>
									<select id="event_<?php echo $eventType.'_'.$actionType;?>" style="width:120px;" >
										<?php
											for ($index=0; $index<count($action_lang[$actionType]); ++$index) {
												$value = $index;
										?>
											<option value="<?php echo $value; ?>" <?php if ($eventConf->event[$event_index[$eventType]]->dataInfo[$action_info[$actionType]]['value'] == $value) echo "selected=\"selected\""; ?>><?php echo $action_lang['preset'][$index]; ?></option>
										<?php
											}
										?>
									</select>
								<?php
									}
								}
								?>	
							</td>			
							<script>
								$("#event_<?php echo $eventType.'_'.$actionType; ?>").styledSelect({innerClass:'selectbox_style_option'});
							</script>
						<?php
							}
							else {
						?>
								<td id="event_<?php echo $eventType; ?>_select_<?php echo $actionType; ?>" <?php if($GLOBALS['M_ALARMOUT_COUNT'] == 0 && !($GLOBALS['M_SUPPORT_PTZ'] || $GLOBALS['M_SUPPORT_EXTERNAL_PTZ'])) echo "style=\"width:130px;\"";?> >
							<?php
								/*
								if(($eventType =='timesched' && ($actionType == 'record' || $actionType == 'email')) || 
									($eventType =='opensdk' && ($actionType == 'record'))	||
									($eventType =='videoloss' && ($actionType == 'ftp' || $actionType == 'record'))	||
									($eventType =='netdiscon' && ($actionType == 'ftp' || $actionType == 'email'))		||
									($eventType =='trackingEvent' && $actionType == 'ftp'))
									 {
								*/
							?>

							<!-- DEV_S1SMS -->
							<?php
								if(($eventType =='timesched' && ($actionType == 'record' || $actionType == 'email' || $actionType == 'sms')) || 
									($eventType =='opensdk' && ($actionType == 'record'))	||
									($eventType =='videoloss' && ($actionType == 'ftp' || $actionType == 'record'))	||
									($eventType =='netdiscon' && ($actionType == 'ftp' || $actionType == 'email' || $actionType == 'sms'))		||
									($eventType =='trackingEvent' && $actionType == 'ftp'))
									 {
							?>
								</td>
							<?php
								}
								else {
									if ($eventType == 'va' && $classInstances['VAConfiguration']->dataInfo['Mode']['value'] == 1) $eventConf->event[$event_index['va']]->dataInfo[$action_info['enable']]['value'] == 1;
									if($eventType =='trackingEvent' && $actionType == 'enable' && $GLOBALS['M_SUPPORT_PTZ'] == PTZ_SUPPORT){
										
									}
									else{
							?>
									<input type=	"checkbox" id="event_<?php echo $eventType.'_'.$actionType;?>" <?php if ($eventConf->event[$event_index[$eventType]]->dataInfo[$action_info[$actionType]]['value'] == 1) echo "checked=\"checked\""; ?> />
								</td>
							<?php
									}
								}
							}
						}
					?>
						</tr>
				<?php
					}
				?>
					</tbody>
				</table>
				<div class="btn_right" style="overflow:auto;width:880px;">
					<a id="mid_ok_btn" class="btn_apply" href="javascript:OnClickApply()"><?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?></a>
				</div>
				</div>
			</div>
		</div>
	</body>
</html>

