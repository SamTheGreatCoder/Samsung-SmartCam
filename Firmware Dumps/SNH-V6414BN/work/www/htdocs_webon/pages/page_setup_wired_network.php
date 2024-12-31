<?php
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";
require_once $_SERVER["DOCUMENT_ROOT"] . "/resources/languages/Language.php";

define("OFF_DNS"		, 65);
define("OFF_NETWORK"	, 230);
define("OFF_GATEWAY"	, 1588);

$_SESSION["GROUP"] = "Setup";
$_SESSION["PAGE"] = "setup_wired_network";

$dhcp = 0; $dns1 = array(); $dns2 = array(); $ipAddress = array();
$subnet = array(); $prefix = array(); $gateway = ""; $error = "";
$status = array();
$network = array();
$token_eth  = ""; $token_wlan  ="";

/*
if(strcmp("SEC-6410", CAMERA_MODEL) != 0 ){
	$result = requestToCamera(CMD_NETWORK_CONFIGURATION, ACTION_GET, TYPE_REQUEST, null);
	if($result[0] == "OK"){
		$dhcp = $result[1][OFF_NETWORK+84];
		$dns1[0] = byte2str($result[1], OFF_DNS+2, 40);				//Static
		$dns1[1] = byte2str($result[1], OFF_DNS+84, 40);			//DHCP
		$dns2[0] = byte2str($result[1], OFF_DNS+43, 40);			//Static
		$dns2[1] = byte2str($result[1], OFF_DNS+125, 40);			//DHCP

		$ipAddress[0] = byte2str($result[1], OFF_NETWORK+85, 16);	//Static
		$ipAddress[1] = byte2str($result[1], OFF_NETWORK+105, 16);	//DHCP
		$prefix[0] = byte2int($result[1], OFF_NETWORK+101);			//Static
		$prefix[1] = byte2int($result[1], OFF_NETWORK+121);			//DHCP
		for($i=0; $i<2; $i++){
			if($prefix[$i] == 8){
				$subnet[$i] = "255.0.0.0";
			}else if($prefix[$i] == 16){
				$subnet[$i] = "255.255.0.0";
			}else if($prefix[$i] == 24){
				$subnet[$i] = "255.255.255.0";
			}else if($prefix[$i] == 32){
				$subnet[$i] = "255.255.255.255";
			}else{
				$subnet[$i] = "0.0.0.0";
			}
		}
		$gateway = byte2str($result[1], OFF_GATEWAY, 16);
	}else{
		$error = $result[1];
	}
}else{
	$result = requestToCamera(getNewCmd(CMD_NETWORK_CONFIGURATION_V2), ACTION_GET, TYPE_REQUEST, null);
	if($result[0] == "OK"){
		$network = $result[1];
		$token_eth  = byte2str($network, 230, 64);
		$token_wlan = byte2str($network, 617, 64);
	}else{
		$error = $result[1];
	}

	$result = requestToCamera(CMD_NETWORK_STATUS, ACTION_GET, TYPE_REQUEST, null);
	if($result[0] == "OK"){
		$status = $result[1];
		$token = byte2str($status, 0, 64);
		if(token == $token_wlan){
			moveToPage("pages/page_setup_wired_network.php?login=true#");
			return;
		}
	}else{
		$error = $result[1];
	}
}
*/

