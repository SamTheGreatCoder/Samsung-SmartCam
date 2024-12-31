<?php
require_once('./adv/_define.inc');
$xmlInfo = CheckXMLMessage();
if ($xmlInfo['menu'] != 'OSD' && $xmlInfo['menu'] != 'RelayOutputState' && $xmlInfo['menu'] !='PTZAuxiliary' && $xmlInfo['menu'] != 'PTZInstantAF' && $xmlInfo['menu'] != 'PTZHomePosition' 
&& $xmlInfo['menu'] != 'PTZPreset' && $xmlInfo['menu'] != 'PTZSwing' && $xmlInfo['menu'] != 'PTZGroup' && $xmlInfo['menu'] != 'PTZTour' && $xmlInfo['menu'] != 'PTZLimit' && $xmlInfo['menu'] != 'PTZTrace'
&& $xmlInfo['menu'] != 'PTZAutorun' && $xmlInfo['menu'] != 'PTZStatus' && $xmlInfo['menu'] != 'PTZStop' && $xmlInfo['menu'] != 'TrackingPreset' && $xmlInfo['menu'] != 'TrackingTargetlock') {
	CheckAdminAccount(FALSE);
}
$_SESSION['count']++;
$GLOBALS['SOCKET_MANAGER'] = new SocketManager();
switch($xmlInfo['menu']) {
	case 'User':								{	require_once ('./adv/user.class');					$targetClass = new UserConfiguration();						}	break;
	case 'NTP':								{	require_once ('./adv/ntp.class');					$targetClass = new NTPConfiguration();						}	break;
	case 'DateTime':						{	require_once ('./adv/datetime.class');				$targetClass = new DateTimeConfiguration();				}	break;
	case 'ProductInfo': 					{	require_once ('./adv/system.class');				$targetClass = new SystemConfiguration();					}	break;
	case 'Reboot': 							{	require_once ('./adv/reset.class');					$targetClass = new RebootConfiguration();					}	break;
	case 'Reset': 							{	require_once ('./adv/reset.class');					$targetClass = new FactoryDefaultConfiguration();		}	break;
	case 'RegisterInfo': 					{	require_once ('./adv/register.class');				$targetClass = new RegInfoList();								}	break;
	case 'HTTPS':							{	require_once ('./adv/https.class');					$targetClass = new HTTPSConfiguration();					}	break;
	case 'HTTPSData':						{	require_once ('./adv/https.class');					$targetClass = new HTTPSData();								}	break;
	case 'Configuration802Dot1x':		{	require_once ('./adv/https.class');					$targetClass = new Configuration802Dot1x();				}	break;
	case 'Data802Dot1x':					{	require_once ('./adv/https.class');					$targetClass = new Data802Dot1x();							}	break;
	case 'Format':							{	require_once ('./adv/record.class');				$targetClass = new StorageFormat();							}	break;
	case 'ImageSetting':					{	require_once ('./adv/imagesetting.class');		$targetClass = new ImageSetting();							}	break;
	case 'PrivacyMask':					{	require_once ('./adv/videosource.class');			$targetClass = new PrivacyMask();								}	break;
	case 'VideoSource':					{	require_once ('./adv/videosource.class'); 		$targetClass = new VideoSource();								}	break;
	case 'Audio':							{	require_once ('./adv/media.class');					$targetClass = new MediaConfiguration();					}	break;
	case 'VideoOutput':					{	require_once ('./adv/media.class');					$targetClass = new MediaConfiguration();					}	break;
	case 'Interface':						{	require_once ('./adv/interface.class');			$targetClass = new InterfaceConfiguration();				}	break;
	case 'Port':								{	require_once ('./adv/network_protocol.class');	$targetClass = new NetworkProtocols();						}	break;
	case 'DDNS':								{	require_once ('./adv/ddns.class');					$targetClass = new DDNSConfiguration();						}	break;
	case 'QuickConnect':					{	require_once ('./adv/ddns.class');					$targetClass = new QuickConnectConfiguration();			}	break;
	case 'IPFiltering':					{	require_once ('./adv/ipfilter.class');				$targetClass = new IPFilterConfiguration();				}	break;
	case 'FTP':								{	require_once ('./adv/network_ftp.class');			$targetClass = new FTPSetting();								}	break;
	case 'Email':							{	require_once ('./adv/network_smtp.class');		$targetClass = new SMTPSetting();								}	break;
	// DEV_S1SMS
	case 'Sms':								{	require_once ('./adv/network_sms.class');	    $targetClass = new SMSSetting();							} 	break;
	case 'RelaySetting':					{	require_once ('./adv/relay_setting.class');		$targetClass = new RelayOutputConfiguration();			}	break;
	case 'AlarmInput':						{	require_once ('./adv/alarm.class');					$targetClass = new SensorConfiguration();					}	break;
	case 'MDConfiguration':				{	require_once ('./adv/va.class');						$targetClass = new MDConfiguration();						}	break;
	case 'IVConfiguration':				{	require_once ('./adv/va.class');						$targetClass = new IVConfiguration();						}	break;
	case 'VAConfiguration':				{	require_once ('./adv/va.class');						$targetClass = new VAConfiguration();						}	break;
	case 'TimeSchedule':					{	require_once ('./adv/timesched.class');			$targetClass = new TimeScheduleConfiguration();			}	break;
	case 'NetworkEvent':					{	require_once ('./adv/netdiscon.class');			$targetClass = new NetworkDisconnectConfiguration();	}	break;
	case 'TamperingConfiguration':		{	require_once ('./adv/tampering.class');			$targetClass = new TamperingConfiguration();				} 	break;
	case 'OpenSDKConfiguration':						{	require_once ('./adv/opensdk.class');			$targetClass = new OpenSDKConfiguration();	}	break;
	case 'FDConfiguration':				{	require_once ('./adv/fd.class');						$targetClass = new FDConfiguration();						} 	break;
	case 'ADConfiguration':				{	require_once ('./adv/ad.class');						$targetClass = new ADConfiguration();						} 	break;
	case 'Search':							{	require_once ('./adv/search.class');				$targetClass = new SearchRequest();							}	break;
	case 'Backup':							{	require_once ('./adv/search.class');				$targetClass = new RecordBackupRequest();					}	break;
	case 'Serial':							{	require_once ('./adv/serial.class');				$targetClass = new SerialConfiguration();					}	break;
	case 'PTZAuxiliary':					{	require_once ('./adv/relay.class');					$targetClass = new PTZAuxiliary();							}	break;
	case 'PTZInstantAF':					{	require_once ('./adv/relay.class');					$targetClass = new PTZInstantAF();							}	break;
	case 'VideoSourceSelection':		{	require_once ('./adv/av.class');						$targetClass = new VideoSourceSelection();					}	break;
	case 'SmartCodecConfiguration':	{	require_once ('./adv/fd.class');						$targetClass = new SmartCodecConfiguration();				}	break;
	case 'PTZPreset':						{	require_once ('./adv/preset.class');				$targetClass = new PTZPreset($xmlInfo['action']);		}	break;
	case 'PTZSwing': 						{	require_once ('./adv/ptz.class');					$targetClass = new PTZSwing($xmlInfo['action']);			}	break;
	case 'PTZGroup':						{	require_once ('./adv/ptz.class');					$targetClass = new PTZGroup($xmlInfo['action']);			}	break;
	case 'PTZTour': 						{	require_once ('./adv/ptz.class');					$targetClass = new PTZTour($xmlInfo['action']);			}	break;
	case 'PTZLimit': 						{	require_once ('./adv/ptzlimit.class');				$targetClass = new PTZLimit($xmlInfo['action']);			}	break;
	case 'PTZTrace': 						{	require_once ('./adv/ptz.class');					$targetClass = new PTZTrace($xmlInfo['action']);			}	break;
	case 'PTZAutorun': 					{	require_once ('./adv/ptz.class');					$targetClass = new PTZAutorun($xmlInfo['action']);		}	break;
	case 'PTZStatus': 						{	require_once ('./adv/ptzmove.class');				$targetClass = new PTZStatus($xmlInfo['action']);		}	break;
	case 'PTZStop':							{	require_once ('./adv/ptzmove.class');				$targetClass = new PTZStop($xmlInfo['action']);			}	break;
	case 'MotorizedLensSetup':			{	require_once ('./adv/ptzmove.class');				$targetClass = new MotorizedLensSetup();					}	break;
	case 'QoS':								{	require_once ('./adv/qos.class');					$targetClass = new QoSConfiguration();						}	break;
	case 'ContinuousRecord':				{	require_once ('./adv/continuous_record.class');	$targetClass = new ContinuousRecord();						}	break;
	case 'SNMP':								{	require_once ('./adv/network_snmp.class');		$targetClass = new SNMPConfiguration();						}	break;
	case 'SNMPTrap':						{	require_once ('./adv/network_snmp.class');		$targetClass = new SNMPTrapConfiguration();				}	break;
	case 'UPNP':								{	require_once ('./adv/autodiscovery.class');		$targetClass = new UPNPConfiguration();						}	break;
	case 'Bonjour':							{	require_once ('./adv/autodiscovery.class');		$targetClass = new BonjourConfiguration();					}	break;
	case 'ZeroConfig':						{	require_once ('./adv/autodiscovery.class');		$targetClass = new ZeroConfiguration();						}	break;
	case 'NasConfiguration':				{	require_once ('./adv/nas.class');					$targetClass = new NasConfiguration();						}	break;
	case 'ISCSIConfiguration':			{	require_once ('./adv/nas.class');					$targetClass = new ISCSIConfiguration();					}	break;
	case 'ISCSIDiscovery':				{	require_once ('./adv/nas.class');					$targetClass = new ISCSIDiscovery();							}	break;
	case 'EventConfiguration':			{	require_once ('./adv/event.class');					$targetClass = new EventConfiguration();					}	break;
	case 'TrackingPreset':				{	require_once ('./adv/tracking.class');				$targetClass = new TrackingPreset();							}	break;
	case 'TrackingTargetlock':			{	require_once ('./adv/tracking.class');				$targetClass = new TrackingTargetlock();					}	break;
	case 'TrackingConfiguration':		{	require_once ('./adv/trackingEvent.class');		$targetClass = new TrackingConfiguration();				}	break;
	case 'OnvifConfiguration':			{	require_once ('./adv/system.class');				$targetClass = new OnvifConfiguration()	;					}	break;
	case 'VideoProfile':					{	require_once ('./adv/profile.class');				$targetClass = new VideoProfile();							}	break;
	case 'StreammingDisconnection':	{	require_once ('./adv/profile.class');				$targetClass = new StreammingDisconnection();				}	break;
	case 'PrivacyArea':					{	require_once ('./adv/maskarea.class');				$targetClass = GetMaskArea();								}	break;
	case 'VAMaskArea':						{	require_once ('./adv/maskarea.class');				$targetClass = GetMaskArea();								}	break;
	case 'TrackingMaskArea':				{	require_once ('./adv/maskarea.class');				$targetClass = GetMaskArea();								}	break;
	case 'RecordConfiguration':			{	require_once ('./adv/record.class');				$targetClass = new RecordConfiguration();					}	break;
	case 'RegisterData':					{	require_once ('./adv/register.class');				$targetClass = GetRegisterClass();							}	break;
	case 'RelayOutputState':				{	require_once ('./adv/relay.class');					$targetClass = GetRelayClass();								}	break;
	case 'ManualRecording':				{	require_once ('./adv/relay.class');					$targetClass = new ManualRecording();						} 	break;
	case 'PTZPreseEdit':					{	require_once ('./adv/ptz.class');					$targetClass = new PTZPreseEdit();							}	break;
	case 'PresetList':						{ 	require_once ('./adv/simplepreset.class');		$targetClass = new PresetList();							}	break;
	case 'Log':								{	require_once ('./adv/log.class');					ConnectionLog();													}	break;
	case 'Configuration':					{	require_once ('./adv/backup.class');				ConnectionConfiguration();									}	break;
	case 'PTZHomePosition':				{	require_once ('./adv/ptz.class');					ConnectionHomePosition();									}	break;
	case 'PTZAzimuthPosition':			{	require_once ('./adv/ptz.class');					ConnectionAzimuthPosition();								}	break;	
	case 'OSD':								{	require_once ('./adv/osd.class');					ConnectionOSD();													}	break;
// OPEN PLATFORM
	case 'SDK':								{	require_once ('./adv/sdk.class');					SDK_Information();												} 	break;
	case 'SDKTaskManager':       		{	require_once ('./adv/sdk.class');					SDK_TaskManager();												}	break;
	case 'SDKAppAttributes':				{	require_once ('./adv/sdk.class');					SDK_ReadWriteAppAttributes();								} 	break;
	case 'SDK_APP':							{	                                  					SDK_APP_ReadWriteSettings();						      } 	break;
	case 'SDK_APP_DATA':					{	require_once ('./adv/sdk_app.class');				SDK_APP_DATA_GetSetAppData();				            } 	break;
	case 'CMD_SDK_MARKET':				{																	SDK_MARKET_InstallApp();										} 	break;
	case 'CMD_SDK_MARKET_SERVERSETTINGS':	{                                       		SDK_MARKET_ServerSettings();								} 	break;
	case 'SDK_APP_STATUS':            {																	GetAppStatus();						        					}	break;
	case 'SDK_APP_INFO':                            {       require_once ('./adv/sdk.class');SDK_APP_Information();                 } break;
	case 'CMD_SDK_CANCEL':                          {
                                                                SDK_CancelInstallation();
					                } break;
	case 'PresetVAConfiguration':		{	require_once ('./adv/presetedit.class');			ConnectionPresetEdit();										}	break;
	case 'PresetImageConfiguration':	{	require_once ('./adv/presetedit.class');			ConnectionPresetEdit();										}	break;
	case 'CMD_REMOTE_DEBUG':						{	require_once ('./adv/sdk.class');					SDK_APP_Debug();								} break;
	case 'CONFORMANCE':                {   require_once ('./adv/sdk_conformance.class');           SDK_ConformanceRequest(); } break;
}

