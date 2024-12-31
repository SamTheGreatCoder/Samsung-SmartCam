<?php
require_once ('./adv/_define.inc');
CheckAdminAccount(FALSE);
// reset
//http://107.108.58.32/cgi-bin/opensdk.cgi?msubmenu=debug&enable=1
function cgi_debug()
{
	if ((!isset($_REQUEST['enable'])) || (!isset($_REQUEST['port'])) || (!isset($_REQUEST['name'])) )	return FALSE;
	
	if ($_REQUEST['enable'] != 1 && $_REQUEST['enable'] != 0)	return FALSE;

	$debugConf = NULL;
	require_once ('./adv/sdk.class');
	
		$debugConf = new SDK_DebugConfig();
		$debugConf->dataInfo['enable']['value'] = $_REQUEST['enable'];
		$debugConf->dataInfo['viewer_ip']['value'] = $_SERVER['REMOTE_ADDR'];
		$debugConf->dataInfo['viewer_port']['value'] = $_REQUEST['port'];
		$debugConf->dataInfo['app_name']['value'] = $_REQUEST['name'];

	$debugConf->payload = MakePayload($debugConf->dataInfo);
	$socketManager = new SocketManager();
	$socketManager->Connection($debugConf);
	
	//socketListen();
	
	return TRUE;
}

function socketListen(){
	if (($sock = socket_create(AF_INET,SOCK_STREAM,SOL_TCP)) === false) {
		echo "socket_create() failed: reason: " . socket_strerror(socket_last_error()) . "\n";
		exit;
	}
	
	if (!socket_set_option($sock, SOL_SOCKET, SO_REUSEADDR, 1)) { 
		echo "socket_strerror() failed: reason: " .socket_strerror(socket_last_error($sock)); 
		exit; 
	}
	if (!socket_set_nonblock($sock)) { 
		echo "socket_set_nonblock() failed: reason: " . socket_strerror(socket_last_error($sock)); 
		exit; 
	}
	
	
	
	$port=$_REQUEST['port'];
	if (socket_bind($sock, "0.0.0.0", $port) === false) {
		echo "socket_bind() failed: reason: " . socket_strerror(socket_last_error($sock)) . "\n";
		exit;
	}
	
	if (socket_listen($sock,5) === false) {
		echo "socket_listen() falló: razón: " . socket_strerror(socket_last_error($sock)) . "\n";
		exit;
	}
	while (true) 
    { 
        $connection = @socket_accept($sock); 
        if ($connection === false) 
        { 
            usleep(100); 
        }elseif ($connection > 0) 
        { 
            print_r($sock);
            print_r($connection);
	}else 
        { 
            echo "error: ".socket_strerror($connection); 
            die; 
        } 
    } 
 
	
		/*while(true)
		{
				echo "Client $newc has connected\n";
				echo $clients[] = $newc;
		}*/
	
	
	/*$socket = stream_socket_server("tcp://127.0.0.1:1234", $errno, $errstr);
if (!$socket) {
  echo "$errstr ($errno)<br />\n";
} else {
	while ($conn = stream_socket_accept($socket)) {
		echo $conn;
		fclose($conn);
	}
	fclose($socket);
}
	
	while(true)
	{
		if(($newc = socket_accept($socket)) !== false)
		{
			echo "Client $newc has connected\n";
			$clients[] = $newc;
		}
	}
	
	$socket = stream_socket_server("udp://127.0.0.1:1113", $errno, $errstr, STREAM_SERVER_BIND);
	if (!$socket) {
		die("$errstr ($errno)");
	}
	
	do {
		$pkt = stream_socket_recvfrom($socket, 1, 0, $peer);
		echo "$peer\n";
	} while ($pkt !== false); */
	
	
	
	/*header("Content-type: text/x-mixed-replace; boundary=$boundary");
	do {
		//echo date('h:i:s');
		print_r($sock);
	}while (true); */
	
}

