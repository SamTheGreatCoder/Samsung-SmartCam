<?php
require_once ('./adv/_define.inc');

CheckAdminAccount(FALSE);

$PermissionValues = array(1, 2, 4, 8); // 1=>"Device", 2=>"PTZ", 4=>"Network",8=>"SDCard"

$PermissionArr = array(
	1=>"Device", 
	2=>"PTZ", 
	4=>"Network",
	8=>"SDCard"
);

function cgi_setSDKAppAttributes()
{
	$responseOutput = new ResponseOutput();
	
	if ((!isset($_REQUEST['AppID'])))
	{
		$responseOutput->errCode = STATUS_MISSING_PARAMETER;
		return $responseOutput;
	}
	
	if((!isset($_REQUEST['Priority'])) && (!isset($_REQUEST['AutoStart'])))
	{
		$responseOutput->errCode = STATUS_MISSING_PARAMETER;
		return $responseOutput;
	}
	
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
	$getTargetClass->dataInfo['AppName']['value'] = $_REQUEST['AppID'];
	$getTargetClass->payload = MakePayload($getTargetClass->dataInfo);
	$socketManager = new SocketManager();
	$socketManager->Connection($getTargetClass);
	
	//print_r($getTargetClass->sdk_app_attributes_result->dataInfo);
	
	//setting app info
	$targetClass = NULL;
	$msg = 'hello';
	$targetClass = new SDK_App_Attributes(ACTION_SET);
	$targetClass->headerInfo['Action'] = ACTION_SET;
	$targetClass->dataInfo['AppName']['value'] = $_REQUEST['AppID'];
	
	if((isset($_REQUEST['AutoStart']))){
		if(($_REQUEST['AutoStart'] == 'True') || ($_REQUEST['AutoStart'] == 'False')){
			$targetClass->dataInfo['IsAutoStart']['value'] = $AutoStart[$_REQUEST['AutoStart']]; 
		}
		else{
			$responseOutput->errCode = STATUS_INVALID_VALUE;
			return $responseOutput;
		}
	}else{
		$targetClass->dataInfo['IsAutoStart']['value']=$getTargetClass->sdk_app_attributes_result->dataInfo['app_is_auto_start']['value'];
	}
	if((isset($_REQUEST['Priority']))){ 
		if(($_REQUEST['Priority'] == 'High') || ($_REQUEST['Priority'] == 'Medium') || ($_REQUEST['Priority'] == 'Low')){
			$targetClass->dataInfo['Priority']['value'] = $Priority[$_REQUEST['Priority']]; 
		}
		else{
			$responseOutput->errCode = STATUS_INVALID_VALUE;
			return $responseOutput;
		}
	}else{
		$targetClass->dataInfo['Priority']['value']=$getTargetClass->sdk_app_attributes_result->dataInfo['app_priority']['value'];
	}
	
	$targetClass->payload = MakePayload($targetClass->dataInfo);
	$socketManager = new SocketManager();
	$socketManager->Connection($targetClass);
	
	$responseOutput->errCode = STATUS_OK;
	$responseOutput->outputMsg = 'OK';
	return $responseOutput;
}

function cgi_controlSDKAPP()
{
	$responseOutput = new ResponseOutput();
	
	if ((!isset($_REQUEST['AppID'])))
	{
		$responseOutput->errCode = STATUS_MISSING_PARAMETER;
		return $responseOutput;
	}
	if ((!isset($_REQUEST['Mode'])))
	{
		$responseOutput->errCode = STATUS_MISSING_PARAMETER;
		return $responseOutput;
	}

	require_once('./adv/sdk.class');
	$targetClass	= NULL;
	$msg = 'hello';
	if($_REQUEST['Mode'] == 'Start')
	{
		$targetClass = new SDK(ACTION_START);
		$targetClass->headerInfo['Action']	= ACTION_START;
		$targetClass->dataInfo['AppName']['value']	= $_REQUEST['AppID'];
		$targetClass->payload 	= MakePayload($targetClass->dataInfo);
		$socketManager	= new SocketManager();
		$socketManager->Connection($targetClass);
	}
	else if($_REQUEST['Mode'] == 'Stop')
	{
		$targetClass = new SDK(ACTION_STOP);
		$targetClass->headerInfo['Action'] = ACTION_STOP;
		$targetClass->dataInfo['AppName']['value'] = $_REQUEST['AppID'];
		$targetClass->payload = MakePayload($targetClass->dataInfo);
		$socketManager = new SocketManager();
		$socketManager->Connection($targetClass);
	}
	else
	{
		$responseOutput->errCode = STATUS_INVALID_VALUE;
		return $responseOutput;
	}
	
	$responseOutput->errCode = STATUS_OK;
	$responseOutput->outputMsg = 'OK';
	return $responseOutput;
}

