<script type="text/javascript" language="javascript">

var mode 		= new Array();
var fromHour 	= new Array();
var fromMin 	= new Array();
var toHour 		= new Array();
var toMin 		= new Array();

$(document).ready(function(){
	<?php for($index=0; $index<5; $index++){ ?>
		mode[<?php echo $index; ?>]		= <?php echo $imagePreset->schedule[$index]->dataInfo['Mode']['value']; ?>;
		fromHour[<?php echo $index; ?>]	= <?php echo $imagePreset->schedule[$index]->dataInfo['StartHour']['value']; ?>;
		fromMin[<?php echo $index; ?>]	= <?php echo $imagePreset->schedule[$index]->dataInfo['StartMin']['value']; ?>;
		toHour[<?php echo $index; ?>] 	= <?php echo $imagePreset->schedule[$index]->dataInfo['EndHour']['value']; ?>;
		toMin[<?php echo $index; ?>]		= <?php echo $imagePreset->schedule[$index]->dataInfo['EndMin']['value']; ?>;
	
		$("#imagepreset_mode_<?php echo $index; ?>").val(mode[<?php echo $index; ?>]);
		$("#from_hour_<?php echo $index; ?>").val(fromHour[<?php echo $index; ?>]);
		$("#from_min_<?php echo $index; ?>").val(fromMin[<?php echo $index; ?>]);
		$("#to_hour_<?php echo $index; ?>").val(toHour[<?php echo $index; ?>]);
		$("#to_min_<?php echo $index; ?>").val(toMin[<?php echo $index; ?>]);	
	<?php } ?>
	OnChangeSchedulePresetMode();
});

	function updatePresetScheduleTimeBar() {
		var defaultMode = $("#preset_default").val();
		var timeObj = $("#imagepreset_timebar");

		timeObj.children(" div").removeClass();
		timeObj.children(" div").css("display","none");
		timeObj.children(" div").html("");

		if($("#imagepreset_act_always").is(':checked')) {	
			$("#imagepreset_set_btn").removeClass();
			$("#imagepreset_set_btn").addClass("btn_disable");
			$("#imagepreset_set_btn").unbind("click");
			$("#imagepreset_set_btn").css("cursor","default");
			MakeTimeBar(0, 24, 0, defaultMode, 0, 0, 23, 59);
			return;
		}
		else {			
			$("#imagepreset_set_btn").removeClass();
			$("#imagepreset_set_btn").addClass("btn_type01");
			$("#imagepreset_set_btn").css("cursor","pointer");
			$("#imagepreset_set_btn").bind("click",function(e){
				$("#presetScheduleSet").dialog("open");	
				$("#presetScheduleSet").dialog("widget").position({
					my: 'center',
					of: window
				});
			});
		}
		
		var tmpMode = new Array();
		var tmpFromHour = new Array();
		var tmpFromMin = new Array();
		var tmpToHour = new Array();
		var tmpToMin = new Array();
		
		var index = 0;
		for(var i = 0; i < 5; i++){
			if(mode[i] != 0){
				tmpMode[index]    = mode[i];
				tmpFromHour[index]= fromHour[i];
				tmpFromMin[index] = fromMin[i];
				tmpToHour[index]	= toHour[i];
				tmpToMin[index]	= toMin[i];
				index++;
			}
		}

		if(tmpMode.length == 0){
			MakeTimeBar(0, 24, 0, defaultMode, 0, 0, 23, 59);
			return;
		}
		var swpMode = 0;
		var swpFromHour = 0;
		var swpFromMin = 0;
		var swpToHour = 0;
		var swpToMin = 0;
		
		if(tmpMode.length > 1){				//Sorting
			for(var i =0; i < tmpMode.length-1; i++){
				for(var j = i+1; j < tmpMode.length; j++){
					if((tmpFromHour[i] > tmpToHour[j]) || ((tmpFromHour[i] == tmpToHour[j]) && (tmpFromMin[i] > tmpToMin[j]))){
						swpMode = tmpMode[i];	
						swpFromHour = tmpFromHour[i];
						swpFromMin = tmpFromMin[i];
						swpToHour = tmpToHour[i];
						swpToMin = tmpToMin[i];
						
						tmpMode[i] = tmpMode[j];	
						tmpFromHour[i] = tmpFromHour[j];
						tmpFromMin[i] = tmpFromMin[j];
						tmpToHour[i] = tmpToHour[j];
						tmpToMin[i] = tmpToMin[j];

						tmpMode[j] = swpMode;	
						tmpFromHour[j] = swpFromHour;
						tmpFromMin[j] = swpFromMin;
						tmpToHour[j] = swpToHour;
						tmpToMin[j] = swpToMin;						
					}
				}
			}
		}
		
		var divIndex = 0;
		var totalWidth = 0;
		for(var i = 0; i < tmpMode.length; i++){
			if(i == 0){
				if(tmpFromHour[i] == 0 && tmpFromMin[i] == 0){
					totalWidth += MakeTimeBar(divIndex, tmpToHour[i], tmpToMin[i], tmpMode[i], 0, 0, tmpToHour[i], tmpToMin[i]);
				}else{
					var eM = tmpFromMin[i] -1;
					var eH = tmpFromHour[i];
					if(eM < 0){
						eH = eH-1;
						eM = 59;
					}
					totalWidth += MakeTimeBar(divIndex, eH, eM, defaultMode, 0, 0, eH, eM);
					divIndex++;
					totalWidth += MakeTimeBar(divIndex, tmpToHour[i]-eH, tmpToMin[i]-eM, tmpMode[i], tmpFromHour[i], tmpFromMin[i], tmpToHour[i], tmpToMin[i]);
				}
				divIndex++;
			}else{				
				var eM = tmpFromMin[i] -1;
				var eH = tmpFromHour[i];
				if(eM < 0){
					eH = eH -1;
					eM = 59;
				}	
				if(!(eH == tmpToHour[i-1] && eM == tmpToMin[i-1])){
					var sM = tmpToMin[i-1] +1;
					var sH = tmpToHour[i-1];
					if(sM > 59){
						sH = sH +1;
						sM = 0;
					}
					totalWidth += MakeTimeBar(divIndex, tmpFromHour[i]-sH, tmpFromMin[i]-sM, defaultMode, sH, sM, eH, eM);
					divIndex++;
				}
				totalWidth += MakeTimeBar(divIndex, tmpToHour[i]-eH, tmpToMin[i]-eM, tmpMode[i], tmpFromHour[i], tmpFromMin[i], tmpToHour[i], tmpToMin[i]);
				divIndex++;
			}
		}
		if(!(tmpToHour[tmpMode.length-1] == 23 && tmpToMin[tmpMode.length-1] == 59)){
			var sM = tmpToMin[tmpMode.length-1] +1;
			var sH = tmpToHour[tmpMode.length-1];
			if(sM > 59){
				sH = sH +1;
				sM = 0;
			}
			totalWidth += MakeTimeBar(divIndex, 23-tmpToHour[tmpMode.length-1], 59-tmpToMin[tmpMode.length-1], defaultMode, sH, sM, 23, 59);
		}

		if(totalWidth != 672){
			divIndex = divIndex-1;
			var overWidth = totalWidth - 672;
			var lastWidth = parseInt(timeObj.children(" div:eq("+divIndex+")").css("width"),10)-overWidth;
			var timeObj = $("#imagepreset_timebar")	;
			timeObj.children(" div:eq("+divIndex+")").css({"width":lastWidth+"px"});
		}		
	}

	function MakeTimeBar(divIndex, hWidth, mWidth, mode, sHour, sMin, eHour, eMin){
		var strMode = GetScheduleClass(mode);
		var timeObj = $("#imagepreset_timebar")	;
		var hWidth = hWidth * 28;
		var mWidth = parseInt(mWidth/2, 10);
		var divWidth = 0;

		if(mWidth > 28)
			mWidth = 28;
			
		divWidth = hWidth + mWidth;
		timeObj.children(" div:eq("+divIndex+")").addClass(strMode);
		timeObj.children(" div:eq("+divIndex+")").css({"width":divWidth+"px","display":"block"});
		timeObj.children(" div:eq("+divIndex+")").append("<span class=\"startTime\" style=\"display:none\">"+sHour+","+sMin+"</span><span class=\"endTime\" style=\"display:none\">"+eHour+","+eMin+"</span>");

		return divWidth;
	}
	
	function GetScheduleClass(index){
		var strMode = "";
		var index = parseInt(index,10);
		switch(index){
			case 0 : strMode= "none"; break;
			case 1 : strMode= "setDefineFocus"; break;
			case 2 : strMode= "setMotionFocus"; break;
			case 3 : strMode= "setReduceNoise"; break;
			case 4 : strMode= "setBrightVideo"; break;
			case 5 : strMode= "setMotionFocus_ReduceNoise"; break;
			case 6 : strMode= "setMotionFocus_BrightVideo"; break;	
			case 7 : strMode= "setUserPreset"; break;
		}		
		return strMode;
	}

	function OnChangeSchedulePresetMode() {
		for(var i = 0; i < 5; i++) {
			if($("#imagepreset_mode_"+ i).val() != 0) {			
				$("#from_hour_"+ i).removeAttr('disabled');
				$("#from_min_"+ i).removeAttr('disabled');
				$("#from_sec_"+ i).css('color', '#000');
				$("#to_hour_"+ i).removeAttr('disabled');
				$("#to_min_"+ i).removeAttr('disabled');
				$("#to_sec_"+ i).css('color', '#000');
			}
			else {
				$("#from_hour_"+ i).attr('disabled', 'disabled');
				$("#from_min_"+ i).attr('disabled', 'disabled');
				$("#from_sec_"+ i).css('color', '#808080');
				$("#to_hour_"+ i).attr('disabled', 'disabled');
				$("#to_min_"+ i).attr('disabled', 'disabled');
				$("#to_sec_"+ i).css('color', '#808080');
			}
		}
	}

	function MakeImagepresetXml()
	{
		var msg = "";	

		var presetMode = "#imagepreset_mode_";	
		var startTimeId = "#imagepreset_list input[name='start']";
		var endTimeId = "#imagepreset_list input[name='end']";
		
		msg += "<ImagePreset>";
		msg +=	"<DefaultMode>"+ $("#preset_default").val() +"</DefaultMode>";
		msg +=	"<ScheduleMode>"+ ($("#imagepreset_act_timesched").is(':checked')?1:0) +"</ScheduleMode>";
		
		for (var index=0; index<5; index++) {
			msg +=	"<PresetSchedule"+index+">";
			
			var tempMode = $("#imagepreset_mode_"+index+" option:selected").val();
			var tempStartHour = $("#from_hour_"+index).val();
			var tempStartMin	= $("#from_min_"+index).val();
			var tempEndHour	= $("#to_hour_"+index).val();
			var tempEndMin 	= $("#to_min_"+index).val();
		
			msg +=	"<Mode>"+ tempMode +"</Mode>";
			msg += "<StartHour>"+ tempStartHour +"</StartHour>";
			msg += "<StartMin>"+ tempStartMin +"</StartMin>";
			msg += "<EndHour>"+ tempEndHour +"</EndHour>";
			msg += "<EndMin>"+ tempEndMin +"</EndMin>";
			
			msg +=	"</PresetSchedule"+index+">";
		}
		msg +="</ImagePreset>"
		return msg;
	}