function cgi_setSDKAppAttributes()
{

	if ((!isset($_REQUEST['AppName'])))	return FALSE;
	
	if((!isset($_REQUEST['Priority'])) && (!isset($_REQUEST['AutoStart']))) return FALSE;
	
	$AutoStart=array(
					"True"=>1,
					"False"=>0
					);
					
	$Priority=array(
					"Low"=>0,
					"Medium"=>1,
					"High"=>2
					);
	
	require_once ('./adv/sdk.class');
	
	//getting app info
	$getTargetClass = NULL;
	 $getTargetClass = new SDK_App_Attributes(ACTION_GET);
	$getTargetClass->dataInfo['AppName']['value'] = $_REQUEST['AppName'];
	$getTargetClass->payload = MakePayload($getTargetClass->dataInfo);
	$socketManager = new SocketManager();
    $socketManager->Connection($getTargetClass);
	
	//print_r($getTargetClass->sdk_app_attributes_result->dataInfo);
	
	//setting app info
	$targetClass = NULL;
	$msg = 'hello';
    $targetClass = new SDK_App_Attributes(ACTION_SET);
    $targetClass->headerInfo['Action'] = ACTION_SET;
	$targetClass->dataInfo['AppName']['value'] = $_REQUEST['AppName'];
	
	if((isset($_REQUEST['AutoStart']))){
		if(($_REQUEST['AutoStart'] == 'True') || ($_REQUEST['AutoStart'] == 'False')){
			$targetClass->dataInfo['IsAutoStart']['value'] = $AutoStart[$_REQUEST['AutoStart']]; 
		}
		else{
			return FALSE;
		}
	}else{
		$targetClass->dataInfo['IsAutoStart']['value']=$getTargetClass->sdk_app_attributes_result->dataInfo['app_is_auto_start']['value'];
	}
	if((isset($_REQUEST['Priority']))){ 
		if(($_REQUEST['Priority'] == 'High') || ($_REQUEST['Priority'] == 'Medium') || ($_REQUEST['Priority'] == 'Low')){
			$targetClass->dataInfo['Priority']['value'] = $Priority[$_REQUEST['Priority']]; 
		}
		else{
			return FALSE;
		}
	}else{
		$targetClass->dataInfo['Priority']['value']=$getTargetClass->sdk_app_attributes_result->dataInfo['app_priority']['value'];
	}
	//print_r($targetClass->dataInfo);
	$targetClass->payload = MakePayload($targetClass->dataInfo);
	$socketManager = new SocketManager();
	$socketManager->Connection($targetClass);
	return TRUE;
}

function cgi_controlSDKAPP()
{
	if ((!isset($_REQUEST['AppName'])))	return FALSE;
	if ((!isset($_REQUEST['Mode'])))	return FALSE;

	require_once('./adv/sdk.class');
	$targetClass	= NULL;
	$msg = 'hello';
	if($_REQUEST['Mode'] == 'Start')
	{
		$targetClass	= new SDK(ACTION_START);
		$targetClass->headerInfo['Action']	= ACTION_START;
		$targetClass->dataInfo['AppName']['value']	= $_REQUEST['AppName'];
		$targetClass->payload 	= MakePayload($targetClass->dataInfo);
		$socketManager	= new SocketManager();
		$socketManager->Connection($targetClass);
	}
	else if($_REQUEST['Mode'] == 'Stop')
	{
		$targetClass = new SDK(ACTION_STOP);
		$targetClass->headerInfo['Action'] = ACTION_STOP;
		$targetClass->dataInfo['AppName']['value'] = $_REQUEST['AppName'];
		$targetClass->payload = MakePayload($targetClass->dataInfo);
		$socketManager = new SocketManager();
		$socketManager->Connection($targetClass);
	}
	else
	{
		return FALSE;
	}
	return TRUE;
}

function cgi_removeSDKAPP()
{
	if ((!isset($_REQUEST['AppName'])))	return FALSE;
	
	require_once ('./adv/sdk.class');
    $targetClass = NULL;
	$msg = 'hello';
    $targetClass = new SDK(ACTION_REMOVE);
    $targetClass->headerInfo['Action'] = ACTION_REMOVE;
    $targetClass->dataInfo['AppName']['value'] = $_REQUEST['AppName'];
	$targetClass->payload = MakePayload($targetClass->dataInfo);
	$socketManager = new SocketManager();
	$socketManager->Connection($targetClass);

	return TRUE;
}

