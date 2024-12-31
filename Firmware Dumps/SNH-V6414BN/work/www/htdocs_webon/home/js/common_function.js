var gAlertMsg = "";
var gPageState = "REFRESH";
 //Bring back the browser object 

jQuery.browser={};(function(){jQuery.browser.msie=false;
jQuery.browser.version=0;if(navigator.userAgent.match(/MSIE ([0-9]+)\./)){
jQuery.browser.msie=true;jQuery.browser.version=RegExp.$1;}})();

//jQuery.browser = {}; 
//Rest all is self explanatory. 
jQuery.browser.mozilla = /mozilla/.test(navigator.userAgent.toLowerCase())&& !/webkit/.test(navigator.userAgent.toLowerCase()); 
jQuery.browser.webkit = /webkit/.test(navigator.userAgent.toLowerCase()); 
jQuery.browser.opera = /opera/.test(navigator.userAgent.toLowerCase()); 
//jQuery.browser.msie = /msie/.test(navigator.userAgent.toLowerCase()); 
//jQuery.browser.version = /version/.test(navigator.userAgent.toLowerCase()); 

$(document).ready(function(){	
	$("input,textarea").bind("paste", function(e){
		return false;
	});

	if(BrowserDetect.browser == "Explorer" && getIEVersion() <= 7) {
		$.fn.extend({
			optionDisable:function()
			{
				if ($(this).prop('tagName') == null) return;
				var ths = $(this);
				if(ths.prop('tagName').toLowerCase() == 'option')
				{
					ths.before($('<optgroup>&nbsp;</optgroup>').css({color:'#ccc',height:ths.height()}).attr({id:ths.attr('value'),label:ths.text()})).remove();
				}
				return ths;
			},
			optionEnable:function()
			{
				if ($(this).prop('tagName') == null) return;
				var ths = $(this);
				var tag = ths.prop('tagName').toLowerCase();
				if(tag == 'option')
				{
					ths.removeAttr('disabled');
				}
				else if(tag == 'optgroup')
				{
					ths.before($('<option />').attr({value:ths.attr('id')}).text(ths.attr('label'))).remove();
				}
				return ths;
			}
		}); 
	}
});

function RequestGetConfig(account)
{
	if( window.XMLHttpRequest ) {
		var req = new XMLHttpRequest();
	} else {
		var req = new ActiveXObject("Microsoft.XMLHTTP");
	}

	var reqstr = './account_temp.cgi?msubmenu=account&id='+account;

	req.open('GET', reqstr, false );
	req.send(null);
	if( req ) {
		if( req.readyState == 4 && req.status == 200 )
			return req.responseText;
//		else
//			alert(request+' not found!');
	}
	return '';
}

function RequestAjaxMsg(msg, alertMsg, reqUrl, command, asyncVal, funcName)
{
	if (typeof command == "undefined")	command = "REFRESH";
	if (typeof asyncVal == "undefined")	asyncVal = false;
	if (typeof funcName == "undefined")	funcName = OnSuccessApply;
	gPageState = command;
	gAlertMsg = alertMsg;
	if (BrowserDetect.browser == "Explorer" || (BrowserDetect.browser == 'Safari' && reqUrl.search('.local') != -1)) {
		reqUrl = "../.."+reqUrl.substr(reqUrl.indexOf("/cgi"));
	}

	$.ajax({
		type: "POST",
		async: asyncVal,
		cache: false,
		url: reqUrl,
		dataType: "text",
		data: encodeURIComponent(msg),
		success: funcName
	});
}

function ChangeApplyState(command)
{
	// Just for Open Platform 1.0 Web page compatibility
	// Empty function
}

function OnSuccessApply(req)
{
	if (gAlertMsg != "")	alert(gAlertMsg);
	switch(gPageState)
	{	
		case 'NO_REFRESH':		break;
		case 'PAGE_CLOSE':		window.open('about:blank', '_self').close();	break;
		case 'TIMEOUT_REFRESH':	window.setTimeout('window.location.reload(true)', 3000);	break;
		default: 				window.location.reload(true);	break;
	}
}

function PrintObjectTag(objName, onloadName, width, height, sourceName, bgType, lanStr, snapUUID, jpegUUID, model, userLevel, userCtrl)
{
	if 		(typeof snapUUID 	== "undefined")	snapUUID = "";
	else if	(typeof jpegUUID 	== "undefined")	jpegUUID = "";
	else if	(typeof model 		== "undefined")	model = "";
	else if	(typeof userLevel 	== "undefined")	userLevel = "";
	else if	(typeof userCtrl 	== "undefined")	userCtrl = "";

	var str = '';
	str += '<object id='+objName+' data="data:application/x-silverlight-2," type="application/x-silverlight-2" width='+width+' height='+height+'>';
	if (onloadName != '')
	{
		str += '<param name="onload" value='+onloadName+' />';
	}
	str += '<param name="source" value='+sourceName+' />';
	str += '<param name="onError" value="onSilverlightError" />';
	str += '<param name="background" value='+bgType+' />';
	str += '<param name="minRuntimeVersion" value="4.0.50917.0" />';
	str += '<param name="initParams" value="culture='+lanStr+', snapUUID='+snapUUID+', jpegUUID='+jpegUUID+', model='+model+', currentUserLevel='+userLevel+', userRightCtrl='+userCtrl+'" />';
	str += '<param name="autoUpgrade" value="false" />'
	str += '<a href="./SilverlightInstall.cgi " style="text-decoration:none">Get Microsoft Silverlight</a>';
	str += '</object>';
 	str += '<iframe id="_sl_historyFrame" style="visibility:hidden;height:0px;width:0px;border:0px"></iframe>';
	document.write(str);
}

function onSilverlightError(sender, args)
{
   var appSource = "";
   if (sender != null && sender != 0) {
       appSource = sender.getHost().Source;
   }

   var errorType = args.ErrorType;
   var iErrorCode = args.ErrorCode;

   if (errorType == "ImageError" || errorType == "MediaError") {
       return;
   }

   var errMsg = "Unhandled Error in Silverlight Application " + appSource + "\n";

   errMsg += "Code: " + iErrorCode + "    \n";
   errMsg += "Category: " + errorType + "       \n";
   errMsg += "Message: " + args.ErrorMessage + "     \n";

   if (errorType == "ParserError") {
       errMsg += "File: " + args.xamlFile + "     \n";
       errMsg += "Line: " + args.lineNumber + "     \n";
       errMsg += "Position: " + args.charPosition + "     \n";
   } else if (errorType == "RuntimeError") {
   	if (args.lineNumber != 0) {
      	     errMsg += "Line: " + args.lineNumber + "     \n";
      	     errMsg += "Position: " + args.charPosition + "     \n";
      	 }
      	 errMsg += "MethodName: " + args.methodName + "     \n";
   }
   throw new Error(errMsg);
}

