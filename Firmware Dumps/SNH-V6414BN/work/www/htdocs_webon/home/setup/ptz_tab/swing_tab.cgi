<script type="text/javascript" language="javascript">

var SWINGENABLE		= new Array();
var SWINGMODE			= new Array();
var SWINGFIRSTPRESET = new Array();
var SWINGSECPRESET	= new Array();
var SWINGSPEED 		= new Array();
var SWINGDWT			= new Array();

var PRESETENABLE		= new Array();
var PRESETNAME			= new Array();

<?php
	for($index=0; $index<MAX_PTZ_SWING; ++$index) {
?>
		SWINGENABLE[<?php echo $index; ?>]		= <?php echo $swingsConf->swing[$index]['Enabled']['value']; ?>;
		SWINGMODE[<?php echo $index; ?>] 		= <?php echo $swingsConf->swing[$index]['Mode']['value']; ?>;
		SWINGFIRSTPRESET[<?php echo $index; ?>]= <?php echo $swingsConf->swing[$index]['FirstPreset']['value']; ?>;
		SWINGSECPRESET[<?php echo $index; ?>]	= <?php echo $swingsConf->swing[$index]['SecondPreset']['value']; ?>;
		SWINGSPEED[<?php echo $index; ?>]		= <?php echo $swingsConf->swing[$index]['Speed']['value']; ?>;
		SWINGDWT[<?php echo $index; ?>]			= <?php echo $swingsConf->swing[$index]['DWT']['value']; ?>;
<?php
	}
?>

<?php
	for($index=1; $index<=MAX_PTZ_PRESET255; ++$index) {
		if ($presetConf->preset[$index-1]->dataInfo['Enabled']['value'] == 0) continue;
?>
		PRESETNAME[<?php echo $index; ?>] = "<?php echo trim($presetConf->preset[$index-1]->dataInfo['Name']['value']); ?>";
<?php
	}
?>

function DrawSwingList() {
	var firstPresetList;
	var secondPresetList
	var swingMode = $("#SwingMode").val();

		if(swingMode == 0 && SWINGFIRSTPRESET[0] != 0 && SWINGSECPRESET[0] != 0) {
			firstPresetList = "<option value="+SWINGFIRSTPRESET[0]+" selected=\"selected\">"+SWINGFIRSTPRESET[0]+":"+PRESETNAME[SWINGFIRSTPRESET[0]];
			secondPresetList = "<option value="+SWINGSECPRESET[0]+" selected=\"selected\">"+SWINGSECPRESET[0]+":"+PRESETNAME[SWINGSECPRESET[0]];
		} else if(swingMode == 1 && SWINGFIRSTPRESET[1] != 0 && SWINGSECPRESET[1] != 0) {
			firstPresetList = "<option value="+SWINGFIRSTPRESET[1]+" selected=\"selected\">"+SWINGFIRSTPRESET[1]+":"+PRESETNAME[SWINGFIRSTPRESET[1]];		
			secondPresetList = "<option value="+SWINGSECPRESET[1]+" selected=\"selected\">"+SWINGSECPRESET[1]+":"+PRESETNAME[SWINGSECPRESET[1]];
		} else if(swingMode == 2 && SWINGFIRSTPRESET[2] != 0 && SWINGSECPRESET[2] != 0) {
			firstPresetList = "<option value="+SWINGFIRSTPRESET[2]+" selected=\"selected\">"+SWINGFIRSTPRESET[2]+":"+PRESETNAME[SWINGFIRSTPRESET[2]];
			secondPresetList = "<option value="+SWINGSECPRESET[2]+" selected=\"selected\">"+SWINGSECPRESET[2]+":"+PRESETNAME[SWINGSECPRESET[2]];
		} else {
			firstPresetList = "<option value=0><?php echo $t_none[$GLOBALS["LANGINDEX"]]; ?></option>";		
			secondPresetList = "<option value=0><?php echo $t_none[$GLOBALS["LANGINDEX"]]; ?></option>";		
		}

	$("#SwingFirstPreset").append(firstPresetList);	
	$("#SwingSecondPreset").append(secondPresetList);	
}

