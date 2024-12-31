<script type="text/javascript" language="javascript">

$(document).ready(function(){
<?php
	$sliderlist = array(	"brightness"=>array(1,100,$imageExposure->dataInfo["Brightness"]["value"]));
	foreach ($sliderlist as $name=>$data) {
?>
		$("#<?php echo $name; ?>").slider({
			orientation: "horizontal",
			min: <?php echo $data[0]; ?>,
			max: <?php echo $data[1]; ?>,
			value: <?php echo $data[2]; ?>,
			range: "min",
			slide: function( event, ui ) {
				$("#<?php echo $name; ?>_value").html(ui.value);
			},
			change: function(event, ui) {
				SetTimeOut();
			},
			stop: function(event, ui) {

			}
		});
		$("#<?php echo $name; ?>_value").html($("#<?php echo $name; ?>").slider("value"));
<?php
	}
?>
});

function MakeExposureXml()
{
	var msg = "";
	msg += "<ImageExposure>";
  	msg += "<Brightness>" + $("#brightness").slider("option","value") + "</Brightness>";
	msg += "<ShutterMode>" + (parseInt($("#aflk").val(),10) == 1 ? 2 : 0) + "</ShutterMode>";
	if(currentCameraSetupType == 'global') {
  		msg += "<LongShutterSpeed>" + parseInt($("#shutter_speed_min").val(),10)+ "</LongShutterSpeed>";
		msg += "<ShortShutterSpeed>" + parseInt($("#shutter_speed_max").val(),10) + "</ShortShutterSpeed>";
	}
  	msg += "<UseAFLK>" + parseInt($("#aflk").val(),10) + "</UseAFLK>";
  	msg += "<IrisMode>" + $("#iris_mode").val() + "</IrisMode>";  	
	msg += "<PIrisFno>" + parseInt($("#iris_number").val(),10) + "</PIrisFno>";
  	msg += "<AGCMode>" + $("#agc_mode").val() + "</AGCMode>";
  	msg += "<AGCLevel>" + $("#agcval").val() + "</AGCLevel>";
  	msg += "<SSNRMode>" + $("#ssnr").val() + "</SSNRMode>";
  	msg += "<SSNRLevel>" + $("#ssnr_level").val() + "</SSNRLevel>";
  	msg += "</ImageExposure>";
  	return msg;
}

function OnChangeExposure()
{
	if(currentCameraSetupType == 'global') {
		if ($("#aflk").val() >= 1) {
			$("#shutter_speed_min").attr("disabled","disabled");
			$("#shutter_speed_max").attr("disabled","disabled");		
		}
		else {
			$("#shutter_speed_min").removeAttr("disabled");
			$("#shutter_speed_max").removeAttr("disabled");		
		}
	}
	
	if ($("#iris_mode").val() == 0) {
		$("#iris_number").attr("disabled","disabled");
	}
	else {
		$("#iris_number").removeAttr("disabled");
	}
	OnChangeAGCMode();
	OnChangeShutter();	
	SetTimeOut();
}

function OnChangeAGCMode()
{
	if($("#agc_mode").val() == 0)	// Off 
	{
		oldDN = $("#day_night").val();
		if ($("#day_night").val() == 2)	// Auto
		{
			$("#day_night").val(0);		//Color
			$("#dwell_time").attr("disabled", "disabled");
			$("#duration").attr("disabled", "disabled");
		}
		ChangeOption('day_night', 2, 'Disable');	//Auto
		$("#ssnr").attr("disabled", "disabled");
		$("#ssnr_level").attr("disabled", "disabled");
	}
	else {	
		ChangeOption('day_night', 2, 'Enable');		//Auto
		$("#ssnr").removeAttr("disabled");
		if ($("#ssnr").val() == 0) {
			$("#ssnr_level").attr("disabled", "disabled");	
		}
		else {
			$("#ssnr_level").removeAttr("disabled");
		}
		if (oldDN == 2) {			
			$("#day_night").val(oldDN);
			$("#dwell_time").removeAttr("disabled");
			$("#duration").removeAttr("disabled");
		}
	}	
}

