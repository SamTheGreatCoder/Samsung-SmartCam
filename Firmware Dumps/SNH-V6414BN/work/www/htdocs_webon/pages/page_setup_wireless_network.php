<?php
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";
require_once $_SERVER["DOCUMENT_ROOT"] . "/resources/languages/Language.php";

define("OFF_WLAN", 909);

$_SESSION["GROUP"] = "Setup";
$_SESSION["PAGE"] = "setup_wireless_network";

//ini_set("max_execution_time", 3);
//$scanList = requestToCamera(getNewCmd(CMD_WIRELESS_SCANNING), ACTION_GET, TYPE_REQUEST, null);
//sleep(1);

$result = requestToCamera(getNewCmd(CMD_NETWORK_CONFIGURATION), ACTION_GET, TYPE_REQUEST, null);
$useWLAN = 0; $currentAP = ""; $currentPW = ""; $error = "";
$network = array();
$wireless = null;
$wlan = null;
$token_wlan="";

if($result[0] == "OK"){
	//if(strcmp("SEC-6410", CAMERA_MODEL) != 0){ //기존
	if(CheckModelName_SNH('WR15')) {
		// 	$useWLAN = $result[1][OFF_WLAN+64];
		$useWLAN = $result[1][OFF_WLAN+551]; //20120207_lcy changed position
		$currentAP = byte2str($result[1], (OFF_WLAN+359), 64);
		if($currentAP == "" || $useWLAN == 0){
			$currentAP = $Lang["Not connected."];
		}
		$currentPW = byte2str($result[1], (OFF_WLAN+423), 128);
	}else{
		$network = $result[1];
		$token_wlan = array_slice($network, 617, 64);
		$useWLAN = $network[681];

		$result = requestToCamera(CMD_NETWORK_IF_EXTENSION, ACTION_GET, TYPE_REQUEST, null);
		if($result[0] == "OK"){
			$wireless = $result[1];
		}else{
			$error = $result[1];
		}

		$result = requestToCamera(CMD_NETWORK_DOT11_STATUS, ACTION_GET, TYPE_REQUEST, $token_wlan);
		if($result[0] == "OK"){
			$wlan = $result[1];
			$currentAP = rawurlencode(byte2str($wlan, 0, 128));

			if($currentAP == "" || $useWLAN == 0){
				$currentAP = $Lang["Not connected."];
			}
		}else{
			$error = $result[1];
		}

		$result[1] = array(0, 0, 0, 0);
	}
}else{
	$error = $result[1];
}

?>

