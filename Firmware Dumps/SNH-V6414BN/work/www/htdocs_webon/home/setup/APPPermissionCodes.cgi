<?php
require_once ('../language/language_sdk_permissioncode.cgi');
$APP_PERMISSION_CODES_MAP = array();

for($i=0;$i<23;$i++){
	$tempArray = array(
		0 => $t_permissionNone[$i],
		1 => $t_device[$i],
		2 => $t_PTZ[$i],
		4 => $t_network[$i],
		8 => $t_SDCard[$i]
	);
	array_push($APP_PERMISSION_CODES_MAP,$tempArray);
}
?>