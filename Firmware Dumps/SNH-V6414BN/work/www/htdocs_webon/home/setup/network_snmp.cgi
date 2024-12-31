<?php
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_menu.cgi');
require_once ('../language/language_network_snmp.cgi');

$classInstances= GetClassInstance('SNMP');
$snmp	= $classInstances['SNMPConfiguration'];
$snmpTrap = $classInstances['SNMPTrapConfiguration'];
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="kr" xml:lang="kr">
<head>
	<title>iPOLiS NETWORK CAMERA WEBVIEWER</title>
	<meta http-equiv="X-UA-Compatible" content="IE=Edge; requiresActiveX=true">
	<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
	<link rel="stylesheet" type="text/css" href="../css/techwin.css" />
	<script type="text/javascript" src="../js/jquery-1.9.1.js"></script>
	<script type="text/javascript" src="../js/lnb.js"></script>
	<script type="text/javascript" src="../js/common_function.js"></script>
	<script type="text/javascript" language="javascript">

	var localSeq				= <?php echo $_SESSION['count']; ?>;

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

<?php
	if (trim($snmp->dataInfo['SecurityPassword']['value'])=='') {
?>
	var PWset = false;
<?php
	}
	else 
	{
?>
	var PWset = true;
<?php
	}
?>


	$(document).ready(function(){ lnbonoff("lnb_network"); });

	var httpsType = parseInt(<?php echo $classInstances['Information']->dataInfo['IsHTTPS']['value']; ?>);

	function OnClickApply()
	{
		if ($('#snmp_ver2c').is(':checked')) {
			if( (!TypeCheck($('#snmp_ver2c_read').val(), NUM+ALPHA)) || $('#snmp_ver2c_read').val().length < 4) {
				alert("<?php echo $msg_invalid_readcommunity[$GLOBALS['LANGINDEX']]; ?>");
				return;
			}
			if( (!TypeCheck($('#snmp_ver2c_write').val(), NUM+ALPHA)) || $('#snmp_ver2c_write').val().length < 4) {
				alert("<?php echo $msg_invalid_writecommunity[$GLOBALS['LANGINDEX']]; ?>");
				return;
			}
		}

		if ($('#snmp_ver3').is(':checked')) {
			if(!($('#snmp_ver3_pw').val().length == 0  && PWset))
			{	
				if( (!TypeCheck($('#snmp_ver3_pw').val(), NUM+ALPHA)) || $('#snmp_ver3_pw').val().length < 8) {
					alert("<?php echo $msg_invalid_pw[$GLOBALS['LANGINDEX']]; ?>");
					return;
				}
			}
		}

		if (httpsType == 1) {
			if ($('#snmp_ver1').is(':checked') == false && $('#snmp_ver2c').is(':checked') == false && $('#snmp_ver3').is(':checked') == false) {
				alert("<?php echo $msg_select_SNMP[$GLOBALS['LANGINDEX']]; ?>");
				return;
			}
		}
		else {
			if ($('#snmp_ver1').is(':checked') == false && $('#snmp_ver2c').is(':checked') == false) {
				alert("<?php echo $msg_select_SNMP[$GLOBALS['LANGINDEX']]; ?>");
				return;
			}
		}

		if ($('#snmptrap_enable').is(':checked')) {
			if (!CheckValidIPv4Address($('#snmptrap_address').val())) {
				 alert("<?php echo $msg_chkIPAddress[$GLOBALS['LANGINDEX']]; ?>");
				 return;
			}

			if( (!TypeCheck($('#snmptrap_community').val(), NUM+ALPHA)) || $('#snmptrap_community').val().length < 4) {
				alert("<?php echo $msg_invalid_community[$GLOBALS['LANGINDEX']]; ?>");
				return;
			}
		}

		var msg = "<SetSNMP>";
		msg += "<EnabledVersion1>"+($('#snmp_ver1').is(':checked') ? 1 : 0)+"</EnabledVersion1>";
		msg += "<EnabledVersion2>"+($('#snmp_ver2c').is(':checked') ? 1 : 0)+"</EnabledVersion2>";
		msg += "<EnabledVersion3>"+($('#snmp_ver3').is(':checked') ? 1 : 0)+"</EnabledVersion3>";
		msg += "<ReadCommunity>"+$('#snmp_ver2c_read').val()+"</ReadCommunity>";
		msg += "<WriteCommunity>"+$('#snmp_ver2c_write').val()+"</WriteCommunity>";
		if(!($('#snmp_ver3_pw').val().length == 0  && PWset))
		{
			msg += "<SecurityPassword>"+$('#snmp_ver3_pw').val()+"</SecurityPassword>";
		}
		msg += "</SetSNMP>";
		RequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, 'SNMP');
		localSeq++;

		msg = "<SetSNMPTrap>";
		msg += "<Enabled>"+($('#snmptrap_enable').is(':checked') ? 1 : 0)+"</Enabled>";
		msg += "<TrapInfo0>";
		msg += "<Address>"+$('#snmptrap_address').val()+"</Address>";
		msg += "<Community>"+$('#snmptrap_community').val()+"</Community>";
		msg += "<AuthenticationFailure>"+($('#snmptrap_authfail').is(':checked') ? 1 : 0)+"</AuthenticationFailure>";
		<?php if ($GLOBALS['M_SUPPORT_EVENT_ND']) { ?>
		msg += "<LinkUp>"+($('#snmptrap_linkup').is(':checked') ? 1 : 0)+"</LinkUp>";
		<?php } ?>
		<?php for($i=1;$i<=$GLOBALS['M_ALARMIN_COUNT'];$i++) { ?>
		msg += "<AlarmIn<?php echo $i;?>>"+($('#snmptrap_alarmin<?php echo $i;?>').is(':checked') ? 1 : 0)+"</AlarmIn<?php echo $i;?>>";
		<?php } ?>
		<?php for($i=1;$i<=$GLOBALS['M_ALARMOUT_COUNT'];$i++) { ?>
		msg += "<AlarmOut<?php echo $i;?>>"+($('#snmptrap_alarmout<?php echo $i;?>').is(':checked') ? 1 : 0)+"</AlarmOut<?php echo $i;?>>";
		<?php } ?>
		msg += "<Tampering>"+($('#snmptrap_tampering').is(':checked') ? 1 : 0)+"</Tampering>";
		msg += "</TrapInfo0>";
		msg += "</SetSNMPTrap>";
		RequestAjaxMsg(msg, "<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, 'SNMPTrap');
	}

	function OnClickVersion()
	{
		if ($('#snmp_ver2c').is(':checked')) {
			$('#snmp_ver2c_read').removeAttr('disabled');
			$('#snmp_ver2c_write').removeAttr('disabled');
			$('#snmp_ver3_pw').attr('disabled', 'disabled');
		}
		else {
			$('#snmp_ver2c_read').attr('disabled', 'disabled');
			$('#snmp_ver2c_write').attr('disabled', 'disabled');
		}
		if ($('#snmp_ver3').is(':checked')) 	$('#snmp_ver3_pw').removeAttr('disabled');
		else											$('#snmp_ver3_pw').attr('disabled', 'disabled');

		if ($('#snmptrap_enable').is(':checked')) {
			$('#snmptrap_community').removeAttr('disabled');
			$('#snmptrap_address').removeAttr('disabled');
			$('#snmptrap_authfail').removeAttr('disabled');
			<?php if ($GLOBALS['M_SUPPORT_EVENT_ND']) { ?>
			$('#snmptrap_linkup').removeAttr('disabled');
			<?php } ?>
			<?php for($i=1;$i<=$GLOBALS['M_ALARMIN_COUNT'];$i++) { ?>
			$('#snmptrap_alarmin<?php echo $i;?>').removeAttr('disabled');
			<?php } ?>
			<?php for($i=1;$i<=$GLOBALS['M_ALARMOUT_COUNT'];$i++) { ?>
			$('#snmptrap_alarmout<?php echo $i;?>').removeAttr('disabled');
			<?php } ?>
			$('#snmptrap_tampering').removeAttr('disabled');
		}
		else {
			$('#snmptrap_community').attr('disabled', 'disabled');
			$('#snmptrap_address').attr('disabled', 'disabled');
			$('#snmptrap_authfail').attr('disabled', 'disabled');
			<?php if ($GLOBALS['M_SUPPORT_EVENT_ND']) { ?>
			$('#snmptrap_linkup').attr('disabled', 'disabled');
			<?php } ?>
			<?php for($i=1;$i<=$GLOBALS['M_ALARMIN_COUNT'];$i++) { ?>
			$('#snmptrap_alarmin<?php echo $i;?>').attr('disabled', 'disabled');
			<?php } ?>
			<?php for($i=1;$i<=$GLOBALS['M_ALARMOUT_COUNT'];$i++) { ?>
			$('#snmptrap_alarmout<?php echo $i;?>').attr('disabled', 'disabled');
			<?php } ?>
			$('#snmptrap_tampering').attr('disabled', 'disabled');
		}
	}

	function OnLoad()
	{
		//$('#snmp_ver3_pw').val(RequestGetConfig("ttttttttttttttttt3"));
		if (httpsType == 1){
			$('#snmp_ver1').removeAttr('disabled');
			$('#snmp_ver2c').removeAttr('disabled');
			$('#snmp_ver3').removeAttr('disabled');
		}
		else {
			$('#snmp_ver3').attr('disabled', 'disabled');
			$('#snmp_ver3_pw').attr('disabled', 'disabled');
		}
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
			<div id="container">
			<?php
				PrintLeftMenu($_SERVER['SCRIPT_NAME']);
			?>
			<div id="contents" >
				<div class="h3_tit mgt0" >
					<h3>SNMP v1, v2c</h3>
				</div>
				<table class="data_write">
					<colgroup>
						<col style="width:27px;" />
						<col style="width:200px;" />
						<col />
					</colgroup>
					<tbody>
						<tr>
							<td colspan=3><label class="labelBold"><input type="checkbox" id="snmp_ver1" <?php if ($snmp->dataInfo['EnabledVersion1']['value'] == 1) echo "checked=\"checked\""; ?>/><?php echo $t_enableV1[$GLOBALS['LANGINDEX']]; ?></label></td>
						</tr>
						<tr>
							<td colspan=3><label class="labelBold"><input type="checkbox" id="snmp_ver2c" <?php if ($snmp->dataInfo['EnabledVersion2']['value'] == 1) echo "checked=\"checked\""; ?> onClick="OnClickVersion()"/><?php echo $t_enableV2[$GLOBALS['LANGINDEX']]; ?></label></td>
						</tr>
						<tr>
							<td></td>
							<td scope="row"><?php echo $t_readCommunity[$GLOBALS['LANGINDEX']]; ?></td>
							<td><input type="text" id="snmp_ver2c_read" class="text" style="width:191px;"  onkeypress="IsNumChar(event);" onkeydown="CheckKorean(event);"  value= "<?php echo $snmp->dataInfo['ReadCommunity']['value']; ?>" maxlength="16" <?php if ($snmp->dataInfo['EnabledVersion2']['value'] != 1) echo "disabled=\"disabled\""; ?>/></td>
						</tr>
						<tr>
							<td></td>
							<td scope="row"><?php echo $t_writeCommunity[$GLOBALS['LANGINDEX']]; ?></td>
							<td><input type="text" id="snmp_ver2c_write" class="text" style="width:191px;"  onkeypress="IsNumChar(event);" onkeydown="CheckKorean(event);" value= "<?php echo $snmp->dataInfo['WriteCommunity']['value']; ?>" maxlength="16" <?php if ($snmp->dataInfo['EnabledVersion2']['value'] != 1) echo "disabled=\"disabled\""; ?>/></td>
						</tr>
						<tr>
							<td colspan=3><label class="labelBold"><input type="checkbox" id="snmptrap_enable" <?php if ($snmpTrap->enabled == 1) echo "checked=\"checked\""; ?> onClick="OnClickVersion()"/><?php echo $t_enableTrap[$GLOBALS["LANGINDEX"]]; ?></label></td>
						</tr>
						<tr>
							<td></td>
							<td scope="row"><?php echo $t_community[$GLOBALS["LANGINDEX"]]; ?></td>
							<td><input type="text" id="snmptrap_community" class="text" style="width:191px;" onkeypress="IsNumChar(event);" onkeydown="CheckKorean(event);"  value= "<?php echo $snmpTrap->trapInfo[0]->dataInfo['Community']['value']; ?>" maxlength="16" <?php if ($snmp->dataInfo['EnabledVersion2']['value'] != 1) echo "disabled=\"disabled\""; ?>  <?php if ($snmpTrap->enabled != 1) echo "disabled=\"disabled\""; ?>/></td>
						</tr>
						<tr>
							<td></td>
							<td scope="row"><?php echo $t_IPAddress[$GLOBALS["LANGINDEX"]]; ?></td>
							<td><input type="text" id="snmptrap_address" class="text" style="width:191px;" maxlength="15" onkeypress='CheckIPv4(event)' onkeydown='CheckIPv4(event)' value= "<?php echo $snmpTrap->trapInfo[0]->dataInfo['Address']['value']; ?>" maxlength="16" <?php if ($snmp->dataInfo['EnabledVersion2']['value'] != 1) echo "disabled=\"disabled\""; ?>  <?php if ($snmpTrap->enabled != 1) echo "disabled=\"disabled\""; ?>/></td>
						</tr>
						<tr>
							<td colspan="2"></td>
							<td><label><input type="checkbox" id="snmptrap_authfail" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" <?php if ($snmpTrap->trapInfo[0]->dataInfo['AuthenticationFailure']['value'] == 1) echo "checked=\"checked\""; ?>  <?php if ($snmpTrap->enabled != 1) echo "disabled=\"disabled\""; ?>/><?php echo $t_authfail[$GLOBALS['LANGINDEX']];?></label></td>
						</tr>
						<?php if ($GLOBALS['M_SUPPORT_EVENT_ND']) { ?>
						<tr>
							<td colspan="2"></td>
							<td><label><input type="checkbox" id="snmptrap_linkup" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" <?php if ($snmpTrap->trapInfo[0]->dataInfo['LinkUp']['value'] == 1) echo "checked=\"checked\""; ?>  <?php if ($snmpTrap->enabled != 1) echo "disabled=\"disabled\""; ?>/><?php echo $t_linkup[$GLOBALS['LANGINDEX']];?></label></td>
						</tr>
						<?php } ?>
						<?php for($i=1;$i<=$GLOBALS['M_ALARMIN_COUNT'];$i++) { ?>
						<tr> 
   							<td colspan="2"></td> 
   							<td><label><input type="checkbox" id="snmptrap_alarmin<?php echo $i; ?>" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" <?php if ($snmpTrap->trapInfo[0]->dataInfo['AlarmIn'.$i]['value'] == 1) echo "checked=\"checked\""; ?>  <?php if ($snmpTrap->enabled != 1) echo "disabled=\"disabled\""; ?>/><?php echo $t_alarmInput[$GLOBALS['LANGINDEX']];?> <?php echo $i; ?></label></td> 
   						</tr>
						<?php } ?>
						<?php for($i=1;$i<=$GLOBALS['M_ALARMOUT_COUNT'];$i++) { ?>
						<tr> 
   							<td colspan="2"></td> 
   							<td><label><input type="checkbox" id="snmptrap_alarmout<?php echo $i; ?>" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" <?php if ($snmpTrap->trapInfo[0]->dataInfo['AlarmOut'.$i]['value'] == 1) echo "checked=\"checked\""; ?>  <?php if ($snmpTrap->enabled != 1) echo "disabled=\"disabled\""; ?>/><?php echo $t_alarmOutput[$GLOBALS['LANGINDEX']];?> <?php echo $i; ?></label></td> 
   						</tr>
						<?php } ?>
						<tr> 
   							<td colspan="2"></td> 
   							<td><label><input type="checkbox" id="snmptrap_tampering" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" <?php if ($snmpTrap->trapInfo[0]->dataInfo['Tampering']['value'] == 1) echo "checked=\"checked\""; ?>  <?php if ($snmpTrap->enabled != 1) echo "disabled=\"disabled\""; ?>/><?php echo $t_tampering[$GLOBALS['LANGINDEX']];?></label></td> 
   						</tr> 
					</tbody>
				</table>
				<div class="h3_tit">
					<h3>SNMP v3</h3>
				</div>
				<table class="data_write">
					<colgroup>
						<col style="width:27px;" />
						<col style="width:200px;" />
						<col />
					</colgroup>
					<tbody>
						<tr>
							<td colspan=3><label class="labelBold"><input type="checkbox" id="snmp_ver3" <?php if ($snmp->dataInfo['EnabledVersion3']['value'] == 1) echo "checked=\"checked\""; ?> onClick="OnClickVersion()"/><?php echo $t_enableV3[$GLOBALS['LANGINDEX']]; ?></label></td>
						</tr>
						<tr>
							<td></td>
							<td scope="row"><?php echo $t_v3Pass[$GLOBALS['LANGINDEX']]; ?></td>
							<td><input type="password" id="snmp_ver3_pw" class="text" style="width:191px;"  onkeypress="IsNumChar(event);" onkeydown="CheckKorean(event);" maxlength="16" <?php if ($snmp->dataInfo['EnabledVersion3']['value'] != 1) echo "disabled=\"disabled\""; ?>/></td>
						</tr>
					</tbody>
				</table>
				<div class="btn_right">
					<a id="mid_ok_btn" class="btn_apply" href="javascript:OnClickApply()"><?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?></a>
				</div>
				</div>
			</div>
		</div>
	</div>
</body>
</html>
