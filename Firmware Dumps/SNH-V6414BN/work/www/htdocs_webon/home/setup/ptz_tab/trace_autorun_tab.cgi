<script type="text/javascript" language="javascript">

var presetNumberAlert = "<?php echo $t_preset[$GLOBALS['LANGINDEX']]; ?> : <?php echo EnterNumber(1,255); ?>";
var groupNumberAlert = "<?php echo $t_group[$GLOBALS['LANGINDEX']]; ?> : <?php echo EnterNumber(1,6); ?>";
var traceNumberAlert = "<?php echo $t_trace[$GLOBALS['LANGINDEX']]; ?> : <?php echo EnterNumber(1,4); ?>";
var autoPanSpeedAlert = "<?php echo $t_autoPan[$GLOBALS['LANGINDEX']]; ?> : <?php echo EnterNumber(1,50); ?>";
var autoPanTiltangleAlert = "<?php echo $t_autoPan[$GLOBALS['LANGINDEX']]; ?> : <?php echo EnterNumber(0,85); ?>";

function OnClickTrace(mode)
{
	var msg = "";
	msg += "<StartPTZTrace>";
	msg += "<Index>"+$("#Trace-Number").val()+"</Index>";
	msg += "<Mode>"+mode+"</Mode>";
	msg += "</StartPTZTrace>";
	RequestAjaxMsg(msg, "", ajaxReqUrl, 'NO_REFRESH');
}

function OnClickApplyAutorun()
{
	if (CheckValueRange($("#AutoRunPreset-Number").val(), 1, 255, "<?php echo $t_preset[$GLOBALS['LANGINDEX']]; ?> : <?php echo EnterNumber(1,255); ?>")) return;
	if (CheckValueRange($("#AutoRunGroupNo").val(), 1, 6, "<?php echo $t_group[$GLOBALS['LANGINDEX']]; ?> : <?php echo EnterNumber(1,6); ?>")) return;
	if (CheckValueRange($("#AutoRunTrace-Number").val(), 1, 4, "<?php echo $t_trace[$GLOBALS['LANGINDEX']]; ?> : <?php echo EnterNumber(1,4); ?>")) return;
	if (CheckValueRange($("#AutoPan-Speed").val(), 1, 50, "<?php echo $t_autoPan[$GLOBALS['LANGINDEX']]; ?> : <?php echo EnterNumber(1,50); ?>")) return;
	if (CheckValueRange($("#AutoPan-Tiltangle").val(), 0, 85, "<?php echo $t_autoPan[$GLOBALS['LANGINDEX']]; ?> : <?php echo EnterNumber(0,85); ?>")) return;
	
	if(!TypeCheck($('#AutoRunPreset-Number').val(), NUM+ALPHA)) {
		alert("<?php echo $t_preset[$GLOBALS['LANGINDEX']]; ?> : <?php echo EnterNumber(1,255); ?>");
		return;
	}
	if(!TypeCheck($('#AutoRunGroupNo').val(), NUM+ALPHA)) {
		alert("<?php echo $t_group[$GLOBALS['LANGINDEX']]; ?> : <?php echo EnterNumber(1,6); ?>");
		return;
	}
	if(!TypeCheck($('#AutoRunTrace-Number').val(), NUM+ALPHA)) {
		alert("<?php echo $t_trace[$GLOBALS['LANGINDEX']]; ?> : <?php echo EnterNumber(1,4); ?>");
		return;
	}
	if(!TypeCheck($('#AutoPan-Speed').val(), NUM+ALPHA)) {
		alert("<?php echo $t_autoPan[$GLOBALS['LANGINDEX']]; ?> : <?php echo EnterNumber(1,50); ?>");
		return;
	}
	if(!TypeCheck($('#AutoPan-Tiltangle').val(), NUM+ALPHA)) {
		alert("<?php echo $t_autoPan[$GLOBALS['LANGINDEX']]; ?> : <?php echo EnterNumber(0,85); ?>");
		return;
	}
	
	var msg = "";
	msg += "<SetPTZAutorun>";
	msg += "<Autorun>";
	msg += "<Mode>"+$("#AutoRunMode").val()+"</Mode>";
	msg += "<HomeTime>"+$("#AutoRunHome-Time").val()+"</HomeTime>";
	msg += "<PresetNumber>"+$("#AutoRunPreset-Number").val()+"</PresetNumber>";
	msg += "<PresetTime>"+$("#AutoRunPreset-Time").val()+"</PresetTime>";
	msg += "<SwingMode>"+$("#AutoRunSwingMode").val()+"</SwingMode>";
	msg += "<SwingTime>"+$("#AutoRunSwingTime").val()+"</SwingTime>";
	msg += "<GroupNumber>"+$("#AutoRunGroupNo").val()+"</GroupNumber>";
	msg += "<GroupTime>"+$("#AutoRunGroupTime").val()+"</GroupTime>";
	msg += "<TourTime>"+$("#AutoRunTourTime").val()+"</TourTime>";
	msg += "<TraceNumber>"+$("#AutoRunTrace-Number").val()+"</TraceNumber>";
	msg += "<TraceTime>"+$("#AutoRunTrace-Time").val()+"</TraceTime>";
	msg += "<AutoPanSpeed>"+$("#AutoPan-Speed").val()+"</AutoPanSpeed>";
	msg += "<AutoPanTiltangle>"+$("#AutoPan-Tiltangle").val()+"</AutoPanTiltangle>";
	msg += "<AutoPanTime>"+$("#AutoPan-Time").val()+"</AutoPanTime>";
	msg += "<ScheduleTime>"+$("#Schedule-Time").val()+"</ScheduleTime>";
	msg += "</Autorun>";
	msg += GetAutoRunScheduleData();
	msg += "</SetPTZAutorun>";

	SetPTZCookie('Autorun');
	RequestAjaxMsg(msg, "<?php echo $t_set[$GLOBALS['LANGINDEX']]; ?>", ajaxReqUrl);
}

