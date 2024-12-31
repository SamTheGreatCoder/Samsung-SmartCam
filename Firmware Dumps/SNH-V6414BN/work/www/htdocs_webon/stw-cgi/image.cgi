<?php

require_once ('./adv/_define.inc');



function getMaxWidthHeight(&$width, &$height, $in_3_mega_mode)
{
	switch ($GLOBALS['M_MAX_RESOLUTION']) {
		case MAX_3_MEGA:
			if ($in_3_mega_mode == 3) {
				$width = 2048;
				$height = 1536;
			}
			else {
				$width = 1920;
				$height = 1080;
			}
			break;
		case MAX_2_MEGA:
			$width = 1920;
			$height = 1080;
			break;
		case MAX_1_MEGA:
			$width = 1280;
			$height = 1024;
			break;
	}
}

define('TEN_THOUSAND', 10000);

function PixelToTenThounsand(&$maxCoordinate, $coordinate)
{
	$result = TEN_THOUSAND * ($coordinate - 1) / ($maxCoordinate - 1);
	return round($result);
}

function TenThounsandToPixel(&$maxCoordinate, $coordinate)
{
	if ($coordinate == 0) return 0;
	$result = (($coordinate / TEN_THOUSAND) * ($maxCoordinate - 1)) + 1;
	return round($result);
}

//////////////////////////////////////////////
// Overlay 
///////////////////////////////////////////////
function submenu_overlay()
{
	CheckAdminAccount(FALSE);
	$responseOutput = new ResponseOutput();
	global $boolArray;

	$TimeFormat = array(
		0 => 'YYYY-MM-DD',
		1 => 'MM-DD-YYYY',
		2 => 'DD-MM-YYYY'
	);
	/* $OSDColor = array(
	  0 => 'White',
	  1 => 'Red',
	  2 => 'Blue',
	  3 => 'Green',
	  4 => 'Yellow'
	  );
	  $BackgroundColor = array(
	  0 => 'White',
	  1 => 'Red',
	  2 => 'Blue',
	  3 => 'Green',
	  4 => 'Yellow'
	  );
	 */
	$FontSize = array(
		0 => 'Small',
		1 => 'Medium',
		2 => 'Large'
	);

	if ($_REQUEST['Channel'] != 0)
	{
		$responseOutput->errCode = STATUS_INVALID_VALUE;
		return $responseOutput;
	}

	$classInstances = GetClassInstance('image');

	if ($_REQUEST['action'] == 'set')
	{
		if (count($_REQUEST) < 3)
		{
			$responseOutput->errCode = STATUS_MISSING_PARAMETER;
			return $responseOutput;
		}

		$OverlayInfo = array(
			'TitleEnable' => array('target' => 'imageSpecial', 'name' => 'CamTitleMode'),
			'Title' => array('target' => 'imageSpecial', 'name' => 'CamTitle'),
			'TitlePositionX' => array('target' => 'imageSpecial', 'name' => 'CamTitlePosX'),
			'TitlePositionY' => array('target' => 'imageSpecial', 'name' => 'CamTitlePosY'),
			'TimeEnable' => array('target' => 'imageOSD', 'name' => 'DispDate'),
			'TimeFormat' => array('target' => 'imageOSD', 'name' => 'DateFormat'),
			'TimePositionX' => array('target' => 'imageOSD', 'name' => 'DatePosX'),
			'TimePositionY' => array('target' => 'imageOSD', 'name' => 'DatePosY'),
			'WeekdayEnable' => array('target' => 'imageOSD', 'name' => 'DispWeekday'),
			'FontSize' => array('target' => 'imageOSD', 'name' => 'OSDSize'),
			'CameraIDEnable' => array('target' => 'imageOSD', 'name' => 'CamIDMode'),
			'PresetNameEnable' => array('target' => 'imageOSD', 'name' => 'PresetNameDisplay'),
			'PTZPositionEnable' => array('target' => 'imageSpecial', 'name' => 'PTZPositionDisplay'),
			'AzimuthEnable' => array('target' => 'imageOSD', 'name' => 'AzimuthEnable')
		);

		foreach ($OverlayInfo as $name => $data)
		{
			if (!isset($_REQUEST[$name]))
			{
				continue;
			}

			else if ($name == 'AzimuthEnable')
			{
				if (!$GLOBALS["M_SUPPORT_AZIMUTH"])
				{
					$responseOutput->errCode = STATUS_INVALID_PARAMETER;
					return $responseOutput;
				}
				
				$newValue = array_search($_REQUEST['AzimuthEnable'], $boolArray);
				if (is_bool($newValue))
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				$classInstances['ImageSetting']->$data['target']->dataInfo[$data['name']]['value'] = $newValue;
			}
			if ($name == 'TitleEnable')
			{
				$newValue = array_search($_REQUEST['TitleEnable'], $boolArray);
				if (is_bool($newValue))
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				$classInstances['ImageSetting']->$data['target']->dataInfo[$data['name']]['value'] = $newValue;
			}
			else if ($name == 'Title')
			{
				if (isset($_REQUEST['TitleEnable']))
				{
					if ($_REQUEST['TitleEnable'] != 'True')
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				else
				{
					if ($classInstances['ImageSetting']->imageSpecial->dataInfo['CamTitleMode']['value'] != 1)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				$classInstances['ImageSetting']->$data['target']->dataInfo[$data['name']]['value'] = $_REQUEST[$name];
			}
			else if ($name == 'TitlePositionX')
			{
				if (isset($_REQUEST['TitleEnable']))
				{
					if ($_REQUEST['TitleEnable'] != 'True')
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				else
				{
					if ($classInstances['ImageSetting']->imageSpecial->dataInfo['CamTitleMode']['value'] != 1)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}

				if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ)
				{
					if ($_REQUEST[$name] < 0 || $_REQUEST[$name] > 50)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				else if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3 || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ ||  $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_HISILICON)
				{
					$max_camtitle_pos = GetCamTitlePosMax();
					if ($_REQUEST[$name] < 1 || $_REQUEST[$name] > $max_camtitle_pos[0])
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}

				$classInstances['ImageSetting']->$data['target']->dataInfo[$data['name']]['value'] = $_REQUEST[$name];
			}
			else if ($name == 'TitlePositionY')
			{
				if (isset($_REQUEST['TitleEnable']))
				{
					if ($_REQUEST['TitleEnable'] != 'True')
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				else
				{
					if ($classInstances['ImageSetting']->imageSpecial->dataInfo['CamTitleMode']['value'] != 1)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}

				if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ)
				{
					if ($_REQUEST[$name] < 0 || $_REQUEST[$name] > 17)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				else if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3 || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ ||  $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_HISILICON )
				{
					$max_camtitle_pos = GetCamTitlePosMax();
					if ($_REQUEST[$name] < 1 || $_REQUEST[$name] > $max_camtitle_pos[1])
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}

				$classInstances['ImageSetting']->$data['target']->dataInfo[$data['name']]['value'] = $_REQUEST[$name];
			}
			else if ($name == 'TimeEnable')
			{
				$newValue = array_search($_REQUEST['TimeEnable'], $boolArray);
				if (is_bool($newValue))
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				$classInstances['ImageSetting']->$data['target']->dataInfo[$data['name']]['value'] = $newValue;
			}
			else if ($name == 'TimeFormat')
			{
				if (isset($_REQUEST['TimeEnable']))
				{
					if ($_REQUEST['TimeEnable'] != 'True')
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				else
				{
					if ($classInstances['ImageSetting']->imageOSD->dataInfo['DispDate']['value'] != 1)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}

				$newValue = array_search($_REQUEST['TimeFormat'], $TimeFormat);
				if (is_bool($newValue))
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				$classInstances['ImageSetting']->$data['target']->dataInfo[$data['name']]['value'] = $newValue;
			}
			else if ($name == 'TimePositionX')
			{
				if (isset($_REQUEST['TimeEnable']))
				{
					if ($_REQUEST['TimeEnable'] != 'True')
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				else
				{
					if ($classInstances['ImageSetting']->imageOSD->dataInfo['DispDate']['value'] != 1)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}

				if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ)
				{
					if ($_REQUEST[$name] < 0 || $_REQUEST[$name] > 32)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				else if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3 || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ ||  $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_HISILICON)
				{
					$max_camtime_pos_tmp = GetCamTitlePosMax();
					$max_camtime_pos = $max_camtime_pos_tmp[0] - 18;

					if ($_REQUEST[$name] < 1 || $_REQUEST[$name] > $max_camtime_pos)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}

				$classInstances['ImageSetting']->$data['target']->dataInfo[$data['name']]['value'] = $_REQUEST[$name];
			}
			else if ($name == 'TimePositionY')
			{
				if (isset($_REQUEST['TimeEnable']))
				{
					if ($_REQUEST['TimeEnable'] != 'True')
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				else
				{
					if ($classInstances['ImageSetting']->imageOSD->dataInfo['DispDate']['value'] != 1)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}

				if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ)
				{
					if ($_REQUEST[$name] < 0 || $_REQUEST[$name] > 17)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				else if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3 || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ ||  $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_HISILICON)
				{
					$max_camtitle_pos = GetCamTitlePosMax();
					if ($_REQUEST[$name] < 1 || $_REQUEST[$name] > $max_camtitle_pos[1])
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}

				$classInstances['ImageSetting']->$data['target']->dataInfo[$data['name']]['value'] = $_REQUEST[$name];
			}
			else if ($name == 'WeekdayEnable')
			{
				if (isset($_REQUEST['TimeEnable']))
				{
					if ($_REQUEST['TimeEnable'] != 'True')
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				else
				{
					if ($classInstances['ImageSetting']->imageOSD->dataInfo['DispDate']['value'] != 1)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}

				$newValue = array_search($_REQUEST['WeekdayEnable'], $boolArray);
				if (is_bool($newValue))
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				$classInstances['ImageSetting']->$data['target']->dataInfo[$data['name']]['value'] = $newValue;
			}
			else if ($name == 'FontSize')
			{
				$newValue = array_search($_REQUEST['FontSize'], $FontSize);
				if (is_bool($newValue))
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				$classInstances['ImageSetting']->imageOSD->dataInfo['OSDSize']['value'] = $newValue;
			}
			else if ($name == 'CameraIDEnable')
			{
				$newValue = array_search($_REQUEST['CameraIDEnable'], $boolArray);
				if (is_bool($newValue))
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				$classInstances['ImageSetting']->imageOSD->dataInfo['CamIDMode']['value'] = $newValue;
			}
			else if ($name == 'PresetNameEnable')
			{
				$newValue = array_search($_REQUEST['PresetNameEnable'], $boolArray);
				if (is_bool($newValue))
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				$classInstances['ImageSetting']->imageOSD->dataInfo['PresetNameDisplay']['value'] = $newValue;
			}
			else if ($name == 'PTZPositionEnable')
			{
				$newValue = array_search($_REQUEST['PTZPositionEnable'], $boolArray);
				if (is_bool($newValue))
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				$classInstances['ImageSetting']->imageSpecial->dataInfo['PTZPositionDisplay']['value'] = $newValue;
			}
		}
		$classInstances['ImageSetting']->imageSSDR->payload = MakePayload($classInstances['ImageSetting']->imageSSDR->dataInfo);
		$classInstances['ImageSetting']->imageWhiteBalance->payload = MakePayload($classInstances['ImageSetting']->imageWhiteBalance->dataInfo);
		$classInstances['ImageSetting']->imageBackLight->payload = MakePayload($classInstances['ImageSetting']->imageBackLight->dataInfo);
		$classInstances['ImageSetting']->imageExposure->payload = MakePayload($classInstances['ImageSetting']->imageExposure->dataInfo);
		$classInstances['ImageSetting']->imageSpecial->payload = MakePayload($classInstances['ImageSetting']->imageSpecial->dataInfo);
		$classInstances['ImageSetting']->imageIR->payload = MakePayload($classInstances['ImageSetting']->imageIR->dataInfo);
		$classInstances['ImageSetting']->imageOSD->payload = MakePayload($classInstances['ImageSetting']->imageOSD->dataInfo);
		$classInstances['ImageSetting']->imageDayNightSchedule->SetPayload();
		$classInstances['ImageSetting']->imagePreset->SetPayload();
		$classInstances['ImageSetting']->imagePTZIR->payload = MakePayload($classInstances['ImageSetting']->imagePTZIR->dataInfo);
		$classInstances['ImageSetting']->imageTracking->payload = MakePayload($classInstances['ImageSetting']->imageTracking->dataInfo);
		$classInstances['ImageSetting']->headerInfo['Action'] = ACTION_SET;
		$classInstances['ImageSetting']->SetPayload();
		$GLOBALS['SOCKET_MANAGER']->Connection($classInstances['ImageSetting']);

		$responseOutput->errCode = STATUS_OK;
		$responseOutput->outputMsg .= 'OK';
		return $responseOutput;
	}
	else if ($_REQUEST['action'] == 'view')
	{
		$responseOutput->outputMsg .= 'Channel.0.TitleEnable=' . $boolArray[$classInstances['ImageSetting']->imageSpecial->dataInfo['CamTitleMode']['value']] . "\r\n";
		$responseOutput->outputMsg .= 'Channel.0.Title=' . $classInstances['ImageSetting']->imageSpecial->dataInfo['CamTitle']['value'] . "\r\n";
		$responseOutput->outputMsg .= 'Channel.0.TitlePositionX=' . $classInstances['ImageSetting']->imageSpecial->dataInfo['CamTitlePosX']['value'] . "\r\n";
		$responseOutput->outputMsg .= 'Channel.0.TitlePositionY=' . $classInstances['ImageSetting']->imageSpecial->dataInfo['CamTitlePosY']['value'] . "\r\n";

		$responseOutput->outputMsg .= 'Channel.0.TimeEnable=' . $boolArray[$classInstances['ImageSetting']->imageOSD->dataInfo['DispDate']['value']] . "\r\n";
		$responseOutput->outputMsg .= 'Channel.0.TimeFormat=' . $TimeFormat[$classInstances['ImageSetting']->imageOSD->dataInfo['DateFormat']['value']] . "\r\n";
		$responseOutput->outputMsg .= 'Channel.0.TimePositionX=' . $classInstances['ImageSetting']->imageOSD->dataInfo['DatePosX']['value'] . "\r\n";
		$responseOutput->outputMsg .= 'Channel.0.TimePositionY=' . $classInstances['ImageSetting']->imageOSD->dataInfo['DatePosY']['value'] . "\r\n";
		$responseOutput->outputMsg .= 'Channel.0.WeekdayEnable=' . $boolArray[$classInstances['ImageSetting']->imageOSD->dataInfo['DispWeekday']['value']] . "\r\n";

		if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3 || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ)
		{
			$responseOutput->outputMsg .= 'Channel.0.FontSize=' . $FontSize[$classInstances['ImageSetting']->imageOSD->dataInfo['OSDSize']['value']] . "\r\n";
		}

		if ($GLOBALS['M_SUPPORT_PTZ'] == PTZ_SUPPORT)
		{
			$responseOutput->outputMsg .= 'Channel.0.PTZPositionEnable=' . $boolArray[$classInstances['ImageSetting']->imageSpecial->dataInfo['PTZPositionDisplay']['value']] . "\r\n";
			$responseOutput->outputMsg .= 'Channel.0.CameraIDEnable=' . $boolArray[$classInstances['ImageSetting']->imageOSD->dataInfo['CamIDMode']['value']] . "\r\n";
			$responseOutput->outputMsg .= 'Channel.0.PresetNameEnable=' . $boolArray[$classInstances['ImageSetting']->imageOSD->dataInfo['PresetNameDisplay']['value']] . "\r\n";
			if ($GLOBALS["M_SUPPORT_AZIMUTH"])
			{
				$responseOutput->outputMsg .= 'Channel.0.AzimuthEnable=' . $boolArray[$classInstances['ImageSetting']->imageOSD->dataInfo['AzimuthEnable']['value']];
			}
		}

		/*
		  $responseOutput->outputMsg .= 'FaceDetectionCountEnable=' . $boolArray[$classInstances['ImageSetting']->imageOSD->dataInfo['FaceDetection']['value']] . "\r\n"; //Need to check Model Support
		  $responseOutput->outputMsg .= 'OSDColor=' . $OSDColor[$classInstances['ImageSetting']->imageOSD->dataInfo['OSDColor']['value']] . "\r\n";
		  $responseOutput->outputMsg .= 'BackgroundColor=' . $BackgroundColor[$classInstances['ImageSetting']->imageOSD->dataInfo['BackgroundColor']['value']] . "\r\n";
		  $responseOutput->outputMsg .= 'OverlayText=' . $boolArray[$classInstances['ImageSetting']->imageOSD->dataInfo['OverlayText']['value']] . "\r\n"; //Need to check Model Support
		  $responseOutput->outputMsg .= 'OverlayTextColor=' . $OSDColor[$classInstances['ImageSetting']->imageOSD->dataInfo['OverlayTextColor']['value']] . "\r\n";
		  $responseOutput->outputMsg .= 'OverlayTextPosition=' . $BackgroundColor[$classInstances['ImageSetting']->imageOSD->dataInfo['OverlayTextPosition']['value']] . "\r\n";
		 */

		$responseOutput->errCode = STATUS_OK;
		return $responseOutput;
	}
	else
	{
		$responseOutput->errCode = STATUS_ACTION_NOT_FOUND;
		return $responseOutput;
	}
}

///////////////////////////////////////////////
// White Balance
///////////////////////////////////////////////
function submenu_whitebalance()
{
	CheckAdminAccount(FALSE);
	$responseOutput = new ResponseOutput();

	$WhiteBalanceMode = array(
		0 => 'ATW',
		1 => 'Manual',
		2 => 'AWC',
		3 => 'Outdoor',
		4 => 'Indoor'
	);
	if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ)
	{
		$WhiteBalanceMode[5] = 'Mercury';
	}
	if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ)
	{
		$WhiteBalanceMode[6] = 'Sodium';
	}
	
	$classInstances = GetClassInstance('image');

	if ($_REQUEST['action'] == 'set')
	{
		if (count($_REQUEST) < 3)
		{
			$responseOutput->errCode = STATUS_MISSING_PARAMETER;
			return $responseOutput;
		}
		if ($_REQUEST['Channel'] != 0)
		{
			$responseOutput->errCode = STATUS_INVALID_VALUE;
			return $responseOutput;
		}

		$CameraInfo = array(
			'WhiteBalanceMode' => array('target' => 'imageWhiteBalance', 'name' => 'Mode'),
			'WhiteBalanceManualRedLevel' => array('target' => 'imageWhiteBalance', 'name' => 'Red'),
			'WhiteBalanceManualBlueLevel' => array('target' => 'imageWhiteBalance', 'name' => 'Blue')
		);


		foreach ($CameraInfo as $name => $data)
		{
			if (!isset($_REQUEST[$name]))
			{
				continue;
			}
			if ($name == 'WhiteBalanceManualRedLevel' || $name == 'WhiteBalanceManualBlueLevel')
			{
				if (isset($_REQUEST['WhiteBalanceMode']))
				{
					if ($_REQUEST['WhiteBalanceMode'] != "Manual")
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				else
				{
					if ($classInstances['ImageSetting']->imageWhiteBalance->dataInfo['Mode']['value'] != 1)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}

				if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3 || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ ||  $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_HISILICON)
				{
					if ($_REQUEST[$name] < 1 || $_REQUEST[$name] > 2048)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				else if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ)
				{
					if ($_REQUEST[$name] < 0 || $_REQUEST[$name] > 255)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}

				$classInstances['ImageSetting']->$data['target']->dataInfo[$data['name']]['value'] = $_REQUEST[$name];
			}
			else if ($name == 'WhiteBalanceMode')
			{
				$newValue = array_search($_REQUEST['WhiteBalanceMode'], $WhiteBalanceMode);
				if (is_bool($newValue))
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				$classInstances['ImageSetting']->$data['target']->dataInfo[$data['name']]['value'] = $newValue;
			}
		}

		$classInstances['ImageSetting']->imageWhiteBalance->payload = MakePayload($classInstances['ImageSetting']->imageWhiteBalance->dataInfo);

		$classInstances['ImageSetting']->imageSSDR->payload = MakePayload($classInstances['ImageSetting']->imageSSDR->dataInfo);
		$classInstances['ImageSetting']->imageWhiteBalance->payload = MakePayload($classInstances['ImageSetting']->imageWhiteBalance->dataInfo);
		$classInstances['ImageSetting']->imageBackLight->payload = MakePayload($classInstances['ImageSetting']->imageBackLight->dataInfo);
		$classInstances['ImageSetting']->imageExposure->payload = MakePayload($classInstances['ImageSetting']->imageExposure->dataInfo);
		$classInstances['ImageSetting']->imageSpecial->payload = MakePayload($classInstances['ImageSetting']->imageSpecial->dataInfo);
		$classInstances['ImageSetting']->imageIR->payload = MakePayload($classInstances['ImageSetting']->imageIR->dataInfo);
		$classInstances['ImageSetting']->imageOSD->payload = MakePayload($classInstances['ImageSetting']->imageOSD->dataInfo);
		$classInstances['ImageSetting']->imageDayNightSchedule->SetPayload();
		$classInstances['ImageSetting']->imagePreset->SetPayload();
		$classInstances['ImageSetting']->imagePTZIR->payload = MakePayload($classInstances['ImageSetting']->imagePTZIR->dataInfo);
		$classInstances['ImageSetting']->imageTracking->payload = MakePayload($classInstances['ImageSetting']->imageTracking->dataInfo);
		$classInstances['ImageSetting']->headerInfo['Action'] = ACTION_SET;
		$classInstances['ImageSetting']->SetPayload();
		$GLOBALS['SOCKET_MANAGER']->Connection($classInstances['ImageSetting']);


		$responseOutput->errCode = STATUS_OK;
		$responseOutput->outputMsg .= 'OK';
		return $responseOutput;
	}
	else if ($_REQUEST['action'] == 'view')
	{
		if ($_REQUEST['Channel'] != 0)
		{
			//$responseOutput->outputMsg = "Invalid Channel Number";
			$responseOutput->errCode = STATUS_INVALID_VALUE;
			return $responseOutput;
		}

		$responseOutput->outputMsg .= 'Channel.0.WhiteBalanceMode=' . $WhiteBalanceMode[$classInstances['ImageSetting']->imageWhiteBalance->dataInfo['Mode']['value']] . "\r\n";
		$responseOutput->outputMsg .= 'Channel.0.WhiteBalanceManualRedLevel=' . $classInstances['ImageSetting']->imageWhiteBalance->dataInfo['Red']['value'] . "\r\n";
		$responseOutput->outputMsg .= 'Channel.0.WhiteBalanceManualBlueLevel=' . $classInstances['ImageSetting']->imageWhiteBalance->dataInfo['Blue']['value'] . "\r\n";


		//AWCSet need to be added...6004 and other series Models Doesnt Support this functionality

		$responseOutput->errCode = STATUS_OK;
		return $responseOutput;
	}
	else if ($_REQUEST['action'] == 'control')
	{
		if ($_REQUEST['Channel'] != 0)
		{
			$responseOutput->errCode = STATUS_INVALID_VALUE;
			return $responseOutput;
		}

		if ((isset($_REQUEST['AWCSet']) && $classInstances['ImageSetting']->imageWhiteBalance->dataInfo['Mode']['value'] == 2))
		{
			require_once ('./adv/imagesetting.class');
			$AWCConf = new ImageSetting();
			$AWCConf->headerInfo['Action'] = ACTION_START;
			$AWCConf->payload = "";
			$AWCConf->payload .= pack('i1', 0);
			$AWCConf->payload .= pack('c1', 1);
			$AWCConf->payload .= pack('A63', 0);

			$socketManager = new SocketManager();
			$socketManager->Connection($AWCConf);

			$responseOutput->errCode = STATUS_OK;
			$responseOutput->outputMsg .= 'OK';
			return $responseOutput;
		}
		else
		{
			$responseOutput->errCode = STATUS_INVALID_VALUE;
			return $responseOutput;
		}
	}
	else
	{
		$responseOutput->errCode = STATUS_ACTION_NOT_FOUND;
		//$responseOutput->outputMsg .= "Invalid action";
		return $responseOutput;
	}
}

///////////////////////////////////////////////
// Flip
///////////////////////////////////////////////
function submenu_flip()
{
	CheckAdminAccount(FALSE);
	$responseOutput = new ResponseOutput();
	global $boolArray;
	
	//2 is unused -> 180*
	$RotateArray = array(
			0 => '0',
			1 => '90',
			3 => '270',
	);

	$classInstances = GetClassInstance('image');

	if ($_REQUEST['Channel'] != 0)
	{
		$responseOutput->errCode = STATUS_INVALID_VALUE;
		return $responseOutput;
	}

	if ($_REQUEST['action'] == 'set')
	{
		if (count($_REQUEST) < 3)
		{
			$responseOutput->errCode = STATUS_MISSING_PARAMETER;
			return $responseOutput;
		}

		$CameraInfo = array(
			'HorizontalFlipEnable' => array('target' => '', 'name' => 'Mirror'),
			'VerticalFlipEnable' => array('target' => '', 'name' => 'Flip'),
			'Rotate' => array('target' => '', 'name' => 'Rotate')
		);

		foreach ($CameraInfo as $name => $data)
		{
			if (!isset($_REQUEST[$name]))
			{
				continue;
			}
			if ($name == 'HorizontalFlipEnable')
			{
				if (isset($_REQUEST['HorizontalFlipEnable']))
				{
					$newValue = array_search($_REQUEST['HorizontalFlipEnable'], $boolArray);
					if (is_bool($newValue))
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						//$responseOutput->outputMsg .= "Invalid Value for Horizontal Flip Enable";
						return $responseOutput;
					}
					if($GLOBALS['M_SUPPORT_PTZ'] == PTZ_SUPPORT)
					{
						$classInstances['VideoSource']->dataInfo['Mirror']['value'] = $newValue;
						$classInstances['VideoSource']->dataInfo['Flip']['value'] = $newValue;
					}
					else
					{
						$classInstances['VideoSource']->dataInfo['Mirror']['value'] = $newValue;
					}
				}
			}
			else if ($name == 'VerticalFlipEnable')
			{
				if (isset($_REQUEST['VerticalFlipEnable']))
				{
					$newValue = array_search($_REQUEST['VerticalFlipEnable'], $boolArray);
					if (is_bool($newValue))
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						//$responseOutput->outputMsg .= "Invalid Value for Vertical Flip Enable";
						return $responseOutput;
					}
					if($GLOBALS['M_SUPPORT_PTZ'] == PTZ_SUPPORT)
					{
						$classInstances['VideoSource']->dataInfo['Mirror']['value'] = $newValue;
						$classInstances['VideoSource']->dataInfo['Flip']['value'] = $newValue;
					}
					else
					{
						$classInstances['VideoSource']->dataInfo['Flip']['value'] = $newValue;
					}
					
				}
			}
			else if ($name == 'Rotate')
			{
				if(!$GLOBALS['M_SUPPORT_ROTATE'])
				{
					$responseOutput->errCode = STATUS_NOT_IMPLEMENTED;
					return $responseOutput;
				}
				
				$newValue = array_search($_REQUEST['Rotate'], $RotateArray);
				if (is_bool($newValue))
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				
				$classInstances['MediaConfiguration']->dataInfo['Rotate']['value'] = $newValue;
			}
		}

		if (isset($_REQUEST['HorizontalFlipEnable']) || isset($_REQUEST['VerticalFlipEnable']))
		{
			$classInstances['VideoSource']->payload = MakePayload($classInstances['VideoSource']->dataInfo);
			$classInstances['VideoSource']->headerInfo['Action'] = ACTION_SET;
			$GLOBALS['SOCKET_MANAGER']->Connection($classInstances['VideoSource']);
		}

		if (isset($_REQUEST['Rotate']))
		{
			$classInstances['MediaConfiguration']->SetPayload();
			$classInstances['MediaConfiguration']->headerInfo['Action'] = ACTION_SET;
			$GLOBALS['SOCKET_MANAGER']->Connection($classInstances['MediaConfiguration']);
		}
		
		$responseOutput->errCode = STATUS_OK;
		$responseOutput->outputMsg .= 'OK';
		return $responseOutput;
	}
	else if ($_REQUEST['action'] == 'view')
	{
		$responseOutput->outputMsg .= 'Channel.0.HorizontalFlipEnable=' . $boolArray[$classInstances['VideoSource']->dataInfo['Mirror']['value']] . "\r\n";
		$responseOutput->outputMsg .= 'Channel.0.VerticalFlipEnable=' . $boolArray[$classInstances['VideoSource']->dataInfo['Flip']['value']] . "\r\n";
		if($GLOBALS['M_SUPPORT_ROTATE'])
		{
			$responseOutput->outputMsg .= 'Channel.0.Rotate=' . $RotateArray[$classInstances['MediaConfiguration']->dataInfo['Rotate']['value']] . "\r\n";
		}

		$responseOutput->errCode = STATUS_OK;
		return $responseOutput;
	}
	else
	{
		$responseOutput->errCode = STATUS_ACTION_NOT_FOUND;
		//$responseOutput->outputMsg .= "Invalid action";
		return $responseOutput;
	}
}

