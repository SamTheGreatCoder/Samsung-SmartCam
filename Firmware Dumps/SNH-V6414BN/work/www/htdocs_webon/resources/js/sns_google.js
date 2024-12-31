var googleMemList = new Array();

function getGoogleData(){
	if(googleData[1] == "1"){
		document.getElementById("img_2").src = "/resources/images/sns_on.png";
	}
	$("input:radio[name=google_status]").filter("input[value=" + googleData[0] + "]").attr("checked", "checked");

	for(var i=0, j=0; i<googleMembers.length; i++){
		if(googleMembers[i] != ""){
			googleMemList[j++] = googleMembers[i];
		}
	}
	//createGoogleMemberList();	
}	

function createGoogleMemberList(){			
	var html = "<h2>User(ID) List</h2>";	
	html += "<ul class='emList'>";
	if(googleMemList != null && googleMemList.length > 0){
		for(var i=0; i<googleMemList.length; i++){
			html += "<li><label for=''>" + (i+1) + "." + googleMemList[i] + "</label></li>";
		}
	}
	html += "</ul>";
	//document.getElementById("google_member_list").innerHTML = html;
}

function saveGoogleData(){
	var sendData = google + ";";
	$("input:radio[name=google_status]:checked").each(function(){
		sendData += this.value + "; ";
   	});	
	/*
	if(googleMemList.length > 0){
		sendData += googleMemList.join(";");
	}else{	   			
		sendData += " ";
	}*/
	
	$.post("/classes/class_sns_google.php", {data: sendData}, returnGoogleMessage, "text");
}

function returnGoogleMessage(resp){
	var recvData = resp.split(";");
	if(recvData[0] == "OK"){
		alert(strSucceeded);
	}else{
		alert(strFailed + "-" + recvData[1]);
	}
}