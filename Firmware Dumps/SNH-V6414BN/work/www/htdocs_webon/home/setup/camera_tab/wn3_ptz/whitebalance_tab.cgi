<script type="text/javascript" language="javascript">

$(document).ready(function(){
<?php
	$sliderlist = array( "red_gain"=>array(1,2048,$imageWhiteBalance->dataInfo["Red"]["value"]),
								"blue_gain"=>array(1,2048,$imageWhiteBalance->dataInfo["Blue"]["value"]));
	foreach ($sliderlist as $name=>$data) {
?>
		InitCameraSetupSlider("<?php echo $name; ?>", <?php echo $data[0]; ?>, <?php echo $data[1]; ?>, <?php echo $data[2]; ?>);
<?php
	}
?>
});

function MakeWhitebalanceXml()
{
	var msg = "";
	msg += "<ImageWhiteBalance>";
	msg += "<Mode>" + $("#wb_mode").val() +"</Mode>";
	msg += "<Red>" + $("#red_gain").slider("option","value") + "</Red>";
	msg += "<Blue>" + $("#blue_gain").slider("option","value") + "</Blue>";
	msg += "</ImageWhiteBalance>";
	return msg;
}

function OnChangeWhitebalnaceMode()
{	
	if($("#wb_mode").val() == 1){
		if(currentCameraSetupType == 'global'){
			$("#awc_btn").removeClass("btn_setup");
			$("#awc_btn").attr('class', 'btn_setup_disable');
			$("#awc_btn").unbind('click');
		}
		isDisable = false;
	}
	else if($("#wb_mode").val() == 2){	// AWC
		if(currentCameraSetupType == 'global'){
			$("#awc_btn").removeClass("btn_setup_disable");
			$("#awc_btn").attr('class', 'btn_setup');
			$("#awc_btn").bind("click", OnClickAWCSet);
		}
		isDisable = true;
	}
	else{
		if(currentCameraSetupType == 'global'){
			$("#awc_btn").removeClass("btn_setup");
			$("#awc_btn").attr('class', 'btn_setup_disable');
			$("#awc_btn").unbind('click');
		}
		isDisable = true;
	}
	
	SetButtonHoverFunction(isDisable, 'red_gain_left');
	SetButtonHoverFunction(isDisable, 'red_gain_right');
	SetButtonHoverFunction(isDisable, 'blue_gain_left');
	SetButtonHoverFunction(isDisable, 'blue_gain_right');
	$("#red_gain").slider("option","disabled",isDisable);
	$("#blue_gain").slider("option","disabled",isDisable);
	SetTimeOut();
}

function OnClickAWCSet()
{
	var msg = "";
	msg += "<StartImageSetting>";
	msg += "<VideoSourceIndex>0</VideoSourceIndex>";
	msg += "<AWC>1</AWC>";
	msg += "</StartImageSetting>";
	clearTimeout(timer);
	RequestAjaxMsg(msg, "<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>", ajaxReqUrl, "NO_REFRESH", true);
}

function ParsingXML_ImageWhiteBalance(xmlData)
{
	if (currentCameraSetupType == 'global') {
		$('#wb_mode').children().remove();
		$('#wb_mode').append(
			"<option value=\"0\"><?php echo $t_atw[$GLOBALS['LANGINDEX']]; ?></option>\
			<option value=\"1\"><?php echo $t_manual[$GLOBALS['LANGINDEX']]; ?></option>\
			<option value=\"2\"><?php echo $t_awc[$GLOBALS['LANGINDEX']]; ?></option>\
			<option value=\"3\"><?php echo $t_outdoor[$GLOBALS['LANGINDEX']]; ?></option>\
			<option value=\"4\"><?php echo $t_indoor[$GLOBALS['LANGINDEX']]; ?></option>\
			<option value=\"5\"><?php echo 'MERCURY'; ?></option>"
		);
		$('#awc_btn').show();
	}
	else {
		$('#wb_mode').children().remove();
		$('#wb_mode').append(
			"<option value=\"0\"><?php echo $t_atw[$GLOBALS['LANGINDEX']]; ?></option>\
			<option value=\"1\"><?php echo $t_manual[$GLOBALS['LANGINDEX']]; ?></option>\
			<option value=\"3\"><?php echo $t_outdoor[$GLOBALS['LANGINDEX']]; ?></option>\
			<option value=\"4\"><?php echo $t_indoor[$GLOBALS['LANGINDEX']]; ?></option>\
			<option value=\"5\"><?php echo 'MERCURY'; ?></option>"
		);
		$('#awc_btn').hide();
	}
	$("#wb_mode").val(xmlData.find('Mode').text());
	$("#red_gain").slider("option","value", parseInt(xmlData.find('Red').text()));
	$("#red_gain_value").html(xmlData.find('Red').text());
	$("#blue_gain").slider("option","value", parseInt(xmlData.find('Blue').text()));
	$("#blue_gain_value").html(xmlData.find('Blue').text());	
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
			<td colspan="3">
				<select id="wb_mode"  class="selectbox_style_wid230" onchange="OnChangeWhitebalnaceMode()">
					<option value="0" <?php if ($imageWhiteBalance->dataInfo["Mode"]["value"] == 0) echo "selected=\"selected\""; ?>><?php echo $t_atw[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="1" <?php if ($imageWhiteBalance->dataInfo["Mode"]["value"] == 1) echo "selected=\"selected\""; ?>><?php echo $t_manual[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="2" <?php if ($imageWhiteBalance->dataInfo["Mode"]["value"] == 2) echo "selected=\"selected\""; ?>><?php echo $t_awc[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="3" <?php if ($imageWhiteBalance->dataInfo["Mode"]["value"] == 3) echo "selected=\"selected\""; ?>><?php echo $t_outdoor[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="4" <?php if ($imageWhiteBalance->dataInfo["Mode"]["value"] == 4) echo "selected=\"selected\""; ?>><?php echo $t_indoor[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="5" <?php if ($imageWhiteBalance->dataInfo["Mode"]["value"] == 5) echo "selected=\"selected\""; ?>><?php echo "MERCURY"; ?></option>
				</select>
			</td>
			<td>	
				<a class="btn_setup_disable" id ="awc_btn" type="button"> <?php echo $t_set[$GLOBALS['LANGINDEX']]; ?> </a>
			</td>
		</tr>
		<tr>
			<th class="top_txt"><?php echo $t_redgain[$GLOBALS["LANGINDEX"]]; ?></th>
			<td>
				<img id="red_gain_left" src="../images/common/btn/slider_-_normal.png" />	
			</td>
			<td style="padding-right:4px;">
				<div id="red_gain" class="slider_style_wid163"></div>
			</td>
			<td>
				<img id="red_gain_right" src="../images/common/btn/slider_+_normal.png" />	
			</td>
			<td>
				<label id="red_gain_value"></label>
			</td>
		</tr>
		<tr>
			<th class="top_txt"><?php echo $t_bluegain[$GLOBALS["LANGINDEX"]]; ?></th>
			<td>
				<img id="blue_gain_left" src="../images/common/btn/slider_-_normal.png" />
			</td>
			<td style="padding-right:4px;">
				<div id="blue_gain" class="slider_style_wid163"></div>
			</td>
			<td>
				<img id="blue_gain_right" src="../images/common/btn/slider_+_normal.png" />
			</td>
			<td>
				<label id="blue_gain_value"></label>
			</td>
		</tr>
	</tbody>
</table>