///////////////////////////////////////////////
// SSDR 
///////////////////////////////////////////////
function submenu_ssdr()
{
	CheckAdminAccount(FALSE);
	$responseOutput = new ResponseOutput();
	global $boolArray;

	$SSDRDynamicRange = array(
		0 => 'Wide',
		1 => 'Narrow'
	);

	if ($_REQUEST['Channel'] != 0)
	{
		$responseOutput->errCode = STATUS_INVALID_VALUE;
		return $responseOutput;
	}

	$classInstances = GetClassInstance('image');

	if ($_REQUEST['action'] == 'set')
	{
		if (count($_REQUEST) < 3)
		{
			$responseOutput->errCode = STATUS_MISSING_PARAMETER;
			return $responseOutput;
		}

		$CameraInfo = array(
			'Enable' => array('target' => 'imageSSDR', 'name' => 'Enabled'),
			'Level' => array('target' => 'imageSSDR', 'name' => 'Level'),
			'DynamicRange' => array('target' => 'imageSSDR', 'name' => 'DynamicRange')
		);

		foreach ($CameraInfo as $name => $data)
		{
			if (!isset($_REQUEST[$name]))
			{
				continue;
			}

			if ($name == 'Level' || $name == 'DynamicRange')
			{
				if (isset($_REQUEST['Enable']))
				{
					$newValue = array_search($_REQUEST['Enable'], $boolArray);
					if ($newValue != 1)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				else
				{
					if ($classInstances['ImageSetting']->imageSSDR->dataInfo['Enabled']['value'] != 1)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
			}
			if ($name == 'DynamicRange')
			{
				if ($GLOBALS['M_ISP_TYPE'] != ISP_TYPE_WN3 && $GLOBALS['M_ISP_TYPE'] != ISP_TYPE_HISILICON)
				{
					$responseOutput->errCode = STATUS_INVALID_PARAMETER;
					return $responseOutput;
				}
				$newValue = array_search($_REQUEST['DynamicRange'], $SSDRDynamicRange);
				if (is_bool($newValue))
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				$classInstances['ImageSetting']->$data['target']->dataInfo[$data['name']]['value'] = $newValue;
			}
			else if ($name == 'Enable')
			{
				$newValue = array_search($_REQUEST['Enable'], $boolArray);
				if (is_bool($newValue))
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				$classInstances['ImageSetting']->$data['target']->dataInfo[$data['name']]['value'] = $newValue;
			}
			else if ($name == 'Level')
			{
				if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ)
				{
					if ($_REQUEST[$name] < 1 || $_REQUEST[$name] > 15)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				else if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3 || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_HISILICON)
				{
					if ($_REQUEST[$name] < 1 || $_REQUEST[$name] > 32)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}

				$classInstances['ImageSetting']->$data['target']->dataInfo[$data['name']]['value'] = $_REQUEST[$name];
			}
		}

		$classInstances['ImageSetting']->imageSSDR->payload = MakePayload($classInstances['ImageSetting']->imageSSDR->dataInfo);
		$classInstances['ImageSetting']->imageWhiteBalance->payload = MakePayload($classInstances['ImageSetting']->imageWhiteBalance->dataInfo);
		$classInstances['ImageSetting']->imageBackLight->payload = MakePayload($classInstances['ImageSetting']->imageBackLight->dataInfo);
		$classInstances['ImageSetting']->imageExposure->payload = MakePayload($classInstances['ImageSetting']->imageExposure->dataInfo);
		$classInstances['ImageSetting']->imageSpecial->payload = MakePayload($classInstances['ImageSetting']->imageSpecial->dataInfo);
		$classInstances['ImageSetting']->imageIR->payload = MakePayload($classInstances['ImageSetting']->imageIR->dataInfo);
		$classInstances['ImageSetting']->imageOSD->payload = MakePayload($classInstances['ImageSetting']->imageOSD->dataInfo);
		$classInstances['ImageSetting']->imageDayNightSchedule->SetPayload();
		$classInstances['ImageSetting']->imagePreset->SetPayload();
		$classInstances['ImageSetting']->imagePTZIR->payload = MakePayload($classInstances['ImageSetting']->imagePTZIR->dataInfo);
		$classInstances['ImageSetting']->imageTracking->payload = MakePayload($classInstances['ImageSetting']->imageTracking->dataInfo);
		$classInstances['ImageSetting']->headerInfo['Action'] = ACTION_SET;
		$classInstances['ImageSetting']->SetPayload();
		$GLOBALS['SOCKET_MANAGER']->Connection($classInstances['ImageSetting']);

		$responseOutput->outputMsg .= 'OK';
		$responseOutput->errCode = STATUS_OK;
		return $responseOutput;
	}
	else if ($_REQUEST['action'] == 'view')
	{
		$responseOutput->outputMsg .= 'Channel.0.Enable=' . $boolArray[$classInstances['ImageSetting']->imageSSDR->dataInfo['Enabled']['value']] . "\r\n";
		$responseOutput->outputMsg .= 'Channel.0.Level=' . $classInstances['ImageSetting']->imageSSDR->dataInfo['Level']['value'] . "\r\n";
		if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3 ||  $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_HISILICON)
		{
			$responseOutput->outputMsg .= 'Channel.0.DynamicRange=' . $SSDRDynamicRange[$classInstances['ImageSetting']->imageSSDR->dataInfo['DynamicRange']['value']] . "\r\n";
		}

		$responseOutput->errCode = STATUS_OK;
		return $responseOutput;
	}
	else
	{
		$responseOutput->errCode = STATUS_ACTION_NOT_FOUND;
		return $responseOutput;
	}
}

function GetMaxShutterLowLimit($shutterSpeed, $sensorFrameMode, $isWDR)
{
	$lowLimitValue = 7;
	if ($sensorFrameMode == 0)
	{
		$lowLimitValue = '1/60';
	}
	else if ($sensorFrameMode == 1)
	{
		$lowLimitValue = '1/50';
	}
	else if ($sensorFrameMode == 2)
	{
		if ($isWDR)
		{
			$lowLimitValue = '1/60';
		}
		else
		{
			$lowLimitValue = '1/30';
		}
	}
	else if ($sensorFrameMode == 3)
	{
		if ($isWDR)
		{
			$lowLimitValue = '1/50';
		}
		else
		{
			$lowLimitValue = '1/25';
		}
	}

	$lowLimitIndex = array_search($lowLimitValue, $shutterSpeed);
	if (is_bool($lowLimitIndex))
	{
		return -1;
	}
	return $lowLimitIndex;
}

function GetCamTitlePosMax()
{
	require_once ('./adv/info.class');
	$info = $GLOBALS['SOCKET_MANAGER']->Connection(new Information());
	$langIndex = $info->dataInfo['Language']['value'];

	if ($langIndex == 2) // Language is "Chinese"
	{
		if ($GLOBALS['M_MAX_RESOLUTION'] == MAX_1_MEGA)
		{
			$max_camtitle_pos_x = 41;
			$max_camtitle_pos_y = 26;
		}
		else if ($GLOBALS['M_MAX_RESOLUTION'] == MAX_3_MEGA && $GLOBALS['MEGAMODE'] == 3)
		{
			$max_camtitle_pos_x = 62;
			$max_camtitle_pos_y = 31;
		}
		else
		{
			$max_camtitle_pos_x = 58;
			$max_camtitle_pos_y = 24;
		}
	}
	else
	{
		if ($GLOBALS['M_MAX_RESOLUTION'] == MAX_1_MEGA)
		{
			$max_camtitle_pos_x = 51;
			$max_camtitle_pos_y = 20;
		}
		else if ($GLOBALS['M_MAX_RESOLUTION'] == MAX_3_MEGA && $GLOBALS['MEGAMODE'] == 3)
		{
			$max_camtitle_pos_x = 58;
			$max_camtitle_pos_y = 27;
		}
		else
		{
			$max_camtitle_pos_x = 56;
			$max_camtitle_pos_y = 20;
		}
	}
	return array($max_camtitle_pos_x, $max_camtitle_pos_y);
}

function CheckSupportBLC($backlightMode)
{
	if (isset($_REQUEST['CompensationMode']))
	{
		if ($_REQUEST['CompensationMode'] != 'BLC')
		{
			return False;
		}
	}
	else
	{
		if ($backlightMode != 1)
		{
			return False;
		}
	}
	return True;
}

