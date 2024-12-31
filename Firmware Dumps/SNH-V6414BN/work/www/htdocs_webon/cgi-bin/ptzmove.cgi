<?php
define('ACTION_GET', 		0);
define('ACTION_GET_ALL',	1);
define('ACTION_SET', 		4);
define('ACTION_START',		7);
define('CMD_PTZ_CONTMOVE', 137);

$PTZ_MODELNAME = $_SERVER['MODELNAME'];
if (strlen($PTZ_MODELNAME) < 2)
{
	$socket = socket_create(AF_UNIX, SOCK_STREAM, 0);
	if ($socket < 0)	PTZResponseResult(FALSE);
	socket_set_option($socket, SOL_SOCKET, SO_RCVTIMEO, array('sec'=>3, 'usec'=>0));
	$retVal = socket_connect($socket, '/tmp/ipc_path');
	if ($retVal == FALSE)	 PTZResponseResult(FALSE);
	$headerInfo = array(	'MagicNumber' 		=> array('value'=>(int)0xFFFEFFFE,'type'=>'i1'),
								'IPCMajorVersion' => array('value'=>0, 	'type'=>'c1'),	'IPCMinorVersion' => array('value'=>6, 	'type'=>'c1'),
								'Command'			=>	array('value'=>24, 'type'=>'i1'),	'Action'				=>	array('value'=>0,	'type'=>'c1'),
								'Type'				=>	array('value'=>0, 'type'=>'c1'),	'ErrorCode' 		=> array('value'=>0, 'type'=>'c1'),
								'PayloadLength'	=>	array('value'=>0,'type'=>'i1'),	'PeerIP' 			=> array('value'=>'127.0.0.1', 'type'=>'A40'),
								'PeerPort' 			=> array('value'=>80, 'type'=>'i1'),	'PeerAccount' 		=> array('value'=>'', 'type'=>'a16'),
								'Reserved' 			=> array('value'=>'', 'type'=>'A8'));
	$headerPayload = '';
	foreach($headerInfo as $data) {	$headerPayload .= pack($data['type'], $data['value']);	}
	if (socket_write($socket, $headerPayload, strlen($headerPayload)) == FALSE) PTZResponseResult(FALSE);
	$recvPacket = PTZReceivePacket($socket, strlen($headerPayload));
	$dataArray = unpack('A12header/c1ErrorCode/i1PayloadLength/A68reserved', $recvPacket);
	if ($dataArray['ErrorCode'] != 1) PTZResponseResult(FALSE);
	$recvPacket = PTZReceivePacket($socket, $dataArray['PayloadLength']);
	$dataArray = unpack('A64data/A32model/A1246reserved', $recvPacket);
	socket_close($socket);
	$PTZ_MODELNAME = trim($dataArray['model']);
}

$PAYLOAD			= '';
$HEADER_ACTION = NULL;
$DATAINFO = array(	'PosPanReal'	=> array('value'=>0, 'type'=>'i1'), 	'PosPanNorm'	=> array('value'=>0, 'type'=>'i1'),
						'PosTiltReal'	=> array('value'=>0, 'type'=>'i1'), 'PosTiltNorm'	=> array('value'=>0, 'type'=>'i1'),
						'PosZoomReal'	=> array('value'=>0, 'type'=>'i1'), 'PosZoomNorm'	=> array('value'=>0, 'type'=>'i1'),
						'PosFocusReal' => array('value'=>0, 'type'=>'i1'), 'PosFocusNorm' => array('value'=>0, 'type'=>'i1'),
						'SpdPanReal'	=> array('value'=>0, 'type'=>'i1'), 'SpdPanNorm'		=> array('value'=>0, 'type'=>'i1'),
						'SpdTiltReal'	=> array('value'=>0, 'type'=>'i1'), 'SpdTiltNorm'	=> array('value'=>0, 'type'=>'i1'),
						'SpdZoomReal'	=> array('value'=>4, 'type'=>'i1'), 'SpdZoomNorm'	=> array('value'=>0, 'type'=>'i1'),
						'Timeout'		=> array('value'=>0, 'type'=>'i1'));
