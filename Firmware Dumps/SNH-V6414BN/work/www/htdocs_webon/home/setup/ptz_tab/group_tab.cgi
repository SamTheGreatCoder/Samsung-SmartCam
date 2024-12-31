<script type="text/javascript" language="javascript">
var oldSelNo;
var groupSetStatus = new Array(7);
var groupNo				= new Array();
var GROUPPRESTNUM 	= new Array();
var GROUPSPEED			= new Array();
var GROUPDWELLTIME	= new Array();


for(var index=0; index<=6; ++index) {
    groupSetStatus[index] = false;
}

function OnClickGroup(actionCmd)
{
	var msg = "";
	var name = '';
	var applyMsg = '';
	var cmdMsg = '';
	var grpIndex = ($("#GroupNo").val()-1)* 128 ;
	var groupNo = parseInt($("#GroupNo").val());
	var presetListCnt = $("#GroupList_"+groupNo+" tbody tr").size();
	var grouppresetList = $('#GroupPresetList option').size();
	
	if(actionCmd == 'Start') {
		if (groupSetStatus[groupNo] == true) {
			alert("<?php echo $msg_presetListChange[$GLOBALS['LANGINDEX']]; ?>");
			return;
		}
		cmdMsg = 'NO_REFRESH';
	}
	else {
		if ($("#GroupPresetList").val() == 0) {
			alert("<?php echo $msg_checkGroupSettingValue[$GLOBALS['LANGINDEX']]; ?>");
			return;
		}
		
		if (presetListCnt == 0) {
			alert("<?php echo $msg_selValidPresetNumber[$GLOBALS['LANGINDEX']]; ?>");
			return;
		}
	}	
	
	msg += "<"+actionCmd+"PTZGroup>";
	msg += "<Index>"+groupNo+"</Index>";
	if (actionCmd == 'Add') {
		msg += "<Enabled>1</Enabled>";
		for (var index=0; index<presetListCnt; ++index) {
			var params = ['', '', 'Speed', 'DWT'];
			msg += "<PresetList"+(index+1)+">";
			var presetVal = $("#GroupList_"+groupNo+" tbody tr:eq("+index+") td:eq(1) select").val();

			msg += "<Preset>"+presetVal+"</Preset>";
			for (var index2=2; index2<params.length; ++index2) {
				var selector = "#GroupList_"+groupNo+" tbody tr:eq("+index+") td:eq("+(index2)+")";
				
				if (CheckValueRange($("#GroupList_"+groupNo+" tbody tr:eq("+index+") td:eq(2) input").val(), 1, 64, "<?php echo EnterNumber(1,64); ?>")) return;
				if (CheckValueRange($("#GroupList_"+groupNo+" tbody tr:eq("+index+") td:eq(3) input").val(), 1, 128, "<?php echo EnterNumber(1,128); ?>")) return;
				
				if(!TypeCheck($("#GroupList_"+groupNo+" tbody tr:eq("+index+") td:eq(2) input").val(), NUM+ALPHA)) {
					alert("<?php echo EnterNumber(1,64); ?>");
					return;
				}
				if(!TypeCheck($("#GroupList_"+groupNo+" tbody tr:eq("+index+") td:eq(3) input").val(), NUM+ALPHA)) {
					alert("<?php echo EnterNumber(1,128); ?>");
					return;
				}
				
				selector += " input";
				msg += "<"+params[index2]+">"+$(selector).val()+"</"+params[index2]+">";
			}
			msg += "</PresetList"+(index+1)+">";
		}
		applyMsg = "<?php echo $t_set[$GLOBALS['LANGINDEX']]; ?>";
	}
	else if (actionCmd == 'Remove') {
		msg += "<Enabled>0</Enabled>";
		for (var index=0; index<presetListCnt; ++index) {
			var params = ['', '', 'Speed', 'DWT'];
			msg += "<PresetList"+(index+1)+">";
			msg += "<Preset>0</Preset>";
			msg += "<Speed>64</Speed>";			
			msg += "<DWT>3</DWT>";
			msg += "</PresetList"+(index+1)+">";
		}
		applyMsg = "<?php echo $t_remove[$GLOBALS['LANGINDEX']]; ?>";
	}
	msg += "</"+actionCmd+"PTZGroup>";
	SetPTZCookie('Group');
	RequestAjaxMsg(msg, applyMsg, ajaxReqUrl, cmdMsg);	
}

function OnChangeSpeed(index) {
	var groupNo = $("#GroupNo").val();
	if (CheckValueRange($('#GroupList_'+groupNo+' #GroupList_speed_'+index).val(), 1, 64, "<?php echo EnterNumber(1,64); ?>")) return;

	if(!TypeCheck($("#GroupList_" +groupNo+ " #GroupList_speed_"+index).val(), NUM+ALPHA)) {
		alert("<?php echo EnterNumber(1,64); ?>");
		return;
	}
}

