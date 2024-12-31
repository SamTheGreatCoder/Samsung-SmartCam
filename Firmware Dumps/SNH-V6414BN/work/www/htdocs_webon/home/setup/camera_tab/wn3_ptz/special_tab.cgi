<script type="text/javascript" language="javascript">

$(document).ready(function(){
<?php
	$sliderlist = array( "color_level"=>array(1,100,$imageSpecial->dataInfo["ColorLevel"]["value"]),
								"defog_level"=>array(1,10,$imageSpecial->dataInfo["DefogLevel"]["value"]));
	foreach ($sliderlist as $name=>$data) {
?>
		InitCameraSetupSlider("<?php echo $name; ?>", <?php echo $data[0]; ?>, <?php echo $data[1]; ?>, <?php echo $data[2]; ?>);
<?php
	}
?>
});

function MakeSpecialXml()
{
	var msg = "";
	msg += "<ImageSpecial>";
  	msg += "<DayNightMode>" + $("#day_night").val() + "</DayNightMode>";
  	msg += "<DayNightDwellTime>" + $("#dwell_time").val() + "</DayNightDwellTime>";
  	msg += "<DayNightDuration>" + $("#duration").val() + "</DayNightDuration>";
  	msg += "<SharpnessMode>" + $("#sharpness_mode").val() + "</SharpnessMode>";
<?php if($GLOBALS['M_ALARMIN_COUNT'] > 0 ) { ?>
	msg += "<DayNightExtMode>" + $("#alarm_in").val() + "</DayNightExtMode>";
<?php } ?>
  	msg += "<SharpnessLevel>" + $("#sharpness_level").val() + "</SharpnessLevel>";
	if (currentCameraSetupType == 'global') {
		msg += MakeTitleOsdXml();
		msg += MakePtzPositionXml();
	}	
  	msg += "<ColorLevel>" + $("#color_level").slider("option","value") + "</ColorLevel>";
  	<?php if($GLOBALS['M_SUPPORT_DEFOG']) { ?>
  	msg += "<Defog>" + $("#defog").val() + "</Defog>";
  	msg += "<DefogLevel>" + $("#defog_level").slider("option","value") + "</DefogLevel>";
  	<?php } ?>
	<?php if ($GLOBALS['M_SUPPORT_DIS']) { ?>
  	msg += "<DIS>" + $("#dis").val() + "</DIS>";
	<?php } ?>
  	msg += "</ImageSpecial>";
  	
	return msg;
}

function OnChangeSpecial()
{
	if ($("#sharpness_mode").val() == 1) {
		$("#sharpness_level").removeAttr("disabled");
	}
	else {
		$("#sharpness_level").attr("disabled", "disabled");
	}

	oldDN = $("#day_night").val();
	if ($("#day_night").val() == 2) {
		$("#dwell_time").removeAttr("disabled");
		$("#duration").removeAttr("disabled");
	}
	else {
		$("#dwell_time").attr("disabled", "disabled");
		$("#duration").attr("disabled", "disabled");
	}
	
<?php
	if ($GLOBALS['M_SUPPORT_DIS']) {
?>
		if(currentCameraSetupType == 'global'){
			if(TAMPERING_ENABLE == 1 || MD_ENABLE == 1 || IV_ENABLE == 1) {
				$("#dis").attr("disabled", "disabled");
			}
			else{
				$("#dis").removeAttr("disabled");			
			}
		}else{
			if(TAMPERING_ENABLE == 1 || currentAfterActionValue == 3){
				$("#dis").attr("disabled", "disabled");
			}
			else{
				$("#dis").removeAttr("disabled");
			}
		}
		OnChangeDigitalZoom();
<?php 
	} 
	
	if ($GLOBALS['M_SUPPORT_DEFOG']) {
?>
		var isDisable = false;
		if($("#defog").val() == 0) isDisable = true;

		SetButtonHoverFunction(isDisable, 'defog_level_left');
		SetButtonHoverFunction(isDisable, 'defog_level_right');
		$("#defog_level").slider("option","disabled",isDisable);
<?php 
	}
?>

	SetTimeOut();
}

