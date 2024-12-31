<?php

require_once ('./adv/_define.inc');
CheckAdminAccount(FALSE);

///////////////////////////////////////////////
// Input
///////////////////////////////////////////////
function submenu_alarminput()
{
    $responseOutput = new ResponseOutput();
    $responseOutput->outputMsg = '';

    global $boolArray;
    
    $alarmNo = -1;

    $InputState = array(
        0 => 'Off',
        1 => 'NormallyOpen',
        2 => 'NormallyClose'
    );

    $classInstances = GetClassInstance('alarm');

    if ($_REQUEST['action'] == 'set')
    {
        if (count($_REQUEST) < 3)
        {
            $responseOutput->errCode = STATUS_MISSING_PARAMETER;
            return $responseOutput;
        }

        $allowed_params = array("msubmenu", "action", "Alarminput_1_State", "AlarmInput_1_State", "Alarminput_2_State", "AlarmInput_2_State", "Alarminput_3_State", "AlarmInput_3_State", 
        						"Alarminput_4_State", "AlarmInput_4_State", "Alarminput_1_Enable", "AlarmInput_1_Enable", "Alarminput_2_Enable", "AlarmInput_2_Enable", "Alarminput_3_Enable", 
        						"AlarmInput_3_Enable", "Alarminput_4_Enable", "AlarmInput_4_Enable");

        if(CheckAllowedParams($allowed_params) === FALSE)
        {
        	$responseOutput->errCode = STATUS_INVALID_PARAMETER;
            return $responseOutput;
        }

        foreach ($_REQUEST as $name => $value)
        {
            switch ($name)
            {
                case 'Alarminput_1_State':
                case 'AlarmInput_1_State':
                case 'Alarminput_2_State':
                case 'AlarmInput_2_State':
                case 'Alarminput_3_State':
                case 'AlarmInput_3_State':
                case 'Alarminput_4_State':
                case 'AlarmInput_4_State':
                    {
                        $newvalue = array_search($value, $InputState);
                        if ($newvalue === FALSE)
                        {
                            $responseOutput->errCode = STATUS_INVALID_VALUE;
                            return $responseOutput;
                        }

                        $alarmNo = (int)substr($name, -7) - 1;

                        if($alarmNo >= $GLOBALS['M_ALARMIN_COUNT'])
                        {
                        	$responseOutput->errCode = STATUS_INVALID_PARAMETER;
                            return $responseOutput;
                        }
                        
                        $classInstances['SensorConfiguration']->alarmInput[$alarmNo]->dataInfo['Type']['value'] = $newvalue - 1;
                        $classInstances['SensorConfiguration']->alarmInput[$alarmNo]->SetPayload();
                    }
                    break;
                case 'Alarminput_1_Enable':
                case 'AlarmInput_1_Enable':
                case 'Alarminput_2_Enable':
                case 'AlarmInput_2_Enable':
                case 'Alarminput_3_Enable':
                case 'AlarmInput_3_Enable':
                case 'Alarminput_4_Enable':
                case 'AlarmInput_4_Enable':
                    {
                        $newvalue = array_search($value, $boolArray);
                        if ($newvalue === FALSE)
                        {
                            $responseOutput->errCode = STATUS_INVALID_VALUE;
                            return $responseOutput;
                        }
                        
                        $alarmNo = (int)substr($name, -8) - 1;

                        if($alarmNo >= $GLOBALS['M_ALARMIN_COUNT'])
                        {
                        	$responseOutput->errCode = STATUS_INVALID_PARAMETER;
                            return $responseOutput;
                        }
                        
                        $classInstances['SensorConfiguration']->alarmInput[$alarmNo]->dataInfo['Enabled']['value'] = $newvalue;
                        $classInstances['SensorConfiguration']->alarmInput[$alarmNo]->SetPayload();
                    }
                    break;
            }
        }
        
        if ($alarmNo >= 0)
        {
            $classInstances['SensorConfiguration']->SetPayload();
            $classInstances['SensorConfiguration']->headerInfo['Action'] = ACTION_SET;
            $GLOBALS['SOCKET_MANAGER']->Connection($classInstances['SensorConfiguration']);

            $responseOutput->outputMsg = 'OK';
        }
        else
        {
            $responseOutput->errCode = STATUS_MISSING_PARAMETER;
            return $responseOutput;
        }
    }
    else if ($_REQUEST['action'] == 'view')
    {
    	$allowed_params = array("msubmenu", "action");

        if(CheckAllowedParams($allowed_params) === FALSE)
        {
        	$responseOutput->errCode = STATUS_INVALID_PARAMETER;
            return $responseOutput;
        }
        
        for ($index = 0; $index < $GLOBALS['M_ALARMIN_COUNT']; ++$index)
        {
            $responseOutput->outputMsg .= 'AlarmInput.' . ($index + 1) . '.Enable=' . $boolArray[$classInstances['SensorConfiguration']->alarmInput[$index]->dataInfo['Enabled']['value']] . "\r\n";
            $responseOutput->outputMsg .= 'AlarmInput.' . ($index + 1) . '.State=' . $InputState[$classInstances['SensorConfiguration']->alarmInput[$index]->dataInfo['Type']['value'] + 1] . "\r\n";
        }
    }
    else
    {
        $responseOutput->errCode = STATUS_ACTION_NOT_FOUND;
        return $responseOutput;
    }

    $responseOutput->errCode = STATUS_OK;
    return $responseOutput;
}

///////////////////////////////////////////////
// Remove IV Rules
///////////////////////////////////////////////
function RemoveIVRule(&$ivConf, $rmIndex)
{
	for ($index = 0; $index < $GLOBALS['M_MAX_IV_LINE_POINT']; ++$index)
    {
        $ivConf->objectRule[$rmIndex]->point[$index]->InitData();
    }
    
    $ivConf->objectRule[$rmIndex]->type = 0;
    $ivConf->objectRule[$rmIndex]->InitData();
    $ivConf->objectRule[$rmIndex]->SetPayload();
}

///////////////////////////////////////////////
// View VA
///////////////////////////////////////////////
function ViewVideoAnalysis($Conf, $resMaxWidth, $resMaxHeight)
{
	global $Sensitivity;

	$res = 'Channel.0.Sensitivity=' . $Sensitivity[($Conf->dataInfo['Sensitivity']['value'] + 1 )] . "\r\n";

	$hsl = round((($Conf->manualSize->dataInfo['MinWidth']['value'] - 24) * 99) / ($resMaxWidth - 24));
	$vsl = round((($Conf->manualSize->dataInfo['MinHeight']['value'] - 24) * 99) / ($resMaxHeight - 24));
    $res .= 'Channel.0.MinimumObjectSize=' . $hsl . "," . $vsl . "\r\n";

	$hsh = round((($Conf->manualSize->dataInfo['MaxWidth']['value'] - 24) * 99) / ($resMaxWidth - 24));
	$vsh = round((($Conf->manualSize->dataInfo['MaxHeight']['value'] - 24) * 99) / ($resMaxHeight - 24));
    $res .= 'Channel.0.MaximumObjectSize=' . $hsh . "," . $vsh . "\r\n";

    $res .= 'Channel.0.MinimumObjectSizeInPixels=' . $Conf->manualSize->dataInfo['MinWidth']['value'] . ",";
    $res .= $Conf->manualSize->dataInfo['MinHeight']['value'] . "\r\n";
    $res .= 'Channel.0.MaximumObjectSizeInPixels=' . $Conf->manualSize->dataInfo['MaxWidth']['value'] . ",";
    $res .= $Conf->manualSize->dataInfo['MaxHeight']['value'] . "\r\n";

    return $res;
}

///////////////////////////////////////////////
// View IV Rules
///////////////////////////////////////////////
function ViewIVRule($ivConf)
{
    $responseOutput = new ResponseOutput();

    global $LineDetectionMode;
    global $EntireAreaMode;
    global $DefinedAreaMode;

	$lineMsg = '';
    $areaMsg = '';
    $appearMsg = '';
    $enteringMsg = '';
    
    for ($index = 0; $index < $GLOBALS['M_MAX_IV_OBJECT'] ; ++$index)
    {
        if ($ivConf->objectRule[$index]->type == 0)
        {
            continue;
        }

        $coordinateMsg = '';

        for ($index2 = 0; $index2 < $GLOBALS['M_MAX_IV_LINE_POINT']; ++$index2)
        {
            if ($ivConf->objectRule[$index]->point[$index2]->dataInfo['Valid']['value'] == 0)
            {
                continue;
            }
            
            $coordinateMsg .= $ivConf->objectRule[$index]->point[$index2]->dataInfo['PosX']['value'] . ',';
            $coordinateMsg .= $ivConf->objectRule[$index]->point[$index2]->dataInfo['PosY']['value'] . ',';
        }

        if ($ivConf->objectRule[$index]->type == 1) // Line
        {  
            $lineMsg .= 'Channel.0.Line.' . ($index + 1) . '.Mode=' . $LineDetectionMode[$ivConf->objectRule[$index]->dataInfo['LineRule']['value']] . "\r\n";
            $lineMsg .= 'Channel.0.Line.' . ($index + 1) . '.Coordinate=' . substr($coordinateMsg, 0, -1) . "\r\n";
        }
        else if ($ivConf->objectRule[$index]->type == 2) // defined area
        { 
            if ($ivConf->objectRule[$index]->dataInfo['AreaEnter']['value'] == 1 && $ivConf->objectRule[$index]->dataInfo['AreaExit']['value'] == 1)
            {
                $DefinedArea = 4;
            }
            else if ($ivConf->objectRule[$index]->dataInfo['AreaEnter']['value'] == 1)
            {
                $DefinedArea = 2;
            }
            else if ($ivConf->objectRule[$index]->dataInfo['AreaExit']['value'] == 1)
            {
                $DefinedArea = 3;
            }
            else if ($ivConf->objectRule[$index]->dataInfo['AreaAppear']['value'] == 1 || $ivConf->objectRule[$index]->dataInfo['AreaDisappear']['value'] == 1)
            {
                $DefinedArea = 1;
            }

			if($GLOBALS['M_SUPPORT_PTZ'] == PTZ_SUPPORT)
			{
				if($DefinedArea == 1) // appeardisappear
				{
					$idx = $ivConf->objectRule[$GLOBALS['M_MAX_IV_OBJECT'] - 1]->dataInfo['LineRuleDetail']['value'] - 1 ;
					
					$appearMsg .= 'Channel.0.DefinedArea.' . $idx . '.Mode=' . $DefinedAreaMode[$DefinedArea] . "\r\n";
		            $appearMsg .= 'Channel.0.DefinedArea.' . $idx . '.Coordinate=' . substr($coordinateMsg, 0, -1);
		            $appearMsg .= "\r\n";
				}
				else // enteringexiting
				{
					$idx = $ivConf->objectRule[$GLOBALS['M_MAX_IV_OBJECT'] - 1]->dataInfo['LineRule']['value'] + 1;
					
					$enteringMsg .= 'Channel.0.DefinedArea.' . $idx . '.Mode=' . $DefinedAreaMode[$DefinedArea] . "\r\n";
		            $enteringMsg .= 'Channel.0.DefinedArea.' . $idx . '.Coordinate=' . substr($coordinateMsg, 0, -1);
		            $enteringMsg .= "\r\n";
				}
			}
			else
			{
	            $areaMsg .= 'Channel.0.DefinedArea.' . ($index - 2) . '.Mode=' . $DefinedAreaMode[$DefinedArea] . "\r\n";
	            $areaMsg .= 'Channel.0.DefinedArea.' . ($index - 2) . '.Coordinate=' . substr($coordinateMsg, 0, -1);
				$areaMsg .= "\r\n";
			}
        }
    }

    if($GLOBALS['M_SUPPORT_PTZ'] == PTZ_SUPPORT)
    {
    	$checkMsgOrder = explode(".", $appearMsg);
    	if((int)$checkMsgOrder[3] == 1)
    	{
    		$areaMsg .= $appearMsg;
    		$areaMsg .= $enteringMsg;
    	}
    	else
    	{
    		$areaMsg .= $enteringMsg;
    		$areaMsg .= $appearMsg;
    	}
    }

	$responseOutput->outputMsg .= $areaMsg;
    $responseOutput->outputMsg .= $lineMsg;

    if(CheckModelName('CHECK_IV_ENTIREAREA_MODE'))
    {
		$entireMode = 0;
		
        if($ivConf->fullScreenRule->dataInfo['FullAppear']['value'])
        	$entireMode = 1;
        else if($ivConf->fullScreenRule->dataInfo['FullSceneChange']['value'])
        	$entireMode = 2;
                    	
	    $responseOutput->outputMsg .= 'Channel.0.EntireAreaMode=' . $EntireAreaMode[$entireMode] . "\r\n";
    }

    return $responseOutput->outputMsg;
}

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