function cgi_installSDKAPP()
{
	$responseOutput = new ResponseOutput();
	
	$socket = new SocketManager();
	
	$installType=array(
					0 => "New",
					1 => "Upgrade"
				);
	
	if (!isset($_REQUEST['AppID']))
	{
		$responseOutput->errCode = STATUS_MISSING_PARAMETER;
		return $responseOutput;
	}

	$License_Name	= $_FILES['LicenseFile']['name'];
	$License_Size	= $_FILES['LicenseFile']['size'];
	
	if (strlen($License_Name) != 0 && $License_Size != 0) 
	{
		$App_Name		= substr($License_Name, 0, -4);

		$Target_Directory = $GLOBALS['SDK_APP_DOWNLOAD_DIRECTORY'].$License_Name;
		
		if (@move_uploaded_file($_FILES['LicenseFile']['tmp_name'], $Target_Directory )) 
		{
			try
			{
				$fd	= fopen($Target_Directory, "r");
				$licenseContents = "";
				while($line = fgets($fd, 1024))
				{
					$line = str_replace('&', '&amp;', $line);
					$line = str_replace('"', '&quot;', $line);
					$line = str_replace("'", '&apos;', $line);
					$line = str_replace('<', '&lt;', $line);
					$line = str_replace('>', '&gt;', $line);
					$licenseContents .= $line;
				}
			}
			catch (Exception $e)
			{
				$responseOutput->errCode = STATUS_UNKNOWN_ERROR;
				SendResponse($responseOutput);
			}

			$FILE_PATH = $GLOBALS['SDK_APP_INSTALL_DIRECTORY'].$_REQUEST['AppID']."/".$GLOBALS['SDK_APP_CONFIG_FILE'];
			try
			{
				$manifestXml = new SimpleXMLElement($FILE_PATH, NULL, TRUE);
			}
			catch (Exception $e)
			{
				$responseOutput->errCode = STATUS_UNKNOWN_ERROR;
				SendResponse($responseOutput);
			}

			$old_license	= $manifestXml->xpath('//license');
			// Remove old license
			if($old_license)
			{
				unset($old_license[0]->{0});
			}
			$manifestXml->addChild('license', $licenseContents);
			
			$XML_FILE_STRING = $manifestXml;
			$manifestXml->asXML($FILE_PATH);
			unlink($Target_Directory); // Delete uploaded file
			$responseOutput->errCode = STATUS_OK;
			$responseOutput->outputMsg = 'OK';

			require_once('./adv/sdk.class');
			$targetClass	= new SDK_App_license(ACTION_SET);
			$targetClass->headerInfo['Action'] = ACTION_SET;
			$targetClass->dataInfo['AppName']['value'] = $_REQUEST['AppID'];
			$targetClass->payload = MakePayload($targetClass->dataInfo);
			$socketManager	= new SocketManager();
			$socketManager->Connection($targetClass);

			return $responseOutput;
		}
		else
		{
			$responseOutput->errCode = STATUS_INVALID_FILE;
			return $responseOutput;
		}
	}
	
	require_once ('./adv/sdk.class');
	$cookie_name = 'AppInstallSessionID';
	
	if(!isset($_COOKIE[$cookie_name]))
	{
		$Cap_Name = $_FILES['UploadedFile']['name'];
		$Cap_Size = $_FILES['UploadedFile']['size'];

		$App_Name =  substr($Cap_Name, 0, -4); // Remove file extention
		error_log($Cap_Size, 0);
		$allowedExts = "cap";
		$extension = end(explode(".", $_FILES["UploadedFile"]["name"]));
		error_log($extension, 0);

		if($_REQUEST['AppID'] != $App_Name)
		{
			$responseOutput->errCode = STATUS_INVALID_VALUE;
			return $responseOutput;
		}

		$Target_Directory = $GLOBALS['SDK_APP_DOWNLOAD_DIRECTORY'].$Cap_Name;

		if (strlen($App_Name) == 0) {
			$responseOutput->errCode = STATUS_INVALID_FILE;
			return $responseOutput;
		} else {
			if($Cap_Size == 0) {
				$responseOutput->errCode = STATUS_INVALID_FILE;
				return $responseOutput;
			}
			if (($extension != $allowedExts) && $errorStatus == 0) {
				$responseOutput->errCode = STATUS_INVALID_FILE;
				return $responseOutput;
			}
		}
	
		if (@move_uploaded_file($_FILES['UploadedFile']['tmp_name'], $Target_Directory )) 
		{
			// The code line below was initially from webviewer but seems this does nothing actually.
			//unlink($_FILES['UploadedFile']['tmp_name']);
			$cookie_value = $App_Name . '-' . $_SERVER['REMOTE_ADDR'];

			setcookie($cookie_name, $cookie_value); // set cookie
			
			$targetClass = new SDK(ACTION_ADD);
			$targetClass->headerInfo['Action'] = ACTION_ADD;
			$targetClass->dataInfo['AppName']['value'] = $App_Name;
			$targetClass->dataInfo['AppUploadPath']['value'] = $GLOBALS['SDK_APP_DOWNLOAD_DIRECTORY'];
			$targetClass->payload = MakePayload($targetClass->dataInfo);
			$socket->Connection($targetClass);

			global $PermissionValues;
			global $PermissionArr;

			$msg = 'Permission=';

			$permRes = "";
			foreach($PermissionValues as $value)
			{
				$res = $value & $targetClass->sdk_app_upload_response->dataInfo['app_permissions']['value'];

				if($res != 0)
					$permRes .= $PermissionArr[$value] . ',';
			}

			if($permRes != "")
				$msg .= rtrim($permRes, ",") . "\r\n";
			else
				$msg .= 'None' . "\r\n";

			$msg .= 'InstallType=' . $installType[$targetClass->sdk_app_upload_response->dataInfo['app_upgrade']['value']];

			$responseOutput->outputMsg .= $msg;
		}
	}
	else // second session
	{
		$cookie_value = explode('-', $_COOKIE[$cookie_name]);
		if($_REQUEST['AppID'] != $cookie_value[0] || $_SERVER['REMOTE_ADDR'] != $cookie_value[1])
		{
			$responseOutput->errCode = STATUS_INVALID_VALUE;
			return $responseOutput;
		}
		
		$targetClass = new SDK(ACTION_SET);
		$targetClass->headerInfo['Action'] = ACTION_SET;
		$targetClass->dataInfo['AppName']['value'] = $_REQUEST['AppID'];
		
		if(isset($_REQUEST['KeepOldSettings']))
		{
			if($_REQUEST['KeepOldSettings'] == "True")
				$targetClass->dataInfo['RetainSettings']['value'] = "1";
			else if($_REQUEST['KeepOldSettings'] == "False")
				$targetClass->dataInfo['RetainSettings']['value'] = "0";
			else
			{
				$responseOutput->errCode = STATUS_INVALID_VALUE;
				return $responseOutput;
			}
		}
		
		$targetClass->payload = MakePayload($targetClass->dataInfo);
		$socket->Connection($targetClass);

		setcookie($cookie_name, "", time() - 3600); // delete cookie

		$responseOutput->outputMsg = 'OK';
	}
	
	$responseOutput->errCode = STATUS_OK;
	return $responseOutput;
}