function ChangeImage(id,imgpath) 
{
	try{
		document.getElementById(id).src = imgpath;
	}catch(e){

	}
}

var intTab = 0;
var intJump = 0;

function IsTab(event) 
{
	var keyCode;
	if(window.event){  //ie,crome, safari
		keyCode = event.keyCode;
	} else {  //firefox
		keyCode = event.which;
	}

	if (keyCode == 9) {
		intTab = 1;
	}
}

function IsNum(event) 
{
	var keyCode;
	if(window.event){  //ie,crome, safari
		keyCode = event.keyCode;

	} else {  //firefox
		keyCode = event.which;
	}
	var rv = getIEVersion();
	
	if ((keyCode > 47 && keyCode < 58) || keyCode == 8 ) {
		//0,1,2,3,4,5,6,7,8,9
	} else {
		if(window.event){ //ie
			if(rv < 9)
				event.returnValue = false;
			else
				event.preventDefault();
		} else { //firefox
			event.preventDefault();
		}
	}

	if (keyCode == 46) {
		intJump = 1;
	}
	intTab = 0;//tab key cannot generate onkeypress event

	/*
	if (event.keyCode < 48 || event.keyCode > 57)
		event.returnValue = false;
	if (event.keyCode == 46) {
		intJump = 1;
	}
	intTab = 0;//tab key cannot generate onkeypress event
	*/
}

function OnlyNUm(event) 
{
	var keyCode;
	if(window.event){  //ie,crome, safari
		keyCode = event.keyCode;

	} else {  //firefox
		keyCode = event.which;

	}
	var rv = getIEVersion();

	//delete 46
	if ((keyCode > 47 && keyCode < 58) || keyCode == 8 || keyCode == 9 || keyCode == 37 || keyCode == 39 || keyCode == 46 ||(keyCode > 95 && keyCode < 106)) {
		//0,1,2,3,4,5,6,7,8,9
	} else {
		if(window.event){ //ie
			if(rv < 9)
				event.returnValue = false;
			else
				event.preventDefault();
		} else { //firefox
			event.preventDefault();
		}
	}

	if (keyCode == 46) {
		intJump = 1;
	}
	intTab = 0;//tab key cannot generate onkeypress event

	/*
	if (event.keyCode < 48 || event.keyCode > 57)
		event.returnValue = false;
	if (event.keyCode == 46) {
		intJump = 1;
	}
	intTab = 0;//tab key cannot generate onkeypress event
	*/
}

function CheckKorean(event)
{
	var keyCode;
	if(window.event){  //ie,crome, safari
		keyCode = event.keyCode;

	} else {  //firefox
		keyCode = event.which;

	}
	var rv = getIEVersion();
	var check =  /^[a-zA-Z0-9]+$/;

	keychar = String.fromCharCode(keyCode);

	if(event.shiftKey && keyCode == 37)
	{
		if(window.event){ //ie
			if(rv < 9)
				event.returnValue = false;
			else
				event.preventDefault();
		} else { //firefox
			event.preventDefault();
		}
	}

	if(check.test(keychar) || keyCode == 8 || keyCode == 9 || keyCode == 37 || keyCode == 39 || keyCode == 46 || keyCode ==96) {}
	else {

		if(window.event){ //ie
			if(rv < 9)
				event.returnValue = false;
			else
				event.preventDefault();
		} else { //firefox
			event.preventDefault();
		}
	}

}

function NoKorean(event)
{
	var keyCode;
	if(window.event){  //ie,crome, safari
		keyCode = event.keyCode;

	} else {  //firefox
		keyCode = event.which;

	}
	var rv = getIEVersion();
	
	if(BrowserDetect.browser=='Firefox' && keyCode == 9) {
		event.preventDefault();
	}
	if (keyCode == 229){
		if(window.event){ //ie
			if(rv < 9)
				event.returnValue = false;
			else
				event.preventDefault();
		} else { //firefox
			
			event.preventDefault();
		}
	}
}

function CheckIPv4(event)
{	var keyCode;

	if(window.event){  //ie,crome, safari
		keyCode = event.keyCode;

	} else {  //firefox
		keyCode = event.which;

	}

	var rv = getIEVersion();
	var check =  /^[0-9]+$/;

	keychar = String.fromCharCode(keyCode);

	if(event.shiftKey && keyCode == 37){

		if(window.event){ //ie
			if(rv < 9)
				event.returnValue = false;
			else
				event.preventDefault();
		} else { //firefox
			event.preventDefault();
		}
	}
	if(check.test(keychar) || keyCode == 8 || keyCode == 9|| keyCode == 46 || keyCode == 37 || keyCode == 39 ||(keyCode > 95 && keyCode < 106) || keyCode == 110 ||  keyCode == 190 ) {}
	//backspace, tab, delete, <-, ->, keypadNumber, . , keypad.
	else {

		if(window.event){ //ie
			if(rv < 9)
				event.returnValue = false;
			else
				event.preventDefault();
		} else { //firefox
			event.preventDefault();
		}
	}

}

function CheckIPv6(event, type)
{	var keyCode;

	if(window.event){  //ie,crome, safari
		keyCode = event.keyCode;

	} else {  //firefox
		keyCode = event.which;

	}

	var rv = getIEVersion();
	var check =  /^[a-fA-F0-9]+$/;
	keychar = String.fromCharCode(keyCode);
	if((event.shiftKey && keyCode == 37) || (type== 'down' && keyCode == 110) || (type== 'press' && keyCode == 59)){

		if(window.event){ //ie
			if(rv < 9)
				event.returnValue = false;
			else
				event.preventDefault();
		} else { //firefox
			event.preventDefault();
		}
	}
	if(check.test(keychar) || keyCode == 8|| keyCode == 9 || keyCode == 46 || keyCode == 37 || keyCode == 39 ||(keyCode > 95 && keyCode < 106) || keyCode == 186 ||  keyCode == 58 ||  keyCode == 59) {}
	//backspace, delete, <-, ->, keypadNumber, :
	else {

		if(window.event){ //ie
			if(rv < 9)
				event.returnValue = false;
			else
				event.preventDefault();
		} else { //firefox
			event.preventDefault();
		}
	}
}