///////////////////////////////////////////////
// Set VA
///////////////////////////////////////////////
function SetVideoAnalysis(&$Conf, $resMaxWidth, $resMaxHeight)
{
	$responseOutput = new ResponseOutput();
	global $boolArray;
	global $Sensitivity;

	$classInstances = GetClassInstance('va');
    $VAConf = $classInstances['VAConfiguration'];

	$setMinWidth = $Conf->manualSize->dataInfo['MinWidth']['value'];
	$setMinHeight = $Conf->manualSize->dataInfo['MinHeight']['value'];
	$setMaxWidth = $Conf->manualSize->dataInfo['MaxWidth']['value'];
	$setMaxHeight = $Conf->manualSize->dataInfo['MaxHeight']['value'];

	if((isset($_REQUEST['MinimumObjectSize']) || isset($_REQUEST['MaximumObjectSize'])) && (isset($_REQUEST['MinimumObjectSizeInPixels']) || isset($_REQUEST['MaximumObjectSizeInPixels'])))
    {
    	$responseOutput->errCode = STATUS_INVALID_PARAMETER;
        SendResponse($responseOutput);
    }
	
	foreach ($_REQUEST as $name => $value)
    {
        switch ($name)
        {
            case 'Sensitivity':
                {
                    $newValue = array_search($value, $Sensitivity);
                    if($newValue === FALSE)
                    {
                        $responseOutput->errCode = STATUS_INVALID_VALUE;
                        SendResponse($responseOutput);
                    }
                    
                    $Conf->dataInfo['Sensitivity']['value'] = $newValue - 1;
                }
                break;

            case 'MinimumObjectSize':
                {               	
                    $ObjectSizeData = explode(",", $value);
                    if (count($ObjectSizeData) != 2)
                    {
                        $responseOutput->errCode = STATUS_INVALID_VALUE;
                        SendResponse($responseOutput);
                    }

                    if (($ObjectSizeData[0] < 0 || $ObjectSizeData[0] > 99) || ($ObjectSizeData[1] < 0 || $ObjectSizeData[1] > 99))
                    {
                        $responseOutput->errCode = STATUS_INVALID_VALUE;
                        SendResponse($responseOutput);
                    }

                    $Conf->manualSize->dataInfo['HSL']['value'] = $ObjectSizeData[0];
                    $Conf->manualSize->dataInfo['VSL']['value'] = $ObjectSizeData[1];

                    $inpixelWidth = (round(($ObjectSizeData[0] * ($resMaxWidth - 24)) / 99)) + 24;
                    $inpixelHeight = (round(($ObjectSizeData[1] * ($resMaxHeight - 24)) / 99)) + 24;

                    $Conf->manualSize->dataInfo['MinWidth']['value'] = $inpixelWidth;
                    $Conf->manualSize->dataInfo['MinHeight']['value'] = $inpixelHeight;
                }
                break;
            case 'MaximumObjectSize':
                {
                    $ObjectSizeData = explode(",", $value);
                    if (count($ObjectSizeData) != 2)
                    {
                        $responseOutput->errCode = STATUS_INVALID_VALUE;
                        SendResponse($responseOutput);
                    }

                    if (($ObjectSizeData[0] < 0 || $ObjectSizeData[0] > 99) || ($ObjectSizeData[1] < 0 || $ObjectSizeData[1] > 99))
                    {
                        $responseOutput->errCode = STATUS_INVALID_VALUE;
                        SendResponse($responseOutput);
                    }

                    $Conf->manualSize->dataInfo['HSH']['value'] = $ObjectSizeData[0];
                    $Conf->manualSize->dataInfo['VSH']['value'] = $ObjectSizeData[1];

                    $inpixelWidth = (round(($ObjectSizeData[0] * ($resMaxWidth - 24)) / 99)) + 24;
                    $inpixelHeight = (round(($ObjectSizeData[1] * ($resMaxHeight - 24)) / 99)) + 24;

                    $Conf->manualSize->dataInfo['MaxWidth']['value'] = $inpixelWidth;
                    $Conf->manualSize->dataInfo['MaxHeight']['value'] = $inpixelHeight;
                }
                break;
           case 'MinimumObjectSizeInPixels':
           case 'MaximumObjectSizeInPixels':		   	
	           {	           
					/** If va or md is not enabled */
					if($VAConf->mdConf->dataInfo['Enabled']['value'] == 0 && $VAConf->ivConf->dataInfo['Enabled']['value'] == 0)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						SendResponse($responseOutput);
					}
      	
					$ObjectSizeData = explode(",", $value);
					if (count($ObjectSizeData) != 2)
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						SendResponse($responseOutput);
					}
	
					/** If it is PTZ based on WN3*/
					if($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ)
					{
						/** If given value is greater than supported value */
						if( ($ObjectSizeData[0] < 32) || ($ObjectSizeData[1] < 32) )
						{
							$responseOutput->errCode = STATUS_INVALID_VALUE;
							SendResponse($responseOutput);
						}
					}
					else
					{
						/** If given value is greater than supported value */
						if( ($ObjectSizeData[0] < 24) || ($ObjectSizeData[1] < 24) )
						{
							$responseOutput->errCode = STATUS_INVALID_VALUE;
							SendResponse($responseOutput);
						}
					}

					if( $ObjectSizeData[0] > $resMaxWidth || $ObjectSizeData[1] > $resMaxHeight )
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
	                    SendResponse($responseOutput);			
					}

					if ($name == 'MinimumObjectSizeInPixels')
					{
						$setMinWidth = $ObjectSizeData[0];
						$setMinHeight = $ObjectSizeData[1];
					}

					if($name == 'MaximumObjectSizeInPixels')
					{
						$setMaxWidth = $ObjectSizeData[0];
						$setMaxHeight = $ObjectSizeData[1];
					}
				}
           		break;
			}
	}

	if(isset($_REQUEST['MinimumObjectSizeInPixels']) || isset($_REQUEST['MaximumObjectSizeInPixels']))
	{
		if( $setMinWidth > $setMaxWidth || $setMinHeight > $setMaxHeight )
		{
			$responseOutput->errCode = STATUS_INVALID_VALUE;
			SendResponse($responseOutput);			
		}

		$Conf->manualSize->dataInfo['MinWidth']['value'] = $setMinWidth;
		$Conf->manualSize->dataInfo['MinHeight']['value'] = $setMinHeight;
		$Conf->manualSize->dataInfo['MaxWidth']['value'] = $setMaxWidth;
		$Conf->manualSize->dataInfo['MaxHeight']['value'] = $setMaxHeight;
	}
}

