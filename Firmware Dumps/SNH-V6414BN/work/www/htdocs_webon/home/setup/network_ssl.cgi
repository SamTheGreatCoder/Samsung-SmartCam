<?php
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_menu.cgi');
require_once ('../language/language_network_ssl.cgi');

$classInstances = GetClassInstance('https');
$httpsConf	= $classInstances['HTTPSConfiguration'];
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="kr" xml:lang="kr">
<head>
	<title>iPOLiS NETWORK CAMERA WEBVIEWER</title>
	<meta http-equiv="X-UA-Compatible" content="IE=Edge; requiresActiveX=true">
	<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
	<link rel="stylesheet" type="text/css" href="../css/techwin.css" />
	
	<script type="text/javascript" src="../js/jquery-1.9.1.js"></script>
	<script type="text/javascript" src="../js/jquery.form.js"></script>
	<script type="text/javascript" src="../js/lnb.js"></script>
	<script type="text/javascript" src="../js/common_function.js"></script>
	<script type="text/javascript" language="javascript">
	
	var localSeq				= <?php echo $_SESSION['count']; ?>;

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
	lnbonoff("lnb_network");
	
		$("ssl-set").disabled = false;
		var currentMode = parseInt(<?php echo $httpsConf->dataInfo['Mode']['value']; ?>);
		var installCertName = "<?php echo $httpsConf->dataInfo['PublicCertName']['value']; ?>";

		if (installCertName.length == 0) {
			$("#delete_button").css("display", "none");
			$("#delete_button1").css("display", "inline-table");

			$("#certificateName").attr("readonly", false);
			$("#install_button").css("display" , "inline-table");
			$("#install_button1").css("display" , "none");

			$(".btn_browse_disable").css("display", "none");
			$("#certificateFile").attr("disabled", false);
			$("#keyFile").attr("disabled", false);
			if (currentMode == 1) {
				$("#install_button").css("display" , "none");
				$("#install_button1").css("display" , "inline-table");
				
				$(".btn_browse").css("display" , "none");
				$(".btn_browse_disable").css("display", "inline-table");
				$("#certificateFile").attr("disabled", true);				
				$("#keyFile").attr("disabled", true);
			}
			else if (currentMode == 0) {
				$("#install_button").css("display" , "inline-table");
				$("#install_button1").css("display" , "none");
			}
			$('#https_public').attr('disabled', 'disabled');
		}
		else {
			$("#certificateName").val(installCertName);
			$("#certificateName").attr("readonly", true);
			$("#certificateName").attr("disabled", true);
			
			$("#install_button").css("display" , "none");
			$("#install_button1").css("display" , "inline-table");
			
			$(".btn_browse").css("display" , "none");
			$(".btn_browse_disable").css("display", "inline-table");
			$("#certificateFile").attr("disabled", true);
			$("#keyFile").attr("disabled", true);
			
			if(currentMode == 2) {
				$("#delete_button").css("display" , "none");
				$("#delete_button1").css("display" , "inline-table");
			}
			else if (currentMode == 0 || currentMode == 1) {
				$("#delete_button").css("display" , "inline-table");
				$("#delete_button1").css("display" , "none");
			}
		}
	});

	var relocate_page = "/home/setup/network_ssl.cgi";
	var IsChangedCertificate = 0;

	function OnClickApply()
	{
		if (IsChangedCertificate == 1) return;

		var secureSelect = 2;
		if 		($('#http').is(':checked')) 		secureSelect = 0;
		else if 	($('#https_self').is(':checked'))	secureSelect = 1;
		var msg = "<SetHTTPS><Mode>"+secureSelect+"</Mode></SetHTTPS>";

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
			data: encodeURIComponent(msg)
		});

		alert("<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>");
		SetPolicy(secureSelect);
	}

	function auth(auth)
	{
		document.location = "/cgi-bin/onvifconf?auth=" + auth;
	}

	function OnClickInstall(publicCertName, certLength, certData, keyLength, keyData)
	{
		var msg = "<SetHTTPSData>";
		msg += "<PublicCertName>"+publicCertName+"</PublicCertName>";
		msg += "<CertLength>"+certLength+"</CertLength>";
		msg += "<CertData>"+certData+"</CertData>";
		msg += "<KeyLength>"+keyLength+"</KeyLength>";
		msg += "<KeyData>"+keyData+"</KeyData>";
		msg += "</SetHTTPSData>";

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
			data: encodeURIComponent(msg)
		});

		window.setTimeout('window.location.reload(true)', 3000);
	}

	function OnSuccessInstall(req)
	{
		relocate_page = '/home/network_ssl.cgi';
		window.setTimeout("RefreshPage(relocate_page, 1)", 3000);
	}

	function OnClickRemove(publicCertName)
	{
		if (confirm("<?php echo $msg_delete[$GLOBALS['LANGINDEX']];?>")) {
			var msg = "<RemoveHTTPSData><PublicCertName>"+publicCertName+"</PublicCertName></RemoveHTTPSData>";
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
				data: encodeURIComponent(msg)
			});
			relocate_page = '/home/network_ssl.cgi';
			window.setTimeout("RefreshPage(relocate_page, 1)", 3000);
		}
	}

	function SetPolicy(secureSelect)
	{
		var the_hostname	= document.location.hostname;
		var ipaddr			= the_hostname.split(':');
		var ipv6addr		= false;
		var httpsmode		= 0;
		var httpPort		= <?php echo $classInstances['Information']->dataInfo['HttpPort']['value']; ?>;
		var httpsPort		= <?php echo $classInstances['NetworkProtocols']->protocol[1]->dataInfo['Port']['value']; ?>;
		var control 		= $('#sslUploader').get(0);

		httpsmode = parseInt(<?php echo $httpsConf->dataInfo['Mode']['value']; ?>);

		if (ipaddr.length > 1) {
			ipv6addr = true;
			the_hostname = the_hostname.replace('[', '');
			the_hostname = the_hostname.replace(']', '');
		}

		if (httpsmode == 0 && secureSelect == 0) {
			relocate_page = 'http://';
			if (ipv6addr) relocate_page += '[';
			relocate_page += the_hostname;
			if (ipv6addr) relocate_page += ']';
			if (httpPort != 80) relocate_page += ':'+httpPort;
			relocate_page += '/home/setup/network_ssl.cgi';
		}
		else if (httpsmode == 0 && secureSelect != 0) {
			relocate_page = 'https://';
			if (ipv6addr) relocate_page += '[';
			relocate_page += the_hostname;
			if (ipv6addr) relocate_page += ']';
			if (httpPort != 443) relocate_page += ':'+httpsPort;
			relocate_page += '/home/setup/network_ssl.cgi';
		}
		else if (httpsmode == 1 && secureSelect == 0) {
			relocate_page = 'http://';
			if (ipv6addr) relocate_page += '[';
			relocate_page += the_hostname;
			if (ipv6addr) relocate_page += ']';
			if (httpPort != 80 && httpPort != 443) relocate_page += ':'+httpPort;
			relocate_page += '/home/setup/network_ssl.cgi';
		}
		else if (httpsmode == 1 && secureSelect != 0) {
			relocate_page = 'https://';
			if (ipv6addr) relocate_page += '[';
			relocate_page += the_hostname;
			if (ipv6addr) relocate_page += ']';
			if (httpPort != 80 && httpPort != 443) relocate_page += ':'+httpPort;
			relocate_page += '/home/setup/network_ssl.cgi';
		}
		else if (httpsmode == 2 && secureSelect != 0) {
			relocate_page = 'https://';
			if (ipv6addr) relocate_page += '[';
			relocate_page += the_hostname;
			if (ipv6addr) relocate_page += ']';
			if (httpPort != 443) relocate_page += ':'+httpsPort;
			relocate_page += '/home/setup/network_ssl.cgi';
		}
		else if (httpsmode == 2 && secureSelect == 0) {
			relocate_page = 'http://';
			if (ipv6addr) relocate_page += '[';
			relocate_page += the_hostname;
			if (ipv6addr) {
				var xp = control.content.SSLUploaderControl.isXP();
				if (xp) {
					relocate_page += "%";
					relocate_page += "2";
					relocate_page += "5";
					relocate_page += "4";
				}
				relocate_page += ']';
			}
			if (httpPort != 80 && httpPort != 443) relocate_page += ':'+httpPort;
			relocate_page += '/home/setup/network_ssl.cgi';
		}
		window.setTimeout("RefreshPage(relocate_page, 0)", 3000);
	}

	function RefreshPage(relocate_page, state)
	{	
		window.location.href = relocate_page;
		if (state) window.location.reload(true);
	}

	function SetCertificateInstallling()
	{
		IsChangedCertificate = 1;
	}

	function OnClickDeleteButton() {
		var formData;
		var certName = $("#certificateName").val();	 		
		formData = 'certificateName=' + certName + '&action=Delete';
				
		$.ajax({
			url: "ssl_cert_upload.cgi",
			type: "POST",
			data: formData,
			processData: false,
			contentType: "application/x-www-form-urlencoded",
			async : false,
			success: function (res) {
				if(res == "success") {
				  window.setTimeout("RefreshPage(relocate_page, 0)", 3000);	
				} else {
				  alert("<?php echo $msg_deleteError_cert[$GLOBALS['LANGINDEX']]; ?>");
				}
			}
		});		
	}
	
	function OnClickInstallButton() {		
	
	   var certName = $("#certificateName").val();	   
	   if(!certName) {
		 alert("<?php echo $msg_please_input_certname[$GLOBALS['LANGINDEX']]; ?>");
		 $("#certificateName").focus();
		 return;
	   }

		var element = document.getElementById("certificateFile");	
		//var file = element.files[0];
		var fileName = element.value.split('/').pop().split('\\').pop();
		var ext = fileName.split('.').pop();

		//Check for file extension validity.
		if (ext != "crt") {
			  alert("<?php echo $msg_wrong_file[$GLOBALS['LANGINDEX']]; ?>");
			  element.focus();
			  return;
		}
		
		var element = document.getElementById("keyFile");	
		//var file = element.files[0];
		var fileName = element.value.split('/').pop().split('\\').pop();
		var ext = fileName.split('.').pop();
		
		//Check for file extension validity.
		if (ext != "key") {
			alert("<?php echo $msg_wrong_file[$GLOBALS['LANGINDEX']]; ?>");
			element.focus();
			return;
		}
		
		$('form').ajaxSubmit({
			success : function (res) {
			//console.log(res);
				if(res == "success") {
				  window.setTimeout("RefreshPage(relocate_page, 0)", 3000);	
				} else {
				  alert("<?php echo $msg_installError_cert[$GLOBALS['LANGINDEX']]; ?>");
				}
			}
		       //target: 'myResultsDiv'
		})
		    
		 return;
	}	

	function setFilename(obj,TextID){
	
				var fullPath=obj.value
				var filename = fullPath.replace(/^.*[\\\/]/, '')
				$('#'+TextID).val(filename);
		
	}
	</script>

	<style>
	.FileUpload {
		position:relative;
	}
	.FileField {
		height:15px;
		margin-right:12px;
		border:solid 1px #CFD2D9;
		background:#CFD2D9;
		width:260px;
		margin-top: 1px;
	}
	.FileType {
		width:260px; 
		opacity:0; 
		position:absolute; 
		left:0px;
		cursor: pointer;
	}
	.btn_browse {
		display:inline-block;
		width:105px;
		height:20px;
		padding-top:2px;
		background:#1b2029;
		text-align:center;
		font-weight:bold;
	}
	.btn_browse_disable {
		display:inline-block;
		width:105px;
		height:20px;
		padding-top:2px;
		background:#1b2029;
		text-align:center;
		font-weight:bold;
		color:gray;
	}
	
	.btn_browse:hover {
		background:#0b76d5;
		text-decoration:none;
	}
	.btn_browse input {
		position: absolute;
		top: 1px;
		left: 280px;
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
	</style>
	</head>
	
	<body onselectstart="return false">
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
					<h3 class="wid320"><?php echo $t_secureConnection[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>
				<table class="data_write">
					<colgroup>
						<col />
					</colgroup>
					<tbody>
						<tr>
							<td><label class="labelBold"><input type="radio" name="ssl_type" id="http" <?php if ($httpsConf->dataInfo['Mode']['value'] == 0) echo "checked=\"checked\""; ?>/><?php echo $t_http[$GLOBALS['LANGINDEX']]; ?></label></td>
						</tr>
						<tr>
							<td><label class="labelBold"><input type="radio" name="ssl_type" id="https_self" <?php if ($httpsConf->dataInfo['Mode']['value'] == 1) echo "checked=\"checked\""; ?>/><?php echo $t_https[$GLOBALS['LANGINDEX']]; ?></label></td>
						</tr>
						<tr>
							<td><label class="labelBold"><input type="radio" name="ssl_type" id="https_public" <?php if ($httpsConf->dataInfo['Mode']['value'] == 2) echo "checked=\"checked\""; ?>/><?php echo $t_httpsp[$GLOBALS['LANGINDEX']]; ?></label></td>
						</tr>
					</tbody>
				</table>
				<div class="h3_tit">
					<h3 class="wid280"><?php echo $t_installCertificate[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>				
				<form id="installCertificate" name="installCertificate" action="/home/setup/ssl_cert_upload.cgi" method="Post" enctype="multipart/form-data">
					<table class="data_write">
						<colgroup>
							<col style="width:200px;" />
							<col />
						</colgroup>
						<tbody>
							<tr>
								<th>
									<?php echo $t_nameofCertificate[$GLOBALS['LANGINDEX']]; ?>
								</th>
								<td>
						      	<input type="text" name="certificateName" id="certificateName" class="text" size="40" onkeypress="IsNumChar(event);" onkeydown="CheckKorean(event);"
						      		maxlength="31" style="width:<?php if (GetBrowserName()=='Google Chrome') {echo '258px';} else {echo '260px';} ?>; "/>
						      	<input type="hidden" value="Install" name="action" id="action" />	
								</td>
							</tr>
							<tr>
								<th>
									<?php echo $t_certfile[$GLOBALS['LANGINDEX']]; ?>
								</th>
								<td>
									<div class="FileUpload">
										<input type="text" readonly id="CCText" name="CCText" class="FileField" />			
									
										<span class="btn_browse">
											<input type="file" name="certificateFile" id="certificateFile" accept=".crt" onchange="setFilename(this,'CCText')" style="font-size:20px; height:22px;"/>
											<span id="browse"><?php echo $t_browse[$GLOBALS['LANGINDEX']]; ?></span>
										</span>
										<span class="btn_browse_disable">
											<span id="browse"><?php echo $t_browse[$GLOBALS['LANGINDEX']]; ?></span>
										</span>
									</div> 
								</td>
							</tr>
							<tr>
								<th>
									<?php echo $t_keyfile[$GLOBALS['LANGINDEX']]; ?>
								</th>
								<td>
									<div class="FileUpload">
										<input type="text" readonly id="keyText" name="keyText" class="FileField" />

										<span class="btn_browse">
											<input type="file" name="keyFile" id="keyFile" accept=".key"  onchange="setFilename(this,'keyText')" style="font-size:20px; height:22px;" />  
											<span id="browse"><?php echo $t_browse[$GLOBALS['LANGINDEX']]; ?></span>
										</span>
										<span class="btn_browse_disable">
											<span id="browse"><?php echo $t_browse[$GLOBALS['LANGINDEX']]; ?></span>
										</span>
									</div>
								</td>
							</tr>
							<tr>
								<td>
									&nbsp; 
								</td>
								<td>
							      <a id="install_button" class="btn_type01 btn_type01_08" href="javascript:OnClickInstallButton()" > <?php echo $t_install[$GLOBALS['LANGINDEX']]; ?> </a>
							      <a id="install_button1" class="btn_type01_disable btn_type01_08" style="color:grey;display:none" > <?php echo $t_install[$GLOBALS['LANGINDEX']]; ?> </a>

							      <a id="delete_button" class="btn_type01 btn_type01_08" href="javascript:OnClickDeleteButton()" style="display:none;margin-left:10px"> <?php echo $t_delete[$GLOBALS['LANGINDEX']]; ?> </a>
							      <a id="delete_button1" class="btn_type01_disable btn_type01_08 " style="color:grey;margin-left:10px" > <?php echo $t_delete[$GLOBALS['LANGINDEX']]; ?> </a>
								</td>
							</tr>
						</tbody>
					</table>
				</form>

				<div class="btn_right">
					<a id="mid_ok_btn" class="btn_apply" href="javascript:OnClickApply()"><?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?></a>
				</div>
				</div>
			</div>
		</div>
	</div>
</body>
</html>