function ParsingXML_ImageExposure(xmlData)
{
	$("#brightness").slider("option","value", xmlData.find('Brightness').text());
	$("#brightness_value").html(xmlData.find('Brightness').text());
	$("#aflk").val(xmlData.find('UseAFLK').text());
	$("#iris_mode").val(xmlData.find('IrisMode').text());
	$("#iris_number").val(xmlData.find('PIrisFno').text());
	$("#agc_mode").val(xmlData.find('AGCMode').text());
	$("#agcval").val(xmlData.find('AGCLevel').text());
	$("#ssnr").val(xmlData.find('SSNRMode').text());
	$("#ssnr_level").val(xmlData.find('SSNRLevel').text());

	if (currentCameraSetupType == 'global') {
		$('.shutterspeed_area').show();
	}
	else {
		$('.shutterspeed_area').hide();
	}
}

function SetEnableAllShutter(){
	<?php if(GetBrowserName() == 'IE' && ieversion() <= 7) { ?>
	var size = $("#shutter_speed_min").children().length;
	for(var i = 0 ; i < size; i++){
		ChangeOption('shutter_speed_min', i, 'Enable');
		ChangeOption('shutter_speed_max', i, 'Enable');
	}
	<?php } ?>
}


function OnChangeShutter(){
	SetShutterMin();
	SetShutterMax();
	// disable 2 sec
	if(SENSOR_MODE < 2)			// 60fps, 50 fps
	{
		ChangeOption('shutter_speed_min', 0, 'Disable');
		ChangeOption('shutter_speed_max', 0, 'Disable');
	}
	else
	{
		ChangeOption('shutter_speed_min', 0, 'Enable');
		ChangeOption('shutter_speed_max', 0, 'Enable');
		// re-init lists...
		SetShutterMin();
		SetShutterMax();
	}
}

function SetShutterMin()
{
	var minValue = $("#shutter_speed_min").val();
	var size = $("#shutter_speed_min").children().length;

	for(var i = 0 ; i < size; i++)
	{			
		if (minValue > i)
		{
			ChangeOption('shutter_speed_max', i, 'Disable');
		}
		else
		{
			ChangeOption('shutter_speed_max', i, 'Enable');
		}
	}

	ChangeMaxShutterLowLimit();
	ChangeMaxShutterHighLimit();
	<?php if(GetBrowserName() == 'IE' && ieversion() <= 7) { ?>
		document.getElementById('shutter_speed_max').style.display ='none';
		document.getElementById('shutter_speed_max').style.display ='';
	<?php } ?>
}

function SetShutterMax()
{
	var maxValue = $("#shutter_speed_max").val();
	var size = $("#shutter_speed_max").children().length;
	
	for(var i = 0 ; i < size; i++)
	{
		if (maxValue < i)
		{
			ChangeOption("shutter_speed_min", i, 'Disable');
		}
		else
		{
			ChangeOption("shutter_speed_min", i, 'Enable');
		}
	}
	<?php if(GetBrowserName() == 'IE' && ieversion() <= 7) { ?>
		document.getElementById("shutter_speed_min").style.display ='none';
		document.getElementById("shutter_speed_min").style.display ='';
	<?php } ?>
}

function ChangeMaxShutterLowLimit()
{
	var maxSpeedLowLimit = 7;

	if (SENSOR_MODE == 0){
		maxSpeedLowLimit = 10; // 1/60
	}
	else if (SENSOR_MODE == 1){
		maxSpeedLowLimit = 9; // 1/50
	}
	else if (SENSOR_MODE == 2)
	{
		if($("#blc_mode").val() == 3)		// WDR
		{
			maxSpeedLowLimit = 10; // 1/60
		}
		else
		{
			maxSpeedLowLimit = 8; // 1/30
		}
	}
	else if (SENSOR_MODE == 3)
	{
		if($("#blc_mode").val() == 3)		//WDR
		{
			maxSpeedLowLimit = 9; // 1/50
		}
		else
		{
			maxSpeedLowLimit = 7; // 1/25
		}
	}
	
	for(var i = 0 ; i < 30; i++)
	{
		if (i < maxSpeedLowLimit) // set MAX shutter low limit
		{
			ChangeOption('shutter_speed_max', i, 'Disable');
		}
	}
	
}