switch($xmlInfo['action']) {
	case ACTION_GET_ALL: {
		if ($xmlInfo['menu'] == 'RegisterData') {
			$targetClass->XMLtoArray($xmlInfo['action']);
		}
		$GLOBALS['SOCKET_MANAGER']->Connection($targetClass);
		ResponseXML($targetClass, $xmlInfo['menu']);
	} break;
	case ACTION_GET: {
		if (	$xmlInfo['menu'] == 'PTZPreset' 	|| $xmlInfo['menu'] == 'PTZSwing'	|| $xmlInfo['menu'] == 'ImageSetting' 	||	$xmlInfo['menu'] == 'PTZAuxliary' ||
				$xmlInfo['menu'] == 'Backup'		||	$xmlInfo['menu'] == 'PTZGroup'	|| $xmlInfo['menu'] == 'RegisterData'	||	substr($xmlInfo['menu'], 0, 13) == 'PTZPresetAttr') {
			$targetClass->XMLtoArray($xmlInfo['action']);
		}
		$GLOBALS['SOCKET_MANAGER']->Connection($targetClass);
		if ($xmlInfo['menu'] != 'Backup') ResponseXML($targetClass, $xmlInfo['menu']);
	} break;
	case ACTION_STOP: 	{
		if ($xmlInfo['menu'] == 'ImageSetting' || $xmlInfo['menu'] == 'ManualRecording') {
			$targetClass->headerInfo['Action'] = $xmlInfo['action'];
			$targetClass->payload = '';
			$GLOBALS['SOCKET_MANAGER']->Connection($targetClass);
		}
		else if ($xmlInfo['menu'] == 'PTZPresetAttr' || $xmlInfo['menu'] == 'PresetImageConfiguration' || $xmlInfo['menu'] == 'PTZPreseEdit') {
			$targetClass->headerInfo['Action'] = $xmlInfo['action'];
			$targetClass->XMLtoArray($xmlInfo['action']);
			$GLOBALS['SOCKET_MANAGER']->Connection($targetClass);
		}
	} break;
	default: 	{
		if (	$xmlInfo['menu'] != 'Format'	&& $xmlInfo['menu'] != 'PrivacyArea'		&&	$xmlInfo['menu'] != 'HTTPSData' 		&&	$xmlInfo['menu'] != 'RelayOutputState'		&&
				$xmlInfo['menu'] != 'Reboot'	&& $xmlInfo['menu'] != 'VAMaskArea'			&&	$xmlInfo['menu'] != 'RegisterData'	&&	$xmlInfo['menu'] != 'MotorizedLensSetup' 	&&
				$xmlInfo['menu'] != 'Reset'		&& $xmlInfo['menu'] != 'Search'				&&	$xmlInfo['menu'] != 'PTZInstantAF'	&&	$xmlInfo['menu'] != 'Data802Dot1x' 			&&
				$xmlInfo['menu'] != 'Backup'	&&	$xmlInfo['menu'] != 'NasConfiguration' &&	$xmlInfo['menu'] != 'PTZAuxiliary'	&&	$xmlInfo['menu'] != 'ManualRecording'		&&
				$xmlInfo['menu'] != 'TrackingTargetlock' && $xmlInfo['menu'] != 'TrackingMaskArea' && substr($xmlInfo['menu'], 0, 3) != 'PTZ' && $xmlInfo['action'] != ACTION_START) {
			$GLOBALS['SOCKET_MANAGER']->Connection($targetClass);
		}
		$targetClass->headerInfo['Action'] = $xmlInfo['action'];
		$targetClass->XMLtoArray($xmlInfo['menu']);
		$GLOBALS['SOCKET_MANAGER']->Connection($targetClass);
	} break;
}

