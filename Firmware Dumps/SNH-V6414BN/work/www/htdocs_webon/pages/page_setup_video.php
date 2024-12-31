<?php
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";
require_once $_SERVER["DOCUMENT_ROOT"] . "/resources/languages/Language.php";

$_SESSION["GROUP"] = "Setup";
$_SESSION["PAGE"] = "setup_video";

$temp = array(0, 0, 0, 0);
$cmos = array_fill(0, 120, 0x00);
$newCmos = array_fill(0, 478, 0x00);
$media = array_fill(0, 414, 0x00);
$motion = array_fill(0, 2113, 0x00);

$adEvent = array();
$vaConf = array();
$recordConf = array();

$brightness = 5; $flip_mode = 0; $flicker = 0; $ir_mode = 0; $error = "";
$audio_mic = 3; $audio_spk = 5;
$motion_enable = 0; $motion_sens = 2; $time_act = 0; $audio_enable = 0; $audio_sens = 2;
$recordMnt = 0; $recordOw = 0;
$times = array(); //Time Schedule

$result = requestToCamera(CMD_MEDIA_CONFIGURATION, ACTION_GET, TYPE_REQUEST, null);

if($result[0] == "OK")
{
	$media = $result[1];

//	if(strcmp("SEC-6410", CAMERA_MODEL) != 0 )
	if(CheckModelName_SNH('WR15'))
	{
		$audio_mic = byte2int($media, 212);		//Audio_mic
		$audio_mic = ($audio_mic > 3)? 3 : $audio_mic;
		$audio_spk = byte2int($media, 282);		//Audio_spk
	}
	else
	{
		$audio_spk = byte2int($media, 283);		//Audio_spk
		$audio_mic = byte2int($media, 212);		//Audio_mic
		if ($media[210] == 0) {
			$audio_mic = 0;
		} else if ($audio_mic >= 1 && $audio_mic < 4) {
			$audio_mic = 1;
		} else if ($audio_mic >= 4 && $audio_mic < 7) {
			$audio_mic = 2;
		} else if ($audio_mic >= 7) {
			$audio_mic = 3;
		}
	}
}
else
{
	$error = $result[1];
}