</script>

	<div style="margin-top:10px;">		
		<div class="h3_tit mgt0" style="overflow:auto;width:680px;">
			<h3 class="wid220"><?php echo $t_activation_time[$GLOBALS['LANGINDEX']]; ?></h3>
		</div>
		<table class="data_write">
			<tbody>
				<tr>
					<td>
						<label>
							<input type="radio" name="imagepreset_act" id="imagepreset_act_always" onclick="updatePresetScheduleTimeBar()" <?php if ($imagePreset->dataInfo['ScheduleMode']['value'] == 0) echo "checked=\"checked\""; ?> style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_off[$GLOBALS['LANGINDEX']]; ?> &nbsp;&nbsp;
						</label>
						<label>
							<input type="radio" name="imagepreset_act" id="imagepreset_act_timesched" onclick="updatePresetScheduleTimeBar()" <?php if ($imagePreset->dataInfo['ScheduleMode']['value'] == 1) echo "checked=\"checked\""; ?> /><?php echo $t_only_schedule[$GLOBALS['LANGINDEX']]; ?>
						</label>
					</td>				
					<td>
						<a class="btn_type01" style="position:relative; float:right; margin-right:2px" id="imagepreset_set_btn"><?php echo $t_set[$GLOBALS['LANGINDEX']]; ?></a>
					</td>
				</tr>
				<tr>
				</tr>
			</tbody>
		</table>
		<div class="mgl5" style="height:100px;width:100%">
			<div id="imagepreset_timeschedule_cover" class="timeschedule_cover">				
				<div id="imagepreset_timeschedule_table" style="" cellspacing="0" cellpadding="0" class="scheduleTable">
					<div style="height:27px">
						<?php for($index=0; $index < 24; $index++){ 
							$hour = $index;
							if($index < 10)
								$hour = "0".$index;
						?>
							<div style="float:left" class="dayHead"><?php echo $hour;?></div>
						<?php } ?>
					</div>
					<div id="imagepreset_timebar">
						<div style="float:left;width:672px;height:25px;display:block;background:#8E939E;color:#000;"></div>
					<?php for($index=1; $index < 11; $index++){ ?>
						<div style="float:left;height:25px;display:none;background:#8E939E;color:#000;"></div>
					<?php } ?>
					</div>
				</div>
				<div>
					<table style="width:680px; font:12px/15px Verdana, sans-serif;">
						<colgroup>
							<col style="width:50%;"/>
							<col />
						</colgroup>
						<tbody>
							<tr>
								<td> <a class="setDefineFocus scheduleColorInfo"></a><span style="color:#fff;font-size:9px"><?php echo $t_defineFocus[$GLOBALS['LANGINDEX']]; ?></span> </td>
								<td> <a class="setMotionFocus scheduleColorInfo"></a><span style="color:#fff;font-size:9px"><?php echo $t_motionFocus[$GLOBALS['LANGINDEX']]; ?></span> </td>
							</tr> 
							<tr>
								<td> <a class="setReduceNoise scheduleColorInfo"></a><span style="color:#fff;font-size:9px"><?php echo $t_reduceNoise[$GLOBALS['LANGINDEX']]; ?></span> </td>
								<td> <a class="setBrightVideo scheduleColorInfo"></a><span style="color:#fff;font-size:9px"><?php echo $t_brightVideo[$GLOBALS['LANGINDEX']]; ?></span><br/> </td>
							</tr>
							<tr>
								<td> <a class="setMotionFocus_ReduceNoise scheduleColorInfo"></a><span style="color:#fff;font-size:9px"><?php echo $t_motionFocus[$GLOBALS['LANGINDEX']].'&'.$t_reduceNoise[$GLOBALS["LANGINDEX"]]; ?></span> </td>
								<td> <a class="setMotionFocus_BrightVideo scheduleColorInfo"></a><span style="color:#fff;font-size:9px"><?php echo $t_motionFocus[$GLOBALS['LANGINDEX']].'&'.$t_brightVideo[$GLOBALS["LANGINDEX"]]; ?></span> </td>
							</tr>
							<tr>
								<td colspan="2"> <a class="setUserPreset scheduleColorInfo"></a><span style="color:#fff;font-size:9px"><?php echo $t_userPreset[$GLOBALS['LANGINDEX']]; ?></span>  </td>
							</tr>
						</tbody>
					</table>
				</div>				
			</div>
		</div>