if(CheckModelName_SNH('WR15'))
{
	$result = requestToCamera(CMD_NETWORK_CONFIGURATION, ACTION_GET, TYPE_REQUEST, null);
	if($result[0] == "OK")
	{
		$dhcp = $result[1][OFF_NETWORK+84];
		$dns1[0] = byte2str($result[1], OFF_DNS+2, 40);				//Static
		$dns1[1] = byte2str($result[1], OFF_DNS+84, 40);			//DHCP
		$dns2[0] = byte2str($result[1], OFF_DNS+43, 40);			//Static
		$dns2[1] = byte2str($result[1], OFF_DNS+125, 40);			//DHCP

		$ipAddress[0] = byte2str($result[1], OFF_NETWORK+85, 16);	//Static
		$ipAddress[1] = byte2str($result[1], OFF_NETWORK+105, 16);	//DHCP
		$prefix[0] = byte2int($result[1], OFF_NETWORK+101);			//Static
		$prefix[1] = byte2int($result[1], OFF_NETWORK+121);			//DHCP
		for($i=0; $i<2; $i++)
		{
			if($prefix[$i] == 8){
				$subnet[$i] = "255.0.0.0";
			}else if($prefix[$i] == 16){
				$subnet[$i] = "255.255.0.0";
			}else if($prefix[$i] == 24){
				$subnet[$i] = "255.255.255.0";
			}else if($prefix[$i] == 32){
				$subnet[$i] = "255.255.255.255";
			}else{
				$subnet[$i] = "0.0.0.0";
			}
		}
		$gateway = byte2str($result[1], OFF_GATEWAY, 16);
	}
	else
	{
		$error = $result[1];
	}
}
else //WR3.0 and WR4.0
{
	$result = requestToCamera(getNewCmd(CMD_NETWORK_CONFIGURATION_V2), ACTION_GET, TYPE_REQUEST, null);
	if($result[0] == "OK")
	{
		$network = $result[1];
		$token_eth  = byte2str($network, 230, 64);
		$token_wlan = byte2str($network, 617, 64);
	}
	else
	{
		$error = $result[1];
	}

	$result = requestToCamera(CMD_NETWORK_STATUS, ACTION_GET, TYPE_REQUEST, null);
	if($result[0] == "OK")
	{
		$status = $result[1];
		$token = byte2str($status, 0, 64);
		if(token == $token_wlan)
		{
			moveToPage("pages/page_setup_wired_network.php?login=true#");
			return;
		}
	}
	else
	{
		$error = $result[1];
	}
}

?>

<? include $_SERVER["DOCUMENT_ROOT"] . "/common/html_head.php"; ?>

	<script type="text/javascript">
		var OFF_DNS 			= 65;
		var OFF_DNS_MANUAL_1	= 67;
		var OFF_DNS_MANUAL_2	= 108;
		var OFF_DNS_DYNAMIC_1	= 149;
		var OFF_DNS_DYNAMIC_2	= 190;

		var OFF_NETWORK 		= 230;
		var OFF_GATEWAY 		= 1588;
		var OFF_GATEWAY_V2 		= 4100;
		var OFF_NETWORK_CHANGED	= 11709;

		var ipAddress = new Array(2);
		var subnet = new Array(2);
		var isChanged = false;
		var network = '<?=implode(",", $network)?>'.split(",");
		var netInfo = {};

		if('<?=$error?>' != ""){
			alert('<?=$error?>');
		}

		function is6410(){
			return 'SEC-6410'=='<?=CAMERA_MODEL?>';
		}

		$(document).ready(function(){
		<? if(!CheckModelName_SNH('WR15'))  { ?>
				netInfo['ip_mode'] = network[OFF_NETWORK+84];
				netInfo['ip_addr'] = byte2str(network, OFF_NETWORK+85, 16);

				<? if(CheckModelName_SNH('WR40'))  { ?>
					netInfo['subnet'] = getSubnet(network[OFF_NETWORK+101]);
				<? } else { ?>
					netInfo['subnet'] = getSubnet(byte2int(network, OFF_NETWORK+101));
				<? } ?>
				netInfo['gateway'] = byte2str(network, OFF_GATEWAY_V2, 16);
				netInfo['manual_first_dns'] = byte2str(network, OFF_DNS_MANUAL_1, 40);
				netInfo['manual_second_dns'] = byte2str(network, OFF_DNS_MANUAL_2, 40);
				netInfo['dynamic_first_dns'] = byte2str(network, OFF_DNS_DYNAMIC_1, 40);
				netInfo['dynamic_second_dns'] = byte2str(network, OFF_DNS_DYNAMIC_2, 40);

				var ipMode = netInfo['ip_mode'];
				$("input:radio[name=IPMode]").filter("input[value=" + ipMode + "]").attr("checked", "checked");

				if(ipMode == '1')
				{
					$("#ip_address").val(byte2str(network, OFF_NETWORK+105, 16));

					var mSubMaskData = getSubnet(byte2int(network, OFF_NETWORK+121));
					if(mSubMaskData != '' || mSubMaskData != null)
					{
						$("#subnet_mask").val(mSubMaskData);
					}
					$("#pref_dns_serv").val(netInfo['dynamic_first_dns']);
		   		$("#alter_dns_serv").val(netInfo['dynamic_second_dns']);
		   		disableControl();
				}
				else
				{
					$("#ip_address").val(netInfo['ip_addr']);
					$("#subnet_mask").val(netInfo['subnet']);
					$("#pref_dns_serv").val(netInfo['manual_first_dns']);
			   	$("#alter_dns_serv").val( netInfo['manual_second_dns']);
				}
				$("#gateway").val(netInfo['gateway']);
		<? } else { ?>
				ipAddress[0] = '<?=$ipAddress[0]?>';
	   			ipAddress[1] = '<?=$ipAddress[1]?>';
	   			subnet[0] = '<?=$subnet[0]?>';
	   			subnet[1] = '<?=$subnet[0]?>';

	   			$("input:radio[name=IPMode]").filter("input[value=" + <?=$dhcp?> + "]").attr("checked", "checked");
		   		$("#ip_address").val(ipAddress[<?=$dhcp?>]);
		   		$("#subnet_mask").val(subnet[<?=$dhcp?>]);
		   		$("#gateway").val('<?=$gateway?>');
		   		$("#pref_dns_serv").val('<?=$dns1[0]?>');
		   		$("#alter_dns_serv").val('<?=$dns2[0]?>');

		   		if('<?=$dhcp?>' == '1')
		   		{
		   			disableControl();
		   		}
		<? } ?>
		});