//if(strcmp("SEC-6410", CAMERA_MODEL) != 0 )
if(CheckModelName_SNH('WR15'))
{
	$result = requestToCamera(CMD_CMOS_CONFIGURATION, ACTION_GET, TYPE_REQUEST, $temp);
	if($result[0] == "OK")
	{
		$cmos = $result[1];
		$brightness = byte2int($cmos, 24);		//Brightness
		$flip_mode = byte2int($cmos, 72);		//FlipMode
		$flicker = byte2int($cmos, 76);			//FlickerMode
		$ir_mode = byte2int($cmos, 96);			//IrMode
	}
	else
	{
		$error = $result[1];
	}

	$result = requestToCamera(CMD_VA_CONFIGURATION, ACTION_GET, TYPE_REQUEST, null);
	if($result[0] == "OK")
	{
		$motion = $result[1];
		$motion_enable = $motion[1]; 			//Motion-Enabled
		$motion_sens = $motion[4];				//Motion-Sensitivity
		$time_act = $motion[1106];				//Time Activation
		for($i=0, $k=1107; $i<7; $i++){
			$times[$i] = array();
			for($j=0; $j<24; $j++, $k++){
				$times[$i][$j] = $motion[$k];
			}
		}
		$audio_enable = $motion[2055];  		//Audio-Enabled
		$audio_sens = ($motion[2056] + 1);		//Audio-Sensitivity
	}
	else
	{
		$error = $result[1];
	}

}
else
{
	$result = requestToCamera(getNewCmd(CMD_CMOS_CONFIGURATION), ACTION_GET, TYPE_REQUEST, $temp);
	if($result[0] == "OK")
	{
		$newCmos = $result[1];
		if(CheckModelName_SNH('All6410') || CheckModelName_SNH('All6400'))
		{
			$isWDR = byte2int($newCmos, 57); // WDR  (SNH-6411BN not support WDR)
		}
		//$brightness = round(byte2int($newCmos, 105) / 10); // Brightness 1~100
		$flicker = $newCmos[158]; // 0:auto, 2:50hz, 3:60hz
		$nightVisionAuto = byte2int($newCmos, 261); // night vision
	}
	else
	{
		$error = $result[1];
	}

	$result = requestToCamera(getNewCmd(CMD_VA_CONFIGURATION), ACTION_GET, TYPE_REQUEST, null);
	if($result[0] == "OK")
	{
		$vaConf = $result[1];
		if(CheckModelName_SNH('All6410'))
		{
			$motion_enable = $vaConf[1];
		}
		else
		{
			$motion_enable = $vaConf[666];
		}

		if($motion_enable != 0)
		{
			$motion_enable = 1;
		}

		if(CheckModelName_SNH('All6410'))
		{
			$motion_sens = byte2int($vaConf, 4) + 1;
		}
		else
		{
			$motion_sens = $vaConf[669] + 1;
		}

//		$time_act = $vaConf[345];
		$time_act = $vaConf[1020];
/*		for($i=0, $k=346; $i<7; $i++){
			$times[$i] = array();
			for($j=0; $j<24; $j++, $k++){
				$times[$i][$j] = $vaConf[$k];
			}
		} */
		for($i=0, $k=1021; $i<7; $i++){
			$times[$i] = array();
			for($j=0; $j<24; $j++, $k++){
				$times[$i][$j] = $vaConf[$k];
			}
		}
	}
	else
	{
		$error = $result[1];
	}

	$result = requestToCamera(getNewCmd(CMD_AD_EVENT), ACTION_GET, TYPE_REQUEST, null);
	if($result[0] == "OK")
	{
		$adEvent = $result[1];
		$audio_enable = $adEvent[0];
		if($audio_enable != 0)
		{
			$audio_enable = 1;
		}
		$audio_sens = $adEvent[1];
		if ($audio_sens <= 20) {
			$audio_sens = 5;
		} else if($audio_sens >= 21 && $audio_sens <= 40) {
			$audio_sens = 4;
		} else if($audio_sens >= 41 && $audio_sens <= 60) {
			$audio_sens = 3;
		} else if($audio_sens >= 61 && $audio_sens <= 80) {
			$audio_sens = 2;
		} else if($audio_sens >= 81) {
			$audio_sens = 1;
		}
	}
	else
	{
		$error = $result[1];
	}

	$result = requestToCamera(getNewCmd(CMD_RECORD_CONFIGURATION), ACTION_GET, TYPE_REQUEST, null);
	if($result[0] == "OK")
	{
		$recordConf = $result[1];
		$recordMnt = $recordConf[0];
		$recordOw = $recordConf[2];
	}
	else
	{
		$error = $result[1];
	}

	/* $result = requestToCamera(CMD_VIDEO_SOURCE, ACTION_GET, TYPE_REQUEST, null);
	if($result[0] == "OK"){
		$vdo_src = $result[1];
	}else{
		$error = $result[1];
	} */
}
?>

<? include $_SERVER["DOCUMENT_ROOT"] . "/common/html_head.php"; ?>
	<link type="text/css" href="/resources/css/jquery-ui.css" rel="stylesheet" />
	<script type="text/javascript" src="/resources/js/jquery-ui.js"></script>
	<script type="text/javascript">
		var cmos = '<?=implode(",", $cmos)?>'.split(",");
		var newCmos = '<?=implode(",", $newCmos)?>'.split(",");
		var media = '<?=implode(",", $media)?>'.split(",");
		var motion = '<?=implode(",", $motion)?>'.split(",");
		var vaConf = '<?=implode(",", $vaConf)?>'.split(",");
		var adEvent = '<?=implode(",", $adEvent)?>'.split(",");
		var recordConf = '<?=implode(",", $recordConf)?>'.split(",");
		var isFirst = true;
		var flipMode = 0;
	    var time = new Array();
	    var isPlaying = false;
	    var brightness = '<?=$brightness?>';

	    if('<?=$error?>' != ""){
			alert('<?=$error?>');
		}

	    $(function() {
			$("#slider_AUDIO_MIC").slider({
				range: "min",
				value: <?=$audio_mic?>,
				min: 0,
				max: 3,
				slide: function(event, ui){
					$("#AUDIO_MIC").val(ui.value);
				}
			});

			$("#slider_AUDIO_SPK").slider({
				range: "min",
				value: <?=$audio_spk?>,
				min: 1,
				max: 10,
				slide: function(event, ui){
					$("#AUDIO_SPK").val(ui.value);
				}
			});

			$("#slider_MOTION_SENS").slider({
				range: "min",
				value: <?=$motion_sens?>,
				min: 1,
				max: 5,
				slide: function(event, ui){
					$("#MOTION_SENS").val(ui.value);
				}
			});

			$("#slider_AUDIO_SENS").slider({
				range: "min",
				value: <?=$audio_sens?>,
				min: 1,
				max: 5,
				slide: function(event, ui){
					$("#AUDIO_SENS").val(ui.value);
				}
			});
		});

	    $(document).ready(function(){
			$(".toggleBtn1").click(function() {
				var tar = $(".snsBox");
    		   	tar.slideUp(200);
			});
			$(".toggleBtn2").click(function() {
				var tar = $(".snsBox");
				tar.slideDown(200);
			});

			initData();
		});

