<?php
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_menu.cgi');
require_once ('../language/language_network_qos.cgi');

$classInstances= GetClassInstance('QoS');
$qos = $classInstances['QoSConfiguration'];
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
		height:1000px;
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
	var qos_ipv4_cnt = 0;
	var qos_ipv6_cnt = 0;

	function OnClickApply()
	{
		var msg = '';
		for (var index=0; index<10; ++index) {
			if($('tr').hasClass('qos_ipv4_list_'+index)) {
				if (!CheckValidIPv4Address($('#qos_ipv4_addr_'+index).val())) {
					 alert("<?php echo $msg_chkIPAddress[$GLOBALS['LANGINDEX']]; ?>");
					 return;
				}
				if (!CheckIPv4Prefix($('#qos_ipv4_prefix_'+index).val()) || !TypeCheck($('#qos_ipv4_prefix_'+index).val(), NUM)) {
					 alert("<?php echo $msg_IPv4Prefix1to32[$GLOBALS['LANGINDEX']]; ?>");
					 return;
				}
				if ((parseInt($('#qos_ipv4_dscp_'+index).val()) < 0 || parseInt($('#qos_ipv4_dscp_'+index).val()) > 63) || !TypeCheck($('#qos_ipv4_dscp_'+index).val(), NUM)) {
					 alert("<?php echo $msg_invalidDSCP[$GLOBALS['LANGINDEX']]; ?>");
					 return;
				}
				if ($('#qos_ipv4_prefix_'+index).val() == ''){
					alert("<?php echo $msg_IPv4Prefix1to32[$GLOBALS['LANGINDEX']]; ?>");
					return;
				}

			}
		}

		for (var index=0; index<10; ++index) {
			if($('tr').hasClass('qos_ipv4_list_'+index)) {
				if (!CheckDuplicatedAddress('qos_ipv4', 10)) {
					alert("<?php echo $msg_IPv4AddressDuplicate[$GLOBALS['LANGINDEX']]; ?>");
					return;
				}
				
				msg += "<IPv4QoS>";
				msg += "<Enabled>"+$('#qos_ipv4_enable_'+index).val()+"</Enabled>";
				msg += "<Address>"+$('#qos_ipv4_addr_'+index).val()+"</Address>";
				msg += "<Prefix>"+$('#qos_ipv4_prefix_'+index).val()+"</Prefix>";
				msg += "<DSCP>"+$('#qos_ipv4_dscp_'+index).val()+"</DSCP>";
				msg += "</IPv4QoS>";
			}
		}

		for (var index=0; index<10; ++index) {
			if($('tr').hasClass('qos_ipv6_list_'+index)) {
				if (!CheckValidIPv6Address($('#qos_ipv6_addr_'+index).val())) {
					 alert("<?php echo $msg_chkIPv6Address[$GLOBALS['LANGINDEX']]; ?>");
					 return;
				}

				if (!CheckIPv6Prefix($('#qos_ipv6_prefix_'+index).val()) || !TypeCheck($('#qos_ipv6_prefix_'+index).val(), NUM)) {
					 alert("<?php echo $msg_IPv6Prefix1to128[$GLOBALS['LANGINDEX']]; ?>");
					 return;
				}
				if ((parseInt($('#qos_ipv6_dscp_'+index).val()) < 0 || parseInt($('#qos_ipv6_dscp_'+index).val()) > 63) || !TypeCheck($('#qos_ipv6_dscp_'+index).val(), NUM)) {
					 alert("<?php echo $msg_invalidDSCP[$GLOBALS['LANGINDEX']]; ?>");
					 return;
				}
				if ($('#qos_ipv6_prefix_'+index).val() == '') {
					 alert("<?php echo $msg_IPv6Prefix1to128[$GLOBALS['LANGINDEX']]; ?>");
					 return;
				}

			}
		}

		for (var index=0; index<10; ++index) {
			if($('tr').hasClass('qos_ipv6_list_'+index)) {	
				if (!CheckDuplicatedAddress('qos_ipv6', 10) || !CheckCrashIPv6Address()) {
					alert("<?php echo $msg_IPv4AddressDuplicate[$GLOBALS['LANGINDEX']]; ?>");
					return;
				}
				
				msg += "<IPv6QoS>";
				msg += "<Enabled>"+$('#qos_ipv6_enable_'+index).val()+"</Enabled>";
				msg += "<Address>"+$('#qos_ipv6_addr_'+index).val()+"</Address>";
				msg += "<Prefix>"+$('#qos_ipv6_prefix_'+index).val()+"</Prefix>";
				msg += "<DSCP>"+$('#qos_ipv6_dscp_'+index).val()+"</DSCP>";
				msg += "</IPv6QoS>";
			}
		}
		RequestAjaxMsg("<SetQoS>"+msg+"</SetQoS>", "<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $GLOBALS['REQUEST_URI'].'?seq='.$_SESSION['count'] ?>");
	}

	function CheckCrashIPv6Address()
	{
		var temp1 = new Array();
		var temp2 = new Array();
		for (var index=0; index<9; ++index) {
			for (var index2=(index+1); index2<10; ++index2) {
				if($('tr').hasClass('qos_ipv6_list_'+index) && $('tr').hasClass('qos_ipv6_list_'+index2)) {
					temp1 = SplitIPv6Address($('#qos_ipv6_addr_'+index).val().toLowerCase());
					temp2 = SplitIPv6Address($('#qos_ipv6_addr_'+index2).val().toLowerCase());
					if ((temp1[0]==temp2[0]) && (temp1[1]==temp2[1])  && (temp1[2]==temp2[2]) && (temp1[3]==temp2[3]) && (temp1[4]==temp2[4]) && (temp1[5]==temp2[5]) && (temp1[6]==temp2[6]) && (temp1[7]==temp2[7])) {
						return false;
					}
				}
			}
		}
		return true;
		
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
	function OnChangeIPv4Address(index)
	{
		var ipPattern	= /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/;
		var ipArray 	= $('#qos_ipv4_addr_'+index).val().match(ipPattern);

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
			if (thisSegment>255) {
				alert("<?php echo $msg_chkIPAddress[$GLOBALS['LANGINDEX']]; ?>");
				return false;
			}
		}

		return OnChangeIPv4Prefix(index);
	}

	function OnChangeIPv4Prefix(index)
	{
		if(parseInt($('#qos_ipv4_prefix_'+index).val()) < 1 || parseInt($('#qos_ipv4_prefix_'+index).val()) > 32) {
			alert("<?php echo $msg_IPv4Prefix1to32[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		return true;
	}

	function OnChangeIPv6Address(index)
	{
		var ipv6Addr = $('#qos_ipv6_addr_'+index).val().split(":");
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
		return OnChangeIPv6Prefix(index);
	}


	function OnChangeIPv6Prefix(index)
	{
		if(parseInt($('#qos_ipv6_prefix_'+index).val()) < 1 || parseInt($('#qos_ipv6_prefix_'+index).val()) > 128) {
			alert("<?php echo $msg_IPv6Prefix1to128[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		return true;
	}

	function OnChangeIPv4DSCP(index)
	{
		if(parseInt($('#qos_ipv4_dscp_'+index).val()) < 0 || parseInt($('#qos_ipv4_dscp_'+index).val()) > 63) {
			alert("<?php echo $msg_invalidDSCP[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		return true;
	}

	function OnChangeIPv6DSCP(index)
	{
		if(parseInt($('#qos_ipv6_dscp_'+index).val()) < 0 || parseInt($('#qos_ipv6_dscp_'+index).val()) > 63) {
			alert("<?php echo $msg_invalidDSCP[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		return true;
	}

	function OnClickQosList(protocol)
	{
		var selNo = $("input[name='qos_"+protocol+"_select']:checked").val();
		if ((selNo != oldSelNo || protocol != oldSelProtocol) && typeof oldSelNo != "undefined") {
			$('#qos_'+oldSelProtocol+'_select_'+oldSelNo).prop('checked', false);
			$('#qos_'+oldSelProtocol+'_enable_'+oldSelNo).attr('disabled', 'disabled');
			$('#qos_'+oldSelProtocol+'_enable_'+oldSelNo).parent().css('color', '#6d6d6d');
			$('#qos_'+oldSelProtocol+'_addr_'+oldSelNo).attr('disabled', 'disabled');
			$('#qos_'+oldSelProtocol+'_prefix_'+oldSelNo).attr('disabled', 'disabled');
			$('#qos_'+oldSelProtocol+'_dscp_'+oldSelNo).attr('disabled', 'disabled');
		}
		$('#qos_'+protocol+'_enable_'+selNo).removeAttr('disabled');
		$('#qos_'+protocol+'_enable_'+selNo).parent().css('color', '#1c1c1c');
		$('#qos_'+protocol+'_addr_'+selNo).removeAttr('disabled');
		$('#qos_'+protocol+'_prefix_'+selNo).removeAttr('disabled');
		$('#qos_'+protocol+'_dscp_'+selNo).removeAttr('disabled');
		oldSelNo = selNo;
		oldSelProtocol = protocol;
	}

	function OnClickAdd(protocol)
	{
		if ((protocol == 'ipv4' && qos_ipv4_cnt == 10) || (protocol == 'ipv6' && qos_ipv6_cnt == 10)) {
			alert("<?php echo $msg_cannot_add[$GLOBALS['LANGINDEX']]; ?>");
			return;
		}

		var addNo = 0;
		for(var index=0; index<10; ++index) {
			if($('tr').hasClass('qos_'+protocol+'_list_'+index)) continue;
			addNo = index;
			break;
		}

		if (protocol == 'ipv4') {
			$('#qos_ipv4_list').append(
				"<tr class='qos_ipv4_list_"+addNo+"'>\
					<td><input type='radio' name='qos_ipv4_select' id='qos_ipv4_select_"+addNo+"' onClick='OnClickQosList(\"ipv4\");' value='"+addNo+"' checked='checked'/></td>\
					<td><select id='qos_ipv4_enable_"+addNo+"' class='selectbox_style' style='width:110px'><option value='0'><?php echo $t_off[$GLOBALS['LANGINDEX']]; ?></option><option value='1' selected='selected'><?php echo $t_on[$GLOBALS['LANGINDEX']]; ?></option></select></td>\
					<td><input type='text' id='qos_ipv4_addr_"+addNo+"' class='listtext' style='width:300px;' value='' maxlength='15' onpaste='javascript:return false;' onkeypress='CheckIPv4(event)' onkeydown='CheckIPv4(event)' onChange='OnChangeIPv4Address("+addNo+")' onclick='OnClickInput(4,\"addr\");'/></td>\
					<td><input type='text' id='qos_ipv4_prefix_"+addNo+"' class='listtext' style='width:30px;' value='32' maxlength='2' onpaste='javascript:return false;' onkeypress='IsNum(event)' onkeydown='OnlyNUm(event);' onchange='OnChangeIPv4Prefix("+addNo+")' onclick='OnClickInput(4,\"prefix\");'/></td>\
					<td><input type='text' id='qos_ipv4_dscp_"+addNo+"' class='listtext' style='width:30px;' value='63' maxlength='2' onpaste='javascript:return false;' onkeypress='IsNum(event)' onkeydown='OnlyNUm(event);' onchange='OnChangeIPv4DSCP("+addNo+")' onclick='OnClickInput(4,\"dscp\");' /></td>\
				</tr>"
			);
			qos_ipv4_cnt++;
		}
		else {
			$('#qos_ipv6_list').append(
				"<tr class='qos_ipv6_list_"+addNo+"'>\
					<td><input type='radio' name='qos_ipv6_select' id='qos_ipv6_select_"+addNo+"' onClick='OnClickQosList(\"ipv6\");' value='"+addNo+"' checked='checked'/></td>\
					<td><select id='qos_ipv6_enable_"+addNo+"' class='selectbox_style' style='width:110px'><option value='0'><?php echo $t_off[$GLOBALS['LANGINDEX']]; ?></option><option value='1' selected='selected'><?php echo $t_on[$GLOBALS['LANGINDEX']]; ?></option></select></td>\
					<td><input type='text' id='qos_ipv6_addr_"+addNo+"' class='listtext' style='width:300px;' value='' maxlength='39' onpaste='javascript:return false;' onkeypress=\"CheckIPv6(event, 'press')\" onkeydown=\"CheckIPv6(event, 'down')\" onChange='OnChangeIPv6Address("+addNo+")' onclick='OnClickInput(6,\"addr\");'/></td>\
					<td><input type='text' id='qos_ipv6_prefix_"+addNo+"' class='listtext' style='width:30px;' value='128' maxlength='3' onpaste='javascript:return false;' onkeypress='IsNum(event)' onkeydown='OnlyNUm(event);' onchange='OnChangeIPv6Prefix("+addNo+")' onclick='OnClickInput(6,\"prefix\");'/></td>\
					<td><input type='text' id='qos_ipv6_dscp_"+addNo+"' class='listtext' style='width:30px;' value='63' maxlength='2' onpaste='javascript:return false;' onkeypress='IsNum(event)' onkeydown='OnlyNUm(event);' onchange='OnChangeIPv6DSCP("+addNo+")' onclick='OnClickInput(6,\"dscp\"); '/></td>\
				</tr>"
			);
			qos_ipv6_cnt++;
		}
		$('#qos_'+protocol+'_enable_'+addNo).styledSelect( {innerClass:'selectbox_style_option'} );
		$('#qos_'+oldSelProtocol+'_select_'+oldSelNo).prop('checked', false);
		OnClickQosList(protocol);
	}

	function OnClickInput(protocol, type)
	{

		var selNo = $("input[name='qos_ipv"+protocol+"_select']:checked").val();

		$('#qos_ipv'+protocol+'_'+type+'_'+selNo).focus();
	}

	function OnClickDelete(protocol)
	{
		if (!CheckDeletedTarget('qos_'+protocol)) return;
		OnClickQosList(protocol);
	}

	function OnLoad() {}

		</script>
	</head>
	<body onload="OnLoad()" onselectstart="return false">
		<div id="wrap">
			<div id="head">
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
					<h3>IPv4</h3>
				</div>
				<table id="qos_ipv4_list" class="data_table2" style="width:680px;table-layout:fixed;">
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
							<th>DSCP</th>
						</tr>
					</thead>
					<tbody>
			<?php
				$qosCnt = 0;
				for ($index=0; $index<10; ++$index) {
					if ($qos->ipv4QoS[$index]->dataInfo['Address']['value'] != "") {
			?>
						<tr class="qos_ipv4_list_<?php echo $qosCnt; ?>">
							<td><input type="radio" name="qos_ipv4_select" id="qos_ipv4_select_<?php echo $qosCnt; ?>" onClick="OnClickQosList('ipv4');" value="<?php echo $qosCnt; ?>"/></td>
							<td>
								<select id="qos_ipv4_enable_<?php echo $qosCnt; ?>" class="selectbox_style" style="width:110px" disabled="disabled">
									<option value="0" <?php if ($qos->ipv4QoS[$index]->dataInfo['Enabled']['value'] == 0) echo "selected=\"selected\""; ?>><?php echo $t_off[$GLOBALS['LANGINDEX']]; ?></option>
									<option value="1" <?php if ($qos->ipv4QoS[$index]->dataInfo['Enabled']['value'] == 1) echo "selected=\"selected\""; ?>><?php echo $t_on[$GLOBALS['LANGINDEX']]; ?></option>
								</select>
								<script>$('#qos_ipv4_enable_<?php echo $qosCnt; ?>').styledSelect( {innerClass:'selectbox_style_option'} );</script>
							</td>
							<td><input type="text" id="qos_ipv4_addr_<?php echo $qosCnt; ?>" class="listtext" style="width:300px;" value="<?php echo trim($qos->ipv4QoS[$index]->dataInfo['Address']['value']); ?>" maxlength="15" onpaste="javascript:return false;" onkeypress='CheckIPv4(event)' onkeydown='CheckIPv4(event)' onChange="OnChangeIPv4Address(<?php echo $qosCnt; ?>)" disabled onclick="OnClickInput(4,'addr');"/></td>
							<td><input type="text" id="qos_ipv4_prefix_<?php echo $qosCnt; ?>" class="listtext" style="width:30px;" value="<?php echo $qos->ipv4QoS[$index]->dataInfo['Prefix']['value']; ?>" maxlength="2" onpaste="javascript:return false;" onkeypress="IsNum(event)" onkeydown="OnlyNUm(event);" onchange="OnChangeIPv4Prefix(<?php echo $qosCnt; ?>)" disabled="disabled" onclick="OnClickInput(4,'prefix');"/></td>
							<td><input type="text" id="qos_ipv4_dscp_<?php echo $qosCnt; ?>" class="listtext" style="width:30px;" value="<?php echo $qos->ipv4QoS[$index]->dataInfo['DSCP']['value']; ?>" maxlength="2" onpaste="javascript:return false;" onkeypress="IsNum(event)" onkeydown="OnlyNUm(event);" onchange="OnChangeIPv4DSCP(<?php echo $qosCnt; ?>)" disabled="disabled"  onclick="OnClickInput(4,'dscp');" /></td>
						</tr>
			<?php
						$qosCnt++;
					}
				}
			?>
					</tbody>
				</table>
				<script>qos_ipv4_cnt = parseInt(<?php echo $qosCnt; ?>);	</script>
				<div class="btn_add_left">
					<a class="btn_type01" href="javascript:OnClickAdd('ipv4')"><?php echo $t_add[$GLOBALS['LANGINDEX']]; ?></a>
					&nbsp;
					<a class="btn_type01" href="javascript:OnClickDelete('ipv4')"><?php echo $t_delete[$GLOBALS['LANGINDEX']]; ?></a>
				</div>

				<div class="h3_tit">
					<h3>IPv6</h3>
				</div>
				<table id="qos_ipv6_list" class="data_table2" style="width:680px;table-layout:fixed;">
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
							<th>DSCP</th>
						</tr>
					</thead>
					<tbody>
			<?php
				$qosCnt = 0;
				for ($index=0; $index<10; ++$index) {
					if ($qos->ipv6QoS[$index]->dataInfo['Address']['value'] != "") {
			?>
						<tr class="qos_ipv6_list_<?php echo $qosCnt; ?>">
							<td><input type="radio" name="qos_ipv6_select" id="qos_ipv6_select_<?php echo $qosCnt; ?>" onClick="OnClickQosList('ipv6');" value="<?php echo $qosCnt; ?>"/></td>
							<td>
								<select id="qos_ipv6_enable_<?php echo $qosCnt; ?>" class="selectbox_style" style="width:110px" disabled="disabled">
									<option value="0" <?php if ($qos->ipv6QoS[$index]->dataInfo['Enabled']['value'] == 0) echo "selected=\"selected\""; ?>><?php echo $t_off[$GLOBALS['LANGINDEX']]; ?></option>
									<option value="1" <?php if ($qos->ipv6QoS[$index]->dataInfo['Enabled']['value'] == 1) echo "selected=\"selected\""; ?>><?php echo $t_on[$GLOBALS['LANGINDEX']]; ?></option>
								</select>
								<script>$('#qos_ipv6_enable_<?php echo $qosCnt; ?>').styledSelect( {innerClass:'selectbox_style_option'} );</script>
							</td>
							<td><input type="text" id="qos_ipv6_addr_<?php echo $qosCnt; ?>" class="listtext" style="width:300px;" value="<?php echo trim($qos->ipv6QoS[$index]->dataInfo['Address']['value']); ?>" maxlength="39" onpaste="javascript:return false;" onkeypress="CheckIPv6(event, 'press')" onkeydown="CheckIPv6(event, 'down')" onChange="OnChangeIPv6Address(<?php echo $qosCnt; ?>)" disabled="disabled" onclick="OnClickInput(6,'addr');"/></td>
							<td><input type="text" id="qos_ipv6_prefix_<?php echo $qosCnt; ?>" class="listtext" style="width:30px;" value="<?php echo $qos->ipv6QoS[$index]->dataInfo['Prefix']['value']; ?>" maxlength="3" onpaste="javascript:return false;" onkeypress="IsNum(event)" onkeydown="OnlyNUm(event);" onchange="OnChangeIPv6Prefix(<?php echo $qosCnt; ?>)" disabled="disabled" onclick="OnClickInput(6,'prefix');"/></td>
							<td><input type="text" id="qos_ipv6_dscp_<?php echo $qosCnt; ?>" class="listtext" style="width:30px;" value="<?php echo $qos->ipv6QoS[$index]->dataInfo['DSCP']['value']; ?>" maxlength="2" onpaste="javascript:return false;" onkeypress="IsNum(event)" onkeydown="OnlyNUm(event);" onchange="OnChangeIPv6DSCP(<?php echo $qosCnt; ?>)" disabled="disabled" onclick="OnClickInput(6,'dscp');"/></td>
						</tr>

				<?php
						$qosCnt++;
					}
				}
				?>
					</tbody>
				</table>
				<script>qos_ipv6_cnt = parseInt(<?php echo $qosCnt; ?>);	</script>
				<div class="btn_add_left">
					<a class="btn_type01" href="javascript:OnClickAdd('ipv6')"><?php echo $t_add[$GLOBALS['LANGINDEX']]; ?></a>	&nbsp;
					<a class="btn_type01" href="javascript:OnClickDelete('ipv6')"><?php echo $t_delete[$GLOBALS['LANGINDEX']]; ?></a>
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
