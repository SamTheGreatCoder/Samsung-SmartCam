<script type="text/javascript" language="javascript">
<?php
	if($GLOBALS['M_MAX_RESOLUTION'] == MAX_3_MEGA){
		$shutterspeed = array("2", "1", "1/2", "1/4", "1/5", "1/8", "1/15", "1/20", "1/25", "1/30", "1/50", "1/60", "1/100", "1/120", 
									 "1/150", "1/180", "1/200", "1/240", "1/250", "1/300", "1/360", "1/480", "1/500", "1/600", "1/700", 
									 "1/1000", "1/1500", "1/2500", "1/5000", "1/10000", "1/12000");
	}else{
		$shutterspeed = array("2", "1", "1/2", "1/4", "1/5", "1/8", "1/15", "1/25", "1/30", "1/50", "1/60", "1/100", "1/120", 
									 "1/150", "1/180", "1/200", "1/240", "1/250", "1/300", "1/360", "1/480", "1/500", "1/600", "1/700", 
									 "1/1000", "1/1500", "1/2500", "1/5000", "1/10000", "1/12000");
	}
?>	


$(document).ready(function(){
<?php
	$sliderlist = array(	"brightness"=>array(1,100,$imageExposure->dataInfo["Brightness"]["value"]),
								"iris_piris_pos"=>array(1,100,$imageExposure->dataInfo["PIrisPosition"]["value"]));

	if (($GLOBALS['M_SUPPORT_IRIS'] & PIRIS_SUPPORT) != PIRIS_SUPPORT)
		array_pop($sliderlist);

	foreach ($sliderlist as $name=>$data) {
?>
		$("#<?php echo $name; ?>").slider({
			orientation: "horizontal",
			min: <?php echo $data[0]; ?>,
			max: <?php echo $data[1]; ?>,
			value: <?php echo $data[2]; ?>,
			range: "min",
			slide: function( event, ui ) {
				<?php if($name == "iris_piris_pos") { ?>
					pirisVal = ui.value;
					DrawPIrisValue();			//exposure_tab.cgi
					SetPIris_Fno(ui.value);	//exposure_tab.cgi
				<?php } else { ?>
					$("#<?php echo $name; ?>_value").html(ui.value);
				<?php } ?>
			},
			change: function(event, ui) {
				SetTimeOut();
			},
			stop: function(event, ui) {

			}
		});
		<?php if($name == "iris_piris_pos") { ?>
			DrawPIrisValue();															//exposure_tab.cgi
			SetPIris_Fno($("#<?php echo $name; ?>").slider("value"));		//exposure_tab.cgi
		<?php } else { ?>
			$("#<?php echo $name; ?>_value").html($("#<?php echo $name; ?>").slider("value"));
		<?php } ?>
<?php
	}
?>
});

function MakeExposureXml(presetMode)
{
	var msg = "";
	msg += "<ImageExposure>";
  	msg += "<Brightness>" + $("#brightness").slider("option","value") + "</Brightness>";
	msg += "<ShutterMode>" + (parseInt($("#aflk").val(),10) == 0 ? 0 : 2) + "</ShutterMode>";
	<?php 
		if ($GLOBALS['M_SUPPORT_IRIS'] != IRIS_NO_SUPPORT) { 
	?>
	  		msg += "<IrisMode>" + $("#iris_mode").val() + "</IrisMode>";  	
		<?php 
			if($GLOBALS['M_SUPPORT_IRIS'] & IRIS_FNO_SUPPORT) { 
		?>
				msg += "<PIrisFno>" + parseInt($("#iris_number").val(),10) + "</PIrisFno>";
		<?php 
			} 
			
			if ($GLOBALS['M_SUPPORT_IRIS'] & PIRIS_SUPPORT) { 
	?>
			  	msg += "<PIrisMode>" + parseInt($("#iris_piris").val(),10) + "</PIrisMode>";
			  	msg += "<PIrisPosition>" + parseInt($("#iris_piris_pos_value").text(),10) + "</PIrisPosition>";
		<?php 
			}
		}
	?>	
	msg += "<UseAFLK>" + parseInt($("#aflk").val(),10) + "</UseAFLK>";

  	if(presetMode == 7){
  		msg += "<LongShutterSpeed>" + parseInt($("#shutter_speed_min").val(),10)+ "</LongShutterSpeed>";
		msg += "<ShortShutterSpeed>" + parseInt($("#shutter_speed_max").val(),10) + "</ShortShutterSpeed>";
	  	msg += "<AGCMode>" + $("#agc_mode").val() + "</AGCMode>";
	  	msg += "<SSNRMode>" + $("#ssnr").val() + "</SSNRMode>";
	  	msg += "<SSNRLevel>" + $("#ssnr_level").val() + "</SSNRLevel>";
  	}else{
		msg += "<LongShutterSpeed>" + userPresetValue["MinShutter"] + "</LongShutterSpeed>";
		msg += "<ShortShutterSpeed>" + userPresetValue["MaxShutter"] + "</ShortShutterSpeed>";		
  	}
  	
  	msg += "</ImageExposure>";
  	return msg;
}