function initData()
{
		flipMode = '<?=$flip_mode?>';
		$("input:radio[name=flicker]").filter("input[value=" + <?=$flicker?> + "]").attr("checked", "checked");
		$("input:radio[name=ir_led]").filter("input[value=" + <?=$nightVisionAuto?> + "]").attr("checked", "checked");
		$("#AUDIO_MIC").val('<?=$audio_mic?>');
		$("#AUDIO_SPK").val('<?=$audio_spk?>');
		$("input:radio[name=motion]").filter("input[value=" + <?=$motion_enable?> + "]").attr("checked", "checked");
		$("#MOTION_SENS").val('<?=$motion_sens?>');
		$("input:radio[name=audio]").filter("input[value=" + <?=$audio_enable?> + "]").attr("checked", "checked");
		$("#AUDIO_SENS").val('<?=$audio_sens?>');
		$("input:radio[name=wdr]").filter("input[value=" + <?=$isWDR?> + "]").attr("checked", "checked");
		$("input:radio[name=sdcard_mnt]").filter("input[value=" + <?=$recordMnt?> + "]").attr("checked", "checked");
		$("input:radio[name=sdcard_ow]").filter("input[value=" + <?=$recordOw?> + "]").attr("checked", "checked");
		$("input:radio[name=time_schedule]").filter("input[value=" + <?=$time_act?> + "]").attr("checked", "checked");


		if(<?=$time_act?> == 0)
		{
			document.getElementById("set_time").className = "vs_tb snsBox close";
			document.getElementById("set_time").style.display = "none";
			$("#btnClear").attr("disabled", true);
		}
		else
		{
			document.getElementById("set_time").className = "vs_tb snsBox";
			$("#btnClear").removeAttr("disabled");
		}

		initTimers();

		$("#AUDIO_MIC").attr("disabled", true);
		$("#AUDIO_SPK").attr("disabled", true);
		$("#MOTION_SENS").attr("disabled", true);
		$("#AUDIO_SENS").attr("disabled", true);
}

function initTimers()
{
	time[0] = '<?=implode(",", $times[0])?>'.split(",");
	time[1] = '<?=implode(",", $times[1])?>'.split(",");
	time[2] = '<?=implode(",", $times[2])?>'.split(",");
	time[3] = '<?=implode(",", $times[3])?>'.split(",");
	time[4] = '<?=implode(",", $times[4])?>'.split(",");
	time[5] = '<?=implode(",", $times[5])?>'.split(",");
	time[6] = '<?=implode(",", $times[6])?>'.split(",");

	createActivationTime();
}

function returnLiveMessage(resp)
{
	var recvData = resp.split(";");
	if(recvData[0] != "OK")
	{
		alert('<?=$Lang["Failed to save."]?>');
	}
}

