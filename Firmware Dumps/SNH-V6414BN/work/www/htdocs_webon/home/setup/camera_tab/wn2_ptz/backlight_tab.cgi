<script type="text/javascript" language="javascript">
$(document).ready(function(){
	//top
	$("#top_up").hover(function(){ ChangeImage('top_up','../images/common/btn/backlight_up_press.png');
					}, function(){ ChangeImage('top_up','../images/common/btn/backlight_up_normal.png');
					}).click(function(){	OnClickBLCRange('top','up'); });
	$("#top_down").hover(function(){ ChangeImage('top_down','../images/common/btn/backlight_down_press.png');
					}, function(){ ChangeImage('top_down','../images/common/btn/backlight_down_normal.png');
					}).click(function(){ 	OnClickBLCRange('top','down'); });		
	//right
	$("#right_up").hover(function(){ ChangeImage('right_up','../images/common/btn/backlight_right_press.png');
					}, function(){ ChangeImage('right_up','../images/common/btn/backlight_right_normal.png');
					}).click(function(){ 	OnClickBLCRange('right','up'); });
	$("#right_down").hover(function(){ ChangeImage('right_down','../images/common/btn/backlight_left_press.png');
					}, function(){ ChangeImage('right_down','../images/common/btn/backlight_left_normal.png');
					}).click(function(){ 	OnClickBLCRange('right','down'); });
	//left
	$("#left_up").hover(function(){ ChangeImage('left_up','../images/common/btn/backlight_left_press.png');
					}, function(){ ChangeImage('left_up','../images/common/btn/backlight_left_normal.png');
					}).click(function(){ 	OnClickBLCRange('left','up'); });
	$("#left_down").hover(function(){ ChangeImage('left_down','../images/common/btn/backlight_right_press.png');
					}, function(){ ChangeImage('left_down','../images/common/btn/backlight_right_normal.png');
					}).click(function(){ 	OnClickBLCRange('left','down'); }); 
	//bottom
	$("#bottom_up").hover(function(){ ChangeImage('bottom_up','../images/common/btn/backlight_down_press.png');
					}, function(){ ChangeImage('bottom_up','../images/common/btn/backlight_down_normal.png');
					}).click(function(){ 	OnClickBLCRange('bottom','up'); });
	$("#bottom_down").hover(function(){ ChangeImage('bottom_down','../images/common/btn/backlight_up_press.png');
					}, function(){ ChangeImage('bottom_down','../images/common/btn/backlight_up_normal.png');
					}).click(function(){ 	OnClickBLCRange('bottom','down'); });
});

function MakeBacklightXml(mode)
{
	var msg = "";
	msg += "<ImageBackLight>";
  	msg += "<Mode>" + $("#blc_mode").val() + "</Mode>";
  	msg += "<BLCLevel>" + $("#blc_level").val() + "</BLCLevel>";
  	if (mode == TEST) {
  		msg += "<BLCDisplay>" + ($("#blc_boxmode").is(':checked') ? 1 : 0) + "</BLCDisplay>";
  	}
  	else {
		msg += "<BLCDisplay>0</BLCDisplay>";
		$("#blc_boxmode").prop("checked", false);
  	}

  	msg += "<BLCTop>" + blc_top + "</BLCTop>";
  	msg += "<BLCBottom>" + blc_bottom + "</BLCBottom>";
  	msg += "<BLCLeft>" + blc_left + "</BLCLeft>";
  	msg += "<BLCRight>" + blc_right + "</BLCRight>";
  	msg += "<WDRLevel>" + $("#wdr_level").val() + "</WDRLevel>";
  	msg += "<HLCLevel>" + $("#hlc_level").val() + "</HLCLevel>";
  	msg += "<HLCMasktone>" + $("#masktone").val() + "</HLCMasktone>";	
  	msg += "</ImageBackLight>";

  	blc_top = 0;
	blc_bottom = 0;
	blc_left = 0;
	blc_right = 0;
	return msg;
}