//			if(is6410()){
//				netInfo['ip_mode'] = network[OFF_NETWORK+84];
//				netInfo['ip_addr'] = byte2str(network, OFF_NETWORK+85, 16);
////			netInfo['subnet'] = getSubnet(byte2int(network, OFF_NETWORK+101));
//				netInfo['subnet'] = getSubnet(network[OFF_NETWORK+101]);
//				netInfo['gateway'] = byte2str(network, OFF_GATEWAY_V2, 16);
//				netInfo['manual_first_dns'] = byte2str(network, OFF_DNS_MANUAL_1, 40);
//				netInfo['manual_second_dns'] = byte2str(network, OFF_DNS_MANUAL_2, 40);
//				netInfo['dynamic_first_dns'] = byte2str(network, OFF_DNS_DYNAMIC_1, 40);
//				netInfo['dynamic_second_dns'] = byte2str(network, OFF_DNS_DYNAMIC_2, 40);

/*				var ipMode = netInfo['ip_mode'];
				$("input:radio[name=IPMode]").filter("input[value=" + ipMode + "]").attr("checked", "checked");

				if(ipMode == '1'){
					$("#ip_address").val(byte2str(network, OFF_NETWORK+105, 16));

					var mSubMaskData = getSubnet(byte2int(network, OFF_NETWORK+121));
					if(mSubMaskData != '' || mSubMaskData != null){
						$("#subnet_mask").val(mSubMaskData);
					}
					$("#pref_dns_serv").val(netInfo['dynamic_first_dns']);
			   		$("#alter_dns_serv").val(netInfo['dynamic_second_dns']);
			   		disableControl();
				}else{
					$("#ip_address").val(netInfo['ip_addr']);
					$("#subnet_mask").val(netInfo['subnet']);
					$("#pref_dns_serv").val(netInfo['manual_first_dns']);
			   		$("#alter_dns_serv").val( netInfo['manual_second_dns']);
				}
				$("#gateway").val(netInfo['gateway']); */
/*			}else{
				ipAddress[0] = '<?=$ipAddress[0]?>';
	   			ipAddress[1] = '<?=$ipAddress[1]?>';
	   			subnet[0] = '<?=$subnet[0]?>';
	   			subnet[1] = '<?=$subnet[0]?>';

	   			$("input:radio[name=IPMode]").filter("input[value=" + <?=$dhcp?> + "]").attr("checked", "checked");
		   		$("#ip_address").val(ipAddress[<?=$dhcp?>]);
		   		$("#subnet_mask").val(subnet[<?=$dhcp?>]);
		   		$("#gateway").val('<?=$gateway?>');
		   		$("#pref_dns_serv").val('<?=$dns1[0]?>');
		   		$("#alter_dns_serv").val('<?=$dns2[0]?>');

		   		if('<?=$dhcp?>' == '1'){
		   			disableControl();
		   		}
			}*/
//		});

function changeIPMode(mode)
{
	if(mode == "0")
	{
		$("#ip_address").val(ipAddress[0]);
		$("#subnet_mask").val(subnet[0]);
		enableControl();
	}
	else
	{
		$("#ip_address").val(ipAddress[1]);
		$("#subnet_mask").val(subnet[1]);
		disableControl();
	}
}

function enableControl()
{
	$("#ip_address").removeAttr("disabled");
	$("#subnet_mask").removeAttr("disabled");
	$("#gateway").removeAttr("disabled");
	$("#pref_dns_serv").removeAttr("disabled");
	$("#alter_dns_serv").removeAttr("disabled");
}

