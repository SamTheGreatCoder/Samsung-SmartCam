<?php
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_menu.cgi');
require_once ('../language/language_network_ipfilter.cgi');

$classInstances= GetClassInstance('ipfilter');
$ipFiltering	= $classInstances['IPFilterConfiguration'];
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="kr" xml:lang="kr">
<head>
	<title>iPOLiS NETWORK CAMERA WEBVIEWER</title>
	<meta http-equiv="X-UA-Compatible" content="IE=Edge; requiresActiveX=true">
	<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
	<link rel="stylesheet" type="text/css" href="../css/techwin.css" />
	<style>
	#lnb-list {
		height:1100px;
	}
	table.data_table2 tbody td {
		color:#6d6d6d;
	}
	</style>
	<script type="text/javascript" src="../js/jquery-1.9.1.js"></script>
	<script type="text/javascript" src="../js/lnb.js"></script>
	<script type="text/javascript" src="../js/common_function.js"></script>
	<script type="text/javascript" language="javascript">
<?php
	if ($classInstances['Information']->dataInfo['PasswordCheck']['value'] == 1) {
?>
		window.location.href = '../pw_change.cgi';
<?php
	}
	else if ($classInstances['Information']->dataInfo['PasswordCheck']['value'] == 2) {
?>
		alert("<?php echo $msg_change_weak_password[$GLOBALS['LANGINDEX']]; ?>");
<?php
	}
