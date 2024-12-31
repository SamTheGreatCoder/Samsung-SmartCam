<?php
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_menu.cgi');
require_once ('../language/language_system_user.cgi');

$classInstances = GetClassInstance('user');
$userConf = $classInstances['UserConfiguration'];
if ($GLOBALS['M_SPECIAL_TYPE'] == 1)
{
	$Period = $userConf->dataInfo['Period']['value'];	// DEV_S1PWD_CHANGE_TIME
}
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
	<script type="text/javascript">
	<!--
<?php
if ($GLOBALS['M_SPECIAL_TYPE'] == 1)
{		
?>
		$(document).ready(function(){
			$("#PWDPeriod").val(<?=$Period?>).attr('selected',true);
		});
<?php 
}
?>
	//-->
	</script>
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

	var oldSelNo;
	var user_cnt = 0;
	var maxUserNum = <?php echo MAX_USER_10; ?>;
	var adminPw		= "";
	var passwdMsgArray = new Array();
	var passwdArray = new Array();
	var pwvalidArray = new Array();
	<?php
		for ($index=1; $index<=10; ++$index) { ?>
			pwvalidArray[<?php echo $index-1?>] = "<?php echo SafePassword($userConf->user[$index]->dataInfo['Password']['value'],  $userConf->user[$index]->dataInfo['Name']['value'])?>";
	<?php } ?>
	var errNumCharSymMsg = "<?php echo $msg_pw_rule9[$GLOBALS['LANGINDEX']]; ?>";

	var isS1model = <?php echo $GLOBALS['M_SPECIAL_TYPE']; ?>;

	function OnClickApply()
	{
		if (!CheckNamePw() || !CheckAdminPW())	return;

		var nameArr = new Array();
		for (var index=0; index<10; ++index) {
			if($('tr').hasClass('user_list_'+index)) {
				nameArr[index] = $('#user_name_'+index).val();
				if((nameArr[index]).toLowerCase() == "admin" || (nameArr[index]).toLowerCase() == "guest"){
					alert("<?php echo $msg_adminguest[$GLOBALS['LANGINDEX']]; ?>");
					return;
				}

				if ((($('#user_enable_'+index).is(':checked')) == 0) ) continue;
				
				if($('#user_name_'+index).val() == ""  || ($('#user_pw_'+index).val() == "" && pwvalidArray[index] != 0) ) {
					alert("<?php echo $msg_id_pw_msg[$GLOBALS['LANGINDEX']]; ?> ["+$('#user_name_'+index).val()+"]");
					return;
				}

				if($('#user_name_'+index).val().indexOf(" ") >=0 || $('#user_pw_'+index).val().indexOf(" ") >=0 ) {
					alert("<?php echo $msg_invalid_id_pw[$GLOBALS['LANGINDEX']]; ?>["+$('#user_name_'+index).val()+"]");
					return;
				}
			}
		}

		for (var index=0; index<9; ++index) {
			for (var index2=(index+1); index2<10; ++index2) {
				if($('tr').hasClass('user_list_'+index) && $('tr').hasClass('user_list_'+index2)) {
					if(nameArr[index] == nameArr[index2]) {
						alert("<?php echo $msg_id_duplicate[$GLOBALS['LANGINDEX']]; ?>");
						return;
					}
				}
			}
		}
		if (isS1model == 1) {
			adminPw = convertSymbolForXML(adminPw);
		}
		var msg = "<SetUser>";
		if($('#user_admin_pw').val() != "" && $('#user_admin_cpw').val() != "")
			msg += "<Admin><Password>"+adminPw+"</Password></Admin>";

		for (var index=0; index<10; ++index) {
			if($('tr').hasClass('user_list_'+index)) {
				msg += "<User>";
				msg += "<Enabled>"+($('#user_enable_'+index).is(':checked') ? 1 : 0)+"</Enabled>";
				msg += "<Name>"+$('#user_name_'+index).val()+"</Name>";
				if (isS1model == 1) {
					var pw = convertSymbolForXML($('#user_pw_'+index).val());
					msg += "<Password>"+ pw +"</Password>";
				}
				else {
					msg += "<Password>"+$('#user_pw_'+index).val()+"</Password>";
				}
				msg += "<UserRightProfile>"+$('#user_profile_'+index).val()+"</UserRightProfile>";
		<?php	
			if ($GLOBALS['M_SUPPORT_AUDIO']) { 
		?>
				msg += "<UserRightAudioIn>"+($('#user_audioin_'+index).is(':checked') ? 1 : 0)+"</UserRightAudioIn>";
			<?php	
				if ($GLOBALS['M_SUPPORT_AUDIO_OUT']) { 
			?>
				msg += "<UserRightAudioOut>"+($('#user_audioout_'+index).is(':checked') ? 1 : 0)+"</UserRightAudioOut>";
			<?php 
				}
			?>
		<?php 
			}
			if($GLOBALS['M_ALARMOUT_COUNT'] > 0) {
		?>
				msg += "<UserRightRelay>"+($('#user_relay_'+index).is(':checked') ? 1 : 0)+"</UserRightRelay>";
		<?php 
			}
			if($GLOBALS['M_SUPPORT_PTZ'] || $GLOBALS['M_SUPPORT_EXTERNAL_PTZ']) {
		?>
				msg += "<UserRightPTZ>"+($('#user_ptz_'+index).is(':checked') ? 1 : 0)+"</UserRightPTZ>";
		<?php 
			}
		?>
				msg += "</User>";
			}
		}
		msg += "<Guest>";
		msg += "<Enabled>"+($('#guest_use').is(':checked') ? 1 : 0)+"</Enabled>";
		msg += "<UserRightProfile>"+($('#rtsp_noauth_use').is(':checked') ? 1 : 0)+"</UserRightProfile>";
		msg += "</Guest>";
		if (isS1model == 1)
		{
			// DEV_S1PWD_CHANGE_TIME start
			msg += "<PWDTime>";
			msg += "<Period>" + ($('#PWDPeriod').val())+"</Period>";
			msg += "</PWDTime>";
			// DEV_S1PWD_CHANGE_TIME end

			// DEV_S1ENC start
			msg += "<RTPEncryptSetting>";
			msg += "<IsEnableNoEncrypt>" + ($('#rtsp_noencrypt_use').is(':checked') ? 1 : 0) + "</IsEnableNoEncrypt>";
			msg += "</RTPEncryptSetting>";	
			// DEV_S1ENC start

			// DEV_S1PWRESTORE start
			msg += "<PasswordRestoreSetting>";
			msg += "<IsEnablePasswordRestore>" + ($('#password_restore_use').is(':checked') ? 1 : 0) + "</IsEnablePasswordRestore>";
			msg += "</PasswordRestoreSetting>";
			// DEV_S1PWRESTORE end
		}
		msg += "</SetUser>";

		RequestAjaxMsg(msg, "<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $GLOBALS['REQUEST_URI'].'?seq='.$_SESSION['count'] ?>");
	}

	function CheckNamePw()
	{
		for(var index=0; index<10; ++index) {
			if($('tr').hasClass('user_list_'+index)) {
				if(!TypeCheck($('#user_name_'+index).val(), ALPHA+NUM)) {
					if($('#user_name_'+index).val() == ''){
						alert("<?php echo $msg_invalid_id[$GLOBALS['LANGINDEX']]; ?>");
					} else {
						alert("<?php echo $msg_invalid_id[$GLOBALS['LANGINDEX']]; ?> ["+$('#user_name_'+index).val()+"]");
					}
					return false;
				}
				
				if ($('#user_enable_'+index).is(':checked') == false) continue;
				if ( $('#user_pw_'+index).val().length==0) 
				{
					if (pwvalidArray[index] == 0)
					{
						continue;
					}
					else
					{
						alert(" \""+$('#user_name_'+index).val()+"\" : "+passwdMsgArray[pwvalidArray[index]]);
						return false;
					}
				}
				<?php if($GLOBALS['M_SPECIAL_TYPE'] != 1) { ?>
					if(!CheckNumCharSym($('#user_pw_'+index).val()))
					{
						alert("<?php echo $msg_invalid_id_pw[$GLOBALS['LANGINDEX']]; ?> ["+$('#user_name_'+index).val()+"]");
						return false;
					}
				<?php } ?>
				<?php if($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>
					var ret = isSafePassword_S1($('#user_pw_'+index).val(),$('#user_name_'+index).val());
				<?php } 
				else { ?>
					var ret = isSafePassword($('#user_pw_'+index).val(),$('#user_name_'+index).val());
				<?php } ?>
					if (ret != 0) {
						alert(passwdMsgArray[ret]+" ["+$('#user_name_'+index).val()+"]");
						return false;
					}
					
			}
		}
		return true;
	}

	function CheckAdminPW()
	{
		if($('#user_admin_pw').val() == "" && $('#user_admin_cpw').val() == "") return true;
		
		<?php if($GLOBALS['M_SPECIAL_TYPE'] != 1) { ?>
			if(!CheckNumCharSym($('#user_admin_pw').val()))
			{
				alert("<?php echo $msg_invalid_id_pw[$GLOBALS['LANGINDEX']]; ?> [admin]");
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
			alert(passwdMsgArray[ret]+" [admin]");
			return false;
		}
		<?php if($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>
			ret = isSafePassword_S1($('#user_admin_cpw').val());
		<?php } 
		else { ?>
			ret = isSafePassword($('#user_admin_cpw').val());
		<?php } ?>
		if (ret != 0) {
			alert(passwdMsgArray[ret]+" [admin]");
			return false;
		}

		if($('#user_admin_pw').val() != $('#user_admin_cpw').val()) {
			alert("<?php echo $msg_chek_Admin_pw[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		adminPw = $('#user_admin_pw').val();
		return true;
	}

	function CheckCurrentPW()
	{
		var direcmsg = $('#user_current_admin_pw').val();
// DEV_S1COMPLEX
		if (isS1model == 1) {
			$.ajax({
			  type: 'POST',
			  url: '/home/setup/pw_check.cgi',
			  data: { pw : encodeURIComponent(direcmsg) },
			  async: true,
			  success:  function(data){
			  				if($('#user_admin_pw').val() == "" && $('#user_admin_cpw').val() == "" && $('#user_current_admin_pw').val() == "") {
								OnClickApply();
			  				}else {
				  				if(data == 0)
								{
				  			   		alert("<?php echo $msg_invalid_userPW[$GLOBALS['LANGINDEX']]; ?>");
								}
			  				 	else {
			  				 		if($('#user_admin_pw').val() == "" && $('#user_admin_cpw').val() == "")
			  				 			alert("<?php echo $msg_pw_rule1[$GLOBALS['LANGINDEX']]; ?> [admin]");
			  				 		else
			  				   		OnClickApply();
			  				   }
		  				   }},
		  	dataType: 'text'
			});
		}

		else {
			while(direcmsg.indexOf('%') >= 0)
			{
				direcmsg = direcmsg.replace('%', '#4!2');
			}

			while(direcmsg.indexOf('+') >= 0)
			{
				direcmsg = direcmsg.replace('+', '#4!3');
			}
			$.ajax({
			  type: 'POST',
			  url: '/home/setup/pw_check.cgi',
			  data: 'pw='+direcmsg,
			  async: true,
			  success:  function(data){
			  				if($('#user_admin_pw').val() == "" && $('#user_admin_cpw').val() == "" && $('#user_current_admin_pw').val() == "") {
								OnClickApply();
			  				}else {
				  				if(data == 0)
								{
				  			   		alert("<?php echo $msg_invalid_userPW[$GLOBALS['LANGINDEX']]; ?>");
								}
			  				 	else {
			  				 		if($('#user_admin_pw').val() == "" && $('#user_admin_cpw').val() == "")
			  				 			alert("<?php echo $msg_pw_rule1[$GLOBALS['LANGINDEX']]; ?> [admin]");
			  				 		else
			  				   		OnClickApply();
			  				   }
		  				   }},
		  	dataType: 'text'
			});
		}
	}
	function OnClickUserList()
	{
		var selNo = $("input[name='user_select']:checked").val();
		if (selNo != oldSelNo && typeof oldSelNo != "undefined") {
			$('#user_enable_'+oldSelNo).attr('disabled', 'disabled');
			$('#user_name_'+oldSelNo).attr('disabled', 'disabled');
			$('#user_pw_'+oldSelNo).attr('disabled', 'disabled');
			$('#user_audioin_'+oldSelNo).attr('disabled', 'disabled');
			$('#user_audioout_'+oldSelNo).attr('disabled', 'disabled');
			$('#user_relay_'+oldSelNo).attr('disabled', 'disabled');
			$('#user_ptz_'+oldSelNo).attr('disabled', 'disabled');
			$('#user_profile_'+oldSelNo).attr('disabled', 'disabled');			
			$('#user_profile_'+oldSelNo).parent().css('color', '#6d6d6d');
		}
		$('#user_enable_'+selNo).removeAttr('disabled');
		$('#user_name_'+selNo).removeAttr('disabled');
		$('#user_pw_'+selNo).removeAttr('disabled');
		$('#user_audioin_'+selNo).removeAttr('disabled');
		$('#user_audioout_'+selNo).removeAttr('disabled');
		$('#user_relay_'+selNo).removeAttr('disabled');
		$('#user_ptz_'+selNo).removeAttr('disabled');
		$('#user_profile_'+selNo).removeAttr('disabled');
		$('#user_profile_'+selNo).parent().css('color', '#1c1c1c');
		oldSelNo = selNo;
	}

	function OnClickAdd()
	{
		if (user_cnt == 10) {
			alert("<?php echo $msg_cannot_add[$GLOBALS['LANGINDEX']]; ?>");
			return;
		}

		var addNo = 0;
		for(var index=0; index<10; ++index) {
			if($('tr').hasClass('user_list_'+index)) continue;
			addNo = index;
			break;
		}

		$('#user_list').append(
			"<tr class='user_list_"+addNo+"'>\
				<td><input type='radio' name='user_select' id='user_select_"+addNo+"' onClick='OnClickUserList();' value='"+addNo+"' checked='checked'/></td>\
				<td><input type='checkbox' id='user_enable_"+addNo+"'/></td>\
				<td><input type='text' id='user_name_"+addNo+"' class='listtext' style='width:78px;'  onkeypress='IsNumChar(event);' onkeydown='CheckKorean(event);'  value='' maxlength='8' /></td>\
				<?php if($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>
				<td><input type='password' id='user_pw_"+addNo+"' class='listtext' style='width:104px;' onkeypress='IsNumCharSym_S1(event);' value='' maxlength='16' /></td>\
				<?php } 
				else { ?>
				<td><input type='password' id='user_pw_"+addNo+"' class='listtext' style='width:104px;' onkeypress='IsNumCharSym(event, errNumCharSymMsg);' value='' maxlength='15' /></td>\
				<?php } ?>
				<?php if($GLOBALS['M_SUPPORT_AUDIO']) { ?>
				<td><input type='checkbox' id='user_audioin_"+addNo+"'/></td>\
					<?php if($GLOBALS['M_SUPPORT_AUDIO_OUT']) { ?>
				<td><input type='checkbox' id='user_audioout_"+addNo+"'/></td>\
					<?php }?>
				<?php }if($GLOBALS['M_ALARMOUT_COUNT'] > 0) {?>
				<td><input type='checkbox' id='user_relay_"+addNo+"'/></td>\
				<?php }if($GLOBALS['M_SUPPORT_PTZ'] || $GLOBALS['M_SUPPORT_EXTERNAL_PTZ']) { ?>
				<td><input type='checkbox' id='user_ptz_"+addNo+"'/></td>\
				<?php }?>
				<td><select id='user_profile_"+addNo+"' class='selectbox_style_wid123' >	<option value='0'><?php echo $t_default[$GLOBALS['LANGINDEX']]; ?></option><option value='1'><?php echo $t_all[$GLOBALS['LANGINDEX']]; ?></option></select></td>\
			</tr>"
		);
		user_cnt++;

		//$('#user_enable_'+addNo).styledSelect( {innerClass:'selectbox_style_option'} );
		$('#user_profile_'+addNo).styledSelect( {innerClass:'selectbox_style_option'} );
		$('#user_select_'+oldSelNo).prop('checked',false);
		OnClickUserList();
	}

	function OnClickDelete()
	{
		if (!CheckDeletedTarget('user'))	return;
		OnClickUserList();
	}
	
	var userkey	= new Array();

	function GetUserInfo()
	{
		var temp = RequestGetConfig("ttttttttttttttttt");
		userkey = temp.split(" ");

	}

	function OnLoad()
	{
		//GetUserInfo();

		passwdMsgArray[0] = "<?php echo ""; ?>";
		passwdMsgArray[1] = "<?php echo $msg_pw_rule1[$GLOBALS['LANGINDEX']]; ?>";
		passwdMsgArray[2] = "<?php echo $msg_pw_rule2[$GLOBALS['LANGINDEX']]; ?>";
		passwdMsgArray[3] = "<?php echo $msg_pw_rule3[$GLOBALS['LANGINDEX']]; ?>";
		passwdMsgArray[4] = "<?php echo $msg_pw_rule4[$GLOBALS['LANGINDEX']]; ?>";
		if (isS1model == 1) {
			passwdMsgArray[5] = "<?php echo $msg_pw_rule5_s1[$GLOBALS['LANGINDEX']]; ?>";
		}
		else {
			passwdMsgArray[5] = "<?php echo $msg_pw_rule5[$GLOBALS['LANGINDEX']]; ?>";
		}

		//for (var index=0; index<10; ++index) {
		//	$('#user_pw_'+index).val(userkey[index]);
		//}
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
			<div id="container" style="width:1350px">
			<?php
				PrintLeftMenu($_SERVER['SCRIPT_NAME']);
			?>

			<div id="contents" style="<?php if($GLOBALS['M_SUPPORT_AUDIO'] && $GLOBALS['M_ALARMOUT_COUNT'] > 0) { if($GLOBALS['M_SUPPORT_PTZ'] || $GLOBALS['M_SUPPORT_EXTERNAL_PTZ']) {echo 'width:785px;';} else {echo 'width:735px;';} }else {echo 'width:680px;';} ?>">
				<div class="h3_tit mgt0" style="overflow:auto;width:100%;">
					<h3 class="wid320" ><?php echo $t_adminPwChange[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>
				<table class="data_write">
					<colgroup>
						<col style="width:180px;" />
						<col />
					</colgroup>
					<tbody>
						<tr>
							<th scope="row"><?php echo $t_current_pw[$GLOBALS['LANGINDEX']]; ?></th>
						<?php if($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>
							<td><input type="password" id="user_current_admin_pw" name="current_pw" class="text" style="width:210px;"  onkeypress="IsNumCharSym_S1(event);" maxlength="16" /></td>
						<?php } 
						else { ?>
							<td><input type="password" id="user_current_admin_pw" name="current_pw" class="text" style="width:210px;"  onkeypress="IsNumCharSym(event, errNumCharSymMsg);" maxlength="15" /></td>
						<?php } ?>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_new_pw[$GLOBALS['LANGINDEX']]; ?></th>
						<?php if($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>					
							<td><input type="password" id="user_admin_pw" class="text" style="width:210px;"  onkeypress="IsNumCharSym_S1(event);" maxlength="16" /></td>
						<?php } 
						else { ?>
							<td><input type="password" id="user_admin_pw" class="text" style="width:210px;"  onkeypress="IsNumCharSym(event, errNumCharSymMsg);" maxlength="15" /></td>
						<?php } ?>	
						</tr>
						<tr>
							<th scope="row"><?php echo $t_cPassword[$GLOBALS['LANGINDEX']]; ?></th>
						<?php if($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>	
							<td><input type="password" id="user_admin_cpw" class="text" style="width:210px;"  onkeypress="IsNumCharSym_S1(event);" maxlength="16"/></td>
						<?php } 
						else { ?>
							<td><input type="password" id="user_admin_cpw" class="text" style="width:210px;"  onkeypress="IsNumCharSym(event, errNumCharSymMsg);" maxlength="15"/></td>
						<?php } ?>	
						
						</tr>
					</tbody>
				</table>
				<table style="width:785px;margin-top:10px;padding:10px;border:1px solid #fff;">
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
				<div class="h3_tit" style="overflow:auto;width:100%">
					<h3 class="wid220"><?php echo $t_guestSetup[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>
				<table class="data_write">
					<tr>
						<td>
							<label><input type="checkbox" id="guest_use" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" <?php if ($userConf->user[11]->dataInfo['Enabled']['value'] == true) echo "checked=\"checked\""; ?> /><?php echo $t_enableGuest[$GLOBALS['LANGINDEX']]; ?></label>
						</td>
					</tr>
				</table>
				<div class="h3_tit" style="overflow:auto;width:100%">
					<h3 class="wid320"><?php echo $t_authSetup[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>
				<table class="data_write">
					<tr>
						<td>
							<label><input type="checkbox" id="rtsp_noauth_use" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" <?php if ($userConf->user[11]->dataInfo['UserRightProfile']['value'] == true) echo "checked=\"checked\""; ?> /><?php echo $msg_rtspNoAuth[$GLOBALS['LANGINDEX']]; ?></label>
						</td>
					</tr>
				</table>
				<?php if($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>
				<!-- DEV_S1ENC start -->
				<div class="h3_tit" style="overflow:auto;width:100%">
					<h3 class="wid320"><?php echo $t_rtspSetup[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>
				<table class="data_write">
					<tr>
						<td>
							<label><input type="checkbox" id="rtsp_noencrypt_use" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" <?php if ($userConf->dataInfo['IsEnableNoEncrypt']['value'] == true) echo "checked=\"checked\""; ?> /><?php echo $t_rtspNoEncrypt[$GLOBALS['LANGINDEX']]; ?></label>
						</td>
					</tr>
				</table>
				<!-- DEV_S1ENC start -->

				<!-- DEV_S1PWRESTORE -->
				<div class="h3_tit" style="overflow:auto;width:100%">
					<h3 class="wid320"><?php echo $t_passwordRestore[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>
				<table class="data_write">
					<tr>
						<td>
							<label><input type="checkbox" id="password_restore_use" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" <?php if ($userConf->dataInfo['IsEnablePasswordRestore']['value'] == true) echo "checked=\"checked\""; ?> /><?php echo $t_passwordRestoreUse[$GLOBALS['LANGINDEX']]; ?></label>
						</td>
					</tr>
				</table>
				<!-- DEV_S1PWRESTORE // -->

				<!-- DEV_S1PWD_CHANGE_TIME -->
				<div class="h3_tit" style="overflow:auto;width:100%">
					<h3 class="wid320"><?php echo $t_passwordChangePeriod[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>
				<table class="data_write">
					<tr>
						<td>
							<select name="select" id="PWDPeriod" class="selectbox_style_width160" >
							<?for ($index=1; $index<=6; ++$index) {?>
								<option value="<?=$index?>"> <?php	echo ($index * 30). $t_passwordChangeUnit[$GLOBALS['LANGINDEX']];	?> </option>
							<?}?>
							</select>
						</td>
					</tr>
				</table>
				<!-- DEV_S1PWD_CHANGE_TIME // -->
				<?php } ?>
				<div class="h3_tit" style="overflow:auto;width:100%">
					<h3 class="wid180"><?php echo $t_currentUsers[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>
				<table id="user_list" class="data_table2" style="overflow:auto;table-layout:auto">
					<colgroup>
						<col style="width:19px;" />
						<col style="width:98px;" />
						<col style="width:82px;" />
						<col style="width:104px;" />
				<?php if($GLOBALS['M_SUPPORT_AUDIO']) { ?>
						<col style="width:100px;" />
					<?php if($GLOBALS['M_SUPPORT_AUDIO_OUT']) { ?>	
						<col style="width:100px;" />
					<?php }?>	
				<?php }if($GLOBALS['M_ALARMOUT_COUNT'] > 0) {?>
						<col style="width:100px;" />
				<?php }if($GLOBALS['M_SUPPORT_PTZ'] || $GLOBALS['M_SUPPORT_EXTERNAL_PTZ']){?>
						<col style="width:100px;" />
				<?php }?>
						<col style="width:123px;" />
					</colgroup>
					<thead>
						<tr>
							<th></th>
							<th><?php echo $t_use[$GLOBALS['LANGINDEX']]; ?></th>
							<th><?php echo $t_name[$GLOBALS['LANGINDEX']]; ?></th>
							<th><?php echo $t_password[$GLOBALS['LANGINDEX']]; ?></th>
			<?php if($GLOBALS['M_SUPPORT_AUDIO']) { ?>
							<th><?php echo $t_audioIn[$GLOBALS['LANGINDEX']]; ?></th>
				<?php if($GLOBALS['M_SUPPORT_AUDIO_OUT']) { ?>		
							<th><?php echo $t_audioOut[$GLOBALS['LANGINDEX']]; ?></th>
				<?php }?>		
			<?php }if($GLOBALS['M_ALARMOUT_COUNT'] > 0) {?>
							<th><?php echo $t_alarmOutput[$GLOBALS['LANGINDEX']]; ?></th>
			<?php }if($GLOBALS['M_SUPPORT_PTZ'] || $GLOBALS['M_SUPPORT_EXTERNAL_PTZ']) {?>
							<th>PTZ</th>
			<?php }?>
							<th><?php echo $t_profile[$GLOBALS['LANGINDEX']]; ?></th>
						</tr>
					</thead>
					<tbody>
			<?php
				$userCnt=0;
				for ($index=1; $index<=10; ++$index) {
					if ($userConf->user[$index]->dataInfo['Name']['value'] != "") {
			?>
						<tr class="user_list_<?php echo $userCnt; ?>">
							<td><input type="radio" name="user_select" id="user_select_<?php echo $userCnt; ?>" onClick="OnClickUserList();" value="<?php echo $userCnt; ?>" style="margin-left:2px"/></td>
							<td>
								<input type="checkbox" id="user_enable_<?php echo $userCnt; ?>" disabled="disabled" <?php if ($userConf->user[$index]->dataInfo['Enabled']['value'] == 1) echo "checked=\"checked\""; ?>/>
							</td>
							<td><input type="text" id="user_name_<?php echo $userCnt; ?>" class="listtext"  style="width:78px;" onkeypress="IsNumChar(event);" onkeydown="CheckKorean(event);"  value="<?php echo trim($userConf->user[$index]->dataInfo['Name']['value']); ?>" maxlength="8" disabled="disabled" /></td>
						<?php if($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>
							<td><input type="password" id="user_pw_<?php echo $userCnt; ?>" class="listtext" style="width:104px;"  onkeypress="IsNumCharSym_S1(event);" maxlength="16"  disabled="disabled" /></td>
						<?php } 
						else { ?>
							<td><input type="password" id="user_pw_<?php echo $userCnt; ?>" class="listtext" style="width:104px;"  onkeypress="IsNumCharSym(event, errNumCharSymMsg);" maxlength="15"  disabled="disabled" /></td>
						<?php } ?>
						
		<?php if($GLOBALS['M_SUPPORT_AUDIO']) { ?>
							<td><input type="checkbox" id="user_audioin_<?php echo $userCnt; ?>" <?php if ($userConf->user[$index]->dataInfo['UserRightAudioIn']['value'] == true) echo "checked=\"checked\""; ?> disabled="disabled"/></td>
			<?php if($GLOBALS['M_SUPPORT_AUDIO_OUT']) { ?>
							<td><input type="checkbox" id="user_audioout_<?php echo $userCnt; ?>" <?php if ($userConf->user[$index]->dataInfo['UserRightAudioOut']['value'] == true) echo "checked=\"checked\""; ?> disabled="disabled"/></td>
			<?php }?>	
		<?php }if($GLOBALS['M_ALARMOUT_COUNT'] > 0) {?>
							<td><input type="checkbox" id="user_relay_<?php echo $userCnt; ?>" <?php if ($userConf->user[$index]->dataInfo['UserRightRelay']['value'] == true) echo "checked=\"checked\""; ?> disabled="disabled"/></td>
		<?php }if($GLOBALS['M_SUPPORT_PTZ'] || $GLOBALS['M_SUPPORT_EXTERNAL_PTZ']) {?>
							<td><input type="checkbox" id="user_ptz_<?php echo $userCnt; ?>" <?php if ($userConf->user[$index]->dataInfo['UserRightPTZ']['value'] == true) echo "checked=\"checked\""; ?> disabled="disabled"/></td>
		<?php }?>
							<td>
								<select id="user_profile_<?php echo $userCnt; ?>" class="selectbox_style_wid123" disabled="disabled">
									<option value="0" <?php if ($userConf->user[$index]->dataInfo['UserRightProfile']['value'] == 0) echo "selected=\"selected\""; ?>><?php echo $t_default[$GLOBALS['LANGINDEX']]; ?></option>
									<option value="1" <?php if ($userConf->user[$index]->dataInfo['UserRightProfile']['value'] == 1) echo "selected=\"selected\""; ?>><?php echo $t_all[$GLOBALS['LANGINDEX']]; ?></option>
								</select>
								<script>
									$('#user_profile_<?php echo $userCnt; ?>').styledSelect( {innerClass:'selectbox_style_option'} );
								</script>
							</td>
						</tr>
				<?php
						$userCnt++;
					}
				}
				?>
					</tbody>
				</table>
				<script>user_cnt = parseInt(<?php echo $userCnt; ?>);</script>
				<div class="btn_add_left">
					<a id="mid_add_btn" class="btn_type01" href="javascript:OnClickAdd()"><?php echo $t_add[$GLOBALS['LANGINDEX']]; ?></a>&nbsp;
					<a id="mid_del_btn" class="btn_type01" href="javascript:OnClickDelete()"><?php echo $t_delete[$GLOBALS['LANGINDEX']]; ?></a>
				</div>
				<div class="btn_right">
					<a id="mid_ok_btn" class="btn_apply" href="javascript:CheckCurrentPW()"><?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?></a>
				</div>
				</div>
			</div>
		</div>
	</div>
</body>
</html>

