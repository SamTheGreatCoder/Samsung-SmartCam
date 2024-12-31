<?php
// DEV_S1LOGIN
require_once ('../cgi-bin/adv/_define.inc');
require_once ('./language/language_menu.cgi');
require_once ('./language/language_system_user.cgi');

$classInstances = array();
$GLOBALS['SOCKET_MANAGER'] = new SocketManager();

if (isset($_REQUEST['user_id'])) {	

	$user_id = $_REQUEST['user_id'];	
	$user_pw = $_REQUEST['user_pw'];	
	$user_pw = str_replace('\\\\', '\\', $user_pw );
	$user_pw = str_replace('\\\'', '\'', $user_pw );
	$user_pw = str_replace("\\\"", "\"", $user_pw );
	$user_pw = urldecode($user_pw);
	$updateCount = 1;

	$lastAuthTime = $_REQUEST['lastAuthTime'];

	$UserLoginClassInstances = GetClassInstance('userlogin');
	$userlogin = $UserLoginClassInstances['UserLogin'];	
	
	$systemClockTime = $userlogin->dataInfo['SystemClockTime']['value']; // save current system clock time
	if ($lastAuthTime == 0) $lastAuthTime = $systemClockTime;	// for first login..

	$userlogin->dataInfo['ID']['value'] = $user_id;
	$userlogin->dataInfo['IP']['value'] = $_SESSION['sess_ip'];
	$userlogin->dataInfo['LastAuthTime']['value'] = $lastAuthTime;
	$userlogin->dataInfo['IsLoginCmd']['value'] = $updateCount;

	$ha1 = md5($user_id.':'.$user_pw);
	$ha2 = md5($_SESSION['sess_ip'].':'.$lastAuthTime);
	$userlogin->dataInfo['AuthKey']['value'] = md5($ha1.':'.$ha2);
	
	$_SESSION['sess_sub_key'] = $ha1;

	$userlogin->headerInfo['Action'] = ACTION_SET;
	$userlogin->SetPayload();
	
	$GLOBALS['SOCKET_MANAGER']->Connection($userlogin);	

	// success!!
	if ($GLOBALS['SOCKET_MANAGER']->dataInfo['ErrorCode']['value']== 1){

		$_SESSION['sess_user_id'] = $user_id;
		$_SESSION['sess_last_auth_time'] = $systemClockTime; // update current system clock time
		//$_SESSION['sess_last_auth_time'] = time(); // update current time
		
 		$ha2 = md5($_SESSION['sess_ip'].':'.$_SESSION['sess_last_auth_time']);
 		$_SESSION['sess_auth_key'] = md5($_SESSION['sess_sub_key'].':'.$ha2);	// save new auth key
		
		ResponseLoginResult(True);
	}
	
	// fail!!
	if ($GLOBALS['SOCKET_MANAGER']->dataInfo['ErrorCode']['value'] == 90) ResponseLoginResult(LOCKED);
	ResponseLoginResult(FALSE);

	/*
	if($user_id == $GLOBALS['USERINFO']['name'] && $user_pw == $GLOBALS['USERINFO']['pw']){

		$_SESSION['sess_user_id'] = $user_id;
		$_SESSION['sess_last_auth_time'] = time();
		$_SESSION['sess_sub_key'] = md5($user_id.':'.$user_pw);

		$ha1 = md5($_SESSION['sess_ip'].':'.$_SESSION['sess_last_auth_time']);
		$_SESSION['sess_auth_key'] = md5($_SESSION['sess_sub_key'].':'.$ha1);
		ResponseText(TRUE);
		
	}else{
		ResponseText(FALSE);
	}
	*/
}


$classInstances= GetClassInstance('user');
$userConf	= $classInstances['UserConfiguration'];

function isEmailSmsData()
{
	$classInstances= GetClassInstance('ftpemail');
	$smtpConf 		= $classInstances['SMTPSetting'];
	$smsConf		= $classInstances['SMSSetting'];

	if( !empty($smtpConf->dataInfo['Server']['value']) || !empty($smsConf->dataInfo['Sender']['value']))
	{
		return true;
	}
	else
	{
		return false;
	}
}

