<script type="text/javascript" language="javascript">

function CheckImagePresetSchedule()
{
	if($("#preset_schedule").val() == 1){
		var presetCheck = "#imagepreset_list input[type='radio']";
		var presetMode = "#imagepreset_list select";
		var startTimeId = "#imagepreset_list input[name='start']";
		var endTimeId = "#imagepreset_list input[name='end']";
		
		for (var index=0; index< $("#imagepreset_list tbody tr").size(); ++index) {
			var temp1 = $(startTimeId+":eq("+index+")").val();
			var tempStartTime = temp1.split(':');
			var temp2 = $(endTimeId+":eq("+index+")").val();
			var tempEndTime = temp2.split(':');
		
			var baseStartTime = new Date(2000,1,1,tempStartTime[0], tempStartTime[1], 0).valueOf();
			var baseEndTime = new Date(2000,1,1,tempEndTime[0], tempEndTime[1], 59).valueOf();
		
			if (baseStartTime > baseEndTime) {
				alert("<?php echo $msg_invalid_time[$GLOBALS['LANGINDEX']]; ?>");
				MoveTapLink("imagepreset");
			
				$(presetCheck+":eq("+index+")").prop("checked",true);
				OnClickImagePresetList();
				$(startTimeId+":eq("+index+")").focus();
				return false;
			}
			for (var index2=index+1; index2< $("#imagepreset_list tbody tr").size(); ++index2) {
				temp1 = $(startTimeId+":eq("+index2+")").val();
				tempStartTime = temp1.split(':');
				temp2 = $(endTimeId+":eq("+index2+")").val();
				tempEndTime = temp2.split(':');				
		
				var compareStartTime = new Date(2000,1,1,tempStartTime[0], tempStartTime[1], 0).valueOf();
				var compareEndTime = new Date(2000,1,1,tempEndTime[0], tempEndTime[1], 59).valueOf();

				if ((baseStartTime <= compareStartTime && compareStartTime <= baseEndTime) || (baseStartTime <= compareEndTime && compareEndTime <= baseEndTime)) {
					alert("<?php echo $msg_preset_duplicate[$GLOBALS['LANGINDEX']]; ?>");
					MoveTapLink("imagepreset");
					$(presetCheck+":eq("+index2+")").prop("checked",true);
					OnClickImagePresetList();
					$(startTimeId+":eq("+index2+")").focus();
					return false;
				}

				if ((compareStartTime <= baseStartTime && baseStartTime <= compareEndTime) || (compareStartTime <= baseEndTime && baseEndTime <= compareEndTime)) {
					alert("<?php echo $msg_preset_duplicate[$GLOBALS['LANGINDEX']]; ?>");
					MoveTapLink("imagepreset");
					$(presetCheck+":eq("+index2+")").prop("checked",true);
					OnClickImagePresetList();
					$(startTimeId+":eq("+index2+")").focus();
					return false;
				}
			}
		}
		if (imagepreset_cnt == 0 && $("#preset_schedule").val() == 1) {
			alert("<?php echo $msg_preset_delete[$GLOBALS['LANGINDEX']]; ?>");
			MoveTapLink("imagepreset");
			return false;
		}
	}
	return true;
}

function MakeImagepresetXml()
{
	var msg = "";	

	var presetMode = "#imagepreset_list select";	
	var startTimeId = "#imagepreset_list input[name='start']";
	var endTimeId = "#imagepreset_list input[name='end']";
	
	msg += "<ImagePreset>";
	msg +=	"<DefaultMode>"+ $("#preset_default").val() +"</DefaultMode>";
	msg +=	"<ScheduleMode>"+ $("#preset_schedule").val() +"</ScheduleMode>";
	for (var index=0; index< $("#imagepreset_list tbody tr").size(); ++index) {
		msg +=	"<PresetSchedule"+index+">";
		msg +=	"<Mode>"+ $(presetMode+":eq("+index+")").val() +"</Mode>";
	
		var temp1 = $(startTimeId+":eq("+index+")").val();
		var tempStartTime = temp1.split(':');
		var temp2 = $(endTimeId+":eq("+index+")").val();
		var tempEndTime = temp2.split(':');
	
		msg += "<StartHour>"+ tempStartTime[0] +"</StartHour>";
		msg += "<StartMin>"+ tempStartTime[1] +"</StartMin>";
		msg += "<EndHour>"+ tempEndTime[0] +"</EndHour>";
		msg += "<EndMin>"+ tempEndTime[1] +"</EndMin>";
		/*
		msg += "<StartHour>"+$("#imagepreset_start_"+index).timepicker('getHour')+"</StartHour>";
		msg += "<StartMin>"+$("#imagepreset_start_"+index).timepicker('getMinute')+"</StartMin>";
		msg += "<EndHour>"+$("#imagepreset_end_"+index).timepicker('getHour')+"</EndHour>";
		msg += "<EndMin>"+$("#imagepreset_end_"+index).timepicker('getMinute')+"</EndMin>";
		*/
		msg +=	"</PresetSchedule"+index+">";
	}
	msg +="</ImagePreset>"
	return msg;
}