function OnChangeAutoRunMode(param)
{
	if (typeof param == 'undefined') param = '';
	var autorunList = ['', 'Home', 'Preset', 'Swing', 'Group', 'Tour', 'Trace', 'Pan', 'Schedule'];
	for (var index=1; index<autorunList.length; ++index) {
		$("."+param+"Auto"+autorunList[index]+"Area").hide();
		if (autorunList[$('#'+param+'AutoRunMode').val()] == autorunList[index]) $("."+param+"Auto"+autorunList[index]+"Area").show();
	}
}

</script>

<div id="tabs-autorun">
	<table class="data_write mgt10 mgl-20 pdl15">
		<colgroup>
			<col style="width:180px;"/>
			<col />
		</colgroup>
		<tbody>
			<tr>
				<th colspan="2"> <?php echo $t_trace[$GLOBALS['LANGINDEX']]; ?> </th>
			</tr>
			<tr>
				<td style="padding-left:20px"> <?php echo $t_traceNo[$GLOBALS['LANGINDEX']]; ?> </td>
				<td>
					<select id="Trace-Number" class="selectbox_style" style="width:54px;">
						<option value="1">1</option>
						<option value="2">2</option>
						<option value="3">3</option>
						<option value="4">4</option>
					</select>
					&nbsp;
						<a class="btn_setup" href="javascript:OnClickTrace(0);" style="color:#fff; margin-top:-2px;"><?php echo $t_start[$GLOBALS['LANGINDEX']]; ?></a>
						<a class="btn_setup" href="javascript:OnClickTrace(2);" style="color:#fff; margin-top:-2px;"><?php echo $t_stop[$GLOBALS['LANGINDEX']]; ?></a>				
						<a class="btn_setup" href="javascript:OnClickTrace(1);" style="color:#fff; margin-top:-2px;"><?php echo $t_set[$GLOBALS['LANGINDEX']]; ?></a>
				</td>
			</tr>
		</tbody>
	</table>
	<table class="data_write mgt20 mgl-20 pdl15">
		<colgroup>
			<col style="width:180px;"/>
			<col />
		</colgroup>
		<tbody>
			<tr>
				<th colspan="2"> <?php echo $t_autoRun[$GLOBALS['LANGINDEX']]; ?> </th>
			</tr>
			<tr>
				<td style="padding-left:20px"> <?php echo $t_mode[$GLOBALS["LANGINDEX"]]; ?> </td>
				<td>
					<select id="AutoRunMode" class="selectbox_style_wid245" onchange="OnChangeAutoRunMode()" >
						<option value="0" <?php if($autorunConf->dataInfo['Mode']['value'] == 0) echo 'selected'; ?> ><?php echo $t_off[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="1" <?php if($autorunConf->dataInfo['Mode']['value'] == 1) echo 'selected'; ?> ><?php echo $t_home[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="2" <?php if($autorunConf->dataInfo['Mode']['value'] == 2) echo 'selected'; ?> ><?php echo $t_preset[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="3" <?php if($autorunConf->dataInfo['Mode']['value'] == 3) echo 'selected'; ?> ><?php echo $t_swing[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="4" <?php if($autorunConf->dataInfo['Mode']['value'] == 4) echo 'selected'; ?> ><?php echo $t_group[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="5" <?php if($autorunConf->dataInfo['Mode']['value'] == 5) echo 'selected'; ?> ><?php echo $t_tour[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="6" <?php if($autorunConf->dataInfo['Mode']['value'] == 6) echo 'selected'; ?> ><?php echo $t_trace[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="7" <?php if($autorunConf->dataInfo['Mode']['value'] == 7) echo 'selected'; ?> ><?php echo $t_autoPan[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="8" <?php if($autorunConf->dataInfo['Mode']['value'] == 8) echo 'selected'; ?> ><?php echo $t_schedule[$GLOBALS['LANGINDEX']]; ?></option>
					</select>
					&nbsp;
					<a class="btn_setup" href="javascript:OnClickApplyAutorun();" style="color:#fff; margin-left:-3px; margin-top:-3px"> <?php echo $t_set[$GLOBALS['LANGINDEX']]; ?> </a>
				</td>
			</tr>
			<tr class="AutoHomeArea">
				<td style="padding-left:20px"> <?php echo $t_time[$GLOBALS['LANGINDEX']]; ?> </td>
				<td>
					<select id="AutoRunHome-Time" class="selectbox_style_wid245">
						<option value="5"   <?php if($autorunConf->dataInfo['HomeTime']['value'] == 5) echo 'selected'; ?> >5 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="10"  <?php if($autorunConf->dataInfo['HomeTime']['value'] == 10) echo 'selected'; ?> >10 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="20"  <?php if($autorunConf->dataInfo['HomeTime']['value'] == 20) echo 'selected'; ?> >20 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="30"  <?php if($autorunConf->dataInfo['HomeTime']['value'] == 30) echo 'selected'; ?> >30 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="60"  <?php if($autorunConf->dataInfo['HomeTime']['value'] == 60) echo 'selected'; ?> >1 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="120" <?php if($autorunConf->dataInfo['HomeTime']['value'] == 120) echo 'selected'; ?> >2 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="180" <?php if($autorunConf->dataInfo['HomeTime']['value'] == 180) echo 'selected'; ?> >3 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="240" <?php if($autorunConf->dataInfo['HomeTime']['value'] == 240) echo 'selected'; ?> >4 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="300" <?php if($autorunConf->dataInfo['HomeTime']['value'] == 300) echo 'selected'; ?> >5 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
					</select>
				</td>
			</tr>
			<tr class="AutoPresetArea">
				<td style="padding-left:20px"> <?php echo $t_time[$GLOBALS['LANGINDEX']]; ?> </td>
				<td>
					<select id="AutoRunPreset-Time" class="selectbox_style_wid245">
						<option value="5"   <?php if($autorunConf->dataInfo['PresetTime']['value'] == 5) echo 'selected'; ?> >5 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="10"  <?php if($autorunConf->dataInfo['PresetTime']['value'] == 10) echo 'selected'; ?> >10 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="20"  <?php if($autorunConf->dataInfo['PresetTime']['value'] == 20) echo 'selected'; ?> >20 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="30"  <?php if($autorunConf->dataInfo['PresetTime']['value'] == 30) echo 'selected'; ?> >30 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="60"  <?php if($autorunConf->dataInfo['PresetTime']['value'] == 60) echo 'selected'; ?> >1 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="120" <?php if($autorunConf->dataInfo['PresetTime']['value'] == 120) echo 'selected'; ?> >2 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="180" <?php if($autorunConf->dataInfo['PresetTime']['value'] == 180) echo 'selected'; ?> >3 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="240" <?php if($autorunConf->dataInfo['PresetTime']['value'] == 240) echo 'selected'; ?> >4 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="300" <?php if($autorunConf->dataInfo['PresetTime']['value'] == 300) echo 'selected'; ?> >5 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
					</select>
				</td>
			</tr>
			<tr class="AutoPresetArea">
				<td style="padding-left:20px"> <?php echo $t_number[$GLOBALS['LANGINDEX']]; ?> </td>
				<td>
					<input type="text" id="AutoRunPreset-Number" class="text" style="width:50px;" onkeypress="IsNum(event); NoKorean(event)" onkeydown='NoKorean(event)' maxlength="3" value="<?php echo $autorunConf->dataInfo['PresetNumber']['value']; ?>" /> (1 ~ 255)
				</td>
			</tr>
			<tr class="AutoSwingArea">
				<td style="padding-left:20px"> <?php echo $t_swingMode[$GLOBALS['LANGINDEX']]; ?> </td>
				<td>
					<select id="AutoRunSwingMode" class="selectbox_style_wid245">
						<option value="0" <?php if($autorunConf->dataInfo['SwingMode']['value'] == 0) echo	"selected=\"selected\""; ?>><?php echo $t_pan[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="1" <?php if($autorunConf->dataInfo['SwingMode']['value'] == 1) echo	"selected=\"selected\""; ?>><?php echo $t_tilt[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="2" <?php if($autorunConf->dataInfo['SwingMode']['value'] == 2) echo	"selected=\"selected\""; ?>><?php echo $t_pantilt[$GLOBALS['LANGINDEX']]; ?></option>
					</select>
				</td>
			</tr>
			<tr class="AutoSwingArea">
				<td style="padding-left:20px"> <?php echo $t_time[$GLOBALS['LANGINDEX']]; ?> </td>
				<td>
					<select id="AutoRunSwingTime" class="selectbox_style_wid245">
						<option value="5"   <?php if($autorunConf->dataInfo['SwingTime']['value'] == 5) echo 'selected'; ?> >5 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="10"  <?php if($autorunConf->dataInfo['SwingTime']['value'] == 10) echo 'selected'; ?> >10 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="20"  <?php if($autorunConf->dataInfo['SwingTime']['value'] == 20) echo 'selected'; ?> >20 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="30"  <?php if($autorunConf->dataInfo['SwingTime']['value'] == 30) echo 'selected'; ?> >30 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="60"  <?php if($autorunConf->dataInfo['SwingTime']['value'] == 60) echo 'selected'; ?> >1 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="120" <?php if($autorunConf->dataInfo['SwingTime']['value'] == 120) echo 'selected'; ?> >2 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="180" <?php if($autorunConf->dataInfo['SwingTime']['value'] == 180) echo 'selected'; ?> >3 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="240" <?php if($autorunConf->dataInfo['SwingTime']['value'] == 240) echo 'selected'; ?> >4 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="300" <?php if($autorunConf->dataInfo['SwingTime']['value'] == 300) echo 'selected'; ?> >5 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
					</select>
				</td>
			</tr>
			<tr class="AutoGroupArea">
				<td style="padding-left:20px"> <?php echo $t_time[$GLOBALS['LANGINDEX']]; ?> </td>
				<td>
					<select id="AutoRunGroupTime" class="selectbox_style_wid245">
						<option value="5"   <?php if($autorunConf->dataInfo['GroupTime']['value'] == 5) echo 'selected'; ?> >5 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="10"  <?php if($autorunConf->dataInfo['GroupTime']['value'] == 10) echo 'selected'; ?> >10 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="20"  <?php if($autorunConf->dataInfo['GroupTime']['value'] == 20) echo 'selected'; ?> >20 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="30"  <?php if($autorunConf->dataInfo['GroupTime']['value'] == 30) echo 'selected'; ?> >30 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="60"  <?php if($autorunConf->dataInfo['GroupTime']['value'] == 60) echo 'selected'; ?> >1 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="120" <?php if($autorunConf->dataInfo['GroupTime']['value'] == 120) echo 'selected'; ?> >2 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="180" <?php if($autorunConf->dataInfo['GroupTime']['value'] == 180) echo 'selected'; ?> >3 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="240" <?php if($autorunConf->dataInfo['GroupTime']['value'] == 240) echo 'selected'; ?> >4 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="300" <?php if($autorunConf->dataInfo['GroupTime']['value'] == 300) echo 'selected'; ?> >5 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
					</select>
				</td>
			</tr>

			<tr class="AutoGroupArea">
				<td style="padding-left:20px"> <?php echo $t_number[$GLOBALS['LANGINDEX']]; ?> </td>
				<td>
					<input type="text" id="AutoRunGroupNo" class="text" style="width:50px;" onkeypress="IsNum(event); NoKorean(event)" onkeydown='NoKorean(event)' maxlength="1" value="<?php echo $autorunConf->dataInfo['GroupNumber']['value']; ?>"/> (1 ~ 6)
				</td>
			</tr>
			<tr class="AutoTourArea">
				<td style="padding-left:20px"> <?php echo $t_time[$GLOBALS['LANGINDEX']]; ?> </td>
				<td>
					<select id="AutoRunTourTime" class="selectbox_style_wid245">
						<option value="5" 	<?php if($autorunConf->dataInfo['TourTime']['value'] == 5) echo 'selected'; ?> >5 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="10"	<?php if($autorunConf->dataInfo['TourTime']['value'] == 10) echo 'selected'; ?> >10 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="20"	<?php if($autorunConf->dataInfo['TourTime']['value'] == 20) echo 'selected'; ?> >20 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="30"	<?php if($autorunConf->dataInfo['TourTime']['value'] == 30) echo 'selected'; ?> >30 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="60"	<?php if($autorunConf->dataInfo['TourTime']['value'] == 60) echo 'selected'; ?> >1 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="120"	<?php if($autorunConf->dataInfo['TourTime']['value'] == 120) echo 'selected'; ?> >2 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="180"	<?php if($autorunConf->dataInfo['TourTime']['value'] == 180) echo 'selected'; ?> >3 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="240"	<?php if($autorunConf->dataInfo['TourTime']['value'] == 240) echo 'selected'; ?> >4 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="300"	<?php if($autorunConf->dataInfo['TourTime']['value'] == 300) echo 'selected'; ?> >5 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
					</select>
				</td>
			</tr>
			<tr class="AutoTraceArea">
				<td style="padding-left:20px">
					<?php echo $t_time[$GLOBALS['LANGINDEX']]; ?>
				</td>
				<td>
					<select id="AutoRunTrace-Time" class="selectbox_style_wid245">
						<option value="5" 	<?php if($autorunConf->dataInfo['TraceTime']['value'] == 5) echo 'selected'; ?> >5 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="10"	<?php if($autorunConf->dataInfo['TraceTime']['value'] == 10) echo 'selected'; ?> >10 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="20"	<?php if($autorunConf->dataInfo['TraceTime']['value'] == 20) echo 'selected'; ?> >20 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="30"	<?php if($autorunConf->dataInfo['TraceTime']['value'] == 30) echo 'selected'; ?> >30 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="60"	<?php if($autorunConf->dataInfo['TraceTime']['value'] == 60) echo 'selected'; ?> >1 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="120"	<?php if($autorunConf->dataInfo['TraceTime']['value'] == 120) echo 'selected'; ?> >2 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="180"	<?php if($autorunConf->dataInfo['TraceTime']['value'] == 180) echo 'selected'; ?> >3 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="240"	<?php if($autorunConf->dataInfo['TraceTime']['value'] == 240) echo 'selected'; ?> >4 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="300"	<?php if($autorunConf->dataInfo['TraceTime']['value'] == 300) echo 'selected'; ?> >5 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
					</select>
				</td>
			</tr>
			<tr class="AutoTraceArea">
				<td style="padding-left:20px"> <?php echo $t_number[$GLOBALS['LANGINDEX']]; ?> </td>
				<td>
					<input type="text" id="AutoRunTrace-Number" class="text" style="width:50px;" onkeypress="IsNum(event); NoKorean(event)" onkeydown='NoKorean(event)' maxlength="1" value="<?php echo $autorunConf->dataInfo['TraceNumber']['value']; ?>"/> (1 ~ 4)
				</td>
			</tr>
			<tr class="AutoPanArea">
				<td style="padding-left:20px"> <?php echo $t_speed[$GLOBALS['LANGINDEX']]; ?> </td>
				<td>
					<input type="text" id="AutoPan-Speed" maxlength="2" class="text" onkeypress="IsNum(event); NoKorean(event)" onkeydown='NoKorean(event)' style="width: 50px;" value="<?php echo $autorunConf->dataInfo['AutoPanSpeed']['value']; ?>"/> (1 ~ 50)
				</td>
			</tr>
			<tr class="AutoPanArea">
				<td style="padding-left:20px"> <?php echo $t_tiltAngle[$GLOBALS['LANGINDEX']]; ?> </td>
				<td>
					<input type="text" id="AutoPan-Tiltangle" maxlength="2" class="text" onkeypress="IsNum(event); NoKorean(event)" onkeydown='NoKorean(event)' style="width: 50px;" value="<?php echo $autorunConf->dataInfo['AutoPanTiltangle']['value']; ?>"/> (0 ~ 85)
				</td>
			</tr>
			<tr class="AutoPanArea">
				<td style="padding-left:20px"> <?php echo $t_time[$GLOBALS['LANGINDEX']]; ?> 	</td>
				<td>
					<select id="AutoPan-Time" class="selectbox_style_wid245">
						<option value="5"   <?php if($autorunConf->dataInfo['AutoPanTime']['value'] == 5) echo 'selected'; ?> >5 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="10"  <?php if($autorunConf->dataInfo['AutoPanTime']['value'] == 10) echo 'selected'; ?> >10 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="20"  <?php if($autorunConf->dataInfo['AutoPanTime']['value'] == 20) echo 'selected'; ?> >20 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="30"  <?php if($autorunConf->dataInfo['AutoPanTime']['value'] == 30) echo 'selected'; ?> >30 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="60"  <?php if($autorunConf->dataInfo['AutoPanTime']['value'] == 60) echo 'selected'; ?> >1 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="120" <?php if($autorunConf->dataInfo['AutoPanTime']['value'] == 120) echo 'selected'; ?> >2 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="180" <?php if($autorunConf->dataInfo['AutoPanTime']['value'] == 180) echo 'selected'; ?> >3 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="240" <?php if($autorunConf->dataInfo['AutoPanTime']['value'] == 240) echo 'selected'; ?> >4 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="300" <?php if($autorunConf->dataInfo['AutoPanTime']['value'] == 300) echo 'selected'; ?> >5 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
					</select>
				</td>
			</tr>
			<tr class="AutoScheduleArea">
				<td style="padding-left:20px"> <?php echo $t_time[$GLOBALS['LANGINDEX']]; ?> 	</td>
				<td>
					<select id="Schedule-Time" class="selectbox_style_wid245">
						<option value="5"   <?php if($autorunConf->dataInfo['ScheduleTime']['value'] == 5) echo 'selected'; ?> >5 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="10"  <?php if($autorunConf->dataInfo['ScheduleTime']['value'] == 10) echo 'selected'; ?> >10 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="20"  <?php if($autorunConf->dataInfo['ScheduleTime']['value'] == 20) echo 'selected'; ?> >20 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="30"  <?php if($autorunConf->dataInfo['ScheduleTime']['value'] == 30) echo 'selected'; ?> >30 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="60"  <?php if($autorunConf->dataInfo['ScheduleTime']['value'] == 60) echo 'selected'; ?> >1 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="120" <?php if($autorunConf->dataInfo['ScheduleTime']['value'] == 120) echo 'selected'; ?> >2 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="180" <?php if($autorunConf->dataInfo['ScheduleTime']['value'] == 180) echo 'selected'; ?> >3 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="240" <?php if($autorunConf->dataInfo['ScheduleTime']['value'] == 240) echo 'selected'; ?> >4 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="300" <?php if($autorunConf->dataInfo['ScheduleTime']['value'] == 300) echo 'selected'; ?> >5 <?php echo $t_min[$GLOBALS['LANGINDEX']]; ?></option>
					</select>
				</td>
			</tr>
		</tbody>
	</table>
	<div class="AutoScheduleArea" style="margin-top:10px; height:260px">
		<div style="position:absolute; top:460px; width:620px; ">
		
			<table>
				<colgroup>
					<col style="width:150px;"/>
					<col style="width:150px;"/>
					<col style="width:150px;"/>
					<col />
				</colgroup>
				<tbody>
					<tr>
					<td> <a class="setHome scheduleColorInfo"></a><span style="color:#fff;font-size:11px"><?php echo $t_home[$GLOBALS['LANGINDEX']]; ?></span> </td>
					<td> <a class="setPreset scheduleColorInfo"></a><span style="color:#fff;font-size:11px"><?php echo $t_preset[$GLOBALS['LANGINDEX']]; ?></span> </td>
					<td> <a class="setSwing scheduleColorInfo"></a><span style="color:#fff;font-size:11px"><?php echo $t_swing[$GLOBALS['LANGINDEX']]; ?></span> </td>
					<td> <a class="setGroup scheduleColorInfo"></a><span style="color:#fff;font-size:11px"><?php echo $t_group[$GLOBALS['LANGINDEX']]; ?></span><br/> </td>
					</tr>
					<tr>
					<td> <a class="setTour scheduleColorInfo"></a><span style="color:#fff;font-size:11px"><?php echo $t_tour[$GLOBALS['LANGINDEX']]; ?></span> </td>
					<td> <a class="setTrace scheduleColorInfo"></a><span style="color:#fff;font-size:11px"><?php echo $t_trace[$GLOBALS['LANGINDEX']]; ?></span> </td>
					<td colspan="2"> <a class="setAutopan scheduleColorInfo"></a><span style="color:#fff;font-size:11px"><?php echo $t_autoPan[$GLOBALS['LANGINDEX']]; ?></span>  </td>
					</tr>
				</tbody>
			</table>
		</div>
			<a class="btn_type01 mgb10" style="float:right; position:<?php if (GetBrowserName()=='Mozilla Firefox') {echo 'relative';} ?>; top:<?php if (GetBrowserName()=='Mozilla Firefox') {echo '-32';} ?>px;" href="javascript:AutoRunScheduleClear();" id="autorun_clear_btn"><?php echo $t_clear[$GLOBALS['LANGINDEX']]; ?></a>

		<div id="autorun_timeschedule_cover" class="timeschedule_cover AutoScheduleArea">
			<table id="autorun_timeschedule_table" border="0" width="100%" cellspacing="0" cellpadding="0" class="eventTable AutoScheduleArea" >
				<thead><tr><td class="dayHead">&nbsp;</td><td class="dayHead">00</td><td class="dayHead">01</td><td class="dayHead">02</td><td class="dayHead">03</td><td class="dayHead">04</td><td class="dayHead">05</td><td class="dayHead">06</td><td class="dayHead">07</td><td class="dayHead">08</td><td class="dayHead">09</td><td class="dayHead">10</td><td class="dayHead">11</td><td class="dayHead">12</td><td class="dayHead">13</td><td class="dayHead">14</td><td class="dayHead">15</td><td class="dayHead">16</td><td class="dayHead">17</td><td class="dayHead">18</td><td class="dayHead">19</td><td class="dayHead">20</td><td class="dayHead">21</td><td class="dayHead">22</td><td class="dayHead">23</td></tr></thead>
				<tbody>
				<tr class="weekHead"><td class="dayHead"><?php echo $t_sun[$GLOBALS["LANGINDEX"]]; ?></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
				<tr class="weekHead"><td class="dayHead"><?php echo $t_mon[$GLOBALS["LANGINDEX"]]; ?></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
				<tr class="weekHead"><td class="dayHead"><?php echo $t_tue[$GLOBALS["LANGINDEX"]]; ?></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
				<tr class="weekHead"><td class="dayHead"><?php echo $t_wed[$GLOBALS["LANGINDEX"]]; ?></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
				<tr class="weekHead"><td class="dayHead"><?php echo $t_thu[$GLOBALS["LANGINDEX"]]; ?></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
				<tr class="weekHead"><td class="dayHead"><?php echo $t_fri[$GLOBALS["LANGINDEX"]]; ?></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
				<tr class="weekHead"><td class="dayHead"><?php echo $t_sat[$GLOBALS["LANGINDEX"]]; ?></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
				</tbody>
			</table>
			<script type="text/javascript" language="javascript">

var daysList = ["<?php echo $t_sun[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $t_mon[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $t_tue[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $t_wed[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $t_thu[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $t_fri[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $t_sat[$GLOBALS['LANGINDEX']]; ?>"];
var modeNameList = ["", "Home","Preset","Swing","Group","Tour","Trace","Autopan"];
var modeLanguageList = ["", "<?php echo $t_home[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $t_preset[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $t_swing[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $t_group[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $t_tour[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $t_trace[$GLOBALS['LANGINDEX']]; ?>",  "<?php echo $t_autoPan[$GLOBALS['LANGINDEX']]; ?>"];
var swingModeList = ["<?php echo $t_pan[$GLOBALS['LANGINDEX']]; ?>","<?php echo $t_tilt[$GLOBALS['LANGINDEX']]; ?>","<?php echo $t_pantilt[$GLOBALS['LANGINDEX']]; ?>"];
var tooltipInfo = {	"Mode":"<?php echo $t_mode[$GLOBALS['LANGINDEX']]; ?>",
							"PresetNumber":"<?php echo $t_number[$GLOBALS['LANGINDEX']]; ?>",
							"SwingMode":"<?php echo $t_swingMode[$GLOBALS['LANGINDEX']]; ?>",
							"GroupNumber":"<?php echo $t_number[$GLOBALS['LANGINDEX']]; ?>",
							"TraceNumber":"<?php echo $t_number[$GLOBALS['LANGINDEX']]; ?>",
							"AutoPanSpeed":"<?php echo $t_speed[$GLOBALS['LANGINDEX']]; ?>",
							"AutoPanTiltangle":"<?php echo $t_tiltAngle[$GLOBALS['LANGINDEX']]; ?>"};
var buttonLang = ["<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $t_cancel[$GLOBALS['LANGINDEX']]; ?>"];

							
var currClassName = '';
///var currMode = 0;
//var currDetail = new Array();    //[0] : presetNo,  [1] : swingMode, [2] : groupNo, [3] : traceNo, [4] : apSpd, [5] : apTiltAngle
var detailSchedObjList = {};

var startScheduleIndex = new Array();
var autorunScheduleXML = "";
autorunScheduleXML += "<AutorunSchedule>\r\n";

var isDetectFirst = true;
<?php
	for ($i=0; $i<7; $i++) {
?>
		autorunScheduleXML += "<Day"+<?php echo $i;?>+">\r\n";
	<?php
		for($j=0; $j<24; $j++) {
	?>
			autorunScheduleXML += "<H"+<?php echo $j; ?>+">\r\n";
			autorunScheduleXML += "<Enable>"+<?php echo $autorunConf->autorunSchedule[$i]->autorunDetailSchdule[$j]->dataInfo['Enable']['value']; ?>+"</Enable>";
			autorunScheduleXML += "<Mode>"+<?php echo $autorunConf->autorunSchedule[$i]->autorunDetailSchdule[$j]->autorunDetail->dataInfo['Mode']['value']; ?>+"</Mode>";
			autorunScheduleXML += "<PresetNo>"+<?php echo $autorunConf->autorunSchedule[$i]->autorunDetailSchdule[$j]->autorunDetail->dataInfo['PresetNumber']['value']; ?>+"</PresetNo>";
			autorunScheduleXML += "<SwingMode>"+<?php echo $autorunConf->autorunSchedule[$i]->autorunDetailSchdule[$j]->autorunDetail->dataInfo['SwingMode']['value']; ?>+"</SwingMode>";
			autorunScheduleXML += "<GroupNo>"+<?php echo $autorunConf->autorunSchedule[$i]->autorunDetailSchdule[$j]->autorunDetail->dataInfo['GroupNumber']['value']; ?>+"</GroupNo>";
			autorunScheduleXML += "<TraceNo>"+<?php echo $autorunConf->autorunSchedule[$i]->autorunDetailSchdule[$j]->autorunDetail->dataInfo['TraceNumber']['value']; ?>+"</TraceNo>";
			autorunScheduleXML += "<AutoPanSpeed>"+<?php echo $autorunConf->autorunSchedule[$i]->autorunDetailSchdule[$j]->autorunDetail->dataInfo['AutoPanSpeed']['value']; ?>+"</AutoPanSpeed>";
			autorunScheduleXML += "<AutoPanTiltangle>"+<?php echo $autorunConf->autorunSchedule[$i]->autorunDetailSchdule[$j]->autorunDetail->dataInfo['AutoPanTiltangle']['value']; ?>+"</AutoPanTiltangle>";
			autorunScheduleXML += "</H"+<?php echo $j;?>+">\r\n";
			if(isDetectFirst){
				<?php if($autorunConf->autorunSchedule[$i]->autorunDetailSchdule[$j]->dataInfo['Enable']['value'] == 1) {?>
				startScheduleIndex[0] = <?php echo $i; ?>;
				startScheduleIndex[1] = <?php echo $j; ?>;
				isDetectFirst = false;
				<?php } ?>
			}
	<?php
		}
	?>
		autorunScheduleXML += "</Day"+<?php echo $i;?>+">\r\n";
<?php
	}
?>
	autorunScheduleXML += "</AutorunSchedule>\r\n";
	//console.log(startScheduleIndex[0],startScheduleIndex[1]);
	SetAutoRunScheduleDataToTable(startScheduleIndex, autorunScheduleXML);
</script>
			<div id="tmMinute" style="display:none;width:350px;" >
				<table class="data_write mgt10 mgl-20 pdl15" style="width:100%">
					<colgroup>
						<col style="width:100px;"/>
						<col />
					</colgroup>
					<tbody>
						<tr>
							<th> <?php echo $t_mode[$GLOBALS["LANGINDEX"]]; ?> </th>
							<td>
								<select id="ScheduleAutoRunMode" class="selectbox_style_wid250" onchange="OnChangeAutoRunMode('Schedule')" >
									<option value="1" <?php if($autorunConf->dataInfo['Mode']['value'] == 1) echo 'selected'; ?> > <?php echo $t_home[$GLOBALS['LANGINDEX']]; ?></option>
									<option value="2" <?php if($autorunConf->dataInfo['Mode']['value'] == 2) echo 'selected'; ?> > <?php echo $t_preset[$GLOBALS['LANGINDEX']]; ?></option>
									<option value="3" <?php if($autorunConf->dataInfo['Mode']['value'] == 3) echo 'selected'; ?> > <?php echo $t_swing[$GLOBALS['LANGINDEX']]; ?></option>
									<option value="4" <?php if($autorunConf->dataInfo['Mode']['value'] == 4) echo 'selected'; ?> > <?php echo $t_group[$GLOBALS['LANGINDEX']]; ?></option>
									<option value="5" <?php if($autorunConf->dataInfo['Mode']['value'] == 5) echo 'selected'; ?> > <?php echo $t_tour[$GLOBALS['LANGINDEX']]; ?></option>
									<option value="6" <?php if($autorunConf->dataInfo['Mode']['value'] == 6) echo 'selected'; ?> > <?php echo $t_trace[$GLOBALS['LANGINDEX']]; ?></option>
									<option value="7" <?php if($autorunConf->dataInfo['Mode']['value'] == 7) echo 'selected'; ?> > <?php echo $t_autoPan[$GLOBALS['LANGINDEX']]; ?></option>
								</select>
							</td>
						</tr>
						<tr class="ScheduleAutoPresetArea">
							<th> <?php echo $t_number[$GLOBALS['LANGINDEX']]; ?> </th>
							<td>
								<input type="text" id="AutoRunPresetNumber" class="text" style="width:50px;" onkeypress="IsNum(event); NoKorean(event)" onkeydown='NoKorean(event)' maxlength="3" value="<?php echo $autorunConf->dataInfo['PresetNumber']['value']; ?>" /> (1 ~ 255)
							</td>
						</tr>
						<tr class="ScheduleAutoSwingArea">
							<th> <?php echo $t_swingMode[$GLOBALS['LANGINDEX']]; ?> </th>
							<td>
								<select id="ScheduleAutoRunSwingMode" class="selectbox_style_wid260">
									<option value="0" <?php if($autorunConf->dataInfo['SwingMode']['value'] == 0) echo	"selected=\"selected\""; ?>><?php echo $t_pan[$GLOBALS['LANGINDEX']]; ?></option>
									<option value="1" <?php if($autorunConf->dataInfo['SwingMode']['value'] == 1) echo	"selected=\"selected\""; ?>><?php echo $t_tilt[$GLOBALS['LANGINDEX']]; ?></option>
									<option value="2" <?php if($autorunConf->dataInfo['SwingMode']['value'] == 2) echo	"selected=\"selected\""; ?>><?php echo $t_pantilt[$GLOBALS['LANGINDEX']]; ?></option>
								</select>
							</td>
						</tr>
						<tr class="ScheduleAutoGroupArea">
							<th> <?php echo $t_number[$GLOBALS['LANGINDEX']]; ?> </th>
							<td>
								<input type="text" id="ScheduleAutoRunGroupNo" class="text" style="width:50px;" onkeypress="IsNum(event); NoKorean(event)" onkeydown='NoKorean(event)' maxlength="1" value="<?php echo $autorunConf->dataInfo['GroupNumber']['value']; ?>"/> (1 ~ 6)
							</td>
						</tr>
						<tr class="ScheduleAutoTraceArea">
							<th> <?php echo $t_number[$GLOBALS['LANGINDEX']]; ?> </th>
							<td>
								<input type="text" id="ScheduleAutoRunTraceNumber" class="text" style="width:50px;" onkeypress="IsNum(event); NoKorean(event)" onkeydown='NoKorean(event)' maxlength="1" value="<?php echo $autorunConf->dataInfo['TraceNumber']['value']; ?>"/> (1 ~ 4)
							</td>
						</tr>
						<tr class="ScheduleAutoPanArea">
							<th> <?php echo $t_speed[$GLOBALS['LANGINDEX']]; ?> </th>
							<td>
								<input type="text" id="ScheduleAutoPanSpeed" maxlength="2" class="text" onkeypress="IsNum(event); NoKorean(event)" onkeydown='NoKorean(event)' style="width: 50px;" value="<?php echo $autorunConf->dataInfo['AutoPanSpeed']['value']; ?>"/> (1 ~ 50)
							</td>
						</tr>
						<tr class="ScheduleAutoPanArea">
							<th> <?php echo $t_tiltAngle[$GLOBALS['LANGINDEX']]; ?> </th>
							<td>
								<input type="text" id="ScheduleAutoPanTiltangle" maxlength="2" class="text" onkeypress="IsNum(event); NoKorean(event)" onkeydown='NoKorean(event)' style="width: 50px;" value="<?php echo $autorunConf->dataInfo['AutoPanTiltangle']['value']; ?>"/> (0 ~ 85)
							</td>
						</tr>
						<tr>
							<th><?php echo $t_from[$GLOBALS['LANGINDEX']]; ?> </th>
							<td>
								<table style="margin-left:-9px">
									<tr>
										<td><select id="from_days" class="selectbox_style" style="width:70px"></select></td>
										<td> - </td>
										<td><select id="from_hour" class="selectbox_style" style="width:70px"></select></td>
									</tr>
								</table>
							</td>
						</tr>
						<tr>
							<th><?php echo $t_to[$GLOBALS['LANGINDEX']]; ?> </th>
							<td>
								<table style="margin-left:-9px">
									<tr>
										<td><select id="to_days" class="selectbox_style" style="width:70px"></select></td>
										<td> - </td>
										<td><select id="to_hour" class="selectbox_style" style="width:70px"></select></td>
									</tr>
								</table>
							</td>
						</tr>
						
					</tbody>
				</table>
			</div>
		</div>
	</div>
</div>

<script>
	jQuery("#tmMinute").dialog({
		autoOpen: false,
		modal: true,	
		title: "<?php echo $t_setup[$GLOBALS['LANGINDEX']]; ?>"
	});	
</script>
											
<style>
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
.setHome {
	background:#54c0ff !important;
}
.setPreset {
	background:#ffa52f !important;
}
.setSwing {
	background:#5eec5f !important;
}
.setGroup {
	background:#923ee6 !important;
}
.setTour {
	background:#ef5ca8 !important;
}
.setTrace {
	background:#ffff77 !important;
}
.setAutopan {
	background:#3464ff !important;
}

.scheduleColorInfo{
	display:inline-block;
	width:18px;
	height:18px;
	vertical-align:middle;
	font-weight:bold;
	margin-right:3px;
}
.btn_right {
	 border-top: 1px solid #737C8F;
	 float: left;
	 margin-top: 45px;
	 padding-top: 10px;
	 text-align: right;
	 width: 100%;
}
.ui-dialog-titlebar-close .ui-button-text{
display:none;
}
.ui-dialog-titlebar-close{
float:right;
}
#poly-dialog p{
	margin:4px;
}
.scheduleTable .ui-dialog-title{
float:left;
}

	#polyDraw div{
	}
	#polyDraw div div{
			cursor: pointer;
			opacity: 0.4;
	}
	.dot {
	background-color: green;
	position:absolute;
	height:3px;
	width:3px;
	line-height:3px;
	float:left;
	padding:0;
	margin:0;
	overflow:hidden;
	z-index:100;
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
		
.ui-dialog .ui-dialog-titlebar-close{
	background: none;
	border: none;
}
.ui-dialog .ui-widget-content {background: #EFF1F3;border: none;margin-left: 20px;}
.ui-dialog .ui-dialog-buttonpane .ui-dialog-buttonset { text-align:center}
.ui-dialog .ui-dialog-buttonset button{ background: #EFF1F3; margin: 0 10px;}
.ui-dialog .ui-dialog-buttonpane{ border: none; padding: 10px 0}
.ui-dialog .ui-resizable-handle{ display: none !important;}
.ui-dialog .ui-widget-content p{ display:block;clear: both;}
.ui-dialog .ui-widget-content input,.ui-dialog .ui-widget-content label{float:left;}
.ui-button.ui-state-default { color:#000;}

.ui-dialog.scheduleTable {
	left: 490px !important;
	width: 400px !important;
}
.ui-dialog table.data_write tbody th {
	padding:5px 0;
	padding-left:9px;
	text-align:left;
	color:black;
}
.ui-dialog table.data_write tbody td {
	padding:5px 0;
	padding-left:9px;
	font-weight:normal;
	color:black;
}

.ui-dialog input.text {
	background: none repeat scroll 0 0 #FFFFFF;
	margin-left:-1px;
	margin-right:10px;
}

.ui-dialog select {
	background: none repeat scroll 0 0 #FFFFFF;
	width:251px;
}

.ui-tooltip-autorun_timeschedule_table {width: 150px; word-break:break-all;}

</style> 	

