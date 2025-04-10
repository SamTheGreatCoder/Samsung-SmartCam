<script type="text/javascript" language="javascript">

$(document).ready(function(){
<?php
	$max_camtitle_pos_x = 50;
	$max_camtitle_pos_y = 17;
	//if ($GLOBALS["LANGINDEX"] == 2) {	
	//	$max_time_pos_x = $titlePosX-19;
	//}
	//else {
	$max_time_pos_x = $max_camtitle_pos_x-18;
	//}

	$sliderlist = array( "title_pos_x"	=>array(0,$max_camtitle_pos_x,	$imageSpecial->dataInfo["CamTitlePosX"]["value"]),
								"title_pos_y"	=>array(0,$max_camtitle_pos_y,	$imageSpecial->dataInfo["CamTitlePosY"]["value"]), 
								"time_pos_x"	=>array(0,$max_time_pos_x,		$imageOSD->dataInfo["DatePosX"]["value"]),
								"time_pos_y"	=>array(0,$max_camtitle_pos_y,	$imageOSD->dataInfo["DatePosY"]["value"]));
	foreach ($sliderlist as $name=>$data) {
?>
		InitCameraSetupSlider("<?php echo $name; ?>", <?php echo $data[0]; ?>, <?php echo $data[1]; ?>, <?php echo $data[2]; ?>);
<?php
	}
?>
	<?php if($GLOBALS["M_SUPPORT_AZIMUTH"]) { ?>
		$("#camera_tabs").tabs({
			activate:function(event, ui){
				var index = $("#camera_tabs").tabs("option","active");
				if(ui.newTab.find("a").attr("href") == "#tabs-osd"){
					$("#azimuthArea").show();
				}else{
					$("#azimuthArea").hide();
				}
			}
		});
	<?php } ?>
});

function MakeOsdXml()
{
	var msg = "";
	msg += "<ImageOSD>";
	msg += "<DispDate>" + ($("#time_display").is(':checked')?1:0) + "</DispDate>";
	msg += "<DateFormat>" + $("#date_notation").val() + "</DateFormat>";
	msg += "<DatePosX>" + $("#time_pos_x").slider("option","value") + "</DatePosX>";
	msg += "<DatePosY>" + $("#time_pos_y").slider("option","value") + "</DatePosY>";
	msg += "<TimeFormat>1</TimeFormat>";
	msg += "<DispWeekday>" + ($("#weekday_display").is(':checked')?1:0) + "</DispWeekday>";
	msg += "<PresetNameDisplay>" + ($("#presetname_display").is(':checked')?1:0) + "</PresetNameDisplay>";
	msg += "<CamIDMode>" + ($("#cameraid_display").is(':checked')?1:0) + "</CamIDMode>";
	<?php if($GLOBALS['M_SUPPORT_AZIMUTH']) { ?>
	msg += "<AzimuthEnable>" + ($("#useAzimuth").is(':checked')?1:0) + "</AzimuthEnable>";
	<?php } ?>
	msg += "</ImageOSD>";
	return msg;
}

function MakePtzPositionXml()
{
	var msg = "";
	msg += "<PTZPositionDisplay>" + ($("#ptzposition_display").is(':checked')?1:0) + "</PTZPositionDisplay>";
	return msg ;
}

function MakeTitleOsdXml()
{
	var msg = "";
	msg += "<CamTitleMode>" + ($("#camera_title_mode").is(':checked')?1:0) + "</CamTitleMode>";
  	msg += "<CamTitle>" + $("#camera_title").val() + "</CamTitle>";
  	msg += "<CamTitlePosX>" + $("#title_pos_x").slider("option","value") + "</CamTitlePosX>";
  	msg += "<CamTitlePosY>" + $("#title_pos_y").slider("option","value") + "</CamTitlePosY>";
	return msg;
}

function OnChangeTitleTimeMode(mode)
{
	var name = '', isDisable = false;
	if (mode == 'title') {
		if ($("#camera_title_mode").is(':checked')) {	
			$("#camera_title").removeAttr("disabled");
			isDisable = false;
		}
		else {
			$("#camera_title").attr("disabled", "disabled");
			isDisable = true;
		}
	}
	else {
		if ($("#time_display").is(':checked')) {		
			$("#date_notation").removeAttr("disabled");
			$("#weekday_display").removeAttr("disabled");
			isDisable = false;
		}
		else {
			$("#date_notation").attr("disabled", "disabled");
			$("#weekday_display").attr("disabled", "disabled");
			isDisable = true;
		}
	}

	SetButtonHoverFunction(isDisable, mode+'_pos_x_left');
	SetButtonHoverFunction(isDisable, mode+'_pos_x_right');
	SetButtonHoverFunction(isDisable, mode+'_pos_y_left');
	SetButtonHoverFunction(isDisable, mode+'_pos_y_right');
	$("#"+mode+"_pos_x").slider("option","disabled",isDisable);
	$("#"+mode+"_pos_y").slider("option","disabled",isDisable);

	OnChangeTitleTimePos(mode);
}