<? include $_SERVER["DOCUMENT_ROOT"] . "/common/html_head.php"; ?>

	<script type="text/javascript">
		var signal = new Array(
			"/resources/images/network_signal_00.gif",
			"/resources/images/network_signal_01.gif",
			"/resources/images/network_signal_02.gif",
			"/resources/images/network_signal_03.gif",
			"/resources/images/network_signal_04.gif",
			"/resources/images/network_signal_05.gif"
		);

		var OFF_WLAN 			= 909;
		var OFF_CURRENT_WLAN	= 1268;
		var OFF_CURRENT_WLAN_PW	= 1332;
		var OFF_NETWORK_CHANGED	= 11709;

		var OFF_WLAN_V2 					= 0;
		var OFF_CURRENT_WLAN_V2				= 64;
		var OFF_CURRENT_WLAN_V2_MODE		= 192;
		var OFF_CURRENT_WLAN_V2_ENABLE		= 681; // CMD_NETWORK_CONFIGURATION_V2
		var OFF_CURRENT_WLAN_V2_SEC_MODE	= 325;
		var OFF_CURRENT_WLAN_V2_PW			= 327;

		var selectAP;
		var useWlan = '<?=$useWLAN?>';
		var currentPW = '<?=$currentPW?>';
		var apList = new Array();
		var scanCount = 0;
		var changeAP = false;
		var currentWlan="undefined"; //2012.6.12.pys

		var network = '<?=implode(",", $network)?>'.split(",");
		var wireless = '<?=implode(",", $wireless)?>'.split(",");

		if('<?=$error?>' != ""){
			alert('<?=$error?>');
		}

		$(document).ready(function(){
			$("#current_wlan").attr("readonly", true);
			$("#select_wlan").attr("readonly", true);
			$("#wlan_password").attr("disabled", true);
			$("#other_wlan_password").attr("disabled", true);

			$("input:radio[name=wlan]").filter("input[value=" + parseInt(useWlan) + "]").attr("checked", "checked");
			$("#current_wlan").val(decodeURIComponent('<?=$currentAP?>'));

	   		if(useWlan == "1"){
	   			scanAPList();
	   			currentWlan = decodeURIComponent('<?=$currentAP?>'); //2012.6.12.pys
	   		}else{
	   			otherNetEnable(1);
	   		}
		});

		function scanAPList(){
			useWlan = "1";
			if(scanCount >= 2){
				scanCount = 0;
				hideProgress();
				return;
			}
			scanCount++;

			showProgress('<?=$Lang["Searching for a wireless network"]?>' + "...");
			$.post("/classes/class_setup_wireless_network.php", {data: "SCAN; "}, returnScanMessage, "text");
		}
		function returnScanMessage(resp){
			var recvData = resp.split(";");
			apList = new Array();

			if(recvData[0] == "OK"){
				for(var i=1; i<recvData.length; i++){
					apList[i-1] = recvData[i];
				}
				var data = apList[0].split(",");
				if(data[0] == undefined || data[1] == undefined || data[2] == undefined){
					reScanAPList()
					return;
				}else{
					createAPList();
					hideProgress();
				}
				scanCount = 0;
			}else{
				if(recvData[1] == undefined || recvData[1] == ""){
					reScanAPList();
					return;
				}else{
					hideProgress();
					alert(recvData[1]);
				}
			}
		}

		function reScanAPList(){
			sleep(2000);
			scanAPList();
		}

		function createAPList(){
			var html = "";
			document.getElementById("ap_list").innerHTML = html;
			if(apList != null && apList.length > 0){
				for(var i=0; i<apList.length; i++){
					var data = apList[i].split(",");
					if(data[0] != undefined && data[1] != undefined && data[2] != undefined){
						html += "<li>";
						//2012.6.12.pys
						var apName = decodeURIComponent(data[0]);
						if(currentWlan == apName){
							html += "<div class='wn' id='wn_" + i + "' onclick='changeCurrentWlan(" + i + ");'>" + "<font color=#000000><i><b>" + apName + "</b></i></font>" + "</div>";
						}else{
							html += "<div class='wn' id='wn_" + i + "' onclick='changeCurrentWlan(" + i + ");'>" + apName + "</div>";
						}

						if(data[1] == "open" || data[1] == "OPEN"){
							html += "<span class='prt'><img src='/resources/images/icon_network_protect_off.gif' width='13' height='13'/></span>";
						}else{
							html += "<span class='prt'><img src='/resources/images/icon_network_protect_on.gif' width='13' height='13'/></span>";
						}
						if(parseInt(data[2]) <= 5){
							html += "<span class='sgn'><img src='" + signal[parseInt(data[2])] + "' width='19' height='13'/></span>";
						}else{
							html += "<span class='sgn'><img src='" + signal[0] + "' width='19' height='13'/></span>";
						}
						html += "</li>";
					}
				}
			}
			document.getElementById("ap_list").innerHTML = html;

			otherNetEnable(0);
	   	}

		function deleteAPList(){
			useWlan = "0";
			$.post("/classes/class_setup_wireless_network.php", {data: "SCAN; "}, "", "text");
			sleep(1000);
			$("#select_wlan").val("");
			$("#wlan_password").val("");
			$("#wlan_password").attr("disabled", true);

			otherNetEnable(1);
	   	}

	   	function changeCurrentWlan(idx){
		   	if(useWlan == "1"){
		   		selectAP = apList[idx];
		   		if(selectAP != null && selectAP != ""){
			   		var data = selectAP.split(",");
			   		$("#select_wlan").val(decodeURIComponent(data[0]));
			   		if($("#current_wlan").val() == $("#select_wlan").val()){
			   			$("#wlan_password").val(currentPW);
			   		}else{
			   			$("#wlan_password").val("");
			   		}
			   		if(data[1] != "open" && data[1] != "OPEN"){
			   			$("#wlan_password").removeAttr("disabled");
			   		}else{
			   			$("#wlan_password").attr("disabled", true);
			   		}

			   		//2012.6.12.pys
			   		if(apList != null && apList.length > 0){
						for(var i=0; i<apList.length; i++){
							var data = apList[i].split(",");
							if(currentWlan == data[0]){
								//document.getElementById("wn_"+idx).innerHTML = "<font color=#000000><i><b>" + data[0] +" </b></i></font>";
							}else{
								if(idx == i){
									document.getElementById("wn_"+idx).setAttribute("class", "wn2");
								}else{
									document.getElementById("wn_"+i).setAttribute("class", "wn");
								}
							}
						}
					}
		   		}
		   	}
	   	}

	   	function is6410(){
			return 'SEC-6410'=='<?=CAMERA_MODEL?>';
		}

