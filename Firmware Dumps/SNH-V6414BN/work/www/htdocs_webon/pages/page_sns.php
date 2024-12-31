<?php
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";
require_once $_SERVER["DOCUMENT_ROOT"] . "/resources/languages/Language.php";

define("OFF_EMAIL"			, 3660);
define("OFF_EMAIL_LIST"		, 128);
define("OFF_EMAIL_SERVER"	, 1408);

$_SESSION["GROUP"] = "Video";
$_SESSION["PAGE"] = "video_live";

while(true){
	$result = requestToCamera(CMD_PROFILE, ACTION_GET, TYPE_REQUEST, null);
	$profile = array(); $error = "";
	if($result[0] == "OK"){
		$videoLive = $result[1];
		for($i=708, $j=0; $i<count($videoLive); $i+=708){
			$prof = byte2str($videoLive, $i, 64);
			if($prof != ""){
				$profile[$j++] = $prof;
			}
		}
		if(count($profile) > 0){
			break;
		}
	}else{
		$error = $result[1];
	}
}

$result = requestToCamera(getNewCmd(CMD_YOUTUBE_CONFIGURATION), ACTION_GET, TYPE_REQUEST, null);
$youtube = array(); $youtube_data = "";
if($result[0] == "OK"){
	$youtube = $result[1];
	$youtube_data = $youtube[0] . ";";						//0: Enable
	$youtube_data .= $youtube[1] . ";";						//1: Status
	$youtube_data .= byte2str($youtube, 2, 128) . ";";    	//2: ID
	$youtube_data .= byte2str($youtube, 130, 128) . ";";	//3: Password
	$youtube_data .= $youtube[258];							//4: Access
}else{
	$error = $result[1];
}

$result = requestToCamera(getNewCmd(CMD_PICASA_CONFIGURATION), ACTION_GET, TYPE_REQUEST, null);
$picasa = array(); $picasa_data = "";
if($result[0] == "OK"){
	$picasa = $result[1];
	$picasa_data = $picasa[0] . ";";    				//0: Enable
	$picasa_data .= $picasa[1] . ";";    				//1: Status
	$picasa_data .= byte2str($picasa, 2, 128) . ";";    //2: ID
	$picasa_data .= byte2str($picasa, 130, 128) . ";";	//3: Password
	$picasa_data .= $picasa[514];						//4: Access
}else{
	$error = $result[1];
}

$result = requestToCamera(getNewCmd(CMD_GOOGLE_CONFIGURATION), ACTION_GET, TYPE_REQUEST, null);
$google = array(); $google_data = ""; $google_users = array();
if($result[0] == "OK"){
	$google = $result[1];
	$google_data = $google[0] . ";";	//0: Enable
	$google_data .= $google[1];			//1: Status
	for($i=0, $k=0, $j=935; $i<10; $i++, $j+=253){
		$user = byte2str($google, $j, 128);
		if($user != null && $user != ""){
			$google_users[$k++] = $user;
		}
	}
}else{
	$error = $result[1];
}

$result = requestToCamera(getNewCmd(CMD_TWITTER_CONFIGURATION), ACTION_GET, TYPE_REQUEST, null);
$twitter = array(); $twitter_data = "";
if($result[0] == "OK"){
	$twitter = $result[1];
	$twitter_data = $twitter[0] . ";";	//0: Enable
	$twitter_data .= $twitter[1];		//1: Status
}else{
	$error = $result[1];
}

$result = requestToCamera(getNewCmd(CMD_NETWORK_CONFIGURATION), ACTION_GET, TYPE_REQUEST, null);
$email = array(); $email_data = "";
if($result[0] == "OK"){
	$email = $result[1];
	if(CheckModelName_SNH('WR15')){
		$email_data = byte2str($result[1], OFF_EMAIL, 128) . ";";      							//0: Sender
		$email_data .= byte2str($result[1], (OFF_EMAIL + OFF_EMAIL_SERVER), 128) . ";";      	//1: Server
		$email_data .= byte2int($result[1], (OFF_EMAIL + OFF_EMAIL_SERVER + 128)) . ";";		//2: Port
		$email_data .= $result[1][OFF_EMAIL + OFF_EMAIL_SERVER + 132] . ";";					//3: Needed
		$email_data .= byte2str($result[1], (OFF_EMAIL + OFF_EMAIL_SERVER + 133), 64) . ";";	//4: User Name
		$email_data .= byte2str($result[1], (OFF_EMAIL + OFF_EMAIL_SERVER + 197), 64) . ";";	//5: Password
		$email_data .= $result[1][OFF_EMAIL + 2949] . ";";										//6: Use SSL
		$email_data .= byte2int($result[1], (OFF_EMAIL + 2950)) . ";";							//7: SSL Port
		/* for($i=0, $j=(OFF_EMAIL + OFF_EMAIL_LIST), $k=0; $i<10; $i++, $j+=128){
		 $user = byte2str($result[1], $j, 128);
		if($user != null && $user != ""){
		$email_users[$k++] = $user;
		}
		} */

		$result = requestToCamera(CMD_SMTP_EXT_CONFIG, ACTION_GET, TYPE_REQUEST, null);
		$email_users = array();
		if($result[0] == "OK"){
			$email = $result[1];
			for($i=0, $j=(OFF_EMAIL + OFF_EMAIL_LIST), $k=0; $i<10; $i++, $j+=128){
				$user = byte2str($result[1], $j, 128);
				if($user != null && $user != ""){
					$email_users[$k++] = $user;
				}
			}
		}else{
			$error = $result[1];
		}
	}else{
		$port[0] = byte2int($result[1], 6560); // email port
		$port[1] = byte2int($result[1], 7974); // email ssl port
		$result = requestToCamera(getNewCmd(CMD_SMTP_EXT_CONFIG), ACTION_GET, TYPE_REQUEST, null);
		if($result[0] == "OK"){
			$email_users = $result[1];
		}else{
			$error = $result[1];
		}
	}

}else{
	$error = $result[1];
}

?>