function OnChangePresetMode(){
	var preset = $("#preset_default").val();
	var minSpeedOffset = 0;
	var maxSpeedOffset = 0;

	<?php if($GLOBALS['M_MAX_RESOLUTION'] == MAX_3_MEGA) { ?>
		minSpeedOffset = 1;
		maxSpeedOffset = 1;
	<?php } ?>

	if($("#aflk").val() != "0"){
		$("#aflk").val("0");
		$("#shutter_speed_min").removeAttr("disabled");
		$("#shutter_speed_max").removeAttr("disabled");
	}

	$("#ssnr").removeAttr("disabled","disabled");
	$("#ssdr_level").removeAttr("disabled","disabled");
	$("#ssdr_range").removeAttr("disabled","disabled");
	$("#ssnr_level").removeAttr("disabled","disabled");

	switch(preset){
		case "1" :
			$("#shutter_speed_min").val(4);
			$("#agc_mode").val(3);
			$("#ssdr_mode").val(1);
			$("#ssdr_level").val(12);
			$("#ssnr").val(1);
			$("#ssnr_level").val(12);
			break;
		case "2" : 
			$("#shutter_speed_min").val(8 + minSpeedOffset);
			$("#shutter_speed_max").val(29 + maxSpeedOffset);
			$("#agc_mode").val(3);
			$("#ssdr_mode").val(1);
			$("#ssdr_level").val(12);
			$("#ssnr").val(1);
			$("#ssnr_level").val(4);
			break;
		case "3" : 
			$("#shutter_speed_min").val(6);
			$("#agc_mode").val(2);
			$("#ssdr_mode").val(1);
			$("#ssdr_level").val(12);
			$("#ssnr").val(1);
			$("#ssnr_level").val(12);
			break;
		case "4" : 
			$("#shutter_speed_min").val(4);
			$("#agc_mode").val(3);
			$("#ssdr_mode").val(1);
			$("#ssdr_level").val(18);
			$("#ssnr").val(1);
			$("#ssnr_level").val(12);
			break;
		case "5" : 
			$("#shutter_speed_min").val(8 + minSpeedOffset);
			$("#shutter_speed_max").val(29 + maxSpeedOffset);
			$("#agc_mode").val(2);
			$("#ssdr_mode").val(1);
			$("#ssdr_level").val(12);
			$("#ssnr").val(1);
			$("#ssnr_level").val(4);
			break;
		case "6" : 
			$("#shutter_speed_min").val(8 + minSpeedOffset);
			$("#shutter_speed_max").val(29 + maxSpeedOffset);
			$("#agc_mode").val(3);
			$("#ssdr_mode").val(1);
			$("#ssdr_level").val(18);
			$("#ssnr").val(1);
			$("#ssnr_level").val(4);
			break;
	}
	OnChangeShutter();
	OnChangeAGCMode();
}

