<?php
define('OPENSDK_MAX_SIZE_APP_NAME', 	        60);
define('OPENSDK_MAX_SIZE_INSTALLED_DATE', 	40);

require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_system_opensdk.cgi');
require_once ('SDKErrorCodes.cgi');
require_once ('SDKAppStatusCodes.cgi');
require_once ('APPPermissionCodes.cgi');
error_log("LanguageCode System_OpenSdk---->".$GLOBALS['LANGINDEX']);
   $classInstances = GetClassInstance('sdk');
	$sdkSearchConf = $classInstances['SDKInfoRequest'];
	$sdkSearchConf->SetHeaderCommand(CMD_SDK_SEARCH_DETAIL);
	$sdkSearchConf->SetCGIPayload();

        $GLOBALS['SOCKET_MANAGER']->Connection($sdkSearchConf);
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="kr" xml:lang="kr">
<head>
	<title>iPOLiS NETWORK CAMERA WEBVIEWER</title>
	<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
	<meta http-equiv="X-UA-Compatible" content="IE=8" />
	<link rel="stylesheet" type="text/css" href="../css/techwin.css" />
	<link rel="stylesheet" type="text/css" href="../css/jquery.dataTables.css">
	<!--<script type="text/javascript" src="../js/jquery-1.5.1.min.js"></script>-->
	<script type="text/javascript" src="../js/jquery-1.10.0.min.js"></script>
	<script type="text/javascript" src="../js/lnb.js"></script>
	<script type="text/javascript" src="../js/common_function.js"></script>
	<script type="text/javascript" src="../js/xml2json.js"></script>
	<script type="text/javascript" charset="utf8" src="../js/jquery.dataTables.min.js"></script>
	<script src="../js/jquery.alerts.js" type="text/javascript"></script>
	<link href="../css/jquery.alerts.css" rel="stylesheet" type="text/css" media="screen" />
	<style type="text/css">
		.sbtn2{
			font-size: 11px;
			padding: 5px 16px;
			color: #000;
			margin: 0 6px 0 10px;
		}
		.FileField {
			height:15px;
			margin-right:12px;
			border:solid 1px #CFD2D9;
			background:#CFD2D9;
			width:350px;
			margin-top: 1px;
		}
		/*.control-button {
			-webkit-box-shadow:rgba(0,0,0,0.98) 0 1px 0 0;
			-moz-box-shadow:rgba(0,0,0,0.98) 0 1px 0 0;
			box-shadow:rgba(0,0,0,0.98) 0 1px 0 0;
			background-color:#FFFFFF;
			border-radius:0;
			-webkit-border-radius:0;
			-moz-border-radius:0;
			border:1px solid #999;
			color:#666;
			font-family:'Lucida Grande',Tahoma,Verdana,Arial,Sans-serif;
			font-size:11px;
			font-weight:700;
			padding:2px 6px;
			width:100px;
			text-align:center;
			text-decoration: none!important;
			cursor: default;
		}*/
		#installed_apps_list .control-button {
			display:inline-block;
			width:200px;
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
			/*Handle Text Overflow*/
			text-overflow: ellipsis;
			overflow: hidden; 
			white-space: nowrap;
			display: inline-block;
		}
		#installed_apps_list .control-button-disabled {
			display:inline-block;
			width:200px;
			height:20px;
			margin-top:1px;
			padding-top:2px;
			background:#1b2029;
			color:grey;
			text-align:center;
			text-decoration:none;
			vertical-align:middle;
			font-weight:bold;
			border:none;
			margin-right:5px;
			/*Handle Text Overflow*/
			text-overflow: ellipsis;
			overflow: hidden; 
			white-space: nowrap;
			display: inline-block;
		}
		#f1_upload_form .control-button {
			display:inline-block;
			width:150px;
			height:20px;
			margin-top:1px;
			background:#1b2029;
			color:#fff;
			text-align:center;
			vertical-align:middle;
			font-weight:bold;
			border:none;
			margin-right:5px;
			/*Handle Text Overflow*/
			text-overflow: ellipsis;
			overflow: hidden; 
			white-space: nowrap;
			display: inline-block;
		}
		#installed_apps_list .control-button:hover, #f1_upload_form .control-button:hover{
			background:#0b76d5;
			text-decoration:none;
			cursor:pointer;
		}
		.fileinput-button {
			position: relative;
			overflow: hidden;
			/*float: left;*/
			margin-right: 4px;
			cursor: pointer;
		}
		.fileinput-button input {
			position: absolute;
			top: 0;
			right: 0;
			margin: 0;
			border: solid transparent;
			width:104px;
			/*border-width: 0 0 100px 200px;*/
			opacity: 0;
			filter: alpha(opacity=0);
			/*-moz-transform: translate(-300px, 0) scale(4);*/
			direction: ltr;
			cursor: pointer;
		}	
		.fileinput-button span {
			/*padding-left: 20px;
			padding-right: 20px;*/
			text-align:center;
			/*Handle Text Overflow*/
			text-overflow: ellipsis;
			width: 90px;
			overflow: hidden; 
			white-space: nowrap;
			display: inline-block;
		}
		.AppStatus{margin: 18px}
		.loadingTableCover{
			height: 695px;
			width: 860px;
			background: #000;
			opacity: 0.65;
			filter: alpha(opacity=60);
			position: absolute;
			top: 90px;
			left: 300px;
			display: none;
		}
		.loadingTableCover img{
			position:absolute;
			left: 50%;
			top: 50%;
		}
	</style>
<script type="text/javascript" language="javascript">
	var SDK_APP_STATUS = <?php echo json_encode($SDK_APP_STATUS_CODES_MAP[$GLOBALS['LANGINDEX']]);?>;
	var LangIndex = <?php echo $GLOBALS['LANGINDEX'];?>;
	var MAX_SIZE_INSTALLED_DATE = parseInt("<?php echo OPENSDK_MAX_SIZE_INSTALLED_DATE;?>");