///////////////////////////////////////////////
// Camera 
///////////////////////////////////////////////
function submenu_camera()
{
	CheckAdminAccount(FALSE);
	$responseOutput = new ResponseOutput();
	global $boolArray;

	$classInstances = GetClassInstance('image');

	$CompensationMode = array(
		0 => "Off",
		1 => 'BLC'
	);
	if (($GLOBALS['M_SUPPORT_BACKLIGHT'] & BACKLIGHT_MASK_HLC) == BACKLIGHT_MASK_HLC)
	{
		$CompensationMode[2] = 'HLC';
	}

	if (($GLOBALS['M_SUPPORT_BACKLIGHT'] & BACKLIGHT_MASK_WDR) == BACKLIGHT_MASK_WDR)
	{
		//if ($sensorFrameMode != 50 && $sensorFrameMode != 60) {
		$CompensationMode[3] = 'WDR';
		//}
	}

	$BLCLevel = array(
		0 => 'Low',
		1 => 'Medium',
		2 => 'High'
	);

	$HLCLevel = array(
		0 => 'Low',
		1 => 'Medium',
		2 => 'High'
	);

	$WDRLevel = array(
		0 => 'Low',
		1 => 'Medium',
		2 => 'High'
	);

	$DayNightMode = array(
		0 => 'Color',
		1 => 'BW',
		2 => 'Auto'
	);
	if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3 || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_HISILICON)
	{
		if ($GLOBALS['M_ALARMIN_COUNT'] > 0)
		{
			$DayNightMode[3] = 'ExternalBW';
		}
		$DayNightMode[4] = 'Schedule';
	}

	$DayNightModeSwitchingMode = array(
		0 => 'VeryFast',
		1 => 'Fast',
		2 => 'Normal',
		3 => 'Slow',
		4 => 'VerySlow'
	);

	if ($GLOBALS['M_SUPPORT_IRIS'] & PIRIS_SUPPORT)
	{
		$IrisMode = array(
			0 => 'Auto',
			1 => 'Manual',
			2 => 'P-Iris-SLAM3180PN',
			3 => 'P-Iris-M13VP288IR',
			4 => 'P-Iris-SLAM2890PN'
		);
	}
	else if ($GLOBALS['M_SUPPORT_IRIS'] & DOME_PIRIS_SUPPORT)
	{
		$IrisMode = array(
			0 => 'Auto',
			1 => 'Manual',
			2 => 'P-Iris'
		);
	}
	else if ($GLOBALS['M_SUPPORT_IRIS'] & IRIS_SUPPORT)
	{
		$IrisMode = array(
			0 => 'Auto',
			1 => 'Manual'
		);
	}
	else
	{
		$IrisMode = array();
	}

	$PIrisMode = array(
		0 => 'Auto',
		1 => 'Manual'
	);

	if ($GLOBALS['M_SUPPORT_IRIS'] & IRIS_FNO_SUPPORT)
	{
		if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3)
		{
			//if ($GLOBALS['M_SUPPORT_IRIS'] & DOME_PIRIS_SUPPORT)
			$IrisFno = array(
				0 => 'F1.2',
				1 => 'F1.4',
				2 => 'F1.6',
				3 => 'F2.0',
				4 => 'F2.4',
				5 => 'F2.8',
				6 => 'F3.4',
				7 => 'F4.0',
				8 => 'F4.8',
				9 => 'F5.6',
				10 => 'F6.8',
				11 => 'F8.0',
				12 => 'F9.6',
				13 => 'F11.0',
				14 => 'F14.0',
				15 => 'F16.0',
				16 => 'F19.0',
				17 => 'F22.0',
				18 => 'F28.0'
			);
		}
		else if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ)
		{
			if ($GLOBALS["M_MODEL_GROUP"] == MF_5430)
			{
				$IrisFno = array(
					0 => "F1.4",
					1 => "F1.6",
					2 => "F2.0",
					3 => "F2.4",
					4 => "F2.8",
					5 => "F3.4",
					6 => "F4.0",
					7 => "F4.8",
					8 => "F5.6",
					9 => "F6.8",
					10 => "F8.0",
					11 => "F9.6",
					12 => "F11.0",
					13 => "F14.0",
					14 => "Close"
				);
			}
			else
			{
				$IrisFno = array(
					0 => 'F1.6',
					1 => 'F2.0',
					2 => 'F2.4',
					3 => 'F2.8',
					4 => 'F3.4',
					5 => 'F4.0',
					6 => 'F4.8',
					7 => 'F5.6',
					8 => 'Close'
				);
			}
		}
	}

	$AGCMode = array(
		0 => 'Off',
		1 => 'Low',
		2 => 'Medium',
		3 => 'High'
	);
	if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ)
	{
		$AGCMode[4] = 'Manual';
	}

	$DayNightAlarmIn = array(
		0 => 'SwitchToBWIfCloses',
		1 => 'SwitchToBWIfOpens'
	);

	$sensorFrame = $classInstances['ImageSetting']->imageExposure->dataInfo['SensorFrameMode']['value'];

	if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3 || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ ||  $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_HISILICON)
	{
		$ShutterSpeed = array(
			0 => '2',
			1 => '1',
			2 => '1/2',
			3 => '1/4',
			4 => '1/5',
			5 => '1/8',
			6 => '1/15',
			7 => '1/25',
			8 => '1/30',
			9 => '1/50',
			10 => '1/60',
			11 => '1/100',
			12 => '1/120',
			13 => '1/150',
			14 => '1/180',
			15 => '1/200',
			16 => '1/240',
			17 => '1/250',
			18 => '1/300',
			19 => '1/360',
			20 => '1/480',
			21 => '1/500',
			22 => '1/600',
			23 => '1/700',
			24 => '1/1000',
			25 => '1/1500',
			26 => '1/2500',
			27 => '1/5000',
			28 => '1/10000',
			29 => '1/12000'
		);
		
		if ($GLOBALS['M_MAX_RESOLUTION'] == MAX_3_MEGA)
		{
			array_splice($ShutterSpeed, 7, 0, array('1/20'));
		}

		if ($GLOBALS['M_SUPPORT_SENSOR_FRAMEMODE'])
		{
			if ($GLOBALS['M_MAX_SERSORFRAME'] == 60)
			{
				if ($sensorFrame == 0 || $sensorFrame == 1)
				{
					$ShutterSpeed[0] = "";
				}
			}
			else if ($GLOBALS['M_MAX_SERSORFRAME'] == 30)
			{
				if ($GLOBALS['M_SUPPORT_MEGAMODE'] && $GLOBALS['MEGAMODE'] == 3)
				{
					$ShutterSpeed[0] = "";
				}
				else
				{
					if ($sensorFrame == 0 || $sensorFrame == 1) // 60fps, 50fps
					{
						$ShutterSpeed[0] = "";
					}
				}
			}
		}
	}
	else if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ)
	{
		if ($GLOBALS['M_MODEL_GROUP'] == MF_5430)
		{
			$ShutterSpeed = array(
				0 => "60",
				1 => "48",
				2 => "40",
				3 => "32",
				4 => "24",
				5 => "20",
				6 => "16",
				7 => "14",
				8 => "12",
				9 => "10",
				10 => "8",
				11 => "6",
				12 => "4",
				13 => "2",
				14 => "1/30",
				15 => "1/50",
				16 => "1/60",
				17 => "1/100",
				18 => "1/120",
				19 => "1/150",
				20 => "1/180",
				21 => "1/200",
				22 => "1/240",
				23 => "1/250",
				24 => "1/300",
				25 => "1/360",
				26 => "1/480",
				27 => "1/500",
				28 => "1/600",
				29 => "1/700",
				30 => "1/1000",
				31 => "1/1500",
				32 => "1/2500",
				33 => "1/5000",
				34 => "1/10000",
				35 => "1/11000",
				36 => "1/16000",
				37 => "1/33000"
			);

			if ($sensorFrame == 0) // 60 fps
			{
				$ShutterSpeed[15] = "1/60";
			}
			else if ($sensorFrame == 1) // 50 fps
			{
				$ShutterSpeed[15] = "1/50";
			}
			else if ($sensorFrame == 2) // 30 fps
			{
				$ShutterSpeed[14] = "1/30";
			}
			else // 25 fps
			{
				$ShutterSpeed[14] = "1/25";
			}
			
			if ($sensorFrame == 0 || $sensorFrame == 1) // 60/50 fps
			{
				array_splice($ShutterSpeed, 16, 1);
				array_splice($ShutterSpeed, 14, 1);
			}
		}
		else // SNP-6320
		{
			$ShutterSpeedLowFps = array(
				0 => "60",
				1 => "48",
				2 => "40",
				3 => "32",
				4 => "24",
				5 => "20",
				6 => "16",
				7 => "14",
				8 => "12",
				9 => "10",
				10 => "8",
				11 => "6",
				12 => "4",
				13 => "2",
				14 => "1/30",
				15 => "1/50",
				16 => "1/60",
				17 => "1/100",
				18 => "1/120",
				19 => "1/150",
				20 => "1/180",
				21 => "1/200",
				22 => "1/240",
				23 => "1/250",
				24 => "1/300",
				25 => "1/360",
				26 => "1/480",
				27 => "1/500",
				28 => "1/600",
				29 => "1/700",
				30 => "1/1000",
				31 => "1/1500",
				32 => "1/2500",
				33 => "1/5000",
				34 => "1/10000",
				35 => "1/11000",
				36 => "1/16000",
				37 => "1/33000"
			);

			$ShutterSpeedHighFps = array(
				0 => "30",
				1 => "24",
				2 => "20",
				3 => "16",
				4 => "14",
				5 => "12",
				6 => "10",
				7 => "8",
				8 => "6",
				9 => "4",
				10 => "2",
				11 => "1/50",
				12 => "1/100",
				13 => "1/150",
				14 => "1/200",
				15 => "1/250",
				16 => "1/300",
				17 => "1/400",
				18 => "1/500",
				19 => "1/600",
				20 => "1/700",
				21 => "1/1000",
				22 => "1/1500",
				23 => "1/2500",
				24 => "1/5000",
				25 => "1/10000",
				26 => "1/11000",
				27 => "1/12000",
				28 => "1/16000"
			);

			if ($sensorFrame == 0) // 60 fps
			{
				$ShutterSpeedHighFps[11] = "1/60";
				$ShutterSpeedHighFps[12] = "1/120";
				$ShutterSpeedHighFps[13] = "1/180";
				$ShutterSpeedHighFps[14] = "1/240";
				$ShutterSpeedHighFps[15] = "1/300";
				$ShutterSpeedHighFps[16] = "1/360";
			}
			else if ($sensorFrame == 1) // 50 fps
			{
				$ShutterSpeedHighFps[11] = "1/50";
				$ShutterSpeedHighFps[12] = "1/100";
				$ShutterSpeedHighFps[13] = "1/150";
				$ShutterSpeedHighFps[14] = "1/200";
				$ShutterSpeedHighFps[15] = "1/250";
				$ShutterSpeedHighFps[16] = "1/300";
			}
			else if ($sensorFrame == 2) // 30 fps
			{
				$ShutterSpeedLowFps[14] = "1/30";
			}
			else // 25 fps
			{
				$ShutterSpeedLowFps[14] = "1/25";
			}

			if ($sensorFrame == 0 || $sensorFrame == 1) // 60/50 fps
			{
				$ShutterSpeed = $ShutterSpeedHighFps;
			}
			else
			{
				$ShutterSpeed = $ShutterSpeedLowFps;
			}
		}
	}

	$DayNightDwellTime = array(
		5 => '5s',
		7 => '7s',
		10 => '10s',
		15 => '15s',
		20 => '20s',
		30 => '30s',
		40 => '40s',
		60 => '60s'
	);

	$AFLKMode = array(
		0 => 'Off',
		1 => 'On',
		2 => '50',
		3 => '60'
	);


	if ($_REQUEST['Channel'] != 0)
	{
		//$responseOutput->outputMsg = "Invalid Channel Number";
		$responseOutput->errCode = STATUS_INVALID_VALUE;
		return $responseOutput;
	}

	if ($_REQUEST['action'] == 'set')
	{
		if (count($_REQUEST) < 3)
		{
			//$responseOutput->outputMsg = "Insufficient Number of Parameter";
			$responseOutput->errCode = STATUS_MISSING_PARAMETER;
			return $responseOutput;
		}

		$CameraInfo = array(
			'CompensationMode' => array('target' => 'imageBackLight', 'name' => 'Mode'),
			'BLCLevel' => array('target' => 'imageBackLight', 'name' => 'BLCLevel'),
			'BLCAreaTop' => array('target' => 'imageBackLight', 'name' => 'BLCTop'),
			'BLCAreaBottom' => array('target' => 'imageBackLight', 'name' => 'BLCBottom'),
			'BLCAreaLeft' => array('target' => 'imageBackLight', 'name' => 'BLCLeft'),
			'BLCAreaRight' => array('target' => 'imageBackLight', 'name' => 'BLCRight'),
			'HLCLevel' => array('target' => 'imageBackLight', 'name' => 'HLCLevel'),
			'HLCMaskTone' => array('target' => 'imageBackLight', 'name' => 'HLCMasktone'),
			'WDRLevel' => array('target' => 'imageBackLight', 'name' => 'WDRLevel'),
			'SSNREnable' => array('target' => 'imageExposure', 'name' => 'SSNRMode'),
			'SSNRLevel' => array('target' => 'imageExposure', 'name' => 'SSNRLevel'),
			'IrisMode' => array('target' => 'imageExposure', 'name' => 'IrisMode'),
			'PIrisMode' => array('target' => 'imageExposure', 'name' => 'PIrisMode'),
			'PIrisPosition' => array('target' => 'imageExposure', 'name' => 'PIrisPosition'),
			'IrisFno' => array('target' => 'imageExposure', 'name' => 'PIrisFno'),
			'ShutterMode' => array('target' => 'imageExposure', 'name' => 'ShutterMode'),
			'AutoShortShutterSpeed' => array('target' => 'imageExposure', 'name' => 'ShortShutterSpeed'),
			'AutoLongShutterSpeed' => array('target' => 'imageExposure', 'name' => 'LongShutterSpeed'),
			'AFLKMode' => array('target' => 'imageExposure', 'name' => 'UseAFLK'),
			'AGCMode' => array('target' => 'imageExposure', 'name' => 'AGCMode'),
			'AGCLevel' => array('target' => 'imageExposure', 'name' => 'AGCLevel'),
			'DayNightMode' => array('target' => 'imageSpecial', 'name' => 'DayNightMode'),
			'DayNightSwitchingTime' => array('target' => 'imageSpecial', 'name' => 'DayNightDwellTime'),
			'DayNightSwitchingMode' => array('target' => 'imageSpecial', 'name' => 'DayNightDuration'),
			'DayNightAlarmIn' => array('target' => 'imageSpecial', 'name' => 'DayNightExtMode'),
			'SimpleFocus' => array('target' => 'imageSpecial', 'name' => 'AutoFocusEnable'),
			'DayNightModeSchedule_EveryDay' => array('target' => 'imageDayNightSchedule', 'index' => 0),
			'DayNightModeSchedule_SUN' => array('target' => 'imageDayNightSchedule', 'index' => 1),
			'DayNightModeSchedule_MON' => array('target' => 'imageDayNightSchedule', 'index' => 2),
			'DayNightModeSchedule_TUE' => array('target' => 'imageDayNightSchedule', 'index' => 3),
			'DayNightModeSchedule_WED' => array('target' => 'imageDayNightSchedule', 'index' => 4),
			'DayNightModeSchedule_THU' => array('target' => 'imageDayNightSchedule', 'index' => 5),
			'DayNightModeSchedule_FRI' => array('target' => 'imageDayNightSchedule', 'index' => 6),
			'DayNightModeSchedule_SAT' => array('target' => 'imageDayNightSchedule', 'index' => 7)
		);

		$minBlcHeightLength = 40;
		$minBlcWidthLength = 30;
		$maxBlcLength = 60;
		
		$blcTopDelta = 0;
		$blcBottomDelta = 0;
		$blcLeftDelta = 0;
		$blcRightDelta = 0;
		$blcBoxInputCountForPtz = 0;

		foreach ($CameraInfo as $name => $data)
		{
			if (!isset($_REQUEST[$name]))
			{
				continue;
			}

			if ($name == 'CompensationMode')
			{
				$newValue = array_search($_REQUEST['CompensationMode'], $CompensationMode);
				if (is_bool($newValue))
				{
					//$responseOutput->outputMsg .= 'Value for CompensationMode is not correct';
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}

				if ($newValue == 3) // WDR
				{
					//Max and Min Shutter need to be set as below when CompensationMode is WDR
					if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3)
					{
						$classInstances['ImageSetting']->imageExposure->dataInfo['LongShutterSpeed']['value'] = 4; //MinShutter = 1/5
						if($GLOBALS['M_MAX_RESOLUTION'] == MAX_3_MEGA)
						{
							$classInstances['ImageSetting']->imageExposure->dataInfo['ShortShutterSpeed']['value'] = 17; //MaxShutter = 1/240
						}
						else
						{
							$classInstances['ImageSetting']->imageExposure->dataInfo['ShortShutterSpeed']['value'] = 16; //MaxShutter = 1/240
						}
					}

					//If SensorCaptureFrameRate 60/50, WDR can not be set.
					if ($GLOBALS['M_MAX_SERSORFRAME'] == 60 || ($GLOBALS['M_SUPPORT_MEGAMODE'] && $GLOBALS['MEGAMODE'] == 2))
					{
						$sensorFrame = $classInstances['ImageSetting']->imageExposure->dataInfo['SensorFrameMode']['value'];
						if ($sensorFrame == 0 || $sensorFrame == 1)
						{
							$responseOutput->errCode = STATUS_INVALID_VALUE;
							//$responseOutput->outputMsg .= 'SensorCaptureFrameRate is 50/60';
							return $responseOutput;
						}
					}
				}
				else
				{
					if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3 &&
						$classInstances['ImageSetting']->imageBackLight->dataInfo['Mode']['value'] == 3)
					{
						$classInstances['ImageSetting']->imageExposure->dataInfo['LongShutterSpeed']['value'] = 4; //MinShutter = 1/5
						if($GLOBALS['M_MAX_RESOLUTION'] == MAX_3_MEGA)
						{
							$classInstances['ImageSetting']->imageExposure->dataInfo['ShortShutterSpeed']['value'] = 30; //MaxShutter = 1/12000
						}
						else
						{
							$classInstances['ImageSetting']->imageExposure->dataInfo['ShortShutterSpeed']['value'] = 29; //MaxShutter = 1/12000
						}
					}
				}

				$classInstances['ImageSetting']->imageBackLight->dataInfo['Mode']['value'] = $newValue;
			}
			else if ($name == 'BLCLevel')
			{
				if (CheckSupportBLC($classInstances['ImageSetting']->imageBackLight->dataInfo['Mode']['value']) == False)
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					//$responseOutput->outputMsg .= 'CompensationMode is not in BLC Mode';
					return $responseOutput;
				}

				$newValue = array_search($_REQUEST['BLCLevel'], $BLCLevel);
				if (is_bool($newValue))
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				$classInstances['ImageSetting']->imageBackLight->dataInfo['BLCLevel']['value'] = $newValue;
			}
			else if ($name == 'BLCAreaTop')
			{				
				if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3 ||  $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_HISILICON)
				{
					if ($_REQUEST[$name] < 1 || $_REQUEST[$name] > 60)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
					
					if(isset($_REQUEST['BLCAreaBottom']))
					{
						$blcTopMin = $_REQUEST['BLCAreaBottom'] - $maxBlcLength;
						$blcTopMax = $_REQUEST['BLCAreaBottom'] - $minBlcHeightLength;
					}
					else
					{
						$blcTopMin = $classInstances['ImageSetting']->imageBackLight->dataInfo["BLCBottom"]["value"] - $maxBlcLength;
						$blcTopMax = $classInstances['ImageSetting']->imageBackLight->dataInfo["BLCBottom"]["value"] - $minBlcHeightLength;
					}
					
					if ($_REQUEST[$name] < $blcTopMin || $_REQUEST[$name] > $blcTopMax)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
					$classInstances['ImageSetting']->imageBackLight->dataInfo['BLCTop']['value'] = $_REQUEST[$name];
				}
				else if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ)
				{
					if ($_REQUEST[$name] < 0 || $_REQUEST[$name] > 100)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
					$classInstances['ImageSetting']->testCmd = 1;
					$blcTopDelta = $classInstances['ImageSetting']->imageBackLight->dataInfo['CoordBlcTop']['value'] - $_REQUEST[$name];
					$blcBoxInputCountForPtz++;
				}
				
				if (CheckSupportBLC($classInstances['ImageSetting']->imageBackLight->dataInfo['Mode']['value']) == False)
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					//$responseOutput->outputMsg .= 'CompensationMode is not in BLC Mode';
					return $responseOutput;
				}
			}
			else if ($name == 'BLCAreaLeft')
			{
				if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3 || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_HISILICON)
				{
					if ($_REQUEST[$name] < 1 || $_REQUEST[$name] > 70)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
					
					if(isset($_REQUEST['BLCAreaRight']))
					{
						$blcLeftMin = $_REQUEST['BLCAreaRight'] - $maxBlcLength;
						$blcLeftMax = $_REQUEST['BLCAreaRight'] - $minBlcWidthLength;						
					}
					else
					{
						$blcLeftMin = $classInstances['ImageSetting']->imageBackLight->dataInfo["BLCRight"]["value"] - $maxBlcLength;
						$blcLeftMax = $classInstances['ImageSetting']->imageBackLight->dataInfo["BLCRight"]["value"] - $minBlcWidthLength;					
					}
					if ($_REQUEST[$name] < $blcLeftMin || $_REQUEST[$name] > $blcLeftMax)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
					$classInstances['ImageSetting']->imageBackLight->dataInfo['BLCLeft']['value'] = $_REQUEST[$name];
				}
				else if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ)
				{
					if ($_REQUEST[$name] < 0 || $_REQUEST[$name] > 100)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
					$classInstances['ImageSetting']->testCmd = 1;
					$blcLeftDelta = $classInstances['ImageSetting']->imageBackLight->dataInfo['CoordBlcLeft']['value'] - $_REQUEST[$name];
					$blcBoxInputCountForPtz++;
				}

				if (CheckSupportBLC($classInstances['ImageSetting']->imageBackLight->dataInfo['Mode']['value']) == False)
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					//$responseOutput->outputMsg .= 'CompensationMode is not in BLC Mode';
					return $responseOutput;
				}
			}
			else if ($name == 'BLCAreaBottom')
			{
				if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3 || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_HISILICON)
				{
					if ($_REQUEST[$name] < 41 || $_REQUEST[$name] > 100)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
					
					if(isset($_REQUEST['BLCAreaTop']))
					{
						$blcBottomMin = $_REQUEST['BLCAreaTop'] + $minBlcHeightLength;
						$blcBottomMax = $_REQUEST['BLCAreaTop'] + $maxBlcLength;					
					}
					else
					{
						$blcBottomMin = $classInstances['ImageSetting']->imageBackLight->dataInfo["BLCTop"]["value"] + $minBlcHeightLength;
						$blcBottomMax = $classInstances['ImageSetting']->imageBackLight->dataInfo["BLCTop"]["value"] + $maxBlcLength;
					}
					if ($_REQUEST[$name] < $blcBottomMin || $_REQUEST[$name] > $blcBottomMax)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
					$classInstances['ImageSetting']->imageBackLight->dataInfo['BLCBottom']['value'] = $_REQUEST[$name];
				}
				else if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ)
				{
					if ($_REQUEST[$name] < 0 || $_REQUEST[$name] > 100)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
					$classInstances['ImageSetting']->testCmd = 1;
					$blcBottomDelta = $_REQUEST[$name] - $classInstances['ImageSetting']->imageBackLight->dataInfo['CoordBlcBottom']['value'];
					$blcBoxInputCountForPtz++;
				}

				if (CheckSupportBLC($classInstances['ImageSetting']->imageBackLight->dataInfo['Mode']['value']) == False)
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					//$responseOutput->outputMsg .= 'CompensationMode is not in BLC Mode';
					return $responseOutput;
				}
			}
			else if ($name == 'BLCAreaRight')
			{
				if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3 || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_HISILICON)
				{
					if ($_REQUEST[$name] < 31 || $_REQUEST[$name] > 100)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				
					if(isset($_REQUEST['BLCAreaLeft']))
					{
						$blcRightMin = $_REQUEST['BLCAreaLeft'] + $minBlcWidthLength;
						$blcRightMax = $_REQUEST['BLCAreaLeft'] + $maxBlcLength;					
					}
					else
					{
						$blcRightMin = $classInstances['ImageSetting']->imageBackLight->dataInfo["BLCLeft"]["value"] + $minBlcWidthLength;
						$blcRightMax = $classInstances['ImageSetting']->imageBackLight->dataInfo["BLCLeft"]["value"] + $maxBlcLength;
					}
					if ($_REQUEST[$name] < $blcRightMin || $_REQUEST[$name] > $blcRightMax)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
					$classInstances['ImageSetting']->imageBackLight->dataInfo['BLCRight']['value'] = $_REQUEST[$name];
				}
				else if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ)
				{
					if ($_REQUEST[$name] < 0 || $_REQUEST[$name] > 100)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
					$classInstances['ImageSetting']->testCmd = 1;
					$blcRightDelta = $_REQUEST[$name] - $classInstances['ImageSetting']->imageBackLight->dataInfo['CoordBlcRight']['value'];
					$blcBoxInputCountForPtz++;
				}

				if (CheckSupportBLC($classInstances['ImageSetting']->imageBackLight->dataInfo['Mode']['value']) == False)
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					//$responseOutput->outputMsg .= 'CompensationMode is not in BLC Mode';
					return $responseOutput;
				}
			}
			else if ($name == 'HLCLevel')
			{
				if (($GLOBALS['M_SUPPORT_BACKLIGHT'] & BACKLIGHT_MASK_HLC) != BACKLIGHT_MASK_HLC)
				{
					$responseOutput->errCode = STATUS_INVALID_PARAMETER;
					return $responseOutput;
				}

				$newValue = array_search($_REQUEST['HLCLevel'], $HLCLevel);
				if (is_bool($newValue))
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				$classInstances['ImageSetting']->imageBackLight->dataInfo['HLCLevel']['value'] = $newValue;
			}
			else if ($name == 'HLCMaskTone')
			{
				if (($GLOBALS['M_SUPPORT_BACKLIGHT'] & BACKLIGHT_MASK_HLC) != BACKLIGHT_MASK_HLC)
				{
					$responseOutput->errCode = STATUS_INVALID_PARAMETER;
					return $responseOutput;
				}

				if ($_REQUEST['HLCMaskTone'] < 0 || $_REQUEST['HLCMaskTone'] > 15)
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				$classInstances['ImageSetting']->imageBackLight->dataInfo['HLCMasktone']['value'] = $_REQUEST['HLCMaskTone'];
			}
			else if ($name == 'WDRLevel')
			{
				if (isset($_REQUEST['CompensationMode']))
				{
					if ($_REQUEST['CompensationMode'] != 'WDR')
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						//$responseOutput->outputMsg .= 'CompensationMode is not in BLC Mode';
						return $responseOutput;
					}
				}
				else
				{
					if ($classInstances['ImageSetting']->imageBackLight->dataInfo['Mode']['value'] != 3)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						//$responseOutput->outputMsg .= 'CompensationMode is not in BLC Mode';
						return $responseOutput;
					}
				}

				//If SensorCaptureFrameRate 50/60 WDR can not be set.
				//if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3)
				{
					$sensorFrame = $classInstances['ImageSetting']->imageExposure->dataInfo['SensorFrameMode']['value'];

					if ($sensorFrame == 0 || $sensorFrame == 1)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						//$responseOutput->outputMsg .= 'SensorCaptureFrameRate is 50/60';
						return $responseOutput;
					}
				}

				$newValue = array_search($_REQUEST['WDRLevel'], $WDRLevel);

				if (is_bool($newValue))
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				$classInstances['ImageSetting']->imageBackLight->dataInfo['WDRLevel']['value'] = $newValue;
			}
			else if ($name == 'ShutterMode')
			{
				$responseOutput->errCode = STATUS_INVALID_PARAMETER;
				return $responseOutput;
				/*
				$newValue = array_search($_REQUEST['ShutterMode'], $ShutterMode);
				if (is_bool($newValue))
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				
				if ($newValue == 0)
				{
					$classInstances['ImageSetting']->imageExposure->dataInfo['UseAFLK']['value'] = 0; // Off
				}
				else
				{
					if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3)
					{
						$classInstances['ImageSetting']->imageExposure->dataInfo['UseAFLK']['value'] = 2; // 50
					}
					else
					{
						$classInstances['ImageSetting']->imageExposure->dataInfo['UseAFLK']['value'] = 1; // On
					}
				}
				$classInstances['ImageSetting']->imageExposure->dataInfo['ShutterMode']['value'] = $newValue;*/
			}
			else if ($name == 'IrisMode')
			{
				if (!($GLOBALS['M_SUPPORT_IRIS'] & IRIS_SUPPORT))
				{
					$responseOutput->errCode = STATUS_INVALID_PARAMETER;
					return $responseOutput;
				}

				$newValue = array_search($_REQUEST['IrisMode'], $IrisMode);

				if (is_bool($newValue))
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				$classInstances['ImageSetting']->imageExposure->dataInfo['IrisMode']['value'] = $newValue;
			}
			else if ($name == 'PIrisMode')
			{
				if (!($GLOBALS['M_SUPPORT_IRIS'] & PIRIS_SUPPORT))
				{
					$responseOutput->errCode = STATUS_INVALID_PARAMETER;
					return $responseOutput;
				}

				if (isset($_REQUEST['IrisMode']))
				{
					if ($_REQUEST['IrisMode'] == 'Auto' || $_REQUEST['IrisMode'] == 'Manual')
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				else
				{
					if ($classInstances['ImageSetting']->imageExposure->dataInfo['IrisMode']['value'] == 0 && $classInstances['ImageSetting']->imageExposure->dataInfo['IrisMode']['value'] == 1)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						//$responseOutput->outputMsg .= 'IrisMode is not in P-Iris Mode';
						return $responseOutput;
					}
				}

				$newValue = array_search($_REQUEST['PIrisMode'], $PIrisMode);

				if (is_bool($newValue))
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				$classInstances['ImageSetting']->imageExposure->dataInfo['PIrisMode']['value'] = $newValue;
			}
			else if ($name == 'PIrisPosition')
			{
				if (!($GLOBALS['M_SUPPORT_IRIS'] & PIRIS_SUPPORT))
				{
					$responseOutput->errCode = STATUS_INVALID_PARAMETER;
					return $responseOutput;
				}

				if (isset($_REQUEST['PIrisMode']))
				{
					if ($_REQUEST['PIrisMode'] != 'Manual')
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						//$responseOutput->outputMsg .= 'PIrisMode is not in Manual Mode';
						return $responseOutput;
					}
				}
				else
				{
					if ($classInstances['ImageSetting']->imageExposure->dataInfo['PIrisMode']['value'] != 1)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						//$responseOutput->outputMsg .= 'PIrisMode is not in Manual Mode';
						return $responseOutput;
					}
				}

				if (isset($_REQUEST['IrisMode']))
				{
					if ($_REQUEST['IrisMode'] == 'Auto' || $_REQUEST['IrisMode'] == 'Manual')
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				else
				{
					if ($classInstances['ImageSetting']->imageExposure->dataInfo['IrisMode']['value'] == 0 ||
						$classInstances['ImageSetting']->imageExposure->dataInfo['IrisMode']['value'] == 1)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						//$responseOutput->outputMsg .= 'IrisMode is not in P-Iris Mode';
						return $responseOutput;
					}
				}

				if ($_REQUEST[$name] < 1 || $_REQUEST[$name] > 100)
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				$classInstances['ImageSetting']->imageExposure->dataInfo['PIrisPosition']['value'] = $_REQUEST[$name];
			}
			else if ($name == 'IrisFno')
			{
				if (!($GLOBALS['M_SUPPORT_IRIS'] & IRIS_FNO_SUPPORT))
				{
					$responseOutput->errCode = STATUS_INVALID_PARAMETER;
					return $responseOutput;
				}

				if (isset($_REQUEST['IrisMode']))
				{
					if ($_REQUEST['IrisMode'] != 'Manual')
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						//$responseOutput->outputMsg .= 'IrisMode is not in Manual Mode';
						return $responseOutput;
					}
				}
				else
				{
					if ($classInstances['ImageSetting']->imageExposure->dataInfo['IrisMode']['value'] != 1)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						//$responseOutput->outputMsg .= 'IrisMode is not in Manual Mode';
						return $responseOutput;
					}
				}

				$newValue = array_search($_REQUEST['IrisFno'], $IrisFno);
				if (is_bool($newValue))
				{
					$newIrisFno = substr($_REQUEST['IrisFno'], 1);
					foreach ($IrisFno as $name => $value)
					{
						$irisFnoInList = substr($value, 1);
						if ($newIrisFno == $irisFnoInList)
						{
							$newValue = $name;
						}
					}
					
					if (is_bool($newValue))
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				$classInstances['ImageSetting']->imageExposure->dataInfo['PIrisFno']['value'] = $newValue;
			}
			else if ($name == 'AutoShortShutterSpeed') // Minimum Shutter
			{
				//AFLK Dependency
				if (isset($_REQUEST['AFLKMode']))
				{
					if ($_REQUEST['AFLKMode'] != 'Off')
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				else
				{
					if ($classInstances['ImageSetting']->imageExposure->dataInfo['UseAFLK']['value'] != 0)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}

				$newMinShutter = array_search($_REQUEST['AutoShortShutterSpeed'], $ShutterSpeed);
				if (is_bool($newMinShutter))
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}

				if (isset($_REQUEST['AutoLongShutterSpeed']))
				{
					$maxShutter = array_search($_REQUEST['AutoLongShutterSpeed'], $ShutterSpeed);
				}
				else
				{
					$maxShutter = $classInstances['ImageSetting']->imageExposure->dataInfo['ShortShutterSpeed']['value'];
				}

				if ($newMinShutter > $maxShutter)
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				
				if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3)
				{
					// WDR Dependency
					if ($sensorFrame >= 2)
					{
						if (isset($_REQUEST['CompensationMode']))
						{
							$isWDR = ($_REQUEST['CompensationMode'] == "WDR");
						}
						else
						{
							$isWDR = ($classInstances['ImageSetting']->imageBackLight->dataInfo['Mode']['value'] == 3);
						}
						if ($isWDR)
						{
							$lowLimit = array_search('1/240', $ShutterSpeed);
							if (is_bool($lowLimit))
							{
								$responseOutput->errCode = STATUS_INVALID_VALUE;
								return $responseOutput;
							}
							if ($newMinShutter > $lowLimit)
							{
								$responseOutput->errCode = STATUS_INVALID_VALUE;
								return $responseOutput;
							}
						}
					}
				}
				else if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ)
				{
					//WDR Dependency
					if (isset($_REQUEST['CompensationMode']))
					{
						if ($_REQUEST['CompensationMode'] == 'WDR')
						{
							$responseOutput->errCode = STATUS_INVALID_VALUE;
							return $responseOutput;
						}
					}
					else
					{
						if ($classInstances['ImageSetting']->imageBackLight->dataInfo['Mode']['value'] == 3)
						{
							$responseOutput->errCode = STATUS_INVALID_VALUE;
							return $responseOutput;
						}
					}

					if (isset($_REQUEST['AGCMode']))
					{
						$agcMode = array_search($_REQUEST['AGCMode'], $AGCMode);
						if (is_bool($agcMode))
						{
							$responseOutput->errCode = STATUS_INVALID_VALUE;
							return $responseOutput;
						}
					}
					else
					{
						$agcMode = $classInstances['ImageSetting']->imageExposure->dataInfo['AGCMode']['value'];
					}

					if ($sensorFrame < 2)
					{ // Sensor fps = 60 or 50
						if ($newMinShutter >= 0 && $newMinShutter <= 10)
						{ //x30 ~ x2
							if ($agcMode == 0 || $agcMode == 4)
							{ //Off, Manual
								$classInstances['ImageSetting']->imageExposure->dataInfo['AGCMode']['value'] = 2; //Medium
							}
						}
					}
					else
					{
						if ($newMinShutter >= 0 && $newMinShutter <= 13)
						{ //x60 ~ x2
							if ($agcMode == 0 || $agcMode == 4)
							{ //Off, Manual
								$classInstances['ImageSetting']->imageExposure->dataInfo['AGCMode']['value'] = 2; //Medium
							}
						}
					}
				}

				$classInstances['ImageSetting']->imageExposure->dataInfo['LongShutterSpeed']['value'] = $newMinShutter;
			}
			else if ($name == 'AutoLongShutterSpeed') // Maximum Shutter
			{
				//AFLK Dependency
				if (isset($_REQUEST['AFLKMode']))
				{
					if ($_REQUEST['AFLKMode'] != 'Off')
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				else
				{
					if ($classInstances['ImageSetting']->imageExposure->dataInfo['UseAFLK']['value'] != 0)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}

				$newMaxShutter = array_search($_REQUEST['AutoLongShutterSpeed'], $ShutterSpeed);
				if (is_bool($newMaxShutter))
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}

				if (isset($_REQUEST['AutoShortShutterSpeed']))
				{
					$minShutter = array_search($_REQUEST['AutoShortShutterSpeed'], $ShutterSpeed);
				}
				else
				{
					$minShutter = $classInstances['ImageSetting']->imageExposure->dataInfo['LongShutterSpeed']['value'];
				}
				if ($newMaxShutter < $minShutter)
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}				
				
				if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3 || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_HISILICON)
				{
					// Sensor Framerate Dependency
					if (isset($_REQUEST['CompensationMode']))
					{
						$isWDR = ($_REQUEST['CompensationMode'] == "WDR");
					}
					else
					{
						$isWDR = ($classInstances['ImageSetting']->imageBackLight->dataInfo['Mode']['value'] == 3);
					}
					$index = GetMaxShutterLowLimit($ShutterSpeed, $sensorFrame, $isWDR);
					if ($minShutter > $index)
					{
						$index = $minShutter;
					}
					
					if ($newMaxShutter < $index)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}

					// WDR Dependency
					if ($isWDR)
					{
						if($GLOBALS['M_MAX_RESOLUTION'] == MAX_1_MEGA)
						{	
							$highLimit = "1/700";
						}
						else if ($GLOBALS['M_MODEL_GROUP'] == MF_7010FE)
						{
							$highLimit = "1/240";
						}
						else
						{
							if ($sensorFrame >= 2)
							{
								$highLimit = "1/240";
							}
						}
						
						if (isset($highLimit))
						{
							$lowLimit = array_search($highLimit, $ShutterSpeed);
							if (is_bool($lowLimit))
							{
								$responseOutput->errCode = STATUS_INVALID_VALUE;
								return $responseOutput;
							}
							if ($newMaxShutter > $lowLimit)
							{
								$responseOutput->errCode = STATUS_INVALID_VALUE;
								return $responseOutput;
							}
						}
					}
				}
				else if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ)
				{
					//WDR Dependency
					if (isset($_REQUEST['CompensationMode']))
					{
						if ($_REQUEST['CompensationMode'] == 'WDR')
						{
							$responseOutput->errCode = STATUS_INVALID_VALUE;
							return $responseOutput;
						}
					}
					else
					{
						if ($classInstances['ImageSetting']->imageBackLight->dataInfo['Mode']['value'] == 3)
						{
							$responseOutput->errCode = STATUS_INVALID_VALUE;
							return $responseOutput;
						}
					}
					
					// MaxShutterLowLimit
					if ($minShutter < 14)
					{
						$minShutter = 14;
					}

					if ($newMaxShutter < $minShutter)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}

				$classInstances['ImageSetting']->imageExposure->dataInfo['ShortShutterSpeed']['value'] = $newMaxShutter;
			}
			else if ($name == 'AFLKMode')
			{
//				if ($GLOBALS['M_ISP_TYPE'] != ISP_TYPE_WN3)
//				{
//					$responseOutput->errCode = STATUS_INVALID_PARAMETER;
//					return $responseOutput;
//				}
				
				// ShutterMode should be AFLK to configure AFLKMode.
//				if (isset($_REQUEST['ShutterMode']))
//				{
//					if ($_REQUEST['ShutterMode'] != 'AFLK')
//					{
//						$responseOutput->errCode = STATUS_INVALID_VALUE;
//						return $responseOutput;
//					}
//				}
//				else
//				{
//					if ($classInstances['ImageSetting']->imageExposure->dataInfo['ShutterMode']['value'] != 2)
//					{
//						$responseOutput->errCode = STATUS_INVALID_VALUE;
//						return $responseOutput;
//					}
//				}

				$newValue = array_search($_REQUEST['AFLKMode'], $AFLKMode);
				if (is_bool($newValue))
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				$classInstances['ImageSetting']->imageExposure->dataInfo['UseAFLK']['value'] = $newValue;
			}
			else if ($name == 'SSNREnable')
			{
				if (isset($_REQUEST['AGCMode']))
				{
					if ($_REQUEST['AGCMode'] == 'Off')
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
					
					if (($GLOBALS['M_ISP_TYPE'] != ISP_TYPE_WN2_PTZ) && ($_REQUEST['AGCMode'] == 'Manual'))
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				else
				{
					if ($classInstances['ImageSetting']->imageExposure->dataInfo['AGCMode']['value'] == 0 )
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}

				$newValue = array_search($_REQUEST['SSNREnable'], $boolArray);
				if (is_bool($newValue))
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				$classInstances['ImageSetting']->imageExposure->dataInfo['SSNRMode']['value'] = $newValue;
			}
			else if ($name == 'SSNRLevel')
			{
				if (isset($_REQUEST['AGCMode']))
				{
					if ($_REQUEST['AGCMode'] == 'Off')
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
					
					if (($GLOBALS['M_ISP_TYPE'] != ISP_TYPE_WN2_PTZ) && ($_REQUEST['AGCMode'] == 'Manual'))
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				else
				{
					if ($classInstances['ImageSetting']->imageExposure->dataInfo['AGCMode']['value'] == 0)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}

				if (isset($_REQUEST['SSNREnable']))
				{
					if ($_REQUEST['SSNREnable'] != 'True')
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				else
				{
					if ($classInstances['ImageSetting']->imageExposure->dataInfo['SSNRMode']['value'] == 0)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}

				if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3 || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_HISILICON)
				{
					if ($_REQUEST[$name] < 1 || $_REQUEST[$name] > 32)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				else if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ)
				{
					if ($_REQUEST[$name] < 1 || $_REQUEST[$name] > 3)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				$classInstances['ImageSetting']->imageExposure->dataInfo['SSNRLevel']['value'] = $_REQUEST[$name];
			}
			else if ($name == 'AGCMode')
			{
				$newValue = array_search($_REQUEST['AGCMode'], $AGCMode);
				if (is_bool($newValue))
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}

				if (isset($_REQUEST['AutoShortShutterSpeed']))
				{
					$minShutter = array_search($_REQUEST['AutoShortShutterSpeed'], $ShutterSpeed);
					if (is_bool($newMinShutter))
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				else
				{
					$minShutter = $classInstances['ImageSetting']->imageExposure->dataInfo['LongShutterSpeed']['value'];
				}

				if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ)
				{
					if ($newValue == 0 || $newValue == 4)
					{
						if ($sensorFrame < 2)
						{ // Sensor fps = 60 or 50
							if ($minShutter >= 0 && $minShutter <= 10)
							{ //x30 ~ x2
								$responseOutput->errCode = STATUS_INVALID_VALUE;
								return $responseOutput;
							}
						}
						else
						{
							if ($minShutter >= 0 && $minShutter <= 13)
							{ //x60 ~ x2
								$responseOutput->errCode = STATUS_INVALID_VALUE;
								return $responseOutput;
							}
						}
					}
				}

				// If AGC Mode is Off or Manual then
				if ($_REQUEST['AGCMode'] == 'Off' || $_REQUEST['AGCMode'] == 'Manual')
				{
					// Set to Color if DayNightMode is in Auto
					if (isset($_REQUEST['DayNightMode']))
					{
						// Cant set DayNightMode in IR On mode
						if ($GLOBALS['M_SUPPORT_IR'] == 1)
						{
							// 0 => Off, 1 => On, 2 => DayNight, 3 => Sensor, 4 => Schedule
							$IRMode;
							
							if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ)
	                        {
	                        	$IRMode = $classInstances['ImageSetting']->imagePTZIR->dataInfo['Mode']['value'];
	                        }
	                        else
	                        {
								$IRMode = $classInstances['ImageSetting']->imageIR->dataInfo['Mode']['value'];
	                        }

							if($GLOBALS['M_SUPPORT_PTZ'] != PTZ_NOT_SUPPORT)
							{
		                        switch($IRMode)
		                        {
		                        	case 1:
		                        	case 3:
		                        	case 4:
		                        		$responseOutput->errCode = STATUS_INVALID_VALUE;
										return $responseOutput;
										break;
									case 2:
										if($_REQUEST['DayNightMode'] != "Auto")
										{
											$responseOutput->errCode = STATUS_INVALID_VALUE;
											return $responseOutput;
										}
										break;
		                        }
	                        }
	                        else
	                        {
	                        	if($_REQUEST['DayNightMode'] == "Auto")
	                        	{
	                        		$responseOutput->errCode = STATUS_INVALID_VALUE;
									return $responseOutput;
	                        	}
	                        }
                        }
                        
						if ($_REQUEST['DayNightMode'] == 'Auto')
						{
							$classInstances['ImageSetting']->imageSpecial->dataInfo['DayNightMode']['value'] = 0;
						}
					}
					else
					{
						if ($classInstances['ImageSetting']->imageSpecial->dataInfo['DayNightMode']['value'] == 2)
						{
							$classInstances['ImageSetting']->imageSpecial->dataInfo['DayNightMode']['value'] = 0;
						}
					}
				}

				$classInstances['ImageSetting']->imageExposure->dataInfo['AGCMode']['value'] = $newValue;
			}
			else if ($name == 'AGCLevel')
			{
				if ($GLOBALS['M_ISP_TYPE'] != ISP_TYPE_WN2_PTZ)
				{
					$responseOutput->errCode = STATUS_INVALID_PARAMETER;
					return $responseOutput;
				}
				if (isset($_REQUEST['AGCMode']))
				{
					if ($_REQUEST['AGCMode'] != 'Manual')
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				else
				{
					if ($classInstances['ImageSetting']->imageExposure->dataInfo['AGCMode']['value'] != 4)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				
				if ($_REQUEST['AGCLevel'] < 0 || $_REQUEST['AGCLevel'] > 42)
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				$classInstances['ImageSetting']->imageExposure->dataInfo['AGCLevel']['value'] = $_REQUEST['AGCLevel'];
			}
			else if ($name == 'DayNightMode')
			{
				// Cant set DayNightMode in IR On mode
				if ($GLOBALS['M_SUPPORT_IR'] == 1 && $GLOBALS['M_SUPPORT_PTZ'] != PTZ_NOT_SUPPORT)
				{
					// 0 => Off, 1 => On, 2 => DayNight, 3 => Sensor, 4 => Schedule
                    $IRMode = $classInstances['ImageSetting']->imagePTZIR->dataInfo['Mode']['value'];

                    switch($IRMode)
					{
	                    case 1:
	                    case 3:
	                    case 4:
	                    	$responseOutput->errCode = STATUS_INVALID_VALUE;
							return $responseOutput;
							break;
						case 2:
							if($_REQUEST['DayNightMode'] != "Auto")
							{
								$responseOutput->errCode = STATUS_INVALID_VALUE;
								return $responseOutput;
							}
							break;
	                }
				}

				if ($_REQUEST['DayNightMode'] == "Auto")
				{
					if (isset($_REQUEST['AGCMode']))
					{
						if ($_REQUEST['AGCMode'] == 'Off' || $_REQUEST['AGCMode'] == 'Manual')
						{
							$responseOutput->errCode = STATUS_INVALID_VALUE;
							return $responseOutput;
						}
					}
					else
					{
						if ($classInstances['ImageSetting']->imageExposure->dataInfo['AGCMode']['value'] == 0 ||
							$classInstances['ImageSetting']->imageExposure->dataInfo['AGCMode']['value'] == 4)
						{
							$responseOutput->errCode = STATUS_INVALID_VALUE;
							return $responseOutput;
						}
					}
				}

				$newValue = array_search($_REQUEST['DayNightMode'], $DayNightMode);
				if (is_bool($newValue))
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}

				$classInstances['ImageSetting']->imageSpecial->dataInfo['DayNightMode']['value'] = $newValue;
			}
			else if ($name == 'DayNightSwitchingMode')
			{
				if (isset($_REQUEST['DayNightMode']))
				{
					if ($_REQUEST['DayNightMode'] != 'Auto')
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				else
				{
					if ($classInstances['ImageSetting']->imageSpecial->dataInfo['DayNightMode']['value'] != 2)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}

				$newValue = array_search($_REQUEST['DayNightSwitchingMode'], $DayNightModeSwitchingMode);
				if (is_bool($newValue))
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				$classInstances['ImageSetting']->imageSpecial->dataInfo['DayNightDuration']['value'] = $newValue;
			}
			else if ($name == 'DayNightSwitchingTime')
			{
				if (isset($_REQUEST['DayNightMode']))
				{
					if ($_REQUEST['DayNightMode'] != 'Auto')
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				else
				{
					if ($classInstances['ImageSetting']->imageSpecial->dataInfo['DayNightMode']['value'] != 2)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}

				$newValue = array_search($_REQUEST['DayNightSwitchingTime'], $DayNightDwellTime);
				if (is_bool($newValue))
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				$classInstances['ImageSetting']->imageSpecial->dataInfo['DayNightDwellTime']['value'] = $newValue;
			}
			else if ($name == 'DayNightAlarmIn')
			{
				if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3)
				{
					if ($GLOBALS['M_ALARMIN_COUNT'] <= 0)
					{
						$responseOutput->errCode = STATUS_INVALID_PARAMETER;
						return $responseOutput;
					}
				}
				else
				{
					$responseOutput->errCode = STATUS_INVALID_PARAMETER;
					return $responseOutput;
				}

				if (isset($_REQUEST['DayNightMode']))
				{
					if ($_REQUEST['DayNightMode'] != 'ExternalBW')
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				else
				{
					if ($classInstances['ImageSetting']->imageSpecial->dataInfo['DayNightMode']['value'] != 3)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}

				$newValue = array_search($_REQUEST['DayNightAlarmIn'], $DayNightAlarmIn);
				if (is_bool($newValue))
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				$classInstances['ImageSetting']->imageSpecial->dataInfo['DayNightExtMode']['value'] = $newValue;
			}
			else if ($name == 'SimpleFocus')
			{
				if ($GLOBALS['M_SUPPORT_MOTORIZE'] != MOTORIZE_FOCUS_ONLY_SUPPORT)
				{
					$responseOutput->errCode = STATUS_INVALID_PARAMETER;
					return $responseOutput;
				}

				$newValue = array_search($_REQUEST['SimpleFocus'], $boolArray);
				if (is_bool($newValue))
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				$classInstances['ImageSetting']->imageSpecial->dataInfo['AutoFocusEnable']['value'] = $newValue;
			}
			else if ($name == 'DayNightModeSchedule_EveryDay' || $name == 'DayNightModeSchedule_SUN' || $name == 'DayNightModeSchedule_MON' || $name == 'DayNightModeSchedule_TUE' ||
				$name == 'DayNightModeSchedule_WED' || $name == 'DayNightModeSchedule_THU' || $name == 'DayNightModeSchedule_FRI' || $name == 'DayNightModeSchedule_SAT')
			{
				if ($GLOBALS['M_ISP_TYPE'] != ISP_TYPE_WN3 && $GLOBALS['M_ISP_TYPE'] != ISP_TYPE_HISILICON)
				{
					$responseOutput->errCode = STATUS_INVALID_PARAMETER;
					return $responseOutput;
				}
				if (isset($_REQUEST['DayNightMode']))
				{
					if ($_REQUEST['DayNightMode'] != 'Schedule')
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				else
				{
					if ($classInstances['ImageSetting']->imageSpecial->dataInfo['DayNightMode']['value'] != 4)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				if ($_REQUEST[$name] < 0 || $_REQUEST[$name] > 1)
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}

				if ($name == 'DayNightModeSchedule_EveryDay')
				{
					if ($_REQUEST['DayNightModeSchedule_EveryDay'] == 1)
					{
						if (isset($_REQUEST['DayNightModeSchedule_SUN']) || isset($_REQUEST['DayNightModeSchedule_MON']) ||
							isset($_REQUEST['DayNightModeSchedule_TUE']) || isset($_REQUEST['DayNightModeSchedule_WED']) ||
							isset($_REQUEST['DayNightModeSchedule_THU']) || isset($_REQUEST['DayNightModeSchedule_FRI']) ||
							isset($_REQUEST['DayNightModeSchedule_SAT']))
						{
							$responseOutput->errCode = STATUS_INVALID_PARAMETER;
							//$responseOutput->outputMsg .= 'EveryDay is Set';
							return $responseOutput;
						}
					}
					else
					{
						if (isset($_REQUEST['DayNightModeSchedule_EveryDay']))
						{
							if ($_REQUEST['DayNightModeSchedule_EveryDay'] != 0)
							{
								$responseOutput->errCode = STATUS_INVALID_VALUE;
								//$responseOutput->outputMsg .= 'EveryDay is on';
								return $responseOutput;
							}
						}
						else
						{
							if ($classInstances['ImageSetting']->imageDayNightSchedule->schedule[0]->dataInfo['Enable']['value'] != 0)
							{
								$responseOutput->errCode = STATUS_INVALID_VALUE;
								//$responseOutput->outputMsg .= 'EveryDay is off';
								return $responseOutput;
							}
						}
					}
				}

				if ($_REQUEST[$name] == 1)
				{
					$tempTovalue = split("-", $_REQUEST[$name . '_FromTo']);

					$tempFrom = split(":", $tempTovalue[0]);
					$tempTo = split(":", $tempTovalue[1]);


					if ($tempFrom[0] < 0 && $tempFrom[0] > 23)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
					else if ($tempTo[0] < 0 && $tempTo[0] > 23)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
					else if ($tempFrom[1] < 0 && $tempFrom[1] > 59)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
					else if ($tempTo[1] < 0 && $tempTo[1] > 59)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
					else if ($tempFrom[0] > $tempTo[0])
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
					else if ($tempFrom[0] == $tempTo[0])
					{
						if ($tempFrom[1] > $tempTo[1])
						{
							$responseOutput->errCode = STATUS_INVALID_VALUE;
							return $responseOutput;
						}
					}
				}
				else if ($_REQUEST[$name] == 0)
				{
					if (isset($_REQUEST[$name . '_FromTo']))
					{
						$responseOutput->errCode = STATUS_INVALID_PARAMETER;
						return $responseOutput;
					}
				}
				else
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}


				$classInstances['ImageSetting']->$data['target']->schedule[$data['index']]->dataInfo['Enable']['value'] = $_REQUEST[$name];

				if ($_REQUEST[$name] == 1)
				{
					$tempTovalue = split("-", $_REQUEST[$name . '_FromTo']);

					$tempFrom = split(":", $tempTovalue[0]);
					$tempTo = split(":", $tempTovalue[1]);

					$classInstances['ImageSetting']->$data['target']->schedule[$data['index']]->dataInfo['StartHour']['value'] = $tempFrom[0];
					$classInstances['ImageSetting']->$data['target']->schedule[$data['index']]->dataInfo['StartMin']['value'] = $tempFrom[1];
					$classInstances['ImageSetting']->$data['target']->schedule[$data['index']]->dataInfo['EndHour']['value'] = $tempTo[0];
					$classInstances['ImageSetting']->$data['target']->schedule[$data['index']]->dataInfo['EndMin']['value'] = $tempTo[1];
				}
			}
		}

		if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ)
		{
			// For PTZ models, the BLCAreaTop, BLCAreaBottom, BLCAreaRight, and BLCAreaLeft parameters cannot be set altogether
			// Only one of them can be set at a time.
			if ($blcBoxInputCountForPtz >= 2)
			{
				$responseOutput->errCode = STATUS_INVALID_PARAMETER;
				return $responseOutput;
			}
			
			if ($classInstances['ImageSetting']->testCmd == 1)
			{
				$classInstances['ImageSetting']->imageBackLight->dataInfo['BLCDisplay']['value'] = 1;

				$classInstances['ImageSetting']->imageSSDR->payload = MakePayload($classInstances['ImageSetting']->imageSSDR->dataInfo);
				$classInstances['ImageSetting']->imageWhiteBalance->payload = MakePayload($classInstances['ImageSetting']->imageWhiteBalance->dataInfo);
				$classInstances['ImageSetting']->imageBackLight->payload = MakePayload($classInstances['ImageSetting']->imageBackLight->dataInfo);
				$classInstances['ImageSetting']->imageExposure->payload = MakePayload($classInstances['ImageSetting']->imageExposure->dataInfo);
				$classInstances['ImageSetting']->imageSpecial->payload = MakePayload($classInstances['ImageSetting']->imageSpecial->dataInfo);
				$classInstances['ImageSetting']->imageIR->payload = MakePayload($classInstances['ImageSetting']->imageIR->dataInfo);
				$classInstances['ImageSetting']->imageOSD->payload = MakePayload($classInstances['ImageSetting']->imageOSD->dataInfo);
				$classInstances['ImageSetting']->imageDayNightSchedule->SetPayload();
				$classInstances['ImageSetting']->imagePreset->SetPayload();
				$classInstances['ImageSetting']->headerInfo['Action'] = ACTION_SET;
				$classInstances['ImageSetting']->SetPayload();
				$GLOBALS['SOCKET_MANAGER']->Connection($classInstances['ImageSetting']);
				
				$classInstances['ImageSetting']->imageBackLight->dataInfo['BLCTop']['value'] = $blcTopDelta;
				$classInstances['ImageSetting']->imageBackLight->dataInfo['BLCBottom']['value'] = $blcBottomDelta;
				$classInstances['ImageSetting']->imageBackLight->dataInfo['BLCLeft']['value'] = $blcLeftDelta;
				$classInstances['ImageSetting']->imageBackLight->dataInfo['BLCRight']['value'] = $blcRightDelta;
				//if ($blcTopDelta || $blcBottomDelta || $blcLeftDelta || $blcRightDelta)
				//{
					$classInstances['ImageSetting']->imageBackLight->payload = MakePayload($classInstances['ImageSetting']->imageBackLight->dataInfo);
					$classInstances['ImageSetting']->SetPayload();
					$GLOBALS['SOCKET_MANAGER']->Connection($classInstances['ImageSetting']);
				//}

				$classInstances['ImageSetting']->imageBackLight->dataInfo['BLCDisplay']['value'] = 0;
				$classInstances['ImageSetting']->testCmd = 0;
				$classInstances['ImageSetting']->imageBackLight->dataInfo['BLCTop']['value'] = 0;
				$classInstances['ImageSetting']->imageBackLight->dataInfo['BLCLeft']['value'] = 0;
				$classInstances['ImageSetting']->imageBackLight->dataInfo['BLCRight']['value'] = 0;
				$classInstances['ImageSetting']->imageBackLight->dataInfo['BLCBottom']['value'] = 0;
			}
		}

		$classInstances['ImageSetting']->imageSSDR->payload = MakePayload($classInstances['ImageSetting']->imageSSDR->dataInfo);
		$classInstances['ImageSetting']->imageWhiteBalance->payload = MakePayload($classInstances['ImageSetting']->imageWhiteBalance->dataInfo);
		$classInstances['ImageSetting']->imageBackLight->payload = MakePayload($classInstances['ImageSetting']->imageBackLight->dataInfo);
		$classInstances['ImageSetting']->imageExposure->payload = MakePayload($classInstances['ImageSetting']->imageExposure->dataInfo);
		$classInstances['ImageSetting']->imageSpecial->payload = MakePayload($classInstances['ImageSetting']->imageSpecial->dataInfo);
		$classInstances['ImageSetting']->imageIR->payload = MakePayload($classInstances['ImageSetting']->imageIR->dataInfo);
		$classInstances['ImageSetting']->imageOSD->payload = MakePayload($classInstances['ImageSetting']->imageOSD->dataInfo);
		$classInstances['ImageSetting']->imageDayNightSchedule->SetPayload();
		$classInstances['ImageSetting']->imagePreset->SetPayload();
		$classInstances['ImageSetting']->headerInfo['Action'] = ACTION_SET;
		$classInstances['ImageSetting']->SetPayload();
		$GLOBALS['SOCKET_MANAGER']->Connection($classInstances['ImageSetting']);

		$responseOutput->errCode = STATUS_OK;
		$responseOutput->outputMsg .= 'OK';
		return $responseOutput;
	}
	else if ($_REQUEST['action'] == 'view')
	{
		$responseOutput->outputMsg .= 'Channel.0.CompensationMode=' . $CompensationMode[$classInstances['ImageSetting']->imageBackLight->dataInfo['Mode']['value']] . "\r\n";
		$responseOutput->outputMsg .= 'Channel.0.BLCLevel=' . $BLCLevel[$classInstances['ImageSetting']->imageBackLight->dataInfo['BLCLevel']['value']] . "\r\n";
		if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3 || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_HISILICON)
		{
			$responseOutput->outputMsg .= 'Channel.0.BLCAreaTop=' . $classInstances['ImageSetting']->imageBackLight->dataInfo['BLCTop']['value'] . "\r\n";
			$responseOutput->outputMsg .= 'Channel.0.BLCAreaBottom=' . $classInstances['ImageSetting']->imageBackLight->dataInfo['BLCBottom']['value'] . "\r\n";
			$responseOutput->outputMsg .= 'Channel.0.BLCAreaLeft=' . $classInstances['ImageSetting']->imageBackLight->dataInfo['BLCLeft']['value'] . "\r\n";
			$responseOutput->outputMsg .= 'Channel.0.BLCAreaRight=' . $classInstances['ImageSetting']->imageBackLight->dataInfo['BLCRight']['value'] . "\r\n";
		}
		else // ISP_TYPE_WN2_PTZ || ISP_TYPE_WN3_PTZ
		{
			$responseOutput->outputMsg .= 'Channel.0.BLCAreaTop=' . $classInstances['ImageSetting']->imageBackLight->dataInfo['CoordBlcTop']['value'] . "\r\n";
			$responseOutput->outputMsg .= 'Channel.0.BLCAreaBottom=' . $classInstances['ImageSetting']->imageBackLight->dataInfo['CoordBlcBottom']['value'] . "\r\n";
			$responseOutput->outputMsg .= 'Channel.0.BLCAreaLeft=' . $classInstances['ImageSetting']->imageBackLight->dataInfo['CoordBlcLeft']['value'] . "\r\n";
			$responseOutput->outputMsg .= 'Channel.0.BLCAreaRight=' . $classInstances['ImageSetting']->imageBackLight->dataInfo['CoordBlcRight']['value'] . "\r\n";
		}
		if (($GLOBALS['M_SUPPORT_BACKLIGHT'] & BACKLIGHT_MASK_HLC) == BACKLIGHT_MASK_HLC)
		{
			$responseOutput->outputMsg .= 'Channel.0.HLCLevel=' . $HLCLevel[$classInstances['ImageSetting']->imageBackLight->dataInfo['HLCLevel']['value']] . "\r\n";
			$responseOutput->outputMsg .= 'Channel.0.HLCMaskTone=' . $classInstances['ImageSetting']->imageBackLight->dataInfo['HLCMasktone']['value'] . "\r\n";
		}

		if (($GLOBALS['M_SUPPORT_BACKLIGHT'] & BACKLIGHT_MASK_WDR) == BACKLIGHT_MASK_WDR)
		{
			$responseOutput->outputMsg .= 'Channel.0.WDRLevel=' . $WDRLevel[$classInstances['ImageSetting']->imageBackLight->dataInfo['WDRLevel']['value']] . "\r\n";
		}

		//$responseOutput->outputMsg .= 'Channel.0.ShutterMode=' . $ShutterMode[$classInstances['ImageSetting']->imageExposure->dataInfo['ShutterMode']['value']] ."\r\n";
		$responseOutput->outputMsg .= 'Channel.0.AutoShortShutterSpeed=' . $ShutterSpeed[$classInstances['ImageSetting']->imageExposure->dataInfo['LongShutterSpeed']['value']] . "\r\n";
		$responseOutput->outputMsg .= 'Channel.0.AutoLongShutterSpeed=' . $ShutterSpeed[$classInstances['ImageSetting']->imageExposure->dataInfo['ShortShutterSpeed']['value']] . "\r\n";
		//if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3)
		{
			$responseOutput->outputMsg .= 'Channel.0.AFLKMode=' . $AFLKMode[$classInstances['ImageSetting']->imageExposure->dataInfo['UseAFLK']['value']] . "\r\n";
		}
		$responseOutput->outputMsg .= 'Channel.0.SSNREnable=' . $boolArray[$classInstances['ImageSetting']->imageExposure->dataInfo['SSNRMode']['value']] . "\r\n";
		$responseOutput->outputMsg .= 'Channel.0.SSNRLevel=' . $classInstances['ImageSetting']->imageExposure->dataInfo['SSNRLevel']['value'] . "\r\n";

		//if ($GLOBALS['M_SUPPORT_IRIS'] != 0)
		if ($GLOBALS['M_SUPPORT_IRIS'] & IRIS_SUPPORT)
		{
			$responseOutput->outputMsg .= 'Channel.0.IrisMode=' . $IrisMode[$classInstances['ImageSetting']->imageExposure->dataInfo['IrisMode']['value']] . "\r\n";
		}

		//if ($GLOBALS['M_SUPPORT_IRIS'] & DOME_PIRIS_SUPPORT)
		if ($GLOBALS['M_SUPPORT_IRIS'] & PIRIS_SUPPORT)
		{
			$responseOutput->outputMsg .= 'Channel.0.PIrisMode=' . $PIrisMode[$classInstances['ImageSetting']->imageExposure->dataInfo['PIrisMode']['value']] . "\r\n";
			$responseOutput->outputMsg .= 'Channel.0.PIrisPosition=' . $classInstances['ImageSetting']->imageExposure->dataInfo['PIrisPosition']['value'] . "\r\n";
		}
		if (($GLOBALS['M_SUPPORT_IRIS'] & IRIS_FNO_SUPPORT) == IRIS_FNO_SUPPORT)
		{
			$responseOutput->outputMsg .= 'Channel.0.IrisFno=' . $IrisFno[$classInstances['ImageSetting']->imageExposure->dataInfo['PIrisFno']['value']] . "\r\n";
		}

		$responseOutput->outputMsg .= 'Channel.0.AGCMode=' . $AGCMode[$classInstances['ImageSetting']->imageExposure->dataInfo['AGCMode']['value']] . "\r\n";
		if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ)
		{
			$responseOutput->outputMsg .= 'Channel.0.AGCLevel=' . $classInstances['ImageSetting']->imageExposure->dataInfo['AGCLevel']['value'] . "\r\n";
		}
		$responseOutput->outputMsg .= 'Channel.0.DayNightMode=' . $DayNightMode[$classInstances['ImageSetting']->imageSpecial->dataInfo['DayNightMode']['value']] . "\r\n";
		$responseOutput->outputMsg .= 'Channel.0.DayNightSwitchingTime=' . $DayNightDwellTime[$classInstances['ImageSetting']->imageSpecial->dataInfo['DayNightDwellTime']['value']] . "\r\n";
		$responseOutput->outputMsg .= 'Channel.0.DayNightSwitchingMode=' . $DayNightModeSwitchingMode[$classInstances['ImageSetting']->imageSpecial->dataInfo['DayNightDuration']['value']] . "\r\n";

		if ($GLOBALS['M_SUPPORT_MOTORIZE'] == MOTORIZE_FOCUS_ONLY_SUPPORT)
		{
			$responseOutput->outputMsg .= 'Channel.0.SimpleFocus=' . $boolArray[$classInstances['ImageSetting']->imageSpecial->dataInfo['AutoFocusEnable']['value']] . "\r\n";
		}

		if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3 && $GLOBALS['M_ALARMIN_COUNT'] > 0)
		{
			$responseOutput->outputMsg .= 'Channel.0.DayNightAlarmIn=' . $DayNightAlarmIn[$classInstances['ImageSetting']->imageSpecial->dataInfo['DayNightExtMode']['value']] . "\r\n";
		}

		// If Day night Mode is schedule
		if ($DayNightMode[$classInstances['ImageSetting']->imageSpecial->dataInfo['DayNightMode']['value']] == 'Schedule')
		{
			$time_array = array('EveryDay', 'SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT');
			for ($index = 0; $index < 8; $index++)
			{
				$responseOutput->outputMsg .= 'Channel.0.DayNightModeSchedule.' . $time_array[$index];
				$responseOutput->outputMsg .= '=' . $classInstances['ImageSetting']->imageDayNightSchedule->schedule[$index]->dataInfo['Enable']['value'] . "\r\n";

				//To take care of HH:MM format
				if ($classInstances['ImageSetting']->imageDayNightSchedule->schedule[$index]->dataInfo['StartHour']['value'] < 10)
				{
					$responseOutput->outputMsg .= 'Channel.0.DayNightModeSchedule.' . $time_array[$index] . '.FromTo=0' . $classInstances['ImageSetting']->imageDayNightSchedule->schedule[$index]->dataInfo['StartHour']['value'];
				}
				else
				{
					$responseOutput->outputMsg .= 'Channel.0.DayNightModeSchedule.' . $time_array[$index] . '.FromTo=' . $classInstances['ImageSetting']->imageDayNightSchedule->schedule[$index]->dataInfo['StartHour']['value'];
				}
				if ($classInstances['ImageSetting']->imageDayNightSchedule->schedule[$index]->dataInfo['StartMin']['value'] < 10)
				{
					$responseOutput->outputMsg .= ':0' . $classInstances['ImageSetting']->imageDayNightSchedule->schedule[$index]->dataInfo['StartMin']['value'];
				}
				else
				{
					$responseOutput->outputMsg .= ':' . $classInstances['ImageSetting']->imageDayNightSchedule->schedule[$index]->dataInfo['StartMin']['value'];
				}
				if ($classInstances['ImageSetting']->imageDayNightSchedule->schedule[$index]->dataInfo['EndHour']['value'] < 10)
				{
					$responseOutput->outputMsg .= '-0' . $classInstances['ImageSetting']->imageDayNightSchedule->schedule[$index]->dataInfo['EndHour']['value'];
				}
				else
				{
					$responseOutput->outputMsg .= '-' . $classInstances['ImageSetting']->imageDayNightSchedule->schedule[$index]->dataInfo['EndHour']['value'];
				}
				if ($classInstances['ImageSetting']->imageDayNightSchedule->schedule[$index]->dataInfo['EndMin']['value'] < 10)
				{
					$responseOutput->outputMsg .= ':0' . $classInstances['ImageSetting']->imageDayNightSchedule->schedule[$index]->dataInfo['EndMin']['value'] . "\r\n";
				}
				else
				{
					$responseOutput->outputMsg .= ':' . $classInstances['ImageSetting']->imageDayNightSchedule->schedule[$index]->dataInfo['EndMin']['value'] . "\r\n";
				}
			}
		}

		$responseOutput->errCode = STATUS_OK;
		return $responseOutput;
	}
	else
	{
		$responseOutput->errCode = STATUS_ACTION_NOT_FOUND;
		//$responseOutput->outputMsg .= 'Invalid Action';
		return $responseOutput;
	}
}