function disableControl()
{
	$("#ip_address").attr("disabled", true);
	$("#subnet_mask").attr("disabled", true);
	$("#gateway").attr("disabled", true);
	$("#pref_dns_serv").attr("disabled", true);
	$("#alter_dns_serv").attr("disabled", true);
}

function saveData()
{
/*	if(is6410())
	{
		saveData6410();
		return;
	}
*/
	<? if(!CheckModelName_SNH('WR15')) { ?>
		saveData6410();
		return;
	<? } else { ?>

	var ipMode = "0";
	$("input:radio[name=IPMode]:checked").each(function(){
		ipMode = this.value;
	});

	if(ipMode == "0"){
		if(!checkIPAddress(document.getElementById("ip_address"), false)){
		return;
	}
	if(!checkIPAddress(document.getElementById("subnet_mask"), false)){
		return;
	}
	if(!checkIPAddress(document.getElementById("gateway"), false)){
		return;
	}
	if(!checkIPAddress(document.getElementById("pref_dns_serv"), false)){
		return;
	}
	if(!checkIPAddress(document.getElementById("alter_dns_serv"), false)){
		return;
	}
	}

	isChanged = false;
	if('<?=$dhcp?>' != ipMode){isChanged = true;}
	if(ipAddress[0] != $("#ip_address").val()){isChanged = true;}
	if(subnet[0] != $("#subnet_mask").val()){isChanged = true;}
	if('<?=$gateway?>' != $("#gateway").val()){isChanged = true;}
	if('<?=$dns1[0]?>' != $("#pref_dns_serv").val()){isChanged = true;}
	if('<?=$dns2[0]?>' != $("#alter_dns_serv").val()){isChanged = true;}

	if(isChanged)
	{
		showProgress('<?=$Lang["Updating the camera"]?>' + "...");

		var sendData = "IPCV0.6;" + '<?=implode(",", $result[1])?>' + ";";
		sendData += ipMode + ";";
		sendData += $("#ip_address").val() + ";";
		sendData += $("#subnet_mask").val() + ";";
		sendData += $("#gateway").val() + ";";
		sendData += $("#pref_dns_serv").val() + ";";
		sendData += $("#alter_dns_serv").val();

	   $.post("/classes/class_setup_wired_network.php", {data: sendData}, returnSetMessage, "text");
	}
	<? } ?>
}

function saveData6410()
{
	var ipMode = "0";
	$("input:radio[name=IPMode]:checked").each(function(){
		ipMode = this.value;
   	});

	var first_dns = $("#pref_dns_serv").val();
	var second_dns = $("#alter_dns_serv").val();
	var ipaddress = $("#ip_address").val();
	var subnet = $("#subnet_mask").val();
	var gateway = $("#gateway").val();

	var isChanged = false;
	if(netInfo['ip_mode'] != ipMode){isChanged = true;}
	if(netInfo['ip_addr'] != ipaddress){isChanged = true;}
	if(netInfo['subnet'] != subnet){isChanged = true;}
	if(netInfo['gateway'] != gateway){isChanged = true;}
	if(netInfo['manual_first_dns'] != first_dns){isChanged = true;}
	if(netInfo['manual_second_dns'] != second_dns){isChanged = true;}

	if(isChanged)
	{
		network[OFF_NETWORK + 84] = parseInt(ipMode);
		if(parseInt(ipMode) == 0)
		{ //Manual
			str2byte(network, OFF_DNS_MANUAL_1, 40, first_dns);
			str2byte(network, OFF_DNS_MANUAL_2, 40, second_dns);
			str2byte(network, OFF_NETWORK+85, 16, ipaddress);
			str2byte(network, OFF_GATEWAY_V2, 16, gateway);
		}
		var sendData = "IPCV0.7;" + network.join(",");
		$.post("/classes/class_setup_wired_network.php", {data: sendData}, returnSetMessage, "text");
	}
}

function returnSetMessage(resp)
{
	var recvData = resp.split(";");
	hideProgress();

	if(recvData[0] == "OK")
	{
		alert('<?=$Lang["Wired network information changed"]?>' + '\n' +  '<?=$Lang["Please reconnect to the camera"]?>');
		popupReConnect();
	}
	else
	{
		alert('<?=$Lang["Failed to save."]?>' + "-" + recvData[1]);
	}
}

