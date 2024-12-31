<?php
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/constant.php";

$CLASS_PATH = $_SERVER["DOCUMENT_ROOT"] . "/stw-cgi/adv/";

/*****************************************************************************************************************
* function    : sendDataToSystem($cmd, $act, $type, $sendMsg)
* Description :
*****************************************************************************************************************/
function requestToCamera($cmd, $act, $type, $sendMsg, $isWiredNetwork=false){
	$retryCnt = 0;
	$sleepVal = array(10000, 30000, 50000);	
	if($act == ACTION_GET && $cmd == CMD_WIRELESS_SCANNING){
		ini_set("max_execution_time", 3);
	}else{
		ini_set("max_execution_time", 20);
	}
	
	if(($socket = socket_create(AF_UNIX, SOCK_STREAM, 0)) == false){
		return array("NOK", "socket create error.");
	}
	
	while($retryCnt < 3){	
		$result = @socket_connect($socket, "/tmp/ipc_path") or die("Check network connection and camera power.");
		if($result != false){
			break;
		}
		usleep($sleepVal[$retryCnt++]);
	}	
	if($retryCnt > 2){
		socket_shutdown($socket);
		socket_close($socket);
		return array("NOK", "Check network connection and camera power.");
	}
		
	$msgLen = ($sendMsg == null)? 0 : count($sendMsg);
	$header = makeHeader($cmd, $act, $type, $msgLen);
	$packet = ($msgLen == 0)? $header : array_merge($header, $sendMsg);
// 	if($act == ACTION_SET){
// 		echo implode(",", array_slice($packet, 0, 85)) . "\n\n";
// 		for($i=85, $j=1; $i<count($packet); $i+=100,$j++){
// 			if(count($packet) < ($i + 100)){
// 				echo implode(",", array_slice($packet, $i)) . "\n";
// 			}else{
// 				echo implode(",", array_slice($packet, $i, 100)) . "\n";
// 			}
// 			if(($j % 10) == 0){
// 				echo "\n";
// 			}
// 		}
// 	}
	$sendPacket = "";
	for($i=0; $i<count($packet); $i++){
		$sendPacket .= pack('C', $packet[$i]);
	}	

	$result = socket_write($socket, $sendPacket, strlen($sendPacket)) or die("Check network connection and camera power.");
	if($result == false){
		socket_shutdown($socket);
		socket_close($socket);
		return array("NOK", "Check network connection and camera power.");
	}
	
	$recvMsg = array(); 
	$chkLen = false;
	$msgLen = 0;
	$recvPacket;	
	$org_recvMsg;
	while(true){
		$data = socket_read($socket, BUFFER_SIZE) or die("Check network connection and camera power.");
		if($data == false){
			socket_shutdown($socket);
			socket_close($socket);
			return array("NOK", "Check network connection and camera power.");
		}
		
		if($isWiredNetwork == true){
			return array("OK", null);
		}
		
		$recvPacket .= $data;
		if(strlen($recvPacket) >= HEADER_OFF_PAYLOAD){
			if($chkLen == false){
				$length = array();
				for($i=0; $i<4; $i++){
					$length[$i] = ord(substr($recvPacket, HEADER_OFF_MSG_LENGTH + $i, 1));
				}
				$msgLen = byte2int($length, 0);
				$chkLen = true;
			}
			if($chkLen == true && $msgLen == 0){
				for($i=0; $i<HEADER_OFF_PAYLOAD; $i++){
					$recvHeader[$i] = ord(substr($recvPacket, $i, 1));
				}
				socket_shutdown($socket);
				socket_close($socket);
				
				if($recvHeader[HEADER_OFF_ERROR_CODE] != 0 && $recvHeader[HEADER_OFF_ERROR_CODE] != 1){
					if($recvHeader[HEADER_OFF_ERROR_CODE] == 27){
						return array("NOK", "Invalid Gateway!!");
					}else if($recvHeader[HEADER_OFF_ERROR_CODE] == 2){
						return array("NOK", "Invalid data!!");
					}else{
						return array("NOK", "Error code: " . $recvHeader[HEADER_OFF_ERROR_CODE]);
					}
				}else{
					return array("OK", null);
				}
			}
			
			if($msgLen <= (strlen($recvPacket) - HEADER_OFF_PAYLOAD)){
				for($i=0; $i<$msgLen; $i++){
					$org_recvMsg .= substr($recvPacket, ($i + HEADER_OFF_PAYLOAD), 1);
					$recvMsg[$i] = ord(substr($recvPacket, ($i + HEADER_OFF_PAYLOAD), 1));
				}				
// 				if($act == ACTION_GET && $cmd == CMD_WIRELESS_SCANNING){					
// 					for($i=0, $j=1; $i<count($recvMsg); $i+=100, $j++){
// 						if(count($recvMsg) < ($i + 100)){
// 							echo implode(",", array_slice($recvMsg, $i)) . "\n";
// 						}else{
// 							echo implode(",", array_slice($recvMsg, $i, 100)) . "\n";
// 						}
// 						if(($j % 10) == 0){
// 							echo "\n";
// 						}
// 					}					
// 				}				
				socket_shutdown($socket);
				socket_close($socket);
				return array("OK", $recvMsg, $org_recvMsg);
			}
		}
	}
	
	socket_shutdown($socket);
	socket_close($socket);
	return array("NOK", "Failed a receive data from system.");
}

function GetPayloads($_dataClass, $_max)
{
    $payloads = '';
    for ($index = 0; $index < $_max; ++$index)
    {

        $payloads .= $_dataClass[$index]->payload;
    }
    return $payloads;
}