function submenu_imagepreset()
{
	CheckAdminAccount(FALSE);
	$responseOutput = new ResponseOutput();

	$ImagePresetMode = array(
		0 => 'Off',
		1 => 'DefinitionFocus',
		2 => 'MotionFocus',
		3 => 'ReducedNoise',
		4 => 'BrightVideo',
		5 => 'MotionFocus+ReducedNoise',
		6 => 'MotionFocus+BrightVideo',
		7 => 'UserPreset'
	);
	global $boolArray;

	if ($_REQUEST['Channel'] != 0)
	{
		$responseOutput->errCode = STATUS_INVALID_VALUE;
		return $responseOutput;
	}

	$classInstances = GetClassInstance('image');

	if ($_REQUEST['action'] == 'set')
	{
		if (count($_GET) < 3)
		{
			$responseOutput->errCode = STATUS_MISSING_PARAMETER;
			return $responseOutput;
		}
		foreach ($_REQUEST as $name => $value)
		{
			switch ($name)
			{
				case 'Mode':
					{
						if ($_REQUEST['Mode'] == "MotionFocus ReducedNoise")
						{
							$classInstances["ImageSetting"]->imagePreset->dataInfo['DefaultMode']['value'] = 5;
						}
						else if ($_REQUEST['Mode'] == "MotionFocus BrightVideo")
						{
							$classInstances["ImageSetting"]->imagePreset->dataInfo['DefaultMode']['value'] = 6;
						}
						else
						{
							unset($ImagePresetMode[0]);
							$newValue = array_search($_REQUEST['Mode'], $ImagePresetMode);
							if (is_bool($newValue))
							{
								$responseOutput->errCode = STATUS_INVALID_VALUE;
								return $responseOutput;
							}
							$classInstances["ImageSetting"]->imagePreset->dataInfo['DefaultMode']['value'] = $newValue;
						}
					}
					break;
				case 'ScheduleEnable':
					{
						$newValue = array_search($_REQUEST['ScheduleEnable'], $boolArray);
						if (is_bool($newValue))
						{
							$responseOutput->errCode = STATUS_INVALID_VALUE;
							return $responseOutput;
						}
						$classInstances["ImageSetting"]->imagePreset->dataInfo['ScheduleMode']['value'] = $newValue;
					}
					break;
				case 'Schedule_1_EveryDay_FromTo':
				case 'Schedule_2_EveryDay_FromTo':
				case 'Schedule_3_EveryDay_FromTo':
				case 'Schedule_4_EveryDay_FromTo':
				case 'Schedule_5_EveryDay_FromTo':
				case 'Schedule_1_Mode':
				case 'Schedule_2_Mode':
				case 'Schedule_3_Mode':
				case 'Schedule_4_Mode':
				case 'Schedule_5_Mode':
					{
						if (isset($_REQUEST['ScheduleEnable']))
						{
							$newValue = array_search($_REQUEST['ScheduleEnable'], $boolArray);
							if ($newValue != 1)
							{
								$responseOutput->errCode = STATUS_INVALID_VALUE;
								return $responseOutput;
							}
						}
						else
						{
							if ($classInstances["ImageSetting"]->imagePreset->dataInfo['ScheduleMode']['value'] != 1)
							{
								$responseOutput->errCode = STATUS_INVALID_VALUE;
								return $responseOutput;
							}
						}

						for ($index = 1; $index <= 5; $index++)
						{
							if (isset($_REQUEST['Schedule_' . $index . '_Mode']))
							{
								// Schedule.#.Mode : Off -> Scheduled : Schedule.#.EveryDay.FromTo should come together
//								if ($classInstances["ImageSetting"]->imagePreset->schedule[$index - 1]->dataInfo['Mode']['value'] == 0 &&
//									$_REQUEST['Schedule_' . $index . '_Mode'] != "Off" &&
//									!isset($_REQUEST['Schedule_' . $index . '_EveryDay_FromTo']))
//								{
//									$responseOutput->errCode = STATUS_MISSING_PARAMETER;
//									return $responseOutput;
//								}
								if ($_REQUEST['Schedule_' . $index . '_Mode'] == "MotionFocus BrightVideo")
								{
									$classInstances["ImageSetting"]->imagePreset->schedule[$index - 1]->dataInfo['Mode']['value'] = 6;
								}
								else if ($_REQUEST['Schedule_' . $index . '_Mode'] == "MotionFocus ReducedNoise")
								{
									$classInstances["ImageSetting"]->imagePreset->schedule[$index - 1]->dataInfo['Mode']['value'] = 5;
								}
								else
								{
									$newValue = array_search($_REQUEST['Schedule_' . $index . '_Mode'], $ImagePresetMode);
									if (is_bool($newValue))
									{
										$responseOutput->errCode = STATUS_INVALID_VALUE;
										return $responseOutput;
									}
									$classInstances["ImageSetting"]->imagePreset->schedule[$index - 1]->dataInfo['Mode']['value'] = $newValue;
								}
							}
							
							if (isset($_REQUEST['Schedule_' . $index . '_EveryDay_FromTo']))
							{
								$tempTovalue = split("-", $_REQUEST['Schedule_' . $index . '_EveryDay_FromTo']);

								$tempFrom = split(":", $tempTovalue[0]);
								$tempTo = split(":", $tempTovalue[1]);

								if ($tempFrom[0] < 0 && $tempFrom[0] > 23)
								{
									$responseOutput->errCode = STATUS_INVALID_VALUE;
									return $responseOutput;
								}
								else if ($tempTo[0] < 0 && $tempTo[0] > 23)
								{
									$responseOutput->errCode = STATUS_INVALID_VALUE;
									return $responseOutput;
								}
								else if ($tempFrom[1] < 0 && $tempFrom[1] > 59)
								{
									$responseOutput->errCode = STATUS_INVALID_VALUE;
									return $responseOutput;
								}
								else if ($tempTo[1] < 0 && $tempTo[1] > 59)
								{
									$responseOutput->errCode = STATUS_INVALID_VALUE;
									return $responseOutput;
								}
								else if ($tempFrom[0] > $tempTo[0])
								{
									$responseOutput->errCode = STATUS_INVALID_VALUE;
									return $responseOutput;
								}
								else if ($tempFrom[0] == $tempTo[0])
								{
									if ($tempFrom[1] > $tempTo[1])
									{
										$responseOutput->errCode = STATUS_INVALID_VALUE;
										return $responseOutput;
									}
								}
								$classInstances["ImageSetting"]->imagePreset->schedule[$index - 1]->dataInfo['StartHour']['value'] = $tempFrom[0];
								$classInstances["ImageSetting"]->imagePreset->schedule[$index - 1]->dataInfo['StartMin']['value'] = $tempFrom[1];
								$classInstances["ImageSetting"]->imagePreset->schedule[$index - 1]->dataInfo['EndHour']['value'] = $tempTo[0];
								$classInstances["ImageSetting"]->imagePreset->schedule[$index - 1]->dataInfo['EndMin']['value'] = $tempTo[1];
							}
						}
					}
					break;
			}
		}
		
		// CheckImagePresetSchedule()
		{
			$schedule = $classInstances["ImageSetting"]->imagePreset->schedule;
			for ($index = 0; $index < 5; $index++)
			{
				$selMode = $schedule[$index]->dataInfo['Mode']['value'];
				if($selMode == 0) continue;
				
				$startHour = $schedule[$index]->dataInfo['StartHour']['value'];
				$startMin = $schedule[$index]->dataInfo['StartMin']['value'];
				$endHour = $schedule[$index]->dataInfo['EndHour']['value'];
				$endMin = $schedule[$index]->dataInfo['EndMin']['value'];
				
				$baseStartTime = strtotime(sprintf("2000-01-01 %02d:%02d", $startHour, $startMin));
				$baseEndTime = strtotime(sprintf("2000-01-01 %02d:%02d", $endHour, $endMin));
				
				if ($baseStartTime > $baseEndTime)
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				
				for ($index2 = 0; $index2 < 5; ++$index2)
				{
					$nextSelMode = $schedule[$index2]->dataInfo['Mode']['value'];
					if($index2 == $index || $nextSelMode == 0) continue;
					
					$tempStartHour = $schedule[$index2]->dataInfo['StartHour']['value'];
					$tempStartMin = $schedule[$index2]->dataInfo['StartMin']['value'];
					$tempEndHour = $schedule[$index2]->dataInfo['EndHour']['value'];
					$tempEndMin = $schedule[$index2]->dataInfo['EndMin']['value'];
					
					$compareStartTime = strtotime(sprintf("2000-01-01 %02d:%02d", $tempStartHour, $tempStartMin));
					$compareEndTime = strtotime(sprintf("2000-01-01 %02d:%02d", $tempEndHour, $tempEndMin));
					
					if (($baseStartTime <= $compareStartTime && $compareStartTime <= $baseEndTime) || ($baseStartTime <= $compareEndTime && $compareEndTime <= $baseEndTime))
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}

					if (($compareStartTime <= $baseStartTime && $baseStartTime <= $compareEndTime) || ($compareStartTime <= $baseEndTime && $baseEndTime <= $compareEndTime))
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
			}
		}
		
		$classInstances['ImageSetting']->imageSSDR->payload = MakePayload($classInstances['ImageSetting']->imageSSDR->dataInfo);
		$classInstances['ImageSetting']->imageWhiteBalance->payload = MakePayload($classInstances['ImageSetting']->imageWhiteBalance->dataInfo);
		$classInstances['ImageSetting']->imageBackLight->payload = MakePayload($classInstances['ImageSetting']->imageBackLight->dataInfo);
		$classInstances['ImageSetting']->imageExposure->payload = MakePayload($classInstances['ImageSetting']->imageExposure->dataInfo);
		$classInstances['ImageSetting']->imageSpecial->payload = MakePayload($classInstances['ImageSetting']->imageSpecial->dataInfo);
		$classInstances['ImageSetting']->imageIR->payload = MakePayload($classInstances['ImageSetting']->imageIR->dataInfo);
		$classInstances['ImageSetting']->imageOSD->payload = MakePayload($classInstances['ImageSetting']->imageOSD->dataInfo);
		$classInstances['ImageSetting']->imageDayNightSchedule->SetPayload();
		$classInstances['ImageSetting']->imagePreset->SetPayload();
		$classInstances['ImageSetting']->headerInfo['Action'] = ACTION_SET;
		$classInstances['ImageSetting']->SetPayload();
		$GLOBALS['SOCKET_MANAGER']->Connection($classInstances['ImageSetting']);

		$responseOutput->errCode = STATUS_OK;
		$responseOutput->outputMsg .= 'OK';
		return $responseOutput;
	}
	else if ($_REQUEST['action'] == 'view')
	{
		$responseOutput->outputMsg .= 'Channel.0.Mode=' . $ImagePresetMode[$classInstances["ImageSetting"]->imagePreset->dataInfo['DefaultMode']['value']] . "\r\n";
		$responseOutput->outputMsg .= 'Channel.0.ScheduleEnable=' . $boolArray[$classInstances["ImageSetting"]->imagePreset->dataInfo['ScheduleMode']['value']] . "\r\n";
		for ($index = 1; $index <= 5; $index++)
		{
			$responseOutput->outputMsg .= 'Channel.0.Schedule.' . $index . '.Mode=' . $ImagePresetMode[$classInstances["ImageSetting"]->imagePreset->schedule[$index - 1]->dataInfo['Mode']['value']] . "\r\n";

			//To take care of HH:MM format
			$schedule_temp = "";
			//if ($classInstances["ImageSetting"]->imagePreset->schedule[$index - 1]->dataInfo['Mode']['value'] != 0)
			{
				if ($classInstances["ImageSetting"]->imagePreset->schedule[$index - 1]->dataInfo['StartHour']['value'] < 10)
				{
					$schedule_temp = '0' . $classInstances["ImageSetting"]->imagePreset->schedule[$index - 1]->dataInfo['StartHour']['value'];
				}
				else
				{
					$schedule_temp = $classInstances["ImageSetting"]->imagePreset->schedule[$index - 1]->dataInfo['StartHour']['value'];
				}

				if ($classInstances["ImageSetting"]->imagePreset->schedule[$index - 1]->dataInfo['StartMin']['value'] < 10)
				{
					$schedule_temp .= ':0' . $classInstances["ImageSetting"]->imagePreset->schedule[$index - 1]->dataInfo['StartMin']['value'];
				}
				else
				{
					$schedule_temp .= ':' . $classInstances["ImageSetting"]->imagePreset->schedule[$index - 1]->dataInfo['StartMin']['value'];
				}

				if ($classInstances["ImageSetting"]->imagePreset->schedule[$index - 1]->dataInfo['EndHour']['value'] < 10)
				{
					$schedule_temp .= '-0' . $classInstances["ImageSetting"]->imagePreset->schedule[$index - 1]->dataInfo['EndHour']['value'];
				}
				else
				{
					$schedule_temp .= '-' . $classInstances["ImageSetting"]->imagePreset->schedule[$index - 1]->dataInfo['EndHour']['value'];
				}

				if ($classInstances["ImageSetting"]->imagePreset->schedule[$index - 1]->dataInfo['EndMin']['value'] < 10)
				{
					$schedule_temp .= ':0' . $classInstances["ImageSetting"]->imagePreset->schedule[$index - 1]->dataInfo['EndMin']['value'];
				}
				else
				{
					$schedule_temp .= ':' . $classInstances["ImageSetting"]->imagePreset->schedule[$index - 1]->dataInfo['EndMin']['value'];
				}
			}
			
			$responseOutput->outputMsg .= 'Channel.0.Schedule.' . $index . '.EveryDay.FromTo=' . $schedule_temp . "\r\n";
		}
		$responseOutput->errCode = STATUS_OK;
		return $responseOutput;
	}
	else
	{
		$responseOutput->errCode = STATUS_ACTION_NOT_FOUND;
		return $responseOutput;
	}
}