function ChangeMaxShutterHighLimit()
{
	if($("#blc_mode").val() == 3)
	{
		if (SENSOR_MODE >= 2)				// 30fps
			maxSpeedHighLimit = 16;		// 1/240
		
		for(var i = 0 ; i < 30; i++)
		{
			if (i > maxSpeedHighLimit) // set MAX shutter high limit
			{
				ChangeOption('shutter_speed_max', i, 'Disable');
				continue;
			}
		}
		
		if($("#shutter_speed_max").val() > maxSpeedHighLimit)
		{
			$("#shutter_speed_max").val(maxSpeedHighLimit);
			SetShutterMax();
		}
	}
}

</script>
<table class= "data_write mgt10 mgl-20 pdl15" style="width:670px;">
	<colgroup>
		<col style="width:180px;"/>
		<col style="width:30px;"/>
		<col style="width:150px;"/>
		<col style="width:30px;"/>
		<col />
	</colgroup>
	<tbody>
		<tr>
		<th class="top_txt"><?php echo $t_brightness[$GLOBALS["LANGINDEX"]]; ?></th>
		<td>
			<img id="brightness_left" src="../images/common/btn/slider_-_normal.png" onclick="ControlSlider('brightness','left')"
				onMouseOver="ChangeImage('brightness_left','../images/common/btn/slider_-_press.png');" 
				onMouseOut="ChangeImage('brightness_left','../images/common/btn/slider_-_normal.png');"/>
		</td>
		<td style="padding-right:4px;">
			<div id="brightness" class="slider_style_wid163"></div>
		</td>
		<td>
			<img id="brightness_right" src="../images/common/btn/slider_+_normal.png" onclick="ControlSlider('brightness','right')"
				onMouseOver="ChangeImage('brightness_right','../images/common/btn/slider_+_press.png');" 
				onMouseOut="ChangeImage('brightness_right','../images/common/btn/slider_+_normal.png');"/>
		</td>
		<td>
			<label id="brightness_value"></label>
		</td>
		</tr>
	<?php 
		$shutterspeed = array("2", "1", "1/2", "1/4", "1/5", "1/8", "1/15", "1/25", "1/30", "1/50", "1/60", "1/100", "1/120", 
									 "1/150", "1/180", "1/200", "1/240", "1/250", "1/300", "1/360", "1/480", "1/500", "1/600", "1/700", 
									 "1/1000", "1/1500", "1/2500", "1/5000", "1/10000", "1/12000");
	?>		
		<tr class="shutterspeed_area">
			<th class="top_txt"><?php echo $t_minshutter[$GLOBALS["LANGINDEX"]]; ?></th>
			<td colspan="3">
				<select id="shutter_speed_min" class="selectbox_style_wid230" onchange="OnChangeExposure()">
				<?php for ($index=0; $index<count($shutterspeed); ++$index) { ?>
					<option value="<?php echo $index; ?>" <?php if($imageExposure->dataInfo["LongShutterSpeed"]["value"] == $index) echo "selected=\"selected\""; ?> ><?php echo $shutterspeed[$index]; ?></option>
				<?php } ?>
				</select>
			</td>
		</tr>
		<tr class="shutterspeed_area">
			<th class="top_txt"><?php echo $t_maxshutter[$GLOBALS["LANGINDEX"]]; ?></th>
			<td colspan="3">
				<select id="shutter_speed_max" class="selectbox_style_wid230" onchange="OnChangeExposure()" style="">
				<?php for ($index=0; $index<count($shutterspeed); ++$index) { ?>
					<option value="<?php echo $index; ?>" <?php if($imageExposure->dataInfo["ShortShutterSpeed"]["value"] == $index) echo "selected=\"selected\""; ?>><?php echo $shutterspeed[$index]; ?></option>
				<?php } ?>
				</select>
			</td>
		</tr>
		<tr>
			<th class="top_txt"><?php echo $t_aflk[$GLOBALS["LANGINDEX"]]; ?></th>
			<td colspan="3">
				<select id="aflk" class="selectbox_style_wid230" onchange="OnChangeExposure()">
					<option value="0" <?php if ($imageExposure->dataInfo["UseAFLK"]["value"] == 0) echo "selected=\"selected\""; ?>><?php echo $t_off[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="2" <?php if ($imageExposure->dataInfo["UseAFLK"]["value"] == 2) echo "selected=\"selected\""; ?>>50Hz</option>
					<option value="3" <?php if ($imageExposure->dataInfo["UseAFLK"]["value"] == 3) echo "selected=\"selected\""; ?>>60Hz</option>
				</select>
			</td>
		</tr>
		<tr>
			<th class="top_txt"><?php echo $t_ssnr[$GLOBALS["LANGINDEX"]]."3"; ?></th>
			<td colspan="3">
				<select id="ssnr" class="selectbox_style_wid230" onchange="OnChangeExposure()">
					<option value="0" <?php if ($imageExposure->dataInfo["SSNRMode"]["value"] == 0) echo "selected=\"selected\""; ?>><?php echo $t_off[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="1" <?php if ($imageExposure->dataInfo["SSNRMode"]["value"] == 1) echo "selected=\"selected\""; ?>><?php echo $t_on[$GLOBALS["LANGINDEX"]]; ?></option>
				</select>
			</td>
		</tr>
		<tr>
			<th class="top_txt"><?php echo $t_ssnr3level[$GLOBALS["LANGINDEX"]]; ?></th>
			<td colspan="3">
				<select id="ssnr_level" class="selectbox_style_wid230" onchange="OnChangeExposure()">
					<option value="1" <?php if ($imageExposure->dataInfo["SSNRLevel"]["value"] == 1) echo "selected=\"selected\""; ?>><?php echo $t_low[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="2" <?php if ($imageExposure->dataInfo["SSNRLevel"]["value"] == 2) echo "selected=\"selected\""; ?>><?php echo $t_middle[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="3" <?php if ($imageExposure->dataInfo["SSNRLevel"]["value"] == 3) echo "selected=\"selected\""; ?>><?php echo $t_high[$GLOBALS["LANGINDEX"]]; ?></option>
				</select>				
			</td>
		</tr>
		<tr>
			<th class="top_txt"><?php echo $t_iris[$GLOBALS["LANGINDEX"]]; ?></th>
			<td colspan="3">
				<select id="iris_mode" class="selectbox_style_wid230" onchange="OnChangeExposure()">
					<option value="0" <?php if ($imageExposure->dataInfo["IrisMode"]["value"] == 0) echo "selected=\"selected\""; ?>><?php echo $t_auto[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="1" <?php if ($imageExposure->dataInfo["IrisMode"]["value"] == 1) echo "selected=\"selected\""; ?>><?php echo $t_manual[$GLOBALS["LANGINDEX"]]; ?></option>
				</select>
			</td>
		</tr>
		<tr>
			<th class="top_txt"><?php echo $t_iris[$GLOBALS["LANGINDEX"]]; ?> F-No</th>
			<td colspan="3">
				<select id="iris_number" class="selectbox_style_wid230" onchange="OnChangeExposure()">
			<?php 
				$iris = array("F1.6", "F2.0", "F2.4", "F2.8", "F3.4", "F4.0", "F4.8", "F5.6", $t_close[$GLOBALS["LANGINDEX"]]);
				for($index=0; $index<count($iris); ++$index) { 
			?>
					<option value="<?php echo $index; ?>" <?php if ($imageExposure->dataInfo["PIrisFno"]["value"] == $index) echo "selected=\"selected\""; ?>><?php echo $iris[$index]; ?></option>
			<?php 
				} 
			?>
				</select>
			</td>
		</tr>
		<tr>
			<th class="top_txt"><?php echo $t_agcmode[$GLOBALS["LANGINDEX"]]; ?></th>
			<td colspan="3">
				<select id="agc_mode"  class="selectbox_style_wid230" onchange="OnChangeExposure()">
					<option value="0" <?php if ($imageExposure->dataInfo["AGCMode"]["value"] == 0) echo "selected=\"selected\""; ?>><?php echo $t_off[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="1" <?php if ($imageExposure->dataInfo["AGCMode"]["value"] == 1) echo "selected=\"selected\""; ?>><?php echo $t_low[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="2" <?php if ($imageExposure->dataInfo["AGCMode"]["value"] == 2) echo "selected=\"selected\""; ?>><?php echo $t_middle[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="3" <?php if ($imageExposure->dataInfo["AGCMode"]["value"] == 3) echo "selected=\"selected\""; ?>><?php echo $t_high[$GLOBALS["LANGINDEX"]]; ?></option>
				</select>
			</td>
		</tr>
	</tbody>
</table>
