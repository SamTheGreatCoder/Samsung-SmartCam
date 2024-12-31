<?php
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_playback.cgi');
require_once ('../language/language_menu.cgi');
CheckAdminAccount();
$classInstances= GetClassInstance();
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" >
	<head>
		<title>iPOLiS NETWORK CAMERA WEBVIEWER</title>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		<link rel="stylesheet" type="text/css" href="../css/techwin.css" />
		<style type="text/css">
		    body {
			    padding: 0;
			    margin: 0;
		    }
    	</style>
    	<script type="text/javascript" src="../js/jquery-1.10.0.min.js"></script>
 		<script type="text/javascript" src="../js/jquery.fileDownload.js"></script>
    	<script type="text/javascript" src="../js/common_function.js"></script>    	
		<script type="text/javascript" src="../js/pluginCheck.js"></script>
		<script type="text/javascript" src="../js/pluginControl.js"></script>
    	<script type="text/javascript">
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

		var limitHour = 0;
		var limitMin = 0;
		var limitSec = 0;
		var isCheckLimit = 0;
		
		var encName 				= "<?php echo $GLOBALS['USERINFO']['encname']; ?>";
		var encPW					= "<?php echo $GLOBALS['USERINFO']['encpw']; ?>";
		var installMsg 			= new Array();
		installMsg[0]				= "<?php echo $msg_plugin_install[$GLOBALS['LANGINDEX']]; ?>";
		installMsg[1]				= "<?php echo $msg_plugin_install2[$GLOBALS['LANGINDEX']]; ?>";
		installMsg[2]				= "<?php echo $msg_notsupport_plugin[$GLOBALS['LANGINDEX']]; ?>";

		function OnLoadSD()
		{
			var control = document.getElementById("SDBackup");
			control.content.SDBackupControl.SetBackupMode(1);
			//RequestTime();
			SetDate();

			<?php if($_REQUEST['starthour'] >= 0) { ?>
			SetTime();
			<?php } ?>

			<?php if($_REQUEST['starthour'] == -1) { ?>
			SetEndTimeLimit();
			<?php } ?>
			
		}

		function SetDate()
		{
			var year = <?php echo $_REQUEST['year']; ?>;
			var month = <?php echo $_REQUEST['month']; ?>;
			var day = <?php echo $_REQUEST['day']; ?>;

			$("#from_year").val(year);
			$("#from_month").val(month);
			$("#from_day").val(day);
			$("#to_year").val(year);
			$("#to_month").val(month);
			$("#to_day").val(day);

			$("#from_year").attr('disabled', 'disabled');
			$("#from_month").attr('disabled', 'disabled');
			$("#from_day").attr('disabled', 'disabled');
			$("#to_year").attr('disabled', 'disabled');
			$("#to_month").attr('disabled', 'disabled');
			$("#to_day").attr('disabled', 'disabled');
		}

		function SetTime()
		{
		  var starthour = <?php echo $_REQUEST['starthour']; ?>;
		  var startmin = <?php echo $_REQUEST['startmin']; ?>;
		  var startsec = <?php echo $_REQUEST['startsec']; ?>;
		  var endhour = <?php echo $_REQUEST['endhour']; ?>;
		  var endmin = <?php echo $_REQUEST['endmin']; ?>;
		  var endsec = <?php echo $_REQUEST['endsec']; ?>;
		  var dbindex = <?php echo $_REQUEST['dbindex']; ?>;

		  $("#from_hour").val(starthour);
			$("#from_min").val(startmin);
			$("#from_sec").val(startsec);
			$("#to_hour").val(endhour);
			$("#to_min").val(endmin);
			$("#to_sec").val(endsec);

			var timeDiff = Math.abs((endhour * 60 * 60 + endmin * 60 + endsec) - (starthour * 60 * 60 + startmin * 60 + startsec));

			if (timeDiff < 5 * 60) {
				$("#from_hour").attr('disabled', 'disabled');
				$("#from_min").attr('disabled', 'disabled');
				$("#from_sec").attr('disabled', 'disabled');
				$("#to_hour").attr('disabled', 'disabled');
				$("#to_min").attr('disabled', 'disabled');
				$("#to_sec").attr('disabled', 'disabled');
			}

			//var control = document.getElementById("SDBackup");
			//control.content.SDBackupControl.SetDBIndex(dbindex);
		}

		function CheckTime()
		{
			  var starthour = parseInt($("#from_hour").val(),10);
			  var startmin = parseInt($("#from_min").val(),10);
			  var startsec = parseInt($("#from_sec").val(),10);
			  var endhour = parseInt($("#to_hour").val(),10);
			  var endmin = parseInt($("#to_min").val(),10);
			  var endsec = parseInt($("#to_sec").val(),10);

			  var timeDiff = (endhour * 60 * 60 + endmin * 60 + endsec) - (starthour * 60 * 60 + startmin * 60 + startsec);

			  if (timeDiff > 5 * 60)
			  {
				 return -1;
			  }
			  else if (timeDiff < 0) {
			     return -2;
			  }
			  else if (timeDiff == 0) {
				 return 0;
			  }

			  return 1;

		}

		function SetEndTimeLimit()
		{
			isCheckLimit = 1;
			limitHour = <?php echo $_REQUEST['endhour']; ?>;
			limitMin = <?php echo $_REQUEST['endmin']; ?>;
			limitSec = <?php echo $_REQUEST['endsec']; ?>;
		}


		function OpenSDWaitWindow()
		{
			var msg = "<div id='SDWaitInfo' style='padding:10px;font-size: 14px;font-family: Verdana, sans-serif;position:relative; left:0px; top:0px; width:100%; height:100%; z-index:12000; background-color: #181e28;color:#BFC0C2;'>";
			msg += "<p align='center'><?php echo $msg_sdWait[$GLOBALS['LANGINDEX']];?><br /><br /><img src='../images/common/download.gif' /></p>";
			msg += "</div>";
			$("#BackupWaitPaneltxt").html(msg);
			$("#backup_box").hide();
		}

		function CloseSDWaitWindow()
		{
			$("#BackupWaitPaneltxt").html("");
			$("#backup_box").show();
		}
		
	function OnLoad()
	{
		// draw plugin area
		SISOPlugin.init(installMsg, 0, 0);
		SISOPlugin.setSecurityEnhancement();

		SetDate();

		<?php if($_REQUEST['starthour'] >= 0) { ?>
		SetTime();
		<?php } ?>

		<?php if($_REQUEST['starthour'] == -1) { ?>
		SetEndTimeLimit();
		<?php } ?>
	}


  function OnClickBackup()
  {
	    if (CheckTime() == 0) {
			alert("<?php echo $msg_From_To_Diff[$GLOBALS['LANGINDEX']]; ?>");
			return;
	    }
		else if (CheckTime() == -1) {
			alert("<?php echo $msg_no_more_than_5min[$GLOBALS['LANGINDEX']]; ?>");
			return;
	    }
		else if (CheckTime() == -2) {
			alert("<?php echo $msg_From_To_Late[$GLOBALS['LANGINDEX']]; ?>");
			return;
	    }

  		$("#infoMsg").css("visibility", "visible");
		OpenSDWaitWindow();

		var data = "<GetBackup><StartTime><Year>" + $("#from_year").val() + "</Year><Month>" + $("#from_month").val() + "</Month><Day>" + $("#from_day").val() + 
					"</Day><Hour>" + $("#from_hour").val() + "</Hour><Min>" + $("#from_min").val() + "</Min><Sec>" + $("#from_sec").val() + 
					"</Sec></StartTime><EndTime><Year>" + $("#to_year").val() + "</Year><Month>" + $("#to_month").val() + "</Month><Day>" + $("#to_day").val() +
					"</Day><Hour>" + $("#to_hour").val() + "</Hour><Min>" + $("#to_min").val() + "</Min><Sec>" + $("#to_sec").val() + 
					"</Sec></EndTime><DBIndex>" + <?php echo $_REQUEST['dbindex']; ?> +"</DBIndex></GetBackup> ";
					   
		var url;
		if (  window.location.protocol == 'https:' ) {
			url = "https://" + location.host;
		}
		else
		{
			url = "http://" + location.host;
		}
		var result = SISOPlugin.playbackBackup(url,encName,encPW,data);
		//CloseSDWaitWindow();

		if(result == 1)		// Success
		{	
			//alert('Saving Completed!');
		}
		else if(result != 0)
		{
			//alert("<?php echo $msg_downloadingFail[$GLOBALS['LANGINDEX']]; ?>");
		}
  }

  function DownloadStatus(status)
  {
	  if (status == "PASS") {
		  alert("<?php echo $msg_savingComplete[$GLOBALS['LANGINDEX']]; ?>");
		  CloseSDWaitWindow();
		  return 1;
	  }
	  else if (status == "CANCEL") {
		  CloseSDWaitWindow();
		  return 0;
	  }
	  else if (status == "CODEC") {
		  alert("<?php echo $msg_codecChange[$GLOBALS['LANGINDEX']]; ?>" + "\n" + "<?php echo $msg_savingComplete[$GLOBALS['LANGINDEX']]; ?>");
		  CloseSDWaitWindow();
		  return 1;
	  }
	  else {
		  alert("<?php echo $msg_downloadingFail[$GLOBALS['LANGINDEX']]; ?>");
		  CloseSDWaitWindow();
		  return 0;
	  }

  }
		


   		</script>
	</head>
	<body onselectstart="return false" ondragstart="return false" onload="OnLoad();">

	  <div id="wrap">
			<div id="head">
		<?php 
			
			if($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>
				<div class="head-top2">
				<h1><img src="../images/common/top_title_1.png" alt="S1" /></h1>
				<div class="logo"></div>
			<?php } 
				else { 
			?>
			<div class="head-top">

				<h1><img src="../images/common/top_title.gif" alt="iPOLiS NETWORK CAMERA WEBVIEWER" /></h1>
				<div class="logo"><img src="../images/common/top_logo.gif" alt="SAMSUNG TECHWIN" /></div>
			<?php } ?>
				</div>
			</div>

			<div id="contents" >
			    <div class="h3_tit mgt0" >
					<h3 class="wid220"><?php echo $t_backup[$GLOBALS['LANGINDEX']];?></h3>
				</div>
				<span id="BackupWaitPaneltxt">
			    </span>
				<div id="backup_box">
					<table class="data_write">
						<tr>
							<td><b><?php echo $t_from[$GLOBALS['LANGINDEX']];?></b></td>
							<td>
								<select id="from_year" class="selectbox_style_backup">
									<?php for ($i = 0; $i<=37; $i++) { ?>
										<option value ="<?php echo (2000+$i); ?>"><?php echo (2000+$i); ?></option>
									<?php } ?>
								</select><?php echo $t_year[$GLOBALS['LANGINDEX']];?>
							</td>
							<td>
								<select id="from_month" class="selectbox_style_backup">
									<?php for ($i = 1; $i<=12; $i++) { ?>
										<option value ="<?php echo ($i); ?>"><?php echo ($i); ?></option>
									<?php } ?>
								</select><?php echo $t_month[$GLOBALS['LANGINDEX']];?>
							</td>
							<td>
								<select id="from_day" class="selectbox_style_backup">
									<?php for ($i = 1; $i<=31; $i++) { ?>
										<option value ="<?php echo ($i); ?>"><?php echo ($i); ?></option>
									<?php } ?>
								</select><?php echo $t_day[$GLOBALS['LANGINDEX']];?>
							</td>
							<td>
								<select id="from_hour" class="selectbox_style_backup">
									<?php for ($i = 0; $i<=23; $i++) { ?>
										<option value ="<?php echo ($i); ?>"><?php echo ($i); ?></option>
									<?php } ?>
								</select><?php echo $t_hour[$GLOBALS['LANGINDEX']];?>
							</td>
							<td/>
								<select id="from_min" class="selectbox_style_backup">
									<?php for ($i = 0; $i<=59; $i++) { ?>
										<option value ="<?php echo ($i); ?>"><?php echo ($i); ?></option>
									<?php } ?>
								</select><?php echo $t_minute[$GLOBALS['LANGINDEX']];?>
							</td>
							<td>
								<select id="from_sec" class="selectbox_style_backup">
									<?php for ($i = 0; $i<=59; $i++) { ?>
										<option value ="<?php echo ($i); ?>"><?php echo ($i); ?></option>
									<?php } ?>
								</select><?php echo $t_sec[$GLOBALS['LANGINDEX']];?>
							</td>
						</tr>
						
						<tr>
							<td><b><?php echo $t_to[$GLOBALS['LANGINDEX']];?></b></td>
							<td>
								<select id="to_year" class="selectbox_style_backup">
									<?php for ($i = 0; $i<=37; $i++) { ?>
										<option value ="<?php echo (2000+$i); ?>"><?php echo (2000+$i); ?></option>
									<?php } ?>
								</select><?php echo $t_year[$GLOBALS['LANGINDEX']];?>
							</td>
							<td>
								<select id="to_month" class="selectbox_style_backup">
									<?php for ($i = 1; $i<=12; $i++) { ?>
										<option value ="<?php echo ($i); ?>"><?php echo ($i); ?></option>
									<?php } ?>
								</select><?php echo $t_month[$GLOBALS['LANGINDEX']];?>
							</td>
							<td>
								<select id="to_day" class="selectbox_style_backup">
									<?php for ($i = 1; $i<=31; $i++) { ?>
										<option value ="<?php echo ($i); ?>"><?php echo ($i); ?></option>
									<?php } ?>
								</select><?php echo $t_day[$GLOBALS['LANGINDEX']];?>
							</td>
							<td>
								<select id="to_hour" class="selectbox_style_backup">
									<?php for ($i = 0; $i<=23; $i++) { ?>
										<option value ="<?php echo ($i); ?>"><?php echo ($i); ?></option>
									<?php } ?>
								</select><?php echo $t_hour[$GLOBALS['LANGINDEX']];?>
							</td>
							<td>
								<select id="to_min" class="selectbox_style_backup">
									<?php for ($i = 0; $i<=59; $i++) { ?>
										<option value ="<?php echo ($i); ?>"><?php echo ($i); ?></option>
									<?php } ?>
								</select><?php echo $t_minute[$GLOBALS['LANGINDEX']];?>
							</td>
							<td>
								<select id="to_sec" class="selectbox_style_backup">
									<?php for ($i = 0; $i<=59; $i++) { ?>
										<option value ="<?php echo ($i); ?>"><?php echo ($i); ?></option>
									<?php } ?>
								</select><?php echo $t_sec[$GLOBALS['LANGINDEX']];?>
							</td>
							<td style="text-align:center;">
								<a href="javascript:OnClickBackup();" class="btn_type01 btn_type01_03"><img src="../images/common/btn/btn_cd.png" alt="" /></a>
							</td>
						</tr>
					</table>
				</div>

			</div>

		</div>
		<span id="pluginArea" style="width:0;height:0;"></span>
	</body>
</html>
