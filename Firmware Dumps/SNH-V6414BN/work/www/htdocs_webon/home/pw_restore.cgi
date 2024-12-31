<?php
//DEV_S1PWRESTORE
require_once ('../cgi-bin/adv/_define.inc');
require_once ('./language/language_pw_restore.cgi');

$classInstances = array();
$GLOBALS['SOCKET_MANAGER'] = new SocketManager();

if (isset($_REQUEST['menu'])){

	if($_REQUEST['menu'] == 'SMTP_Send')
	{
		require_once ('../cgi-bin/adv/password_restore.class');
		$passWordRestoreConf = new PasswordRestoreConfiguration();
		$passWordRestoreConf->headerInfo['Action'] = ACTION_START;
		$passWordRestoreConf->dataInfo['sendtype']['value'] = 0;
		$passWordRestoreConf->dataInfo['Recipient']['value'] = $_REQUEST['address'];
		$passWordRestoreConf->SetPayload();
		$socketManager = new SocketManager();
		$socketManager->Connection($passWordRestoreConf);
		echo $passWordRestoreConf->result;
		exit;
	}
	else if($_REQUEST['menu'] == 'SMS_Send')
	{
		require_once ('../cgi-bin/adv/password_restore.class');
		$passWordRestoreConf = new PasswordRestoreConfiguration();
		$passWordRestoreConf->headerInfo['Action'] = ACTION_START;
		$passWordRestoreConf->dataInfo['sendtype']['value'] = 1;
		$passWordRestoreConf->dataInfo['Sender']['value'] = $_REQUEST['address'];
		$passWordRestoreConf->SetPayload();
		$socketManager = new SocketManager();
		$socketManager->Connection($passWordRestoreConf);
		echo $passWordRestoreConf->result;
		exit;
	}
}

require_once ('../cgi-bin/adv/info.class');
$classInstances['Information'] = $GLOBALS['SOCKET_MANAGER']->Connection(new Information());

?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="kr" xml:lang="kr">
<head>
	<meta http-equiv="X-UA-Compatible" content="IE=Edge; requiresActiveX=true">
	<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
	<title>iPOLiS NETWORK CAMERA WEBVIEWER</title>
	<link rel="stylesheet" type="text/css" href="./css/techwin.css" />
	<style>
		#container {
			overflow:hidden;
		}
		.window {
			position:absolute; 
			top:275px; 
			width:100%; 
			height:200px; 
			overflow:hidden; 
			}
		}
	</style>
	<script type="text/javascript" src="./js/jquery-1.9.1.js"></script>
	<script type="text/javascript" src="./js/common_function.js"></script>
	<script type="text/javascript">
	<!--
<?php
	if ($classInstances['Information']->dataInfo['PasswordCheck']['value'] == 1) {
?>
		window.location.href = './pw_change.cgi';
<?php
	}
	else if ($classInstances['Information']->dataInfo['PasswordCheck']['value'] == 2) {
?>
		alert("<?php echo $msg_change_weak_password[$GLOBALS['LANGINDEX']]; ?>");
<?php
	}	
