<?php
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/xmlParser.php";
require_once $_SERVER["DOCUMENT_ROOT"] . "/resources/languages/Language.php";

$_SESSION["GROUP"] = "Admin";
$_SESSION["PAGE"] = "admin_firmware";

$result = requestToCamera(CMD_SYSTEM_CONFIGURATION, ACTION_GET, TYPE_REQUEST, null);
$curMajor = "0"; $curMinor = "0"; $curDate = "000000";
$lastMajor = "0"; $lastMinor = "0"; $lastDate = "000000";
$error = "";
if($result[0] == "OK"){
	$device = byte2str($result[1], 224, 32);   	//Device Name
	$serial = byte2str($result[1], 176, 32);	//Serial Number
	$firmware = byte2str($result[1], 96, 16);	//FirmwareVersion
	$arrFirm = explode("_", $firmware);
	$arrVersion = explode(".", $arrFirm[0]);
	$curMajor = $arrVersion[0];
	$curMinor = $arrVersion[1];
	$curDate = $arrFirm[1];

   $curMinor = (strlen($curMinor) < 2)? "0" . $curMinor : $curMinor;
	$firmware = $curMajor . "." . $curMinor . "_" . $curDate;
}else{
	$error = $result[1];
}

$isUpdate = "0";
$lastVersion = $Lang["Unknown"];
$parser = new xmlParser("https://www.samsungsmartcam.com/firmware/firmware.xml");
if($parser->result){
	$models = $parser->getData("FIRMWARE/MODEL");
	if($models != null && is_array($models)){
		foreach($models as $model){
//			if($model["NAME"] == "SNH-P6410BN"){
			if($model["NAME"] == "SNH-C6111BN"){
				$lastMajor = trim($model["MAJOR"]);
				$lastMinor = trim($model["MINOR"]);
				$lastMinor = (strlen($lastMinor) < 2)? $lastMinor . "0" : $lastMinor;
				$lastDate = trim($model["DATE"]);
				$lastVersion = $lastMajor . "." . $lastMinor . "_" . $lastDate;
				break;
			}
		}

		if((intval($lastMajor) > intval($curMajor)) ||
		   (intval($lastMajor) >= intval($curMajor)) && (intval($lastMinor) > intval($curMinor)) ||
		   (intval($lastMajor) >= intval($curMajor)) && (intval($lastMinor) >= intval($curMinor)) && (intval($lastDate) > intval($curDate))){
			$isUpdate = "1";
		}
	}
}
?>

<? include $_SERVER["DOCUMENT_ROOT"] . "/common/html_head.php"; ?>
	<script type="text/javascript">
		var isUpdate = '<?=$isUpdate?>';

		if('<?=$error?>' != ""){
			alert('<?=$error?>');
		}

		$(document).ready(function(){
			$("#camera_name").attr("readonly", true);
			$("#serial_number").attr("readonly", true);
			$("#firmware").attr("readonly", true);

/*			if(isUpdate == "0"){
				$("#upgrade").attr("disabled", true);
			}
*/
			$("#camera_name").val('<?=$device?>');
	   		$("#serial_number").val('<?=$serial?>');
	   		$("#firmware").val('<?=$firmware?>');
		});

	   	function upgradeFirmware(){
		   	if(confirm('<?=$Lang["Do you want to update to a new firmware?"]?>')){
		   		$.post("/classes/class_admin_firmware_dev.php", {data: "FIRMWARE"}, "", "text");
		   		alert('<?=$Lang["Upgrading to a new firmware. Do not unplug the camera."]?>' + "\n" +
				   	  '<?=$Lang["Camera will re-connect after firmware is updated completely."]?>' + "\n" +
		   			  '<?=$Lang["Firmware update process will take approximately 10 minutes."]?>');
		   		moveToPage('pages/camera_login.php');
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
					<!-- s:Firmware Upgrade -->
					<h2 class="cl_tit"><?=$Lang["Update Firmware"]?></h2>
					<div id="ad" class="cl_gBox">
						<div class="cl_cBox nbd">
							<dl class="frm floatClear">
								<dt><?=$Lang["Camera Name"]?> : </dt>
								<dd><input name="" type="text" id="camera_name" title="txtData" value="" readonly="readonly" /></dd>
								<dt><?=$Lang["Serial Number"]?> : </dt>
								<dd><input type="text" title="txtData" id="serial_number" value="" readonly="readonly" /></dd>
								<dt><?=$Lang["Current Camera Firmware"]?> : </dt>
								<dd><input type="text" title="txtData" id="firmware" value="" readonly="readonly" /></dd>
							</dl>
						</div>
						<div class="cl_btnBox">
							<dl class="frm floatClear">
								<dt><?=$Lang["Latest firmware on the server"]?> : </dt>
								<dd><input type="text" title="txtData" id="last_version" value="<?=$lastVersion?>" readonly="readonly" /></dd>
							</dl>
							<button type="button" id="upgrade" class="btnTxt bType1" onclick="upgradeFirmware();"><?=$Lang["Update Firmware"]?></button>
						</div>
					</div>
					<!-- e:Firmware Upgrade -->
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