$(document).ready(function(){
	lnbonoff("lnb_system");
	///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	// Initialise var for i18n
	///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	
        var lang_lbl_Version="<?php echo $t_version[$GLOBALS['LANGINDEX']]?>";
        var lang_lbl_InstalledDate="<?php echo $t_installedDate[$GLOBALS['LANGINDEX']]?>";
        var lang_lbl_slNo="<?php echo $t_number[$GLOBALS['LANGINDEX']]?>"
        var lang_lbl_appName="<?php echo $t_appName[$GLOBALS['LANGINDEX']]?>"
        var lang_lbl_uninstall="<?php echo $t_uninstall[$GLOBALS['LANGINDEX']]?>"
        var lang_lbl_goapp="<?php echo $t_goApp[$GLOBALS['LANGINDEX']]?>"
        var lang_lbl_status="<?php echo $t_status[$GLOBALS['LANGINDEX']]?>"
        var lang_lbl_start="<?php echo $t_start[$GLOBALS['LANGINDEX']]?>"
        var lang_lbl_stop="<?php echo $t_stop[$GLOBALS['LANGINDEX']]?>"
        var lang_lbl_health="<?php echo $t_health[$GLOBALS['LANGINDEX']]?>"
        var lang_lbl_setup="<?php echo $t_setup[$GLOBALS['LANGINDEX']]?>"
        var lang_lbl_priority="<?php echo $t_priority[$GLOBALS['LANGINDEX']]?>"
        var lang_lbl_low="<?php echo $t_low[$GLOBALS['LANGINDEX']]?>"
        var lang_lbl_medium="<?php echo $t_medium[$GLOBALS['LANGINDEX']]?>"
        var lang_lbl_high="<?php echo $t_high[$GLOBALS['LANGINDEX']]?>"
        var lang_lbl_autostart="<?php echo $t_autostart[$GLOBALS['LANGINDEX']]?>"
        var lang_lbl_use="<?php echo $t_use[$GLOBALS['LANGINDEX']]?>"
        var lang_lbl_apply="<?php echo $t_apply[$GLOBALS['LANGINDEX']]?>"
        ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	/////////////////////////////////////////
	// Creating Table
	////////////////////////////////////////
	var oTable = $('#installed_apps_list').dataTable( {
		"aaData": null,
		"bProcessing": true,
		"bAutoWidth": false,
		"bFilter": false,
		"bPaginate": false,
		"sScrollY": "520px",
		"oLanguage": {
			"sEmptyTable":"<?php echo $msg_noApplication[$GLOBALS['LANGINDEX']]?>", //No Application is running
			"sInfoEmpty": "<?php echo $t_total[$GLOBALS['LANGINDEX']]?> : _TOTAL_",
			"sInfo": "<?php echo $t_total[$GLOBALS['LANGINDEX']]?> : _TOTAL_",
			"sZeroRecords": "<?php echo $msg_noApplication[$GLOBALS['LANGINDEX']]?>"
		},
		"aoColumns": [{
			"mDataProp": "slNo",
			"sTitle": lang_lbl_slNo,
			"sClass": "center",
			"sDefaultContent": ""
		},{
			"mDataProp": "appName",
			"sTitle": lang_lbl_appName,
			"sDefaultContent": "",
			"sWidth":"270px",
			"mRender":function(data, type, full){
				return "<p style='word-break:break-all'>"+data+"</p>"+lang_lbl_InstalledDate+" : "+timeConverter(full['InstalledDate'])+"<br>"+lang_lbl_Version+" : "+full['Version']+"<br><input class='control-button uninstallButton' type='button' name="+'UNINSTALL-'+data+" id="+'UNINSTALL-'+data+" value="+"'"+lang_lbl_uninstall+"'"+"></input><input class='control-button goAppButton' type='button' id="+'GOAPP-'+data+" name="+'GOAPP-'+data+" value="+"'"+lang_lbl_goapp+"'"+"></input>";;
			}
		},{
			"mDataProp": "AppStatus",
			"sTitle": lang_lbl_status,
			"sDefaultContent": "",
			"sWidth":"220px",
			"sClass": "center",
			"mRender":function(data, type, full){
				if(data == "2" || data == "6"){
					returnButton = "<div class='AppStatus Status-"+full['appName']+"'>"+SDK_APP_STATUS[data]+"</div><input class='control-button startStopButton' type='button' name='START-"+full['appName']+"' id='START-"+full['appName']+"' value="+"'"+lang_lbl_start+"'"+"></input><a class='control-button-disabled healthButton' name="+'HEALTH-'+full['appName']+" id="+'HEALTH-'+full['appName']+" >" + lang_lbl_health + "</a>";
				}else if(data == "4" || data == "5"){
					returnButton = "<div class='AppStatus Status-"+full['appName']+"'>"+SDK_APP_STATUS[data]+"</div><input class='control-button startStopButton' type='button' name='STOP-"+full['appName']+"' id='STOP-"+full['appName']+"' value="+"'"+lang_lbl_stop+"'"+"></input><input class='control-button healthButton' type='button' name="+'HEALTH-'+full['appName']+" id="+'HEALTH-'+full['appName']+" value="+"'"+lang_lbl_health+"'"+" ></input>";
				} else { 
					returnButton = "<div class='AppStatus Status-"+full['appName']+"'>"+SDK_APP_STATUS[data];
				}
				return returnButton;
			}
		},{
			"mDataProp": "Priority",
			"sTitle": lang_lbl_setup,
			"sDefaultContent": "",
			"mRender":function(data, type, full){
				switch(data){
					case '0' : returnButton=lang_lbl_priority+'<br><input type="radio" value="0" id="PriorityLo_'+full['appName']+'" checked="true" name="Priority_'+full['appName']+'"/><?php echo $t_low[$GLOBALS['LANGINDEX']]?><input type="radio" value="1" id="PriorityMi_'+full['appName']+'" name="Priority_'+full['appName']+'"/><?php echo $t_medium[$GLOBALS['LANGINDEX']]?><input type="radio" value="2" id="PriorityHi_'+full['appName']+'" name="Priority_'+full['appName']+'"/>'+lang_lbl_high+'<br>'; break;

					case '1' : returnButton=lang_lbl_priority+'<br><input type="radio" value="0" id="PriorityLo_'+full['appName']+'" name="Priority_'+full['appName']+'"/><?php echo $t_low[$GLOBALS['LANGINDEX']]?><input type="radio" value="1" id="PriorityMi_'+full['appName']+'" checked="checked" name="Priority_'+full['appName']+'"/><?php echo $t_medium[$GLOBALS['LANGINDEX']]?><input type="radio" value="2" id="PriorityHi_'+full['appName']+'" name="Priority_'+full['appName']+'"/>'+lang_lbl_high+'<br>'; break;

					case '2' : returnButton=lang_lbl_priority+'<br><input type="radio" value="0" id="PriorityLo_'+full['appName']+'" name="Priority_'+full['appName']+'"/><?php echo $t_low[$GLOBALS['LANGINDEX']]?><input type="radio" value="1" id="PriorityMi_'+full['appName']+'" name="Priority_'+full['appName']+'"/><?php echo $t_medium[$GLOBALS['LANGINDEX']]?><input type="radio" value="2" id="PriorityHi_'+full['appName']+'" checked="checked" name="Priority_'+full['appName']+'"/>'+lang_lbl_high+'<br>'; break;
					
					default : break;
				}
				if(full['AutoStart'] == '1'){
					returnButton+=lang_lbl_autostart+'<input type="checkbox" value="0" checked="checked" id="autoStart_'+full['appName']+'" name="autoStart_'+full['appName']+'"/>'+lang_lbl_use+'<br>';
				}
				else{
					returnButton+=lang_lbl_autostart+'<input type="checkbox" value="0" id="autoStart_'+full['appName']+'" name="autoStart_'+full['appName']+'"/>'+lang_lbl_use+'<br>';
				}
				returnButton+='<input class="control-button applyButton" type="button" id="APPLY-'+full['appName']+'" name="APPLY-'+full['appName']+'" value="'+lang_lbl_apply+'">';
				return returnButton;
				
			}
		}]
		
	} );
	//setInterval(function(){
		reloadAppTableData();
		
	//},20000);
	
   $(document).delegate(".uninstallButton", "click", function(obj){
		var str = obj.target.id;
		var splitStr=str.split('-');
		onUnistallBtnClk(splitStr[1]);
	});
	$(document).delegate(".goAppButton", "click", function(obj){
		var str = obj.target.id;
        var splitStr=str.split('-');
		onGoAppPageBtnClk(splitStr[1]);
	});
	$(document).delegate(".startStopButton", "click", function(obj){
		var str = obj.target.id;
		var splitStr=str.split('-');
		if(splitStr[0] == 'START'){
			onStartBtnClk(splitStr[1]);
		}
		else if(splitStr[0] == 'STOP'){
			onStopBtnClk(splitStr[1]);
		}
	});
	$(document).delegate(".healthButton", "click", function(obj){
		var str = obj.target.id;
                var splitStr=str.split('-');
		onHealthBtnClk(splitStr[1]);
	});
	$(document).delegate("#taskManagerLink", "click", function(obj){
	    //alert("Button clicked");
		window.open("system_taskmanager2.cgi","", "scrollbars=1,width=900,height=400");
        //window.open('system_taskmanager2.cgi');
		//var NWin = window.open($(this).prop('href'), '', 'height=800,width=800');
		//var NWin = window.open('system_taskmanager2.cgi', '', 'scrollbar=1,height=800,width=800');
		return false;
	});
	$(document).delegate(".applyButton", "click", function(obj){
		var str = obj.target.id;
                var splitStr=str.split('-');
		onApplyBtnClk(splitStr[1]);
	});
	//$(document).delegate("input[type=file]#myfile","change",function(event){
	$('#myfile').on('change' ,function(){
		var filePath = $(this).val();
		var fileName;
		var fileNameStartFS = filePath.lastIndexOf('/');
		var fileNameStartBS = filePath.lastIndexOf('\\');
		if(fileNameStartFS == -1){
			fileName = filePath.slice((fileNameStartBS+1),filePath.length);
		}else{
			fileName = filePath.slice((fileNameStartFS+1),filePath.length);
		}	
		$("#fakeBrowseField").val(fileName);
	});
	
	// loading image for install and un install
	$('#contents').append("<div style='' class='loadingTableCover'><img src='../images/common/cgi_loading.gif' ></div>");
	
	
	
	
});


