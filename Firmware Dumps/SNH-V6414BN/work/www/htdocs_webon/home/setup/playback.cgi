<?php
require_once ('../../cgi-bin/adv/_define.inc');

if (isset($_REQUEST['message']))
{
	require_once ('../../cgi-bin/adv/search.class');
	$searchConf 	= new SearchRequest();
	$socketManager = new SocketManager();
	$searchConf->headerInfo['Command'] = CMD_RECORD_SEARCH;
	$searchConf->XMLtoArray($_REQUEST['message']);
	$socketManager->Connection($searchConf);
	$searchConf->headerInfo['Command'] = CMD_RECORD_SEARCH_DETAIL;
	$searchConf->XMLtoArray($_REQUEST['message']);
	$socketManager->Connection($searchConf);

	header('Content-Type: text/xml; charset=utf-8');
	echo $searchConf->GetXMLData();
	exit;
}
require_once ('../language/language_playback.cgi');
require_once ('../language/language_tooltip.cgi');
require_once ('../language/language_menu.cgi');
require_once ('../language/language_av_videoprofile.cgi');

$classInstances = GetClassInstance('');
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="kr" xml:lang="kr">
<head>
	<META HTTP-EQUIV="Pragma" CONTENT="no-cache">
	<META HTTP-EQUIV="Expires" CONTENT="-1">
	<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
	<meta http-equiv="X-UA-Compatible" content="IE=Edge; requiresActiveX=true">
	<title>iPOLiS NETWORK CAMERA WEBVIEWER</title>
	<link rel="stylesheet" type="text/css" href="../css/techwin.css" />
	<link rel="stylesheet" type="text/css" href="../css/jquery-ui.css" />
	<link rel="stylesheet" type="text/css" href="../css/jquery.ui.slider.css" />
	<link rel="stylesheet" type="text/css" href="../css/jquery.ui.datepicker.css" />

	<style type="text/css">
	div.gnb-tab {
		width: 560px;
	}
	a.pluginInstall:link, a.pluginInstall:visited, a.pluginInstall:focus, a.pluginInstall:hover, a.pluginInstall:active {
		color:#FFFFFF;
		text-decoration:underline;
		font-size:16px;
	}
	#container {
		overflow:hidden;
		width:2600px;
	}
	#lnb-list, #lnb-list-fold {
		height:1200px;
	}
	a:focus { outline: none; }
	.ui-slider .ui-slider-handle {
		margin-top: -.3em;
		z-index:1;
	}
	.ui-datepicker table {
		margin-top: .7em;
	}
	.ui-widget-content {
		color: #000000;
	}
	.ui-widget-content .ui-state-default, .ui-widget-header .ui-state-default {
		background: #7d8494;
		border: 1px solid #7d8494;
		color: #fff;
	}
	.ui-datepicker .ui-datepicker-prev span, .ui-datepicker .ui-datepicker-next span {
		margin-left: -6px;
		margin-top: -8px;
	}
	.ui-datepicker-current-day .ui-state-active{
		background: #2078da;
		border: 1px solid #2078da;
	}
	.ui-datepicker-today .ui-state-active{
		background: #2078da;
		border: 1px solid #2078da;
	}
	.ui-priority-secondary, .ui-widget-content .ui-priority-secondary, .ui-widget-header .ui-priority-secondary {
		opacity: 1;		
		filter:alpha(opacity=100);		
	}
	.ui-datepicker .ui-state-active .ui-state-highlight{background: #2078da; border: 1px solid #2078da;}

	.ui-datepicker-week-end, .ui-datepicker-week-end .ui-state-default {color:red;}

	th+th.ui-datepicker-week-end {
		color:#50a2ff;
	}
	td+td.ui-datepicker-week-end .ui-state-default {
		color:#50a2ff;
	}
	.ui-state-highlight, .ui-widget-content .ui-state-highlight, .ui-widget-header .ui-state-highlight { 
	//	border:1px solid #fcefa1;
	}
	.ui-datepicker tr td.eventDay.ui-datepicker-current-day {
		background: #DBEDF3;
	}
	.ui-datepicker-calendar .eventDay a.ui-state-default{
		background: #55DCD4;
		border: 1px solid #AAAAAA;
		color: #212121;
		font-weight: normal;
	}
	#Timesearch .ui-datepicker-calendar tr td {
		opacity: 1;
		filter:alpha(opacity=100);		
	}
	.ui-tooltip { padding-top:2px; padding-bottom:2px; padding-left:5px; padding-right:5px; width:auto; position:absolute; z-index:9999; background: #ffffff; color: black; border:0; }
	#pluginArea{
		display: block;
	   position: relative;
		min-height: 480px;
	}
	#ui-datepicker-div button.ui-datepicker-current {display: none;}
	</style>
	
	<script type="text/javascript" src="../js/jquery-1.9.1.js"></script>
	<script type="text/javascript" src="../js/jquery-ui.js"></script>
	<script type="text/javascript" src="../js/lnb_playback.js"></script>	
	<script type="text/javascript" src="../js/playback.js"></script>
	<script type="text/javascript" src="../js/common_function.js"></script>
	<script type="text/javascript" src="../js/fullscreenApi.js"></script>
	<script type="text/javascript" src="../js/jquery-datetimepicker.js"></script>

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
	$(function(){
		// Slider
		$(document).tooltip({
			open: function (event, ui) {
				setTimeout(function () {
					$(ui.tooltip).hide();
				}, 1000);
			}
		});
		$('#slider-vol').slider({
			orientation: "horizontal",
			value:3,
			min: 0,
			max: 5,
			range: "min",
			slide: function( event, ui ) {
			SISOPlugin.SetVolume(ui.value);
			volumeVal = ui.value;
			}
		});

		//Datepicker
		$('#eventFrom').datetimepicker({
	      showOn: "both",
	      buttonImage: "../images/common/btn/btn_calender.png",
	      buttonImageOnly: true,
	      showButtonPanel: true,
	      buttonText: "",
	      changeMonth: true,
      	changeYear: true,
      	showOtherMonths: false,
      	selectOtherMonths: false,
      	yearRange: '2000:2037',
	      closeText: "<?php echo $t_ok[$GLOBALS['LANGINDEX']];?>",
			onSelect: function(dateText, inst) {
		   //	$('#eventTo').datepicker("option", "minDate", new Date(dateText));
			},
			dayNamesMin: ["<?php echo $t_sun_short[$GLOBALS['LANGINDEX']];?>","<?php echo $t_mon_short[$GLOBALS['LANGINDEX']];?>","<?php echo $t_tue_short[$GLOBALS['LANGINDEX']];?>","<?php echo $t_wed_short[$GLOBALS['LANGINDEX']];?>",
								"<?php echo $t_thu_short[$GLOBALS['LANGINDEX']];?>", "<?php echo $t_fri_short[$GLOBALS['LANGINDEX']];?>", "<?php echo $t_sat_short[$GLOBALS['LANGINDEX']];?>"],
			monthNamesShort: [1,2,3,4,5,6,7,8,9,10,11,12]
     	});
     	
     	$('#eventTo').datetimepicker({
	      showOn: "both",
	      buttonImage: "../images/common/btn/btn_calender.png",
	      buttonImageOnly: true,
	      showButtonPanel: true,
	      buttonText: "",
	      changeMonth: true,
      	changeYear: true,
			showOtherMonths: false,
			selectOtherMonths: false,
      	yearRange: '2000:2037',
	     	closeText: "<?php echo $t_ok[$GLOBALS['LANGINDEX']];?>",
	      onSelect: function() {
				$('#Timesearch').datepicker('destroy');	
	      },
		   dayNamesMin: ["<?php echo $t_sun_short[$GLOBALS['LANGINDEX']];?>","<?php echo $t_mon_short[$GLOBALS['LANGINDEX']];?>","<?php echo $t_tue_short[$GLOBALS['LANGINDEX']];?>","<?php echo $t_wed_short[$GLOBALS['LANGINDEX']];?>",
								"<?php echo $t_thu_short[$GLOBALS['LANGINDEX']];?>", "<?php echo $t_fri_short[$GLOBALS['LANGINDEX']];?>", "<?php echo $t_sat_short[$GLOBALS['LANGINDEX']];?>"],
			monthNamesShort: [1,2,3,4,5,6,7,8,9,10,11,12]
     	});
     
		$('#From img').mouseover(function(){
			$('#From .ui-datepicker-trigger').attr({src: '../images/common/btn/btn_calender_press.png'});
		}).mouseout(function(){
			$('#From .ui-datepicker-trigger').attr({src: '../images/common/btn/btn_calender.png'});
		});
		
		$('#To img').mouseover(function(){
			$('#To .ui-datepicker-trigger').attr({src: '../images/common/btn/btn_calender_press.png'});
		}).mouseout(function(){
			$('#To .ui-datepicker-trigger').attr({src: '../images/common/btn/btn_calender.png'});
		});


		$('#Timesearch').datepicker('destroy');	
		$('#lnb02').click(function(){
			$('#Timesearch').datepicker({
		      buttonImageOnly: false,
		      showButtonPanel: false,
		      buttonText: "",
		      changeMonth: true,
	      	changeYear: true,
				showOtherMonths: false,
				selectOtherMonths: false,
	      	yearRange: '2000:2037',
	      	defaultDate: new Date(cameraYear, cameraMonth-1, cameraDay),
				dayNamesMin: ["<?php echo $t_sun_short[$GLOBALS['LANGINDEX']];?>","<?php echo $t_mon_short[$GLOBALS['LANGINDEX']];?>","<?php echo $t_tue_short[$GLOBALS['LANGINDEX']];?>","<?php echo $t_wed_short[$GLOBALS['LANGINDEX']];?>",
									"<?php echo $t_thu_short[$GLOBALS['LANGINDEX']];?>", "<?php echo $t_fri_short[$GLOBALS['LANGINDEX']];?>", "<?php echo $t_sat_short[$GLOBALS['LANGINDEX']];?>"],
				monthNamesShort: [1,2,3,4,5,6,7,8,9,10,11,12],
				onSelect: function(selectedDate){	
					var datArr=selectedDate.split("/");
					SearchDay(parseInt(datArr[2], 10), parseInt(datArr[0], 10), parseInt(datArr[1], 10));
				},
				onChangeMonthYear: function(year, month, inst) 
				{ 	
					if(cameraYear!=parseInt(year) || cameraMonth!=parseInt(month))
					{
						cameraYear=parseInt(year); cameraMonth=parseInt(month);
						SearchCalendar(cameraYear, cameraMonth);
					}
				},
				beforeShowDay: function(eachDate) {				
					if (jQuery.inArray(parseInt(eachDate.getDate()), eventDays)>=0 && (eachDate.getMonth()+1)==cameraMonth &&  eachDate.getFullYear()==cameraYear) { 
						return [true, 'eventDay', ''];
					}
					else  return [false, '', ''];
				}
			});
			$('#Timesearch .ui-datepicker-calendar tbody .ui-datepicker-today a').removeClass('ui-state-active');
		});
			
		$('#lnb01').click(function(){
			$('#Timesearch').datepicker('destroy');
		});

		$( ".profileAccess" ).mouseup(function() {
     		window.open('../monitoring_info.cgi', 'popup', 'top=150, left=420, width=960, height=500, location=no, status=no, scrollbars=yes, resizable=no');
  		});
	});	
	</script>

	<script type="text/javascript">
	var SISOPlugin = null;
	var Startkey;
	var totalCount;
	var resultCount;
	var currPageNum = 1;
	var totalPageNum = 1;
	var currEventType = 0;
	var tempSuccess	= 0;
	var MAX_PLAYLIST 	= 10;
	var resultList 	= new Array();
	var invalidlist 	= new Array();
	var infoStatus = false;
	var isBackup = false;
	var eventSearchType;
	var startTime = new Array();
	var endTime = new Array();
	var cameraYear = 2000, cameraMonth = 1, cameraDay = 1;
	var isTimeRequestCompleted = 0;
	var isDaySelected = 0;
	var FullScreenStatus = 0;
	var OriginalStatus = 1;
	var FittStatus = 0;
	var viewportWidth, viewportHeight;
	var playSpeed = 1;
	var mode = 0; // 0 is event, 1 is time search...
	var searchYear, searchMonth, searchDayVal;
	var isEventSearchSuccess = 0, isDoneSpeedCtrl = 0;
	var isSnapshot = 0;
	var ListenStatus = 0;
	var waitLimit = 15000;
	var RewFFTimeoutValue = 0;
	var recordingEnable = <?php echo $classInstances['Information']->dataInfo['RecordingEnable']['value']; ?>;
  	var volumeVal = 3;
	var doit;
	var isShowing = 0;
	var defaultWidth = 800;
	var defaultHeight = 600;

  window.onkeydown = document.onkeydown = bodyOnkeydown;

	function bodyOnkeydown(event)
	{
		var event = event?event:window.event?window.event:null;
		if(event.keyCode==27 && FullScreenStatus == 1) {
			var ProfileStatus = $('#liveProfile').val();
			SISOPlugin.MakeBrowserFullScreen(0);
			FullScreenStatus = 0;
			OriginalStatus = 1;
			FittStatus = 0;
			SISOPlugin.SetResolution(defaultWidth, defaultHeight);
			document.getElementById('plugin').width = defaultWidth;
			document.getElementById('plugin').height = defaultHeight;
			$('#head').show();
			$('#lnb').show();
			if(mode != 0) {
				$('#timebarHtml').show();
			}
			document.getElementById('contents').style.padding = "20px 100px 20px 19px";
  			$("body").css("overflow","auto");
  			document.body.scroll = 'yes';
		}
		else if(event.keyCode == 9 && FullScreenStatus == 1)
		{
			return false;
		}
	}

	function DoChromeFullScreen()
	{
		SetViewportSize();
		SISOPlugin.SetResolution(viewportWidth, viewportHeight);
		document.getElementById('plugin').width = viewportWidth;
		document.getElementById('plugin').height = viewportHeight;
		document.getElementById('contents').style.padding = '0px';
		FullScreenStatus = 1;
	}

	var offset = $('#contents').offset();
	function OnFullScreenClick()
	{
		if(SeekStatus == 0) return;
		if(document.getElementById('plugin').width == 1) return;
		if(!(BrowserDetect.browser == "Explorer")) {
			window.scrollTo( 0, 0);
			if(FullScreenStatus == 0) {
				var element = $('#contents').get(0);

				if (fullScreenApi.supportsFullScreen) {
					fullScreenApi.requestFullScreen(element);

					element.addEventListener(fullScreenApi.fullScreenEventName, function() {
						if (fullScreenApi.isFullScreen()) {
							$('#head').hide();
							$('#lnb').hide();
							if(mode != 0) {
								$('#timebarHtml').hide();
							}
							window.setTimeout('DoChromeFullScreen()', 500);
						} else {
							$('#head').show();
							$('#lnb').show();
							FullScreenStatus = 0;
							OriginalStatus = 1;
							FittStatus = 0;
							SISOPlugin.SetResolution(defaultWidth, defaultHeight);
							document.getElementById('plugin').width = defaultWidth;
							document.getElementById('plugin').height = defaultHeight;
							document.getElementById('contents').style.padding = '20px';
							if(mode != 0) {
								$('#timebarHtml').show();
							}
						}
					}, true);
				}
			}
		}
		else {
			if(FullScreenStatus == 0) {
				SISOPlugin.MakeBrowserFullScreen(1);
				FullScreenStatus = 1;

				window.scrollTo( 0, 0);
				
				$("body").css("overflow","hidden");
				document.body.scroll = 'no';
  				SetViewportSize();

				//$('#contents').offset({top:0, left:0});
				document.getElementById('contents').style.padding = '0px';
				$('#head').hide();
				$('#lnb').hide();
				$('#timebarHtml').hide();

				document.getElementById('plugin').width = viewportWidth;
				document.getElementById('plugin').height = viewportHeight;
				SISOPlugin.SetResolution(viewportWidth, viewportHeight);
			}
		}
	}

	function SetViewportSize()
	{
		// the more standards compliant browsers (mozilla/netscape/opera/IE7) use window.innerWidth and window.innerHeight
		if (typeof window.innerWidth != 'undefined') {
			viewportWidth = window.innerWidth;
			viewportHeight = window.innerHeight;
		}
		// IE6 in standards compliant mode (i.e. with a valid doctype as the first line in the document)
		else if (typeof document.documentElement != 'undefined'
		&& typeof document.documentElement.clientWidth !=
		'undefined' && document.documentElement.clientWidth != 0) {
			viewportWidth = document.documentElement.clientWidth;
			viewportHeight = document.documentElement.clientHeight;
		}
		// older versions of IE
		else {
			viewportWidth = document.getElementsByTagName('body')[0].clientWidth;
			viewportHeight = document.getElementsByTagName('body')[0].clientHeight;
		}
	}

	function OnResizeEvent()
	{
		<?php	if (GetBrowserName() == 'Google Chrome') { ?>
		if (FullScreenStatus == 1) {
			window.setTimeout('DoChromeFullScreen()', 500);
		}
		<?php } ?>

		window.scrollTo( 20, 0);
		window.scrollTo( 0, 0);		
	}

	function OnLoad()
	{
		openlnbMenu(1);
		// draw plugin area
		var msg=""
		if(BrowserDetect.browser == "Explorer") { // activex
			msg += "<object id=\'plugin\' width=\"0\" height=\"0\"";
			msg += "classid=\"clsid:58930875-5F98-4151-B894-A7A3EA94ABC8\">";
			msg += "<a class='pluginInstall' href='../WebviewerInstaller.msi'>No Webviewer plugin. Click here to install.";
			msg += "<br />After installation process, please close all opened browser windows and open camera's web page again.</a>";
			msg += "</object>";
		} else { // npapi
			msg += "<object type=\"application/WebViewer-plugin\" width=\"0\" height=\"0\" id='plugin'>";
			msg += "<a class='pluginInstall' href='../WebviewerInstaller.msi'>No Webviewer plugin. Click here to install.";
			msg += "<br />After installation process, please close all opened browser windows and open camera's web page again.</a>";
			msg += "</object>";
			waitLimit = 20000;
		}
		$('#pluginArea').html(msg);

		// initialize plugin object instance
		try {
			SISOPlugin = document.getElementById("plugin");
		} catch (err) { alert(err); }

		RequestTime();
		//DrawToday();

		SISOPlugin.SetSecurityEnhancement();
		SISOPlugin.TimelineSearchStart(location.hostname, parseInt(<?php echo $classInstances['Information']->dataInfo['DevicePort']['value']; ?>), "<?php echo $GLOBALS['USERINFO']['encname']; ?>", "<?php echo $GLOBALS['USERINFO']['encpw']; ?>");

		window.onresize = function(event) {
			clearTimeout(doit);
			doit = window.setTimeout("OnResizeEvent()", 100);
		}
	}
	
	function DrawToday() {
		var date = new Date();
		var from = $.datepicker.formatDate('mm/dd/yy', new Date(date.getFullYear(), date.getMonth(), date.getDate()));
		from += " 00:00:00";
		$('#eventFrom').val(from);
		var to = $.datepicker.formatDate('mm/dd/yy', new Date(date.getFullYear(), date.getMonth(), date.getDate()));
		to += " 23:59:59";
		$('#eventTo').val(to);		
	}

	function OnUnload()
	{
		SISOPlugin.Stop();
 		SISOPlugin.TimelineSearchEnd();
		
		if(BrowserDetect.browser == "Explorer")
			SISOPlugin.Release();
	}

	function RequestTime()
	{
		var now			= new Date();

		// disable get PC time
		/*cameraYear = now.getFullYear();
		cameraMonth = now.getMonth() + 1;
		cameraDay = now.getDate();
		isTimeRequestCompleted = 1;*/

		// enable get camera time
		var timezone	= now.getTimezoneOffset();
		requestTime1	= now.getTime();

		var reqUrl = "<?php echo GetMyRequestURI('/home/setup/basic_datetime.cgi'); ?>";
		if (BrowserDetect.browser == "Explorer" || (BrowserDetect.browser == 'Safari' && reqUrl.search('.local') != -1)) {
			reqUrl = ".."+reqUrl.substr(reqUrl.indexOf("/setup/"));
		}

		$.ajax({
			type: "GET",
			async: false,
			cache: false,
			dataType: "text",
			url: reqUrl,
			data: "action=TimeServer&pctz="+now.getTimezoneOffset(),
			success: OnSuccessRequestTime,
			error: OnSuccessRequestTime
		});
	}

	function OnSuccessRequestTime(req)
	{
		var today 			= new Date();
		requestTime2		= today.getTime();
		var time 			= req.split('#');
		var datePattern 	= /(\d*)\-(\d*)\-(\d*)/;
		var dateData 		= time[0].match(datePattern);
		startYear = dateData[1];
		startMonth = dateData[2];
		startDay = dateData[3];

		if (startYear > 2037) // fix 2038.1 -> 2037.12
		{
			startYear = 2037;
			startMonth = 12;
		}

		cameraYear = startYear;
		cameraMonth = startMonth;
		cameraDay = startDay;

		isTimeRequestCompleted = 1;

		var from = $.datepicker.formatDate('mm/dd/yy', new Date(cameraYear, cameraMonth-1, cameraDay));
		from += " 00:00:00";
		$('#eventFrom').val(from);
		var to = $.datepicker.formatDate('mm/dd/yy', new Date(cameraYear, cameraMonth-1, cameraDay));
		to += " 23:59:59";
		$('#eventTo').val(to);
	}

	function PlayRecordedVideo()
	{
	//temp
		SISOPlugin.SetStartTime(100, 2, 16, 8, 13, 43, 0);
		SISOPlugin.SetEndTime(100, 2, 16, 8, 14, 14);
		SISOPlugin.PlayRecordedVideo(location.hostname, parseInt(<?php echo $classInstances['Information']->dataInfo['DevicePort']['value']; ?>), "<?php echo $GLOBALS['USERINFO']['encname']; ?>", "<?php echo $GLOBALS['USERINFO']['encpw']; ?>");
	}

	function StopRecordedVideo(isBackup)
	{
		if (typeof isBackup == 'undefined') {
			isBackup = 0;
		}

		if(isSnapshot == 1) return;

		SISOPlugin.SetResolution(1, 1);
		document.getElementById('plugin').width = 1;
		document.getElementById('plugin').height = 1;

		SeekStatus = 0;
		SISOPlugin.Stop();
		OriginalStatus = 1;
		FittStatus = 0;

		if(mode == 1) {
			$("#rewind_btn").html("<img src=\"../images/search/common/btn/02.jpg\" />");
			$("#stepbackward_btn").html("<a href=\"javascript:StepBackward()\"><img src=\"../images/search/common/btn/btn_stepbackward.jpg\" /></a>");
			$("#ff_btn").html("<img src=\"../images/search/common/btn/05.jpg\" />");
			$("#stepforward_btn").html("<a href=\"javascript:StepForward()\"><img src=\"../images/search/common/btn/btn_stepforward.jpg\" /></a>");

			playSpeed = 1;
			$('#speed_ff').html(playSpeed + "x");
			$('#speed_prev').html("<font color='#2A303C'>-1x</font>");
			isDoneSpeedCtrl = 0;

			$('#timebarHtml').show();
		}

		stopInterval();
			
		if (!isBackup) {
			$('#Timesearch .datetimepicker-hour').val("00");
			$('#Timesearch .datetimepicker-minuts').val("00");
			$('#Timesearch .datetimepicker-second').val("00");

			playback.timeline.moveTime(0,0,0);
		}
  }
  
	function OnClickStop()  // SEARCH_STOP
	{
		if(SeekStatus == 0) return;
		
		if (mode == 1) {
			$("#rewind_btn").html("<img src=\"../images/search/common/btn/02.jpg\" />");
			$("#stepbackward_btn").html("<a href=\"javascript:StepBackward()\"><img src=\"../images/search/common/btn/btn_stepbackward.jpg\" /></a>");
			$("#ff_btn").html("<img src=\"../images/search/common/btn/05.jpg\" />");
			$("#stepforward_btn").html("<a href=\"javascript:StepForward()\"><img src=\"../images/search/common/btn/btn_stepforward.jpg\" /></a>");
			//stopInterval();
		}
		SISOPlugin.SearchStop();
	}

	function GetDateDiff(date1,date2)
	{
		var arrDate1 = date1.split("-");
		var getDate1 = new Date(parseInt(arrDate1[0], 10),parseInt(arrDate1[1], 10)-1,parseInt(arrDate1[2], 10));
		var arrDate2 = date2.split("-");
		var getDate2 = new Date(parseInt(arrDate2[0], 10),parseInt(arrDate2[1], 10)-1,parseInt(arrDate2[2], 10));
		var getDiffTime = getDate1.getTime() - getDate2.getTime();

		return Math.floor(getDiffTime / (1000 * 60 * 60 * 24));
	}

	function OnClickEventSearch()
	{
		var from = $('#eventFrom').val();
		var to = $('#eventTo').val();

		var splitFrom = from.replace('/', ':').replace('/', ':').replace(' ', ':').split(":");
		var splitTo = to.replace('/', ':').replace('/', ':').replace(' ', ':').split(":");

		var validOnclickSearch = true;
		currPageNum = 1;

	  	var fromYear = splitFrom[2];
	  	var toYear = splitTo[2];
	  	var fromMonth = splitFrom[0];
	  	var toMonth = splitTo[0];
	  	var fromDay = splitFrom[1];
	  	var toDay = splitTo[1];
	  	var fromHour = splitFrom[3];
	  	var toHour = splitTo[3];
	  	var fromMin = splitFrom[4];
	  	var toMin = splitTo[4];
	  	var fromSec = splitFrom[5];
	  	var toSec = splitTo[5];

		if(recordingEnable == 0)
		{
			alert("<?php echo $msg_no_result[$GLOBALS['LANGINDEX']];?>");
			return;
		}

		/*var term = 31;
		var strSDT = new Date(fromYear, fromMonth, fromDay);
		var strEDT = new Date(toYear, toMonth, toDay);
		var searchDateDiff = parseInt((strEDT.getTime() - strSDT.getTime()) / (1000*60*60*24), 10);
		if (searchDateDiff > term) {
			 alert("<?php echo $msg_search_range[$GLOBALS['LANGINDEX']];?> ");
			 validOnclickSearch = false;
		}*/

		// SNB-8000] [SNV-8080] Event Search result no of day >32 
        var term = 31; 
        var strSDT = $('#eventFrom').datepicker('getDate'); 
        var strEDT = $('#eventTo').datepicker('getDate');
		
        var timeDiff = strEDT.getTime() - strSDT.getTime(); 
        var diffDays = Math.ceil(timeDiff / (1000 * 3600 * 24));     
        
		if (diffDays >= term) { 
			alert("<?php echo $msg_search_range[$GLOBALS['LANGINDEX']];?>"); 
			validOnclickSearch = false; 
        }

	  	if(fromYear == toYear
	  	&& fromMonth == toMonth
	  	&& fromDay == toDay
	  	&& fromHour == toHour
	  	&& fromMin == toMin
	  	&& fromSec == toSec){
	  		alert("<?php echo $msg_From_To_Diff[$GLOBALS['LANGINDEX']];?>");
	  		validOnclickSearch = false;
	  	} else {
	  		if(fromYear > toYear){
	  			alert("<?php echo $msg_From_To_Late[$GLOBALS['LANGINDEX']];?>");
	  			validOnclickSearch = false;
	  		} else {
	  			if(fromYear == toYear
	  				&& fromMonth > toMonth ) {
	  				alert("<?php echo $msg_From_To_Late[$GLOBALS['LANGINDEX']];?>");
	  				validOnclickSearch = false;
	  			} else if(fromYear == toYear
	  				&& fromMonth ==  toMonth
	  				&& fromDay > toDay ) {
	  				alert("<?php echo $msg_From_To_Late[$GLOBALS['LANGINDEX']];?>");
	  				validOnclickSearch = false;
	  			} else if(fromYear == toYear
	  			 	&& fromMonth ==  toMonth
	  			 	&& fromDay == toDay
	  			 	&& fromHour > toHour){
	  				alert("<?php echo $msg_From_To_Late[$GLOBALS['LANGINDEX']];?>");
	  				validOnclickSearch = false;
	  			} else if(fromYear == toYear
	  			 	&& fromMonth ==  toMonth
	  			 	&& fromDay == toDay
	  			 	&& fromHour == toHour
	  			 	&& fromMin > toMin ){
	  				alert("<?php echo $msg_From_To_Late[$GLOBALS['LANGINDEX']];?>");
	  				validOnclickSearch = false;
	  			} else if(fromYear == toYear
	  			 	&& fromMonth ==  toMonth
	  			 	&& fromDay == toDay
	  			 	&& fromHour == toHour
	  			 	&& fromMin == toMin
	  			 	&& fromSec > toSec ){
	  				alert("<?php echo $msg_From_To_Late[$GLOBALS['LANGINDEX']];?>");
	  				validOnclickSearch = false;
	  			}
	  		}

	  		if( (fromMonth == 2 && fromDay > 28 && isLeapYear(fromYear) == 0)
	  		||(fromMonth == 2 && fromDay > 29 && isLeapYear(fromYear) == 1)
	  		||(fromMonth == 4 && fromDay > 30)
	  		||(fromMonth == 6 && fromDay > 30)
	  		||(fromMonth == 9 && fromDay > 30)
	  		||(fromMonth == 11 && fromDay > 30)
	  		||(toMonth == 2 && toDay > 28 && isLeapYear(toYear) == 0)
	  		||(toMonth == 2 && toDay > 29 && isLeapYear(toYear) == 1)
	  		||(toMonth == 4 && toDay > 30)
	  		||(toMonth == 6 && toDay > 30)
	  		||(toMonth == 9 && toDay > 30)
	  		||(toMonth == 11 && toDay > 30)){
	  			alert("<?php echo $msg_invalid_day[$GLOBALS['LANGINDEX']]; ?>");
	  			validOnclickSearch = false;
	  		}
	  	}

	  	if (validOnclickSearch == false) return; 

	  	var msg = "";

		msg += "<GetSearch>";
		msg += "<EventToken>"+$('#eventSearchType').val()+"</EventToken>";
		msg += "<StartTime>";
		msg += "<Year>" + fromYear + "</Year>";
		msg += "<Month>" + fromMonth + "</Month>";
		msg += "<Day>" + fromDay + "</Day>";
		msg += "<Hour>" + fromHour + "</Hour>";
		msg += "<Min>" + fromMin + "</Min>";
		msg += "<Sec>" + fromSec + "</Sec>";
		msg += "</StartTime>";
		msg += "<EndTime>";
		msg += "<Year>" + toYear + "</Year>";
		msg += "<Month>" + toMonth + "</Month>";
		msg += "<Day>" + toDay + "</Day>";
		msg += "<Hour>" + toHour + "</Hour>";
		msg += "<Min>" + toMin + "</Min>";
		msg += "<Sec>" + toSec + "</Sec>";
		msg += "</EndTime>";
		msg += "<Direction>" + 1 + "</Direction>";
		msg += "<StartKey>" + 0 + "</StartKey>";
		msg += "<PageNo>"+ 1 + "</PageNo>";
		msg += "</GetSearch>";

		eventSearchType = $('#eventSearchType').val();
		startTime.year = fromYear;
		startTime.month = fromMonth;
		startTime.day = fromDay;
		startTime.hour = fromHour;
		startTime.min = fromMin;
		startTime.sec = fromSec;
		endTime.year = toYear;
		endTime.month = toMonth;
		endTime.day = toDay;
		endTime.hour = toHour;
		endTime.min = toMin;
		endTime.sec = toSec;

	  	var reqUrl = "./playback.cgi";

	  	$.ajax({
	  		type: "POST",
	  		data: {
	  			message: msg,
				trycount: (new Date()).getTime()
	  		},
	  		async: false,
	  		cache: false,
	  		url: reqUrl,
	  		dataType: "text",
	  		success: DrawEventSearchResult,
	  		error: function(xhr, status, error) {alert("<?php echo $msg_tryAgain[$GLOBALS['LANGINDEX']];?>"); }
	  	});
	}

	function DrawEventSearchResult(req)
	{
		var xml = $.parseXML(req);
		var index = 0;

		if($(xml).find("SearchResult").length > 0) {
			totalCount = $(xml).find("TotalCount").text();
			resultCount = $(xml).find("ResultCount").text();
			$(xml).find("Result").each(function() {
				resultList[index] = {};
				resultList[index].startTime = $("StartTime", this).text();
				resultList[index].endTime = $("EndTime", this).text();
				resultList[index].encode = $("Encoding", this).text();
				resultList[index].width = $("Width", this).text();
				resultList[index].height = $("Height", this).text();
				resultList[index].key = $("Key", this).text();
				resultList[index].dbIndex = $("DBIndex", this).text();
				index++;
			});
		} else {
			alert("<?php echo $msg_XMLdataError[$GLOBALS['LANGINDEX']]; ?>");
			return;
		}

		if(resultCount != 10) {
			for(var j = 0; j<resultCount; j++) {
			invalidlist[j] = "valid";
			}
			for(j = resultCount; j<10; j++) {
				invalidlist[j] = "invalid";
			}
		} else {
			for(j = 0; j<10; j++) {
			invalidlist[j] = "valid";
			}
		}
		if(totalCount == 0 && tempSuccess == 0) {
			alert("<?php echo $msg_no_result[$GLOBALS['LANGINDEX']]; ?>");
			return;
		}

		CurrPlayList = 0;

		$('#lnb01_span').html(""); // initialize list

		var msg = "";
		msg += "<table border='0' style='width:100%; text-align:center;'>";
		msg += "<tbody >";
		for (var index=0; index<resultCount; ++index) {
			msg += "<tr>";
			msg += "<td style='border-top:1px solid #1B2029; width:50px;'><input type='radio' name='eventResultList' id='eventResult" + (index+1) + "' value='" + (index+1) + "' onclick='javascript:OnClickList()'";
			if(index == 0)
			msg += " checked='checked' ";
			msg += "/></td>";
			msg += "<td style='border-top:1px solid #1B2029; width:50px;'><span>" + (index+1) + "</span></td>";
			msg += "<td style='text-align:center;padding:5px 0 6px;border-top:1px solid #1B2029;'>";
			msg += resultList[CurrPlayList+index].startTime + "<br />";
			msg += resultList[CurrPlayList+index].endTime;
			msg += "</td>";
			msg += "</tr>";
		}
		msg += "</tbody>";
		msg += "</table>";
		msg += "<ul class='list_box_2depth' >";
		msg += "<li style='width:261px;'>";
		msg += " <a href='javascript:ChangeCurrPage(\"First\")'><img src='../images/common/btn/btn_first.gif' /></a>";
		msg += "	<a href='javascript:ChangeCurrPage(\"Prev\")'><img src='../images/common/btn/btn_prev.gif' /></a>";
		msg += "	<span id='event_page_no'><strong>" + currPageNum + "/" + CalPLTotalPage() + "</strong></span>";
		msg += "	<a href='javascript:ChangeCurrPage(\"Next\")'><img src='../images/common/btn/btn_next.gif' /></a>";
		msg += "	<a href='javascript:ChangeCurrPage(\"Last\")'><img src='../images/common/btn/btn_last.gif' /></a>";
		msg += "<img src='../images/common/blank.jpg' />";
		msg += "	<a href='javascript:OnClickClose()'><img src='../images/common/btn/back_01.png' /></a>";
		msg += "</li>";
		msg += "</ul>";

		$('#lnb01_span').html(msg);
		$('#event_box').hide();
		isEventSearchSuccess = 1;
		isDaySelected = 1;

		$("#stop_btn").html("<a href=\"javascript:OnClickStop()\"><img src=\"../images/search/common/btn/03_normal.jpg\" /></a>");
		$("#play_btn").html("<a href=\"javascript:OnClickPlay()\"><img src=\"../images/search/common/btn/04_normal.jpg\" /></a>");
	}

	function OnClickPlay()
	{
		if(mode == 1) // timeline search seek
		{
			if(isDaySelected == 0) return;

			Play(searchYear, searchMonth, searchDayVal,parseInt($('#Timesearch .datetimepicker-hour').val(), 10),parseInt($('#Timesearch .datetimepicker-minuts').val(), 10),parseInt($('#Timesearch .datetimepicker-second').val(), 10) );
			startInterval();
		}
		else // event search
		{
			var selectedNo;
			for (var index=1; index<=10; ++index) {
				if ($('#eventResult'+index).is(':checked')) {
					selectedNo = index-1;
				}
			}
			if(isEventSearchSuccess == 0) return;

			var YearStartTemp;
			var YearEndTemp;
			var YearStart;
			var YearEnd;
			var YearStartSplit;
			var TimeStartSplit;
			var YearEndSplit;
			var TimeEndSplit;

			YearStartTemp = resultList[selectedNo].startTime;
			YearStart = YearStartTemp.split(" ");
			YearStartSplit = YearStart[0].split("/");
			TimeStartSplit = YearStart[1].split(":");

			YearEndTemp = resultList[selectedNo].endTime;
			YearEnd = YearEndTemp.split(" ");
			YearEndSplit = YearEnd[0].split("/");
			TimeEndSplit = YearEnd[1].split(":");

			// stop and play
			StopRecordedVideo();
			SISOPlugin.SetStartTime(parseInt(YearStartSplit[0]-1900, 10),parseInt(YearStartSplit[1]-1, 10),parseInt(YearStartSplit[2], 10),parseInt(TimeStartSplit[0], 10),parseInt(TimeStartSplit[1], 10),parseInt(TimeStartSplit[2], 10), parseInt(resultList[selectedNo].dbIndex, 10));
			SISOPlugin.SetEndTime(parseInt(YearEndSplit[0]-1900, 10),parseInt(YearEndSplit[1]-1, 10),parseInt(YearEndSplit[2], 10),parseInt(TimeEndSplit[0], 10),parseInt(TimeEndSplit[1], 10),parseInt(TimeEndSplit[2], 10));
			SISOPlugin.PlayRecordedVideo(location.hostname, parseInt(<?php echo $classInstances['Information']->dataInfo['DevicePort']['value']; ?>), "<?php echo $GLOBALS['USERINFO']['encname']; ?>", "<?php echo $GLOBALS['USERINFO']['encpw']; ?>");

			SISOPlugin.SetResolution(defaultWidth, defaultHeight);
			document.getElementById('plugin').width = defaultWidth;
			document.getElementById('plugin').height = defaultHeight;

			OriginalStatus = 1;
			FittStatus = 0;

			playSpeed = 1;
			//$('#speed_ff').html(playSpeed + "x");
			//$('#speed_prev').html("<font color='#2A303C'>-1x</font>");
			isDoneSpeedCtrl = 0;

			SeekStatus = 1;

			startInterval();
			
			if(ListenStatus == 1)
				SISOPlugin.StartAudio();
		}
	}

	function ChangeCurrPage(mode)
	{
		if(isBackup == true) return;

		StopRecordedVideo();

		var direction;
		var YearStartTemp;
		var YearEndTemp;
		var YearStart;
		var YearEnd;
		var YearStartSplit;
		var TimeStartSplit;
		var YearEndSplit;
		var TimeEndSplit;
		var ValidRequestTable = true;
		InfoStatus = false;

		if (mode == "First") {
			if(currPageNum > 1){
				currPageNum = 1;
				/*startTime.year = $('eventFromYear').val();
				startTime.month = $('eventFromMonth').val();
				startTime.day = $('eventFromDay').val();
				startTime.hour = $('eventFromHour').val();
				startTime.min = $('eventFromMin').val();
				startTime.sec = $('eventFromSec').val();
				endTime.year = $('eventToYear').val();
				endTime.month = $('eventToMonth').val();
				endTime.day = $('eventToDay').val();
				endTime.hour = $('eventToHour').val();
				endTime.min = $('eventToMin').val();
				endTime.sec = $('eventToSec').val();*/
				Startkey = 0;
				direction = 1; //backword
				ValidRequestTable = true;
			} else {
				ValidRequestTable = false;
			}
		} else if (mode == "Prev") {
			if (currPageNum > 1) {
				currPageNum--;
				/*startTime.year = $('eventFromYear').val();
				startTime.month = $('eventFromMonth').val();
				startTime.day = $('eventFromDay').val();
				startTime.hour = $('eventFromHour').val();
				startTime.min = $('eventFromMin').val();
				startTime.sec = $('eventFromSec').val();
				endTime.year = $('eventToYear').val();
				endTime.month = $('eventToMonth').val();
				endTime.day = $('eventToDay').val();
				endTime.hour = $('eventToHour').val();
				endTime.min = $('eventToMin').val();
				endTime.sec = $('eventToSec').val();*/
				direction = 0; //Forward
				Startkey = resultList[0].key;
				ValidRequestTable = true;
			} else {
				ValidRequestTable = false;
			}
		} else if (mode == "Next") {
			if (currPageNum != CalPLTotalPage() ) {
				currPageNum++;
				/*startTime.year = $('eventFromYear').val();
				startTime.month = $('eventFromMonth').val();
				startTime.day = $('eventFromDay').val();
				startTime.hour = $('eventFromHour').val();
				startTime.min = $('eventFromMin').val();
				startTime.sec = $('eventFromSec').val();
				endTime.year = $('eventToYear').val();
				endTime.month = $('eventToMonth').val();
				endTime.day = $('eventToDay').val();
				endTime.hour = $('eventToHour').val();
				endTime.min = $('eventToMin').val();
				endTime.sec = $('eventToSec').val();*/
				Startkey = resultList[9].key;
				direction = 1; //backword
				ValidRequestTable = true;
			} else {
				ValidRequestTable = false;
			}
		} else {
			if(currPageNum < CalPLTotalPage()){
				currPageNum = CalPLTotalPage();
				/*startTime.year = $('eventFromYear').val();
				startTime.month = $('eventFromMonth').val();
				startTime.day = $('eventFromDay').val();
				startTime.hour = $('eventFromHour').val();
				startTime.min = $('eventFromMin').val();
				startTime.sec = $('eventFromSec').val();
				endTime.year = $('eventToYear').val();
				endTime.month = $('eventToMonth').val();
				endTime.day = $('eventToDay').val();
				endTime.hour = $('eventToHour').val();
				endTime.min = $('eventToMin').val();
				endTime.sec = $('eventToSec').val();*/
				Startkey = 0;
				direction = 0; //Forward
				ValidRequestTable = true;
			} else {
				ValidRequestTable = false;
			}
		}

		if(ValidRequestTable == true){
			var msg = "";
			msg += "<GetSearch>";
			msg += "<EventToken>"+eventSearchType+"</EventToken>";
			msg += "<StartTime>";
			msg += "<Year>"+startTime.year+"</Year>";
			msg += "<Month>"+startTime.month+"</Month>";
			msg += "<Day>"+startTime.day+"</Day>";
			msg += "<Hour>"+startTime.hour+"</Hour>";
			msg += "<Min>"+startTime.min+"</Min>";
			msg += "<Sec>"+startTime.sec+"</Sec>";
			msg += "</StartTime>";
			msg += "<EndTime>";
			msg += "<Year>"+endTime.year+"</Year>";
			msg += "<Month>"+endTime.month+"</Month>";
			msg += "<Day>"+endTime.day+"</Day>";
			msg += "<Hour>"+endTime.hour+"</Hour>";
			msg += "<Min>"+endTime.min+"</Min>";
			msg += "<Sec>"+endTime.sec+"</Sec>";
			msg += "</EndTime>";
			msg += "<Direction>"+direction+"</Direction>";
			msg += "<StartKey>"+Startkey+"</StartKey>";
			// -- Use below code in WR3.0
			msg += "<PageNo>"+ currPageNum + "</PageNo>";
			// --
			msg += "</GetSearch>";

			var reqUrl = "./playback.cgi";

			$.ajax({
				type: "POST",
				data: {
					message: msg,
					trycount: (new Date()).getTime()
				},
				async: false,
				cache: false,
				url: reqUrl,
				dataType: "text",
				success: DrawEventSearchResult,
				error: function(xhr, status, error) {alert("<?php echo $msg_tryAgain[$GLOBALS['LANGINDEX']];?>"); }
			});
		}
		// disable ctrl btn..
	}

	function CalPLTotalPage() {
		var temp;
		if (totalCount < MAX_PLAYLIST) {
			temp = 1;
		} else {
			temp =  totalCount - (MAX_PLAYLIST*(parseInt(totalCount/MAX_PLAYLIST)));
			if (temp == 0) {
				temp = parseInt(totalCount/MAX_PLAYLIST);
			} else {
			temp = parseInt(totalCount/MAX_PLAYLIST) + 1;
			}
		}
		return temp;
	}

	function OnClickClose()
	{
		SISOPlugin.SetResolution(0, 0);
		document.getElementById('plugin').width = '1px';
		document.getElementById('plugin').height = '1px';

		isDaySelected = 0;
		StopRecordedVideo();
		RequestTime();

		isEventSearchSuccess = 0;
		$("#stop_btn").html("<img src=\"../images/search/common/btn/03_disable.jpg\" />");
		$("#play_btn").html("<img src=\"../images/search/common/btn/04_disable.jpg\" />");

		$('#lnb01_span').html("");
		$("#event_box").show();
	}

	function OnClickInfo()
	{
		if (infoStatus == false) {
			SISOPlugin.DisplayTimeOn();
			infoStatus = true;
		} else {
			SISOPlugin.DisplayTimeOff();
			infoStatus = false;
		}
	}

	function OnClickList()
	{
		isDaySelected = 1;
	}

	function SetCalendarDisplayDate()
	{
		//window.setTimeout('SetCalendarDisplayDateDone()', 0);
		SearchCalendar(cameraYear, cameraMonth);		
	}
	
	function SetCalendarDisplayDateDone()
	{
		//var control = $('#PlaybackControl').get(0);
		if (mode == 1)
		{
			//control.content.PlaybackControl.DisplayDate(cameraYear, cameraMonth, 1);
			//control.width = '200px';
			//control.height = '170px';
			SearchCalendar(cameraYear, cameraMonth);
		}
	}
	
	function SetTimelineBlock()
	{
		if(isSnapshot == 1)
		{
			SearchDay(searchYear, searchMonth, searchDayVal);
		}
	}

	function SearchCalendar(year, month)
   {
		if(SeekStatus == 0) {
			StopRecordedVideo();
			isDaySelected = 0;
		}
	   var playbackControl = $('#PlaybackControl').get(0);
	   year -= 1900; month -= 1; // FIX ME : Calendar control must give date as unix form!
	   SISOPlugin.SearchCalendar(year, month);
	   var searchDates = -1;
		var waitCount = 0;
		var time1, time2;
		time1 = new Date();
		time2 = new Date();
		while (searchDates < 0 && waitCount < waitLimit) {
			//waitCount++;
			time2 = new Date();
			waitCount = time2 - time1;
			searchDates = SISOPlugin.GetSearchCalendarResult();
		}
		if(waitCount >= waitLimit) {
			alert("<?php echo $t_timeout[$GLOBALS['LANGINDEX']]; ?>");
			window.location.reload(true);
			return;
	   }		
		playback.timeline.displaySearchDay(searchDates);		
   }

  //var firsthour, firstmin, firstsec;
  var starttimeArr, endtimeArr;
  var searchCount;
  var lasthour, lastmin, lastsec;

	function SearchDay(year, month, day)
	{
		StopRecordedVideo();

		isDaySelected = 1;
		// var timelineControl = $('#TimelineControl').get(0);
		//timelineControl.content.TimelineControl.ClearTimebar();
		year -= 1900; month -= 1; // FIX ME : Calendar control must give date as unix form!
		SISOPlugin.SearchDay(year, month, day);
		searchCount = -1;
		var waitCount = 0;
		var time1, time2;
		time1 = new Date();
		time2 = new Date();
		while (searchCount < 0 && waitCount < waitLimit) {
			//waitCount++;
			time2 = new Date();
			waitCount = time2 - time1;
	  		searchCount = SISOPlugin.GetTimelineCount();
	  	}
		if(waitCount >= waitLimit) {
			alert("<?php echo $t_timeout[$GLOBALS['LANGINDEX']]; ?>");
			window.location.reload(true);
			return;
		}

		$('#Timesearch .datetimepicker-hour').val("00");
		$('#Timesearch .datetimepicker-minuts').val("00");
		$('#Timesearch .datetimepicker-second').val("00");

		//timelineControl.content.TimelineControl.MoveTime(0,0,0);

		starttimeArr = new Array();
		endtimeArr = new Array();

		//timelineControl.content.TimelineControl.SetDate(year, month, day);

		searchYear = year;
		searchMonth = month;
		searchDayVal = day;

		timelineBlockArray = new Array();
		duplicateBlockArray = new Array();
		isDuplicateBlockStarts = false;
		isDuplicatePlay = false;
		timelineBlockCount = 0;
		duplicateBlockCount = 0;

		$(".timeLineDiv").html(""); //clearing previous added content
	
		for(var i = 0 ; i < searchCount ; i++) 	{
			var tStart = SISOPlugin.GetTimelineStartTime(i);
			starttimeArr[i] = tStart;
			var tEnd = SISOPlugin.GetTimelineEndTime(i);
			endtimeArr[i] = tEnd;
			var nRecType = SISOPlugin.GetTimelineRecType(i);
			var dbIndex = SISOPlugin.GetTimelineDBIndex(i);
			var fileIndex = SISOPlugin.GetTimelineFileIndex(i);
			var doubleIndex = SISOPlugin.GetTimelineDoubleIndex(i);

			var tmStart = timet_to_stm(parseInt(tStart,10));
			var tmEnd = timet_to_stm(parseInt(tEnd,10));
			//// sending data to js function
			playback.timeline.setTimeLineData(parseInt(tmStart.tm_hour, 10), parseInt(tmStart.tm_min, 10), parseInt(tmStart.tm_sec, 10), parseInt(tmEnd.tm_hour, 10), parseInt(tmEnd.tm_min, 10), parseInt(tmEnd.tm_sec, 10), nRecType, dbIndex, fileIndex, doubleIndex);

			var block = new TimelineBlock(parseInt(tmStart.tm_hour, 10), parseInt(tmStart.tm_min, 10), parseInt(tmStart.tm_sec, 10), parseInt(tmEnd.tm_hour, 10), parseInt(tmEnd.tm_min, 10), parseInt(tmEnd.tm_sec, 10), nRecType, dbIndex, fileIndex, doubleIndex);
			if (doubleIndex == 1) {
				duplicateBlockArray[duplicateBlockCount] = block;
				duplicateBlockCount++;
			} else {
				timelineBlockArray[timelineBlockCount] = block;
				timelineBlockCount++;
			}
		}
	}

  var SeekStatus = 0;

  // only send SEEK
	function Seek(year, month, day, hour, min, sec, dbindex)
	{
		if(typeof dbindex == "undefined") dbindex = 0; 
		if (endtimeArr == null) return;

		var maxtime, maxtimeIndex;
		for(var i = 0 ; i < endtimeArr.length ; i++) {
			var endtimeTm = timet_to_stm(endtimeArr[i]);
			var timeVal = parseInt(endtimeTm.tm_hour, 10) * 60 * 60 + parseInt(endtimeTm.tm_min, 10) * 60 + parseInt(endtimeTm.tm_sec, 10);
			if(i == 0) {
				maxtime = timeVal;
				maxtimeIndex = 0;
			}
			if(timeVal > maxtime) {
				maxtime = timeVal;
				maxtimeIndex = i;
			}
		}
		var endtimeTm = timet_to_stm(endtimeArr[maxtimeIndex]);
		var val1 = parseInt(endtimeTm.tm_hour, 10) * 60 * 60 + parseInt(endtimeTm.tm_min, 10) * 60 + parseInt(endtimeTm.tm_sec, 10);
		var val2 = hour * 60 * 60 + min * 60 + sec;
		
		if(val1 < val2) return;

	//timelineControl.content.TimelineControl.StopGetTime();
		stopInterval();
    //var newIndex;
    //if(index == 0) newIndex = 0;
    //else newIndex = index;
    //var seekTimeTm = timet_to_stm(starttimeArr[newIndex])

		SISOPlugin.SetStartTime(year,month,day,hour,min,sec,dbindex);
		SISOPlugin.SetEndTime(year,month,day,parseInt(endtimeTm.tm_hour, 10),parseInt(endtimeTm.tm_min, 10),parseInt(endtimeTm.tm_sec, 10));
		if(SeekStatus == 0) {
			SISOPlugin.SearchReady(location.hostname, parseInt(<?php echo $classInstances['Information']->dataInfo['DevicePort']['value']; ?>), "<?php echo $GLOBALS['USERINFO']['encname']; ?>", "<?php echo $GLOBALS['USERINFO']['encpw']; ?>");
		}
		// wait for searchready complete (it is slow in Mac NPAPI) 
		// Also wait for Picasso!
			var waitCount = 0;
			var time1 = new Date();
			var time2 = new Date();
			while (waitCount < 1000) {
				time2 = new Date();
				waitCount = time2 - time1;
			}
		//	
		SISOPlugin.SearchSeek(year,month,day,hour,min,sec,1,dbindex);
		if(SeekStatus == 0) {
			SeekStatus = 1;
			SISOPlugin.SearchPlay(1);
		}

		OriginalStatus = 1;
		FittStatus = 0;

		if(BrowserDetect.browser != 'Safari') {
			SISOPlugin.SetResolution(defaultWidth, defaultHeight);
			document.getElementById('plugin').width = defaultWidth;
			document.getElementById('plugin').height = defaultHeight;
		}

		playSpeed = 1;
		$('#speed_ff').html(playSpeed + "x");
		$('#speed_prev').html("<font color='#2A303C'>-1x</font>");

		//timelineControl.content.TimelineControl.StartGetTime();
		startInterval();
		if(BrowserDetect.browser == 'Safari') {
			SISOPlugin.SetResolution(1, 1);
			document.getElementById('plugin').width = 1;
			document.getElementById('plugin').height = 1;

			SISOPlugin.SetResolution(defaultWidth, defaultHeight);
			document.getElementById('plugin').width = defaultWidth;
			document.getElementById('plugin').height = defaultHeight;
		}
	
		if(ListenStatus == 1)
			SISOPlugin.StartAudio();
		
		$("#rewind_btn").html("<a href=\"javascript:Rewind()\"><img src=\"../images/search/common/btn/btn_prevspeed.jpg\" /></a>");
		//$("#stepbackward_btn").html("<a href=\"javascript:StepBackward()\"><img src=\"../images/search/common/btn/btn_stepbackward.jpg\" /></a>");
		$("#ff_btn").html("<a href=\"javascript:FastForward()\"><img src=\"../images/search/common/btn/btn_ffspeed.jpg\" /></a>");
		//$("#stepforward_btn").html("<a href=\"javascript:StepForward()\"><img src=\"../images/search/common/btn/btn_stepforward.jpg\" /></a>");
		$("#stepbackward_btn").html("<img src=\"../images/search/common/btn/btn_stepbackward_disable.jpg\" />");
		$("#stepforward_btn").html("<img src=\"../images/search/common/btn/btn_stepforward_disable.jpg\" />");
	}
  
  // only send PLAY when click play button
	function Play(year, month, day, hour, min, sec, dbindex)
	{
		if(typeof dbindex == "undefined") dbindex = 0; 
		if (endtimeArr == null) return;

		//var timelineControl = $("#TimelineControl").get(0);

		var maxtime, maxtimeIndex;
		for(var i = 0 ; i < endtimeArr.length ; i++) {
			var endtimeTm = timet_to_stm(endtimeArr[i]);
			var timeVal = parseInt(endtimeTm.tm_hour, 10) * 60 * 60 + parseInt(endtimeTm.tm_min, 10) * 60 + parseInt(endtimeTm.tm_sec, 10);
			if(i == 0) {
				maxtime = timeVal;
				maxtimeIndex = 0;
			}
			if(timeVal > maxtime) {
				maxtime = timeVal;
				maxtimeIndex = i;
			}
		}
		var endtimeTm = timet_to_stm(endtimeArr[maxtimeIndex]);
		var val1 = parseInt(endtimeTm.tm_hour, 10) * 60 * 60 + parseInt(endtimeTm.tm_min, 10) * 60 + parseInt(endtimeTm.tm_sec, 10);
		var val2 = hour * 60 * 60 + min * 60 + sec;
		if(val1 < val2) return;

		//timelineControl.content.TimelineControl.StopGetTime();

		isDoneSpeedCtrl = 0;
		//SISOPlugin.Stop();
		SISOPlugin.SetStartTime(year,month,day,hour,min,sec,dbindex);
		SISOPlugin.SetEndTime(year,month,day,parseInt(endtimeTm.tm_hour, 10),parseInt(endtimeTm.tm_min, 10),parseInt(endtimeTm.tm_sec, 10));
		if(SeekStatus == 0) {
			SISOPlugin.SearchReady(location.hostname, parseInt(<?php echo $classInstances['Information']->dataInfo['DevicePort']['value']; ?>), "<?php echo $GLOBALS['USERINFO']['encname']; ?>", "<?php echo $GLOBALS['USERINFO']['encpw']; ?>");

			// wait for searchready complete (it is slow in Mac NPAPI) 
			// Also wait for Picasso!
			var waitCount = 0;
			var time1 = new Date();
			var time2 = new Date();
			while (waitCount < 2000) {
				time2 = new Date();
				waitCount = time2 - time1;
			}
			//
			
		}
	
		SISOPlugin.SearchPlay(1);
		startInterval();
		SeekStatus = 1;

		if(BrowserDetect.browser != 'Safari' && FittStatus == 0 && OriginalStatus == 1) {
			SISOPlugin.SetResolution(defaultWidth, defaultHeight);
			document.getElementById('plugin').width = defaultWidth;
			document.getElementById('plugin').height = defaultHeight;
		}

		playSpeed = 1;
		$('#speed_ff').html(playSpeed + "x");
		$('#speed_prev').html("<font color='#2A303C'>-1x</font>");

		//timelineControl.content.TimelineControl.StartGetTime();

		if(BrowserDetect.browser == 'Safari' && FittStatus == 0 && OriginalStatus == 1) {
			SISOPlugin.SetResolution(1, 1);
			document.getElementById('plugin').width = 1;
			document.getElementById('plugin').height = 1;

			SISOPlugin.SetResolution(defaultWidth, defaultHeight);
			document.getElementById('plugin').width = defaultWidth;
			document.getElementById('plugin').height = defaultHeight;
		}

		if(ListenStatus == 1)
			SISOPlugin.StartAudio();

		$("#rewind_btn").html("<a href=\"javascript:Rewind()\"><img src=\"../images/search/common/btn/btn_prevspeed.jpg\" /></a>");
		//$("#stepbackward_btn").html("<a href=\"javascript:StepBackward()\"><img src=\"../images/search/common/btn/btn_stepbackward.jpg\" /></a>");
		$("#ff_btn").html("<a href=\"javascript:FastForward()\"><img src=\"../images/search/common/btn/btn_ffspeed.jpg\" /></a>");
		//$("#stepforward_btn").html("<a href=\"javascript:StepForward()\"><img src=\"../images/search/common/btn/btn_stepforward.jpg\" /></a>");
		$("#stepbackward_btn").html("<img src=\"../images/search/common/btn/btn_stepbackward_disable.jpg\" />");
		$("#stepforward_btn").html("<img src=\"../images/search/common/btn/btn_stepforward_disable.jpg\" />");
	}

	function GetFrameTimeHtml()
	{

		var hour = SISOPlugin.GetCurrentFrameTimeHour();
		var min = SISOPlugin.GetCurrentFrameTimeMin();
		var sec = SISOPlugin.GetCurrentFrameTimeSec();

		if(hour == -1 || min == -1 || sec == -1 || SeekStatus == 0 || intervalStatus == 1)
			return;

		if (mode == 1) {

			if(hour < 10) {
			$('#Timesearch .datetimepicker-hour').val("0" + hour); 
			} else {
				$('#Timesearch .datetimepicker-hour').val(parseInt(hour, 10)); 
			}

			if(min < 10) {
				$('#Timesearch .datetimepicker-minuts').val("0" + min);
			} else {
				$('#Timesearch .datetimepicker-minuts').val(parseInt(min, 10));
			}

			if(sec < 10) {
				$('#Timesearch .datetimepicker-second').val("0" + sec);
			} else {  		
				$('#Timesearch .datetimepicker-second').val(parseInt(sec, 10));
			}

			playback.timeline.moveTime(hour, min, sec);

		}

		var width = parseInt(SISOPlugin.GetFrameWidth());
     	var height = parseInt(SISOPlugin.GetFrameHeight());

		var checkRotateChange = 0;
		if (defaultWidth > defaultHeight) {
			checkRotateChange++;
		}
		if (width > height) {
			checkRotateChange++;
		}

		if (checkRotateChange == 1 && OriginalStatus == 1 && FittStatus == 0) {

			defaultWidth = 800;
			defaultHeight = 600;
			if (height > width) {
				defaultWidth = 600;
				defaultHeight = 800;
			}

			SISOPlugin.SetResolution(defaultWidth, defaultHeight);
			document.getElementById('plugin').width = defaultWidth;
			document.getElementById('plugin').height = defaultHeight;
		}
	} 

	var intervalStatus = 0;
	function setIntervalStatus() {
		intervalStatus = 1;
	}

	function clearIntervalStatus() {
		intervalStatus = 0;
	}

	var handle;
	var intervalFlag = 0;
	function startInterval(){
		if (intervalFlag > 0) {
			return;
		}
		handle = setInterval(GetFrameTimeHtml, 1000);
		intervalFlag = 1;
	}

	function stopInterval(){
		//When you want to cancel it:
		clearInterval(handle);
		handle = 0;
		intervalFlag = 0;
	}
   
	function FastForward()
	{
	/*if ($('#StepChk').is(':checked')  && SeekStatus == 1)
	{
	SISOPlugin.SearchStepForward();
	return;
	}*/

		if(SeekStatus == 1) {
			if (RewFFTimeoutValue == 1) return;

			if(playSpeed == 1) {
				playSpeed = 2;
				$('#speed_ff').html(playSpeed + "x");
				$('#speed_prev').html("<font color='#2A303C'>-1x</font>");
			} else if(playSpeed == 2) {
				playSpeed = 4;
				$('#speed_ff').html(playSpeed + "x");
				$('#speed_prev').html("<font color='#2A303C'>-1x</font>");
			} else if(playSpeed == 4) {
				playSpeed = 8;
				$('#speed_ff').html(playSpeed + "x");
				$('#speed_prev').html("<font color='#2A303C'>-1x</font>");
			} else if(playSpeed == 8) {
				return;
			} else if(playSpeed == -1) {
				playSpeed = 1;
				$('#speed_ff').html(playSpeed + "x");
				$('#speed_prev').html("<font color='#2A303C'>-1x</font>");
			} else if(playSpeed == -2) {
				playSpeed = -1;
				$('#speed_prev').html(playSpeed + "x");
				$('#speed_ff').html("<font color='#2A303C'>1x</font>");
			} else if(playSpeed == -4) {
				playSpeed = -2;
				$('#speed_prev').html(playSpeed + "x");
				$('#speed_ff').html("<font color='#2A303C'>1x</font>");
			} else if(playSpeed == -8) 	{
				playSpeed = -4;
				$('#speed_prev').html(playSpeed + "x");
				$('#speed_ff').html("<font color='#2A303C'>1x</font>");
			}

			//SISOPlugin.SearchSeek(year,month,day,hour,min,sec,1,0);
			SISOPlugin.SearchPlay(playSpeed);
			isDoneSpeedCtrl = 1;

			RewFFTimeoutValue = 1;
			window.setTimeout('ResetRewFFTimeoutValue();', 3000);
		}
	}

	function Rewind()
	{
		/*if ($('#StepChk').is(':checked') && SeekStatus == 1)
		{
		SISOPlugin.SearchStepBackward();
		return;
		}*/

		if(SeekStatus == 1) {
			if (RewFFTimeoutValue == 1) return;

			if(playSpeed == 1) {
				playSpeed = -1;
				$('#speed_prev').html(playSpeed + "x");
				$('#speed_ff').html("<font color='#2A303C'>1x</font>");
			} else if(playSpeed == 2) {
				playSpeed = 1;
				$('#speed_ff').html(playSpeed + "x");
				$('#speed_prev').html("<font color='#2A303C'>-1x</font>");
			} else if(playSpeed == 4) {
				playSpeed = 2;
				$('#speed_ff').html(playSpeed + "x");
				$('#speed_prev').html("<font color='#2A303C'>-1x</font>");
			} else if(playSpeed == 8) {
				playSpeed = 4;
				$('#speed_ff').html(playSpeed + "x");
				$('#speed_prev').html("<font color='#2A303C'>-1x</font>");
			} else if(playSpeed == -1) {
				playSpeed = -2;
				$('#speed_prev').html(playSpeed + "x");
				$('#speed_ff').html("<font color='#2A303C'>1x</font>");
			} else if(playSpeed == -2)	{
				playSpeed = -4;
				$('#speed_prev').html(playSpeed + "x");
				$('#speed_ff').html("<font color='#2A303C'>1x</font>");
			} else if(playSpeed == -4) {
				playSpeed = -8;
				$('#speed_prev').html(playSpeed + "x");
				$('#speed_ff').html("<font color='#2A303C'>1x</font>");
			} else if(playSpeed == -8) 	{
				return;
			}
		//SISOPlugin.SearchSeek(year,month,day,hour,min,sec,1,0);
		SISOPlugin.SearchPlay(playSpeed);
		isDoneSpeedCtrl = 1;

		RewFFTimeoutValue = 1;
		window.setTimeout('ResetRewFFTimeoutValue();', 3000);
		}
	}

	function StepBackward()
	{
		playSpeed = 1;
		$('#speed_ff').html(playSpeed + "x");
		$('#speed_prev').html("<font color='#2A303C'>-1x</font>");
		isDoneSpeedCtrl = 0;

		SISOPlugin.SearchStepBackward();
	}
  
	function StepForward()
	{
		playSpeed = 1;
		$('#speed_ff').html(playSpeed + "x");
		$('#speed_prev').html("<font color='#2A303C'>-1x</font>");
		isDoneSpeedCtrl = 0;

		SISOPlugin.SearchStepForward();
	}
  
	function ResetRewFFTimeoutValue()
	{
		RewFFTimeoutValue = 0;
	}

	function OnChangeSeekTime()
	{

		if(isDaySelected == 0) return;

		$('#Timesearch .datetimepicker-hour').get(0).blur();
		$('#Timesearch .datetimepicker-minuts').get(0).blur();
		$('#Timesearch .datetimepicker-second').get(0).blur();

		//var timelineControl = $('#TimelineControl').get(0);
		//timelineControl.content.TimelineControl.StopGetTime();

		var selhour = $('#Timesearch .datetimepicker-hour').val();
		var selmin = $('#Timesearch .datetimepicker-minuts').val();
		var selsec = $('#Timesearch .datetimepicker-second').val();

		Seek(searchYear,searchMonth,searchDayVal,parseInt(selhour, 10),parseInt(selmin, 10),parseInt(selsec,10));

	}

	function OnClickSnapshot()
	{
		if(document.getElementById('plugin').width == 1) return;

		var date = new Date();
		defaultFilename = "<?php echo $_SERVER['MODELNAME']; ?>" + "_";
		defaultFilename += leadingZeros(date.getFullYear(), 4) + leadingZeros(date.getMonth() + 1, 2) + leadingZeros(date.getDate(), 2) + leadingZeros(date.getHours(), 2) + leadingZeros(date.getMinutes(), 2) + leadingZeros(date.getSeconds(), 2);
		
		SISOPlugin.SaveSnapShotNoDialog(defaultFilename);

		$('#snapshotCompleted').get(0).style.display = "block";

		if (isShowing == 0) {
			setTimeout(function () {
				isShowing = 0;
				$('#snapshotCompleted').get(0).style.display = "none";
			}, 1000);
		}

		isShowing = 1;
	}

	function OnClickBackup()
	{
		if(mode == 0) {
			if(isDaySelected == 0 && isEventSearchSuccess == 0) return;
			var YearStartTemp;
			var YearEndTemp;
			var YearStart;
			var YearEnd;
			var YearStartSplit;
			var TimeStartSplit;
			var YearEndSplit;
			var TimeEndSplit;
			var CurDBIndex;

			var selectedNo;
			for (var index=1; index<=10; ++index) {
				if ($('#eventResult'+index).is(':checked')) {
					selectedNo = index-1;
				}
			}
			if(selectedNo < 0) return;

			YearStartTemp = resultList[selectedNo].startTime;
			YearStart = YearStartTemp.split(" ");
			YearStartSplit = YearStart[0].split("/");
			TimeStartSplit = YearStart[1].split(":");

			YearEndTemp = resultList[selectedNo].endTime;
			YearEnd = YearEndTemp.split(" ");
			YearEndSplit = YearEnd[0].split("/");
			TimeEndSplit = YearEnd[1].split(":");
			CurDBIndex = resultList[selectedNo].dbIndex;

			var msg = './playback_backup.cgi?year=' + YearStartSplit[0] + '&month=' + YearStartSplit[1] + '&day=' + YearStartSplit[2] + '&starthour=' + TimeStartSplit[0] + '&startmin=' + TimeStartSplit[1] + '&startsec=' + TimeStartSplit[2] + '&endhour=' + TimeEndSplit[0] + '&endmin=' + TimeEndSplit[1] + '&endsec=' + TimeEndSplit[2] + '&dbindex=' + CurDBIndex;
			SISOPlugin.Stop();
			window.open(msg,'timebackup','width=735,height=400,location=0,toolbar=0,scrollbars=0,resizable=0,status=0,menubar=0');
		} else {
			if(isDaySelected == 0)
			{
			alert("<?php echo $msg_timebackupDateError[$GLOBALS['LANGINDEX']]; ?>");
			return;
			}

			var maxtime, maxtimeIndex;
			for(var i = 0 ; i < endtimeArr.length ; i++) {
				var endtimeTm = timet_to_stm(endtimeArr[i]);
				var timeVal = parseInt(endtimeTm.tm_hour, 10) * 60 * 60 + parseInt(endtimeTm.tm_min, 10) * 60 + parseInt(endtimeTm.tm_sec, 10);
				if(i == 0) {
					maxtime = timeVal;
					maxtimeIndex = 0;
				}
				if(timeVal > maxtime) {
					maxtime = timeVal;
					maxtimeIndex = i;
				}
			}
			var endtimeTm = timet_to_stm(endtimeArr[maxtimeIndex]);
			var endHour = parseInt(endtimeTm.tm_hour, 10);
			var endMin = parseInt(endtimeTm.tm_min, 10);
			var endSec = parseInt(endtimeTm.tm_sec, 10);

			var msg = './playback_backup.cgi?year=' + (searchYear+1900) + '&month=' + (searchMonth+1) + '&day=' + searchDayVal + '&starthour=' + '-1' + '&startmin=' + '-1' + '&startsec=' + '-1' + '&endhour=' + endHour + '&endmin=' + endMin + '&endsec=' + endSec + '&dbindex=' + 0;
			StopRecordedVideo(1);
			window.open(msg,'timebackup','width=735,height=400,location=0,toolbar=0,scrollbars=0,resizable=0,status=0,menubar=0');
		}
	}

	function GetSelectedTime() {
		//var control = document.getElementById("SDBackup");

		var selectedNo;
		for (var index=1; index<=10; ++index) {
			if ($('#eventResult'+index).is(':checked')) {
			selectedNo = index-1;
			}
		}
  	//control.content.SDBackupControl.SetDBIndex(resultList[selectedNo].dbIndex);
  	//control.content.SDBackupControl.GetTime(YearStartSplit[0],YearStartSplit[1],YearStartSplit[2],TimeStartSplit[0],TimeStartSplit[1],TimeStartSplit[2],YearEndSplit[0] ,YearEndSplit[1] ,YearEndSplit[2] ,TimeEndSplit[0],TimeEndSplit[1],TimeEndSplit[2]);
	}

	function OnClickOriginal()
	{
		if(SeekStatus == 0) return;
		var CurrProfile;
		CurrProfile = $('#liveProfile').val();
		var width = parseInt(SISOPlugin.GetFrameWidth());
     	var height = parseInt(SISOPlugin.GetFrameHeight());

		if(OriginalStatus == 0) 	{
			defaultWidth = 800;
			defaultHeight = 600;
			if (height > width) {
				defaultWidth = 600;
				defaultHeight = 800;
			}
			SISOPlugin.SetResolution(defaultWidth, defaultHeight);
			document.getElementById('plugin').width = defaultWidth;
			document.getElementById('plugin').height = defaultHeight;
			OriginalStatus = 1;
			FittStatus = 0;
			//if (mode == 1) {
			//	$('#timebarHtml').show();
			//}
			/* if($('#TimelineControl').get(0) != null)
			{
			  $('#TimelineControl').get(0).width = 900;
			  $('#TimelineControl').get(0).height = 93;
			}*/
		} else {
		  SISOPlugin.SetResolution(parseInt(width), parseInt(height));
		  document.getElementById('plugin').width = width;
		  document.getElementById('plugin').height = height;
		  OriginalStatus = 0;
		  FittStatus = 0;
		  //if (mode == 1) {
		  //	$('#timebarHtml').hide();
		  //}
		 /* if($('#TimelineControl').get(0) != null)
		  {
			  $('#TimelineControl').get(0).width = 1;
			  $('#TimelineControl').get(0).height = 1;
		  }*/
		}
	}

	function OnClickFitt()
	{
		if(SeekStatus == 0) return;
		var width = parseInt(SISOPlugin.GetFrameWidth());
		var height = parseInt(SISOPlugin.GetFrameHeight());

		if(FittStatus == 0) {
			SetViewportSize();
			var widthVal = parseInt(viewportWidth) - 345;
			var heightVal = parseInt(viewportHeight) - 135;
			var ratio = width / height;
			var viewportRatio = widthVal / heightVal;

			viewportRatio = viewportRatio.toFixed(1);
			ratio = ratio.toFixed(1);

			if (height > width)  // rotate view
			{
				if(ratio == 0.6){				// 16:9
					if(viewportRatio < ratio)
						heightVal = (widthVal * 25 / 9) - widthVal;
					else
						widthVal = (heightVal * 25 / 16) - heightVal;

					if(widthVal < 180 || heightVal < 320)
					{
						widthVal = 180;
						heightVal = 320;
					}
				}
				else if(ratio == 0.8 && height != 1280 && width != 1024 && height != 720 && width != 576){		//4//4:3
					if(viewportRatio < ratio)
						heightVal = (widthVal * 7 / 3) - widthVal;
					else
						widthVal = (heightVal * 7 / 4) - heightVal;

					if(widthVal < 240 || heightVal < 320)
					{
						widthVal = 240;
						heightVal = 320;
					}
				}
				else{								//5:4
					if(viewportRatio < ratio)
						heightVal = (widthVal * 9 / 4) - widthVal;
					else
						widthVal = (heightVal * 9 / 5) - heightVal;

					if(widthVal < 320 || heightVal < 256)
					{
						widthVal = 320;
						heightVal = 256;
					}
				}
			}
			else
			{
				if(ratio == 1.8){				// 16:9
					if(viewportRatio < ratio)
						heightVal = (widthVal * 25 / 16) - widthVal;
					else
						widthVal = (heightVal * 25 / 9) - heightVal;

					if(widthVal < 320 || heightVal < 180)
					{
						widthVal = 320;
						heightVal = 180;
					}
				}
				else if(ratio == 1.3 && height != 1024 && height != 576){		//4//4:3
					if(viewportRatio < ratio)
						heightVal = (widthVal * 7 / 4) - widthVal;
					else
						widthVal = (heightVal * 7 / 3) - heightVal;

					if(widthVal < 320 || heightVal < 240)
					{
						widthVal = 320;
						heightVal = 240;
					}
				}
				else{								//5:4
					if(viewportRatio < ratio)
						heightVal = (widthVal * 9 / 5) - widthVal;
					else
						widthVal = (heightVal * 9 / 4) - heightVal;

					if(widthVal < 320 || heightVal < 256)
					{
						widthVal = 320;
						heightVal = 256;
					}
				}
			}

			SISOPlugin.SetResolution(widthVal, heightVal);
			document.getElementById('plugin').width = widthVal;
			document.getElementById('plugin').height = heightVal;
			FittStatus = 1;
			OriginalStatus = 1;
			//if(BrowserDetect.browser != 'Firefox')
			//{
			//  document.body.style.overflow = 'hidden';
			//}
			//if (mode == 1) {
			//	$('#timebarHtml').hide();
			//}
			if($('#TimelineControl').get(0) != null) {
				$('#TimelineControl').get(0).width = 1;
				$('#TimelineControl').get(0).height = 1;
			}
		} else {
			defaultWidth = 800;
			defaultHeight = 600;
			if (height > width) {
				defaultWidth = 600;
				defaultHeight = 800;
			}
			SISOPlugin.SetResolution(defaultWidth, defaultHeight);
			document.getElementById('plugin').width = defaultWidth;
			document.getElementById('plugin').height = defaultHeight;
			FittStatus = 0;
			OriginalStatus = 1;
			//if(BrowserDetect.browser != 'Firefox')
			//{
			//  document.body.style.overflow = 'auto';
			//}
			//if (mode == 1) {
			//	$('#timebarHtml').show();
			//}
			/*if($('#TimelineControl').get(0) != null)
			{
			$('#TimelineControl').get(0).width = 900;
			$('#TimelineControl').get(0).height = 93;
			}*/
		}
	}

	function SetViewportSize()
	{
		if (typeof document.documentElement.clientWidth != 'undefined' && document.documentElement.clientWidth != 0 && typeof document.documentElement != 'undefined') {
			viewportWidth = document.documentElement.clientWidth;
			viewportHeight = document.documentElement.clientHeight;
		} else if (typeof window.innerWidth != 'undefined') {
			viewportWidth = window.innerWidth;
			viewportHeight = window.innerHeight;
		} else {
			viewportWidth = document.getElementsByTagName('body')[0].clientWidth;
			viewportHeight = document.getElementsByTagName('body')[0].clientHeight;
		}
	}
	
	function OnListenClick()
	{
		if(ListenStatus == 0) {
			SISOPlugin.StartAudio();
			ListenStatus = 1;
			$('#btnListen').get(0).style.backgroundColor = '#0b76d5';
			//window.setTimeout('SISOPlugin.SetVolume(volumeVal)', 1000);
		} else {
			SISOPlugin.StopAudio();
			ListenStatus = 0;
			$('#btnListen').get(0).style.backgroundColor = '#656e83';
		}
	}

	function DrawTimeline()
	{
		if(recordingEnable == 0) {
			alert("<?php echo $msg_no_result[$GLOBALS['LANGINDEX']];?>");
			return;
		}
		SetTimelineBlock();
		SetCalendarDisplayDate();
	} 
	///////////////////////////////////////////////////
	$(function(){
		$('#timebarHtml').hide();
	});
	</script>
