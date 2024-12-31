<script type="text/javascript" language="javascript">

function CheckDayNightSchedule()
{
	if($("#day_night").val() == 4){
		for (var i=0; i<8; ++i) {
			var temp1 = $("#daynight_start_"+i).val();
			var tempStartTime = temp1.split(':');
			var temp2 = $("#daynight_end_"+i).val();
			var tempEndTime = temp2.split(':');			
			var id = document.getElementById('li-daynight');					

			var baseStartTime = new Date(2000,1,1,tempStartTime[0], tempStartTime[1], 0).valueOf();
			var baseEndTime = new Date(2000,1,1,tempEndTime[0], tempEndTime[1], 59).valueOf();
			if (baseStartTime > baseEndTime) {
				alert("<?php echo $msg_invalid_time[$GLOBALS['LANGINDEX']]; ?>");
				MoveTapLink("daynight");
				$("#daynight_start_"+i).focus();
				return false;
			}
		}
	}
	
	return true;
}

function MakeDayNightScheduleXml()
{
	var msg = "";
	msg = "<ImageDayNightSchedule>";
  	for (var i=0; i<8; ++i) {
		msg += "<Schedule"+i+">";	
		msg += "<Enable>"+($("#dnschedule_"+dayslist[i]+"_enable").is(':checked') ? 1 : 0)+"</Enable>";
		var temp1 = $("#daynight_start_"+i).val();
		var tempStartTime = temp1.split(':');
		var temp2 = $("#daynight_end_"+i).val();
		var tempEndTime = temp2.split(':');
		
		msg += "<StartHour>"+ tempStartTime[0] +"</StartHour>";
		msg += "<StartMin>"+ tempStartTime[1] +"</StartMin>";
		msg += "<EndHour>"+ tempEndTime[0] +"</EndHour>";
		msg += "<EndMin>"+ tempEndTime[1]+"</EndMin>";
		msg += "</Schedule"+i+">";
  	}	  
  	msg += "</ImageDayNightSchedule>";  	
	return msg;
}

function MakeDayNightXml()
{
	var msg = '';
	msg += MakeTitleOsdXml();
  	msg += "<DayNightMode>" + $("#day_night").val() + "</DayNightMode>";
  	msg += "<DayNightDwellTime>" + $("#dwell_time").val() + "</DayNightDwellTime>";
  	msg += "<DayNightDuration>" + $("#duration").val() + "</DayNightDuration>";
<?php if($GLOBALS['M_ALARMIN_COUNT'] > 0 ) { ?>
  	msg += "<DayNightExtMode>" + $("#alarm_in").val() + "</DayNightExtMode>";
<?php } 
	if($GLOBALS['M_SUPPORT_MOTORIZE'] == MOTORIZE_FOCUS_ONLY_SUPPORT) {?>
  	msg += "<AutoFocusEnable>" + $("#simplefocus_dn").val() + "</AutoFocusEnable>";
<?php } ?>
  	return msg;
}

function OnChangeDayNight()
{
	if ($("#day_night").val() == 0) { // COLOR
		$("#dwell_time").attr("disabled", "disabled");
		$("#duration").attr("disabled", "disabled");
		$("#alarm_in").attr("disabled", "disabled");
		for (var i=0; i<8; ++i) {				
			$("#dnschedule_"+dayslist[i]+"_enable").attr("disabled", "disabled");				
			$("#daynight_start_"+i).attr("disabled", "disabled");
			$("#daynight_start_"+i).attr("disabled", "disabled");
			$("#daynight_end_"+i).attr("disabled", "disabled");
			$("#daynight_end_"+i).attr("disabled", "disabled");
		}
	}
	else if ($("#day_night").val() == 1) { // BW
		$("#dwell_time").attr("disabled", "disabled");
		$("#duration").attr("disabled", "disabled");
		$("#alarm_in").attr("disabled", "disabled");
		for (var i=0; i<8; ++i) {				
			$("#dnschedule_"+dayslist[i]+"_enable").attr("disabled", "disabled");				
			$("#daynight_start_"+i).attr("disabled", "disabled");
			$("#daynight_start_"+i).attr("disabled", "disabled");
			$("#daynight_end_"+i).attr("disabled", "disabled");
			$("#daynight_end_"+i).attr("disabled", "disabled");
		}
	}
	else if ($("#day_night").val() == 2) { // AUTO
		$("#dwell_time").removeAttr("disabled");
		$("#duration").removeAttr("disabled");
		$("#alarm_in").attr("disabled", "disabled");
		for (var i=0; i<8; ++i) {				
			$("#dnschedule_"+dayslist[i]+"_enable").attr("disabled", "disabled");				
			$("#daynight_start_"+i).attr("disabled", "disabled");
			$("#daynight_start_"+i).attr("disabled", "disabled");
			$("#daynight_end_"+i).attr("disabled", "disabled");
			$("#daynight_end_"+i).attr("disabled", "disabled");
		}
	}
	else if ($("#day_night").val() == 3) { // EXTERNAL BW
		$("#dwell_time").attr("disabled", "disabled");
		$("#duration").attr("disabled", "disabled");
		$("#alarm_in").removeAttr("disabled");
		for (var i=0; i<8; ++i) {				
			$("#dnschedule_"+dayslist[i]+"_enable").attr("disabled", "disabled");				
			$("#daynight_start_"+i).attr("disabled", "disabled");
			$("#daynight_start_"+i).attr("disabled", "disabled");
			$("#daynight_end_"+i).attr("disabled", "disabled");
			$("#daynight_end_"+i).attr("disabled", "disabled");
		}
	}
	else if ($("#day_night").val() == 4) { // SCHEDULE
		$("#dwell_time").attr("disabled", "disabled");
		$("#duration").attr("disabled", "disabled");
		$("#alarm_in").attr("disabled", "disabled");
		for (var i=0; i<8; ++i) {
			$("#dnschedule_"+dayslist[i]+"_enable").removeAttr("disabled");
			$("#daynight_start_"+i).removeAttr("disabled");
			$("#daynight_start_"+i).removeAttr("disabled");
			$("#daynight_end_"+i).removeAttr("disabled");
			$("#daynight_end_"+i).removeAttr("disabled");
		}	
		OnClickDnSchedule();
	}
	
	oldDN = $("#day_night").val();
	
	SetTimeOut();
}