function OnFocusSwingPresetList(id) {
	var firstPresetList="";	
	var select = document.getElementById(id);
	var option_value = select.options[select.selectedIndex].value;
	
	document.getElementById(id).innerHTML = "";
	firstPresetList = "<option value=0><?php echo $t_none[$GLOBALS["LANGINDEX"]]; ?></option>"
	
	<?php
		for($index=1; $index<=MAX_PTZ_PRESET255; ++$index) {
			if ($presetConf->preset[$index-1]->dataInfo['Enabled']['value'] == 0) continue;
	?>
			firstPresetList += '<option value="<?php echo $index; ?>"><?php echo $index.':'.trim($presetConf->preset[$index-1]->dataInfo['Name']['value']); ?></option>';
	<?php
		}
	?>	
	$("#" + id).append(firstPresetList);		
	$("#" + id + " option[value = "+option_value+"]").attr("selected", true);
}

function OnClickSwing(actionCmd)
{
	if (actionCmd == "Set") {
		if (CheckValueRange($("#SwingFirstPreset").val(), 1, MAX_PRESET_CNT, "<?php echo $msg_selValidPresetNumber[$GLOBALS['LANGINDEX']]; ?>")) return;
		if (CheckValueRange($("#SwingSecondPreset").val(), 1, MAX_PRESET_CNT, "<?php echo $msg_selValidPresetNumber[$GLOBALS['LANGINDEX']]; ?>")) return;
		if (CheckValueRange($("#SwingSpeed").val(), 1, 64, "<?php echo EnterNumber(1,64); ?>")) return;	
		if (CheckValueRange($("#SwingDWT").val(), 1, 128, "<?php echo EnterNumber(1,128); ?>")) return;	
		if(!TypeCheck($('#SwingSpeed').val(), NUM+ALPHA)) {
			alert("<?php echo EnterNumber(1,64); ?>");
			return;
		}
		if(!TypeCheck($('#SwingDWT').val(), NUM+ALPHA)) {
			alert("<?php echo EnterNumber(1,128); ?>");
			return;
		}	
		if($("#SwingFirstPreset").val() == $("#SwingSecondPreset").val()) {
			alert("<?php echo $msg_selValidPresetNumber[$GLOBALS['LANGINDEX']]; ?>");
			return;
		}
	}

	var msg = "";
	var applyMsg = '';
	var cmdMsg = '';
	msg += "<"+actionCmd+"PTZSwing>";
	if (actionCmd == "Start") {
		msg += "<Index>"+$("#SwingMode").val()+"</Index>";
		cmdMsg = 'NO_REFRESH';
	}
	else if (actionCmd == 'Set') {		
		msg += "<Index>"+$("#SwingMode").val()+"</Index>";
		msg += "<Enabled>1</Enabled>";
		msg += "<Mode>"+$("#SwingMode").val()+"</Mode>";
		msg += "<FirstPreset>"+$("#SwingFirstPreset").val()+"</FirstPreset>";
		msg += "<SecondPreset>"+$("#SwingSecondPreset").val()+"</SecondPreset>";
		msg += "<Speed>"+$("#SwingSpeed").val()+"</Speed>";
		msg += "<DWT>"+$("#SwingDWT").val()+"</DWT>";
		applyMsg = "<?php echo $t_set[$GLOBALS['LANGINDEX']]; ?>";
	}
	msg += "</"+actionCmd+"PTZSwing>";
	
	SetPTZCookie('Swing');
	RequestAjaxMsg(msg, applyMsg, ajaxReqUrl, cmdMsg);
}

function RedrawSwingArea()
{
	var SwingMode = $("#SwingMode").val();

	DrawSwingList();

	if ($("#SwingFirstPreset").val() == null) {	
		$("#SwingFirstPreset").val(0);		
	}
	else {		
		$("#SwingFirstPreset").val(SWINGFIRSTPRESET[SwingMode]); 
	}
	
	if ($("#SwingSecondPreset").val() == null) {	
		$("#SwingSecondPreset").val(0);
	}
	else {
		$("#SwingSecondPreset").val(SWINGSECPRESET[SwingMode]);
	}
	
	$("#SwingSpeed").val(SWINGSPEED[SwingMode]);
	$("#SwingDWT").val(SWINGDWT[SwingMode]);
	$("#SwingFirstPreset").trigger('change');
	$("#SwingSecondPreset").trigger('change');
}

</script>

