<?php
require_once ('./adv/_define.inc');
CheckAdminAccount(FALSE);

//프리셋 모션기능 없음 -> 있을 가능성있음(다른 모델에)
//알람출력 제어기능 삭제됨

$getEventCapabilityCmd = "get_setup.event.event_capability";
$getMotionCmd = "get_setup.event.motion";
$setMotionCmd = "set_setup.event.motion";
$getPresetMotionCmd = "get_setup.event.preset_motion";
$setPresetMotionCmd = "set_setup.event.preset_motion";
// $getAlarmSensorCmd = "get_setup.event.alarm_sensor";
// $setAlarmSensorCmd = "set_setup.event.alarm_sensor";
// $getAlarmControlCmd = "get_setup.event.alarm_control";
// $setAlarmControlCmd = "set_setup.event.alarm_control";
$getMirrorCapabilityCmd = "get_setup.mirror.capability";
$getMirrorModeCmd = "get_setup.mirror.mirror_mode";//11
$setMirrorModeCmd = "set_setup.mirror.mirror_mode";
$getOnePushFocusCapabilityCmd = "get_setup.onepush.capability";
$setOnePushFocus = "set_setup.onepush.go";

$apiCmd = $_GET["api"];

if($apiCmd == NULL){
	ResponseText(FALSE);
}
else{
	switch ($apiCmd){
		case $getEventCapabilityCmd:
			ViewEventCapability();
			break;
		case $getMotionCmd:
			ViewMotion();
			break;
		case $setMotionCmd:
			ResponseText( ApplyMotion() );
			break;
 		case $getPresetMotionCmd:
 			ViewPTZPresetVAMD();
 			break;
 		case $setPresetMotionCmd:
 			ResponseText( ApplyPTZPresetVAMD() );
 			break;
// 		case $getAlarmSensorCmd:
// 			ViewAlarm();
// 			break;
// 		case $setAlarmSensorCmd:
// 			ResponseText( ApplyAlarm());
// 			break;
// 		case $getAlarmControlCmd:
// 			break;
// 		case $setAlarmControlCmd:
			// 			ResponseText( ApplyRelayOutput() );
// 			break;
		case $getMirrorCapabilityCmd:
			ViewMirrorCapability();
			break;
		case $getMirrorModeCmd:
			ViewCamera();
			break;
		case $setMirrorModeCmd:
			ResponseText( ApplyCamera() );
			break;
		case $getOnePushFocusCapabilityCmd:
			ViewOnePushFocusCapability();
			break;
		case $setOnePushFocus:
			ResponseText( ApplyFocus() );
			break;
		default:
			ResponseText(FALSE);
			break;
	}
}

