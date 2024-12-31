<? include $_SERVER["DOCUMENT_ROOT"] . "/pages/page_sns.php"; ?>
<? include $_SERVER["DOCUMENT_ROOT"] . "/common/html_head.php"; ?>
<? require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php"; ?>

<?
$temp = array(0, 0, 0, 0);
$cmos = array_fill(0, 120, 0x00);
$newCmos = array_fill(0, 478, 0x00);
$vdo_src = array_fill(0, 81, 0x00);

$brightness = 5; $flip_mode = 0; $flicker = 0; $ir_mode = 0; $error = "";
$isWDR = 0; $nightVisionAuto = 0;

if(CheckModelName_SNH('WR15'))
{
	$result = requestToCamera(CMD_CMOS_CONFIGURATION, ACTION_GET, TYPE_REQUEST, $temp);
	$sPrivateKey = $_GET['pvKey'];
	if($result[0] == "OK"){
		$cmos = $result[1];
		$brightness = byte2int($cmos, 24);		//Brightness
		$flip_mode = byte2int($cmos, 72);		//FlipMode
		$flicker = byte2int($cmos, 76);			//FlickerMode
		$ir_mode = byte2int($cmos, 96);			//IrMode
	}else{
		$error = $result[1];
	}
} else if(CheckModelName_SNH('WR30')) {
	$cmd = getNewCmd(CMD_CMOS_CONFIGURATION);
	$result = requestToCamera($cmd, ACTION_GET, TYPE_REQUEST, $temp);
	if($result[0] == "OK"){
		$newCmos = $result[1];
		$isWDR = byte2int($newCmos, 57); // WDR
		$brightness = round(byte2int($newCmos, 105) / 10); // Brightness 1~100
		$nightVisionAuto = byte2int($newCmos, 261); // ����Ʈ���� auto / off ����
	}else{
		$error = $result[1];
	}
} else if(CheckModelName_SNH('WR40')) {
	$cmd = getNewCmd(CMD_CMOS_CONFIGURATION);
	$result = requestToCamera($cmd, ACTION_GET, TYPE_REQUEST, $temp);
	if($result[0] == "OK"){
		$newCmos = $result[1];
		if(CheckModelName_SNH('WDR')) {
			$isWDR = byte2int($newCmos, 57); // WDR
		}
		$brightness = round(byte2int($newCmos, 105) / 10); // Brightness 1~100
		$nightVisionAuto = byte2int($newCmos, 261); // ����Ʈ���� auto / off ����
	}else{
		$error = $result[1];
	}
}

if(CheckModelName_SNH('All_WR'))
{
	$result = requestToCamera(CMD_VIDEO_SOURCE, ACTION_GET, TYPE_REQUEST, null);
	if($result[0] == "OK"){
		$vdo_src = $result[1];
		$flip = $vdo_src[80];
		$mirror = $vdo_src[81];
		$flip_mode = (2 * $flip) + (1 * $mirror);
	}else{
		$error = $result[1];
	}
}

$isConn = "TRUE";
/*
$version = @file_get_contents("http://www.samsungsmartcam.com/web/version.stw?action=version");

if ($version == FALSE) {
	$version = "unknown";
	$isConn = "FALSE";
} else {
	if (substr($version, 0 , 1) != '1') {
		$version = "unknown";
		$isConn = "FALSE";
	}
}
*/
?>

<script type="text/javascript" src="/resources/js/video_live.js" ></script>
<script type="text/javascript" src="/resources/js/video_live_webviewer.js" ></script>
<script type="text/javascript" src="/resources/js/sns_youtube.js" ></script>
<script type="text/javascript" src="/resources/js/sns_picasa.js" ></script>
<script type="text/javascript" src="/resources/js/sns_google.js" ></script>
<script type="text/javascript" src="/resources/js/sns_twitter.js" ></script>
<script type="text/javascript" src="/resources/js/sns_email.js" ></script>