function checkHealthready(){ //  disable the health button if app is not running
	
	
	$(".startStopButton").each(function(){
		
		var str=$(this).attr("name");
		var splitStr=str.split('-');
		if($(this).val()=="Stop"){
			//console.log($(this).attr("name"),"started");
			$("#HEALTH-"+splitStr[1]).prop("disabled",false); 
		}
		else
		{	//console.log($(this).attr("name"),"stopped");
			$("#HEALTH-"+splitStr[1]).prop("disabled",true); 
		}
		
	});
}

function reloadAppTableData(){
	var reqUrl = "<?php echo $GLOBALS['REQUEST_URI']; ?>";
	var msg = "<GetAllSDK_APP_INFO></GetAllSDK_APP_INFO>";
	if (BrowserDetect.browser == 'Explorer' || BrowserDetect.browser == 'Firefox' || (BrowserDetect.browser == 'Safari' && reqUrl.search('.local') != -1)) {
		reqUrl = "../.."+reqUrl.substr(reqUrl.indexOf("/cgi"));
	}
	$.ajax({
		type: "POST",
		cache: false,
		url: reqUrl,
		dataType: "text",
		data: encodeURI(msg),
		success: function(response){
			var oTable = $('#installed_apps_list').dataTable();
			//console.log(response);
			var jsonResponse = $.xml2json(response);
			//console.log("Raw JSON: ",$.xml2json(response));
			if(jsonResponse['AppDetail']){
				var appDetails = jsonResponse['AppDetail']
				if( !(appDetails instanceof Array)){
					var tempAppdetails=appDetails;
					appDetails= new Array();
					appDetails.push(tempAppdetails);
				}
				oTable.fnClearTable();
				oTable.fnAddData(appDetails);
				//console.log("After JSON Test: ",appDetails);
			}else{
				//Table is Empty
				oTable.fnClearTable();
			}
			
		}
	});
	
} 


       var APP_NAME = '';
        var MAX_APP_PERMISSIONS = 32; // 32 bits
        
        // Define ERROR CODES map here
        var SDK_ERROR_CODES_MAP = <?php echo json_encode($SDK_ERROR_CODES_MAP[$GLOBALS['LANGINDEX']]);?>;

        // Define Permissions map here
        var APP_PERMISSION_CODES = <?php echo json_encode($APP_PERMISSION_CODES_MAP[$GLOBALS['LANGINDEX']]);?>;

        function onUnistallBtnClk(App_Name)
        {
			 var conf_message = "<?php echo $t_uninstall[$GLOBALS['LANGINDEX']];?>: "+App_Name+"\n\n"+"<?php echo $lang_msg_ok[$GLOBALS['LANGINDEX']];?>";
			 var confirm_status;
			 var reqUrl = "<?php echo $GLOBALS['REQUEST_URI']; ?>";
			 confirm_status = confirm(conf_message);
  
			 if (confirm_status == true)
			 {
				var msg = "";
				msg += "<RemoveSDK>";
				msg += "<AppName>"+ App_Name +"</AppName>";
				msg += "</RemoveSDK>";
				
		        if (BrowserDetect.browser == 'Explorer' || BrowserDetect.browser == 'Firefox' || (BrowserDetect.browser == 'Safari' && reqUrl.search('.local') != -1)) {
			         reqUrl = "../.."+reqUrl.substr(reqUrl.indexOf("/cgi"));
		        }
				$(".loadingTableCover").show();
				$.ajax({
					type: "POST",
					cache: false,
					url: reqUrl,
					dataType: "text",
					data: encodeURI(msg),
					success: function(ack){
						var msg = "";
						var result = '';
						var xml = $.parseXML(ack);
						var Is_valid_error_code = $(xml).find("ErrorCode").text();

						if(Is_valid_error_code != "")
						{
							var error_code = parseInt(Is_valid_error_code);
							msg += "<?php echo $msg_uninstall_error[$GLOBALS['LANGINDEX']]?>: "+SDK_ERROR_CODES_MAP[error_code];
							result = '<span class="emsg"><?php echo $msg_start_error[$GLOBALS['LANGINDEX']]?>!<\/span><br/><br/>';
							alert(msg);
							//window.location.reload(true);
							reloadAppTableData();
						} else {
							msg += "<?php echo $lang_msg_uninstall_success[$GLOBALS['LANGINDEX']]?>";
							alert(msg);
							//window.location.reload(true);
							reloadAppTableData();
						}
						$(".loadingTableCover").hide();
					},
					error:function(){
						//window.location.reload(true);
						reloadAppTableData();
						$(".loadingTableCover").hide();
					}
				});              
				 //RequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>", 'SDK', 'undefined');
			 }
        }
		

        function onGoAppPageBtnClk(App_Name){
        		var	msg	 	= "";
        		var	reqUrl	= "<?php echo $GLOBALS['REQUEST_URI']; ?>";
        		msg				+= "<GetSDK_APP><AppName>" + App_Name + "</AppName></GetSDK_APP>";
        		if (BrowserDetect.browser == 'Explorer' || BrowserDetect.browser == 'Firefox' || (BrowserDetect.browser == 'Safari' && reqUrl.search('.local') != -1)) {
                reqUrl = "../.."+reqUrl.substr(reqUrl.indexOf("/cgi"));
            }
            $.ajax({
            	type: "POST",
            	cache: false,
            	url: reqUrl,
            	dataType: "text",
            	data: encodeURI(msg),
            	success: function(ack){
						var msg = "";
						var result = '';
						//console.log(ack);
						var xml = $.parseXML(ack);
						var Is_valid_error_code = $(xml).find("ErrorCode").text();

						if(Is_valid_error_code != "")
						{
							var error_code = parseInt(Is_valid_error_code);
							msg += "<?php echo $msg_start_error[$GLOBALS['LANGINDEX']]?>: "+SDK_ERROR_CODES_MAP[error_code];
							result = '<span class="emsg"><?php echo $msg_start_error[$GLOBALS['LANGINDEX']]?>!<\/span><br/><br/>';
							alert(msg);
							reloadAppTableData();
						} else {
							result	= $(xml).find("targetSDK").text();
							if(result != "")
							{
								window.open("../setup/opensdk/html/"+App_Name+"/index.html?AppName="+App_Name);
							}
							else
							{
								window.open("../setup/opensdk/html/"+App_Name+"/index.cgi?AppName="+App_Name);
							}
						}
            	}
            });
        }

        function onStartBtnClk(App_Name)
        {
			var msg = "";
			var reqUrl = "<?php echo $GLOBALS['REQUEST_URI']; ?>";
			msg += "<StartSDK>";
			msg += "<AppName>"+ App_Name +"</AppName>";
			msg += "</StartSDK>";

		    if (BrowserDetect.browser == 'Explorer' || BrowserDetect.browser == 'Firefox' || (BrowserDetect.browser == 'Safari' && reqUrl.search('.local') != -1)) {
                reqUrl = "../.."+reqUrl.substr(reqUrl.indexOf("/cgi"));
            }
			$(".loadingTableCover").show();
			$.ajax({
				type: "POST",
				cache: false,
				url: reqUrl,
				dataType: "text",
				data: encodeURI(msg),
				success: function(ack){
					var msg = "";
					var result = '';
					//console.log(ack);
					var xml = $.parseXML(ack);
					var Is_valid_error_code = $(xml).find("ErrorCode").text();

					if(Is_valid_error_code != "")
					{
						var error_code = parseInt(Is_valid_error_code);
						msg += "<?php echo $msg_start_error[$GLOBALS['LANGINDEX']]?>: "+SDK_ERROR_CODES_MAP[error_code];
						result = '<span class="emsg"><?php echo $msg_start_error[$GLOBALS['LANGINDEX']]?>!<\/span><br/><br/>';
						alert(msg);
						//window.location.reload(true);
						reloadAppTableData();
					} else {
						//window.location.reload(true);
						reloadAppTableData();
					}
					$(".loadingTableCover").hide();
				}
			});
              
        }
        
        function onStopBtnClk(App_Name)
        {
			var msg = "";
			var reqUrl = "<?php echo $GLOBALS['REQUEST_URI']; ?>";
			msg += "<StopSDK>";
			msg += "<AppName>"+ App_Name +"</AppName>";
			msg += "</StopSDK>";

            if (BrowserDetect.browser == 'Explorer' || BrowserDetect.browser == 'Firefox' || (BrowserDetect.browser == 'Safari' && reqUrl.search('.local') != -1)) {
                reqUrl = "../.."+reqUrl.substr(reqUrl.indexOf("/cgi"));
            }
			$(".loadingTableCover").show();
			$.ajax({
				type: "POST",
				cache: false,
				url: reqUrl,
				dataType: "text",
				data: encodeURI(msg),
				success: function(ack){
					var msg = "";
					var result = '';
					//console.log(ack);
					var xml = $.parseXML(ack);
					var Is_valid_error_code = $(xml).find("ErrorCode").text();

					if(Is_valid_error_code != "")
					{
						var error_code = parseInt(Is_valid_error_code);
						msg += "<?php echo $lang_msg_stop_error[$GLOBALS['LANGINDEX']]?>: "+SDK_ERROR_CODES_MAP[error_code];
						//result = '<span class="emsg"><?php echo $msg_start_error[$GLOBALS['LANGINDEX']]?>!<\/span><br/><br/>';
						alert(msg);
						//window.location.reload(true);
						reloadAppTableData();
					} else {
						//window.location.reload(true);
						reloadAppTableData();
					}
					$(".loadingTableCover").hide();
				}
			});

			//RequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>", 'SDK', 'undefined');
        }

        function onHealthBtnClk(App_Name)
        {
                 var msg = "";
                 msg += "<GetSDK>";
                 msg += "<AppName>"+ App_Name +"</AppName>";
                 msg += "</GetSDK>";
              
                 SDKHealthRequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>", 'SDK', 'undefined');
        }

        function onApplyBtnClk(App_Name)
        {
                var priority = 0;  // Default - Low Priority
                var AutoStart = 0; // Default - Not to use Auto start
    
                if(document.getElementById('PriorityHi_'+App_Name).checked)
                {
                   priority = document.getElementById('PriorityHi_'+App_Name).value;
                }
                else if(document.getElementById('PriorityMi_'+App_Name).checked)
                {
                   priority = document.getElementById('PriorityMi_'+App_Name).value;
                }
    
                if(document.getElementById('autoStart_'+App_Name).checked){
                   AutoStart = 1;
                }
    
                var msg ="";
                msg += "<SetSDKAppAttributes>";
                msg += "<AppName>"+ App_Name +"</AppName>"+"\n";
                msg += "<IsAutoStart>"+ AutoStart +"</IsAutoStart>"+"\n";
                msg += "<Priority>"+ priority +"</Priority>"+"\n";
                msg += "</SetSDKAppAttributes>";
    
                SDKUpdateSettingsRequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>", 'SDKAppAttributes', 'undefined');
        }

        function SDKUploadRequestAjaxMsg(msg, alertMsg, reqUrl, command, asyncVal)
        {
            if (typeof command == "undefined")	command = "";
        	if (typeof asyncVal == "undefined")	asyncVal = false;
        	gAlertMsg = alertMsg;
            if (BrowserDetect.browser == 'Explorer' || BrowserDetect.browser == 'Firefox' || (BrowserDetect.browser == 'Safari' && reqUrl.search('.local') != -1)) {
                reqUrl = "../.."+reqUrl.substr(reqUrl.indexOf("/cgi"));
            }
        
        	$.ajax({
        		type: "POST",
        		async: asyncVal,
        		cache: false,
        		url: reqUrl,
        		dataType: "text",
        		data: encodeURI(msg),
        		success: OnSuccessUpload
                        });
        }


        function SDKInstallRequestAjaxMsg(msg, alertMsg, reqUrl, command, asyncVal)
        {
            if (typeof command == "undefined")	command = "";
        	if (typeof asyncVal == "undefined")	asyncVal = false;
        	gAlertMsg = alertMsg;
            if (BrowserDetect.browser == 'Explorer' || BrowserDetect.browser == 'Firefox' || (BrowserDetect.browser == 'Safari' && reqUrl.search('.local') != -1)) {
                reqUrl = "../.."+reqUrl.substr(reqUrl.indexOf("/cgi"));
            }
        
        	$.ajax({
        		type: "POST",
        		async: asyncVal,
        		cache: false,
        		url: reqUrl,
        		dataType: "text",
        		data: encodeURI(msg),
        		success: OnSuccessInstall
                        });
        }

        function SDKHealthRequestAjaxMsg(msg, alertMsg, reqUrl, command, asyncVal)
        {
        	if (typeof command == "undefined")	command = "";
        	if (typeof asyncVal == "undefined")	asyncVal = false;
        	gAlertMsg = alertMsg;
            if (BrowserDetect.browser == 'Explorer' || BrowserDetect.browser == 'Firefox' || (BrowserDetect.browser == 'Safari' && reqUrl.search('.local') != -1)) {
                reqUrl = "../.."+reqUrl.substr(reqUrl.indexOf("/cgi"));
            }

        	$.ajax({
        		type: "POST",
        		async: asyncVal,
        		cache: false,
        		url: reqUrl,
        		dataType: "text",
        		data: encodeURI(msg),
        		success: OnSuccessHealth
                        });
        }
		
	

        function SDKUpdateSettingsRequestAjaxMsg(msg, alertMsg, reqUrl, command, asyncVal)
        {
        	if (typeof command == "undefined")	command = "";
        	if (typeof asyncVal == "undefined")	asyncVal = false;
        	gAlertMsg = alertMsg;
            if (BrowserDetect.browser == 'Explorer' || BrowserDetect.browser == 'Firefox' || (BrowserDetect.browser == 'Safari' && reqUrl.search('.local') != -1)) {
                reqUrl = "../.."+reqUrl.substr(reqUrl.indexOf("/cgi"));
            }
        
        	$.ajax({
        		type: "POST",
        		async: asyncVal,
        		cache: false,
        		url: reqUrl,
        		dataType: "text",
        		data: encodeURI(msg),
        		success: OnSuccessUpdateSettings
            });
        }

		function OnSuccessUpload(ack)
        {
            var msg = "";
            var result ='';

            var xml = $.parseXML(ack);
            var Is_valid_error_code = $(xml).find("ErrorCode").text();

            if(Is_valid_error_code != "")
            {
                var error_code = parseInt(Is_valid_error_code);
                msg += "<?php echo $msg_error_upload[$GLOBALS['LANGINDEX']]?> : "+SDK_ERROR_CODES_MAP[error_code];
                result = '<span class="emsg"><?php echo $msg_error_upload2[$GLOBALS['LANGINDEX']]?><\/span><br/><br/>';
                alert(msg);
			} else {
             	Install(ack);    
            }
            //document.getElementById("f1_upload_process").innerHTML='';
            document.getElementById('f1_upload_process').style.display = 'none';
            //document.getElementById('f1_upload_form').innerHTML = result + '<input id="myfile" name="myfile" type="file" size="70"/><input type="submit" name="submitBtn" value="Install" />';
            document.getElementById('f1_upload_form').style.display = 'block';
        }

	function Install(ack)
	{
	    var msg = "";
	    var IsUpgrade = false;
		var IsDebug   = false;
		
	    var xml = $.parseXML(ack);
            var permissions = parseInt($(xml).find("AddResult").text());
	    var upgrade = parseInt($(xml).find("Upgrade").text());

            var permissionsMsg = "<?php echo $msg_permission[$GLOBALS['LANGINDEX']]?>"+ "\n";
            var result = 0;

	    if(1 == upgrade) {
	        IsUpgrade = true;
	    }
		var confirm_result;
		var debug = parseInt($(xml).find("Debug").text());
		if(1 == debug) {
			var debugMsg= "WARNING: The Debug mode of this application is ON. \nIt will consume more space on disk.\nContinue?" ;
			confirm_result = confirm(debugMsg);
			if(confirm_result == false) 
			{
			    var DIR_PATH = "<?php echo $GLOBALS['SDK_APP_EXTRACTED_DIRECTORY'];?>";
                DIR_PATH += APP_NAME;
                msg = "";
                msg += "<GetCMD_SDK_CANCEL>";
                msg += "<DirPath>"+ DIR_PATH +"</DirPath>";
                msg += "</GetCMD_SDK_CANCEL>";
                SDKCancelRequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>", 'SDK', 'undefined');
				return;
			}
		}

		if(0 == permissions)
		{
			permissionsMsg += (APP_PERMISSION_CODES[result] + "\n");
		}
		else
		{
			for(i=0; i<MAX_APP_PERMISSIONS; i++)
			{
				result = permissions & (1<<i);
				if(0 == result)
					continue;

				permissionsMsg += (APP_PERMISSION_CODES[result] + "\n");
			}	
		}
	    permissionsMsg += "<?php echo $msg_permission2[$GLOBALS['LANGINDEX']]?>";
	    
            var confirm_result;
	
	    confirm_result = confirm(permissionsMsg);
		if (confirm_result == true)
		{
			msg = "";
			msg += "<SetSDK>";
			msg += "<AppName>"+ APP_NAME +"</AppName>";

			if(IsUpgrade) {
				var settingsMsg = "<?php echo $msg_settings[$GLOBALS['LANGINDEX']]?>"+"\n"+"<?php echo $msg_press_ok[$GLOBALS['LANGINDEX']]?>";
				var confirm_retain = confirm(settingsMsg);
				if (confirm_retain == true)
				{
					msg += "<RetainSettings>"+ "1" +"</RetainSettings>";
				} else {
					msg += "<RetainSettings>"+ "0" +"</RetainSettings>";
				}
			}

			msg += "</SetSDK>";
			SDKInstallRequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>", 'SDK', 'undefined');
			return;
		} else {
			//msg="Install Canceled!";
			//result = '<span class="emsg">Installation Error: Install Canceled!<\/span><br/><br/>';
			//jAlert(msg, "CANCEL");

			var DIR_PATH = "<?php echo $GLOBALS['SDK_APP_EXTRACTED_DIRECTORY'];?>";
			DIR_PATH +=APP_NAME;
			var msg = "";
			msg += "<GetCMD_SDK_CANCEL>";
			msg += "<DirPath>"+ DIR_PATH +"</DirPath>";
			msg += "</GetCMD_SDK_CANCEL>";
			SDKCancelRequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>", 'SDK', 'undefined');
		}
	}

        function SDKCancelRequestAjaxMsg(msg, alertMsg, reqUrl, command, asyncVal)
        {
            if (typeof command == "undefined")  command = "";
            if (typeof asyncVal == "undefined") asyncVal = false;
            gAlertMsg = alertMsg;
            if (BrowserDetect.browser == 'Explorer' || BrowserDetect.browser == 'Firefox' || (BrowserDetect.browser == 'Safari' && reqUrl.search('.local') != -1)) {
                reqUrl = "../.."+reqUrl.substr(reqUrl.indexOf("/cgi"));
            }
            $.ajax({
                type: "POST",
                async: asyncVal,
                cache: false,
                url: reqUrl,
                dataType: "text",
                data: encodeURI(msg),
                success: OnSuccessCancel
            });
        }
        function OnSuccessCancel(ack)
        {
       	    var msg = "";
            //msg +="Install Canceled!";
            msg += "<?php echo $msg_install_cancel[$GLOBALS['LANGINDEX']]?>";
            alert(msg);
        }

        function OnSuccessInstall(ack)
        {
            var msg = "";
            var result = '';
        
            var xml = $.parseXML(ack);
            var Is_valid_error_code = $(xml).find("ErrorCode").text();
        
            if(Is_valid_error_code != "")
            {
                var error_code = parseInt(Is_valid_error_code);
                msg += "<?php echo $msg_install_error[$GLOBALS['LANGINDEX']]?> : "+SDK_ERROR_CODES_MAP[error_code];
				if(SDK_ERROR_CODES_MAP[error_code] == "NO ENOUGH SPACE LEFT ON DEVICE") {
					msg +="\nEither space may not be available on disc or maximum count of installed applications reached";
				}
                result = '<span class="emsg"><?php echo $msg_install_error[$GLOBALS['LANGINDEX']]?>.!<\/span><br/><br/>';
                alert(msg);
                //window.location.reload(true);
				reloadAppTableData();
            } else {				
                msg += "<?php echo $msg_install_success[$GLOBALS['LANGINDEX']]?>";
                result = '<span class="emsg"><?php echo $msg_install_success[$GLOBALS['LANGINDEX']]?><\/span><br/><br/>';
                alert(msg);
				//$("#fakeBrowseField").val("");
                window.location.reload(true);
				//reloadAppTableData();
            }
            //document.getElementById("f1_upload_process").innerHTML='';
            document.getElementById('f1_upload_process').style.display = 'none';
            //document.getElementById('f1_upload_form').innerHTML = result + '<input id="myfile" name="myfile" type="file" size="70"/><input type="submit" name="submitBtn" value="<?php echo $t_install[$GLOBALS['LANGINDEX']]?>" />';
            document.getElementById('f1_upload_form').style.display = 'block';
        }

        function OnSuccessHealth(ack)
        {
            var msg = "";

            var xml = $.parseXML(ack);
            var Is_valid_error_code = $(xml).find("ErrorCode").text();

            if(Is_valid_error_code != "")
            {
                var error_code = parseInt(Is_valid_error_code);
                msg += "<?php echo $msg_health_error[$GLOBALS['LANGINDEX']]?> : "+SDK_ERROR_CODES_MAP[error_code];
                alert(msg);
            } else {
                var xml = $.parseXML(ack);
				var appName = $(xml).find("appName").text();
                var app_cpu_usage_percent = $(xml).find("cpuPercent").text();
                var app_mem_usage_percent = $(xml).find("memPercent").text();
                var threads_count = $(xml).find("threadsCnt").text();
                var duration = parseInt($(xml).find("Duration").text());  // Time in seconds
        
                var hours = parseInt( duration / 3600 );     // Time in hours
                var min_balance =  parseInt( duration % 3600 )
                var minutes = parseInt( min_balance / 60 ); // Time in minutes
                var seconds = min_balance % 60;             // Time in seconds

                var result = hours+" Hrs"+" : "+minutes+" Min"+" : "+seconds+" Sec";

                msg += "<?php echo $t_health2[$GLOBALS['LANGINDEX']]?>"+"\n\n";
				msg += "<?php echo $t_appName[$GLOBALS['LANGINDEX']]?> : "+appName+"\n";
                msg += "<?php echo $t_cpuUsage[$GLOBALS['LANGINDEX']]?> : "+app_cpu_usage_percent+" %"+"\n";
                msg += "<?php echo $t_memoryUsage[$GLOBALS['LANGINDEX']]?> : "+app_mem_usage_percent+" %"+"\n";
                msg += "<?php echo $t_threadCount[$GLOBALS['LANGINDEX']]?> : "+threads_count+"\n";
                msg += "<?php echo $t_duration[$GLOBALS['LANGINDEX']]?> : "+result+"\n";
                alert(msg);
				//jAlert(msg,"APPLICATION HEALTH");
            }
        }
		
        function OnSuccessUpdateSettings(ack)
        {
            jAlert("<?php echo $msg_settings_saved[$GLOBALS['LANGINDEX']]?>", "<?php echo $msg_success[$GLOBALS['LANGINDEX']]?>");
        }

        function startUpload()
        {
			if (window.File && window.FileReader && window.FileList && window.Blob) {
				// Great success! All the File APIs are supported.
				var uploadSize = document.getElementById('myfile').files[0].size;
				var uploadSizeInKB = Math.ceil(uploadSize/1024);
				var uploadSizeLimitInKB =(6.5)*1024;
				//console.log("uploadSize: ", uploadSize,"uploadSizeInKB: ",uploadSizeInKB, "uploadSizeLimitInKB: ",uploadSizeLimitInKB);
				if(uploadSizeInKB >= uploadSizeLimitInKB){
					alert("Current File exceed Upload limit\n Please choose a different File");
					return false;
				}
				
			}
			document.getElementById("f1_upload_process").innerHTML='<p><?php echo $msg_uploadProgress[$GLOBALS['LANGINDEX']]?> ...!<br/><img src="../images/opensdk/loader.gif" /><br/></p>';
			document.getElementById('f1_upload_process').style.display = 'block';
			//console.log($('#myfile').val());
			document.getElementById('f1_upload_form').style.display = 'none';
			return true;
        }

        function postUploadDetails(success, App_Name, app_downloaded_directory, error_message_str)
        {
            var result = '';

            if (success == 1)
            {
            	result = '<span class="msg"><?php echo $msg_uploadSucess[$GLOBALS['LANGINDEX']]?>!<\/span><br/><br/>';
                    APP_NAME = App_Name;
            	var msg = "";
            	msg += "<AddSDK>";
            	msg += "<AppName>"+ APP_NAME +"</AppName>";
            	msg += "<AppUploadPath>" + app_downloaded_directory + "</AppUploadPath>";
            	msg += "</AddSDK>";
            	SDKUploadRequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>", 'SDK', 'undefined');

                document.getElementById('f1_upload_process').style.display = 'block';
                return true;
            }
            else
            {
                alert(error_message_str); // Upload failed Alert
                result = '<span class="emsg"><?php echo $msg_uploadError[$GLOBALS['LANGINDEX']]?>!<\/span><br/><br/>';
            }
            //document.getElementById("f1_upload_process").innerHTML='';
            document.getElementById('f1_upload_process').style.display = 'none';
            //document.getElementById('f1_upload_form').innerHTML = result + '<input id="myfile" name="myfile" type="file" size="70"/><input type="submit" name="submitBtn" value="<?php echo $t_install[$GLOBALS['LANGINDEX']]?>" />';
            document.getElementById('f1_upload_form').style.display = 'block';
            return true;
        }

	function timeConverter(UNIX_timestamp){
		var a = new Date(UNIX_timestamp*1000);

		var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
		var dayNames = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"];

		var year = a.getUTCFullYear();
		var month = months[a.getMonth()];
		var date = a.getUTCDate();
		var hours = a.getUTCHours();
		var min = a.getUTCMinutes();
		min = ( min < 10) ? "0"+min : min;
		var sec = a.getSeconds();
		sec = ( sec < 10) ? "0"+ sec : sec;
		// If hour is 0, set it to 24
		//hours = hours || 24;
		hours = (hours  < 10) ? "0"+ hours : hours;
		// var time = date+','+month+' '+year+' '+hours+':'+min+':'+sec ;
		//Thu Sep 19 03:25:11 2013  
		var time = dayNames[a.getDay()]+" "+month+" "+ date+" "+hours + ':' + min + ':' + sec +" " +a.getFullYear();
		return time;
	}