function OnChangeTitleTimePos(mode)
{
	var valX = 0, valY = 0;

	if (mode == 'title') {
		valX = <?php echo $max_camtitle_pos_x; ?>;
		valY = <?php echo $max_camtitle_pos_y; ?>;
		if ($("#camera_title").val() != "") {
			valX = valX - $("#camera_title").val().length + 1;
		}
	}
	else {
		valX = <?php echo $max_time_pos_x; ?>;
		valY = <?php echo $max_camtitle_pos_y; ?>;
	}
	
	if (mode == 'time') {
		if($("#weekday_display").is(':checked')) valX -= 4;
	}
	
	if(valX < 1) valX = 0;
		
	$("#"+mode+"_pos_x").slider("option", "max", valX);
	$("#"+mode+"_pos_x").slider("value", $("#"+mode+"_pos_x").slider("value"));
	$("#"+mode+"_pos_x_value").html($("#"+mode+"_pos_x").slider("value"));
	
	$("#"+mode+"_pos_y").slider("option", "max", valY);
	$("#"+mode+"_pos_y").slider("value", $("#"+mode+"_pos_y").slider("value"));
	$("#"+mode+"_pos_y_value").html($("#"+mode+"_pos_y").slider("value"));
}

function OnClickOSD(changeMode)			//change mode   0 : load  1 : common  2 : Title   3 : time  4 : week day  5 : size
{
	switch(changeMode){
		case 1 : SetTimeOut(); break;
		case 2 : OnChangeTitleTimeMode('title'); break;
		case 3 : OnChangeTitleTimeMode('time'); break;
		case 4 : OnChangeTitleTimePos('time'); break;
		case 5 : {
			OnChangeTitleTimePos('title');
			OnChangeTitleTimePos('time');
			break;
		}
		default : {
			OnChangeTitleTimeMode('title');
			OnChangeTitleTimeMode('time');
			break;
		}
	}
}

function ParsingXML_ImageOSD(xmlData)
{
	$("#time_pos_x").slider("option","value", parseInt(xmlData.find('DatePosX').text()));
	$("#time_pos_x_value").html(xmlData.find('DatePosX').text());
	$("#time_pos_y").slider("option","value", parseInt(xmlData.find('DatePosY').text()));
	$("#time_pos_y_value").html(xmlData.find('DatePosY').text());
	$("#time_display").prop("checked", (xmlData.find('DispDate').text()==1?true:false));
	$("#date_notation").val(xmlData.find('DateFormat').text());
	$("#weekday_display").prop("checked", (xmlData.find('DispWeekday').text()==1?true:false));
	$("#presetname_display").prop("checked", (xmlData.find('PresetNameDisplay').text()==1?true:false));
	$("#cameraid_display").prop("checked", (xmlData.find('CamIDMode').text()==1?true:false));
	$("#useAzimuth").prop("checked", (xmlData.find('AzimuthEnable').text()==1?true:false));
}
</script>

