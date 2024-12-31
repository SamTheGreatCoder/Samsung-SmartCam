<?php
/******************************************************************************************************************
 * define constant
 ******************************************************************************************************************/
//	define("CAMERA_MODEL"			    , "SEC-6410");
//	define("CAMERA_MODEL"			    , "SNH-E6110BN");
	define("CAMERA_MODEL"			    , "SNH-V6414BN");

	define("MAJOR_VERSION"			    , 0x00);
	define("MINOR_VERSION"  			, 0x06);

	define("HEADER_OFF_MAGIC_NUMBER"    , 0);
	define("HEADER_OFF_MAJOR_VERSION"   , 4);
	define("HEADER_OFF_MINOR_VERSION"   , 5);
	define("HEADER_OFF_COMMAND"         , 6);
	define("HEADER_OFF_ACTION"          , 10);
	define("HEADER_OFF_MSG_TYPE"        , 11);
	define("HEADER_OFF_ERROR_CODE"      , 12);
	define("HEADER_OFF_MSG_LENGTH"      , 13);
	define("HEADER_OFF_PEER_IP"         , 17);
	define("HEADER_OFF_PEER_PORT"       , 57);
	define("HEADER_OFF_PEER_ACCOUNT"    , 61);
	define("HEADER_OFF_RESERVED"        , 77);
	define("HEADER_OFF_PAYLOAD"         , 85);

	define("ACTION_GET"          		, 0x00);
  	define("ACTION_GET_ALL"      		, 0x01);
  	define("ACTION_GET_COMPATIBLE"		, 0x02);
  	define("ACTION_GET_OPTION"     		, 0x03);
  	define("ACTION_SET"           		, 0x04);
  	define("ACTION_ADD"           		, 0x05);
  	define("ACTION_REMOVE"        		, 0x06);
  	define("ACTION_START"         		, 0x07);
  	define("ACTION_STOP"          		, 0x08);
  	define("ACTION_PAUSE"         		, 0x09);
  	define("ACTION_RESUME"        		, 0x0A);
  	define("ACTION_GET_ALL_POSITION"	, 0x0B);

  	define("TYPE_REQUEST"        		, 0x00);
  	define("TYPE_RESPONSE"       		, 0x01);
  	define("TYPE_SERVER_PUSH"			, 0x02);

  	define('CMD_SMTP_SETTING'			, 13);
  	define("CMD_NETWORK_CONFIGURATION"	, 15);
  	define("CMD_DATETIME"				, 18);
  	define("CMD_TIMEZONE_INFORMATION"	, 19); // new 0.7
  	define("CMD_FACTORY_DEFAULT"		, 20); 
  	define("CMD_REBOOT"					, 21);
  	define("CMD_SYSTEM_CONFIGURATION"	, 24);
  	define("CMD_USER"					, 25);
  	define("CMD_IMAGING"				, 35);
  	define("CMD_PROFILE"				, 36);
  	define("CMD_PROFILE_CONFIGURATION"	, 37);
  	define("CMD_MEDIA_CONFIGURATION"	, 38);
  	define("CMD_STORAGE_INFORMATION"	, 45);	// new 0.7
  	define("CMD_RECORD_CONFIGURATION"	, 46);	// new 0.7
  	define("CMD_IMAGE_CONFIGURATION"	, 80);	// new 0.7
  	define("CMD_VA_CONFIGURATION"		, 89);
  	define("CMD_VIDEO_SOURCE"			, 101); // new 0.7
  	define("CMD_AD_EVENT"				, 149);	// new 0.7
  	define("CMD_FIRMWARE_UPGRADE"		, 150);
  	define("CMD_WIRELESS_SCANNING"		, 151);
  	define("CMD_CMOS_CONFIGURATION"		, 154);
  	define("CMD_YOUTUBE_CONFIGURATION"	, 156);
  	define("CMD_PICASA_CONFIGURATION"	, 157);
  	define("CMD_GOOGLE_CONFIGURATION"	, 155);
  	define("CMD_TWITTER_CONFIGURATION"	, 158);
  	define("CMD_TWITTER_AUTH_URL"		, 159);
  	define("CMD_TWITTER_ACCESS_TOKEN"	, 160);
  	define("CMD_BUDDY_LIST"				, 161);
  	define("CMD_NETWORK_INTERFACE_DETAIL"	, 305);

  	// new 0.7
  	define("CMD_SNS_CONFIG"					, 1000);
  	define("CMD_XMPP_CONFIG"				, 1001);
  	define("CMD_YOUTUBE_CONFIG"				, 1002);
  	define("CMD_PICASA_CONFIG"				, 1003);
  	define("CMD_TWITTER_CONFIG"				, 1004);
  	define("CMD_TWITTER_GET_AUTH_URL"		, 1005);
  	define("CMD_TWITTER_GET_ACCESS_TOKEN"	, 1006);
  	define("CMD_BUDDY_LIST_2"				, 1007);
  	define("CMD_NETWORK_CONFIGURATION_V2"	, 1008);
  	define("CMD_NETWORK_IF_EXTENSION"		, 1009);	// new 0.7
  	define("CMD_WIRELESS_SCANNING_2"		, 1010);
  	define("CMD_FIRMWARE_UPGRADE_2"			, 1011);
  	define("CMD_NETWORK_DOT11_STATUS"		, 1014);	// new 0.7
  	define("CMD_SMTP_EXT_CONFIG"			, 1015);	// new 0.7
  	define("CMD_NETWORK_STATUS"				, 1016);	// new 0.7
  	define("CMD_LED"						, 1028);	// new 0.7
  	define("CMD_LULLABY"					, 1029);	// new 0.7  	

  	define("BUFFER_SIZE"				, 16384);

	define("MAX_USER_10"				, 12);
  	define("MAX_MD_AREA_HSS"			, 3); // based on smartcam
  	define("MAX_MD_AREA"				, 8);

  	function getNewCmd($cmd){
//  		if(strcmp("SEC-6410",CAMERA_MODEL) == 0 ){
			if (CheckModelName_SNH('WR30') || CheckModelName_SNH('WR40')) {
  			if ($cmd == CMD_NETWORK_CONFIGURATION) {
  				$cmd = CMD_NETWORK_CONFIGURATION_V2;
  			} else if($cmd == CMD_CMOS_CONFIGURATION){
  				$cmd = CMD_IMAGE_CONFIGURATION;
  			} else if($cmd == CMD_GOOGLE_CONFIGURATION){
  				$cmd = CMD_XMPP_CONFIG;
  			} else if($cmd == CMD_YOUTUBE_CONFIGURATION){
  				$cmd = CMD_YOUTUBE_CONFIG;
  			} else if($cmd == CMD_PICASA_CONFIGURATION){
  				$cmd = CMD_PICASA_CONFIG;
  			} else if($cmd == CMD_TWITTER_CONFIGURATION){
  				$cmd = CMD_TWITTER_CONFIG;
  			} else if($cmd == CMD_TWITTER_AUTH_URL){
  				$cmd = CMD_TWITTER_GET_AUTH_URL;
  			} else if($cmd == CMD_TWITTER_ACCESS_TOKEN){
  				$cmd = CMD_TWITTER_GET_ACCESS_TOKEN;
  			} else if($cmd == CMD_BUDDY_LIST){
  				$cmd = CMD_BUDDY_LIST_2;
  			} else if($cmd == CMD_WIRELESS_SCANNING){
  				$cmd = CMD_WIRELESS_SCANNING_2;
  			} else if($cmd == CMD_FIRMWARE_UPGRADE){
  				$cmd = CMD_FIRMWARE_UPGRADE_2;
  			}
  			return $cmd;
  		}
  		return $cmd;
  	}