function InitDayNightScheduleTime()
{
	<?php
		for ($index=0; $index<8; ++$index) {
			$hour = $imageDayNightSchedule->schedule[$index]->dataInfo['StartHour']['value'];
			$min = $imageDayNightSchedule->schedule[$index]->dataInfo['StartMin']['value'];
			$startTime = ($hour<10?'0'.$hour:$hour).':'.($min<10?'0'.$min:$min);
			$hour = $imageDayNightSchedule->schedule[$index]->dataInfo['EndHour']['value'];
			$min = $imageDayNightSchedule->schedule[$index]->dataInfo['EndMin']['value'];
			$endTime = ($hour<10?'0'.$hour:$hour).':'.($min<10?'0'.$min:$min);

	?>
			$('#daynight_start_<?php echo $index;?>').timepicker({
				hourText:"<?php echo $t_hour[$GLOBALS['LANGINDEX']];?>",
				minuteText:"<?php echo $t_minute[$GLOBALS['LANGINDEX']];?>"
			});
			$('#daynight_end_<?php echo $index;?>').timepicker({
				hourText:"<?php echo $t_hour[$GLOBALS['LANGINDEX']];?>",
				minuteText:"<?php echo $t_minute[$GLOBALS['LANGINDEX']];?>"
			});
			
			$('#daynight_start_<?php echo $index;?>').val("<?php echo $startTime; ?>"+":00");
			$('#daynight_end_<?php echo $index;?>').val("<?php echo $endTime; ?>"+":59");
	/*		
			$('#daynight_start_<?php echo $index;?>').timepicker('setTime',"<?php echo $startTime; ?>");
			$('#daynight_end_<?php echo $index;?>').timepicker('setTime',"<?php echo $endTime; ?>");
	*/		
	<?php
		}
	?>		
	$('#daynight_start_0').change(function(e){
		for(var i = 1; i < 8; i++){
			$('#daynight_start_'+i).val($('#daynight_start_0').val());
		}
	});
	$('#daynight_end_0').change(function(e){
		for(var i = 1; i < 8; i++){
			$('#daynight_end_'+i).val($('#daynight_end_0').val());
		}
	});
}


function OnClickDnSchedule()
{		
	var disabledVal = false;
	for (var i=0; i<8; ++i) {	
		disabledVal = false;
		if ($("#dnschedule_"+dayslist[i]+"_enable").is(':checked') == 0) disabledVal = true;			
		if (i != 0 && $("#dnschedule_everyday_enable").is(':checked') == 1) {
			$("#dnschedule_"+dayslist[i]+"_enable").attr("disabled", "disabled");
			disabledVal = true;
			$('#daynight_start_'+i).val($('#daynight_start_0').val());
			$('#daynight_end_'+i).val($('#daynight_end_0').val());			
		}
		else {
			$("#dnschedule_"+dayslist[i]+"_enable").removeAttr("disabled");
		}

		if (disabledVal == true) {
			$("#daynight_start_"+i).attr("disabled", "disabled");
			$("#daynight_start_"+i).attr("disabled", "disabled");
			$("#daynight_end_"+i).attr("disabled", "disabled");
			$("#daynight_end_"+i).attr("disabled", "disabled");
		}
		else {
			$("#daynight_start_"+i).removeAttr("disabled");
			$("#daynight_start_"+i).removeAttr("disabled");
			$("#daynight_end_"+i).removeAttr("disabled");
			$("#daynight_end_"+i).removeAttr("disabled");
		}
	}
}