$digest = '';
$currentUserName = '';
preg_match_all('/(\w+)="([\w\s\~\`\!\@\$\^\*\(\)\_\-\|\{\}\[\]\;\,\.\?\/]+)"/', $_SERVER['PHP_AUTH_DIGEST'], $digest);
for ($index=0; $index<count($digest[1]); ++$index) {
	if ($digest[1][$index] == 'username') {
		$currentUserName = trim($digest[2][$index]);
		break;
	}
}

$model = $GLOBALS['PTZ_MODELNAME'];
if(!($model == 'SNP-3120V'	|| 	$model == 'SNP-3120VH'|| $model == 'SNP-3120'		|| $model == 'SNV-3120' 	||
	  $model == 'SNP-5200' 	|| 	$model == 'SNP-5200H' || $model == 'SNZ-5200'		||
	  $model == 'SNP-3371' 	||	$model == 'SNP-3371H' || $model == 'SNP-3371TH'  ||
     $model == 'SNP-3302'  ||  $model == 'SNP-3302H' || $model == 'SNP-6200' 	|| 	$model == 'SNP-6200H' ) ) PTZResponseResult(FALSE);


$GLOBALS['HEADER_COMMAND'] = CMD_PTZ_CONTMOVE;
$GLOBALS['HEADER_ACTION'] = ACTION_START;

if(isset($_REQUEST['move'])) {
	$speed = 6;
	if (isset($_REQUEST['speed'])) {
		if ($_REQUEST['speed'] < 1 || $_REQUEST['speed'] > 6 ) PTZResponseResult(FALSE);
		$speed = $_REQUEST['speed'];
	}

	switch($_REQUEST['move']) {
		case 'leftup': case 'leftdown': case 'rightup': case 'rightdown': {

				$cmdArr = array('down'=>-1, 'up'=>1);
				if (substr($_REQUEST['move'], 0, 4) == 'left') {
					$panReal = -1;
					$tiltMsg = substr($_REQUEST['move'], 4);
				}
				else {
					$panReal = 1;
					$tiltMsg = substr($_REQUEST['move'], 5);
				}
				$GLOBALS['DATAINFO']['PosPanReal']['value']	= $panReal;
				$GLOBALS['DATAINFO']['PosTiltReal']['value']	= $cmdArr[$tiltMsg];
				$GLOBALS['DATAINFO']['SpdPanReal']['value']	= $speed;
				$GLOBALS['DATAINFO']['SpdTiltReal']['value']	= $speed;
			}break;
		case 'left': case 'right': case 'up': case 'down': {

				$posCmd = array('left'=>array('PosPanReal', -1), 'right'=>array('PosPanReal', 1), 'down'=>array('PosTiltReal', -1), 'up'=>array('PosTiltReal', 1));
				$spdCmd = array('left'=>'SpdPanReal', 'right'=>'SpdPanReal', 'down'=>'SpdTiltReal', 'up'=>'SpdTiltReal');
				$GLOBALS['DATAINFO'][$posCmd[$_REQUEST['move']][0]]['value'] = $posCmd[$_REQUEST['move']][1];
				$GLOBALS['DATAINFO'][$spdCmd[$_REQUEST['move']]]['value'] = $speed;
			}
	}
}else if(isset($_REQUEST['zoom'])) {
	$cmdArray = array ('in'=>'1', 'out'=>'-1');
	if ($_REQUEST['zoom'] != 'in' && $_REQUEST['zoom'] != 'out' && $_REQUEST['zoom'] != 'stop')	PTZResponseResult(FALSE);
	if ($_REQUEST['zoom'] != 'stop') {
		$GLOBALS['DATAINFO']['PosZoomReal']['value'] = $cmdArray[$_REQUEST['zoom']];
	}

	$speed = 4;
	if (isset($_REQUEST['speed'])) {
		if ($_REQUEST['speed'] < 1 || $_REQUEST['speed'] > 4 ) PTZResponseResult(FALSE);
		$speed = $_REQUEST['speed'];
	}
	$GLOBALS['DATAINFO']['SpdZoomReal']['value'] = $speed;
}else {
	PTZResponseResult(FALSE);
}

foreach($GLOBALS['DATAINFO'] as $data) {
	$GLOBALS['PAYLOAD'] .= pack($data['type'], $data['value']);
}

