var OFF_EMAIL			= 3660;
var OFF_EMAIL_LIST		= 128;
var OFF_EMAIL_SERVER	= 1408;
var OFF_NETWORK_CHANGED	= 11709;

var OFF_EMAIL_V2_SENDER		= 6176;
var OFF_EMAIL_V2_RECIPIENT	= 6304;
var OFF_EMAIL_V2_SERVER		= 6432;
var OFF_EMAIL_V2_PORT		= 6560;
var OFF_EMAIL_V2_AUTH		= 6564;
var OFF_EMAIL_V2_ID			= 6565;
var OFF_EMAIL_V2_PW			= 6629;
var OFF_EMAIL_V2_SUBJECT	= 6693;
var OFF_EMAIL_V2_BODY		= 6949;
var OFF_EMAIL_V2_SSL		= 7973;
var OFF_EMAIL_V2_SSL_PORT	= 7974;

var eMailMemList = new Array();
var useSSL = '0';
var port = new Array("", "");

function getEmailData(){
	if(is6410()){
		getEmailData6410();
		return;
	}
	useSSL = emailData[6];
	port[0] = emailData[2];
	port[1] = emailData[7];
	
	$("#server").val(emailData[1]);
	$("input:radio[name=ssl]").filter("input[value=" + parseInt(useSSL) + "]").attr("checked", "checked");
	$("#port").val(port[parseInt(useSSL)]);								
	$("#auth").val(emailData[3]);
	$("#user_id").val(emailData[4]);
	$("#password").val(emailData[5]);	
	$("#sender").val(emailData[0]);			
	for(var i=0, j=0; i<emailMembers.length; i++){
		if(emailMembers[i] != ""){
			eMailMemList[j++] = emailMembers[i];
		}
	}
		
	createEmailMemberList();
}

function getEmailData6410(){
	eMailMemList = new Array();
	maxEmail = byte2int(emailMembers, 0);

	var cnt = 0;	
	var emailArr_user = byte2str(emailArr, OFF_EMAIL_V2_RECIPIENT, 128);

	if(emailArr_user != '' && emailArr_user != null){
		eMailMemList[cnt++] = emailArr_user;
	}
	
	for(var i=0, j=4; i<maxEmail; i++){
		var user = byte2str(emailMembers, j, 128);
		if(user != null && user != ""){
			eMailMemList[cnt++] = user;
		}
		j+=128;
	}
	
	var server = byte2str(emailArr, OFF_EMAIL_V2_SERVER, 128);
	var useSSL = emailArr[OFF_EMAIL_V2_SSL];
	var SSLPort = byte2int(emailArr, OFF_EMAIL_V2_SSL_PORT);
	var plainPort = byte2int(emailArr, OFF_EMAIL_V2_PORT);
	var authYn = emailArr[OFF_EMAIL_V2_AUTH];
	var id =  byte2str(emailArr, OFF_EMAIL_V2_ID, 64);
	var pw =  byte2str(emailArr, OFF_EMAIL_V2_PW, 64);
	
	var sender = byte2str(emailArr, OFF_EMAIL_V2_SENDER, 128);
	port[0] = plainPort, port[1] = SSLPort;
	
	$("#server").val(server);
	$("input:radio[name=ssl]").filter("input[value=" + parseInt(useSSL) + "]").attr("checked", "checked");
	$("#port").val(port[parseInt(useSSL)]);								
	$("#auth").val(authYn);
	$("#user_id").val(id);
	$("#password").val(pw);	
	$("#sender").val(sender);

	createEmailMemberList();
}


function createEmailMemberList(){
	var html = "<p><input type='text' id='add_member' maxlength='128'/>";
	html += "<button type='button' class='btnTxt bType2b' onclick='addEmailMember();'>" + strAdd + "</button></p>";			
	html += "<h2>List</h2>";
	html += "<ul class='emList'>";
	if(eMailMemList != null && eMailMemList.length > 0){
		for(var i=0; i<eMailMemList.length; i++){
			if(eMailMemList[i] != ''){
				html += "<li>" + (i+1) + "." + eMailMemList[i];
				html += "<button type='button' class='btnTxt bType2a' onclick='deleteEmailMember(" + i + ");'>" + strDelete + "</button></li>";
			}
		}
	}
	html += "</ul>";
	//document.getElementById("email_member_list").innerHTML = html;
}

