<?php
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";
require_once $_SERVER["DOCUMENT_ROOT"] . "/resources/languages/Language.php";
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/datetime_constant.php";

$_SESSION["GROUP"] = "Setup";
$_SESSION["PAGE"] = "setup_time";

$result = requestToCamera(CMD_DATETIME, ACTION_GET, TYPE_REQUEST, null);
$error = "";
if($result[0] == "OK"){
	$datetime = $result[1];
	$year = byte2int($result[1], 90);
	$month = byte2int($result[1], 94); 		$month = ($month < 10)? "0".$month : $month;
	$date = byte2int($result[1], 98);		$date = ($date < 10)? "0".$date : $date;
	$hour = byte2int($result[1], 102);		$hour = ($hour < 10)? "0".$hour : $hour;
	$minute = byte2int($result[1], 106);	$minute = ($minute < 10)? "0".$minute : $minute;
	$second = byte2int($result[1], 110);	$second = ($second < 10)? "0".$second : $second;
	$time_zone = $result[1][118];
	$summer = $result[1][1];

	$date_time =  $month . "." . $date . ".". $year . " " . $hour . ":" . $minute . ":" . $second;
}else{
	$error = $result[1];
}
if(!CheckModelName_SNH('WR15')) {
	$sendData = array(0,0,0,0);
	$result = requestToCamera(CMD_IMAGE_CONFIGURATION, ACTION_GET, TYPE_REQUEST, $sendData);
	if($result[0] == "OK"){
		$osd = $result[1];
		if(CheckModelName_SNH('SEC-6410')) {
			$osd_enable = $result[1][362];
		} else {
			$osd_enable = $result[1][373];
		}
	} else {
		$error = $result[1];
		echo $error;
	}
}
?>

