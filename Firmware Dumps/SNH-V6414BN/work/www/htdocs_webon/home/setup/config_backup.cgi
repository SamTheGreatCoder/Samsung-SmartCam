<?php
//require_once ('authorization.cgi');
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('stw_util.cgi');

$_sendrequest = "<BackupConfiguration/>";	

$result = sendStwRequest($_sendrequest);

header('Content-Description: File Transfer');
header('Content-Type: application/octet-stream');
header('Content-Disposition: attachment; filename=backup_config.bin');
header('Set-Cookie: fileDownload=true; path=/');
header('Content-Transfer-Encoding: binary');
header('Expires: 0');
header('Cache-Control: must-revalidate');
header('Pragma: public');
//header('Content-Length: ' . filesize($result));
ob_clean();
flush();
echo $result;
exit;
?>