function ChangePIrisMenu(isDisable)
{
	SetButtonHoverFunction(isDisable, 'iris_piris_pos_left');
	SetButtonHoverFunction(isDisable, 'iris_piris_pos_right');
	$("#iris_piris_pos").slider("option","disabled",isDisable);
}

function OnChangeExposure()
{
<?php 
	if ($GLOBALS['M_SUPPORT_IRIS'] & IRIS_FNO_SUPPORT) { 
?>
		if ($("#iris_mode").val() == 1) {
			$("#iris_number").removeAttr("disabled");
		}
		else {
			$("#iris_number").attr("disabled","disabled");
		}
<?php
	}
?>
	
<?php 
	if ($GLOBALS['M_SUPPORT_IRIS'] & PIRIS_SUPPORT) { 
?>
		if(parseInt($("#iris_mode").val()) >= 2) {
			$("#iris_piris").removeAttr("disabled");
			if($("#iris_piris").val() == 1) {
				ChangePIrisMenu(false);
			}
			else {
				ChangePIrisMenu(true);
			}
		}
		else {
			$("#iris_piris").attr("disabled", "disabled");
			ChangePIrisMenu(true);
		}
<?php 
	}
?>
	if($("#aflk").val() >= 1)
	{
		$("#shutter_speed_min").attr("disabled", "disabled");
		$("#shutter_speed_max").attr("disabled", "disabled");
	}
	else
	{
		if($("#preset_default").val() == 7){
			$("#shutter_speed_min").removeAttr("disabled");
			$("#shutter_speed_max").removeAttr("disabled");			
		}
	}

	if($("#preset_default").val() == 7){
		if($("#ssnr").val() == 0 || $("#agc_mode").val() == 0)
		{
			$("#ssnr_level").attr("disabled", "disabled");
		}
		else
		{
			$("#ssnr_level").removeAttr("disabled");
		}
		
		OnChangeAGCMode();
	}	
	OnChangeShutter();

	SetTimeOut();
}

