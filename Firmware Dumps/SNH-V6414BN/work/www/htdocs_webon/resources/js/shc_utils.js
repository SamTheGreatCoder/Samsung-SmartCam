var ptnNumOnly = /(^[0-9]+$)/;
var ptnNumDot = /(^[0-9.]+$)/;
var ptnAlphaNum = /(^[a-zA-Z0-9]+$)/;
var ptnAlphaNumDot = /(^[a-zA-Z0-9.]+$)/;
var ptnEmail = /^((\w|[\-\.])+)@((\w|[\-\.])+)\.([A-Za-z]+)$/;
var ptnIPAddress = /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/;

var keyFunctionList = new Array(8, 9, 13, 32, 46);	//backspace,tab,return,space,delete
var keyNumericList = new Array(48, 49, 50, 51, 52, 53, 54, 55, 56, 57);
var keyAlphaList = new Array(
	65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 
	78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90,								
	1065, 1066, 1067, 1068, 1069, 1070, 1071, 1072, 1073, 1074, 1075, 1076, 1077, 
	1078, 1079, 1080, 1081, 1082, 1083, 1084, 1085, 1086, 1087, 1088, 1089, 1090
);
var keySpecialList1 = new Array( //For Camera Name
	192, 1192, 1048, 1049, 1050, 1051, 1052, 1053, 1054, 1055, 1056, 1057, 	//`~!@#$%^&*()	
	189, 1189, 219, 221, 1219, 1221, 1220, 186, 222, 188, 190, 191, 1191	//-_[]{}|;',./?
);
var keySpecialList2 = new Array( //For PrivateKey and Password
	192, 1192, 1048, 1049, 1050, 1051, 1052, 1053, 1054, 1055, 1056, 1057, 	//`~!@#$%^&*()	
	189, 1189, 219, 221, 1219, 1221, 1220, 186, 222, 190, 191, 1191			//-_[]{}|;'./?
);
var keyNumLock = new Array(96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 144);	//0~9, NumLock

function keyCameraName(evt){
	var code = (evt.shiftKey == 1)? (evt.keyCode + 1000) : evt.keyCode;	
	if(evt.ctrlKey && code == 86) return false; //ctrl + v
	
	if(!checkAlphaNumeric(code)){
		for(var i=0; i<keySpecialList1.length; i++){
			if(code == keySpecialList1[i]){
				return true;
			}
		}
		return false;
	}
	return true;
}
function keyUserId(evt){
	var code = (evt.shiftKey == 1)? (evt.keyCode + 1000) : evt.keyCode;	
	if(evt.ctrlKey && code == 86) return false; //ctrl + v
	
	if(!checkAlphaNumeric(code)){
		if(code == 190){
			return true;
		}
		return false;
	}		
	return true;
}
function keyPassword(evt){
	var code = (evt.shiftKey == 1)? (evt.keyCode + 1000) : evt.keyCode;	
	if(evt.ctrlKey && code == 86) return false; //ctrl + v
	
	if(!checkAlphaNumeric(code)){
		for(var i=0; i<keySpecialList2.length; i++){
			if(code == keySpecialList2[i]){
				return true;
			}
		}
		return false;
	}
	return true;
}
function keySerialNo(evt){
	var code = (evt.shiftKey == 1)? (evt.keyCode + 1000) : evt.keyCode;	
	//if(evt.ctrlKey && code == 86) return false; //ctrl + v
	
	return checkAlphaNumeric(code);
}

function checkAlphaNumeric(code){
	for(var i=0; i<keyFunctionList.length; i++){
		if(code == keyFunctionList[i]){
			return true;
		}
	}
	for(var i=0; i<keyNumericList.length; i++){
		if(code == keyNumericList[i]){
			return true;
		}
	}
	for(var i=0; i<keyAlphaList.length; i++){
		if(code == keyAlphaList[i]){
			return true;
		}
	}
	for(var i=0; i<keyNumLock.length; i++){
		if(code == keyNumLock[i]){
			return true;
		}
	}
	return false;
}
//-------------------------------------------------------------------------------------------------------------------

function checkNumPattern(obj){
	var value = obj.value;
	if(value != ""){
		if(!ptnNumOnly.test(value)){
			obj.value = value.substr(0, (value.length-1));
		}
	}
}
function checkNumDotPattern(obj){
	var value = obj.value;
	if(value != ""){
		if(!ptnNumDot.test(value)){
			obj.value = value.substr(0, (value.length-1));
		}
	}
}
function checkAlphaNumPattern(obj){
	var value = obj.value;
	if(value != ""){
		if(!ptnAlphaNum.test(value)){
			obj.value = value.substr(0, (value.length-1));
		}
	}
}
function checkAlphaNumDotPattern(obj){
	var value = obj.value;
	if(value != ""){
		if(!ptnAlphaNumDot.test(value)){
			obj.value = value.substr(0, (value.length-1));
		}
	}
}

function checkInputValue(obj, blank, min, max, title){
	var value = obj.value;	
	if(!blank && value == ""){
		alert("Input the " + title);
		obj.focus();
		return false;
	}
	if(min > 0 && value.length < min){
		alert("You must input of " + min + " to " + max + " characters in length containing letters A-Z or numbers 0-9.");
		obj.value = "";
		obj.focus();
		return false;
	}
	return true;
}

function checkIPAddressField(obj, blank){
	var value = obj.value;	
	if(!blank && value == ""){
		alert("Input the address.");
		obj.focus();
		return false;
	}
	
	var result = value.match(ptnIPAddress);				
	if(result != null){
		var arrAddr = addr.split(".");
		for(var i=0; i<arrAddr.length; i++){
			if(parseInt(arrAddr[i]) > 255){
				break;
			}
			if(i == (arrAddr.length - 1)){
				return true;
			}
		}
	}
	alert("The address is wrong. Input the address again.");
	obj.value = "";
	obj.focus();
	return false;
}

function checkEmailField(obj, blank){
	var value = obj.value;	
	if(!blank && value == ""){
		alert("Input the user e-mail.");
		obj.focus();
		return false;
	}
	if(!ptnEmail.test(value)){		
		obj.value = "";
		obj.focus();
		return false;
	}
	return true;
}

function sleep(milliseconds){
	var start = new Date().getTime();
	for(var i=0; i<1e7; i++){
		if((new Date().getTime() - start) > milliseconds){
			break;
		}
	}
}