function IsIPv6Char(event) {
	//0~9, : ,a~f, A~F
	var keyCode;
	if(window.event){  //ie,crome, safari
		keyCode = event.keyCode;
	} else {  //firefox
		keyCode = event.which;
	}
	var rv = getIEVersion();

	if (   (keyCode >= 48 && keyCode <= 57)
	  ||  (keyCode == 58)
	  ||  (keyCode >= 65 && keyCode <= 70)
	  ||  (keyCode >= 97 && keyCode <= 102)
	  ||keyCode == 8
	  || keyCode == 190) {
		//0~9, : ,a~f, A~F
	} else {
		if(window.event){ //ie
			if(rv < 9)
				event.returnValue = false;
			else
				event.preventDefault();
		} else { //firefox
			event.preventDefault();
		}
	}
}

function IsIPv4Char(event) 
{
	//0~9, .
	var keyCode;
	if(window.event){  //ie,crome, safari
		keyCode = event.keyCode;
	} else {  //firefox
		keyCode = event.which;
	}
	var rv = getIEVersion();

	if (  (keyCode > 47 && keyCode < 58)
	||keyCode ==46
       ||keyCode == 8
	   || keyCode == 190) {
		//0~9, .
	} else {
		if(window.event){ //ie
			if(rv < 9)
				event.returnValue = false;
			else
				event.preventDefault();
		} else { //firefox
			event.preventDefault();
		}
	}
}

function IsUrlChar(event) 
{
	var keyCode;
	if(window.event){  //ie,crome, safari
		keyCode = event.keyCode;
	} else {  //firefox
		keyCode = event.which;
	}
	var rv = getIEVersion();
	
	if ( (keyCode >= 97 && keyCode <= 122)
		|| (keyCode >= 65 && keyCode <= 90)
		|| (keyCode >= 48 && keyCode <= 57)
		|| keyCode == 45 || keyCode == 46 || keyCode == 47||keyCode == 8 ||keyCode == 95) {
		// a~z, A~Z, 0~9, -, ., /, _

	} else {
		if(window.event){ //ie
			if(rv < 9)
				event.returnValue = false;
			else
				event.preventDefault();
		} else { //firefox
			event.preventDefault();
		}
	}
}

function IsBackSlash(event)
{ // cannot input '\'
	var keyCode;
	if(window.event){  //ie,crome, safari
		keyCode = event.keyCode;
	}else	{  //firefox
		keyCode = event.which;
	}
	var rv = getIEVersion();

	if(keyCode == 92){
		if(window.event){ //ie
			if(rv < 9)
				event.returnValue = false;
			else
				event.preventDefault();
		} else { //firefox
			event.preventDefault();
		}
	}
}

function IsBackSlashOrSmallQuote(event)
{ // cannot input ' or \ for 802.1x
	var keyCode;
	if(window.event){  //ie,crome, safari
		keyCode = event.keyCode;
	}else	{  //firefox
		keyCode = event.which;
	}
	var rv = getIEVersion();

	if(keyCode == 92 || keyCode == 39){
		if(window.event){ //ie
			if(rv < 9)
				event.returnValue = false;
			else
				event.preventDefault();
		} else { //firefox
			event.preventDefault();
		}
	}
}

function IsSIM(event) 
{
	var keyCode;
	if(window.event){  //ie,crome, safari
		keyCode = event.keyCode;

	} else {  //firefox
		keyCode = event.which;
	}

	var rv = getIEVersion();

	if ( (keyCode >= 97 && keyCode <= 122)
		|| (keyCode >= 65 && keyCode <= 90)
		|| (keyCode >= 48 && keyCode <= 57)
		|| keyCode == 126 || keyCode == 96  || keyCode == 32 || keyCode == 33 || keyCode == 36
		|| keyCode == 40  || keyCode == 41 || keyCode == 44 || keyCode == 45 || keyCode == 46 || keyCode == 47
		|| keyCode == 59  || keyCode ==63  ||keyCode == 64  || keyCode == 91 ||keyCode == 93  ||keyCode==94
		|| keyCode == 95  || keyCode ==123 || keyCode == 124 || keyCode == 125
	    ||keyCode == 8) {
		// ~`!@$^()_-|{}[];,./?
	} else {
		if(window.event){ //ie
			if(rv < 9)
				event.returnValue = false;
			else
				event.preventDefault();
		} else { //firefox
			event.preventDefault();
		}
	}
}

function IsFriendlyName(event) 
{
	var keyCode;
	if(window.event){  //ie,crome, safari
		keyCode = event.keyCode;

	} else {  //firefox
		keyCode = event.which;
	}

	var rv = getIEVersion();

	if ( (keyCode >= 97 && keyCode <= 122)
		|| (keyCode >= 65 && keyCode <= 90)
		|| (keyCode >= 48 && keyCode <= 57)
		|| keyCode == 32 || keyCode == 126 	|| keyCode == 33 || keyCode == 64 || keyCode == 36 || keyCode == 95 || keyCode == 45 || keyCode == 124
		|| keyCode == 123|| keyCode == 125	|| keyCode == 91 || keyCode == 93 || keyCode == 44 || keyCode == 46 || keyCode == 47 || keyCode == 63   
	    || keyCode == 8) {
		// SPACE~!@$_-|{}[],./?
	} else {
		if(window.event){ //ie
			if(rv < 9)
				event.returnValue = false;
			else
				event.preventDefault();
		} else { //firefox
			event.preventDefault();
		}
	}
}

function IsNumChar(event)
{
	//0~9 a~z A~Z
	var keyCode;
	if(window.event){  //ie,crome, safari
		keyCode = event.keyCode;
	} else {  //firefox
		keyCode = event.which;
	}
	var rv = getIEVersion();

	if (( keyCode >= 48 && keyCode <= 57 )
	  ||(keyCode >= 65 && keyCode <= 90 )
	  ||( keyCode >= 97 && keyCode <= 122)
	  ||(keyCode == 8)){

	} else {
		if(window.event){ //ie
			if(rv < 9)
				event.returnValue = false;
			else
				event.preventDefault();
		} else { //firefox
			event.preventDefault();
		}
	}
}

function SetCookie(name, value) 
{
	$.cookie(name, null);
	$.cookie(name, value, {path:'/', expires:365});
}

