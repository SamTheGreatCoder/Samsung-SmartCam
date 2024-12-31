<script type="text/javascript" language="javascript">
function OnClickSavePreset() {	
	$("#savePreset").dialog("open"); 
	
	<?php if($event_name=='presetedit') { ?>
		var target = $(".ptzControl");
	<? } else { ?>	
		var target = $(".ptztitle");
	<? } ?>
	$("#savePreset").dialog("widget").position({
		my: 'center',
		of: target
	});

	$("#PresetList").empty();

	var isFirstUnSet = false;
	for (var index=1; index<=MAX_PRESET_CNT; index++) {
		$("#PresetList").append('<option value="'+index+'">'+index+':'+selectPresetName[index-1]+'</option>');
		if(selectPresetName[index-1] == "" && !isFirstUnSet){
			$("#PresetList").val(index);	
			isFirstUnSet = true;
		}
	}
}

function SetSavePresetDialog(){
	var msg = "";
	var cmdMsg = "NO_REFRESH";
	
	$("#savePreset").dialog({
		autoOpen: false,
		modal: true,
		draggable: false,
		dialogClass: 'scheduleTable',
		title: "<?php echo $menu_presetsetup[$GLOBALS['LANGINDEX']]; ?>",
		buttons: [{
			text: "<?php echo $t_ok[$GLOBALS['LANGINDEX']]; ?>",		//Apply
			click: function() { 

				var tempPresetNum = parseInt($("#PresetList option:selected").val());
				var tempPresetName = $("#PresetName").val();
				var presetListCnt = 0;
				
	
				if($('#PresetName').val() == "" || !TypeCheck($('#PresetName').val(), NUM+ALPHA)) {
					alert("<?php echo $msg_validPresetName[$GLOBALS['LANGINDEX']]; ?>");
					return;
				}	
				
				msg = "<AddPTZPreset>"; 				
				msg += "<Index>"+tempPresetNum+"</Index>";
				msg += "<Name>"+tempPresetName+"</Name>"; 				
				msg += "</AddPTZPreset>";
			

				$("#PresetList option:eq("+(tempPresetNum-1)+")").empty().append(tempPresetNum + ":" + tempPresetName);				
				$("#PresetName").val("");

				RequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, "NO_REFRESH", true);
				localSeq++;

				
				$("#preset_list li").remove();	
				$("#ptzPresetNo").empty();
				DrawPresetList(1, tempPresetNum, tempPresetName);
				
				SetCookie("PresetStatus", $("#PresetList").val());
				$(this).dialog( "close" );
				$("#PresetList option:eq("+(tempPresetNum-1)+")").attr('selected',true)
				}
			}, {
				text: "<?php echo $t_cancel[$GLOBALS['LANGINDEX']]; ?>", 	// Cancel
				click: function() {
					$("#PresetName").val("");
					$(this).dialog( "close" );
				}
			}]
		});
}

</script>

<div id="savePreset" style="display:none;width:300px;" >
	<table class="data_write" style="width:280px;">
		<colgroup>
			<col style="width:100px;" />
			<col />
		</colgroup>
		<tbody>
			<tr>
				<th scope="row"><?php echo $t_number[$GLOBALS['LANGINDEX']]; ?></th>
				<td>
					<select class="selectbox_style" id="PresetList" style="width:160px;"></select>
				</td>
			</tr>
			<tr>
				<th scope="row"><?php echo $t_name[$GLOBALS['LANGINDEX']]; ?></th>
				<td>
					<input type="text" class="text" id="PresetName" value="" maxlength ="12" onkeypress="IsNumChar(event); NoKorean(event)" onkeydown='NoKorean(event);' style="width:155px;" >
				</td>
			</tr>
		</tbody>
	</table>
</div>	
					
<style>
.ui-dialog{
	z-index:1000 !important;
	background: #EFF1F3;
}
.ui-widget-overlay {
	width:1200px;
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
.ui-dialog .ui-widget-content {background: #EFF1F3;border: none;margin-left: 10px;margin-top:10px;}
.ui-dialog .ui-dialog-buttonpane .ui-dialog-buttonset { text-align:center}
.ui-dialog .ui-dialog-buttonset button{ background: #EFF1F3; margin: 0 10px;}
.ui-dialog .ui-dialog-buttonpane{ border: none; padding: 10px 0}
.ui-dialog .ui-resizable-handle{ display: none !important;}
.ui-dialog .ui-widget-content p{ display:block;clear: both;}
.ui-dialog .ui-widget-content input,.ui-dialog .ui-widget-content label{float:left;}
.ui-button.ui-state-default { color:#000;}

.ui-dialog.scheduleTable {
	left: 490px !important;
	width: 300px !important;
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
	//width:251px;
}
</style>

