<script type="text/javascript" language="javascript">

$(document).ready(function(){
	<?php if($GLOBALS['M_ISP_TYPE'] != ISP_TYPE_HISILICON) { ?>
		<?php
			$sliderlist = array( "ir_level"=>array(1,99,$imageIR->dataInfo["Level"]["value"]));
			foreach ($sliderlist as $name=>$data) {
		?>
				InitCameraSetupSlider("<?php echo $name; ?>", <?php echo $data[0]; ?>, <?php echo $data[1]; ?>, <?php echo $data[2]; ?>);
		<?php
			}
		?>
	<?php } ?>
});

function MakeIrXml()
{
	var msg = "";
	msg += "<ImageIR>";
	msg += "<Mode>" + $("#ir_mode").val() + "</Mode>";
	<?php if($GLOBALS['M_ISP_TYPE'] != ISP_TYPE_HISILICON) { ?>
	msg += "<Level>" + $("#ir_level").slider("option","value") + "</Level>";
	<?php } ?>
	msg += "</ImageIR>";
	
	return msg;
}

function OnChangeIR()
{
	<?php if($GLOBALS['M_ISP_TYPE'] != ISP_TYPE_HISILICON) { ?>
		if($("#ir_mode").val() == 2)
		{
			SetButtonHoverFunction(false, 'ir_level_left');
			SetButtonHoverFunction(false, 'ir_level_right');
			$("#ir_level").slider("option", "disabled", false);
		}
		else
		{
			SetButtonHoverFunction(true, 'ir_level_left');
			SetButtonHoverFunction(true, 'ir_level_right');
			$("#ir_level").slider("option", "disabled", true);
		}
	<?php } ?>
	SetTimeOut();
}

</script>
<table class="data_write mgt10 mgl-20 pdl15" style="width:670px;">
	<colgroup>
		<?php if($GLOBALS['M_ISP_TYPE'] != ISP_TYPE_HISILICON) { ?>
			<col style="width:180px;"/>
			<col style="width:30px;"/>
			<col style="width:150px;"/>
			<col style="width:30px;"/>
			<col />
		<?php } else { ?>
			<col style="width:180px;"/>
			<col></col>
		<?php } ?>
	</colgroup>
	<tbody>
		<tr>
			<th class="top_txt"><?php echo $t_mode[$GLOBALS["LANGINDEX"]]; ?></th>
			<td colspan="4">
				<select id="ir_mode"  class="selectbox_style_wid230" onchange="OnChangeIR()">
					<option value="0" <?php if ($imageIR->dataInfo["Mode"]["value"] == 0) echo "selected=\"selected\""; ?>><?php echo $t_off[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="1" <?php if ($imageIR->dataInfo["Mode"]["value"] == 1) echo "selected=\"selected\""; ?>><?php echo $t_auto[$GLOBALS["LANGINDEX"]]; ?></option>
					<?php if($GLOBALS['M_ISP_TYPE'] != ISP_TYPE_HISILICON) { ?>
					<option value="2" <?php if ($imageIR->dataInfo["Mode"]["value"] == 2) echo "selected=\"selected\""; ?>><?php echo $t_manual[$GLOBALS["LANGINDEX"]]; ?></option>
					<?php } ?>
				</select>
			</td>
		</tr>
		<?php if($GLOBALS['M_ISP_TYPE'] != ISP_TYPE_HISILICON) { ?>
		<tr>
			<th class="top_txt"><?php echo $t_level[$GLOBALS["LANGINDEX"]]; ?></th>
			<td>
				<img id="ir_level_left" src="../images/common/btn/slider_-_normal.png" />
			</td>
			<td>
				<div id="ir_level" class="slider_style_wid150"></div>
			</td>
			<td>
				<img id="ir_level_right" src="../images/common/btn/slider_+_normal.png" />
			</td>
			<td>
				<label id="ir_level_value"></label>
			</td>
		</tr>	
		<?php } ?>
	</tbody>
</table>
