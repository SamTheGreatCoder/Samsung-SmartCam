<script type="text/javascript" language="javascript">
var tourSetStatus = false;

var tourEnable	= new Array();
var tourNo 		= new Array();
var tourDWT 	= new Array();

<?php
	for($index = 0; $index<MAX_PTZ_GROUP; $index++) {
?>
	tourEnable[<?php echo $index; ?>] = <?php echo $tourConf->dataInfo['Enabled']['value']; ?>;

	<?php
		$tempVal = $tourConf->groupList[$index]->dataInfo['Group']['value'];
		if ($groupsConf->group[$tempVal-1]['DataInfo']['Enabled']['value'] == 1) { 
	?>
		tourNo[<?php echo $index; ?>] = <?php echo $tempVal; ?>;
	<?php }else{ ?>
		tourNo[<?php echo $index; ?>] = 0;
	<?php } ?>
	
	
	tourDWT[<?php echo $index; ?>] = <?php echo $tourConf->groupList[$index]->dataInfo['DWT']['value']; ?>;
<?php
	}
?> 

function OnMouseEnterGroupList(id) {
	var groupList="";
	var select = document.getElementById(id);
	var option_value = select.options[select.selectedIndex].value;
	
	if($("#" + id).children().length <= 1){
		groupList += '<option value=0>---</option>';
			<?php
				for ($index=0; $index<MAX_PTZ_GROUP; ++$index) {
					if ($groupsConf->group[$index]['DataInfo']['Enabled']['value'] == 1) {
			?>
						groupList +='<option value="<?php echo ($index+1); ?>"><?php echo ($index+1); ?></option>';
			<?php
					}
				}
			?>
		$("#" + id).html("");
		$("#" + id).append(groupList);	
		$("#" + id + " option[value = "+option_value+"]").attr("selected", true);
	}
}

function DrawTourList() {
	for(var index=0; index<MAX_PTZ_GROUP; index++) {
		var tourList ="<tr class='TourList_"+index+"'>\
						<td></td>\
						<td>\
							<select class='selectbox_style' id='TourGroupNo_"+index+"' style='float:inherit;margin-left:5px;width:54px;background-color:#b4b9c5' onmouseenter=\"OnMouseEnterGroupList('TourGroupNo_"+index+"')\">"
			if(tourNo[index] != 0) {
					tourList += "<option value='"+tourNo[index]+"' selected=\"selected\">"+tourNo[index]+"</option>"
			} else {
					tourList += "<option value='0'>---</option>"
			}	
			tourList += "</select>\
							<td>\
								<input id = 'TourDWT_"+index+"' type='text' class='listtext' maxlength='3' style='width: 50px;' onkeypress='IsNum(event); NoKorean(event)' onkeydown='NoKorean(event)' value='"+tourDWT[index]+"' />\
							</td>" 
			
		$("#TourList").append(tourList);
	}
}


function OnClickTour(actionCmd)
{
	var msg = "";
	var applyMsg = '';
	var cmdMsg = '';
	var groupListCnt = $("#TourList tbody tr").size();
	
	if(actionCmd == 'Start') {
		if (tourSetStatus == true) {
			alert("<?php echo $msg_groupListChange[$GLOBALS['LANGINDEX']]; ?>");
			return;
		}
	}
	else {
		for (var index=0; index<groupListCnt; ++index) {
			if (CheckValueRange($("#TourDWT_"+index).val(), 1, 128, "<?php echo EnterNumber(1,128); ?>")) return;	
			if(!TypeCheck($('#TourDWT_'+index).val(), NUM+ALPHA)) {
				alert("<?php echo EnterNumber(1,128); ?>");
				return;
			}
		}
		
		if (groupListCnt == 0) {
			alert("<?php echo $msg_checkTourSettingValue[$GLOBALS['LANGINDEX']]; ?>");
			return;
		}
	}	

	if(actionCmd == "Remove") {
		msg += "<SetPTZTour>";
		for(var i=0; i < MAX_GROUP_OF_TOUR_CNT; i++) {
			msg += "<GroupList"+(i+1)+">";
			msg += "<Group>0</Group>";
			msg += "<DWT>1</DWT>";
			msg += "</GroupList"+(i+1)+">";
		}
		msg += "</SetPTZTour>";
	}
	else {
		msg += "<"+actionCmd+"PTZTour>";
		if (actionCmd == "Set") {
			msg += "<Enabled>1</Enabled>";
			for (var index=0; index<groupListCnt; ++index) {
				msg += "<GroupList"+index+">";
				msg += "<Group>"+$('#TourGroupNo_'+index).val()+"</Group>";
				msg += "<DWT>"+$('#TourDWT_'+index).val()+"</DWT>";
				msg += "</GroupList"+index+">";
			}
		}
		msg += "</"+actionCmd+"PTZTour>";
	}
	if(actionCmd == "Set") {
		applyMsg = "<?php echo $t_set[$GLOBALS['LANGINDEX']]; ?>";
	}
	else if(actionCmd == "Remove") {
		applyMsg = "<?php echo $t_remove[$GLOBALS['LANGINDEX']]; ?>";
	}
	else if (actionCmd == 'Start') {
		cmdMsg = 'NO_REFRESH';
	}
	SetPTZCookie('Tour');
	RequestAjaxMsg(msg, applyMsg, ajaxReqUrl, cmdMsg);
}

</script>

<div id="tabs-tour">
	<table class="data_write mgl-20 pdl15 mgt10" style="width:645px;">
		<colgroup>
			<col style="width:180px;"/>
			<col />
		</colgroup>
		<tbody>
			<tr>
				<td colspan="2" style="text-align:right;">
					<a class="btn_setup" href="javascript:OnClickTour('Remove');" style="color:#fff; margin-right:18px;"> <?php echo $t_remove[$GLOBALS['LANGINDEX']]; ?> </a>
				</td>
			</tr>
			<tr>
				<th style="vertical-align:top"> <?php echo $t_groupList[$GLOBALS['LANGINDEX']]; ?> </th>
				<td>
					<table id="TourList" class="data_table2" style="width:429px;">
						<colgroup>
							<col style="width:20px;" />
							<col style="width:100px;" />
							<col style="width:130px;" />
							<col />
						</colgroup>
						<thead>
							<tr>
								<th></th>
								<th> <?php echo $t_groupNo[$GLOBALS['LANGINDEX']]; ?> </th>
								<th> <?php echo $t_dwt[$GLOBALS['LANGINDEX']]; ?></th>
							</tr>
						</thead>
						<tbody>
						</tbody>
					</table>
				</td>
			</tr>
			<tr>
				<td></td>
				<td>
					<a class="btn_setup" href="javascript:OnClickTour('Start');" style="color:#fff"> <?php echo $t_start[$GLOBALS['LANGINDEX']]; ?> </a>			
					<a class="btn_setup" href="javascript:SISOPlugin.ptzControl.onClickPtzStop('sequence');" style="color:#fff"> <?php echo $t_stop[$GLOBALS['LANGINDEX']]; ?> </a>
					<a class="btn_setup" href="javascript:OnClickTour('Set');" style="color:#fff; margin-left:152px;"> <?php echo $t_set[$GLOBALS['LANGINDEX']]; ?> </a>		
				</td>
			</tr>
		</tbody>
	</table>
</div>