<script type="text/javascript" language="javascript">

var modeNameList = ["", "DefineFocus","MotionFocus","ReduceNoise","BrightVideo","MotionFocus_ReduceNoise","MotionFocus_BrightVideo","UserPreset"];
var modeLanguageList = ["", "<?php echo $t_defineFocus[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $t_motionFocus[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $t_reduceNoise[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $t_brightVideo[$GLOBALS['LANGINDEX']]; ?>", 
								"<?php echo $t_motionFocus[$GLOBALS['LANGINDEX']].'&'.$t_reduceNoise[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $t_motionFocus[$GLOBALS['LANGINDEX']].'&'.$t_brightVideo[$GLOBALS['LANGINDEX']]; ?>",  "<?php echo $t_userPreset[$GLOBALS['LANGINDEX']]; ?>"];
var alertList = ["<?php echo $msg_invalid_time[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $msg_preset_duplicate[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $msg_cannot_add[$GLOBALS['LANGINDEX']]; ?>"];				
var tooltipInfo = {	"Mode":"<?php echo $t_mode[$GLOBALS['LANGINDEX']]; ?>",
							"Time":"<?php echo $t_time[$GLOBALS['LANGINDEX']]; ?>" }
var buttonLang = ["<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $t_cancel[$GLOBALS['LANGINDEX']]; ?>"];

