<?php
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_sdk_app_statuscode.cgi');
$SDK_APP_STATUS_CODES_MAP = array();
for($i=0;$i<23;$i++){
	$tempArray = array(
		-1 => $t_installFailed[$i],
		0 	=> $t_uninstalled[$i],
		1 	=> $t_uninstalling[$i],
		2 	=> $t_installed[$i],
		3 	=> $t_installing[$i],
		4 	=> $t_startedNotRunning[$i],
		5 	=> $t_running[$i],
		6 	=> $t_stopped[$i]
	);
	array_push($SDK_APP_STATUS_CODES_MAP,$tempArray);
}
?>
