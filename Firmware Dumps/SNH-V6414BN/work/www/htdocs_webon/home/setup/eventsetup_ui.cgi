<div id="eventsetup_area">
<?php 
	if ($event_name != 'storage') {
?>
<div class="h3_tit <?php if (($event_name =='va' || $event_name =='trackingEvent') && $GLOBALS['M_SUPPORT_PTZ'] != PTZ_NOT_SUPPORT) echo 'mgt0';?>">
	<h3 class="wid320"><?php echo $t_eventActionSetup[$GLOBALS['LANGINDEX']]; ?></h3>
</div>
<table class="data_write" >
	<colgroup>
		<col style="width:190px;"/>
		<col />
	</colgroup>
	<tbody>
<?php
	if ($event_name != 'netdiscon' && $event_name != 'trackingEvent' && $event_name != 'videoloss') {
?>
		<tr>
			<td><label class="labelBold"><input type="checkbox" id="event_<?php echo $event_name; ?>_ftp" style="margin-left:<?php if (GetBrowserName()=='IE') { echo '-3'; } else { echo '1'; } ?>px" <?php if ($event_class->action->dataInfo['FTPSending']['value'] == 1) echo "checked=\"checked\""; ?> />FTP</label></td>
			<td></td>
		</tr>
<?php
	}
	if ($event_name != 'timesched' && $event_name != 'netdiscon') {
?>
		<tr>
			<td><label class="labelBold"><input type="checkbox" id="event_<?php echo $event_name; ?>_email" style="margin-left:<?php if (GetBrowserName()=='IE') { echo '-3'; } else { echo '1'; } ?>px" <?php if ($event_class->action->dataInfo['SMTPSending']['value'] == 1) echo "checked=\"checked\""; ?> /><?php echo $t_email[$GLOBALS['LANGINDEX']]; ?></label></td>
			<td></td>
		</tr>
<?php
	}
	// DEV_S1SMS
	if ($GLOBALS['M_SPECIAL_TYPE'] == 1 && $event_name != 'timesched' && $event_name != 'netdiscon') {
?>
		<tr>
			<td><label class="labelBold"><input type="checkbox" id="event_<?php echo $event_name; ?>_sms" style="margin-left:<?php if (GetBrowserName()=='IE') { echo '-3'; } else { echo '1'; } ?>px" <?php if ($event_class->action->dataInfo['SMSSending']['value'] == 1) echo "checked=\"checked\""; ?> /><?php echo $t_sms[$GLOBALS['LANGINDEX']]; ?></label></td>
			<td></td>
		</tr>
<?php
	}
	if ($GLOBALS['M_SPECIAL_TYPE'] != 1 && $event_name != 'timesched' && $event_name != 'videoloss' && $event_name != 'opensdk' && ($GLOBALS['M_SUPPORT_SD'] || $GLOBALS['M_SUPPORT_NAS'])) {
?>
		<tr>
			<td><label class="labelBold"><input type="checkbox" id="event_<?php echo $event_name; ?>_record" style="margin-left:<?php if (GetBrowserName()=='IE') { echo '-3'; } else { echo '1'; } ?>px" <?php if ($event_class->action->dataInfo['Record']['value'] == 1) echo "checked=\"checked\""; ?> /><?php echo $t_record[$GLOBALS['LANGINDEX']]; ?></label></td>
			<td></td>
		</tr>
<?php
	}

	if($event_name != 'timesched' && $event_name != 'opensdk' && $GLOBALS['M_ALARMOUT_COUNT'] > 0) {
		for ($index = 1; $index <=$GLOBALS['M_ALARMOUT_COUNT']; $index++)
		{
			$outputName = $t_alarmOutput[$GLOBALS['LANGINDEX']];
			if ($GLOBALS['M_ALARMOUT_COUNT'] > 1) {
				$outputName = $outputName.' '.$index;
			}
?>
			<tr>
				<th><?php echo $outputName; ?></th>
				<td>
					<select name="select" id="event_<?php echo $event_name; ?>_output_<?php echo $index; ?>" class="selectbox_style">
				<?php
					$outputLang = array($t_off[$GLOBALS['LANGINDEX']], $t_always[$GLOBALS['LANGINDEX']], '5 '.$t_sec[$GLOBALS['LANGINDEX']], '10 '.$t_sec[$GLOBALS['LANGINDEX']], '15 '.$t_sec[$GLOBALS['LANGINDEX']]);
					for($index2=0; $index2<count($outputLang); ++$index2) {
						$value = $index2;
						if ($index2 == 1) $value = -1;
						else if ($index2 >= 2) $value = ($index2-1)*5;
				?>	
						<option value="<?php echo $value;?>" <?php if ($event_class->action->relayOutput[$index-1] == $value) echo "selected=\"selected\""; ?>> <?php echo $outputLang[$index2]; ?></option>
				<?php
					}
				?>
					</select>
				</td>
			</tr>
<?php
		}
	}

	if ($event_name != 'timesched' && $event_name != 'opensdk' && $event_name != 'trackingEvent' && (($GLOBALS['M_SUPPORT_PTZ'] && $event_name != 'va' && $event_name != 'fd' && $event_name != 'tampering') || ($GLOBALS['M_RS485_OP_MODE'] == 0 && $GLOBALS['M_SUPPORT_EXTERNAL_PTZ']))) {
?>
		<tr>
			<th scope="row"><?php echo $t_gotoPreset[$GLOBALS['LANGINDEX']]; ?></th>
			<td>
				<select name="select" id="event_<?php echo $event_name; ?>_preset" class="selectbox_style">
					<option value="0" <?php if ($event_class->action->dataInfo['GotoPreset']['value'] == 0) echo "selected=\"selected\""; ?>><?php echo $t_off[$GLOBALS['LANGINDEX']]; ?></option>
			<?php
				for($index=1; $index<=$GLOBALS['M_PRESET_COUNT'] ; ++$index) {
			?>	
					<option value="<?php echo $index;?>" <?php if ($event_class->action->dataInfo['GotoPreset']['value'] == $index) echo "selected=\"selected\""; ?>> <?php echo $index; ?></option>
			<?php
				}
			?>
				</select>
				
			</td>
		</tr>
<?php
	}
?>
	</tbody>
</table>
<?php
}
?>
<div class="h3_tit" style="overflow:auto;width:100%;">
<?php
	if ($event_name == 'storage') {
?>
	<h3 class="wid320"><?php echo $t_normalRecordSetup[$GLOBALS['LANGINDEX']]; ?></h3>
<?php
	}
	else {
?>
	<h3 class="wid220"><?php echo $t_activation_time[$GLOBALS['LANGINDEX']]; ?></h3>
<?php
	}