<table class="data_write mgt10 mgl-20 pdl15" style="width:670px;">
	<tr>
		<th colspan="12" class="top_txt"><?php echo $t_camtitle[$GLOBALS["LANGINDEX"]]; ?></th>
	</tr>
	<tr>
		<td style="padding-left:20px;">
			<label><input type="checkbox" id="camera_title_mode" onclick="OnClickOSD(2)" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" <?php if ($imageSpecial->dataInfo["CamTitleMode"]["value"] == 1) { echo "checked=\"checked\""; } ?>/><?php echo $t_use[$GLOBALS['LANGINDEX']]; ?></label>			
		</td>
		<td colspan="5" style="padding-left:0px;">
			<input id="camera_title" type="text" class="text" maxlength="15" style="width:225px" value="<?php echo $imageSpecial->dataInfo['CamTitle']['value']; ?>" onkeypress="NoKorean(event);OnCheckValue(event)" onkeydown="NoKorean(event);OnCamTitleKeydown(event)" onkeyup="OnChangeCamTitle()" onpaste="return false;"/>
		</td>		
		<td colspan="5"><label id="title_range">(a~z,A~Z,0~9,-,.)</label></td>
	</tr>
	<tr>
		<td style="width:120px"></td>
		<td style="width:15px;padding-left:0px;">X</td>
		<td style="width:25px;"><img id="title_pos_x_left" src="../images/common/btn/slider_-_normal.png" /></td>
		<td style="width:125px;"><div id="title_pos_x" class="slider_style_wid115"></div></td>
		<td style="width:25px;padding-left:3px;"><img id="title_pos_x_right" src="../images/common/btn/slider_+_normal.png" /></td>
		<td style="width:25px;"><label id="title_pos_x_value" style="margin-right:0px"></label></td>
		<td style="width:15px;">Y</td>
		<td style="width:25px;"><img id="title_pos_y_left" src="../images/common/btn/slider_-_normal.png" /></td>
		<td style="width:125px;"><div id="title_pos_y" class="slider_style_wid115"></div></td>
		<td style="width:25px;padding-left:3px;"><img id="title_pos_y_right" src="../images/common/btn/slider_+_normal.png" /></td>
		<td><label id="title_pos_y_value" style="margin-right:0px"></label></td>
	</tr>	
	<tr>
		<th colspan="12" class="top_txt"><?php echo $t_datetime[$GLOBALS["LANGINDEX"]]; ?></th>
	</tr>
	<tr>
		<td style="padding-left:20px;">
			<label><input type="checkbox" id="time_display" onclick="OnClickOSD(3)" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" <?php if ($imageOSD->dataInfo["DispDate"]["value"] == 1) { echo "checked=\"checked\""; } ?>/><?php echo $t_use[$GLOBALS['LANGINDEX']]; ?></label>
		</td>
		<td colspan="6" style="padding-left:0px;">
			<select id="date_notation"  class="selectbox_style_wid230" style="float:none" onchange="OnClickOSD(1)">
				<option value="0" <?php if ($imageOSD->dataInfo["DateFormat"]["value"] == 0) echo "selected=\"selected\""; ?>><?php echo $t_year[$GLOBALS["LANGINDEX"]]; ?></option>
				<option value="1" <?php if ($imageOSD->dataInfo["DateFormat"]["value"] == 1) echo "selected=\"selected\""; ?>><?php echo $t_month[$GLOBALS["LANGINDEX"]]; ?></option>
				<option value="2" <?php if ($imageOSD->dataInfo["DateFormat"]["value"] == 2) echo "selected=\"selected\""; ?>><?php echo $t_day[$GLOBALS["LANGINDEX"]]; ?></option>
			</select>
		</td>
	</tr>
	<tr>
		<td style="width:120px"></td>
		<td style="width:15px;padding-left:0px;">X</td>
		<td style="width:25px;"><img id="time_pos_x_left" src="../images/common/btn/slider_-_normal.png" /></td>
		<td style="width:125px;"><div id="time_pos_x" class="slider_style_wid115"></div></td>
		<td style="width:25px;padding-left:3px;"><img id="time_pos_x_right" src="../images/common/btn/slider_+_normal.png" /></td>
		<td style="width:25px;"><label id="time_pos_x_value" style="margin-right:0px"></label></td>
		<td style="width:15px;">Y</td>
		<td style="width:25px;"><img id="time_pos_y_left" src="../images/common/btn/slider_-_normal.png" /></td>
		<td style="width:125px;"><div id="time_pos_y" class="slider_style_wid115"></div></td>
		<td style="width:25px;padding-left:3px;"><img id="time_pos_y_right" src="../images/common/btn/slider_+_normal.png" /></td>
		<td><label id="time_pos_y_value" style="margin-right:0px"></label></td>
	</tr>
</table>

<table class="data_write mgt10 mgl-20 pdl15" style="width:670px;">
	<colgroup>
		<col style="width:120px;"/>
		<col style="width:120px;"/>
		<col />
	</colgroup>
	<tbody>
		<tr>
			<td style="padding-left:20px" colspan="2">
				<label><input type="checkbox" id="weekday_display" onclick="OnClickOSD(4)" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" <?php if ($imageOSD->dataInfo["DispWeekday"]["value"] == 1) { echo "checked=\"checked\""; } ?>/><?php echo $t_weekdaydisplay[$GLOBALS['LANGINDEX']]; ?></label>
			</td>
		</tr>
		<tr>
			<th colspan="2" class="top_txt"><?php echo $t_overlay[$GLOBALS['LANGINDEX']]; ?></th>
		</tr>
		
		<tr>
			<td style="padding-left:20px" colspan="2">
				<label><input type="checkbox" id="ptzposition_display" onclick="OnClickOSD(1)" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" <?php if ($imageSpecial->dataInfo["PTZPositionDisplay"]["value"] == 1) { echo "checked=\"checked\""; } ?>/><?php echo $t_ptzPosition[$GLOBALS['LANGINDEX']]; ?></label>
			</td>
		</tr>
		<tr>
			<td style="padding-left:20px" colspan="2">
				<label><input type="checkbox" id="presetname_display" onclick="OnClickOSD(1)" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" <?php if ($imageOSD->dataInfo["PresetNameDisplay"]["value"] == 1) { echo "checked=\"checked\""; } ?>/><?php echo $t_presetName[$GLOBALS['LANGINDEX']]; ?></label>
			</td>
		</tr>
		<tr>
			<td style="padding-left:20px" colspan="2">
				<label><input type="checkbox" id="cameraid_display" onclick="OnClickOSD(1)" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" <?php if ($imageOSD->dataInfo["CamIDMode"]["value"] == 1) { echo "checked=\"checked\""; } ?>/><?php echo $t_cameraID[$GLOBALS['LANGINDEX']]; ?></label>
			</td>
		</tr>
		<?php if($GLOBALS['M_SUPPORT_AZIMUTH']) { ?>
		<tr>
			<td style="padding-left:20px" colspan="2">
				<label><input type="checkbox" id="useAzimuth" onclick="OnClickOSD(1)" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" <?php if ($imageOSD->dataInfo["AzimuthEnable"]["value"] == 1) { echo "checked=\"checked\""; } ?>/><?php echo $t_azimuth[$GLOBALS['LANGINDEX']]; ?></label>
			</td>
		</tr>
		<?php } ?>
	</tbody>
</table>