function OnChangePresetScheduleMode()
{
	if ($("#preset_schedule").val() == 0) {
		$("#mid_add_btn").removeAttr('href');
		$("#mid_add_btn").attr('class','btn_disable');
		$("#mid_add_btn").css('color','gray');
		
		$("#mid_del_btn").removeAttr('href');
		$("#mid_del_btn").attr('class','btn_disable');
		$("#mid_del_btn").css('color','gray');
	}
	else{
		$("#mid_add_btn").attr('href',"javascript:OnClickAdd()");
		$("#mid_add_btn").attr('class','btn_type01');
		$("#mid_add_btn").css('color','#fff');
		
		$("#mid_del_btn").attr('href',"javascript:OnClickDelete()");
		$("#mid_del_btn").attr('class','btn_type01');
		$("#mid_del_btn").css('color','#fff');
	}
	for(var index=0; index<5; index++)
	{			
		if ($("#preset_schedule").val() == 0) {
			$('#imagepreset_select_'+index).attr('disabled','disabled');
			$('#imagepreset_mode_'+index).attr('disabled', 'disabled');
			$('#imagepreset_start_'+index).attr('disabled', 'disabled');
			$('#imagepreset_end_'+index).attr('disabled', 'disabled');
		}
		else {				
			$('#imagepreset_select_'+index).removeAttr("disabled");
			if ($("input[name='imagepreset_select']:checked").val() == index) {
				$('#imagepreset_mode_'+index).removeAttr("disabled");
				$('#imagepreset_start_'+index).removeAttr("disabled");
				$('#imagepreset_end_'+index).removeAttr("disabled");
			}
		}
	}
}

function InitImagePresetScheduleTime()
{
<?php
	for ($index=0; $index<5; ++$index) {
		$hour = $imagePreset->schedule[$index]->dataInfo['StartHour']['value'];
		$min = $imagePreset->schedule[$index]->dataInfo['StartMin']['value'];
		$startTime = ($hour<10?'0'.$hour:$hour).':'.($min<10?'0'.$min:$min);
		$hour = $imagePreset->schedule[$index]->dataInfo['EndHour']['value'];
		$min = $imagePreset->schedule[$index]->dataInfo['EndMin']['value'];
		$endTime = ($hour<10?'0'.$hour:$hour).':'.($min<10?'0'.$min:$min);
?>
		if($('tr').hasClass("imagepreset_list_<?php echo $index;?>")) {
			selNo = "<?php echo $index;?>";

			$('#imagepreset_start_<?php echo $index;?>').timepicker({
				hourText:"<?php echo $t_hour[$GLOBALS['LANGINDEX']];?>",
				minuteText:"<?php echo $t_minute[$GLOBALS['LANGINDEX']];?>"
			});
			$('#imagepreset_end_<?php echo $index;?>').timepicker({
				hourText:"<?php echo $t_hour[$GLOBALS['LANGINDEX']];?>",
				minuteText:"<?php echo $t_minute[$GLOBALS['LANGINDEX']];?>"
			});
			
			$('#imagepreset_start_<?php echo $index;?>').val("<?php echo $startTime; ?>"+":00");
			$('#imagepreset_end_<?php echo $index;?>').val("<?php echo $endTime; ?>"+":59");
			
			/*
			$('#imagepreset_start_<?php echo $index;?>').timepicker('setTime',"<?php echo $imagePreset->schedule[$index]->dataInfo['StartHour']['value'].':'.$imagePreset->schedule[$index]->dataInfo['StartMin']['value']; ?>");
			$('#imagepreset_end_<?php echo $index;?>').timepicker('setTime',"<?php echo $imagePreset->schedule[$index]->dataInfo['EndHour']['value'].':'.$imagePreset->schedule[$index]->dataInfo['EndMin']['value']; ?>");
			*/
		}
<?php
	}
?>
	selNo = 0;
}


function OnClickImagePresetList()
{
	selNo = $("input[name='imagepreset_select']:checked").val(); 
	if ((selNo != oldSelNo) && typeof oldSelNo != "undefined") {
		$('#imagepreset_mode_'+oldSelNo).attr('disabled', 'disabled');
		$('#imagepreset_start_'+oldSelNo).attr('disabled', 'disabled');
		$('#imagepreset_end_'+oldSelNo).attr('disabled', 'disabled');
	}
	$('#imagepreset_mode_'+selNo).removeAttr('disabled');
	$('#imagepreset_start_'+selNo).removeAttr('disabled');
	$('#imagepreset_end_'+selNo).removeAttr('disabled');
	oldSelNo = selNo;
}


