<script type="text/javascript" language="javascript">

function MakeSsdrXml()
{
	var msg = "";
	msg += "<ImageSSDR>";
	msg += "<Enabled>" + ($("#ssdr_mode_enable").is(':checked')?1:0) +"</Enabled>";
	msg += "<Level>" + $("#ssdr_level").val() + "</Level>";
	msg += "</ImageSSDR>";
	return msg;
}

function OnClickSsdrMode()
{
	if ($("#ssdr_mode_enable").is(':checked')) {
		$("#ssdr_level").removeAttr("disabled");
	}
	else {
		$("#ssdr_level").attr("disabled", "disabled");
	}
	SetTimeOut();
}

function ParsingXML_ImageSSDR(xmlData)
{
	$('input:radio[name=ssdr_mode]').filter('[value="'+xmlData.find('Enabled').text()+'"]').prop("checked", true);
	$("#ssdr_level").val(xmlData.find('Level').text());
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
				<label><input type="radio" name="ssdr_mode" id="ssdr_mode_enable" value="1" onClick="OnClickSsdrMode()" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" <?php if($imageSSDR->dataInfo['Enabled']['value'] == 1) echo "checked=\"checked\"" ?> /><?php echo $t_on[$GLOBALS["LANGINDEX"]]; ?></label>
				<label><input type="radio" name="ssdr_mode" id="ssdr_mode_disable" value="0" onClick="OnClickSsdrMode()" <?php if($imageSSDR->dataInfo['Enabled']['value'] == 0) echo "checked=\"checked\"" ?> /><?php echo $t_off[$GLOBALS["LANGINDEX"]]; ?></label>
			</td>
		</tr>
		<tr>
			<th class="top_txt"><?php echo $t_level[$GLOBALS["LANGINDEX"]]; ?></th>
			<td>
				<select id="ssdr_level"  class="selectbox_style_wid230" onchange="OnClickSsdrMode()">
					<?php 	
						$max_ssdr_level = 32;
						for ($index2=1; $index2<=$max_ssdr_level; $index2++) { ?>
						<option value="<?php echo $index2; ?>" <?php if ($imageSSDR->dataInfo["Level"]["value"] == $index2) echo "selected=\"selected\""; ?>><?php echo $index2; ?></option>
					<?php } ?>
				</select>
			</td>
		</tr>
	</tbody>
</table>
