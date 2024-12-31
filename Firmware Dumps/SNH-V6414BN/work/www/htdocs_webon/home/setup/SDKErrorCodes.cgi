<?php
require_once ('../language/language_sdk_errorcode.cgi');
$SDK_ERROR_CODES_MAP = array();
for($i=0;$i<23;$i++){
	$tempArray = array(
		66  => $t_tempUnavailable[$i],
		100 => $t_appAlreadyRunning[$i],
		101 => $t_appStartFailed[$i],
		102 => $t_appStopFailed[$i],
		103 => $t_appUploadFailed[$i],
		104 => $t_notEnoughSpace[$i],
		105 => $t_invalidAppPackage[$i],
		106 => $t_sameVersionInstalled[$i],
		107 => $t_installationFailed[$i],
                108 => $t_uninstallationFailed[$i],                 
		109 => $t_appNotFound[$i],
		110 => $t_appRecordRunning[$i],
		111 => $t_appNotRunning[$i],
		112 => $t_debugViewerRunning[$i], 
		113 => $t_invalidCameraPlatform[$i],
		114 => $t_cameraPlatformMismatch[$i],
		115 => $t_systemRecoverDBError[$i],
		116 => $t_parallelinstallInProgress[$i],
		117 => $t_CPULimitReached[$i],
		118 => $t_memoryLimitReached[$i],
		119 => $t_SDKVersionNotSupported[$i],
	);
	array_push($SDK_ERROR_CODES_MAP,$tempArray);
}
?>