function GetCookie(name) 
{
	return $.cookie(name);
}

function DeleteCookie(name) {
	var temp;
	temp = GetCookie(name);
	document.cookie = name+ '=' + ';path=/'+';expires=Thu, 01 Jan 1970 00:00:01 GMT';
}

function ChkSilverInstalled() 
{
	if(Silverlight.isInstalled("4.0") == false || Silverlight.isInstalled("4.0.50917.0") == false)
		document.location = "./SilverlightInstall.cgi ";
}

var FRIENDLY_NAME = '~!@$_-|{}[],./?';
var SIM = '~`!@$^*()_-|{}[];,./?';
var NUM = '0123456789';
var ALPHA = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
var PATH_SIM = '~`!@$^()_-{}[];,./\\';
var FILE_SIM = '~`!@$^()_-{}[];,.';
var SPACE = ' ';
//var TAB = '\t';
var CR = '\r';
var LF = '\n';
var IPv6 = '0123456789abcdefABCDEF:';
var SIM2 = '#"%&';
var QUOTATION = "'";
var Directory ="`~!@#$%^&()-_=+[]{};',./";
var NasDirectory = "`~!@#$^&()-_=+[]{};',./";
var Folder = "'-!#$%&(),;@[]^_`{}~+=";

function CheckSpace(str)
{
	if(str.search(/\s/) != -1) {
		return true;
	}
	else {
		return false;
	}
}

function TypeCheck(s, spc)
{
	var i;
	var check = 0;
	var ls = 0;

	for(i=0; i<s.length; i++) {
		if (ls = spc.indexOf(s.substring(i, i+1)) >= 0){

			check = 1;
		}
		else {
			check = 0;
			break;
		}
	}

	if(check == 1) return true;
	else return false;
}

var BrowserDetect = {
	initialize: function () {
		this.OS = this.StringSearch(this.OSInfo) || "unknownOS";
		this.browser = this.StringSearch(this.BrowserInfo) || "unknownbrowser";
		this.version = this.VersionSearch(navigator.appVersion) || this.VersionSearch(navigator.userAgent) || "unknownversion";
	},
	VersionSearch: function (datastr) {
		var index = datastr.indexOf(this.versionSearchString);
		if (index == -1) return;
		return parseFloat(datastr.substring(index+this.versionSearchString.length+1));
	},
	StringSearch: function (data) {
		for (var i=0;i<data.length;i++)	{
			var dataprop = data[i].prop;
			var datastr = data[i].string;
			this.versionSearchString = data[i].identity || data[i].versionSearch;
			if (datastr) {
				if (datastr.indexOf(data[i].subString) != -1)
					return data[i].identity;
			}
			else if (dataprop)
				return data[i].identity;
		}
	},
	OSInfo : [
		{
			string: navigator.platform,
			subString: "Win",
			identity: "Windows"
		},
		{
			string: navigator.platform,
			subString: "Mac",
			identity: "Mac"
		}
	],
	BrowserInfo: [
		{
			string: navigator.userAgent,
			subString: "Chrome",
			identity: "Chrome"
		},
		{
			string: navigator.userAgent,
			subString: "Firefox",
			identity: "Firefox"
		},
		{
			string: navigator.vendor,
			subString: "Apple",
			identity: "Safari",
			versionSearch: "Version"
		},
		{
			string: navigator.userAgent,
			subString: "MSIE",
			identity: "Explorer",
			versionSearch: "MSIE"
		},
		{
			string: navigator.userAgent,
			subString: "Trident",
			identity: "Explorer",
			versionSearch: "rv"
		},
		{
			string: navigator.userAgent,
			subString: "Gecko",
			identity: "Mozilla",
			versionSearch: "rv"
		},
		{
			prop: window.opera,
			identity: "Opera"
		}
	]

};
BrowserDetect.initialize();

function getIEVersion(){
	var rv = -1;
	if (navigator.appName == 'Microsoft Internet Explorer') {
		var ua = navigator.userAgent;
		var re = new RegExp("MSIE ([0-9]{1,}[\.0-9]{0,})");
		if (re.exec(ua) != null)
			rv = parseFloat(RegExp.$1);
	}else if (navigator.appName == 'Netscape'){
		var ua = navigator.userAgent;
		var re  = new RegExp("Trident/.*rv:([0-9]{1,}[\.0-9]{0,})");
		if (re.exec(ua) != null)
		  rv = parseFloat( RegExp.$1 );
	}
	return rv;
}

String.prototype.replaceAll = function( searchStr, replaceStr )
{
	var temp = this;
	while( temp.indexOf( searchStr ) != -1 )
	{
	temp = temp.replace( searchStr, replaceStr );
	}
	return temp;
}

function leadingZeros(n, digits) 
{
	var zero = '';
	n = n.toString();
	if (n.length < digits) {
		for (i = 0; i < digits - n.length; i++)
			zero += '0';
	}
	return zero + n;
}

////////////////////////////////////////////////
/////////// 	NETWORK			////////////////
////////////////////////////////////////////////
function CalSubnetMask(prefix)
{
	var dataVal = new Array("255", "254", "252", "248", "240", "224", "192", "128", "0");
	var prefixVal = "";

	if (prefix >= 24) {
		prefixVal = "255.255.255.";
		prefixVal += dataVal[32-prefix];
	}
	else if (prefix >= 16) {
		prefixVal = "255.255.";
		prefixVal += dataVal[24-prefix]+".0";
	}
	else if (prefix >= 8) {
		prefixVal = "255.";
		prefixVal += dataVal[16-prefix]+".0.0";
	}
	else {
		prefixVal += dataVal[8-prefix]+".0.0.0";
	}

	return prefixVal;
}

