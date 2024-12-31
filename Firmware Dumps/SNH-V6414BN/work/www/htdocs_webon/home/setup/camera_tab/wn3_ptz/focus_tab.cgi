<script type ="text/javascript" language="javascript">

function MakeFocusXml()
{
	var msg = "";
	msg += "<ImageFocus>";
	msg += "<Mode>" + $("#focus_mode").val() + "</Mode>";
	msg += "<DZoom>" + $("#digital_zoom").val() + "</DZoom>";
	msg += "<DZoomLimit>" + $("#digital_zoom_limit").val() + "</DZoomLimit>";
	if (currentCameraSetupType == 'global') {
		msg += "<ZoomTrack>" + $("#zoom_tracking").val() + "</ZoomTrack>";
		msg += "<ZoomSpeed>" + $("#zoom_speed").val() + "</ZoomSpeed>";
		msg += "<InitLens>" + $("#init_lens").val() + "</InitLens>";
		msg += "<InitLensDur>" + $("#lens_duration").val() + "</InitLensDur>";
	}
	msg += "</ImageFocus>";

	return msg;
}

function OnChangeFocus()
{
	OnChangeDigitalZoom();

	if (currentCameraSetupType == 'global') {
		if ($("#init_lens").val() == 1) {
			$("#lens_duration").removeAttr("disabled");
		}
		else {
			$("#lens_duration").attr("disabled", "disabled");
		}
	}

	SetTimeOut();
}

function OnChangeDigitalZoom()
{
	if ($("#dis").val() == 1) {	//on
		$("#digital_zoom").attr("disabled", "disabled");
		$("#digital_zoom_limit").attr("disabled", "disabled");
	}
	else if ($("#dis").val() == 0) {
		$("#digital_zoom").removeAttr("disabled");
		if ($("#digital_zoom").val()==0) 	$("#digital_zoom_limit").attr("disabled", "disabled");
		else										$("#digital_zoom_limit").removeAttr("disabled");
	}
}