function ChangeBlcMenu(mode)
{
	if (mode == 'show') {
		if(SISOPlugin.ptzControl.ptzSlideStatus == 1) $('#blcbox').show();
		$("#blc_level").removeAttr("disabled");
		$("#blc_boxmode").removeAttr("disabled");
		$("#blc_boxadjust").removeAttr("disabled");
		$("#blc_boxstep").removeAttr("disabled");
	}
	else {
		$('#blcbox').hide();
		$("#blc_level").attr("disabled", "disabled");
		$("#blc_boxmode").attr("disabled", "disabled");
	}
}

function OnChangeBlcMode()
{
	if($("#blc_mode").val() == 1) { //BLC
		ChangeBlcMenu('show');
		$("#hlc_level").attr("disabled", "disabled");
		$("#masktone").attr("disabled", "disabled");
		$("#wdr_level").attr("disabled", "disabled");
		ChangeOption("sensor_mode", 0, 'Enable');		//sensor_tab.cgi
		ChangeOption("sensor_mode", 1, 'Enable');		//sensor_tab.cgi
	}
	else if($("#blc_mode").val() == 2) { //HLC
		ChangeBlcMenu('hide');
		$("#hlc_level").removeAttr("disabled");
		$("#masktone").removeAttr("disabled");
		$("#wdr_level").attr("disabled", "disabled");			
		ChangeOption("sensor_mode", 0, 'Enable');		//sensor_tab.cgi
		ChangeOption("sensor_mode", 1, 'Enable');		//sensor_tab.cgi
	}
	else if($("#blc_mode").val() == 3) { //WDR
		ChangeBlcMenu('hide');
		$("#hlc_level").attr("disabled", "disabled");
		$("#masktone").attr("disabled", "disabled");
		if(SENSOR_MODE == 0 || SENSOR_MODE == 1){
			$('#wdr_level').attr("disabled","disabled");
			$("#blc_mode").val(oldBlc_mode);
		}
		else{
			$("#wdr_level").removeAttr("disabled");
		}			
		ChangeOption("sensor_mode", 0, 'Disable');		//sensor_tab.cgi
		ChangeOption("sensor_mode", 1, 'Disable');		//sensor_tab.cgi
	}
	else { //OFF
		ChangeBlcMenu('hide');
		$("#hlc_level").attr("disabled", "disabled");
		$("#masktone").attr("disabled", "disabled");
		$("#wdr_level").attr("disabled", "disabled");		
		ChangeOption("sensor_mode", 0, 'Enable');		//sensor_tab.cgi
		ChangeOption("sensor_mode", 1, 'Enable');		//sensor_tab.cgi
	}
	
	<?php if ($event_name != 'presetedit') { ?>
		if ($("#blc_mode").val() == 3) {
			$("#shutter_min_lowFps").attr("disabled","disabled");
			$("#shutter_min_highFps").attr("disabled","disabled");
			$("#shutter_max_lowFps").attr("disabled","disabled");
			$("#shutter_max_highFps").attr("disabled","disabled");
		}
		else {
			if($("#aflk").val() != 1){		//exposure_tab.cgi
				$("#shutter_min_lowFps").removeAttr("disabled");
				$("#shutter_min_highFps").removeAttr("disabled");
				$("#shutter_max_lowFps").removeAttr("disabled");
				$("#shutter_max_highFps").removeAttr("disabled");
			}				
		}
	<?php } ?>
	oldBlc_mode = $("#blc_mode").val();
	SetTimeOut();
}

function OnClickBLCRange(pos1, pos2) 
{
	var blc_step = $("#blc_boxstep").val();

	blc_top = 0;
	blc_bottom = 0;
	blc_left = 0;
	blc_right = 0;
	if (pos1 == 'top') {
		if (pos2 == 'up') blc_top = blc_step;
		else	blc_top = blc_step * -1;
	}else if (pos1 == 'bottom') {
		if (pos2 == 'up') blc_bottom = blc_step;
		else	blc_bottom = blc_step * -1;
	}else if (pos1 == 'left') {
		if (pos2 == 'up') blc_left = blc_step;
		else	blc_left = blc_step * -1;
	}else if (pos1 == 'right') {
		if (pos2 == 'up') blc_right = blc_step;
		else	blc_right = blc_step * -1;
	}
	SetTimeOut();
}

