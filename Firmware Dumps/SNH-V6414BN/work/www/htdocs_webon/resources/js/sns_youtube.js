function getYoutubeData(){
	if(youtubeData[1] == "1"){
		document.getElementById("img_0").src = "/resources/images/sns_on.png";
	}
	$("input:radio[name=youtube_status]").filter("input[value=" + youtubeData[0] + "]").attr("checked", "checked");
	$("#youtube_id").val(youtubeData[2]);
	$("#youtube_pw").val(youtubeData[3]);
	$("input:radio[name=youtube_access]").filter("input[value=" + youtubeData[4] + "]").attr("checked", "checked");
}
		
function saveYoutubeData(){
	var sendData = youtube + ";";
	$("input:radio[name=youtube_status]:checked").each(function(){
		sendData += this.value + ";";
   	});	   		
	sendData += $("#youtube_id").val() + ";";
	sendData += $("#youtube_pw").val() + ";";
	$("input:radio[name=youtube_access]:checked").each(function(){
		sendData += this.value + ";";
   	});
	sendData += "2";
	
	$.post("/classes/class_sns_youtube.php", {data: sendData}, returnYoutubeMessage, "text");	
}

function returnYoutubeMessage(resp){
	var recvData = resp.split(";");	   		
	if(recvData[0] == "OK"){
		alert(strSucceeded);
	}else{
		alert(strFailed + "-" + recvData[1]);
	}
}