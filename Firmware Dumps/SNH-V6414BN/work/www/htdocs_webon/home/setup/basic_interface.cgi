<?php
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_menu.cgi');
require_once ('../language/language_network_interface.cgi');
require_once ('../language/language_network_ipfilter.cgi');
require_once ('../language/language_network_port.cgi');

$classInstances= GetClassInstance('interface');
$ipConf 			= $classInstances['InterfaceConfiguration']->ipConf;
$gatewayConf	= $classInstances['InterfaceConfiguration']->gateway;
$dnsConf 		= $classInstances['InterfaceConfiguration']->dnsInfo;
$protocolConf	= $classInstances['InterfaceConfiguration']->networkProtocol;
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<title>iPOLiS NETWORK CAMERA WEBVIEWER</title>
	<meta http-equiv="X-UA-Compatible" content="IE=Edge; requiresActiveX=true">
	<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
	<link rel="stylesheet" type="text/css" href="../css/techwin.css" />
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
	$(document).ready(function(){ lnbonoff("lnb_basic"); });

	var localSeq				= <?php echo $_SESSION['count']; ?>;
	var ajaxReqUrl				= "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq;
	var oldIPType				= <?php echo $ipConf->ipv4AddrConf->dataInfo['Type']['value']; ?>;
	var oldStaticIP 			= "<?php echo trim($ipConf->ipv4AddrConf->staticAddr->dataInfo['Address']['value']); ?>"
	var oldStaticSubnet		= CalSubnetMask(<?php echo $ipConf->ipv4AddrConf->staticAddr->dataInfo['Prefix']['value']; ?>);
	var oldDynamicSubnet		= CalSubnetMask(<?php echo $ipConf->ipv4AddrConf->dynamicAddr->dataInfo['Prefix']['value']; ?>);
	var oldGateway				= "<?php echo $gatewayConf->dataInfo['IPv4Gateway']['value']; ?>";
	var oldDNS1					= "<?php echo $dnsConf->dnsManual[0]->dataInfo['Address']['value']; ?>";
	var oldDNS2 				= "<?php echo $dnsConf->dnsManual[1]->dataInfo['Address']['value']; ?>";
	var oldID				 	= "<?php echo trim($ipConf->ipv4AddrConf->dataInfo['XDSLUserName']['value']); ?>";
	var oldPW					= "<?php echo trim($ipConf->ipv4AddrConf->dataInfo['XDSLPassword']['value']); ?>";
	var oldIPv6					= <?php echo $ipConf->ipv6AddrConf->dataInfo['Enabled']['value']; ?>;
	var staticIPv6Address 	= "<?php echo $ipConf->ipv6AddrConf->staticAddr->dataInfo['Address']['value']; ?>";
	var staticIPv6Prefix 	= "<?php echo $ipConf->ipv6AddrConf->staticAddr->dataInfo['Prefix']['value']; ?>";
	var dynamicIPv6Address 	= "<?php echo $ipConf->ipv6AddrConf->dynamicAddr->dataInfo['Address']['value']; ?>";
	var dynamicIPv6Prefix 	= "<?php echo $ipConf->ipv6AddrConf->dynamicAddr->dataInfo['Prefix']['value']; ?>";
	var ipv6Mode 				= parseInt(<?php echo $ipConf->ipv6AddrConf->dataInfo['DHCP']['value']; ?>);
	var oldIPv6Gateway		= "<?php echo $gatewayConf->dataInfo['IPv6Gateway']['value']; ?>";
	var oldHTTPPort 			= "<?php echo $protocolConf->protocol[0]->dataInfo['Port']['value'];?>";
	var oldHTTPSPort 			= "<?php echo $protocolConf->protocol[1]->dataInfo['Port']['value'];?>";
	var IsChangedHTTP = false;
	var IsChangedPort = false;
	var IsBrowserClose = false;

	function OnClickApply()
	{		
		var ipv4Type = parseInt($('#ipv4_type option:selected').val());

		if (ipv4Type == 0) {
			var ipaddr = $('#ipv4_addr').val().split(".");
			if(ipaddr[3] == 255) {
				alert("<?php echo $msg_chkIPAddress[$GLOBALS['LANGINDEX']]; ?>");
				return;
			}
		}
		if ($('#ipv6_use').is(':checked') && $('#ipv6_manual').is(':checked')) {
			if (!CheckValidIPv6Address($('#ipv6_manual_addr').val())) {
				alert("<?php echo $msg_chkIPv6Address[$GLOBALS['LANGINDEX']]; ?>");
				return;
			}
			if ($('#ipv6_manual_gateway').val().length > 0 && !CheckValidIPv6Address($('#ipv6_manual_gateway').val())) {
				alert("<?php echo $msg_chkGateway[$GLOBALS['LANGINDEX']]; ?>");
				return;
			}
			if ($('#ipv6_manual_addr').val() == $('#ipv6_manual_gateway').val()) {
				alert("<?php echo $msg_chkGateway[$GLOBALS['LANGINDEX']]; ?>");
				return;
			}
		}
		if (!CheckPort())										return;
		if (!CheckIPv4DNS())								return;
		if (ipv4Type == 0 && !CheckIPv4Address())	return;
		if (ipv4Type == 2 && !CheckIPv4PPPoE())		return;
		IsChangedHTTP = GetIsChangedValue();
	
		if ((IsChangedHTTP || IsChangedPort) && GetVaildIPv6Setting()) {
			if (confirm("<?php echo $msg_confirmInterface[$GLOBALS['LANGINDEX']]; ?>")) {
				var msg = "";
				msg += "<SetInterface>";
				msg += "<Interface>";
				msg += "<IPv4Interface>";
				msg += "<Type>"+$('#ipv4_type').val()+"</Type>";
				if (ipv4Type == 0) {
					msg += "<Address>"+$('#ipv4_addr').val() +"</Address>";
					msg += "<Prefix>"+ChangeSubnetToPrefix($('#ipv4_subnet').val())+"</Prefix>";
				}
				if (ipv4Type == 2) {
					msg +="<XDSLUserName>"+$('#ipv4_pppoe_name').val()+"</XDSLUserName>";
					msg +="<XDSLPassword>"+$('#ipv4_pppoe_pw').val()+"</XDSLPassword>";
				}
				msg += "</IPv4Interface>";
				msg +="<IPv6Interface>";
				msg +="<Enabled>"+ ($('#ipv6_use').is(':checked') ? 1: 0)+"</Enabled>";
				if ($('#ipv6_default').is(':checked'))		msg +="<DHCP>3</DHCP>";
				else if ($('#ipv6_dhcp').is(':checked'))	msg +="<DHCP>1</DHCP>";
				else if ($('#ipv6_manual').is(':checked')) {
					msg +="<DHCP>4</DHCP>";
					msg +="<Address>"+$('#ipv6_manual_addr').val()+"</Address>";
					msg +="<Prefix>"+$('#ipv6_manual_prefix').val()+"</Prefix>";
				}
				else	msg +="<DHCP>3</DHCP>";
				msg +="</IPv6Interface>";
				msg += "</Interface>";
				msg += "<Gateway>";
				msg += "<IPv4Gateway>"+$('#ipv4_gateway').val()+"</IPv4Gateway>";
				if ($('#ipv6_manual').is(':checked')) {
					msg += "<IPv6Gateway>"+$('#ipv6_manual_gateway').val()+"</IPv6Gateway>";
				}
			 	msg += "</Gateway>";
				msg += "<DNS>";
				msg += "<Manual>";
				msg +="<Address0>"+$('#ipv4_dns1').val()+"</Address0>";
				msg +="<Address1>"+$('#ipv4_dns2').val()+"</Address1>";
				msg +="</Manual>";
				msg +="</DNS>";
				msg +="</SetInterface>";

				var reqUrl = "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq;
				if (BrowserDetect.browser == "Explorer" || (BrowserDetect.browser == 'Safari' && reqUrl.search('.local') != -1)) {
					reqUrl = "../.."+reqUrl.substr(reqUrl.indexOf("/cgi"));
				}

				<?php if ($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>
					$.ajax({
						type: "POST",
						async: true,
						cache: false,
						url: reqUrl,
						dataType: "text",
						data: encodeURI(msg),
						success: null
					});
				<?php } else { ?>
					$.ajax({
						type: "POST",
						async: false,
						cache: false,
						url: reqUrl,
						dataType: "text",
						data: encodeURI(msg),
						success: null
					});
				<?php } ?>
				
				var msg = "<SetPort>";
				msg += "<HTTP><Port>"+$('#port_http').val()+"</Port></HTTP>";
				msg += "<HTTPS><Port>"+$('#port_https').val()+"</Port></HTTPS>";
				msg += "<RTSP><Port>"+$('#port_rtsp').val()+"</Port></RTSP>";
				msg += "<VNP><Port>"+$('#port_vnp').val()+"</Port></VNP>";
				msg += "<RTSPTimeout>"+($('#port_rtsp_timeout').is(':checked') ? 0 : 1)+"</RTSPTimeout>";
				msg += "</SetPort>";

				if (IsChangedPort || IsChangedHTTP) IsBrowserClose = true;
				else IsBrowserClose = false;
			
				var reqUrl = "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq;
				if (BrowserDetect.browser == "Explorer" || (BrowserDetect.browser == 'Safari' && reqUrl.search('.local') != -1)) {
					reqUrl = "../.."+reqUrl.substr(reqUrl.indexOf("/cgi"));
				}
				<?php if ($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>
					$.ajax({
						type: "POST",
						async: true,
						cache: false,
						url: reqUrl,
						dataType: "text",
						data: encodeURI(msg),
						success: OnSuccessApply,
						error: OnFailApply
					});
				<?php } else { ?>
					$.ajax({
						type: "POST",
						async: false,
						cache: false,
						url: reqUrl,
						dataType: "text",
						data: encodeURI(msg),
						success: OnSuccessApply,
						error: OnFailApply
					});
				<?php } ?>
			}
		}else{
			var msg = "<SetPort>";
			msg += "<HTTP><Port>"+$('#port_http').val()+"</Port></HTTP>";
			msg += "<HTTPS><Port>"+$('#port_https').val()+"</Port></HTTPS>";
			msg += "<RTSP><Port>"+$('#port_rtsp').val()+"</Port></RTSP>";
			msg += "<VNP><Port>"+$('#port_vnp').val()+"</Port></VNP>";
		//	msg += "<WebViewer><Port>"+$('#port_viewer').val()+"</Port></WebViewer>";
			msg += "<RTSPTimeout>"+($('#port_rtsp_timeout').is(':checked') ? 0 : 1)+"</RTSPTimeout>";
			msg += "</SetPort>";
			IsBrowserClose = false;
			
			var reqUrl = "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq;
			if (BrowserDetect.browser == "Explorer" || (BrowserDetect.browser == 'Safari' && reqUrl.search('.local') != -1)) {
				reqUrl = "../.."+reqUrl.substr(reqUrl.indexOf("/cgi"));
			}

			<?php if ($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>
				$.ajax({
					type: "POST",
					async: true,
					cache: false,
					url: reqUrl,
					dataType: "text",
					data: encodeURI(msg),
					success: OnSuccessApply,
					error: OnSuccessApply
				});
			<?php } else { ?>
				$.ajax({
					type: "POST",
					async: false,
					cache: false,
					url: reqUrl,
					dataType: "text",
					data: encodeURI(msg),
					success: OnSuccessApply,
					error: OnSuccessApply
				});
			<?php } ?>
		}
	}
	function OnFailApply()
	{
		IsBrowserClose = false;
		var msg = "<SetPort>";
		msg += "<HTTP><Port>"+$('#port_http').val()+"</Port></HTTP>";
		msg += "<HTTPS><Port>"+$('#port_https').val()+"</Port></HTTPS>";
		msg += "<RTSP><Port>"+$('#port_rtsp').val()+"</Port></RTSP>";
		msg += "<VNP><Port>"+$('#port_vnp').val()+"</Port></VNP>";
		msg += "<RTSPTimeout>"+($('#port_rtsp_timeout').is(':checked') ? 0 : 1)+"</RTSPTimeout>";
		msg += "</SetPort>";

		if (IsChangedPort || IsChangedHTTP) IsBrowserClose = true;
		else IsBrowserClose = false;
	
		var reqUrl = "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq;
		if (BrowserDetect.browser == "Explorer" || (BrowserDetect.browser == 'Safari' && reqUrl.search('.local') != -1)) {
			reqUrl = "../.."+reqUrl.substr(reqUrl.indexOf("/cgi"));
		}
		$.ajax({
			type: "POST",
			async: false,
			cache: false,
			url: reqUrl,
			dataType: "text",
			data: encodeURI(msg),
			success: OnSuccessApply,
			error: OnFailApply
		});
	}
	
	function OnSuccessApply(req)
	{
		if(IsBrowserClose) {
			if(BrowserDetect.browser == 'Firefox'){
				window.open('about:blank', '_self');
				//window.location.reload(true);
			}
			else {
				window.open('about:blank', '_self').close();
				window.location.reload(true);
				}
		}
		else {
			if (!IsChangedHTTP && !IsChangedPort) {
				alert("<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>");
				window.location.reload(true);
			}
		}
	}

	function GetStatusCloseBrowser()
	{
		var ipv6Type = $(':radio[name="ipv6_type"]:checked').val();

		if (ipv6Type != oldIPType) return true;
		if (ipv6Type == 0) {
			if ($('#ipv4_addr').val() != oldStaticIP) 			return true;
			if ($('#ipv4_subnet').val() != oldStaticSubnet) 	return true;
		}
		else if (ipv6Type == 2) {
			if ($('#ipv4_pppoe_name').val() != oldID || $('#ipv4_pppoe_pw') != oldPW) return true
			if ($('#ipv4_subnet').val() != oldDynamicSubnet) return true;
		}
	
		if (ipv6Type != 1 && $('#ipv4_gateway').val() != oldGateway) 	return true;

		if ($('#ipv4_dns1').val() != oldDNS1 || $('#ipv4_dns2').val() != oldDNS2 ) 	return true;
		

		if ($('#ipv6_use').is(':checked')) {
			if (oldIPv6 != 1 )	return true;
		}
		else {
			if (oldIPv6 != 0 )	return true;
		}


		if ($('#ipv6_dhcp').is(':checked')) {
			if (ipv6Mode != 1)		return true;		}
		else if ($('#ipv6_manual').is(':checked')) {
			if (ipv6Mode != 4)		return true;
			if ($('#ipv6_manual_addr').val() != staticIPv6Address)					return true;
			if (parseInt($('#ipv6_manual_prefix').val()) != staticIPv6Prefix)	return true;
		}
		else {
			if (ipv6Mode != 3)		return true;
		}
		
		return false;
	}

	function ChangeSubnetToPrefix(subnetValue)
	{
		var prefixVal 	= 0;
		var subnetArr 	= new Array();
		var dataVal 	= new Array("0", "128", "192", "224", "240", "248", "252", "254", "255");
		subnetArr 		= subnetValue.split('.');
		for (var index=0; index<4; ++index) {
			for (var index2=0; index2<dataVal.length; ++index2) {
				if (parseInt(subnetArr[index], 10) == dataVal[index2]) {
					prefixVal += index2;
					break;
				}
			}
		}
		return prefixVal;
	}

	function CheckIPv6ManualAddress()
	{
		if ($('#ipv6_use').is(':checked') && ($('#ipv6_manual_addr').val().length == 0 || $('#ipv6_manual_prefix').val().length == 0)) {
			alert("<?php echo $msg_chkIPv6Address[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}

		var ipv6Addr = $('#ipv6_manual_addr').val().split(":");
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
			if (ipv6Addr[ix].length == 0) 	spaceCnt++;
		}

		if ((spaceCnt > 1 && ipv6Addr[0].length != 0 && ipv6Addr[ipv6Addr.length - 1].length != 0) || (spaceCnt == 0 && ipv6Addr.length != 8)) {
			alert("<?php echo $msg_chkIPv6Address[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		return true;
	}

	function GetVaildIPv6Setting()
	{
		if ($('#ipv6_use').is(':checked') == false || ($('#ipv6_use').is(':checked') && ($('#ipv6_default').is(':checked') || $('#ipv6_dhcp').is(':checked'))))	return true;
		if (CheckIPv6ManualAddress() == false)	return false;

		var ipv6Address = $('#ipv6_manual_addr').val();
		if (!TypeCheck(ipv6Address, IPv6)) 	{
			alert("<?php echo $msg_chkIPv6Address[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		var ipv6prefix = parseInt($('#ipv6_manual_prefix').val());
		if (ipv6prefix >= 0 && ipv6prefix <= 127) return true;
		else {
			alert("<?php echo $msg_IPv6Prefix0to127[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		return false;
	}

	function GetIsChangedValue()
	{
		if (parseInt($('#port_http').val()) != oldHTTPPort || parseInt($('#port_https').val()) != oldHTTPSPort) 	IsChangedPort = true;

		var ipv4Type = parseInt($('#ipv4_type option:selected').val());
		if (ipv4Type != oldIPType) return true;
		if (ipv4Type == 0) {
			if ($('#ipv4_addr').val() != oldStaticIP) 			return true;
			if ($('#ipv4_subnet').val() != oldStaticSubnet) 	return true;
		}
		else if (ipv4Type == 2) {
			if ($('#ipv4_pppoe_name').val() != oldID || $('#ipv4_pppoe_pw') != oldPW) return true;
			if ($('#ipv4_subnet').val() != oldDynamicSubnet) return true;
		}
		if (ipv4Type != 1 && $('#ipv4_gateway').val() != oldGateway) return true;
		if ($('#ipv4_dns1').val() != oldDNS1 || $('#ipv4_dns2').val() != oldDNS2) return true;

		if ($('#ipv6_use').is(':checked') != oldIPv6) 				return true;
		if (ipv6Mode != 1 && $('#ipv6_dhcp').is(':checked')) 		return true;	// add junghyun 2012.02.22 : dhcp not setting
		if (ipv6Mode != 3 && $('#ipv6_default').is(':checked')) 	return true;	// add junghyun 2012.02.22 : default not setting
		if (ipv6Mode != 4 && $('#ipv6_manual').is(':checked'))		return true;
		if ($('#ipv6_manual').is(':checked')) {
			if ($('#ipv6_manual_addr').val() != staticIPv6Address 	|| $('#ipv6_manual_prefix').val() != staticIPv6Prefix)		return true;
			if ($('#ipv6_manual_gateway').val() != oldIPv6Gateway)	return true;
		}
		else {
			if ($('#ipv6_manual_addr').val() != dynamicIPv6Address	|| $('#ipv6_manual_prefix').val() != dynamicIPv6Prefix)	return true;
		}
		
		return false;
	}

	function CheckIPv4PPPoE()
	{
		if($('#ipv4_pppoe_name').val().length == 0) {
			alert("<?php echo $msg_inputxDSLid[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}

		if($('#ipv4_pppoe_pw').val().length == 0) {
			alert("<?php echo $msg_inputxDSLPass[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		return true;
	}

	function CheckIPv4Address()
	{
		var ipPattern = /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/;
		var ipArray 	= $('#ipv4_addr').val().match(ipPattern);
		var smArray 	= $('#ipv4_subnet').val().match(ipPattern);
		var gwArray 	= $('#ipv4_gateway').val().match(ipPattern);
		var ip_num, gw_num, sm_num, not_sm_num;

		if(ipArray == null) {
			alert("<?php echo $msg_chkIPAddress[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		
		for(var index=1; index<5; index++){
			if(ipArray[index].length > 1){
				if(ipArray[index].charAt(0) == '0'){
					alert("<?php echo $msg_chkIPAddress[$GLOBALS['LANGINDEX']]; ?>");
					return false;
				}
			}
		}
		
		if(smArray == null) {
			alert("<?php echo $msg_chkSubnetMask[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}

		for(var index=1; index<5; index++){
			if(smArray[index].length > 1){
				if(smArray[index].charAt(0) == '0'){
					alert("<?php echo $msg_chkSubnetMask[$GLOBALS['LANGINDEX']]; ?>");
					return false;
				}
			}
		}

		if(gwArray == null) {
			alert("<?php echo $msg_chkGateway[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}

		for(var index=1; index<5; index++){
			if(gwArray[index].length > 1){
				if(gwArray[index].charAt(0) == '0'){
					alert("<?php echo $msg_chkGateway[$GLOBALS['LANGINDEX']]; ?>");
					return false;
				}
			}
		}	

		var ip_num 		= ((ipArray[1]&0xFF)<<24) + ((ipArray[2]&0xFF)<<16) + ((ipArray[3]&0xFF)<<8) + ((ipArray[4]&0xFF)<<0);
		var gw_num 		= ((gwArray[1]&0xFF)<<24) + ((gwArray[2]&0xFF)<<16) + ((gwArray[3]&0xFF)<<8) + ((gwArray[4]&0xFF)<<0);
		var sm_num 		= ((smArray[1]&0xFF)<<24) + ((smArray[2]&0xFF)<<16) + ((smArray[3]&0xFF)<<8) + ((smArray[4]&0xFF)<<0);
		var not_sm_num = (((~smArray[1])&0xFF)<<24) + (((~smArray[2])&0xFF)<<16) + (((~smArray[3])&0xFF)<<8) + (((~smArray[4])&0xFF)<<0);
		thisSegment 	= ipArray[1];

		if(thisSegment<1 || thisSegment>223) {
			alert("<?php echo $msg_chkIPAddress[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}

		for(i=2; i<5; i++) {
			thisSegment = ipArray[i];
			if(thisSegment>255) {
				alert("<?php echo $msg_chkIPAddress[$GLOBALS['LANGINDEX']]; ?>");
				return false;
			}
		}

		thisSegment = gwArray[1];
		if(thisSegment<1 || thisSegment>223) {
			alert("<?php echo $msg_chkGateway[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}

		for(i=2; i<5; i++) {
			thisSegment = gwArray[i];
			if(thisSegment>255) {
				alert("<?php echo $msg_chkGateway[$GLOBALS['LANGINDEX']]; ?>");
				return false;
			}
		}

		for(i=1; i<5; i++) {
			thisSegment = smArray[i];
			if(thisSegment>255) {
				alert("<?php echo $msg_chkSubnetMask[$GLOBALS['LANGINDEX']]; ?>");
				return false;
			}
		}

		for(i=0; i<32; i++) {
			var token = 1<<i;
			if((sm_num&token)>0) break;
		}

		for(i++; i<32; i++) {
			var token = 1<<i;
			if((sm_num&token)==0) {
				alert("<?php echo $msg_chkSubnetMask[$GLOBALS['LANGINDEX']]; ?>");
				return false;
			}
		}

		if(ip_num==gw_num) {
			alert("<?php echo $msg_chkIPAddress[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}

		if(((ip_num&not_sm_num)==not_sm_num) || ((ip_num&not_sm_num)==0) || ((ip_num&sm_num)==0)) {
			alert("<?php echo $msg_chkIPAddress[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}

		if(((gw_num&not_sm_num)==not_sm_num) || ((gw_num&not_sm_num)==0) || ((gw_num&sm_num)==0)) {
			alert("<?php echo $msg_chkGateway[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}

		if((ip_num&sm_num) != (gw_num&sm_num)) {
			alert("<?php echo $msg_chkIPAddress[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}

		return true;
	}

	function CheckIPv4DNS()
	{
		var ipPattern 	= /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/;
		var dnsArray1 	= $('#ipv4_dns1').val().match(ipPattern);
		var dnsArray2 	= $('#ipv4_dns2').val().match(ipPattern);

		if(dnsArray1 == null) {
			alert("<?php echo $msg_chkDNSserver1[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		
		for(var index=1; index<5; index++){
			if(dnsArray1[index].length > 1){
				if(dnsArray1[index].charAt(0) == '0'){
					alert("<?php echo $msg_chkDNSserver1[$GLOBALS['LANGINDEX']]; ?>");
					return false;
				}
			}
		}
		
		if(dnsArray2 == null) {
			alert("<?php echo $msg_chkDNSserver2[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}

		for(var index=1; index<5; index++){
			if(dnsArray2[index].length > 1){
				if(dnsArray2[index].charAt(0) == '0'){
					alert("<?php echo $msg_chkDNSserver2[$GLOBALS['LANGINDEX']]; ?>");
					return false;
				}
			}
		}

		thisSegment=dnsArray1[1];
		if(thisSegment<1 || thisSegment>223) {
			alert("<?php echo $msg_chkDNSserver1[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}

		thisSegment=dnsArray2[1];
		if(thisSegment<1 || thisSegment>223) {
			alert("<?php echo $msg_chkDNSserver2[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}

		for(i=2; i<4; i++) {
			thisSegment = dnsArray1[i];
			if(thisSegment>255) {
				alert("<?php echo $msg_chkDNSserver1[$GLOBALS['LANGINDEX']]; ?>");
				return false;
			}
		}
		thisSegment = dnsArray1[4];
		if(thisSegment > 254) {
			alert("<?php echo $msg_chkDNSserver1[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}

		for(i=2; i<4; i++) {
			thisSegment = dnsArray2[i];
			if(thisSegment>255) {
				alert("<?php echo $msg_chkDNSserver2[$GLOBALS['LANGINDEX']]; ?>");
				return false;
			}
		}
		thisSegment = dnsArray2[4];
		if(thisSegment > 254) {
			alert("<?php echo $msg_chkDNSserver2[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}

		return true;
	}

	function CheckPort()
	{
		var portValues = new Array();
		IsChangedHTTP = false;
		if (($('#port_http').val() == $('#port_vnp').val()) || ($('#port_https').val() == $('#port_vnp').val()) || ($('#port_https').val() == $('#port_http').val())) {
			alert("<?php echo $msg_portOverlap[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}

		if ($('#port_http').val() == "" || $('#port_http').val() == 3702 || $('#port_http').val() == 49152 || ($('#port_http').val() > -1 && $('#port_http').val() < 80) || ($('#port_http').val() > 80 && $('#port_http').val() < 1024) || $('#port_http').val() > 65535 || !TypeCheck($('#port_http').val(), NUM)) {
		 	alert("<?php echo $msg_errHTTPport[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}

		if ($('#port_https').val() == "" || $('#port_https').val() == 3702 || $('#port_https').val() == 49152 || ($('#port_https').val() > -1 && $('#port_https').val() < 443) || ($('#port_https').val() > 443 && $('#port_https').val() < 1024) || $('#port_https').val() > 65535 || !TypeCheck($('#port_https').val(), NUM)) {
		 	alert("<?php echo $msg_errHTTPSport[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}

		if ($('#port_vnp').val() == "" || $('#port_vnp').val() == 3702 || $('#port_vnp').val() == 49152 || ($('#port_vnp').val() > -1 && $('#port_vnp').val() < 1024) || ($('#port_vnp').val() > 65535) || !TypeCheck($('#port_vnp').val(), NUM)) {
			alert("<?php echo $msg_errDeviceport[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}

		if ($('#port_rtsp').val() == "" || $('#port_rtsp').val() == 3702 || $('#port_rtsp').val() == 49152 || ($('#port_rtsp').val()  > -1 && $('#port_rtsp').val() < 554) || ($('#port_rtsp').val() > 554 && $('#port_rtsp').val() < 1024) || $('#port_rtsp').val() > 65535 || !TypeCheck($('#port_rtsp').val(), NUM)) {
		 	alert("<?php echo $msg_errRTSPport[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}

		portValues[0] = $('#port_http').val();
		portValues[1] = $('#port_https').val();
		portValues[2] = $('#port_vnp').val();
		portValues[3] = $('#port_rtsp').val();
//		portValues[4] = $('#port_viewer').val();

		for (var index=0; index<3; ++index) {
			for (var index2=(index+1); index2<4; ++index2) {
				if (portValues[index] == portValues[index2]) {
			//		if (index == 2 && index2 == 4 && portValues[index] >= 4502 && portValues[index] <= 4534) continue;
					alert("<?php echo $msg_portOverlap[$GLOBALS['LANGINDEX']]; ?>  "+portValues[index]+","+portValues[index2]);
					return false;
				}
			}
		}
		return true;
	}

	function OnChangeIPv4Type()
	{
		var ipv4Type = parseInt($('#ipv4_type option:selected').val());
		switch(ipv4Type) {
			case 0:
				$('#ipv4_addr').removeAttr('disabled');
				$('#ipv4_subnet').removeAttr('disabled');
				$('#ipv4_gateway').removeAttr('disabled');
				$('#ipv4_pppoe_name').attr('disabled', 'disabled');
				$('#ipv4_pppoe_pw').attr('disabled', 'disabled');
				$('#ipv4_addr').val("<?php echo trim($ipConf->ipv4AddrConf->staticAddr->dataInfo['Address']['value']); ?>");
				$('#ipv4_subnet').val(oldStaticSubnet);
				$('.pppoe_space').hide();
				break;
			case 1:
				$('#ipv4_addr').attr('disabled', 'disabled');
				$('#ipv4_subnet').attr('disabled', 'disabled');
				$('#ipv4_gateway').attr('disabled', 'disabled');
				$('#ipv4_addr').val("<?php echo trim($ipConf->ipv4AddrConf->dynamicAddr->dataInfo['Address']['value']); ?>");
				$('#ipv4_subnet').val(oldDynamicSubnet);
				$('.pppoe_space').hide();
				break;
			case 2:
				$('#ipv4_addr').attr('disabled', 'disabled');
				$('#ipv4_subnet').attr('disabled', 'disabled');
				$('#ipv4_gateway').attr('disabled', 'disabled');
				$('#ipv4_addr').val("<?php echo trim($ipConf->ipv4AddrConf->dynamicAddr->dataInfo['Address']['value']); ?>");
				$('#ipv4_subnet').val(oldDynamicSubnet);
				$('#ipv4_pppoe_name').removeAttr('disabled');
				$('#ipv4_pppoe_pw').removeAttr('disabled');
				$('.pppoe_space').show();
				break;
		}
	}

	function OnClickIPv6Use()
	{
		if ($('#ipv6_use').is(':checked')) {
			$('#ipv6_default').removeAttr('disabled');
			$('#ipv6_dhcp').removeAttr('disabled');
			$('#ipv6_manual').removeAttr('disabled');

			$('#ipv6_manual_addr').removeAttr('disabled');
			$('#ipv6_manual_prefix').removeAttr('disabled');
			$('#ipv6_manual_gateway').removeAttr('disabled');
			OnChangeIPv6Type();
		}
		else {
			$('#ipv6_default').attr('disabled', 'disabled');
			$('#ipv6_dhcp').attr('disabled', 'disabled');
			$('#ipv6_manual').attr('disabled', 'disabled');

			$('#ipv6_manual_addr').attr('disabled', 'disabled');
			$('#ipv6_manual_prefix').attr('disabled', 'disabled');
			$('#ipv6_manual_gateway').attr('disabled', 'disabled');

		}
	}

	function OnChangeIPv6Type()
	{
		if ($('#ipv6_default').is(':checked') || $('#ipv6_dhcp').is(':checked')) {
			$('#ipv6_manual_addr').attr('disabled', 'disabled');
			$('#ipv6_manual_prefix').attr('disabled', 'disabled');
			$('#ipv6_manual_gateway').attr('disabled', 'disabled');
		}
		else if ($('#ipv6_manual').is(':checked')) {
			$('#ipv6_manual_addr').removeAttr('disabled');
			$('#ipv6_manual_prefix').removeAttr('disabled');
			$('#ipv6_manual_gateway').removeAttr('disabled');
		}
	}

	function OnLoad()
	{
		OnChangeIPv4Type();
	}

	</script>
	</head>
	<body onload="OnLoad()" onselectstart="return false">
		<div id="wrap">
			<?php
				require_once ('left_menu.cgi');
				require_once ('top_menu.cgi');
			?>
			<div id="container">
			<?php
				PrintLeftMenu($_SERVER['SCRIPT_NAME']);
			?>
			<div id="contents" >
				<div class="h3_tit mgt0" >
					<h3 class="wid220"><?php echo $t_IPv4Setup[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>
				<table class="data_write">
					<colgroup>
						<col style="width:180px;" />
						<col />
					</colgroup>
					<tbody>
						<tr>
							<th scope="row"><?php echo $t_IPType[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<select name="select" id="ipv4_type" class="selectbox_style" onchange="OnChangeIPv4Type();">
						         <option value="0" <?php if ($ipConf->ipv4AddrConf->dataInfo['Type']['value'] == 0) echo "selected=\"selected\""; ?>><?php echo $t_manual[$GLOBALS['LANGINDEX']]; ?></option>
									<option value="1" <?php if ($ipConf->ipv4AddrConf->dataInfo['Type']['value'] == 1) echo "selected=\"selected\""; ?>>DHCP</option>
									<option value="2" <?php if ($ipConf->ipv4AddrConf->dataInfo['Type']['value'] == 2) echo "selected=\"selected\""; ?>>PPPoE</option>
								</select>
							</td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_macAddress[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<input type="text" class="text" style="width:191px;" value="<?php echo $ipConf->dataInfo['HWAddress']['value']; ?>" disabled="disabled"/>
							</td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_IPAddress[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
							<?php
								$ipv4Addr = $ipConf->ipv4AddrConf->staticAddr->dataInfo['Address']['value'];
								if ($ipConf->ipv4AddrConf->dataInfo['Type']['value'] == 0) $ipv4Addr = $ipConf->ipv4AddrConf->dynamicAddr->dataInfo['Address']['value'];
							?>
								<input type="text" id="ipv4_addr" class="text" style="width:191px;" maxlength="15" onkeypress='CheckIPv4(event)' onkeydown='CheckIPv4(event)' value="<?php echo $ipv4Addr; ?>"/>
							</td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_subnetMask[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<input type="text" id="ipv4_subnet" class="text" style="width:191px;" maxlength="15" onkeypress='CheckIPv4(event)' onkeydown='CheckIPv4(event)' />
							</td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_gateway[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<input type="text" id="ipv4_gateway" class="text" style="width:191px;"  maxlength="15" onkeypress='CheckIPv4(event)' onkeydown='CheckIPv4(event)' value="<?php echo $gatewayConf->dataInfo['IPv4Gateway']['value'];; ?>"/>
							</td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_DNS1[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<input type="text" id="ipv4_dns1" class="text" style="width:191px;" maxlength="15" onkeypress='CheckIPv4(event)' onkeydown='CheckIPv4(event)' value="<?php echo $dnsConf->dnsManual[0]->dataInfo['Address']['value']; ?>"/>
							</td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_DNS2[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<input type="text" id="ipv4_dns2" class="text" style="width:191px;" maxlength="15" onkeypress='CheckIPv4(event)' onkeydown='CheckIPv4(event)' value="<?php echo $dnsConf->dnsManual[1]->dataInfo['Address']['value']; ?>"/>
							</td>
						</tr>
						<tr class="pppoe_space">
							<th scope="row"><?php echo $t_ID[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<input type="text" id="ipv4_pppoe_name" class="text" style="width:191px;" maxlength="20"  onkeypress='NoKorean(event)' onkeydown='NoKorean(event)' value="<?php echo $ipConf->ipv4AddrConf->dataInfo['XDSLUserName']['value']; ?>"
									<?php if ($ipConf->ipv4AddrConf->dataInfo['Type']['value'] != 2) echo "disabled=\"disabled\"";?>/>
							</td>
						</tr>
						<tr class="pppoe_space">
							<th scope="row"><?php echo $t_password[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<input type="password" id="ipv4_pppoe_pw" class="text" style="width:191px;" onkeypress='NoKorean(event)' onkeydown='NoKorean(event)' maxlength="20" value="<?php echo $ipConf->ipv4AddrConf->dataInfo['XDSLPassword']['value']; ?>"
									<?php if ($ipConf->ipv4AddrConf->dataInfo['Type']['value'] != 2) echo "disabled=\"disabled\"";?>/>
							</td>
						</tr>
						<script>
							<?php if ($ipConf->ipv4AddrConf->dataInfo['Type']['value'] == 2) { ?>
								$('.pppoe_space').hide();
							<?php } else { ?>
								$('.pppoe_space').show();
							<?php } ?>
						</script>
					</tbody>
				</table>
				<div class="h3_tit" >
					<h3 class="wid180"><?php echo $t_IPv6Setup[$GLOBALS['LANGINDEX']]; ?></h3>
					<table class="data_write" style="width:400px">
						<tbody>
							<tr>
								<td style="padding:0">
									<label><input type="checkbox" id="ipv6_use" style="margin-left:<?php if (GetBrowserName()=='IE') { if(ieversion() < 8) {echo '2';} else{echo '-3';} } else { echo '1'; } ?>px" <?php if ($ipConf->ipv6AddrConf->dataInfo['Enabled']['value'] == 1) echo "checked=\"checked\""; ?> onclick="OnClickIPv6Use()"/><?php echo $t_use[$GLOBALS['LANGINDEX']]; ?></label>
								</td>
							</tr>
						</tbody>
					</table>
				</div>
				<table class="data_write" >
					<colgroup>
						<col style="width:<?php if (GetBrowserName()=='IE' && ieversion() < 8) {echo '152';}else{echo '180';}?>px" />
						<col />
					</colgroup>
					<?php
						$ipv6Use = $ipConf->ipv6AddrConf->dataInfo['Enabled']['value'];
						$ipv6Mode = $ipConf->ipv6AddrConf->dataInfo['DHCP']['value'];
					?>
					<tbody>
						<tr>
							<td><label class="labelBold" for="ipv6_default"><input type="radio" name="ipv6_type" id="ipv6_default" value="3" onclick="OnChangeIPv6Type()" <?php if ($ipv6Mode==3) echo "checked=\"checked\""; if (!$ipv6Use) echo " disabled=\"disabled\""; ?>/><?php echo $t_default[$GLOBALS['LANGINDEX']]; ?></label></td>
							<td></td>
						</tr>
						<tr>
							<td style="padding-left:38px"><?php echo $t_IPv6Address[$GLOBALS['LANGINDEX']]; ?></td>
							<td>
								<input type="text" id="ipv6_default_addr" class="text" style="width:191px;" value="<?php echo $ipConf->ipv6AddrConf->defaultAddr->dataInfo['Address']['value']; ?>" disabled="disabled"/>
								<span class="color01">/</span>
								<input type="text" id="ipv6_default_prefix" class="text" style="width:30px;" value="<?php echo $ipConf->ipv6AddrConf->defaultAddr->dataInfo['Prefix']['value']; ?>" disabled="disabled"/>
							</td>
						</tr>
						<tr>
							<td><label class="labelBold" for="ipv6_dhcp"><input type="radio" name="ipv6_type" id="ipv6_dhcp"  value="1" onclick="OnChangeIPv6Type()" <?php if ($ipv6Mode==1) echo "checked=\"checked\""; if (!$ipv6Use) echo "disabled=\"disabled\""; ?>/>DHCP</label></td>
							<td></td>
						</tr>
						<tr>
							<td  style="padding-left:38px"><?php echo $t_IPv6Address[$GLOBALS['LANGINDEX']]; ?></td>
							<td>
								<input type="text" id="ipv6_dhcp_addr" class="text" style="width:191px;" disabled="disabled" value="<?php echo $ipConf->ipv6AddrConf->dynamicAddr->dataInfo['Address']['value']; ?>" />
								<span class="color01">/</span>
								<input type="text" id="ipv6_dhcp_prefix" class="text" style="width:30px;" disabled="disabled" value="<?php echo $ipConf->ipv6AddrConf->dynamicAddr->dataInfo['Prefix']['value']; ?>" />
							</td>
						</tr>
						<tr>
							<td><label class="labelBold" for="ipv6_manual"><input type="radio" name="ipv6_type" id="ipv6_manual" value="4" onclick="OnChangeIPv6Type()" <?php if ($ipv6Mode==4) echo "checked=\"checked\""; if (!$ipv6Use) echo "disabled=\"disabled\""; ?>/><?php echo $t_manual[$GLOBALS['LANGINDEX']]; ?></label></td>
							<td></td>
						</tr>
						<tr>
							<td style="padding-left:38px; width:"><?php echo $t_IPv6Address[$GLOBALS['LANGINDEX']]; ?></td>
							<td>
								<input type="text" id="ipv6_manual_addr" class="text" style="width:191px;" maxlength="39" onkeypress="CheckIPv6(event, 'press')" onkeydown="CheckIPv6(event, 'down')" value="<?php echo $ipConf->ipv6AddrConf->staticAddr->dataInfo['Address']['value']; ?>" <?php if (!$ipv6Use || $ipv6Mode!=4) echo "disabled=\"disabled\""; ?>/>
								<span class="color01">/</span>
								<input type="text" id="ipv6_manual_prefix" class="text" style="width:30px;" maxlength="3" onkeypress="IsNum(event)" onkeydown="OnlyNUm(event);" value="<?php echo $ipConf->ipv6AddrConf->staticAddr->dataInfo['Prefix']['value']; ?>" <?php if (!$ipv6Use || $ipv6Mode!=4) echo "disabled=\"disabled\""; ?>/>
							</td>
						</tr>
						<tr>
							<td style="padding-left:38px"><?php echo $t_gateway[$GLOBALS['LANGINDEX']]; ?></td>
							<td><input type="text" id="ipv6_manual_gateway" class="text" style="width:191px;" maxlength="39" onkeypress="CheckIPv6(event, 'press')" onkeydown="CheckIPv6(event, 'down')" value="<?php echo $gatewayConf->dataInfo['IPv6Gateway']['value']; ?>" <?php if (!$ipv6Use || $ipv6Mode!=4) echo "disabled=\"disabled\""; ?>/></td>
						</tr>
					</tbody>
				</table>
				<div class="h3_tit" >
					<h3><?php echo $menu_port[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>
				<table class="data_write">
					<colgroup>
						<col style="width:180px;" />
						<col />
					</colgroup>
					<tbody>
						<tr>
							<th scope="row">HTTP</th>
							<td>
								<input type="text" id="port_http" class="text" style="width:124px;" onkeypress="IsNum(event)" onkeydown="OnlyNUm(event);" value="<?php echo $protocolConf->protocol[0]->dataInfo['Port']['value']; ?>" maxlength="5" />
							</td>
						</tr>
						<tr>
							<th scope="row">HTTPS</th>
							<td>
								<input type="text" id="port_https" class="text" style="width:124px;" onkeypress="IsNum(event)" onkeydown="OnlyNUm(event);" value="<?php echo $protocolConf->protocol[1]->dataInfo['Port']['value']; ?>" maxlength="5" />
							</td>
						</tr>						
						<tr>
							<th scope="row">RTSP</th>
							<td>
								<input type="text" id="port_rtsp" class="text" style="width:124px;" onkeypress="IsNum(event)" onkeydown="OnlyNUm(event);" value="<?php echo $protocolConf->protocol[2]->dataInfo['Port']['value']; ?>" maxlength="5" />
								<label><input type="checkbox" id="port_rtsp_timeout" <?php if ($protocolConf->rtspTimeout == 0) echo "checked=\"checked\""; ?>/><?php echo $t_useTimeout[$GLOBALS['LANGINDEX']]; ?></label>
							</td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_deviceport[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<input type="text" id="port_vnp" class="text" style="width:124px;" onkeypress="IsNum(event)" onkeydown="OnlyNUm(event);" value="<?php echo $protocolConf->protocol[3]->dataInfo['Port']['value']; ?>" maxlength="5" />
							</td>
						</tr>
						<!-- tr>
							<th scope="row"><?php echo $t_webStreamingport[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<input type="text" id="port_viewer" class="text" style="width:124px;" value="<?php echo $protocolConf->protocol[5]->dataInfo['Port']['value']; ?>" disabled="disabled"/>
							</td>
						</tr-->
					</tbody>
				</table>
				<div class="btn_right">
					<a id="mid_ok_btn" class="btn_apply" href="javascript:OnClickApply()"><?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?></a>
				</div>
			</div>
		</div>
	</div>
</body>
</html>