///////////////////////////////////////////////
// Set IV Rules
///////////////////////////////////////////////
function SetIVRule(&$ivConf)
{
    $responseOutput = new ResponseOutput();

    global $LineDetectionMode;
    global $EntireAreaMode;
    global $DefinedAreaMode;

    if($GLOBALS['M_SUPPORT_PTZ'] == PTZ_SUPPORT) /** PTZ model index rule : [3] -> entering, [4] -> appering */
	{
		/** check requested value (defined area mode is duplicate or not & update case) */
		if(isset($_REQUEST['DefinedArea_1_Mode']) && isset($_REQUEST['DefinedArea_2_Mode']))
		{
			if($_REQUEST['DefinedArea_1_Mode'] == $_REQUEST['DefinedArea_2_Mode'])
			{
				$responseOutput->errCode = STATUS_INVALID_VALUE;
	            SendResponse($responseOutput);
			}
		}
		else if(isset($_REQUEST['DefinedArea_1_Mode']))
		{
			if($_REQUEST['DefinedArea_1_Mode'] == 'AppearDisappear')
			{
				if($ivConf->objectRule[$GLOBALS['M_MAX_IV_OBJECT'] - 1]->dataInfo['LineRuleDetail']['value'] == 2)
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
		            SendResponse($responseOutput);
				}

				if($ivConf->objectRule[$GLOBALS['M_MAX_IV_OBJECT'] - 1]->dataInfo['LineRule']['value'] == 1) // update case
				{
					RemoveIVRule($ivConf, 3);
        			$ivConf->objectRule[$GLOBALS['M_MAX_IV_OBJECT'] - 1]->dataInfo['LineRule']['value'] = 0;
				}
			}
			else // entering
			{
				if($ivConf->objectRule[$GLOBALS['M_MAX_IV_OBJECT'] - 1]->dataInfo['LineRule']['value'] == 2)
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
		            SendResponse($responseOutput);
				}

				if($ivConf->objectRule[$GLOBALS['M_MAX_IV_OBJECT'] - 1]->dataInfo['LineRuleDetail']['value'] == 1) // update case
				{
					RemoveIVRule($ivConf, 4);
        			$ivConf->objectRule[$GLOBALS['M_MAX_IV_OBJECT'] - 1]->dataInfo['LineRuleDetail']['value'] = 0;
				}
			}
		}
		else if(isset($_REQUEST['DefinedArea_2_Mode']))
		{
			if($_REQUEST['DefinedArea_2_Mode'] == 'AppearDisappear')
			{
				if($ivConf->objectRule[$GLOBALS['M_MAX_IV_OBJECT'] - 1]->dataInfo['LineRuleDetail']['value'] == 1)
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
		            SendResponse($responseOutput);
				}

				if($ivConf->objectRule[$GLOBALS['M_MAX_IV_OBJECT'] - 1]->dataInfo['LineRule']['value'] == 2) // update case
				{
					RemoveIVRule($ivConf, 3);
        			$ivConf->objectRule[$GLOBALS['M_MAX_IV_OBJECT'] - 1]->dataInfo['LineRule']['value'] = 0;
				}
			}
			else // entering
			{
				if($ivConf->objectRule[$GLOBALS['M_MAX_IV_OBJECT'] - 1]->dataInfo['LineRule']['value'] == 1)
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
		            SendResponse($responseOutput);
				}

				if($ivConf->objectRule[$GLOBALS['M_MAX_IV_OBJECT'] - 1]->dataInfo['LineRuleDetail']['value'] == 2) // update case
				{
					RemoveIVRule($ivConf, 4);
        			$ivConf->objectRule[$GLOBALS['M_MAX_IV_OBJECT'] - 1]->dataInfo['LineRuleDetail']['value'] = 0;
				}
			}
		}
	}
	
    foreach ($_REQUEST as $name => $value)
    {
        switch ($name)
        {
            case 'DefinedArea_1_Coordinates': case 'DefinedArea_2_Coordinates': case 'DefinedArea_3_Coordinates':
            case 'DefinedArea_1_Coordinate': case 'DefinedArea_2_Coordinate': case 'DefinedArea_3_Coordinate':
            case 'Line_1_Coordinates': case 'Line_2_Coordinates': case 'Line_3_Coordinates':
            case 'Line_1_Coordinate': case 'Line_2_Coordinate': case 'Line_3_Coordinate':
                {
                	if(!($GLOBALS['M_SUPPORT_EVENT_VA'] & IV_SUPPORT))
		        	{
		        		$responseOutput->errCode = STATUS_INVALID_PARAMETER;
		                SendResponse($responseOutput);
		        	}
		        	
                	$reqNameArr = explode("_", $name);
                	$coordIndex = ((int)$reqNameArr[1]) - 1;

					if($GLOBALS['M_ISP_TYPE'] != ISP_TYPE_WN3 && $coordIndex > 1) /** Only WN3 supports 3 object rules(When apply old box/dome models, need to add more condition for them)*/
                    {
                        $responseOutput->errCode = STATUS_INVALID_PARAMETER;
                        SendResponse($responseOutput);
                    }

					$pointLimit = 0;
                    if($reqNameArr[0] == 'DefinedArea')
                    {
                    	if (isset($_REQUEST['DefinedArea_' . ($coordIndex + 1) . '_Mode']))
                        {
                        	$tempDefinedAreaMode = array_search($_REQUEST['DefinedArea_' . ($coordIndex + 1) . '_Mode'], $DefinedAreaMode);
                            if ($tempDefinedAreaMode === FALSE)
                            {
                                $responseOutput->errCode = STATUS_INVALID_VALUE;
                                SendResponse($responseOutput);
                            }

                            $coordIndex = $coordIndex + 3; /** defined area index starts from 3 */

                            if ($tempDefinedAreaMode == 1)
                            {
                            	if($GLOBALS['M_SUPPORT_PTZ'] == PTZ_SUPPORT) /** PTZ model index rule : [3] -> entering, [4] -> appering */
                            	{
                            		$coordIndex = 4;

                            		/** use last field of objectRule to distinguish setting order between appeardisappear and enteringexiting	*/
                            		/** LineRuleDetail is to store client requested index number for appeardisappear defined area 				*/
	                            	$ivConf->objectRule[$GLOBALS['M_MAX_IV_OBJECT'] - 1]->dataInfo['LineRuleDetail']['value'] = (int)$reqNameArr[1];
                            	}
                            		
                                $ivConf->objectRule[$coordIndex]->dataInfo['AreaDisappear']['value'] = 1;
                                $ivConf->objectRule[$coordIndex]->dataInfo['AreaAppear']['value'] = 1;
                                $ivConf->objectRule[$coordIndex]->dataInfo['AreaExit']['value'] = 0;
                                $ivConf->objectRule[$coordIndex]->dataInfo['AreaEnter']['value'] = 0;
                            }
                            else 
                            {
                            	if($GLOBALS['M_SUPPORT_PTZ'] == PTZ_SUPPORT) /** PTZ model index rule : [3] -> entering, [4] -> appering */
                            	{
                            		$coordIndex = 3;

                            		/** use last field of objectRule to distinguish setting order between appeardisappear and enteringexiting	*/
                            		/** LineRule is to store client requested index number for enteringexiting defined area		 				*/
                            		$ivConf->objectRule[$GLOBALS['M_MAX_IV_OBJECT'] - 1]->dataInfo['LineRule']['value'] = (int)$reqNameArr[1];
                            	}
                            	
	                            if ($tempDefinedAreaMode == 2)
	                            {
	                                $ivConf->objectRule[$coordIndex]->dataInfo['AreaEnter']['value'] = 1;
	                                $ivConf->objectRule[$coordIndex]->dataInfo['AreaExit']['value'] = 0;
	                                $ivConf->objectRule[$coordIndex]->dataInfo['AreaDisappear']['value'] = 0;
	                                $ivConf->objectRule[$coordIndex]->dataInfo['AreaAppear']['value'] = 0;
	                            }
	                            else if ($tempDefinedAreaMode == 3)
	                            {
	                                $ivConf->objectRule[$coordIndex]->dataInfo['AreaExit']['value'] = 1;
	                                $ivConf->objectRule[$coordIndex]->dataInfo['AreaEnter']['value'] = 0;
	                                $ivConf->objectRule[$coordIndex]->dataInfo['AreaDisappear']['value'] = 0;
	                                $ivConf->objectRule[$coordIndex]->dataInfo['AreaAppear']['value'] = 0;
	                            }
	                            else
	                            {
	                                $ivConf->objectRule[$coordIndex]->dataInfo['AreaEnter']['value'] = 1;
	                                $ivConf->objectRule[$coordIndex]->dataInfo['AreaExit']['value'] = 1;
	                                $ivConf->objectRule[$coordIndex]->dataInfo['AreaDisappear']['value'] = 0;
	                                $ivConf->objectRule[$coordIndex]->dataInfo['AreaAppear']['value'] = 0;
	                            }
							}

                            $ivConf->objectRule[$coordIndex]->type = 2;

							if($GLOBALS['M_ISP_TYPE'] != ISP_TYPE_WN3 && $tempDefinedAreaMode == 1)
                            	$pointLimit = 2;
                            else
                            	$pointLimit = 4;
                        }
                        else
                        {
                        	$responseOutput->errCode = STATUS_MISSING_PARAMETER;
                            SendResponse($responseOutput);
                        }
                    }
                    else // Line
                    {
                    	if(isset($_REQUEST['Line_' . ($coordIndex + 1) . '_Mode']))
	                    {
	                    	if($GLOBALS['M_ISP_TYPE'] != ISP_TYPE_WN3 && $coordIndex >= 1) /** Only WN3 supports 3 object rules(When apply old box/dome models, need to add more condition for them)*/
		                    {
		                        $responseOutput->errCode = STATUS_INVALID_PARAMETER;
		                        SendResponse($responseOutput);
		                    }
		                    
	                    	$newLineMode = array_search($_REQUEST['Line_' . ($coordIndex + 1) . '_Mode'], $LineDetectionMode);
	                        if ($newLineMode === FALSE)
	                        {
	                            $responseOutput->errCode = STATUS_INVALID_VALUE;
	                            SendResponse($responseOutput);
	                        }

	                        if ($newLineMode == 3)
	                            $newLineMode = 2;
	                        
	                        $ivConf->objectRule[$coordIndex]->dataInfo['LineRule']['value'] = $newLineMode;

	                        $ivConf->objectRule[$coordIndex]->type = 1;
	                        $pointLimit = 2;
	                    }
	                    else
                        {
                        	$responseOutput->errCode = STATUS_MISSING_PARAMETER;
                            SendResponse($responseOutput);
                        }
                    }

                    $ivConf->fullScreenRule->dataInfo['FullAppear']['value'] = 0;
                    $ivConf->fullScreenRule->dataInfo['FullDisappear']['value'] = 0;

                    $Data = explode(",", $value);

                    if(count($Data) > $pointLimit * 2)
                    {
                    	$responseOutput->errCode = STATUS_INVALID_VALUE;
                        SendResponse($responseOutput);
                    }

					if(count($Data) == 4)
					{
						if(isset($_REQUEST['DefinedArea_1_Mode']) || isset($_REQUEST['DefinedArea_2_Mode']))
						{
							if( ($_REQUEST['DefinedArea_1_Mode'] == 'AppearDisappear') || ($_REQUEST['DefinedArea_2_Mode'] == 'AppearDisappear') )
							{
								$width = $Data[2] - $Data[0];
								$height = $Data[3] - $Data[1];

								if($width < 100 || $height < 100)
								{
									$responseOutput->errCode = STATUS_INVALID_VALUE;
									SendResponse($responseOutput);
								}
							}
						}
					}                    

                    for ($index = 0, $tempIndex = 0; $index < $pointLimit; ++$index, $tempIndex += 2)
                    {
                        $ivConf->objectRule[$coordIndex]->point[$index]->dataInfo['Valid']['value'] = 1;
                        $ivConf->objectRule[$coordIndex]->point[$index]->dataInfo['PosX']['value'] = $Data[$tempIndex];
                        $ivConf->objectRule[$coordIndex]->point[$index]->dataInfo['PosY']['value'] = $Data[$tempIndex + 1];
                        $ivConf->objectRule[$coordIndex]->point[$index]->payload = MakePayload($ivConf->objectRule[$coordIndex]->point[$index]->dataInfo);
                    }

                    for ($index = $pointLimit; $index < $GLOBALS['M_MAX_IV_LINE_POINT']; ++$index)
                    {
                        $ivConf->objectRule[$coordIndex]->point[$index]->InitData();
                    }

                    for ($index = 0; $index < $GLOBALS['M_MAX_IV_OBJECT']; ++$index)
                    {
                        $ivConf->objectRule[$index]->SetPayload();
                    }
                }break;

            case 'EntireAreaMode':
                {
                	if(!($GLOBALS['M_SUPPORT_EVENT_VA'] & IV_SUPPORT))
		        	{
		        		$responseOutput->errCode = STATUS_INVALID_PARAMETER;
		                SendResponse($responseOutput);
		        	}

		        	if(!CheckModelName('CHECK_IV_ENTIREAREA_MODE'))
		        	{
		        		$responseOutput->errCode = STATUS_INVALID_PARAMETER;
		                SendResponse($responseOutput);
		        	}
		        	
                    $newValueEntireMode = array_search($value, $EntireAreaMode);
                    if ($newValueEntireMode === FALSE)
                    {
                        $responseOutput->errCode = STATUS_INVALID_VALUE;
                        SendResponse($responseOutput);
                    }
                    
                    if ($newValueEntireMode == 1)
                    {
                        $ivConf->fullScreenRule->dataInfo['FullAppear']['value'] = 1;
                        $ivConf->fullScreenRule->dataInfo['FullSceneChange']['value'] = 0;
                    }
                    else if($newValueEntireMode == 2)
                    {
                    	$ivConf->fullScreenRule->dataInfo['FullSceneChange']['value'] = 1;
                    	$ivConf->fullScreenRule->dataInfo['FullAppear']['value'] = 0;
                    }
                    else
                    {
                    	$ivConf->fullScreenRule->dataInfo['FullAppear']['value'] = 0;
                    	$ivConf->fullScreenRule->dataInfo['FullDisappear']['value'] = 0;
                    	$ivConf->fullScreenRule->dataInfo['FullSceneChange']['value'] = 0;
                    }
                } break;
        }
    }
}