//	Function
function GetMaskArea()
{
	$cmd 		= CMD_PRIVACY_AREA;
	$maxArea = $GLOBALS['M_SUPPORT_PRIVACY_AREA'];
	if ($GLOBALS['xmlInfo']['menu'] == 'VAMaskArea') {
		$cmd 		= CMD_VAMASK_AREA;
		$maxArea = 4;
	}
	else if ($GLOBALS['xmlInfo']['menu'] == 'TrackingMaskArea') {
		$cmd		= CMD_TRACKING_TRACEZONE;
		$maxArea = 8;
	}
	if ($GLOBALS['xmlInfo']['action'] == ACTION_GET_ALL) {
		$targetClass = new MaskAreas($cmd, $maxArea);
		return $targetClass;
	}
	else {
		$targetClass = new MaskArea($cmd);
		$targetClass->headerInfo['Action'] = $GLOBALS['xmlInfo']['action'];
		$targetClass->XMLtoArray($GLOBALS['xmlInfo']['action']);
		$GLOBALS['SOCKET_MANAGER']->Connection($targetClass);
		exit;
	}
}

function GetRegisterClass()
{
	if ($GLOBALS['xmlInfo']['action'] == ACTION_SET)	return new RegData();
	return new RegDataRequest();
}

function GetRelayClass()
{
	require_once ('./adv/info.class');
	$info = $GLOBALS['SOCKET_MANAGER']->Connection(new Information());
	if ($info->dataInfo['UserRightRelay']['value'] != 1) ResponseText(FALSE);
	return new RelayOutputState();
}