$socket = socket_create(AF_UNIX, SOCK_STREAM, 0);
if ($socket < 0)	PTZResponseResult(FALSE);
socket_set_option($socket, SOL_SOCKET, SO_RCVTIMEO, array('sec'=>3, 'usec'=>0));
$retVal = socket_connect($socket, '/tmp/ipc_path');
if ($retVal == FALSE)	 PTZResponseResult(FALSE);
$headerInfo = array(	'MagicNumber' 		=> array('value'=>(int)0xFFFEFFFE,'type'=>'i1'),
							'IPCMajorVersion' => array('value'=>0, 	'type'=>'c1'),
							'IPCMinorVersion' => array('value'=>6, 	'type'=>'c1'),
							'Command'			=>	array('value'=>$GLOBALS['HEADER_COMMAND'], 'type'=>'i1'),
							'Action'				=>	array('value'=>$GLOBALS['HEADER_ACTION'],	'type'=>'c1'),
							'Type'				=>	array('value'=>0, 'type'=>'c1'),
							'ErrorCode' 		=> array('value'=>0, 'type'=>'c1'),
							'PayloadLength'	=>	array('value'=>strlen($GLOBALS['PAYLOAD']),'type'=>'i1'),
							'PeerIP' 			=> array('value'=>'127.0.0.1', 'type'=>'A40'),
							'PeerPort' 			=> array('value'=>80, 'type'=>'i1'),
							'PeerAccount' 		=> array('value'=>$GLOBALS['currentUserName'], 'type'=>'a16'),
							'Reserved' 			=> array('value'=>'', 'type'=>'A8'));
$headerPayload = '';
foreach($headerInfo as $data) {
	$headerPayload .= pack($data['type'], $data['value']);
}
if (socket_write($socket, $headerPayload, strlen($headerPayload)) == FALSE) PTZResponseResult(FALSE);
if ($GLOBALS['HEADER_ACTION'] == ACTION_SET || ($GLOBALS['HEADER_ACTION'] == ACTION_START && $GLOBALS['HEADER_COMMAND'] != 51)) {
	if (socket_write($socket, $GLOBALS['PAYLOAD'], strlen($GLOBALS['PAYLOAD'])) == FALSE) PTZResponseResult(FALSE);
}

$recvPacket = PTZReceivePacket($socket, strlen($headerPayload));
$dataArray = unpack('A12header/c1ErrorCode/i1PayloadLength/A68reserved', $recvPacket);
if ($dataArray['ErrorCode'] != 1) PTZResponseResult(FALSE);
if ($GLOBALS['HEADER_ACTION'] == ACTION_GET || $GLOBALS['HEADER_ACTION'] == ACTION_GET_ALL) {
	$recvPacket = PTZReceivePacket($socket, $dataArray['PayloadLength']);
	$dataFormat = '';
	while($data = current($GLOBALS['DATAINFO'])) {
		$dataFormat .= $data['type'].key($GLOBALS['DATAINFO'])."/";
		next($GLOBALS['DATAINFO']);
	}
	$dataArray = unpack($dataFormat, $recvPacket);
	foreach ($dataArray as $name=>$value) {
		$GLOBALS['DATAINFO'][$name]['value'] = $value;
	}
}

socket_close($socket);

header("Content-Type: text/plain");
header("Content-Length: 2");
echo "OK";
flush();

exit;

function PTZResponseResult($_value, $_status=FALSE)
{
	if ($_status && $GLOBALS['currentUserName'] != 'admin') return;
	$msgType = array('NG', 'OK');
	header("Content-Type: text/plain");
	header("Content-Length: 2");
	echo $msgType[$_value];
	flush();
	if (!$_status)	exit;
}

function PTZReceivePacket($_socket, $_packetSize)
{
	$recvPacketSize = 0;
	$totalRecvPacket = '';
	do {
		$recvPacket = socket_read($_socket, ($_packetSize-$recvPacketSize));
		if ($recvPacket < 0 || $recvPacket == NULL) {
			PTZResponseResult(FALSE);
		}
		$totalRecvPacket .= $recvPacket;
		$recvPacketSize = strlen($totalRecvPacket);
	}
	while($_packetSize != $recvPacketSize);
	return $totalRecvPacket;
}

?>