function ViewEventCapability()
{
	$model = $_SERVER['MODELNAME'];
	$classInstances= GetClassInstance('va');
	
	header("Content-Type: text/plain");
	
	if($model == "SNP-6200" || $model == "SNP-6200H") {
		echo "motion_type=rect"."\r\n";
		echo"area_count=1"."\r\n";
		echo "block_width=0"."\r\n";
		echo "block_height=0"."\r\n";
		echo "sensitivity=yes"."\r\n";
		echo "sens_min=1"."\r\n";
		echo "sens_max=5"."\r\n";
		echo "preset_md_count=1"."\r\n";
		echo "alarm_in=4"."\r\n";
		echo "alarm_out=2";
		exit;
	}else if($model == "SNB-6004" || $model == "VDR-10001" || $model == "VBR-10003"){
		echo "motion_type=rect"."\r\n";
		echo "area_count=4"."\r\n";
		echo "block_width=0"."\r\n";
		echo "block_height=0"."\r\n";
		for ($index=0; $index<4; ++$index)
		{
			echo 'area'.($index).'_width='.($classInstances['VAConfiguration']->mdConf->objectRule[$index]->mdPoint[1]->dataInfo['PosX']['value'] 
															- $classInstances['VAConfiguration']->mdConf->objectRule[$index]->mdPoint[0]->dataInfo['PosX']['value'])."\r\n";
			echo 'area'.($index).'_height='.($classInstances['VAConfiguration']->mdConf->objectRule[$index]->mdPoint[2]->dataInfo['PosY']['value'] 
															- $classInstances['VAConfiguration']->mdConf->objectRule[$index]->mdPoint[1]->dataInfo['PosY']['value'])."\r\n";
		}
		echo "sensitivity=yes"."\r\n";
		echo "sens_min=1"."\r\n";
		echo "sens_max=5"."\r\n";
		echo "preset_md_count=0"."\r\n";
		echo "alarm_in=1"."\r\n";
		echo "alarm_out=1";
		exit;
	}else if($model == "SNO-L6013RS1" || $model == "SND-L6013RS1"){
		echo "motion_type=rect"."\r\n";
		echo "area_count=4"."\r\n";
		echo "block_width=0"."\r\n";
		echo "block_height=0"."\r\n";
		for ($index=0; $index<4; ++$index)
		{
			echo 'area'.($index).'_width='.($classInstances['VAConfiguration']->mdConf->objectRule[$index]->mdPoint[1]->dataInfo['PosX']['value'] 
															- $classInstances['VAConfiguration']->mdConf->objectRule[$index]->mdPoint[0]->dataInfo['PosX']['value'])."\r\n";
			echo 'area'.($index).'_height='.($classInstances['VAConfiguration']->mdConf->objectRule[$index]->mdPoint[1]->dataInfo['PosY']['value'] 
															- $classInstances['VAConfiguration']->mdConf->objectRule[$index]->mdPoint[0]->dataInfo['PosY']['value'])."\r\n";
		}
		echo "sensitivity=yes"."\r\n";
		echo "sens_min=1"."\r\n";
		echo "sens_max=5"."\r\n";
		echo "preset_md_count=0"."\r\n";
		echo "alarm_in=0"."\r\n";
		echo "alarm_out=0";
		exit;

	}else {
		//일단 모델명이 정확하지않은거같다.
		echo "motion_type=rect"."\r\n";
		echo "area_count=4"."\r\n";
		echo "block_width=0"."\r\n";
		echo "block_height=0"."\r\n";
		for ($index=0; $index<4; ++$index)
		{
			echo 'area'.($index).'_width='.($classInstances['VAConfiguration']->mdConf->objectRule[$index]->mdPoint[1]->dataInfo['PosX']['value'] 
															- $classInstances['VAConfiguration']->mdConf->objectRule[$index]->mdPoint[0]->dataInfo['PosX']['value'])."\r\n";
			echo 'area'.($index).'_height='.($classInstances['VAConfiguration']->mdConf->objectRule[$index]->mdPoint[2]->dataInfo['PosY']['value'] 
															- $classInstances['VAConfiguration']->mdConf->objectRule[$index]->mdPoint[1]->dataInfo['PosY']['value'])."\r\n";
		}
		echo "sensitivity=yes"."\r\n";
		echo "sens_min=1"."\r\n";
		echo "sens_max=5"."\r\n";
		echo "preset_md_count=0"."\r\n";
		echo "alarm_in=1"."\r\n";
		echo "alarm_out=1";
		exit;
	}
}

