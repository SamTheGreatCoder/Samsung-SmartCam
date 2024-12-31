<?php
define('OPENSDK_MAX_SIZE_APP_NAME', 	        60);
define('OPENSDK_MAX_SIZE_INSTALLED_DATE', 	40);

require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_system_taskmanager.cgi');

$classInstances = GetClassInstance('sdk');
$sdkSearchConf = $classInstances['SDKInfoRequest'];
$sdkSearchConf->SetHeaderCommand(CMD_SDK_SEARCH_DETAIL);
$sdkSearchConf->SetCGIPayload();

$GLOBALS['SOCKET_MANAGER']->Connection($sdkSearchConf);
?>


<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head>
	<title>iPOLiS NETWORK CAMERA WEBVIEWER</title>
	<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
	<meta http-equiv="X-UA-Compatible" content="IE=7" />
	<link rel="stylesheet" type="text/css" href="../css/techwin.css" />
	<link rel="stylesheet" type="text/css" href="../css/jquery.dataTables.css">
	<style type="text/css">
	@import url("../css/jquery-ui.css");
	#dia1 .ui-dialog,#dia1 .ui-dialog,#dia1 .ui-widget, #dia1 .ui-widget-content, #dia1 .ui-corner-all, #dia1 .foo, #dia1 .ui-draggable, #dia1 .ui-resizable {background:white !important}
	#dia1 .ui-dialog .ui-dialog-titlebar{background:#3598DD !important}
	#dia1 .dataTables_wrapper{padding-left:50px !important}
	html{
		overflow: auto !important;
	}
	.control-button {
		display:inline-block;
		width:90px;
		height:20px;
		margin-top:1px;
		padding-top:2px;
		background:#1b2029;
		color:#fff;
		text-align:center;
		vertical-align:middle;
		font-weight:bold;
		border:none;
		margin-right:5px;
	}
	.kill-button{
		display:inline-block;
		width:160px;
		height:20px;
		margin-top:1px;
		padding-top:2px;
		background:#1b2029;
		color:#fff;
		text-align:center;
		vertical-align:middle;
		font-weight:bold;
		border:none;
		margin-right:5px;
	}
	.control-button:hover{
		background:#0b76d5;
		text-decoration:none;
	}
	.kill-button:hover{
		background:#0b76d5;
		text-decoration:none;
	}

	</style>
	
	<script type="text/javascript" src="../js/jquery-1.5.1.min.js"></script>
	<!--<script type="text/javascript" src="../js/jquery-1.10.0.min.js"></script>-->
	<script type="text/javascript" src="../js/jquery-ui-1.8.16.custom.min.js "></script>
	<script type="text/javascript" src="../js/lnb.js"></script>
	<script type="text/javascript" src="../js/common_function.js"></script>
	<script type="text/javascript" src="../js/jquery.dataTables.min.js"></script>
	<script type="text/javascript" src="../js/xml2json.js"></script>
    <script type="text/javascript" src="../js/json2xml.js"></script>
	<script type="text/javascript" src="/home/js/SDKApi.js"></script>