function ParsingXML_ImageBackLight(xmlData)
{
	$("#blc_mode").val(xmlData.find('Mode').text());
	oldBlc_mode = $("#blc_mode").val();
	$("#blc_level").val(xmlData.find('BLCLevel').text());
	$("#wdr_level").val(xmlData.find('WDRLevel').text());
	$("#blc_boxmode").prop("checked", (xmlData.find('BLCDisplay').text()=='1'?true:false));
	$("#hlc_level").val(xmlData.find('HLCLevel').text());
	$("#masktone").val(xmlData.find('HLCMasktone').text());
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
				<select id="blc_mode"  class="selectbox_style_wid230" onchange="OnChangeBlcMode()" onclick="javascript:SISOPlugin.ptzControl.onClickBLCStatus();">
						<option value="0" <?php if ($imageBackLight->dataInfo["Mode"]["value"] == 0) echo "selected=\"selected\""; ?>><?php echo $t_off[$GLOBALS["LANGINDEX"]]; ?></option>
						<option value="1" <?php if ($imageBackLight->dataInfo["Mode"]["value"] == 1) echo "selected=\"selected\""; ?>><?php echo $t_blc[$GLOBALS["LANGINDEX"]]; ?></option>
				<?php 
					if (($GLOBALS['M_SUPPORT_BACKLIGHT']&BACKLIGHT_MASK_HLC) == BACKLIGHT_MASK_HLC) {
				?>	
						<option value="2" <?php if ($imageBackLight->dataInfo["Mode"]["value"] == 2) echo "selected=\"selected\""; ?>><?php echo $t_hlc[$GLOBALS["LANGINDEX"]]; ?></option>
				<?php
					}
					if (($GLOBALS['M_SUPPORT_BACKLIGHT']&BACKLIGHT_MASK_WDR) == BACKLIGHT_MASK_WDR) {
				?>
						<option value="3" <?php if ($imageBackLight->dataInfo["Mode"]["value"] == 3) echo "selected=\"selected\""; ?>><?php echo $t_wdr[$GLOBALS["LANGINDEX"]]; ?></option>
				<?php
					}
				?>
				</select>
			</td>
		</tr>		
		<?php 
			if (($GLOBALS['M_SUPPORT_BACKLIGHT']&BACKLIGHT_MASK_HLC) == BACKLIGHT_MASK_HLC) {
		?>				
		<tr>
			<th class="top_txt"><?php echo $t_hlclevel[$GLOBALS['LANGINDEX']]; ?></th>
			<td>
				<select id="hlc_level" class="selectbox_style_wid230" onchange="SetTimeOut()">
					<option value="0" <?php if ($imageBackLight->dataInfo["HLCLevel"]["value"] == 0) echo "selected=\"selected\""; ?>><?php echo $t_low[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="1" <?php if ($imageBackLight->dataInfo["HLCLevel"]["value"] == 1) echo "selected=\"selected\""; ?>><?php echo $t_middle[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="2" <?php if ($imageBackLight->dataInfo["HLCLevel"]["value"] == 2) echo "selected=\"selected\""; ?>><?php echo $t_high[$GLOBALS["LANGINDEX"]]; ?></option>
				</select>
			</td>
		</tr>
		<tr>
			<th class="top_txt"><?php echo $t_masktone[$GLOBALS["LANGINDEX"]]; ?></th>
			<td>
				<select id="masktone" class="selectbox_style_wid230" onchange="SetTimeOut()">
					<?php for ($index2=0; $index2<=15; $index2++) { ?>
					<option value="<?php echo $index2; ?>" <?php if ($imageBackLight->dataInfo["HLCMasktone"]["value"] == $index2) echo "selected=\"selected\""; ?>><?php echo $index2; ?></option>
					<?php } ?>
				</select>
			</td>
		</tr>
		<?php 
			}
			if (($GLOBALS['M_SUPPORT_BACKLIGHT']&BACKLIGHT_MASK_WDR) == BACKLIGHT_MASK_WDR) {
		?>
		<tr>
			<th class="top_txt"><?php echo $t_wdrlevel[$GLOBALS["LANGINDEX"]]; ?></th>
			<td>
				<select id="wdr_level"	class="selectbox_style_wid230" onchange="SetTimeOut()">
					<option value="0" <?php if ($imageBackLight->dataInfo["WDRLevel"]["value"] == 0) echo "selected=\"selected\""; ?>><?php echo $t_low[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="1" <?php if ($imageBackLight->dataInfo["WDRLevel"]["value"] == 1) echo "selected=\"selected\""; ?>><?php echo $t_middle[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="2" <?php if ($imageBackLight->dataInfo["WDRLevel"]["value"] == 2) echo "selected=\"selected\""; ?>><?php echo $t_high[$GLOBALS["LANGINDEX"]]; ?></option>
				</select>
			</td>
		</tr>
		<?php
			}
		?>
		<tr>
			<th class="top_txt"><?php echo $t_blclevel[$GLOBALS["LANGINDEX"]]; ?></th>
			<td>
				<select id="blc_level" class="selectbox_style_wid230" onchange="SetTimeOut()">
					<option value="0" <?php if ($imageBackLight->dataInfo["BLCLevel"]["value"] == 0) echo "selected=\"selected\""; ?>><?php echo $t_low[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="1" <?php if ($imageBackLight->dataInfo["BLCLevel"]["value"] == 1) echo "selected=\"selected\""; ?>><?php echo $t_middle[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="2" <?php if ($imageBackLight->dataInfo["BLCLevel"]["value"] == 2) echo "selected=\"selected\""; ?>><?php echo $t_high[$GLOBALS["LANGINDEX"]]; ?></option>
				</select>
			</td>
		</tr>		
		<tr>
			<th class="top_txt"> <?php echo $t_blcboxmode[$GLOBALS["LANGINDEX"]]; ?></th>
			<td>
				<label><input type="checkbox" id="blc_boxmode" onclick="SetTimeOut()" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_use[$GLOBALS['LANGINDEX']]; ?></label>
			</td>
		</tr>		
	</tbody>
</table>
	<div id="blcbox" style="display=none;width:320px;position:absolute;top:-355px;left:345px;">
	<table class="data_write mgt10 mgl-20" style="width:320px;">
		<colgroup>
			<col style="width:180px;"/>
			<col />
		</colgroup>
		<tr>
			<th class="top_txt"> <?php echo $t_blcboxadjust[$GLOBALS["LANGINDEX"]]; ?></th>
			<td>
				<div id="blc_boxadjust">
					<table id="adjust">
						<tr>
							<td style="text-align:center;padding:0px;">
								<table class="blc_box">
									<tr>
										<td colspan="2"></td>
										<td>
											<img id="top_up" src="../images/common/btn/backlight_up_normal.png" style="margin-bottom:-2px" />
										</td>
										<td colspan="2"></td>
									</tr>
									<tr>
										<td colspan="2"></td>
										<td>
											<img id="top_down" src="../images/common/btn/backlight_down_normal.png" style="" />
										</td>
										<td colspan="2"></td>
									</tr>
									<tr>
										<td>
											<img id="left_up" src="../images/common/btn/backlight_left_normal.png" style="margin-right:2px" />
										</td>
										<td>
											<img id="left_down" src="../images/common/btn/backlight_right_normal.png" style="margin-left:-12px" />
										</td>
										<td>
										</td>
										<td>
											<img id="right_down" src="../images/common/btn/backlight_left_normal.png" style="margin-right:-16px" />
										</td>
										<td>
											<img id="right_up" src="../images/common/btn/backlight_right_normal.png" style="margin-left:4px" />
										</td>
									</tr>
									<tr>
										<td colspan="2"></td>
										<td>
											<img id="bottom_down" src="../images/common/btn/backlight_up_normal.png" style="" />
										</td>
										<td colspan="2"></td>
									</tr>
									<tr>
										<td colspan="2"></td>
										<td>
											<img id="bottom_up" src="../images/common/btn/backlight_down_normal.png" style="" />
										</td>
										<td colspan="2"></td>
									</tr>
								</table>
							</td>
						</tr>
					</table>
				</div>
			</td>
		</tr>
		<tr>
			<th class="top_txt"> <?php echo $t_blcboxstep[$GLOBALS['LANGINDEX']]; ?></th>
			<td>
				<select id="blc_boxstep" class="selectbox_style" style="width:145px;" onchange="">
					<option value="5" selected="seledted">5</option>
					<option value="4">4</option>
					<option value="3">3</option>
					<option value="2">2</option>
					<option value="1">1</option>
				</select>
			</td>
		</tr>
	</table>
</div>