//function cgi_motion()
function ViewMotion()
{
	$msg = TRUE;
	$classInstances= GetClassInstance('va');
	$model = $_SERVER['MODELNAME'];
	
	header("Content-Type: text/plain");
	
	if($model == "SNB-6004" || $model == "VDR-10001" || $model == "VBR-10003"){
		for ($index=0; $index<4; ++$index) {

// 		echo 'area'.($index).'_0x='. $classInstances['VAConfiguration']->mdConf->objectRule[$index]->mdPoint[0]->dataInfo['PosX']['value']."\r\n";
// 		echo 'area'.($index).'_0y='. $classInstances['VAConfiguration']->mdConf->objectRule[$index]->mdPoint[0]->dataInfo['PosY']['value']."\r\n";
// 		echo 'area'.($index).'_1x='. $classInstances['VAConfiguration']->mdConf->objectRule[$index]->mdPoint[1]->dataInfo['PosX']['value']."\r\n";
// 		echo 'area'.($index).'_1y='. $classInstances['VAConfiguration']->mdConf->objectRule[$index]->mdPoint[1]->dataInfo['PosY']['value']."\r\n";
// 		echo 'area'.($index).'_2x='.$classInstances['VAConfiguration']->mdConf->objectRule[$index]->mdPoint[2]->dataInfo['PosX']['value']."\r\n";
// 		echo 'area'.($index).'_2y='.$classInstances['VAConfiguration']->mdConf->objectRule[$index]->mdPoint[2]->dataInfo['PosY']['value']."\r\n";
// 		echo 'area'.($index).'_3x='.$classInstances['VAConfiguration']->mdConf->objectRule[$index]->mdPoint[3]->dataInfo['PosX']['value']."\r\n";
// 		echo 'area'.($index).'_3y='.$classInstances['VAConfiguration']->mdConf->objectRule[$index]->mdPoint[3]->dataInfo['PosY']['value']."\r\n";
		
			echo 'area'.($index).'_left='. $classInstances['VAConfiguration']->mdConf->objectRule[$index]->mdPoint[0]->dataInfo['PosX']['value']."\r\n";
// 		echo 'area'.($index).'_top='. $classInstances['VAConfiguration']->mdConf->objectRule[$index]->mdPoint[0]->dataInfo['PosY']['value']."\r\n";
			echo 'area'.($index).'_right='. $classInstances['VAConfiguration']->mdConf->objectRule[$index]->mdPoint[1]->dataInfo['PosX']['value']."\r\n";
			echo 'area'.($index).'_top='. $classInstances['VAConfiguration']->mdConf->objectRule[$index]->mdPoint[1]->dataInfo['PosY']['value']."\r\n";
// 		echo 'area'.($index).'_right='.$classInstances['VAConfiguration']->mdConf->objectRule[$index]->mdPoint[2]->dataInfo['PosX']['value']."\r\n";
			echo 'area'.($index).'_bottom='.$classInstances['VAConfiguration']->mdConf->objectRule[$index]->mdPoint[2]->dataInfo['PosY']['value']."\r\n";
// 		echo 'area'.($index).'_left='.$classInstances['VAConfiguration']->mdConf->objectRule[$index]->mdPoint[3]->dataInfo['PosX']['value']."\r\n";
// 		echo 'area'.($index).'_bottom='.$classInstances['VAConfiguration']->mdConf->objectRule[$index]->mdPoint[3]->dataInfo['PosY']['value']."\r\n";
			echo 'area'.($index).'_sensitivity='. ($classInstances['VAConfiguration']->mdConf->dataInfo['Sensitivity']['value']+1)."\r\n";		
		}
	}else if($model == "SNO-L6013RS1" || $model == "SND-L6013RS1"){
		for ($index=0; $index<4; ++$index) {		
			echo 'area'.($index).'_left='. $classInstances['VAConfiguration']->mdConf->objectRule[$index]->mdPoint[0]->dataInfo['PosX']['value']."\r\n";
			echo 'area'.($index).'_right='. $classInstances['VAConfiguration']->mdConf->objectRule[$index]->mdPoint[1]->dataInfo['PosX']['value']."\r\n";
			echo 'area'.($index).'_top='. $classInstances['VAConfiguration']->mdConf->objectRule[$index]->mdPoint[0]->dataInfo['PosY']['value']."\r\n";
			echo 'area'.($index).'_bottom='.$classInstances['VAConfiguration']->mdConf->objectRule[$index]->mdPoint[1]->dataInfo['PosY']['value']."\r\n";
			echo 'area'.($index).'_sensitivity='. ($classInstances['VAConfiguration']->mdConf->dataInfo['Sensitivity']['value']+1)."\r\n";	
			}
	}
	exit;
}