///////////////////////////////////////////////
// SmartCodec 
///////////////////////////////////////////////
function submenu_smartcodec()
{
	CheckAdminAccount(FALSE);
	$responseOutput = new ResponseOutput();
	//  global $boolArray;

	$SmartCodecMode = array(
		0 => 'FaceDetection',
		1 => 'Manual'
	);

	$Quality = array(
		1 => 'Low',
		2 => 'Medium',
		3 => 'High'
	);

	if ($_REQUEST['Channel'] != 0)
	{
		$responseOutput->errCode = STATUS_INVALID_VALUE;
		return $responseOutput;
	}

	$classInstances = GetClassInstance('smartcodec');
	$fdConf = $classInstances['FDConfiguration'];

	if ($_REQUEST['action'] == 'set')
	{
		if (count($_REQUEST) < 3)
		{
			$responseOutput->errCode = STATUS_MISSING_PARAMETER;
			return $responseOutput;
		}

		foreach ($_REQUEST as $name => $value)
		{
			switch ($name)
			{
				case 'Mode':
					{
						$newValue = array_search($_REQUEST['Mode'], $SmartCodecMode);
						if (is_bool($newValue))
						{
							$responseOutput->errCode = STATUS_INVALID_VALUE;
							return $responseOutput;
						}
						if ($fdConf->dataInfo['Enabled']['value'] == 0 && $newValue == 0)
						{
							$responseOutput->errCode = STATUS_INVALID_VALUE;
							return $responseOutput;
						}
						$classInstances['SmartCodecConfiguration']->dataInfo['Mode']['value'] = $newValue;
					}
					break;
				case 'QualityLevel':
					{
						$newValue = array_search($_REQUEST['QualityLevel'], $Quality);
						if (is_bool($newValue))
						{
							$responseOutput->errCode = STATUS_INVALID_VALUE;
							return $responseOutput;
						}
						$classInstances['SmartCodecConfiguration']->dataInfo['QualityLevel']['value'] = $newValue;
					}
					break;
			}
		}
		$classInstances['SmartCodecConfiguration']->SetPayload();
		$classInstances['SmartCodecConfiguration']->headerInfo['Action'] = ACTION_SET;
		$GLOBALS['SOCKET_MANAGER']->Connection($classInstances['SmartCodecConfiguration']);

		$responseOutput->errCode = STATUS_OK;
		$responseOutput->outputMsg .= 'OK';
		return $responseOutput;
	}
	else if ($_REQUEST['action'] == 'add')
	{
		foreach ($_REQUEST as $name => $value)
		{
			switch ($name)
			{
				case 'Area_1_Coordinate':
				case 'Area_2_Coordinate':
				case 'Area_3_Coordinate':
				case 'Area_4_Coordinate':
				case 'Area_5_Coordinate':
					{
						if (isset($_REQUEST['Mode']) && $SmartCodecMode[$_REQUEST['Mode']] != 1)
						{
							$responseOutput->errCode = STATUS_INVALID_VALUE;
							return $responseOutput;
						}
						else
						{
							if ($classInstances['SmartCodecConfiguration']->dataInfo['Mode']['value'] != 1)
							{
								$responseOutput->errCode = STATUS_INVALID_VALUE;
								return $responseOutput;
							}
						}

						$areaIndex = ((int) substr($name, -12)) - 1;
						$areaData = explode(",", $_REQUEST[$name]);

						if (count($areaData) != 4)
						{
							$responseOutput->errCode = STATUS_INVALID_VALUE;
							return $responseOutput;
						}
						$classInstances['SmartCodecConfiguration']->smartCodecArea[$areaIndex]->dataInfo['Enabled']['value'] = 1;
						$classInstances['SmartCodecConfiguration']->smartCodecArea[$areaIndex]->dataInfo['AreaLeft']['value'] = $areaData[0];
						$classInstances['SmartCodecConfiguration']->smartCodecArea[$areaIndex]->dataInfo['AreaTop']['value'] = $areaData[1];
						$classInstances['SmartCodecConfiguration']->smartCodecArea[$areaIndex]->dataInfo['AreaRight']['value'] = $areaData[2];
						$classInstances['SmartCodecConfiguration']->smartCodecArea[$areaIndex]->dataInfo['AreaBottom']['value'] = $areaData[3];
						$classInstances['SmartCodecConfiguration']->smartCodecArea[$areaIndex]->payload = MakePayload($classInstances['SmartCodecConfiguration']->smartCodecArea[$areaIndex]->dataInfo);
					}
					break;
			}
		}

		$classInstances['SmartCodecConfiguration']->SetPayload();
		$classInstances['SmartCodecConfiguration']->headerInfo['Action'] = ACTION_SET;
		$GLOBALS['SOCKET_MANAGER']->Connection($classInstances['SmartCodecConfiguration']);

		$responseOutput->errCode = STATUS_OK;
		$responseOutput->outputMsg .= 'OK';
		return $responseOutput;
	}
	else if ($_REQUEST['action'] == 'remove')
	{
		if (!isset($_REQUEST['Area']))
		{
			$responseOutput->errCode = STATUS_MISSING_PARAMETER;
			return $responseOutput;
		}

		$value = $_REQUEST['Area'];
		if ($value != 'All')
		{
			$responseOutput->errCode = STATUS_INVALID_VALUE;
			return $responseOutput;
		}

		if ($classInstances['SmartCodecConfiguration']->dataInfo['Mode']['value'] != 1)
		{
			$responseOutput->errCode = STATUS_INVALID_VALUE;
			return $responseOutput;
		}

		for ($index = 0; $index < 5; ++$index)
		{
			$classInstances['SmartCodecConfiguration']->smartCodecArea[$index]->InitData();
		}
		$classInstances['SmartCodecConfiguration']->SetPayload();
		$classInstances['SmartCodecConfiguration']->headerInfo['Action'] = ACTION_SET;
		$GLOBALS['SOCKET_MANAGER']->Connection($classInstances['SmartCodecConfiguration']);

		$responseOutput->errCode = STATUS_OK;
		$responseOutput->outputMsg .= 'OK';
		return $responseOutput;
	}
	else if ($_REQUEST['action'] == 'view')
	{
		$responseOutput->outputMsg .= 'Channel.0.Mode=' . $SmartCodecMode[$classInstances['SmartCodecConfiguration']->dataInfo['Mode']['value']] . "\r\n";
		$responseOutput->outputMsg .= 'Channel.0.QualityLevel=' . $Quality[$classInstances['SmartCodecConfiguration']->dataInfo['QualityLevel']['value']] . "\r\n";

		for ($index = 0; $index < 5; ++$index)
		{
			if ($classInstances['SmartCodecConfiguration']->smartCodecArea[$index]->dataInfo['Enabled']['value'] != 1)
			{
				continue;
			}
			$areaConf = $classInstances['SmartCodecConfiguration']->smartCodecArea[$index];
			$responseOutput->outputMsg .= 'Channel.0.Area.' . ($index + 1) . '.Coordinate=';
			$responseOutput->outputMsg .= $areaConf->dataInfo['AreaLeft']['value'] . ',';
			$responseOutput->outputMsg .= $areaConf->dataInfo['AreaTop']['value'] . ',';
			$responseOutput->outputMsg .= $areaConf->dataInfo['AreaRight']['value'] . ',';
			$responseOutput->outputMsg .= $areaConf->dataInfo['AreaBottom']['value'] . "\r\n";
		}

		$responseOutput->errCode = STATUS_OK;
		return $responseOutput;
	}
	else
	{
		$responseOutput->errCode = STATUS_ACTION_NOT_FOUND;
		return $responseOutput;
	}
}