<div id="tabs-swing">

	<table class="data_write mgt10 mgl-20 pdl15">
		<colgroup>
			<col style="width:180px;"/>
			<col />
		</colgroup>
		<tbody>
			<tr>
				<th> <?php echo $t_mode[$GLOBALS["LANGINDEX"]]; ?> </th>
				<td>
    				<select id="SwingMode" class="selectbox_style_wid260" onchange="RedrawSwingArea()">
						<option value="0" <?php if ($swingsConf->swing[0]['Enabled']['value'] == 1) echo "selected=\"selected\""; ?>><?php echo $t_pan[$GLOBALS['LANGINDEX']]; ?> </option>
   					<option value="1" <?php if ($swingsConf->swing[1]['Enabled']['value'] == 1) echo "selected=\"selected\""; ?>><?php echo $t_tilt[$GLOBALS['LANGINDEX']]; ?> </option>
						<option value="2" <?php if ($swingsConf->swing[2]['Enabled']['value'] == 1) echo "selected=\"selected\""; ?>><?php echo $t_pantilt[$GLOBALS['LANGINDEX']]; ?> </option>
    				</select>
				</td>
			</tr>			
			<tr>
				<th> <?php echo $t_speed[$GLOBALS["LANGINDEX"]]; ?> </th>
				<td>
					<input id = "SwingSpeed" type="text" class="text" maxlength="2" style="width: 50px;" onkeypress="IsNum(event); NoKorean(event)" onkeydown='NoKorean(event)' value="<?php echo $swingConf->dataInfo['Speed']['value']; ?>" /> (1 ~ 64)
				</td>
			</tr>
			<tr>
				<th> <?php echo $t_dwt[$GLOBALS['LANGINDEX']]; ?> </th>
				<td>
					<input id = "SwingDWT" type="text" class="text" maxlength="3" style="width: 50px;"	onkeypress="IsNum(event); NoKorean(event)" onkeydown='NoKorean(event)' value="<?php echo $swingConf->dataInfo['DWT']['value']; ?>" /> (1 ~ 128 <?php echo $t_sec[$GLOBALS['LANGINDEX']]; ?>)
				</td>
			</tr>
		</tbody>
	</table> 

	<table class="data_write mgl-20 pdl15 mgt20" style="width:645px;">
		<colgroup>
			<col style="width:180px;"/>
			<col />
		</colgroup>
		<tbody>
			<tr>
				<th style="vertical-align:top"> <?php echo $t_presetList[$GLOBALS['LANGINDEX']]; ?> </th>
				<td>
					<table class="data_table" border="0" style="width:429px;overflow:auto;">
						<colgroup>
							<col style="width:214px;">
							<col style="width:215px;">
						</colgroup>
						<thead>
							<tr>
								<th></th>
								<th style="text-align:center;"><?php echo $t_presetNo[$GLOBALS['LANGINDEX']]; ?></th>					
							</tr>
						</thead>
						<tbody>
							<tr>
								<td style="text-align:left;padding-left:10px"><b><?php echo $t_firstPreset[$GLOBALS["LANGINDEX"]]; ?></b></td>
								<td>
									<select id="SwingFirstPreset" class="selectbox_style" style="width:150px;float:inherit;background-color:#b4b9c5;" onchange="OnFocusSwingPresetList('SwingFirstPreset');">
										<option value=0><?php echo $t_none[$GLOBALS["LANGINDEX"]]; ?></option>									
									</select>
								</td> 						
							</tr>
							
							<tr>
								<td style="text-align:left;padding-left:10px"><b><?php echo $t_secondPresets[$GLOBALS["LANGINDEX"]]; ?></b></td>
								<td>
									<select id="SwingSecondPreset" class="selectbox_style" style="width:150px;float:inherit;background-color:#b4b9c5;" onchange="OnFocusSwingPresetList('SwingSecondPreset');">
										<option value=0><?php echo $t_none[$GLOBALS["LANGINDEX"]]; ?></option>
									</select>
								</td> 						
							</tr>
						</tbody>
					</table>
				</td>
			</tr>
			<tr>
				<td></td>
				<td>
					<a class="btn_setup" href="javascript:OnClickSwing('Start');" style="color:#fff"> <?php echo $t_start[$GLOBALS['LANGINDEX']]; ?> </a>					
					<a class="btn_setup" href="javascript:SISOPlugin.ptzControl.onClickPtzStop('sequence');" style="color:#fff"> <?php echo $t_stop[$GLOBALS['LANGINDEX']]; ?> </a>				
					<a class="btn_setup" href="javascript:OnClickSwing('Set');" style="color:#fff; margin-left:152px;"> <?php echo $t_set[$GLOBALS['LANGINDEX']]; ?> </a>	
				</td>		
			</tr>
		</tbody>
	</table>
</div>