</script>
	<div id="presetScheduleSet" style="display:none;width:auto;" >
		<table id="imagepreset_list" class="data_write mgt10 mgl-20 pdl15" style="width:auto;">
			<colgroup>
				<col style="width:100px;"/>
				<col style="width:70px;"/>
				<col style="width:70px;"/>
				<col style="width:32px;"/>
				<col style="width:70px;"/>
				<col style="width:70px;"/>
				<col />
			</colgroup>
			<tbody>
				<tr>
					<th colspan="7"><?php echo $msg_cannot_preset_duplicate[$GLOBALS["LANGINDEX"]]; ?></th>
				</tr>
			<?php for($index=0; $index<5; $index++) { ?>
				<tr class="imagepreset_list_<?php echo $index; ?>">
					<th> <?php echo $t_mode[$GLOBALS["LANGINDEX"]]; ?> </th>
					<td colspan="7">
						<select id="imagepreset_mode_<?php echo $index; ?>" class="selectbox_style" style="width: 340px" onchange="OnChangeSchedulePresetMode()">	
							<option value="0" > --- </option>
							<option value="1" > <?php echo $t_defineFocus[$GLOBALS['LANGINDEX']]; ?> </option>
							<option value="2" > <?php echo $t_motionFocus[$GLOBALS['LANGINDEX']]; ?> </option>
							<option value="3" > <?php echo $t_reduceNoise[$GLOBALS['LANGINDEX']]; ?> </option>
							<option value="4" > <?php echo $t_brightVideo[$GLOBALS['LANGINDEX']]; ?> </option>
							<option value="5" > <?php echo $t_motionFocus[$GLOBALS['LANGINDEX']].'&'.$t_reduceNoise[$GLOBALS["LANGINDEX"]]; ?> </option>
							<option value="6" > <?php echo $t_motionFocus[$GLOBALS['LANGINDEX']].'&'.$t_brightVideo[$GLOBALS["LANGINDEX"]]; ?> </option>
							<option value="7" > <?php echo $t_userPreset[$GLOBALS['LANGINDEX']]; ?> </option>
						</select>
					</td>
				</tr>
				<tr>
					<th><?php echo $t_time[$GLOBALS['LANGINDEX']]; ?> </th>
					<td><select id="from_hour_<?php echo $index; ?>" class="selectbox_style" style="width:70px;" disabled="disabled"></select>:</td>
					<td><select id="from_min_<?php echo $index; ?>" class="selectbox_style" style="width:70px" disabled="disabled"></select></td>
					<!--td><input type="text" id="from_sec_<?php echo $index; ?>" style="width:40px;text-align:center;margin-right:1px;" value="00" readonly="" onkeydown="return false;" /></td-->
					<td style="padding-left:16px"> ~ </td>
					<td><select id="to_hour_<?php echo $index; ?>" class="selectbox_style" style="width:70px;" disabled="disabled"></select>:</td>
					<td><select id="to_min_<?php echo $index; ?>" class="selectbox_style" style="width:70px" disabled="disabled"></select></td>
					<td></td>
					<!--td><input type="text" id="to_sec_<?php echo $index; ?>" style="width:40px;text-align:center;margin-right:1px;" value="59" readonly="" onkeydown="return false;" /></td-->
				</tr>
				<tr>	
					<td colspan="7"><div style="border-bottom:1px solid #737c8f"></div>	</td> 			
				</tr>
			
			<?php } ?>
			</tbody>
		</table>
	</div>	

