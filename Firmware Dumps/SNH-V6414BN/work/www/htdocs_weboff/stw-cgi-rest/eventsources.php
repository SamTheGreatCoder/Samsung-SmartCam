<?php
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";

function submenu_videoanalysis()
{
	if($_SERVER['REQUEST_METHOD'] != "GET" && $_SERVER['REQUEST_METHOD'] != "PUT" && $_SERVER['REQUEST_METHOD'] != "DELETE")
	{
		header("HTTP/1.1 405 Method Not Allowed");
		return;
	}

	$result_va = requestToCamera(CMD_VA_CONFIGURATION, ACTION_GET, TYPE_REQUEST, null);
	if($result_va[0] == "OK")
	{
		global $CLASS_PATH;
		require_once($CLASS_PATH . "va.class");

		$va['VAConfiguration'] = new VAConfiguration();
		$va['VAConfiguration']->PayloadToArray($result_va[2]);

		$VAConf = $va['VAConfiguration'];
	}
	else
	{
		header("HTTP/1.1 500 Internal Server Error");
		return;
	}

	$Sensitivity = array('VeryLow', 'Low', 'Medium', 'High', 'VeryHigh');
	$DetectionType = array(
		0 => 'MotionDetection',
//		1 => 'IntelligentVideo',
//		2 => 'MDAndIV',
		3 => 'Off'
	);
	$EventAreaMode = array(
		0 => 'Outside',
		1 => 'Inside'
	);
	$EntireAreaMode = array(
	    0 => 'Off',
	    1 => 'AppearDisappear',
	    2 => 'Scenechange'
	);

    $resMaxWidth = 1920; // 2mega max resolution (when adding other devices, need to check getting max resolution information)
	$resMaxHeight = 1080;
	
	if($_SERVER['REQUEST_METHOD'] == "GET")
	{
		$detectType = 3;
		if($VAConf->mdConf->dataInfo['Enabled']['value'] == 1) /** ivConf->Enabled and mdConf->Enabled have same value, so just check one.*/
		{
			$detectType = $VAConf->dataInfo['Mode']['value'];
		}
		
		$data = array("Channel.0.DetectionType"=>$DetectionType[$detectType], 
						"Channel.0.DetectionResultOverlay"=>(bool)$VAConf->mdConf->dataInfo['VABoxDisplay']['value'], 
						"Channel.0.Sensitivity"=>$Sensitivity[$VAConf->mdConf->dataInfo['Sensitivity']['value']], 
						"Channel.0.MinimumObjectSize"=>$VAConf->mdConf->manualSize->dataInfo['HSL']['value'] .','.$VAConf->mdConf->manualSize->dataInfo['VSL']['value'], 
						"Channel.0.MaximumObjectSize"=>$VAConf->mdConf->manualSize->dataInfo['HSH']['value'] .','.$VAConf->mdConf->manualSize->dataInfo['VSH']['value'], 
						"Channel.0.ROIMode"=>$EventAreaMode[$VAConf->mdConf->dataInfo['ObjectMode']['value']]);

		for ($index = 0; $index < MAX_MD_AREA_HSS ; ++$index)
        {
            if ($VAConf->mdConf->objectRule[$index]->dataInfo['NumPoint']['value'] == 0)
            {
                continue;
            }

            $points = $VAConf->mdConf->objectRule[$index]->mdPoint[0]->dataInfo['PosX']['value'] . ',';
            $points .= $VAConf->mdConf->objectRule[$index]->mdPoint[0]->dataInfo['PosY']['value'] . ',';
            $points .= $VAConf->mdConf->objectRule[$index]->mdPoint[1]->dataInfo['PosX']['value'] . ',';
            $points .= $VAConf->mdConf->objectRule[$index]->mdPoint[1]->dataInfo['PosY']['value'];

            if ($VAConf->mdConf->objectRule[$index]->dataInfo['NumPoint']['value'] == 4) //Poly
            {
                $points .= ',' . $VAConf->mdConf->objectRule[$index]->mdPoint[2]->dataInfo['PosX']['value'] . ',';
                $points .= $VAConf->mdConf->objectRule[$index]->mdPoint[2]->dataInfo['PosY']['value'] . ',';
                $points .= $VAConf->mdConf->objectRule[$index]->mdPoint[3]->dataInfo['PosX']['value'] . ',';
                $points .= $VAConf->mdConf->objectRule[$index]->mdPoint[3]->dataInfo['PosY']['value'];
            }

            $data['Channel.0.ROI.' . ($index + 1) . '.Coordinate='] = $points;
        }

		header("Content-type: application/json");
		echo json_encode($data);
	}
	else if($_SERVER['REQUEST_METHOD'] == "PUT")
	{
		$put_data = json_decode(file_get_contents("php://input"));

		if(!isset($put_data->{'DetectionType'}))
		{
			header("HTTP/1.1 400 Bad Request");
			return;
		}

		foreach ($put_data as $name => $value)
		{
			switch ($name)
            {
            	case 'Channel':
            		{
            			if($value != 0)
            			{
            				header("HTTP/1.1 400 Bad Request");
							return;
            			}
            		}
            		break;
            	case 'DetectionType':
            		{
						$newValue = array_search($value, $DetectionType);
			        	if($newValue === FALSE)
			        	{
			                header("HTTP/1.1 400 Bad Request");
							return;
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
            		break;
            	case 'Sensitivity':
	                {
	                    $newValue = array_search($value, $Sensitivity);
	                    if($newValue === FALSE)
	                    {
	                        header("HTTP/1.1 400 Bad Request");
							return;
	                    }

	                    $VAConf->mdConf->dataInfo['Sensitivity']['value'] = $newValue;
	                    $VAConf->ivConf->dataInfo['Sensitivity']['value'] = $newValue;
	                }
	                break;
	            case 'MinimumObjectSize':
	                {
	                    $ObjectSizeData = explode(",", $value);
	                    if (count($ObjectSizeData) != 2)
	                    {
	                        header("HTTP/1.1 400 Bad Request");
							return;
	                    }

	                    if (($ObjectSizeData[0] < 0 || $ObjectSizeData[0] > 99) || ($ObjectSizeData[1] < 0 || $ObjectSizeData[1] > 99))
	                    {
	                        header("HTTP/1.1 400 Bad Request");
							return;
	                    }

	                    $VAConf->mdConf->manualSize->dataInfo['HSL']['value'] = $ObjectSizeData[0];
	                    $VAConf->mdConf->manualSize->dataInfo['VSL']['value'] = $ObjectSizeData[1];
	                    $VAConf->ivConf->ivObjectSizeManual->dataInfo['HSL']['value'] = $ObjectSizeData[0];
	                    $VAConf->ivConf->ivObjectSizeManual->dataInfo['VSL']['value'] = $ObjectSizeData[1];
	                }
	                break;
	            case 'MaximumObjectSize':
	                {
	                    $ObjectSizeData = explode(",", $value);
	                    if (count($ObjectSizeData) != 2)
	                    {
	                        header("HTTP/1.1 400 Bad Request");
							return;
	                    }

	                    if (($ObjectSizeData[0] < 0 || $ObjectSizeData[0] > 99) || ($ObjectSizeData[1] < 0 || $ObjectSizeData[1] > 99))
	                    {
	                        header("HTTP/1.1 400 Bad Request");
							return;
	                    }

	                    $VAConf->mdConf->manualSize->dataInfo['HSH']['value'] = $ObjectSizeData[0];
	                    $VAConf->mdConf->manualSize->dataInfo['VSH']['value'] = $ObjectSizeData[1];
	                    $VAConf->ivConf->ivObjectSizeManual->dataInfo['HSH']['value'] = $ObjectSizeData[0];
	                    $VAConf->ivConf->ivObjectSizeManual->dataInfo['VSH']['value'] = $ObjectSizeData[1];
	                }
	                break;
	            case 'DetectionResultOverlay':
	                {	
	                    if(!is_bool($value))
	                    {
	                        header("HTTP/1.1 400 Bad Request");
							return;
	                    }

	                    $VAConf->ivConf->dataInfo['VABoxDisplay']['value'] = (int)$value;
	                    $VAConf->mdConf->dataInfo['VABoxDisplay']['value'] = (int)$value;
	                }
	                break;
                case 'ROIMode':
                    {
                        $value = array_search($value, $EventAreaMode);
                        if($value === FALSE)
                        {
                        	header("HTTP/1.1 400 Bad Request");
							return;
                        }

                        $VAConf->mdConf->dataInfo['ObjectMode']['value'] = $value;
                    }
                    break;
                case 'ROI.1.Coordinate': case 'ROI.2.Coordinate': case 'ROI.3.Coordinate': 
                    {
                    	$reqNameArray = explode(".", $name);
                        $areaIndex = ((int)$reqNameArray[1]) - 1;
                        $areaData = explode(",", $value);

                        if (count($areaData) != 8)
                        {
                            $responseOutput->errCode = STATUS_INVALID_VALUE;
                            return $responseOutput;
                        }

                        $VAConf->mdConf->objectRule[$areaIndex]->dataInfo['NumPoint']['value'] = 2;
                        $VAConf->mdConf->objectRule[$areaIndex]->dataInfo['Index']['value'] = $areaIndex;
                        $VAConf->mdConf->objectRule[$areaIndex]->mdPoint[0]->dataInfo['PosX']['value'] = $areaData[0];
                        $VAConf->mdConf->objectRule[$areaIndex]->mdPoint[0]->dataInfo['PosY']['value'] = $areaData[1];
                        $VAConf->mdConf->objectRule[$areaIndex]->mdPoint[1]->dataInfo['PosX']['value'] = $areaData[2];
                        $VAConf->mdConf->objectRule[$areaIndex]->mdPoint[1]->dataInfo['PosY']['value'] = $areaData[3];

                        //if (CheckModelName('CHECK_MD_POLY_SUPPORT'))
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
            	default:
	            	{
	            		header("HTTP/1.1 400 Bad Request");
	            		return;
	            	}
	            	break;
            }
		}

		$VAConf->mdConf->SetPayload();
        $VAConf->ivConf->SetPayload();
        $VAConf->SetPayload();

        $result = requestToCamera(CMD_VA_CONFIGURATION, ACTION_SET, TYPE_REQUEST, unpack('c*', $VAConf->payload));
        if($result[0] != "OK")
		{
			header("HTTP/1.1 500 Internal Server Error");
		}
	}
	else if($_SERVER['REQUEST_METHOD'] == "DELETE")
	{
		$put_data = json_decode(file_get_contents("php://input"));
		if($put_data != null)
		{
			foreach ($put_data as $name => $value)
			{
				switch ($name)
	            {
	            	case 'Channel':
	            		{
	            			if($value != 0)
	            			{
	            				header("HTTP/1.1 400 Bad Request");
								return;
	            			}
	            		}
	            		break;
	            	case 'ROIIndex':
	            		{
	            			 $idx = explode(",", $value);
	            			 if(count($idx) > 3)
	            			 {
	            			 	header("HTTP/1.1 400 Bad Request");
								return;
	            			 }

	            			 if(in_array("All", $idx) && $value != "All")
	            			 {
	            			 	header("HTTP/1.1 400 Bad Request");
								return;
	            			 }

	            			 if($value == "All")
	            			 {
	            			 	for($rmIdx = 0 ; $rmIdx < MAX_MD_AREA_HSS ; $rmIdx++)
	                        	{
	                        		$VAConf->mdConf->objectRule[$rmIdx]->InitData();
	                                $VAConf->mdConf->objectRule[$rmIdx]->SetPayload();
	                        	}
	            			 }
	            			 else
	            			 {
	            			 	for($i = 0 ; $i < count($idx) ; $i++)
	                        	{
	                        		$rmIdx = ((int)$idx[$i]) - 1;

	                        		if($rmIdx < 0 || $rmIdx > 2)
	                        		{
	                        			header("HTTP/1.1 400 Bad Request");
										return;
	                        		}

	                        		$VAConf->mdConf->objectRule[$rmIdx]->InitData();
	                                $VAConf->mdConf->objectRule[$rmIdx]->SetPayload();
	                        	}
	            			 }
	            		}
	            		break;
	            	default:
		            	{
		            		header("HTTP/1.1 400 Bad Request");
		            		return;
		            	}
		            	break;
	        	}
	        }
		}
		else
		{
			for($rmIdx = 0 ; $rmIdx < MAX_MD_AREA_HSS ; $rmIdx++)
        	{
        		$VAConf->mdConf->objectRule[$rmIdx]->InitData();
                $VAConf->mdConf->objectRule[$rmIdx]->SetPayload();
        	}
		}

		$VAConf->mdConf->SetPayload();
		$VAConf->SetPayload();

		$result = requestToCamera(CMD_VA_CONFIGURATION, ACTION_SET, TYPE_REQUEST, unpack('c*', $VAConf->payload));
		if($result[0] != "OK")
		{
			header("HTTP/1.1 500 Internal Server Error");
		}
	}
}

function submenu_audiodetection()
{
	if($_SERVER['REQUEST_METHOD'] != "GET" && $_SERVER['REQUEST_METHOD'] != "PUT")
	{
		header("HTTP/1.1 405 Method Not Allowed");
		return;
	}

	$result_ad = requestToCamera(CMD_AD_EVENT, ACTION_GET, TYPE_REQUEST, null);
	if($result_ad[0] == "OK")
	{
		global $CLASS_PATH;
		require_once($CLASS_PATH . "ad.class");

		$ad['ADConfiguration'] = new ADConfiguration();
		$ad['ADConfiguration']->PayloadToArray($result_ad[2]);

		$adConf = $ad['ADConfiguration'];
	}
	else
	{
		header("HTTP/1.1 500 Internal Server Error");
		return;
	}
	
	if($_SERVER['REQUEST_METHOD'] == "GET")
	{
		$data = array("Channel.0.Enable"=>(bool)$adConf->dataInfo['Enabled']['value'], 
						"Channel.0.InputThresholdLevel"=>(int)floor($adConf->dataInfo['Sensitivity']['value']/20));
		
		header("Content-type: application/json");
		echo json_encode($data);
	}
	else if($_SERVER['REQUEST_METHOD'] == "PUT")
	{
		$put_data = json_decode(file_get_contents("php://input"));

		if(!isset($put_data->{'Enable'}))
		{
			header("HTTP/1.1 400 Bad Request");
			return;
		}

		foreach ($put_data as $name => $value)
		{
			switch ($name)
            {
            	case 'Channel':
            		{
            			if($value != 0)
            			{
            				header("HTTP/1.1 400 Bad Request");
							return;
            			}
            		}
            		break;
            	case 'Enable':
            		{
            			if(!is_bool($value))
            			{
            				header("HTTP/1.1 400 Bad Request");
							return;
            			}
            			
            			$adConf->dataInfo['Enabled']['value'] = (int)$value;
            		}
            		break;
            	case 'InputThresholdLevel':
            		{
            			if($value < 1 || $value > 5)
            			{
            				header("HTTP/1.1 400 Bad Request");
							return;
            			}

            			$adConf->dataInfo['Sensitivity']['value'] = (int)$value * 20;
            		}
            		break;
            	default:
	            	{
	            		header("HTTP/1.1 400 Bad Request");
	            		return;
	            	}
	            	break;
            }
		}

		$adConf->SetPayload();		
		$result = requestToCamera(CMD_AD_EVENT, ACTION_SET, TYPE_REQUEST, unpack('c*', $adConf->payload));
		if($result[0] != "OK")
		{
			header("HTTP/1.1 500 Internal Server Error");
		}
	}
}

switch (@$_REQUEST['msubmenu'])
{
    case 'videoanalysis': 
    case 'audiodetection': 
        {
            $funcName = 'submenu_' . $_REQUEST['msubmenu'];
            $funcName();
        }
        break;
    default:
    	header("HTTP/1.1 501 Not Implemented");
		break;
}
?>