//function cgi_motion()
function ApplyMotion()
{
	$model = $_SERVER['MODELNAME'];
	$classInstances= GetClassInstance('va');
	
	for ($index=0; $index<8; ++$index) {
		$classInstances['VAConfiguration']->mdConf->objectRule[$index]->InitData();
		$classInstances['VAConfiguration']->mdConf->objectRule[$index]->SetPayload();
	}
	
	$sens = $_GET['area0_sensitivity'];
	if( $sens != NULL){
		$value = $sens;
		$classInstances['VAConfiguration']->mdConf->dataInfo['Sensitivity']['value'] = $value-1;
		if(CheckModelName('All7002') || CheckModelName('MEGA') || CheckModelName('All7000') || CheckModelName('All6004')){
			$classInstances['VAConfiguration']->ivConf->dataInfo['Sensitivity']['value'] = $value-1;
		}
	}
	$sens = $_GET['area1_sensitivity'];
	if( $sens != NULL){
		$value = $sens;
		$classInstances['VAConfiguration']->mdConf->dataInfo['Sensitivity']['value'] = $value-1;
		if(CheckModelName('All7002') || CheckModelName('MEGA') || CheckModelName('All7000') || CheckModelName('All6004')){
			$classInstances['VAConfiguration']->ivConf->dataInfo['Sensitivity']['value'] = $value-1;
		}
	}
	$sens = $_GET['area2_sensitivity'];
	if( $sens != NULL){
		$value = $sens;
		$classInstances['VAConfiguration']->mdConf->dataInfo['Sensitivity']['value'] = $value-1;
		if(CheckModelName('All7002') || CheckModelName('MEGA') || CheckModelName('All7000') || CheckModelName('All6004')){
			$classInstances['VAConfiguration']->ivConf->dataInfo['Sensitivity']['value'] = $value-1;
		}
	}
	$sens = $_GET['area3_sensitivity'];
	if( $sens != NULL){
		$value = $sens;
		$classInstances['VAConfiguration']->mdConf->dataInfo['Sensitivity']['value'] = $value-1;
		if(CheckModelName('All7002') || CheckModelName('MEGA') || CheckModelName('All7000') || CheckModelName('All6004')){
			$classInstances['VAConfiguration']->ivConf->dataInfo['Sensitivity']['value'] = $value-1;
		}
	}
	
	$area0_left = $_GET['area0_left'];
	$area0_right = $_GET['area0_right'];
	$area0_top = $_GET['area0_top'];
	$area0_bottom = $_GET['area0_bottom'];
	
	if( $area0_left != NULL){
		$areaIndex = 0;
		if($area0_right >= 1920){
			$area0_right = 1920 -1;
		}
		if($area0_bottom >= 1080){
			$area0_bottom = 1080 -1;
		}
		
		$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->dataInfo['NumPoint']['value'] = 2;
		$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->dataInfo['Index']['value'] = $areaIndex;
		$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[0]->dataInfo['PosX']['value'] = $area0_left;
		$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[0]->dataInfo['PosY']['value'] = $area0_top;
		$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[1]->dataInfo['PosX']['value'] = $area0_right;
		$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[1]->dataInfo['PosY']['value'] = $area0_bottom;
		if (CheckModelName('All6004') ){
			$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->dataInfo['NumPoint']['value'] = 4;
			$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[2]->dataInfo['PosX']['value'] = $area0_right;
			$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[2]->dataInfo['PosY']['value'] = $area0_bottom;
			$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[3]->dataInfo['PosX']['value'] = $area0_left;
			$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[3]->dataInfo['PosY']['value'] = $area0_bottom;
		
			$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[2]->payload = MakePayload($classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[2]->dataInfo);
			$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[3]->payload = MakePayload($classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[3]->dataInfo);
		}
		$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[0]->payload = MakePayload($classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[0]->dataInfo);
		$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[1]->payload = MakePayload($classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[1]->dataInfo);
		$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->SetPayload();
	}
	
	$area1_left = $_GET['area1_left'];
	$area1_right = $_GET['area1_right'];
	$area1_top = $_GET['area1_top'];
	$area1_bottom = $_GET['area1_bottom'];
	
	if( $area1_left != NULL){
		$areaIndex = 1;
		
		if($area1_right >= 1920){
			$area1_right = 1920 -1;
		}
		if($area1_bottom >= 1080){
			$area1_bottom = 1080 -1;
		}
		
		$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->dataInfo['NumPoint']['value'] = 2;
		$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->dataInfo['Index']['value'] = $areaIndex;
		$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[0]->dataInfo['PosX']['value'] = $area1_left;
		$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[0]->dataInfo['PosY']['value'] = $area1_top;
		$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[1]->dataInfo['PosX']['value'] = $area1_right;
		$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[1]->dataInfo['PosY']['value'] = $area1_bottom;
		if (CheckModelName('All6004') ){
			$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->dataInfo['NumPoint']['value'] = 4;
			$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[2]->dataInfo['PosX']['value'] = $area1_right;
			$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[2]->dataInfo['PosY']['value'] = $area1_bottom;
			$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[3]->dataInfo['PosX']['value'] = $area1_left;
			$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[3]->dataInfo['PosY']['value'] = $area1_bottom;

			$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[2]->payload = MakePayload($classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[2]->dataInfo);
			$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[3]->payload = MakePayload($classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[3]->dataInfo);
		}
		$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[0]->payload = MakePayload($classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[0]->dataInfo);
		$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[1]->payload = MakePayload($classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[1]->dataInfo);
		$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->SetPayload();
	}

	$area2_left = $_GET['area2_left'];
	$area2_right = $_GET['area2_right'];
	$area2_top = $_GET['area2_top'];
	$area2_bottom = $_GET['area2_bottom'];
	
	if( $area2_left != NULL){
		$areaIndex = 2;
		
		if($area2_right >= 1920){
			$area2_right = 1920 -1;
		}
		if($area2_bottom >= 1080){
			$area2_bottom = 1080 -1;
		}
		
		$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->dataInfo['NumPoint']['value'] = 2;
		$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->dataInfo['Index']['value'] = $areaIndex;
		$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[0]->dataInfo['PosX']['value'] = $area2_left;
		$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[0]->dataInfo['PosY']['value'] = $area2_top;
		$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[1]->dataInfo['PosX']['value'] = $area2_right;
		$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[1]->dataInfo['PosY']['value'] = $area2_bottom;
		if (CheckModelName('All6004') ){
			$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->dataInfo['NumPoint']['value'] = 4;
			$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[2]->dataInfo['PosX']['value'] = $area2_right;
			$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[2]->dataInfo['PosY']['value'] = $area2_bottom;
			$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[3]->dataInfo['PosX']['value'] = $area2_left;
			$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[3]->dataInfo['PosY']['value'] = $area2_bottom;

			$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[2]->payload = MakePayload($classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[2]->dataInfo);
			$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[3]->payload = MakePayload($classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[3]->dataInfo);
		}
		$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[0]->payload = MakePayload($classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[0]->dataInfo);
		$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[1]->payload = MakePayload($classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[1]->dataInfo);
		$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->SetPayload();
	}
	
	$area3_left = $_GET['area3_left'];
	$area3_right = $_GET['area3_right'];
	$area3_top = $_GET['area3_top'];
	$area3_bottom = $_GET['area3_bottom'];
	
	if( $area3_left != NULL){
		$areaIndex = 3;
		
		if($area3_right >= 1920){
			$area3_right = 1920 -1;
		}
		if($area3_bottom >= 1080){
			$area3_bottom = 1080 -1;
		}
		
		$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->dataInfo['NumPoint']['value'] = 2;
		$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->dataInfo['Index']['value'] = $areaIndex;
		$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[0]->dataInfo['PosX']['value'] = $area3_left;
		$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[0]->dataInfo['PosY']['value'] = $area3_top;
		$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[1]->dataInfo['PosX']['value'] = $area3_right;
		$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[1]->dataInfo['PosY']['value'] = $area3_bottom;
		if (CheckModelName('All6004') ){
			$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->dataInfo['NumPoint']['value'] = 4;
			$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[2]->dataInfo['PosX']['value'] = $area3_right;
			$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[2]->dataInfo['PosY']['value'] = $area3_bottom;
			$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[3]->dataInfo['PosX']['value'] = $area3_left;
			$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[3]->dataInfo['PosY']['value'] = $area3_bottom;

			$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[2]->payload = MakePayload($classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[2]->dataInfo);
			$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[3]->payload = MakePayload($classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[3]->dataInfo);
		}
		$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[0]->payload = MakePayload($classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[0]->dataInfo);
		$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[1]->payload = MakePayload($classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->mdPoint[1]->dataInfo);
		$classInstances['VAConfiguration']->mdConf->objectRule[$areaIndex]->SetPayload();
	}
	
	SetEventSchedule($classInstances['VAConfiguration']->mdConf->schedule);
	SetEventAction($classInstances['VAConfiguration']->mdConf->action);
	
	if($area0_left == NULL && $area1_left == NULL && $area2_left == NULL && $area3_left == NULL){
		//area default
		$classInstances['VAConfiguration']->mdConf->dataInfo['Enabled']['value'] = 0;
		$classInstances['VAConfiguration']->ivConf->dataInfo['Enabled']['value'] = 0;
		for ($index=0; $index<8; ++$index) {
			$classInstances['VAConfiguration']->mdConf->objectRule[$index]->InitData();
			$classInstances['VAConfiguration']->mdConf->objectRule[$index]->SetPayload();
		}
	}
	
	if( $_GET['area0_left'] != NULL && $area0_left == 0 && $area0_right == 0 && $area0_top == 0 && $area0_bottom == 0 ){
		$classInstances['VAConfiguration']->mdConf->objectRule[0]->InitData();
		$classInstances['VAConfiguration']->mdConf->objectRule[0]->SetPayload();
	}
	
	if( $_GET['area1_left'] != NULL && $area1_left == 0 && $area1_right == 0 && $area1_top == 0 && $area1_bottom == 0 ){
		$classInstances['VAConfiguration']->mdConf->objectRule[1]->InitData();
		$classInstances['VAConfiguration']->mdConf->objectRule[1]->SetPayload();
	}
	
	if( $_GET['area2_left'] != NULL && $area2_left == 0 && $area2_right == 0 && $area2_top == 0 && $area2_bottom == 0 ){
		$classInstances['VAConfiguration']->mdConf->objectRule[2]->InitData();
		$classInstances['VAConfiguration']->mdConf->objectRule[2]->SetPayload();
	}
	
	if( $_GET['area3_left'] != NULL && $area3_left == 0 && $area3_right == 0 && $area3_top == 0 && $area3_bottom == 0 ){
		$classInstances['VAConfiguration']->mdConf->objectRule[3]->InitData();
		$classInstances['VAConfiguration']->mdConf->objectRule[3]->SetPayload();
	}
	
	if($model == "SNB-6004" || $model == "VDR-10001" || $model == "VBR-10003"){
		for ($idx=0; $idx<4; ++$idx){
			if( $classInstances['VAConfiguration']->mdConf->objectRule[$idx]->mdPoint[0]->dataInfo['PosX']['value'] == 0 && 
					$classInstances['VAConfiguration']->mdConf->objectRule[$idx]->mdPoint[1]->dataInfo['PosX']['value'] == 0 &&
					$classInstances['VAConfiguration']->mdConf->objectRule[$idx]->mdPoint[1]->dataInfo['PosY']['value'] == 0 && 
					$classInstances['VAConfiguration']->mdConf->objectRule[$idx]->mdPoint[2]->dataInfo['PosY']['value'] == 0){
				$classInstances['VAConfiguration']->mdConf->dataInfo['Enabled']['value'] = 0;
				$classInstances['VAConfiguration']->ivConf->dataInfo['Enabled']['value'] = 0;
			}else{
				$classInstances['VAConfiguration']->mdConf->dataInfo['Enabled']['value'] = 1;
				$classInstances['VAConfiguration']->ivConf->dataInfo['Enabled']['value'] = 1;
				break;
			}
		}
	}else if($model == "SNO-L6013RS1" || $model == "SND-L6013RS1"){
		for ($idx=0; $idx<4; ++$idx){
			if( $classInstances['VAConfiguration']->mdConf->objectRule[$idx]->mdPoint[0]->dataInfo['PosX']['value'] == 0 && 
					$classInstances['VAConfiguration']->mdConf->objectRule[$idx]->mdPoint[1]->dataInfo['PosX']['value'] == 0 &&
					$classInstances['VAConfiguration']->mdConf->objectRule[$idx]->mdPoint[0]->dataInfo['PosY']['value'] == 0 && 
					$classInstances['VAConfiguration']->mdConf->objectRule[$idx]->mdPoint[1]->dataInfo['PosY']['value'] == 0){
				$classInstances['VAConfiguration']->mdConf->dataInfo['Enabled']['value'] = 0;
				$classInstances['VAConfiguration']->ivConf->dataInfo['Enabled']['value'] = 0;
			}else{
				$classInstances['VAConfiguration']->mdConf->dataInfo['Enabled']['value'] = 1;
				$classInstances['VAConfiguration']->ivConf->dataInfo['Enabled']['value'] = 1;
				break;
			}
		}
	}
	
	if(CheckModelName('All7002') || CheckModelName('MEGA') || CheckModelName('All7000') || CheckModelName('All6004'))
	{
		SetEventSchedule($classInstances['VAConfiguration']->ivConf->schedule);
		SetEventAction($classInstances['VAConfiguration']->ivConf->action);
		$classInstances['VAConfiguration']->mdConf->SetPayload();
		$classInstances['VAConfiguration']->ivConf->SetPayload();
		$classInstances['VAConfiguration']->SetPayload();
		$classInstances['VAConfiguration']->headerInfo['Action'] = ACTION_SET;
		$GLOBALS['SOCKET_MANAGER']->Connection($classInstances['VAConfiguration']);
		return TRUE;
	}else{
		$classInstances['VAConfiguration']->mdConf->SetPayload();
		$classInstances['VAConfiguration']->mdConf->headerInfo['Action'] = ACTION_SET;
		$GLOBALS['SOCKET_MANAGER']->Connection($classInstances['VAConfiguration']->mdConf);
		return TRUE;
	}
	
	
}