///////////////////////////////////////////////
// Video Analysis
///////////////////////////////////////////////
function submenu_videoanalysis()
{
    $responseOutput = new ResponseOutput();
    $responseOutput->outputMsg = '';

    global $boolArray;
    global $EventAreaMode;
    global $DetectionType;
	
    if(isset($_REQUEST['Channel']) && $_REQUEST['Channel'] != 0)
    {
        $responseOutput->errCode = STATUS_INVALID_VALUE;
        return $responseOutput;
    }

    $classInstances = GetClassInstance('va');
    $VAConf = $classInstances['VAConfiguration'];

    $megaModeConf = new VideoSourceSelection();
    $megaModeConf = $GLOBALS['SOCKET_MANAGER']->Connection($megaModeConf);

	$resMaxWidth = 0;
	$resMaxHeight = 0;
    getMaxWidthHeight($resMaxWidth, $resMaxHeight, $megaModeConf->dataInfo['VideoSource']['value']);

    if($GLOBALS['M_SUPPORT_PTZ'] == PTZ_SUPPORT) /** PTZ model index rule : [3] -> entering, [4] -> appering */
	{
		/** initialize appear/enetering index information only for PTZ models */
		$isEnableAppear = TRUE;
		$isEnableEnter = TRUE;

		/* update removed defined area index information */
		if($VAConf->ivConf->objectRule[4]->dataInfo['AreaAppear']['value'] == 0 && $VAConf->ivConf->objectRule[4]->dataInfo['AreaDisappear']['value'] == 0)
		{
			$VAConf->ivConf->objectRule[$GLOBALS['M_MAX_IV_OBJECT'] - 1]->dataInfo['LineRuleDetail']['value'] = 0;
			$isEnableAppear = FALSE;
		}

		if($VAConf->ivConf->objectRule[3]->dataInfo['AreaEnter']['value'] == 0 && $VAConf->ivConf->objectRule[3]->dataInfo['AreaExit']['value'] == 0)
		{
			$VAConf->ivConf->objectRule[$GLOBALS['M_MAX_IV_OBJECT'] - 1]->dataInfo['LineRule']['value'] = 0;
			$isEnableEnter = FALSE;
		}
		
		if($isEnableAppear && $VAConf->ivConf->objectRule[$GLOBALS['M_MAX_IV_OBJECT'] - 1]->dataInfo['LineRuleDetail']['value'] == 0)
		{
			if($VAConf->ivConf->objectRule[$GLOBALS['M_MAX_IV_OBJECT'] - 1]->dataInfo['LineRule']['value'] == 2)
			{
				$VAConf->ivConf->objectRule[$GLOBALS['M_MAX_IV_OBJECT'] - 1]->dataInfo['LineRuleDetail']['value'] = 1;
			}
			else
			{
				$VAConf->ivConf->objectRule[$GLOBALS['M_MAX_IV_OBJECT'] - 1]->dataInfo['LineRuleDetail']['value'] = 2;
			}
		}

		if($isEnableEnter && $VAConf->ivConf->objectRule[$GLOBALS['M_MAX_IV_OBJECT'] - 1]->dataInfo['LineRule']['value'] == 0)
		{
			if($VAConf->ivConf->objectRule[$GLOBALS['M_MAX_IV_OBJECT'] - 1]->dataInfo['LineRuleDetail']['value'] == 1)
			{
				$VAConf->ivConf->objectRule[$GLOBALS['M_MAX_IV_OBJECT'] - 1]->dataInfo['LineRule']['value'] = 2;
			}
			else
			{
				$VAConf->ivConf->objectRule[$GLOBALS['M_MAX_IV_OBJECT'] - 1]->dataInfo['LineRule']['value'] = 1;
			}
		}

		$VAConf->ivConf->objectRule[$GLOBALS['M_MAX_IV_OBJECT'] - 1]->SetPayload();
	}

    if ($_REQUEST['action'] == 'set')
    {
        if (count($_REQUEST) < 3)
        {
            $responseOutput->errCode = STATUS_MISSING_PARAMETER;
            return $responseOutput;
        }

		/** ObjectSize parameter is not supported **/
        $allowed_params = array("msubmenu", "action", "Channel", "DetectionType", "Sensitivity", "MinimumObjectSize", "MaximumObjectSize", "MinimumObjectSizeInPixels", 
        							"MaximumObjectSizeInPixels", "ROIGrid", "GridSize", "ROI_1_Coordinates", "ROI_1_Coordinate", "ROI_2_Coordinates", "ROI_2_Coordinate", 
        							"ROI_3_Coordinates", "ROI_3_Coordinate", "ROI_4_Coordinates", "ROI_4_Coordinate", "ROIMode", "DetectionResultOverlay", "DisplayRules", 
        							"DefinedArea_1_Mode", "DefinedArea_2_Mode", "DefinedArea_3_Mode", "DefinedArea_1_Coordinates", "DefinedArea_1_Coordinate", 
        							"DefinedArea_2_Coordinates", "DefinedArea_2_Coordinate", "DefinedArea_3_Coordinates", "DefinedArea_3_Coordinate", "EntireAreaMode", 
        							"Line_1_Mode", "Line_2_Mode", "Line_3_Mode", "Line_1_Coordinates", "Line_1_Coordinate", "Line_2_Coordinates", "Line_2_Coordinate", 
        							"Line_3_Coordinates", "Line_3_Coordinate");

        if(CheckAllowedParams($allowed_params) === FALSE)
        {
        	$responseOutput->errCode = STATUS_INVALID_PARAMETER;
            return $responseOutput;
        }

        if(isset($_REQUEST['DetectionType']))
        {
        	$newValue = array_search($_REQUEST['DetectionType'], $DetectionType);
        	if($newValue === FALSE)
        	{
                $responseOutput->errCode = STATUS_INVALID_VALUE;
                return $responseOutput;
            }

			/* if camera doesn't support IV(VA) it will return Error */
        	if(!($GLOBALS['M_SUPPORT_EVENT_VA'] & IV_SUPPORT) && ($newValue == 1 || $newValue == 2))
        	{
        		$responseOutput->errCode = STATUS_INVALID_VALUE;
                return $responseOutput;
        	}

			/*PTZ Models doesn't support MD/IV Mode*/
        	if($GLOBALS['M_SUPPORT_PTZ'] != PTZ_NOT_SUPPORT && $newValue == 2)
        	{
        		$responseOutput->errCode = STATUS_INVALID_VALUE;
                return $responseOutput;
        	}
        	
            if ($newValue == 0 || $newValue == 1 || $newValue == 2) //0=>MotionDetection,1=>IntelligentVideo,2=>MD/IV
            {
                $VAConf->dataInfo['Mode']['value'] = $newValue;
                $VAConf->mdConf->dataInfo['Enabled']['value'] = 1;
                $VAConf->ivConf->dataInfo['Enabled']['value'] = 1;
            }
            else //Off
            {
                $VAConf->mdConf->dataInfo['Enabled']['value'] = 0;
                $VAConf->ivConf->dataInfo['Enabled']['value'] = 0;
            }
        }

		if($GLOBALS['M_SUPPORT_PTZ'] == PTZ_NOT_SUPPORT)
		{
			SetVideoAnalysis($VAConf->mdConf, $resMaxWidth, $resMaxHeight);
		}
		else
		{
			if($VAConf->dataInfo['Mode']['value'] == 0)
			{
		        SetVideoAnalysis($VAConf->mdConf, $resMaxWidth, $resMaxHeight);
		    }
		    else
		    {
		    	SetVideoAnalysis($VAConf->ivConf, $resMaxWidth, $resMaxHeight);
		  	}
	  	}
        
        foreach ($_REQUEST as $name => $value)
        {
            switch ($name)
            {
            	case 'DisplayRules':
		            {
		            	if($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ)
		            	{
							$responseOutput->errCode = STATUS_INVALID_PARAMETER;
		            		return $responseOutput;
		            	}
		            	
		            	if($VAConf->dataInfo['Mode']['value'] == 0)
		            	{
		            		$responseOutput->errCode = STATUS_INVALID_PARAMETER;
	                        return $responseOutput;
		            	}
		            	
		            	$newValue = array_search($value, $boolArray);
	                    if($newValue === FALSE)
	                    {
	                        $responseOutput->errCode = STATUS_INVALID_VALUE;
	                        return $responseOutput;
	                    }

	                    $VAConf->ivConf->dataInfo['Overlay']['value'] = $newValue;
		            }
		            break;
	            case 'DetectionResultOverlay':
	                {
	                	if($GLOBALS['M_SUPPORT_PTZ'] && $VAConf->dataInfo['Mode']['value'] == 0)
	                	{
	                		$responseOutput->errCode = STATUS_INVALID_PARAMETER;
	                        return $responseOutput;
	                	}
	                	
	                	/** LitenNet Models don't support */
	                	if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_HISILICON)
	                	{
	                		$responseOutput->errCode = STATUS_INVALID_PARAMETER;
	                		return $responseOutput;
	                	}
	                	
	                    $newValue = array_search($value, $boolArray);
	                    if($newValue === FALSE)
	                    {
	                        $responseOutput->errCode = STATUS_INVALID_VALUE;
	                        return $responseOutput;
	                    }

	                    $VAConf->ivConf->dataInfo['VABoxDisplay']['value'] = $newValue;

	                    if($GLOBALS['M_SUPPORT_PTZ'] == PTZ_NOT_SUPPORT)
						{
							/*
								FishEye model have DetectionResultOverlay option on MD mode
								Box model have DetectionResultOverlay option on every mode
							*/
							$VAConf->mdConf->dataInfo['VABoxDisplay']['value'] = $newValue;
						}
						else
						{
							/*PTZ model have DetectionResultOverlay option on IV mode*/
							$VAConf->ivConf->dataInfo['VABoxDisplay']['value'] = $newValue;
						}
	                }
	                break;
                case 'ROIMode':
                    {
                        $value = array_search($value, $EventAreaMode);
                        if($value === FALSE)
                        {
                        	$responseOutput->errCode = STATUS_INVALID_VALUE;
                            return $responseOutput;
                        }

                        $VAConf->mdConf->dataInfo['ObjectMode']['value'] = $value;
                    }
                    break;

                case 'ROI_1_Coordinates': case 'ROI_2_Coordinates': case 'ROI_3_Coordinates': case 'ROI_4_Coordinates':
                case 'ROI_1_Coordinate': case 'ROI_2_Coordinate': case 'ROI_3_Coordinate': case 'ROI_4_Coordinate':
                    {
                    	$reqNameArray = explode("_", $name);
                        $areaIndex = ((int)$reqNameArray[1]) - 1;
                        $areaData = explode(",", $value);

                        if (CheckModelName('CHECK_MD_POLY_SUPPORT'))
                        {
                            if (count($areaData) != 8)
                            {
                                $responseOutput->errCode = STATUS_INVALID_VALUE;
                                return $responseOutput;
                            }
                        }
                        else
                        {
                            if (count($areaData) != 4)
                            {
                                $responseOutput->errCode = STATUS_INVALID_VALUE;
                                return $responseOutput;
                            }
                        }

                        $VAConf->mdConf->objectRule[$areaIndex]->dataInfo['NumPoint']['value'] = 2;
                        $VAConf->mdConf->objectRule[$areaIndex]->dataInfo['Index']['value'] = $areaIndex;
                        $VAConf->mdConf->objectRule[$areaIndex]->mdPoint[0]->dataInfo['PosX']['value'] = $areaData[0];
                        $VAConf->mdConf->objectRule[$areaIndex]->mdPoint[0]->dataInfo['PosY']['value'] = $areaData[1];
                        $VAConf->mdConf->objectRule[$areaIndex]->mdPoint[1]->dataInfo['PosX']['value'] = $areaData[2];
                        $VAConf->mdConf->objectRule[$areaIndex]->mdPoint[1]->dataInfo['PosY']['value'] = $areaData[3];

                        if (CheckModelName('CHECK_MD_POLY_SUPPORT'))
                        {
                            $VAConf->mdConf->objectRule[$areaIndex]->dataInfo['NumPoint']['value'] = 4;
                            $VAConf->mdConf->objectRule[$areaIndex]->mdPoint[2]->dataInfo['PosX']['value'] = $areaData[4];
                            $VAConf->mdConf->objectRule[$areaIndex]->mdPoint[2]->dataInfo['PosY']['value'] = $areaData[5];
                            $VAConf->mdConf->objectRule[$areaIndex]->mdPoint[3]->dataInfo['PosX']['value'] = $areaData[6];
                            $VAConf->mdConf->objectRule[$areaIndex]->mdPoint[3]->dataInfo['PosY']['value'] = $areaData[7];

                            $VAConf->mdConf->objectRule[$areaIndex]->mdPoint[2]->payload = MakePayload($VAConf->mdConf->objectRule[$areaIndex]->mdPoint[2]->dataInfo);
                            $VAConf->mdConf->objectRule[$areaIndex]->mdPoint[3]->payload = MakePayload($VAConf->mdConf->objectRule[$areaIndex]->mdPoint[3]->dataInfo);
                        }
                        
                        $VAConf->mdConf->objectRule[$areaIndex]->mdPoint[0]->payload = MakePayload($VAConf->mdConf->objectRule[$areaIndex]->mdPoint[0]->dataInfo);
                        $VAConf->mdConf->objectRule[$areaIndex]->mdPoint[1]->payload = MakePayload($VAConf->mdConf->objectRule[$areaIndex]->mdPoint[1]->dataInfo);
                        $VAConf->mdConf->objectRule[$areaIndex]->SetPayload();
                    }
                    break;
            }
        }

        SetIVRule($VAConf->ivConf);

        $VAConf->mdConf->SetPayload();
        $VAConf->ivConf->SetPayload();
        $VAConf->SetPayload();
        $VAConf->headerInfo['Action'] = ACTION_SET;
        $GLOBALS['SOCKET_MANAGER']->Connection($VAConf);

        $responseOutput->outputMsg = 'OK';
    }
    else if ($_REQUEST['action'] == 'remove')
    {
    	$allowed_params = array("msubmenu", "action", "Channel", "LineIndex", "DefinedAreaIndex", "ROIIndex");

        if(CheckAllowedParams($allowed_params) === FALSE)
        {
        	$responseOutput->errCode = STATUS_INVALID_PARAMETER;
            return $responseOutput;
        }
        
        $removeAll = TRUE;

        foreach ($_REQUEST as $name => $value)
        {
            switch ($name)
            {
                case 'DefinedAreaIndex': case 'LineIndex':
                    {
                    	if(!($GLOBALS['M_SUPPORT_EVENT_VA'] & IV_SUPPORT))
			        	{
			        		$responseOutput->errCode = STATUS_INVALID_PARAMETER;
			                return $responseOutput;
			        	}
			        	
                    	$Indexlist = explode(",", $value);
                        $Indexcount = count($Indexlist);

                        if(array_search("All", $Indexlist) !== FALSE && $Indexcount > 1)
                        {
                        	$responseOutput->errCode = STATUS_INVALID_VALUE;
			                return $responseOutput;
                        }

                        if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3)
                        {
                            if ($Indexcount > 3)
                            {
                                $responseOutput->errCode = STATUS_INVALID_VALUE;
                                return $responseOutput;
                            }
                        }
                        else
                        {
                            if ($Indexcount > 2)
                            {
                                $responseOutput->errCode = STATUS_INVALID_VALUE;
                                return $responseOutput;
                            }
                        }
                        
                        if ($name == 'DefinedAreaIndex')
                        {
                        	if($value == 'All')
                        	{
                        		for($rmIdx = 3 ; $rmIdx < $GLOBALS['M_MAX_IV_OBJECT'] ; $rmIdx++)
                        		{
                        			RemoveIVRule($VAConf->ivConf, $rmIdx);
                        		}
                        	}
                        	else
                        	{
                        		for($i = 0 ; $i < $Indexcount ; $i++)
                        		{
                        			$reqRemoveIdx = ((int)$Indexlist[$i]) - 1;

                        			if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3)
			                        {
			                            if ($reqRemoveIdx >= 3)
			                            {
			                                $responseOutput->errCode = STATUS_INVALID_VALUE;
			                                return $responseOutput;
			                            }
			                        }
			                        else
			                        {
			                            if ($reqRemoveIdx >= 2)
			                            {
			                                $responseOutput->errCode = STATUS_INVALID_VALUE;
			                                return $responseOutput;
			                            }
			                        }

                        			$rmIdx = $reqRemoveIdx + 3; /** defined area starts from [3] */

                        			if($GLOBALS['M_SUPPORT_PTZ'] == PTZ_SUPPORT)
			                        {
			                        	if($rmIdx == 3)
			                        	{
			                        		if($VAConf->ivConf->objectRule[$GLOBALS['M_MAX_IV_OBJECT'] - 1]->dataInfo['LineRule']['value'] == 2 || 
			                        				($VAConf->ivConf->objectRule[$GLOBALS['M_MAX_IV_OBJECT'] - 1]->dataInfo['LineRule']['value'] == 0 && 
			                        						$VAConf->ivConf->objectRule[$GLOBALS['M_MAX_IV_OBJECT'] - 1]->dataInfo['LineRuleDetail']['value'] == 1))
			                        		{
				                        		$rmIdx = 4;
				                        		$VAConf->ivConf->objectRule[$GLOBALS['M_MAX_IV_OBJECT'] - 1]->dataInfo['LineRuleDetail']['value'] = 0;
				                        		$VAConf->ivConf->objectRule[$GLOBALS['M_MAX_IV_OBJECT'] - 1]->SetPayload();
				                        	}
			                        	}
			                        	else if($rmIdx == 4)
			                        	{
			                        		if($VAConf->ivConf->objectRule[$GLOBALS['M_MAX_IV_OBJECT'] - 1]->dataInfo['LineRuleDetail']['value'] == 1 || 
			                        				($VAConf->ivConf->objectRule[$GLOBALS['M_MAX_IV_OBJECT'] - 1]->dataInfo['LineRuleDetail']['value'] == 0 && 
			                        						$VAConf->ivConf->objectRule[$GLOBALS['M_MAX_IV_OBJECT'] - 1]->dataInfo['LineRule']['value'] == 2))
			                        		{
				                        		$rmIdx = 3;
				                        		$VAConf->ivConf->objectRule[$GLOBALS['M_MAX_IV_OBJECT'] - 1]->dataInfo['LineRule']['value'] = 0;
				                        		$VAConf->ivConf->objectRule[$GLOBALS['M_MAX_IV_OBJECT'] - 1]->SetPayload();
				                        	}
			                        	}
			                        }

                        			if ($VAConf->ivConf->objectRule[$rmIdx]->type != 2)
                                    {
                                        $responseOutput->errCode = STATUS_INVALID_VALUE;
                                        return $responseOutput;
                                    }

                                    RemoveIVRule($VAConf->ivConf, $rmIdx);
                        		}
                        	}
                        }
                        else if ($name == 'LineIndex')
                        {
                        	if($value == 'All')
                        	{
                        		for ($rmIdx = 0; $rmIdx < 3; ++$rmIdx)
                        		{
                        			RemoveIVRule($VAConf->ivConf, $rmIdx);
                        		}
                        	}
                        	else
                        	{
                        		for($i = 0 ; $i < $Indexcount ; $i++)
                        		{
                        			$reqRemoveIdx = ((int)$Indexlist[$i]) - 1;

                        			if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3)
			                        {
			                            if ($reqRemoveIdx >= 3)
			                            {
			                                $responseOutput->errCode = STATUS_INVALID_VALUE;
			                                return $responseOutput;
			                            }
			                        }
			                        else
			                        {
			                            if ($reqRemoveIdx >= 1)
			                            {
			                                $responseOutput->errCode = STATUS_INVALID_VALUE;
			                                return $responseOutput;
			                            }
			                        }

			                        if ($VAConf->ivConf->objectRule[$reqRemoveIdx]->type != 1)
                                    {
                                        $responseOutput->errCode = STATUS_INVALID_VALUE;
                                        return $responseOutput;
                                    }

                                    RemoveIVRule($VAConf->ivConf, $reqRemoveIdx);
                        		}
                        	}
                        }

                        $removeAll = FALSE;
                    }
                    break;
                case 'ROIIndex':
                    {
                        $Indexlist = explode(",", $value);
                        $Indexcount = count($Indexlist);

                        if ($Indexcount > 4)
                        {
                            $responseOutput->errCode = STATUS_INVALID_VALUE;
                            return $responseOutput;
                        }

                        if(array_search("All", $Indexlist) !== FALSE && $Indexcount > 1)
                        {
                        	$responseOutput->errCode = STATUS_INVALID_VALUE;
			                return $responseOutput;
                        }

                        if($value == 'All')
                        {
                        	for($rmIdx = 0 ; $rmIdx < $GLOBALS['M_MAX_MD_AREA'] ; $rmIdx++)
                        	{
                        		$VAConf->mdConf->objectRule[$rmIdx]->InitData();
                                $VAConf->mdConf->objectRule[$rmIdx]->SetPayload();
                        	}
                        }
                        else
                        {
                        	for($i = 0 ; $i < $Indexcount ; $i++)
                        	{
                        		$rmIdx = ((int)$Indexlist[$i]) - 1;

                        		if($rmIdx < 0 || $rmIdx > 3)
                        		{
                        			$responseOutput->errCode = STATUS_INVALID_VALUE;
		                            return $responseOutput;
                        		}

                        		$VAConf->mdConf->objectRule[$rmIdx]->InitData();
                                $VAConf->mdConf->objectRule[$rmIdx]->SetPayload();
                        	}
                        }
                        $removeAll = FALSE;
                    }
                    break;
            }
        }

        if ($removeAll)
        {
            /** remove Defined Area & Line */
            for ($index=0; $index < $GLOBALS['M_MAX_IV_OBJECT']; ++$index)
            {
            	RemoveIVRule($VAConf->ivConf, $index);
            }

            /** remove ROI */
            for ($index = 0; $index < $GLOBALS['M_MAX_MD_AREA'] ; ++$index)
            {
                $VAConf->mdConf->objectRule[$index]->InitData();
                $VAConf->mdConf->objectRule[$index]->SetPayload();
            }
        }

        $VAConf->mdConf->SetPayload();
        $VAConf->ivConf->SetPayload();
        $VAConf->SetPayload();
        $VAConf->headerInfo['Action'] = ACTION_SET;
        $GLOBALS['SOCKET_MANAGER']->Connection($VAConf);

        $responseOutput->outputMsg = 'OK';
    }
    else if ($_REQUEST['action'] == 'view')
    {
    	/*
    		Box Model's supporting Detection Type = MotionDetection, IntelligentVideo, Off, MDAndIV
    		PTZ Model's supporting Detection Type = MotionDetection, IntelligentVideo, Off
    	*/
    	
    	$allowed_params = array("msubmenu", "action", "Channel", "DetectionType");

        if(CheckAllowedParams($allowed_params) === FALSE)
        {
        	$responseOutput->errCode = STATUS_INVALID_PARAMETER;
            return $responseOutput;
        }
        
        $IVEnabled = $VAConf->ivConf->dataInfo['Enabled']['value'];
        $MDEnabled = $VAConf->mdConf->dataInfo['Enabled']['value'];
        
        if ($IVEnabled == 1 || $MDEnabled ==1 )
        {
            $responseOutput->outputMsg .= 'Channel.0.DetectionType=' . $DetectionType[$VAConf->dataInfo['Mode']['value']] . "\r\n"; 
        }
        else
        {
            $responseOutput->outputMsg .= 'Channel.0.DetectionType=' . $DetectionType[3] . "\r\n";
        }

		if($GLOBALS['M_SUPPORT_PTZ'] == PTZ_NOT_SUPPORT)
		{
			/*
				FishEye model have DetectionResultOverlay option on MD mode
				Box model have DetectionResultOverlay option on every mode
			*/
			if ($GLOBALS['M_ISP_TYPE'] != ISP_TYPE_HISILICON)
			{
				$responseOutput->outputMsg .= 'Channel.0.DetectionResultOverlay=' . $boolArray[$VAConf->mdConf->dataInfo['VABoxDisplay']['value']] . "\r\n";
			}
		}
		else
		{
			/*PTZ model have DetectionResultOverlay option on IV mode*/
			$responseOutput->outputMsg .= 'Channel.0.DetectionResultOverlay=' . $boolArray[$VAConf->ivConf->dataInfo['VABoxDisplay']['value']] . "\r\n";
		}
        
		/** Shall Be displayed only for VA*/
		if ($GLOBALS['M_SUPPORT_EVENT_VA'] & IV_SUPPORT)
		{
		    $responseOutput->outputMsg .= 'Channel.0.DisplayRules=' . $boolArray[$VAConf->ivConf->dataInfo['Overlay']['value']] . "\r\n";
		}

	    if(isset($_REQUEST['DetectionType']))
	    {
			if($_REQUEST['DetectionType'] == "Off")
			{
				if($GLOBALS['M_SUPPORT_PTZ'] == PTZ_NOT_SUPPORT)
				{
					$Conf = $VAConf->mdConf;
				}
				else
				{
					if($VAConf->dataInfo['Mode']['value'] == 0)	//MD
					{
						$Conf = $VAConf->mdConf;
					}
					else if($VAConf->dataInfo['Mode']['value'] == 1)	//IV
					{
						$Conf = $VAConf->ivConf;
					}
					else 
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
			}
			else if($_REQUEST['DetectionType'] == "MotionDetection")
			{
				$Conf = $VAConf->mdConf;
			}
			else
			{
				if(($GLOBALS['M_SUPPORT_EVENT_VA'] & IV_SUPPORT) != IV_SUPPORT)
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
		            return $responseOutput;
				}

				if($GLOBALS['M_SUPPORT_PTZ'] == PTZ_NOT_SUPPORT)
				{
					if($_REQUEST['DetectionType'] == "IntelligentVideo" || $_REQUEST['DetectionType'] == "MDAndIV")
					{					
						$Conf = $VAConf->mdConf;
					}
				}
				else
				{
					if($_REQUEST['DetectionType'] == "IntelligentVideo")
					{
						$Conf = $VAConf->ivConf;
					}
					else
					{
						$responseOutput->errCode = STATUS_INVALID_VALUE;
						return $responseOutput;
					}
				}
			}
			$responseOutput->outputMsg .= ViewVideoAnalysis($Conf, $resMaxWidth, $resMaxHeight);
		}
		else
		{
			if($GLOBALS['M_SUPPORT_PTZ'] == PTZ_NOT_SUPPORT)
			{
				$Conf = $VAConf->mdConf;
			}
			else
			{
				if($VAConf->dataInfo['Mode']['value'] == 0)	//MD
				{
					$Conf = $VAConf->mdConf;
				}
				else if($VAConf->dataInfo['Mode']['value'] == 1)	//IV
				{
					$Conf = $VAConf->ivConf;
				}
				else 
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
			}
			$responseOutput->outputMsg .= ViewVideoAnalysis($Conf, $resMaxWidth, $resMaxHeight);
		}
		/** MD Object rules */
		if($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ)
		{
			$responseOutput->outputMsg .= 'Channel.0.ROIMode=' . $EventAreaMode[1] . "\r\n";
		}
		else
		{
			$responseOutput->outputMsg .= 'Channel.0.ROIMode=' . $EventAreaMode[$VAConf->mdConf->dataInfo['ObjectMode']['value']] . "\r\n";
		}

        for ($index = 0; $index < $GLOBALS['M_MAX_MD_AREA']; ++$index)
        {
            if ($VAConf->mdConf->objectRule[$index]->dataInfo['NumPoint']['value'] == 0)
            {
                continue;
            }

            $responseOutput->outputMsg .= 'Channel.0.ROI.' . ($index + 1) . '.Coordinate=';
            $responseOutput->outputMsg .= $VAConf->mdConf->objectRule[$index]->mdPoint[0]->dataInfo['PosX']['value'] . ',';
            $responseOutput->outputMsg .= $VAConf->mdConf->objectRule[$index]->mdPoint[0]->dataInfo['PosY']['value'] . ',';
            $responseOutput->outputMsg .= $VAConf->mdConf->objectRule[$index]->mdPoint[1]->dataInfo['PosX']['value'] . ',';
            $responseOutput->outputMsg .= $VAConf->mdConf->objectRule[$index]->mdPoint[1]->dataInfo['PosY']['value'];

            if ($VAConf->mdConf->objectRule[$index]->dataInfo['NumPoint']['value'] == 4) //Poly
            {
                $responseOutput->outputMsg .= ',' . $VAConf->mdConf->objectRule[$index]->mdPoint[2]->dataInfo['PosX']['value'] . ',';
                $responseOutput->outputMsg .= $VAConf->mdConf->objectRule[$index]->mdPoint[2]->dataInfo['PosY']['value'] . ',';
                $responseOutput->outputMsg .= $VAConf->mdConf->objectRule[$index]->mdPoint[3]->dataInfo['PosX']['value'] . ',';
                $responseOutput->outputMsg .= $VAConf->mdConf->objectRule[$index]->mdPoint[3]->dataInfo['PosY']['value'];
            }
            
            $responseOutput->outputMsg .= "\r\n";
        }

        $responseOutput->outputMsg .= ViewIVRule($VAConf->ivConf);
    }
    else
    {
        $responseOutput->errCode = STATUS_ACTION_NOT_FOUND;
        return $responseOutput;
    }

    $responseOutput->errCode = STATUS_OK;
    return $responseOutput;
}