?>	
		function OnLoad() {}

		function OnClickPasswordFind(){			
			var send_adress = "";
			if($('#email').is(':checked') == true)
			{
				send_adress = $('#email_address').val();
				
			}else if($('#sms').is(':checked') == true)
			{
				send_adress = $('#sms_address').val();
			}
			
			if($('#email').is(':checked') == false && $('#sms').is(':checked') == false && send_adress  == ""){
				alert("<?php echo $t_emailsmsinvalid[$GLOBALS['LANGINDEX']]; ?>");
				return;
			}

			var menu_val = "";
			var operation_val = "";

			if($('#email').is(':checked')){
				menu_val = "SMTP_Send";
				operation_val = "";
			}else if($('#sms').is(':checked')){
				menu_val = "SMS_Send";
				operation_val = "FTP";
			}else{
				alert("<?php echo $t_emailsmsinvalid[$GLOBALS['LANGINDEX']]; ?>");
				return;
			}

			var reqUrl = "<?php echo GetMyRequestURI($_SERVER['SCRIPT_NAME']); ?>";
			if (BrowserDetect.browser == 'Explorer' || (BrowserDetect.browser == 'Safari' && reqUrl.search('.local') != -1)) {
				reqUrl = ".."+reqUrl.substr(reqUrl.indexOf("/home/"));
			}

			//location.href = reqUrl+"?menu="+menu_val+"&operation="+operation_val+"&address="+$('#address').val()+"&trycount="+(new Date()).getTime();	
			//return;
			
			$.ajax({
				type: "POST",
				async: false,
				cache: false,
				url: reqUrl,
				dataType: "text",
				data: { menu: menu_val, operation: operation_val, address: send_adress, trycount: (new Date()).getTime()},
				success: PasswordFindSuccess
			});

		}

		function OnClickPWType()
		{	
	
			if ($('#email').is(':checked')) 
			{
				$('#email_display').attr('style','display:block');	
				$('#sms_display').attr('style','display:none');
			} 
			else if ($('#sms').is(':checked')) 
			{
				$('#sms_display').attr('style','display:block');	
				$('#email_display').attr('style','display:none');
			}
	
		}

		function PasswordFindSuccess(req){
			console.log("req : "+req);

			var result = parseInt(req);
	
			switch (result){
				case 0: 
					alert("<?php echo $t_emailSendFail[$GLOBALS['LANGINDEX']]; ?>");
					break;
				case 1: 
					alert("<?php echo $t_emailSendSuccess[$GLOBALS['LANGINDEX']]; ?>");
					break;
				case 2:
					//continue
					break;
				case 3:
					alert("<?php echo $t_smsSendFail[$GLOBALS['LANGINDEX']]; ?>");
					break;
				case 4:
					alert("<?php echo $t_smsSendSuccess[$GLOBALS['LANGINDEX']]; ?>");
					break;
				case 5:
					alert("<?php echo $t_emailCompareFail[$GLOBALS['LANGINDEX']]; ?>");
					break;
				case 6:
					alert("<?php echo $t_smsCompareFail[$GLOBALS['LANGINDEX']]; ?>");
					break;
			}

			gTimerSend = setTimeout('OnClickPasswordFind()', 1000);

			if (result != 2){
				clearTimeout(gTimerSend);
			}
		}

		function onKeyNumber()
		{
			if ( (event.keyCode < 48 ) || (event.keyCode > 57) )
			{
				event.returnValue = false;			
			}
		}
		
	//-->
	</script>
	</head>
	<body onload="OnLoad()" onContextmenu="return false" onselectstart="return false"  ondragstart="return false">
		
		<div id="wrap">
			<div id="head">
				<div class="head-top2">
					<h1><img src="./images/common/top_title_1.png" alt="S1" /></h1>
					<!--div class="logo"><img src="./images/common/top_logo.gif" alt="SAMSUNG TECHWIN" /></div-->
				</div>
			</div>
		</div>
		<div id="container">
			<div class="window" align="center">
				<div class="h3_tit mgt0" style="width:400px">
					<h3 class="wid320" align="left" style="width:400px"><?php echo $t_titlePWRestore[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>	

				<table class="data_write"  align="center" style="width:400px">
				
					<colgroup>
						<col />
					</colgroup>
					<tbody>
						<tr>
							<td>
								<label for="email"><input type="radio" name="sendRadioType" id="email" onClick="OnClickPWType()" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" checked/><?php echo $t_emailAddress[$GLOBALS["LANGINDEX"]]; ?></label>								
								<label for="sms"><input type="radio" name="sendRadioType" id="sms" onClick="OnClickPWType()" /><?php echo $t_smsAddress[$GLOBALS["LANGINDEX"]]; ?></label>
							</td>
						</tr>
						<tr id="email_display" >
							<td>
								<input type="text" id="email_address" class="text" style="width:300px;" onkeypress="NoKorean(event);" onpaste="javascript:return false;"  ondrop="javascript:return false;" style="ime-mode:disabled;" maxlength="60"/>
							</td>
						</tr>
						<tr id="sms_display" style="display:none">
							<td>
								<input type="text" id="sms_address" class="text" style="width:300px;" onkeypress="onKeyNumber();" onpaste="javascript:return false;"  ondrop="javascript:return false;" style="ime-mode:disabled;" maxlength="15"/>
							</td>
						</tr>
					</tbody>
				</table>				
				<div style="text-align:center; margin-top:40px;">
					<a id="window_crop_mid_ok_btn" class="btn_apply_login" href="javascript:OnClickPasswordFind();"><?php echo $t_passwordRestoreBtn[$GLOBALS['LANGINDEX']]; ?></a>
					<!-- DEV_S1PWRESTORE -->
					<a id="window_crop_mid_cancel_btn" class="btn_apply_login" href="./loginpage.cgi"><?php echo $t_backBtn[$GLOBALS['LANGINDEX']]; ?></a>
					<!-- DEV_S1PWRESTORE // -->
				</div>
			</div>
		</div>
	</body>
</html>