function cgi_removeSDKAPP()
{
	$responseOutput = new ResponseOutput();
	
	if ((!isset($_REQUEST['AppID'])))
	{
		$responseOutput->errCode = STATUS_MISSING_PARAMETER;
		return $responseOutput;
	}
	
	require_once ('./adv/sdk.class');
	$targetClass = NULL;
	$msg = 'hello';
	$targetClass = new SDK(ACTION_REMOVE);
	$targetClass->headerInfo['Action'] = ACTION_REMOVE;
	$targetClass->dataInfo['AppName']['value'] = $_REQUEST['AppID'];
	$targetClass->payload = MakePayload($targetClass->dataInfo);
	$socketManager = new SocketManager();
	$socketManager->Connection($targetClass);

	$responseOutput->errCode = STATUS_OK;
	$responseOutput->outputMsg = 'OK';
	return $responseOutput;
}

function cgi_getIPCameraManifest(){
	$responseOutput = new ResponseOutput();
	
	if ((!isset($_REQUEST['AppID'])))
	{
		$responseOutput->errCode = STATUS_MISSING_PARAMETER;
		SendResponse($responseOutput);
	}
	
	$APP_NAME=$_REQUEST['AppID'];
	
	$FILE_PATH = $GLOBALS['SDK_APP_INSTALL_DIRECTORY'].$APP_NAME."/".$GLOBALS['SDK_APP_CONFIG_FILE'];
	
	if (file_exists($FILE_PATH))
	{
		try
		{
			$xmlToObject = new SimpleXMLElement($FILE_PATH, NULL, TRUE);
		}
		catch (Exception $e)
		{
			$responseOutput->errCode = STATUS_UNKNOWN_ERROR;
			SendResponse($responseOutput);
		}
	}
	else
	{
		$responseOutput->errCode = STATUS_UNKNOWN_ERROR;
		SendResponse($responseOutput);
	}
	
	$XML_FILE_STRING = $xmlToObject->asXML();
	
	$responseOutput->errCode = STATUS_OK;
	$responseOutput->outputMsg = $XML_FILE_STRING;
	SendResponse($responseOutput, 2);
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

function cgi_getApplicationStatus()
{
	$responseOutput = new ResponseOutput();
	
	if(isset($_REQUEST['Check']) && $_REQUEST['Check'] != 'Once')
	{
		$responseOutput->errCode = STATUS_INVALID_VALUE;
		return $responseOutput;
	}
	
	if(isset($_REQUEST['Periodicity']))
	{
		$responseOutput->errCode = STATUS_INVALID_PARAMETER;
		return $responseOutput;
	}
	
	require_once ('./adv/sdk.class');
	$targetClass = NULL;
	
	$targetClass = new SDK_Task_Manager(ACTION_GET);
	$targetClass->headerInfo['Action'] = ACTION_GET;
	$socketManager = new SocketManager();
	$socketManager->Connection($targetClass);
	
	$msg = "";
	$app_cnt = $targetClass->dataInfo['max_apps_count']['value'];

	$msg .= 'TotalCPUUsage=' . $targetClass->dataInfo['sys_cpu']['value'] . "\r\n";
	$msg .= 'TotalMemoryUsage=' . $targetClass->dataInfo['sys_memory']['value'] . "\r\n";
	
	if (isset($_REQUEST['AppID']))
	{
		$apps = explode(',', trim($_REQUEST['AppID']));
		
		for ($i=0; $i < sizeof($apps); $i++)
		{
			$value_chk = 1;

			for ($j=0; $j < $app_cnt; $j++)
			{
				if(trim($apps[$i])==trim($targetClass->sdk_taskManager[$j]->dataInfo['app_name']['value'])) 
				{
					$app_name = $targetClass->sdk_taskManager[$j]->dataInfo['app_name']['value'];
					$app_cpu_usage_percent = $targetClass->sdk_taskManager[$j]->dataInfo['app_cpu_usage_percent']['value'];
					$app_mem_usage_percent = $targetClass->sdk_taskManager[$j]->dataInfo['app_mem_usage_percent']['value'];
					$threads_count = $targetClass->sdk_taskManager[$j]->dataInfo['threads_count']['value'];
					$running_duration_secs = $targetClass->sdk_taskManager[$j]->dataInfo['running_duration_secs']['value'];
					
					$msg .= stripslashes(trim($app_name)) . '.CPUUsage=' . $app_cpu_usage_percent . "\r\n";
					$msg .= stripslashes(trim($app_name)) . '.MemoryUsage=' . $app_mem_usage_percent . "\r\n";
					$msg .= stripslashes(trim($app_name)) . '.ThreadsCount=' . $threads_count . "\r\n";
					//$msg .= stripslashes(trim($app_name)) . '.ConcurrentUserCount=' . "\r\n";
					$msg .= stripslashes(trim($app_name)) . '.Duration=' . durationFormatting($running_duration_secs) . "\r\n";
					
					$value_chk = 0;
					break;
				}
			}
			
			if($value_chk)
			{
				$responseOutput->errCode = STATUS_INVALID_VALUE;
				return $responseOutput;
			}
		}
	}
	else
	{
		for ($index=0; $index < $app_cnt; $index++)
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
		}
	}
	
	if($msg == "")
	{
		$responseOutput->errCode = STATUS_UNKNOWN_ERROR;
		return $responseOutput;
	}
	
	$responseOutput->errCode = STATUS_OK;
	$responseOutput->outputMsg = $msg;
	return $responseOutput;
}