///////////////////////////////////////////////
//Facedetection
///////////////////////////////////////////////
function submenu_facedetection()
{
    $responseOutput = new ResponseOutput();
    $responseOutput->outputMsg = '';
    
    global $boolArray;
    global $EventAreaMode;

    if (isset($_REQUEST['Channel']) && $_REQUEST['Channel'] != '0')
    {
        $responseOutput->errCode = STATUS_INVALID_VALUE;
        return $responseOutput;
    }

    $classInstances = GetClassInstance('fd');
    $fdConf = $classInstances['FDConfiguration'];

    if ($_REQUEST['action'] == 'set')
    {
        if (count($_REQUEST) < 3)
        {
            $responseOutput->errCode = STATUS_MISSING_PARAMETER;
            return $responseOutput;
        }

        $allowed_params = array("msubmenu", "action", "Channel", "Enable", "Sensitivity", "MarkDetectedFaces", "DetectionAreaMode", "DetectionArea_1_Coordinates", "DetectionArea_1_Coordinate", 
        						"DetectionArea_2_Coordinates", "DetectionArea_2_Coordinate", "DetectionArea_3_Coordinates", "DetectionArea_3_Coordinate", 
        						"DetectionArea_4_Coordinates", "DetectionArea_4_Coordinate");

        if(CheckAllowedParams($allowed_params) === FALSE)
        {
        	$responseOutput->errCode = STATUS_INVALID_PARAMETER;
            return $responseOutput;
        }
        
        foreach ($_REQUEST as $name => $value)
        {
            switch ($name)
            {
                case 'Enable':
                    {
                        $value = array_search($value, $boolArray);
                        if ($value === FALSE)
                        {
                            $responseOutput->errCode = STATUS_INVALID_VALUE;
                            return $responseOutput;
                        }
                        $fdConf->dataInfo['Enabled']['value'] = $value;
                    }
                    break;
                case 'MarkDetectedFaces':
                    {
                        $value = array_search($value, $boolArray);
                        if ($value === FALSE)
                        {
                            $responseOutput->errCode = STATUS_INVALID_VALUE;
                            return $responseOutput;
                        }
                        $fdConf->dataInfo['FDBoxDisplay']['value'] = $value;
                    } break;
                case 'Sensitivity':
                    {
                    	if($value < 1 || $value > 10)
                    	{
                    		$responseOutput->errCode = STATUS_INVALID_VALUE;
                            return $responseOutput;
                    	}
                        $fdConf->dataInfo['Sensitivity']['value'] = $value;
                    }
                    break;
                case 'DetectionAreaMode':
                    {
                        $value = array_search($value, $EventAreaMode);
                        $fdConf->dataInfo['ObjectMode']['value'] = $value;
                    }
                    break;
                case 'DetectionArea_1_Coordinates':	case 'DetectionArea_2_Coordinates':	case 'DetectionArea_3_Coordinates':	case 'DetectionArea_4_Coordinates':
                case 'DetectionArea_1_Coordinate':	case 'DetectionArea_2_Coordinate':	case 'DetectionArea_3_Coordinate':	case 'DetectionArea_4_Coordinate':
                    {
                    	$reqCmdList = explode("_", $name);
                    	$areaIndex = ((int)$reqCmdList[1]) - 1;
                        $areaData = explode(",", $value);

                        if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3 || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ) /** support poly */
                        {
                            if (count($areaData) != 8)
                            {
                                $responseOutput->errCode = STATUS_INVALID_VALUE;
                                return $responseOutput;
                            }
                            $fdConf->objectConf[$areaIndex]->dataInfo['NumPoint']['value'] = 4;
                        }
                        else
                        {
                            if (count($areaData) != 4)
                            {
                                $responseOutput->errCode = STATUS_INVALID_VALUE;
                                return $responseOutput;
                            }
                            $fdConf->objectConf[$areaIndex]->dataInfo['NumPoint']['value'] = 2;
                        }
                        
                        $fdConf->objectConf[$areaIndex]->dataInfo['Index']['value'] = $areaIndex;
                        $fdConf->objectConf[$areaIndex]->fdPoint[0]->dataInfo['PosX']['value'] = $areaData[0];
                        $fdConf->objectConf[$areaIndex]->fdPoint[0]->dataInfo['PosY']['value'] = $areaData[1];
                        $fdConf->objectConf[$areaIndex]->fdPoint[1]->dataInfo['PosX']['value'] = $areaData[2];
                        $fdConf->objectConf[$areaIndex]->fdPoint[1]->dataInfo['PosY']['value'] = $areaData[3];
                        
                        if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3 || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ)
                        {
                            $fdConf->objectConf[$areaIndex]->fdPoint[2]->dataInfo['PosX']['value'] = $areaData[4];
                            $fdConf->objectConf[$areaIndex]->fdPoint[2]->dataInfo['PosY']['value'] = $areaData[5];
                            $fdConf->objectConf[$areaIndex]->fdPoint[3]->dataInfo['PosX']['value'] = $areaData[6];
                            $fdConf->objectConf[$areaIndex]->fdPoint[3]->dataInfo['PosY']['value'] = $areaData[7];

                            $fdConf->objectConf[$areaIndex]->fdPoint[2]->payload = MakePayload($fdConf->objectConf[$areaIndex]->fdPoint[2]->dataInfo);
                            $fdConf->objectConf[$areaIndex]->fdPoint[3]->payload = MakePayload($fdConf->objectConf[$areaIndex]->fdPoint[3]->dataInfo);
                        }
                        
                        $fdConf->objectConf[$areaIndex]->fdPoint[0]->payload = MakePayload($fdConf->objectConf[$areaIndex]->fdPoint[0]->dataInfo);
                        $fdConf->objectConf[$areaIndex]->fdPoint[1]->payload = MakePayload($fdConf->objectConf[$areaIndex]->fdPoint[1]->dataInfo);
                        
                        $fdConf->objectConf[$areaIndex]->SetPayload();
                    } break;
            }
        }

        $fdConf->SetPayload();
        $fdConf->headerInfo['Action'] = ACTION_SET;
        $GLOBALS['SOCKET_MANAGER']->Connection($fdConf);

        $responseOutput->outputMsg = 'OK';
    }
    else if ($_REQUEST['action'] == 'remove')
    {
    	$allowed_params = array("msubmenu", "action", "Channel", "DetectionAreaIndex");

        if(CheckAllowedParams($allowed_params) === FALSE)
        {
        	$responseOutput->errCode = STATUS_INVALID_PARAMETER;
            return $responseOutput;
        }
        
        $removeAll = TRUE;

        if (isset($_REQUEST['DetectionAreaIndex']))
        {
            $removeAll = FALSE;

            $Indexlist = explode(",", $_REQUEST['DetectionAreaIndex']);
            $Indexcount = count($Indexlist);

            if(array_search('All', $Indexlist) !== FALSE && $Indexcount > 1)
            {
            	$responseOutput->errCode = STATUS_INVALID_VALUE;
                return $responseOutput;
            }

            if($_REQUEST['DetectionAreaIndex'] == 'All')
            {
            	$removeAll = TRUE;
            }
            else
            {
            	for($i = 0 ; $i < $Indexcount ; $i++)
	            {
	            	$rmIdx = (int)$Indexlist[$i] - 1;

	            	if ($rmIdx < 0 || $rmIdx > 3)
		            {
		                $responseOutput->errCode = STATUS_INVALID_VALUE;
		                return $responseOutput;
		            }

		            $fdConf->objectConf[$rmIdx]->InitData();
                    $fdConf->objectConf[$rmIdx]->SetPayload();
	            }
            }
        }

        if ($removeAll)
        {
            for ($index = 0; $index < MAX_FD_OBJECT; ++$index)
            {
                $fdConf->objectConf[$index]->InitData();
                $fdConf->objectConf[$index]->SetPayload();
            }
        }

        $fdConf->SetPayload();
        $fdConf->headerInfo['Action'] = ACTION_SET;
        $GLOBALS['SOCKET_MANAGER']->Connection($fdConf);

        $responseOutput->outputMsg = 'OK';
    }
    else if ($_REQUEST['action'] == 'view')
    {
    	$allowed_params = array("msubmenu", "action", "Channel");

        if(CheckAllowedParams($allowed_params) === FALSE)
        {
        	$responseOutput->errCode = STATUS_INVALID_PARAMETER;
            return $responseOutput;
        }
        
        $responseOutput->outputMsg .= 'Channel.0.Enable=' . $boolArray[$fdConf->dataInfo['Enabled']['value']] . "\r\n";
        $responseOutput->outputMsg .= 'Channel.0.Sensitivity=' . $fdConf->dataInfo['Sensitivity']['value'] . "\r\n";
        $responseOutput->outputMsg .= 'Channel.0.MarkDetectedFaces=' . $boolArray[$fdConf->dataInfo['FDBoxDisplay']['value']] . "\r\n";
        $responseOutput->outputMsg .= 'Channel.0.DetectionAreaMode=' . $EventAreaMode[$fdConf->dataInfo['ObjectMode']['value']] . "\r\n";

        for ($index = 0; $index < MAX_FD_OBJECT; ++$index)
        {
            if ($fdConf->objectConf[$index]->dataInfo['NumPoint']['value'] == 0)
            {
                continue;
            }
            
            $responseOutput->outputMsg .= 'Channel.0.DetectionArea.' . ($index + 1) . '.Coordinate=';
            $responseOutput->outputMsg .= $fdConf->objectConf[$index]->fdPoint[0]->dataInfo['PosX']['value'] . ',';
            $responseOutput->outputMsg .= $fdConf->objectConf[$index]->fdPoint[0]->dataInfo['PosY']['value'] . ',';
            $responseOutput->outputMsg .= $fdConf->objectConf[$index]->fdPoint[1]->dataInfo['PosX']['value'] . ',';
            $responseOutput->outputMsg .= $fdConf->objectConf[$index]->fdPoint[1]->dataInfo['PosY']['value'] . ',';
            $responseOutput->outputMsg .= $fdConf->objectConf[$index]->fdPoint[2]->dataInfo['PosX']['value'] . ',';
            $responseOutput->outputMsg .= $fdConf->objectConf[$index]->fdPoint[2]->dataInfo['PosY']['value'] . ',';
            $responseOutput->outputMsg .= $fdConf->objectConf[$index]->fdPoint[3]->dataInfo['PosX']['value'] . ',';
            $responseOutput->outputMsg .= $fdConf->objectConf[$index]->fdPoint[3]->dataInfo['PosY']['value'] . "\r\n";
        }
    }
    else
    {
        $responseOutput->errCode = STATUS_ACTION_NOT_FOUND;
        return $responseOutput;
    }

    $responseOutput->errCode = STATUS_OK;
    return $responseOutput;
}