<script>
	jQuery("#presetScheduleSet").dialog({
		autoOpen: false,
		modal: true,	
		title: "<?php echo $t_setup[$GLOBALS['LANGINDEX']]; ?>"
	});
</script>
											
<style>
div.scheduleTable{
	width: 100%;
	height: 60px;
}

/*
div.scheduleTable tbody tr td:first-child{
}
*/
.dayHead{
	border-top: 1px solid #7C7F85;
	border-left: 1px solid #7C7F85;
	border-bottom: 1px solid #7C7F85;
	line-height:25px;
	text-align: center;
 	background: none repeat scroll 0 0 #8E939E;
	color: #000;
	width: 27px;
	height: 25px;
}

.timeschedule_cover{
	width: 100%;
	height: 60px;
	position: relative;
	float:left;
	margin-top:10px;
}
.setDefineFocus {
	background:#54c0ff !important;
}
.setMotionFocus {
	background:#ffa52f !important;
}
.setReduceNoise {
	background:#5eec5f !important;
}
.setBrightVideo {
	background:#923ee6 !important;
}
.setMotionFocus_ReduceNoise {
	background:#ef5ca8 !important;
}
.setMotionFocus_BrightVideo {
	background:#ffff77 !important;
}
.setUserPreset {
	background:#3464ff !important;
}
.scheduleColorInfo{
	display:inline-block;
	width:9px;
	height:9px;
	vertical-align:middle;
	font-weight:bold;
	margin-right:3px;
}
.ui-dialog-titlebar-close .ui-button-text{
	display:none;
}
.ui-dialog-titlebar-close{
	float:right;
}
.scheduleTable .ui-dialog-title{
	float:left;
}
	.ui-dialog{
		z-index:1000 !important;
		background: #EFF1F3;
	}
	.ui-dialog .ui-widget-header {
			background: #E4E7EA;
			font-weight: bold;
			font-size: 11px;
			border: none;
			height: 20px;
			padding-left: 10px;
		}