<script type="text/javascript" language="javascript">
$(document).ready(function(){
	var oTable=null;
	var msg = "";
	var App_Name = "TestName";
	msg += "<GetSDKTaskManager>";
	//msg += "<AppName>"+ App_Name +"</AppName>";
	msg += "</GetSDKTaskManager>";
	var totalCPU=0;
	var totalMem=0;
	var reqUrl = "<?php echo $GLOBALS['REQUEST_URI']; ?>";
	if (BrowserDetect.browser == 'Explorer' || BrowserDetect.browser == 'Firefox' || (BrowserDetect.browser == 'Safari' && reqUrl.search('.local') != -1)) {
		reqUrl = "../.."+reqUrl.substr(reqUrl.indexOf("/cgi"));
	}
	oTable = $('#taskmanager').dataTable({
		"bFilter": false,
		"bSort": false,
		"bLengthChange": false,
		//"bAutoWidth": true,
		"aaData": null,
		"bPaginate": false,
		"oLanguage": {
			"sEmptyTable":"<?php echo $msg_noApplication[$GLOBALS['LANGINDEX']]?>", //No Application is running
		/*	"oPaginate" : {
				"sPrevious": "<?php echo $t_prev[$GLOBALS['LANGINDEX']]?>",
				"sNext": "<?php echo $t_next[$GLOBALS['LANGINDEX']]?>"
			},*/
				"sInfoEmpty": "<?php echo $t_total[$GLOBALS['LANGINDEX']]?> : _TOTAL_",
				"sInfo": "<?php echo $t_total[$GLOBALS['LANGINDEX']]?> : _TOTAL_"
		},
		"aoColumns": [
			{
				"mDataProp": "appName",
				"sTitle": "<?php echo $t_appName[$GLOBALS['LANGINDEX']]?>"
			},
			{
				"mDataProp": "memPercent",
				"sTitle": "<?php echo $t_memory[$GLOBALS['LANGINDEX']]?>"
			},
			{
				"mDataProp": "cpuPercent",
				"sTitle": "<?php echo $t_cpu[$GLOBALS['LANGINDEX']]?>"
			},
			{
				"mDataProp": "threadsCnt",
				"sTitle": "<?php echo $t_threadsCnt[$GLOBALS['LANGINDEX']]?>"
			},
			{
				"mDataProp": "Duration",
				"sTitle": "<?php echo $t_duration[$GLOBALS['LANGINDEX']]?>",
				"sWidth":"250px",
				"fnRender": function(obj) {
					var duration= obj.aData["Duration"];
					var days = Math.floor(duration / 86400);
					var hours = Math.floor(duration / 3600) % 24;
					var minutes = Math.floor(duration / 60) % 60;
					var seconds = duration % 60;
					var returnButton = days+" Days "+hours+" Hours "+minutes+" Minutes "+seconds+" Seconds";
					return returnButton;
				}
			},
			{
				"mDataProp": "killTask",
				"sDefaultContent": "",
				"sTitle": "<?php echo $t_action[$GLOBALS['LANGINDEX']]?>",
				"sWidth": "200px",
				"fnRender": function(obj) {
					var returnButton = "<input class='kill-button killButton' type='button' value='<?php echo $t_killtask[$GLOBALS['LANGINDEX']]?>' appname='"+obj.aData["appName"]+"'>";
					return returnButton;
				}
			}
		],
		"fnFooterCallback": function ( nRow, aaData, iStart, iEnd, aiDisplay ) {
				//nRow.getElementsByTagName('th')[1].innerHTML = "Starting index is "+iStart;
				//var totalCPU=0;
				//var totalMem=0;
				/*for(index = iStart ; index < iEnd ; index++){
					totalCPU+=parseInt(aaData[index].cpuPercent);
					totalMem+=parseInt(aaData[index].memPercent);
				}*/
				//console.log("CPU::"+totalCPU+" Total Memory:: "+totalMem);
				if(totalMem)
					nRow.getElementsByTagName('th')[1].innerHTML = totalMem;
				if(totalCPU)
					nRow.getElementsByTagName('th')[2].innerHTML = totalCPU;
		}
	});
	$.ajax({
		type: "POST",
		url: reqUrl,
		dataType: "text",
		timeout:1500,
		cache:false,
		data: encodeURIComponent(msg),
		success: function (response) {
			var jsonResponse = $.xml2json(response);
			totalCPU=jsonResponse["syscpu"];
			totalMem=jsonResponse["sysmem"];
			if(jsonResponse.appCount == 1){
				var tempAppdetails=jsonResponse.AppDetails;
				jsonResponse["AppDetails"]= new Array();
				jsonResponse["AppDetails"].push(tempAppdetails);
			}
						   

			oSettings = oTable.fnSettings();
			oTable.fnClearTable(this);
			if(jsonResponse.AppDetails){
				for (var i=0; i<jsonResponse.AppDetails.length; i++){
					oTable.oApi._fnAddData(oSettings, jsonResponse.AppDetails[i]);
				}
			}
			oSettings.aiDisplay = oSettings.aiDisplayMaster.slice();
			$(".customFooter").show();
			oTable.fnDraw(false);
		},
		error:function(error,textStatus, errorThrown){
            //    console.log(textStatus);
				//console.log(JSON.stringify(errorThrown));
				totalCPU = 0;
				totalMem = 0;
				if(!oTable){

				}
			}
	});
   
	setInterval(function(){
                //console.log("TableObject "+oTable);
                //$.support.cors = true
		$.ajax({
			type: "POST",
			cache: false,
			url: reqUrl,
			dataType: "text",
			data: encodeURIComponent(msg),
			success: function (response) {
				//console.log(response);
				var jsonResponse = $.xml2json(response);
				totalCPU=jsonResponse["syscpu"];
				totalMem=jsonResponse["sysmem"];
				if(jsonResponse.appCount == 1){
					var tempAppdetails=jsonResponse.AppDetails;
					jsonResponse["AppDetails"]= new Array();
					jsonResponse["AppDetails"].push(tempAppdetails);
				}
                               

				oSettings = oTable.fnSettings();
				oTable.fnClearTable(this);
				if(jsonResponse.AppDetails){
					for (var i=0; i<jsonResponse.AppDetails.length; i++){
						oTable.oApi._fnAddData(oSettings, jsonResponse.AppDetails[i]);
					}
				}
				oSettings.aiDisplay = oSettings.aiDisplayMaster.slice();
				$(".customFooter").show();
				oTable.fnDraw(false);
			},
			error:function(error,textStatus, errorThrown){
          //                      console.log(textStatus);
				//console.log(errorThrown);
				totalCPU = totalMem = 0;
				if(oTable){
					oTable.fnClearTable();
					$(".customFooter").hide();
				}
			}
		});
	},5000);
	$(document).delegate(".killButton","click",function(){
		$(this).stopApplication({
			appname:$(this).attr("appname"),
			success:function(){
				alert("<?php echo $t_stopped[$GLOBALS['LANGINDEX']]?>");
				//location.reload();
			},
			error: function (errorMsg) {
				alert(errorMsg);
			}
		});
	});
});
</script>

</head>
<body onselectstart="return false" id="dia1">
<br><br><br><br><br><br>
<div class="h3_tit mgt0" style="width:100%;">
	<h3 class="wid220"><?php echo $t_taskmanager[$GLOBALS['LANGINDEX']]?></h3>
</div>
<br>
<div id="tablewrapper" style="width:700px;">
	<table id="taskmanager" style="overflow-x:auto;">
	<tfoot class="customFooter">
	  <tr role="row" style="background-color: #AAB0BD;color: black;">
		<th class="sorting_disabled"><?php echo $t_totalUsage[$GLOBALS['LANGINDEX']]?></th>
		<th class="sorting_disabled"></th>
		<th class="sorting_disabled"></th>
		<th class="sorting_disabled"></th>
		<th class="sorting_disabled"></th>
		<th class="sorting_disabled"></th>
	  </tr>
	</tfoot>
	</table>	
</div>
<div>
</div>
</body>
</html>