function createActivationTime()
{
		var day = ["", '<?=$Lang["Sun"]?>', '<?=$Lang["Mon"]?>', '<?=$Lang["Tue"]?>',
		        	   '<?=$Lang["Wed"]?>', '<?=$Lang["Thu"]?>', '<?=$Lang["Fri"]?>', '<?=$Lang["Sat"]?>'];

		var html = "<table>";
		for(var i=0; i<8; i++)
		{
			html += "<tr>";
			for(var j=0; j<25; j++)
			{
				if(j == 0)
				{
					html += "<th style='cursor:pointer; cursor:hand' onclick='selectAllRow(" + i + ");'>" + day[i] + "</td>";
				}
				else
				{
					if(i == 0)
					{
						if((j-1) <= 9)
						{
							html += "<th style='cursor:pointer; cursor:hand' onclick='selectAllColumn(" + j + ");'>0" + (j-1) + "</td>";
		 				}
		 				else
		 				{
		 					html += "<th style='cursor:pointer; cursor:hand' onclick='selectAllColumn(" + j + ");'>" + (j-1) + "</td>";
						}
					}
					else
					{
						if(time[i-1][j-1] == 1)
						{
							html += "<td id='T" + i + "-" + j + "' style='background-color:#979EE4; cursor:pointer; cursor:hand' onclick='selectActivationTime(" + i + "," + j + ");'></td>";
						}
						else
						{
							html += "<td id='T" + i + "-" + j + "' style='background-color:#C1C8C5; cursor:pointer; cursor:hand' onclick='selectActivationTime(" + i + "," + j + ");'></td>";
						}
					}
				}
			}
			html += "</tr>";
		}
	html += "</table>";
	document.getElementById("set_time").innerHTML = html;
	}

function clearActivationTime()
{
		for(var i=0; i<time.length; i++)
		{
			for(var j=0; j<time[i].length; j++)
			{
				time[i][j] = 0;
			}
		}
		createActivationTime();
}