function OnClickAdd()
{
	if ($("#preset_schedule").val() == 0) return;
	if (imagepreset_cnt == 5) {
		alert("<?php echo $msg_cannot_add[$GLOBALS['LANGINDEX']]; ?>");
		return;
	}

	var addNo = 0;
	for(var index=0; index<5; ++index) {
		if($('tr').hasClass('imagepreset_list_'+index)) continue;
		addNo = index;
		break;
	}
 
	$('#imagepreset_list').append(
		"<tr class='imagepreset_list_"+addNo+"'>\
			<td><input type='radio' name='imagepreset_select' id='imagepreset_select_"+addNo+"' onClick='OnClickImagePresetList();' value='"+addNo+"' checked='checked'/></td>\
			<td><select id='imagepreset_mode_"+addNo+"' class='selectbox_style_wid230' style='width:340px;' >\
		<?php
			for($index2=1; $index2<count($presetModeLangList); ++$index2) {
		?>
				<option value=\"<?php echo $index2;?>\"><?php echo $presetModeLangList[$index2]; ?></option>\
		<?php
			}
		?>
			</select></td>\
			<td><input type='text' class='text' name='start' style='width:110px;text-align:center' id='imagepreset_start_"+addNo+"' onkeydown='return false;'/></td><td>~</td><td><input type='text' class='text' name='end' style='width:110px;text-align:center' id='imagepreset_end_"+addNo+"' onkeydown='return false;'/></td>\
		</tr>"
	);

	imagepreset_cnt++;		
	OnClickImagePresetList();

	$('#imagepreset_start_'+addNo).timepicker({
		hourText:"<?php echo $t_hour[$GLOBALS['LANGINDEX']];?>",
		minuteText:"<?php echo $t_minute[$GLOBALS['LANGINDEX']];?>"
	});
	$('#imagepreset_end_'+addNo).timepicker({
		hourText:"<?php echo $t_hour[$GLOBALS['LANGINDEX']];?>",
		minuteText:"<?php echo $t_minute[$GLOBALS['LANGINDEX']];?>"
	});
	$('#imagepreset_start_'+addNo).val('00:00:00');
	$('#imagepreset_end_'+addNo).val('23:59:59');
}

function CheckDeletedImagePreset(obj)
{
	var selNo = $("input[name='"+obj+"_select']:checked").val();
	var selClassName = obj+'_list_'+selNo;
	var trNo = $('#'+obj+'_list tbody tr').size();
	
	if (typeof selNo == "undefined") return false;

	for(var index=0; index < trNo; ++index){
		if($("#"+obj+"_list tbody tr:eq("+index+")").attr("class") == selClassName){
			trNo = index;
			break;
		}
	}
	
	$('tr').detach('.'+obj+'_list_'+selNo);
	
	if($('#'+obj+'_list tbody tr').size() != 0){
		if($('#'+obj+'_list tbody tr').size() == trNo){
			trNo -= 1;
		}
		$("input[name='"+obj+"_select']:eq("+trNo+")").prop('checked', true);
	}
	
	eval(obj+"_cnt--;");
	return true;
}

function OnClickDelete()
{
	if ($("#preset_schedule").val() == 0) return;
	if ($("#imagepreset_list tbody tr").size() == 1){
		alert("<?php echo $msg_preset_delete[$GLOBALS['LANGINDEX']]; ?>");
		return;
	}
	if (!CheckDeletedImagePreset('imagepreset')) return;
	OnClickImagePresetList();
}

</script>