function OnChangeDwelltime(index) {	
	var groupNo = $("#GroupNo").val();
	if (CheckValueRange($('#GroupList_'+groupNo+' #GroupList_dwt_'+index).val(), 1, 128, "<?php echo EnterNumber(1,128); ?>")) return;	
	if(!TypeCheck($("#GroupList_" +groupNo+ " #GroupList_dwt_"+index).val(), NUM+ALPHA)) {
		alert("<?php echo EnterNumber(1,128); ?>");
		return;
	}
}

function OnChangeGroupNo()
{
	var groupNo = $('#GroupNo').val();
	$('#GroupList_'+prevGroupNo).css('display', 'none');
	$('#GroupList_'+prevGroupNo+' tbody').empty();
	$('#GroupList_'+groupNo).css('display', 'inline');
	prevGroupNo = groupNo;
	DrawGroupList();
}

function OnChangeGroupListNum(index){
	var groupNo = $("#GroupNo").val();
	if (CheckValueRange($('#GroupList_'+groupNo+' #GroupList_presetno_'+index).val(), 0, 255, "<?php echo EnterNumber(0,255); ?>")) return;

	if(!TypeCheck($("#GroupList_" +groupNo+ " #GroupList_presetno_"+index).val(), NUM+ALPHA)) {
		alert("<?php echo EnterNumber(0,255); ?>");
		return;
	}
}

function CheckGroupList(isAdd)
{
	if($("#GroupList_"+$("#GroupNo").val()+" tbody tr").size() > 8){
		$("#Groupdiv").css("overflow-y", "scroll");
		$("#Groupdiv").css("height", "288px");
		if(isAdd){
			$("#Groupdiv").scrollTop($("#Groupdiv")[0].scrollHeight);
		}
	}
	else{
		$("#Groupdiv").css("overflow-y", "hidden");
		$("#Groupdiv").css("height", "");
	}
}

function InitGroupList() {
	<?php
		for ($index=0; $index<MAX_PTZ_GROUP; ++$index) { 
	?>
			groupNo[<?php echo $index; ?>] = {};			
			groupNo[<?php echo $index; ?>].presetList = new Array();
	<?php
		for ($index2=0; $index2<MAX_PRESET_OF_PRESETLIST; ++$index2) { ?>
	
			
			groupNo[<?php echo $index; ?>].presetList[<?php echo $index2; ?>] = {};
	<?php
			if ($groupsConf->group[$index]['PresetList'][$index2]['Preset']['value'] != 0) {
	?> 		
				groupNo[<?php echo $index; ?>].presetList[<?php echo $index2; ?>].presetNum = <?php echo $groupsConf->group[$index]['PresetList'][$index2]['Preset']['value']; ?>;
				<?php $tempValue = $groupsConf->group[$index]['PresetList'][$index2]['Preset']['value']-1; ?>
				groupNo[<?php echo $index; ?>].presetList[<?php echo $index2; ?>].presetName = "<?php echo trim($presetConf->preset[$tempValue]->dataInfo['Name']['value']); ?>";
				groupNo[<?php echo $index; ?>].presetList[<?php echo $index2; ?>].speed = <?php echo $groupsConf->group[$index]['PresetList'][$index2]['Speed']['value']; ?>;
				groupNo[<?php echo $index; ?>].presetList[<?php echo $index2; ?>].dwt = <?php echo $groupsConf->group[$index]['PresetList'][$index2]['DWT']['value']; ?>;

	<?php		
			} else {
	?>			
			groupNo[<?php echo $index; ?>].presetList[<?php echo $index2; ?>].presetNum = 0;
			groupNo[<?php echo $index; ?>].presetList[<?php echo $index2; ?>].presetName = "<?php echo $t_none[$GLOBALS["LANGINDEX"]]; ?>";
			groupNo[<?php echo $index; ?>].presetList[<?php echo $index2; ?>].speed = 64;
			groupNo[<?php echo $index; ?>].presetList[<?php echo $index2; ?>].dwt = 3;	
			
	<?php	
				}
			}
		}
	?>	
}

function DrawGroupList() {
	var groupList = "";
	var groupNum = parseInt($("#GroupNo").val());

	for(var index=0; index<MAX_PRESET_OF_PRESETLIST; ++index) {
		groupList = "<tr class='GroupList_"+groupNum+"_PresetList_"+index+"'>\
					<td></td>\
					<td>\
						<select id='GroupList_presetno_"+index+"' class='selectbox_style' style='float:inherit;margin-left:5px;width:150px;background-color:#b4b9c5' onmouseenter=\"OnMouseEnterPresetList('GroupList_"+groupNum+"', 'GroupList_presetno_"+index+"');\">"
		if(groupNo[groupNum-1].presetList[index].presetNum != 0 && groupNo[groupNum-1].presetList[index].presetName.length != 0) {
			groupList += "<option value='"+(groupNo[groupNum-1].presetList[index].presetNum)+"' selected=\"selected\">"+groupNo[groupNum-1].presetList[index].presetNum+":"+groupNo[groupNum-1].presetList[index].presetName+"</option>"
		} else { 
			groupList += "<option value='0'><?php echo $t_none[$GLOBALS["LANGINDEX"]]; ?></option>"
		}
		groupList += "</select>\
				</td>\
				<td><input type='text' id='GroupList_speed_"+index+"' class='listtext' style='width:80px;' value='"+groupNo[groupNum-1].presetList[index].speed+"' maxlength='2'\
						onkeypress=\"IsNum(event)\" onkeydown=\"OnlyNUm(event);\" onchange=\"OnChangeSpeed("+groupNum+")\" />\
				</td>\
				<td><input type='text' id='GroupList_dwt_"+index+"' class='listtext' style='width:80px;' value='"+groupNo[groupNum-1].presetList[index].dwt+"' maxlength='3'\
						onkeypress=\"IsNum(event)\" onkeydown=\"OnlyNUm(event);\" onchange=\"OnChangeDwelltime("+groupNum+")\" />\
				</td>\
			</tr>"
			
			$("#GroupList_"+groupNum+" tbody").append(groupList);
		}
		CheckGroupList(false);	
}

