<?php
require_once ('./adv/_define.inc');

function camera_capability() {
	$cameraInfo = array( 'sensor_mode'	=>array('type'=>'enum', 'entry'=>array('60fps'=>'60', '50fps'=>'50', '30fps'=>'30', '25fps'=>'25'), 'dependency'=>'false'),
								'ssdr' 			=>array('type'=>'enum', 'entry'=>array('Off'=>'0', 'On'=>'1'), 'dependency'=>'false'),
								'ssdr_level' 	=>array('type'=>'int', 'entry'=>array('min'=>'1', 'max'=>'15'), 'dependency'=>'false'),
								'ssdr_drange' 	=>array('type'=>'enum', 'entry'=>array('Wide'=>'0', 'Narrow'=>'1'), 'dependency'=>'false'),
								'wb' 				=>array('type'=>'enum', 'entry'=>array('ATW'=>'0', 'Manual'=>'1', 'AWC'=>'2', 'Outdoor'=>'3', 'Indoor'=>'4'), 'dependency'=>'false'),
								'wb_red' 		=>array('type'=>'int', 'entry'=>array('min'=>'1', 'max'=>'1024'), 'dependency'=>'true'),
								'wb_blue' 		=>array('type'=>'int', 'entry'=>array('min'=>'1', 'max'=>'1024'), 'dependency'=>'true'),
								'blc' 			=>array('type'=>'enum', 'entry'=>array('Off'=>'0', 'On'=>'1'), 'dependency'=>'false'),
								'blc_level' 	=>array('type'=>'enum', 'entry'=>array('Low'=>'0', 'Middle'=>'1', 'High'=>'2'), 'dependency'=>'false'),
								'blc_top' 		=>array('type'=>'int', 'entry'=>array('min'=>'0', 'max'=>'60'), 'dependency'=>'false'),
								'blc_bottom' 	=>array('type'=>'int', 'entry'=>array('min'=>'40', 'max'=>'100'), 'dependency'=>'false'),
								'blc_left' 		=>array('type'=>'int', 'entry'=>array('min'=>'0', 'max'=>'60'), 'dependency'=>'false'),
								'blc_right' 	=>array('type'=>'int', 'entry'=>array('min'=>'40', 'max'=>'100'), 'dependency'=>'false'),
								'wdr' 			=>array('type'=>'enum', 'entry'=>array('Off'=>'0', 'On'=>'1'), 'dependency'=>'false'),
								'wdr_level' 	=>array('type'=>'enum', 'entry'=>array('Low'=>'0', 'Middle'=>'1', 'High'=>'2'), 'dependency'=>'false'),
								'brightness' 	=>array('type'=>'int', 'entry'=>array('min'=>'1', 'max'=>'100'), 'dependency'=>'false'),
								'iris' 			=>array('type'=>'enum', 'entry'=>array('Auto'=>'0', 'Manual'=>'1', 'P-Iris'=>'2'), 'dependency'=>'false'),
								'p-iris' 		=>array('type'=>'enum', 'entry'=>array('Auto'=>'0', 'Manual'=>'1'), 'dependency'=>'true'),
								'p-iris_pos' 	=>array('type'=>'int', 'entry'=>array('min'=>'1', 'max'=>'100'), 'dependency'=>'true'),
								'shutter_min' 	=>array('type'=>'enum', 'entry'=>array('2'=>'0', '1'=>'1', '1/2'=>'2', '1/4'=>'3', '1/5'=>'4', '1/8'=>'5', '1/15'=>'6', '1/25'=>'7', '1/30'=>'8', '1/50' => '9', '1/60'=>'10', '1/100'=>'11', '1/120'=>'12', '1/150'=>'13', '1/180'=>'14', '1/200'=>'15', '1/240'=>'16', '1/250'=>'17', '1/300'=>'18', '1/360'=>'19','1/480'=>'20','1/500'=>'21',  '1/600'=>'22', '1/700'=>'23', '1/1000'=>'24', '1/1500'=>'25', '1/2500'=>'26', '1/5000'=>'27', '1/10000'=>'28', '1/12000'=>'29' ), 'dependency'=>'false'),
								'shutter_max' 	=>array('type'=>'enum', 'entry'=>array('2'=>'0', '1'=>'1', '1/2'=>'2', '1/4'=>'3', '1/5'=>'4', '1/8'=>'5', '1/15'=>'6', '1/25'=>'7', '1/30'=>'8', '1/50' => '9', '1/60'=>'10', '1/100'=>'11', '1/120'=>'12', '1/150'=>'13', '1/180'=>'14', '1/200'=>'15', '1/240'=>'16', '1/250'=>'17', '1/300'=>'18', '1/360'=>'19','1/480'=>'20','1/500'=>'21',  '1/600'=>'22', '1/700'=>'23', '1/1000'=>'24', '1/1500'=>'25', '1/2500'=>'26', '1/5000'=>'27', '1/10000'=>'28', '1/12000'=>'29' ), 'dependency'=>'false'),
								'aflk'			=>array('type'=>'int', 'entry'=>array('min'=>'1', 'max'=>'100'), 'dependency'=>'false'),
								'ssnr' 			=>array('type'=>'enum', 'entry'=>array('Off'=>'0', 'On'=>'1'), 'dependency'=>'false'),
								'ssnr_level' 	=>array('type'=>'int', 'entry'=>array('min'=>'0', 'max'=>'16'), 'dependency'=>'false'),
								'agc' 			=>array('type'=>'enum', 'entry'=>array('Off'=>'0', 'Low'=>'1', 'Middle'=>'2', 'High'=>'3'), 'dependency'=>'false'),
								'daynight' 		=>array('type'=>'enum', 'entry'=>array('Color'=>'0', 'B/W'=>'1', 'Auto'=>'2', 'External B/W'=>'3'), 'dependency'=>'true'),
								'dwell_time'	=>array('type'=>'enum', 'entry'=>array('5sec'=>'5', '7sec'=>'7', '10sec'=>'10', '20sec'=>'20', '30sec'=>'30', '40sec'=>'40', '60sec'=>'60'), 'dependency'=>'true'),
								'simple_focus'	=>array('type'=>'enum', 'entry'=>array('Off'=>'0', 'On'=>'1'), 'dependency'=>'false'),
								'duration'		=>array('type'=>'enum', 'entry'=>array('Fast'=>'0', 'Slow'=>'1'), 'dependency'=>'true'),
								'sharpness'		=>array('type'=>'enum', 'entry'=>array('Off'=>'0', 'On'=>'1'), 'dependency'=>'false'),
								'sharpness_level'	=>array('type'=>'int', 'entry'=>array('min'=>'1', 'max'=>'32'), 'dependency'=>'false'),
								'gamma'			=>array('type'=>'enum', 'entry'=>array('0.2'=>'0', '0.25'=>'1', '0.3'=>'2', '0.35'=>'3', '0.4'=>'4', '0.45'=>'5', '0.5'=>'6', '0.55'=>'7', '0.6'=>'8', '0.65'=>'9', '0.7'=>'10', '0.75'=>'11', '0.8'=>'12', '0.85'=>'13', '0.9'=>'14', '0.95'=>'15', '1'=>'16'), 'dependency'=>'false'),
								'saturation' 	=>array('type'=>'int', 'entry'=>array('min'=>'1', 'max'=>'100'), 'dependency'=>'false'),
								'alarm_in'	 	=>array('type'=>'enum', 'entry'=>array('Open:Color/Close:BW'=>'0', 'Open:BW/Close:Color'=>'1'), 'dependency'=>'true'),
								'defog'			=>array('type'=>'enum', 'entry'=>array('Off'=>'0', 'On'=>'1'), 'dependency'=>'false'),
								'defog_level'	=>array('type'=>'int', 'entry'=>array('min'=>'1', 'max'=>'10'), 'dependency'=>'false'),
								'camera_title_mode'=>array('type'=>'enum', 'entry'=>array('Off'=>'0', 'On'=>'1'), 'dependency'=>'false'),
								'camera_title'	=>array('type'=>'string', 'entry'=>array('length'=>'15'), 'dependency'=>'false'),
								'camera_title_posX'=>array('type'=>'int', 'entry'=>array('min'=>'1', 'max'=>'55'), 'dependency'=>'false'),
								'camera_title_posY'=>array('type'=>'int', 'entry'=>array('min'=>'1', 'max'=>'20'), 'dependency'=>'false'),
								'time_display'	=>array('type'=>'enum', 'entry'=>array('Off'=>'0', 'On'=>'1'), 'dependency'=>'false'),
								'time_display_format'=>array('type'=>'enum', 'entry'=>array('YYYY-MM-DD'=>'0', 'MM-DD-YYYY'=>'1', 'DD-MM-YYYY'=>'2'), 'dependency'=>'false'),
								'time_posX'		=>array('type'=>'int', 'entry'=>array('min'=>'1', 'max'=>'37'), 'dependency'=>'true'),
								'time_posY'		=>array('type'=>'int', 'entry'=>array('min'=>'1', 'max'=>'20'), 'dependency'=>'false'),
								'osd_size'		=>array('type'=>'enum', 'entry'=>array('Small'=>'0', 'Medium'=>'1', 'Large'=>'2'), 'dependency'=>'false'),
								'hflip'			=>array('type'=>'enum', 'entry'=>array('Off'=>'0', 'On'=>'1'), 'dependency'=>'false'),
								'vflip'			=>array('type'=>'enum', 'entry'=>array('Off'=>'0', 'On'=>'1'), 'dependency'=>'false'),
								'video_type'	=>array('type'=>'enum', 'entry'=>array('Off'=>'0', 'On'=>'1'), 'dependency'=>'false'),
								'video_output'	=>array('type'=>'enum', 'entry'=>array('Off'=>'0', 'On'=>'1'), 'dependency'=>'false'));


	function check_dependency($name, $entry, $dependency) {

		if ($name == 'wb_red' || $name == 'wb_blue'){
			$parameterName = 'wb';
			$parameterValue = 'Manual';
			$property= 'Use';
		}else if ($name == 'p-iris'){
			$parameterName = 'iris';
			$parameterValue = 'P-Iris';
			$property= 'Use';
		}else if ($name == 'p-iris_pos') {
			$parameterName = 'p-iris';
			$parameterValue = 'Manual';
			$property= 'Use';
		}else if ($name == 'daynight') {
			if ($entry != 2) $dependency = 'false';
			$parameterName = 'agc';
			$parameterValue = 'Off';
			$property= 'UnUse';
		}else if ($name == 'dwell_time' || $name == 'duration') {
			$parameterName = 'daynight';
			$parameterValue = 'Auto';
			$property= 'Use';
		}else if ($name == 'alarm_in') {
			$parameterName = 'daynight';
			$parameterValue = 'External B/W';
			$property= 'Use';
		}else if ($name == 'time_posX') {
			$parameterName = 'display_weekday';
			$parameterValue = 'On';
			$property= 'Change:33';
		}

		$msg = array ($dependency, $parameterName,$parameterValue,$property );

		return $msg;
	}

	$msg = "<camerasetup>"."\r\n";
	foreach($cameraInfo as $name=>$type) {
		$msg .= "\t"."<parameter name='".$name."'>"."\r\n";
		if ($type['type'] == 'enum') {
			$msg .="\t"."\t"."<type value='enum'>"."\r\n";
				foreach ($type['entry'] as $entry=>$value) {
					$msg .="\t"."\t"."\t"."<entry name='".$entry."' value='".$value."' " ;
					$depend = check_dependency($name, $value, $type['dependency']);
					if ($depend[0] == 'true') {
						$msg .= "dependency='".$depend[0]."' />"."\r\n";
						$msg .= "\t"."\t"."\t"."\t"."<dependency parameterName='".$depend[1]."' parameterValue='".$depend[2]."' property='".$depend[3]."/>"."\r\n";
					}else{
						$msg .= "dependency='".$depend[0]."' />"."\r\n";
					}
				$msg .="\t"."\t"."\t"."</entry>"."\r\n";
			}
		}
		else if ($type['type'] == 'int') {
			$msg .="\t"."\t"."<type value='int'>"."\r\n";
			foreach ($type['entry'] as $entry=>$value) {
				$msg .="\t"."\t"."\t"."<".$entry." value='".$value." '";
				$depend = check_dependency($name, $value, $type['dependency']);
				if ($depend[0] == 'true') {
					$msg .= "dependency='".$depend[0]."' />"."\r\n";
					$msg .= "\t"."\t"."\t"."\t"."<dependency parameterName='".$depend[1]."' parameterValue='".$depend[2]."' property='".$depend[3]."/>"."\r\n";
				}else{
					$msg .= "dependency='".$depend[0]."' />"."\r\n";
				}
				$msg .="\t"."\t"."\t"."</".$entry.">"."\r\n";

			}
		}
		else if ($type['type'] == 'string') {
			$msg .="\t"."\t"."<type value='int'>"."\r\n";
			foreach ($type['entry'] as $entry=>$value) {
				$msg .="\t"."\t"."\t"."<string length='".$value." '";
				$depend = check_dependency($name, $value, $type['dependency']);
				if ($depend[0] == 'true') {
					$msg .= "dependency='".$depend[0]."' />"."\r\n";
					$msg .= "\t"."\t"."\t"."\t"."<dependency parameterName='".$depend[1]."' parameterValue='".$depend[2]."' property='".$depend[3]."/>"."\r\n";
				}else{
					$msg .= "dependency='".$depend[0]."' />"."\r\n";
				}
				$msg .="\t"."\t"."\t"."</string>"."\r\n";

			}
		}

		$msg .="\t"."\t"."</type>"."\r\n";
		$msg .= "\t"."</parameter>"."\r\n";
	}
	$msg .= "</camerasetup>"."\r\n";
	return $msg;
}

switch(@$_REQUEST['msubmenu']) {
	case 'camera': {
		if ($_REQUEST['action'] != 'view') ResponseText(FALSE);
		$funcName = $_REQUEST['msubmenu'].'_capability';
		ResponseText($funcName());
	} break;
}
ResponseText(FALSE);
?>