function cgi_getIPCameraManifest(){
	
	if ((!isset($_REQUEST['AppName'])))	return FALSE;
	
	
	$APP_NAME=$_REQUEST['AppName'];
	
	$FILE_PATH = $GLOBALS['SDK_APP_INSTALL_DIRECTORY'].$APP_NAME."/".$GLOBALS['SDK_APP_CONFIG_FILE'];
	
	//echo $FILE_PATH;
	
	if (file_exists($FILE_PATH))
	{
		try
		{
			$xmlToObject = new SimpleXMLElement($FILE_PATH, NULL, TRUE);
		}
		catch (Exception $e)
		{
          	$msg = '<?xml version="1.0" encoding="utf-8" ?>'."\n";
          	$msg .= '<Error>'."\n";
          	$msg .= '<ErrorString>';
          	$msg .= "ERROR: Failed to Create File object!";
          	$msg .= '</ErrorString>'."\n";
          	$msg .= '</Error>'."\n";
          	header('Content-Type: text/xml; charset=utf-8');
          	header('Content-Length: '.strlen($msg));
          	echo $msg;
			exit;
		}
	}
	else
	{
		$msg = '<?xml version="1.0" encoding="utf-8" ?>'."\n";
		$msg .= '<Error>'."\n";
		$msg .= '<ErrorString>';
		$msg .= "ERROR: Configuration file not found!";
		$msg .= '</ErrorString>'."\n";
		$msg .= '</Error>'."\n";
		header('Content-Type: text/xml; charset=utf-8');
		header('Content-Length: '.strlen($msg));
		echo $msg;
		exit;
	}
	
	
		$XML_FILE_STRING = $xmlToObject->asXML();
		
		header('Content-Type: text/xml; charset=utf-8');
		header('Content-Length: '.strlen($XML_FILE_STRING));
		echo $XML_FILE_STRING;
	
}

function durationFormatting($secs)
{
	$dur_dt = array();
	
	$dur_dt["y"] =  floor($secs / (60*60*24*365));
	$remain_secs = $secs - ($dur_dt["y"] * (60*60*24*365));
	$dur_dt["m"] =  floor($remain_secs / (60*60*24*30));
	$remain_secs -= ($dur_dt["m"] * (60*60*24*30));
	$dur_dt["d"] =  floor($remain_secs / (60*60*24));
	$remain_secs -= ($dur_dt["d"] * (60*60*24));
	$dur_dt["h"] =  floor($remain_secs / (60*60));
	$remain_secs -= ($dur_dt["h"] * (60*60));
	$dur_dt["i"] = floor($remain_secs / 60);
	$dur_dt["s"] =  $remain_secs - ($dur_dt["i"] * 60);

	$dur = 'P' . $dur_dt["y"] . 'Y' . $dur_dt["m"] . 'M' . $dur_dt["d"] . 'DT'
			. $dur_dt["h"] . 'H' . $dur_dt["i"] . 'M' . $dur_dt["s"] . 'S';
	
	return $dur;
}

