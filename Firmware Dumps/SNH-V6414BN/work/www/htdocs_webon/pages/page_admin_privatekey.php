<?php
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";
require_once $_SERVER["DOCUMENT_ROOT"] . "/resources/languages/Language.php";

$_SESSION["GROUP"] = "Admin";
$_SESSION["PAGE"] = "admin_privatekey";
?>

<? include $_SERVER["DOCUMENT_ROOT"] . "/common/html_head.php"; ?>
	<script type="text/javascript">
		function changePrivateKey(){
			if($("#current_key").val() == ""){
				alert('<?=$Lang["Enter the current private key"]?>');
				$("#current_key").focus();
				return;
			}
			if($("#private_key").val() == ""){
				alert('<?=$Lang["Enter the new private key"]?>');
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
			if($("#current_key").val() == $("#private_key").val()){
				alert('<?=$Lang["The new private key is the same as the current one."]?>');
				$("#private_key").val("");
				$("#private_key").focus();
				return;
			}
			
			showProgress('<?=$Lang["Updating the camera"]?>');
			var sendData = "SET;";
			sendData += $("#current_key").val() + ";" + $("#private_key").val();

			$.post("/classes/class_admin_privatekey.php", {data: sendData}, returnSetMessage, "text");
		}
		function returnSetMessage(resp){
			var recvData = resp.split(";");
			hideProgress();
			
			if(recvData[0] == "OK"){
				alert('<?=$Lang["Changes saved."]?>');
				moveToPage("pages/camera_login.php");
			}else{
				if(recvData[1] == null || recvData[1] == ""){
					alert('<?=$Lang["Failed to save."]?>');
				}else{
					alert(recvData[1]);
				}
			}
		}
	</script>
</head>

		<? include $_SERVER["DOCUMENT_ROOT"] . "/common/header.php"; ?>
	
		<!-- s:height100% -->
		<div id="hgt100">
			<!-- s:contBox_cl -->
			<div id="contBox_cl" class="floatClear">
			
				<? include $_SERVER["DOCUMENT_ROOT"] . "/common/side_menu.php"; ?>
				
				<!-- s:컨텐츠 영역 -->
				<div id="contDiv2">
					<!-- s:Change Private Key -->
					<h2 class="cl_tit"><?=$Lang["Change Private Key"]?></h2>
					<p> <!-- insert contents -->  </p>			
					<div id="ad" class="cl_gBox">
						<div class="cl_cBox nbd">						
							<dl class="floatClear">
								<dt>
									<label for="current_key"><?=$Lang["Current Private Key"]?></label></dt>
								<dd>
									<input type="password" id="current_key" maxlength="8" onkeyup="keyPassword(event);"/>
								</dd>	
								<dt><label for="private_key"><?=$Lang["New Private Key"]?></label></dt>
								<dd>
									<input type="password" id="private_key" maxlength="8" onkeyup="keyPassword(event);"/>
								</dd>	
								<dt><label for="confirm_key"><?=$Lang["Confirm private key"]?></label></dt>
								<dd>
									<input type="password" id="confirm_key" maxlength="8" onkeyup="keyPassword(event);"/>
								</dd>	
							</dl>
						</div>
						<div class="cl_txt">
							<?=$Lang["Enter 1-8 alphanumeric characters."]?>
						</div>
						<div class="cl_btnBox">
							<button type="button" class="btnTxt bType1" onclick="changePrivateKey();"><?=$Lang["Apply"]?></button>
						</div>
					</div>
					<!-- e:Change Private Key -->				
				</div>
				<!-- e:컨텐츠 영역 -->
			 </div>
			<!-- e:contBox_cl --> 
		</div>
		<!-- e:height100% -->
		
		<? include $_SERVER["DOCUMENT_ROOT"] . "/common/footer.php"; ?>
	</div>
</body>
</html>