function ViewPTZPresetVAMD()
{
	$model = $_SERVER['MODELNAME'];

	 if($model == "SNO-L6013RS1" || $model == "SND-L6013RS1")
	{
		ResponseText(FALSE);
	}
	exit;
}

function ApplyPTZPresetVAMD()
{
	$model = $_SERVER['MODELNAME'];
	
	 if($model == "SNO-L6013RS1" || $model == "SND-L6013RS1")
	 {
	 	ResponseText(FALSE);
	 }
	exit;
}

function ViewMirrorCapability(){
	$model = $_SERVER['MODELNAME'];

	header("Content-Type: text/plain");

	if($model == "SNP-6200" || $model == "SNP-6200H") {
		echo "vertical=0"."\r\n";
		echo "horizontal=0"."\r\n";
		echo "flip=1";
		exit;

	}else if($model == "SNB-6004" || $model == "VDR-10001" || $model == "VBR-10003" || $model == "SNO-L6013RS1" || $model == "SND-L6013RS1" || $model == "SND-L6013R" || $model == "SNO-L6013R"){
		echo "vertical=1"."\r\n";
		echo "horizontal=1"."\r\n";
		echo "flip=1";
		exit;
	}else {
		echo "vertical=1"."\r\n";
		echo "horizontal=1"."\r\n";
		echo "flip=1";
		exit;
	}
}

