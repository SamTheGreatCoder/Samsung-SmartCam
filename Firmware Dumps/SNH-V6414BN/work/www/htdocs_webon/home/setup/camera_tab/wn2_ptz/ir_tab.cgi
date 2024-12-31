<script type="text/javascript" language="javascript">

$(document).ready(function(){
<?php
	$sliderlist = array(	"ledOn_level"=>array(1,90,$imagePTZIR->dataInfo["LedOnLevel"]["value"]),
					  			"ledOff_level"=>array(11,100,$imagePTZIR->dataInfo["LedOffLevel"]["value"]));
	foreach ($sliderlist as $name=>$data) {
?>
		$("#"+"<?php echo $name; ?>").slider({
			orientation: "horizontal",
			min: <?php echo $data[0]; ?>,
			max: <?php echo $data[1]; ?>,
			value: <?php echo $data[2]; ?>,
			range: "min",
			slide: function( event, ui ) {
				$("#"+"<?php echo $name; ?>_value").html(ui.value);
				<?php if($name == "ledOn_level"){ ?>
					if(ui.value+10 > $("#ledOff_level").slider("value")){
						$("#ledOff_level").slider("value",ui.value+10);
						$("#ledOff_level_value").html(ui.value+10);
					}
				<?php }else{ ?>
					if(ui.value-10 < $("#ledOn_level").slider("value")){
						$("#ledOn_level").slider("value",ui.value-10);
						$("#ledOn_level_value").html(ui.value-10);
					}				
				<?php } ?>
			},
			change: function(event, ui) {
				<?php if($name == "ledOn_level"){ ?>
					if(ui.value+10 > $("#ledOff_level").slider("value")){
						$("#ledOff_level").slider("value",ui.value+10);
						$("#ledOff_level_value").html(ui.value+10);
					}
				<?php }else{ ?>
					if(ui.value-10 < $("#ledOn_level").slider("value")){
						$("#ledOn_level").slider("value",ui.value-10);
						$("#ledOn_level_value").html(ui.value-10);
					}				
				<?php } ?>
			
				SetTimeOut();
			},
			stop: function(event, ui) {

			}
		});
		$("#"+"<?php echo $name; ?>_value").html($("#"+"<?php echo $name; ?>").slider("value"));
		
<?php
	}
?>
	$(".spinnerHour").spinner({
		min:-1,
		max:24,
		spin: function(event, ui) {		
			if (ui.value > 23) {
				$(this).val("00");
				return false;
			}
			else if (ui.value < 0) {
				$(this).val(23);
				return false;
			}
			if(ui.value < 10){
				$(this).val("0"+ui.value);
				return false;
			}
		},
		stop: function(event, ui) {
			if(parseInt($("#ledOnTime_Min").val(),10) == parseInt($("#ledOffTime_Min").val(),10) && parseInt($("#ledOnTime_Hour").val(),10) == parseInt($("#ledOffTime_Hour").val(),10)){
				if($(this).attr("id") == "ledOnTime_Hour"){
					var hourVal = parseInt($("#ledOffTime_Hour").val(),10) + 1;
					hourVal = GetValidHour(hourVal);
					$("#ledOffTime_Hour").val(hourVal);
				}else{
					var hourVal = parseInt($("#ledOnTime_Hour").val(),10) - 1;
					hourVal = GetValidHour(hourVal);					
					$("#ledOnTime_Hour").val(hourVal);
				}
			}
		
			SetTimeOut();
		}
	});

	$(".spinnerMin").spinner({
		min:-1,
		max:60,
		spin: function(event, ui) {
			if (ui.value > 59) {
				$(this).val("00");
				var timeId = $(this).attr("id").split("_");
				var hourVal = parseInt($("#"+timeId[0]+"_Hour").val(),10) + 1;
				hourVal = GetValidHour(hourVal);
				$("#"+timeId[0]+"_Hour").val(hourVal);
				return false;
			}
			else if (ui.value < 0) {
				$(this).val(59);
				var timeId = $(this).attr("id").split("_");
				var hourVal = parseInt($("#"+timeId[0]+"_Hour").val(),10) - 1;
				hourVal = GetValidHour(hourVal);
				$("#"+timeId[0]+"_Hour").val(hourVal);				
				return false;
			}
			if(ui.value < 10){
				$(this).val("0"+ui.value);
				return false;
			}
		},
		stop: function(event, ui) {
			if(parseInt($("#ledOnTime_Min").val(),10) == parseInt($("#ledOffTime_Min").val(),10) && parseInt($("#ledOnTime_Hour").val(),10) == parseInt($("#ledOffTime_Hour").val(),10)){
				if($(this).attr("id") == "ledOnTime_Min"){
					var hourVal = parseInt($("#ledOffTime_Hour").val(),10) + 1;
					hourVal = GetValidHour(hourVal);
					$("#ledOffTime_Hour").val(hourVal);
				}else{
					var hourVal = parseInt($("#ledOnTime_Hour").val(),10) - 1;
					hourVal = GetValidHour(hourVal);
					$("#ledOnTime_Hour").val(hourVal);
				}
			}
			SetTimeOut();
		}
	});

	$("#ledOnTime_Hour").val("<?php echo $imagePTZIR->dataInfo["LedOnTimeHour"]["value"]; ?>");
	$("#ledOnTime_Min").val("<?php echo $imagePTZIR->dataInfo["LedOnTimeMin"]["value"]; ?>");
	$("#ledOffTime_Hour").val("<?php echo $imagePTZIR->dataInfo["LedOffTimeHour"]["value"]; ?>");
	$("#ledOffTime_Min").val("<?php echo $imagePTZIR->dataInfo["LedOffTimeMin"]["value"]; ?>");	
	SetLedTimeFormat();
});

