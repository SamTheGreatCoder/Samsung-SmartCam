<?php
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_menu.cgi');
require_once ('../language/language_network_autoipconfig.cgi');

if (isset($_REQUEST['menu']) && $_REQUEST['menu'] == 'GetZeroconfig') {
	require_once ('../../cgi-bin/adv/autodiscovery.class');
	$zeroConf = new ZeroConfiguration();
	$socketManager = new SocketManager();
	$socketManager->Connection($zeroConf);
	if (trim($zeroConf->dataInfo['PrefixLength']['value']) == 0) echo '0';
	else echo $zeroConf->dataInfo['Address']['value'];
	exit;
}

$classInstances= GetClassInstance('autoipconfig');
$bonjour	= $classInstances['BonjourConfiguration'];
$zeroconfig	= $classInstances['ZeroConfiguration'];
$upnp	= $classInstances['UPNPConfiguration'];
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="kr" xml:lang="kr">
<head>
	<title>iPOLiS NETWORK CAMERA WEBVIEWER</title>
	<meta http-equiv="X-UA-Compatible" content="IE=Edge; requiresActiveX=true">
	<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
	<link rel="stylesheet" type="text/css" href="../css/techwin.css" />
	<script type="text/javascript" src="../js/jquery-1.5.1.min.js"></script>
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
	$(document).ready(function(){ lnbonoff("lnb_network"); });
	var gTimerZeroconfig = "";
	var tryCnt = 0;
	
	function OnClickApply()
	{
		if(TypeCheck($('#bonjour_name').val(), ALPHA+NUM+FRIENDLY_NAME+SPACE) == false || TypeCheck($('#upnp_name').val(), ALPHA+NUM+FRIENDLY_NAME+SPACE) == false ||
			$('#bonjour_name').val().charAt(0) == SPACE || $('#upnp_name').val().charAt(0) == SPACE) {
			alert("<?php echo $msg_invalid_friendlyname[$GLOBALS['LANGINDEX']];?>");
			return;
		}
		var msg = "<SetUPNP>";
		msg += "<Enabled>"+($('#upnp_enable').is(':checked') ? 1 : 0)+"</Enabled>";
		msg += "<FriendlyName>"+$('#upnp_name').val()+"</FriendlyName>";
		msg += "</SetUPNP>";
		RequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, 'NO_REFRESH');
		localSeq++;
		
		var msg = "<SetBonjour>";
		msg += "<Enabled>"+($('#bonjour_enable').is(':checked') ? 1 : 0)+"</Enabled>";
		msg += "<FriendlyName>"+$('#bonjour_name').val()+"</FriendlyName>";
		msg += "</SetBonjour>";
		RequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, 'NO_REFRESH');
		localSeq++;

		var msg = "<SetZeroConfig>";
		msg += "<Enabled>"+($('#zeroconfig_enable').is(':checked') ? 1 : 0)+"</Enabled>";
		msg += "</SetZeroConfig>";
		RequestAjaxMsg(msg, "<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq);
	}

	function RequestZeroconfig()
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
			data: "menu=GetZeroconfig",
			success: OnSuccessZeroconfigResult,
			error: OnFailZeroconfigResult
		});
	}

	function OnSuccessZeroconfigResult(req)
	{
		if (tryCnt > 10) {
			$('#zeroconfig_status').text("<?php echo $msg_test_fail[$GLOBALS['LANGINDEX']]; ?>");
			clearTimeout(gTimerZeroconfig);
			$('#address').val("");
			$('#subnet').val("");
			return;
		}
		if (req == '0') {
			$('#zeroconfig_status').text("<?php echo $msg_test_connecting[$GLOBALS['LANGINDEX']]; ?>");
			gTimerZeroconfig = setTimeout('RequestZeroconfig()', 2000);
			tryCnt++;
		}
		else {
			$('#zeroconfig_status').text("");
			$('#address').val(req);
			$('#subnet').val("255.255.0.0");
			clearTimeout(gTimerZeroconfig);
		}
	}

	function OnFailZeroconfigResult(req)
	{
		gTimerZeroconfig = setTimeout('RequestZeroconfig()', 5000);
	}

	function OnChangeChkBox(id)
	{
		if($('#'+id+'_enable').is(':checked'))
		{
			$('#'+id+'_name').removeAttr("disabled");
		}
		else
		{
			$('#'+id+'_name').attr("disabled", "disabled");
		}
	}
	
	function OnLoad()
	{
		OnChangeChkBox('bonjour');
		OnChangeChkBox('upnp');
		if ($('#zeroconfig_enable').is(':checked') == 1 && $('#address').val().length == 0) {
			RequestZeroconfig();
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
					<h3 class="wid400"><?php echo $menu_zeroconfig[$GLOBALS['LANGINDEX']]; ?>&nbsp;&nbsp;<span id="zeroconfig_status" style="color:red;"></span></h3>
					
				</div>
				<table class="data_write">
					<colgroup>
						<col style="width:240px;" />
						<col />
					</colgroup>
					<tbody>
						<tr>
							<th scope="row"><?php echo $t_autoConfig[$GLOBALS['LANGINDEX']]; ?></th>
							<td><label><input type="checkbox" id="zeroconfig_enable" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" <?php if($zeroconfig->dataInfo['Enabled']['value'] == 1) echo "checked=\"checked\""; ?> onchange='OnChangeChkBox()'/><?php echo $t_use[$GLOBALS['LANGINDEX']]; ?></label></td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_IPAddress[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<input type="text" id="address" disabled="disabled" class="text" style="width:191px;" maxlength="15" onkeypress='CheckIPv4(event)' onkeydown='CheckIPv4(event)' value=""/>
							</td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_subnetMask[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<input type="text" id="subnet" disabled="disabled" class="text" style="width:191px;" maxlength="15" onkeypress='CheckIPv4(event)' onkeydown='CheckIPv4(event)' value=""/>
							</td>
						</tr>
					</tbody>
				</table>
				<div class="h3_tit" >
					<h3 class="wid400"><?php echo $menu_upnp[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>
				<table class="data_write">
					<colgroup>
						<col style="width:240px;" />
						<col />
					</colgroup>
					<tbody>
						<tr>
							<th scope="row"><?php echo $menu_upnp[$GLOBALS['LANGINDEX']]; ?></th>
							<td><label><input type="checkbox" id="upnp_enable" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" <?php if($upnp->dataInfo['Enabled']['value'] == 1) echo "checked=\"checked\""; ?> onchange='OnChangeChkBox()'/><?php echo $t_use[$GLOBALS['LANGINDEX']]; ?></label></td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_friendlyName[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<input type="text" id="upnp_name" class="text" maxlength="63" style="width:250px;" value="<?php echo $upnp->dataInfo['FriendlyName']['value']; ?>" onkeypress='NoKorean(event); IsFriendlyName(event);' onkeydown='NoKorean(event)' onpaste='return false'/>
							</td>
						</tr>
					</tbody>
				</table>
				<div class="h3_tit" >
					<h3><?php echo "Bonjour" ?></h3>
				</div>
				<table class="data_write">
					<colgroup>
						<col style="width:240px;" />
						<col />
					</colgroup>
					<tbody>
						<tr>
							<th scope="row">Bonjour</th>
							<td><label><input type="checkbox" id="bonjour_enable" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" <?php if($bonjour->dataInfo['Enabled']['value'] == 1) echo "checked=\"checked\""; ?> onchange="OnChangeChkBox()" /><?php echo $t_use[$GLOBALS['LANGINDEX']]; ?></label></td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_friendlyName[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<input type="text" id="bonjour_name" class="text" maxlength="63" style="width:250px;" value="<?php echo $bonjour->dataInfo['FriendlyName']['value']; ?>" onkeypress='NoKorean(event); IsFriendlyName(event);' onkeydown='NoKorean(event)' onpaste='return false'/>
							</td>
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