function saveData(){
/*			if(is6410()){
	saveData6410();
	return;
}
*/
<? if(!CheckModelName_SNH('WR15')) { ?>
		saveData6410();
		return;
<? } else { ?>
		changeAP = false;
		var sendData = "SET;" + '<?=implode(",", $result[1])?>' + ";" + useWlan + ";";

		if(useWlan == "0")
		{
			if('<?=$useWLAN?>' == "1")
			{ //Wireless On -> Off
				sendData += " ; ; ";
				changeAP = true;
			}
		}
		else
		{
			var obj = document.getElementsByName("other_net");
			if(obj[0].checked == true)
			{
				var security = document.getElementsByName("other_security");
				var securityVal = "OPEN";
	  			for(var i=0; i<security.length;i++)
	  			{
	  				if(security[i].checked == true)
	  				{
	  					securityVal = security[i].value;
	  					break;
	  				}
	  			}

			  	if($("#other_select_wlan").val() == "")
			  	{
					alert("<?=$Lang["Enter the SSID."]?>");
					return;
				}
				else if(securityVal != "OPEN" && $("#other_wlan_password").val() == "")
				{
					alert("<?=$Lang["Enter the password."]?>");
   				return;
				}

		 		sendData += securityVal + ";";
   			sendData += $("#other_select_wlan").val() + ";";

   			if($("#other_wlan_password").val() == "")
   			{
   				sendData += " ";
   			}
   			else
   			{
   				sendData += $("#other_wlan_password").val();
   			}

   			changeAP = true;
			}
			else
			{
				if(selectAP != null && selectAP != "")
				{
					var data = selectAP.split(",");
	   			if(data[1] != "open" && data[1] != "OPEN" && $("#wlan_password").val() == "")
	   			{
	   				alert("<?=$Lang["Enter the password."]?>");
	   				return;
	   			}

	   			sendData += data[1] + ";";
	   			sendData += $("#select_wlan").val() + ";";

	   			if($("#wlan_password").val() == "")
	   			{
	   				sendData += " ";
	   			}
	   			else
	   			{
	   				sendData += $("#wlan_password").val();
	   			}

	   			changeAP = true;
				}
				else
				{
					alert("<?=$Lang["Select the AP."]?>");
				}
			}
		}

		if(changeAP)
		{
			showProgress("<?=$Lang["Updating the camera"]?>");
			$.post("/classes/class_setup_wireless_network.php", {data: sendData}, returnSetMessage, "text");
		}
<? } ?>
}
	   	function saveData6410(){

	   		//changeAP = false;

	   		if ($("input:radio[name=wlan]:checked").val() == "0") { // wireless unchecked
				str2byte(wireless, OFF_WLAN_V2, 64, "");
				network[OFF_CURRENT_WLAN_V2_ENABLE] = 0;
				str2byte(wireless, OFF_CURRENT_WLAN_V2, 128, "");
				wireless[OFF_CURRENT_WLAN_V2_MODE] = 1;
				wireless[OFF_CURRENT_WLAN_V2_SEC_MODE] = 0;
				str2byte(wireless, OFF_CURRENT_WLAN_V2_PW, 256, "");
				changeAP = true;
	   		} else { // wireless checked
	   			var obj = document.getElementsByName("other_net");
				str2byte(wireless, OFF_WLAN_V2, 64, '<?=byte2str($token_wlan,0,64)?>');

				if (obj[0].checked == true) {
					var security = document.getElementsByName("other_security");
					var securityVal = "OPEN";
					for ( var i = 0; i < security.length; i++) {
						if (security[i].checked == true) {
							securityVal = security[i].value;
							break;
						}
					}
					if ($("#other_select_wlan").val() == "") {
						alert("<?=$Lang["Enter the SSID."]?>");
						return;
					} else if (securityVal != "OPEN" && $("#other_wlan_password").val() == "") {
						alert("<?=$Lang["Enter the password."]?>");
						return;
					}

					//int2byte(wireless, 0, 0); // interface type

					//wireless[OFF_CURRENT_WLAN_V2_MODE] = 1; // Infrastructure
					network[OFF_CURRENT_WLAN_V2_ENABLE] = 1; // wlan enabled

					str2byte(wireless, OFF_CURRENT_WLAN_V2, 128, $("#other_select_wlan").val()); // ssid

					if (securityVal == "open" || securityVal == "OPEN") {
						wireless[OFF_CURRENT_WLAN_V2_SEC_MODE] = 0; // scurity mode
					} else if (securityVal == "WEP") {
						wireless[OFF_CURRENT_WLAN_V2_SEC_MODE] = 1; // scurity mode
					} else if (securityVal == "WPA") {
						wireless[OFF_CURRENT_WLAN_V2_SEC_MODE] = 2; // scurity mode
					}

					if ($("#other_wlan_password").val() == "") {
						str2byte(wireless, OFF_CURRENT_WLAN_V2_PW, 256, ""); // open
					} else {
						str2byte(wireless, OFF_CURRENT_WLAN_V2_PW, 256, $("#other_wlan_password").val()); // pw
					}

					changeAP = true;
				} else {
					if (selectAP != null) {
						var data = selectAP.split(",");
				   		if(data[1] != "open" && data[1] != "OPEN" && $("#wlan_password").val() == ""){
				   			alert("<?=$Lang["Enter the password."]?>");
				   			return;
				   		}
						network[OFF_CURRENT_WLAN_V2_ENABLE] = 1; // wlan enabled
						str2byte(wireless, OFF_CURRENT_WLAN_V2, 128, decodeURIComponent(data[0])); // ssid

						if (data[1] == "open" || data[1] == "OPEN") {
							wireless[OFF_CURRENT_WLAN_V2_SEC_MODE] = 0; // scurity mode
						} else if (data[1] == "WEP") {
							wireless[OFF_CURRENT_WLAN_V2_SEC_MODE] = 1; // scurity mode
						} else if (data[1] == "WPA") {
							wireless[OFF_CURRENT_WLAN_V2_SEC_MODE] = 2; // scurity mode
						}

						if ($("#wlan_password").val() == "") {
							str2byte(wireless, OFF_CURRENT_WLAN_V2_PW, 256, ""); // open
						} else {
							str2byte(wireless, OFF_CURRENT_WLAN_V2_PW, 256, $("#wlan_password").val()); // pw
						}
						changeAP = true;
					} else {
						alert("<?=$Lang["Select the AP."]?>");
					}
				}
	   		}
	   		if(changeAP){
				showProgress("<?=$Lang["Updating the camera"]?>");
				var sendData = "IPCV0.7;" + network.join(",") + ";" + wireless.join(",");
				$.post("/classes/class_setup_wireless_network.php", {data: sendData}, returnSetMessage, "text");
			}
		}
	   	function returnSetMessage(resp){
	   		hideProgress();
			if(resp.indexOf("OK", 0) == 0){
				if(changeAP){
					alert("<?=$Lang["Wireless network information changed"]?>" + '\n' + "<?=$Lang["Please reconnect to the camera"]?>");
					moveToPage('pages/camera_login.php');
				}else{
					alert("<?=$Lang["Changes saved."]?>");
				}
			}else{
				alert("<?=$Lang["Failed to save."]?> : "+resp);
			}
	   	}

		function selectOtherNet(){
	   		var obj = document.getElementsByName("other_net");
	   		if(obj[0].checked == true){
	   			document.getElementById("other_notuse").style.display = "none";
		   		document.getElementById("other_use").style.display = "block";
	   		}else{
	   			document.getElementById("other_notuse").style.display = "block";
		   		document.getElementById("other_use").style.display = "none";
	   		}
	   	}

	   	function otherNetEnable(enable){
	   		if(enable == 0){
	   			document.getElementById("other_net1").disabled=false;
				$("#other_security1").attr("disabled", false);
				$("#other_security2").attr("disabled", false);
				$("#other_security3").attr("disabled", false);
				$("#other_select_wlan").attr("disabled", false);

				var security = document.getElementsByName("other_security");
   		  		for(var i=0; i<security.length;i++){
   		  			if(security[i].checked == true){
   	   		  			if(security[i].value == "OPEN"){
   	   		  				$("#other_wlan_password").attr("disabled", true);
   	   		  			}else{
   	   		  				$("#other_wlan_password").attr("disabled", false);
   	   	   		  		}
   		  				break;
   		  			}
   		  		}
	   		}else{
	   			document.getElementById("other_net1").disabled=true;
				$("#other_security1").attr("disabled", true);
				$("#other_security2").attr("disabled", true);
				$("#other_security3").attr("disabled", true);
				$("#other_select_wlan").attr("disabled", true);
				$("#other_wlan_password").attr("disabled", true);

				$("#other_select_wlan").val("");
				$("#other_wlan_password").val("");

				//2012.6.12.pys
		   		if(apList != null && apList.length > 0){
					for(var i=0; i<apList.length; i++){
						document.getElementById("wn_"+i).setAttribute("class", "wn");
					}
				}
	   		}
	   	}

		function clickSecurity(val){
	   		if(val == "0"){
	   			$("#other_wlan_password").attr("disabled", true);
	   			$("#other_wlan_password").val("");
	   		}else{
	   			$("#other_wlan_password").attr("disabled", false);
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
					<!-- s:NetworkSetting -->
					<h2 class="cl_tit"><?=$Lang["Wireless Network"]?></h2>
					<div id="nwks2" class="cl_gBox">
						<div class="cl_cBox nbd">
							<p style="text-align:center">
								<input name="wlan" type="radio" value="1" id="wnt1" onclick="scanAPList();"/><label for="wnt1"><?=$Lang["Wireless On"]?></label>
								<input name="wlan" type="radio" value="0" id="wnt2" onclick="deleteAPList();"/><label for="wnt2"><?=$Lang["Wireless Off"]?></label>
							</p>
							<dl class="floatClear" style="overflow:hidden;">
								<dt><?=$Lang["Current AP"]?></dt>
								<dd>: <input type="text" title="txtData" id="current_wlan" value="" size="40" readonly="readonly" /></dd>
							</dl>
							<h3 class="ntl_h">
								<span class="wn"><?=$Lang["Wireless Network Name(SSID)"]?></span>
								<span class="prt"><?=$Lang["Protected"]?></span>
								<span class="sgn"><?=$Lang["Signal"]?></span>
							</h3>
							<ul class="ntl_list" id="ap_list">
								<!-- insert AP List -->
							</ul>
							<dl class="floatClear">
								<dt><input name="other_net" type="checkbox" value="1" id="other_net1" onclick="selectOtherNet();" style="height:20px;" /><?=$Lang["Other WiFi Networks"]?></dt>
								<dd></dd>
								<div id="other_notuse">
									<dt><?=$Lang["Network SSID"]?></dt>
									<dd>: <input type="text" title="txtData" id="select_wlan" value="" size="40" readonly="readonly" /></dd>
									<dt><label for="wlan_password"><?=$Lang["Password"]?></label></dt>
									<dd>: <input type="password" id="wlan_password" maxlength="128"/></dd>
								</div>

								<div id="other_use" style="display:none">
									<dt><?=$Lang["Security"]?></dt>
									<dd>
										<input name="other_security" type="radio" value="OPEN" id="other_security1" onclick="clickSecurity(0);" checked /><label for="other_security1"><?=$Lang["None"]?></label>
										<input name="other_security" type="radio" value="WEP" id="other_security2" onclick="clickSecurity(1);" /><label for="other_security2">WEP</label>
										<input name="other_security" type="radio" value="WPA" id="other_security3" onclick="clickSecurity(2);" /><label for="other_security3">WPA/WPA2 PSK</label>
									</dd>
									<dt><?=$Lang["Network SSID"]?></dt>
									<dd>: <input type="text" title="txtData" id="other_select_wlan" value="" size="40" style=" border:1px solid #ccc;"/></dd>
									<dt><?=$Lang["Password"]?></dt>
									<dd>: <input type="password" id="other_wlan_password" maxlength="128" style="height:20px;"/></dd>
								</div>
							</dl>
						</div>
						<div class="cl_btnBox"><button type="button" class="btnTxt bType1" onclick="saveData();"><?=$Lang["Apply"]?></button></div>
					</div>
					<!-- e:NetworkSetting -->
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