function popupReConnect()
{
	parent.close();
	window.close();
	self.close();

	var ipAddr = $("#ip_address").val();
	window.open("http://" + ipAddr, "");
	//location.href="http://" + ipAddr;
}

function checkIPAddress(obj, blank)
{
	var ptnIPAddress = /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/;
	var value = obj.value;
	if(!blank && value == "")
	{
		alert('<?=$Lang["Enter the address."]?>');
		obj.focus();
		return false;
	}

	var result = value.match(ptnIPAddress);
	if(result != null)
	{
		var arrAddr = value.split(".");
		for(var i=0; i<arrAddr.length; i++)
		{
			if(parseInt(arrAddr[i]) > 255)
			{
				alert('<?=$Lang["The IP Address should be between 0 and 255."]?>');
				obj.value = "";
		   		obj.focus();
				return false;
			}
			if(i == (arrAddr.length - 1)){
				return true;
			}
		}
	}
	alert('<?=$Lang["Incorrect address."]?>');
	obj.value = "";
	obj.focus();
	return false;
}

function getSubnet(arg)
{
	var val = parseInt(arg);
	var mSubMask = new Array();
	var returnVal = '0.0.0.0';

	if(val > 0)
	{
		if(val >= 32)
		{
			returnVal = "255.255.255.255";
		}
		else
		{
			//서브넷 마스크 구하기 ////////////////////////////////////////////////////////////////
			var a = Math.floor(val/8);
			var b = a*8;
			var c = val-b;
			var d = 8-c;
			var e = 1;
			for(var i=0; i<d; i++) e = e*2;
			var f = 256 - e;
			switch(a){
			case 0:
				mSubMask[0] = f;
				mSubMask[1] = "0";
				mSubMask[2] = "0";
				mSubMask[3] = "0";
				break;
			case 1:
				mSubMask[0] = "255";
				mSubMask[1] = f;
				mSubMask[2] = "0";
				mSubMask[3] = "0";
				break;
			case 2:
				mSubMask[0] = "255";
				mSubMask[1] = "255";
				mSubMask[2] = f;
				mSubMask[3] = "0";
				break;
			case 3:
				mSubMask[0] = "255";
				mSubMask[1] = "255";
				mSubMask[2] = "255";
				mSubMask[3] = f;
				break;
			}
			returnVal = mSubMask[0] + "." + mSubMask[1] + "." + mSubMask[2] + "." + mSubMask[3];
		}
	}
	return returnVal;
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
					<h2 class="cl_tit"><?=$Lang["Wired Network"]?></h2>
					<div id="nwks1" class="cl_gBox">
						<div class="cl_cBox nbd">
							<input name="IPMode" type="radio" value="1" id="wnt1" onclick="changeIPMode('1');"/><label for="wnt1"><?=$Lang["Dynamic IP Address"]?></label>
							<input name="IPMode" type="radio" value="0" id="wnt2" onclick="changeIPMode('0');"/><label for="wnt2"><?=$Lang["Static IP Address"]?></label>
						</div>
						<div class="cl_cBox">
							<dl class="floatClear">
								<dt><label for="ip_address"><?=$Lang["IP Address"]?></label></dt>
								<dd>
									<input type="text" id="ip_address" class="input_w1" onkeyup="checkNumDotPattern(this);"/>
								</dd>
								<dt><label for="sbm"><?=$Lang["Subnet Mask"]?></label></dt>
								<dd>
									<input type="text" id="subnet_mask" class="input_w1" onkeyup="checkNumDotPattern(this);"/>
								</dd>
								<dt><label for="gtw"><?=$Lang["Gateway"]?></label></dt>
								<dd>
									<input type="text" id="gateway" class="input_w1" onkeyup="checkNumDotPattern(this);"/>
								</dd>
							</dl>
						</div>
						<div class="cl_cBox">
							<dl class="floatClear">
								<dt><label for="dns1"><?=$Lang["Primary DNS Server"]?></label></dt>
								<dd>
									<input type="text" id="pref_dns_serv" class="input_w1" onkeyup="checkNumDotPattern(this);"/>
								</dd>
								<dt><label for="dns2"><?=$Lang["Secondary DNS Server"]?></label></dt>
								<dd>
									<input type="text" id="alter_dns_serv" class="input_w1" onkeyup="checkNumDotPattern(this);"/>
								</dd>
							</dl>
						</div>
						<div class="cl_btnBox">
							<button type="button" class="btnTxt bType1" onclick="saveData();"><?=$Lang["Apply"]?></button>
						</div>
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