function OnChangeAGCMode()
{
	if($("#agc_mode").val() == 0)	// Off  or Manual
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

function DrawPIrisValue()
{
	if (pirisVal % 2 != 0 && pirisVal > 2)
		$("#iris_piris_pos_value").html(pirisVal + 1);
	else
		$("#iris_piris_pos_value").html(pirisVal);
}

function SetPIris_Fno(pIrisFno)
{
	var manualFno = parseInt((pIrisFno)/2);
	var fNo = new Array('F16.00', 'F14.13', 'F11.00', 'F10.20', 'F8.95', 'F8.00', 'F7.12', 'F6.50', 'F5.97', 'F5.60',
								'F5.11', 'F4.76', 'F4.46', 'F4.12', 'F4.00', 'F3.69', 'F3.48', 'F3.29', 'F3.12', 'F2.96', 
								'F2.80', 'F2.70', 'F2.59', 'F2.48', 'F2.40', 'F2.30', 'F2.22', 'F2.08', 'F2.01', 'F2.00', 
								'F1.95', 'F1.90', 'F1.85', 'F1.80', 'F1.75', 'F1.71', 'F1.67', 'F1.63', 'F1.60', 'F1.56', 
								'F1.53', 'F1.50', 'F1.47', 'F1.44', 'F1.42', 'F1.40', 'F1.36', 'F1.34', 'F1.30', 'F1.28', 
								'F1.26', 'F1.20');
	
	if(manualFno < 0 && manualFno > 50)
		return;

	if(pIrisFno == 1 || pIrisFno == 2){
		$("#iris_piris_fno").html(fNo[manualFno]);
	}
	else if(pIrisFno == 35 || pIrisFno == 68){
		$("#iris_piris_fno").html(fNo[manualFno+1]);
	}
	else if(pIrisFno < 35 && pIrisFno > 2){
		if(pIrisFno % 2 == 0){
			$("#iris_piris_fno").html(fNo[manualFno]);
		}
		else{
			$("#iris_piris_fno").html(fNo[manualFno+1]);
		}
	}
	else if(pIrisFno < 68 && pIrisFno > 35){
		$("#iris_piris_fno").html(fNo[manualFno+1]);
	}
	else if(pIrisFno < 101 && pIrisFno > 68){
		if(pIrisFno % 2 == 0){
			$("#iris_piris_fno").html(fNo[manualFno+1]);
		}
		else{
			$("#iris_piris_fno").html(fNo[manualFno+2]);
		}
	}
}

function OnChangeShutter()
{
	SetShutterMin();
	SetShutterMax();
	<?php if($GLOBALS['M_SUPPORT_SENSOR_FRAMEMODE'] && $GLOBALS['M_MAX_SERSORFRAME'] == 60) { ?>
		if(SENSOR_MODE <= 1)
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
	<?php }else if($GLOBALS['M_SUPPORT_SENSOR_FRAMEMODE'] && $GLOBALS['M_MAX_SERSORFRAME'] == 30){ ?>
		<?php if($GLOBALS['M_SUPPORT_MEGAMODE'] && $GLOBALS['MEGAMODE'] == 3){ ?>
			ChangeOption('shutter_speed_min', 0, 'Disable');
			ChangeOption('shutter_speed_max', 0, 'Disable');
		<?php }else{ ?>
			if(SENSOR_MODE == 0 || SENSOR_MODE == 2)
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
		<?php } ?>
	<?php } ?>
}

function SetShutterMin()
{
	var minValue = $("#shutter_speed_min").val();
	var shutterSize = <?php echo count($shutterspeed);?>;

	for(var i = 0 ; i < shutterSize; i++)
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
	if(BrowserDetect.browser == "Explorer" && getIEVersion() <= 7) {
		document.getElementById("shutter_speed_max").style.display ='none';
		document.getElementById("shutter_speed_max").style.display ='';
	}
}

function SetShutterMax()
{
	var maxValue = $("#shutter_speed_max").val();
	var shutterSize = <?php echo count($shutterspeed);?>;

	for(var i = 0 ; i < shutterSize; i++)
	{
		if (maxValue < i)
		{
			ChangeOption('shutter_speed_min', i, 'Disable');
		}
		else
		{
			ChangeOption('shutter_speed_min', i, 'Enable');
		}
	}
	
	if(BrowserDetect.browser == "Explorer" && getIEVersion() <= 7) {
		document.getElementById("shutter_speed_min").style.display ='none';
		document.getElementById("shutter_speed_min").style.display ='';
	}
}

function ChangeMaxShutterLowLimit()
{
	var maxSpeedLowLimit = 0;
	var shutterSize = <?php echo count($shutterspeed);?>;

	var shutterOffset = 0;
	<?php if($GLOBALS['M_MAX_RESOLUTION'] == MAX_3_MEGA){ ?>
		shutterOffset = 1;
	<?php } ?>
	
	if (SENSOR_MODE == 0){
		maxSpeedLowLimit = 10 + shutterOffset; // 1/60
	}
	else if (SENSOR_MODE == 1){
		maxSpeedLowLimit = 9 + shutterOffset; // 1/50
	}
	else if (SENSOR_MODE == 2)
	{
		if($("#blc_mode").val() == 3)
		{
			maxSpeedLowLimit = 10 + shutterOffset; // 1/60
		}
		else
		{
			maxSpeedLowLimit = 8 + shutterOffset; // 1/30
		}
	}
	else if (SENSOR_MODE == 3)
	{
		if($("#blc_mode").val() == 3)
		{
			maxSpeedLowLimit = 9 + shutterOffset; // 1/50
		}
		else
		{
			maxSpeedLowLimit = 7+ shutterOffset; // 1/25
		}
	}

	<?php if($GLOBALS['M_MODEL_GROUP'] == MF_7010FE){ ?>
		maxSpeedLowLimit = 7;
	<?php } ?>
	
	for(var i = 0 ; i < shutterSize; i++)
	{
		if (i < maxSpeedLowLimit) // set MAX shutter low limit
		{
			ChangeOption('shutter_speed_max', i, 'Disable');
		}
	}
}

function ChangeMaxShutterHighLimit()
{
	var shutterSize = <?php echo count($shutterspeed);?>;
	var maxSpeedHighLimit = 0;	

	if($("#blc_mode").val() == 3)
	{	
		<?php if($GLOBALS['M_MAX_RESOLUTION'] == MAX_3_MEGA){ ?>
			maxSpeedHighLimit = 17;		// 1/240
		<?php }else if($GLOBALS['M_MAX_RESOLUTION'] == MAX_1_MEGA){ ?>
			maxSpeedHighLimit = 23;		// 1/700
		<?php }else{ ?>
			if (SENSOR_MODE >= 2){
				maxSpeedHighLimit = 16;		// 1/240
			}
		<?php } ?>
		
		for(var i = 0 ; i < shutterSize; i++)
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
		<tr>
			<th class="top_txt"><?php echo $t_minshutter[$GLOBALS["LANGINDEX"]]; ?></th>
			<td colspan="3">
				<select id="shutter_speed_min"  class="selectbox_style_wid230" onchange="OnChangeExposure()">
				<?php for($index=0; $index<count($shutterspeed); ++$index) { ?>
					<option value="<?php echo $index; ?>" ><?php echo $shutterspeed[$index]; ?></option>
				<?php } ?>			
				</select>
			</td>
		</tr>
		<tr>
			<th class="top_txt"><?php echo $t_maxshutter[$GLOBALS["LANGINDEX"]]; ?></th>
			<td colspan="3">
				<select id="shutter_speed_max" class="selectbox_style_wid230" onchange="OnChangeExposure()">
				<?php for($index=0; $index<count($shutterspeed); ++$index) { ?>
					<option value="<?php echo $index; ?>" ><?php echo $shutterspeed[$index]; ?></option>
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
					<option value="0"><?php echo $t_off[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="1"><?php echo $t_on[$GLOBALS["LANGINDEX"]]; ?></option>
				</select>
			</td>
		</tr>
		<tr>
			<th class="top_txt"><?php echo $t_ssnr3level[$GLOBALS["LANGINDEX"]]; ?></th>
			<td colspan="3">
				<select id="ssnr_level" class="selectbox_style_wid230" onchange="OnChangeExposure()">
				<?php for($i=1; $i<=32; $i++){ ?>
					<option value="<?php echo $i ?>" <?php if ($imageExposure->dataInfo["SSNRLevel"]["value"] == $i) echo "selected=\"selected\""; ?>><?php echo $i ?></option>
				<?php } ?>
				</select>
			</td>
		</tr>		
<?php 
	if ($GLOBALS['M_SUPPORT_IRIS'] & PIRIS_SUPPORT) { 
?>
		<tr>
			<th class="top_txt"><?php echo $t_lens[$GLOBALS["LANGINDEX"]]; ?></th>
			<td colspan="3">
				<select id="iris_mode"  class="selectbox_style_wid230" onchange="OnChangeExposure()">
					<option value="0" <?php if ($imageExposure->dataInfo["IrisMode"]["value"] == 0) echo "selected=\"selected\""; ?> ><?php echo "DC(".$t_auto[$GLOBALS["LANGINDEX"]].")"; ?></option>
					<option value="1" <?php if ($imageExposure->dataInfo["IrisMode"]["value"] == 1) echo "selected=\"selected\""; ?> ><?php echo $t_manual[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="2" <?php if ($imageExposure->dataInfo["IrisMode"]["value"] == 2) echo "selected=\"selected\""; ?> ><?php echo $t_pirisM3180PN[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="3" <?php if ($imageExposure->dataInfo["IrisMode"]["value"] == 3) echo "selected=\"selected\""; ?> ><?php echo $t_pirisM13VP288IR[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="4" <?php if ($imageExposure->dataInfo["IrisMode"]["value"] == 4) echo "selected=\"selected\""; ?> ><?php echo $t_pirisM2890PN[$GLOBALS["LANGINDEX"]]; ?></option>
				</select>
			</td>
		</tr>
		<tr>
			<th class="top_txt"><?php echo $t_piris[$GLOBALS["LANGINDEX"]]; ?></th>
			<td colspan="3">
				<select id="iris_piris"  class="selectbox_style_wid230" onchange="OnChangeExposure()">
					<option value="0" <?php if ($imageExposure->dataInfo["PIrisMode"]["value"] == 0) echo "selected=\"selected\""; ?> ><?php echo $t_auto[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="1" <?php if ($imageExposure->dataInfo["PIrisMode"]["value"] == 1) echo "selected=\"selected\""; ?> ><?php echo $t_manual[$GLOBALS["LANGINDEX"]]; ?></option>
				</select>
			</td>
		</tr>
		<tr>
			<th class="top_txt"><?php echo $t_pirisposition[$GLOBALS["LANGINDEX"]]; ?></th>
			<td>
				<img id="iris_piris_pos_left" src="../images/common/btn/slider_-_normal.png" />
			</td>
			<td><div id="iris_piris_pos" class="slider_style_wid163"></div></td>
			<td>		
				<img id="iris_piris_pos_right" src="../images/common/btn/slider_+_normal.png" />
			</td>
			<td><label id="iris_piris_pos_value"></label><label id="iris_piris_fno"></label></td>
		</tr>
<?php 
	}
	else if ($GLOBALS['M_SUPPORT_IRIS'] & DOME_PIRIS_SUPPORT) { 
?>
		<tr>
			<th class="top_txt"><?php echo $t_lens[$GLOBALS["LANGINDEX"]]; ?></th>
			<td colspan="3">
				<select id="iris_mode"  class="selectbox_style_wid230" onchange="OnChangeExposure()">
					<option value="0" <?php if ($imageExposure->dataInfo["IrisMode"]["value"] == 0) echo "selected=\"selected\""; ?> ><?php echo "DC(".$t_auto[$GLOBALS["LANGINDEX"]].")"; ?></option>
					<option value="1" <?php if ($imageExposure->dataInfo["IrisMode"]["value"] == 1) echo "selected=\"selected\""; ?> ><?php echo $t_manual[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="2" <?php if ($imageExposure->dataInfo["IrisMode"]["value"] == 2) echo "selected=\"selected\""; ?> ><?php echo $t_piris[$GLOBALS["LANGINDEX"]]; ?></option>
				</select>
			</td>
		</tr>
<?php
	}else if ($GLOBALS['M_SUPPORT_IRIS'] & IRIS_SUPPORT) {
?>
		<tr>
			<th class="top_txt"><?php echo $t_iris[$GLOBALS["LANGINDEX"]]; ?></th>
			<td colspan="3">
				<select id="iris_mode"	class="selectbox_style_wid230" onchange="OnChangeExposure()">
					<option value="0" <?php if ($imageExposure->dataInfo["IrisMode"]["value"] == 0) echo "selected=\"selected\""; ?> ><?php echo $t_auto[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="1" <?php if ($imageExposure->dataInfo["IrisMode"]["value"] == 1) echo "selected=\"selected\""; ?> ><?php echo $t_manual[$GLOBALS["LANGINDEX"]]; ?></option>
				</select>
			</td>
		</tr>
<?php 
	}
	if($GLOBALS['M_SUPPORT_IRIS'] & IRIS_FNO_SUPPORT) {
?>
		<tr>
			<th class="top_txt"><?php echo $t_iris[$GLOBALS["LANGINDEX"]]; ?> F-No</th>
			<td colspan="3">
				<select id="iris_number" class="selectbox_style_wid230" onchange="OnChangeExposure()">
			<?php 
				$iris = array("F1.2", "F1.4", "F1.6", "F2", "F2.4", "F2.8", "F3.4", "F4", "F4.8", "F5.6", "F6.8", "F8", "F9.6", "F11", "F14", "F16", "F19", "F22", "F28");
				for($index=0; $index<count($iris); ++$index) { 
			?>
					<option value="<?php echo $index; ?>" <?php if ($imageExposure->dataInfo["PIrisFno"]["value"] == $index) echo "selected=\"selected\""; ?>><?php echo $iris[$index]; ?></option>
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
			<th class="top_txt"><?php echo $t_agcmode[$GLOBALS["LANGINDEX"]]; ?></th>
			<td colspan="3">
				<select id="agc_mode"  class="selectbox_style_wid230" onchange="OnChangeExposure()">
					<option value="0"><?php echo $t_off[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="1"><?php echo $t_low[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="2"><?php echo $t_middle[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="3"><?php echo $t_high[$GLOBALS["LANGINDEX"]]; ?></option>
				</select>
			</td>
		</tr>
	</tbody>
</table>
