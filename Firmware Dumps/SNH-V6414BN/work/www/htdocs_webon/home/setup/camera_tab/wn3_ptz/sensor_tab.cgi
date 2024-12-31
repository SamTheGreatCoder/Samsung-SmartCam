<script type="text/javascript" language="javascript">

function MakeSensorXml()
{
	var msg = "";
	msg += "<ImageExposure>";
	msg += "<SensorFrameMode>" + $("#sensor_mode").val() + "</SensorFrameMode>";		//sensor_tab.cgi
	msg += "</ImageExposure>";
	return msg;
}

function OnChangeSensorMode()
{
	SENSOR_MODE = parseInt($("#sensor_mode").val());

	if ($("#sensor_mode").val() == 0 || $("#sensor_mode").val() == 1) {		
		ChangeOption('blc_mode', 3, 'Disable');
	}
	else {
		if($("#blc_mode").val() != 3) {
			ChangeOption('blc_mode', 3, 'Enable');
		}
	}
	SetTimeOut();
	if(!isOnloading){
		$("#sensor_mode").attr("disabled","disabled");
		setTimeout(function(){
			$("#sensor_mode").removeAttr("disabled");	
		},10000);
	}
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
			<select id="sensor_mode"  class="selectbox_style_wid230" onchange="OnChangeSensorMode()">
				<?php if($GLOBALS['M_MAX_SERSORFRAME'] == 60) { ?>
				<option value="0" <?php if ($imageExposure->dataInfo["SensorFrameMode"]["value"] == 0) echo "selected=\"selected\""; ?>>60 fps</option>
				<option value="1" <?php if ($imageExposure->dataInfo["SensorFrameMode"]["value"] == 1) echo "selected=\"selected\""; ?>>50 fps</option>
				<?php } ?>
				<option value="2" <?php if ($imageExposure->dataInfo["SensorFrameMode"]["value"] == 2) echo "selected=\"selected\""; ?>>30 fps</option>
				<option value="3" <?php if ($imageExposure->dataInfo["SensorFrameMode"]["value"] == 3) echo "selected=\"selected\""; ?>>25 fps</option>
			</select>
		</td>
		</tr>
	</tbody>
</table>
<div style="margin-top:30px; color:#fff; width:640px; font:12px/18px Verdana, sans-serif"> <?php echo $msg_sensorchange[$GLOBALS["LANGINDEX"]]; ?> </div>
