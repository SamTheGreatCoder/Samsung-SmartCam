<?php
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_menu.cgi');
require_once ('../language/language_system_datetime.cgi');
require_once ('../../cgi-bin/adv/datetime.class');

if (isset($_REQUEST['action']) && $_REQUEST['action'] == 'TimeServer') {
	$socketManager = new SocketManager();
	$datetimeConf = $socketManager->Connection(new DateTimeConfiguration());
	$localTime  = $datetimeConf->localDateTime->dataInfo['Year']['value'].'-';
	$localTime .= $datetimeConf->localDateTime->dataInfo['Month']['value'].'-';
	$localTime .= $datetimeConf->localDateTime->dataInfo['Day']['value'].'#';
	$localTime .= $datetimeConf->localDateTime->dataInfo['Hour']['value'].':';
	$localTime .= $datetimeConf->localDateTime->dataInfo['Min']['value'].':';
	$localTime .= $datetimeConf->localDateTime->dataInfo['Sec']['value'].':';
	$localTime .= $datetimeConf->milliSecond;
	echo $localTime;
	unset($socketManager);
	exit;
}

$classInstances= GetClassInstance('datetime');
$ntpConf 		= $classInstances['NTPConfiguration'];
$datetimeConf 	= $classInstances['DateTimeConfiguration'];

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
	$(document).ready(function(){ lnbonoff("lnb_basic"); });

	var localSeq				= <?php echo $_SESSION['count']; ?>;
	var ajaxReqUrl				= "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq;

	var gSysTime		= null;
	var gTimer			= null;
	var timezoneInfo 	= new Array();
	var requestTime1	= 0;
	var requestTime2	= 0;
	var diffMilliSecTime = 0;

	<?php
		for ($index=0; $index<count($timezoneList); ++$index) {
	?>
			timezoneInfo[<?php echo $index; ?>] = {};
			timezoneInfo[<?php echo $index; ?>].sMonth		= "<?php echo $timezoneList[$index][1]; ?>";
			timezoneInfo[<?php echo $index; ?>].sWeek 		= "<?php echo $timezoneList[$index][2]; ?>";
			timezoneInfo[<?php echo $index; ?>].sDay		= "<?php echo $timezoneList[$index][3]; ?>";
			timezoneInfo[<?php echo $index; ?>].sHour 		= "<?php echo $timezoneList[$index][4]; ?>";
			timezoneInfo[<?php echo $index; ?>].sMin		= "<?php echo $timezoneList[$index][5]; ?>";
			timezoneInfo[<?php echo $index; ?>].sSec		= "<?php echo $timezoneList[$index][6]; ?>";
			timezoneInfo[<?php echo $index; ?>].eMonth		= "<?php echo $timezoneList[$index][7]; ?>";
			timezoneInfo[<?php echo $index; ?>].eWeek 		= "<?php echo $timezoneList[$index][8]; ?>";
			timezoneInfo[<?php echo $index; ?>].eDay		= "<?php echo $timezoneList[$index][9]; ?>";
			timezoneInfo[<?php echo $index; ?>].eHour 		= "<?php echo $timezoneList[$index][10]; ?>";
			timezoneInfo[<?php echo $index; ?>].eMin		= "<?php echo $timezoneList[$index][11]; ?>";
			timezoneInfo[<?php echo $index; ?>].eSec		= "<?php echo $timezoneList[$index][12]; ?>";
	<?php
		}
	?>

	function OnClickTimeZoneApply()
	{
		var msg = "";
		msg += "<SetDateTime>";
		msg += "<DaylightSavings>"+($('#datetime_dst_use').is(':checked')?1:0)+"</DaylightSavings>";
		msg += "<CurrTimezoneIdx>"+$('#datetime_dst_timezone').val()+"</CurrTimezoneIdx>";
		msg += "</SetDateTime>";

		var reqUrl = "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq;
		if (BrowserDetect.browser == "Explorer" || (BrowserDetect.browser == 'Safari' && reqUrl.search('.local') != -1)) {
			reqUrl = "../.."+reqUrl.substr(reqUrl.indexOf("/cgi"));
		}

		$.ajax({
			type: "POST",
			async: false,
			cache: false,
			url: reqUrl,
			dataType: "text",
			data: encodeURI(msg),
			success: OnSuccessTimeApply
		});
		localSeq++;
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

	function OnClickApply()
	{
		var today, lastDay, timeSelect = 0;
		var year, month, day, hour, minute, sec, msec = 0;
		var msg = "";
                var msg1 = "";		
		var tzIndex	= parseInt($('#datetime_dst_timezone').val());

		if ($('#datetime_sync_ntp_use').is(':checked')) {
			for (var index=1; index<6; ++index) {
				if (CheckAddrKorean($('#datetime_ntp_server'+index).val())) {
					alert("<?php echo $msg_invalid_address[$GLOBALS['LANGINDEX']]; ?>");
					return;
				}
			}
		}

		if ($('#datetime_sync_ntp_use').is(':checked')) timeSelect = 1;
		else if ($('#datetime_sync_pc_use').is(':checked')) timeSelect = 2;

		if (timeSelect == 0) {
			lastDay = GetLastday($('#datetime_manual_year').val(), $('#datetime_manual_month').val());
			if ($('#datetime_manual_day').val() > lastDay) {
				alert("<?php echo $msg_invalid_day[$GLOBALS['LANGINDEX']]; ?>");
				return;
			}
			year	= $('#datetime_manual_year').val();
			month = $('#datetime_manual_month').val();
			day	= $('#datetime_manual_day').val();
			hour	= $('#datetime_manual_hour').val();
			minute= $('#datetime_manual_min').val();
			sec	= $('#datetime_manual_sec').val();
		}
		else if (timeSelect == 2) {		// pc sync
			today = new Date();
			if (today.getYear() > 2037) {
				alert("<?php echo $msg_invalid_year[$GLOBALS['LANGINDEX']]; ?>");
				$('#datetime_sync_pc_use').attr('disabled', 'disabled');
				return;
			}
			var tempTime = today.getTime()+diffMilliSecTime;
			tempTime = new Date(tempTime);
			year	= tempTime.getUTCFullYear();
			month = tempTime.getUTCMonth() + 1;
			day	= tempTime.getUTCDate();
			hour	= tempTime.getUTCHours();
			minute= tempTime.getUTCMinutes();
			sec	= tempTime.getUTCSeconds();
			msec	= tempTime.getUTCMilliseconds();
		}

		msg += "<SetDateTime>";
		msg += "<Type>"+timeSelect+"</Type>";
		
		if (timezoneInfo[tzIndex].sMonth == "invalid") {
			msg += "<DaylightSavings>"+$('#datetime_dst_use').val(0)+"</DaylightSavings>";
		} else {
			msg += "<DaylightSavings>"+($('#datetime_dst_use').is(':checked')?1:0)+"</DaylightSavings>";
		}
		if (timeSelect != 1)
		{
			msg += "<DateTime>";
			msg += "<Year>"+year+"</Year>";
			msg += "<Month>"+month+"</Month>";
			msg += "<Day>"+day+"</Day>";
			msg += "<Hour>"+hour+"</Hour>";
			msg += "<Min>"+minute+"</Min>";
			msg += "<Sec>"+sec+"</Sec>";
			msg += "</DateTime>";
			msg += "<MilliSecond>"+parseInt(msec)+"</MilliSecond>";
		}
		msg += "<CurrTimezoneIdx>"+$('#datetime_dst_timezone').val()+"</CurrTimezoneIdx>";
		msg += "</SetDateTime>";

		var reqUrl = "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq;
		if (BrowserDetect.browser == "Explorer" || (BrowserDetect.browser == 'Safari' && reqUrl.search('.local') != -1)) {
			reqUrl = "../.."+reqUrl.substr(reqUrl.indexOf("/cgi"));
		}

		/*$.ajax({
			type: "POST",
			async: false,
			cache: false,
			url: reqUrl,
			dataType: "text",
			data: encodeURI(msg)
		});*/
		localSeq++;

		//msg = "";
		var ntpAddr="";
		var ntpAddrCheck = 0;
		var ntpDeleteSupport = "<?php echo $GLOBALS['M_SUPPORT_DELETE_NTP_LIST']; ?>";

		for (var index=1; index<6; ++index) {
			ntpAddr = $('#datetime_ntp_server'+index).val();
			if (ntpDeleteSupport ==0 || ntpAddr.length >0) {
			ntpAddrCheck ++;
			if(ntpAddr == ''){
				alert("<?php echo $msg_invalid_address[$GLOBALS['LANGINDEX']]; ?>");
				return;
			}
			if (CheckSpace(ntpAddr)) {
				alert("<?php echo $msg_invalid_address[$GLOBALS['LANGINDEX']]; ?>");
				return;
			}
			if(ntpAddr.search(':') != -1){
				if(!CheckValidIPv6Address(ntpAddr)){
					alert("<?php echo $msg_invalid_address[$GLOBALS['LANGINDEX']]; ?>");
					return;
				}
			}
			else{
				if(TypeCheck(ntpAddr.charAt(0), NUM)){
					if(!CheckValidIPv4Address(ntpAddr)){	
						alert("<?php echo $msg_invalid_address[$GLOBALS['LANGINDEX']]; ?>");
						return;
					}
					else{
						var str = ntpAddr.split('.');
						if(str[str.length-1] > 254){
							alert("<?php echo $msg_invalid_address[$GLOBALS['LANGINDEX']]; ?>");
							return;
						}
					}
				}
				else{
					if(!(TypeCheck(ntpAddr, ALPHA+NUM+'.'+'-') && TypeCheck(ntpAddr.charAt(0), ALPHA) && ntpAddr.charAt(ntpAddr.length-1) != '.')){
						alert("<?php echo $msg_invalid_address[$GLOBALS['LANGINDEX']]; ?>");
						return;
					}
				}
			}
		}
			msg1 += "<Address>"+$('#datetime_ntp_server'+index).val()+"</Address>";
		
		}

		if (timeSelect == 1 && ntpAddrCheck == 0) {
			alert("<?php echo $msg_invalid_address[$GLOBALS['LANGINDEX']]; ?>");
			return;
		}
		
		$.ajax({
			type: "POST",
			async: false,
			cache: false,
			url: reqUrl,
			dataType: "text",
			data: encodeURI("<SetNTP><Manual>"+msg1+"</Manual></SetNTP>")
			//success: OnSuccessTimeApply
		});

                $.ajax({
                        type: "POST",
                        async: false,
                        cache: false,
                        url: reqUrl,
                        dataType: "text",
                        data: encodeURI(msg),
                        success: OnSuccessTimeApply
                });

		localSeq++;
	}

	function OnSuccessTimeApply(req)
	{
		alert("<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>");
		clearTimeout(gTimer);
		RequestTime();
	}

	function GetLastday(year, month)
	{
		var last_month = new Array(31,  28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31);
		if (((year%4 == 0) && (year%100 != 0)) || (year%400 == 0)) last_month[1] = 29;
		else last_month[1] = 28;
		return last_month[month-1];
	}

	function MakeDate(dateVal)
	{
		var month = dateVal.getMonth()+1;
		var dateResult = dateVal.getFullYear();
		dateResult += ((month < 10)? "-0":"-") + month ;
		dateResult += ((dateVal.getDate() < 10)? "-0":"-") + dateVal.getDate();
		return dateResult;
	}

	function MakeTime(timeVal)
	{
		var hours = timeVal.getHours();
		var minutes = timeVal.getMinutes();
		var seconds = timeVal.getSeconds();
		timeResult = ((hours < 10)? "0":"") + hours ;
		timeResult += ((minutes < 10)? ":0":":") + minutes;
		timeResult += ((seconds < 10)? ":0":":") + seconds;
		return timeResult;
	}

	function ShowClock(today)
	{
		if (today.getFullYear() < 2000 || today.getFullYear() > 2037) {
			if ($('#datetime_sync_pc_use').is(':disabled') == false) {
				$('#datetime_sync_pc_use').attr('disabled', 'disabled');
				$('#datetime_sync_manual_use').removeAttr('disabled');
				$('#datetime_sync_manual_use').prop('checked', true);
				OnClickSyncType();
				return false;
			}
		}
		else {
			$('#datetime_sync_pc_use').removeAttr('disabled');
		}
		$('#datetime_pc_datetime').val(MakeDate(today)+" "+MakeTime(today));
		return true;
	}

	function DispalyCurrentTime()
	{
		var today = new Date();
		var isAlreadyShowedOvertimeErr = false;

		if (today.getFullYear() < 2000 || today.getFullYear() > 2037) {
			if ($('#datetime_sync_pc_use').is(':disabled') == false){
				isAlreadyShowedOvertimeErr = true;
				alert("<?php echo $msg_overtime[$GLOBALS['LANGINDEX']]; ?>");
			}
		}

		if (ShowClock(today)) {
			$('#datetime_current_datetime').val(MakeDate(gSysTime)+" "+MakeTime(gSysTime));
		}

		if (gSysTime.getFullYear() < 2000 || gSysTime.getFullYear() > 2037) {
			if (isAlreadyShowedOvertimeErr == false) {
				alert("<?php echo $msg_overtime[$GLOBALS['LANGINDEX']]; ?>");
			}
			InitStore();
		}

		if (gSysTime.getSeconds() == 59) {
			// TODO: HOW to LAST TIME HANDLING
			if (gSysTime.getFullYear() == 2037 && gSysTime.getMonth() == 11 && gSysTime.getDate() == 31 && gSysTime.getHours() == 23 && gSysTime.getMinutes() == 59) {
				if (isAlreadyShowedOvertimeErr == false) {
					alert("<?php echo $msg_overtime[$GLOBALS['LANGINDEX']]; ?>");
				}
				InitStore();
			}
			else {
				RequestTime();
			}
		}
		else {
			var oldTime = gSysTime.getFullYear();
			gSysTime 	= new Date(gSysTime.getFullYear(), gSysTime.getMonth(), gSysTime.getDate(), gSysTime.getHours(), gSysTime.getMinutes(), gSysTime.getSeconds()+1);
			// don't delete this code (because PC timezone)
			var newTime = gSysTime.getFullYear();
			gTimer		= setTimeout(DispalyCurrentTime, 1000);
		}
	}

	function InitStore()
	{
		var msg = "<SetDateTime><Type>0</Type><DateTime><Year>2000</Year><Month>1</Month><Day>1</Day><Hour>0</Hour><Min>0</Min><Sec>0</Sec></DateTime></SetDateTime>";
		RequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, 'InitDateTime');
		localSeq++;
	}

	function OnSuccessInitStore(req)
	{
		window.location.reload(true);
	}

	function RequestTime()
	{
		var now			= new Date();
		var timezone	= now.getTimezoneOffset();
		requestTime1	= now.getTime();

		var reqUrl = "<?php echo GetMyRequestURI($_SERVER['SCRIPT_NAME']); ?>";
		if (BrowserDetect.browser == "Explorer" || (BrowserDetect.browser == 'Safari' && reqUrl.search('.local') != -1)) {
			reqUrl = ".."+reqUrl.substr(reqUrl.indexOf("/setup/"));
		}

		$.ajax({
			type: "GET",
			async: true,
			cache: false,
			dataType: "text",
			url: reqUrl,
			data: "action=TimeServer&pctz="+now.getTimezoneOffset(),
			success: OnSuccessRequestTime,
			error: OnErrorRequestTime
		});
	}

	function OnSuccessRequestTime(req)
	{
		var today			= new Date();
		requestTime2		= today.getTime();
		var time 			= req.split('#');
		var datePattern	= /(\d*)\-(\d*)\-(\d*)/;
		var dateData		= time[0].match(datePattern);
		var timePattern	= /(\d*)\:(\d*)\:(\d*)\:(\d*)/;
		var timeData		= time[1].match(timePattern);
		if (timeData[3] == 59) {
			RequestTime();
			return false;
		}
		gSysTime 			= new Date(dateData[1], dateData[2]-1, dateData[3], timeData[1], timeData[2], timeData[3]);
		diffMilliSecTime	= parseInt((requestTime2-requestTime1)/2);
		var tempSysTime	= parseInt(new Date(dateData[1], dateData[2]-1, dateData[3], timeData[1], timeData[2], timeData[3]).getTime())+parseInt(timeData[4])+diffMilliSecTime+100;
		gSysTime 			= new Date(tempSysTime);
		diffHour 			= today.getHours() - gSysTime.getHours();
		DispalyCurrentTime();
	}

	function OnErrorRequestTime(req)
	{
		var today = new Date();
		ShowClock(today);
		gTimer = setTimeout(DispalyCurrentTime, 1000);
	}

	function OnClickSyncType()
	{
		var manual_name = ['year', 'month', 'day', 'hour', 'min', 'sec'];

		if ($('#datetime_sync_manual_use').is(':checked')) {
			for(var index=1; index<6; ++index) {
				$('#datetime_ntp_server'+index).attr('disabled', 'disabled');				
			}
			for(var index=0; index<6; ++index) {
				$('#datetime_manual_'+manual_name[index]).removeAttr('disabled');				
				$('#datetime_manual_'+manual_name[index]).css('color', '#1c1c1c')
			}
		}
		else if ($('#datetime_sync_ntp_use').is(':checked')) {
			for(var index=1; index<6; ++index) {
				$('#datetime_ntp_server'+index).removeAttr('disabled');
			}
			for(var index=0; index<6; ++index) {
				$('#datetime_manual_'+manual_name[index]).attr('disabled', 'disabled');				
				$('#datetime_manual_'+manual_name[index]).css('color', '#6d6d6d')
			}
		}
		else if ($('#datetime_sync_pc_use').is(':checked')) {
			for(var index=1; index<6; ++index) {
				$('#datetime_ntp_server'+index).attr('disabled', 'disabled');				
			}
			for(var index=0; index<6; ++index) {
				$('#datetime_manual_'+manual_name[index]).attr('disabled', 'disabled');				
					$('#datetime_manual_'+manual_name[index]).css('color', '#6d6d6d')
			}
		}
	}

	function OnChangeTimezone()
	{
		var tzIndex		= parseInt($('#datetime_dst_timezone').val());
		var monthArr	= new Array("", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December");
		var weekArr 	= new Array("", "1st", "2nd", "3rd", "4th", "last");
		var dayArr		= new Array("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat");
		
		if (timezoneInfo[tzIndex].sMonth == "invalid") {
			$('.datetime_dst_area').hide();
		}
		else {
			$('.datetime_dst_area').show();
		
			var DSTStartMonth = monthArr[timezoneInfo[tzIndex].sMonth];
			var DSTStartWeek	= weekArr[timezoneInfo[tzIndex].sWeek];
			var DSTStartDay	= dayArr[timezoneInfo[tzIndex].sDay];
			var DSTStartHour	= (timezoneInfo[tzIndex].sHour < 10)	? "0"+timezoneInfo[tzIndex].sHour	: timezoneInfo[tzIndex].sHour;
			var DSTStartMin	= (timezoneInfo[tzIndex].sMin < 10)	? "0"+timezoneInfo[tzIndex].sMin	: timezoneInfo[tzIndex].sMin;
			var DSTStartSec	= (timezoneInfo[tzIndex].sSec < 10)	? "0"+timezoneInfo[tzIndex].sSec	: timezoneInfo[tzIndex].sSec;

			var DSTEndMonth	= monthArr[timezoneInfo[tzIndex].eMonth];
			var DSTEndWeek 	= weekArr[timezoneInfo[tzIndex].eWeek];
			var DSTEndDay		= dayArr[timezoneInfo[tzIndex].eDay];
			var DSTEndHour 	= (timezoneInfo[tzIndex].eHour < 10)	? "0"+timezoneInfo[tzIndex].eHour	: timezoneInfo[tzIndex].eHour;
			var DSTEndMin		= (timezoneInfo[tzIndex].eMin < 10)	? "0"+timezoneInfo[tzIndex].eMin 	: timezoneInfo[tzIndex].eMin;
			var DSTEndSec		= (timezoneInfo[tzIndex].eSec < 10)	? "0"+timezoneInfo[tzIndex].eSec 	: timezoneInfo[tzIndex].eSec;

			$('#datetime_dst_stime').val(DSTStartMonth	 + "-" + DSTStartWeek + "-" + DSTStartDay	+ " " + DSTStartHour + ":" + DSTStartMin	+ ":" + DSTStartSec);
			$('#datetime_dst_etime').val(DSTEndMonth + "-" + DSTEndWeek	+ "-" + DSTEndDay 	+ " " + DSTEndHour	+ ":" + DSTEndMin 	+ ":" + DSTEndSec);
		}
	}

	function OnLoad()
	{
		RequestTime();
		OnChangeTimezone();
		OnClickSyncType();
	}

	function OnClickClearBtn()
	{
		for(var index=1; index<6; ++index) {
			$('#datetime_ntp_server'+index).val("");				
		}
		
	}

		</script>
	</head>
	<body onload="OnLoad()" onselectstart="return false">
		<div id="wrap" >
			<div id="head">
			<?php
				require_once ('left_menu.cgi');
				require_once ('top_menu.cgi');
			?>
			<div id="container">
			<?php
				PrintLeftMenu($_SERVER['SCRIPT_NAME']);
			?>
			<div id="contents">
				<div class="h3_tit mgt0">
					<h3 class="wid280"><?php echo $t_currentSystemTime[$GLOBALS['LANGINDEX']];?></h3>
				</div>
				<table class="data_write">
					<colgroup>
						<col style="width:<?php if(GetBrowserName()=='IE' && ieversion() < 8) {echo '210';}else {echo'200';}?>px;" />
						<col />
					</colgroup>
					<tbody>
						<tr>	
							<th scope="row"><?php echo $t_datetime[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<label>
									<input type="text" id="datetime_current_datetime" class="text" style="width:191px;" disabled="disabled" />
								</label>
							</td>
						</tr>
					</tbody>
				</table>

				<div class="h3_tit">
					<h3 class="wid220"><?php echo $t_timezone[$GLOBALS['LANGINDEX']];?></h3>
				</div>
				<table class="data_write">
					<colgroup>
						<col style="width:<?php if(GetBrowserName()=='IE' && ieversion() < 8) {echo '210';}else {echo'200';}?>px;"/>
						<col />
					</colgroup>
					<tbody>
						<tr>
							<th scope="row"><?php echo $t_timezone[$GLOBALS['LANGINDEX']];?></th>
							<td>
								<select name="select" id="datetime_dst_timezone" style="width:<?php if(GetBrowserName()=='IE' && ieversion() < 8) {echo '450';}else {echo'470';}?>px; height:22px; background-color:#868fa3; color:#1c1c1c;" onKeyDown="window.setTimeout(function(e0){return function() {OnChangeTimezone(e0)}}(),0)" onChange="OnChangeTimezone()">
							<?php
								for ($index=0; $index<count($timezoneList); ++$index) {
							?>
									<option value="<?php echo $index; ?>" <?php if ($index == $datetimeConf->currTimezoneIdx) echo "selected=\"selected\""; ?>>
							<?php
									echo $timezoneList[$index][0];
								}
							?>
									</option>
								</select>
							</td>
						</tr>
						<tr height="10px"></tr>
						<tr class="datetime_dst_area">
							<td colspan="2">
								<label>
									<input type="checkbox" id="datetime_dst_use" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} ?>px;" <?php if($datetimeConf->dataInfo['DaylightSavings']['value'] == 1) echo 'checked=\'checked\''; ?> /><?php echo $t_dstUse[$GLOBALS['LANGINDEX']]; ?>
								</label>
							</td>
						</tr>
						<tr class="datetime_dst_area">
							<th scope="row"><?php echo $t_startTime[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<input type="text" id="datetime_dst_stime" class="text" style="width:191px;" disabled="disabled" />
							</td>
						</tr>
						<tr class="datetime_dst_area">
							<th scope="row"><?php echo $t_endTime[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<input type="text" id="datetime_dst_etime" class="text" style="width:191px;" disabled="disabled" />
							</td>
						</tr>
						<script>
							var tindex = parseInt(<?php echo $datetimeConf->currTimezoneIdx; ?>);
							if (timezoneInfo[tindex].sMonth == 'invalid')
								$('.datetime_dst_area').hide();
						</script>

					</tbody>
				</table>
				<div class="btn_right mgt30">
					<a id="mid_ok_btn" class="btn_apply" href="javascript:OnClickTimeZoneApply()"><?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?></a>
				</div>
				<div class="h3_tit">
					<h3 class="wid320"><?php echo $t_timeConf[$GLOBALS['LANGINDEX']];?></h3>
				</div>
				<table class="data_write">
					<colgroup>
						<col style="width:27px;" />
						<col style="width:<?php if(GetBrowserName()=='IE') {echo '171';}else {echo '170';}?>px;"/>
						<col />
					</colgroup>
					<tbody>
						<tr>
							<td colspan=3><label class="labelBold"><input type="radio" name="datetime_sync" id="datetime_sync_manual_use" <?php if($datetimeConf->dataInfo['Type']['value'] == 0) echo "checked=\"checked\""; ?> onClick="OnClickSyncType()"/><?php echo $t_timeManual[$GLOBALS['LANGINDEX']]; ?></label></td>
						</tr>
						<tr>
							<td></td>
							<td scope="row"><?php echo $t_datetime[$GLOBALS['LANGINDEX']]; ?></td>
							<td>
						<?php
							$datetimeInfo = array(	'Year'=>array('min'=>2000, 'max'=>2037), 'Month'=>array('min'=>1, 'max'=>12), 'Day'=>array('min'=>1, 'max'=>31),
															'Hour'=>array('min'=>0, 'max'=>23), 'Min'=>array('min'=>0, 'max'=>59), 'Sec'=>array('min'=>0, 'max'=>59));
							foreach($datetimeInfo as $item=>$info) {
						?>
								<select id="datetime_manual_<?php echo strtolower($item); ?>" style="width:60px; height:22px; background-color:#868fa3; color:#1c1c1c; margin-right:3px" <?php if($datetimeConf->dataInfo['Type']['value'] != 0) echo "disabled=\"disabled\""; ?>>
							<?php
								for ($index=$info['min']; $index<=$info['max']; ++$index) {
							?>
									<option value="<?php echo $index;?>" <?php if ($index == $datetimeConf->localDateTime->dataInfo[$item]['value']) echo "selected=\"selected\""; ?> >
								<?php
										if ($index<10) echo '0'.$index;
										else 				echo $index;
									}
								?>
									</option>
				         	</select>
						<?php
								if ($item=='Day') echo "&nbsp;&nbsp;";
							}
						?>
							</td>
						</tr>
						<tr>
							<td colspan=3><label class="labelBold"><input type="radio" name="datetime_sync" id="datetime_sync_ntp_use" <?php if($datetimeConf->dataInfo['Type']['value'] == 1) echo "checked=\"checked\""; ?> onClick="OnClickSyncType()"/><?php echo $t_timeServer[$GLOBALS['LANGINDEX']]; ?></label></td>
						</tr>
				<?php
					for($index=1; $index<6; ++$index) {
				?>
						<tr>
							<td></td>
							<td scope="row"><?php echo $t_timeSyncAddress[$GLOBALS['LANGINDEX']].$index; ?></td>
							<td>
								<input type="text" id="datetime_ntp_server<?php echo $index;?>" class="text" style="width:191px;" onkeypress='NoKorean(event)' onkeydown='NoKorean(event)' value ="<?php echo $ntpConf->ntpManual[$index-1]->dataInfo['Address']['value']; ?>" <?php if($datetimeConf->dataInfo['Type']['value'] != 1) echo "disabled=\"disabled\""; ?>/>
							</td>
						</tr>
				<?php
					}
				?>
				<?php
					if ($GLOBALS['M_SUPPORT_DELETE_NTP_LIST']) {
				?>
						<tr>
							<td></td>
							<td scope="row"></td>
							<td>
								<a class="btn_type01" href="javascript:OnClickClearBtn();" id="roi_clear_btn"><?php echo $t_clear[$GLOBALS['LANGINDEX']]; ?></a>
							</td>
						</tr>
				<?php
					}
				?>		
						<tr>
							<td colspan=3><label class="labelBold"><input type="radio" name="datetime_sync" id="datetime_sync_pc_use" <?php if($datetimeConf->dataInfo['Type']['value'] == 2) echo "checked=\"checked\""; ?> onClick="OnClickSyncType()"/><?php echo $t_timeSyncPC[$GLOBALS['LANGINDEX']]; ?></label></td>
						</tr>
						<tr>
							<td></td>
							<td scope="row"><?php echo $t_datetime[$GLOBALS['LANGINDEX']]; ?></td>
							<td>
								<input type="text" id="datetime_pc_datetime" class="text" style="width:191px;" disabled="disabled"/>
							</td>
						</tr>
					</tbody>
				</table>
				<div class="btn_right mgt30">
					<a id="mid_ok_btn" class="btn_apply" href="javascript:OnClickApply()"><?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?></a>
				</div>
				</div>
			</div>
		</div>
	</div>
</body>
</html>

