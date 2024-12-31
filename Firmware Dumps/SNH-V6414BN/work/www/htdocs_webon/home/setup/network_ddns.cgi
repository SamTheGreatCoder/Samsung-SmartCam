<?php
require_once ('../../cgi-bin/adv/_define.inc');
if (isset($_REQUEST['menu']) && $_REQUEST['menu'] == 'DDNS_Result')
{
	class NetworkTest
	{
		public	$result;
		public 	$payload;
		public	$headerInfo;

		function __construct($_action=ACTION_START)
		{
			$this->headerInfo	= array('Command'=>CMD_NETWORK_TEST, 'Action'=>$_action);
		}

		function SetOperation($_operation)
		{
			$operArr = array('SMTP'=>0, 'FTP'=>1, 'DDNS'=>2, 'SMTP_Test'=>10, 'FTP_Test'=>11);
			$this->payload = pack('c1', $operArr[$_operation]);
		}

		function PayloadToArray($_payload)
		{
			$dataArray = unpack('c1result', $_payload);
			$this->result = $dataArray['result'];
		}
	}

	$networkTestConf = new NetworkTest();
	$socketManager = new SocketManager();
	$networkTestConf->SetOperation($_REQUEST['operation']);
	$socketManager->Connection($networkTestConf);
	echo $networkTestConf->result;
	exit;
}
require_once ('../language/language_network_ddns.cgi');
require_once ('../language/language_menu.cgi');

$classInstances 	= GetClassInstance('ddns');
$ddnsConf 			= $classInstances['DDNSConfiguration'];
$samsungDDNSConf 	= $ddnsConf->ddns[0];
$publicDDNSConf 	= $ddnsConf->ddns[1];
$quickConnectConf	= $classInstances['QuickConnectConfiguration'];
if ($GLOBALS['M_SPECIAL_TYPE'] == 1)
{
	$s1DDNSConf 		= $ddnsConf->ddns[3];
}

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
	var s1ddns				= <?php echo $GLOBALS['M_SPECIAL_TYPE']; ?>;
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

	var gTimerDDNS = "";
	var currentDDNSType = parseInt(<?php echo $ddnsConf->dataInfo['Type']['value']; ?>);

	if (s1ddns == 1)
	{
		if (currentDDNSType != 4) currentDDNSType = 0;
	}
<?php
	if (trim($publicDDNSConf->dataInfo['Password']['value'])=='') {
?>
	var publicDDNSPWset = false;
<?php
	}
	else 
	{
?>
	var publicDDNSPWset = true;
<?php
	}
