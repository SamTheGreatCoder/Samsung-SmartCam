<?php	
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";	

$pageData = explode(";", $_POST["data"]); 
if($pageData[0] == "LIVE"){ //0:action, 1:cmos, 2:FlipMode, 3:Brightness
	$sendData = explode(",", $pageData[1]);
	
// 	int2byte($sendData, intval($pageData[3]), 24); //Brightness
// 	int2byte($sendData, intval($pageData[2]), 72); //FlipMode
	$sendData[count($sendData)] = 0;
	
	$result = requestToCamera(CMD_CMOS_CONFIGURATION, ACTION_SET, TYPE_REQUEST, $sendData);
	if($result[0] == "OK"){
		echo "OK";
	}else{
		echo "NOK;" . $result[1];
	}
}else if($pageData[0] == "SET"){ //0:action, 1:cmos, 2:media, 3:motion
	$sendData = explode(",", $pageData[1]);  		//4:FlipMode, 5:Brightness, 6:FlickerMode, 7:IrMode	
// 	int2byte($sendData, intval($pageData[5]), 24);	//Brightness
// 	int2byte($sendData, intval($pageData[4]), 72); 	//FlipMode
// 	int2byte($sendData, intval($pageData[6]), 76); 	//FlickerMode
// 	int2byte($sendData, intval($pageData[7]), 96); 	//IrMode
	$sendData[count($sendData)] = 0;
	
	$result = requestToCamera(CMD_CMOS_CONFIGURATION, ACTION_SET, TYPE_REQUEST, $sendData);
	if($result[0] != "OK"){
		echo "NOK;" . $result[1];
		return;
	}
	
	$sendData = explode(",", $pageData[2]);  		//8:Audio_mic, 9:Audio_spk		
// 	int2byte($sendData, intval($pageData[8]), 212); //Audio_mic
// 	int2byte($sendData, intval($pageData[9]), 282); //Audio_spk
	
	$result = requestToCamera(CMD_MEDIA_CONFIGURATION, ACTION_SET, TYPE_REQUEST, $sendData);
	if($result[0] != "OK"){
		echo "NOK;" . $result[1];
		return;
	}
	
	$sendData = explode(",", $pageData[3]);  		//10:Motion, 11:Sensitivity, 12:Activation, 13~19:Sun ~ Sat, 20:Enabled, 21:Sensitivity	
// 	$sendData[1] = intval($pageData[10]);
// 	$sendData[4] = intval($pageData[11]);
// 	$sendData[1106] = intval($pageData[12]);
	
// 	for($i=13, $k=1107; $i<20; $i++){
// 		$time = explode(",", $pageData[$i]);
// 		for($j=0; $j<24; $j++, $k++){
// 			$sendData[$k] = intval($time[$j]);
// 		}
// 	}
// 	$sendData[2055] = intval($pageData[20]);
// 	$sendData[2056] = intval($pageData[21]);
	
	$result = requestToCamera(CMD_VA_CONFIGURATION, ACTION_SET, TYPE_REQUEST, $sendData);
	if($result[0] == "OK"){
		echo "OK";
	}else{
		echo "NOK;" . $result[1];
	}
}else if($pageData[0] == "IPCV0.7"){
	if($pageData[1] == "FLIP"){
		$sendData = explode(",", $pageData[2]);
		$result = requestToCamera(getNewCmd(CMD_VIDEO_SOURCE), ACTION_SET, TYPE_REQUEST, $sendData);
		if($result[0] == "OK"){
			echo "OK";
		}else{
			echo "NOK;" . $result[1];
		}
	}else if($pageData[1] == "CMOS"){
		$sendData = explode(",", $pageData[2]);
		$sendData[count($sendData)] = 0;
		$result = requestToCamera(getNewCmd(CMD_CMOS_CONFIGURATION), ACTION_SET, TYPE_REQUEST, $sendData);
		if($result[0] == "OK"){
			echo "OK";
		}else{
			echo "NOK;" . $result[1];
		}
	}else if($pageData[1] == "VIDEO_SET_ALL"){  
		//1.newCmos 2.media 3.vaConf 4.adEvent 5.recordConf
		//$media // 스피커, 마이크 CMD_MEDIA_CONFIGURATION
		//$newCmos //WDR, Brightness, flk, night  getNewCmd(CMD_CMOS_CONFIGURATION)
		//$vaConf // motion, sens, times getNewCmd(CMD_VA_CONFIGURATION)
		//$adEvent // audio sens, getNewCmd(CMD_AD_EVENT)
		//$recordConf // mnt, ow, getNewCmd(CMD_RECORD_CONFIGURATION)
		
		$sendData = explode(",", $pageData[2]); //newCmos
		$sendData[count($sendData)] = 0;
		$result = requestToCamera(getNewCmd(CMD_CMOS_CONFIGURATION), ACTION_SET, TYPE_REQUEST, $sendData);
		if($result[0] != "OK"){
			echo "NOK;" . $result[1];
			return;
		}
		
		$sendData = explode(",", $pageData[3]); //media
		$result = requestToCamera(CMD_MEDIA_CONFIGURATION, ACTION_SET, TYPE_REQUEST, $sendData);
		if($result[0] != "OK"){
			echo "NOK;" . $result[1];
			return;
		}
		
		$sendData = explode(",", $pageData[4]); //vaConf
		$result = requestToCamera(getNewCmd(CMD_VA_CONFIGURATION), ACTION_SET, TYPE_REQUEST, $sendData);
		if($result[0] != "OK"){
			echo "NOK;" . $result[1];
			return;
		}
		
		$sendData = explode(",", $pageData[5]); //adEvent
		$result = requestToCamera(getNewCmd(CMD_AD_EVENT), ACTION_SET, TYPE_REQUEST, $sendData);
		if($result[0] != "OK"){
			echo "NOK;" . $result[1];
			return;
		}
		
		$sendData = explode(",", $pageData[6]); //recordConf
		$result = requestToCamera(getNewCmd(CMD_RECORD_CONFIGURATION), ACTION_SET, TYPE_REQUEST, $sendData);
		if($result[0] == "OK"){
			echo "OK";
		}else{
			echo "NOK;" . $result[1];
		}
	}
	
}