function cgi_getApplicationStatus(){
	
	if ((!isset($_REQUEST['AppName'])))	return FALSE;
	if (isset($_REQUEST['Check']) && $_REQUEST['Check'] != 'Once')
		return FALSE;

	if(isset($_REQUEST['Periodicity']))	return FALSE;
	
	require_once ('./adv/sdk.class');
    $targetClass = NULL;
    	
	$targetClass = new SDK_Task_Manager(ACTION_GET);
	$targetClass->headerInfo['Action'] = ACTION_GET;
	$socketManager = new SocketManager();
	$socketManager->Connection($targetClass);
	//$targetClass->SendResponse();
	$msg="";
	$app_cnt = $targetClass->dataInfo['max_apps_count']['value'];
	$msg .= 'TotalCPUUsage=' . $targetClass->dataInfo['sys_cpu']['value'] . "\r\n";
	$msg .= 'TotalMemoryUsage=' . $targetClass->dataInfo['sys_memory']['value'] . "\r\n";
	
	//$msg .= '<AppHealth>'."\n";
	for ($index=0; $index < $app_cnt; $index++)
	{
			//echo $_REQUEST['AppName']."==".$targetClass->sdk_taskManager[$index]->dataInfo['app_name']['value'];
		if(trim($_REQUEST['AppName'])==trim($targetClass->sdk_taskManager[$index]->dataInfo['app_name']['value'])) 
		{
			$app_name = $targetClass->sdk_taskManager[$index]->dataInfo['app_name']['value'];
			$app_cpu_usage_percent = $targetClass->sdk_taskManager[$index]->dataInfo['app_cpu_usage_percent']['value'];
			$app_mem_usage_percent = $targetClass->sdk_taskManager[$index]->dataInfo['app_mem_usage_percent']['value'];
			$threads_count = $targetClass->sdk_taskManager[$index]->dataInfo['threads_count']['value'];
			$running_duration_secs = $targetClass->sdk_taskManager[$index]->dataInfo['running_duration_secs']['value'];
			
			$msg .= stripslashes(trim($app_name)) . '.CPUUsage=' . $app_cpu_usage_percent . "\r\n";
			$msg .= stripslashes(trim($app_name)) . '.MemoryUsage=' . $app_mem_usage_percent . "\r\n";
			$msg .= stripslashes(trim($app_name)) . '.ThreadsCount=' . $threads_count . "\r\n";
			//$msg .= stripslashes(trim($app_name)) . '.ConcurrentUserCount=' . "\r\n";
			$msg .= stripslashes(trim($app_name)) . '.Duration=' . durationFormatting($running_duration_secs) . "\r\n";
					
			break;
		}
	}
	if($msg == "")
		return FALSE;
	else 
		return $msg;
}
function ref_getApplicationStatus($AppName, $boundary){
	require_once ('./adv/sdk.class');
   $targetClass = NULL;

	$targetClass = new SDK_Task_Manager(ACTION_GET);
	$targetClass->headerInfo['Action'] = ACTION_GET;
	$socketManager = new SocketManager();
	$socketManager->Connection($targetClass);
	//$targetClass->SendResponse();
	$msg="";
	$app_cnt = $targetClass->dataInfo['max_apps_count']['value'];
	$msg .= 'TotalCPUUsage=' . $targetClass->dataInfo['sys_cpu']['value'] . "\r\n";
	$msg .= 'TotalMemoryUsage=' . $targetClass->dataInfo['sys_memory']['value'] . "\r\n";
	
	//$msg .= '<AppHealth>'."\n";
	for ($index=0; $index < $app_cnt; $index++)
	{
		//echo $_REQUEST['AppName']."==".$targetClass->sdk_taskManager[$index]->dataInfo['app_name']['value'];
		if(trim($AppName)==trim($targetClass->sdk_taskManager[$index]->dataInfo['app_name']['value'])) 
		{
			$app_name = $targetClass->sdk_taskManager[$index]->dataInfo['app_name']['value'];
			$app_cpu_usage_percent = $targetClass->sdk_taskManager[$index]->dataInfo['app_cpu_usage_percent']['value'];
			$app_mem_usage_percent = $targetClass->sdk_taskManager[$index]->dataInfo['app_mem_usage_percent']['value'];
			$threads_count = $targetClass->sdk_taskManager[$index]->dataInfo['threads_count']['value'];
			$running_duration_secs = $targetClass->sdk_taskManager[$index]->dataInfo['running_duration_secs']['value'];
			
			$msg .= stripslashes(trim($app_name)) . '.CPUUsage=' . $app_cpu_usage_percent . "\r\n";
			$msg .= stripslashes(trim($app_name)) . '.MemoryUsage=' . $app_mem_usage_percent . "\r\n";
			$msg .= stripslashes(trim($app_name)) . '.ThreadsCount=' . $threads_count . "\r\n";
			//$msg .= stripslashes(trim($app_name)) . '.ConcurrentUserCount=' . "\r\n";
			$msg .= stripslashes(trim($app_name)) . '.Duration=' . durationFormatting($running_duration_secs) . "\r\n";
			break;
			return $msg;
		}
	}
	if($msg == "")
		return FALSE;
	else
		return $msg;
}

function cgi_getPeriodicity(){
	if ((!isset($_REQUEST['AppName'])))	return FALSE;
	$periode = 1;
	$regexp = "/^[\d]$/";
	if(isset($_REQUEST['Periodicity']))
	{
		$periode = $_REQUEST['Periodicity'];
		if($periode < 1 || !is_numeric($periode))
		{
			$responseOutput = new ResponseOutput();
			$responseOutput->errCode = STATUS_INVALID_VALUE;
			SendResponse($responseOutput);
		}
	}
	if(preg_match($regexp, $periode)){				
		$boundary = "STW_openSDK";
		header("Content-Type: multipart/x-mixed-replace; boundary={$boundary}");
		echo "\r\n--{$boundary}\r\n";
		
		while (1<2)
		{
			echo "Content-Type: text/plain\r\n\r\n";
			echo ref_getApplicationStatus($_REQUEST['AppName'], $boundary);
			echo "\r\n--{$boundary}\r\n";
			
			flush();
			ob_flush();		
			
			sleep($periode);
		}
		
	}
	else
		return FALSE;
	
}
//$timestamp=1333699439;
//echo gmdate("Y-m-d H:i:s ", $timestamp);
	