//require_once ('../cgi-bin/adv/info.class');
//$classInstances['Information'] = $GLOBALS['SOCKET_MANAGER']->Connection(new Information());

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

		function Restore(){
			document.location = './pw_restore.cgi';
		}

		function LoginChk()
		{
			if ($("#user_id").val() == '' || $("#user_pw").val() == ''){
				alert("<?php echo $msg_id_pw_msg[$GLOBALS['LANGINDEX']]; ?>");
				return;
			}
			ajaxLogin();
		}

		function ajaxLogin()
		{
			var reqUrl = "<?php echo GetMyRequestURI($_SERVER['SCRIPT_NAME']); ?>";
			if (BrowserDetect.browser == 'Explorer' || (BrowserDetect.browser == 'Safari' && reqUrl.search('.local') != -1)) {
				reqUrl = ".."+reqUrl.substr(reqUrl.indexOf("/home/"));
			}
			
			$.ajax({
				type: "POST",
				async: false,
				cache: false,
				url: reqUrl,
				dataType: "text",
				data: { user_id: $('#user_id').val(), user_pw: encodeURIComponent($('#user_pw').val()), lastAuthTime : 0 },
				success: LoginSuccess
			});
		}

		function LoginSuccess(req)
		{			
			if (typeof req == "undefined")	{
				alert("undefined");
				return;
			}

			switch (req) {
				case 'OK':
					document.location.replace("<?php echo $_SESSION['sess_last_page']; ?>");
					break;
				case 'LO':
					alert("<?php echo $t_LoginLocked[$GLOBALS['LANGINDEX']]; ?>");
					break;
				default:
					//location.href = reqUrl+"?user_id="+$("#user_id").val()+"&user_pw="+encodeURIComponent($("#user_pw").val())+"&lastAuthTime=0";			
					alert("<?php echo $msg_invalid_id_pw[$GLOBALS['LANGINDEX']]; ?>");
					break;
			}
		}
	//-->
	</script>
	</head>
	<body onload="OnLoad()" onselectstart="return false">
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
					<h3 class="wid320" align="left" style="width:400px" ><?php echo $t_UserLogin[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>
				<table class="data_write" align="center" style="width:400px">

					<colgroup>
						<col style="width:140px;" />
						<col />
					</colgroup>
					<tbody>
						<tr>
							<th scope="row"><?php echo $t_UserName[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<input type="text" id="user_id" class="text" style="width:210px;" maxlength="8"/>
							</td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_password[$GLOBALS['LANGINDEX']]; ?></th>
						<?php if($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>
							<td>
								<input type="password" id="user_pw" class="text"  onkeypress="IsNumCharSym_S1(event);" style="width:210px;" maxlength="16"/>
							</td>
						<?php } 
						else { ?>
							<td>
								<input type="password" id="user_pw" class="text" style="width:210px;" maxlength="15"/>
							</td>	
						<?php } ?>	
						</tr>
					</tbody>
				</table>
				<div style="text-align:center; margin-top:40px;">
					<a id="window_crop_mid_ok_btn" class="btn_apply_login" href="javascript:LoginChk()"><?php echo $t_loginBtn[$GLOBALS['LANGINDEX']]; ?></a>
					
					<?php if( $userConf->dataInfo['IsEnablePasswordRestore']['value'] == 1) { ?>
					<!-- DEV_S1PWRESTORE -->
					<!--<a id="window_crop_mid_store_btn" class="btn_apply_login" href="javascript:Restore()"><?php echo $t_passwordRestoreBtn[$GLOBALS['LANGINDEX']]; ?></a>-->
						<?php if ( isEmailSmsData() ) { ?>
							<a id="window_crop_mid_store_btn" class="btn_apply_login" href="javascript:Restore()"><?php echo $t_passwordRestoreBtn[$GLOBALS['LANGINDEX']]; ?></a>
						<?php } ?>
					<!-- DEV_S1PWRESTORE // -->
					<?php } ?>
				</div>
			</div>
		</div>
	</body>
</html>