function ConnectionLog()
{
	$logSearchConf = new LogSearchRequest();
	$logSearchConf->SetHeaderCommand(CMD_LOG_SEARCH);
	$logSearchConf->SetCGIPayload();
	$GLOBALS['SOCKET_MANAGER']->Connection($logSearchConf);
	$logTotalCount = $logSearchConf->logSearchResults->dataInfo['ResultCount']['value'];
	$logSearchConf->SetHeaderCommand(CMD_LOG_SEARCH_DETAIL);
	$logSearchConf->SetCGIPayload($logTotalCount);
	$GLOBALS['SOCKET_MANAGER']->Connection($logSearchConf);
	$logResultConf = $logSearchConf->logSearchDetailResults;
	header('Content-Type: text/xml; charset=utf-8');
	echo $logSearchConf->GetXMLData();
	exit;
}

function ConnectionConfiguration()
{
	$targetClass = new ConfigurationData($GLOBALS['xmlInfo']['action']);
	if ($GLOBALS['xmlInfo']['action'] == ACTION_SET) {
		$targetClass->headerInfo['Action'] = $GLOBALS['xmlInfo']['action'];
		$targetClass->XMLtoArray($GLOBALS['xmlInfo']['menu']);
	}
	$GLOBALS['SOCKET_MANAGER']->Connection($targetClass);
	exit;
}