function SetLedTimeFormat(){
	$(".ledTime").each(function(e){
		if($(this).val() < 10){
			$(this).val("0"+$(this).val());
		}
	});
}
function GetValidHour(ledHour){
	var validTime = parseInt(ledHour,10);
	if(validTime >= 24) 
		validTime = 0;
	else if(validTime <= 0){
		validTime = 23;
	}
	
	if(validTime < 10){
		validTime = "0"+validTime;
	}	
	return validTime;
}

function MakeIrXml()
{
	var msg = "";
	msg += "<ImagePTZIR>";
	msg += "<Mode>" + $("#ir_mode").val() + "</Mode>";
	msg += "<LedOnLevel>"+ $("#ledOn_level").slider("option","value") +"</LedOnLevel>";
	msg += "<LedOffLevel>"+ $("#ledOff_level").slider("option","value") +"</LedOffLevel>";
	msg += "<LedOnTimeHour>"+parseInt($("#ledOnTime_Hour").val(),10)+"</LedOnTimeHour>";
	msg += "<LedOnTimeMin>"+parseInt($("#ledOnTime_Min").val(),10)+"</LedOnTimeMin>";
	msg += "<LedOffTimeHour>"+parseInt($("#ledOffTime_Hour").val(),10)+"</LedOffTimeHour>";
	msg += "<LedOffTimeMin>"+parseInt($("#ledOffTime_Min").val(),10)+"</LedOffTimeMin>";
	msg += "<LedMaxPower>"+ $("#led_maxPower").val() +"</LedMaxPower>";
	msg += "<LedPowerControl>"+ $("#led_powerControl").val() +"</LedPowerControl>";
	//msg += "<Level>" + $("#ir_level").slider("option","value") + "</Level>";
	msg += "</ImagePTZIR>";
	return msg;
}

function OnChangeIR()
{
	var irMode = parseInt($("#ir_mode").val(),10);

	if(irMode == 0){	//Off
		$("#led_maxPower").prop("disabled", true);
		$("#led_powerControl").prop("disabled", true);
	}else{
		$("#led_maxPower").prop("disabled", false);
		$("#led_powerControl").prop("disabled", false);
	}

	if(irMode == 3){ //Sensor
		$("#ledOn_level").slider("option","disabled",false);
		$("#ledOff_level").slider("option","disabled",false);
		SetButtonHoverFunction(false, 'ledOn_level_left');
		SetButtonHoverFunction(false, 'ledOn_level_right');
		SetButtonHoverFunction(false, 'ledOff_level_left');
		SetButtonHoverFunction(false, 'ledOff_level_right');		
	}else{
		$("#ledOn_level").slider("option","disabled",true);
		$("#ledOff_level").slider("option","disabled",true);
		SetButtonHoverFunction(true, 'ledOn_level_left');
		SetButtonHoverFunction(true, 'ledOn_level_right');
		SetButtonHoverFunction(true, 'ledOff_level_left');
		SetButtonHoverFunction(true, 'ledOff_level_right');		
	}

	if(irMode == 4){ //Timed
		$("#ledOnTime_Hour").prop("disabled", false);
		$("#ledOnTime_Min").prop("disabled", false);
		$("#ledOffTime_Hour").prop("disabled", false);
		$("#ledOffTime_Min").prop("disabled", false);
		$('.ui-spinner a.ui-spinner-button').css('display','block');
	}else{
		$("#ledOnTime_Hour").prop("disabled", true);
		$("#ledOnTime_Min").prop("disabled", true);
		$("#ledOffTime_Hour").prop("disabled", true);
		$("#ledOffTime_Min").prop("disabled", true);
		$('.ui-spinner a.ui-spinner-button').css('display','none');
	}
	SetIrModeDependence(irMode);		//  wn2_ptz/special_tab.cgi
	SetTimeOut();
}