function CheckModelName_SNH($_param)
{
//	$model = $_SERVER['MODELNAME'];
	$model = CAMERA_MODEL;

	switch($_param) {

///////////////////////////////////////
////////////// PLATFORM
///////////////////////////////////////
		case 'WR15':		               {	if	($model == 'SNH-1011'	) return TRUE;		}	break;
		case 'WR30':		               {	if	($model == 'SNH-6410'		|| $model == 'SNH-P6410BN'		|| $model == 'SEC-6410'	) return TRUE;		}	break;
		case 'WR40':		               {	if	($model == 'SNH-E6411BN' || $model == 'SNH-E6110BN'||	$model == 'SNH-E6440BN' ||	$model == 'SNH-V6414BN' ) return TRUE;		}	break;
		case 'All_WR':					{	if (CheckModelName_SNH('WR15')		|| CheckModelName_SNH('WR30')		|| CheckModelName_SNH('WR40')	) return TRUE;		}	break;

///////////////////////////////////////
////////////// MODEL
///////////////////////////////////////
		case 'All1011':							{	if ($model == 'SNH-1011'		) return TRUE; 	}	break;
		case 'All6410':		               {	if	($model == 'SNH-6410'		|| $model == 'SNH-P6410BN'		|| $model == 'SEC-6410') return TRUE;		}	break;
		case 'All6411':		               {	if	($model == 'SNH-6411'		|| $model == 'SNH-E6411BN' || $model == 'SNH-E6440BN'	) return TRUE;		}	break;
		case 'All6400':							{	if ($model == 'SNH-V6414BN'		) return TRUE; 	}	break;

///////////////////////////////////////
////////////// FEATURE
///////////////////////////////////////
		case 'WDR':						{	if (CheckModelName_SNH('All6411') || CheckModelName_SNH('All6400')) 	return TRUE; } break;
		case 'NO_YTB':						{	if (CheckModelName_SNH('All6411')) 	return TRUE; } break;
		case 'SD':						{	if (CheckModelName_SNH('All6411') || CheckModelName_SNH('All6410') || CheckModelName_SNH('All6400')) 	return TRUE; } break;
	}

	return FALSE;
}

?>