// function cgi_camera()
function ApplyCamera()
{
	$classInstances= GetClassInstance('cgi_image');
	$videoSrcConf		= $classInstances['videosource'];
	
	$digital_flip = $_GET['mode'];
	
	if( $digital_flip != NULL){
		$value = $digital_flip;
		
		if($value == 'flip'){
			$classInstances['VideoSource']->dataInfo['Mirror']['value'] = 1;
			$classInstances['VideoSource']->dataInfo['Flip']['value'] = 1;
		}else if($value == 'none'){
			$classInstances['VideoSource']->dataInfo['Mirror']['value'] = 0;
			$classInstances['VideoSource']->dataInfo['Flip']['value'] = 0;
		}else if($value == 'vert'){
			$classInstances['VideoSource']->dataInfo['Mirror']['value'] = 0;
			$classInstances['VideoSource']->dataInfo['Flip']['value'] = 1;
		}else if($value == 'hori'){
			$classInstances['VideoSource']->dataInfo['Mirror']['value'] = 1;
			$classInstances['VideoSource']->dataInfo['Flip']['value'] = 0;
		}else{
			return FALSE;
		}
		
		$classInstances['VideoSource']->payload = MakePayload($classInstances['VideoSource']->dataInfo);
		$classInstances['VideoSource']->headerInfo['Action'] 	= ACTION_SET;
		$GLOBALS['SOCKET_MANAGER']->Connection($classInstances['VideoSource']);
		
		return TRUE;
	}
	
}