function OnMouseEnterPresetList(group, id) {
	var select = document.getElementById(id);
	var option_value = select.options[select.selectedIndex].value;

	if($("#" + id).children().length > 1)
		return false;

	$("#" + id).html("");
	$("#" + id).append('<option value=0><?php echo $t_none[$GLOBALS["LANGINDEX"]]; ?></option>');
<?php
	for($index=1; $index<=MAX_PTZ_PRESET255; ++$index) {
		if ($presetConf->preset[$index-1]->dataInfo['Enabled']['value'] == 0) continue;
?>
			$("#"+ group + " #" + id).append('<option value="<?php echo $index; ?>"><?php echo $index.':'.trim($presetConf->preset[$index-1]->dataInfo['Name']['value']); ?></option>');
<?php
	}
?>
	$("#"+ group + " #" + id + " option[value = "+option_value+"]").attr("selected", true);
	
}

</script>

<div id="tabs-group">
	<table class="data_write mgt10 mgl-20 pdl15">
		<colgroup>
			<col style="width:180px;"/>
			<col />
		</colgroup>
		<tbody>
			<tr>
				<th> <?php echo $t_groupNo[$GLOBALS['LANGINDEX']]; ?> </th>
				<td>
					<select id="GroupNo" class="selectbox_style" style="width:54px;" onchange="OnChangeGroupNo();" >
						<option value="1">1</option>
						<option value="2">2</option>
						<option value="3">3</option>
						<option value="4">4</option>
						<option value="5">5</option>
						<option value="6">6</option>
					</select>
				</td>
			</tr>
			</tbody>
	</table>
	<table class="data_write mgl-20 pdl15" style="width:645px;">
		<colgroup>
			<col style="width:180px;"/>
			<col />
		</colgroup>
		<tbody>
			<tr>
				<td colspan="2" style="text-align:right;">
					<a class="btn_setup" href="javascript:OnClickGroup('Remove');" style="color:#fff"> <?php echo $t_remove[$GLOBALS['LANGINDEX']]; ?> </a>
				</td>
			</tr>
			<tr>
				<th style="vertical-align:top"><?php echo $t_presetList[$GLOBALS['LANGINDEX']]; ?></th>
				<td>
					<div id="Groupdiv" style="overflow-y:hidden;">
				<?php
					for ($index=0; $index<MAX_PTZ_GROUP; ++$index) {
				?>

						<table id="GroupList_<?php echo ($index+1); ?>" class="data_table2" style="width:429px; <?php if ($index != 0) echo 'display:none'; ?>">
							<colgroup>
								<col style="width:20px;" />
								<col style="width:170px;" />
								<col style="width:100px;" />
								<col style="width:130px;" />
							</colgroup>
							<thead>
								<tr>
									<th></th>
									<th> <?php echo $t_presetNo[$GLOBALS['LANGINDEX']]; ?> </th>
									<th> <?php echo $t_speed[$GLOBALS['LANGINDEX']]; ?> </th>
									<th> <?php echo $t_dwt[$GLOBALS['LANGINDEX']]; ?> </th>
								</tr>
							</thead>
							<tbody>						
					
							</tbody>
						</table>
				<?php
					}
				?>
					</div>
				</td>
			</tr>
			<tr>
				<td></td>
				<td>
					<a class="btn_setup" href="javascript:OnClickGroup('Start');" style="color:#fff"> <?php echo $t_start[$GLOBALS['LANGINDEX']]; ?> </a>
					<a class="btn_setup" href="javascript:SISOPlugin.ptzControl.onClickPtzStop('sequence');" style="color:#fff"> <?php echo $t_stop[$GLOBALS['LANGINDEX']]; ?> </a>
					<a class="btn_setup" href="javascript:OnClickGroup('Add');" style="color:#fff; margin-left:170px;"> <?php echo $t_set[$GLOBALS['LANGINDEX']]; ?> </a>
				</td>
			</tr>
		</tbody>
	</table>
</div>