function ref_getApplicationStatus($AppName, $boundary)
{
	require_once ('./adv/sdk.class');
	$targetClass = NULL;
	
	$targetClass = new SDK_Task_Manager(ACTION_GET);
	$targetClass->headerInfo['Action'] = ACTION_GET;
	$socketManager = new SocketManager();
	$socketManager->Connection($targetClass);
	
	$msg = "";
	$app_cnt = $targetClass->dataInfo['max_apps_count']['value'];

	$msg .= 'TotalCPUUsage=' . $targetClass->dataInfo['sys_cpu']['value'] . "\r\n";
	$msg .= 'TotalMemoryUsage=' . $targetClass->dataInfo['sys_memory']['value'] . "\r\n";
	
	if (isset($_REQUEST['AppID']))
	{
		$apps = explode(',', trim($AppName));
		
		for ($i=0; $i < sizeof($apps); $i++)
		{
			$value_chk = 1;

			for ($j=0; $j < $app_cnt; $j++)
			{
				if(trim($apps[$i])==trim($targetClass->sdk_taskManager[$j]->dataInfo['app_name']['value'])) 
				{
					$app_name = $targetClass->sdk_taskManager[$j]->dataInfo['app_name']['value'];
					$app_cpu_usage_percent = $targetClass->sdk_taskManager[$j]->dataInfo['app_cpu_usage_percent']['value'];
					$app_mem_usage_percent = $targetClass->sdk_taskManager[$j]->dataInfo['app_mem_usage_percent']['value'];
					$threads_count = $targetClass->sdk_taskManager[$j]->dataInfo['threads_count']['value'];
					$running_duration_secs = $targetClass->sdk_taskManager[$j]->dataInfo['running_duration_secs']['value'];

					$msg .= stripslashes(trim($app_name)) . '.CPUUsage=' . $app_cpu_usage_percent . "\r\n";
					$msg .= stripslashes(trim($app_name)) . '.MemoryUsage=' . $app_mem_usage_percent . "\r\n";
					$msg .= stripslashes(trim($app_name)) . '.ThreadsCount=' . $threads_count . "\r\n";
					//$msg .= stripslashes(trim($app_name)) . '.ConcurrentUserCount=' . "\r\n";
					$msg .= stripslashes(trim($app_name)) . '.Duration=' . durationFormatting($running_duration_secs) . "\r\n";
					
					$value_chk = 0;
					break;
				}
			}
			
			if($value_chk)
			{
				$responseOutput = new ResponseOutput();
				$responseOutput->errCode = STATUS_INVALID_VALUE;
				SendResponse($responseOutput, 3, $boundary);
			}
		}
	}
	else
	{
		for ($index=0; $index < $app_cnt; $index++)
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
		}
	}
	
	if($msg == "")
	{
		$responseOutput = new ResponseOutput();
		$responseOutput->errCode = STATUS_UNKNOWN_ERROR;
		SendResponse($responseOutput, 3, $boundary);
	}
	
	return $msg;
}

