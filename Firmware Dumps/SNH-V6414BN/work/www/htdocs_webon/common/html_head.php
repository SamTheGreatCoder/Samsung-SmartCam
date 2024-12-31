<?php
require_once $_SERVER["DOCUMENT_ROOT"] . "/resources/languages/Language.php";
if(!isset($_GET["login"])){
	echo "<meta http-equiv='refresh' content='0; url=http://".trim($_SERVER['HTTP_HOST'])."/index.htm'>";
}

$userAgent =  $_SERVER["HTTP_USER_AGENT"];

if(strpos($userAgent, "MSIE") || strpos($userAgent, "Trident")){
	$isMSIE = true;
} else {
	$isMSIE = false;
}
$isMSIE = ($isMSIE != null && trim($isMSIE) != "")? "1" : "0";
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
	<meta http-equiv="X-UA-Compatible" content="IE=8; requiresActiveX=true" />
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

	<title><?=$Lang["Samsung SmartCam"]?></title>

	<link href="../resources/css/reset.css" rel="stylesheet" type="text/css" />
	<link href="../resources/css/common.css" rel="stylesheet" type="text/css" />
	<link href="../resources/css/sub.css" rel="stylesheet" type="text/css" />
	<link href="../resources/css/cl.css" rel="stylesheet" type="text/css" />

	<script type="text/javascript" src="../resources/js/jquery.js" ></script>
	<script type="text/javascript" src="../resources/js/json2.js" ></script>
	<script type="text/javascript" src="/resources/js/shc_utils.js" ></script>
	<script type="text/javascript">
		if(document.all){
			document.onkeydown = trapRefreshIE;
		}else{
			document.captureEvents(Event.KEYDOWN);
			document.onkeydown = trapRefreshNS;
		}
		function trapRefreshNS(e){
			if(e.keyCode == 116){
				e.preventDefault();
				document.location.reload(true);
			}
		}
		function trapRefreshIE(){
			if(event.keyCode == 116){
				event.keyCode = 0;
				event.cancelBubble = true;
				event.returnValue = false;
				document.location.reload(true);
			}
		}

		function moveToPage(page){
			parent.moveToPage(page);
		}

		function showProgress(title){
			$("#prog_title").val(title);
			document.getElementById("mw_progress").style.display = "block";
		}
		function hideProgress(){
			document.getElementById("mw_progress").style.display = "none";
		}
		function byte2int(data, pos){
			var val = parseInt(data[pos+3] << 24) + parseInt(data[pos+2] << 16) + parseInt(data[pos+1] << 8) + parseInt(data[pos]);
			return (val < 0)? (val + 4294967296) : val;
		}

		function byte2str(data, pos, size){
			var result = "";
			for (var i=0, j=pos; i<size; i++, j++){
				if (data[j] != 0x00 && data[j] != 0xFF){
					result += String.fromCharCode(data[j]);
				}
			}
			return result;
		}

		function int2byte(data, pos, val){
			if(val < 0){
				val += 4294967296;
			}

			data[pos+3] = (val >>> 24);
			data[pos+2] = ((val & 0xFF0000) >> 16);
			data[pos+1] = ((val & 0xFF00) >> 8);
			data[pos] = (val & 0xFF);
		}

		function str2byte(data, pos, size, str){
			var len = (str.length > size)? size : str.length;

			for (var i=0; i<len; i++){
				data[pos + i] = str.charCodeAt(i);
			}
			for (var i=len; i<size; i++){
				data[pos + i] = 0x00;
			}
		}
	</script>
