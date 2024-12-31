var strSucceeded;
var strFailed;
var strFailURL;
var strInputToken;
var strNewMember;
var strDuplicate;
var strPrivacy;
var strTwitterSite;
var strRequestURL;
var strTwitterComplete;
var strDelete;
var strAdd;
var strMove;

var soundMode = true;
var irTimer = false;
var navEnabled = false;
var isPrivacy = false;
var isBusy = false;
var isPlaying = false;

var returnMsg = new Array();

var youtube;
var picasa;
var google;
var twitter;
var email;
var emailArr;

var youtubeData;
var picasaData;
var googleData;
var twitterData;
var emailData;

var profile;
var googleMembers;
var emailMembers;

var isAudio = true;

function createProfile(){
	var html = "<select id='sel_profile' onchange='changeProfile(this);'>";
	profile[1] = "Low Network";
	profile[2] = "Mid Network";
	profile[3] = "High Network";
	if(profile != null && profile.length > 0){
		for(var i=1; i<=3; i++){
			if(profile[i] != null && profile[i] != ""){
				if(i == 2){
					html += "<option value='profile" + (i+2) + "' selected>" + profile[i] + "</option>";
				}else{
					html += "<option value='profile" + (i+2) + "'>" + profile[i] + "</option>";
				}
			}
		}
	}
	html += "</select>&nbsp;&nbsp;";
	html += "<img src='/resources/images/btn_image_capture.gif' width='43' height='23' title='Capture' onclick='takePicture();'/> &nbsp;&nbsp;";
	html += "<img src='/resources/images/btn_speaker_on.gif' id='spk_bt' width='43' height='23' title='Audio' onclick='soundControl(this);'/>&nbsp;&nbsp;&nbsp;";

	document.getElementById('profile_select').innerHTML = html;

	if(getProfile()!=''){
		$("#sel_profile").val(getProfile());
		changeProfile(document.getElementById("sel_profile"));
	}
}

function changeProfile(obj){
	soundMode = true;
	$("#spk_bt").attr("src", "/resources/images/btn_speaker_on.gif");
	Webviewer.profileChange(obj.value);
	setProfile(obj.value);
	sleep(500);
}

function takePicture(){
	Webviewer.capture("");
}

function soundControl(obj) {
	if(isAudio){
		soundMode = !soundMode;
		if(soundMode){
			obj.src = "/resources/images/btn_speaker_on.gif";
			Webviewer.soundOn();
		}else{
			obj.src = "/resources/images/btn_speaker_off.gif";
			Webviewer.soundOff();
		}
	}
}

function navigationEnabled(obj) {
	navEnabled = !navEnabled;
	if(navEnabled){
		obj.src = "/resources/images/btn_navigation_on.png";
	}else{
		obj.src = "/resources/images/btn_navigation_off.png";
	}
	document.player.setNavigationImageEnabled(navEnabled);
}

function fullscreenEnabled(){
	document.player.setFullscreenEnabled();
}

function setParameter(){
	if(!irTimer){
		Webviewer.irFlashOn();
		irTimer = true;
		$("#ir_led").attr("src", "/resources/images/IR_LED_btn_dim.png");
		setTimeout("resetIrTimer();", (120 * 1000));
	}
}

function resetIrTimer(){
	irTimer = false;
	$("#ir_led").attr("src", "/resources/images/IR_LED_btn.png");
}

function returnAppletMessage(msg){
	if(msg == "play"){
		isPlaying = true;
	}else if(msg == "event"){
	}else if(msg == "privacy"){
		alert(strPrivacy);
		moveToPage("pages/camera_login.php");
	}else if(msg == "audio"){
		isAudio = false;
	}else if(msg == "close"){
		moveToPage("pages/camera_login.php");
	}else{
		alert(msg);
	}
}

function setProfile(cValue){
    document.cookie = 'viewer_profile=' + escape(cValue) + '; path=/ ';
}

function getProfile() {
    var start = document.cookie.indexOf('viewer_profile=');
    var cValue = '';
    if(start != -1){
         start += 'viewer_profile='.length;
         var end = document.cookie.indexOf(';', start);
         if(end == -1)end = document.cookie.length;
         cValue = document.cookie.substring(start, end);
    }
    return unescape(cValue);
}

