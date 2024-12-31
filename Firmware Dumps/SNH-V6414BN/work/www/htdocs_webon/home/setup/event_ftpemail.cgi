<?php
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_menu.cgi');
if (isset($_REQUEST['operation']))
{
	//if ($_REQUEST['menu'] == 'FTP_Result' || $_REQUEST['menu'] == 'SMTP_Result')
	if ($_REQUEST['menu'] == 'FTP_Result' || $_REQUEST['menu'] == 'SMTP_Result' || $_REQUEST['menu'] == 'SMS_Result')
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
}

require_once ('../language/language_event_ftpemail.cgi');
$classInstances= GetClassInstance('ftpemail');
$ftpConf 		= $classInstances['FTPSetting'];
$smtpConf 		= $classInstances['SMTPSetting'];
// DEV_S1SMS
$smsConf		= $classInstances['SMSSetting'];
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
		height:950px;
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
	$(document).ready(function(){ lnbonoff("lnb_event"); });

<?php
	if (trim($ftpConf->dataInfo['Password']['value'])=='') {
?>
	var FTPPWset = false;
<?php
	}
	else 
	{
?>
	var FTPPWset = true;
<?php
	}
?>


<?php
	if (trim($smtpConf->dataInfo['Password']['value'])=='') {
?>
	var EMAILPWset = false;
<?php
	}
	else 
	{
?>
	var EMAILPWset = true;
<?php
	}