<table class="data_write mgt10 mgl-20 pdl15" style="width:670px;">
	<colgroup>
		<col style="width:180px;"/>
		<col />
	</colgroup>
	<tbody>
		<tr>
		<th><?php echo $t_mode[$GLOBALS["LANGINDEX"]]; ?></th>
		<td>
			<select id="preset_default" class="selectbox_style_wid230" style="width:340px;" onchange="OnChangePresetMode()">
		<?php
			for($index=1; $index<count($presetModeLangList); ++$index) {
		?> 			
				<option value="<?php echo $index;?>" <?php if($imagePreset->dataInfo['DefaultMode']['value'] == $index) echo "selected=\"selected\""; ?>><?php echo $presetModeLangList[$index]; ?></option>
		<?php
			}
		?>
			</select>
		</td>
		</tr>
		<tr>
		<th class="top_txt"><?php echo $t_schedule[$GLOBALS["LANGINDEX"]]; ?></th>
		<td>
			<select id="preset_schedule" class="selectbox_style_wid230" onchange="OnChangePresetScheduleMode()">
				<option value="0" <?php if($imagePreset->dataInfo['ScheduleMode']['value'] == 0) echo "selected=\"selected\""; ?>><?php echo $t_off[$GLOBALS["LANGINDEX"]]; ?></option>
				<option value="1" <?php if($imagePreset->dataInfo['ScheduleMode']['value'] == 1) echo "selected=\"selected\""; ?>><?php echo $t_on[$GLOBALS["LANGINDEX"]]; ?></option>
			</select>
		</td>
		</tr>
		<tr>
		<th class="top_txt"><?php echo $t_schedule_time[$GLOBALS["LANGINDEX"]]; ?></th>
		<td>
			<a id="mid_add_btn" class="btn_type01" style="color:#fff" href="javascript:OnClickAdd()"><?php echo $t_add[$GLOBALS['LANGINDEX']]; ?></a>&nbsp;&nbsp;&nbsp;
			<a id="mid_del_btn" class="btn_type01" style="color:#fff" href="javascript:OnClickDelete()"><?php echo $t_delete[$GLOBALS['LANGINDEX']]; ?></a>
		</td>
		</tr>
	</tbody>
</table>
<table id="imagepreset_list" class="data_write mgt10 mgl-20 pdl15" style="width:630px;">
	<colgroup>
		<col style="width:27px;" />
		<col style="width:230px;" />
		<col style="width:115px;" />
		<col style="width:20px;" />
		<col />
	</colgroup>
	<thead>
	<tr style="color:#fff">
		<th></th>
		<th style="font-weight:normal;text-align:center;padding-left:10px;"><?php echo $t_mode[$GLOBALS["LANGINDEX"]]; ?></th>
		<th style="font-weight:normal;text-align:center;padding-left:10px;"><?php echo $t_startTime[$GLOBALS["LANGINDEX"]]; ?></th>
		<th></th>
		<th style="font-weight:normal;text-align:center;padding-left:10px;"><?php echo $t_endTime[$GLOBALS["LANGINDEX"]]; ?></th>
	</tr>
	<tbody>
<?php
	$presetCnt = 0;
for ($index=0; $index<5; ++$index) {
	if ($imagePreset->schedule[$index]->dataInfo['Mode']['value'] != 0) {
?>
		<tr class="imagepreset_list_<?php echo $presetCnt; ?>">
			<td><input type="radio" name="imagepreset_select" id="imagepreset_select_<?php echo $presetCnt; ?>" onClick="OnClickImagePresetList();" value="<?php echo $presetCnt; ?>" <?php if ($presetCnt == 0) echo 'checked';?>/></td>
			<td>
				<select id="imagepreset_mode_<?php echo $presetCnt; ?>" class="selectbox_style_wid230" style="width:340px;" <?php if ($presetCnt != 0) echo "disabled=\"disabled\"";?>>
			<?php
				for($index2=1; $index2<count($presetModeLangList); ++$index2) {
			?>
					<option value="<?php echo $index2;?>" <?php if($imagePreset->schedule[$index]->dataInfo['Mode']['value'] == $index2) echo "selected=\"selected\""; ?>> <?php echo $presetModeLangList[$index2]; ?> </option>
			<?php
				}
			?>
				</select>
			</td>
			<td>	
				<input type="text" class="text" name='start' style="width:110px;text-align:center" id="imagepreset_start_<?php echo $presetCnt;?>" onkeydown="return false;" <?php if ($presetCnt != 0) echo "disabled=\"disabled\"";?>/>
			</td>
			<td>~</td>
			<td>
				<input type="text" class="text" name='end' style="width:110px;text-align:center" id="imagepreset_end_<?php echo $presetCnt;?>" onkeydown="return false;" <?php if ($presetCnt != 0) echo "disabled=\"disabled\"";?>/>
			</td>
		</tr>
<?php
		$presetCnt++;
	}
}
?>
	</tbody>
</table>
<script>
	imagepreset_cnt = parseInt(<?php echo $presetCnt; ?>);
</script>						