</script>
<table class="data_write mgt10 mgl-20 pdl15" style="width:670px;">
	<colgroup>
		<col style="width:180px;"/>
		<col />
	</colgroup>
	<tbody>									
		<tr>
		<th class="top_txt"><?php echo $t_mode[$GLOBALS["LANGINDEX"]]; ?></th>
			<td>
				<select id="day_night"	class="selectbox_style_wid230" onchange="OnChangeDayNight()">
					<option value="0" <?php if ($imageSpecial->dataInfo["DayNightMode"]["value"] == 0) echo "selected=\"selected\""; ?>><?php echo $t_color[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="1" <?php if ($imageSpecial->dataInfo["DayNightMode"]["value"] == 1) echo "selected=\"selected\""; ?>><?php echo $t_bw[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="2" <?php if ($imageSpecial->dataInfo["DayNightMode"]["value"] == 2) echo "selected=\"selected\""; ?>><?php echo $t_auto[$GLOBALS["LANGINDEX"]]; ?></option>		
			<?php if($GLOBALS['M_ALARMIN_COUNT'] > 0) { ?>
					<option value="3" <?php if ($imageSpecial->dataInfo["DayNightMode"]["value"] == 3) echo "selected=\"selected\""; ?>><?php echo $t_extern[$GLOBALS["LANGINDEX"]]; ?></option>
			<?php } ?>
					<option value="4" <?php if ($imageSpecial->dataInfo["DayNightMode"]["value"] == 4) echo "selected=\"selected\""; ?>><?php echo $t_schedule[$GLOBALS["LANGINDEX"]]; ?></option>
				</select>
			</td>
		</tr>
		<tr>
			<th class="top_txt"><?php echo $t_dwelltime[$GLOBALS["LANGINDEX"]]; ?></th>
			<td>
				<select id="dwell_time"  class="selectbox_style_wid230" onchange="OnChangeDayNight()">
					<option value="5"  <?php if ($imageSpecial->dataInfo["DayNightDwellTime"]["value"] == 5) echo "selected=\"selected\""; ?>>5 <?php echo $t_sec[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="7"  <?php if ($imageSpecial->dataInfo["DayNightDwellTime"]["value"] == 7) echo "selected=\"selected\""; ?>>7 <?php echo $t_sec[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="10" <?php if ($imageSpecial->dataInfo["DayNightDwellTime"]["value"] == 10) echo "selected=\"selected\""; ?>>10 <?php echo $t_sec[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="15" <?php if ($imageSpecial->dataInfo["DayNightDwellTime"]["value"] == 15) echo "selected=\"selected\""; ?>>15 <?php echo $t_sec[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="20" <?php if ($imageSpecial->dataInfo["DayNightDwellTime"]["value"] == 20) echo "selected=\"selected\""; ?>>20 <?php echo $t_sec[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="30" <?php if ($imageSpecial->dataInfo["DayNightDwellTime"]["value"] == 30) echo "selected=\"selected\""; ?>>30 <?php echo $t_sec[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="40" <?php if ($imageSpecial->dataInfo["DayNightDwellTime"]["value"] == 40) echo "selected=\"selected\""; ?>>40 <?php echo $t_sec[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="60" <?php if ($imageSpecial->dataInfo["DayNightDwellTime"]["value"] == 60) echo "selected=\"selected\""; ?>>60 <?php echo $t_sec[$GLOBALS["LANGINDEX"]]; ?></option>
				</select>
			</td>
		</tr>
		<tr>
			<th class="top_txt"><?php echo $t_duration[$GLOBALS["LANGINDEX"]]; ?></th>
			<td>
				<select id="duration"  class="selectbox_style_wid230" onchange="OnChangeSpecial()">
					<option value="0" <?php if ($imageSpecial->dataInfo["DayNightDuration"]["value"] == 0) echo "selected=\"selected\""; ?>><?php echo $t_veryfast[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="1" <?php if ($imageSpecial->dataInfo["DayNightDuration"]["value"] == 1) echo "selected=\"selected\""; ?>><?php echo $t_fast[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="2" <?php if ($imageSpecial->dataInfo["DayNightDuration"]["value"] == 2) echo "selected=\"selected\""; ?>><?php echo $t_normal[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="3" <?php if ($imageSpecial->dataInfo["DayNightDuration"]["value"] == 3) echo "selected=\"selected\""; ?>><?php echo $t_slow[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="4" <?php if ($imageSpecial->dataInfo["DayNightDuration"]["value"] == 4) echo "selected=\"selected\""; ?>><?php echo $t_veryslow[$GLOBALS["LANGINDEX"]]; ?></option>
				</select>
			</td>
		</tr>
<?php 
	if($GLOBALS['M_ALARMIN_COUNT'] > 0) {
?>
		<tr>
			<th class="top_txt"><?php echo $t_alarmin[$GLOBALS["LANGINDEX"]]; ?></th>
			<td>
				<select id="alarm_in"  class="selectbox_style_wid230" onchange="OnChangeDayNight()">
					<option value="0" <?php if ($imageSpecial->dataInfo["DayNightExtMode"]["value"] == 0) echo "selected=\"selected\""; ?>><?php echo $t_opencolorclosebw[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="1" <?php if ($imageSpecial->dataInfo["DayNightExtMode"]["value"] == 1) echo "selected=\"selected\""; ?>><?php echo $t_openbwclosecolor[$GLOBALS["LANGINDEX"]]; ?></option>
				</select>
			</td>
		</tr>
<?php 
	} 
	if($GLOBALS['M_SUPPORT_MOTORIZE'] == MOTORIZE_FOCUS_ONLY_SUPPORT) { 
?>
		<tr>
			<th class="top_txt"><?php echo $t_simplefocusafterdn[$GLOBALS["LANGINDEX"]]; ?></th>
			<td>
				<select id="simplefocus_dn"  class="selectbox_style_wid230" onchange="OnChangeDayNight()">
					<option value="0" <?php if ($imageSpecial->dataInfo["AutoFocusEnable"]["value"] == 0) echo "selected=\"selected\""; ?>><?php echo $t_off[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="1" <?php if ($imageSpecial->dataInfo["AutoFocusEnable"]["value"] == 1) echo "selected=\"selected\""; ?>><?php echo $t_on[$GLOBALS["LANGINDEX"]]; ?></option>
				</select>
			</td>
		</tr>
<?php 
	} 
?>
	</tbody>
</table>
<table class="data_write mgt10 mgl-20 pdl15" style="width:670px;">
	<colgroup>
		<col style="width:180px;"/>
		<col style="width:115px;"/>
		<col style="width:20px;"/>
		<col style="width:115px;"/>
		<col />
	</colgroup>
	<tbody>
		<th class="top_txt" colspan="2"><?php echo $t_dnActivation_time[$GLOBALS["LANGINDEX"]]; ?></th>
		<tr>
			<th class="top_txt"></th>
			<td class="top_txt" style="text-align:center"><?php echo $t_startTime[$GLOBALS["LANGINDEX"]]; ?></td>
			<td></td>
			<td class="top_txt" style="text-align:center"><?php echo $t_endTime[$GLOBALS["LANGINDEX"]]; ?></td>
			<td></td>
		</tr> 							
<?php
	$dayslist = array("everyday", "sun", "mon", "tue", "wed", "thu", "fri", "sat");
	$dayslang = array($t_everyday[$GLOBALS["LANGINDEX"]], $t_sun[$GLOBALS["LANGINDEX"]], $t_mon[$GLOBALS["LANGINDEX"]], $t_tue[$GLOBALS["LANGINDEX"]], $t_wed[$GLOBALS["LANGINDEX"]], $t_thu[$GLOBALS["LANGINDEX"]], $t_fri[$GLOBALS["LANGINDEX"]], $t_sat[$GLOBALS["LANGINDEX"]]);
	$isEverydayEnable = $imageDayNightSchedule->schedule[0]->dataInfo['Enable']['value'];
	for ($index=0; $index<count($dayslist); ++$index) {
		$enable = $imageDayNightSchedule->schedule[$index]->dataInfo['Enable']['value'];
?>
		<tr>
			<td class="top_txt">
				<label><input type="checkbox" id="dnschedule_<?php echo $dayslist[$index]; ?>_enable" <?php if ($enable == 1) echo "checked=\"checked\""; if ($index != 0 && $isEverydayEnable == 1) echo "disabled='disabled'"; ?> onclick="OnClickDnSchedule();" /><?php echo $dayslang[$index]; ?></label>
			</td>
			<td>
				<input type="text" class="text" name='start' style="width:110px;text-align:center" id="daynight_start_<?php echo $index;?>" onkeydown="return false;" <?php if (($index != 0 && $isEverydayEnable == 1) || $enable == 0) echo "disabled=\"disabled\""; ?> />											
			</td>
			<td>~</td>
			<td>
				<input type="text" class="text" name='end' style="width:110px;text-align:center" id="daynight_end_<?php echo $index;?>" onkeydown="return false;" <?php if (($index != 0 && $isEverydayEnable == 1) || $enable == 0) echo "disabled=\"disabled\""; ?> />
			</td>
			<td></td>
		</tr>
	<?php
		}
	?> 				
	</tbody>
</table>