///////////////////////////////////////////////
// Tamperingdetection
///////////////////////////////////////////////
function submenu_tamperingdetection()
{
    $responseOutput = new ResponseOutput();
    global $boolArray;
	global $Sensitivity;
	
	if (!$GLOBALS['M_SUPPORT_PTZ'])
	{
		unset($Sensitivity[1]);
		unset($Sensitivity[5]);
	}
	
    if (isset($_REQUEST['Channel']) && $_REQUEST['Channel'] != '0')
    {
        $responseOutput->errCode = STATUS_INVALID_VALUE;
        return $responseOutput;
    }

    $classInstances = GetClassInstance('tampering');
    $tamperingConf = $classInstances['TamperingConfiguration'];

    if ($_REQUEST['action'] == 'set')
    {
        if (count($_REQUEST) < 3)
        {
            $responseOutput->errCode = STATUS_MISSING_PARAMETER;
            return $responseOutput;
        }

        $allowed_params = array("msubmenu", "action", "Channel", "Enable", "Sensitivity");

        if(CheckAllowedParams($allowed_params) === FALSE)
        {
        	$responseOutput->errCode = STATUS_INVALID_PARAMETER;
            return $responseOutput;
        }
        
        if (isset($_REQUEST['Enable']))
        {
            $NewValue = array_search($_REQUEST['Enable'], $boolArray);
            if ($NewValue === FALSE)
            {
                $responseOutput->errCode = STATUS_INVALID_VALUE;
                return $responseOutput;
            }

            $tamperingConf->dataInfo['Enabled']['value'] = $NewValue;
        }

        if (isset($_REQUEST['Sensitivity']))
        {
            $NewValue = array_search($_REQUEST['Sensitivity'], $Sensitivity);

            if ($NewValue === FALSE)
            {
                $responseOutput->errCode = STATUS_INVALID_VALUE;
                return $responseOutput;
            }

			/*
				1 is VeryLow, 5 is Very High
				All WN3 chip base models support Low/Normal/High levels
			*/
			if($GLOBALS['M_ISP_TYPE'] != ISP_TYPE_WN2_PTZ)
            {
				if($NewValue == 1 || $NewValue  == 5)
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
	            }
            }
			
            $tamperingConf->dataInfo['Sensitivity']['value'] = $NewValue - 1;
        }

        $tamperingConf->SetPayload();
        $tamperingConf->headerInfo['Action'] = ACTION_SET;
        $GLOBALS['SOCKET_MANAGER']->Connection($tamperingConf);

        $responseOutput->outputMsg = 'OK';
    }
    else if ($_REQUEST['action'] == 'view')
    {
    	$allowed_params = array("msubmenu", "action", "Channel");

        if(CheckAllowedParams($allowed_params) === FALSE)
        {
        	$responseOutput->errCode = STATUS_INVALID_PARAMETER;
            return $responseOutput;
        }
        
        $responseOutput->outputMsg = 'Channel.0.Enable=' . $boolArray[$tamperingConf->dataInfo['Enabled']['value']] . "\r\n";
        $responseOutput->outputMsg .= 'Channel.0.Sensitivity=' . $Sensitivity[$tamperingConf->dataInfo['Sensitivity']['value']+1] . "\r\n";
    }
    else
    {
        $responseOutput->errCode = STATUS_ACTION_NOT_FOUND;
        return $responseOutput;
    }

    $responseOutput->errCode = STATUS_OK;
    return $responseOutput;
}

///////////////////////////////////////////////
// AudioDetection
///////////////////////////////////////////////
function submenu_audiodetection()
{

    $responseOutput = new ResponseOutput();
    global $boolArray;

    if (isset($_REQUEST['Channel']) && $_REQUEST['Channel'] != '0')
    {
        $responseOutput->errCode = STATUS_INVALID_VALUE;
        return $responseOutput;
    }

    $classInstances = GetClassInstance('ad');
    $adConf = $classInstances['ADConfiguration'];

    if ($_REQUEST['action'] == 'set')
    {
        if (count($_REQUEST) < 3)
        {
            $responseOutput->errCode = STATUS_MISSING_PARAMETER;
            return $responseOutput;
        }

        $allowed_params = array("msubmenu", "action", "Channel", "Enable", "InputThresholdLevel");

        if(CheckAllowedParams($allowed_params) === FALSE)
        {
        	$responseOutput->errCode = STATUS_INVALID_PARAMETER;
            return $responseOutput;
        }
        
        if (isset($_REQUEST['Enable']))
        {
            $NewValue = array_search($_REQUEST['Enable'], $boolArray);
            if ($NewValue === FALSE)
            {
                $responseOutput->errCode = STATUS_INVALID_VALUE;
                return $responseOutput;
            }

            $adConf->dataInfo['Enabled']['value'] = $NewValue;
        }
        
        if (isset($_REQUEST['InputThresholdLevel']))
        {
            if ($_REQUEST['InputThresholdLevel'] < 1 || $_REQUEST['InputThresholdLevel'] > 100)
            {
                $responseOutput->errCode = STATUS_INVALID_VALUE;
                return $responseOutput;
            }
            $adConf->dataInfo['Sensitivity']['value'] = $_REQUEST['InputThresholdLevel'];
        }

        $adConf->SetPayload();
        $adConf->headerInfo['Action'] = ACTION_SET;
        $GLOBALS['SOCKET_MANAGER']->Connection($adConf);

        $responseOutput->outputMsg = 'OK';
    }
    else if ($_REQUEST['action'] == 'view')
    {
    	$allowed_params = array("msubmenu", "action", "Channel");

        if(CheckAllowedParams($allowed_params) === FALSE)
        {
        	$responseOutput->errCode = STATUS_INVALID_PARAMETER;
            return $responseOutput;
        }
        
        $responseOutput->outputMsg = 'Channel.0.Enable=' . $boolArray[$adConf->dataInfo['Enabled']['value']] . "\r\n";
        $responseOutput->outputMsg .= 'Channel.0.InputThresholdLevel=' . $adConf->dataInfo['Sensitivity']['value'] . "\r\n";
    }
    else
    {
        $responseOutput->errCode = STATUS_ACTION_NOT_FOUND;
        return $responseOutput;
    }

    $responseOutput->errCode = STATUS_OK;
    return $responseOutput;
}