function cgi_viewSDKAPP(){
	
	require_once ('./adv/sdk.class');
    $targetClass = NULL;
	
	$targetClass = new SDKInfoRequest();
	$socketManager = new SocketManager();
	$socketManager->Connection($targetClass);
	//$targetClass->SendResponse();
	$AutoStartArr=array(
					1=>"True",
					0=>"False"
					);
					
	$PriorityArr=array(
					0=>"Low",
					1=>"Medium",
					2=>"High"
					);
	$PermissionValues	= array(1, 2, 4, 8); // 1: Device, 2: PTZ, 4:Network, 8:SDcard
	$PermissionArr = array(
		1=>"Device", 
		2=>"PTZ", 
		4=>"Network",
		8=>"SDCard"
	);
	
	$SDK_APP_STATUS_CODES_MAP = array(
		-1 => "installFailed",
		0 	=> "uninstalled",
		1 	=> "uninstalling",
		2 	=> "installed",
		3 	=> "installing",
		4 	=> "startedNotRunning",
		5 	=> "running",
		6 	=> "stopped"
	);

	$msg	= 'InstalledApps=';
	$msg	.= $targetClass->dataInfo['max_apps_count']['value']."\r\n";

	for ($index=0; $index < $targetClass->dataInfo['max_apps_count']['value']; $index++) {
		$AppStatus_Val	= $targetClass->sdk_app[$index]->dataInfo['app_status']['value'];
		$Raw_AppName	= $targetClass->sdk_app[$index]->dataInfo['app_name']['value'];
		$AppName			= $Raw_AppName;
		$InstalledDate	= $targetClass->sdk_app[$index]->dataInfo['installed_date']['value'];
		$Version			= $targetClass->sdk_app[$index]->dataInfo['app_version']['value'];
		$Version			= trim($Version);
		$Priority		=  $PriorityArr[$targetClass->sdk_app[$index]->dataInfo['app_priority']['value']];
		$AutoStart		= $AutoStartArr[$targetClass->sdk_app[$index]->dataInfo['app_is_auto_start']['value']];
		$Permission		= $targetClass->sdk_app[$index]->dataInfo['app_permissions']['value'];

		$msg	.= stripslashes(trim($Raw_AppName)).'.Status='.$SDK_APP_STATUS_CODES_MAP[$AppStatus_Val]."\r\n";
		$msg	.= stripslashes(trim($Raw_AppName)) . '.InstalledDate=' . strftime('%Y-%m-%dT%TZ', strtotime(stripslashes(trim($InstalledDate)))) . "\r\n";
		$msg	.= stripslashes(trim($Raw_AppName)) . '.Version=' . $Version . "\r\n";
		$msg	.= stripslashes(trim($Raw_AppName)) . '.Permission=';

		$permRes = "";
		foreach($PermissionValues as $value)
		{
			$res = $value & $Permission;
			
			if($res != 0)
				$permRes .= $PermissionArr[$value] . ',';
		}
		
		if($permRes != "")
			$msg .= rtrim($permRes, ",") . "\r\n";
		else
			$msg .= 'None' . "\r\n";
		
		$msg	.= stripslashes(trim($Raw_AppName)) . '.AutoStart=' . $AutoStart . "\r\n";
		$msg	.= stripslashes(trim($Raw_AppName)) . '.Priority=' . $Priority . "\r\n";
	}

	return $msg;
}

error_log("Hi i am in opensdk.cgi");
error_log("".$_SERVER['REMOTE_ADDR']);
//exit;
switch(@$_REQUEST['msubmenu']) {
	case 'debug': {
		$funcName = 'cgi_'.$_REQUEST['msubmenu'];
		error_log("Hi i am in 1 opensdk.cgi");
		ResponseText($funcName());
		//$funcName();
	} break;
	case 'apps': {
		switch(@$_REQUEST['action']) {
			case 'view': {
				//view all applications
				ResponseText(cgi_viewSDKAPP());
			}break;
			case 'set': {
				//SetSDKAppAttributes
				ResponseText(cgi_setSDKAppAttributes());
			}break;
			case 'control': {
				//StartSDK
				ResponseText(cgi_controlSDKAPP());
			}break;
			case 'install': {
				//install
			}break;
			case 'remove': {
				//RemoveSDK
				ResponseText(cgi_removeSDKAPP());
			}break;
			default: {
				return FALSE;
			}break;
		}
	} break;	
	case 'appstatus': {
		switch(@$_REQUEST['action']) {
			case 'view': {
				if(isset($_REQUEST['Check']) && $_REQUEST['Check'] == 'Periodically'){
					cgi_getPeriodicity();
				}
				else{
					ResponseText(cgi_getApplicationStatus());
				}
			}break;
			default:
			{
				return FALSE;
			}break;
		}
	} break;
	case 'manifest': {
		switch(@$_REQUEST['action']) {
			case 'view': {
				//Show IPCameraManifest.xml
				ResponseText(cgi_getIPCameraManifest());
			}break;
			default:{
				return FALSE;
			}break;
		}
	} break;
}
ResponseText(FALSE);
?>
