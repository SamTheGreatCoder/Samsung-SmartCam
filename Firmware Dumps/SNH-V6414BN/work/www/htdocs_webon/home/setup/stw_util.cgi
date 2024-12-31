<?php
//require_once ('authorization.cgi');
session_start();
require_once($_SERVER["DOCUMENT_ROOT"]."/cgi-bin/adv/_define.inc");

function sendStwRequest($_sendrequest)
{
	$digest_header = "Digest " . $_SERVER['PHP_AUTH_DIGEST']; 
	//$sessId = session_id();		
	$cookieStr = $_SESSION['USERNAME'] . ":" . $_SESSION['PW']; 
	
  	$requestHeaders = array(
	    'Content-Type: application/x-www-form-urlencoded; charset=utf-8',
	    sprintf('Content-Length: %d', strlen($_sendrequest)),
	    "Authorization: " . $digest_header,
	    "Cookie:authCookie=$cookieStr"
	    //'Cookie: PHPSESSID=' . $sessId
	);
  	
	$opts = array('http' =>
	  array(
	    'method'  => 'POST',
	    'header'  => implode("\r\n", $requestHeaders),
	    'content' => $_sendrequest
	  )
	);

	//$addr = str_replace("::ffff:", "", $_SERVER['REMOTE_ADDR']);
	$url =  siteURL() . "/cgi-bin/stw.cgi";	
	//echo "url " . $url;
		
	$context  = stream_context_create($opts);
	$result = file_get_contents($url, false, $context);
	//echo "result " . $result;	
	return $result;
}

function siteURL()
{	//$addr = str_replace("::ffff:", "", $_SERVER['HTTP_HOST']);
	$protocol = ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] != 'off') || $_SERVER['SERVER_PORT'] == 443) ? "https://" : "http://";
	$domainName = $_SERVER['HTTP_HOST'];
	//echo " Protocol: Domainanme is ".$protocol.$domainName;
	return $protocol.$domainName;
}


function createContext($_sendrequest)
{
	$digest_header = "Digest " . $_SERVER['PHP_AUTH_DIGEST']; 
  	
  	$requestHeaders = array(
	    'Content-Type: application/x-www-form-urlencoded; charset=utf-8',
	    sprintf('Content-Length: %d', strlen($_sendrequest)),
	    "Authorization: " . $digest_header
	);
  	
	$opts = array('http' =>
	  array(
	    'method'  => 'POST',
	    'header'  => implode("\r\n", $requestHeaders),
	    'content' => $_sendrequest
	  )
	);

	$url =  siteURL() . "/cgi-bin/stw.cgi";
		
	$context  = stream_context_create($opts);
	return $context;
}

?>