?>

	function OnClickApply()
	{
		if (s1ddns == 1)
		{
			var ddnsType = ($('#ddns_type_disable').is(':checked') ? 0 : 4);
		}
		else
		{
			var ddnsType = ($('#ddns_type_disable').is(':checked') ? 0 : ($('#ddns_type_samsung').is(':checked') ? 1 : 2));
			if (ddnsType == 1) {
				if ($('#ddns_samsung_server').val().length == 0) {
					alert("<?php echo $msg_SamsungDDNSserver[$GLOBALS['LANGINDEX']]; ?>");
					return;
				}
				if ($('#ddns_samsung_hostname').val().length == 0) {
					alert("<?php echo $msg_SamsungDDNSuser[$GLOBALS['LANGINDEX']]; ?>");
					return;
				}
			}
			else if (ddnsType == 2) {
				if ($('#ddns_public_hostname').val().length == 0) {
					alert("<?php echo $msg_publicDDNShost[$GLOBALS['LANGINDEX']]; ?>");
					return;
				}
				if ($('#ddns_public_name').val().length == 0) {
					alert("<?php echo $msg_publicDDNSuser[$GLOBALS['LANGINDEX']]; ?>");
					return;
				}
				if ($('#ddns_public_pw').val().length == 0 && publicDDNSPWset ==false) {
					alert("<?php echo $msg_publicDDNSpass[$GLOBALS['LANGINDEX']]; ?>");
					return;
				}
			}
		}
			var msg = "";
			msg += "<SetQuickConnect>";
			msg += "<UseQuickConnect>"+($('#ddns_samsung_quick_connect').is(':checked')?1:0)+"</UseQuickConnect>"
			msg += "</SetQuickConnect>";
			RequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, "");
			localSeq++;
		
			var msg = "";
			msg += "<SetDDNS>";
			msg += "<Type>"+ddnsType+"</Type>"
			msg += "<SamsungDDNS>";
		if (s1ddns == 1)
		{
			msg += "<Name><?php echo $samsungDDNSConf->dataInfo['Name']['value']; ?></Name>";
		}
		else
		{
			msg += "<Name>"+$('#ddns_samsung_server').val()+"</Name>";
		}
			msg += "<UserName>"+$('#ddns_samsung_hostname').val()+"</UserName>";
			msg += "</SamsungDDNS>";
			msg += "<PublicDDNS>";
			msg += "<Name>"+$('#ddns_public_hostname').val()+"</Name>";
		if (s1ddns == 1)
		{
			msg += "<Service><?php echo $publicDDNSConf->dataInfo['Service']['value']; ?></Service>";
		}
		else
		{
			msg += "<Service>"+$('#ddns_public_service').val()+"</Service>";
		}
			msg += "<UserName>"+$('#ddns_public_name').val()+"</UserName>";
			msg += "<Password>"+$('#ddns_public_pw').val()+"</Password>";
			msg += "</PublicDDNS>";
			
			msg += "<S1DDNS>";
			msg += "<Name>"+$('#ddns_s1_hostname').val()+"</Name>";
			msg += "<Service>"+$('#ddns_s1_service').val()+"</Service>";
			msg += "<UserName>"+$('#ddns_s1_username').val()+"</UserName>";
			msg += "<Password>"+$('#ddns_s1_password').val()+"</Password>";
			msg += "<SystemCode>"+$('#ddns_s1_systemcode').val()+"</SystemCode>";
			msg += "<UseEncrypt>"+$('#ddns_s1_useencrypt').val()+"</UseEncrypt>";
			msg += "<Port>"+$('#ddns_s1_port').val()+"</Port>";
			msg += "</S1DDNS>";
			msg += "</SetDDNS>";
			
			RequestAjaxMsg(msg, "<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, "DDNS");		
	}

	function RequestDDNSResult()
	{
		var reqUrl = "<?php echo GetMyRequestURI($_SERVER['SCRIPT_NAME']); ?>";
		if (BrowserDetect.browser == "Explorer" || (BrowserDetect.browser == 'Safari' && reqUrl.search('.local') != -1)) {
			reqUrl = ".."+reqUrl.substr(reqUrl.indexOf("/setup/"));
		}
		$.ajax({
			type: "GET",
			async: false,
			cache: false,
			dataType: "text",
			url: reqUrl,
			data: "menu=DDNS_Result&operation=DDNS",
			success: OnSuccessDDNSResult,
			error: OnFailDDNSResult
		});
	}

	function OnSuccessDDNSResult(req)
	{
		switch(req) {
			case '0':
				if 		(currentDDNSType == 1)	$('#ddns_samsung_status').text("<?php echo $msg_test_fail[$GLOBALS['LANGINDEX']]; ?>");
				else if	(currentDDNSType == 2)	$('#ddns_public_status').text("<?php echo $msg_test_fail[$GLOBALS['LANGINDEX']]; ?>");
				else if 	(currentDDNSType == 4)	$('#ddns_s1_status').text("<?php echo $msg_test_fail[$GLOBALS['LANGINDEX']]; ?>");
				break;
			case '1':
				if 		(currentDDNSType == 1)	$('#ddns_samsung_status').text("<?php echo $msg_test_success[$GLOBALS['LANGINDEX']]; ?>");
				else if	(currentDDNSType == 2)	$('#ddns_public_status').text("<?php echo $msg_test_success[$GLOBALS['LANGINDEX']]; ?>");
				else if	(currentDDNSType == 4)	$('#ddns_s1_status').text("<?php echo $msg_test_success[$GLOBALS['LANGINDEX']]; ?>");
				break;
			case '2':
				if 		(currentDDNSType == 1)	$('#ddns_samsung_status').text("<?php echo $msg_test_connecting[$GLOBALS['LANGINDEX']]; ?>");
				else if	(currentDDNSType == 2)	$('#ddns_public_status').text("<?php echo $msg_test_connecting[$GLOBALS['LANGINDEX']]; ?>");
				else if	(currentDDNSType == 4)	$('#ddns_s1_status').text("<?php echo $msg_test_connecting[$GLOBALS['LANGINDEX']]; ?>");
				break;
			}
		gTimerDDNS = setTimeout('RequestDDNSResult()', 3000);
		if (req != '2') clearTimeout(gTimerDDNS);
	}

	function OnFailDDNSResult(req)
	{
		gTimerDDNS = setTimeout('RequestDDNSResult()', 5000);
	}

	function OnClickDdnsType()
	{
	
			if ($('#ddns_type_disable').is(':checked')) 
			{
				$('#ddns_samsung_server').attr('disabled', 'disabled');
				$('#ddns_samsung_hostname').attr('disabled', 'disabled');
				$('#ddns_samsung_quick_connect').attr('disabled', 'disabled');
				$('#ddns_public_service').attr('disabled', 'disabled');
				$('#ddns_public_hostname').attr('disabled', 'disabled');
				$('#ddns_public_name').attr('disabled', 'disabled');
				$('#ddns_public_pw').attr('disabled', 'disabled');
				$('#ddns_s1_service').attr('disabled', 'disabled');
				$('#ddns_s1_hostname').attr('disabled', 'disabled');
				$('#ddns_s1_username').attr('disabled', 'disabled');
				$('#ddns_s1_password').attr('disabled', 'disabled');
				$('#ddns_s1_port').attr('disabled', 'disabled');
				$('#ddns_s1_systemcode').attr('disabled', 'disabled');
				$('#ddns_s1_useencrypt').attr('disabled', 'disabled');
			} 
			else if ($('#ddns_type_samsung').is(':checked')) 
			{
				$('#ddns_samsung_server').removeAttr('disabled');
				$('#ddns_samsung_hostname').removeAttr('disabled');
				$('#ddns_samsung_quick_connect').removeAttr('disabled');
				$('#ddns_public_service').attr('disabled', 'disabled');
				$('#ddns_public_hostname').attr('disabled', 'disabled');
				$('#ddns_public_name').attr('disabled', 'disabled');
				$('#ddns_public_pw').attr('disabled', 'disabled');
			}
			else if ($('#ddns_type_public').is(':checked')) 
			{
				$('#ddns_samsung_server').attr('disabled', 'disabled');
				$('#ddns_samsung_hostname').attr('disabled', 'disabled');
				$('#ddns_samsung_quick_connect').attr('disabled', 'disabled');
				$('#ddns_public_service').removeAttr('disabled');
				$('#ddns_public_hostname').removeAttr('disabled');
				$('#ddns_public_name').removeAttr('disabled');
				$('#ddns_public_pw').removeAttr('disabled');
			}
			else if ($('#ddns_type_s1').is(':checked')) 
			{				
				$('#ddns_s1_service').removeAttr('disabled');			
				$('#ddns_s1_username').removeAttr('disabled');
				$('#ddns_s1_password').removeAttr('disabled');
				$('#ddns_s1_port').removeAttr('disabled');			
				$('#ddns_samsung_quick_connect').removeAttr('disabled');	
			}
	}

	function OnLoad()
	{
		//$('#ddns_public_pw').val(RequestGetConfig("ttttttttttttttttt2"));
		OnClickDdnsType();		
		if ($('#ddns_type_disable').is(':checked') != 1)	RequestDDNSResult();		
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
					<h3 class="wid220"><?php echo $menu_ddns[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>
				<table class="data_write">
					<colgroup>
						<col style="width:27px;" />
						<col style="width:200px;" />
						<col />
					</colgroup>
					<tbody>
						<tr>
							<td colspan=3>
								<label class="labelBold"><input type="radio" name="ddns_type" id="ddns_type_disable" <?php if ($ddnsConf->dataInfo['Type']['value'] == 0) echo "checked=\"checked\""; ?> onClick="OnClickDdnsType()"/><?php echo $t_off[$GLOBALS['LANGINDEX']]; ?></label>
							</td>
						</tr>
<?php
if ($GLOBALS['M_SPECIAL_TYPE'] == 1)
{		
?>
						<tr>
							<td><input type="radio" name="ddns_type" id="ddns_type_s1" <?php if ($ddnsConf->dataInfo['Type']['value'] == 4) echo "checked=\"checked\""; ?> onClick="OnClickDdnsType()"/></td>
							<th scope="row" colspan="2"><?php echo $t_S1DDNS[$GLOBALS['LANGINDEX']]; ?>&nbsp;&nbsp;<span id="ddns_s1_status" style="color:red;"></span></th>
						</tr>
						<tr style="display: none;">
							<td></td>
							<td scope="row"><?php echo $t_serverName[$GLOBALS['LANGINDEX']]; ?></td>
							<td><input type="text" id="ddns_s1_service" class="text" style="width:191px;ime-mode:disabled;" onkeypress='NoKorean(event); IsUrlChar(event)' onkeydown='NoKorean(event)' value="<?php echo '3'; ?>" maxlength="31"/></td>
						</tr>
						<tr style="display: none;">
							<td></td>
							<td scope="row"><?php echo "s1_systemcode"; ?></td>
							<td><input type="text" id="ddns_s1_systemcode" class="text" style="width:191px;" onkeypress='NoKorean(event); IsUrlChar(event)' onkeydown='NoKorean(event)' value="<?php echo 'nh'; ?>" maxlength="31"/></td>
						</tr>
						<tr>
							<td scope="row"></td>
							<td scope="row"><?php echo $t_hostName[$GLOBALS['LANGINDEX']]; ?></td>
							<td><input type="text" id="ddns_s1_hostname" class="text" style="width:191px;" onkeypress='NoKorean(event); IsSIM(event)' onkeydown='NoKorean(event)' value="<?php echo 'ddns.s1.co.kr'; // $s1DDNSConf->dataInfo['Name']['value']; ?>" maxlength="31"/></td>
						</tr>
					

						<tr>
							<td scope="row"></td>
							<td scope="row"><?php echo $t_port[$GLOBALS['LANGINDEX']]; ?></td>
							<td><input type="text" id="ddns_s1_port" class="text" style="width:191px;" onkeypress="IsNum(event)" onkeydown="OnlyNUm(event);" value="<?php echo $s1DDNSConf->dataInfo['Port']['value']; ?>" maxlength="31"/></td>
						</tr>		
						
						<tr>
							<td scope="row"></td>
							<td scope="row"><?php echo $t_userName[$GLOBALS['LANGINDEX']]; ?></td>
							<td><input type="text" id="ddns_s1_username" class="text" style="width:191px;" onkeypress='NoKorean(event); IsSIM(event)' onkeydown='NoKorean(event)' value="<?php echo $s1DDNSConf->dataInfo['UserName']['value']; ?>" maxlength="31"/></td>
						</tr>
						<tr>
							<td scope="row"></td>
							<td scope="row"><?php echo $t_password[$GLOBALS['LANGINDEX']]; ?></td>
							<td><input type="password" id="ddns_s1_password" class="text" style="width:191px;" onkeypress='NoKorean(event); IsSIM(event)' onkeydown='NoKorean(event)' value="<?php echo $s1DDNSConf->dataInfo['Password']['value']; ?>" maxlength="31"/></td>
						</tr>
						<tr style="display: none;">
							<td align="right"><?php echo $t_S1Encrypt[$GLOBALS['LANGINDEX']]; ?></td>
							<td>
								<select id="ddns_s1_useencrypt" class="selectbox_style">
									<option value="1" <?php echo 'selected'; ?> ><?php echo $t_on[$GLOBALS['LANGINDEX']];?></option>
									<!-- 
									<option value="1" <?php if ($s1DDNSConf->dataInfo['UseEncrypt']['value'] == 0) echo 'selected=\"selected\"'; ?> ><?php echo $t_off[$GLOBALS['LANGINDEX']];?></option>
									<option value="2" <?php if ($s1cDDNSConf->dataInfo['UseEncrypt']['value'] == 1) echo 'selected=\"selected\"'; ?> ><?php echo $t_on[$GLOBALS['LANGINDEX']];?></option>
									 -->
								</select>
							</td>
						</tr>
						<tr>
							<td scope="row" colspan="2"></td>
							<td>
								<label><input type="checkbox" id="ddns_samsung_quick_connect" style="margin-left:<?php if (GetBrowserName()=='IE') { if(ieversion() < 8) {echo '2';} else{echo '-3';} } else { echo '1'; } ?>px" <?php if ($quickConnectConf->dataInfo['UseQuickConnect']['value'] == 1) echo "checked=\"checked\""; ?> /><?php echo $t_quickConnect[$GLOBALS['LANGINDEX']]; ?></label>
							</td>
						</tr>
<?php
} else{

?>
						<tr>
							<td colspan=2>
								<label class="labelBold"><input type="radio" name="ddns_type" id="ddns_type_samsung" <?php if ($ddnsConf->dataInfo['Type']['value'] == 1) echo "checked=\"checked\""; ?> onClick="OnClickDdnsType()"/><?php echo $t_SamsungDDNS[$GLOBALS['LANGINDEX']]; ?></label>
							</td>
							<th scope="row"><span id="ddns_samsung_status" style="color:red;"></span></th>
						</tr>
						<tr>
							<td></td>
							<td scope="row"><?php echo $t_serverName[$GLOBALS['LANGINDEX']]; ?></td>
							<td><input type="text" id="ddns_samsung_server" class="text" style="width:191px;" onkeypress='NoKorean(event); IsUrlChar(event)' onkeydown='NoKorean(event)' value="<?php echo $samsungDDNSConf->dataInfo['Name']['value']; ?>" maxlength="31"/></td>
						</tr>
						<tr>
							<td scope="row"></td>
							<td scope="row"><?php echo $t_productID[$GLOBALS['LANGINDEX']]; ?></td>
							<td><input type="text" id="ddns_samsung_hostname" class="text" style="width:191px;" onkeypress='NoKorean(event); IsSIM(event)' onkeydown='NoKorean(event)' value="<?php echo $samsungDDNSConf->dataInfo['UserName']['value']; ?>" maxlength="31"/></td>
						</tr>
						<tr>
							<td scope="row" colspan="2"></td>
							<td>
								<label><input type="checkbox" id="ddns_samsung_quick_connect" style="margin-left:<?php if (GetBrowserName()=='IE') { if(ieversion() < 8) {echo '2';} else{echo '-3';} } else { echo '1'; } ?>px" <?php if ($quickConnectConf->dataInfo['UseQuickConnect']['value'] == 1) echo "checked=\"checked\""; ?> /><?php echo $t_quickConnect[$GLOBALS['LANGINDEX']]; ?></label>
							</td>
						</tr>
						<tr>
							<td colspan=2>
								<label class="labelBold"><input type="radio" name="ddns_type" id="ddns_type_public" <?php if ($ddnsConf->dataInfo['Type']['value'] == 2) echo "checked=\"checked\""; ?> onClick="OnClickDdnsType()"/><?php echo $t_publicDDNS[$GLOBALS['LANGINDEX']]; ?></label>
							</td>
							<th scope="row"><span id="ddns_public_status" style="color:red;"></span></th>
						</tr>
						<tr>
							<td></td>
							<td scope="row"><?php echo $t_service[$GLOBALS['LANGINDEX']]; ?></td>
							<td>
								<select id="ddns_public_service" class="selectbox_style">
									<option value="1" <?php if ($publicDDNSConf->dataInfo['Service']['value'] == 1) echo "selected=\"selected\""; ?> >www.dyndns.org</option>
									<option value="2" <?php if ($publicDDNSConf->dataInfo['Service']['value'] == 2) echo "selected=\"selected\""; ?> >www.no-ip.org</option>
								</select>
							</td>
						</tr>
						<tr>
							<td></td>
							<td scope="row"><?php echo $t_hostName[$GLOBALS['LANGINDEX']]; ?></td>
							<td><input type="text" id="ddns_public_hostname" class="text" style="width:191px;" onkeypress='NoKorean(event); IsSIM(event)' onkeydown='NoKorean(event)' value="<?php echo $publicDDNSConf->dataInfo['Name']['value']; ?>" maxlength="31"/></td>
						</tr>
						<tr>
							<td></td>
							<td scope="row"><?php echo $t_userName[$GLOBALS['LANGINDEX']]; ?></td>
							<td><input type="text" id="ddns_public_name" class="text" style="width:191px;" onkeypress='NoKorean(event); IsSIM(event)' onkeydown='NoKorean(event)' value="<?php echo $publicDDNSConf->dataInfo['UserName']['value']; ?>" maxlength="31"/></td>
						</tr>
						<tr>
							<td></td>
							<td scope="row"><?php echo $t_password[$GLOBALS['LANGINDEX']]; ?></td>
							<td><input type="password" id="ddns_public_pw" class="text" style="width:191px;" onkeypress='NoKorean(event); IsSIM(event)' onkeydown='NoKorean(event)' maxlength="31"/></td>
						</tr>
<?php 
}
?>
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
