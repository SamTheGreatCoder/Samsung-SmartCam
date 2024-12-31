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
	msg += MakeTitleOsdXml();
	msg += MakeDayNightXml();
  	msg += "<SharpnessMode>" + $("#sharpness_mode").val() + "</SharpnessMode>";
  	msg += "<SharpnessLevel>" + $("#sharpness_level").val() + "</SharpnessLevel>";
  	msg += "<Gamma>" + $("#gamma").val() + "</Gamma>";
  	msg += "<ColorLevel>" + $("#color_level").slider("option","value") + "</ColorLevel>";
  	<?php if($GLOBALS['M_SUPPORT_DEFOG']) { ?>
  	msg += "<Defog>" + $("#defog").val() + "</Defog>";
  	msg += "<DefogLevel>" + $("#defog_level").slider("option","value") + "</DefogLevel>";
  	<?php } ?>
	<?php if ($GLOBALS['M_SUPPORT_DIS']) { ?>
  	msg += "<DIS>" + $("#dis").val() + "</DIS>";
	<?php } ?>  	
  	<?php if($GLOBALS['M_SPECIAL_TYPE'] == 2) { ?>
  	msg += "<CAR>" + $("#car").val() + "</CAR>";
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

<?php  
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
				<select id="dis"	class="selectbox_style_wid230" onchange="OnChangeSpecial()">
					<option value="0" <?php if ($imageSpecial->dataInfo["DIS"]["value"] == 0) echo "selected=\"selected\""; ?>><?php echo $t_off[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="1" <?php if ($imageSpecial->dataInfo["DIS"]["value"] == 1) echo "selected=\"selected\""; ?>><?php echo $t_on[$GLOBALS["LANGINDEX"]]; ?></option>
				</select>
			</td>
		</tr>
<?php } ?>
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
			<th class="top_txt"><?php echo $t_gammavalue[$GLOBALS["LANGINDEX"]]; ?></th>
			<td colspan="3">
				<select id="gamma"  class="selectbox_style_wid230" onchange="OnChangeSpecial()">
					<?php for($i = 0.20,$count = 0; $i < 1.05; $i += 0.05 ){ ?>
					<option value="<?php echo $count ?>" <?php if ($imageSpecial->dataInfo["Gamma"]["value"] == $count) echo "selected=\"selected\""; ?>><?php echo $i ?></option>
					<?php $count++;} ?>
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
			<?php
				if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3) {
			?>
					<option value="0" <?php if ($imageSpecial->dataInfo["Defog"]["value"] == 0) echo "selected=\"selected\""; ?>><?php echo $t_off[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="1" <?php if ($imageSpecial->dataInfo["Defog"]["value"] == 1) echo "selected=\"selected\""; ?>><?php echo $t_auto[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="2" <?php if ($imageSpecial->dataInfo["Defog"]["value"] == 2) echo "selected=\"selected\""; ?>><?php echo $t_manual[$GLOBALS["LANGINDEX"]]; ?></option>
			<?php 
				}
				else {
			?>
					<option value="0" <?php if ($imageSpecial->dataInfo["Defog"]["value"] == 0) echo "selected=\"selected\""; ?>><?php echo $t_off[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="1" <?php if ($imageSpecial->dataInfo["Defog"]["value"] == 1) echo "selected=\"selected\""; ?>><?php echo $t_low[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="2" <?php if ($imageSpecial->dataInfo["Defog"]["value"] == 2) echo "selected=\"selected\""; ?>><?php echo $t_middle[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="3" <?php if ($imageSpecial->dataInfo["Defog"]["value"] == 3) echo "selected=\"selected\""; ?>><?php echo $t_high[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="4" <?php if ($imageSpecial->dataInfo["Defog"]["value"] == 4) echo "selected=\"selected\""; ?>><?php echo $t_auto[$GLOBALS["LANGINDEX"]]; ?></option>
			<?php
				}
			?>
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
	
	if($GLOBALS['M_SPECIAL_TYPE'] == 2) { ?>
		<tr>
			<th class="top_txt"><?php echo $t_car[$GLOBALS["LANGINDEX"]]; ?></th>
			<td colspan="3">
				<select id="car" class="selectbox_style_wid230" onchange="SetTimeOut()">
					<option value="0" <?php if ($imageSpecial->dataInfo["CAR"]["value"] == 0) echo "selected=\"selected\""; ?>><?php echo $t_off[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="1" <?php if ($imageSpecial->dataInfo["CAR"]["value"] == 1) echo "selected=\"selected\""; ?>><?php echo $t_low[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="2" <?php if ($imageSpecial->dataInfo["CAR"]["value"] == 2) echo "selected=\"selected\""; ?>><?php echo $t_medium[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="3" <?php if ($imageSpecial->dataInfo["CAR"]["value"] == 3) echo "selected=\"selected\""; ?>><?php echo $t_high[$GLOBALS["LANGINDEX"]]; ?></option>
				</select>
			</td>
		</tr>
<?php } ?>
	</tbody>
</table>
