<?php
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_menu.cgi');
require_once ('../language/language_system_productInfo.cgi');

$classInstances= GetClassInstance('system');
$productInfo 	= $classInstances['SystemConfiguration']->deviceInfo;
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
	$(document).ready(function() { 
		lnbonoff("lnb_system");
		<?php if($GLOBALS['M_DEFAULT_LANGUAGE'] == 2) { ?>
		$("#info_language").attr('disabled', 'disabled'); 
		<?php } ?>
	});

	function OnClickApply()
	{
		if(TypeCheck($('#info_devicename').val(), ALPHA+NUM+'~`!@$^()_-|{}[];,./?'+SPACE) == false) {
			alert("<?php echo $msg_check_deviceName[$GLOBALS['LANGINDEX']];?>");
			return;
		}

		if(TypeCheck($('#info_location').val(), ALPHA+NUM+'~`!@$^()_-|{}[];,./?'+SPACE) == false) {
			alert("<?php echo $msg_check_location[$GLOBALS['LANGINDEX']];?>");
			return;
		}

		if(TypeCheck($('#info_desc').val(), ALPHA+NUM+'~`!@$^()_-|{}[];,./?'+SPACE) == false) {
			alert("<?php echo $msg_check_description[$GLOBALS['LANGINDEX']];?>");
			return;
		}

		if(TypeCheck($('#info_memo').val(), ALPHA+NUM+'~`!@$^()_-|{}[];,./?'+SPACE) == false) {
			alert("<?php echo $msg_check_memo[$GLOBALS['LANGINDEX']];?>");
			return;
		}

		var msg = "<SetProductInfo>";
		msg += "<DeviceName>"+$('#info_devicename').val()+"</DeviceName>";
		msg += "<Location>"+$('#info_location').val()+"</Location>";
		msg += "<Description>"+$('#info_desc').val()+"</Description>";
		msg += "<Memo>"+$('#info_memo').val()+"</Memo>";
		msg += "<Language>"+$('#info_language option:selected').val()+"</Language>";
		msg += "</SetProductInfo>";
		//msg = msg.split("?").join("%3F");
		RequestAjaxMsg(msg, "<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $GLOBALS['REQUEST_URI'].'?seq='.$_SESSION['count'] ?>");
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
				<div class="h3_tit mgt0">
					<h3 class="wid220"><?php echo $menu_proinfo[$GLOBALS['LANGINDEX']];?></h3>
				</div>
				<table class="data_write">
					<colgroup>
						<col style="width:180px;" />
						<col />
					</colgroup>
					<tbody>
						<tr>
							<th scope="row"><?php echo $t_model[$GLOBALS['LANGINDEX']];?></th>
							<td>
								<input type="text" class="text" style="width:191px;" value="<?php echo $productInfo->dataInfo['Model']['value']; ?>" disabled="disabled"/>
							</td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_serialNumber[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<input type="text" class="text" style="width:191px;" value="<?php echo $productInfo->dataInfo['SerialNum']['value']; ?>" disabled="disabled"/>
							</td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_deviceName[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<input type="text" id="info_devicename" class="text" style="width:191px;" value="<?php echo $productInfo->dataInfo['DeviceName']['value']; ?>" maxlength="8" onkeypress='NoKorean(event); IsSIM(event);' onkeydown='NoKorean(event)' />
							</td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_location[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<input id="info_location" class="text" style="width:191px;"  value="<?php echo $productInfo->dataInfo['Location']['value']; ?>" maxlength="32" onkeypress='NoKorean(event); IsSIM(event);' onkeydown='NoKorean(event)'/>
							</td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_description[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<input type="text" id="info_desc" class="text" style="width:191px;" value="<?php echo $productInfo->dataInfo['Description']['value']; ?>" maxLength="32" onkeypress='NoKorean(event); IsSIM(event);' onkeydown='NoKorean(event)'/>
							</td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_memo[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<input type="text" id="info_memo" class="text" style="width:191px;" value="<?php echo $productInfo->dataInfo['Memo']['value']; ?>" maxLength="32" onkeypress='NoKorean(event); IsSIM(event);' onkeydown='NoKorean(event)'/>
							</td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_language[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<select id="info_language" class="selectbox_style">
							<?php
								for ($index=0; $index<count($t_languageList); ++$index) {
							?>
									<option value="<?php echo $index;?>" <?php if ($index==$GLOBALS['LANGINDEX']) echo "selected=\"selected\""; ?>><?php echo $t_languageList[$index];?></option>
							<?php
								}
							?>
								</select>
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
