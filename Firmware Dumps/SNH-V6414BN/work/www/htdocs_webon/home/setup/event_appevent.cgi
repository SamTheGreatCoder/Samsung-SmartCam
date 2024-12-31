<?php

require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_menu.cgi');
require_once ('../language/language_event_common.cgi');
$event_name 	= 'opensdk';

$classInstances= GetClassInstance($event_name);
$event_class	= $classInstances['OpenSDKConfiguration'];
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="kr" xml:lang="kr">
<head>
	<title>iPOLiS NETWORK CAMERA WEBVIEWER</title>
	<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
	<meta http-equiv="X-UA-Compatible" content="IE=Edge; requiresActiveX=true" />
	<link rel="stylesheet" type="text/css" href="../css/techwin.css" />
	<link rel="stylesheet" type="text/css" href="../css/jquery.ui.core.css"/>
	<link rel="stylesheet" type="text/css" href="../css/jquery.ui.theme.css"/>
	<link rel="stylesheet" type="text/css" href="../css/event_canvas.css" />
	
	<style>
		#lnb-list {
			height:900px;
		}
	</style>
	<script type="text/javascript" src="../js/jquery-1.9.1.js"></script>
	<script type="text/javascript" src="../js/lnb.js"></script>
	<script type="text/javascript" src="../js/common_function.js"></script>
	<script type="text/javascript" src="../js/jquery-ui.js"></script>
	<script type="text/javascript" src="../js/jquery.ui.dialog.js"></script>
	<script type="text/javascript" src="../js/timeSchedule.js"></script>
	<script type="text/javascript" src="../js/eventcontrol.js"></script>
	<script type="text/javascript" language="javascript">
	<?php if (!$GLOBALS['M_SUPPORT_EVENT_TD']) { ?>
		document.location = "../../index.htm";
	<?php } ?>
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
	$(document).ready(function(){
		lnbonoff("lnb_event");
	});
	
	function OnClickApply()
	{
		if (CheckScheduleSetting("<?php echo $event_name; ?>") == 0) {
			alert("<?php echo $msg_checkthetable[$GLOBALS['LANGINDEX']]; ?>");
			return; 
		}
			
		var msg = '';
		msg += "<SetOpenSDKConfiguration>";
		msg += "<Enabled>"+($("#event_<?php echo $event_name; ?>_use_on").is(':checked') ? 1 : 0 )+"</Enabled>";
		<?php if($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>	
		msg += MakeScheduleAndActionSetupXML_S1("<?php echo $event_name; ?>");
		<?php } else { ?>
		msg += MakeScheduleAndActionSetupXML("<?php echo $event_name; ?>");
		<?php } ?>	
		msg += "</SetOpenSDKConfiguration>";
		RequestAjaxMsg(msg, "<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $GLOBALS['REQUEST_URI'].'?seq='.$_SESSION['count'] ?>");
	}

	function OnLoad() {}

		</script>
	</head>
	<body onload="OnLoad()" onselectstart="return false">
		<div id="wrap">
		<?php
			require_once ('left_menu.cgi');
			require_once ('top_menu.cgi');
		?>
		<div id="container" <?php if($GLOBALS['M_SUPPORT_EVENT_VA'] & IV_SUPPORT) echo "style='width:1400px;'"; ?> >
		<?php
			PrintLeftMenu($_SERVER['SCRIPT_NAME']);
		?>
			<div id="contents"  style="width:680px;">				
				<div class="h3_tit mgt0">
					<h3 class="wid320"><?php echo $menu_appevent[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>
				<table class="data_write" >
					<colgroup>
						<col style="width:190px;"/>
						<col />
					</colgroup>
					<tbody>
						<tr>
							<th scope="row"><?php echo $t_enable[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<label><input type="radio" name="event_<?php echo $event_name; ?>_use" id="event_<?php echo $event_name; ?>_use_on"  <?php if ($event_class->dataInfo['Enabled']['value'] == 1) echo "checked=\"checked\""; ?> style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_on[$GLOBALS['LANGINDEX']]; ?></label>
								<label><input type="radio" name="event_<?php echo $event_name; ?>_use" id="event_<?php echo $event_name; ?>_use_off" <?php if ($event_class->dataInfo['Enabled']['value'] == 0) echo "checked=\"checked\""; ?> /><?php echo $t_off[$GLOBALS['LANGINDEX']]; ?></label>
							</td>
						</tr>
						
					</tbody>
				</table>
				<?php
					require_once ('eventsetup_ui.cgi');
				?>
				<div class="btn_right">
					<a id="mid_ok_btn" class="btn_apply" href="javascript:OnClickApply()"><?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?></a>
				</div>
			</div>
		</div>
	</body>
</html>

