<?php
function PrintLeftMenu($path)
{
	$bas_menulist	= array('videoprofile','user','datetime','interface', 'eventsetup');
	$av_menulist 	= array('videosrc','audiosrc','camera', 'smartcodec', 'focus', 'ptzsetup');
	$ptz_menulist	= array('presetsetup', 'ptzsequence', 'ptzlimit', 'ptztrackingsetup', 'rs485');
	if ($GLOBALS['M_SPECIAL_TYPE'] == 1)
	{
		$net_menulist 	= array('ddns','ipfilter','ssl','8021x', 'qos', 'autoipconfig');
		//DEV_S1SMS
		//$eve_menulist 	= array('ftpemail', 'output', 'alarminput', 'timeschedule', 'tamperingdetection', 'videoanalytics', 'facedetection', 'audiodetection', 'networkdisconnect', 'ptztracking','appevent');
		$eve_menulist 	= array('ftpemail','storage', 'output', 'alarminput', 'timeschedule', 'tamperingdetection', 'videoanalytics', 'facedetection', 'audiodetection', 'networkdisconnect', 'ptztracking','appevent');
	}
	else
	{
		$net_menulist 	= array('ddns','ipfilter','ssl','8021x', 'qos', 'snmp', 'autoipconfig');
		$eve_menulist 	= array('ftpemail','storage', 'output', 'alarminput', 'timeschedule', 'tamperingdetection', 'videoanalytics', 'facedetection', 'audiodetection', 'networkdisconnect', 'ptztracking','appevent');
	}

	$sys_menulist 	= array('proinfo','upgrade','log','opensdk');

	if	(!$GLOBALS['M_SUPPORT_AUDIO'])				ArrayPop($av_menulist, 'audiosrc');
	if (!$GLOBALS['M_SUPPORT_SMARTCODEC'])		ArrayPop($av_menulist, 'smartcodec');
	if (!$GLOBALS['M_SUPPORT_MOTORIZE'])			ArrayPop($av_menulist, 'focus');
	if (!($GLOBALS['M_SUPPORT_EXTERNAL_PTZ']&&$GLOBALS['M_RS485_OP_MODE'] == 0))	ArrayPop($av_menulist, 'ptzsetup');
	if ($GLOBALS['M_SUPPORT_PTZ'] == 0)				{ArrayPop($ptz_menulist, 'ptzlimit');ArrayPop($ptz_menulist, 'presetsetup');}
	if (!$GLOBALS['M_SUPPORT_PTZ_TRACKING'])	{ArrayPop($ptz_menulist, 'ptztrackingsetup');ArrayPop($eve_menulist, 'ptztracking');};
	if ($GLOBALS['M_ALARMOUT_COUNT'] == 0)		ArrayPop($eve_menulist, 'output');
	if (!$GLOBALS['M_SUPPORT_EVENT_ND']) 		ArrayPop($eve_menulist, 'networkdisconnect');
	if (!$GLOBALS['M_SUPPORT_EVENT_FD'])			ArrayPop($eve_menulist, 'facedetection');
	if (!$GLOBALS['M_SUPPORT_EVENT_TD'])			ArrayPop($eve_menulist, 'tamperingdetection');
	if (!$GLOBALS['M_SUPPORT_EVENT_AD']) 		ArrayPop($eve_menulist, 'audiodetection');
	if (!($GLOBALS['M_SUPPORT_SD'] || $GLOBALS['M_SUPPORT_NAS']))	ArrayPop($eve_menulist, 'storage');
	if ($GLOBALS['M_ALARMIN_COUNT'] == 0 || $GLOBALS[classInstances]['Information']->dataInfo['DayNightMode']['value'] == 3) ArrayPop($eve_menulist, 'alarminput');
	if (!$GLOBALS['M_SUPPORT_OPENSDK'])	
	{
		ArrayPop($sys_menulist, 'opensdk');
		ArrayPop($eve_menulist, 'appevent');
	}
	if (!($GLOBALS['M_RS485_OP_MODE'] == 1 && $GLOBALS['M_SUPPORT_EXTERNAL_PTZ'] == 1))
	{
		ArrayPop($ptz_menulist, 'rs485');
	}
	
	$leftmenulist = array("basic"=>$bas_menulist, "ptz"=>$ptz_menulist, "av"=>$av_menulist, "network"=>$net_menulist, "event"=>$eve_menulist, "system"=>$sys_menulist);
	$menu = explode("_", substr($path, 0, -4), 2);
	echo "<div id=\"lnb\"><div id=\"lnb-list\" class=\"lnb-list\"><ul class=\"lnb-list-in\">";
	$index = 1;
	foreach($leftmenulist as $name=>$menulist) {
		if ($name == 'ptz' && $GLOBALS['M_SUPPORT_PTZ'] == 0)
		{
			continue;
		}
		if($name == 'av' && $GLOBALS['M_SUPPORT_AUDIO'])
			echo "<li id="."lnb_".$name."><a href=\"#\"><img src=\"../images/setup/lnb_".$name."_off2.gif\" alt=\"".$name."\" /></a><ul class=\"two_depth\">";
		else if ($name == 'basic') {
			echo "<li id=\"lnb_basic\"><img src=\"../images/setup/lnb_".$name."_off.png\" alt=\"".'basic'."\" /><ul class=\"two_depth_basic\">";
		}
		else {
			echo "<li id="."lnb_".$name."><a href=\"#\"><img src=\"../images/setup/lnb_".$name."_off.gif\" alt=\"".$name."\" /></a><ul class=\"two_depth\">";
		}
		for($index2=0; $index2<count($menulist); ++$index2) {		
			if ($menulist[$index2] == $menu[1]) 	echo "<li class=\"selected\">";
			else 											echo "<li>";
			$menuName = $menulist[$index2];
			if ($menuName == 'videoanalytics' && ($GLOBALS['M_SUPPORT_EVENT_VA'] & IV_SUPPORT) != IV_SUPPORT) $menuName = 'motiondetection';
			if ($GLOBALS['M_SPECIAL_TYPE'] == 1)
			{
				//DEV_S1SMS
				if ($menuName == 'ftpemail') 
				{
					echo "<a href=\"".$name."_ftpemail.cgi\">".$GLOBALS['menu_ftpemailsms'][$GLOBALS['LANGINDEX']]."</a></li>";
				}
				else
				{
					echo "<a href=\"".$name.'_'.$menulist[$index2].".cgi\" ".((($menuName == 'ptztrackingsetup' && $GLOBALS['LANGINDEX'] == 4) || ($menuName == 'ptztrackingsetup' && $GLOBALS['LANGINDEX'] == 11) ) ? "style='height:30px;'" : "").">".$GLOBALS['menu_'.$menuName][$GLOBALS['LANGINDEX']]."</a></li>";
				}
			}
			else
			{
				echo "<a href=\"".$name.'_'.$menulist[$index2].".cgi\" ".((($menuName == 'ptztrackingsetup' && $GLOBALS['LANGINDEX'] == 4) || ($menuName == 'ptztrackingsetup' && $GLOBALS['LANGINDEX'] == 11) ) ? "style='height:30px;'" : "").">".$GLOBALS['menu_'.$menuName][$GLOBALS['LANGINDEX']]."</a></li>";
			}
		}
		echo "</ul></li>";
		if (stristr($path, $name) == FALSE) {
			echo "<script>$('.two_depth').hide();</script>";
		}
	}
	echo "</ul></div></div>";
}
?>
