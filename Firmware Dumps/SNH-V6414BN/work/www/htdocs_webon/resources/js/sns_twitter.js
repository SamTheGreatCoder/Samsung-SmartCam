var count = 0;
var twitterSite = "";

function getTwitterData(){
	var html = "";
	
	$("input:radio[name=twitter_status]").filter("input[value=" + twitterData[0] + "]").attr("checked", "checked");
	if(twitterData[1] == '1'){
		document.getElementById("img_3").src = "/resources/images/sns_on.png";
		html = strTwitterComplete;
	}else{
		html ="<button type='button' class='btnTxt bType2a' onclick='requestURL();'>" + strRequestURL + "</button>";
	}	
	//document.getElementById('auth_status').innerHTML = html;
}

function requestURL(){
	$.post("/classes/class_sns_twitter.php", {data: "GET;"}, returnGetMessage, "text");
}	
function returnGetMessage(resp){
	var recvData = resp.split(";");
	if(recvData[0] == "OK"){
		if(recvData[1] == ""){
			count++;
			if(count < 3){
				sleep(1000);
				requestURL();
			}else{
				alert(strFailURL);
				count = 0;
			}
		}else{
			twitterSite = recvData[1];
			
			var html = strTwitterSite + "&nbsp;&nbsp;";
			html += "<button type='button' class='btnTxt bType2' onclick='goTwitterSite();'>" + strMove + "</button>";
			
			document.getElementById("auth_url").innerHTML = html;	
			document.getElementById("auth_status").style.display = "none";
			document.getElementById("auth_url").style.display = "block";
			document.getElementById("token_input").style.display = "block";
		}
	}
}

function goTwitterSite(){
	window.open(twitterSite, '', '');
}

function sendToken(){
	if($("#access_token").val() == ""){
		alert(strInputToken);
		$("#access_token").focus();
	}else{
		var sendData = "SET;" + $("#access_token").val();
		$.post("/classes/class_sns_twitter.php", {data: sendData}, returnTwitterMessage, "text");
	}
}

function saveTwitterData(){	   		 		
	var sendData = "LIVE;" + twitter + ";";
	$("input:radio[name=twitter_status]:checked").each(function(){
		sendData += this.value;
	});	   		
	$.post("/classes/class_sns_twitter.php", {data: sendData}, returnTwitterMessage, "text");
}

function returnTwitterMessage(resp){
	var recvData = resp.split(";");	
	if(recvData[0] == "OK"){
		alert(strSucceeded);
	}else{
		alert(strFailed + "-" + recvData[1]);
		$("#access_token").val("");
	}
}