?>
	$(document).ready(function(){ lnbonoff("lnb_network"); });
	
	var oldSelNo;
	var oldSelProtocol;
	var filter_ipv4_cnt = 0;
	var filter_ipv6_cnt = 0;
	var IsIncludedMyIPv4 = false;
	var IsIncludedMyIPv6 = false;
	var INVALID_PREFIX = 2;
	
	function OnClickApply()
	{
		var myiptemp = GetMyIPAddress("<?php echo $_SERVER['REMOTE_ADDR']; ?>");
		var ipType;
		var crash_result4 = new Array();
		var crash_result6 = new Array();
		(myiptemp.indexOf(".") == -1) ? ipType = 6 : ipType =4;
		var msg = "<DefaultPolicy>"+($('#filter_policy_deny').is(':checked') ? 0 : 1)+"</DefaultPolicy>";
		for (var index=0; index<10; ++index) {
			if($('tr').hasClass('filter_ipv4_list_'+index)) {
				if(!TypeCheck($('#filter_ipv4_prefix_'+index).val(), NUM))	{
					alert("<?php echo $msg_IPv4Prefix1to32[$GLOBALS['LANGINDEX']]; ?>");
					return;
				}
				if ($('#filter_ipv4_prefix_'+index).val() == '' || !CheckIPv4Prefix($('#filter_ipv4_prefix_'+index).val())) {
					alert("<?php echo $msg_IPv4Prefix1to32[$GLOBALS['LANGINDEX']]; ?>");
					return;
				}

				if (!CheckValidIPv4Address($('#filter_ipv4_addr_'+index).val()) ) {
					alert("<?php echo $msg_chkIPAddress[$GLOBALS['LANGINDEX']]; ?>");
					return;
				}
			}
		}

		for (var index=0; index<10; ++index) {
			if($('tr').hasClass('filter_ipv4_list_'+index)) {
				if (!CheckDuplicatedAddress('filter_ipv4', 10)) {
					alert("<?php echo $msg_IPv4AddressDuplicate[$GLOBALS['LANGINDEX']]; ?>");
					return;
				}
				if (ipType == 4) 
				crash_result4[index] = CheckFilteringCrashIPv4Address($('#filter_ipv4_enable_'+index).val(), $('#filter_ipv4_addr_'+index).val(), $('#filter_ipv4_prefix_'+index).val());
				
				msg += "<IPv4Filtering>";
				msg += "<Enabled>"+$('#filter_ipv4_enable_'+index).val()+"</Enabled>";
				msg += "<Address>"+$('#filter_ipv4_addr_'+index).val()+"</Address>";
				msg += "<Prefix>"+$('#filter_ipv4_prefix_'+index).val()+"</Prefix>";
				msg += "</IPv4Filtering>";
			}
		}
		
		for (var index=0; index<10; ++index) {
			if($('tr').hasClass('filter_ipv6_list_'+index)) {
				if (!TypeCheck($('#filter_ipv6_prefix_'+index).val(), NUM))	{
					alert("<?php echo $msg_IPv6Prefix1to128[$GLOBALS['LANGINDEX']]; ?>");
					return;
				}
				if ($('#filter_ipv6_prefix_'+index).val() == '' || !CheckIPv6Prefix($('#filter_ipv6_prefix_'+index).val())) {
					alert("<?php echo $msg_IPv6Prefix1to128[$GLOBALS['LANGINDEX']]; ?>");
					return;
				}
				if (!CheckValidIPv6Address($('#filter_ipv6_addr_'+index).val())) {
					alert("<?php echo $msg_chkIPv6Address[$GLOBALS['LANGINDEX']]; ?>");
					return;
				}
			}
		}

		for (var index=0; index<10; ++index) {
			if($('tr').hasClass('filter_ipv6_list_'+index)) {
				if (!CheckDuplicatedAddress('filter_ipv6', 10) || !CheckCrashIPv6Address()) {
					alert("<?php echo $msg_IPv4AddressDuplicate[$GLOBALS['LANGINDEX']]; ?>");
					return;
				}
				if (ipType == 6) 
				crash_result6[index] = CheckFilteringCrashIPv6Address($('#filter_ipv6_enable_'+index).val(), $('#filter_ipv6_addr_'+index).val(), $('#filter_ipv6_prefix_'+index).val());
				msg += "<IPv6Filtering>";
				msg += "<Enabled>"+$('#filter_ipv6_enable_'+index).val()+"</Enabled>";
				msg += "<Address>"+$('#filter_ipv6_addr_'+index).val()+"</Address>";
				msg += "<Prefix>"+$('#filter_ipv6_prefix_'+index).val()+"</Prefix>";
				msg += "</IPv6Filtering>";
			}
		}

		for (var index=0; index<10; ++index) {
			if ($('#filter_policy_deny').is(':checked')){
				if (ipType == 4) {
					if (crash_result4[index] == false) {
						alert("<?php echo $msg_chkIPAddress[$GLOBALS['LANGINDEX']]; ?>");
						return;
					}else if (crash_result4[index] == INVALID_PREFIX) {
						alert("<?php echo $msg_chkIPAddress[$GLOBALS['LANGINDEX']]; ?>");
						return;
					}
				}else {
					if (crash_result6[index] == false) {
						alert("<?php echo $msg_chkIPv6Address[$GLOBALS['LANGINDEX']]; ?>");
						return;
					}else if (crash_result6[index] == INVALID_PREFIX) {
						alert("<?php echo $msg_chkIPv6Address[$GLOBALS['LANGINDEX']]; ?>");
						return;
					}
				}
				
			}
		}
		
		if ($('#filter_policy_allow').is(':checked') == 1 && IsIncludedMyIPv4 == false && ipType ==4)	{
			alert("<?php echo $msg_chkIPAddress[$GLOBALS['LANGINDEX']]; ?>");
			return;
		}
		var ipv6Enable = parseInt(<?php echo $classInstances['Information']->dataInfo['IPv6Enable']['value']; ?>);
		if ($('#filter_policy_allow').is(':checked') == 1 && ipv6Enable == 1 && IsIncludedMyIPv6 == false && ipType == 6) {
			alert("<?php echo $msg_chkIPv6Address[$GLOBALS['LANGINDEX']]; ?>");
			return;
		}

		RequestAjaxMsg("<SetIPFiltering>"+msg+"</SetIPFiltering>", "<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $GLOBALS['REQUEST_URI'].'?seq='.$_SESSION['count'] ?>");

	}
	function CheckCrashIPv6Address()
	{
		var temp1 = new Array();
		var temp2 = new Array();
		for (var index=0; index<9; ++index) {
			for (var index2=(index+1); index2<10; ++index2) {
				if($('tr').hasClass('filter_ipv6_list_'+index) && $('tr').hasClass('filter_ipv6_list_'+index2)) {
					temp1 = SplitIPv6Address($('#filter_ipv6_addr_'+index).val().toLowerCase());
					temp2 = SplitIPv6Address($('#filter_ipv6_addr_'+index2).val().toLowerCase());
					if ((temp1[0]==temp2[0]) && (temp1[1]==temp2[1])  && (temp1[2]==temp2[2]) && (temp1[3]==temp2[3]) && (temp1[4]==temp2[4]) && (temp1[5]==temp2[5]) && (temp1[6]==temp2[6]) && (temp1[7]==temp2[7])) {
						return false;
					}
				}
			}
		}
		return true;
		
	}

	function CheckFilteringCrashIPv4Address(enable, ipaddr, prefix)
	{
		if ($('#filter_policy_allow').is(':checked') && IsIncludedMyIPv4 == true) return true;

		var ipv4Addr 	= ipaddr.split(".");
		var myiptemp	= GetMyIPAddress("<?php echo $_SERVER['REMOTE_ADDR']; ?>");

		var myip 		= myiptemp.split(".");
		var ip_32		= (ipv4Addr[0]<<24) |(ipv4Addr[1]<<16) |(ipv4Addr[2]<<8) | ipv4Addr[3];
		var subnetaddr = CalSubnetMask(parseInt(prefix, 10)).split(".");
		var nm_32 		= (subnetaddr[0]<<24)|(subnetaddr[1]<<16)|(subnetaddr[2]<<8)|subnetaddr[3];
		var myip_32		= (myip[0]<<24)|(myip[1]<<16)|(myip[2]<<8)| myip[3];

		if (parseInt(prefix, 10) == 32) {
			if (myip[0] == ipv4Addr[0] && myip[1] == ipv4Addr[1] && myip[2] == ipv4Addr[2] && myip[3] == ipv4Addr[3]) {
				if ($('#filter_policy_deny').is(':checked'))	{
					if (parseInt(enable) == 1) return false;
				}
				else {
					if (parseInt(enable) == 0) return false;
					IsIncludedMyIPv4 = true;
				}
			}
		}
		else {
			if((ip_32&nm_32) == (myip_32&nm_32)) {
				if ($('#filter_policy_deny').is(':checked'))	{
					if (parseInt(enable) == 1) {
						return INVALID_PREFIX;
					}
				}
				else {
					if (parseInt(enable) == 0) return false;
					IsIncludedMyIPv4 = true;
				}
			}
		}
		/*<?php if($classInstances['Information']->dataInfo['IPv6Enable']['value'] == 1){ ?>
				IsIncludedMyIPv4 = true;
		<?php } ?>*/
		return true;

	}

	function CheckFilteringCrashIPv6Address(enable, ipaddr, prefix)
	{
		if ($('#filter_policy_allow').is(':checked') && IsIncludedMyIPv6 == true) return true;

		prefix = parseInt(prefix, 10);
		var ipv6Enable = <?php echo $classInstances['Information']->dataInfo['IPv6Enable']['value']; ?>;
		var inputIP	= SplitIPv6Address(ipaddr.toLowerCase());
		var myIP 	= GetMyIPv6Address("<?php echo $_SERVER['REMOTE_ADDR']; ?>");

		myIP 			= SplitIPv6Address(myIP.toLowerCase());
		if (prefix == 128) {
			if (inputIP[0] == myIP[0] && inputIP[1] == myIP[1] &&inputIP[2] == myIP[2] &&inputIP[3] == myIP[3] &&
				inputIP[4] == myIP[4] && inputIP[5] == myIP[5] &&inputIP[6] == myIP[6] &&inputIP[7] == myIP[7]) {
				if ($('#filter_policy_deny').is(':checked')) {
					if (parseInt(enable) == 1) return false;
				}
				else {
					if (parseInt(enable) == 0) return false;
					IsIncludedMyIPv6 = true;
				}
			}
		}
		else {
			var min_mask 	= 0;
			var max_mask	= 0;
			var min_IP 		= SplitIPv6Address(ipaddr.toLowerCase());
			var max_IP 		= SplitIPv6Address(ipaddr.toLowerCase());
			var div			= parseInt(prefix/16);
			var mod 			= parseInt(prefix%16);

			if (mod != 0) {
				for (var i=(16-mod); i<16; i++) {
					var temp = 1 << i;
					min_mask |= temp;
				}
			}
			min_IP[div] = (GetAddrBinary(min_IP[div], min_IP[div].length) & min_mask).toString(16);

			for (var i=div+1; i<8; i++) min_IP[i] = 0;

			if (mod != 0) {
				for (var i=0; i<(16-mod); i++) {
					var temp = 1 << i;
					max_mask |= temp;
				}
			}
			else {
				max_mask = 65535;
			}

			max_IP[div] = (GetAddrBinary(max_IP[div], max_IP[div].length) | max_mask).toString(16);

			for (var i=div+1; i<8; i++) max_IP[i] = "ffff";

			var isMatch 	= false;
			var matchCnt	= 0;

			for (var ix=0; ix<8; ++ix) {
				if (min_IP[ix].toString(10) < myIP[ix].toString(10) && myIP[ix].toString(10) < max_IP[ix].toString(10)) {
					isMatch = true;
					break;
				}
				else if (min_IP[ix] == myIP[ix] || myIP[ix] == max_IP[ix]) {
					if (ix == 7) {
						if (min_IP[ix] == myIP[ix] || myIP[ix] == max_IP[ix]) {
							isMatch = true;
							break;
						}
					}
					continue;
				}
				else {
					break;
				}
			}
			if (isMatch == true) {
				if ($('#filter_policy_deny').is(':checked')) {
					if (parseInt(enable) == 1) {
						return INVALID_PREFIX;
					}

				}
				else {
					if (parseInt(enable) == 0) return false;
					IsIncludedMyIPv6 = true;
				}
			}
		}
		/*<?php if($classInstances['Information']->dataInfo['IPv6Enable']['value'] == 1){ ?>
				IsIncludedMyIPv6 = true;
		<?php } ?>*/
		return true;
	}

	function CalSubnetMask6(prefix)
	{
		var dataVal = new Array("ffff", "fffe", "fffc", "fff8", "fff0", "ffe0", "ffc0", "ff80", "ff00", "fe00", "fc00", "f800", "f000", "e000", "c000", "8000", "0000");
		var prefixVal = "";

		if (prefix >= 112) {
			prefixVal = "ffff:ffff:ffff:ffff:ffff:ffff:ffff:";
			prefixVal += dataVal[128-prefix];
		}
		else if (prefix >= 96) {
			prefixVal = "ffff:ffff:ffff:ffff:ffff:ffff:";
			prefixVal += dataVal[112-prefix]+":0";
		}
		else if (prefix >= 80) {
			prefixVal = "ffff:ffff:ffff:ffff:ffff:";
			prefixVal += dataVal[96-prefix]+":0:0";
		}
		else if (prefix >= 64) {
			prefixVal = "ffff:ffff:ffff:ffff:";
			prefixVal += dataVal[80-prefix]+":0:0:0";;
		}
		else if (prefix >= 48) {
			prefixVal = "ffff:ffff:ffff:";
			prefixVal += dataVal[64-prefix]+":0:0:0:0";
		}
		else if (prefix >= 32) {
			prefixVal = "ffff:ffff:";
			prefixVal += dataVal[48-prefix]+":0:0:0:0:0";
		}
		else if (prefix >= 16) {
			prefixVal = "ffff:";
			prefixVal += dataVal[32-prefix]+":0:0:0:0:0:0";
		}
		else {
			prefixVal += dataVal[16-prefix]+":0:0:0:0:0:0:0";
		}

		return prefixVal;
	}


	function ViewIPv4FilteringRange(index)
	{
		var mask_data = parseInt($('#filter_ipv4_prefix_'+index).val(),10);

		if (mask_data == 32) {
			$('#filter_ipv4_range_'+index).text($('#filter_ipv4_addr_'+index).val());
		}
		else {
			var min_mask 	= 0;
			var max_mask	= 0;
			var min_IP 		= $('#filter_ipv4_addr_'+index).val().split(".");
			var max_IP 		= $('#filter_ipv4_addr_'+index).val().split(".");
			var div			= parseInt(mask_data/8);
			var mod 			= parseInt(mask_data%8);

			if (mod != 0) {
				for (var i=(8-mod); i<8; i++) {
					var temp = 1 << i;
					min_mask |= temp;
				}
			}
			var tempIP = parseInt(min_IP[div]);
			min_IP[div] = tempIP & min_mask;

			for (var i=div+1; i<4; i++) {
				min_IP[i] = 0;
			}

			if (mod != 0) {
				for (var i=0; i<(8-mod); i++) {
					var temp = 1 << i;
					max_mask |= temp;
				}
			}
			else {
				max_mask = 0xff;
			}

			tempIP = parseInt(max_IP[div]);
			max_IP[div] = tempIP | max_mask;
			for (var i=div+1; i<4; i++) {
				max_IP[i] = 255;
			}

			var filter_msg = min_IP[0]+"."+min_IP[1]+"."+min_IP[2]+"."+min_IP[3]+" ~ "+max_IP[0]+"."+max_IP[1]+"."+max_IP[2]+"."+max_IP[3];
			$('#filter_ipv4_range_'+index).text(filter_msg);
		}
	}

	function ViewIPv6FilteringRange(index)
	{
		var mask_data = parseInt($('#filter_ipv6_prefix_'+index).val(),10);

		if (mask_data == 128) {
			$('#filter_ipv6_range_'+index).text($('#filter_ipv6_addr_'+index).val().toLowerCase());
			return;
		}
		else {
			var min_mask 	= 0;
			var max_mask	= 0;
			var min_IP 		= SplitIPv6Address($('#filter_ipv6_addr_'+index).val().toLowerCase());
			var max_IP 		= SplitIPv6Address($('#filter_ipv6_addr_'+index).val().toLowerCase());
			var div			= parseInt(mask_data/16);
			var mod 			= parseInt(mask_data%16);

			if (mod != 0) {
				for (var i=(16-mod); i<16; i++) {
					var temp = 1 << i;
					min_mask |= temp;
				}
			}

			min_IP[div] = (GetAddrBinary(min_IP[div], min_IP[div].length) & min_mask).toString(16);


			for (var i=div+1; i<8; i++) {
				min_IP[i] = 0;
			}

			if (mod != 0) {
				for (var i=0; i<(16-mod); i++) {
					var temp = 1 << i;
					max_mask |= temp;
				}
			}
			else {
				max_mask = 65535;
			}

			max_IP[div] = (GetAddrBinary(max_IP[div], max_IP[div].length) | max_mask).toString(16);
			for (var i=div+1; i<8; i++) {
				max_IP[i] = "ffff";
			}

			var filter_msg = 	min_IP[0]+":"+min_IP[1]+":"+min_IP[2]+":"+min_IP[3]+":"+min_IP[4]+":"+min_IP[5]+":"+min_IP[6]+":"+min_IP[7]+" ~ "+
								max_IP[0]+":"+max_IP[1]+":"+max_IP[2]+":"+max_IP[3]+":"+max_IP[4]+":"+max_IP[5]+":"+max_IP[6]+":"+max_IP[7];

			$('#filter_ipv6_range_'+index).text(filter_msg);
		}
	}

	function GetMyIPAddress(addrVal)
	{
		var ipPattern 	= /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/;
		var ipArray 	= addrVal.match(ipPattern);

		if(ipArray == null) {					// if ipv6_enable==true, my ip show ipv6 address format. so need parsing
			var splitIP = addrVal.split(":");
			addrVal = splitIP[splitIP.length-1];
		}
		return addrVal;
	}

	function GetMyIPv6Address(addrVal)
	{
		var retVal = addrVal.indexOf(".");
		if (retVal != -1) {
			var splitIP = addrVal.split(":");
			var ipv4Addr = (splitIP[splitIP.length-1]).split(".");
			var tempAddr1	= (ipv4Addr[0]<<8) |ipv4Addr[1];
			var tempAddr2	= (ipv4Addr[2]<<8) |ipv4Addr[3];
			tempAddr1 = tempAddr1.toString(16);
			tempAddr2 = tempAddr2.toString(16);
			addrVal = "";
			for (var index=0; index<(splitIP.length-1); ++index) {
				addrVal += splitIP[index]+":";
			}
			addrVal += tempAddr1+":"+tempAddr2;
		}

		return addrVal;
	}

	function SplitIPv6Address(addrVal)
	{
		var ipVal 		= addrVal.split(":");
		var frontValCnt= 0;
		var backValCnt	= 0;
		var backAddr	= new Array();

		for (var index=0; index<ipVal.length; ++index) {
			if (ipVal[index].length == 0){
				for (var index2=index; index2<ipVal.length; ++index2) {
					if (ipVal[index2].length != 0) {
						backAddr[backValCnt] = ipVal[index2];
						backValCnt++;
					}
				}
				break;
			}
			frontValCnt++;
		}

		for (var index=0; index<backValCnt; ++index) {
			ipVal[8-(backValCnt-index)] = backAddr[index];
		}

		var offset = 8 - (frontValCnt+backValCnt);
		for (var index=frontValCnt; index<(frontValCnt+offset); ++index) {
			ipVal[index] = 0;
		}

		return ipVal;
	}

	function GetAddrBinary(addrVal, valLength)
	{
		var ipBinaryVal = 0;
		for (var i=0; i<valLength; ++i) {
			var binVal = 0;
			if 		(addrVal.charAt(i) == 'f' || addrVal.charAt(i) == 'F') 	binVal = 15;
			else if 	(addrVal.charAt(i) == 'e' || addrVal.charAt(i) == 'E') 	binVal = 14;
			else if 	(addrVal.charAt(i) == 'd' || addrVal.charAt(i) == 'D') 	binVal = 13;
			else if 	(addrVal.charAt(i) == 'c' || addrVal.charAt(i) == 'C')	binVal = 12;
			else if 	(addrVal.charAt(i) == 'b' || addrVal.charAt(i) == 'B')	binVal = 11;
			else if 	(addrVal.charAt(i) == 'a' || addrVal.charAt(0) == 'A')	binVal = 10;
			else 																				binVal = addrVal.charAt(i);
			ipBinaryVal = ipBinaryVal << 4;
			ipBinaryVal |= binVal;
		}
		return ipBinaryVal;
	}

	function OnChangeIPv4Address(index)
	{
		var ipPattern	= /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/;
		var ipArray 	= $('#filter_ipv4_addr_'+index).val().match(ipPattern);

		if(ipArray == null) {
			alert("<?php echo $msg_chkIPAddress[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}

		var ip_num 	= ((ipArray[1]&0xFF)<<24) + ((ipArray[2]&0xFF)<<16) + ((ipArray[3]&0xFF)<<8) + ((ipArray[4]&0xFF)<<0);
		thisSegment = ipArray[1];

		if(thisSegment < 1 || thisSegment > 223) {
			alert("<?php echo $msg_chkIPAddress[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}

		for(var i=2; i<5; i++) {
			thisSegment = ipArray[i];
			if(thisSegment>255) {
				alert("<?php echo $msg_chkIPAddress[$GLOBALS['LANGINDEX']]; ?>");
				return false;
			}
		}
		OnChangeIPv4Prefix(index);
		return true;
	}

	function OnChangeIPv4Prefix(index)
	{
		if(parseInt($('#filter_ipv4_prefix_'+index).val(), 10) < 1 || parseInt($('#filter_ipv4_prefix_'+index).val(), 10) > 32) {
			alert("<?php echo $msg_IPv4Prefix1to32[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		if ($('#filter_ipv4_prefix_'+index).val() == ''){
			alert("<?php echo $msg_IPv4Prefix1to32[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		ViewIPv4FilteringRange(index);
		return true;
	}

	function OnChangeIPv6Address(index)
	{
		var ipv6Addr = $('#filter_ipv6_addr_'+index).val().split(":");
		/*if(!CheckDuplicatedAddress('filter_ipv6', 10)) {
			alert("<?php echo $msg_IPv4AddressDuplicate[$GLOBALS['LANGINDEX']]; ?>");
           	 	return false;
        	}*/
		if (ipv6Addr.length < 3) {
			alert("<?php echo $msg_chkIPv6Address[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}

		var spaceCnt = 0;
		for (var ix=0; ix<ipv6Addr.length; ++ix) {
			if (ipv6Addr[ix].length < 0 || ipv6Addr[ix].length > 4) {
				alert("<?php echo $msg_chkIPv6Address[$GLOBALS['LANGINDEX']]; ?>");
				return false;
			}
			if (ipv6Addr[ix].length == 0) spaceCnt++;
		}

		if ((spaceCnt > 1 && ipv6Addr[0].length != 0 && ipv6Addr[ipv6Addr.length - 1].length != 0) || (spaceCnt == 0 && ipv6Addr.length != 8)) {
			alert("<?php echo $msg_chkIPv6Address[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		OnChangeIPv6Prefix(index)
		return true;
	}

	function OnChangeIPv6Prefix(index)
	{
		if (parseInt($('#filter_ipv6_prefix_'+index).val(), 10) < 1 || parseInt($('#filter_ipv6_prefix_'+index).val(), 10) > 128) {
			alert("<?php echo $msg_IPv6Prefix1to128[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		if ($('#filter_ipv6_prefix_'+index).val() == ''){
			alert("<?php echo $msg_IPv6Prefix1to128[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		ViewIPv6FilteringRange(index);
		return true;
	}

	function OnClickFilterList(protocol)
	{
		var selNo = $("input[name='filter_"+protocol+"_select']:checked").val();

		if ((selNo != oldSelNo || protocol != oldSelProtocol) && typeof oldSelNo != "undefined") {
			$('#filter_'+oldSelProtocol+'_select_'+oldSelNo).prop('checked', false);
			$('#filter_'+oldSelProtocol+'_enable_'+oldSelNo).attr('disabled', 'disabled');
			$('#filter_'+oldSelProtocol+'_enable_'+oldSelNo).parent().css('color', '#6d6d6d');
			$('#filter_'+oldSelProtocol+'_addr_'+oldSelNo).attr('disabled', 'disabled');
			$('#filter_'+oldSelProtocol+'_prefix_'+oldSelNo).attr('disabled', 'disabled');
		}
		$('#filter_'+protocol+'_enable_'+selNo).removeAttr('disabled');
		$('#filter_'+protocol+'_enable_'+selNo).parent().css('color', '#1c1c1c');
		$('#filter_'+protocol+'_addr_'+selNo).removeAttr('disabled');
		$('#filter_'+protocol+'_prefix_'+selNo).removeAttr('disabled');
		oldSelNo = selNo;
		oldSelProtocol = protocol;
	}

	function OnClickAdd(protocol)
	{
		if ((protocol == 'ipv4' && filter_ipv4_cnt == 10) || (protocol == 'ipv6' && filter_ipv6_cnt == 10)) {
			alert("<?php echo $msg_cannot_add[$GLOBALS['LANGINDEX']]; ?>");
			return;
		}

		var addNo = 0;
		for(var index=0; index<10; ++index) {
			if($('tr').hasClass('filter_'+protocol+'_list_'+index)) continue;
			addNo = index;
			break;
		}

		if (protocol == 'ipv4') {
			$('#filter_ipv4_list').append(
				"<tr class='filter_ipv4_list_"+addNo+"'>\
					<td><input type='radio' name='filter_ipv4_select' id='filter_ipv4_select_"+addNo+"' onClick='OnClickFilterList(\"ipv4\");' value='"+addNo+"' checked='checked'/></td>\
					<td><select id='filter_ipv4_enable_"+addNo+"' class='selectbox_style' style='width:110px'><option value='0'><?php echo $t_off[$GLOBALS['LANGINDEX']]; ?></option><option value='1' selected='selected'><?php echo $t_on[$GLOBALS['LANGINDEX']]; ?></option></select></td>\
					<td><input type='text' id='filter_ipv4_addr_"+addNo+"' class='listtext' style='width:300px;' value='' maxlength='15' onpaste='javascript:return false;' onkeypress='CheckIPv4(event)' onkeydown='CheckIPv4(event)' onChange='OnChangeIPv4Address("+addNo+")' onclick='OnClickInput(4,\"addr\");'/></td>\
					<td><input type='text' id='filter_ipv4_prefix_"+addNo+"' class='listtext' style='width:30px;' value='32' maxlength='2' onpaste='javascript:return false;' onkeypress='IsNum(event)' onkeydown='OnlyNUm(event);' onchange='OnChangeIPv4Prefix("+addNo+")' onclick='OnClickInput(4,\"prefix\");'/></td>\
					<td><span id='filter_ipv4_range_"+addNo+"' class='iplist_area'></span></td>\
				</tr>"
			);
			filter_ipv4_cnt++;
		}
		else {
			$('#filter_ipv6_list').append(
				"<tr class='filter_ipv6_list_"+addNo+"'>\
					<td><input type='radio' name='filter_ipv6_select' id='filter_ipv6_select_"+addNo+"' onClick='OnClickFilterList(\"ipv6\");' value='"+addNo+"' checked='checked'/></td>\
					<td><select id='filter_ipv6_enable_"+addNo+"' class='selectbox_style' style='width:110px'><option value='0'><?php echo $t_off[$GLOBALS['LANGINDEX']]; ?></option><option value='1' selected='selected'><?php echo $t_on[$GLOBALS['LANGINDEX']]; ?></option></select></td>\
					<td><input type='text' id='filter_ipv6_addr_"+addNo+"' class='listtext' style='width:300px;' onpaste='javascript:return false;' onkeypress=\"CheckIPv6(event, 'press')\" onkeydown=\"CheckIPv6(event, 'down')\" value='' maxlength='39' onKeyPress='return IsIPv6Char(event)' onChange='OnChangeIPv6Address("+addNo+")' onclick='OnClickInput(6,\"addr\");'/></td>\
					<td><input type='text' id='filter_ipv6_prefix_"+addNo+"' class='listtext' style='width:30px;' onpaste='javascript:return false;' onkeypress='IsNum(event)' onkeydown='OnlyNUm(event);' value='128' maxlength='3' onKeyPress='return IsNum(event)' onchange='OnChangeIPv6Prefix("+addNo+")' onclick='OnClickInput(6,\"prefix\");'/></td>\
					<td><span id='filter_ipv6_range_"+addNo+"' class='iplist_area'></span></td>\
				</tr>"
			);
			filter_ipv6_cnt++;
		}
		$('#filter_'+protocol+'_enable_'+addNo).styledSelect( {innerClass:'selectbox_style_option'} );
		$('#filter_'+oldSelProtocol+'_select_'+oldSelNo).prop('checked', false);
		OnClickFilterList(protocol);
	}

	function OnClickDelete(protocol)
	{
		if (!CheckDeletedTarget('filter_'+protocol)) return;
		OnClickFilterList(protocol);
	}

	function OnClickInput(protocol, type)
	{
		var selNo = $("input[name='filter_ipv"+protocol+"_select']:checked").val();
		$('#filter_ipv'+protocol+'_'+type+'_'+selNo).focus();
	}

	function OnLoad()
	{
		for (var index=0; index<filter_ipv4_cnt; ++index) ViewIPv4FilteringRange(index);
		for (var index=0; index<filter_ipv6_cnt; ++index) ViewIPv6FilteringRange(index);

	}

		</script>
	</head>
	<body onload="OnLoad()" onselectstart="return false">
		<div id="wrap">
			<div id="head">
			<?php
				require_once ('left_menu.cgi');
				require_once ('top_menu.cgi');
			?>
			<div id="container" style="width:1300px">
			<?php
				PrintLeftMenu($_SERVER['SCRIPT_NAME']);
			?>
			<div id="contents" >
				<div class="h3_tit mgt0" style="width:733px;">
					<h3 class="wid320"><?php echo $menu_ipfilter[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>
				<table class="data_write">
					<colgroup>
						<col style="width:180px;" />
						<col />
						<col />
					</colgroup>
					<tbody>
						<tr>
							<th><?php echo $t_filteringType[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<label><input type="radio" name="filter_policy" id="filter_policy_deny" <?php if ($ipFiltering->defaultPolicy == 0) echo "checked=\"checked\""; ?>/><?php echo $t_deny[$GLOBALS['LANGINDEX']]; ?></label>								
								<label><input type="radio" name="filter_policy" id="filter_policy_allow" <?php if ($ipFiltering->defaultPolicy == 1) echo "checked=\"checked\""; ?>/><?php echo $t_allow[$GLOBALS['LANGINDEX']]; ?></label>
							</td>
						</tr>
					</tbody>
				</table>
				<div class="h3_tit" style="width:733px;">
					<h3>IPv4</h3>
				</div>
				<table id="filter_ipv4_list" class="data_table2" style="width:733px;">
					<colgroup>
						<col style="width:27px;" />
						<col style="width:110px;" />
						<col style="width:301px;" />
						<col style="width:70px;" />
						<col />
					</colgroup>
					<thead>
						<tr>
							<th></th>
							<th><?php echo $t_use[$GLOBALS['LANGINDEX']]; ?></th>
							<th>IP</th>
							<th><?php echo $t_prefix[$GLOBALS['LANGINDEX']]; ?></th>
							<th><?php echo $t_filteringRange[$GLOBALS['LANGINDEX']]; ?></th>
						</tr>
					</thead>
					<tbody>
			<?php
				$filterCnt = 0;
				for ($index=0; $index<10; ++$index) {
					if ($ipFiltering->ipv4IPFilter[$index]->dataInfo['Address']['value'] != "") {
			?>
						<tr class="filter_ipv4_list_<?php echo $filterCnt; ?>">
							<td><input type="radio" name="filter_ipv4_select" id="filter_ipv4_select_<?php echo $filterCnt; ?>" onClick="OnClickFilterList('ipv4');" value="<?php echo $filterCnt; ?>" /></td>
							<td>
								<select id="filter_ipv4_enable_<?php echo $filterCnt; ?>"  class="selectbox_style" style="width:110px" disabled="disabled">
									<option value="0" <?php if ($ipFiltering->ipv4IPFilter[$index]->dataInfo['Enabled']['value'] == 0) echo "selected=\"selected\""; ?>><?php echo $t_off[$GLOBALS['LANGINDEX']]; ?></option>
									<option value="1" <?php if ($ipFiltering->ipv4IPFilter[$index]->dataInfo['Enabled']['value'] == 1) echo "selected=\"selected\""; ?>><?php echo $t_on[$GLOBALS['LANGINDEX']]; ?></option>
								</select>
							</td>
							<script>$('#filter_ipv4_enable_<?php echo $filterCnt; ?>').styledSelect( {innerClass:'selectbox_style_option'} );</script>
							<td><input type="text" id="filter_ipv4_addr_<?php echo $filterCnt; ?>" class="listtext" style="width:300px;" onpaste="javascript:return false;" onkeypress='CheckIPv4(event)' onkeydown='CheckIPv4(event)' value="<?php echo trim($ipFiltering->ipv4IPFilter[$index]->dataInfo['Address']['value']); ?>" maxlength="15" onChange="OnChangeIPv4Address(<?php echo $filterCnt; ?>)" disabled="disabled" onclick="OnClickInput(4,'addr');"/></td>
							<td><input type="text" id="filter_ipv4_prefix_<?php echo $filterCnt; ?>" class="listtext" style="width:30px;" onpaste="javascript:return false;" onkeypress="IsNum(event)" onkeydown="OnlyNUm(event);" value="<?php echo $ipFiltering->ipv4IPFilter[$index]->dataInfo['Prefix']['value']; ?>" maxlength="2" onchange="OnChangeIPv4Prefix(<?php echo $filterCnt; ?>)" disabled="disabled" onclick="OnClickInput(4,'prefix');"/></td>
							<td><span id="filter_ipv4_range_<?php echo $filterCnt; ?>" class="iplist_area"></span></td>
						</tr>
			<?php
						$filterCnt++;
					}
				}
			?>
					</tbody>
				</table>
				<script>
					filter_ipv4_cnt = parseInt(<?php echo $filterCnt; ?>);
				</script>
				<div class="btn_add_left">
					<a id="mid_add_btn" class="btn_type01" href="javascript:OnClickAdd('ipv4')"><?php echo $t_add[$GLOBALS['LANGINDEX']]; ?></a>&nbsp;
					<a id="mid_del_btn" class="btn_type01" href="javascript:OnClickDelete('ipv4')"><?php echo $t_delete[$GLOBALS['LANGINDEX']]; ?></a>
				</div>

				<div class="h3_tit" style="width:733px;">
					<h3>IPv6</h3>
				</div>
				<table id="filter_ipv6_list" class="data_table2" style="width:733px;">
					<colgroup>
						<col style="width:27px;" />
						<col style="width:110px;" />
						<col style="width:301px;" />
						<col style="width:70px;" />
						<col />
					</colgroup>
					<thead>
						<tr>
							<th></th>
							<th><?php echo $t_use[$GLOBALS['LANGINDEX']]; ?></th>
							<th>IP</th>
							<th><?php echo $t_prefix[$GLOBALS['LANGINDEX']]; ?></th>
							<th><?php echo $t_filteringRange[$GLOBALS['LANGINDEX']]; ?></th>
						</tr>
					</thead>
					<tbody>
			<?php
				$filterCnt = 0;
				for ($index=0; $index<10; ++$index) {
					if ($ipFiltering->ipv6IPFilter[$index]->dataInfo['Address']['value'] != "") {
				?>
						<tr class="filter_ipv6_list_<?php echo $filterCnt; ?>">
							<td><input type="radio" name="filter_ipv6_select" id="filter_ipv6_select_<?php echo $filterCnt; ?>" onClick="OnClickFilterList('ipv6');" value="<?php echo $filterCnt; ?>" /></td>
							<td>
								<select id="filter_ipv6_enable_<?php echo $filterCnt; ?>" class="selectbox_style" style="width:110px" disabled="disabled">
									<option value="0" <?php if ($ipFiltering->ipv6IPFilter[$index]->dataInfo['Enabled']['value'] == 0) echo "selected=\"selected\""; ?>><?php echo $t_off[$GLOBALS['LANGINDEX']]; ?></option>
									<option value="1" <?php if ($ipFiltering->ipv6IPFilter[$index]->dataInfo['Enabled']['value'] == 1) echo "selected=\"selected\""; ?>><?php echo $t_on[$GLOBALS['LANGINDEX']]; ?></option>
								</select>
							</td>
							<script>$('#filter_ipv6_enable_<?php echo $filterCnt; ?>').styledSelect( {innerClass:'selectbox_style_option'} );</script>
							<td><input type="text" id="filter_ipv6_addr_<?php echo $filterCnt; ?>" class="listtext" style="width:300px;" onpaste="javascript:return false;" onkeypress="CheckIPv6(event, 'press')" onkeydown="CheckIPv6(event, 'down')" value="<?php echo trim($ipFiltering->ipv6IPFilter[$index]->dataInfo['Address']['value']); ?>" maxlength="39"  onChange="OnChangeIPv6Address(<?php echo $filterCnt; ?>)" disabled="disabled" onclick="OnClickInput(6,'addr');"/></td>
							<td><input type="text" id="filter_ipv6_prefix_<?php echo $filterCnt; ?>" class="listtext" style="width:30px;" onpaste="javascript:return false;" onkeypress="IsNum(event)" onkeydown="OnlyNUm(event);" value="<?php echo $ipFiltering->ipv6IPFilter[$index]->dataInfo['Prefix']['value']; ?>" maxlength="3" onchange="OnChangeIPv6Prefix(<?php echo $filterCnt; ?>)" disabled="disabled" onclick="OnClickInput(6,'prefix');"/></td>
							<td><span id="filter_ipv6_range_<?php echo $filterCnt; ?>" class="iplist_area"></span></td>
						</tr>
			<?php
						$filterCnt++;
					}
				}
			?>
					</tbody>
				</table>
				<script>
					filter_ipv6_cnt = parseInt(<?php echo $filterCnt; ?>);
				</script>
				<div class="btn_add_left">
					<a id="mid_add_btn" class="btn_type01" href="javascript:OnClickAdd('ipv6')"><?php echo $t_add[$GLOBALS['LANGINDEX']]; ?></a>&nbsp;
					<a id="mid_del_btn" class="btn_type01" href="javascript:OnClickDelete('ipv6')"><?php echo $t_delete[$GLOBALS['LANGINDEX']]; ?></a>
				</div>
				<div class="btn_right">
					<a id="mid_ok_btn" class="btn_apply" href="javascript:OnClickApply()"><?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?></a>
				</div>
				</div>
			</div>
		</div>
	</div>
</body>
</html>