</script>
</head>
<body onselectstart="return false">
	<div id="wrap">
			<?php
				require_once ('left_menu.cgi');
				require_once ('top_menu.cgi');
			?>
			<div id="container" style="width:1500px" >
			<?php
				PrintLeftMenu($_SERVER['SCRIPT_NAME']);
			?>
			<div id="contents" style="width:820px" >
			<div class="sdkVersion" style="width: 100px;float:right; border: 0px solid rgb(153, 153, 153); padding: 0px 5px; font-size: 11px;"><div class="sdkLabel"><?php echo $t_version[$GLOBALS['LANGINDEX']]?>: <?php echo $sdkSearchConf->dataInfo['sdk_version']['value']?></div></div>
				<div class="h3_tit mgt0" style="width:820px;" >
					<h3 class="wid220"><?php echo $menu_opensdk[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>
           <!--<form action="opensdk_upload.cgi" method="post" enctype="multipart/form-data" target="upload_target" onsubmit="startUpload();">-->
           <form action="opensdk_upload.cgi" method="post" enctype="multipart/form-data" target="upload_target" onsubmit="return startUpload();">
				<div id="f1_upload_process" style="display: none"></div>
				<div id="f1_upload_form">
					<!--<input id="file_id" name="myfile" type="file" size="70"/>-->
					<input readonly type="Text" id="fakeBrowseField" class="FileField"/>
					<!-- The fileinput-button span is used to style the file input field as button -->
					<span class="fileinput-button control-button">
						<input type="file" class="control-button" size="1" name="myfile" id="myfile" value="" style="left:0; font-size:20px; height:22px;">
						<span><?php echo $t_browse[$GLOBALS['LANGINDEX']]?></span>
					</span>
					<input type="submit" class="control-button" name="submitBtn" value="<?php echo $t_install[$GLOBALS['LANGINDEX']]?>" />									
				</div>
				<iframe id="upload_target" name="upload_target" src="#" style="width:0;height:0;border:0px solid #fff;"></iframe>
           </form>
				<div style="float:right; padding-top:5px;"><a style="Text-overflow: ellipsis;overflow: hidden;white-space: nowrap;width:210px" href="system_taskmanager2.cgi" id="taskManagerLink" class="btn_type01"><?php echo $t_taskmanager[$GLOBALS['LANGINDEX']]?></a></div>
				<br/>
				<br/>
				 <table id="installed_apps_list"></table> 
			</div>
		</div>
	</div>
</body>
</html>