<link type="text/css" href="/resources/css/jquery-ui.css" rel="stylesheet" />
<script type="text/javascript" src="/resources/js/jquery-ui.js"></script>
<script type="text/javascript">
	var cameraModel = '<?=CAMERA_MODEL?>';

	<? if(!CheckModelName_SNH('NO_YTB')) { ?>
		var liList = new Array("li_youtube", "li_picasa", "li_google", "li_twitter", "li_email");
		var divList = new Array("ytb", "pica", "gtk", "tt", "em");
		var clsList = new Array("t1 on", "t2 on", "t3 on", "t4 on", "t5 on");
	<? } else { ?>
		var liList = new Array("li_picasa", "li_google", "li_twitter", "li_email");
		var divList = new Array("pica", "gtk", "tt", "em");
		var clsList = new Array("t1 on", "t2 on", "t3 on", "t4 on");
	<? } ?>

	var isWide = false;
	var currentTab = -1;
	<? if($version != "unknown"){?>
	var lastVersion = "<?=$version?>";
	<?} else{?>
	var lastVersion = "1.0.1.62";
	<?}?>

	var cmos = '<?=implode(",", $cmos)?>'.split(",");
	var newCmos = '<?=implode(",", $newCmos)?>'.split(",");
	var vdo_src = '<?=implode(",", $vdo_src)?>'.split(",");
	var flipMode = 0;

	strSucceeded = '<?=$Lang["Update successful"]?>';
	strFailed = '<?=$Lang["Failed to save."]?>';
	strFailURL = '<?=$Lang["Failed to get URL."]?>';
	strInputToken = '<?=$Lang["Enter access token here"]?>';
	strNewMember = '<?=$Lang["The camera is limited to 5 users.  Maximum users reached."]?>';
	strDuplicate = '<?=$Lang["This user ID already exists"]?>';
	strPrivacy = '<?=$Lang["Camera is set to privacy mode"]?>';
	strTwitterSite = '<?=$Lang["To get the access token, please go to twitter website"]?>';
	strRequestURL = '<?=$Lang["Request URL"]?>';
	strTwitterComplete = '<?=$Lang["Twitter authorization is completed!!"]?>';
	strDelete = '<?=$Lang["DEL"]?>';
	strAdd = '<?=$Lang["Add"]?>';
	strMove = '<?=$Lang["Move"]?>';

	profile = '<?=implode(";", $profile)?>'.split(";");
	googleMembers = '<?=implode(";", $google_users)?>'.split(";");
	emailMembers = '<?=implode(";", $email_users)?>'.split(";");

	youtube = '<?=implode(",", $youtube)?>';
	picasa = '<?=implode(",", $picasa)?>';
	google = '<?=implode(",", $google)?>';
	twitter = '<?=implode(",", $twitter)?>';
	email = '<?=implode(",", $email)?>';
	emailArr = '<?=implode(",", $email)?>'.split(",");

	youtubeData = '<?=$youtube_data?>'.split(";");
	picasaData = '<?=$picasa_data?>'.split(";");
	googleData = '<?=$google_data?>'.split(";");
	twitterData = '<?=$twitter_data?>'.split(";");
	var emailData = '<?=$email_data?>'.split(";");

	var isWDR = '<?=$isWDR?>';
	var nightVisionAuto = '<?=$nightVisionAuto?>';


	$(document).ready(function(){
		var res = Webviewer.init({
			width : 640,
			height : 480,
			type : '<?=$isMSIE?>',
			conn : '<?=$isConn?>'
	});

	if(!res){
	//	alert("No Plugin detected! Please setup plugin!");

	var os = navigator.appVersion;

		if(os.indexOf("Mac") != -1)
		{
			html =		"<div id=\"plugin_download\" style=\"position: absolute; margin-left: auto; margin-right: auto; padding: 50px; width: 500px; height: 340px;\">" +
	      				"<div class=\"ps_title\">Plugin Download</div>" +
	      				"<span style=\"padding-top:50px; width: 400px; font-size: 12px;line-height: 12px;\">" +
	      				"<p>No working plug-in was detect on your system." +
					   	"	In order to view live video you need to download and install the plug-in." +
	               	"    Install plug-in by clicking the button below.<p>" +
	               	"</span>" +
	               	"<div style=\"padding-top: 20px;\">" +
	   	            	"<div class=\"cl_btnBox\">" +
		               		"<div class=\"ps_bt\"><button id=\"ps_mac\" class=\"btnTxt bType1\">Download Plugin</button></div>" +
								"</div>" +
							"</div>" +
						"</div>";

			$("#content").html(html);

			$("#ps_mac").click(function(){
				window.location.href = "https://www.samsungsmartcam.com/web/cmm/download.do?req=mac";
			});
		}
		else{
			html =		"<div id=\"plugin_download\" style=\"position: absolute; margin-left: auto; margin-right: auto; padding: 50px; width: 500px; height: 340px;\">" +
							"<div class=\"ps_title\">Plugin Download</div>" +
							"<span style=\"padding-top:50px; width: 400px; font-size: 12px;line-height: 12px;\">" +
							"    <p>No working plug-in was detect on your system." +
	                  "    In order to view live video you need to download and install the plug-in." +
	                  "    Install plug-in by clicking the button below.<p>" +
	                  "</span>" +
	                  "<div style=\"padding-top: 20px;\">" +
	                  	"<div class=\"cl_btnBox\">" +
	                     	"<div class=\"ps_bt\"><button id=\"ps_mac\" class=\"btnTxt bType1\">Download Plugin</button></div>" +
								"</div>" +
							"</div>" +
						"</div>";

			$("#content").html(html);

			$("#ps_mac").click(function(){
				window.location.href = "https://www.samsungsmartcam.com/web/cmm/download.do?req=win";
			});
		}
	}
	else{
		res = Webviewer.play({
			ip : "<?=$_SERVER["SERVER_ADDR"]?>",
			privateKey : "<?=$_SESSION["PRIVATE_KEY"]?>",
			camId : "admin"
		});

		if(res != "1"){
			alert(strFailURL);
			moveToPage("pages/camera_login.php");
		}

		createProfile();
		getVideoLive();
		getYoutubeData();
		getPicasaData();
		getGoogleData();
		getTwitterData();
		getEmailData();
	}
});