function ParsingXML_ImageFocus(xmlData)
{
	$("#focus_mode").val(parseInt(xmlData.find('Mode').text()));
	$("#digital_zoom").val(parseInt(xmlData.find('DZoom').text()));
	$("#digital_zoom_limit").val(parseInt(xmlData.find('DZoomLimit').text()));
	if (currentCameraSetupType == 'global') {
		$('.zoomtracking_area').show();
		$("#zoom_tracking").val(parseInt(xmlData.find('ZoomTrack').text()));
		$("#zoom_speed").val(parseInt(xmlData.find('ZoomSpeed').text()));
		$("#init_lens").val(parseInt(xmlData.find('InitLens').text()));
		$("#lens_duration").val(parseInt(xmlData.find('InitLensDur').text()));
	}
	else {
		$('.zoomtracking_area').hide();
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
			<th class="top_txt"> <?php echo $t_mode[$GLOBALS["LANGINDEX"]]; ?> </th>
			<td>
				<select id="focus_mode" class="selectbox_style_wid250" onchange="OnChangeFocus()">
					<option value="0" <?php if ($imageFocus->dataInfo['Mode']['value'] == 0) echo "selected=\"selected\""; ?> > <?php echo $t_manual[$GLOBALS["LANGINDEX"]]; ?> </option>
					<option value="1" <?php if ($imageFocus->dataInfo['Mode']['value'] == 1) echo "selected=\"selected\""; ?> > <?php echo $t_auto[$GLOBALS["LANGINDEX"]]; ?> </option>
					<option value="2" <?php if ($imageFocus->dataInfo['Mode']['value'] == 2) echo "selected=\"selected\""; ?> ><?php echo $t_oneShotAf[$GLOBALS["LANGINDEX"]]; ?> </option>
				</select>
			</td>
		</tr>
		<tr>
			<th class="top_txt"> <?php echo $t_digitalZoom[$GLOBALS["LANGINDEX"]]; ?> </th>
			<td>
				<select id="digital_zoom" class="selectbox_style_wid250" onchange="OnChangeFocus()">
					<option value="0" <?php if ($imageFocus->dataInfo['DZoom']['value'] == 0) echo "selected=\"selected\""; ?> ><?php echo $t_off[$GLOBALS["LANGINDEX"]]; ?> </option>
					<option value="1" <?php if ($imageFocus->dataInfo['DZoom']['value'] == 1) echo "selected=\"selected\""; ?> ><?php echo $t_on[$GLOBALS["LANGINDEX"]]; ?> </option>
				</select>
			</td>
		</tr>
		<tr>
			<th class="top_txt"> <?php echo $t_digitalZoomLimit[$GLOBALS["LANGINDEX"]]; ?> </th>
			<td>
				<select id="digital_zoom_limit" class="selectbox_style_wid250" onchange="OnChangeFocus()">
			<?php 
				for ($index=0; $index<15; ++$index) {
			?>
					<option value="<?php echo $index; ?>" <?php if ($imageFocus->dataInfo['DZoomLimit']['value'] == $index) echo "selected=\"selected\""; ?> ><?php echo 'x'.($index+2); ?></option>
			<?php
				}
			?>
				</select>
			</td>
		</tr>
		<tr class="zoomtracking_area">
			<th class="top_txt"> <?php echo $t_zoomTracking[$GLOBALS["LANGINDEX"]]; ?> </th>
			<td>
				<select id="zoom_tracking" class="selectbox_style_wid250" onchange="OnChangeFocus()">
					<option value="0" <?php if ($imageFocus->dataInfo['ZoomTrack']['value'] == 0) echo "selected=\"selected\""; ?> > <?php echo $t_off[$GLOBALS["LANGINDEX"]]; ?> </option>
					<option value="1" <?php if ($imageFocus->dataInfo['ZoomTrack']['value'] == 1) echo "selected=\"selected\""; ?> > <?php echo $t_autoTrack[$GLOBALS["LANGINDEX"]]; ?> </option>
					<option value="2" <?php if ($imageFocus->dataInfo['ZoomTrack']['value'] == 2) echo "selected=\"selected\""; ?> > <?php echo $t_tracking[$GLOBALS["LANGINDEX"]]; ?> </option>
				</select>
			</td>
		</tr>
		<tr class="zoomtracking_area">
			<th class="top_txt"> <?php echo $t_zoomSpeed[$GLOBALS["LANGINDEX"]]; ?> </th>
			<td>
				<select id="zoom_speed" class="selectbox_style_wid250" onchange="OnChangeFocus()">
					<option value="0" <?php if ($imageFocus->dataInfo['ZoomSpeed']['value'] == 0) echo "selected=\"selected\""; ?> > <?php echo $t_fast[$GLOBALS["LANGINDEX"]]; ?> </option>
					<option value="1" <?php if ($imageFocus->dataInfo['ZoomSpeed']['value'] == 1) echo "selected=\"selected\""; ?> > <?php echo $t_medium[$GLOBALS["LANGINDEX"]]; ?> </option>
					<option value="2" <?php if ($imageFocus->dataInfo['ZoomSpeed']['value'] == 2) echo "selected=\"selected\""; ?> > <?php echo $t_slow[$GLOBALS["LANGINDEX"]]; ?> </option>
				</select>
			</td>
		</tr>
		<tr class="zoomtracking_area">
			<th class="top_txt"> <?php echo $t_initLens[$GLOBALS["LANGINDEX"]]; ?> </th>
			<td>
				<select id="init_lens" class="selectbox_style_wid250" onchange="OnChangeFocus()">
					<option value="0" <?php if ($imageFocus->dataInfo['InitLens']['value'] == 0) echo "selected=\"selected\""; ?> > <?php echo $t_manual[$GLOBALS["LANGINDEX"]]; ?> </option>
					<option value="1" <?php if ($imageFocus->dataInfo['InitLens']['value'] == 1) echo "selected=\"selected\""; ?> > <?php echo $t_auto[$GLOBALS["LANGINDEX"]]; ?> </option>
				</select>
			</td>
		</tr>
		<tr class="zoomtracking_area">
			<th class="top_txt"> <?php echo $t_duration[$GLOBALS["LANGINDEX"]];; ?> </th>
			<td>
				<select id="lens_duration" class="selectbox_style_wid250" onchange="OnChangeFocus()">
					<option value="0" <?php if ($imageFocus->dataInfo['InitLensDur']['value'] == 0) echo "selected=\"selected\""; ?> >1 <?php echo $t_dayDisplay[$GLOBALS["LANGINDEX"]]; ?> </option>
					<option value="1" <?php if ($imageFocus->dataInfo['InitLensDur']['value'] == 1) echo "selected=\"selected\""; ?> >2 <?php echo $t_dayDisplay[$GLOBALS["LANGINDEX"]]; ?> </option>
					<option value="2" <?php if ($imageFocus->dataInfo['InitLensDur']['value'] == 2) echo "selected=\"selected\""; ?> >3 <?php echo $t_dayDisplay[$GLOBALS["LANGINDEX"]]; ?> </option>
					<option value="3" <?php if ($imageFocus->dataInfo['InitLensDur']['value'] == 3) echo "selected=\"selected\""; ?> >4 <?php echo $t_dayDisplay[$GLOBALS["LANGINDEX"]]; ?> </option>
					<option value="4" <?php if ($imageFocus->dataInfo['InitLensDur']['value'] == 4) echo "selected=\"selected\""; ?> >5 <?php echo $t_dayDisplay[$GLOBALS["LANGINDEX"]]; ?> </option>
					<option value="5" <?php if ($imageFocus->dataInfo['InitLensDur']['value'] == 5) echo "selected=\"selected\""; ?> >6 <?php echo $t_dayDisplay[$GLOBALS["LANGINDEX"]]; ?> </option>
					<option value="6" <?php if ($imageFocus->dataInfo['InitLensDur']['value'] == 6) echo "selected=\"selected\""; ?> >7 <?php echo $t_dayDisplay[$GLOBALS["LANGINDEX"]]; ?> </option>
				</select>
			</td>
		</tr>
	</tbody>
</table>
