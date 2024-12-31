<?php
session_start();

$language = 0;
if(isSet($_SESSION["LANGUAGE"])){
	$language = $_SESSION["LANGUAGE"];
}

if($language == 1){
	$lang_file = 'Korean.php';
}else if($language == 2){
	$lang_file = 'Chinese.php';
}else if($language == 3){
	$lang_file = 'French.php';
}else if($language == 4){
	$lang_file = 'Italian.php';
}else if($language == 5){
	$lang_file = 'Spanish.php';
}else if($language == 6){
	$lang_file = 'German.php';
}else{
	$lang_file = 'English.php';
}

include_once $lang_file;
?>