</head>

<body onload="OnLoad()" onunload="OnUnload()">
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
			<div class="gnb-tab">
				<ul>
					<li><a href="../monitoring.cgi"><img src="../images/common/icon/icon_live.png" class="fix" /><?php echo $GLOBALS['top_monitoring'][0]; ?></a></li>
					<li class="selected"> <a href="../setup/playback.cgi"><img src="../images/common/icon/icon_search.png" class="fix" /><?php echo $GLOBALS['top_playback'][0]; ?></a></li>
					<li><a href="../setup/basic_videoprofile.cgi"><img src="../images/common/icon/icon_setup.png" class="fix" /><?php echo $GLOBALS['top_setup'][0]; ?></a></li>
				</ul>
				<div>
					<div style="position:absolute; top:54px;left:430px;">
						<img src="../images/common/icon/user_icon.png">
					</div>
					<div style="position:absolute; top:58px;left:450px">					
						<h2>
				<?php
					// NO NEED to transrate, ONLY ENGLISH
					if 		($GLOBALS['USERINFO']['name'] == 'admin') echo 'ADMIN';
					else if 	($GLOBALS['USERINFO']['name'] == 'guest') echo 'GUEST';
					else																echo 'USER';
				?>
						</h2>
					</div>
					<div style="position:absolute; top:58px;left:510px">
						<img src="../images/common/PTZ/bar.png">
					</div>
					<div style="position:absolute; top:60px;left:520px">
						<img class="profileAccess" src="../images/common/icon/profileaccess.png" style="cursor:pointer" />
					</div>
					<div style="position:absolute; top:58px;left:545px; cursor:pointer">
						<h2 class="profileAccess">Status</h2>
					</div>
				</div>
			</div>
		</div>
		<div id="container">
			<div id="lnb2" style="display:none;">
				<div id="lnb-list-fold">
					<ul class="lnb-list-in2" style="display:none;">
						<li><a href="javascript:openlnbMenu(1)"><img src="../images/search/lnb_m02_off.gif" /></a></li>
						<li><a href="javascript:openlnbMenu(2)"><img src="../images/search/lnb_m01_off.gif" /></a></li>
					</ul>
					<ul class="lnb-list-in2">
						<li><a href="javascript:openlnbMenu(1)"><img src="../images/search/lnb_m02_s.gif" /></a></li>
						<li><a href="javascript:openlnbMenu(2)"><img src="../images/search/lnb_m01_s.gif" /></a></li>
					</ul>
					<div class="lnb-open">
						<a href="#"><img src="../images/common/btn/btn_lnb_arrow02.gif" /></a>
					</div>
				</div>
			</div>
			<div id="lnb">
				<div id="lnb-list">
					<span id="searchlnb">
						<ul class="lnb-list-in">
							<li id="lnb01"><img src="../images/search/lnb_m02_off.gif" style="cursor:pointer" />
								<div class="hidden_box time_search">
									<span id="lnb01_span">
									</span>
								<div id='event_box' class='h2_box'>
									<table style='width:260px;'>
										<tr><td colspan='6'>
											<?php echo $t_from[$GLOBALS['LANGINDEX']];?>
										</td></tr>
										<tr><td id="From">
											<input type="text" id="eventFrom" class="text" readonly="true" style="width:205px; margin-bottom:10px; margin-right:5px;"/>
										</td></tr>
										<tr><td colspan='6'>
											<?php echo $t_to[$GLOBALS['LANGINDEX']];?>
										</td></tr>
										<tr><td id="To">
											<input type="text" id="eventTo" class="text" readonly="true" style="width:205px; margin-bottom:10px; margin-right:5px;"/>
										</td></tr>
										<tr style="height:40px;"><td colspan='6'>
											<a class='btn_type01' href='javascript:DrawToday()'><?php echo $t_today[$GLOBALS['LANGINDEX']];?></a>
										</td></tr>
										<tr><td colspan='6'>
											<select id='eventSearchType' class="selectbox_style_wid250" style='background-color:#868fa3; color:#1c1c1c; width:255px'>
											<?php if ($GLOBALS['M_ALARMIN_COUNT'] > 0) { ?>
												<option value = '0'><?php echo $t_alarmInput[$GLOBALS['LANGINDEX']];?></option>
											<?php } ?>
											<?php if ($GLOBALS['M_SUPPORT_EVENT_TD']) { ?>
												<option value = '6'><?php echo $t_tampering[$GLOBALS['LANGINDEX']];?></option>
											<?php } ?>
												<option value = '3'><?php echo $t_MD[$GLOBALS['LANGINDEX']];?></option>
	  										<?php if ($GLOBALS['M_SUPPORT_EVENT_VA'] & IV_SUPPORT) { ?>
	  											<option value = '1'><?php echo $t_videoAnalytics[$GLOBALS['LANGINDEX']];?></option>
	  										<?php } 
	  												if ($GLOBALS['M_SUPPORT_EVENT_FD']) { ?>
												<option value = '5'><?php echo $t_fd[$GLOBALS['LANGINDEX']];?></option>
											<?php } 
													if ($GLOBALS['M_SUPPORT_EVENT_AD']) { ?>
												<option value = '7'><?php echo $t_ad[$GLOBALS['LANGINDEX']];?></option>
											<?php } 
													if ($GLOBALS['M_SUPPORT_EVENT_ND']) { ?>
												<option value = '4'><?php echo $t_networkDisconnect[$GLOBALS['LANGINDEX']];?></option>
											<?php } 
													if ($GLOBALS['M_SUPPORT_PTZ_TRACKING']) { ?>
												<option value = '8'><?php echo $t_ptzTracking[$GLOBALS['LANGINDEX']];?></option>
											<?php } 
												if(($GLOBALS['M_SUPPORT_SD'] || $GLOBALS['M_SUPPORT_NAS']) && !$GLOBALS['M_SUPPORT_LOCAL_RECORDING']) { ?>
												<option value = '9'><?php echo $t_manualRecording[$GLOBALS['LANGINDEX']];?></option>
											<?php } ?>
											</select>
										</td></tr>
										<tr><td colspan='5' style='height:60px;'>
											<a class='search search_type3 mgt10 mgb10' style="width:255px" href='javascript:OnClickEventSearch()'><?php echo $t_eventsearch[$GLOBALS['LANGINDEX']];?></a>
										</td><td></td></tr>
							    	</table>
						  		</div>
							</div>
						</li>
						<li id="lnb02"><img src="../images/search/lnb_m01_off.gif" style="cursor:pointer" />
							<div class="hidden_box lnb_box" id="TimeCalDiv">
							<span id="Timesearch" style="position:relative; left:10px;"></span>
							  <span id="lnb02_timeCal"></span>
							</div>
						</li>
					</ul>
					</span>
					<table style="background-color:#394253;text-align:center;width:280px;height:50px;">
						<tr>
							<td style="width:56px;"><span id="speed_prev"><font color='#2A303C'>-1x</font></span></td>
							<td style="width:56px;"><span id="rewind_btn"><img src="../images/search/common/btn/02.jpg" /></span></td>
							<td style="width:56px;"><span id="stepbackward_btn"><img src="../images/search/common/btn/btn_stepbackward_disable.jpg" /></span></td>
							<td style="width:56px;"><span id="stop_btn"><img src="../images/search/common/btn/03_disable.jpg" /></span></td>
							<td style="width:56px;"><span id="play_btn"><img src="../images/search/common/btn/04_disable.jpg" /></span></td>
							<td style="width:56px;"><span id="stepforward_btn"><img src="../images/search/common/btn/btn_stepforward_disable.jpg" /></span></td>
							<td style="width:56px;"><span id="ff_btn"><img src="../images/search/common/btn/05.jpg" /></span></td>
							<td style="width:56px;"><span id="speed_ff"><font color='#2A303C'>1x</font></span></td>
						</tr>
					</table>

					<div class="search_bottom" id="search_bottom_controls" >
						<div class="show_advanced search_view" style="padding-top:0px;">
							<?php if($GLOBALS['M_SUPPORT_AUDIO']) { ?>
							<div class="volume" style="background-color:#394253;height:50px;">
								<table style="margin-left:20px; height: 26px;">
									<colgroup>
										<col style="width:40px;"/>
										<col style="width:180px;"/>
									</colgroup>
									<tr>				
										<td>
											<a href="javascript:OnListenClick()" class="btn_type02a btn_type02_03" id="btnListen" ><img src="../images/common/btn/btn_sound.png" alt="" /></a>
										</td>
										<td valign="center" style="width:26px">
											<div id="slider-vol" style="width:180px; margin-left:12px; margin-top:-10px" ></div>
										</td>
									</tr>
								</table>
								<div style="left:57px;margin-top:-25px;position:absolute">
									<span style="width:30px;">-</span> 
									<span style="margin-left:195px; width:30px;">+</span>
								</div>
							</div>							
							<?php } ?>
							<div id="snapshotCompleted" style="position:absolute; width:270px; height:150px; left: 10px; top: 540px; background-color:#000000; display:none; z-index:1000">
								<p align="center">
									<br /> <br /> 
									<?php echo $t_savingCompleted2[$GLOBALS['LANGINDEX']]; ?>
									<br />
									<script>
										var msg = "C:\\Users\\{Current User}\\Pictures\\";
										if (BrowserDetect.OS == 'Mac') {
											msg = "~/Pictures/";
										}
										document.write(msg);
									</script>
									
								</p>
							</div>
							<div class="view_box" style="background-color:#394253;">
							<?php 	
							if($GLOBALS['M_SPECIAL_TYPE'] != 1) { ?>
								<a href="javascript:OnClickSnapshot()" class="btn_type01 btn_type01_05 mgr3" title="<?php echo $t_capture[$GLOBALS['LANGINDEX']]; ?>"><img src="../images/common/btn/btn_photo.png" /></a>
							<?php }?> 
								<?php if (GetBrowserName() == 'IE' || GetBrowserName() == 'Google Chrome') { ?>
								<a href="javascript:OnFullScreenClick()" class="btn_type01 btn_type01_05 mgr3" title="<?php echo $t_fullScreen[$GLOBALS['LANGINDEX']]; ?>"><img src="../images/common/btn/btn_expand.png" alt="" /></a>
								<?php } else {?>
								<a class="btn_type01_05_disable2 mgr3" title="<?php echo $t_fullScreen[$GLOBALS['LANGINDEX']]; ?>"><img src="../images/common/btn/btn_expand_disabled.png" alt="" /></a>
								<?php } ?>
								<a href="javascript:OnClickOriginal()" class="btn_type01 btn_type01_05 mgr2" title="1:1"><img src="../images/common/btn/btn_realsize.png" alt="" /></a>
								<a href="javascript:OnClickFitt()" class="btn_type01 btn_type01_05" title="<?php echo $t_fit[$GLOBALS['LANGINDEX']]; ?>"><img src="../images/common/btn/btn_updown.png" alt="" /></a>
							</div>
							<div class="view_box view_btm" style="background-color:#394253;height:50px;" >
								<a href="javascript:OnClickInfo()" class="btn_type01 btn_type01_03 mgr2" title="<?php echo $t_information[$GLOBALS['LANGINDEX']]; ?>"><img src="../images/common/btn/btn_i.png" alt="" /></a>
								<a href="javascript:OnClickBackup()" class="btn_type01 btn_type01_03" title="<?php echo $t_backup[$GLOBALS['LANGINDEX']]; ?>"><img src="../images/common/btn/btn_cd.png" alt="" /></a>
							</div>
						</div>
						<div class="lnb-btn">
							<a href="#"><img src="../images/common/btn/btn_lnb_arrow.gif" alt="" /></a>
						</div>
					</div>
				</div>
			</div>
			
			<div id="contents" >
				<div class="ficture">
					<span id="pluginArea"></span>
					<span id="timeBar"></span>
					<div id="timebarHtml">
						<div id="timebarCover">
								<span class="timebarLeft"><img src="../images/timeline/timeLineArrowLeft.png" ></span>
								<div id="timelineLeftBlank" style="width:11px;height:75px;float:left;position:relative;background:transparent;" ></div>
								<div id="timelineBar" >
									<ul id="timeLabel"  >
										<li>2:00</li><li>4:00</li><li>6:00</li><li>8:00</li><li>10:00</li><li class="timAcross">12:00</li><li>14:00</li><li>16:00</li><li>18:00</li><li>20:00</li><li>22:00</li>
									</ul>
									<div class="scrollCover timebartype1" >
										
										<span class="timeLineSeek"><img src="../images/timeline/timeLineSeek.png" ></span>
										<div class="timeLineDiv"></div>
									</div>
									<div id="timelineRightBlank" style="width:11px;height:75px;float:left;position:absolute;left:797px;background:#40495A;" ></div>
								</div>
								<span class="timebarRight"><img src="../images/timeline/timeLineArrowRight.png" ></span>
								<div class="timebarIncDec"><span class="timebarInc"><img src="../images/timeline/timeLineInc.png" ></span><span class="timebarDec"><img src="../images/timeline/timeLineDec.png" ></span></div>
						</div>
					</div>
				</div>
			</div>
			<style>
			.timeLineDiv {
				position: absolute;
				height: 42px;
				float: left;
				//width: 1604px;
				width: 797px;
				border-left: 1px solid #262b35;
				border-right: 1px solid #262b35;
			}
			.timeLineDiv div{
				background:red;height: 15px;width:1px;float:left;position:absolute;top: 1px;
			}
			.timeLineDiv div.tmRed{
				background:red;
			}
			.timeLineDiv div.tmBlue{
				background:#0099ff;
			}
			.timeLineDiv div.bottomAttch{
				top:26px;
			}
			#timebarHtml{
				clear: both;
				float: left;
				left: 305px;
				position: absolute;
				width: 900px;
			}
			.timebartype1{
				background:url("../images/timeline/timeLine1.png") repeat-x scroll 0 0 transparent;
			}
			.timebartype2{
				background:url("../images/timeline/timeLine22.png") repeat-x scroll 0 0 transparent;
			}
			#timelineBar{
				float: left;
				height: 75px;
				margin: 0 0px;
				overflow: hidden;
				position: relative;
				width: 808px;
				z-index: 101;
			}
			.timeLineSeek{
				float: left;
				height: 48px;
				left: 0;
				margin-top: -3px;
				position: absolute;
				width: 11px;
				z-index: 100;
			}
			.timebarIncDec{
				float: left;
				width: 30px;
				margin-left: 3px;
				margin-top: 20px;
			}
			.timebarInc, .timebarDec{
				float: left; width: 37px; height: 21px;
			}
			.timebarLeft, .timebarRight {
				float:left; width: 20px;
				margin-top: 20px;
			}
			.scrollCover{
				float: left;
				height: 50px;
				width: 797px;
				position: relative;
				z-index: 90;
			}
			ul#timeLabel { 
				display: block;
				float: left;
				height: 18px;
				width: 802px;
			}
			ul#timeLabel li{ 
				float: left;
				width: 66px;
				font-size:11px;
			}
			ul#timeLabel li:first-child{ padding-left: 55px; width: 68px} 
			#timelineBar ul.timeLabel2 { 
				float: left;
				height: 18px;
				width: 1602px;
			}
			#timelineBar ul.timeLabel2 li { 
				float: left;
				font-size: 11px;
				padding-right: 100px;
				width: 34px;
			}
			#timelineBar ul.timeLabel2 li:first-child{ padding-left: 120px; padding-right: 100px;} 
			#timelineBar ul.timeLabel2 .timAcross{ padding-left: 10px; padding-right: 85px;}
			#contents div.ficture {
				border: none;
			}
			</style>
			<script>
				$(function(){
					playback.timeline.init();			
				});
			</script>
		</div>
	</div>
</body>
</html>