function saveData()
{
//	if('SEC-6410'=='<?=CAMERA_MODEL?>')
	<? if(!CheckModelName_SNH('WR15')) { ?>
		saveData6410();
		return;
	<? } else { ?>
	cmos[72] = parseInt(flipMode);
	cmos[24] = brightness;
	$("input:radio[name=flicker]:checked").each(function(){
		cmos[76] = parseInt(this.value);
		});
	$("input:radio[name=ir_led]:checked").each(function(){
			cmos[96] = parseInt(this.value);
		});

	media[212] = parseInt($("#AUDIO_MIC").val());
	media[282] = parseInt($("#AUDIO_SPK").val());

	$("input:radio[name=motion]:checked").each(function(){
		motion[1] = parseInt(this.value);
		});

	motion[4] = parseInt($("#MOTION_SENS").val());
	$("input:radio[name=time_schedule]:checked").each(function(){
		motion[1106] = parseInt(this.value);
		});
	for(var i=0, k=1107; i<7; i++)
	{
		for(var j=0; j<24; j++, k++)
		{
			motion[k] = time[i][j];
		}
	}
	$("input:radio[name=audio]:checked").each(function(){
		motion[2055] = parseInt(this.value);
		});
	motion[2056] = (parseInt($("#AUDIO_SENS").val()) - 1);

	var sendData = "SET;" + cmos.join(",") + ";" + media.join(",") + ";" + motion.join(",");
	$.post("/classes/class_setup_video.php", {data: sendData}, returnSetMessage, "text");
	<? } ?>
	/*
		var sendData = "SET;" + '<?=implode(",", $cmos)?>' + ";" + '<?=implode(",", $media)?>' + ";" + '<?=implode(",", $motion)?>' + ";";
		sendData += flipMode + ";";
		sendData += $("#BRIGHTNESS").val() + ";";
		$("input:radio[name=flicker]:checked").each(function(){
			sendData += this.value + ";";
		});
		$("input:radio[name=ir_led]:checked").each(function(){
			sendData += this.value + ";";
		});
		sendData += $("#AUDIO_MIC").val() + ";";
		sendData += $("#AUDIO_SPK").val() + ";";
		$("input:radio[name=motion]:checked").each(function(){
			sendData += this.value + ";";
		});
		sendData += (parseInt($("#MOTION_SENS").val()) - 1) + ";";
		$("input:radio[name=time_schedule]:checked").each(function(){
			sendData += this.value + ";";
		});
		for(var i=0; i<7; i++){
			sendData += time[i].join(",") + ";";
		}
		$("input:radio[name=audio]:checked").each(function(){
			sendData += this.value + ";";
		});
		sendData += (parseInt($("#AUDIO_SENS").val()) - 1);

		$.post("/classes/class_setup_video.php", {data: sendData}, returnSetMessage, "text");
		*/
}
function saveData6410()
{
	newCmos[154] = 29; // 0x1d

	<? if(CheckModelName_SNH('All6410') || CheckModelName_SNH('All6400')) { ?>
	$("input:radio[name=wdr]:checked").each(function(){
	newCmos[57] = parseInt(this.value);
	if(parseInt(this.value) != 0)
	{
		newCmos[154] = 16; // 0x10
	}
	});
	<? } ?>

	$("input:radio[name=flicker]:checked").each(function(){
	newCmos[158] = this.value;
	});
	$("input:radio[name=ir_led]:checked").each(function(){
		newCmos[261] = parseInt(this.value);
	});

	micVal = parseInt($("#AUDIO_MIC").val());
	media[283] = parseInt($("#AUDIO_SPK").val());

	if (micVal == 0) {
		media[210] = 0;
		media[212] = 1;
	} else if (micVal == 1) {
		media[210] = 1;
		media[212] = 3;
	} else if (micVal == 2) {
		media[210] = 1;
		media[212] = 6;
	} else if (micVal == 3) {
		media[210] = 1;
		media[212] = 9;
	}


	$("input:radio[name=motion]:checked").each(function(){
		<? if(CheckModelName_SNH('All6410')) { ?>
		vaConf[1] = this.value;
		<? } else { ?>
		vaConf[1] = this.value;
		vaConf[666] = this.value;
		vaConf[670] = this.value;
		<? } ?>
		});
		<? if(CheckModelName_SNH('All6410')) { ?>
			vaConf[4] = parseInt($("#MOTION_SENS").val()) - 1;
		<? } else { ?>
			vaConf[669] = parseInt($("#MOTION_SENS").val()) - 1;
		<? } ?>

		$("input:radio[name=time_schedule]:checked").each(function(){
			vaConf[1020] = parseInt(this.value);
			adEvent[2] = parseInt(this.value);
		});

		for(var i=0, k=1021, l=3; i<7; i++){
			for(var j=0; j<24; j++, k++, l++){
				vaConf[k] = time[i][j];
				adEvent[l] = time[i][j];
			}
		}
		$("input:radio[name=audio]:checked").each(function(){
			adEvent[0] = this.value;
		});

		var ad_sen = parseInt($("#AUDIO_SENS").val());

		if (ad_sen == 1) {
			adEvent[1] = 100;
		} else if (ad_sen == 2) {
			adEvent[1] = 80;
		} else if (ad_sen == 3) {
			adEvent[1] = 60;
		} else if (ad_sen == 4) {
			adEvent[1] = 40;
		} else if (ad_sen == 5) {
			adEvent[1] = 20;
		} else {
			adEvent[1] = 60;
		}

		$("input:radio[name=sdcard_mnt]:checked").each(function(){
			recordConf[0] = parseInt(this.value);
		});
		$("input:radio[name=sdcard_ow]:checked").each(function(){
			recordConf[2] = parseInt(this.value);
		});


		var sendData = "IPCV0.7;VIDEO_SET_ALL;" + newCmos.join(",") + ";" + media.join(",") + ";" + vaConf.join(",") + ";" + adEvent.join(",") + ";" + recordConf.join(",");
		$.post("/classes/class_setup_video.php", {data: sendData}, returnSetMessage, "text");
}

function returnSetMessage(resp)
{
	var recvData = resp.split(";");
	if(recvData[0] == "OK")
	{
		alert('<?=$Lang["Changes saved."]?>');
	}
	else
	{
		if(recvData[1] != undefined)
		{
		alert('<?=$Lang["Failed to save."]?>' + "-" + recvData[1]);
		}
	}
}

function changeSchedule(status)
{
	if(status == "0")
	{
		$("#btnClear").attr("disabled", true);
	}
	else
	{
		$("#btnClear").removeAttr("disabled");
	}
}

function selectActivationTime(i, j)
{
	var obj = document.getElementById("T" + i + "-" + j);
	if(obj.style.backgroundColor.toUpperCase() == "#979EE4" || obj.style.backgroundColor == "rgb(151, 158, 228)")
	{
		time[i-1][j-1] = 0;
		obj.style.backgroundColor = "#C1C8C5";
	}
	else
	{
		time[i-1][j-1] = 1;
		obj.style.backgroundColor = "#979EE4";
	}
}