function cgi_getPeriodicity()
{
	$regexp = "/^[\d]$/";
	$periode = 1;
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
	
	if(preg_match($regexp, $periode))
	{
		$boundary = "SamsungTechwin";
		header("Content-Type: multipart/x-mixed-replace; boundary={$boundary}");
		echo "\r\n--{$boundary}\r\n";
		
		while (1<2)
		{
			echo "Content-Type: text/plain\r\n\r\n";
			echo ref_getApplicationStatus($_REQUEST['AppID'], $boundary);
			echo "\r\n--{$boundary}\r\n";
			
			flush();
			ob_flush();		
			
			sleep($periode);
		}
	}
	else
	{
		$responseOutput = new ResponseOutput();
		$responseOutput->errCode = STATUS_INVALID_VALUE;
		SendResponse($responseOutput);
	}
}

function cgi_viewSDKAPP()
{
	$responseOutput = new ResponseOutput();

	require_once ('./adv/sdk.class');
	$targetClass = NULL;

	$targetClass = new SDKInfoRequest();
	$socketManager = new SocketManager();
	$socketManager->Connection($targetClass);

	$AutoStartArr=array(
		1=>"True",
		0=>"False"
	);

	$PriorityArr=array(
		0=>"Low",
		1=>"Medium",
		2=>"High"
	);
	
	$SDK_APP_STATUS_CODES_MAP = array(
		-1 => "InstallFailed",
		0 	=> "Uninstalled",
		1 	=> "Uninstalling",
		2 	=> "Installed",
		3 	=> "Installing",
		4 	=> "StartedNotRunning",
		5 	=> "Running",
		6 	=> "Stopped"
	);
	
	global $PermissionValues;
	global $PermissionArr;

	$msg = 'InstalledApps=';
	$msg .= $targetClass->dataInfo['max_apps_count']['value'] . "\r\n";
	
	for ($index=0; $index < $targetClass->dataInfo['max_apps_count']['value']; $index++) 
	{
		$AppStatus_Val = $targetClass->sdk_app[$index]->dataInfo['app_status']['value'];
		$Raw_AppName = $targetClass->sdk_app[$index]->dataInfo['app_name']['value'];
		$AppName = $Raw_AppName;
		$InstalledDate = $targetClass->sdk_app[$index]->dataInfo['installed_date']['value'];
		$Version = $targetClass->sdk_app[$index]->dataInfo['app_version']['value'];
		$Version = trim($Version);
		$Priority =  $PriorityArr[$targetClass->sdk_app[$index]->dataInfo['app_priority']['value']];
		$Permission =  $targetClass->sdk_app[$index]->dataInfo['app_permissions']['value'];
		$AutoStart = $AutoStartArr[$targetClass->sdk_app[$index]->dataInfo['app_is_auto_start']['value']];

		$msg .= stripslashes(trim($Raw_AppName)) . '.Status=' . $SDK_APP_STATUS_CODES_MAP[$AppStatus_Val] . "\r\n";
		$msg .= stripslashes(trim($Raw_AppName)) . '.InstalledDate=' . strftime('%Y-%m-%dT%TZ', strtotime(stripslashes(trim($InstalledDate)))) . "\r\n";
		$msg .= stripslashes(trim($Raw_AppName)) . '.Version=' . $Version . "\r\n";
		$msg .= stripslashes(trim($Raw_AppName)) . '.Permission=';
		
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
		
		$msg .= stripslashes(trim($Raw_AppName)) . '.AutoStart=' . $AutoStart . "\r\n";
		$msg .= stripslashes(trim($Raw_AppName)) . '.Priority=' . $Priority . "\r\n";
	}
	
	$responseOutput->errCode = STATUS_OK;
	$responseOutput->outputMsg = $msg;
	
	return $responseOutput;
}