function ConnectionHomePosition()
{
	$targetClass = new PTZHomePosition($GLOBALS['xmlInfo']['action']);
	if ($GLOBALS['xmlInfo']['action'] == ACTION_START) {
		$targetClass->XMLtoArray($GLOBALS['xmlInfo']['menu']);
	}
	$GLOBALS['SOCKET_MANAGER']->Connection($targetClass);
	exit;
}

function ConnectionAzimuthPosition()
{
	$targetClass = new PTZAzimuthPosition($GLOBALS['xmlInfo']['action']);
	$GLOBALS['SOCKET_MANAGER']->Connection($targetClass);
	exit;
}


function ConnectionOSD()
{
	require_once ('./adv/info.class');
	$info = $GLOBALS['SOCKET_MANAGER']->Connection(new Information());
	if ($info->dataInfo['UserRightCtrl']['value'] != 1) ResponseText(FALSE);
	$targetClass = new OSDOperation($GLOBALS['xmlInfo']['action']);
	if	($GLOBALS['xmlInfo']['action'] == ACTION_SET) {
		$targetClass->headerInfo['Action'] = $GLOBALS['xmlInfo']['action'];
		$targetClass->XMLtoArray($GLOBALS['xmlInfo']['menu']);
	}
	$GLOBALS['SOCKET_MANAGER']->Connection($targetClass);
	exit;
}

function ConnectionPresetEdit()
{
	if ($GLOBALS['xmlInfo']['menu'] == 'PresetVAConfiguration') {
		$targetClass = new PresetVAConfiguration();
	}
	else {
		$targetClass = new PresetImageConfiguration();
	}
	$targetClass->XMLtoArray($GLOBALS['xmlInfo']['menu']);
	$GLOBALS['SOCKET_MANAGER']->Connection($targetClass);

	$targetClass->headerInfo['Action'] = $GLOBALS['xmlInfo']['action'];
	$targetClass->XMLtoArray($GLOBALS['xmlInfo']['menu']);	
	$GLOBALS['SOCKET_MANAGER']->Connection($targetClass);
	exit;
}

function SDK_Information()
{
	$targetClass = new SDK($GLOBALS['xmlInfo']['action']);
	$targetClass->headerInfo['Action'] = $GLOBALS['xmlInfo']['action'];
	$targetClass->XMLtoArray($GLOBALS['xmlInfo']['menu']);
	$GLOBALS['SOCKET_MANAGER']->Connection($targetClass);
	$targetClass->SendResponse();
	exit;
}