function selectAllRow(row)
{
	if(row > 0)
	{
		var obj = document.getElementById("T" + row + "-1");
		var color = getColor(obj.style.backgroundColor);
		for(var i=1; i<=time[row-1].length; i++)
		{
			if(color == "#C1C8C5")
			{
				time[row-1][i-1] = 0;
			}
			else
			{
				time[row-1][i-1] = 1;
			}
		}
		createActivationTime();
	}
}

function selectAllColumn(col)
{
	if(col > 0)
	{
		var obj = document.getElementById("T1-" + col);
		var color = getColor(obj.style.backgroundColor);
		for(var i=1; i<=time.length; i++)
		{
			if(color == "#C1C8C5")
			{
				time[i-1][col-1] = 0;
			}
			else
			{
				time[i-1][col-1] = 1;
			}
		}
		createActivationTime();
	}
}

function getColor(c)
{
	if(c == "#979ee4" || c == "#979EE4" || c == "rgb(151, 158, 228)")
	{
		return "#C1C8C5";
	}
	else
	{
		return "#979EE4";
	}
}

function returnAppletMessage(msg)
{
	if(msg == "play")
	{
		isPlaying = true;
	}else if(msg == "event"){
	}else if(msg == "privacy"){
    	alert('<?=$Lang["Camera is set to privacy mode"]?>');
    	parent.moveToPage("pages/camera_login.php");
	}else if(msg == "close"){
		parent.moveToPage("pages/camera_login.php");
		}else if(msg == "audio"){
 	}else{
 		alert(msg);
 	}
 }
	</script>