function ParsingXML_ImagePTZIR(xmlData)
{
	$("#ir_mode").val(xmlData.find('Mode').text());
	$("#ledOn_level").slider("option","value",xmlData.find('LedOnLevel').text());
	$("#ledOff_level").slider("option","value",xmlData.find('LedOffLevel').text());
	$("#ledOnTime_Hour").val(xmlData.find('LedOnTimeHour').text());
	$("#ledOnTime_Min").val(xmlData.find('LedOnTimeMin').text());
	$("#ledOffTime_Hour").val(xmlData.find('LedOffTimeHour').text());
	$("#ledOffTime_Min").val(xmlData.find('LedOffTimeMin').text());
	SetLedTimeFormat();
	$("#led_maxPower").val(xmlData.find('LedMaxPower').text());
	$("#led_powerControl").val(xmlData.find('LedPowerControl').text());

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
			<td colspan="4">
				<select id="ir_mode"  class="selectbox_style_wid230" onchange="OnChangeIR()">
					<option value="0" <?php if ($imagePTZIR->dataInfo["Mode"]["value"] == 0) echo "selected=\"selected\""; ?>><?php echo $t_off[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="1" <?php if ($imagePTZIR->dataInfo["Mode"]["value"] == 1) echo "selected=\"selected\""; ?>><?php echo $t_on[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="2" <?php if ($imagePTZIR->dataInfo["Mode"]["value"] == 2) echo "selected=\"selected\""; ?>><?php echo $t_daynight[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="3" <?php if ($imagePTZIR->dataInfo["Mode"]["value"] == 3) echo "selected=\"selected\""; ?>><?php echo $t_sensor[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="4" <?php if ($imagePTZIR->dataInfo["Mode"]["value"] == 4) echo "selected=\"selected\""; ?>><?php echo $t_timed[$GLOBALS["LANGINDEX"]]; ?></option>
				</select>
			</td>
		</tr>
		<tr>
			<th class="top_txt"><?php echo $t_ledOnLevel[$GLOBALS["LANGINDEX"]]; ?></th>
			<td>
				<img id="ledOn_level_left" src="../images/common/btn/slider_-_normal.png" />
			</td>
			<td>
				<div id="ledOn_level" class="slider_style_wid150"></div>
			</td>
			<td>
				<img id="ledOn_level_right" src="../images/common/btn/slider_+_normal.png" />
			</td>
			<td>
				<label id="ledOn_level_value"></label>
			</td>
		</tr>
		<tr>
			<th class="top_txt"><?php echo $t_ledOffLevel[$GLOBALS["LANGINDEX"]]; ?></th>
			<td>
				<img id="ledOff_level_left" src="../images/common/btn/slider_-_normal.png" />
			</td>
			<td>
				<div id="ledOff_level" class="slider_style_wid150"></div>
			</td>
			<td>
				<img id="ledOff_level_right" src="../images/common/btn/slider_+_normal.png" />
			</td>
			<td>
				<label id="ledOff_level_value"></label>
			</td>
		</tr>
		<tr>
			<th class="top_txt"><?php echo $t_ledOnTime[$GLOBALS["LANGINDEX"]]; ?></th>
			<td colspan="4">
				<label>
					<input type="text" id="ledOnTime_Hour" class="ledTime spinnerHour text" style="width:40px;" value="" maxlength="2" readonly="readonly" /> :
					<input type="text" id="ledOnTime_Min" class="ledTime spinnerMin text" style="width:40px;" value="" maxlength="2" readonly="readonly" /> ~
					<input type="text" id="ledOffTime_Hour" class="ledTime spinnerHour text" style="width:40px;" value="" maxlength="2" readonly="readonly" /> :
					<input type="text" id="ledOffTime_Min" class="ledTime spinnerMin text" style="width:40px;" value="" maxlength="2" readonly="readonly" />
				<label>
			</td>
		</tr>
		<tr>
			<th class="top_txt"><?php echo $t_ledMaxPower[$GLOBALS["LANGINDEX"]]; ?></th>
			<td colspan="4">
				<select id="led_maxPower"  class="selectbox_style_wid230" onchange="OnChangeIR()">
					<option value="0" <?php if ($imagePTZIR->dataInfo["LedMaxPower"]["value"] == 0) echo "selected=\"selected\""; ?>><?php echo $t_low[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="1" <?php if ($imagePTZIR->dataInfo["LedMaxPower"]["value"] == 1) echo "selected=\"selected\""; ?>><?php echo $t_medium[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="2" <?php if ($imagePTZIR->dataInfo["LedMaxPower"]["value"] == 2) echo "selected=\"selected\""; ?>><?php echo $t_high[$GLOBALS["LANGINDEX"]]; ?></option>
				</select>
			</td>
		</tr>
		<tr>
			<th class="top_txt"><?php echo $t_ledPowerControl[$GLOBALS["LANGINDEX"]]; ?></th>
			<td colspan="4">
				<select id="led_powerControl"  class="selectbox_style_wid230" onchange="OnChangeIR()">
					<option value="0" <?php if ($imagePTZIR->dataInfo["LedPowerControl"]["value"] == 0) echo "selected=\"selected\""; ?>><?php echo $t_off[$GLOBALS["LANGINDEX"]]; ?></option>
					<option value="1" <?php if ($imagePTZIR->dataInfo["LedPowerControl"]["value"] == 1) echo "selected=\"selected\""; ?>><?php echo $t_auto[$GLOBALS["LANGINDEX"]]; ?></option>
				</select>
			</td>
		</tr>
		
	</tbody>
</table>
