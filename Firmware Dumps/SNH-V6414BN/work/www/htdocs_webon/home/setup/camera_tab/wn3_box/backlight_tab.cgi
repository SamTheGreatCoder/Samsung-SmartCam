<script type="text/javascript" language="javascript">

$(document).ready(function(){
<?php
	$minBlcHeightLength = 40;
	$minBlcWidthLength = 30;
	$maxBlcLength = 60;

	$blcTopMin 		= $imageBackLight->dataInfo["BLCBottom"]["value"]-$maxBlcLength;
	$blcTopMax 		= $imageBackLight->dataInfo["BLCBottom"]["value"]-$minBlcHeightLength;
	$blcBottomMin 	= $imageBackLight->dataInfo["BLCTop"]["value"]+$minBlcHeightLength;
	$blcBottomMax 	= $imageBackLight->dataInfo["BLCTop"]["value"]+$maxBlcLength;
	$blcLeftMin 	= $imageBackLight->dataInfo["BLCRight"]["value"]-$maxBlcLength;
	$blcLeftMax 	= $imageBackLight->dataInfo["BLCRight"]["value"]-$minBlcWidthLength;
	$blcRightMin 	= $imageBackLight->dataInfo["BLCLeft"]["value"]+$minBlcWidthLength;
	$blcRightMax 	= $imageBackLight->dataInfo["BLCLeft"]["value"]+$maxBlcLength;
	
	$blclist = array( "blc_top"		=>array(1,100,$blcTopMin,$blcTopMax,$imageBackLight->dataInfo["BLCTop"]["value"]),
							"blc_bottom"=>array(1,100,$blcBottomMin,$blcBottomMax,$imageBackLight->dataInfo["BLCBottom"]["value"]),
							"blc_left"	=>array(1,100,$blcLeftMin,$blcLeftMax,$imageBackLight->dataInfo["BLCLeft"]["value"]), 
							"blc_right"	=>array(1,100,$blcRightMin,$blcRightMax,$imageBackLight->dataInfo["BLCRight"]["value"]));
	foreach ($blclist as $name=>$data) {
?>		
		$("#<?php echo $name; ?>").slider({
			name: "blc_slider",
			orientation: "horizontal",
			min: <?php echo $data[0]; ?>,
			max: <?php echo $data[1]; ?>,
			limitMin: <?php if($data[2] < 1){ echo 1; } else{ echo $data[2]; } ?>,
			limitMax: <?php if($data[3] > 100){ echo 100; } else {echo $data[3]; } ?>,
			value: <?php echo $data[4]; ?>,
			range: "min",
			slide: function( event, ui ) {
				$("#<?php echo $name; ?>_value").html(ui.value);
			},
			change: function(event, ui) {
					SetTimeOut();
			},
			stop: function(event, ui) {
				SetBlcRange("<?php echo $name; ?>", ui.value);
			}
		});
		$("#<?php echo $name; ?>_value").html($("#<?php echo $name; ?>").slider("value"));
<?php		
	}
?>
});

function MakeBacklightXml(mode)
{
	var msg = "";
	msg += "<ImageBackLight>";
  	msg += "<Mode>" + $("#blc_mode").val() + "</Mode>";
  	msg += "<BLCLevel>" + $("#blc_level").val() + "</BLCLevel>";
	msg += "<BLCTop>" + $("#blc_top").slider("option","value") + "</BLCTop>";
	msg += "<BLCBottom>" + $("#blc_bottom").slider("option","value") + "</BLCBottom>";
	msg += "<BLCLeft>" + $("#blc_left").slider("option","value") + "</BLCLeft>";
	msg += "<BLCRight>" + $("#blc_right").slider("option","value") + "</BLCRight>";
<?php 
	if (($GLOBALS['M_SUPPORT_BACKLIGHT']&BACKLIGHT_MASK_WDR) == BACKLIGHT_MASK_WDR) {
?>
		msg += "<WDRLevel>" + $("#wdr_level").val() + "</WDRLevel>";
<?php
	}
?>
  	msg += "</ImageBackLight>";
	return msg;
}