</head>

		<? include $_SERVER["DOCUMENT_ROOT"] . "/common/header.php"; ?>

		<!-- s:height100% -->
		<div id="hgt100">
			<!-- s:contBox_cl -->
			<div id="contBox_cl" class="floatClear">

				<? include $_SERVER["DOCUMENT_ROOT"] . "/common/side_menu.php"; ?>

				<div id="contDiv2" class="vs_area">
					<!-- s:VideoSetting -->
					<div class="sp_box">
						<div class="sp_event">
							<div class="ev_title">
								<h2 class="cl_tit"><?=$Lang["Event Alarm"]?></h2>
							</div>
							<div class="ev_ct">
								<dl>
									<dt><?=$Lang["Motion"]?></dt>
									<dd>
										<input name="motion" type="radio" id="ea1" value="1" /> <label for="ea1"><?=$Lang["On"]?></label>
										<input name="motion" type="radio" id="ea2" value="0" /> <label for="ea2"><?=$Lang["Off"]?></label>
									</dd>
									<dt><?=$Lang["Sensitivity"]?></dt>
									<dd>
										<div class="slider_small">
											<div id="slider_MOTION_SENS"></div>
										</div>
										<input type="text" class="text_small" id="MOTION_SENS" value="" />
									</dd>
									<dt><?=$Lang["Audio"]?></dt>
									<dd>
										<input name="audio" type="radio" id="ea3" value="1" /> <label for="ea3"><?=$Lang["On"]?></label>
										<input name="audio" type="radio" id="ea4" value="0" /> <label for="ea4"><?=$Lang["Off"]?></label>
									</dd>
									<dt><?=$Lang["Sensitivity"]?></dt>
									<dd>
										<div class="slider_small">
											<div id="slider_AUDIO_SENS"></div>
										</div>
										<input type="text" class="text_small" id="AUDIO_SENS" value="" />
									</dd>
								</dl>
							</div>
						</div>


					<div class="sp_audio">
						<div class="au_title">
							<h2 class="cl_tit"><?=$Lang["Audio"]?></h2>
						</div>
						<div class="au_ct">
							<dl>
								<dt><?=$Lang["Mic"]?></dt>
								<dd>
									<div class="slider_small">
										<div id="slider_AUDIO_MIC"></div>
									</div>
									<input type="text" class="text_small" id="AUDIO_MIC" value=""  />
								</dd>
								<dt style="margin-top:28px"><?=$Lang["Speaker"]?></dt>
								<dd>
									<div class="slider_small" style="margin-top:34px">
										<div id="slider_AUDIO_SPK"></div>
									</div>
									<input type="text" class="text_small" id="AUDIO_SPK" value=""  />
								</dd>
							</dl>
						</div>
					</div>
				</div>

				<div class="sp_box2">
					<div class="sp_day">
						<div class="day_title">
							<h2 class="cl_tit"><?=$Lang["Night Vision"]?></h2>
						</div>
						<div class="day_ct">
							<dl>
								<dt><?=$Lang["Night Vision"]?></dt>
								<dd>
									<input name="ir_led" type="radio" id="ir1" value="2" /> <label for="ir1"><?=$Lang["Auto"]?></label>
									<input name="ir_led" type="radio" id="ir2" value="0" /> <label for="ir2"><?=$Lang["Off"]?></label>
								</dd>
							</dl>
						</div>
					</div>
					<div class="sp_flicker">
						<div class="flic_title">
							<h2 class="cl_tit"><?=$Lang["Flickerless"]?></h2>
						</div>
						<div class="flic_ct">
							<dl>
								<dt><?=$Lang["Flickerless"]?></dt>
								<dd>
									<input name="flicker" type="radio" id="fk1" value="0" /> <label for="fk1"><?=$Lang["Off"]?></label>
									<input name="flicker" type="radio" id="fk2" value="2" /> <label for="fk2">50Hz</label>
									<input name="flicker" type="radio" id="fk3" value="3" /> <label for="fk3">60Hz</label>
								</dd>
							</dl>
						</div>
					</div>
				</div>

				<? if(CheckModelName_SNH('SD')) { ?>
				<div class="sp_box3">
				<? if(CheckModelName_SNH('WDR')) { ?>
					<div class="sp_wdr">
						<div class="wdr_title">
							<h2 class="cl_tit">WDR</h2>
						</div>
						<div class="wdr_ct">
							<dl>
								<dt>WDR</dt>
								<dd>
									<input name="wdr" type="radio" id="wdr1" value="3" /> <label for="wdr1"><?=$Lang["On"]?></label>
									<input name="wdr" type="radio" id="wdr2" value="0" /> <label for="wdr2"><?=$Lang["Off"]?></label>
								</dd>
							</dl>
						</div>
					</div>
					<div class="sp_sdcard">
				<? } else { ?>
					<div class="sp_sdcard_modified">
				<? } ?>
						<div class="sdcard_title">
							<h2 class="cl_tit">SD Card</h2>
						</div>
						<div class="sdcard_ct">
							<dl>
								<dt>Mount</dt>
								<dd>
									<input name="sdcard_mnt" type="radio" id="sdcard_mnt1" value="1" /> <label for="sdcard_mnt1">Mount</label>
									<input name="sdcard_mnt" type="radio" id="sdcard_mnt2" value="0" /> <label for="sdcard_mnt2">Unmount</label>
								</dd>

								<dt>Overwrite</dt>
								<dd>
									<input name="sdcard_ow" type="radio" id="sdcard_ow1" value="1" /> <label for="sdcard_ow1"><?=$Lang["On"]?></label>
									<input name="sdcard_ow" type="radio" id="sdcard_ow2" value="0" /> <label for="sdcard_ow2"><?=$Lang["Off"]?></label>
								</dd>
							</dl>
						</div>
					</div>
				</div>
				<?}?>

				<div class="vs_area5">
					<h2 class="cl_tit"><?=$Lang["Event schedule"]?></h2>
						<div class="vs_rdBox">
							<input class="toggleBtn1" name="time_schedule" type="radio" id="at1" value="0" onclick="changeSchedule('0');"/> <label for="at1"><?=$Lang["Always"]?>&nbsp;&nbsp;&nbsp;&nbsp;</label>
							<input class="toggleBtn2" name="time_schedule" type="radio" id="at2" value="1" onclick="changeSchedule('1');"/> <label for="at2"><?=$Lang["Scheduled"]?></label>
							<button type="button" id="btnClear" class="btnTxt bType2a" onclick="clearActivationTime();"><?=$Lang["Clear"]?></button>
						</div>
					<div class="vs_tb snsBox" id="set_time">
						<!-- insert activation time -->
					</div>
				</div>
				<div class="cl_btnBox">
					<button type="button" class="btnTxt bType1" onclick="saveData();"><?=$Lang["Apply"]?></button>
				</div>
				<!-- e:VideoSetting -->
			</div>
			<!-- e:而⑦뀗痢��곸뿭 -->
		 </div>
		<!-- e:contBox_cl -->
	</div>
	<!-- e:height100% -->
		<? include $_SERVER["DOCUMENT_ROOT"] . "/common/footer.php"; ?>
	</div>
</body>
</html>