function CheckValidIPv6Address(ip)
{
	var digits = "0123456789abcdef";
	var check_digit = false;
	var val = 0;
	var colonp = -1;
	var i = 0;
	var j = 0;
	var len;
	var letter1;
	var curtok;
	var ch;
	var V6_INADDRSZ = 16;

	if ((letter1 = ip.charAt(i)) == ':') {
		if ((letter1 = ip.charAt(i++)) != ':')	return false;
	}

	curtok = i;

	while (i < ip.length) {
		ch = ip.charAt(i).toLowerCase();
		i++;
		if ((len = digits.indexOf(ch)) != -1) {
			val <<= 4;
			val |= len;
			if (val > 0xffff)	return false;
			check_digit = true;
			continue;
	 	}

		if (ch == '%') break;

		if (ch == ':') {
			curtok = i;
			if (!check_digit) {
				if (colonp != -1) return false;
				colonp = j;
				continue;
			}
			else if (i == ip.length)	return false;

			if ((j + 2) > V6_INADDRSZ)	return false;
			j += 2;
			val = 0;
			check_digit = false;
			continue;
		}

		if (ch == '.'  && ((j + 4) <= V6_INADDRSZ)) {
			// TODO: IPv4 mapped IPv6 address is not supported
			if (!CheckValidIPv4Address(ip.substring(curtok)))	return false;
			j += 4;
			check_digit = false;
			break;
		}
		return false;
	}

	if (check_digit) {
		if ((j + 2) > V6_INADDRSZ)	return false;
		j += 2;
	}

	if (colonp != -1) {
		if (j == V6_INADDRSZ)	return false;
		j = V6_INADDRSZ;
	}

	if (j != V6_INADDRSZ) return false;

	return true;
}


function CheckValidIPv4Address(addr)
{
	if(addr == '') return false;

	var ipPattern 	= /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/;
	var ipArray 	= addr.match(ipPattern);

	if(ipArray == null) return false;

	var ip_num 	= ((ipArray[1]&0xFF)<<24) + ((ipArray[2]&0xFF)<<16) + ((ipArray[3]&0xFF)<<8) + ((ipArray[4]&0xFF)<<0);
	thisSegment 	= ipArray[1];

	if(thisSegment < 1 || thisSegment > 223) return false;
	for(var i=2; i<5; i++) {
		thisSegment = ipArray[i];
		if(thisSegment>255) return false;
	}

	for (var i=1; i<5; i++){
		 if (ipArray[i].length > 1) {
			if (ipArray[i].charAt(0)  == '0')
				return false;
		}
	}
	return true;
}

function CheckIPv6Address(addr)
{
	if(addr == '')		return false;
	if(CheckValidIPv6Address(addr) == false)		return false;

	var ipv6Addr = addr.split(":");
	if (ipv6Addr.length < 3) return false;

	var spaceCnt = 0;
	for (var ix=0; ix<ipv6Addr.length; ++ix) {
		if (ipv6Addr[ix].length < 0 || ipv6Addr[ix].length > 4) return false;
		if (ipv6Addr[ix].length == 0) 	spaceCnt++;
	}

	if ((spaceCnt > 1 && ipv6Addr[0].length != 0 && ipv6Addr[ipv6Addr.length - 1].length != 0) || (spaceCnt == 0 && ipv6Addr.length != 8)) return false;
	return true;
}

function CheckIPv4Prefix(prefix)
{
	prefix = parseInt(prefix, 10);
	if((prefix < 1) || (prefix > 32)) return false;
	return true;
}

function CheckIPv6Prefix(prefix)
{
	prefix = parseInt(prefix, 10);
	if (prefix < 1 || prefix > 128) return false;
	return true;
}

function CheckPrefix(prefix, protocol)
{
	prefix = parseInt(prefix, 10);
	if (protocol == 'IPv4' && (prefix < 1 || prefix > 32)) return false;
	if (protocol == 'IPv6' && (prefix < 1 || prefix > 128)) return false;
	return true;
}

function GetBasicIPv6Address(address)
{
	var return_address = address;
	var first_address = return_address.split(':');

	if( first_address[0] == "0" ){
		return_address = return_address.replace('0:','0000:');
	}
	if( first_address[0] == "" ){
		return_address = return_address.replace('::','0000::');
	}

	return_address = return_address.replace(/:0:/, ":0000:");

	if(address.match("::") != null){

		var delimeter_count = return_address.match(new RegExp(":","ig")).length;
		var replace0=":0000:";
		for( ind = 0; ind < (7-delimeter_count); ind++ ){
			replace0 += "0000:";
		}
		return_address = return_address.replace('::', replace0);
	}
	return return_address;
}

function CheckDuplicatedAddress(obj, cnt)
{
	for (var index=0; index<(cnt-1); ++index) 
	{
		for (var index2=(index+1); index2<cnt; ++index2)
		{
			if($('tr').hasClass(obj+'_list_'+index) && $('tr').hasClass(obj+'_list_'+index2))
			{
				var compare_address1 = $('#'+obj+'_addr_'+index).val();
				var compare_address2 = $('#'+obj+'_addr_'+index2).val();

				var basic_compare_address1 = GetBasicIPv6Address(compare_address1);
				var basic_compare_address2 = GetBasicIPv6Address(compare_address2);

				if (basic_compare_address1.toLowerCase() == basic_compare_address2.toLowerCase())
				{
				    if ($('#' + obj + '_addr_' + index).val().toLowerCase() == $('#' + obj + '_addr_' + index2).val().toLowerCase())
				        return false;
				}
			}
		}
	}
	return true;
}

function CheckDeletedTarget(obj)
{
	var selNo = $("input[name='"+obj+"_select']:checked").val();
	if (typeof selNo == "undefined") return false;
	$('tr').detach('.'+obj+'_list_'+selNo);

	for(var index=selNo; index<10; ++index) {
		if($('tr').hasClass(obj+'_list_'+index)) {
			selNo = index;
			break;
		}
	}
	if ($('tr').hasClass(obj+'_list_'+selNo) == false) {
		for(var index=selNo; index>=0; --index) {
			if($('tr').hasClass(obj+'_list_'+index)) {
				selNo = index;
				break;
			}
		}
	}
	if ($('tr').hasClass(obj+'_list_'+selNo))	$('#'+obj+'_select_'+selNo).prop('checked', true);
	eval(obj+"_cnt--;");
	return true;
}

function CheckValueRange(val, min, max, alertMsg)
{
	if (val < min || val > max) {
		alert(alertMsg);
		return true;
	}
	return false;
}