?>
</div>
<table class="data_write">
	<tbody>
		<tr>
			<td>
				<label>
					<input type="radio" name="event_<?php echo $event_name; ?>_act" id="event_<?php echo $event_name; ?>_act_always" onclick="OnClickActivationTime('<?php echo $event_name; ?>')" <?php if ($event_class->schedule->enabled == 0) echo "checked=\"checked\""; ?> style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_always[$GLOBALS['LANGINDEX']]; ?> &nbsp;&nbsp;
				</label>
				<label>
					<input type="radio" name="event_<?php echo $event_name; ?>_act" id="event_<?php echo $event_name; ?>_act_timesched" onclick="OnClickActivationTime('<?php echo $event_name; ?>')" <?php if ($event_class->schedule->enabled == 1) echo "checked=\"checked\""; ?> /><?php echo $t_only_schedule[$GLOBALS['LANGINDEX']]; ?>
				</label>
			</td>
		</tr>
		<tr>
			<td>
				<a class="btn_type01 mgb10" style="float:right" href="javascript:ScheduleClear('<?php echo $event_name; ?>');" id="event_<?php echo $event_name; ?>_clear_btn"><?php echo $t_clear[$GLOBALS['LANGINDEX']]; ?></a>
			</td>
		</tr>
	</tbody>