///////////////////////////////////////////////
// Network Disconnect
///////////////////////////////////////////////
function submenu_networkdisconnect()
{
    $responseOutput = new ResponseOutput();

    if (isset($_REQUEST['Channel']) && $_REQUEST['Channel'] != '0')
    {
        $responseOutput->errCode = STATUS_INVALID_VALUE;
        return $responseOutput;
    }
    
    global $boolArray;

    $classInstances = GetClassInstance('netdiscon');

    if ($_REQUEST['action'] == 'set')
    {
        if (count($_REQUEST) < 3)
        {
            $responseOutput->errCode = STATUS_MISSING_PARAMETER;
            return $responseOutput;
        }

        $allowed_params = array("msubmenu", "action", "Channel", "Enable");

        if(CheckAllowedParams($allowed_params) === FALSE)
        {
        	$responseOutput->errCode = STATUS_INVALID_PARAMETER;
            return $responseOutput;
        }
        
        if (isset($_REQUEST['Enable']))
        {
            $NewValue = array_search($_REQUEST['Enable'], $boolArray);
            if ($NewValue === FALSE)
            {
                $responseOutput->errCode = STATUS_INVALID_VALUE;
                return $responseOutput;
            }
            
            $classInstances['NetworkDisconnectConfiguration']->dataInfo['Enabled']['value'] = $NewValue;
        }

        $classInstances['NetworkDisconnectConfiguration']->SetPayload();
        $classInstances['NetworkDisconnectConfiguration']->headerInfo['Action'] = ACTION_SET;
        $GLOBALS['SOCKET_MANAGER']->Connection($classInstances['NetworkDisconnectConfiguration']);

        $responseOutput->outputMsg = 'OK';
    }
    else if ($_REQUEST['action'] == 'view')
    {
    	$allowed_params = array("msubmenu", "action", "Channel");

        if(CheckAllowedParams($allowed_params) === FALSE)
        {
        	$responseOutput->errCode = STATUS_INVALID_PARAMETER;
            return $responseOutput;
        }
        
        $responseOutput->outputMsg = 'Channel.0.Enable=' . $boolArray[$classInstances['NetworkDisconnectConfiguration']->dataInfo['Enabled']['value']] . "\r\n";
    }
    else
    {
        $responseOutput->errCode = STATUS_ACTION_NOT_FOUND;
        return $responseOutput;
    }

    $responseOutput->errCode = STATUS_OK;
    return $responseOutput;
}

// time schedule
function submenu_timer()
{
    $responseOutput = new ResponseOutput();

    global $boolArray;
    
    $Intervalunit = array(
        0 => 'Seconds',
        1 => 'Minutes'
	);

	$IntervalEnum = array(
		1 => '5',
		2 => '10',
		3 => '15',
		4 => '30',
		5 => '45',
		6 => '60'
	);

    $classInstances = GetClassInstance('timesched');
    $timeSchedConf = $classInstances['TimeScheduleConfiguration'];

    if ($_REQUEST['action'] == 'set')
    {
        if (count($_REQUEST) < 3)
        {
            $responseOutput->errCode = STATUS_MISSING_PARAMETER;
            return $responseOutput;
        }

        $allowed_params = array("msubmenu", "action", "Enable", "ScheduleInterval", "ScheduleIntervalUnit");

        if(CheckAllowedParams($allowed_params) === FALSE)
        {
        	$responseOutput->errCode = STATUS_INVALID_PARAMETER;
            return $responseOutput;
        }
        
        if (isset($_REQUEST['Enable']))
        {
            $NewValue = array_search($_REQUEST['Enable'], $boolArray);
            if ($NewValue === FALSE)
            {
                $responseOutput->errCode = STATUS_INVALID_VALUE;
                return $responseOutput;
            }
            $timeSchedConf->dataInfo['Enabled']['value'] = $NewValue;
        }
        
        if (isset($_REQUEST['ScheduleInterval']))//Need to validate values
        {
        	if(array_search($_REQUEST['ScheduleInterval'], $IntervalEnum) === FALSE)
        	{
        		$responseOutput->errCode = STATUS_INVALID_VALUE;
                return $responseOutput;
        	}
        	
            $timeSchedConf->dataInfo['Interval']['value'] = ((($timeSchedConf->dataInfo['Interval']['value'] / 600) <= 1) ? ($_REQUEST['ScheduleInterval'] * 10) : ($_REQUEST['ScheduleInterval'] * 600));
        }
        
        if (isset($_REQUEST['ScheduleIntervalUnit']))
        {
            $Intervalunit = array_search($_REQUEST['ScheduleIntervalUnit'], $Intervalunit);
            if ($Intervalunit === FALSE)
            {
                $responseOutput->errCode = STATUS_INVALID_VALUE;
                return $responseOutput;
            }
            $interval = $timeSchedConf->dataInfo['Interval']['value'];

            if (($interval / 600) <= 1 && $Intervalunit == 1)  // second
            {
                $interval = $timeSchedConf->dataInfo['Interval']['value'] * 60;
            }
            else if (($interval / 600) > 1 && $Intervalunit == 0)
            {
                $interval = $timeSchedConf->dataInfo['Interval']['value'] / 60;
            }

            $timeSchedConf->dataInfo['Interval']['value'] = $interval;
        }

        $timeSchedConf->SetPayload();
        $timeSchedConf->headerInfo['Action'] = ACTION_SET;
        $GLOBALS['SOCKET_MANAGER']->Connection($timeSchedConf);

        $responseOutput->outputMsg = 'OK';
    }
    else if ($_REQUEST['action'] == 'view')
    {
    	$allowed_params = array("msubmenu", "action");

        if(CheckAllowedParams($allowed_params) === FALSE)
        {
        	$responseOutput->errCode = STATUS_INVALID_PARAMETER;
            return $responseOutput;
        }
        
        $responseOutput->outputMsg = 'Enable=' . $boolArray[$timeSchedConf->dataInfo['Enabled']['value']] . "\r\n";

        if (($timeSchedConf->dataInfo['Interval']['value'] / 600) <= 1)
        {
            $responseOutput->outputMsg .= 'ScheduleInterval=' . ($timeSchedConf->dataInfo['Interval']['value'] / 10) . "\r\n";
            $responseOutput->outputMsg .= 'ScheduleIntervalUnit=Seconds' . "\r\n"; 
        }
        else
        {
            $responseOutput->outputMsg .= 'ScheduleInterval=' . ($timeSchedConf->dataInfo['Interval']['value'] / 600) . "\r\n";
            $responseOutput->outputMsg .= 'ScheduleIntervalUnit=Minutes' . "\r\n"; 
        }
    }
    else
    {
        $responseOutput->errCode = STATUS_ACTION_NOT_FOUND;
        return $responseOutput;
    }

    $responseOutput->errCode = STATUS_OK;
    return $responseOutput;
}