jQuery.fn.styledSelect = function(options) {
	var prefs = {
		coverClass : 'select-replace-cover',
		innerClass : 'select-replace',
		adjustPosition : { top:0, left:0 },
		selectOpacity : 0
		}
	if (options) jQuery.extend(prefs,options);
	return this.each( function() {
		var selElm = jQuery(this);
		selElm.wrap('<span><'+'/span>');
		selElm.after('<span><'+'/span>');
		var selReplace = selElm.next();
		var selCover = selElm.parent();
		selElm.css({
			'opacity':prefs.selectOpacity,
			'visibility':'visible',
			'position':'absolute',
			'top':0,
			'left':0,
			'display':'inline',
			'z-index':1
			});
		selCover.addClass(prefs.coverClass).css({
			'display':'inline-block',
			'position':'relative',
			'top':prefs.adjustPosition.top,
			'left':prefs.adjustPosition.left,
			'z-index':0,
			'vertical-align':'middle',
			'text-align':'left'
			});
		selReplace.addClass(prefs.innerClass).css({
			'display':'block',
			'white-space':'nowrap'
			});

		selElm.bind('change',function() {
			jQuery(this).next().text(this.options[this.selectedIndex].text);
			}).bind('resize',function() {
			jQuery(this).parent().width( jQuery(this).width()+'px' );
			});
		selElm.trigger('change').trigger('resize');
		});
	}

function Time_t(year, month, day, hour, minute, second, isdst, wday, mday, yday)
{ // move to common_function.js!
    this.tm_year = year;
    this.tm_month = month;
    this.tm_day = day;
    this.tm_hour = hour;
    this.tm_min = minute;
    this.tm_sec = second;
    this.tm_isdst = isdst;
    this.tm_wday = wday;
    this.tm_mday = mday;
    this.tm_yday = yday;
}

function stm_to_timet( stm )
{
	var tDay = 0;
	tDay += (stm.tm_year-70)*365;
	tDay += (stm.tm_year+1899)/4 - (stm.tm_year+1899)/100 + (stm.tm_year+1899)/400;
	tDay -= 477/* (1969/4) - (1969/100) + (1969/400) */;
	if( ( stm.tm_year%4 == 0 && stm.tm_year%100 != 0 ) || stm.tm_year%400 == 0 )
	{
		switch( stm.tm_mon )
		{
		case 1: tDay += 31; break;
		case 2: tDay += 60; break;
		case 3: tDay += 91; break;
		case 4: tDay += 121; break;
		case 5: tDay += 152; break;
		case 6: tDay += 182; break;
		case 7: tDay += 213; break;
		case 8: tDay += 244; break;
		case 9: tDay += 274; break;
		case 10: tDay += 305; break;
		case 11: tDay += 335; break;
		}
	}
	else
	{
		switch( stm.tm_mon )
		{
		case 1: tDay += 31; break;
		case 2: tDay += 59; break;
		case 3: tDay += 90; break;
		case 4: tDay += 120; break;
		case 5: tDay += 151; break;
		case 6: tDay += 181; break;
		case 7: tDay += 212; break;
		case 8: tDay += 243; break;
		case 9: tDay += 273; break;
		case 10: tDay += 304; break;
		case 11: tDay += 334; break;
		}
	}
	tDay += stm.tm_mday-1;
	return tDay*86400/* 24*60*60 */ + stm.tm_hour*3600/* 60*60 */ + stm.tm_min*60 + stm.tm_sec;
}

function timet_to_stm( timet )// move to common_function.js!
{
  	var tmptm = new Time_t(0,0,0,0,0,0,0,0,0,0);
  	tmptm.tm_sec = timet%60;
  	tmptm.tm_min = timet/60%60;
  	tmptm.tm_hour = timet/60/60%24;
  	var tDay = timet/60/60/24 + 719162/* 1969*365 + (1969/4) - (1969/100) + (1969/400) */;
  	var year400 = tDay/146097/* (400*365+100-4+1) */;
  	var day_year400r = tDay%(146097/* (400*365+100-4+1) */);
  	var year100 = day_year400r/(36524/* 100*365+25-1 */);
  	var day_year100r = day_year400r%(36524/* 100*365+25-1 */);
  	var year4 = day_year100r/(1461/* 4*365+1 */);
  	var day_year4r = day_year100r%(1461/* 4*365+1 */);
  	var year1 = day_year4r/365;
  	var day_year1r = day_year4r % 365;
  	tmptm.tm_isdst = 0;
  	tmptm.tm_wday = (tDay + 1) % 7;
  	if( year1 == 4 )
  	{
  		tmptm.tm_year = year400 * 400 + year100 * 100 + year4 * 4 + year1 - 1900;
  		tmptm.tm_yday = 365;
  		tmptm.tm_mon = 11;
  		tmptm.tm_mday = 31;
  	}
  	else
  	{
  		tmptm.tm_year = year400 * 400 + year100 * 100 + year4 * 4 + year1 - 1899;
  		tmptm.tm_yday = day_year1r;
  		if( year1 == 3 )
  		{
  			if (tmptm.tm_yday < 31) { tmptm.tm_mon = 0; tmptm.tm_mday = tmptm.tm_yday + 1; }
  			else if (tmptm.tm_yday < 60) { tmptm.tm_mon = 1; tmptm.tm_mday = tmptm.tm_yday - 30; }
  			else if (tmptm.tm_yday < 91) { tmptm.tm_mon = 2; tmptm.tm_mday = tmptm.tm_yday - 59; }
  			else if (tmptm.tm_yday < 121) { tmptm.tm_mon = 3; tmptm.tm_mday = tmptm.tm_yday - 90; }
  			else if (tmptm.tm_yday < 152) { tmptm.tm_mon = 4; tmptm.tm_mday = tmptm.tm_yday - 120; }
  			else if (tmptm.tm_yday < 182) { tmptm.tm_mon = 5; tmptm.tm_mday = tmptm.tm_yday - 151; }
  			else if (tmptm.tm_yday < 213) { tmptm.tm_mon = 6; tmptm.tm_mday = tmptm.tm_yday - 181; }
  			else if (tmptm.tm_yday < 244) { tmptm.tm_mon = 7; tmptm.tm_mday = tmptm.tm_yday - 212; }
  			else if (tmptm.tm_yday < 274) { tmptm.tm_mon = 8; tmptm.tm_mday = tmptm.tm_yday - 243; }
  			else if (tmptm.tm_yday < 305) { tmptm.tm_mon = 9; tmptm.tm_mday = tmptm.tm_yday - 273; }
  			else if (tmptm.tm_yday < 335) { tmptm.tm_mon = 10; tmptm.tm_mday = tmptm.tm_yday - 304; }
  			else { tmptm.tm_mon = 11; tmptm.tm_mday = tmptm.tm_yday - 334; }
  		}
  		else
  		{
  			if (tmptm.tm_yday < 31) { tmptm.tm_mon = 0; tmptm.tm_mday = tmptm.tm_yday + 1; }
  			else if (tmptm.tm_yday < 59) { tmptm.tm_mon = 1; tmptm.tm_mday = tmptm.tm_yday - 30; }
  			else if (tmptm.tm_yday < 90) { tmptm.tm_mon = 2; tmptm.tm_mday = tmptm.tm_yday - 58; }
  			else if (tmptm.tm_yday < 120) { tmptm.tm_mon = 3; tmptm.tm_mday = tmptm.tm_yday - 89; }
  			else if (tmptm.tm_yday < 151) { tmptm.tm_mon = 4; tmptm.tm_mday = tmptm.tm_yday - 119; }
  			else if (tmptm.tm_yday < 181) { tmptm.tm_mon = 5; tmptm.tm_mday = tmptm.tm_yday - 150; }
  			else if (tmptm.tm_yday < 212) { tmptm.tm_mon = 6; tmptm.tm_mday = tmptm.tm_yday - 180; }
  			else if (tmptm.tm_yday < 243) { tmptm.tm_mon = 7; tmptm.tm_mday = tmptm.tm_yday - 211; }
  			else if (tmptm.tm_yday < 273) { tmptm.tm_mon = 8; tmptm.tm_mday = tmptm.tm_yday - 242; }
  			else if (tmptm.tm_yday < 304) { tmptm.tm_mon = 9; tmptm.tm_mday = tmptm.tm_yday - 272; }
  			else if (tmptm.tm_yday < 334) { tmptm.tm_mon = 10; tmptm.tm_mday = tmptm.tm_yday - 303; }
  			else { tmptm.tm_mon = 11; tmptm.tm_mday = tmptm.tm_yday - 333; }
  		}
  	}
  	return tmptm;
}

