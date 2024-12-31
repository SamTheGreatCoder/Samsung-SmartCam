<?php
require_once ('../cgi-bin/adv/_define.inc');
require_once ('./language/language_menu.cgi');
require_once ('./language/language_system_user.cgi');

$classInstances = array();
$GLOBALS['SOCKET_MANAGER'] = new SocketManager();
require_once ('../cgi-bin/adv/info.class');

if (isset($_REQUEST['pass'])) {
	if($GLOBALS['M_SPECIAL_TYPE'] == 1) {
		$pass = $_REQUEST['pass'];
		$pass = str_replace('\\\\', '\\', $pass );
		$pass = str_replace('\\\'', '\'', $pass );
		$pass = str_replace("\\\"", "\"", $pass );
		$pass = urldecode($pass);
	}
	else {
		str_replace('&_=', '', urldecode(trim(@file_get_contents('php://input'))));
	}
	require_once ('../cgi-bin/adv/user.class');
	$userConf = new UserConfiguration();
	$GLOBALS['SOCKET_MANAGER']->Connection($userConf);
	if($GLOBALS['M_SPECIAL_TYPE'] == 1) {
		$userConf->user[0]->dataInfo['Password']['value'] = $pass;
	}
	else {
		$userConf->user[0]->dataInfo['Password']['value'] =  $_REQUEST['pass'];
	}

	if($GLOBALS['M_SPECIAL_TYPE'] == 1) {
		$userConf->user[0]->payload = MakePayloadNoTrim($userConf->user[0]->dataInfo);
	}
	else {
		$userConf->user[0]->payload = MakePayload($userConf->user[0]->dataInfo);
	}

	$userConf->headerInfo['Action'] = ACTION_SET;
	$userConf->SetPayload();
	$GLOBALS['SOCKET_MANAGER']->Connection($userConf);
	if($GLOBALS['M_SPECIAL_TYPE'] == 1) {
		$classInstances['Information'] = $GLOBALS['SOCKET_MANAGER']->Connection(new Information());
		if($classInstances['Information']->dataInfo['PasswordCheck']['value'] == 0){
			echo $pass;
		}
	}
	exit;
}

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
		top:53%; 
		left:41%; 
		width:550px; 
		height:500px; 
		overflow:hidden; 
		margin-top:-150px; 
		margin-left:-100px;}
   }
	</style>
	<script type="text/javascript" src="./js/jquery-1.9.1.js"></script>
	<script type="text/javascript" src="./js/common_function.js"></script>
	<script type="text/javascript">

	var errNumCharSymMsg = "<?php echo $msg_pw_rule9[$GLOBALS['LANGINDEX']]; ?>";

<?php
	if ($classInstances['Information']->dataInfo['PasswordCheck']['value'] != 1) {
?>
		document.location = "../index.htm";
<?php
	}