function SDK_APP_Information()
{
	$targetClass = new SDKInfoRequest($GLOBALS['xmlInfo']['action']);
	$targetClass->headerInfo['Action'] = $GLOBALS['xmlInfo']['action'];
	$GLOBALS['SOCKET_MANAGER']->Connection($targetClass);
	$targetClass->SendResponse();
	exit;
}
function SDK_TaskManager()
{
	$targetClass = new SDK_Task_Manager($GLOBALS['xmlInfo']['action']);
	$targetClass->headerInfo['Action'] = $GLOBALS['xmlInfo']['action'];
	$targetClass->XMLtoArray($GLOBALS['xmlInfo']['menu']);
	$GLOBALS['SOCKET_MANAGER']->Connection($targetClass);
	$targetClass->SendResponse();
	exit;
}
function SDK_ConformanceRequest()
{
	$targetClass = new SDK_Conformance($GLOBALS['xmlInfo']['action']);
	$targetClass->headerInfo['Action'] = $GLOBALS['xmlInfo']['action'];
	$targetClass->XMLtoArray($GLOBALS['xmlInfo']['menu']);
	$GLOBALS['SOCKET_MANAGER']->Connection($targetClass);
	$targetClass->SendResponse();
	exit;
}

function SDK_ReadWriteAppAttributes()
{
	$targetClass = new SDK_App_Attributes($GLOBALS['xmlInfo']['action']);
	$targetClass->headerInfo['Action'] = $GLOBALS['xmlInfo']['action'];
	$targetClass->XMLtoArray($GLOBALS['xmlInfo']['menu']);
	$GLOBALS['SOCKET_MANAGER']->Connection($targetClass);
	$targetClass->SendResponse();
	exit;
}

function GetAppStatus()
{
    require_once ('./adv/sdk.class');

    $APP_NAME = "";
    $xmlData = str_replace('&_=', '', rawurldecode(trim(@file_get_contents('php://input'))));
    $xml = simplexml_load_string($xmlData);

    foreach($xml as $NodeName => $NodeValue)
     {
         if($NodeName == 'AppName')
            {
              $APP_NAME = $NodeValue;
              break;
            }
     }

    $targetClass = new SDKInfoRequest(ACTION_GET);
    $targetClass->dataInfo['AppName']['value'] = $APP_NAME;
    $targetClass->payload = MakePayload($targetClass->dataInfo);
    $GLOBALS['SOCKET_MANAGER']->Connection($targetClass);
	$APPSTATUS = $targetClass->sdk_app->dataInfo['app_status']['value'];

	$msg = '<?xml version="1.0" encoding="utf-8" ?>'."\n";
    $msg .= '<Results>'."\n";
    $msg .= '<Status>';
    $msg .= "OK";
    $msg .= '</Status>'."\n";
	$msg .= '<AppName>';
    $msg .= $APP_NAME ;
    $msg .= '</AppName>'."\n";
	$msg .= '<AppStatus>';
    $msg .= $APPSTATUS;
    $msg .= '</AppStatus>'."\n";
    $msg .= '</Results>'."\n";
    header('Content-Type: text/xml; charset=utf-8');
    header('Content-Length: '.strlen($msg));
    echo $msg;


}

function SDK_APP_ReadWriteSettings()
{
        $xmlToObject = '';
        $APP_NAME = "";

        $xmlData = str_replace('&_=', '', rawurldecode(trim(@file_get_contents('php://input'))));
        $xml = simplexml_load_string($xmlData);

        foreach($xml as $NodeName => $NodeValue)
        {
            if($NodeName == 'AppName')
            {
              $APP_NAME = $NodeValue;
              break;
            }
        }

        $FILE_PATH = $GLOBALS['SDK_APP_INSTALL_DIRECTORY'].$APP_NAME."/".$GLOBALS['SDK_APP_CONFIG_FILE'];

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

        if($GLOBALS['xmlInfo']['action'] == ACTION_GET)
        {
              $XML_FILE_STRING = $xmlToObject->asXML();

              header('Content-Type: text/xml; charset=utf-8');
      	      header('Content-Length: '.strlen($XML_FILE_STRING));
      	      echo $XML_FILE_STRING;
        }
        else if($GLOBALS['xmlInfo']['action'] == ACTION_SET)
        {
            foreach($xml as $NodeName => $NodeValue)
            {
                if($NodeName == 'AppName')
                    continue;

                if (is_object($NodeValue))
                {
                     foreach($NodeValue as $ChildNodeName => $ChildNodeValue)
                     {
                          if(isset($xmlToObject->$NodeName->$ChildNodeName))
                          {
                              $xmlToObject->$NodeName->$ChildNodeName = $ChildNodeValue;
                          }
                     }
                }
            }

            $xmlToObject->asXML($FILE_PATH); // Save File

            $msg = '<?xml version="1.0" encoding="utf-8" ?>'."\n";
      	    $msg .= '<Results>'."\n";
      	    $msg .= '<Status>';
      	    $msg .= "OK";
      	    $msg .= '</Status>'."\n";
      	    $msg .= '</Results>'."\n";
      	    header('Content-Type: text/xml; charset=utf-8');
      	    header('Content-Length: '.strlen($msg));
      	    echo $msg;
        }
	exit;
}