///////////////////////////////////////////////
// Privacy 
///////////////////////////////////////////////
function submenu_privacy()
{
	CheckAdminAccount(FALSE);

	$responseOutput = new ResponseOutput();
	global $boolArray;

	$addArea = FALSE;
	$classInstances = GetClassInstance('privacy');
	require_once('./adv/maskarea.class');
	$classInstances['MaskArea'] = new MaskArea(CMD_PRIVACY_AREA);

	$maxArea = $GLOBALS['M_SUPPORT_PRIVACY_AREA'];

	if ($GLOBALS['M_SUPPORT_PRIVACY_COLOR'] == PRIVACY_COLOR_TYPE_EVERY)
	{
		$AreaColor = array('Green', 'Red', 'Blue', 'Black', 'White', 'Gray');
	}
	else
	{
		$AreaColor = array('White', 'Red', 'Green', 'Blue', 'Black', 'Gray');
	}
	
	$MaskPattern = array ("Solid", "Mosaic1", "Mosaic2", "Mosaic3", "Mosaic4");

	if ($_REQUEST['Channel'] != 0)
	{
		$responseOutput->errCode = STATUS_INVALID_VALUE;
		return $responseOutput;
	}

	if ($_REQUEST['action'] == 'add')
	{
		if (!isset($_REQUEST['MaskCoordinate']) || !isset($_REQUEST['MaskName']) || !isset($_REQUEST['MaskColor']))
		{
			$responseOutput->errCode = STATUS_MISSING_PARAMETER;
			return $responseOutput;
		}
		
		$resMaxWidth = 0;
		$resMaxHeight = 0;
		require_once('./adv/va.class');
		$megaModeConf = new VideoSourceSelection();
		$megaModeConf = $GLOBALS['SOCKET_MANAGER']->Connection($megaModeConf);

		getMaxWidthHeight($resMaxWidth, $resMaxHeight, $megaModeConf->dataInfo['VideoSource']['value']);
		foreach ($_REQUEST as $name => $value)
		{
			switch ($name)
			{
				case 'MaskCoordinate':
					{
						$areaData = explode(",", $_REQUEST[$name]);
						
						if ($GLOBALS['M_SUPPORT_PRIVACY_AREA_TYPE'] == PRIVACY_AREA_TYPE_MASK_RECTANGLE)
						{
							if (count($areaData) != 4)
							{
								$responseOutput->errCode = STATUS_INVALID_VALUE;
								return $responseOutput;
							}
							for ($index = 0; $index < count($areaData); ++$index)
							{
								if (($index % 2) == 0) // X
								{
									if ($areaData[$index] < 0 || $areaData[$index] > $resMaxWidth-1)
									{
										$responseOutput->errCode = STATUS_INVALID_VALUE;
										return $responseOutput;
									}
								}
								else // Y
								{
									if ($areaData[$index] < 0 || $areaData[$index] > $resMaxHeight-1)
									{
										$responseOutput->errCode = STATUS_INVALID_VALUE;
										return $responseOutput;
									}
								}
							}

							$classInstances['MaskArea']->point[0]->dataInfo['X']['value'] = $areaData[0];
							$classInstances['MaskArea']->point[0]->dataInfo['Y']['value'] = $areaData[1];
							$classInstances['MaskArea']->point[1]->dataInfo['X']['value'] = $areaData[2];
							$classInstances['MaskArea']->point[1]->dataInfo['Y']['value'] = $areaData[3];
							$classInstances['MaskArea']->point[0]->payload = MakePayload($classInstances['MaskArea']->point[0]->dataInfo);
							$classInstances['MaskArea']->point[1]->payload = MakePayload($classInstances['MaskArea']->point[1]->dataInfo);
							$classInstances['MaskArea']->dataInfo['Enabled']['value'] = 1;
							$classInstances['MaskArea']->dataInfo['NumPoint']['value'] = 2;
						}
						else // PRIVACY_AREA_TYPE_MASK_POLYGON
						{
							if (count($areaData) != 8)
							{
								$responseOutput->errCode = STATUS_INVALID_VALUE;
								return $responseOutput;
							}
							for ($index = 0; $index < count($areaData); ++$index)
							{
								if (($index % 2) == 0) // X
								{
									if ($areaData[$index] < 0 || $areaData[$index] > $resMaxWidth-1)
									{
										$responseOutput->errCode = STATUS_INVALID_VALUE;
										return $responseOutput;
									}
								}
								else // Y
								{
									if ($areaData[$index] < 0 || $areaData[$index] > $resMaxHeight-1)
									{
										$responseOutput->errCode = STATUS_INVALID_VALUE;
										return $responseOutput;
									}
								}
							}
							
							$classInstances['MaskArea']->point[0]->dataInfo['X']['value'] = $areaData[0];
							$classInstances['MaskArea']->point[0]->dataInfo['Y']['value'] = $areaData[1];
							$classInstances['MaskArea']->point[1]->dataInfo['X']['value'] = $areaData[2];
							$classInstances['MaskArea']->point[1]->dataInfo['Y']['value'] = $areaData[3];
							$classInstances['MaskArea']->point[2]->dataInfo['X']['value'] = $areaData[4];
							$classInstances['MaskArea']->point[2]->dataInfo['Y']['value'] = $areaData[5];
							$classInstances['MaskArea']->point[3]->dataInfo['X']['value'] = $areaData[6];
							$classInstances['MaskArea']->point[3]->dataInfo['Y']['value'] = $areaData[7];

							$classInstances['MaskArea']->point[0]->payload = MakePayload($classInstances['MaskArea']->point[0]->dataInfo);
							$classInstances['MaskArea']->point[1]->payload = MakePayload($classInstances['MaskArea']->point[1]->dataInfo);
							$classInstances['MaskArea']->point[2]->payload = MakePayload($classInstances['MaskArea']->point[2]->dataInfo);
							$classInstances['MaskArea']->point[3]->payload = MakePayload($classInstances['MaskArea']->point[3]->dataInfo);
							$classInstances['MaskArea']->dataInfo['Enabled']['value'] = 1;
							$classInstances['MaskArea']->dataInfo['NumPoint']['value'] = 4;
						}

						$addArea = TRUE;
					}
					break;
				case 'MaskName':
					{
						$classInstances['MaskArea']->dataInfo['Name']['value'] = $value;
					}
					break;
				case 'MaskColor':
					{
						$newValue = array_search($value, $AreaColor);
						if (is_bool($newValue))
						{
							$responseOutput->errCode = STATUS_INVALID_VALUE;
							return $responseOutput;
						}
						
						if ($GLOBALS['M_SUPPORT_PRIVACY_COLOR'] == PRIVACY_COLOR_TYPE_EVERY)
						{
							$classInstances['PrivacyMask']->dataInfo['Color']['value'] = $newValue;
						}
						else
						{
							$classInstances['MaskArea']->dataInfo['Color']['value'] = $newValue;
							$addArea = TRUE;
						}
					}
					break;
				case 'ZoomThresholdEnable':
					{
						if (!$GLOBALS['M_SUPPORT_ZOOM_THRESHOLD'])
						{
							$responseOutput->errCode = STATUS_INVALID_PARAMETER;
							return $responseOutput;
						}
						$newValue = array_search($value, $boolArray);
						if (is_bool($newValue))
						{
							$responseOutput->errCode = STATUS_INVALID_VALUE;
							return $responseOutput;
						}
						$classInstances['MaskArea']->dataInfo['ZoomThreshold']['value'] = $newValue;
					}
					break;
			}
		}

		if ($addArea)
		{
			$classInstances['MaskArea']->SetPayload();
			$GLOBALS['SOCKET_MANAGER']->Connection($classInstances['MaskArea']);
		}
		$classInstances['PrivacyMask']->payload = MakePayload($classInstances['PrivacyMask']->dataInfo);
		$classInstances['PrivacyMask']->headerInfo['Action'] = ACTION_SET;
		$GLOBALS['SOCKET_MANAGER']->Connection($classInstances['PrivacyMask']);

		$responseOutput->errCode = STATUS_OK;
		$responseOutput->outputMsg .= 'OK';
		return $responseOutput;
	}
	else if ($_REQUEST['action'] == 'remove')
	{
		$justremove = 1;

		if (isset($_REQUEST['MaskIndex']))
		{
			$justremove = 0;

			$Indexlist = explode(",", $_REQUEST['MaskIndex']);
			$Indexcount = count($Indexlist);

			if ($Indexcount < 1 || $Indexcount > $maxArea)
			{
				$responseOutput->errCode = STATUS_INVALID_VALUE;
				return $responseOutput;
			}

			$classInstances['MaskAreas'] = $GLOBALS['SOCKET_MANAGER']->Connection(new MaskAreas(CMD_PRIVACY_AREA, $maxArea));

			for ($RemoveIndex = 0; $RemoveIndex < $Indexcount; ++$RemoveIndex)
			{
				$RemoveValue = $Indexlist[$RemoveIndex];
				if ($RemoveValue != 'All')
				{
					$RemoveValue = $RemoveValue - 1;
					if ($RemoveValue < 0 || $RemoveValue > $maxArea)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
					else
					{
						$classInstances['MaskArea']->headerInfo['Action'] = ACTION_REMOVE;
						$classInstances['MaskArea']->payload = pack('i1', ($RemoveValue));
						$GLOBALS['SOCKET_MANAGER']->Connection($classInstances['MaskArea']);
					}
				}
				else if ($RemoveValue == 'All')
				{
					for ($index = 0; $index < $maxArea; ++$index)
					{
						$classInstances['MaskArea']->headerInfo['Action'] = ACTION_REMOVE;
						$classInstances['MaskArea']->payload = pack('i1', ($index));
						$GLOBALS['SOCKET_MANAGER']->Connection($classInstances['MaskArea']);
					}
				}
			}
		}
		if ($justremove == 1)
		{
			for ($index = 0; $index < $maxArea; ++$index)
			{
				$classInstances['MaskArea']->headerInfo['Action'] = ACTION_REMOVE;
				$classInstances['MaskArea']->payload = pack('i1', ($index));
				$GLOBALS['SOCKET_MANAGER']->Connection($classInstances['MaskArea']);
			}
		}

		$responseOutput->errCode = STATUS_OK;
		$responseOutput->outputMsg .= 'OK';
		return $responseOutput;
	}
	else if ($_REQUEST['action'] == 'set')
	{
		if (count($_REQUEST) < 3)
		{
			$responseOutput->errCode = STATUS_MISSING_PARAMETER;
			return $responseOutput;
		}
		
		foreach ($_REQUEST as $name => $value)
		{
			if ($name == 'Enable')
			{
				$newValue = array_search($_REQUEST['Enable'], $boolArray);
				if (is_bool($newValue))
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				$classInstances['PrivacyMask']->dataInfo['Use']['value'] = $newValue;
			}
			else if ($name == 'MaskPattern')
			{
				if(!$GLOBALS['M_SUPPORT_PRIVACY_PATTERN'])
				{
					$responseOutput->errCode = STATUS_INVALID_PARAMETER;
					return $responseOutput;
				}
				
				$newValue = array_search($_REQUEST['MaskPattern'], $MaskPattern);
				if (is_bool($newValue))
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				$classInstances['PrivacyMask']->dataInfo['Pattern']['value'] = $newValue;
			}
		}

		$classInstances['PrivacyMask']->payload = MakePayload($classInstances['PrivacyMask']->dataInfo);
		$classInstances['PrivacyMask']->headerInfo['Action'] = ACTION_SET;
		$GLOBALS['SOCKET_MANAGER']->Connection($classInstances['PrivacyMask']);

		$responseOutput->errCode = STATUS_OK;
		$responseOutput->outputMsg .= 'OK';
		return $responseOutput;
	}
	else if ($_REQUEST['action'] == 'update')
	{
		if (!$GLOBALS['M_SUPPORT_ZOOM_THRESHOLD'])
		{
			$responseOutput->errCode = STATUS_ACTION_NOT_FOUND;
			return $responseOutput;
		}
		
		if ((count($_REQUEST) < 4) || (!isset($_REQUEST['MaskIndex'])) || (!isset($_REQUEST['ZoomThresholdEnable'])))
		{
			$responseOutput->errCode = STATUS_MISSING_PARAMETER;
			return $responseOutput;
		}
		
		$classInstances['MaskAreas'] = $GLOBALS['SOCKET_MANAGER']->Connection(new MaskAreas(CMD_PRIVACY_AREA, $maxArea));
		$GLOBALS['SOCKET_MANAGER']->Connection(new PrivacyMask());	
			
		for ($index = 0; $index < $maxArea; ++$index)
		{
			$areaConf = $classInstances['MaskAreas']->maskArea[$index];
						
			if (($areaConf->dataInfo['Enabled']['value'] == 1) && ($areaConf->dataInfo['Index']['value'] == $_REQUEST['MaskIndex'] - 1))
			{			
				$newValue = array_search($_REQUEST['ZoomThresholdEnable'], $boolArray);
				if (is_bool($newValue))
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				
				$classInstances['MaskArea']->dataInfo['ZoomThreshold']['value'] = $newValue;
				$classInstances['MaskArea']->dataInfo['Index']['value'] = $_REQUEST['MaskIndex'] - 1;

				$classInstances['MaskArea']->headerInfo['Action'] = ACTION_ZOOM_THRESHOLD;				
				$classInstances['MaskArea']->SetPayload();
				$GLOBALS['SOCKET_MANAGER']->Connection($classInstances['MaskArea']);
			
				$responseOutput->errCode = STATUS_OK;
				$responseOutput->outputMsg .= 'OK';
				return $responseOutput;
			}
		}
		
		$responseOutput->errCode = STATUS_INVALID_VALUE;
		return $responseOutput;
	}
	else if ($_REQUEST['action'] == 'view')
	{
		require_once('./adv/maskarea.class');
		require_once ('./adv/videosource.class');
		$classInstances['MaskAreas'] = $GLOBALS['SOCKET_MANAGER']->Connection(new MaskAreas(CMD_PRIVACY_AREA, $maxArea));
		$GLOBALS['SOCKET_MANAGER']->Connection(new PrivacyMask());
		
		$responseOutput->outputMsg .= 'Channel.0.Enable=' . $boolArray[$classInstances['PrivacyMask']->dataInfo['Use']['value']] . "\r\n";
		if($GLOBALS['M_SUPPORT_PRIVACY_PATTERN'])
		{
			$responseOutput->outputMsg .= 'Channel.0.MaskPattern=' . $MaskPattern[$classInstances['PrivacyMask']->dataInfo['Pattern']['value']] . "\r\n";
		}

		for ($index = 0; $index < $maxArea; ++$index)
		{
			if ($classInstances['MaskAreas']->maskArea[$index]->dataInfo['Enabled']['value'] != 1)
			{
				continue;
			}
			$areaConf = $classInstances['MaskAreas']->maskArea[$index];
			$maskIndex = $areaConf->dataInfo['Index']['value'] + 1;
			$responseOutput->outputMsg .= 'Channel.0.MaskIndex=' . $maskIndex . "\r\n";
			$responseOutput->outputMsg .= 'Channel.0.MaskName=' . $areaConf->dataInfo['Name']['value'] . "\r\n";
			if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3 || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_HISILICON)
			{
				$responseOutput->outputMsg .= 'Channel.0.MaskColor=' . $AreaColor[$areaConf->dataInfo['Color']['value']] . "\r\n";
			}
			else
			{
				$responseOutput->outputMsg .= 'Channel.0.MaskColor=' . $AreaColor[$classInstances['PrivacyMask']->dataInfo['Color']['value']] . "\r\n";
			}

			if ($areaConf->point[2]->dataInfo['X']['value'] == 0 && $areaConf->point[2]->dataInfo['Y']['value'] == 0)
			{
				$responseOutput->outputMsg .= 'Channel.0.MaskCoordinate=' . $areaConf->point[0]->dataInfo['X']['value'] . ',' . $areaConf->point[0]->dataInfo['Y']['value'] . ',' . $areaConf->point[1]->dataInfo['X']['value'] . ',' . $areaConf->point[1]->dataInfo['Y']['value'] . "\r\n";
			}
			else
			{
				$responseOutput->outputMsg .= 'Channel.0.MaskCoordinate=' . $areaConf->point[0]->dataInfo['X']['value'] . ',' . $areaConf->point[0]->dataInfo['Y']['value'] . ',' . $areaConf->point[1]->dataInfo['X']['value'] . ',' . $areaConf->point[1]->dataInfo['Y']['value'] . ',' . $areaConf->point[2]->dataInfo['X']['value'] . ',' . $areaConf->point[2]->dataInfo['Y']['value'] . ',' . $areaConf->point[3]->dataInfo['X']['value'] . ',' . $areaConf->point[3]->dataInfo['Y']['value'] . "\r\n";
			}
			if ($GLOBALS['M_SUPPORT_ZOOM_THRESHOLD'])
			{
				$responseOutput->outputMsg .= 'Channel.0.ZoomThresholdEnable=' . $boolArray[$areaConf->dataInfo['ZoomThreshold']['value']] . "\r\n";
			}
		}

		$responseOutput->errCode = STATUS_OK;
		return $responseOutput;
	}
	else
	{
		$responseOutput->errCode = STATUS_ACTION_NOT_FOUND;
		return $responseOutput;
	}
}