function MakePayload($_dataInfo)
{
    $payload = '';
    foreach ($_dataInfo as $data)
    {
        $payload .= pack(strtolower($data['type']), trim($data['value']));
    }
    return $payload;
}

function MakeDataFormat($_dataInfo)
{
    $dataFormat = '';
    while ($data = current($_dataInfo))
    {
        $dataFormat .= $data['type'] . key($_dataInfo) . "/";
        next($_dataInfo);
    }
    return $dataFormat;
}

function MakeUnpackFormat($_name, $_length, $_maxValue)
{
    $unpackFormat = '';
    for ($index = 0; $index < $_maxValue; ++$index)
        $unpackFormat .= 'A' . $_length . $_name . $index . '/';
    return $unpackFormat;
}

function GetDataInfoLength($_dataInfo)
{
    $totalLength = 0;
    foreach ($_dataInfo as $data)
    {
        $length = (int) substr($data['type'], 1);
        $type = substr($data['type'], 0, 1);
        if ($type == 'i' || $type == 'I')
            $length *= 4;
        $totalLength += $length;
    }
    return $totalLength;
}

function SetData(&$_dataInfo, &$_payload, $_dataArray, $_dataFormat = '')
{
    if ($_dataFormat == '')
        $_dataFormat = MakeDataFormat($_dataInfo);
    if (is_string($_dataArray))
        $_dataArray = unpack($_dataFormat, $_dataArray);

    foreach ($_dataArray as $name => $value)
    {

        foreach ($_dataInfo as $key => $data)
        {

            if ($key != $name)
                continue;
            if (substr($_dataInfo[$name]['type'], 0, 1) == 'A')
                $value = stripslashes(trim($value));
            //		if ($_bitrateSet && $name == 'BitrateLimit')	$value = (int)$value * 1024;
            if ($name == 'BitrateLimit')
                $value = (int) $value * 1024;
            $_dataInfo[$name]['value'] = $value;
            break;
        }
    }
    $_payload = MakePayload($_dataInfo);
}

/*****************************************************************************************************************
* function    : makeHeader($cmd, $act, $type, $len){
* Description :
*****************************************************************************************************************/
function makeHeader($cmd, $act, $type, $len){
	$header = array();
	$header = array_fill(0, 77, 0x00);
	$header[HEADER_OFF_MAGIC_NUMBER] = 0xFE;
	$header[HEADER_OFF_MAGIC_NUMBER+1] = 0xFF;
	$header[HEADER_OFF_MAGIC_NUMBER+2] = 0xFE;
	$header[HEADER_OFF_MAGIC_NUMBER+3] = 0xFF;
	$header[HEADER_OFF_MAJOR_VERSION]	= MAJOR_VERSION;		//Major Version
	$header[HEADER_OFF_MINOR_VERSION] 	= MINOR_VERSION;		//Minor Version
	int2byte($header, $cmd, HEADER_OFF_COMMAND);				//Command
	$header[HEADER_OFF_ACTION] 			= $act;					//Action
	$header[HEADER_OFF_MSG_TYPE] 		= $type;				//Type
	$header[HEADER_OFF_ERROR_CODE]		= 0xFF;					//Error Code
	int2byte($header, $len, HEADER_OFF_MSG_LENGTH);				//Length
	str2byte($header, "127.0.0.1", HEADER_OFF_PEER_IP, 40);		//Peer IP[40]
	int2byte($header, 80, HEADER_OFF_PEER_PORT);				//Peer Port
	str2byte($header, "admin", HEADER_OFF_PEER_ACCOUNT, 16);	//Peer Account[16] - Current user name
	$header = array_merge($header, array_fill(0, 8, 0xFF));		//Reserved[8]
	
	return $header;
}

/*****************************************************************************************************************
* function    : byte2int($data, $pos)
* Description :
*****************************************************************************************************************/
function byte2int($data, $pos){
	$result = 0;
	for($i=($pos+3), $j=24; $i>=$pos; $i--,$j-=8){
		$result += $data[$i] << $j;
	}	
	$result = ($result < 0)? ($result + 4294967296) : $result;
	return $result;
}

/*****************************************************************************************************************
* function    : byte2str($data, $pos, $size)
* Description :
*****************************************************************************************************************/
function byte2str($data, $pos, $size){
	$sBuffer = "";
	for($i=0; $i<$size; $i++){
		$sBuffer .= chr($data[$pos + $i]);
	}
	return trim($sBuffer);
}

/*****************************************************************************************************************
 * function    : int2byte(&$data, $val, $pos)
* Description :
*****************************************************************************************************************/
function int2byte(&$data, $val, $pos){
	$temp = ($val < 0)? ($val + 4294967296): $val;		
	
	$data[$pos+3] = (($temp >> 24) & 0x000000FF);
	$data[$pos+2] = (($temp >> 16) & 0x0000FF);
	$data[$pos+1] = (($temp >> 8) & 0x00FF);
	$data[$pos] = ($temp & 0xFF);
}

/*****************************************************************************************************************
 * function    : str2byte(&$data, $str, $pos, $size)
* Description :
*****************************************************************************************************************/
function str2byte(&$data, $str, $pos, $size){
	for($i=0; $i<strlen($str); $i++){
		$data[$pos + $i] = ord(substr($str, $i, 1));
	}
	for($i=strlen($str); $i<$size; $i++){
		$data[$pos + $i] = 0x00;
	}
}

?>