function isLeapYear(year)
{
	if(year%4==0 && ( year%100!=0 || year%400==0))
		return 1;
	else
		return 0;
}


var minLen = 8;	 
var PATTERN_NUM = /\d+/;	
var PATTERN_UPPER_ALPHA = /[A-Z]/;
var PATTERN_LOWER_ALPHA = /[a-z]/;
var PATTERN_SIMBOL1 = '/[`~!@#$%^&*()_|+\-=?;:\'",.<>\{\}\[\]\\\/]/'; 
var PATTERN_SIMBOL2 = /[^\w\sa-zA-Z0-9]/; 
var PATTERN_SIMBOL3 = /[^a-zA-Z0-9]/;	 
var PATTERN_SIMBOL4 = /[^\s:\\,a-zA-Z0-9]/;
var PATTERN_SIMBOL5 = /[`~!@#$%^*()_|+\-=?.\{\}\[\]\/]/; 
var PATTERN_CONSE_SIMBOL1 = /(\w)\1\1/; //같은문자 3번
var PATTERN_CONSE_SIMBOL2 = /(\d)\1\1/; //같은숫자 3번

function isSafePassword(passwd, id)
{
	if (passwd.length < minLen)
	{	
		return 1;
	}

	if (passwd == id)
	{
		return 2;
	}
	
    function strncmp(str1, str2, lgth) {

            var s1 = (str1 + '')
            .substr(0, lgth);
            var s2 = (str2 + '')
            .substr(0, lgth);

            return ((s1 == s2) ? 0 : ((s1 > s2) ? 1 : -1));
    }
	

	function isValidRule1(passwd) {

		var acceptCount = 0;	

		if (passwd.match(PATTERN_NUM)) acceptCount++;
		if (passwd.match(PATTERN_UPPER_ALPHA)) acceptCount++;
		if (passwd.match(PATTERN_LOWER_ALPHA)) acceptCount++;
		if (passwd.match(PATTERN_SIMBOL4)) acceptCount++;

		if (passwd.length < 10)
		{
			if (acceptCount < 3) return 3;
		}
		else
		{
			if (acceptCount < 2) return 4;
		}
 		return 0;
	}

	function isValidRule2(value, cnt)
	{
		var result  = 0;
		var checkStr = "";
		var checkAsc = ""; 
		var checkDesc = ""; 
 
		for (var z = 1; z < cnt; z++) 
		{
			checkStr  += "value.charAt(i) == value.charAt(i + " + z + ")";
			checkAsc  += "(value.charCodeAt(i) + " + z + ") == value.charCodeAt(i + " + z + ")";
			checkDesc += "(value.charCodeAt(i) - " + z + ") == value.charCodeAt(i + " + z + ")";
		
			if (z < cnt - 1)
			{
				checkStr  += " && ";
				checkAsc  += " && ";
				checkDesc += " && ";
			}
		}
		for (var i = 0; i < value.length - 2; i++)
		{
			if (eval(checkStr) || eval(checkAsc) || eval(checkDesc))
			{
				result = 5;
			}
 		}

		return result;
	}

	var ret = isValidRule1(passwd);
	
	if (0 == ret)
	{
		return isValidRule2(passwd, 4);
	}
	
	return ret;
}

function isSafePassword_S1(passwd, id)
{
	if (passwd.length < minLen)
	{	
		return 1;
	}

	if (passwd == id)
	{
		return 2;
	}

	function isValidRule1(passwd) {

		var acceptCount = 0;	

		if (passwd.match(PATTERN_NUM)) acceptCount++;
		if (passwd.match(PATTERN_UPPER_ALPHA)) acceptCount++;
		if (passwd.match(PATTERN_LOWER_ALPHA)) acceptCount++;
		if (passwd.match(PATTERN_SIMBOL3)) acceptCount++;

		if (passwd.length < 10)
		{
			if (acceptCount < 3) return 3;
		}
		else
		{
			if (acceptCount < 2) return 4;
		}
		return 0;
	}
	
	//연속적인 문자, 숫자체크
	function isValidRule2(value, cnt)
	{
		var result  = 0;
		var checkStr = "";
		var checkAsc = ""; 
		var checkDesc = ""; 
		var acceptCount1  = 0;

		//같은문자,숫자
		if (value.match(PATTERN_CONSE_SIMBOL1)) acceptCount1++;
		if (value.match(PATTERN_CONSE_SIMBOL2)) acceptCount1++;
		if (acceptCount1 > 0) result = 5;

		for (var z = 1; z < cnt; z++) 
		{
			checkStr  += "value.charAt(i) == value.charAt(i + " + z + ")";
			checkAsc  += "(value.charCodeAt(i) + " + z + ") == value.charCodeAt(i + " + z + ")";
			checkDesc += "(value.charCodeAt(i) - " + z + ") == value.charCodeAt(i + " + z + ")";
		
			if (z < cnt - 1)
			{
				checkStr  += " && ";
				checkAsc  += " && ";
				checkDesc += " && ";
			}
		}
		for (var i = 0; i < value.length - 2; i++)
		{
			if (eval(checkStr) || eval(checkAsc) || eval(checkDesc))
			{
				result = 5;
			}
		}

		return result;
	}

	var ret = isValidRule1(passwd);
	
	if (0 == ret)
	{
		//연속적인 문자, 숫자체크
		return isValidRule2(passwd, 3);
		//return isValidRule2(passwd);
	}
	
	return ret;
}

function IsNumCharSym(event, errPopupMsg) 
{
	var isErrPopup = 0;
	if (typeof errPopupMsg != 'undefined')
	{
		isErrPopUp = 1;
	}

	var keyCode;
	if(window.event){  //ie,crome, safari
		keyCode = event.keyCode;
	} else {  //firefox
		keyCode = event.which;
	}
	
	var value = String.fromCharCode(keyCode);

	if ( (keyCode >= 48 && keyCode <= 57)
	  ||(keyCode >= 65 && keyCode <= 90)
	  ||(keyCode >= 97 && keyCode <= 122)
	  ||(keyCode == 8) || (keyCode == 13)
	  ||value.match(PATTERN_SIMBOL5) ) {

	} else {
		event = event || window.event
		if(event.preventDefault){
			event.preventDefault();
		} else {
			event.returnValue = false;
		}
		/*
		if(window.event){  //ie,crome, safari
			event.returnValue = false;
		} else {
			event.preventDefault();
		}
		*/
		if (isErrPopUp > 0)
		{
			alert(errPopupMsg);
		}
	}
}

function IsNumCharSym_S1(event) 
{
	var keyCode;
	if(window.event){  //ie,crome, safari
		keyCode = event.keyCode;
	} else {  //firefox
		keyCode = event.which;
	}
	
	var value = String.fromCharCode(keyCode);

	if ( (keyCode >= 48 && keyCode <= 57)
	  ||(keyCode >= 65 && keyCode <= 90)
	  ||(keyCode >= 97 && keyCode <= 122)
	  ||(keyCode == 8) 
	  ||value.match(PATTERN_SIMBOL3) ) {

	} else {
		event = event || window.event
		if(event.preventDefault){
			event.preventDefault();
		} else {
			event.returnValue = false;
		}
		/*
		if(window.event){  //ie,crome, safari
			event.returnValue = false;
		} else {
			event.preventDefault();
		}
		*/
	}
}


function convertSymbolForXML(str) {
	str = str.replace(/&/gm, '&amp;');
	str = str.replace(/\</gm, '&lt;');
	str = str.replace(/\>/gm, '&gt;');
	str = str.replace(/\'/gm, '&apos;');
	return str.replace(/\"/gm, '&quot;');
}
function CheckNumCharSym(value)
{
	for(var i=0;i<value.length;i++)
	{
		var ch = value.charAt(i);
		var check = 0;
		if ( ch >= 'a' && ch <= 'z' ){
			check++;
		}else if( ch >= 'A' && ch <= 'Z' ){
			check++;
		}else if( ch >= '0' && ch <= '9' ){
			check++;
		}else if( ch == '~' || ch == '`' || ch == '!' || ch == '@' || ch == '#' || ch == '$' || ch == '%' || ch == '^' || ch == '*' ||
				ch == '(' || ch == ')' || ch == '_' || ch == '-' || ch == '+' || ch == '=' || ch == '|' ||
				ch == '{' || ch == '}' || ch == '[' || ch == ']' || ch == '.' || ch == '?' || ch == '/' ){
			check++;
		}
		if (check == 0)	
			return false;
	}
	
	return true;
}


