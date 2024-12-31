<?php
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_menu.cgi');
require_once ('../language/language_network_8021x.cgi');
require_once ('../language/language_network_ssl.cgi');

$classInstances	= GetClassInstance('8021x');
$IEEE802Dot1xConf = $classInstances['Configuration802Dot1x'];
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

<?php
	if (trim($IEEE802Dot1xConf->setting802Dot1x->dataInfo['PrivateKeyPassword']['value'])=='') {
?>
	var PWset = false;
<?php
	}
	else 
	{
?>
	var PWset = true;
<?php
	}
?>

	var PWInit = false;

	$(document).ready(function(){ lnbonoff("lnb_network");
		//$('#8021x_eapolpw').val(RequestGetConfig("ttttttttttttttttt4"));
		if(<?php echo $IEEE802Dot1xConf->certificate802Dot1x->dataInfo['CaCertificate']['value']; ?>) {
		   $("#ca_certificate_available").css("display", "inline");
		   $("#ca_certificate_not_available").css("display", "none");
		   
		   $("#ca_install_button").css("display", "none");
		   $("#ca_install_button1").css("display", "inline-table");
		   
		   $("#ca_delete_button").css("display", "inline-table");
		   $("#ca_delete_button1").css("display", "none");

		   $('#CA_btn_enable').css("display", "none");
		   $('#CA_btn_disable').css("display", "inline-table");
		   $("#caCertificate").attr("disabled", true);	   
		} else {
		   $("#ca_certificate_available").css("display", "none");
		   $("#ca_certificate_not_available").css("display", "inline");	
		   
		   $("#ca_install_button1").css("display", "none");
		   $("#ca_install_button").css("display", "inline-table");

		   $("#ca_delete_button1").css("display", "inline-table");
		   $("#ca_delete_button").css("display", "none");

		   $('#CA_btn_disable').css("display", "none");
		   $("#caCertificate").attr("disabled", false);
		}
		
		if(<?php echo $IEEE802Dot1xConf->certificate802Dot1x->dataInfo['ClientCertificate']['value']; ?>) {
		   $("#client_certificate_available").css("display", "inline");
		   $("#client_certificate_not_available").css("display", "none");
		   
		   $("#client_install_button").css("display", "none");
		   $("#client_install_button1").css("display", "inline-table");

		   $("#client_delete_button").css("display", "inline-table");
		   $("#client_delete_button1").css("display", "none");
		   
		   $('#cert_btn_enable').css("display", "none");		   
		   $('#cert_btn_disable').css("display", "inline-table");
		   $("#clientCertificate").attr("disabled", true);
			
		} else {
		   $("#client_certificate_available").css("display", "none");
		   $("#client_certificate_not_available").css("display", "inline");
		   
		   $("#client_install_button1").css("display", "none");
		   $("#client_install_button").css("display", "inline-table");

		   $("#client_delete_button1").css("display", "inline-table");
		   $("#client_delete_button").css("display", "none");
		   
		   $('#cert_btn_disable').css("display", "none");
		   $("#clientCertificate").attr("disabled", false);
		}
		
		if(<?php echo $IEEE802Dot1xConf->certificate802Dot1x->dataInfo['ClientPrivateKey']['value']; ?>) {
		   $("#cpk_certificate_available").css("display", "inline");
		   $("#cpk_certificate_not_available").css("display", "none");
		   
		   $("#cpk_install_button").css("display", "none");
		   $("#cpk_install_button1").css("display", "inline-table");

		   $("#cpk_delete_button").css("display", "inline-table");
		   $("#cpk_delete_button1").css("display", "none");
		   
		   $('#CP_btn_enable').css("display", "none");
		   $('#CP_btn_disable').css("display", "inline-table");
		   $("#clientPrivateKey").attr("disabled", true);

		} else {
		   $("#cpk_certificate_available").css("display", "none");
		   $("#cpk_certificate_not_available").css("display", "inline");
		   
		   $("#cpk_install_button1").css("display", "none");
		   $("#cpk_install_button").css("display", "inline-table");

		   $("#cpk_delete_button1").css("display", "inline-table");
		   $("#cpk_delete_button").css("display", "none");
		   
		   $('#CP_btn_disable').css("display", "none");
		   $("#clientPrivateKey").attr("disabled", false);
		}

		if (PWset == true) { 
   			$("#8021x_eapolpw").val("{::::::::}"); // key for maintain password 
   			PWInit = true; 
   		} 

	});

	var relocate_page = "";

	function OnClickApply()
	{
/*		if ($('#8021x_eapolid').val() == '' || $('#8021x_eapolpw').val() == '' )
		{
			alert("<?php echo $msg_invalid_idpw[$GLOBALS['LANGINDEX']]; ?>");
			return;
		}
*/

		var eapolId = $('#8021x_eapolid').val(); 
   		var eapolPw = $('#8021x_eapolpw').val(); 
   		 
   		eapolId = eapolId.replace(/&/gm, '&amp;'); 
   		eapolId = eapolId.replace(/</gm, "&lt;"); 
   		eapolId = eapolId.replace(/>/gm, "&gt;"); 
   		eapolId = eapolId.replace(/\+/gm, '&#43;'); 
		eapolId = eapolId.replace(/\"/gm, "&quot;"); 
    
   		eapolPw = eapolPw.replace(/&/gm, '&amp;'); 
   		eapolPw = eapolPw.replace(/</gm, "&lt;"); 
   		eapolPw = eapolPw.replace(/>/gm, "&gt;"); 
   		eapolPw = eapolPw.replace(/\+/gm, '&#43;'); 
		eapolPw = eapolPw.replace(/\"/gm, "&quot;"); 

		var msg = "<SetConfiguration802Dot1x>";
		msg += "<Enabled>" + ($('#8021x_enable').is(':checked') ? 1 : 0) + "</Enabled>";
		msg += "<Setting>";
		msg += "<EapolVersion>" + $('#8021x_eapolver option:selected').val() + "</EapolVersion>";
		msg += "<EapID>" + eapolId + "</EapID>";
		msg += "<PrivateKeyPassword>" + eapolPw + "</PrivateKeyPassword>";
		msg += "</Setting>";
		msg += "<EAPType>" + $('#8021x_eaptype option:selected').val() + "</EAPType>";
		msg += "</SetConfiguration802Dot1x>";
		RequestAjaxMsg(msg, "<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $GLOBALS['REQUEST_URI'].'?seq='.$_SESSION['count'] ?>", "Audio");
	}

	function auth(auth)
	{
		document.location = "/cgi-bin/onvifconf?auth=" + auth;
	}

	function OnSuccessInstall(req)
	{
		relocate_page = '/home/network_8021x.cgi';
		window.setTimeout("RefreshPage(relocate_page, 1)", 800);
	}

	function RefreshPage(relocate_page, state)
	{
		if (relocate_page == "") 	window.location.reload(true);
		else								window.location.href = relocate_page;
		if (state) window.location.reload(true);
	}

	function OnClickInstallButton(installType, formId)
	{
		var result = valiadteFileBasedOnCertType(installType, formId);
		if(!result) {
			return;
		}
		
		 $('#' + formId).ajaxSubmit({
			success : function (res) {
				if(res == "success") {
				  window.setTimeout("RefreshPage(relocate_page, 0)", 3000);	
				} else {
				  alert("<?php echo $msg_installError_cert[$GLOBALS['LANGINDEX']]; ?>");
				}
			}
		    })
		 return;
		
		 $.ajax({
			url: "network_cert_upload.cgi",
			type: "POST",
			data: formdata,
			processData: false,
			contentType: false,
			async : false,
			success: function (res) {
				if(res == "success") {
				  window.setTimeout("RefreshPage(relocate_page, 0)", 3000);	
				} else {
				  alert("<?php echo $msg_installError_cert[$GLOBALS['LANGINDEX']]; ?>");
				}
			}
		});			
	}
	
	function valiadteFileBasedOnCertType(certType, formId)
	{
		var certFileName;
		var requiredextn = "crt";
		if(certType == 1) {
			certFileName = "caCertificate";
		} else if(certType == 2) {
			certFileName = "clientCertificate";
		} else if(certType == 3) {
			certFileName = "clientPrivateKey";
			requiredextn = "pem";
		}
	
		var element = document.getElementById(certFileName);	
		var fileName = element.value.split('/').pop().split('\\').pop();
		var ext = fileName.split('.').pop();

		//Check for file extension validity.
		if (requiredextn != ext) {		  	
			  alert("<?php echo $msg_wrong_file[$GLOBALS['LANGINDEX']]; ?>");
			  element.focus();
			  return false;
		}
	 return true;		
	}
	
	function OnClickDeleteButton(deleteType)
	{
		var formdata = "certType=" + deleteType + "&action=Delete";
		 $.ajax({
			url: "network_cert_upload.cgi",
			type: "POST",
			data: formdata,
			processData: false,
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

	function setFilename(obj,TextID)
	{
		var fullPath=obj.value
		var filename = fullPath.replace(/^.*[\\\/]/, '')
		$('#'+TextID).val(filename);

	}

	function DoPWInit() 
   	{ 
   		if(PWInit == true) { 
   			$("#8021x_eapolpw").val(""); 
   			PWInit = false; 
   		} 
   	} 


	</script>

	<style>
	object:focus { outline: none; }
	.FileUpload {
		position:relative;
	}
	.FileField {
		height:15px;
		margin-right:12px;
		border:solid 1px #CFD2D9;
		background:#CFD2D9;
		width:200px;
		margin-top: 1px;
	}
	.FileType {
		width:200px; 
		opacity:0; 
		position:absolute; 
		left:0px;
		cursor: pointer;
	}
	.btn_browse {
		display:inline-block;
		width:105px;
		height:20px;
		margin-top:-2px;
		padding-top:2px;
		background:#1b2029;
		text-align:center;
		vertical-align:middle;
		font-weight:bold;
	}
	.btn_browse_disable {
		display:inline-block;
		width:105px;
		height:20px;		
		margin-top:-2px;
		padding-top:2px;
		background:#1b2029;
		text-align:center;
		vertical-align:middle;
		font-weight:bold;
		color:gray;
	}
	.btn_browse:hover {
		background:#0b76d5;
		text-decoration:none;
	}
	.btn_browse input {
		position: absolute;
		top: 0;
		left: 220px;
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
					<h3 style="width:450px;"><?php echo $t_8021xSetup[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>
				<table class="data_write">
					<colgroup>
						<col style="width:212px;" />
						<col />
					</colgroup>
					<tbody>
						<tr>
							<th scope="row">IEEE 802.1x</th>
							<td>
								<label><input type="checkbox" id="8021x_enable" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" <?php if ($IEEE802Dot1xConf->dataInfo['Enabled']['value'] == 1) { echo "checked=\"checked\""; } ?>/><?php echo $t_use[$GLOBALS['LANGINDEX']]; ?></label>
							</td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_EAPType[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<select id="8021x_eaptype" class="selectbox_style" >
									<option value="0" <?php if ($IEEE802Dot1xConf->dataInfo['EAPType']['value'] == 0) { echo "selected=\"selected\""; } ?> >EAP-TLS</option>
									<option value="1" <?php if ($IEEE802Dot1xConf->dataInfo['EAPType']['value'] == 1) { echo "selected=\"selected\""; } ?> >LEAP</option>
								</select>
							</td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_eapolVer[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<select id="8021x_eapolver" class="selectbox_style" >
									<option value="1" <?php if ($IEEE802Dot1xConf->setting802Dot1x->dataInfo['EapolVersion']['value'] == 1) { echo "selected=\"selected\""; } ?> >1</option>
									<option value="2" <?php if ($IEEE802Dot1xConf->setting802Dot1x->dataInfo['EapolVersion']['value'] == 2) { echo "selected=\"selected\""; } ?> >2</option>
								</select>
							</td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_ID[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<input type="text" id="8021x_eapolid" class="text" style="width:191px;" value="<?php echo htmlspecialchars($IEEE802Dot1xConf->setting802Dot1x->dataInfo['EapID']['value'], ENT_QUOTES); ?>" maxlength="30" onKeyPress='return IsBackSlashOrSmallQuote(event); NoKorean(event)' onkeydown='NoKorean(event)'/>
							</td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_password[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<input type="password" id="8021x_eapolpw" class="text" style="width:191px;" maxlength="30"  onclick='DoPWInit();' onKeyPress='return IsBackSlashOrSmallQuote(event); NoKorean(event);DoPWInit();' onkeydown='NoKorean(event);DoPWInit();'/>
							</td>
						</tr>
					</tbody>
				</table>
				<div class="h3_tit">
					<h3 class="wid220"><?php echo $t_certificate[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>
				<table class="data_write">
					<colgroup>
						<col style="width:212px;" />
						<col />
					</colgroup>
					<tbody>
						
							<tr>
								<th><?php echo $t_ca_cert[$GLOBALS['LANGINDEX']]; ?></th>
								<td>
									<div class="FileUpload">				
										<form id="caCertificateForm" action="network_cert_upload.cgi" method="Post" enctype="multipart/form-data" > 
											<input type="text" readonly id="CAText" name="CAText" class="FileField" />											
											<span id="CA_btn_enable" class="btn_browse">
												<input type="file" name="certificateFile" id="caCertificate" accept=".crt"  onchange="setFilename(this,'CAText')" style="font-size:20px; height:22px;" />
												<span><?php echo $t_browse[$GLOBALS['LANGINDEX']]; ?></span>								
											</span>
											<span id="CA_btn_disable" class="btn_browse_disable">
												<span><?php echo $t_browse[$GLOBALS['LANGINDEX']]; ?></span>
											</span>
											<input type='hidden' name="certType" value="1" />
											<input type='hidden' name="action" value="Install" />
										</form>
									</div>
								</td>
							</tr>
						
						<tr>
							<td></td>
							<td>
					      	<a id="ca_install_button" class="btn_type01 btn_type01_08" href="javascript:OnClickInstallButton(1, 'caCertificateForm')"> <?php echo $t_install[$GLOBALS['LANGINDEX']]; ?> </a>
					       	<a id="ca_install_button1" class="btn_type01_disable btn_type01_08" style="color:grey; display:none"> <?php echo $t_install[$GLOBALS['LANGINDEX']]; ?> </a>

					       	<a id="ca_delete_button" class="btn_type01 btn_type01_08" href="javascript:OnClickDeleteButton(1)" style="display:none;margin-left:10px"> <?php echo $t_delete[$GLOBALS['LANGINDEX']]; ?>  </a>	        
								<a id="ca_delete_button1" class="btn_type01_disable btn_type01_08" style="color:grey;margin-left:10px "> <?php echo $t_delete[$GLOBALS['LANGINDEX']]; ?>  </a>

								<span id="ca_certificate_available" style="color:green;display:none"> <b> <?php echo $t_installed[$GLOBALS['LANGINDEX']]; ?>  </b> </span>	
								<span id="ca_certificate_not_available" style="color:red"> <b> <?php echo $t_not_available  [$GLOBALS['LANGINDEX']]; ?> </b> </span>	
							</td>
						</tr>
							<tr>
								<th><?php echo $t_client_cert[$GLOBALS['LANGINDEX']]; ?></th>
								<td>
									<div class="FileUpload">
										<form id="clientCertificateForm" action="/home/setup/network_cert_upload.cgi" method="Post" enctype="multipart/form-data" > 
											<input type="text" readonly id="CCText" name="CCText" class="FileField" />
											
											<span id="cert_btn_enable" class="btn_browse" >
												<input type="file" name="certificateFile" id="clientCertificate" accept=".crt"  onchange="setFilename(this,'CCText')" style="font-size:20px; height:22px;" />
												<span><?php echo $t_browse[$GLOBALS['LANGINDEX']]; ?></span>
											</span>
											<span id="cert_btn_disable" class="btn_browse_disable">
												<span><?php echo $t_browse[$GLOBALS['LANGINDEX']]; ?></span>
											</span>
											<input type='hidden' name="certType" value="2" />
											<input type='hidden' name="action" value="Install" />
										</form>	
									</div>
								</td>
							</tr>						
						<tr>
							<td></td>
							<td>
					     		<a id="client_install_button" class="btn_type01 btn_type01_08" href="javascript:OnClickInstallButton(2, 'clientCertificateForm')" > <?php echo $t_install[$GLOBALS['LANGINDEX']]; ?> </a>
					    		<a id="client_install_button1" class="btn_type01_disable btn_type01_08" style="color:grey; display:none" > <?php echo $t_install[$GLOBALS['LANGINDEX']]; ?> </a>

					      	<a id="client_delete_button" class="btn_type01 btn_type01_08" href="javascript:OnClickDeleteButton(2)"  style="display:none;margin-left:10px" > <?php echo $t_delete[$GLOBALS['LANGINDEX']]; ?>  </a>
								<a id="client_delete_button1" class="btn_type01_disable btn_type01_08" style="color:grey;margin-left:10px" > <?php echo $t_delete[$GLOBALS['LANGINDEX']]; ?>  </a>

								<span id="client_certificate_available" style="color:green;display:none"> <b> <?php echo $t_installed[$GLOBALS['LANGINDEX']]; ?>  </b> </span>	
								<span id="client_certificate_not_available" style="color:red"> <b> <?php echo $t_not_available  [$GLOBALS['LANGINDEX']]; ?>   </b> </span>	
							</td>
						</tr>
							<tr>
								<th><?php echo $t_client_private_key[$GLOBALS['LANGINDEX']]; ?></th>
								<td>
									<div class="FileUpload">
										<form id="clientPrivateKeyForm" action="/home/setup/network_cert_upload.cgi" method="Post" enctype="multipart/form-data" > 
											<input type="text" readonly id="CPText" name="CPText" class="FileField" />

											<span id="CP_btn_enable" class="btn_browse" >
												<input type="file" name="certificateFile" id="clientPrivateKey" accept=".pem"  onchange="setFilename(this,'CPText')" style="font-size:20px; height:22px;" />  
												<span><?php echo $t_browse[$GLOBALS['LANGINDEX']]; ?></span>
											</span>
											<span id="CP_btn_disable" class="btn_browse_disable">
												<span><?php echo $t_browse[$GLOBALS['LANGINDEX']]; ?></span>
											</span>
											<input type='hidden' name="certType" value="3" />
											<input type='hidden' name="action" value="Install" />
										</form>
									</div>
								</td>
							</tr>
						<tr>
							<td></td>
							<td>
						      <a id="cpk_install_button" class="btn_type01 btn_type01_08" href="javascript:OnClickInstallButton(3, 'clientPrivateKeyForm')" > <?php echo $t_install[$GLOBALS['LANGINDEX']]; ?> </a>
						      <a id="cpk_install_button1" class="btn_type01_disable btn_type01_08" style="color:grey; display:none" > <?php echo $t_install[$GLOBALS['LANGINDEX']]; ?> </a>
						       
						      <a id="cpk_delete_button" class="btn_type01 btn_type01_08" href="javascript:OnClickDeleteButton(3)" style="display:none;margin-left:10px" > <?php echo $t_delete[$GLOBALS['LANGINDEX']]; ?>  </a>
						      <a id="cpk_delete_button1" class="btn_type01_disable btn_type01_08" style="color:grey;margin-left:10px" > <?php echo $t_delete[$GLOBALS['LANGINDEX']]; ?>  </a>
						       
						      <span id="cpk_certificate_available" style="color:green;display:none"> <b> <?php echo $t_installed[$GLOBALS['LANGINDEX']]; ?>  </b> </span>	
						      <span id="cpk_certificate_not_available" style="color:red"> <b> <?php echo $t_not_available  [$GLOBALS['LANGINDEX']]; ?>  </b> </span>	
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

