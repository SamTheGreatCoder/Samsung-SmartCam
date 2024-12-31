<?php
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_menu.cgi');
require_once ('../language/language_tooltip.cgi');

if (isset($_REQUEST['message'])) {
	require_once ('../../cgi-bin/adv/log.class');
	$socketManager = new SocketManager();
	$logSearchConf = new LogSearchRequest();
	$logSearchConf->SetHeaderCommand(CMD_LOG_SEARCH);
	$logSearchConf->XMLtoArray('Log', $_REQUEST['message']);
	$socketManager->Connection($logSearchConf);

	$logSearchConf->SetHeaderCommand(CMD_LOG_SEARCH_DETAIL);
	$logSearchConf->XMLtoArray('Log', $_REQUEST['message']);
	$socketManager->Connection($logSearchConf);

	header('Content-Type: text/xml; charset=utf-8');
	echo $logSearchConf->GetXMLData();
	exit;
}
require_once ('../language/language_system_log.cgi');
$classInstances= GetClassInstance();
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="kr" xml:lang="kr">
<head>
	<title>iPOLiS NETWORK CAMERA WEBVIEWER</title>
	<meta http-equiv="X-UA-Compatible" content="IE=Edge; requiresActiveX=true">
	<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
	<link rel="stylesheet" type="text/css" href="../css/techwin.css" />
	<link rel="stylesheet" type="text/css" href="../css/jquery.ui.theme.css"/>
	<script type="text/javascript" src="../js/jquery-1.9.1.js"></script>
	<script type="text/javascript" src="../js/jquery-ui.js"></script>
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
	$(document).ready(function(){ 
		lnbonoff('lnb_system'); 
		$(document).tooltip({
			open: function (event, ui) {
				setTimeout(function () {
					$(ui.tooltip).hide();
				}, 4000);
			}
		});
	});

	var logList = new Array();
	var logResultCount;
	var logTotalCount;
	var logPageNo = 1;
	var totalPageNo = 1;


	var ALL_SYS_LOG = 0;
	var SYS_POWON = 1;
	var SYS_POWREBOOT = 2;
	var SYS_NETWORK = 3;
   var SYS_TIMECHANGE = 4;
   var CONFIG_CHANGED = 5;
	var SYS_BACKUP = 6;
	var SYS_RECORD = 7;
   var SYS_SDFORMAT = 8;
   var SYS_SDERR = 9;
	var SYS_SDFULL = 10;
	var SYS_SDINSERT = 11;
	var SYS_SDREMOVE = 12;
	var SYS_FWUPDATE = 13;
	var SYS_FACRESET = 14;
	var SYS_CONFIGBACKUP = 15;
	var SYS_CONFIGRESTORE = 16;
	var SYS_NASFORMAT = 17;
   var SYS_NASERR = 18;
	var SYS_NASFULL = 19;
	var SYS_NASCONNECT = 20;
	var SYS_NASDISCONNECT = 21;
	var oldSelNo = 1;
	var timer;

	function SearchLog()
	{
		var msg = "<GetLogtSearch>";
		msg += "<Cat1>"+$('#log_type option:selected').val()+"</Cat1>";
		msg += "<Cat2>"+$('#log_detail_type option:selected').val()+"</Cat2>";
		msg += "<Direction>"+logPageNo+"</Direction>";
		msg += "</GetLogtSearch>";

		var reqUrl = "<?php echo GetMyRequestURI($_SERVER['SCRIPT_NAME']); ?>";
		if (BrowserDetect.browser == "Explorer" || (BrowserDetect.browser == 'Safari' && reqUrl.search('.local') != -1)) {
			reqUrl = ".."+reqUrl.substr(reqUrl.indexOf("/setup/"));
		}

		var response = $.ajax({
			type: "POST",
			async: false,
			cache: false,
			url: reqUrl,
			dataType: "xml",
			data: "message="+encodeURIComponent(msg)
			//success: OnSuccessSearchLog
			//error: OnError
		}).responseText.replace(/&/gm, '&amp;');

		if (response == '') {
			SearchLog();
			return;
		}
		
		var xmlData = createXMLFromString(response);
		OnSuccessSearchLog(xmlData);
	}

	function createXMLFromString(string) {
		var xmlDocument;
		var xmlParser;
		if(window.ActiveXObject){	 //IE
			xmlDocument = new ActiveXObject('Microsoft.XMLDOM');
			xmlDocument.async = false;
			xmlDocument.loadXML(string);
		} else if (window.XMLHttpRequest) {   //Firefox, Netscape
			xmlParser = new DOMParser();
			xmlDocument = xmlParser.parseFromString(string, 'text/xml');
		} else {
			return null;
		}
		return xmlDocument;
	}

	function OnSuccessSearchLog(xmlData)
	{
      totalPageNo = parseInt($(xmlData).find("LogTotalCount").text());
      logResultCount = parseInt($(xmlData).find("LogResultCount").text());
      if (totalPageNo == 0) totalPageNo = 1;
 		for (var index=0; index<logResultCount; ++index) {
			$(xmlData).find("Result"+index).each(function() {
				logList[index] = {};
				logList[index].description = "";
				logList[index].cat1 = parseInt($(this).find("Cat1").text());
				logList[index].cat2 = parseInt($(this).find("Cat2").text());
				logList[index].cat3 = parseInt($(this).find("Cat3").text());
				logList[index].description = decodeURIComponent($(this).find("Description").text());
				$(this).find("Time").each(function() {
					logList[index].year = $(this).find("Year").text();
					logList[index].month = $(this).find("Month").text();
					logList[index].day = $(this).find("Day").text();
					logList[index].hour = $(this).find("Hour").text();
					logList[index].min = $(this).find("Min").text();
					logList[index].sec = $(this).find("Sec").text();
				});
			});
 		}
 		
		DrawLogTable();
	}

	function DrawLogTable()
	{
		var timeMsg = "";

		for(var i=0; i<15; i++){
			$('#log_info_no_'+(i+1)).text("");
			$('#log_info_time_'+(i+1)).text("");
			$('#log_info_desc_'+(i+1)).text("");
			$('#log_info_detail_'+(i+1)).text("");
		}

		/////////////////////////////// SYSTEM LOG
		var basicState 	= ["On", "Off"];
		var networkState 	= ["Logical State On", "Logical State Off", "Physical State On", "Physical State Off"];
		var timeState 		= ["Manual", "NTP", "PC Sync"];
		var loginState 	= ["Success", "Failed"];
		var recordState 	= ["On", "Off", "Change"];
		var updateState		= ["", "", "", "", "", "", "", "", "", "", "Micom Programming Success", "Micom Prepare Error", "Micom Program Error", "Micom Verify Error"];
		var configState 	= [/*0*/"Profile",
									/*1*/ "Video",
									/*2*/ "Audio",
									/*3*/ "Network Interface",
									/*4*/ "Network Port",
									/*5*/ "DDNS",
									/*6*/ "IP Filtering",
									/*7*/ "SSL",
									/*8*/ "FTP",
									/*9*/ "SMTP",
									/*10*/ "Record",
									/*11*/ "Alarm Input", // Sensor->Alarm Input
									/*12*/"Motion Detection", // iv
									/*13*/"Time Schedule",
									/*14*/ "Product Info",
									/*15*/ "Time",
									/*16*/ "User",
									/*17*/ "OSD",
									/*18*/ "802.1x",
									<?php if($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ && $GLOBALS['M_SUPPORT_PTZ'] == PTZ_SUPPORT) { ?>
									/*19*/ "RS485/422",
									<?php } else { ?>
									/*19*/ "RS485",
									<?php } ?>
									/*20*/ "Network Disconnect",
									/*21*/ "QoS",
									/*22*/ "SNMP",
									/*23*/ "Continuous Recording",
									/*24*/ "Face Detection",
									/*25*/ "Preset",
									/*26*/ "Tampering Detection",
									/*27*/ "NAS",
									/*28*/ "Audio Detection",
									/*29*/ "Alarm Output",
									/*30*/ "Smart Codec",
									/*31*/ "Link-Local IPv4 address",
									/*32*/ "UPnP",
									/*33*/ "Bonjour",
									/*34*/ "FishEye",
									/*35*/ "ONVIF",
									/*36*/ "Auto Tracking",
									/*37*/ "Preset VA",
									/*38*/ "PTZ Limit",
									/*39*/ "PTZ Swing",
									/*40*/ "PTZ Group",
									/*41*/ "PTZ Tour",
									/*42*/ "Tracking event",
									/*43*/ "PTZ Autorun",
									/*44*/ "Preset OSD",
									/*45*/ "PTZ HomePosition",
									/*46*/ "App Event",
									/*47*/ "iSCSI",
									<?php if ($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>
									/*48*/ "PTZ Azimuth Position",
									/*49*/ "SMS"];
									<?php } else { ?>
									/*48*/ "PTZ Azimuth Position"];
									<?php } ?>

		var systemLogList = [	/*0*/"All",
									/*1*/"Power On",
									/*2*/"Power Reboot",
									/*3*/"Network",
									/*4*/"Time Change",
									/*5*/"Config Change",
									/*6*/"Backup",
									/*7*/"Record",
									/*8*/"SD Format",
									/*9*/"SD Error",
									/*10*/"SD Full",
									/*11*/"SD Insert",
									/*12*/"SD Remove",
									/*13*/"Firmware Update",
									/*14*/"Factory Reset",
									/*15*/"Configuration Backup",
									/*16*/"Configuration Restore",
									/*17*/"NAS Format",
									/*18*/"NAS Error",
									/*19*/"NAS Full",
									/*20*/"NAS Connect",
									/*21*/"NAS Disconnect",
									/*22*/"iSCSI Format",
									/*23*/"iSCSI Error",
									/*24*/"iSCSI Full",
									/*25*/"iSCSI Connect",
									/*26*/"iSCSI Disconnect"];

		var systemLogTable = {"Power On":"",
									"Power Reboot":"",
									"All":"",
									"Network":networkState,
									"Time Change":timeState,
									"Config Change":configState,
									"Backup":"",
									"Record":recordState,
									"SD Format":loginState,
									"SD Error":"",
									"SD Full":"",
									"SD Insert":"",
									"SD Remove":"",
									"Firmware Update":updateState,
									"Factory Reset":"",
									"Configuration Backup":"",
									"Configuration Restore":"",
									"NAS Format":loginState,
									"NAS Error":"",
									"NAS Full":"",
									"NAS Connect":"",
									"NAS Disconnect":"",
									"iSCSI Format":loginState,
									"iSCSI Error":"",
									"iSCSI Full":"",
									"iSCSI Connect":"",
									"iSCSI Disconnect":""};

		/////////////////////////////// EVENT LOG
		var startState 	= ["Start", "End"];
		var sensorState 	= ["Close", "Open", "On", "Off"];
		var vaState 		= ["Pass", "Enter/Exit", "Appear/Disappear", "Scene Change",  "Start", "End"];
		var opensdkState	= ["Install", "Uninstall", "Start", "Stop"];
		var ptzjogState		= ["On", "Off", "Error"];
		var eventLogList	= [/*0*/"All",
									/*1*/"Alarm Input",
									/*2*/"Alarm Output",
									/*3*/"Video Analysis",
									/*4*/"Admin Login",
									/*5*/"Admin Logout",
									/*6*/"User Login",
								 	/*7*/"User Logout",
								 	/*8*/"Guest Login",
								 	/*9*/"Guest Logout",
								 	/*10*/"Motion Detection",
								 	/*11*/"Goto Preset",
								 	/*12*/"AUX",
									/*13*/"Network Disconnect",
									/*14*/"Face Detection",
									/*15*/"Tampering Detection",
									/*16*/"Audio Detection",
									/*17*/"Open SDK",
									/*18*/"Auto Tracking",
									/*19*/"PTZ Jog Move",
									/*20*/"Manual Recording"];

		var eventLogTable = {"Alarm Input":sensorState,
									"Alarm Output":sensorState,
									"Motion Detection":basicState,
									"Admin Login":loginState,
									"Admin Logout":"",
									"User Login":loginState,
									"User Logout":"",
									"Guest Login":loginState,
									"Guest Logout":"",
									"Video Analytics":startState,
									"Goto Preset":basicState,
									"AUX":sensorState,
									"Network Disconnect":basicState,
									"Face Detection":startState,
									"Tampering Detection":"",
									"Audio Detection":vaState,
									"Open SDK":opensdkState,
									"Auto Tracking":basicState,
									"PTZ Jog Move":ptzjogState,
									"Manual Recording":startState};

		var logName="", logState="", stateVal="";
		
		for (var i=0; i<logResultCount; ++i) {
			if (logList[i].cat1 == 0) {		// SYSTEM LOG
				logName = systemLogList[logList[i].cat2];
				logState = systemLogTable[logName];
				stateVal = "";
				if (logName == 'All' && logState == "") continue;
				if (logState != "" && logState[logList[i].cat3] != "") stateVal = " : "+logState[logList[i].cat3];
				if (logList[i].cat2 == CONFIG_CHANGED && logList[i].cat3 == 12) {
				<?php
					if ($GLOBALS['M_SUPPORT_EVENT_VA'] & IV_SUPPORT) {
				?>
						stateVal = " : Video Analytics";
				<?php
					}
				?>
				}
			}
			else {		// EVENT LOG
				logName = eventLogList[logList[i].cat2];
				logState = eventLogTable[logName];
				stateVal = "";
				if (logList[i].cat2 == 3) {    //Video Analysis
				<?php
					if ($GLOBALS['M_SUPPORT_EVENT_VA'] == MD_SUPPORT) {
				?>
						logName = "Motion Detection";						
						stateVal = " : "+vaState[logList[i].cat3];
				<?php
					}
					else {
				?>
						logName = "Video Analytics";
						vaState = ["Pass", "Enter/Exit", "Appear/Disappear", "Scene Change",  "Motion Detection Start", "Motion Detection End"];
						stateVal = " : "+vaState[logList[i].cat3];
				<?php
					}
				?>
				}
				else if (logList[i].cat2 == 2) {    //Alarm Output
					if (logState != "") stateVal = " : "+logState[logList[i].cat3 - 2];
				}
				else if (logList[i].cat2 == 17) {    //OpenSDK
					if (opensdkState != "") stateVal = " : "+opensdkState[logList[i].cat3];
				}
				else if (logList[i].cat2 == 19) {    //PTZ Jog Move
					if (ptzjogState != "") stateVal = " : "+ptzjogState[logList[i].cat3];
				}
				else {
					if (logState != "") stateVal = " : "+logState[logList[i].cat3];
				}
			}
			
			var logNo = ((i+1) < 10 ? '0'+(i+1) : (i+1));
			$('#log_info_no_'+(i+1)).text(logNo);
		 	$('#log_info_time_'+(i+1)).text(logList[i].year+"/"+logList[i].month+"/"+logList[i].day+"   "+logList[i].hour+":"+logList[i].min+":"+logList[i].sec);
		 	$('#log_info_desc_'+(i+1)).text(logName+stateVal);
		 	$('#log_info_detail_'+(i+1)).text(logList[i].description);
		  	$('#mid_desc_btn_'+(i+1)).attr('title', logList[i].description);
		}
		
		if(logResultCount < 15){
			for(var index=logResultCount; index<15; ++index){
				$('#log_info_no_'+(index+1)).text("");
				$('#log_info_time_'+(index+1)).text("");
				$('#log_info_desc_'+(index+1)).text("");
				$('#log_info_detail_'+(index+1)).text("");
				$('#mid_desc_btn_'+(index+1)).removeAttr('title');
				$('#mid_desc_btn_'+(index+1)).html("");
			}
		}

		for(var index=0; index<logResultCount; ++index){
			if($('#mid_desc_btn_'+(index+1)).html() == ""){
				$('#mid_desc_btn_'+(index+1)).append("<img src=\"../images/common/icon/log_tooltip.png\"/>");	
			}
		}
		$('#log_page_total').text(' / '+ totalPageNo);
	}

	function OnClickDescription(selNo)
	{
		return;
		if (selNo > logResultCount) return;
		$('.log_description_'+oldSelNo).hide();		
		$('.log_description_'+selNo).show();
		oldSelNo = selNo;
	}

	function ChangeMoveBtnStatus()
	{
		if (parseInt(logPageNo) == 1) {
			$('#mid_first_btn').attr('disabled', 'disabled');
			$('#mid_prev_btn').attr('disabled', 'disabled');
			$('#mid_next_btn').removeAttr('disabled');
			$('#mid_last_btn').removeAttr('disabled');
		}
		else if (parseInt(logPageNo) == parseInt(totalPageNo)) {
			$('#mid_first_btn').removeAttr('disabled');
			$('#mid_prev_btn').removeAttr('disabled');
			$('#mid_next_btn').attr('disabled', 'disabled');
			$('#mid_last_btn').attr('disabled', 'disabled');
		}
		else {
			$('#mid_first_btn').removeAttr('disabled');
			$('#mid_prev_btn').removeAttr('disabled');
			$('#mid_next_btn').removeAttr('disabled');
			$('#mid_last_btn').removeAttr('disabled');
		}
	}

	function ChangeCurrPage(mode)
	{
		if((mode != 'First' && mode != 'Last') && $('#log_page_no').val() == '' ) return;
		if(isNaN($('#log_page_no').val())) {
			alert("<?php echo $msg_invalidValue[$GLOBALS['LANGINDEX']]; ?>");
			$('#log_page_no').val("");
			return;
		}
		
		if 		(mode == "First") 	logPageNo = 1;
		else if 	(mode == "Prev")	logPageNo -= 1;
		else if 	(mode == "Next") 	logPageNo += 1;
		else if 	(mode == "Last") 	logPageNo = parseInt(totalPageNo)	;
		else 		logPageNo = parseInt($('#log_page_no').val(),10);

		if (logPageNo > parseInt(totalPageNo))	logPageNo = parseInt(totalPageNo)	;
		else if (logPageNo < 1)			logPageNo = 1;

		$('#log_page_no').val(logPageNo);
		$('.log_description_'+oldSelNo).hide();
		
		SearchLog();
		ChangeMoveBtnStatus();
	}

	function OnChangeLogType()
	{
		$('#log_detail_type').find('option[value!="0"]').remove();
		if (parseInt($('#log_type option:selected').val()) == 1) {		// EVENT LOG
		<?php
			$optionHtml = '';
			$eventLogList = array(/*0*/'All',
										/*1*/'Alarm Input',
										/*2*/'Alarm Output',
										/*3*/'Motion Detection',
										/*4*/'Admin Login',
										/*5*/'Admin Logout',
										/*6*/'User Login',
										/*7*/'User Logout',
										/*8*/'Guest Login',
										/*9*/'Guest Logout',
										/*10*/'Video Analytics',
										/*11*/'Goto Preset',
										/*12*/'AUX',
										/*13*/'Network Disconnect',
										/*14*/'Face Detection',
										/*15*/'Tampering Detection',
										/*16*/'Audio Detection',
										/*17*/'Open SDK',
										/*18*/'Auto Tracking',
										/*19*/'PTZ Jog Move',
										/*20*/'Manual Recording');
			for($index=1; $index<count($eventLogList); ++$index) {
				$event = $eventLogList[$index];
				if ($GLOBALS['M_ALARMIN_COUNT'] == 0			&& $event == 'Alarm Input') 			continue;
				if (!$GLOBALS['M_SUPPORT_EVENT_ND'] 			&& $event == 'Network Disconnect') 	continue;
				if (!$GLOBALS['M_SUPPORT_EVENT_FD']			&& $event == 'Face Detection') 		continue;
				if (!$GLOBALS['M_SUPPORT_EVENT_TD'] 			&& $event == 'Tampering Detection') continue;
				if (!$GLOBALS['M_SUPPORT_EVENT_AD'] 			&& $event == 'Audio Detection') 		continue;
				if (!$GLOBALS['M_AUX_COUNT']					&& $event == 'AUX') 						continue;
				if ($event == 'Video Analytics') 		continue;
				if (($GLOBALS['M_SUPPORT_EVENT_VA'] & IV_SUPPORT) && $event == 'Motion Detection') $eventLogList[$index] = 'Video Analytics';
				if (($GLOBALS['M_ALARMIN_COUNT'] == 0 	|| $GLOBALS['M_ALARMOUT_COUNT'] == 0	) && $event == 'Alarm Output') continue;
				if ($GLOBALS['M_PRESET_COUNT'] == 0 			&& $event == 'Goto Preset') 	continue;
				if (!$GLOBALS['M_SUPPORT_PTZ_TRACKING']		&& $event == 'Auto Tracking') continue;
				if (!$GLOBALS['M_SUPPORT_PTZ']		&& $event == 'PTZ Jog Move') continue;
				if ($GLOBALS['M_SUPPORT_LOCAL_RECORDING'] && $event == 'Manual Recording') continue;
				if (!$GLOBALS['M_SUPPORT_OPENSDK']		&& $event == 'Open SDK') continue;
		?>
				$('#log_detail_type').append("<option value='<?php echo $index; ?>'><?php echo $eventLogList[$index]; ?></option>");
		<?php
			}
		?>
		}
		else {			// SYSTEM LOG
		<?php
			$optionHtml = '';
			$systemLogList = array(/*0*/'All',
										  /*1*/'Power On',
										  /*2*/'Power Reboot',
										  /*3*/'Network',
										  /*4*/'Time Change',
										  /*5*/'Config Change',
										  /*6*/'Backup',
										  /*7*/'Record',
										  /*8*/'SD Format',
										  /*9*/'SD Error',
										  /*10*/'SD Full',
										  /*11*/'SD Insert',
										  /*12*/'SD Remove',
										  /*13*/'Firmware Update',
										  /*14*/'Factory Reset',
										  /*15*/'Configuration Backup',
										  /*16*/'Configuration Restore',
										  /*17*/'NAS Format',
										  /*18*/'NAS Error',
										  /*19*/'NAS Full',
										  /*20*/'NAS Connect',
										  /*21*/'NAS Disconnect',
										  /*22*/'iSCSI Format',
										  /*23*/'iSCSI Error',
										  /*24*/'iSCSI Full',
										  /*25*/'iSCSI Connect',
										  /*26*/'iSCSI Disconnect');
			for($index=1; $index<count($systemLogList); ++$index) {
				if (!($GLOBALS['M_SUPPORT_SD'] || $GLOBALS['M_SUPPORT_NAS']) && (strpos($systemLogList[$index], 'SD') !== false || strpos($systemLogList[$index], 'NAS') !== false || $systemLogList[$index] == 'Backup' || $systemLogList[$index] == 'Record')) 			continue;
				if (!$GLOBALS['M_SUPPORT_SD']	&& strpos($systemLogList[$index], 'SD') !== false)		continue;
				if (!$GLOBALS['M_SUPPORT_NAS'] && strpos($systemLogList[$index], 'NAS') !== false) 	continue; // disable NAS
				if (!$GLOBALS['M_SUPPORT_ISCSI'] && strpos($systemLogList[$index], 'iSCSI') !== false) 	continue; // disable iSCSI
				/* ***** [START] S1 model disalbe SD, Backup, Record, NAS **** */	
				if ($GLOBALS['M_SPECIAL_TYPE'] == 1 && strpos($systemLogList[$index], 'SD') !== false)	continue; 
				if ($GLOBALS['M_SPECIAL_TYPE'] == 1 && ($systemLogList[$index] == 'Backup')  !== false)	continue; 
				if ($GLOBALS['M_SPECIAL_TYPE'] == 1 && strpos($systemLogList[$index], 'Record') !== false)	continue; 
				if ($GLOBALS['M_SPECIAL_TYPE'] == 1 && strpos($systemLogList[$index], 'NAS') !== false)	continue; 
				/* ***** [END] S1 model disalbe SD, Backup, Record, NAS **** */	
		?>
				$('#log_detail_type').append("<option value='<?php echo $index; ?>'><?php echo $systemLogList[$index]; ?></option>");
	<?php
			}
	?>
		}
		ChangeCurrPage('First');
	}

	function OnLoad()
	{	
		logPageNo = 1;
		OnChangeLogType();
	}

	function OnClickLogBackup()
	{
		<?php if ($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>
			var reqUrl = "<?php echo GetMyRequestURIS1('/cgi-bin-stw/system.cgi'); ?>";
		<?php } else { ?>
			var reqUrl = "<?php echo GetMyRequestURI('/cgi-bin/system.cgi'); ?>";
		<?php } ?>
		//var reqUrl = "<?php echo GetMyRequestURI('/cgi-bin/system.cgi'); ?>";
		var logVal = parseInt($('#log_type option:selected').val());
		var logType;
		if (logVal == 0) logType = 'system';
		else if (logVal == 1) logType = 'event';
		$('#type').val(logType);
		$.ajax({
			type: "GET",
			async: false,
			cache: false,
			data:"msubmenu=log&type="+logType+"&detail=All&action=view&log_backup=1",
			dataType: "text",
			url: reqUrl,
			success: OnSuccess,
			error: OnSuccess
		});
		
	}

	function OnSuccess(req)
	{	
		var model = "<?php echo $_SERVER['MODELNAME']; ?>";
		$('#log').val(req);
		$('#time').val(new Date().getTime());
		$('#model').val(model);
		window.document.contact.submit();
	}
 
		</script>
		<style>
			.ui-tooltip { padding:8px;max-width:260px; z-index:9999; background: #ffffff; word-break:break-all; }
			.ui-tooltip-content {width: 260px; word-break:break-all;}
		</style>
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
					<h3 class="wid220"><?php echo $menu_log[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>
				<table class="data_write">
					<colgroup>
						<col style="width:180px;" />
						<col style="width:180px;" />
						<col />
					</colgroup>
					<tbody>						
						<tr>
							<th scope="row"><?php echo $t_logType[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<select name="select" id="log_type" style="width:170px; height:22px; background-color:#868fa3; color:#1c1c1c;" onchange="OnChangeLogType();">
						         <option value="0" selected="selected"><?php echo $left_system[$GLOBALS['LANGINDEX']]; ?></option>
									<option value="1"><?php echo $left_event[$GLOBALS['LANGINDEX']]; ?></option>
								</select>
							</td>
							<td>
								<?php if ($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>
									<form name="contact" method="post" action="<?php echo GetMyRequestURIS1('/home/setup/download.cgi'); ?>"> 
								<?php } else { ?>
									<form name="contact" method="post" action="<?php echo GetMyRequestURI('/home/setup/download.cgi'); ?>"> 
								<?php } ?>
								<input id="log" type="hidden" name="log" value=""> 
								<input id="model" type="hidden" name="model" value="">
								<input id="time" type="hidden" name="time" value="">
								<input id="type" type="hidden" name="type" value=""> 
								<a id="backup_button" style="float:left;margin-left:10px" class="btn_type01 btn_type01_11" href="javascript:OnClickLogBackup();" > <?php echo $btn_backup[$GLOBALS['LANGINDEX']]; ?> </a>
								</form>	
							</td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_detailLogtype[$GLOBALS['LANGINDEX']]; ?></th>
							<td colspan=2>
								<select id="log_detail_type" style="width:170px; height:22px; background-color:#868fa3; color:#1c1c1c;" onchange="ChangeCurrPage('First')">
									<option value="0">All</option>
								</select>
							</td>
						</tr>
					</tbody>
				</table>
				<table id="LogTable" class="time_table time_table_type2 mgt10" style="clear:both;">
					<colgroup>
						<col style="width:40px;" />
						<col style="width:200px;"/>
						<col style="width:360px;"/>
						<col style="width:100px;" />
					</colgroup>
					<thead>
						<tr>
							<th class="first"></th>
							<th scope="col" class="first" style="font-weight:bold; font-size:12px"><?php echo $t_datetime[$GLOBALS['LANGINDEX']];?></th>
							<th scope="col" class="first" style="font-weight:bold; font-size:12px"><?php echo $t_description[$GLOBALS['LANGINDEX']];?></th>
							<th scope="col" class="last" style="font-weight:bold; font-size:12px"><?php echo $t_info[$GLOBALS['LANGINDEX']];?></th>
						</tr>
					</thead>
					<tbody>
				<?php
					for($index=1; $index<16; ++$index) {
				?>
						<tr>
							<td style="background:#8e939e; font-weight:bold"><span id="log_info_no_<?php echo $index; ?>" class="loglist_area" style="margin-left:12px"></span></td>
							<td><span id="log_info_time_<?php echo $index; ?>" class="loglist_area" style="margin-left:30px;"></span></td>
							<td><span id="log_info_desc_<?php echo $index; ?>" class="loglist_area" style="margin-left:5px"></span></td>
							<td class="last" style="background: #c3c8d3"><a id="mid_desc_btn_<?php echo $index; ?>" href="javascript:OnClickDescription('<?php echo $index; ?>')" ><img src="../images/common/icon/log_tooltip.png"/></a></td>
						</tr>
				<?php
					}
				?>
					</tbody>
				</table>
				<div class="paging2 mgt10">
					<a id="mid_first_btn" href="javascript:ChangeCurrPage('First')"><img src="../images/common/btn/btn_first.gif"/></a>
					<a id="mid_prev_btn" href="javascript:ChangeCurrPage('Prev')"><img src="../images/common/btn/btn_prev.gif"/></a>&nbsp;
					<input type="text" class="text" id="log_page_no" value="1" style="width:25px; height:20px; font-weight:bold; margin-top:-1px; text-align:center;" onkeypress="IsNum(event)" onkeydown="OnlyNUm(event);" maxlength="2"/><span style="text-valign:top; margin-left:-1px; margin-right:5px; width:10px; height:20px; font-size:120%; font-weight:bold" id="log_page_total"></span>
					<a id="mid_move_btn" href="javascript:ChangeCurrPage('')"><img src="../images/common/btn/log_01.png"/></a>
					<a id="mid_next_btn" href="javascript:ChangeCurrPage('Next')"><img src="../images/common/btn/btn_next.gif"/></a>
					<a id="mid_last_btn" href="javascript:ChangeCurrPage('Last')"><img src="../images/common/btn/btn_last.gif"/></a>
				</div>
				</div>
			</div>
		</div>
	</div>
</body>
</html>
