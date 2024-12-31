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
<?php 
	if($event_name != 'presetedit'){ ?>	
	   if(SENSOR_MODE < 2){
	   	msg += "<LongShutterSpeed>" + parseInt($("#shutter_min_highFps").val(),10) + "</LongShutterSpeed>";
			msg += "<ShortShutterSpeed>" + parseInt($("#shutter_max_highFps").val(),10) + "</ShortShutterSpeed>";
	   } else{		   	
			msg += "<LongShutterSpeed>" + parseInt($("#shutter_min_lowFps").val(),10) + "</LongShutterSpeed>";
			msg += "<ShortShutterSpeed>" + parseInt($("#shutter_max_lowFps").val(),10) + "</ShortShutterSpeed>";						
	   }		   
<?php
	}
?>
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
	<?php if ($event_name != 'presetedit') { ?>
		if($("#blc_mode").val() != 3){			//backlight_tab.cgi
			if ($("#aflk").val() == 0) {
				$("#shutter_min_lowFps").removeAttr("disabled");
				$("#shutter_min_highFps").removeAttr("disabled");
				$("#shutter_max_lowFps").removeAttr("disabled");
				$("#shutter_max_highFps").removeAttr("disabled");		
			}
			else {
				$("#shutter_min_lowFps").attr("disabled","disabled");
				$("#shutter_min_highFps").attr("disabled","disabled");
				$("#shutter_max_lowFps").attr("disabled","disabled");
				$("#shutter_max_highFps").attr("disabled","disabled");
			}
		}
		OnChangeShutterSpeed();		
	<?php } ?>
	var minValue = 0;

	if (SENSOR_MODE == 0 || SENSOR_MODE == 1) {	// 60fps, 50fps	
		<?php if ($event_name != 'presetedit') { ?>
	 		minValue = $("#shutter_min_highFps").val();
	 	<?php }else { ?>
	 		minValue = LONG_SHUTTER_SPEED;
	 	<?php } ?>
	 	if(minValue >= 0 && minValue <= 10){		//x30 ~ x2
	 		if($('#agc_mode').val() == 0 || $('#agc_mode').val() == 4){	//Off, Manual
				$('#agc_mode').val(2);			//Midium
	 		}
			ChangeOption('agc_mode', 0, 'Disable');
			ChangeOption('agc_mode', 4, 'Disable');
	 	}else{
			ChangeOption('agc_mode', 0, 'Enable');
			ChangeOption('agc_mode', 4, 'Enable');
	 	}
	}else{
		<?php if ($event_name != 'presetedit') { ?>
			minValue = $("#shutter_min_lowFps").val();
		<?php }else{ ?>
			minValue = LONG_SHUTTER_SPEED;
		<?php } ?>
	 	if(minValue >= 0 && minValue <= 13){		//x60 ~ x2
	 		if($('#agc_mode').val() == 0 || $('#agc_mode').val() == 4){	//Off, Manual
				$('#agc_mode').val(2);			//Midium
	 		}	 	
			ChangeOption('agc_mode', 0, 'Disable');
			ChangeOption('agc_mode', 4, 'Disable');
	 	}else{
			ChangeOption('agc_mode', 0, 'Enable');
			ChangeOption('agc_mode', 4, 'Enable');
	 	}
	}

	if ($("#iris_mode").val() == 0) {
		$("#iris_number").attr("disabled","disabled");
	}
	else {
		$("#iris_number").removeAttr("disabled");
	}
	OnChangeAGCMode();
	OnChangeAGCMode();
	SetTimeOut();
}

