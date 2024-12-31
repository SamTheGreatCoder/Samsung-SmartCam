#mw_progress .bg { position:fixed; left:0; top:0; z-index:50; width:100%; height:100%; background-color:#000; opacity:.5; filter:alpha(opacity=50);}
<?php
require_once ('../../cgi-bin/adv/_define.inc');
CheckAdminAccount();
if (isset($_REQUEST['menu']))
{
	if ($_REQUEST['menu'] == 'NAS_Result')
	{
		class NetworkTest
		{
			public	$result;
			public	$payload;
			public	$headerInfo;

			function __construct($_action=ACTION_START)
			{
				$this->headerInfo = array('Command'=>CMD_NETWORK_TEST, 'Action'=>$_action);
			}

			function SetOperation($_operation)
			{
				$operArr = array('SMTP'=>0, 'FTP'=>1, 'DDNS'=>2, 'NAS'=>3, 'ISCSI'=>6, 'SMTP_Test'=>10, 'FTP_Test'=>11);
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
	else if ($_REQUEST['menu'] == 'ISCSI_Discovery')
	{
		require_once ('../../cgi-bin/adv/nas.class');
		$iscsiDiscovery = new ISCSIDiscovery();
		$socketManager = new SocketManager();
		$iscsiDiscovery->XMLtoArray($_REQUEST['message']);
		$iscsiDiscovery->headerInfo['Action'] = ACTION_START;
		$socketManager->Connection($iscsiDiscovery);

		$msg = '';
		for ($index=0; $index<MAX_IQN_LIST; ++$index) {
			if (trim($iscsiDiscovery->iqnList[$index]) == '') continue;
			$msg .= $iscsiDiscovery->iqnList[$index].'/';
		}
		echo $msg;
		exit;
	}
	else if ($_REQUEST['menu'] == 'ISCSI_Test') 
	{
		require_once ('../../cgi-bin/adv/nas.class');
		$iscsiConfig = new ISCSIConfiguration();
		$socketManager = new SocketManager();
		$iscsiConfig->headerInfo['Action'] = ACTION_START;
		$iscsiConfig->XMLtoArray($_REQUEST['message']);		
		$socketManager->Connection($iscsiConfig);
		echo $iscsiConfig->result;
		exit;
	}
}
require_once ('../language/language_menu.cgi');
require_once ('../language/language_event_sdrecord.cgi');
require_once ('../language/language_event_common.cgi');

$event_name	= 'storage';
$classInstances= GetClassInstance('storage');
$storageConf 	= $classInstances['StorageInfo'];
$recordConf 	= $classInstances['RecordConfiguration'];
$contRecord	= $classInstances['ContinuousRecord'];
$nasConf = NULL;
$iscsiConf = NULL;
$recordingEnable = 0;
$iscsiIQN = '';

if ($GLOBALS['M_SUPPORT_SD']) {
	if ($recordConf->dataInfo['Enabled']['value'] == 1 && $storageConf->storage[0]->dataInfo['TotalSize']['value'] != 0 && $storageConf->storage[0]->dataInfo['FreeSize']['value'] != 0)
		$recordingEnable = 1;
}

if ($GLOBALS['M_SUPPORT_NAS']) {
	$nasConf = $classInstances['NasConfiguration'];
	if ($nasConf->dataInfo['Enabled']['value'] == 1 && $storageConf->storage[1]->dataInfo['TotalSize']['value'] != 0 && $storageConf->storage[1]->dataInfo['FreeSize']['value'] != 0)
		$recordingEnable = 1;
}
if ($GLOBALS['M_SUPPORT_ISCSI']) {
	$iscsiConf = $classInstances['ISCSIConfiguration'];
	if ($iscsiConf->dataInfo['Enabled']['value'] == 1 && $storageConf->storage[2]->dataInfo['TotalSize']['value'] != 0 && $storageConf->storage[2]->dataInfo['FreeSize']['value'] != 0)
		$recordingEnable = 1;
	$iscsiIQN = $iscsiConf->dataInfo['IQN']['value'];
}
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="kr" xml:lang="kr">
<head>
	<title>iPOLiS NETWORK CAMERA WEBVIEWER</title>
	<meta http-equiv="X-UA-Compatible" content="IE=Edge; requiresActiveX=true">
	<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
	<link rel="stylesheet" type="text/css" href="../css/techwin.css" />
	<link rel="stylesheet" type="text/css" href="../css/jquery.ui.core.css"/>
	<link rel="stylesheet" type="text/css" href="../css/jquery.ui.theme.css"/>
	<link rel="stylesheet" type="text/css" href="../css/event_canvas.css" />
	<style>
		#lnb-list {
			height:1500px;
		}
		dl { overflow:hidden;}
		dt { float:left; margin-bottom:5px; width:150px; height:23px; font-weight:bold; line-height:23px; }
		dd { margin:0 0 5px; height:23px; line-height:23px;}
		dd label { display:inline-block; margin-right:10px;}

		.wn { float:left; width:40px; text-indent:15px; text-align:left;}
		.prt { float:left; width:50px;} 		
		.sgn { float:left; width:370px; }
		.st { float:right; width:200px; color:red;}
	</style>
	<script type="text/javascript" src="../js/jquery-1.9.1.js"></script>
	<script type="text/javascript" src="../js/lnb.js"></script>
	<script type="text/javascript" src="../js/common_function.js"></script>
	<script type="text/javascript" src="../js/jquery-ui.js"></script>
	<script type="text/javascript" src="../js/jquery.ui.dialog.js"></script>
	<script type="text/javascript" src="../js/timeSchedule.js"></script>
	<script type="text/javascript" src="../js/eventcontrol.js"></script>
	<script type="text/javascript">
	<?php if (!($GLOBALS['M_SUPPORT_SD'] || $GLOBALS['M_SUPPORT_NAS'] || $GLOBALS['M_SUPPORT_ISCSI'])) { ?>
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

<?php
	if (trim($nasConf->dataInfo['Password']['value'])=='') {
?>
	var NASPWset = false;
<?php
	}
	else 
	{
?>
	var NASPWset = true;
<?php
	}
?>

<?php
	if (trim($iscsiConf->dataInfo['Password']['value'])=='') {
?>
	var IQNPWset = false;
<?php
	}
	else 
	{
?>
	var IQNPWset = true;
<?php
	}
?>

	var NASPWInit = false;

	$(document).ready(function(){	
		lnbonoff("lnb_event");
	});

	var localSeq                            = <?php echo $_SESSION['count']; ?>;
	var ajaxReqUrl                          = "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq;

	var gTimerNAS = '', gTimerISCSI = '';
	var recordingEnable = <?php echo $recordingEnable; ?>;
	var oldRecordingMode = <?php echo $recordConf->dataInfo['RecordingMode']['value'];?>;
	var oldIQNtext = "<?php echo $iscsiIQN; ?>";
	var selectedIQN = '';
	var selectedNo = 0;
	var formatDisable = 1;
	var sdStatus = parseInt("<?php echo $storageConf->storage[0]->dataInfo['Status']['value']; ?>");
	var nasStatus = parseInt("<?php echo $storageConf->storage[1]->dataInfo['Status']['value']; ?>");
	var iscsiStatus = parseInt("<?php echo $storageConf->storage[2]->dataInfo['Status']['value']; ?>");
	var STORAGE_STATUS = {"None":1, "Error":2, "Stop":3, "Wait":4, "Formatting":5, "FormattingAll":6, "Ready":10, "Recording":11, "Full":13, "Lock":14};
	var storageList = ['SD', 'NAS', 'iSCSI'];
<?php if ($GLOBALS['M_SUPPORT_SD'] == 0) { ?>
	storageList.splice($.inArray('SD',storageList), 1);
<?php } ?>	
<?php if ($GLOBALS['M_SUPPORT_NAS'] == 0) { ?>
	storageList.splice($.inArray('NAS',storageList), 1);
<?php } ?>
<?php if ($GLOBALS['M_SUPPORT_ISCSI'] == 0) { ?>
	storageList.splice($.inArray('iSCSI',storageList), 1);
<?php } ?>

	var SDEnableValue = "<?php echo $recordConf->dataInfo['Enabled']['value']; ?>";
	var NASEnableValue = "<?php echo $nasConf->dataInfo['Enabled']['value']; ?>";
	
	function OnLoad()
	{

		//$('#NASPW').val(RequestGetConfig("ttttttttttttttttt1"));
		$("#RecordProfileID").html("<?php echo $recordConf->dataInfo['RecordProfileName']['value']; ?>");

		OnClickStorageDetail(storageList[0],true);

		OnClickRecordEnable(storageList[0]);

		for (var index=0; index<storageList.length; ++index) {
			SetStorageStatus(storageList[index]);
		}		
		OnChangeAutoRemoval(true);
		OnChangeOverWrite();

		if (NASPWset == true) {
			$("#NASPW").val("{::::::::}"); // key for maintain password
			NASPWInit = true;
		}
	}

	function SetStorageStatus(type) 
	{
		var totalSize = "0";
		var freeSize = "0";
		var status = STORAGE_STATUS.None;		
	
		if (type == 'SD') {
	<?php
		if ($recordConf->dataInfo['Enabled']['value'] == 1) {
	?>
			totalSize = "<?php echo $storageConf->storage[0]->dataInfo['TotalSize']['value']; ?>";
			freeSize = "<?php echo $storageConf->storage[0]->dataInfo['FreeSize']['value']; ?>";
			status = sdStatus;
			formatDisable = 0;
			if (nasStatus == STORAGE_STATUS.Formatting || nasStatus == STORAGE_STATUS.FormattingAll || iscsiStatus == STORAGE_STATUS.Formatting || iscsiStatus == STORAGE_STATUS.FormattingAll) {
				formatDisable = 1;
			}
	<?php
		}
	?>
		}

		if (type == 'NAS') {
	<?php
		if ($nasConf->dataInfo['Enabled']['value'] == 1) {
	?>
			totalSize = "<?php echo $storageConf->storage[1]->dataInfo['TotalSize']['value']; ?>";
			freeSize = "<?php echo $storageConf->storage[1]->dataInfo['FreeSize']['value']; ?>";
			status = nasStatus;
			formatDisable = 0;
			if (sdStatus == STORAGE_STATUS.Formatting || sdStatus == STORAGE_STATUS.FormattingAll || iscsiStatus == STORAGE_STATUS.Formatting || iscsiStatus == STORAGE_STATUS.FormattingAll) {
				formatDisable = 1;
			}
			DisableNASTest();
	<?php
		}
	?>
		}

		if (type == 'iSCSI') {
	<?php
		if ($iscsiConf->dataInfo['Enabled']['value'] == 1) {
	?>
			totalSize = "<?php echo $storageConf->storage[2]->dataInfo['TotalSize']['value']; ?>";
			freeSize = "<?php echo $storageConf->storage[2]->dataInfo['FreeSize']['value']; ?>";
			status = iscsiStatus;
			formatDisable = 0;
			if (sdStatus == STORAGE_STATUS.Formatting || sdStatus == STORAGE_STATUS.FormattingAll || nasStatus == STORAGE_STATUS.Formatting || nasStatus == STORAGE_STATUS.FormattingAll) {
				formatDisable = 1;
			}
	<?php
		}
	?>	
		}

		if(totalSize >= 1024*1024){
			totalSize = (totalSize / 1024 / 1024).toFixed(2);
			$("#"+type+"_TotalSize").html(totalSize+" TB");
		}
		else if(totalSize >= 1024){
			totalSize = (totalSize / 1024).toFixed(2);
			$("#"+type+"_TotalSize").html(totalSize+" GB");
		}
		else{
			$("#"+type+"_TotalSize").html(totalSize+" MB");
		}
		
		if(freeSize >= 1024*1024){
			freeSize = (freeSize / 1024 / 1024).toFixed(2);
			$("#"+type+"_FreeSize").html(freeSize+" TB");
		}
		else if(freeSize >= 1024){
			freeSize = (freeSize / 1024).toFixed(2);
			$("#"+type+"_FreeSize").html(freeSize+" GB");
		}
		else{
			$("#"+type+"_FreeSize").html(freeSize+" MB");
		}
		
		var statusText = "";
		switch (status){
			case STORAGE_STATUS.Lock:
				statusText = "<?php echo $t_lock[$GLOBALS['LANGINDEX']]; ?>";
				$("#"+type+"_Status").css("color","blue"); 
				break;	
			case STORAGE_STATUS.Full:
				statusText = "<?php echo $t_memoryFull[$GLOBALS['LANGINDEX']]; ?>";
				$("#"+type+"_Status").css("color","blue"); 
				break;
			case STORAGE_STATUS.Recording:
				statusText = "<?php echo $t_recording[$GLOBALS['LANGINDEX']]; ?>";
				$("#"+type+"_Status").css("color","blue"); 
				break;
			case STORAGE_STATUS.Ready: 
				statusText = "<?php echo $t_ready[$GLOBALS['LANGINDEX']]; ?>"; 
				$("#"+type+"_Status").css("color","blue"); 
				break;
			case STORAGE_STATUS.Formatting: case STORAGE_STATUS.FormattingAll:
				statusText = "<?php echo $t_formatting[$GLOBALS['LANGINDEX']]; ?>"; 
				$("#"+type+"_Status").css("color","blue"); 
				break;
			case STORAGE_STATUS.Error:
				statusText = "<?php echo $t_error[$GLOBALS['LANGINDEX']]; ?>"; 
				$("#"+type+"_Status").css("color","red"); 
				break;
			default :
				statusText = "<?php echo $t_none[$GLOBALS['LANGINDEX']]; ?>"; 
				break;
		}
		$("#"+type+"_Status").text(statusText);
		ChangeFormatStatus(type, status);
	}

	function CheckNas()
	{
		if ($("#NASIP").val() == '')
		{
			alert("<?php echo $msg_input_ip[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		if (!CheckValidIPv4Address($('#NASIP').val()))
		{
			alert("<?php echo $msg_chkIPAddress[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		
		if ($("#NASID").val() == '')
		{
			alert("<?php echo $msg_input_id[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}

		if (!TypeCheck($('#NASID').val(), ALPHA+NUM+SIM))
		{
			alert("<?php echo $msg_invalid_idpw[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}

		if(!($('#NASPW').val().length == 0 && NASPWset) && !NASPWInit)  
		{
			if($('#NASPW').val() != '')
			{
				if(!TypeCheck($('#NASPW').val(), ALPHA+NUM+SIM))
				{
					alert("<?php echo $msg_invalid_idpw[$GLOBALS['LANGINDEX']]; ?>");
					return false;
				}
			}
		}
		
		if ($("#NASDefaultFolder").val() == '')
		{
			alert("<?php echo $msg_input_folder[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}

		if(!TypeCheck($('#NASDefaultFolder').val(), ALPHA+NUM+NasDirectory))
		{
			alert("<?php echo $msg_invalid_folder[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}

		return true;
	}
	
	function OnClickApply()
	{
		var msg = "";
		var continuous_msg = "";
		var storage_msg = "";

		if (CheckScheduleSetting("<?php echo $event_name; ?>") == 0) {
			alert("<?php echo $msg_checkthetable[$GLOBALS['LANGINDEX']]; ?>");
			return; 
		}

		var removalPeriod = parseInt($('#RemovalPeriod').val());
		if(!(removalPeriod > 0 && removalPeriod < 181)){
			alert("<?php echo $msg_chkPeriodRange[$GLOBALS['LANGINDEX']]; ?>");
			$('#RemovalPeriod').focus();
			return;
		}
		 
	<?php 
		if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_HISILICON) { 
	?>
			if ( ( SDEnableValue == 0  &&  $("#SDEnable").val() == 1) || ( NASEnableValue == 0  &&  $("#NASEnable").val() == 1) ) {
				alert("<?php echo $msg_SDCapabilityLimit[$GLOBALS['LANGINDEX']]; ?>");			
			}
	<?php 
		} 
	?>	

	<?php 
		if ($GLOBALS['M_SUPPORT_NAS']) { 
	?>
			if($('#NASEnable').val() == "1"){
				if (CheckNas() == false) {
					$("#NAS").prop("checked", true);
					OnClickStorageDetail("NAS", false);
					return;
				}
			}
			
			RequestAjaxMsg(MakeNasXmlMsg("Set"), "", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, "NO_REFRESH", true, OnApplyTempSuccess);
			localSeq++;
	<?php 
		}
		
		if ($GLOBALS['M_SUPPORT_ISCSI']) {
	?>
			if($('#iSCSIEnable').val() == "1"){
				if (CheckISCSITest() == false || CheckSearchiSCSI() == false) {
					$("#iSCSI").prop("checked", true);
					OnClickStorageDetail("iSCSI", false);
					return;
				}
			}

			RequestAjaxMsg(MakeISCSIXmlMsg("SetISCSIConfiguration"), "", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, "NO_REFRESH", true, OnApplyTempSuccess);
			localSeq++;
	<?php 
		} 
	?>		
		
		continuous_msg = "<SetContinuousRecord>";
		continuous_msg += "<Normal>"+$("#Normal").val()+"</Normal>";
		continuous_msg += "<Event>"+$("#Event").val()+"</Event>";
		<?php if($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>	
		continuous_msg += MakeScheduleAndActionSetupXML_S1("<?php echo $event_name; ?>");
		<?php } else { ?>
		continuous_msg += MakeScheduleAndActionSetupXML("<?php echo $event_name; ?>");
		<?php } ?>

		
		continuous_msg += "</SetContinuousRecord>";

		storage_msg = "<SetRecordConfiguration>";
		<?php if ($GLOBALS['M_SUPPORT_SD']) { ?>
		storage_msg += "<Enabled>"+$("#SDEnable").val()+"</Enabled>";
		<?php } ?>
		storage_msg += "<OverWrite>"+($('#Overwrite').is(':checked') ? 1 : 0)+"</OverWrite>";
		storage_msg += "<PreAlarmDuration>"+$("#PreDuration").val()+"</PreAlarmDuration>";
		storage_msg += "<PostAlarmDuration>"+$("#PostDuration").val()+"</PostAlarmDuration>";
		storage_msg += "<RecordingMode>"+$('#RecordingMode').val()+"</RecordingMode>";
		storage_msg += "<AutoRemoval>"+($('#RemovalMode').is(':checked') ? 1 : 0)+"</AutoRemoval>";
		storage_msg += "<RemovalPeriod>"+$('#RemovalPeriod').val()+"</RemovalPeriod>";
		storage_msg += "<RemovalPeriodUnit>"+"0"+"</RemovalPeriodUnit>";
		storage_msg += "<SDFileSystem>"+$('#SD_fileSystem').val()+"</SDFileSystem>";
		storage_msg += "</SetRecordConfiguration>";
		
		if(($("#RecordingMode").val() != oldRecordingMode) && recordingEnable == 1) {				
			if(confirm("<?php echo $msg_storage_format[$GLOBALS['LANGINDEX']]; ?>")) {
				RequestAjaxMsg(continuous_msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, "NO_REFRESH", true, OnApplyTempSuccess);
				localSeq++;
				RequestAjaxMsg(storage_msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, "TIMEOUT_REFRESH");
			}
			else {
				return;
			}
		}
		else if($("#SD_fileSystem").val() != <?php echo $recordConf->dataInfo['SDFileSystem']['value']; ?> && $("#SDEnable").val() == 1 && recordingEnable == 1)
		{
			var confirmMsg = "<?php echo $msg_storage_format2[$GLOBALS['LANGINDEX']]; ?>";
			<?php if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_HISILICON) { ?>
			if ($("#SD_fileSystem").val() == 2) { // ext4
				confirmMsg += "\n" + "<?php echo $msg_storage_format3[$GLOBALS['LANGINDEX']]; ?>";
			}
			<?php } ?>
			if(confirm(confirmMsg)) {
				RequestAjaxMsg(continuous_msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, "NO_REFRESH", true, OnApplyTempSuccess);
				localSeq++;
				RequestAjaxMsg(storage_msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, "TIMEOUT_REFRESH");
			}
			else {
				return;
			}
		}
		else{
			RequestAjaxMsg(continuous_msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, "NO_REFRESH", true, OnApplyTempSuccess);
			localSeq++;
			RequestAjaxMsg(storage_msg, "<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, "TIMEOUT_REFRESH");
		}
	}

	function OnClickNasTest()
	{
		if (CheckNas() == false) return;
		DisableNASTest();
		$('#NAS_Connection').text("(<?php echo $msg_test_connecting[$GLOBALS['LANGINDEX']]; ?>)");
		
		RequestAjaxMsg(MakeNasXmlMsg("Start"), "", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, "NO_REFRESH", true);
		localSeq++;
		gTimerNAS = setTimeout('TestNAS()', 500);
	}

	function MakeNasXmlMsg(cmd)
	{
		var msg = "<"+cmd+"NasConfiguration>";
		msg += "<Enabled>"+$("#NASEnable").val()+"</Enabled>";
		msg += "<IPAddress>"+$("#NASIP").val()+"</IPAddress>";
		msg += "<Id>"+$("#NASID").val()+"</Id>";
		if(!($('#NASPW').val().length == 0 && NASPWset))
		{
			msg += "<Password>"+$("#NASPW").val()+"</Password>";
		}
		var nasDefaultfolder = $("#NASDefaultFolder").val();
		nasDefaultfolder = nasDefaultfolder.replace(/\+/gm, '&#43;');
		nasDefaultfolder = nasDefaultfolder.replace(/&/gm, '&amp;');
		msg += "<DefaultFolder>"+nasDefaultfolder+"</DefaultFolder>";
		msg += "</"+cmd+"NasConfiguration>";
		return msg;
	}

	function TestNAS()
	{
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
			data: "menu=NAS_Result&operation=NAS",
			success: OnSuccessNasResult,
			error: OnFailNasResult
		});
	}

	function OnSuccessNasResult(req)
	{
		var nasResult = req;
		switch (nasResult) {
			case '0': $('#NAS_Connection').text("(<?php echo $msg_fail[$GLOBALS['LANGINDEX']]; ?>)");			break;
			case '1': $('#NAS_Connection').text("(<?php echo $msg_success[$GLOBALS['LANGINDEX']]; ?>)");		break;
			case '2': $('#NAS_Connection').text("(<?php echo $msg_test_connecting[$GLOBALS['LANGINDEX']]; ?>)");	break;
			case '3': $('#NAS_Connection').text("(<?php echo $msg_success[$GLOBALS['LANGINDEX']]; ?>)");		break;	// Already mount
		}
		gTimerNAS = setTimeout('TestNAS()', 1000);
		if (nasResult != 2) clearTimeout(gTimerNAS);

		DisableNASTest();
	}

	function OnFailNasResult(req)
	{
		gTimerNAS = setTimeout('TestNAS()', 1000);
	}

	function OnClickStorageDetail(type, isOnload)
	{
		for (var index=0; index<storageList.length; ++index) {
			if (type == storageList[index]) {
				$('#'+type).prop('checked', true);
				$('#'+type+'Enable').removeAttr('disabled');
				$('.data_table .'+type+' td').css('color', '#1c1c1c');
				$('#'+type+'Detail').show();
			}
			else {
				$('#'+storageList[index]).prop('checked', false);
				$('#'+storageList[index]+'Enable').attr('disabled', 'disabled');	
				$('.data_table .'+storageList[index]+' td').css('color', '#6d6d6d');
				$('#'+storageList[index]+'Detail').hide();
			}
		}
		ChangeFormatStatus(type, eval(type.toLowerCase()+"Status"));

		if (type == 'iSCSI') {
			if (oldIQNtext != '') {
				$('#'+type+'Detail').hide();
				$('#'+type+'RegisterArea').show();
			}
			else {
				$('#'+type+'Detail').show();
				$('#'+type+'RegisterArea').hide();
				$("#iSCSIRegister").removeAttr('href');
				$("#iSCSIRegister").attr('class','btn_disable');
			}
		}
		
		if(!isOnload){
			$('#ContinuousRecordingScheduleTable').hide();
			setTimeout(function(){
					$('#ContinuousRecordingScheduleTable').show();
					setTimeout("OnClickActivationTime()", 500);
			}, 100);
		}
	}

	function OnClickRecordEnable(type){

		var sdEnable = $("#SDEnable").val();
		var nasEnable = $("#NASEnable").val();
		var iscsiEnable = $("#iSCSIEnable").val();		

		 if(type == "SD"){
			if(sdEnable == 0){
   				//Off
				$("#Normal").attr('disabled', 'disabled');
				$("#Event").attr('disabled', 'disabled');
				$("#PreDuration").attr('disabled', 'disabled');
				$("#PostDuration").attr('disabled', 'disabled');
				$("#RecordingMode").attr('disabled', 'disabled');
				$("#Overwrite").attr('disabled', 'disabled');
				$("#RemovalMode").attr('disabled', 'disabled');
				$("#RemovalPeriod").attr('disabled', 'disabled');
			}else{
				//On
				$("#Normal").removeAttr('disabled');
				$("#Event").removeAttr('disabled');
				$("#PreDuration").removeAttr('disabled');
				$("#PostDuration").removeAttr('disabled');
				$("#RecordingMode").removeAttr('disabled');
				$("#Overwrite").removeAttr('disabled');

				if($('#Overwrite').is(':checked') == false)
				{					
					$("#RemovalMode").attr('disabled', 'disabled');
					$("#RemovalPeriod").attr('disabled', 'disabled');
				}
				else
				{			
					$("#RemovalMode").removeAttr('disabled');
					if($("#RemovalMode").is(':checked') == false)
					{
						$("#RemovalPeriod").attr('disabled', 'disabled');
					}
					else
					{
						$("#RemovalPeriod").removeAttr('disabled');
					}			
				}
			}

			if(sdStatus == STORAGE_STATUS.Formatting || sdStatus == STORAGE_STATUS.FormattingAll)
			{
				$("#SDEnable").attr('disabled', 'disabled');
			}
		}
		
		 if(type == "NAS"){
			if(nasEnable == 0){
				$("#Normal").attr('disabled', 'disabled');			
				$("#Event").attr('disabled', 'disabled');
				$("#PreDuration").attr('disabled', 'disabled');
				$("#PostDuration").attr('disabled', 'disabled');
				$("#RecordingMode").attr('disabled', 'disabled');
				$("#Overwrite").attr('disabled', 'disabled');
				$("#RemovalMode").attr('disabled', 'disabled');
				$("#RemovalPeriod").attr('disabled', 'disabled');
			}else{
				$("#Normal").removeAttr('disabled');
				$("#Event").removeAttr('disabled');
				$("#PreDuration").removeAttr('disabled');
				$("#PostDuration").removeAttr('disabled');
				$("#RecordingMode").removeAttr('disabled');
				$("#Overwrite").removeAttr('disabled');
				
				if($('#Overwrite').is(':checked') == false)
				{					
					$("#RemovalMode").attr('disabled', 'disabled');
					$("#RemovalPeriod").attr('disabled', 'disabled');
				}
				else
				{			
					$("#RemovalMode").removeAttr('disabled');
					if($("#RemovalMode").is(':checked') == false)
					{
						$("#RemovalPeriod").attr('disabled', 'disabled');
					}
					else
					{
						$("#RemovalPeriod").removeAttr('disabled');
					}			
				}		
			}

			if(nasStatus == STORAGE_STATUS.Formatting || nasStatus == STORAGE_STATUS.FormattingAll)
			{
				$("#NASEnable").attr('disabled', 'disabled');
			}
		}

		 if(type == "iSCSI"){
			if(iscsiEnable == 0){
				$("#Normal").attr('disabled', 'disabled');			
				$("#Event").attr('disabled', 'disabled');
				$("#PreDuration").attr('disabled', 'disabled');
				$("#PostDuration").attr('disabled', 'disabled');
				$("#RecordingMode").attr('disabled', 'disabled');
				$("#Overwrite").attr('disabled', 'disabled');
				$("#RemovalMode").attr('disabled', 'disabled');
				$("#RemovalPeriod").attr('disabled', 'disabled');
			}else{
				$("#Normal").removeAttr('disabled');
				$("#Event").removeAttr('disabled');
				$("#PreDuration").removeAttr('disabled');
				$("#PostDuration").removeAttr('disabled');
				$("#RecordingMode").removeAttr('disabled');
				$("#Overwrite").removeAttr('disabled');
				
				if($('#Overwrite').is(':checked') == false)
				{					
					$("#RemovalMode").attr('disabled', 'disabled');
					$("#RemovalPeriod").attr('disabled', 'disabled');
				}
				else
				{			
					$("#RemovalMode").removeAttr('disabled');
					if($("#RemovalMode").is(':checked') == false)
					{
						$("#RemovalPeriod").attr('disabled', 'disabled');
					}
					else
					{
						$("#RemovalPeriod").removeAttr('disabled');
					}			
				}		
			}
		}

	}

	function ChangeFormatStatus(type, status)
	{
		if (status == STORAGE_STATUS.None || status == STORAGE_STATUS.Stop || status == STORAGE_STATUS.Formatting || status == STORAGE_STATUS.Formatting || formatDisable == 1) {
			$("#"+type+"Format").removeAttr('href');
			$("#"+type+"Format").attr('class','btn_disable');
		}
		else {
			$("#"+type+"Format").attr('href',"javascript:SetFormat('"+type+"')");
			$("#"+type+"Format").attr('class','btn_type01');
		}
	}
	
	function DisableNASTest()
	{ 
		if (nasStatus == STORAGE_STATUS.None || nasStatus == STORAGE_STATUS.Stop)
		{
			$("#NASIP").removeAttr('disabled');
			$("#NASID").removeAttr('disabled');
			$("#NASPW").removeAttr('disabled');
			$("#NASDefaultFolder").removeAttr('disabled');

			$("#NASTest").attr('href',"javascript:OnClickNasTest()");
			$("#NASTest").attr('class','btn_type01');
		}
		else
		{
			// mounted
			$("#NASIP").attr('disabled','disabled');
			$("#NASID").attr('disabled','disabled');
			$("#NASPW").attr('disabled','disabled');
			$("#NASDefaultFolder").attr('disabled','disabled');

			$("#NASTest").removeAttr('href');
			$("#NASTest").attr('class','btn_disable');
		}
	}

	function CheckSearchiSCSI()
	{
		if ($("#iSCSIIP").val() == '')
		{
			alert("<?php echo $msg_input_ip[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		
		if (!CheckValidIPv4Address($('#iSCSIIP').val()))
		{
			alert("<?php echo $msg_chkIPAddress[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		
		return true;		
	}

	function OnClickSearch()
	{
		if (CheckSearchiSCSI() == false) return;

		$('#iSCSI_list').empty();

		var msg = MakeISCSIXmlMsg("StartISCIDiscovery")
		var reqUrl = "<?php echo GetMyRequestURI($_SERVER['SCRIPT_NAME']); ?>";
		if (BrowserDetect.browser == "Explorer" || (BrowserDetect.browser == 'Safari' && reqUrl.search('.local') != -1)) {
			reqUrl = ".."+reqUrl.substr(reqUrl.indexOf("/setup/"));
		}

		var response = $.ajax({
			type: "POST",
			async: false,
			cache: false,
			url: reqUrl,
			dataType: "text",
			data: "menu=ISCSI_Discovery&message="+encodeURIComponent(msg)
		}).responseText.replace(/&/gm, '&amp;');
		
		OnSuccessDiscoveryISCSI(response);
	}

	function OnSuccessDiscoveryISCSI(response)
	{
		var listArray = response.split("/");
		for(var index=0; index<(listArray.length-1); index++) {
			var iscsiList = "<li style='text-align:center; border-bottom:1px solid #8e939e; height:25px; padding-top:5px; color:black;'>\
									<span class='wn'><input type='radio' id='iqn_"+index+"' name='iqnList' value='"+index+"'/></span>\
									<span class='prt'>"+(index+1)+"</span>\
									<span class='sgn' id='iqnTxt_"+index+"'>"+listArray[index]+"</span>\
									<span class='st' id='iqnStatus_"+index+"'></span>\
								  </li>";
			$('#iSCSI_list').append(iscsiList);
		}

		if (listArray.length > 0) {
			$('#iqn_0').prop('checked',true);
		}

		$("#iSCSIRegister").attr('href',"javascript:OnClickISCSIRegister()");
		$("#iSCSIRegister").attr('class','btn_type01');
	}

	function OnChangeAutoRemoval(isOnload)
	{
		if($("#RemovalMode").is(':checked') == false)
		{
			var removalPeriod = parseInt($('#RemovalPeriod').val());
			if(!(removalPeriod > 0 && removalPeriod < 181)){
				alert("<?php echo $msg_chkPeriodRange[$GLOBALS['LANGINDEX']]; ?>");
				$("#RemovalMode").prop('checked', true);
				$('#RemovalPeriod').focus();
				return;
			}
		
			$("#RemovalPeriod").attr('disabled', 'disabled');
		}
		else
		{
			var r = true;
			if(isOnload == false){
				r = confirm("<?php echo $msg_record_delete[$GLOBALS['LANGINDEX']]; ?>");
			}
			if(r){
				$("#RemovalPeriod").removeAttr('disabled');
			}
			else{
				$("#RemovalMode").prop('checked', false);
			}
		}
	}

	function OnChangeOverWrite()
	{
		if($('#Overwrite').is(':checked') == false)
		{				
			var removalPeriod = parseInt($('#RemovalPeriod').val());
			if(!(removalPeriod > 0 && removalPeriod < 181)){
				alert("<?php echo $msg_chkPeriodRange[$GLOBALS['LANGINDEX']]; ?>");
				$("#Overwrite").prop('checked', true);
				$('#RemovalPeriod').focus();
				return;
			}			
			$("#RemovalMode").attr('disabled', 'disabled');
			$("#RemovalPeriod").attr('disabled', 'disabled');
		}
		else
		{			
			$("#RemovalMode").removeAttr('disabled');
			if($("#RemovalMode").is(':checked') == false)
			{
				$("#RemovalPeriod").attr('disabled', 'disabled');
			}
			else
			{
				$("#RemovalPeriod").removeAttr('disabled');
			}			
		}
	}

	function OnChangeNasISCSIEnable(storage)
	{
		var nas = parseInt($('#NASEnable').val());
		var iscsi = parseInt($('#iSCSIEnable').val());

		if (iscsi == 1) {
			$("#delete_iqn").removeAttr('href');
			$("#delete_iqn").attr('class','btn_disable');
		}
		else {
			$("#delete_iqn").attr('href',"javascript:OnClickDeleteIQN()");
			$("#delete_iqn").attr('class','btn_type01');
		}
			
		if(iscsi == 1 && nas == 1) {	
			if(storage == 'iSCSI') {
				$('#NASEnable').val(0);					
				$('#NASEnable').trigger('change');
			}
			else if(storage == 'NAS') {
				$('#iSCSIEnable').val(0);
				$('#iSCSIEnable').trigger('change');
			}
			alert("<?php echo $msg_errNASandiscsiUse[$GLOBALS['LANGINDEX']]; ?>");
		}
		else {
			return;
		}
	}

	function CheckISCSITest() 
	{
		if($('#iqnID').val() != '')
		{
			if (!TypeCheck($('#iqnID').val(), ALPHA+NUM+SIM))
			{
				alert("<?php echo $msg_invalid_idpw[$GLOBALS['LANGINDEX']]; ?>");
				return false;
			}
		}

		if(!($('#iqnPW').val().length == 0 && IQNPWset))  
		{
			if($('#iqnPW').val() != '')
			{
				if(!TypeCheck($('#iqnPW').val(), ALPHA+NUM+SIM))
				{
					alert("<?php echo $msg_invalid_idpw[$GLOBALS['LANGINDEX']]; ?>");
					return false;
				}
			}
		}
		return true;		
	}

	function MakeISCSIXmlMsg(cmd)
	{
		var msg = "<"+cmd+">";
		msg += "<Enabled>"+$("#iSCSIEnable").val()+"</Enabled>";
		msg += "<Idx>"+selectedNo+"</Idx>";
		msg += "<Port>"+$("#iSCSIPort").val()+"</Port>";
		msg += "<IPAddress>"+$("#iSCSIIP").val()+"</IPAddress>";
		msg += "<IQN>"+selectedIQN+"</IQN>";
		msg += "<ID>"+$("#iqnID").val()+"</ID>";
		if(!($('#iqnPW').val().length == 0 && IQNPWset))
		{
			msg += "<Password>"+$("#iqnPW").val()+"</Password>";
		}
		msg += "</"+cmd+">";
		
		return msg;
	}

	function OnClickISCSIRegister() 
	{		
		if (CheckISCSITest() == false) return;

		$("#iSCSIRegister").removeAttr('href');
		$("#iSCSIRegister").attr('class','btn_disable');
		
		selectedNo = $("input[name='iqnList']:checked").val();
		selectedIQN = $('#iqnTxt_'+selectedNo).text();
		msg = MakeISCSIXmlMsg("StartISCSIConfiguration");

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
			data: "menu=ISCSI_Test&message="+msg,
			success: OnSuccessISCSIResult,
			error: OnFailISCSIResult
		});
	}
	
	function OnSuccessISCSIResult(req)
	{
		var result = parseInt(req);
		switch (result) {			
			case 0 : $('#iqnStatus_'+selectedNo).text("<?php echo $msg_success[$GLOBALS['LANGINDEX']]; ?>");	break;
			case 1 : $('#iqnStatus_'+selectedNo).text("<?php echo $msg_invalid_idpw[$GLOBALS['LANGINDEX']]; ?>");	break;
			default: $('#iqnStatus_'+selectedNo).text("<?php echo $msg_fail[$GLOBALS['LANGINDEX']]; ?>");		break;
		}

		$("#iSCSIRegister").attr('href',"javascript:OnClickISCSIRegister()");
		$("#iSCSIRegister").attr('class','btn_type01');
		
		/*
		if (result == 0) {
			$('#iSCSIDetail').hide();
			$('#iSCSIRegisterArea').show();
			
			$('#register_iqn').text(selectedIQN);
			$('#register_ip').text($('#iSCSIIP').val());
			$('#register_port').text($('#iSCSIPort').val());
		}
		*/
	}

	function OnFailISCSIResult(req)
	{
		gTimerISCSI = setTimeout('OnClickISCSIRegister()', 1000);
	}

	function OnClickDeleteIQN() 
	{
		if (confirm("<?php echo $msg_iqnListDelete[$GLOBALS['LANGINDEX']]; ?>")) {

			var msg = "<SetISCSIConfiguration>";
			msg += "<Idx>0</Idx>";
			msg += "<IPAddress></IPAddress>";
			msg += "<IQN></IQN>";
			msg += "<ID></ID>";
			msg += "<Password></Password>";
			msg += "</SetISCSIConfiguration>";

			RequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, "NO_REFRESH", false);
			localSeq++;

			oldIQNtext = "";
			OnClickStorageDetail('iSCSI', false);
			SetStorageStatus('iSCSI');
		}
	}

	function SetFormat(type)
	{
		var msg = "";
		
		if (type == 'SD')
		{
			if (SDEnableValue == 0)
			{
				alert("<?php echo $msg_fail[$GLOBALS['LANGINDEX']]; ?>");
				return;
			}

			if(sdStatus == STORAGE_STATUS.Wait)
			{
				alert("<?php echo $msg_SDLock[$GLOBALS['LANGINDEX']]; ?>");
				return;
			}
			
			var confirmMsg = "<?php echo $msg_start_format[$GLOBALS['LANGINDEX']]; ?>";
			<?php if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_HISILICON) { ?>
			if ($("#SD_fileSystem").val() == 2) { // ext4
				confirmMsg += "\n" + "<?php echo $msg_storage_format3[$GLOBALS['LANGINDEX']]; ?>";
			}
			<?php } ?>

			if (confirm(confirmMsg))
			{
				msg = "";
				msg += "<StartFormat>";
				msg += "<StorageToken>"+"<?php echo $storageConf->storage[0]->dataInfo['StorageToken']['value']; ?>"+"</StorageToken>";
				//msg += "<FileSystem>"+"<?php echo $storageConf->storage[0]->dataInfo['FileSystem']['value']; ?>"+"</FileSystem>";
				msg += "<FileSystem>"+$("#SD_fileSystem").val()+"</FileSystem>";
				msg += "</StartFormat>";
			}
			else {
				return;
			}
		}
		else if (type == 'NAS') {
			if (NASEnableValue == 0)
			{
				alert("<?php echo $msg_fail[$GLOBALS['LANGINDEX']]; ?>");
				return;
			}

			if (confirm("<?php echo $msg_nas_format[$GLOBALS['LANGINDEX']]; ?>"))
			{
				msg = "";
				msg += "<RemoveNasConfiguration>";
				msg += "<Enabled>"+$("#NASEnable").val()+"</Enabled>";
				msg += "<IPAddress>"+$("#NASIP").val()+"</IPAddress>";
				msg += "<Id>"+$("#NASID").val()+"</Id>";
				msg += "<Password>"+$("#NASPW").val()+"</Password>";
				msg += "<DefaultFolder>"+$("#NASDefaultFolder").val()+"</DefaultFolder>";
				msg += "</RemoveNasConfiguration>";
			}
			else {
				return;
			}
		}
		else {
			if (confirm("<?php echo $msg_nas_format[$GLOBALS['LANGINDEX']]; ?>"))
			{
				msg = "<RemoveISCSIConfiguration/>";
			}
			else {
				return;
			}
		}

		RequestAjaxMsg(msg, "<?php echo $msg_success[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, 'Format');
	}

	function DoNASPWInit()
	{
		if(NASPWInit == true) {
			$("#NASPW").val("");
			NASPWInit = false;
		}
	}

	function OnApplyTempSuccess()
	{
		// do nothing
	}
	</script>

</head>
<body onload="OnLoad()" onselectstart="return false">
	<div id="wrap">
		<?php
			require_once ('left_menu.cgi');
			require_once ('top_menu.cgi');
		?>
		<div id="container" >
		<?php
			PrintLeftMenu($_SERVER['SCRIPT_NAME']);
		?>
			<div id="contents" style="width:680px;">
				<div class="h3_tit mgt0" >
					<h3 class="wid320"> <?php echo $t_storageActionSetup[$GLOBALS['LANGINDEX']]; ?> </h3>
				</div>

				<table class="data_table">
					<colgroup>
						<col style="width:20px;"/>
						<col style="width:85px;" />
						<col style="width:105px;" />
						<!-- col style="width:97px;" /-->
						<!-- col style="width:93px;" /-->
						<col style="width:85px;" />
						<col style="width:85px;" />
						<col style="width:85px;" />
						<col style="width:110px;"/>
					</colgroup>
					<thead>
						<tr>
							<th></th>
							<th><?php echo $t_device[$GLOBALS['LANGINDEX']]; ?></th>
							<th><?php echo $t_record[$GLOBALS['LANGINDEX']]; ?></th>
							<th><?php echo $t_freeSize[$GLOBALS['LANGINDEX']]; ?></th>
							<th><?php echo $t_totalSize[$GLOBALS['LANGINDEX']]; ?></th>
							<th><?php echo $t_status[$GLOBALS['LANGINDEX']]; ?></th>
							<th></th>
						</tr>
					</thead>
					<tbody>
						<?php if ($GLOBALS['M_SUPPORT_SD']) { ?>
						<tr class="SD">
							<td><input type="radio" name="StorageList" id="SD" value="1" onclick="OnClickStorageDetail('SD',false);OnClickRecordEnable('SD');"/></td>
							<td>SD</td>
							<td>
								<select id="SDEnable" style="width:110px;" onchange="OnClickRecordEnable('SD');">
									<option value="0" <?php if($recordConf->dataInfo['Enabled']['value'] == 0) echo "selected=\"selected\""; ?>><?php echo $t_off[$GLOBALS['LANGINDEX']]; ?></option>
									<option value="1" <?php if($recordConf->dataInfo['Enabled']['value'] == 1) echo "selected=\"selected\""; ?>><?php echo $t_on[$GLOBALS['LANGINDEX']]; ?></option>
								</select>
							</td>
							<td><span id="SD_FreeSize" class="style6"></span></td>
							<td><span id="SD_TotalSize" class="style6"></span></td>
							<td><span id="SD_Status" class="style6"></span></td>
							<td><a id="SDFormat" href="javascript:SetFormat('SD')" class="btn_type01"><?php echo $t_format[$GLOBALS['LANGINDEX']]; ?></a></td>
							<script>
								$('#SDEnable').styledSelect({innerClass:"selectbox_style_option"});
							</script>
						</tr>
						<?php } ?>
						<?php if ($GLOBALS['M_SUPPORT_NAS']) { ?>
						<tr class="NAS">
							<td><input type="radio" name="StorageList" id="NAS" value="1" onclick="OnClickStorageDetail('NAS',false);OnClickRecordEnable('NAS');" /></td>
							<td>NAS</td>
							<td>
								<select id="NASEnable" style="width:110px;" onchange="OnChangeNasISCSIEnable('NAS');OnClickRecordEnable('NAS');">
									<option value="0" <?php if($nasConf->dataInfo['Enabled']['value'] == 0) echo "selected=\"selected\""; ?>><?php echo $t_off[$GLOBALS['LANGINDEX']]; ?></option>
									<option value="1" <?php if($nasConf->dataInfo['Enabled']['value'] == 1) echo "selected=\"selected\""; ?>><?php echo $t_on[$GLOBALS['LANGINDEX']]; ?></option>
								</select>
							</td>
							<td><span id="NAS_FreeSize" class="style6"></span></td>
							<td><span id="NAS_TotalSize" class="style6"></span></td>
							<td><span id="NAS_Status" class="style6"></span></td>
							<td><a href="javascript:SetFormat('NAS')" id="NASFormat" class="btn_type01"><?php echo $t_format[$GLOBALS['LANGINDEX']]; ?></a></td>
							<script>
								$('#NASEnable').styledSelect({innerClass:"selectbox_style_option"});
							</script>
						</tr>
						<?php } ?>
						<?php if ($GLOBALS['M_SUPPORT_ISCSI']) { ?>
						<tr class="iSCSI">						
							<td><input type="radio" name="StorageList" id="iSCSI" value="1" onclick="OnClickStorageDetail('iSCSI',false);OnClickRecordEnable('iSCSI');" /></td>
							<td>iSCSI</td>
							<td>
								<select id="iSCSIEnable" style="width:110px;" onchange="OnChangeNasISCSIEnable('iSCSI');OnClickRecordEnable('iSCSI');">
									<option value="0" <?php if($iscsiConf->dataInfo['Enabled']['value'] == 0) echo "selected=\"selected\""; ?>><?php echo $t_off[$GLOBALS['LANGINDEX']]; ?></option>
									<option value="1" <?php if($iscsiConf->dataInfo['Enabled']['value'] == 1) echo "selected=\"selected\""; ?>><?php echo $t_on[$GLOBALS['LANGINDEX']]; ?></option>
								</select>
							</td>
							<td><span id="iSCSI_FreeSize" class="style6"></span></td>
							<td><span id="iSCSI_TotalSize" class="style6"></span></td>
							<td><span id="iSCSI_Status" class="style6"></span></td>
							<td><a id="iSCSIFormat" href="javascript:SetFormat('iSCSI')" class="btn_type01"><?php echo $t_format[$GLOBALS['LANGINDEX']]; ?></a></td>							
							<script>
								$('#iSCSIEnable').styledSelect({innerClass:"selectbox_style_option"});
							</script>
						</tr>
						<?php } ?>
					</tbody>
				</table>
				<table id="recordSetup" class="data_write mgt20">
					<colgroup>
						<col style="width:225px;"/>
						<col />
					</colgroup>
					<tbody>
						<tr>
							<th scope="row"> <?php echo $t_recordProfile[$GLOBALS['LANGINDEX']]; ?> </th>
							<td><span id="RecordProfileID"></span></td>
						</tr>						
						<tr>
							<th><?php echo $t_normal[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<select id="Normal" style="width:165px; height:22px; background-color:#868fa3; color:#1c1c1c;" >
									<option value="0" <?php if($contRecord->dataInfo['Normal']['value'] == 0) echo "selected=\"selected\""; ?>> <?php echo $t_none[$GLOBALS['LANGINDEX']]; ?></option>
									<option value="1" <?php if($contRecord->dataInfo['Normal']['value'] == 1) echo "selected=\"selected\""; ?>> <?php echo $t_fullFrame[$GLOBALS['LANGINDEX']]; ?></option>
									<option value="2" <?php if($contRecord->dataInfo['Normal']['value'] == 2) echo "selected=\"selected\""; ?>> <?php echo $t_iFrame[$GLOBALS['LANGINDEX']]; ?></option>
								</select>
							</td>
						</tr>
						<tr>
							<th><?php echo $t_event[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<select id="Event" style="width:165px; height:22px; background-color:#868fa3; color:#1c1c1c;" >
									<option value="1" <?php if($contRecord->dataInfo['Event']['value'] == 1) echo "selected=\"selected\""; ?>> <?php echo $t_fullFrame[$GLOBALS['LANGINDEX']]; ?></option>
									<option value="2" <?php if($contRecord->dataInfo['Event']['value'] == 2) echo "selected=\"selected\""; ?>> <?php echo $t_iFrame[$GLOBALS['LANGINDEX']]; ?></option>
								</select>
							</td>
						</tr>
						<tr>
							<th scope="row"> <?php echo $t_preEventDuration[$GLOBALS['LANGINDEX']]; ?> </th>
							<td>
								<select name="select" id="PreDuration" style="width:165px; height:22px; background-color:#868fa3; color:#1c1c1c;" >
						         <option value="1" <?php if($recordConf->dataInfo['PreAlarmDuration']['value'] == 1) echo "selected=\"selected\""; ?>>1 <?php echo $t_seconds[$GLOBALS['LANGINDEX']]; ?></option>
									<option value="3" <?php if($recordConf->dataInfo['PreAlarmDuration']['value'] == 3) echo "selected=\"selected\""; ?>>3 <?php echo $t_seconds[$GLOBALS['LANGINDEX']]; ?></option>
									<option value="5" <?php if($recordConf->dataInfo['PreAlarmDuration']['value'] == 5) echo "selected=\"selected\""; ?>>5 <?php echo $t_seconds[$GLOBALS['LANGINDEX']]; ?></option>
								</select>
							</td>
						</tr>
						<tr>
							<th scope="row"> <?php echo $t_postEventDuration[$GLOBALS['LANGINDEX']]; ?> </th>
							<td>
								<select name="select" id="PostDuration" style="width:165px; height:22px; background-color:#868fa3; color:#1c1c1c;" >
						         <option value="5" <?php if($recordConf->dataInfo['PostAlarmDuration']['value'] == 5) echo "selected=\"selected\""; ?> >5 <?php echo $t_seconds[$GLOBALS['LANGINDEX']]; ?></option>
									<option value="10" <?php if($recordConf->dataInfo['PostAlarmDuration']['value'] == 10) echo "selected=\"selected\""; ?> >10 <?php echo $t_seconds[$GLOBALS['LANGINDEX']]; ?></option>
									<option value="30" <?php if($recordConf->dataInfo['PostAlarmDuration']['value'] == 30) echo "selected=\"selected\""; ?> >30 <?php echo $t_seconds[$GLOBALS['LANGINDEX']]; ?></option>
									<option value="60" <?php if($recordConf->dataInfo['PostAlarmDuration']['value'] == 60) echo "selected=\"selected\""; ?> >60 <?php echo $t_seconds[$GLOBALS['LANGINDEX']]; ?></option>
									<option value="120" <?php if($recordConf->dataInfo['PostAlarmDuration']['value'] == 120) echo "selected=\"selected\""; ?> >120 <?php echo $t_seconds[$GLOBALS['LANGINDEX']]; ?></option>
								</select>
							</td>
						</tr>
						<tr>
							<th scope="row"> <?php echo $t_recordFileType[$GLOBALS['LANGINDEX']]; ?> </th>
							<td>
								<select name="select" id="RecordingMode" style="width:165px; height:22px; background-color:#868fa3; color:#1c1c1c;">
						         <option value="0" <?php if($recordConf->dataInfo['RecordingMode']['value'] == 0) echo "selected=\"selected\""; ?>>STW</option>
									<option value="1" <?php if($recordConf->dataInfo['RecordingMode']['value'] == 1) echo "selected=\"selected\""; ?>>AVI</option>
								</select>
							</td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_overwrite[$GLOBALS['LANGINDEX']]; ?> </th>
							<td>
								<label><input type="checkbox" id="Overwrite" onClick="OnChangeOverWrite();" style="margin-left:<?php if (GetBrowserName()=='IE') { if(ieversion() < 8) {echo '2';} else{echo '-3';} } else { echo '1'; } ?>px" <?php if ($recordConf->dataInfo['OverWrite']['value'] == 1) echo "checked=\"checked\""; ?> /><?php echo $t_use[$GLOBALS['LANGINDEX']]; ?></label>
							</td>
						</tr>
						<tr>
							<th scope="row"> <?php echo $t_autoDelete[$GLOBALS['LANGINDEX']];; ?> </th>
							<td>
								<label style="margin-right:10px;display:inline-block;vertical-align:middle;"><input type="checkbox" id="RemovalMode" onClick="OnChangeAutoRemoval(false);" style="margin-left:<?php if (GetBrowserName()=='IE') { if(ieversion() < 8) {echo '2';} else{echo '-3';} } else { echo '1'; } ?>px" <?php if ($recordConf->dataInfo['AutoRemoval']['value'] == 1) echo "checked=\"checked\""; ?> /><?php echo $t_use[$GLOBALS['LANGINDEX']]; ?>
								</label>
  								<input id="RemovalPeriod" type="text" class="text" value="<?php echo $recordConf->dataInfo['RemovalPeriod']['value']; ?>" style="width:40px;height:18px;text-align:center;display:inline-block;vertical-align:middle;" maxlength="3" onkeypress="IsNum(event)" onkeydown="OnlyNUm(event);"/>
								<label style="display:inline-block;vertical-align:middle;"><?php echo $t_days[$GLOBALS['LANGINDEX']]; ?> (1 ~ 180)</label>
							</td>
						</tr>
					</tbody>
				</table>
				<?php if ($GLOBALS['M_SUPPORT_SD']) { ?>
				<div id="SDDetail" style="display:none;">
					<div class="h3_tit" >
						<h3 style="width:400px;"><?php echo $t_SDfileSystem[$GLOBALS['LANGINDEX']]; ?></h3>
					</div>
					<table class="data_write" >
						<colgroup>
							<col style="width:225px;" />
							<col />
						</colgroup>
						<tbody>
							<tr>
								<th scope="row"> <?php echo $t_type[$GLOBALS['LANGINDEX']]; ?></th>
								<td>
									<select id="SD_fileSystem" style="width:165px; height:22px; background-color:#868fa3; color:#1c1c1c;" >
										<option value="1" <?php if($recordConf->dataInfo['SDFileSystem']['value'] == 1) echo "selected=\"selected\""; ?>>VFAT</option>
										<option value="2" <?php if($recordConf->dataInfo['SDFileSystem']['value'] == 2) echo "selected=\"selected\""; ?>>ext4</option>
									</select>
								</td>
							</tr>
						</tbody>
					</table>
				</div>
				<?php } ?>
				<?php if ($GLOBALS['M_SUPPORT_NAS']) { ?>
				<div id="NASDetail" style="display:none;">
					<div class="h3_tit" >
						<h3 style="width:400px;"><?php echo $t_nasConnectionSetup[$GLOBALS['LANGINDEX']]; ?> &nbsp;<span class="style7" id="NAS_Connection"  style="color:red;"></span></h3>
					</div>
					<table class="data_write" >
					<colgroup>
						<col style="width:225px;" />
						<col />
					</colgroup>
						<tbody>
							<tr>
								<th scope="row"> <?php echo $t_IPAddress[$GLOBALS['LANGINDEX']]; ?> </th>
								<td>
									<input id="NASIP" class="text" style="width:136px;" value="<?php echo $nasConf->dataInfo['IPAddress']['value']; ?>" maxlength="32" onkeypress='CheckIPv4(event)' onkeydown='CheckIPv4(event)'/>
								</td>
							</tr>
							<tr>
								<th scope="row"> <?php echo $t_ID[$GLOBALS['LANGINDEX']]; ?> </th>
								<td>
									<input id="NASID" class="text" style="width:136px;" value="<?php echo $nasConf->dataInfo['Id']['value']; ?>" maxlength="31" onkeypress='NoKorean(event)' onkeydown='NoKorean(event)'/>
								</td>
							</tr>
							<tr>
								<th scope="row"> <?php echo $t_password[$GLOBALS['LANGINDEX']]; ?> </th>
								<td>
									<input id="NASPW" class="text" style="width:136px;" type="password" maxlength="31" onclick='DoNASPWInit();' onkeypress='NoKorean(event);DoNASPWInit();' onkeydown='NoKorean(event);DoNASPWInit();'/>
								</td>
							</tr>
							<tr>
								<th scope="row"> <?php echo $t_defaultFolder[$GLOBALS['LANGINDEX']]; ?> </th>
								<td>
									<input id="NASDefaultFolder" class="text" style="width:136px;" value="<?php echo $nasConf->dataInfo['DefaultFolder']['value']; ?>" maxlength="31" onkeypress='NoKorean(event)' onkeydown='NoKorean(event)'/>
								</td>
							</tr>
							<tr>
								<th scope="row">  </th>
								<td>
									<a href="javascript:OnClickNasTest()" class="btn_type01" id="NASTest"><?php echo $t_test[$GLOBALS['LANGINDEX']]; ?></a>
								</td>
							</tr>
						</tbody>
					</table>					
				</div>
				<?php } ?>
				<div id="iSCSIDetail" style="display:none;">					
					<div class="h3_tit">
						<h3 style="width:400px;">iSCSI</h3>
					</div>
					<table class="data_write" >
					<colgroup>
						<col style="width:225px;" />
						<col style="width:155px;" />						
						<col />
					</colgroup>
						<tbody>
							<tr>
								<th scope="row"> <?php echo $t_IPAddress[$GLOBALS['LANGINDEX']]; ?> </th>
								<td colspan="2">
									<input id="iSCSIIP" class="text" style="width:136px;" value="" maxlength="32" onkeypress='CheckIPv4(event)' onkeydown='CheckIPv4(event)' />
								</td>
							</tr>
							<tr>
								<th scope="row"> <?php echo $t_port[$GLOBALS['LANGINDEX']]; ?> </th>
								<td>
									<input id="iSCSIPort" class="text" style="width:136px;" value="3260" disabled="disabled"/>
								</td>
								<td> 
									<a href="javascript:OnClickSearch()" class="btn_type01" id="iSCSISearch"><?php echo $t_search[$GLOBALS['LANGINDEX']]; ?></a>
								</td>
							</tr>
						</tbody>
					</table>		
					<div>
						<h3 style="height:25px; background-color:#8e939e; color:black; margin-top:10px; text-align:center">
							<span style="float:left; width:40px; margin-top:3px;">&nbsp;&nbsp;</span>
							<span style="float:left; width:50px; margin-top:3px;"><?php echo $t_number[$GLOBALS['LANGINDEX']]; ?></span>
							<span style="float:left; width:370px; margin-top:3px;"><?php echo $t_iSCSI_Qualified_Name[$GLOBALS['LANGINDEX']]; ?></span>
							<span style="float:left; width:200px; margin-top:3px;"><?php echo $t_status[$GLOBALS['LANGINDEX']]; ?></span>
						</h3>
						<ul id="iSCSI_list" style="overflow-y:scroll; height:180px; background-color:#b4b9c5"></ul>
					</div>
					<table class="data_write mgt10" >
						<colgroup>
							<col style="width:225px;" />
							<col style="width:155px;" />						
							<col />
						</colgroup>
						<tbody>
							<tr>
								<th scope="row"> <?php echo $t_ID[$GLOBALS['LANGINDEX']]; ?> </th>
								<td colspan="2">
									<input type="text" id="iqnID" class="text" style="width:136px;" onkeypress="IsNumChar(event);" onkeydown="CheckKorean(event);" maxlength="31"/>
								</td>
							</tr>
							<tr>
								<th scope="row"> <?php echo $t_password[$GLOBALS['LANGINDEX']]; ?> </th>
								<td>
									<input type="password" id="iqnPW" class="text" style="width:136px;" onkeypress="IsNumChar(event);" onkeydown="CheckKorean(event);" maxlength="31"/>
								</td>
								<td> 
									<a href="javascript:OnClickISCSIRegister()" class="btn_type01" id="iSCSIRegister"><?php echo $t_registration[$GLOBALS['LANGINDEX']]; ?></a>
								</td>
							</tr>
						</tbody>
					</table>	
				</div>
				
				<div id="iSCSIRegisterArea" style="display:none;">
					<a id="delete_iqn" class="btn_type01" href="javascript:OnClickDeleteIQN()" style="margin-top:40px; margin-bottom:10px; float:right;"><?php echo $t_delete[$GLOBALS['LANGINDEX']]; ?></a>
					<div class="h3_tit">
						<h3 style="width:400px;">iSCSI</h3>
					</div>
					<table class="data_table">						
						<colgroup>
							<col style="width:350px;" />
							<col style="width:180px;" />			
							<col />
						</colgroup>						
						<thead>
							<tr>
								<th><?php echo $t_iSCSI_Qualified_Name[$GLOBALS['LANGINDEX']]; ?></th>
								<th><?php echo $t_IPAddress[$GLOBALS['LANGINDEX']]; ?></th>
								<th><?php echo $t_port[$GLOBALS['LANGINDEX']]; ?></th>
							</tr>
						</thead>
						<tbody>
							<tr>
								<td><span id="register_iqn"><?php echo $iscsiConf->dataInfo['IQN']['value']; ?></span></td>
								<td><span id="register_ip"><?php echo $iscsiConf->dataInfo['IPAddress']['value']; ?></span></td>
								<td><span id="register_port"><?php echo $iscsiConf->dataInfo['Port']['value']; ?></span></td>
							</tr>
						</tbody>
					</table>
				</div>
				<?php
					$event_class = $contRecord;
					require_once ('eventsetup_ui.cgi');
				?>
				<div class="btn_right">
					<a id="mid_ok_btn" class="btn_apply" href="javascript:OnClickApply()"><?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?></a>
				</div>
			</div>
		</div>
	</div>
</body>
</html>