?>

	var gTimerFTP	= "";
	var gTimerSMTP = "";
	var gTimerSMS = ""; // DEV_S1SMS

	var localSeq				= <?php echo $_SESSION['count']; ?>;
	var ajaxReqUrl				= "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq;

	function TestFTP()
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
			data: "menu=FTP_Result&operation=FTP",
			success: OnSuccessFTPResult,
			error: OnFailFTPResult
		});
	}

	function OnSuccessFTPResult(req)
	{
		var ftpResult = req;
		switch (ftpResult) {
			case '0': $('#FTP_Status').text("<?php echo $msg_test_fail[$GLOBALS['LANGINDEX']]; ?>");			break;
			case '1': $('#FTP_Status').text("<?php echo $msg_test_success[$GLOBALS['LANGINDEX']]; ?>");		break;
			case '2': $('#FTP_Status').text("<?php echo $msg_test_connecting[$GLOBALS['LANGINDEX']]; ?>");	break;
		}
		gTimerFTP = setTimeout('TestFTP()', 1000);
		if (ftpResult != 2) clearTimeout(gTimerFTP);
	}


	function OnFailFTPResult(req)
	{
		gTimerFTP = setTimeout('TestFTP()', 1000);
	}

	function TestSMTP()
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
			data: "menu=SMTP_Result&operation=SMTP",
			success: OnSuccessSMTPResult,
			error: OnFailSMTPResult
		});
	}

	function OnSuccessSMTPResult(req)
	{
		var smtpResult = req;
		switch (smtpResult) {
			case '0': $('#SMTP_Status').text("<?php echo $msg_test_fail[$GLOBALS['LANGINDEX']]; ?>");			break;
			case '1': $('#SMTP_Status').text("<?php echo $msg_test_success[$GLOBALS['LANGINDEX']]; ?>");		break;
			case '2': $('#SMTP_Status').text("<?php echo $msg_test_connecting[$GLOBALS['LANGINDEX']]; ?>");	break;
		}
		gTimerSMTP = setTimeout('TestSMTP()', 1000);
		if (smtpResult != 2) 	clearTimeout(gTimerSMTP);
	}

	function OnFailSMTPResult(req)
	{
		gTimerSMTP = setTimeout('TestSMTP()', 1000);
	}

	function CheckFTP()
	{

		var ftp = $('#FtpDirectory').val().split("/");
		var ftp_len = $('#FtpDirectory').val().length-1;

		for(var i=1; i<ftp.length-1; i++)
		{
			if(ftp[i].length == 0)
			{
				alert("<?php echo $msg_invalid_path[$GLOBALS['LANGINDEX']]; ?>");
				return false;
			}

			if(ftp[i].length == 1 && ftp[i].charAt(ftp[i].length-1) == ' ')
			{
				alert("<?php echo $msg_invalid_path[$GLOBALS['LANGINDEX']]; ?>");
				return false;
			}	
		}

		for(var j=0; j<ftp.length; j++)
		{
			if (ftp[j].charAt(0) == '.')
			{
				alert("<?php echo $msg_invalid_path[$GLOBALS['LANGINDEX']]; ?>");
				return false;
			}			
		}
			
		
		if(!TypeCheck($('#FtpDirectory').val(), ALPHA+NUM+Directory+SPACE) )
		{
			alert("<?php echo $msg_invalid_path[$GLOBALS['LANGINDEX']]; ?>");
			$('FtpDirectory').focus();
			return  false;
		}

		if($('#FtpServerAddr').val() == '0.0.0.0' || $('#FtpServerAddr').val() == '255.255.255.255' || $('#FtpServerAddr').val() == '' || !TypeCheck($('#FtpServerAddr').val(), ALPHA+NUM+SIM))
		{
			alert("<?php echo $msg_invalid_server_addr[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		if($('#FtpUserId').val() == '' || !TypeCheck($('#FtpUserId').val(), ALPHA+NUM+SIM))
		{
			alert("<?php echo $msg_invalid_userID[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		if(!($('#FtpPw').val().length == 0 && FTPPWset))  
		{
			if($('#FtpPw').val() == '' || !TypeCheck($('#FtpPw').val(), ALPHA+NUM+SIM))
			{
				alert("<?php echo $msg_invalid_userPW[$GLOBALS['LANGINDEX']]; ?>");
				return false;
			}
		}
		if ($('#FtpDirectory').val() == "")
		{
			alert("<?php echo $msg_InputFTPUploadDirectory[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		if ($('#FtpPort').val() == "" || !TypeCheck($('#FtpPort').val(), NUM) || (parseInt($('#FtpPort').val()) < 1) || (parseInt($('#FtpPort').val()) > 65535))
		{
			alert("<?php echo $msg_Theportshouldbebetween1and65535[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}

		return true;
	}

	function FTP_OnclickApply()
	{

		if (!CheckFTP())	return;
		var direcmsg = $("#FtpDirectory").val();


		while(direcmsg.indexOf(' /') > 0)
		{
			direcmsg = direcmsg.replace(' /', '/');
		}


		while(direcmsg.charAt(direcmsg.length-1) == '.')
		{
			direcmsg = direcmsg.substring(0,direcmsg.length-1);
		}

		$("#FtpDirectory").val(direcmsg);

		direcmsg = $("#FtpDirectory").val().replace(/&/gm, '&amp;');
		while(direcmsg.indexOf('+') > 0)
		{
			direcmsg = direcmsg.replace('+', '&#43;');
		}

		var msg = "";
		msg += "<SetFTP>";
		msg += "<Server>"+$("#FtpServerAddr").val()+"</Server>";
		msg += "<Directory>"+direcmsg+"</Directory>";
		msg += "<Port>"+$("#FtpPort").val()+"</Port>";
		msg += "<UserName>"+$("#FtpUserId").val()+"</UserName>";
		msg += "<Password>"+$("#FtpPw").val()+"</Password>";
		if ($('#FtpPassiveOn').is(':checked'))			msg += "<PassiveMode>1</PassiveMode>";
		else if ($('#FtpPassiveOff').is(':checked'))	msg += "<PassiveMode>0</PassiveMode>";
		msg += "</SetFTP>";
		RequestAjaxMsg(msg, "<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, 'NO_REFRESH');
		localSeq++;
		TestFTP();
		if ($("#FtpPw").val().length > 0) {
			FTPPWset = true;
		}
		$("#FtpPw").val("");
	}

	function OnSuccessRequest(req)
	{
		alert("<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>");
		window.location.reload(true);
	}

	function CheckAddrKorean(str)
	{
		var korean = false;
		for(i=0; i<str.length; i++){
		 if (((str.charCodeAt(i) > 0x3130 && str.charCodeAt(i) < 0x318F) || (str.charCodeAt(i) >= 0xAC00 && str.charCodeAt(i) <= 0xD7A3)))
		 {
		 	korean = true;
			break;
		 }

		}

		return korean;
	}

	function CheckSMTP()
	{
		if($('#SmtpBody').val().length >256)
		{
			alert("<?php echo $msg_body_maxlength[$GLOBALS['LANGINDEX']]; ?>");
			$('#SmtpBody').focus();
			return false;
		}

		
		if ($('#SmtpServerAddr').val()=="")
		{
			alert("<?php echo $msg_InputSMTPServerAddress[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		if(CheckAddrKorean($('#SmtpServerAddr').val()))
		{
			alert("<?php echo $msg_invalid_server_addr[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		if($('#SmtpUserId').val() == '')
		{
			alert("<?php echo $msg_InputSMTPUserID[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		if (!TypeCheck($('#SmtpUserId').val(), ALPHA+NUM+SIM))
		{
			alert("<?php echo $msg_invalid_userID[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		if(!($('#SmtpPw').val().length == 0 && EMAILPWset)) 
		{
			if ($('#SmtpPw').val() == '' || !TypeCheck($('#SmtpPw').val(), ALPHA+NUM+SIM))
			{
				alert("<?php echo $msg_invalid_userPW[$GLOBALS['LANGINDEX']]; ?>");
				return false;
			}
		}
		if (!TypeCheck($('#SmtpPort').val(), NUM))
		{
			alert("<?php echo $msg_errPort[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		if($('#SmtpRecipient1').val() == '')
		{
			alert("<?php echo $msg_InputSMTPRecipient[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		if($('#SmtpSender').val() == '')
		{
			alert("<?php echo $msg_InputSMTPSender[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		if (CheckAddrKorean($('#SmtpSender').val()))
		{
			alert("<?php echo $msg_invalid_sender[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		if (CheckAddrKorean($('#SmtpRecipient1').val()))
		{
			alert("<?php echo $msg_invalid_recipient[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		if($('#SmtpSubject').val() == '')
		{
			alert("<?php echo $msg_InputSMTPSubject[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		if (!TypeCheck($('#SmtpSubject').val(), ALPHA+NUM+SIM+SPACE+CR+LF+SIM2+QUOTATION+'<>=+:'))
		{
			alert("<?php echo $msg_invalid_subject[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		if($('#SmtpBody').val() == '')
		{
			alert("<?php echo $msg_InputSMTPBody[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		if (!TypeCheck($('#SmtpBody').val(), ALPHA+NUM+SIM+SPACE+CR+LF+SIM2+QUOTATION+'<>=+:'))
		{
			alert("<?php echo $msg_invalid_body[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}

		if ( $('Smtp.Port').val=="" || (parseInt($('#SmtpPort').val()) < 1) || (parseInt($('#SmtpPort').val()) > 65535))
		{
			alert("<?php echo $msg_Theportshouldbebetween1and65535[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}

		return true;
	}

	function SMTP_OnclickApply()
	{
		if (!CheckSMTP()) return;

		var subjectmsg = $('#SmtpSubject').val();
		var bodymsg = $("#SmtpBody").val();
		
		//bodymsg = bodymsg.replace(/%/gm, '&amp;#37;'); delete 2012.10.07 sh
		subjectmsg = subjectmsg.replace(/&/gm, '&amp;');
		subjectmsg = subjectmsg.replace(/</gm, "&lt;");
		subjectmsg = subjectmsg.replace(/>/gm, "&gt;");
		subjectmsg = subjectmsg.replace(/\+/gm, '&#43;');

		bodymsg = bodymsg.replace(/&/gm, '&amp;');
		bodymsg = bodymsg.replace(/</gm, "&lt;");
		bodymsg = bodymsg.replace(/>/gm, "&gt;");
		bodymsg = bodymsg.replace(/\+/gm, '&#43;');

		var msg = "";
		msg += "<SetEmail>";
		msg += "<Sender>"+$("#SmtpSender").val()+"</Sender>";
		msg += "<Recipient>"+$("#SmtpRecipient1").val()+"</Recipient>";
		msg += "<Server>"+$("#SmtpServerAddr").val()+"</Server>";
		msg += "<Port>"+$("#SmtpPort").val()+"</Port>";
		if ($('#SmtpAuthOn').is(':checked'))			msg += "<AuthNeeded>1</AuthNeeded>";
		else if ($('#SmtpAuthOff').is(':checked'))	msg += "<AuthNeeded>0</AuthNeeded>";

		msg += "<UserName>"+$("#SmtpUserId").val()+"</UserName>";
		msg += "<Password>"+$("#SmtpPw").val()+"</Password>";
		msg += "<Subject>"+subjectmsg+"</Subject>";
		msg += "<Body>"+bodymsg+"</Body>";	// & ±?? XML¿¡¼­ N½ŀ≫ ¸?? ¾?º? ?μ? º??½????

		if ($('#SSLOn').is(':checked'))			msg += "<SSLEnabled>1</SSLEnabled>";
		else if ($('#SSLOff').is(':checked'))	msg += "<SSLEnabled>0</SSLEnabled>";

		if($('#SmtpSSL').is(':checked')){
			msg += "<SSLPort>"+$("#SmtpPort").val()+"</SSLPort>";
		}
		msg += "</SetEmail>";
		RequestAjaxMsg(msg, "<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, 'NO_REFRESH');
		localSeq++;
		TestSMTP();
		if ($("#SmtpPw").val().length > 0) {
			EMAILPWset = true;
		}
		$("#SmtpPw").val("");
	}

	function SSLPortChange()
	{
		if($('#SSLOn').is(':checked'))	$("#SmtpPort").val(465);
		else									$("#SmtpPort").val(25);
	}

	function OnLoad()
	{
		//$('#FtpPw').val(RequestGetConfig("ttttttttttttttttt5"));
		//$('#SmtpPw').val(RequestGetConfig("ttttttttttttttttt6"));


		var passive_mode = <?php echo $ftpConf->dataInfo['PassiveMode']['value']; ?>;
		if (passive_mode == 1) $('#FtpPassiveOn').prop('checked', true);
		else if (passive_mode == 0) $('#FtpPassiveOff').prop('checked', true);

		var auth_mode = <?php echo $smtpConf->dataInfo['AuthNeeded']['value']; ?>;
		if (auth_mode == 1) $('#SmtpAuthOn').prop('checked', true);
		else if (auth_mode == 0) $('#SmtpAuthOff').prop('checked', true);

		var ssl_use = <?php echo $smtpConf->dataInfo['SSLEnabled']['value']; ?>;
		if (ssl_use == 1) $('#SSLOn').prop('checked', true);
		else if (ssl_use == 0) $('#SSLOff').prop('checked', true);

		<?php $smtpSubject = str_replace('"', '&quot;', $smtpConf->dataInfo['Subject']['value']); ?>;
		var subject = "<?php echo $smtpSubject; ?>";
		subject = subject.replace(/&quot;/g, '"');
		$('#SmtpSubject').val(subject);
	}

	//================================================ DEV_S1SMS ===================================================

	function TestSMS()
	{
		var reqUrl = "<?php echo GetMyRequestURI($_SERVER['SCRIPT_NAME']); ?>";
		if (BrowserDetect.browser == 'Explorer' || BrowserDetect.browser == 'Firefox' || (BrowserDetect.browser == 'Safari' && reqUrl.search('.local') != -1)) {
			reqUrl = ".."+reqUrl.substr(reqUrl.indexOf("/setup/"));
		}
		$.ajax({
			type: "GET",
			async: false,
			cache: false,
			dataType: "text",
			url: reqUrl,
			data: "menu=SMS_Result&operation=SMS",
			success: OnSuccessSMSResult,
			error: OnFailSMSResult
		});
	}

	function OnSuccessSMSResult(req)
	{
		var smsResult = req;
		switch (smsResult) {
			case '0': $('#SMS_Status').text("<?php echo $msg_test_fail[$GLOBALS['LANGINDEX']]; ?>");			break;
			case '1': $('#SMS_Status').text("<?php echo $msg_test_success[$GLOBALS['LANGINDEX']]; ?>");		break;
			case '2': $('#SMS_Status').text("<?php echo $msg_test_connecting[$GLOBALS['LANGINDEX']]; ?>");	break;
		}
		gTimerSMS = setTimeout('TestSMS()', 1000);
		if (smsResult != 2) 	clearTimeout(gTimerSMS);
	}

	function OnFailSMSResult(req)
	{
		gTimerSMS = setTimeout('TestSMS()', 1000);
	}

	function CheckSMS(){

		if($('#SmsBody').val().length >30)
		{
			alert("<?php echo $msg_smsbody_maxlength[$GLOBALS['LANGINDEX']]; ?>");
			$('#SmsBody').focus();
			return false;
			
		}else if($('#SmsUserId').val() == ''){

			alert("<?php echo $t_InputSMSUserID[$GLOBALS['LANGINDEX']]; ?>");
			return false;

		}else if (!TypeCheck($('#SmsUserId').val(), ALPHA+NUM+SIM)){

			alert("<?php echo $msg_invalid_userID[$GLOBALS['LANGINDEX']]; ?>");
			return false;

		}else if($('#SmsPw').val() == ''){

			alert("<?php echo $t_InputSMSPassword[$GLOBALS['LANGINDEX']]; ?>");
			return false;

		}else if (!TypeCheck($('#SmsPw').val(), ALPHA+NUM+SIM)){

			alert("<?php echo $msg_invalid_userPW[$GLOBALS['LANGINDEX']]; ?>");
			return false;

		}else if($('#SmsSender').val() == ''){

			alert("<?php echo $t_InputSMSSender[$GLOBALS['LANGINDEX']]; ?>");
			return false;

		}else if (!TypeCheck($('#SmsSender').val(), NUM)){

			alert("<?php echo $msg_invalid_sender[$GLOBALS['LANGINDEX']]; ?>");
			return false;

		}else if($('#SmsBody').val() == ''){

			alert("<?php echo $t_InputSMSBody[$GLOBALS['LANGINDEX']]; ?>");
			return false;

		}else if (!TypeCheck($('#SmsBody').val(), ALPHA+NUM+SIM+SPACE+CR+LF+SIM2+QUOTATION+'<>=+:')){

			alert("<?php echo $msg_invalid_sms_body[$GLOBALS['LANGINDEX']]; ?>");
			return false;

		}
		return true;
	}
	
	
	function SMS_OnclickApply(){
		if (!CheckSMS()) return;

		var bodymsg = $("#SmsBody").val();
		
		bodymsg = bodymsg.replace(/&/gm, '&amp;');
		bodymsg = bodymsg.replace(/</gm, "&lt;");
		bodymsg = bodymsg.replace(/>/gm, "&gt;");
		bodymsg = bodymsg.replace(/\+/gm, '&#43;');

		var msg = "";
		msg += "<SetSms>";
		msg += "<UserName>"+$("#SmsUserId").val()+"</UserName>";
		msg += "<Password>"+$("#SmsPw").val()+"</Password>";
		msg += "<Sender>"+$("#SmsSender").val()+"</Sender>";
		msg += "<Body>"+bodymsg+"</Body>";
		msg += "</SetSms>";

		//RequestAjaxMsg(msg, "<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $GLOBALS['REQUEST_URI']; ?>", 'NO_REFRESH');
		RequestAjaxMsg(msg, "<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, 'NO_REFRESH');
		localSeq++;

		//TestSMS();
	}

	function TestSMS()
	{
		var reqUrl = "<?php echo GetMyRequestURI($_SERVER['SCRIPT_NAME']); ?>";
		if (BrowserDetect.browser == 'Explorer' || BrowserDetect.browser == 'Firefox' || (BrowserDetect.browser == 'Safari' && reqUrl.search('.local') != -1)) {
			reqUrl = ".."+reqUrl.substr(reqUrl.indexOf("/setup/"));
		}
		$.ajax({
			type: "GET",
			async: false,
			cache: false,
			dataType: "text",
			url: reqUrl,
			data: "menu=SMS_Result&operation=SMS",
			success: OnSuccessSMSResult,
			error: OnFailSMSResult
		});
	}

	function OnSuccessSMSResult(req)
	{
		console.log(req);
		var smsResult = req;
		switch (smsResult) {
			case '0': $('#SMS_Status').text("<?php echo $msg_test_fail[$GLOBALS['LANGINDEX']]; ?>");			break;
			case '1': $('#SMS_Status').text("<?php echo $msg_test_success[$GLOBALS['LANGINDEX']]; ?>");		break;
			case '2': $('#SMS_Status').text("<?php echo $msg_test_connecting[$GLOBALS['LANGINDEX']]; ?>");	break;
		}
		gTimerSMS = setTimeout('TestSMS()', 1000);
		if (smsResult != 2) 	clearTimeout(gTimerSMS);
	}

	function OnFailSMSResult(req)
	{
		gTimerSMS = setTimeout('TestSMS()', 1000);
	}
		//============================================= DEV_S1SMS // ===================================================
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
					<h3 class="wid400"><?php echo $t_FtpConfiguration[$GLOBALS['LANGINDEX']]; ?>&nbsp;<span class="style7" id="FTP_Status"  style="color:red;"></span></h3>
				</div>
				<table class="data_write" style="table-layout:fixed">
					<colgroup>
						<col style="width:275px;" />
						<col />
					</colgroup>
					<tbody>
						<tr>
							<th scope="row"><?php echo $t_serverAddress[$GLOBALS['LANGINDEX']]; ?></th>
							<td><input type="text" id="FtpServerAddr" class="text" style="width:191px;" value="<?php echo $ftpConf->dataInfo['Server']['value']; ?>" maxlength="32" onkeypress='NoKorean(event)' onkeydown='NoKorean(event)'/></td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_userID[$GLOBALS['LANGINDEX']]; ?></th>
							<td><input type="text" id="FtpUserId" class="text" style="width:191px;" value="<?php echo $ftpConf->dataInfo['UserName']['value']; ?>" maxlength="30" onkeypress='NoKorean(event)' onkeydown='NoKorean(event)'/></td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_password[$GLOBALS['LANGINDEX']]; ?></th>
							<td><input type="password" id="FtpPw" class="text" style="width:191px;" maxlength="30"  onkeypress='NoKorean(event)' onkeydown='NoKorean(event)' /></td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_uploadDirectory[$GLOBALS['LANGINDEX']]; ?></th>
							<td><input type="text" id="FtpDirectory" class="text" style="width:191px;" value="<?php echo $ftpConf->dataInfo['Directory']['value']; ?>" maxlength="60" onkeypress='NoKorean(event)' onkeydown='NoKorean(event)'/></td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_port[$GLOBALS['LANGINDEX']]; ?></th>
							<td><input type="text" id ="FtpPort" class="text" style="width:191px;" value="<?php echo $ftpConf->dataInfo['Port']['value']; ?>" maxlength="5" onkeypress="IsNum(event)" onkeydown="OnlyNUm(event);"/></td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_passiveMode[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<label><input type="radio" name="FtpPassiveMode" id="FtpPassiveOn" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_on[$GLOBALS['LANGINDEX']]; ?></label>
								<label><input type="radio" name="FtpPassiveMode" id="FtpPassiveOff" /><?php echo $t_off[$GLOBALS['LANGINDEX']]; ?></label>
							</td>
						</tr>
					</tbody>
				</table>
				<div class="btn_right">
					<a id="mid_ok_btn" class="btn_apply" href="javascript:FTP_OnclickApply()"><?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?></a>
				</div>
				<div class="h3_tit" >
					<h3 class="wid400"><?php echo $t_smtpConfiguration[$GLOBALS['LANGINDEX']]; ?>&nbsp;<span class="style7"  id="SMTP_Status"  style="color:red;"></span> &nbsp;</h3>
				</div>
				<table class="data_write" style="table-layout:fixed">
					<colgroup>
						<col style="width:275px;" />
						<col />
					</colgroup>
					<tbody>
						<tr>
							<th scope="row"><?php echo $t_serverAddress[$GLOBALS['LANGINDEX']]; ?></th>
							<td><input type="text" id="SmtpServerAddr" class="text" style="width:191px;" value="<?php echo $smtpConf->dataInfo['Server']['value']; ?>" maxlength="60" onkeypress='NoKorean(event)' onkeydown='NoKorean(event)' /></td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_useAuthentication[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<label><input type="radio" name="SmtpUseAuth" id="SmtpAuthOn" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_on[$GLOBALS['LANGINDEX']]; ?></label>
								<label><input type="radio" name="SmtpUseAuth" id="SmtpAuthOff" /><?php echo $t_off[$GLOBALS['LANGINDEX']]; ?></label>
							</td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_useSSL[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<label><input type="radio" name="SmtpSSL" id="SSLOn" onclick="SSLPortChange()" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_on[$GLOBALS['LANGINDEX']]; ?></label>
								<label><input type="radio" name="SmtpSSL" id="SSLOff" onclick="SSLPortChange()" /><?php echo $t_off[$GLOBALS['LANGINDEX']]; ?></label>
							</td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_userID[$GLOBALS['LANGINDEX']]; ?></th>
							<td><input type="text" id="SmtpUserId" class="text" style="width:191px;" value="<?php echo $smtpConf->dataInfo['UserName']['value']; ?>" maxlength="32" onkeypress='NoKorean(event)' onkeydown='NoKorean(event)' /></td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_password[$GLOBALS['LANGINDEX']]; ?></th>
							<td><input type="password" id ="SmtpPw" class="text" style="width:191px;" maxlength="32" onkeypress='NoKorean(event)' onkeydown='NoKorean(event)' /></td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_port[$GLOBALS['LANGINDEX']]; ?></th>
							<td><input type="text" id="SmtpPort" class="text" style="width:191px;" value= "<?php if($smtpConf->dataInfo['SSLEnabled']['value'] == 0) echo $smtpConf->dataInfo['Port']['value']; else echo $smtpConf->dataInfo['SSLPort']['value']; ?>" maxlength="5" onkeypress="IsNum(event)" onkeydown="OnlyNUm(event);" /></td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_recipient[$GLOBALS['LANGINDEX']]; ?></th>
							<td><input type="text" id="SmtpRecipient1" class="text" style="width:191px;" value="<?php echo $smtpConf->dataInfo['Recipient']['value']; ?>" maxlength="60" onkeypress='NoKorean(event)' onkeydown='NoKorean(event)'/></td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_sender[$GLOBALS['LANGINDEX']]; ?></th>
							<td><input type="text" id="SmtpSender" class="text" style="width:191px;" value="<?php echo $smtpConf->dataInfo['Sender']['value']; ?>" maxlength="60" onkeypress='NoKorean(event)' onkeydown='NoKorean(event)' /></td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_subject[$GLOBALS['LANGINDEX']]; ?></th>
							<td><input type="text" id="SmtpSubject" class="text" style="width:191px;" maxlength="60" onkeypress='NoKorean(event)' onkeydown='NoKorean(event)'/></td>
						</tr>
						<tr>
							<th scope="row" class="top_txt"><?php echo $t_body[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<textarea class="textarea" id="SmtpBody" cols="5" rows="5" style="width:385px; height:79px; resize:none;" onkeypress='NoKorean(event)' onkeydown='NoKorean(event)'><?php echo $smtpConf->dataInfo['Body']['value'];?></textarea>
							</td>
						</tr>
					</tbody>
				</table>
				<div class="btn_right">
					<a id="mid_ok_btn" class="btn_apply" href="javascript:SMTP_OnclickApply()"><?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?></a>
				</div>
<?php
if ($GLOBALS['M_SPECIAL_TYPE'] == 1)
{		
?>
				<!-- DEV_S1SMS -->
				<div class="h3_tit" >
					<h3 class="wid400"><?php echo $t_SmsConfiguration[$GLOBALS['LANGINDEX']]; ?>&nbsp;<span class="style7"  id="SMS_Status"  style="color:red;"></span> &nbsp;</h3>
				</div>
				<table class="data_write" style="table-layout:fixed">
					<colgroup>
						<col style="width:275px;" />
						<col />
					</colgroup>
					<tbody>
						<tr>
							<th scope="row"><?php echo $t_SmsUserID[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<input type="text" id="SmsUserId" class="text" style="width:191px;" value="<?php echo $smsConf->dataInfo['UserName']['value']; ?>" maxlength="32" onkeypress='NoKorean(event)' onkeydown='NoKorean(event)' />
							</td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_SmsPassword[$GLOBALS['LANGINDEX']]; ?></th>
							<td><input type="password" id="SmsPw" class="text" style="width:191px;" value="<?php echo $smsConf->dataInfo['Password']['value']; ?>" maxlength="32" onkeypress='NoKorean(event)' onkeydown='NoKorean(event)' /></td>
						</tr>

						<tr>
							<th scope="row"><?php echo $t_SmsNumber[$GLOBALS['LANGINDEX']]; ?></th>
							<td><input type="text" id="SmsSender" class="text" style="width:191px;" value="<?php echo $smsConf->dataInfo['Sender']['value']; ?>" maxlength="15"  onkeypress="IsNum(event)" onkeydown="OnlyNUm(event);" /></td>
						</tr>

						<tr>
							<th scope="row" class="top_txt"><?php echo $t_body[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<textarea class="textarea" id="SmsBody" maxlength="30" cols="5" rows="5" style="width:385px; height:79px; resize:none;" onkeypress='NoKorean(event)' onkeydown='NoKorean(event)'><?php echo $smsConf->dataInfo['Body']['value'];?></textarea>
							</td>
						</tr>
					</tbody>
				</table>
				<div class="btn_right">
					<a id="mid_ok_btn" class="btn_apply" href="javascript:SMS_OnclickApply()"><?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?></a>
				</div>
				<!-- DEV_S1SMS // -->
<?php 
}
?>
			</div>

		</div>
	</div>
</body>
</html>