?>
	
	function OnLoad() {}

	function CheckAdminPW()
	{
		var passwdMsgArray = new Array();
		passwdMsgArray[0] = "<?php echo ""; ?>";
		passwdMsgArray[1] = "<?php echo $msg_pw_rule1[$GLOBALS['LANGINDEX']]; ?>";
		passwdMsgArray[2] = "<?php echo $msg_pw_rule2[$GLOBALS['LANGINDEX']]; ?>";
		passwdMsgArray[3] = "<?php echo $msg_pw_rule3[$GLOBALS['LANGINDEX']]; ?>";
		passwdMsgArray[4] = "<?php echo $msg_pw_rule4[$GLOBALS['LANGINDEX']]; ?>";
		<?php if($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>
			passwdMsgArray[5] = "<?php echo $msg_pw_rule5_s1[$GLOBALS['LANGINDEX']]; ?>";
		<?php } else { ?>
			passwdMsgArray[5] = "<?php echo $msg_pw_rule5[$GLOBALS['LANGINDEX']]; ?>";
		<?php } ?>


		if($('#user_admin_pw').val() == "" && $('#user_admin_cpw').val() == "") {
			alert("<?php echo $msg_invalid_pw[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		<?php if($GLOBALS['M_SPECIAL_TYPE'] != 1) { ?>
		if(!CheckNumCharSym($('#user_admin_pw').val()))
		{
			alert("<?php echo $msg_invalid_pw[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		<?php } ?>
		<?php if($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>
	
			var ret = isSafePassword_S1($('#user_admin_pw').val());
		<?php } 
		else { ?>
			var ret = isSafePassword($('#user_admin_pw').val());
		<?php } ?>	
		if (ret != 0) {
			alert(passwdMsgArray[ret]);
			return false;
		}
		<?php if($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>
			ret = isSafePassword_S1($('#user_admin_cpw').val());
		<?php } 
		else { ?>
			ret = isSafePassword($('#user_admin_cpw').val());
		<?php } ?>
		if (ret != 0) {
			alert(passwdMsgArray[ret]);
			return false;
		}

		if($('#user_admin_pw').val() != $('#user_admin_cpw').val()) {
			alert("<?php echo $msg_chek_Admin_pw[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		return true;
	}

	function OnClickPasswordApply()
	{
		if (!CheckAdminPW())	return;

		var reqUrl = "<?php echo GetMyRequestURI($_SERVER['SCRIPT_NAME']); ?>";
		if (BrowserDetect.browser == 'Explorer' || (BrowserDetect.browser == 'Safari' && reqUrl.search('.local') != -1)) {
			reqUrl = ".."+reqUrl.substr(reqUrl.indexOf("/home/"));
		}
		$.ajax({
		  type: 'POST',
		  url: reqUrl,
		  data: "pass="+encodeURIComponent($('#user_admin_pw').val()),
		  success:  function(data){ alert("<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>"); window.location.href = './monitoring.cgi'; },
		  dataType: 'text'
		});
	}

	</script>
	</head>
	<body onload="OnLoad()" onselectstart="return false">
		<div id="wrap">
			<div id="head">
		<?php 
			if($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>
				<div class="head-top2">
				<h1><img src="./images/common/top_title_1.png" alt="S1" /></h1>
				<div class="logo"></div>
			<?php } 
				else { 
			?>
				<div class="head-top">
					<h1><img src="./images/common/top_title.gif" alt="iPOLiS NETWORK CAMERA WEBVIEWER" /></h1>
					<div class="logo"><img src="./images/common/top_logo.gif" alt="SAMSUNG TECHWIN" /></div>
			<?php } ?>
				</div>
			</div>
		</div>
		<div id="container">
			<div class="window">
				<div class="h3_tit mgt0" style="width:500px">
					<h3 class="wid320"><?php echo $t_adminPwChange[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>
				<table class="data_write">
					<colgroup>
						<col style="width:240px;" />
						<col />
					</colgroup>
					<tbody>
						<tr>
							<th scope="row"><?php echo $t_new_pw[$GLOBALS['LANGINDEX']]; ?></th>
						<?php if($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>
							<td><input type="password" id="user_admin_pw" class="text" style="width:210px;" onkeypress="IsNumCharSym_S1(event);" maxlength="16"/></td>
						<?php } 
						else { ?>
							<td><input type="password" id="user_admin_pw" class="text" style="width:210px;" onkeypress="IsNumCharSym(event, errNumCharSymMsg);" maxlength="15"/></td>
							<?php } ?>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_new_cpw[$GLOBALS['LANGINDEX']]; ?></th>
						<?php if($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>
							<td><input type="password" id="user_admin_cpw" class="text" style="width:210px;" onkeypress="IsNumCharSym_S1(event);" maxlength="16"/></td>
						<?php } 
						else { ?>
							<td><input type="password" id="user_admin_cpw" class="text" style="width:210px;" onkeypress="IsNumCharSym(event, errNumCharSymMsg);" maxlength="15"/></td>
							<?php } ?>
						</tr>
					</tbody>
				</table>
				
				<table style="width:500px;margin-top:20px;padding:10px;border:1px solid #fff;">
					<tbody>
						<tr>
							<td>. <?php echo $msg_pw_rule6[$GLOBALS['LANGINDEX']]; ?></td>
						</tr> 	
						<tr>
							<?php if($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>
								<td>. <?php echo $msg_pw_rule7_s1[$GLOBALS['LANGINDEX']]; ?></td>
							<?php }else { ?>
								<td>. <?php echo $msg_pw_rule7[$GLOBALS['LANGINDEX']]; ?></td>
							<?php } ?>
						</tr>
						<tr>
							<td>. <?php echo $msg_pw_rule8[$GLOBALS['LANGINDEX']]; ?></td>
						</tr>
						<tr>
							<?php if($GLOBALS['M_SPECIAL_TYPE'] != 1) { ?>
								<td>. <?php echo $msg_pw_rule9[$GLOBALS['LANGINDEX']]; ?></td>
							<?php } ?>
						</tr>
						<tr>
							<?php if($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>
								<td>. <?php echo $msg_pw_rule10_s1[$GLOBALS['LANGINDEX']]; ?></td>
							<?php }else { ?>
								<td>. <?php echo $msg_pw_rule10[$GLOBALS['LANGINDEX']]; ?></td>
							<?php } ?>
						</tr>
						<tr>
							<?php if($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>
								<td>. <?php echo $msg_pw_rule11_s1[$GLOBALS['LANGINDEX']]; ?></td>
							<?php }else { ?>
								<td>. <?php echo $msg_pw_rule11[$GLOBALS['LANGINDEX']]; ?></td>
							<?php } ?>
						</tr>
					</tbody>
				</table>
				<div style="text-align:center; margin-top:40px;">
					<a id="window_crop_mid_ok_btn" class="btn_apply" href="javascript:OnClickPasswordApply()"><?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?></a>
				</div>
			</div>
		</div>
	</body>
</html>