function OnChangeBlcMode()
{
	var isDisable = false;
	if($("#blc_mode").val() == 1){
		$("#blc_level").removeAttr("disabled");		
		$("#blc_top").slider("option","disabled",false);
		$("#blc_bottom").slider("option","disabled",false);
		$("#blc_left").slider("option","disabled",false);
		$("#blc_right").slider("option","disabled",false);
		$("#wdr_level").attr("disabled", "disabled");	
		<?php if($GLOBALS['M_SUPPORT_SENSOR_FRAMEMODE'] && $GLOBALS['M_MAX_SERSORFRAME'] == 60) { ?>
			ChangeOption('sensor_mode', 0, 'Enable');
			ChangeOption('sensor_mode', 1, 'Enable');
		<?php } ?>
		isDisable = false;
	}
	else{
		if($("#blc_mode").val() == 3){
			$("#wdr_level").removeAttr("disabled");	
			<?php if($GLOBALS['M_SUPPORT_SENSOR_FRAMEMODE'] && $GLOBALS['M_MAX_SERSORFRAME'] == 60) { ?>			
				ChangeOption('sensor_mode', 0, 'Disable');
				ChangeOption('sensor_mode', 1, 'Disable');
			<?php } ?>
		}
		else{
			$("#wdr_level").attr("disabled", "disabled");
			<?php if($GLOBALS['M_SUPPORT_SENSOR_FRAMEMODE'] && $GLOBALS['M_MAX_SERSORFRAME'] == 60) { ?>			
				ChangeOption('sensor_mode', 0, 'Enable');
				ChangeOption('sensor_mode', 1, 'Enable');
			<?php } ?>
		}
		$("#blc_level").attr("disabled", "disabled");
		isDisable = true;

		$("#blc_top").slider("option","disabled",true);
		$("#blc_bottom").slider("option","disabled",true);
		$("#blc_left").slider("option","disabled",true);
		$("#blc_right").slider("option","disabled",true);		
	}
	if(!isOnloading){ 
		if(oldBlc_mode == 3){
			<?php if(GetBrowserName() == 'IE' && ieversion() <= 7) { ?>
				SetEnableAllShutter();
			<?php } ?>
			if($("#preset_default").val() == 7){		//av_camera.cgi
				$("#shutter_speed_min").val(4);
			}
			userPresetValue["MinShutter"] = 4;
			<?php if($GLOBALS['M_MAX_RESOLUTION'] == MAX_3_MEGA){ ?>
				$("#shutter_speed_max").val(30);
				userPresetValue["MaxShutter"] = 30;			
			<?php }else{ ?>
				$("#shutter_speed_max").val(29);
				userPresetValue["MaxShutter"] = 29;
			<?php } ?>
			OnChangeShutter();
		}
		else{
			if($("#blc_mode").val() == 3){
				<?php if(GetBrowserName() == 'IE' && ieversion() <= 7) { ?>
					SetEnableAllShutter();
				<?php } ?>
				if($("#preset_default").val() == 7){		//av_camera.cgi
					$("#shutter_speed_min").val(4);
				}
				userPresetValue["MinShutter"] = 4;
				<?php if($GLOBALS['M_MAX_RESOLUTION'] == MAX_3_MEGA){ ?>
					$("#shutter_speed_max").val(17);
					userPresetValue["MaxShutter"] = 17;
				<?php }else{ ?>
					$("#shutter_speed_max").val(16);
					userPresetValue["MaxShutter"] = 16;
				<?php } ?>
				OnChangeShutter();
			}
		}
	}
	oldBlc_mode = $("#blc_mode").val();
	SetButtonHoverFunction(isDisable, 'blc_top_left');
	SetButtonHoverFunction(isDisable, 'blc_top_right');
	SetButtonHoverFunction(isDisable, 'blc_bottom_left');
	SetButtonHoverFunction(isDisable, 'blc_bottom_right');
	SetButtonHoverFunction(isDisable, 'blc_left_left');
	SetButtonHoverFunction(isDisable, 'blc_left_right');
	SetButtonHoverFunction(isDisable, 'blc_right_left');
	SetButtonHoverFunction(isDisable, 'blc_right_right');	
	
	SetTimeOut();
}

