<?php
	require_once ('../../cgi-bin/adv/_define.inc');
	$result = 0;
	$classInstances= GetClassInstance();
// DEV_S1COMPLEX
	if($GLOBALS['M_SPECIAL_TYPE'] == 1) {
		$passwd = $classInstances['Information']->dataInfo['Password']['value'];	
		$pw = $_POST['pw'];
		$pw = str_replace('\\\\', '\\', $pw );
		$pw = str_replace('\\\'', '\'', $pw );
		$pw = str_replace("\\\"", "\"", $pw );
		$pw = urldecode($pw);
		if ($passwd == $pw ) $result = 1; 

	}
	else {
		$passwd = str_replace("%","#4!2", $classInstances['Information']->dataInfo['Password']['value']); 
		$passwd = str_replace("+","#4!3", $passwd);

		if ($passwd == $_POST['pw'] ) $result = strlen($classInstances['Information']->dataInfo['Password']['value']);
	}
	echo $result;
?>