//////////////////////////////////////////////
// IR LED 
///////////////////////////////////////////////
function submenu_irled()
{
	CheckAdminAccount(FALSE);
	$responseOutput = new ResponseOutput();

    if (($_REQUEST['action'] != 'set') && ($_REQUEST['action'] != 'view'))
    {
        $responseOutput->errCode = STATUS_ACTION_NOT_FOUND;       
        return $responseOutput;
    }

	$classInstances = GetClassInstance('image');
    
    if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ)
    {
        $IRMode = array(
            0 => 'Off',
            1 => 'On',
            2 => 'DayNight',
            3 => 'Sensor',
            4 => 'Schedule'
        );
        $MaxPowerLevel = array(
            0 => 'Low',
            1 => 'Medium',
            2 => 'High'
        );
        $PoercontrolMode = array(
            0 => 'Off',
            1 => 'Auto'
        );        
    }
    else
    {
        $IRMode = array(
            0 => 'Off',
            1 => 'Auto',
            2 => 'Manual'
        );
    }
    
    if(isset($_REQUEST['Channel']) && ($_REQUEST['Channel'] != 0))
    {
        $responseOutput->errCode = STATUS_INVALID_VALUE;
        return $responseOutput;
    }
    
    if ($_REQUEST['action'] == 'set')
    {
        if (count($_REQUEST) < 3)
        {
            $responseOutput->errCode = STATUS_MISSING_PARAMETER;
            return $responseOutput;
        }
        
        foreach ($_REQUEST as $name => $value)
        {
            switch ($name)
            {
                case 'Mode' :
                    {
                        $newValue = array_search($_REQUEST['Mode'], $IRMode);

                        if (is_bool($newValue))
                        {
                            $responseOutput->errCode = STATUS_INVALID_VALUE;                           
                            return $responseOutput;
                        }

                        if($_REQUEST['Mode'] == 'Off')
                        {
							if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ)
                        	{
                        		// IR Mode is to be Off from On,Day/Night,Sensor,Schedule
                        		// DayNightMode is to be Auto
                        		if($classInstances['ImageSetting']->imagePTZIR->dataInfo['Mode']['value'] != 0)
                        		{
									$classInstances['ImageSetting']->imageSpecial->dataInfo['DayNightMode']['value'] = 2;
                        		}
                        	}
                        	else
                        	{
                        		// IR Mode is to be Off from On,Day/Night,Sensor,Schedule
                        		// DayNightMode is to be Auto
                        		if($classInstances['ImageSetting']->imageIR->dataInfo['Mode']['value'] != 0)
                        		{
									$classInstances['ImageSetting']->imageSpecial->dataInfo['DayNightMode']['value'] = 2;	
                        		}
                        	}
						}
                        else if($_REQUEST['Mode'] == 'DayNight')
                        {
							// DayNightMode is to be Auto Mode in DayNight IR Mode
                        	// 2 => Auto
                        	$classInstances['ImageSetting']->imageSpecial->dataInfo['DayNightMode']['value'] = 2;
                        }
                        else if($_REQUEST['Mode'] == 'Sensor')
                        {
							/*
                        	// default value of LED On/Off level are below values.
                        	$classInstances['ImageSetting']->imagePTZIR->dataInfo['LedOnLevel']['value'] = 40;
                        	$classInstances['ImageSetting']->imagePTZIR->dataInfo['LedOffLevel']['value'] = 60;
                        	*/
                        }
                        else if($_REQUEST['Mode'] == 'Schedule')
                        {
                        	/*
                        	$classInstances['ImageSetting']->imagePTZIR->dataInfo['LedOnTimeHour']['value'] = 19;
                            $classInstances['ImageSetting']->imagePTZIR->dataInfo['LedOnTimeMin']['value'] = 0;
                            $classInstances['ImageSetting']->imagePTZIR->dataInfo['LedOffTimeHour']['value'] = 5;
                            $classInstances['ImageSetting']->imagePTZIR->dataInfo['LedOffTimeMin']['value'] = 0;
                            */
                        }    
                        
                        if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ)
                        {
                        	$classInstances['ImageSetting']->imagePTZIR->dataInfo['Mode']['value'] = $newValue;                        	
                        }
                        else
                        {
                        	$classInstances['ImageSetting']->imageIR->dataInfo['Mode']['value'] = $newValue;
                        }
                    }
                    break;
                case 'Level':
                    {
                        if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3)
                        {
                           if (isset($_REQUEST['Mode']))
							{
								$newValue = array_search($_REQUEST['Mode'], $IRMode);
								if ($newValue != 2)
								{
									$responseOutput->errCode = STATUS_INVALID_VALUE;
									return $responseOutput;
								}
							}
							else
							{
								if ($classInstances['ImageSetting']->imageIR->dataInfo['Mode']['value'] != 2)
								{
									$responseOutput->errCode = STATUS_INVALID_VALUE;
									return $responseOutput;
								}
							}

							if ($value < 1 || $value > 99)
							{
								$responseOutput->errCode = STATUS_INVALID_VALUE;								
								return $responseOutput;
							}
							$classInstances['ImageSetting']->imageIR->dataInfo['Level']['value'] = $value;
	                    }
                        else
                        {
                            $responseOutput->errCode = STATUS_NOT_IMPLEMENTED;
                            return $responseOutput;
                        }
                    }
                    break;
                case 'LEDOnLevel':
                    {
                        if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ)
                        {
                            if ($value < 1 || $value > 90)
                            {
                                $responseOutput->errCode = STATUS_INVALID_VALUE;
                                return $responseOutput;
                            }

                            if(isset($_REQUEST['LEDOffLevel']))
                            {
                            	if(($_REQUEST['LEDOffLevel'] - $value) < 10)
	                            {
	                            	$responseOutput->errCode = STATUS_INVALID_VALUE;
	                                return $responseOutput;
	                            }
                            }
                            else
                            {
								if(($classInstances['ImageSetting']->imagePTZIR->dataInfo['LedOffLevel']['value'] - $value) < 10)
	                            {
	                            	$responseOutput->errCode = STATUS_INVALID_VALUE;
	                                return $responseOutput;
	                            }
                            }
                            
                            $classInstances['ImageSetting']->imagePTZIR->dataInfo['LedOnLevel']['value'] = $value;
                        }
                        else
                        {
                            $responseOutput->errCode = STATUS_NOT_IMPLEMENTED;
                            return $responseOutput;
                        }
                    }
                    break;
                case 'LEDOffLevel':
                    {
                        if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ)
                        {
                            if ($value < 11 || $value > 100)
                            {
                                $responseOutput->errCode = STATUS_INVALID_VALUE;
                                return $responseOutput;
                            }
                            
                            if(isset($_REQUEST['LEDOnLevel']))
                            {
                            	if(($value - $_REQUEST['LEDOnLevel']) < 10)
	                            {
	                            	$responseOutput->errCode = STATUS_INVALID_VALUE;
	                                return $responseOutput;
	                            }
                            }
                            else
                            {
								if(($value - $classInstances['ImageSetting']->imagePTZIR->dataInfo['LedOnLevel']['value']) < 10)
	                            {
	                            	$responseOutput->errCode = STATUS_INVALID_VALUE;
	                                return $responseOutput;
	                            }
                            }
                            
                            $classInstances['ImageSetting']->imagePTZIR->dataInfo['LedOffLevel']['value'] = $value;
                        }
                        else
                        {
                            $responseOutput->errCode = STATUS_NOT_IMPLEMENTED;
                            return $responseOutput;
                        }
                    }
                    break;
                case 'Schedule_EveryDay_FromTo':
                    {
                        if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ)
                        {
                            $tempTovalue = split("-", $_REQUEST[$name]);

                            $tempFrom = split(":", $tempTovalue[0]);
                            $tempTo = split(":", $tempTovalue[1]);

                            if ($tempFrom[0] < 0 || $tempFrom[0] > 23)
                            {
                                $responseOutput->errCode = STATUS_INVALID_VALUE;                               
                                return $responseOutput;
                            }
                            else if ($tempTo[0] < 0 || $tempTo[0] > 23)
                            {
                                $responseOutput->errCode = STATUS_INVALID_VALUE;                                
                                return $responseOutput;
                            }
                            else if ($tempFrom[1] < 0 || $tempFrom[1] > 59)
                            {
                                $responseOutput->errCode = STATUS_INVALID_VALUE;                                
                                return $responseOutput;
                            }
                            else if ($tempTo[1] < 0 || $tempTo[1] > 59)
                            {
                                $responseOutput->errCode = STATUS_INVALID_VALUE;                                
                                return $responseOutput;
                            }
                            else if ($tempFrom[0] == $tempTo[0])
                            {
                                if ($tempFrom[1] >= $tempTo[1])
                                {
                                    $responseOutput->errCode = STATUS_INVALID_VALUE;                                   
                                    return $responseOutput;
                                }
                            }

                            $classInstances['ImageSetting']->imagePTZIR->dataInfo['LedOnTimeHour']['value'] = $tempFrom[0];
                            $classInstances['ImageSetting']->imagePTZIR->dataInfo['LedOnTimeMin']['value'] = $tempFrom[1];
                            $classInstances['ImageSetting']->imagePTZIR->dataInfo['LedOffTimeHour']['value'] = $tempTo[0];
                            $classInstances['ImageSetting']->imagePTZIR->dataInfo['LedOffTimeMin']['value'] = $tempTo[1];
                        }
                        else
                        {
                            $responseOutput->errCode = STATUS_NOT_IMPLEMENTED;
                            return $responseOutput;
                        }
                    }
                    break;
                case 'LEDMaxPower':
                    {
                        if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ)
                        {
                            $newValue = array_search($_REQUEST['LEDMaxPower'], $MaxPowerLevel);
                            if (is_bool($newValue))
                            {
                                $responseOutput->errCode = STATUS_INVALID_VALUE;
                                return $responseOutput;
                            }
                            $classInstances['ImageSetting']->imagePTZIR->dataInfo['LedMaxPower']['value'] = $newValue;
                        }
                        else
                        {
                            $responseOutput->errCode = STATUS_NOT_IMPLEMENTED;
                            return $responseOutput;
                        }
                    }
                    break;
                case 'LEDPowerControlMode':
                    {
                        if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ)
                        {
                            $newValue = array_search($_REQUEST['LEDPowerControlMode'], $PoercontrolMode);
                            if (is_bool($newValue))
                            {
                                $responseOutput->errCode = STATUS_INVALID_VALUE;
                                return $responseOutput;
                            }
                            $classInstances['ImageSetting']->imagePTZIR->dataInfo['LedPowerControl']['value'] = $newValue;
                        }
                        else
                        {
                            $responseOutput->errCode = STATUS_NOT_IMPLEMENTED;
                            return $responseOutput;
                        }
                    }
                    break;
            }
        }
        
        $classInstances['ImageSetting']->imageSSDR->payload = MakePayload($classInstances['ImageSetting']->imageSSDR->dataInfo);
		$classInstances['ImageSetting']->imageWhiteBalance->payload = MakePayload($classInstances['ImageSetting']->imageWhiteBalance->dataInfo);
		$classInstances['ImageSetting']->imageBackLight->payload = MakePayload($classInstances['ImageSetting']->imageBackLight->dataInfo);
		$classInstances['ImageSetting']->imageExposure->payload = MakePayload($classInstances['ImageSetting']->imageExposure->dataInfo);
		$classInstances['ImageSetting']->imageSpecial->payload = MakePayload($classInstances['ImageSetting']->imageSpecial->dataInfo);
		$classInstances['ImageSetting']->imageIR->payload = MakePayload($classInstances['ImageSetting']->imageIR->dataInfo);
		$classInstances['ImageSetting']->imagePTZIR->payload = MakePayload($classInstances['ImageSetting']->imagePTZIR->dataInfo);
		$classInstances['ImageSetting']->imageOSD->payload = MakePayload($classInstances['ImageSetting']->imageOSD->dataInfo);
		$classInstances['ImageSetting']->imageDayNightSchedule->SetPayload();
		$classInstances['ImageSetting']->imagePreset->SetPayload();
		$classInstances['ImageSetting']->headerInfo['Action'] = ACTION_SET;
		$classInstances['ImageSetting']->SetPayload();
		$GLOBALS['SOCKET_MANAGER']->Connection($classInstances['ImageSetting']);

        $responseOutput->errCode = STATUS_OK;
        $responseOutput->outputMsg .= 'OK';
        return $responseOutput;
    }
    else if ($_REQUEST['action'] == 'view')
    {
        if ($GLOBALS['M_ISP_TYPE'] != ISP_TYPE_WN2_PTZ)
        {
            $responseOutput->outputMsg .= 'Channel.0.Mode=' . $IRMode[$classInstances['ImageSetting']->imageIR->dataInfo['Mode']['value']] . "\r\n";
            if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3)
            {
            	$responseOutput->outputMsg .= 'Channel.0.Level=' . $classInstances['ImageSetting']->imageIR->dataInfo['Level']['value'] . "\r\n";
            }
        }
        else
        {
            if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ)//SNP6320RH
            {
	            $responseOutput->outputMsg .= 'Channel.0.Mode=' . $IRMode[$classInstances['ImageSetting']->imagePTZIR->dataInfo['Mode']['value']] . "\r\n";
	            $responseOutput->outputMsg .= 'Channel.0.LEDOnLevel=' . $classInstances['ImageSetting']->imagePTZIR->dataInfo['LedOnLevel']['value'] . "\r\n";
	            $responseOutput->outputMsg .= 'Channel.0.LEDOffLevel=' . $classInstances['ImageSetting']->imagePTZIR->dataInfo['LedOffLevel']['value'] . "\r\n";
	            $responseOutput->outputMsg .= 'Channel.0.Schedule.EveryDay.FromTo=' . $classInstances['ImageSetting']->imagePTZIR->dataInfo['LedOnTimeHour']['value'];
	            $responseOutput->outputMsg .= ':' . $classInstances['ImageSetting']->imagePTZIR->dataInfo['LedOnTimeMin']['value'];
	            $responseOutput->outputMsg .= '-' . $classInstances['ImageSetting']->imagePTZIR->dataInfo['LedOffTimeHour']['value'];
	            $responseOutput->outputMsg .= ':' . $classInstances['ImageSetting']->imagePTZIR->dataInfo['LedOffTimeMin']['value'] . "\r\n";
	            $responseOutput->outputMsg .= 'Channel.0.LEDMaxPower=' . $MaxPowerLevel[$classInstances['ImageSetting']->imagePTZIR->dataInfo['LedMaxPower']['value']] . "\r\n";
	            $responseOutput->outputMsg .= 'Channel.0.LEDPowerControlMode=' . $PoercontrolMode[$classInstances['ImageSetting']->imagePTZIR->dataInfo['LedPowerControl']['value']] . "\r\n";
	         }           
        }

        $responseOutput->errCode = STATUS_OK;
        return $responseOutput;
    }
    else
    {
        $responseOutput->errCode = STATUS_ACTION_NOT_FOUND;       
        return $responseOutput;
    }	
}