function OnChangeAGCMode()
{
	if($("#agc_mode").val() == 0 || $("#agc_mode").val() == 4)	// Off  or Manual
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
	
	if ($("#agc_mode").val() == 4) {
		$("#agcval").removeAttr("disabled");
	}
	else {
		$("#agcval").attr("disabled", "disabled");	
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
}

function InitShutterSpeed()
{
	if(SENSOR_MODE == 0){
		SetOptionValue('shutter_min_highFps', 11, '1/60');	// 1/50  => 1/60
		SetOptionValue('shutter_max_highFps', 11, '1/60');	// 1/50  => 1/60		

		SetOptionValue('shutter_min_highFps', 12, '1/120');	// 1/100  => 1/120
		SetOptionValue('shutter_max_highFps', 12, '1/120');	// 1/100  => 1/120		

		SetOptionValue('shutter_min_highFps', 13, '1/180');	// 1/150  => 1/180
		SetOptionValue('shutter_max_highFps', 13, '1/180');	// 1/150  => 1/180
		
		SetOptionValue('shutter_min_highFps', 14, '1/240');	// 1/200 => 1/240
		SetOptionValue('shutter_max_highFps', 14, '1/240');	// 1/200  => 1/240

		SetOptionValue('shutter_min_highFps', 15, '1/300'); // 1/250 => 1/300
		SetOptionValue('shutter_max_highFps', 15, '1/300'); // 1/250  => 1/300

		SetOptionValue('shutter_min_highFps', 16, '1/360'); // 1/300 => 1/360
		SetOptionValue('shutter_max_highFps', 16, '1/360'); // 1/300  => 1/360		
	}else if(SENSOR_MODE == 1){
		SetOptionValue('shutter_min_highFps', 11, '1/50');	// 1/60  => 1/50
		SetOptionValue('shutter_max_highFps', 11, '1/50');	// 1/60  => 1/50

		SetOptionValue('shutter_min_highFps', 12, '1/100'); // 1/120  => 1/100
		SetOptionValue('shutter_max_highFps', 12, '1/100'); // 1/120  => 1/100
		
		SetOptionValue('shutter_min_highFps', 13, '1/150'); // 1/180  => 1/150
		SetOptionValue('shutter_max_highFps', 13, '1/150'); // 1/180  => 1/150
		
		SetOptionValue('shutter_min_highFps', 14, '1/200'); // 1/240  => 1/200
		SetOptionValue('shutter_max_highFps', 14, '1/200'); // 1/240  => 1/200
		
		SetOptionValue('shutter_min_highFps', 15, '1/250'); // 1/300 => 1/250
		SetOptionValue('shutter_max_highFps', 15, '1/250'); // 1/300 => 1/250
		
		SetOptionValue('shutter_min_highFps', 16, '1/300'); // 1/360 => 1/300
		SetOptionValue('shutter_max_highFps', 16, '1/300'); // 1/360 => 1/300
	}else if(SENSOR_MODE == 2){
		SetOptionValue('shutter_min_lowFps', 14, '1/30');	// 1/25  => 1/30
		SetOptionValue('shutter_max_lowFps', 14, '1/30');	// 1/25  => 1/30
	}else{
		SetOptionValue('shutter_min_lowFps', 14, '1/25');	// 1/30 => 1/25
		SetOptionValue('shutter_max_lowFps', 14, '1/25');	// 1/30 => 1/25
	}
	
	if (SENSOR_MODE == 0 || SENSOR_MODE == 1) {	// 60fps, 50fps	
		$("#shutter_min_lowFps").hide();
		$("#shutter_min_highFps").show();
		
		$("#shutter_max_lowFps").hide();
		$("#shutter_max_highFps").show();
	}
	else {
		$("#shutter_min_highFps").hide();
		$("#shutter_min_lowFps").show();
		
		$("#shutter_max_highFps").hide();
		$("#shutter_max_lowFps").show();
	}
	
	if(!isOnloading){
		if (SENSOR_MODE == 0 || SENSOR_MODE == 1) {	// 60fps, 50fps	
			$('#shutter_min_highFps').val(11);
			$('#shutter_max_highFps').val(26);		// 1/11000
		}else{
			$('#shutter_min_lowFps').val(14);
			$('#shutter_max_lowFps').val(35);		// 1/11000
		}
	}else{		
		var shutter_speed_min = "<?php echo $imageExposure->dataInfo["LongShutterSpeed"]["value"]; ?>";
		var shutter_speed_max = "<?php echo $imageExposure->dataInfo["ShortShutterSpeed"]["value"]; ?>";
		if (SENSOR_MODE == 0 || SENSOR_MODE == 1) {	// 60fps, 50fps	
			$('#shutter_min_highFps').val(shutter_speed_min);
			$('#shutter_max_highFps').val(shutter_speed_max);
		}else{
			$('#shutter_min_lowFps').val(shutter_speed_min);
			$('#shutter_max_lowFps').val(shutter_speed_max);
		}
	}
	OnChangeShutterSpeed();
}

function OnChangeShutter(){
	SetShutterMin();
	SetShutterMax();
	// disable 2 sec
	if($("#sensor_mode").val() <= 1)
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

function OnChangeShutterSpeed()
{
	SetShutterMin();
	SetShutterMax();
}

function SetShutterMin()
{
	var minValue = 0;
	var size = 0;
	var currentMaxObj = '';
	if (SENSOR_MODE == 0 || SENSOR_MODE == 1) {	// 60fps, 50fps	
		currentMaxObj = "shutter_max_highFps";
	 	minValue = $("#shutter_min_highFps").val();
	 	size = $("#shutter_min_highFps").children().length;
	}else{
		currentMaxObj = "shutter_max_lowFps";
		minValue = $("#shutter_min_lowFps").val();
		size = $("#shutter_min_lowFps").children().length;
	}

	for(var i = 0 ; i < size; i++)
	{			
		if (minValue > i)
		{
			ChangeOption(currentMaxObj, i, 'Disable');
		}
		else
		{
			ChangeOption(currentMaxObj, i, 'Enable');
		}
	}
	ChangeMaxShutterLowLimit();
	<?php if(GetBrowserName() == 'IE' && ieversion() <= 7) { ?>
		document.getElementById(currentMaxObj).style.display ='none';
		document.getElementById(currentMaxObj).style.display ='';
	<?php } ?>
}

function SetShutterMax()
{
	var maxValue = 0;
	var size = 0;
	var currentMinObj = '';
	
	if (SENSOR_MODE == 0 || SENSOR_MODE == 1) {	// 60fps, 50fps	
		currentMinObj = "shutter_min_highFps";
	 	maxValue = $("#shutter_max_highFps").val();
	 	size = $("#shutter_max_highFps").children().length;
	}else{
		currentMinObj = "shutter_min_lowFps";
		maxValue = $("#shutter_max_lowFps").val();
		size = $("#shutter_max_lowFps").children().length;
	}

	for(var i = 0 ; i < size; i++)
	{
		if (maxValue < i)
		{
			ChangeOption(currentMinObj, i, 'Disable');
		}
		else
		{
			ChangeOption(currentMinObj, i, 'Enable');
		}
	}
	<?php if(GetBrowserName() == 'IE' && ieversion() <= 7) { ?>
		document.getElementById(currentMinObj).style.display ='none';
		document.getElementById(currentMinObj).style.display ='';
	<?php } ?>
}

function ChangeMaxShutterLowLimit()
{
	var maxSpeedLowLimit = 0;
	var size = 0;
	var currentMaxObj = '';
	
	if (SENSOR_MODE == 0 || SENSOR_MODE == 1){
		maxSpeedLowLimit = 11; 		// 1/50 ,  1/60
		currentMaxObj = "shutter_max_highFps";
		size = $("#shutter_min_highFps").children().length;
	}
	else{
		maxSpeedLowLimit = 14; 		// 1/25 ,  1/30
		currentMaxObj = "shutter_max_lowFps";
		size = $("#shutter_min_lowFps").children().length;
	}

	for(var i = 0 ; i < size; i++)
	{
		if (i < maxSpeedLowLimit) // set MAX shutter low limit
		{
			ChangeOption(currentMaxObj, i, 'Disable');
		}else{
			break;
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
		if($event_name != 'presetedit') {
			$shutterspeedLowFps = array("x60", "x48", "x40", "x32", "x24", "x20", "x16", "x14", "x12", "x10", "x8", "x6", "x4", "x2",
										 "1/30", "1/50", "1/60", "1/100", "1/120", "1/150", "1/180", "1/200", "1/240", "1/250", "1/300",
										 "1/360", "1/480", "1/500", "1/600", "1/700", "1/1000", "1/1500", "1/2500", "1/5000", "1/10000",
										 "1/11000", "1/16000", "1/33000");
			$shutterspeedHighFps = array("x30", "x24", "x20", "x16", "x14", "x12", "x10", "x8", "x6","x4","x2",
										 "1/50", "1/100", "1/150", "1/200", "1/250", "1/300",
										 "1/400", "1/500", "1/600", "1/700", "1/1000", "1/1500", "1/2500", "1/5000", "1/10000",
										 "1/11000", "1/12000", "1/16000");
	?>		
		<tr>
			<th class="top_txt"><?php echo $t_minshutter[$GLOBALS["LANGINDEX"]]; ?></th>
			<td colspan="3">
				<select id="shutter_min_lowFps" class="selectbox_style_wid230" onchange="OnChangeExposure()">
			<?php 
				for ($index=0; $index<count($shutterspeedLowFps); ++$index) {
			?>
					<option value="<?php echo $index; ?>"><?php echo $shutterspeedLowFps[$index]; ?></option>
			<?php
				}
			?>
				</select>				
				<select id="shutter_min_highFps" class="selectbox_style_wid230" onchange="OnChangeExposure()" style="display:none">
			<?php 
				for ($index=0; $index<count($shutterspeedHighFps); ++$index) {
			?>
					<option value="<?php echo $index; ?>"><?php echo $shutterspeedHighFps[$index]; ?></option>
			<?php
				}
			?>
				</select>
			</td>
		</tr>
		<tr>
			<th class="top_txt"><?php echo $t_maxshutter[$GLOBALS["LANGINDEX"]]; ?></th>
			<td colspan="3">
				<select id="shutter_max_lowFps" class="selectbox_style_wid230" onchange="OnChangeExposure()" style="">
			<?php 
				for ($index=0; $index<count($shutterspeedLowFps); ++$index) {
			?>
					<option value="<?php echo $index; ?>"><?php echo $shutterspeedLowFps[$index]; ?></option>
			<?php
				}
			?>
				</select>				
				<select id="shutter_max_highFps" class="selectbox_style_wid230" onchange="OnChangeExposure()" style="display:none">
			<?php 
				for ($index=0; $index<count($shutterspeedHighFps); ++$index) {
			?>
					<option value="<?php echo $index; ?>"><?php echo $shutterspeedHighFps[$index]; ?></option>
			<?php
				}
			?>
				</select>
			</td>
		</tr>
	<?php
		}
	?>
		<tr>
			<th class="top_txt"><?php echo $t_aflk[$GLOBALS["LANGINDEX"]]; ?></th>
			<td colspan="3">
				<select id="aflk" class="selectbox_style_wid230" onchange="OnChangeExposure()">
					<option value="0" <?php if ($imageExposure->dataInfo["UseAFLK"]["value"] == 0) echo "selected=\"selected\""; ?>><?php echo $t_off[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="1" <?php if ($imageExposure->dataInfo["UseAFLK"]["value"] == 1) echo "selected=\"selected\""; ?>><?php echo $t_on[$GLOBALS["LANGINDEX"]]; ?></option>
				</select>
			</td>
		</tr>
		<tr>
			<th class="top_txt"><?php echo $t_ssnr[$GLOBALS["LANGINDEX"]]; ?></th>
			<td colspan="3">
				<select id="ssnr" class="selectbox_style_wid230" onchange="OnChangeExposure()">
					<option value="0" <?php if ($imageExposure->dataInfo["SSNRMode"]["value"] == 0) echo "selected=\"selected\""; ?>><?php echo $t_off[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="1" <?php if ($imageExposure->dataInfo["SSNRMode"]["value"] == 1) echo "selected=\"selected\""; ?>><?php echo $t_on[$GLOBALS["LANGINDEX"]]; ?></option>
				</select>
			</td>
		</tr>
		<tr>
			<th class="top_txt"><?php echo $t_ssnrlevel[$GLOBALS["LANGINDEX"]]; ?></th>
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
			<th class="top_txt">Iris F-No</th>
			<td colspan="3">
				<select id="iris_number" class="selectbox_style_wid230" onchange="OnChangeExposure()">
			<?php 
				if($GLOBALS["M_MODEL_GROUP"] == MF_6320)
					$iris = array("F1.6", "F2.0", "F2.4", "F2.8", "F3.4", "F4.0", "F4.8", "F5.6", $t_close[$GLOBALS["LANGINDEX"]]);
				else
					$iris = array("F1.4", "F1.6", "F2.0", "F2.4", "F2.8", "F3.4", "F4.0", "F4.8", "F5.6", "F6.8", "F8.0", "F9.6", "F11", "F14", $t_close[$GLOBALS["LANGINDEX"]]);
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
					<option value="4" <?php if ($imageExposure->dataInfo["AGCMode"]["value"] == 4) echo "selected=\"selected\""; ?>><?php echo $t_manual[$GLOBALS["LANGINDEX"]]; ?></option>
				</select>
			</td>
		</tr>
		<tr>
			<th class="top_txt"><?php echo $t_agclevel[$GLOBALS["LANGINDEX"]]; ?></th>
			<td colspan="3">
				<select id="agcval" class="selectbox_style_wid230" onchange="OnChangeExposure()">
				<?php for ($index2=0; $index2<=42; $index2++) { ?>
				<option value="<?php echo $index2; ?>" <?php if ($imageExposure->dataInfo["AGCLevel"]["value"] == $index2) echo "selected=\"selected\""; ?>><?php echo $index2; ?> dB</option>
				<?php } ?>
				</select>
			</td>
		</tr>
	</tbody>
</table>