// autotracking
function submenu_autotracking()
{
    $responseOutput = new ResponseOutput();
    
    global $boolArray;
    
    $ObjectSize = array(
        1 => 'Small',
        2 => 'Medium',
        3 => 'Large'
    );
    $ZoomMode = array(
        0 => 'Off',
        1 => 'On'
    );

    $DisplayIndicator = array(
        0 => 'Off',
        1 => 'On'
    );
    $LostMode = array(
		0 => 'Research',
        1 => 'Stop'
    );

    if (isset($_REQUEST['Channel']) && $_REQUEST['Channel'] != '0')
    {
        $responseOutput->errCode = STATUS_INVALID_VALUE;
        return $responseOutput;
    }

    $addArea = FALSE;

    $classInstances = GetClassInstance('tracking');
    $presetConf = $classInstances['TrackingPreset'];

    require_once('./adv/maskarea.class');

    $maskAreasConf = new MaskAreas(CMD_TRACKING_TRACEZONE, MAX_TRACKING_MASK_AREA);
    $maskAreasConf = $GLOBALS['SOCKET_MANAGER']->Connection($maskAreasConf);
    
    if ($_REQUEST['action'] == 'set')
    {
    	/** AutoReturn, AutoRelease, DisplayTrackingArea, TrackingArea_1_Enable, TrackingArea_2_Enable, TrackingArea_3_Enable, TrackingArea_4_Enable, **/
    	/** TrackingArea_5_Enable, TrackingArea_6_Enable, TrackingArea_7_Enable, TrackingArea_8_Enable are only supported by SNP3371H 				  **/
    	$allowed_params = array("msubmenu", "action", "Channel", "Enable", "CameraHeight", "ObjectSize", "Sensitivity", "ZoomControl", "LostMode", "DisplayIndicator", "TrackingAreaEnable");

        if(CheckAllowedParams($allowed_params) === FALSE)
        {
        	$responseOutput->errCode = STATUS_INVALID_PARAMETER;
            return $responseOutput;
        }

    	if(isset($_REQUEST['AutoReturn']) || isset($_REQUEST['AutoRelease']) || isset($_REQUEST['DisplayTrackingArea'])) /** SNP3371TH only supports. */
        {
        	$responseOutput->errCode = STATUS_INVALID_PARAMETER;
            return $responseOutput;
        }
        
        foreach ($_REQUEST as $name => $value)
        {
            switch ($name)
            {
                case 'Enable':
                    {
                        $Enable = array_search($value, $boolArray);
                        if ($Enable === FALSE)
                        {
                            $responseOutput->errCode = STATUS_INVALID_VALUE;
                            return $responseOutput;
                        }
                        $presetConf->dataInfo['AutoTrack']['value'] = $Enable;
                    }
                    break;
                case 'CameraHeight':
                    {
                        if (strpos($value, "cm") === FALSE)
                        {
                            $responseOutput->errCode = STATUS_INVALID_VALUE;
                            return $responseOutput;
                        }
                        
                        $value = intval($value);
                        $validValue = (($value - 250) % 10);
                        if ($validValue != 0 || ($value < 250 || $value > 3000))
                        {
                            $responseOutput->errCode = STATUS_INVALID_VALUE;
                            return $responseOutput;
                        }

                        $presetConf->dataInfo['CameraHeight']['value'] = $value;
                    }
                    break;
                case 'Sensitivity':
                    {
                    	$responseOutput->errCode = STATUS_INVALID_PARAMETER;
						return $responseOutput;

                        /** SNP-3371TH only supports. */
                        $Sensitivity = array_search($value, $Sensitivity);
                        if ($Sensitivity === FALSE)
                        {
                            $responseOutput->errCode = STATUS_INVALID_VALUE;
                            return $responseOutput;
                        }
                        $presetConf->dataInfo['Sensitivity']['value'] = $Sensitivity;
                    }
                    break;
                case 'ZoomControl':
                    {
                        $ZoomControl = array_search($value, $ZoomMode);
                        if ($ZoomControl === FALSE)
                        {
                            $responseOutput->errCode = STATUS_INVALID_VALUE;
                            return $responseOutput;
                        }
                        $presetConf->dataInfo['ZoomControl']['value'] = $ZoomControl;
                    }
                    break;
                case 'ObjectSize':
                    {
                        $ObjectSize = array_search($value, $ObjectSize);
                        if ($ObjectSize === FALSE)
                        {
                            $responseOutput->errCode = STATUS_INVALID_VALUE;
                            return $responseOutput;
                        }
                        $presetConf->dataInfo['ObjectSize']['value'] = $ObjectSize;
                    }
                    break;
                case 'LostMode':
                    {
                        $LostMode = array_search($value, $LostMode);
                        if ($LostMode === FALSE)
                        {
                            $responseOutput->errCode = STATUS_INVALID_VALUE;
                            return $responseOutput;
                        }
                        $presetConf->dataInfo['AutoMode']['value'] = $LostMode;
                    }
                    break;
                case 'DisplayIndicator':
                    {
                        $DisplayIndicator = array_search($value, $DisplayIndicator);
                        if ($DisplayIndicator === FALSE)
                        {
                            $responseOutput->errCode = STATUS_INVALID_VALUE;
                            return $responseOutput;
                        }
                        $presetConf->dataInfo['Indicator']['value'] = $DisplayIndicator;
                    }
                    break;
                case 'TrackingAreaEnable':
                    {
                        $AutoRelease = array_search($value, $boolArray);
                        if ($AutoRelease === FALSE)
                        {
                            $responseOutput->errCode = STATUS_INVALID_VALUE;
                            return $responseOutput;
                        }
                        $presetConf->dataInfo['AreaActivation']['value'] = $AutoRelease;
                    }
                    break;
            }
        }

        if(isset($_REQUEST['Enable']))
        {
            $targetConf = new TrackingTargetlock();
            $targetConf->dataInfo['AutoTrack']['value'] = $Enable;
            $targetConf->headerInfo['Action'] = ACTION_START;
            $targetConf->payload = MakePayload($targetConf->dataInfo);
            $GLOBALS['SOCKET_MANAGER']->Connection($targetConf);
        }
        
        $presetConf->payload = MakePayload($presetConf->dataInfo);
        $presetConf->headerInfo['Action'] = ACTION_SET;
        $GLOBALS['SOCKET_MANAGER']->Connection($presetConf);

        $responseOutput->outputMsg = 'OK';
    }
    else if ($_REQUEST['action'] == 'view')
    {
    	$allowed_params = array("msubmenu", "action", "Channel");

        if(CheckAllowedParams($allowed_params) === FALSE)
        {
        	$responseOutput->errCode = STATUS_INVALID_PARAMETER;
            return $responseOutput;
        }
        
        $responseOutput->outputMsg = 'Channel.0.Enable=' . $boolArray[$presetConf->dataInfo['AutoTrack']['value']] . "\r\n";
        $responseOutput->outputMsg .= 'Channel.0.CameraHeight=' . $presetConf->dataInfo['CameraHeight']['value'] . "cm\r\n";
        $responseOutput->outputMsg .= 'Channel.0.ObjectSize=' . $ObjectSize[$presetConf->dataInfo['ObjectSize']['value']] . "\r\n";

        $responseOutput->outputMsg .= 'Channel.0.ZoomControl=' . $ZoomMode[$presetConf->dataInfo['ZoomControl']['value']] . "\r\n";
        $responseOutput->outputMsg .= 'Channel.0.LostMode=' . $LostMode[$presetConf->dataInfo['AutoMode']['value']] . "\r\n";

        $responseOutput->outputMsg .= 'Channel.0.DisplayIndicator=' . $DisplayIndicator[$presetConf->dataInfo['Indicator']['value']] . "\r\n";
        $responseOutput->outputMsg .= 'Channel.0.TrackingAreaEnable=' . $boolArray[$presetConf->dataInfo['AreaActivation']['value']] . "\r\n";

        $trackingAreaCount = 0;
        for ($index = 0; $index < MAX_TRACKING_MASK_AREA ; ++$index)
        {
            if ($maskAreasConf->maskArea[$index]->dataInfo['Enabled']['value'] != 1)
            	continue;
            
            $areaConf = $maskAreasConf->maskArea[$index];
            $responseOutput->outputMsg .= 'Channel.0.TrackingArea.' . ($areaConf->dataInfo['Name']['value']) . '.Coordinate=' . 
					            			$areaConf->normalPoint[0]->dataInfo['X']['value'] . ',' . $areaConf->normalPoint[0]->dataInfo['Y']['value'] . ',' . 
					            			$areaConf->normalPoint[1]->dataInfo['X']['value'] . ',' . $areaConf->normalPoint[1]->dataInfo['Y']['value'] . "\r\n";

            $trackingAreaCount++;
        }
        
        $responseOutput->outputMsg .= 'Channel.0.TrackingAreas=' . $trackingAreaCount . "\r\n";
    }
    else if($_REQUEST['action'] == 'control')
    {
		/** TargetLockOn, TrackingArea_1, TrackingArea_2, TrackingArea_3, TrackingArea_4, TrackingArea_5, TrackingArea_6, TrackingArea_7, TrackingArea_8 are only supported by SNP3371H **/
    	$allowed_params = array("msubmenu", "action", "Channel", "TargetLockCoordinate");

        if(CheckAllowedParams($allowed_params) === FALSE)
        {
        	$responseOutput->errCode = STATUS_INVALID_PARAMETER;
            return $responseOutput;
        }
    	
        if($_REQUEST['TargetLockCoordinate'])
        {
    		$areaData = explode(",", $_REQUEST['TargetLockCoordinate']);

    		if (count($areaData) != 2)
    		{
    		    $responseOutput->errCode = STATUS_INVALID_VALUE;
    		    return $responseOutput;
    		}

    		 /*
				validation of allowed values
				areaData is X,Y of TargetLockCoordinate
				allowed values =>  1<= TargetLockCoordinate <= 10000
             */

			if($areaData[0] < 1 || $areaData[0] > 10000 || $areaData[1] < 1 || $areaData[1] > 10000)
			{
				$responseOutput->errCode = STATUS_INVALID_VALUE;
				return $responseOutput;
			}

    		$targetConf = new TrackingTargetlock();
    		$targetConf->dataInfo['Mode']['value'] = 1;
    		$targetConf->dataInfo['AutoTrack']['value'] = 1;
    		$targetConf->dataInfo['NormalizePosX']['value'] = $areaData[0];
    		$targetConf->dataInfo['NormalizePosY']['value'] = $areaData[1];
    		$targetConf->headerInfo['Action'] = ACTION_START;
    		$targetConf->payload = MakePayload($targetConf->dataInfo);
    		$GLOBALS['SOCKET_MANAGER']->Connection($targetConf);
        }

        $responseOutput->outputMsg = 'OK';
    }
    else if($_REQUEST['action'] == 'add')
    {
    	$allowed_params = array("msubmenu", "action", "Channel", "Coordinate", "TrackingAreaID");

        if(CheckAllowedParams($allowed_params) === FALSE)
        {
        	$responseOutput->errCode = STATUS_INVALID_PARAMETER;
            return $responseOutput;
        }
        
        if (!isset($_REQUEST['TrackingAreaID']) || !isset($_REQUEST['Coordinate']))
        {
            $responseOutput->errCode = STATUS_MISSING_PARAMETER;
            return $responseOutput;
        }

        $FreeSlots = 0;
        for ($index = 0; $index < MAX_TRACKING_MASK_AREA ; ++$index)
        {
            if ($maskAreasConf->maskArea[$index]->dataInfo['Enabled']['value'] == 0)
            {
                $FreeSlots = 1;
            }
            else
            {
                if($_REQUEST['TrackingAreaID'] == $maskAreasConf->maskArea[$index]->dataInfo['Name']['value'])
                {
                    $responseOutput->errCode = STATUS_INVALID_VALUE;
                    return $responseOutput;
                }
            }
        }

        if($FreeSlots == 0)
        {
            $responseOutput->errCode = STATUS_LIST_FULL;
            return $responseOutput;
        }	 

        $areaData = explode(",", $_REQUEST['Coordinate']);

        if (count($areaData) != 4)
        {
            $responseOutput->errCode = STATUS_INVALID_VALUE;
            return $responseOutput;
        }

        $maskArea = new MaskArea(CMD_TRACKING_TRACEZONE);
		$maskArea->dataInfo['Name']['value'] = $_REQUEST['TrackingAreaID'];
        $maskArea->dataInfo['Enabled']['value'] = 1;
        $maskArea->dataInfo['NumPoint']['value'] = 2;

        $maskArea->normalPoint[0]->dataInfo['X']['value'] = $areaData[0];
        $maskArea->normalPoint[0]->dataInfo['Y']['value'] = $areaData[1];
        $maskArea->normalPoint[1]->dataInfo['X']['value'] = $areaData[2];
        $maskArea->normalPoint[1]->dataInfo['Y']['value'] = $areaData[3];
        
        $maskArea->normalPoint[0]->payload = MakePayload($maskArea->normalPoint[0]->dataInfo);
        $maskArea->normalPoint[1]->payload = MakePayload($maskArea->normalPoint[1]->dataInfo);
        $maskArea->SetPayload();
        $GLOBALS['SOCKET_MANAGER']->Connection($maskArea);
        
        $responseOutput->outputMsg = 'OK';
    }
    else if ($_REQUEST['action'] == 'remove')
    {
    	$allowed_params = array("msubmenu", "action", "Channel", "TrackingAreaID");

        if(CheckAllowedParams($allowed_params) === FALSE)
        {
        	$responseOutput->errCode = STATUS_INVALID_PARAMETER;
            return $responseOutput;
        }
        
        if (!isset($_REQUEST['TrackingAreaID']))
        {
            $responseOutput->errCode = STATUS_MISSING_PARAMETER;
            return $responseOutput;
        }
        
        $Indexlist = explode(",", $_REQUEST['TrackingAreaID']);
        $Indexcount = count($Indexlist);

        if ($Indexcount < 1 || $Indexcount > 8)
        {
            $responseOutput->errCode = STATUS_INVALID_VALUE;
            return $responseOutput;
        }

        for ($i = 0; $i < $Indexcount; ++$i)
        {
			$RemoveValue = $Indexlist[$i];
			$isMatch = FALSE;

			for ($index = 0; $index < MAX_TRACKING_MASK_AREA ; ++$index)
			{
			     if ($maskAreasConf->maskArea[$index]->dataInfo['Enabled']['value'] == 0)
			     	continue;
			     
			     if ($RemoveValue == $maskAreasConf->maskArea[$index]->dataInfo['Name']['value'])
			     {
					$maskArea = new MaskArea(CMD_TRACKING_TRACEZONE);    
					$maskArea->headerInfo['Action'] = ACTION_REMOVE;
					$maskArea->payload = pack('i1', $index);
					$GLOBALS['SOCKET_MANAGER']->Connection($maskArea);

					$isMatch = TRUE;
					
					break;
			     }
			 }

			 if(!$isMatch)
			 {
			 	$responseOutput->errCode = STATUS_INVALID_VALUE;
	            return $responseOutput;
			 }
        }

        $responseOutput->outputMsg = 'OK';
    }
    else
    {
        $responseOutput->errCode = STATUS_ACTION_NOT_FOUND;
        return $responseOutput;
    }

    $responseOutput->errCode = STATUS_OK;
    return $responseOutput;
}

///////////////////////////////////////////////
// CGI Command - Submenu handler
///////////////////////////////////////////////
switch (@$_REQUEST['msubmenu'])
{
    case 'videoanalysis':
    case 'facedetection':
    case 'tamperingdetection':    
    case 'audiodetection':
    case 'videoloss':
    case 'autotracking':
    case 'timer':
    case 'alarminput':
    case 'networkdisconnect':
        {
        	$responseOutput = new ResponseOutput();
        	
            if (($_REQUEST['msubmenu'] == 'facedetection') && $GLOBALS['M_SUPPORT_EVENT_FD'] == 0)
            {
                $responseOutput->errCode = STATUS_NOT_IMPLEMENTED;
                SendResponse($responseOutput);
            }
            if (($_REQUEST['msubmenu'] == 'tamperingdetection') && $GLOBALS['M_SUPPORT_EVENT_TD'] == 0)
            {

                $responseOutput->errCode = STATUS_NOT_IMPLEMENTED;
                SendResponse($responseOutput);
            }
            if (($_REQUEST['msubmenu'] == 'videoanalysis') && $GLOBALS['M_SUPPORT_EVENT_VA'] == 0)
            {
                $responseOutput->errCode = STATUS_NOT_IMPLEMENTED;
                SendResponse($responseOutput);
            }
            if (($_REQUEST['msubmenu'] == 'audiodetection') && $GLOBALS['M_SUPPORT_EVENT_AD'] == 0)
            {

                $responseOutput->errCode = STATUS_NOT_IMPLEMENTED;
                SendResponse($responseOutput);
            }
            if (($_REQUEST['msubmenu'] == 'videoloss') && $GLOBALS['M_SUPPORT_EVENT_VL'] == 0)
            {

                $responseOutput->errCode = STATUS_NOT_IMPLEMENTED;
                SendResponse($responseOutput);
            }
            if (($_REQUEST['msubmenu'] == 'autotracking') && $GLOBALS['M_SUPPORT_PTZ_TRACKING'] == 0)
            {
                $responseOutput->errCode = STATUS_NOT_IMPLEMENTED;
                SendResponse($responseOutput);
            }
            if ($_REQUEST['msubmenu'] == 'alarminput' && $GLOBALS['M_ALARMIN_COUNT'] == 0)
            {
                $responseOutput->errCode = STATUS_NOT_IMPLEMENTED;
                SendResponse($responseOutput);
            }
            if (($_REQUEST['msubmenu'] == 'networkdisconnect') && $GLOBALS['M_SUPPORT_EVENT_ND'] == 0)
            {
                $responseOutput->errCode = STATUS_NOT_IMPLEMENTED;
                SendResponse($responseOutput);
            }

            $funcName = 'submenu_' . $_REQUEST['msubmenu'];

            SendResponse($funcName());
        }
        break;
    case 'networkalarminput':
		{
			$responseOutput = new ResponseOutput();
			$responseOutput->errCode = STATUS_NOT_IMPLEMENTED;
            SendResponse($responseOutput);
		}
		break;
    default:
        {
            $responseOutput = new ResponseOutput();
            $responseOutput->errCode = STATUS_SUBMENU_NOT_FOUND;
            SendResponse($responseOutput);
        }
}
?>