// function cgi_camera()
function ViewCamera(){
	
	$classInstances= GetClassInstance('cgi_image');
	
	$hflip =	$classInstances['VideoSource']->dataInfo['Mirror']['value'];
	$vflip = $classInstances['VideoSource']->dataInfo['Flip']['value'];
	
	header("Content-Type: text/plain");
	
	if( $hflip == 1 && $vflip == 1 ){
		echo 'mode=flip';
	}else if( $hflip == 0 && $vflip == 1 ){
		echo 'mode=vert';
	}else if( $hflip == 1 && $vflip == 0 ){
		echo 'mode=hori';
	}else if( $hflip == 0 && $vflip == 0 ){
		echo 'mode=none';
	}else{
		ResponseText(FALSE);
	}
}

function ViewOnePushFocusCapability()
{
	$model = $_SERVER['MODELNAME'];
	header("Content-Type: text/plain");

	if($model == "SNO-L6013RS1" || $model == "SND-L6013RS1") {
		echo "onepush=0";
	}else if($model == "SNB-6400" || $model == "VDR-10001" || $model == "VBR-10003"){
		echo "onepush=1";
	}else{
		echo "onepush=1";
	}
}

// function cgi_focus()
function ApplyFocus()
{
	
	require_once ('./adv/ptzmove.class');
	$model = $_SERVER['MODELNAME'];

	 if($model == "SNO-L6013RS1" || $model == "SND-L6013RS1")
	 {
	 	ResponseText(FALSE);
	 	exit;
	 }
	
	
	$focusConf = new MotorizedLensSetup();
	
	$focusConf->dataInfo['Mode']['value'] = 2;
	$focusConf->dataInfo['AF']['value'] = 1;
	
	$focusConf->ptzPosition->payload = MakePayload($focusConf->ptzPosition->dataInfo);
	$focusConf->SetPayload();
	$GLOBALS['SOCKET_MANAGER'] = new SocketManager();
	$GLOBALS['SOCKET_MANAGER']->Connection($focusConf);
	return TRUE;
}