//////////////////////////////////////////////
// Image Enhancements 
///////////////////////////////////////////////
function submenu_imageenhancements()
{
	CheckAdminAccount(FALSE);
	global $boolArray;

	$Defog = array(
		0 => "Off",
		1 => 'Auto',
		2 => 'Manual'
	);

	$CAR = array(
		0 => 'Off',
		1 => 'Low',
		2 => 'Medium',
		3 => 'High'
	);
	$responseOutput = new ResponseOutput();

	if (($_REQUEST['action'] != 'set') && ($_REQUEST['action'] != 'view'))
	{
		$responseOutput->errCode = STATUS_ACTION_NOT_FOUND;
		return $responseOutput;
	}

	$classInstances = GetClassInstance('image');

	if ($_REQUEST['action'] == 'set')
	{
		if (count($_REQUEST) < 3)
		{
			$responseOutput->errCode = STATUS_MISSING_PARAMETER;
			return $responseOutput;
		}
		if ($_REQUEST['Channel'] != 0)
		{
			$responseOutput->errCode = STATUS_INVALID_VALUE;
			return $responseOutput;
		}

		$cameraInfo = array(
			'Brightness' => array('target' => 'imageExposure', 'name' => 'Brightness'),
			'Saturation' => array('target' => 'imageSpecial', 'name' => 'ColorLevel'),
			'SharpnessEnable' => array('target' => 'imageSpecial', 'name' => 'SharpnessMode'),
			'SharpnessLevel' => array('target' => 'imageSpecial', 'name' => 'SharpnessLevel'),
			'Gamma' => array('target' => 'imageSpecial', 'name' => 'Gamma'),
			'DefogMode' => array('target' => 'imageSpecial', 'name' => 'Defog'),
			'DefogLevel' => array('target' => 'imageSpecial', 'name' => 'DefogLevel'),
			'DISEnable' => array('target' => 'imageSpecial', 'name' => 'DIS'),
			'CAR' => array('target' => 'imageSpecial', 'name' => 'CAR'),
			'LDCEnable' => array('target' => 'imageSpecial', 'name' => 'LDCEnable'),
			'LDCLevel' => array('target' => 'imageSpecial', 'name' => 'LDCLevel'),
		);

		foreach ($cameraInfo as $name => $data)
		{
			if (!isset($_REQUEST[$name]))
			{
				continue;
			}

			if ($name == 'Brightness')
			{
				if ($_REQUEST[$name] < 1 || $_REQUEST[$name] > 100)
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				$classInstances['ImageSetting']->imageExposure->dataInfo['Brightness']['value'] = $_REQUEST[$name];
			}
			else if ($name == 'Gamma')
			{
				if ($GLOBALS['M_ISP_TYPE'] != ISP_TYPE_WN3)
				{
					$responseOutput->errCode = STATUS_INVALID_PARAMETER;
					return $responseOutput;
				}
				if ($_REQUEST[$name] < 0 || $_REQUEST[$name] > 16)
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				$classInstances['ImageSetting']->imageSpecial->dataInfo['Gamma']['value'] = $_REQUEST[$name];
			}
			else if ($name == 'Saturation')
			{
				if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3 || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ)
				{
					if ($_REQUEST[$name] < 1 || $_REQUEST[$name] > 100)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				else if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ)
				{
					if ($_REQUEST[$name] < 0 || $_REQUEST[$name] > 100)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				$classInstances['ImageSetting']->imageSpecial->dataInfo['ColorLevel']['value'] = $_REQUEST[$name];
			}
			else if ($name == 'SharpnessLevel')
			{
				if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3 || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ)
				{
					if ($_REQUEST[$name] < 1 || $_REQUEST[$name] > 32)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				else if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ)
				{
					if ($_REQUEST[$name] < 1 || $_REQUEST[$name] > 31)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}

				if (isset($_REQUEST['SharpnessEnable']))
				{
					if (array_search($_REQUEST['SharpnessEnable'], $boolArray) != 1)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				else
				{
					if ($classInstances['ImageSetting']->imageSpecial->dataInfo['SharpnessMode']['value'] != 1)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				$classInstances['ImageSetting']->$data['target']->dataInfo[$data['name']]['value'] = $_REQUEST[$name];
			}
			else if ($name == 'SharpnessEnable')
			{
				$newValue = array_search($_REQUEST['SharpnessEnable'], $boolArray);
				if (is_bool($newValue))
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				$classInstances['ImageSetting']->$data['target']->dataInfo[$data['name']]['value'] = $newValue;
			}
			else if ($name == 'DefogMode')
			{
				if ($GLOBALS['M_SUPPORT_DEFOG'] == 0)
				{
					$responseOutput->errCode = STATUS_NOT_IMPLEMENTED;
					return $responseOutput;
				}
				
				$newValue = array_search($_REQUEST['DefogMode'], $Defog);
				if (is_bool($newValue))
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				$classInstances['ImageSetting']->imageSpecial->dataInfo['Defog']['value'] = $newValue;
			}
			else if ($name == 'DefogLevel')
			{
				if ($GLOBALS['M_SUPPORT_DEFOG'] == 0)
				{
					$responseOutput->errCode = STATUS_NOT_IMPLEMENTED;
					return $responseOutput;
				}

				if (isset($_REQUEST['DefogMode']))
				{
					if ($_REQUEST['DefogMode'] == 'Off')
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				else
				{
					if ($classInstances['ImageSetting']->imageSpecial->dataInfo['Defog']['value'] == 0)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}

				if ($_REQUEST[$name] < 1 || $_REQUEST[$name] > 10)
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}

				$classInstances['ImageSetting']->imageSpecial->dataInfo['DefogLevel']['value'] = $_REQUEST[$name];
			}
			else if ($name == 'DISEnable')
			{
				if (!$GLOBALS['M_SUPPORT_DIS'])
				{
					$responseOutput->errCode = STATUS_INVALID_PARAMETER;
					return $responseOutput;
				}
				
				if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ)
				{
					require_once ('./adv/info.class');
					$info = $GLOBALS['SOCKET_MANAGER']->Connection(new Information());
					if ($info->dataInfo['TamperingEnable']['value'] == 1
						|| $info->dataInfo['MDEnable']['value'] == 1
						|| $info->dataInfo['IVEnable']['value'] == 1)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}

				$newValue = array_search($_REQUEST['DISEnable'], $boolArray);
				if (is_bool($newValue))
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}

				$classInstances['ImageSetting']->imageSpecial->dataInfo['DIS']['value'] = $newValue;
			}
			else if ($name == 'CAR')
			{
				if ($GLOBALS['M_SPECIAL_TYPE'] != 2)
				{
					$responseOutput->errCode = STATUS_INVALID_PARAMETER;
					return $responseOutput;
				}

				$newValue = array_search($_REQUEST['CAR'], $CAR);
				if (is_bool($newValue))
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				$classInstances['ImageSetting']->imageSpecial->dataInfo['CAR']['value'] = $_REQUEST[$name];
			}
			else if ($name == 'LDCEnable')
			{
				if ($GLOBALS['M_ISP_TYPE'] != ISP_TYPE_HISILICON)
				{
					$responseOutput->errCode = STATUS_NOT_IMPLEMENTED;
					return $responseOutput;
				}
			
				$newValue = array_search($_REQUEST['LDCEnable'], $boolArray);
				if (is_bool($newValue))
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
			
				$classInstances['ImageSetting']->imageSpecial->dataInfo['LDCEnable']['value'] = $newValue;
			}
			else if ($name == 'LDCLevel')
			{
				if ($GLOBALS['M_ISP_TYPE'] != ISP_TYPE_HISILICON)
				{
					$responseOutput->errCode = STATUS_NOT_IMPLEMENTED;
					return $responseOutput;
				}
			
				if (isset($_REQUEST['LDCEnable']))
				{
					if ($_REQUEST['LDCEnable'] == 'False')
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
				else
				{
					if ($classInstances['ImageSetting']->imageSpecial->dataInfo['LDCEnable']['value'] == 0)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
			
				if ($_REQUEST[$name] < 1 || $_REQUEST[$name] > 5)
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
			
				$classInstances['ImageSetting']->imageSpecial->dataInfo['LDCLevel']['value'] = $_REQUEST[$name];
			}
		}

		$classInstances['ImageSetting']->imageSSDR->payload = MakePayload($classInstances['ImageSetting']->imageSSDR->dataInfo);
		$classInstances['ImageSetting']->imageWhiteBalance->payload = MakePayload($classInstances['ImageSetting']->imageWhiteBalance->dataInfo);
		$classInstances['ImageSetting']->imageBackLight->payload = MakePayload($classInstances['ImageSetting']->imageBackLight->dataInfo);
		$classInstances['ImageSetting']->imageExposure->payload = MakePayload($classInstances['ImageSetting']->imageExposure->dataInfo);
		$classInstances['ImageSetting']->imageSpecial->payload = MakePayload($classInstances['ImageSetting']->imageSpecial->dataInfo);
		$classInstances['ImageSetting']->imageIR->payload = MakePayload($classInstances['ImageSetting']->imageIR->dataInfo);
		$classInstances['ImageSetting']->imageOSD->payload = MakePayload($classInstances['ImageSetting']->imageOSD->dataInfo);
		$classInstances['ImageSetting']->imageDayNightSchedule->SetPayload();
		$classInstances['ImageSetting']->imagePreset->SetPayload();
		$classInstances['ImageSetting']->headerInfo['Action'] = ACTION_SET;
		$classInstances['ImageSetting']->SetPayload();
		$GLOBALS['SOCKET_MANAGER']->Connection($classInstances['ImageSetting']);

		$responseOutput->errCode = STATUS_OK;
		$responseOutput->outputMsg .= 'OK';
		return $responseOutput;
	}
	else if ($_REQUEST['action'] == 'view')
	{
		if ($_REQUEST['Channel'] != 0)
		{
			$responseOutput->errCode = STATUS_INVALID_VALUE;
			return $responseOutput;
		}

		$responseOutput->outputMsg .= 'Channel.0.Brightness=' . $classInstances['ImageSetting']->imageExposure->dataInfo['Brightness']['value'] . "\r\n";
		$responseOutput->outputMsg .= 'Channel.0.SharpnessEnable=' . $boolArray[$classInstances['ImageSetting']->imageSpecial->dataInfo['SharpnessMode']['value']] . "\r\n";
		$responseOutput->outputMsg .= 'Channel.0.SharpnessLevel=' . $classInstances['ImageSetting']->imageSpecial->dataInfo['SharpnessLevel']['value'] . "\r\n";
		if (($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3) || ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_HISILICON))
		{
			$responseOutput->outputMsg .= 'Channel.0.Gamma=' . $classInstances['ImageSetting']->imageSpecial->dataInfo['Gamma']['value'] . "\r\n";
		}
		$responseOutput->outputMsg .= 'Channel.0.Saturation=' . $classInstances['ImageSetting']->imageSpecial->dataInfo['ColorLevel']['value'] . "\r\n";
		
		if ($GLOBALS['M_SUPPORT_DEFOG'])
		{
			$responseOutput->outputMsg .= 'Channel.0.DefogMode=' . $Defog[$classInstances['ImageSetting']->imageSpecial->dataInfo['Defog']['value']] . "\r\n";
			$responseOutput->outputMsg .= 'Channel.0.DefogLevel=' . $classInstances['ImageSetting']->imageSpecial->dataInfo['DefogLevel']['value'] . "\r\n";
		}
		if ($GLOBALS['M_SUPPORT_DIS'])
		{
			$responseOutput->outputMsg .= 'Channel.0.DISEnable=' . $boolArray[$classInstances['ImageSetting']->imageSpecial->dataInfo['DIS']['value']] . "\r\n";
		}

		if ($GLOBALS['M_SPECIAL_TYPE'] == 2)
		{
			$responseOutput->outputMsg .= 'Channel.0.CAR=' . $CAR[$classInstances['ImageSetting']->imageSpecial->dataInfo['CAR']['value']] . "\r\n";
		}
		if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_HISILICON)
		{
			$responseOutput->outputMsg .= 'Channel.0.LDCEnable=' . $boolArray[$classInstances['ImageSetting']->imageSpecial->dataInfo['LDCEnable']['value']] . "\r\n";
			$responseOutput->outputMsg .= 'Channel.0.LDCLevel=' . $classInstances['ImageSetting']->imageSpecial->dataInfo['LDCLevel']['value'] . "\r\n";
		}

		$responseOutput->errCode = STATUS_OK;
		return $responseOutput;
	}
	else
	{
		$responseOutput->errCode = STATUS_ACTION_NOT_FOUND;
		return $responseOutput;
	}
}

//////////////////////////////////////////////
// Focus 
///////////////////////////////////////////////

function submenu_focus()
{
	CheckAdminAccount(FALSE);

	if ($GLOBALS['M_SUPPORT_MOTORIZE'] == MOTORIZE_FOCUS_ZOOM_SUPPORT)
	{
		$Mode = array(
			//0 => 'Reset',
			1 => 'SimpleFocus',
			2 => 'AutoFocus'
		);
	}
	else if ($GLOBALS['M_SUPPORT_MOTORIZE'] == MOTORIZE_FOCUS_ONLY_SUPPORT)
	{
		$Mode = array(
			0 => 'Reset',
			1 => 'SimpleFocus',
			2 => 'AutoFocus'
		);
	}

	$FocusMode = array(
		0 => 'Manual',
		1 => 'Auto',
		2 => 'OneShotAutoFocus'//OnePushAF
	);
	$ZoomTrack = array(
		0 => 'Off',
		1 => 'AutoTracking',
		2 => 'Tracking'
	);
	$ZoomSpeed = array(
		0 => 'Fast',
		1 => 'Medium',
		2 => 'Slow'
	);
	$LensReset = array(
		0 => '1Day',
		1 => '2Days',
		2 => '3Days',
		3 => '4Days',
		4 => '5Days',
		5 => '6Days',
		6 => '7Days',
		7 => 'Manual'
	);

	$responseOutput = new ResponseOutput();
	if ($_REQUEST['action'] == 'set' || $_REQUEST['action'] == 'view')
	{
		$classInstances = GetClassInstance('image');
		$imageSetConf = $classInstances['ImageSetting'];
	}

	if ($_REQUEST['Channel'] != 0)
	{
		$responseOutput->errCode = STATUS_INVALID_VALUE;
		return $responseOutput;
	}

	if ($_REQUEST['action'] == 'control')
	{
		if (!$GLOBALS['M_SUPPORT_PTZ'])
		{
			if ($GLOBALS['M_SUPPORT_MOTORIZE'] == MOTORIZE_NO_SUPPORT)
			{
				$responseOutput->errCode = STATUS_NOT_IMPLEMENTED;
				return $responseOutput;
			}
		}

		if (!isset($_REQUEST['Mode']) && !isset($_REQUEST['Zoom']) && !isset($_REQUEST['Focus']))
		{
			$responseOutput->errCode = STATUS_MISSING_PARAMETER;
			return $responseOutput;
		}

		// Mode, Zoom, Focus should be set alone
		if (isset($_REQUEST['Mode']) && (isset($_REQUEST['Zoom']) || isset($_REQUEST['Focus'])))
		{
			$responseOutput->errCode = STATUS_INVALID_PARAMETER;
			return $responseOutput;
		}
		if (isset($_REQUEST['Zoom']) && (isset($_REQUEST['Mode']) || isset($_REQUEST['Focus'])))
		{
			$responseOutput->errCode = STATUS_INVALID_PARAMETER;
			return $responseOutput;
		}
		if (isset($_REQUEST['Focus']) && (isset($_REQUEST['Mode']) || isset($_REQUEST['Zoom'])))
		{
			$responseOutput->errCode = STATUS_INVALID_PARAMETER;
			return $responseOutput;
		}

		if (isset($_REQUEST['FocusAreaCoordinate']) && !isset($_REQUEST['Mode']))
		{
			$responseOutput->errCode = STATUS_MISSING_PARAMETER;
			return $responseOutput;
		}

		$GLOBALS['SOCKET_MANAGER'] = new SocketManager();
		
		require_once ('./adv/ptzmove.class');
		$focusConf = new MotorizedLensSetup();
		
		if (isset($_REQUEST['Mode']))
		{	
			if ($GLOBALS['M_SUPPORT_PTZ'])
			{
				if ($_REQUEST['Mode'] != "AutoFocus")
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}

				/** This Paramater is applicable only for Simple Focus*/
				if (isset($_REQUEST['FocusAreaCoordinate']))
				{
					$responseOutput->errCode = STATUS_INVALID_PARAMETER;
					return $responseOutput;
				}
				
				require_once ('./adv/info.class');
				$info = $GLOBALS['SOCKET_MANAGER']->Connection(new Information());
				if ($info->dataInfo['UserRightPTZ']['value'] != 1)
				{
					$responseOutput->errCode = STATUS_NOT_AUTHORIZED;
					return $responseOutput;
				}
				require_once ('./adv/relay.class');
				$instantAF = new PTZInstantAF();
				$instantAF->dataInfo['Index']['value'] = 0;
				$instantAF->payload = MakePayload($instantAF->dataInfo);
				$GLOBALS['SOCKET_MANAGER']->Connection($instantAF);
			}
			else
			{
				$newValue = array_search($_REQUEST['Mode'], $Mode);
				if (is_bool($newValue))
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}

				$focusConf->dataInfo['Mode']['value'] = 2;
				$focusConf->dataInfo['AF']['value'] = ($newValue == 2) ? 1 : $newValue;

				if (isset($_REQUEST['FocusAreaCoordinate']))
				{
					$focusConf->focusArea->dataInfo['Enable']['value'] = 1;
					$areaData = explode(",", $_REQUEST['FocusAreaCoordinate']);
					if (count($areaData) != 4)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}

					$resMaxWidth = 0;
					$resMaxHeight = 0;
					$classInstances = GetClassInstance('va');
					$megaModeConf = new VideoSourceSelection();
					$megaModeConf = $GLOBALS['SOCKET_MANAGER']->Connection($megaModeConf);

					getMaxWidthHeight($resMaxWidth, $resMaxHeight, $megaModeConf->dataInfo['VideoSource']['value']);
					if (($areaData[0] > TEN_THOUSAND) || ($areaData[2] > TEN_THOUSAND) || 
						($areaData[1] > TEN_THOUSAND) || ($areaData[3] > TEN_THOUSAND))
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}

					$focusConf->focusArea->dataInfo['AreaLeft']['value'] = TenThounsandToPixel($resMaxWidth, $areaData[0]);
					$focusConf->focusArea->dataInfo['AreaTop']['value'] = TenThounsandToPixel($resMaxHeight, $areaData[1]);
					$focusConf->focusArea->dataInfo['AreaRight']['value'] = TenThounsandToPixel($resMaxWidth, $areaData[2]);
					$focusConf->focusArea->dataInfo['AreaBottom']['value'] = TenThounsandToPixel($resMaxHeight, $areaData[3]);
				}
			}
		}
		else if (isset($_REQUEST['Zoom']))
		{
			if ($GLOBALS['M_SUPPORT_MOTORIZE'] != MOTORIZE_FOCUS_ZOOM_SUPPORT)
			{
				$responseOutput->errCode = STATUS_INVALID_PARAMETER;
				return $responseOutput;
			}
			if ($_REQUEST['Zoom'] != -100 && $_REQUEST['Zoom'] != -10 &&
				$_REQUEST['Zoom'] != -1 && $_REQUEST['Zoom'] != 1 &&
				$_REQUEST['Zoom'] != 10 && $_REQUEST['Zoom'] != 100)
			{
				$responseOutput->errCode = STATUS_INVALID_VALUE;
				return $responseOutput;
			}
			$focusConf->dataInfo['Mode']['value'] = 0;
			$focusConf->ptzPosition->dataInfo['ZoomReal']['value'] = $_REQUEST['Zoom'];
		}
		else if (isset($_REQUEST['Focus']))
		{
			if ($GLOBALS['M_SUPPORT_MOTORIZE'] == MOTORIZE_NO_SUPPORT)
			{
				$responseOutput->errCode = STATUS_INVALID_PARAMETER;
				return $responseOutput;
			}
			
			if ($_REQUEST['Focus'] != -100 && $_REQUEST['Focus'] != -10 &&
				$_REQUEST['Focus'] != -1 && $_REQUEST['Focus'] != 1 &&
				$_REQUEST['Focus'] != 10 && $_REQUEST['Focus'] != 100)
			{
				$responseOutput->errCode = STATUS_INVALID_VALUE;
				return $responseOutput;
			}
			$focusConf->dataInfo['Mode']['value'] = 1;
			$focusConf->ptzPosition->dataInfo['FocusReal']['value'] = $_REQUEST['Focus'];
		}

		if (!$GLOBALS['M_SUPPORT_PTZ'])
		{
			$focusConf->ptzPosition->payload = MakePayload($focusConf->ptzPosition->dataInfo);
			$focusConf->focusArea->payload = MakePayload($focusConf->focusArea->dataInfo);
			$focusConf->SetPayload();
			$GLOBALS['SOCKET_MANAGER']->Connection($focusConf);
		}

		$responseOutput->errCode = STATUS_OK;
		$responseOutput->outputMsg .= 'OK';
		return $responseOutput;
	}
	if ($_REQUEST['action'] == 'set')
	{
		if ($GLOBALS['M_SUPPORT_PTZ'] == PTZ_NOT_SUPPORT)
		{
			$responseOutput->errCode = STATUS_NOT_IMPLEMENTED;
			return $responseOutput;
		}
		
		if (count($_REQUEST) < 3)
		{
			$responseOutput->errCode = STATUS_MISSING_PARAMETER;
			return $responseOutput;
		}

		foreach ($_REQUEST as $name => $value)
		{
			switch ($name)
			{
				case 'Mode':
					{
						$newValue = array_search($value, $FocusMode);
						if (is_bool($newValue))
						{
							$responseOutput->errCode = STATUS_INVALID_VALUE;
							return $responseOutput;
						}
						$classInstances['ImageSetting']->imageFocus->dataInfo['Mode']['value'] = $newValue;
					}
					break;
				case 'ZoomTrackingMode':
					{
						$newValue = array_search($value, $ZoomTrack);
						if (is_bool($newValue))
						{
							$responseOutput->errCode = STATUS_INVALID_VALUE;
							return $responseOutput;
						}
						$classInstances['ImageSetting']->imageFocus->dataInfo['ZoomTrack']['value'] = $newValue;
					}
					break;
				case 'ZoomTrackingSpeed':
					{
						$newValue = array_search($value, $ZoomSpeed);
						if (is_bool($newValue))
						{
							$responseOutput->errCode = STATUS_INVALID_VALUE;
							return $responseOutput;
						}

						$classInstances['ImageSetting']->imageFocus->dataInfo['ZoomSpeed']['value'] = $newValue;
					}
					break;
				case 'LensResetSchedule':
					{
						$newValue = array_search($value, $LensReset);
						if (is_bool($newValue))
						{
							$responseOutput->errCode = STATUS_INVALID_VALUE;
							return $responseOutput;
						}

						if ($newValue == 7)//Manual
						{
							$classInstances['ImageSetting']->imageFocus->dataInfo['InitLens']['value'] = 0;
						}
						else
						{
							$classInstances['ImageSetting']->imageFocus->dataInfo['InitLens']['value'] = 1;
							$classInstances['ImageSetting']->imageFocus->dataInfo['InitLensDur']['value'] = $newValue;
						}
					}
					break;
			}
		}

		$imageSetConf->imageFocus->payload = MakePayload($classInstances['ImageSetting']->imageFocus->dataInfo);

		$classInstances['ImageSetting']->imageSSDR->payload = MakePayload($classInstances['ImageSetting']->imageSSDR->dataInfo);
		$classInstances['ImageSetting']->imageWhiteBalance->payload = MakePayload($classInstances['ImageSetting']->imageWhiteBalance->dataInfo);
		$classInstances['ImageSetting']->imageBackLight->payload = MakePayload($classInstances['ImageSetting']->imageBackLight->dataInfo);
		$classInstances['ImageSetting']->imageExposure->payload = MakePayload($classInstances['ImageSetting']->imageExposure->dataInfo);
		$classInstances['ImageSetting']->imageSpecial->payload = MakePayload($classInstances['ImageSetting']->imageSpecial->dataInfo);
		$classInstances['ImageSetting']->imageIR->payload = MakePayload($classInstances['ImageSetting']->imageIR->dataInfo);
		$classInstances['ImageSetting']->imageOSD->payload = MakePayload($classInstances['ImageSetting']->imageOSD->dataInfo);
		$classInstances['ImageSetting']->imageDayNightSchedule->SetPayload();
		$classInstances['ImageSetting']->imagePreset->SetPayload();
		$classInstances['ImageSetting']->imagePTZIR->payload = MakePayload($classInstances['ImageSetting']->imagePTZIR->dataInfo);
		$classInstances['ImageSetting']->imageTracking->payload = MakePayload($classInstances['ImageSetting']->imageTracking->dataInfo);
		$classInstances['ImageSetting']->headerInfo['Action'] = ACTION_SET;
		$classInstances['ImageSetting']->SetPayload();
		$GLOBALS['SOCKET_MANAGER']->Connection($classInstances['ImageSetting']);


		$responseOutput->errCode = STATUS_OK;
		$responseOutput->outputMsg .= 'OK';
		return $responseOutput;
	}
	else if ($_REQUEST['action'] == 'view')
	{
		if ($GLOBALS['M_SUPPORT_PTZ'] == PTZ_NOT_SUPPORT)
		{
			$responseOutput->errCode = STATUS_NOT_IMPLEMENTED;
			return $responseOutput;
		}
		
		$responseOutput->outputMsg .= 'Channel.0.Mode=' . $FocusMode[$classInstances['ImageSetting']->imageFocus->dataInfo['Mode']['value']] . "\r\n";
		$responseOutput->outputMsg .= 'Channel.0.ZoomTrackingMode=' . $ZoomTrack[$classInstances['ImageSetting']->imageFocus->dataInfo['ZoomTrack']['value']] . "\r\n";

		$responseOutput->outputMsg .= 'Channel.0.ZoomTrackingSpeed=' . $ZoomSpeed[$classInstances['ImageSetting']->imageFocus->dataInfo['ZoomSpeed']['value']] . "\r\n";

		if ($classInstances['ImageSetting']->imageFocus->dataInfo['InitLens']['value'] == 0)
		{
			$responseOutput->outputMsg .= 'Channel.0.LensResetSchedule=Manual' . "\r\n";
		}
		else if ($classInstances['ImageSetting']->imageFocus->dataInfo['InitLens']['value'] == 1)
		{
			$responseOutput->outputMsg .= 'Channel.0.LensResetSchedule=' . $LensReset[$classInstances['ImageSetting']->imageFocus->dataInfo['InitLensDur']['value']] . "\r\n";
		}

		$responseOutput->errCode = STATUS_OK;
		return $responseOutput;
	}
	else
	{
		$responseOutput->errCode = STATUS_ACTION_NOT_FOUND;
		return $responseOutput;
	}
}

///////////////////////////////////////////////
// CGI Command - Submenu handler
///////////////////////////////////////////////
switch (@$_REQUEST['msubmenu'])
{
	case 'camera':
	case 'whitebalance':
	case 'flip':
	case 'ssdr':
	case 'irled':
	case 'imageenhancements':
	case 'focus':
	case 'overlay':
	case 'smartcodec':
	case 'privacy':
	case 'imagepreset':
		{
			if ($_REQUEST['msubmenu'] == 'ssdr' && $GLOBALS['M_ISP_TYPE'] == ISP_NO_TYPE)
			{
				$responseOutput = new ResponseOutput();
				$responseOutput->errCode = STATUS_NOT_IMPLEMENTED;
				SendResponse($responseOutput);
			}
			if ($_REQUEST['msubmenu'] == 'smartcodec' && $GLOBALS['M_SUPPORT_SMARTCODEC'] == 0)
			{
				$responseOutput = new ResponseOutput();
				$responseOutput->errCode = STATUS_NOT_IMPLEMENTED;
				SendResponse($responseOutput);
			}
			if ($_REQUEST['msubmenu'] == 'irled' && $GLOBALS['M_SUPPORT_IR'] == 0)
			{
				$responseOutput = new ResponseOutput();
				$responseOutput->errCode = STATUS_NOT_IMPLEMENTED;
				SendResponse($responseOutput);
			}
			if ($_REQUEST['msubmenu'] == 'imagepreset' && $GLOBALS['M_ISP_TYPE'] != ISP_TYPE_WN3)
			{
				$responseOutput = new ResponseOutput();
				$responseOutput->errCode = STATUS_NOT_IMPLEMENTED;
				SendResponse($responseOutput);
			}

			$funcName = 'submenu_' . $_REQUEST['msubmenu'];
			SendResponse($funcName());
		} break;

	default:
		{
			$responseOutput = new ResponseOutput();
			$responseOutput->errCode = STATUS_SUBMENU_NOT_FOUND;
			SendResponse($responseOutput);
		}
}
?>
