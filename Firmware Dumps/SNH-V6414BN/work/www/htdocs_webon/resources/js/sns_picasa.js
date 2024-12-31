function getPicasaData(){
	if(picasaData[1] == "1"){
		document.getElementById("img_1").src = "/resources/images/sns_on.png";
	}
	$("input:radio[name=picasa_status]").filter("input[value=" + picasaData[0] + "]").attr("checked", "checked");
	$("#picasa_id").val(picasaData[2]);
	$("#picasa_pw").val(picasaData[3]);
	$("input:radio[name=picasa_access]").filter("input[value=" + picasaData[4] + "]").attr("checked", "checked");
}

function savePicasaData(){
	var sendData = picasa + ";";
	$("input:radio[name=picasa_status]:checked").each(function(){
		sendData += this.value + ";";
   	});	  
	sendData += $("#picasa_id").val() + ";";
	sendData += $("#picasa_pw").val() + ";";
	$("input:radio[name=picasa_access]:checked").each(function(){
		sendData += this.value + ";";
   	});
	
	$.post("/classes/class_sns_picasa.php", {data: sendData}, returnPicasaMessage, "text");
}

function returnPicasaMessage(resp){
	var recvData = resp.split(";");			
	if(recvData[0] == "OK"){
		alert(strSucceeded);
	}else{
		alert(strFailed + "-" + recvData[1]);
	}
}