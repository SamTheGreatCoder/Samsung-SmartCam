<?php
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";
session_start();

$result = requestToCamera(CMD_SYSTEM_CONFIGURATION, ACTION_GET, TYPE_REQUEST, null);
$language = 0; $error = "";
 if($result[0] == "OK"){
 	$language = $result[1][512];	//Language
 }else{
 	$error = $result[1];
 }
 
$_SESSION["LANGUAGE"] = $language;
require_once $_SERVER["DOCUMENT_ROOT"] . "/resources/languages/Language.php";

// $langList = array("English", "한국어", "中国的", "français", "italiano", "español", "Deutsch");
$langList = array("English", "한국어", "", "français", "italiano", "español", "Deutsch");
?>

<? include $_SERVER["DOCUMENT_ROOT"] . "/common/html_head.php"; ?>
<script type="text/javascript">
		var lang = '<?=$language?>';		
		var isNew = false;
		
		$(document).ready(function(){
			$("#private_key").focus();			
		});
		
		$(function(){
	    	$("#private_key:password").keydown(function(e){
				if(e.keyCode == 13){
					if(isNew){
						$("#confirm_key").focus();	
					}else{
						loginCamera();
					}					
				}
			});
		});   

		$(function(){
	    	$("#confirm_key:password").keydown(function(e){
				if(e.keyCode == 13){
					createNewPrivateKey();
				}
			});
		});  

		function runLogin(){
			if(isNew){
				createNewPrivateKey();
			}else{
				loginCamera();
			}
		}
		
		function changeLanguage(){
			lang = $("#sltLang option:selected").val();
		}
		
		function loginCamera(){		
			if($("#private_key").val() == ""){
				alert('<?=$Lang["Enter the private key."]?>');
				$("#private_key").focus();
			}else{
				showProgress('<?=$Lang["Connecting to the camera, please wait"]?>');
				var sendData = "CHECK;" + $("#private_key").val();			
				$.post("/classes/class_admin_privatekey.php", {data: sendData}, returnCheckMessage, "text");
	    	}
		}
		function returnCheckMessage(resp){
			var respData = resp.split(";");
			if(respData[0] == "OK"){
				var sendData = "LANGUAGE;" + '<?=implode(",", $result[1])?>' + ";" + lang;
				$.post("/classes/class_admin_firmware.php", {data: sendData}, returnSetMessage, "text");
			}else if(respData[0] == "NOKEY"){
				hideProgress();
				isNew = true;
				alert('<?=$Lang["The camera has no private key installed."]?>' + "\n" + '<?=$Lang["Please create a new private key."]?>');
				document.getElementById("div_confirm").style.display = "block";
				document.getElementById("div_lang").style.display = "none";
				$("#private_key").val("");
				$("#private_key").focus();
			}else{
				hideProgress();
				alert('<?=$Lang["Incorrect private key."]?>');
				$("#private_key").val("");
				$("#private_key").focus();
			}
		}
		function returnSetMessage(resp){
			var respData = resp.split(";");
			
			hideProgress();
			if(respData[0] == "OK"){
				moveToPage("pages/page_video_live.php");
			}
		}

		function createNewPrivateKey(){
			if($("#private_key").val() == ""){
				alert('<?=$Lang["Enter the private key."]?>');
				$("#private_key").focus();
				return;
			}
			if($("#confirm_key").val() == ""){
				alert('<?=$Lang["Re-enter the new private key"]?>');
				$("#confirm_key").focus();
				return;
			}
			if($("#private_key").val() != $("#confirm_key").val()){
				alert('<?=$Lang["New private key does not match, please enter again"]?>');
				$("#confirm_key").val("");
				$("#confirm_key").focus();
				return;
			}
						
			showProgress('<?=$Lang["Updating the camera"]?>');
			var sendData = "NEW;" + $("#private_key").val();

			$.post("/classes/class_admin_privatekey.php", {data: sendData}, returnNewMessage, "text");
		}
		function returnNewMessage(resp){
			var respData = resp.split(";");

			hideProgress();
			if(respData[0] == "OK"){
				moveToPage("pages/page_video_live.php");
			}else{				
				alert('<?=$Lang["Failed to save."]?>');
				$("#private_key").val("");
				$("#confirm_key").val("");
				$("#private_key").focus();
			}
		}
	</script>
</head>
<body>
	<div id="wrap_cl">
		<!-- s:Skip Navigation --><a class="hide" href="#contBox_cl">Skip Navigation</a> <!-- e:Skip Navigation -->
		<!-- s:header_cl -->
		<div id="header_cl" class="floatClear">
		</div>
		<!-- e:header_cl -->
		<!-- s:height100% -->
		<div id="hgt100">
			<!-- s:contBox_cl -->
			<div id="contBox_cl" class="floatClear">
				<!-- s:컨텐츠 영역 -->
				<div id="prvk">
					<div id="camera_login_ci">
						<img src="/resources/images/smartcam_ci.png" class="ci_logo" alt="Samsung SmartCam" />
						<div class="msg">						
							<p><?=$Lang["To access the camera, enter the private key for the camera you selected."]?></p>
							<div class="pk">
								<div>
									<span><?=$Lang["Private Key"]?> : </span>
									<input type="password" id="private_key" class="input_w1" onkeydown="return keyPassword(event);" style="ime-mode:disabled" maxlength="8"/>
								</div>
								<div id="div_confirm" style="display:none">
									<span><?=$Lang["Confirm Key"]?> : </span> 
									<input type="password" id="confirm_key" class="input_w1" onkeydown="return keyPassword(event);" style="ime-mode:disabled" maxlength="8"/>
								</div>
								<div id="div_lang">
									<span><?=$Lang["Language"]?> : </span>
									<select id="sltLang" name="sltLang" onchange="changeLanguage();">
									<?	for($i=0; $i<count($langList); $i++){
											if($langList[$i] != null && $langList[$i] != ""){
												if($i == $language){
													echo "<option value='" . $i ."' selected>" . $langList[$i] . "</option>";
												}else{
													echo "<option value='" . $i ."'>" . $langList[$i] . "</option>";
												}
											}
										}
									?>
									</select>	
								</div>
							</div>				
						</div>					
						<div class="btnBox">
							<button type="button" class="btn_ty2 btn_colorGray3 btn_w1" onclick="runLogin();"><span><?=$Lang["OK"]?></span></button>
						</div>
					</div>
				</div>
				<!-- e:컨텐츠 영역 -->
			 </div>
			<!-- e:contBox_cl --> 
		</div>
		<!-- e:height100% -->

	<? include $_SERVER["DOCUMENT_ROOT"] . "/common/footer.php"; ?>
</body>
</html>