function SetEnableAllShutter(){
	<?php if(GetBrowserName() == 'IE' && ieversion() <= 7) { ?>
	var shutterSize = $("#shutter_speed_min").length;
	
	for(var i = 0 ; i < shutterSize; i++){
		ChangeOption('shutter_speed_min', i, 'Enable');
		ChangeOption('shutter_speed_max', i, 'Enable');
	}
	<?php } ?>
}


function SetBlcRange(direction, value)
{	
	var MIN_BLC_HEIGHT_LENGTH = 40;
	var MIN_BLC_WIDTH_LENGTH = 30;
	var MAX_BLC_LENGTH = 60;
	
	if(direction == "blc_top") { 
		if(value + MAX_BLC_LENGTH <= 100){
			$("#blc_bottom").slider("option", "limitMax", value + MAX_BLC_LENGTH);
		}
		else {
			$("#blc_bottom").slider("option", "limitMax", 100);
		}
		if(value + MIN_BLC_HEIGHT_LENGTH >= 40){
			$("#blc_bottom").slider("option", "limitMin", value + MIN_BLC_HEIGHT_LENGTH);
		}
		else {
			$("#blc_bottom").slider("option", "limitMin", 40);
		}
		$("#blc_bottom").slider("option", "value", parseInt($("#blc_bottom_value").text(), 10));
	} 
	else if(direction == "blc_bottom") {
		if(value - MIN_BLC_HEIGHT_LENGTH <= 60 ){
			$("#blc_top").slider("option", "limitMax", value - MIN_BLC_HEIGHT_LENGTH);
		}
		else {
			$("#blc_top").slider("option", "limitMax", 60);
		}
		if(value - MAX_BLC_LENGTH > 0) {
			$("#blc_top").slider("option", "limitMin", value - MAX_BLC_LENGTH);
		}
		else{
			$("#blc_top").slider("option", "limitMin", 1);
		}
		$("#blc_top").slider("option", "value", parseInt($("#blc_top_value").text(), 10));
	} 
	else if(direction == "blc_left") {
		if(value + MAX_BLC_LENGTH <= 100){
			$("#blc_right").slider("option", "limitMax", value + MAX_BLC_LENGTH);
		}
		else {
			$("#blc_right").slider("option", "limitMax", 100);
		}
		if(value + MIN_BLC_WIDTH_LENGTH >= 30){			
			$("#blc_right").slider("option", "limitMin", value + MIN_BLC_WIDTH_LENGTH);
		}
		else {
			$("#blc_right").slider("option", "limitMin", 30);
		}
		$("#blc_right").slider("option", "value", parseInt($("#blc_right_value").text(), 10));
	} 
	else {
		if(value - MIN_BLC_WIDTH_LENGTH <= 70 ){
			$("#blc_left").slider("option", "limitMax", value - MIN_BLC_WIDTH_LENGTH);
		}
		else {
			$("#blc_left").slider("option", "limitMax", 70);
		}
		if(value - MAX_BLC_LENGTH > 0) {
			$("#blc_left").slider("option", "limitMin", value - MAX_BLC_LENGTH);
		}
		else{
			$("#blc_left").slider("option", "limitMin", 1);
		}
		$("#blc_left").slider("option", "value", parseInt($("#blc_left_value").text(), 10));
	}
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

</script>

<table class="data_write mgt10 mgl-20 pdl15" style="width:670px;">
	<colgroup>
		<col style="width:180px;"/>
		<col style="width:30px;"/>
		<col style="width:150px;"/>
		<col style="width:30px;"/>
		<col />
	</colgroup>
	<tbody>
		<tr>
			<th class="top_txt"><?php echo $t_mode[$GLOBALS["LANGINDEX"]]; ?></th>
			<td colspan='4'>
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
			<td colspan='4'>
				<select id="hlc_level" class="selectbox_style_wid230" onchange="SetTimeOut()">
					<option value="0" <?php if ($imageBackLight->dataInfo["HLCLevel"]["value"] == 0) echo "selected=\"selected\""; ?>><?php echo $t_low[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="1" <?php if ($imageBackLight->dataInfo["HLCLevel"]["value"] == 1) echo "selected=\"selected\""; ?>><?php echo $t_middle[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="2" <?php if ($imageBackLight->dataInfo["HLCLevel"]["value"] == 2) echo "selected=\"selected\""; ?>><?php echo $t_high[$GLOBALS["LANGINDEX"]]; ?></option>
				</select>
			</td>
		</tr>
		<tr>
			<th class="top_txt"><?php echo $t_masktone[$GLOBALS["LANGINDEX"]]; ?></th>
			<td colspan='4'>
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
			<td colspan='4'>
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
			<td colspan='4'>
				<select id="blc_level" class="selectbox_style_wid230" onchange="SetTimeOut()">
					<option value="0" <?php if ($imageBackLight->dataInfo["BLCLevel"]["value"] == 0) echo "selected=\"selected\""; ?>><?php echo $t_low[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="1" <?php if ($imageBackLight->dataInfo["BLCLevel"]["value"] == 1) echo "selected=\"selected\""; ?>><?php echo $t_middle[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="2" <?php if ($imageBackLight->dataInfo["BLCLevel"]["value"] == 2) echo "selected=\"selected\""; ?>><?php echo $t_high[$GLOBALS["LANGINDEX"]]; ?></option>
				</select>
			</td>
		</tr>	
		<tr>
			<th class="top_txt"><?php echo $t_top[$GLOBALS["LANGINDEX"]]; ?></th>
			<td>	
				<img id="blc_top_left" src="../images/common/btn/slider_-_normal.png" />	
			</td>
			<td style="padding-right:4px;">
				<div id="blc_top" class="slider_style_wid150"></div>
			</td>
			<td>
				<img id="blc_top_right" src="../images/common/btn/slider_+_normal.png" /> 
			</td>
			<td>
				<label id="blc_top_value"></label>
			</td>
		</tr>		
		<tr>
			<th class="top_txt"><?php echo $t_bottom[$GLOBALS["LANGINDEX"]]; ?></th>
			<td>
				<img id="blc_bottom_left" src="../images/common/btn/slider_-_normal.png" />
			</td>
			<td>
				<div id="blc_bottom" class="slider_style_wid150"></div>
			</td>
			<td>	
				<img id="blc_bottom_right" src="../images/common/btn/slider_+_normal.png" />
			</td>
			<td>
				<label id="blc_bottom_value"></label>
			</td>
		</tr>
		<tr>
			<th class="top_txt"><?php echo $t_left[$GLOBALS["LANGINDEX"]]; ?></th>
			<td>
				<img id="blc_left_left" src="../images/common/btn/slider_-_normal.png" />
			</td>
			<td>
				<div id="blc_left" class="slider_style_wid150"></div>
			</td>
			<td>			
				<img id="blc_left_right" src="../images/common/btn/slider_+_normal.png" />
			</td>
			<td>
				<label id="blc_left_value"></label>
			</td>
		</tr>
		<tr>
			<th class="top_txt"><?php echo $t_right[$GLOBALS["LANGINDEX"]]; ?></th>
			<td>		
				<img id="blc_right_left" src="../images/common/btn/slider_-_normal.png" />
			</td>
			<td>
				<div id="blc_right" class="slider_style_wid150"></div>
			</td>
			<td>
				<img id="blc_right_right" src="../images/common/btn/slider_+_normal.png" />
			</td>
			<td>
				<label id="blc_right_value"></label>
			</td>
		</tr>	
	</tbody>
</table>