$responseOutput = new ResponseOutput();
switch(@$_REQUEST['msubmenu']) {
	case 'apps': {
		switch(@$_REQUEST['action']) {
			case 'view': {
				SendResponse(cgi_viewSDKAPP());
			} break;
			case 'set': {
				SendResponse(cgi_setSDKAppAttributes());
			} break;
			case 'control': {
				SendResponse(cgi_controlSDKAPP());
			} break;
			case 'install': {
				SendResponse(cgi_installSDKAPP());
			} break;
			case 'remove': {
				SendResponse(cgi_removeSDKAPP());
			} break;
			default: {
				$responseOutput->errCode = STATUS_ACTION_NOT_FOUND;
				SendResponse($responseOutput);
			} break;
		}
	} break;	
	case 'appstatus': {
		switch(@$_REQUEST['action']) {
			case 'view': {
				if(isset($_REQUEST['Check']) && $_REQUEST['Check'] == 'Periodically')
				{
					cgi_getPeriodicity();
				}
				else
				{
					SendResponse(cgi_getApplicationStatus());
				}
			} break;
			default: {
				$responseOutput->errCode = STATUS_ACTION_NOT_FOUND;
				SendResponse($responseOutput);
			} break;
		}
	} break;
	case 'manifest': {
		switch(@$_REQUEST['action']) {
			case 'view': {
				//Show IPCameraManifest.xml
				cgi_getIPCameraManifest();
			}break;
			default: {
				$responseOutput->errCode = STATUS_ACTION_NOT_FOUND;
				SendResponse($responseOutput);
			} break;
		}
	} break;
	case 'appconfig': {
		$responseOutput->errCode = STATUS_NOT_IMPLEMENTED;
		SendResponse($responseOutput);
	} break;
	default: {
			$responseOutput->errCode = STATUS_SUBMENU_NOT_FOUND;
			SendResponse($responseOutput);
	} break;
}

?>