function SDK_APP_DATA_GetSetAppData()
{
        $APP_NAME = "";
        $DATA_LENGTH = 0;

        $xmlData = str_replace('&_=', '', rawurldecode(trim(@file_get_contents('php://input'))));
        $xml = simplexml_load_string($xmlData);
        foreach($xml as $key => $value)
        {
            if($key == 'AppName')
            {
                 $APP_NAME = $value;
            }
            else if($key == 'Data')
            {
                 $DATA_LENGTH = strlen($value);
            }
            else
            {
                 break;
            }
        }

        $APP_IPC_PATH = $GLOBALS['SDK_APP_IPC_DIRECTORY'].$APP_NAME;

        if (file_exists($APP_IPC_PATH))
        {
	    $targetClass = new SDK_APP_DATA_Request($GLOBALS['xmlInfo']['action'], $DATA_LENGTH);
	    $targetClass->headerInfo['Action'] = $GLOBALS['xmlInfo']['action'];
	    $targetClass->XMLtoArray($GLOBALS['xmlInfo']['menu']);
  	    $App_SocketManager = new SocketManager($APP_IPC_PATH);
            $App_SocketManager->Connection($targetClass);
            $targetClass->SendResponse();
        }
        else
        {
            $msg = '<?xml version="1.0" encoding="utf-8" ?>'."\n";
      	    $msg .= '<Error>'."\n";
      	    $msg .= '<ErrorString>';
      	    $msg .= "ERROR: Failed to establish communication with application."."\n"."Application is not running."."\n"."Please start the application and try again.";
      	    $msg .= '</ErrorString>'."\n";
      	    $msg .= '</Error>'."\n";
      	    header('Content-Type: text/xml; charset=utf-8');
      	    header('Content-Length: '.strlen($msg));
      	    echo $msg;
        }
        exit;
}