.ui-widget-overlay{
	background: none repeat scroll 0 0 #000000;
	opacity: 0;   
	filter:alpha(opacity=0);
	height: 1800px;
	width: 105%;
	position: absolute;
	z-index: 1000;
}		
.ui-dialog .ui-dialog-titlebar-close{
	background: none;
	border: none;
}
.ui-dialog .ui-widget-content {background: #EFF1F3;border: none;margin-left: 20px;}
.ui-dialog .ui-dialog-buttonpane .ui-dialog-buttonset {text-align:center; margin-right:10px;}
.ui-dialog .ui-dialog-buttonset button{background: #EFF1F3; margin: 0 10px;}
.ui-dialog .ui-resizable-handle{ display: none !important;}
.ui-dialog .ui-widget-content p{ display:block;clear: both;}
.ui-dialog .ui-widget-content input,.ui-dialog .ui-widget-content label{float:left;}
.ui-button.ui-state-default { color:#000;}
.ui-dialog.scheduleTable {
	left: 490px !important;
	width: 400px !important;
}
.ui-dialog.scheduleDelTable {
	left: 385px !important;
	width: 620px !important;
}
.ui-dialog.scheduleSetTable {
	left: 385px !important;
	width: 505px !important;
}

.ui-dialog table.data_write tbody th {
	text-align:left;
	color:black;
}
.ui-dialog table.data_write tbody td {
	font-weight:normal;
	color:black;
}

.ui-dialog input.text {
	background: none repeat scroll 0 0 #FFFFFF;
	margin-left:-1px;
	margin-right:10px;
}
	.ui-dialog input.text:disabled {
	color:#6d6d6d;
}
.ui-dialog select {
	background: none repeat scroll 0 0 #FFFFFF;
}

</style> 