//--------------------------부속함수들
// event schedule
function SetEventSchedule(&$_eventSchedule)
{
	$dayArr = array('SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT');
	$isDayMatch = FALSE;
	for ($index=0; $index<7; ++$index) {
		if (isset($_REQUEST[$dayArr[$index]])) {
			if (isset($_REQUEST['active'])) {
				if ($_REQUEST['active'] == 'always') 	ResponseText(FALSE);
			}
			else {
				if($_eventSchedule->enabled == 0) ResponseText(FALSE);
			}
			if ($_REQUEST[$dayArr[$index]] != 0 && $_REQUEST[$dayArr[$index]] !=1) ResponseText(FALSE);
			for ($index2=0; $index2<24; ++$index2) {
				if ($_REQUEST[$dayArr[$index]] == 0) {
					$_eventSchedule->dayTime[$index]->time[$index2] = 0;
				}
				else {
					if (isset($_REQUEST[$dayArr[$index].$index2])) {
						$timeValue = $_REQUEST[$dayArr[$index].$index2];
						$regexp = "/^([\d]{1,2})+([,][\d]{1,2})*$/";

						if(preg_match($regexp, $timeValue)){					//MON19=1 or MON19=10,50
							$regexp2 = "/^[\d]{1,2}$/";
							if(preg_match($regexp2, $timeValue)){				//parameter format : 1number, ex)"0"
								if ($timeValue != 0 && $timeValue != 1) 	ResponseText(FALSE);
								$_eventSchedule->dayTime[$index]->time[$index2] = $timeValue;
								$_eventSchedule->dayDetail[$index]->detailTime[$index2]->dataInfo['isEnabled']['value'] = 0;
								$_eventSchedule->dayDetail[$index]->detailTime[$index2]->dataInfo['from']['value'] = 0;
								$_eventSchedule->dayDetail[$index]->detailTime[$index2]->dataInfo['to']['value'] = 59;
							}
							else{										//parameter format : 2number, ex)"10,40"
								$tempValue = split(",", $timeValue);			//tempValue[0] : Minute From, tempValue[1] : Minute To
								if (($tempValue[0] < 0 || $tempValue[0] > 59)) 	ResponseText(FALSE);
								if (($tempValue[1] < 0 || $tempValue[1] > 59)) 	ResponseText(FALSE);
								if($tempValue[0] > $tempValue[1])					ResponseText(FALSE);

								$_eventSchedule->dayTime[$index]->time[$index2] = 1;
								if($tempValue[0] == 0 && $tempValue[1] == 59)
									$_eventSchedule->dayDetail[$index]->detailTime[$index2]->dataInfo['isEnabled']['value'] = 0;
								else
									$_eventSchedule->dayDetail[$index]->detailTime[$index2]->dataInfo['isEnabled']['value'] = 1;
								$_eventSchedule->dayDetail[$index]->detailTime[$index2]->dataInfo['from']['value'] = $tempValue[0];
								$_eventSchedule->dayDetail[$index]->detailTime[$index2]->dataInfo['to']['value'] = $tempValue[1];
							}
							$isDayMatch = TRUE;
						}
						else{
							$isDayMatch = FALSE;
						}
					}
				}
			}
			if ($isDayMatch == FALSE) ResponseText(FALSE);
		}
		else {
			for ($index2=0; $index2<24; ++$index2)
				if (isset($_REQUEST[$dayArr[$index].$index2]))	ResponseText(FALSE);
		}
		$isDayMatch = FALSE;
		$_eventSchedule->dayTime[$index]->SetPayload();
		$_eventSchedule->dayDetail[$index]->SetPayload();
	}

	if (isset($_REQUEST['active'])) {
		if ($_REQUEST['active'] != 'always' && $_REQUEST['active'] != 'schedule')	ResponseText(FALSE);
		$_eventSchedule->enabled = ($_REQUEST['active']=='always'? 0 : 1);
	}
	$_eventSchedule->SetPayload();
}

// event action
function SetEventAction(&$_actionConf)
{
	$isSchedule = 0;
	if ($_REQUEST['msubmenu'] == 'schedule') $isSchedule = 1;
	foreach($_REQUEST as $name=>$value) {
		switch($name) {
			case 'output_dur':	 case 'output_dur2':{
				if (CheckModelName('NO_OUTPUT') || $_REQUEST['msubmenu'] == 'schedule') ResponseText(FALSE);
				//if (isset($_REQUEST['output_dur2']) && !CheckModelName('ALARM_OUTPUT_2'))	ResponseText(FALSE);
				if ($value != '0' && $value != '-1' && $value != '5' && $value != '10' && $value != '15') ResponseText(FALSE);
				if ($value == 'always') $value = -1;
				else if ($value == 'five') $value = 5;
				$outputIndex = 0;
				if ($name == 'output_dur2') $outputIndex = 1;
				$_actionConf->relayOutput[$outputIndex] = $value;
			}	break;
			case 'smtp_sending':	case 'record': case 'ftp_sending': {
				if ($name == 'record' && CheckModelName('NO_RECORD'))	ResponseText(FALSE);
				if ($name == 'record' && ($isSchedule == 1 && CheckModelName('All7002'))) ResponseText(FALSE);
				if (($name == 'smtp_sending') && ($_REQUEST['msubmenu'] == 'schedule'))	ResponseText(FALSE);
				if (($name == 'smtp_sending' || $name == 'ftp_sending') && ($_REQUEST['msubmenu'] == 'network_event'))	ResponseText(FALSE);
				$dataNameList = array('smtp_sending'=>'SMTPSending', 'record'=>'Record', 'ftp_sending'=>'FTPSending');
				if ($value != 0 && $value != 1)	ResponseText(FALSE);
				$_actionConf->dataInfo[$dataNameList[$name]]['value'] = $value;
			} 	break;
			case 'gotoPreset': {
				if ($_REQUEST['msubmenu'] == 'schedule') ResponseText(FALSE);
				if (!CheckModelName('PRESET_128'))	ResponseText(FALSE);
				if (CheckModelName('PRESET_128'))	 {
					if($value < 0 || $value > 128)
						ResponseText(FALSE);
				}
				else {
					if ($value < 0 || $value > 12)	ResponseText(FALSE);
				}
				$_actionConf->dataInfo['GotoPreset']['value'] = $value;
			}	break;
		}
	}
	$_actionConf->SetPayload();
}

?>