</table>
<div class="mgl5" style="height:260px">
	<div id="event_<?php echo $event_name; ?>_timeschedule_cover" class="timeschedule_cover">
		<table id="event_<?php echo $event_name; ?>_timeschedule_table" border="0" width="100%" cellspacing="0" cellpadding="0" class="eventTable" >
			<thead><tr><td class="dayHead">&nbsp;</td><td class="dayHead">00</td><td class="dayHead">01</td><td class="dayHead">02</td><td class="dayHead">03</td><td class="dayHead">04</td><td class="dayHead">05</td><td class="dayHead">06</td><td class="dayHead">07</td><td class="dayHead">08</td><td class="dayHead">09</td><td class="dayHead">10</td><td class="dayHead">11</td><td class="dayHead">12</td><td class="dayHead">13</td><td class="dayHead">14</td><td class="dayHead">15</td><td class="dayHead">16</td><td class="dayHead">17</td><td class="dayHead">18</td><td class="dayHead">19</td><td class="dayHead">20</td><td class="dayHead">21</td><td class="dayHead">22</td><td class="dayHead">23</td></tr></thead>
			<tbody>
			<tr class="weekHead"><td><?php echo $t_sun[$GLOBALS["LANGINDEX"]]; ?></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
			<tr class="weekHead"><td><?php echo $t_mon[$GLOBALS["LANGINDEX"]]; ?></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
			<tr class="weekHead"><td><?php echo $t_tue[$GLOBALS["LANGINDEX"]]; ?></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
			<tr class="weekHead"><td><?php echo $t_wed[$GLOBALS["LANGINDEX"]]; ?></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
			<tr class="weekHead"><td><?php echo $t_thu[$GLOBALS["LANGINDEX"]]; ?></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
			<tr class="weekHead"><td><?php echo $t_fri[$GLOBALS["LANGINDEX"]]; ?></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
			<tr class="weekHead"><td><?php echo $t_sat[$GLOBALS["LANGINDEX"]]; ?></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
			</tbody>
		</table>
		<div class="labelMinutesHour" style="float:right; margin-top:5px;">
			<img src="../images/timeline/minute.png" /><span style="position:relative; top:-2px; left:2px;"><?php echo $t_minutes[$GLOBALS['LANGINDEX']]; ?></span>&nbsp;&nbsp;
			<img src="../images/timeline/hour.png" /><span style="position:relative; top:-2px; left:2px;"><?php echo $t_hour[$GLOBALS['LANGINDEX']]; ?></span>
		</div>
		<div id="event_<?php echo $event_name; ?>_timeschedule_overlay" class="overlayClass">&nbsp;</div>
	</div>					
</div>
<script>
	if($("#event_<?php echo $event_name; ?>_act_always").is(':checked')) 
		$("#event_<?php echo $event_name; ?>_timeschedule_overlay").show();
	else
		$("#event_<?php echo $event_name; ?>_timeschedule_overlay").hide();

	var msg = "";
	msg += "<Schedule>\r\n";
	msg += "<Enabled><?php echo $event_class->schedule->enabled; ?></Enabled>\r\n";
<?php
	for ($i=0; $i<7; $i++) {
?>
		msg += "<Day"+<?php echo $i;?>+">\r\n";
	<?php
		for($j=0; $j<24; $j++) {
	?>
			msg += "<H"+<?php echo $j; ?>+">"+<?php echo $event_class->schedule->dayTime[$i]->time[$j]; ?>+"</H"+<?php echo $j;?>+">\r\n";
			msg += "<IsEnabled"+<?php echo $j; ?>+">"+<?php echo $event_class->schedule->dayDetail[$i]->detailTime[$j]->dataInfo['isEnabled']['value']; ?>+"</IsEnabled"+<?php echo $j;?>+">\r\n";
			msg += "<From"+<?php echo $j; ?>+">"+<?php echo $event_class->schedule->dayDetail[$i]->detailTime[$j]->dataInfo['from']['value']; ?>+"</From"+<?php echo $j;?>+">\r\n";
			msg += "<To"+<?php echo $j; ?>+">"+<?php echo $event_class->schedule->dayDetail[$i]->detailTime[$j]->dataInfo['to']['value']; ?>+"</To"+<?php echo $j;?>+">\r\n";
	<?php
		}
	?>
		msg += "</Day"+<?php echo $i;?>+">\r\n";
<?php
	}
