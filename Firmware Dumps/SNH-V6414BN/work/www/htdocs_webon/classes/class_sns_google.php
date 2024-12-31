<?php	
//-------------------------------------------------------------------------------------------------------------
/* Structure - tXmppConfiguration
	typedef struct tagXmppSetting {
		char	enabled;					0
		char	status;						1
		struct {
			struct {
				char	enabled;			2
				char	username[16];		3 ~ 18
				char	password[16];		19 ~ 34
				int		level;				35, 36, 37, 38
				char	video_allowed;		39
				char	audio_allowed;		40
				char	ctrl_allowed;		41
			} user[10];
		} users;
		struct {
			char	manufacturer[64];		402 ~ 465
			char	model[32];				466 ~ 497
			char	firmware_version[16];	498 ~ 513
			char	module_version[16];		514 ~ 529
			char	ptz_version[16];		530 ~ 545
			char	last_update[32];		546 ~ 577
			char	serial_number[32];		578 ~ 609
			char	hardware_id[16];		610 ~ 625
			char	device_name[32];		626 ~ 657
			char	location[64];			658 ~ 721
			char	description[64];		722 ~ 785
			char	memo[128];				786 ~ 913
			char	language;				914
			int		video_type;				915, 916, 917, 918
			char	if_board_version[16];	919 ~ 934
		} dev_info;
		struct {
			char	xmpp_id[128];			935 ~ 1062
			char	nickname[64];			1063 ~ 1126
			char	ignore_notify;			1127
			char	reserved[60];			1128 ~ 1187
		} buddies[10];
		char	reserved[64];				3465 ~ 3528
	} XmppSetting;
*/

require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";	

$pageData = explode(";", $_POST["data"]); //0:recvData, 1:Enabled, 2:members
$sendData = explode(",", $pageData[0]);

$sendData[0] = intval($pageData[1]);
// for($i=0, $j=935; $i<10; $i++, $j+=253){
// 	str2byte($sendData, "", $j, 128);
// }
// for($i=2, $j=935; $i<count($pageData); $i++, $j+=253){
// 	str2byte($sendData, $pageData[$i], $j, 128);
// }
	
$result = requestToCamera(getNewCmd(CMD_GOOGLE_CONFIGURATION), ACTION_SET, TYPE_REQUEST, $sendData);
if($result[0] == "OK"){
	echo "OK";
}else{
	echo "NOK;" . $result[1];
}

?>