function ChangeOption(obj, optionIndex, state)
{
	if (state == 'Enable') {
		if(BrowserDetect.browser == "Explorer" && getIEVersion() <= 7)
			$("#"+obj).children(':eq('+optionIndex+')').optionEnable();
		else
			$("#"+obj+" option:eq("+optionIndex+")").removeAttr("disabled");
	}
	else {
		if(BrowserDetect.browser == "Explorer" && getIEVersion() <= 7)
			$("#"+obj).children(':eq('+optionIndex+')').optionDisable();
		else
			$("#"+obj+" option:eq("+optionIndex+")").attr("disabled", "disabled");
	}
}

function SetOptionValue(obj, optionIndex, value)
{
	if(BrowserDetect.browser == "Explorer" && getIEVersion() <= 7)
		$("#"+obj).children(':eq('+optionIndex+')').replaceWith("<option value="+optionIndex+">"+value+"</option>");
	else
		$("#"+obj+" option:eq("+optionIndex+")").replaceWith("<option value="+optionIndex+">"+value+"</option>");
}

function SetButtonHoverFunction(isDisable, name)
{
	var splitValue = name.split('_');
	var direction = splitValue[splitValue.length-1];
	var path='', path1='', path2='';
	var targetName = name.substring(0, (name.length-direction.length-1));
	if (direction == 'left') {
		path = '../images/common/btn/slider_-_';
	}
	else {
		path = '../images/common/btn/slider_+_';
	}
	
	if (isDisable == false) {
		path1 = path+'press.png';
		path2 = path+'normal.png';
		$("#"+name).unbind('click');
		$("#"+name).hover(function(){ ChangeImage(name,path1); }, function(){ ChangeImage(name,path2); }).click(function(){ ControlSlider(targetName,direction); });	
	}
	else {
		path1 = path+'normal.png';
		path2 = path+'normal.png';
		$("#"+name).hover(function(){ ChangeImage(name,path1); }, function(){ ChangeImage(name,path2); }).unbind('click');
	}
}

function StopImageSetting()
{
	var reqUrl = ajaxReqUrl;
  	if (BrowserDetect.browser == "Explorer" || (BrowserDetect.browser == 'Safari' && reqUrl.search('.local') != -1)) {
  		reqUrl = "../.."+reqUrl.substr(reqUrl.indexOf("/cgi"));
  	}

  	$.ajax({
  		type: "POST",
  		data: encodeURI("<StopImageSetting/>"),
  		async: false,
  		cache: false,
  		url: reqUrl,
  		dataType: "text",
		timeout: 10000,
  		success: null,
  		error: null
  	});
}