function cameraStateCheck( res )
{
	/*
		PLAYER_INITIALIZED		= 0
		PLAYER_PLAYING 			= 1
		PLAYER_PLAYING_RELAY 	= 2
		PLAYER_PLAYING_ERROR 	= 3
		PLAYER_RECORDVIDEO 		= 4
		PLAYER_PAUSED 			= 5
		PLAYER_STOPPING 		= 6
		PLAYER_STOPPED 			= 7
		PLAYER_RELAY_EXPIRED 	= 8
		PLAYER_UNKNOWN 			= 9
	*/
	if (typeof(console) != "undefined") {
		console.log("State Response : " + res);
	}
	/*
	switch(res){
		case 0:
			break;
		case 1:
			returnCameraMessage("play");
			break;
		case 2:
			returnCameraMessage("xmpp");
			break;
		case 3:
			returnCameraMessage("busy");
			break;
		case 4:
			returnCameraMessage("privacy");
			break;
		case 5:
		case 6:
		case 7:
			break;
		case 8:
			returnCameraMessage("close");
			break;
		default:
			alert("Unkwon Error");
	}*/
}

function changeTab(idx){
	/*
	if(!isWide){
		document.getElementById(divList[parseInt(idx)]).style.display = "block";
	}*/
}
function selectTab(idx){
	<? if(CheckModelName_SNH('NO_YTB')) { ?>
		idx--;
	<? } ?>

	for(var i=0; i<divList.length; i++){
		document.getElementById(liList[i]).className = "t" + (i+1);
		document.getElementById(divList[i]).style.display = "none";
	}

	if(currentTab == parseInt(idx)){
		isWide = !isWide;
	}else{
		isWide = true;
	}
	if(!isWide){
		document.getElementById(divList[parseInt(idx)]).style.display = "none";
	}else{
		document.getElementById(divList[parseInt(idx)]).style.display = "block";
		document.getElementById(liList[parseInt(idx)]).className = clsList[parseInt(idx)];
	}
	currentTab = parseInt(idx);
}

function releaseTab(idx){
	/*
	if(!isWide){
		document.getElementById(divList[parseInt(idx)]).style.display = "none";
	}*/
}

function getVideoLive(){
	flipMode = '<?=$flip_mode?>';
	changeFlipIcon();

	$("#slider_BRIGHTNESS").slider({
		range: "min",
		value: <?=$brightness?>,
		min: 1,
		max: 10,
		change: function(event, ui){
			$("#BRIGHTNESS").val(ui.value);
			//2013.07.15 6410-Brightness
//		   	if(cameraModel != "SEC-6410"){
			<? if(CheckModelName_SNH('WR15')) { ?>
		   		sendLiveMessage();
			<? }else {?>
				sendNewCmosMessage();
			<? } ?>
		}
	});
	$("#BRIGHTNESS").val('<?=$brightness?>');
	$("#BRIGHTNESS").attr("disabled", true);
}

function changeFlipIcon(){
	for(var i=0; i<4; i++)
	{
		document.getElementById("camera_flip" + i).setAttribute("src", "../resources/images/btn_flip_off_" + (i+1) + ".gif");
		if(i == flipMode)
		{
			document.getElementById("camera_flip" + i).setAttribute("src", "../resources/images/btn_flip_on_" + (i+1) + ".gif");
		}
	}
}

function setFlipMode(idx)
{
		document.getElementById("camera_flip0").setAttribute("src", "../resources/images/btn_flip_off_1.gif");
		document.getElementById("camera_flip1").setAttribute("src", "../resources/images/btn_flip_off_2.gif");
		document.getElementById("camera_flip2").setAttribute("src", "../resources/images/btn_flip_off_3.gif");
		document.getElementById("camera_flip3").setAttribute("src", "../resources/images/btn_flip_off_4.gif");

		flipMode = idx;
		document.getElementById("camera_flip" + idx).setAttribute("src", "../resources/images/btn_flip_on_" + (parseInt(idx)+1) + ".gif");

   	//2013.07.15 6410-flipMode
//   	if(cameraModel != "SEC-6410"){
		<? if(CheckModelName_SNH('WR15')) { ?>
   		sendLiveMessage();
		<? } else { ?>
			boolflipMode = idx / 2;

			if(idx % 2 == 0)
				mirrorMode = 0;
			else
				mirrorMode = 1;

			vdo_src[80] = parseInt(boolflipMode);
			vdo_src[81] = parseInt(mirrorMode);

			var sendData = "IPCV0.7;FLIP;" + vdo_src.join(",");
		   $.post("/classes/class_setup_video.php", {data: sendData}, returnLiveMessage, "text");
		<? } ?>
}