/* Structure - tImageGetRes
	VideoSourceIndex	int		 	0 ~ 3
	wbMode				int		 	4 ~ 7
	Reserved			char[16]	8 ~ 23
	Brightness			int			24 ~ 27
	Reserved			char[16]	28 ~ 43
	CamTitleMode		int			44 ~ 47
	CamTitle			char[16]	48 ~ 63
	CamTitlePosX		int			64 ~ 67
	CamTitlePosY		int			68 ~ 71
	FlipMode			int			72 ~ 75
	FlickerMode			int			76 ~ 79
	Reserved			char[16]	80  95
	IrMode				int			96 ~ 99
	Reserved			char[4]		100 ~ 103
	Reserved			char[16]	104 ~ 119
*/

/* Structure - tMediaConfiguration
	Token			char[64]		0 ~ 63	
	Enabled			bool			64
	Channel			int				65 ~ 68
	Framerate		int				69 ~ 72
	Width			int				73 ~ 76
	Height			int				77 ~ 80
 	Token			char[64]		81 ~ 144		
	Enabled			bool			145
	Token			char[64]		146 ~ 209	
	Enabled			bool			210
	Channel			byte			211
	Gain			int				212 ~ 215  	- Audio_mic
	Token			char[64]		216 ~ 279	
	Enabled			bool			280
	Channel			byte			281
	Gain			int				282 ~ 285	- Audio_spk						
	VideoType		bool			286						
	Reserved		char[127]		287 ~ 413
*/

/* Structure - tVAConfiguration
	Mode				byte							0
	Enabled				bool							1
	Overlay				bool							2
	VABoxDisplay		bool							3
	Sensitivity			byte							4
	ObjectMode			byte							5
	ObjectArea			tMDObjectAreaRule[MAX_MDOBJECT]	6 ~ 333	   (328)
	ObjectCell			tMDObjectCellRule				334 ~ 1105 (772)
	Enabled				bool							1106
	Day					tDayTime[7][24]					1107 ~ 1274(=SUN(0), �� , SAT(6) )
	Action				tEventAction					1275 ~ 1293
	Reserved			char[132]						1294 ~ 1425
	IVConf				tIVConfiguration				1426 ~ 2046
	
	Enabled				bool							2047
	Sensitivity			byte 							2048
	Reserved			char[64]						2049 ~ 2112
*/
	
?>