function SDK_MARKET_ServerSettings()
{
		$MARKET_FILEPATH = "";

		$xmlData = str_replace('&_=', '', rawurldecode(trim(@file_get_contents('php://input'))));
        $xml = simplexml_load_string($xmlData);

		foreach($xml as $NodeName => $NodeValue)
        {
            if($NodeName == 'SettingsPath')
            {
              $MARKET_FILEPATH = $NodeValue;
              break;
            }
        }

		if (file_exists($MARKET_FILEPATH))
        {
            try
            {
                $xmlToObject = new SimpleXMLElement($MARKET_FILEPATH, NULL, TRUE);
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

	if ($GLOBALS['xmlInfo']['action'] == ACTION_GET) {
		 $XML_FILE_STRING = $xmlToObject->asXML();
         header('Content-Type: text/xml; charset=utf-8');
	     header('Content-Length: '.strlen($XML_FILE_STRING));
      	 echo $XML_FILE_STRING;
	}
	if ($GLOBALS['xmlInfo']['action'] == ACTION_SET) {

		foreach($xml as $NodeName => $NodeValue)
            {
               if (is_object($NodeValue))
                {
                   if(isset($xmlToObject->$NodeName))
                   {
                              $xmlToObject->$NodeName = $NodeValue;
                   }
                }
            }

		$xmlToObject->asXML($MARKET_FILEPATH); // Save File

        $msg = '<?xml version="1.0" encoding="utf-8" ?>'."\n";
      	$msg .= '<Results>'."\n";
      	$msg .= '<Status>';
      	$msg .= "OK";
      	$msg .= '</Status>'."\n";
      	$msg .= '</Results>'."\n";
      	header('Content-Type: text/xml; charset=utf-8');
      	header('Content-Length: '.strlen($msg));
      	echo $msg;
	}
    exit;
}
function SDK_MARKET_InstallApp()
{
        $APP_NAME = "";
	$DATA_URL = "";
	$xmlData = str_replace('&_=', '', rawurldecode(trim(@file_get_contents('php://input'))));
        $xml = simplexml_load_string($xmlData);
        foreach($xml as $key => $value)
        {
            if($key == 'AppName')
            {
                 $APP_NAME = $value;
            }
            else if($key == 'Data')
            {
                 $DATA_URL = $value;
            }
        }
	//error_log("stw- market fn - APP_NAME -> ".$APP_NAME);
        //error_log("stw- market fn - DATA_URL -> ".$DATA_URL);

	if($DATA_URL)
	{
		$MARKET_DOWNLOAD_FILE = $GLOBALS['SDK_MARKET_APP_DIRECTORY'].$APP_NAME.".cap";
		$username="admin";
		$password="admin";
		$context = stream_context_create(array(
			'http' => array('header'  => "Authorization: Basic " . base64_encode("$username:$password")
		)));
		;
		$getFile = @file_get_contents($DATA_URL,false,$context);
		if($getFile)
                {
			$putFile = file_put_contents($MARKET_DOWNLOAD_FILE,$getFile);

          		//sending success message
          		$msg = '<?xml version="1.0" encoding="utf-8" ?>'."\n";
                	$msg .= '<Results>';
                	$msg .= '<Status>';
                	    $msg .= "OK";
                	    $msg .= '</Status>';
          			$msg .= "<AppName>".$APP_NAME."</AppName>";
                	    $msg .= '</Results>';
                	    header('Content-Type: text/xml; charset=utf-8');
                	    header('Content-Length: '.strlen($msg));
                	    echo $msg;
          	}
                else
                {
          		    //sending error message
          		    error_log("ERROR: Failed to establish communication with Market Server.");
          		    $msg = '<?xml version="1.0" encoding="utf-8" ?>'."\n";
                	    $msg .= '<Error>';
                	    $msg .= '<ErrorString>';
                	    $msg .= "ERROR: Failed to establish communication with Market Server.";
                	    $msg .= '</ErrorString>';
                	    $msg .= '</Error>';
                	    header('Content-Type: text/xml; charset=utf-8');
                	    header('Content-Length: '.strlen($msg));
          			//header('HTTP', true, 500);
                	    echo $msg;
		}

                //error_log("stw- market fn - MARKET_DOWNLOAD_FILE -> ".$MARKET_DOWNLOAD_FILE);
		//error_log("stw- market fn - getFile -> ".$getFile);
		//error_log("stw- market fn - putFile -> ".$putFile);
	}
       exit;
}

function SDK_CancelInstallation()
{
    error_log("Entered SDK_CancelInstallation");
    $CANCEL_DIR_PATH = "";
    $xmlData = str_replace('&_=', '', rawurldecode(trim(@file_get_contents('php://input'))));
    $xml = simplexml_load_string($xmlData);
    if ($GLOBALS['xmlInfo']['action'] == ACTION_GET) {
        foreach($xml as $NodeName => $NodeValue) {
            if($NodeName == 'DirPath') {
                $CANCEL_DIR_PATH = $NodeValue;
		error_log("SDK_CancelInstallation : path = ".$CANCEL_DIR_PATH);
                break;
            }
        }
        $msg = 'cancelsdk';
        if(!file_exists($CANCEL_DIR_PATH) || !is_dir($CANCEL_DIR_PATH)) {
            error_log("SDK_CancelInstallation : file doesn't exists ".$CANCEL_DIR_PATH);
            exit;
        }
        recursive_remove_directory($CANCEL_DIR_PATH);
        $msg = 'done';
        error_log("****SDK_CancelInstallation*****");
	$msg = '<?xml version="1.0" encoding="utf-8" ?>'."\n";
      	$msg .= '<Results>'."\n";
      	$msg .= '<Status>';
      	$msg .= "OK";
      	$msg .= '</Status>'."\n";
      	$msg .= '</Results>'."\n";
      	header('Content-Type: text/xml; charset=utf-8');
      	header('Content-Length: '.strlen($msg));
      	echo $msg;
        exit;
    }
}
function recursive_remove_directory($directory)
{
    if(is_readable($directory)) {
	$handle = opendir($directory);
        while (FALSE !== ($item = readdir($handle))) {
       	    if($item != '.' && $item != '..') {
                $path = $directory.'/'.$item;
                if(is_dir($path)) {
            	    recursive_remove_directory($path);
                } else {
            	    error_log("recursive_remove_directory : remove = ".$path);
                    unlink($path);
                }
            }
        }
        closedir($handle);
       	error_log("recursive_remove_directory : remove = ".$directory);
        rmdir($directory);
    } else {
        error_log("recursive_remove_directory : folder is not readable");
    }
    return;
}
function SDK_APP_Debug()
{
	
	$targetClass = new SDK_RemoteDebug($GLOBALS['xmlInfo']['action']);
	$targetClass->headerInfo['Action'] = $GLOBALS['xmlInfo']['action'];
	$targetClass->XMLtoArray($GLOBALS['xmlInfo']['menu']);
	$GLOBALS['SOCKET_MANAGER']->Connection($targetClass);
	$targetClass->SendResponse();
	exit;
}
?>