function sendLiveMessage()
{
	cmos[72] = parseInt(flipMode);
	cmos[24] = $("#BRIGHTNESS").val();

	var sendData = "LIVE;" + cmos.join(",");
  	$.post("/classes/class_setup_video.php", {data: sendData}, returnLiveMessage, "text");
}

function sendNewCmosMessage()
{
	newCmos[57] =  parseInt(isWDR);
	newCmos[105] =  parseInt( $("#BRIGHTNESS").val() * 10);
	newCmos[261] =  parseInt(parseInt(nightVisionAuto));

	var sendData = "IPCV0.7;CMOS;" + newCmos.join(",");
  	$.post("/classes/class_setup_video.php", {data: sendData}, returnLiveMessage, "text");
}

function returnLiveMessage(resp)
{
	var recvData = resp.split(";");
	if(recvData[0] != "OK")
	{
		console.log(recvData);
		alert('<?=$Lang["Failed to save."]?>');
	}
	else
	{
		changeFlipIcon();
	}
}

function is6410()
{
	return 'SNH-E6110BN'=='<?=CAMERA_MODEL?>';
}

</script>
</head>

<? include $_SERVER["DOCUMENT_ROOT"] . "/common/header.php"; ?>

	<!-- s:height100% -->
	<div id="hgt100">
		<!-- s:contBox_cl -->
		<div id="contBox_cl" class="floatClear">

			<? include $_SERVER["DOCUMENT_ROOT"] . "/common/side_menu.php"; ?>

				<!-- s:   -->
				<div id="contDiv2">
					<div id="player_area" style="display:block;">
						<div id="content">
				<? if($isMSIE == "0") { ?>
						<embed width="640" height="480" type="application/smartcam-webviewer-plugin" id="plugin" />
				<? } else { ?>
						<object id="plugin" width="640" height="480"
						classid="CLSID:1F66540A-4FBA-4FCA-81A7-3EEA6FA3D358">
					</object>
				<? } ?>
						</div>
					</div>
					<div class="vd_slBox" id="live_contents">
					<!-- insert live contents -->
						<div class="vd_profile">
							<div id="profile_select" style="padding:1px"></div>
						</div>
						<div class="vd_menu">
							<table>
								<tbody>
								<tr>
									<td style="width:10px"></td>
									<td style="width:30px"><?=$Lang["Flip"]?></td>
									<td style="padding:3px; width:25px">
										<img id='camera_flip0' src='../resources/images/btn_flip_off_1.gif' width='25' height='25' onclick="setFlipMode('0');" title='Flip Off'/>
									</td>
									<td style="padding:3px; width:25px">
										<img id='camera_flip1' src='../resources/images/btn_flip_off_2.gif' width='25' height='25' onclick="setFlipMode('1');" title='Vertical Flip'/>
									</td>
									<td style="padding:3px; width:25px">
										<img id='camera_flip2' src='../resources/images/btn_flip_off_3.gif' width='25' height='25' onclick="setFlipMode('2');" title='Horizontal Flip'/>
									</td>
									<td style="padding:3px; width:25px">
										<img id='camera_flip3' src='../resources/images/btn_flip_off_4.gif' width='25' height='25' onclick="setFlipMode('3');" title='Vertical & Horizontal Flip'/>
									</td>
									<td style="width:10px"></td>
								</tr>
								</tbody>
							</table>
						</div>

						<div class="vd_control">
							<table>
								<tbody>
								<tr>
									<td style="width:75px"><?=$Lang["Brightness"]?></td>
									<td style="width:148px"><div id='slider_BRIGHTNESS' class='slider_small' style='width:140px'></div></td>
									<td style="width:30px"><input type='text' id='BRIGHTNESS' style='width:20px; text-align:center; margin:auto;'/></td>
								</tr>
								</tbody>
							</table>
						</div>
					</div>

				</div>
			 </div>
			<!-- e:contBox_cl -->
		</div>
		<!-- e:height100% -->
		<? include $_SERVER["DOCUMENT_ROOT"] . "/common/footer.php"; ?>
	</div>
</body>
</html>