?>
	msg += "</Schedule>\r\n";
	SetScheduleDataToTable(msg,"event_<?php echo $event_name; ?>_timeschedule_table");
	
	var buttonLang = ["<?php echo $t_ok[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $t_cancel[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $t_delete[$GLOBALS['LANGINDEX']]; ?>"];

	$("#tmMinute").removeAttr("style")
</script>
<div id="tmMinute" title="Enter Polygon Area Name" style="display:none; text-align:center">
		<label><b><?php echo $t_from[$GLOBALS['LANGINDEX']]; ?></b></label>
		<select id="fromMinutesHr">	</select>
		<span> :</span>
		<select name="fromMinutes" id="fromMinutes" style="margin-right:5px;" onchange="OnChangeMinutes(true)"></select>
		<span>~</span>
		<label><b><?php echo $t_to[$GLOBALS['LANGINDEX']]; ?></b></label>
		<select id="toMinutesHr"></select>
		<span> :</span>
		<select name="toMinutes" id="toMinutes" onchange="OnChangeMinutes(false)"></select>
</div>
<script>
	jQuery(document).ready(function(){
		jQuery("#tmMinute,#line-dialog,#poly-dialog,#poly-dialog-appear").dialog({
			autoOpen: false,
			modal: true,
			draggable: false
		});
		
		jQuery.fn.extend({ 
			disableSelection: function() { 
			this.each(function() { 
				if (typeof this.onselectstart != 'undefined') {
					this.onselectstart = function() { return false; };
				} else if (typeof this.style.MozUserSelect != 'undefined') {
					this.style.MozUserSelect = 'none';
				} else {
					this.onmousedown = function() { return false; };
				}
					}); 
				} 
		});
		$('.eventTable').disableSelection();   
	});

</script>
</div>

<style>
	#tmMinute select{
		background: none repeat scroll 0 0 #FFFFFF;
		border: 1px solid #CCCCCC;
		width: 55px;
	}
	#tmMinute {
		min-height: 40px !important;
		margin-top: 15px;
	}
	.ui-dialog.scheduleTable {
		height: auto;
		left: 490px !important;
		width: 400px !important;
	}
	table.eventTable{
		border-top: 2px solid #7C7F85;
		border-left: 2px solid #7C7F85;
	}
	
	table.eventTable tr td{
		background: none repeat scroll 0 0 #B4B9C5;
		border-bottom: 2px solid #7C7F85;
		border-right: 2px solid #7C7F85;
		cursor: pointer;
		font-size: 11px;
		height: 18px;
		line-height: 18px;
		width: 18px;
	}
	table.eventTable tbody tr td:first-child{
		background: none repeat scroll 0 0 #8E939E !important;
		color: #000000 !important;
		padding: 3px !important;
		width:80px;
		text-align:center;
	}
	
	table.eventTable tr td:first-child, .dayHead,table.eventTable tr td.dayHead{
	 	background: none repeat scroll 0 0 #8E939E;
		color: #000;
		padding: 3px;
	}
	.selTime{
	background:#4179B9 !important;
	}
	.selHour{
		background:#36567B !important;
	}
	.overlayClass{
		background: none repeat scroll 0 0 #B4B9C5;
		height: 210px;
		left: 0;
		position: absolute;
		top: 0px;
		width: 675px;
		opacity: 0.3;
		filter:alpha(opacity=30); /* For IE8 and earlier */
	}
	.timeschedule_cover{
		height: 235px;
		position: relative;
		 
		float:left;
	}
	.right_btn {
		 border-top: 1px solid #737C8F;
		 float: left;
		 margin-top: 45px;
		 padding-top: 10px;
		 text-align: right;
		 width: 100%;
	}
</style>