function ParsingXML_ImageSpecial(xmlData)
{	
	$("#day_night").val(xmlData.find('DayNightMode').text());
	oldDN = $("#day_night").val();
	$("#dwell_time").val(xmlData.find('DayNightDwellTime').text());
	$("#duration").val(xmlData.find('DayNightDuration').text());
	$("#sharpness_mode").val(xmlData.find('SharpnessMode').text());
	$("#sharpness_level").val(xmlData.find('SharpnessLevel').text());
	$("#color_level").slider("option","value", xmlData.find('ColorLevel').text());
	$("#color_level_value").html(xmlData.find('ColorLevel').text());
<?php
	if ($GLOBALS['M_SUPPORT_DIS']) {
?>
		$("#dis").val(xmlData.find('DIS').text());
<?php
	}

	if ($GLOBALS['M_SUPPORT_DEFOG']) { 
?>
		$("#defog").val(xmlData.find('Defog').text());
		$("#defog_level").slider("option","value",xmlData.find('DefogLevel').text());
		$("#defog_level_value").html(xmlData.find('DefogLevel').text());
<?php 
	}
?>
	if (currentCameraSetupType == 'global') {
		$("#camera_title").val(xmlData.find('CamTitle').text());
		$("#title_pos_x").slider("option","value", parseInt(xmlData.find('CamTitlePosX').text()));
		$("#title_pos_x_value").html(xmlData.find('CamTitlePosX').text());
		$("#title_pos_y").slider("option","value", parseInt(xmlData.find('CamTitlePosY').text()));
		$("#title_pos_y_value").html(xmlData.find('CamTitlePosY').text());
		$("#ptzposition_display").prop("checked", (xmlData.find('PTZPositionDisplay').text()==1?true:false));
	}
	else {
		currentAfterActionValue = parseInt(xmlData.find('AfterAction').text());
	}
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
<?php
	if ($GLOBALS['M_SUPPORT_DIS']) {
?>	
		<tr>
			<th class="top_txt"><?php echo $t_dis[$GLOBALS["LANGINDEX"]]; ?></th>
			<td colspan="3">
				<select id="dis"	class="selectbox_style_wid230" onchange="OnChangeSpecial();">
					<option value="0" <?php if ($imageSpecial->dataInfo["DIS"]["value"] == 0) echo "selected=\"selected\""; ?>><?php echo $t_off[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="1" <?php if ($imageSpecial->dataInfo["DIS"]["value"] == 1) echo "selected=\"selected\""; ?>><?php echo $t_on[$GLOBALS["LANGINDEX"]]; ?></option>
				</select>
			</td>
		</tr>
<?php } ?>
		<tr>
			<th class="top_txt"><?php echo $t_daynight[$GLOBALS["LANGINDEX"]]; ?></th>
			<td colspan="3">
				<select id="day_night" class="selectbox_style_wid230" onchange="OnChangeSpecial()">
					<option value="0" <?php if ($imageSpecial->dataInfo["DayNightMode"]["value"] == 0) echo "selected=\"selected\""; ?>><?php echo $t_color[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="1" <?php if ($imageSpecial->dataInfo["DayNightMode"]["value"] == 1) echo "selected=\"selected\""; ?>><?php echo $t_bw[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="2" <?php if ($imageSpecial->dataInfo["DayNightMode"]["value"] == 2) echo "selected=\"selected\""; ?>><?php echo $t_auto[$GLOBALS["LANGINDEX"]]; ?></option>
				</select>
			</td>
		</tr>
		<tr>
			<th class="top_txt"><?php echo $t_dwelltime[$GLOBALS["LANGINDEX"]]; ?></th>
			<td colspan="3">
				<select id="dwell_time"  class="selectbox_style_wid230" onchange="OnChangeSpecial()">
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
			<td colspan="3">
				<select id="duration"  class="selectbox_style_wid230" onchange="OnChangeSpecial()">
					<option value="0" <?php if ($imageSpecial->dataInfo["DayNightDuration"]["value"] == 0) echo "selected=\"selected\""; ?>><?php echo $t_veryfast[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="1" <?php if ($imageSpecial->dataInfo["DayNightDuration"]["value"] == 1) echo "selected=\"selected\""; ?>><?php echo $t_fast[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="2" <?php if ($imageSpecial->dataInfo["DayNightDuration"]["value"] == 2) echo "selected=\"selected\""; ?>><?php echo $t_normal[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="3" <?php if ($imageSpecial->dataInfo["DayNightDuration"]["value"] == 3) echo "selected=\"selected\""; ?>><?php echo $t_slow[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="4" <?php if ($imageSpecial->dataInfo["DayNightDuration"]["value"] == 4) echo "selected=\"selected\""; ?>><?php echo $t_veryslow[$GLOBALS["LANGINDEX"]]; ?></option>
				</select>
			</td>
		</tr>
		<tr>
			<th class="top_txt"><?php echo $t_sharpness[$GLOBALS["LANGINDEX"]]; ?></th>
			<td colspan="3">
				<select id="sharpness_mode"  class="selectbox_style_wid230" onchange="OnChangeSpecial()">
					<option value="0" <?php if ($imageSpecial->dataInfo["SharpnessMode"]["value"] == 0) echo "selected=\"selected\""; ?>><?php echo $t_off[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="1" <?php if ($imageSpecial->dataInfo["SharpnessMode"]["value"] == 1) echo "selected=\"selected\""; ?>><?php echo $t_on[$GLOBALS["LANGINDEX"]]; ?></option>
				</select>
			</td>
		</tr>
		<tr>
			<th class="top_txt"><?php echo $t_sharpnesslevel[$GLOBALS["LANGINDEX"]]; ?></th>
			<td colspan="3">
				<select id="sharpness_level"	class="selectbox_style_wid230" onchange="OnChangeSpecial()">
					<?php 
					$max_sharpness = 32;
					for($i=1; $i<=$max_sharpness; $i++){ ?>
					<option value="<?php echo $i ?>" <?php if ($imageSpecial->dataInfo["SharpnessLevel"]["value"] == $i) echo "selected=\"selected\""; ?>><?php echo $i ?></option>
					<?php } ?>
				</select>
			</td>
		</tr>
		<tr>
			<th class="top_txt"><?php echo $t_colorlevel[$GLOBALS["LANGINDEX"]]; ?></th>
			<td>
				<img id="color_level_left" src="../images/common/btn/slider_-_normal.png" onclick="ControlSlider('color_level','left')"
					onMouseOver="ChangeImage('color_level_left','../images/common/btn/slider_-_press.png');" 
					onMouseOut="ChangeImage('color_level_left','../images/common/btn/slider_-_normal.png');"/>
			</td>
			<td style="padding-right:4px;">
				<div id="color_level" class="slider_style_wid163"></div>
			</td>
			<td>
				<img id="color_level_right" src="../images/common/btn/slider_+_normal.png" onclick="ControlSlider('color_level','right')"
					onMouseOver="ChangeImage('color_level_right','../images/common/btn/slider_+_press.png');" 
					onMouseOut="ChangeImage('color_level_right','../images/common/btn/slider_+_normal.png');"/>
			</td>
			<td>
				<label id="color_level_value"></label>
			</td>
		</tr>
<?php if ($GLOBALS['M_SUPPORT_DEFOG']) { ?>
		<tr>
			<th class="top_txt"><?php echo $t_defog[$GLOBALS["LANGINDEX"]]; ?></th>
			<td colspan="3">	
				<select id="defog"  class="selectbox_style_wid230" onchange="OnChangeSpecial()">
					<option value="0" <?php if ($imageSpecial->dataInfo["Defog"]["value"] == 0) echo "selected=\"selected\""; ?>><?php echo $t_off[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="1" <?php if ($imageSpecial->dataInfo["Defog"]["value"] == 1) echo "selected=\"selected\""; ?>><?php echo $t_auto[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="2" <?php if ($imageSpecial->dataInfo["Defog"]["value"] == 2) echo "selected=\"selected\""; ?>><?php echo $t_manual[$GLOBALS["LANGINDEX"]]; ?></option>
				</select>
			</td>
		</tr>
		<tr>
			<th class="top_txt"><?php echo $t_defoglevel[$GLOBALS["LANGINDEX"]]; ?></th>
			<td>
				<img id="defog_level_left" src="../images/common/btn/slider_-_normal.png"/>
			</td>
			<td style="padding-right:4px;">
				<div id="defog_level" class="slider_style_wid163"></div>
			</td>
			<td>
				<img id="defog_level_right" src="../images/common/btn/slider_+_normal.png"/>
			</td>
			<td>
				<label id="defog_level_value"></label>
			</td>
		</tr>
<?php 
	}
?>
	</tbody>
</table>