<? include $_SERVER["DOCUMENT_ROOT"] . "/common/html_head.php"; ?>
	<script type="text/javascript" src="/resources/js/shc_constant.js" ></script>
	<script type="text/javascript">
		var startTimer = new Date(<?=$year?>, (<?=$month?> - 1), <?=$date?>, <?=$hour?>, <?=$minute?>, <?=$second?>);

		if('<?=$error?>' != ""){
			alert('<?=$error?>');
		}

		$(document).ready(function(){
			$("#current_time").val('<?=$date_time?>');

			var html = "<select id='tmz' onchange='changeTimeZone();'>";
//			if('SEC-6410'=='<?=CAMERA_MODEL?>'){
			<? if(!CheckModelName_SNH('WR15')) { ?>
				for(var i=0; i<TIME_ZONE_LIST_V2.length; i++){
	   				if(i == <?=$time_zone?>){
	   					html += "<option value='" + i + "' selected>" + TIME_ZONE_LIST_V2[i][0] + "</option>";
	   				}else{
	   					html += "<option value='" + i + "'>" + TIME_ZONE_LIST_V2[i][0] + "</option>";
	   				}
	   			}
			<? } else { ?>
				for(var i=0; i<TIME_ZONE_LIST.length; i++){
	   				if(i == <?=$time_zone?>){
	   					html += "<option value='" + i + "' selected>" + TIME_ZONE_LIST[i][0] + "</option>";
	   				}else{
	   					html += "<option value='" + i + "'>" + TIME_ZONE_LIST[i][0] + "</option>";
	   				}
	   			}
			<? } ?>

			html += "</select>";
			document.getElementById("time_zone").innerHTML = html;
			setSummerTime(<?=$time_zone?>);

			$("input:radio[name=summer_time]").filter("input[value=" + <?=$summer?> + "]").attr("checked", "checked");
			$("input:radio[name=time_osd]").filter("input[value=" + <?=$osd_enable?> + "]").attr("checked", "checked");
			setInterval("changeDateTime()", 1000);
		});

		function changeDateTime() {
			var tt = startTimer.getTime() + 1000;
			startTimer.setTime(tt);

			var year = startTimer.getYear();
			year = (year < 1000)? (year + 1900) : year;
			var month = (startTimer.getMonth() + 1);
			month = (month < 10)? "0" + month : month;
			var day = startTimer.getDate();
			day = (day < 10)? "0" + day : day;
			var hour = startTimer.getHours();
			hour = (hour < 10)? "0" + hour : hour;
			var minute = startTimer.getMinutes();
			minute = (minute < 10)? "0" + minute : minute;
			var second = startTimer.getSeconds();
			second = (second < 10)? "0" + second : second;

			var date_time = month + "." + day + "." + year + " " + hour + ":" + minute + ":" + second;
			$("#current_time").val(date_time);
		}

		function changeTimeZone(){
			var zone = $("#tmz > option:selected").val();
			setSummerTime(zone);
			$("input:radio[name=summer_time]").filter("input[value=0]").attr("checked", "checked");
		}

		function setSummerTime(idx){
			var list;
//			if('SEC-6410'=='<?=CAMERA_MODEL?>'){
			<? if(!CheckModelName_SNH('WR15')) { ?>
				list = TIME_ZONE_LIST_V2[idx];
			<? } else { ?>
				list = TIME_ZONE_LIST[idx];
			<? } ?>

			if(list[1] == 'invalid'){
				$("#summer_time1").attr("disabled", true);
				$("#summer_time2").attr("disabled", true);
			}else{
				$("#summer_time1").removeAttr("disabled");
				$("#summer_time2").removeAttr("disabled");
			}
		}

	   	function saveData(){
	   		showProgress('<?=$Lang["Updating the camera"]?>');

	   		var sendData = '<?=implode(",", $datetime)?>' + ";";
	   		var timezone;
//			if('SEC-6410'=='<?=CAMERA_MODEL?>'){
			<? if(!CheckModelName_SNH('WR15')) { ?>
				timezone = '<?=implode(";", $TIME_ZONE_V2)?>'.split(";");
			<? } else { ?>
				timezone = '<?=implode(";", $TIME_ZONE)?>'.split(";");
			<? } ?>
	   		var zone = $("#tmz > option:selected").val();

	   		sendData += zone + ";";
	   		sendData += timezone[zone] + ";"

	   		$("input:radio[name=summer_time]:checked").each(function(){
	   			sendData += this.value +  ';' ;
		   	});

			<? if(!CheckModelName_SNH('WR15')) { ?>
	   		var osd = '<?=implode(",", $osd)?>' + ";";
		   	sendData += osd;
	   		$("input:radio[name=time_osd]:checked").each(function(){
	   			sendData += this.value +  ';' ;
		   	});
			<? if(CheckModelName_SNH('WR30')) { ?>
	   			sendData += 'WR3.0' +  ';' ;
			<?} else if(CheckModelName_SNH('WR40')) { ?>
	   			sendData += 'WR4.0' +  ';' ;
			<?} ?>
			<?} ?>

		   	$.post("/classes/class_setup_time.php", {data: sendData}, returnSetMessage, "text");
	   	}
	   	function returnSetMessage(resp){
	   		var recvData = resp.split(";");
	   		hideProgress();

			if(recvData[0] == "OK"){
				alert('<?=$Lang["Changes saved."]?>');
				moveToPage("pages/page_setup_time.php");
			}else{
				alert('<?=$Lang["Failed to save."]?>' + "-" + recvData[1]);
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

				<!-- s:컨텐츠 영역 -->
				<div id="contDiv2">
					<!-- s:TimeSetting -->
					<h2 class="cl_tit"><?=$Lang["Time Setting"]?></h2>
					<div id="tms" class="cl_gBox">
						<div class="cl_cBox nbd">
							<dl class='floatClear'>
								<dt>Time</dt>
								<dd><input type='text' id='current_time' title='txtData' value='' readonly='readonly'/></dd>
								<dt><label for='tmz'><?=$Lang["Time Zone"]?></label></dt>
								<dd id="time_zone">
									<!-- insert time zone list -->
								</dd>
								<dt><label for='sm1'><?=$Lang["Summer Time"]?></label></dt>
								<dd>
								<input name='summer_time' id='summer_time1' type='radio' value='0' id='sm1' /><label for='sm1'><?=$Lang["Disable"]?>&nbsp;&nbsp;</label>
								<input name='summer_time' id='summer_time2' type='radio' value='1' id='sm2' /><label for='sm2'><?=$Lang["Enable"]?></label>
								</dd>
								<dt><label for='sm1'>Time OSD</label></dt>
								<dd>
								<input name='time_osd' id='time_osd1' type='radio' value='0' /><label for='sm1'><?=$Lang["Disable"]?>&nbsp;&nbsp;</label>
								<input name='time_osd' id='time_osd2' type='radio' value='1' /><label for='sm2'><?=$Lang["Enable"]?></label>
								</dd>
							</dl>
						</div>
						<div class="cl_btnBox">
							<button type="button" class="btnTxt bType1" onclick="saveData();"><?=$Lang["Apply"]?></button>
						</div>
					</div>
					<!-- e:TimeSetting -->
				</div>
				<!-- e:컨텐츠 영역 -->
			 </div>
			<!-- e:contBox_cl -->
		</div>
		<!-- e:height100% -->

		<? include $_SERVER["DOCUMENT_ROOT"] . "/common/footer.php"; ?>
	</div>
</body>
</html>