function addEmailMember(){
	var newMember = $("#add_member").val();
	if(!checkEmailField(document.getElementById("add_member"), false)){
		return;
	}
	
	if(eMailMemList.length >= 5){
		alert(strNewMember);
		$("#add_member").val("");
		return;
	}
	
	for(var i=0; i<eMailMemList.length; i++){
		if(eMailMemList[i] == newMember){
			alert(strDuplicate);
			$("#add_member").val("");
			$("#add_member").focus();
			return;
		}
	}
	eMailMemList[eMailMemList.length] = newMember;				
	$("#add_member").val("");
	
	createEmailMemberList();			
}

function deleteEmailMember(idx){
	if(eMailMemList.length <= 1){
		eMailMemList = new Array();
	}else{
		var mem1 = eMailMemList.slice(0, idx);
		var mem2 = eMailMemList.slice((idx+1));
		var member = mem1.concat(mem2);			
		eMailMemList = member;
	}
	
	createEmailMemberList();	
}

function changeSSLMode(idx){
	useSSL = idx;
	$("#port").val(port[useSSL]);
}

function saveEmailData(){
	if(is6410()){
		saveEmailData6410();
		return;
	}
	
	var sendData = "IPCV0.6;" + email + ";";
	sendData += $("#server").val() + ";";
	if(useSSL == '0'){
		sendData += $("#port").val() + ";";
	}else{
		sendData += port[0] + ";";
	}
	sendData += $("#auth > option:selected").val() + ";";
	sendData += $("#user_id").val() + ";";
	sendData += $("#password").val() + ";";
	sendData += useSSL + ";";
	if(useSSL == '1'){
		sendData += $("#port").val() + ";";
	}else{
		sendData += port[1] + ";";
	}
	if(eMailMemList.length > 0){				
		sendData += eMailMemList.join(",");
	}else{
		sendData += " ";
	}			
	if($("#sender").val() == ""){
		sendData += "; ";
	}else{
		sendData += ";" + $("#sender").val();
	}			
	
	$.post("/classes/class_sns_email.php", {data: sendData}, returnEmailMessage, "text");
}

function saveEmailData6410(){	
	useSSL = $("input:radio[name=ssl]:checked").val();
	str2byte(emailArr, OFF_EMAIL_V2_SERVER, 128,  $("#server").val());	
	emailArr[OFF_EMAIL_V2_AUTH] = $("#auth").val(); 
	emailArr[OFF_EMAIL_V2_SSL] = useSSL;

	if(useSSL=="1"){
		int2byte(emailArr, OFF_EMAIL_V2_PORT, port[0]);
		int2byte(emailArr, OFF_EMAIL_V2_SSL_PORT, $("#port").val());
	}else{
		int2byte(emailArr, OFF_EMAIL_V2_PORT, $("#port").val());
		int2byte(emailArr, OFF_EMAIL_V2_SSL_PORT, port[1]);
	}
	str2byte(emailArr, OFF_EMAIL_V2_SENDER, 128, $("#sender").val());
	str2byte(emailArr, OFF_EMAIL_V2_ID, 64, $("#user_id").val());
	str2byte(emailArr, OFF_EMAIL_V2_PW, 64, $("#password").val());
	str2byte(emailArr, OFF_EMAIL_V2_SUBJECT, 256, "Event Alarm");
	str2byte(emailArr, OFF_EMAIL_V2_BODY, 1024, "Event Alarm Detection");
	
	if(eMailMemList[0] =="" || eMailMemList[0] ==null){
		eMailMemList[0] = $("#user_id").val();
	}
	str2byte(emailArr, OFF_EMAIL_V2_RECIPIENT, 128, eMailMemList[0]);
	createEmailMemberList();
	var sendData = "IPCV0.7;" + emailArr.join(",") + ";" + eMailMemList.join(",");
	$.post("/classes/class_sns_email.php", {data: sendData}, returnEmailMessage, "text");
}

function returnEmailMessage(resp){
	var recvData = resp.split(";");
	if(recvData[0] == "OK" || recvData[1] == undefined){				
		alert(strSucceeded);
	}else{
		alert(strFailed + "-" + recvData[1]);
	}		
}