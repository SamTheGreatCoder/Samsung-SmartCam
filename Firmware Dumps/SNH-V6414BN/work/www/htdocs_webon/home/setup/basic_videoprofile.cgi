<?php
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_menu.cgi');
require_once ('../language/language_av_videoprofile.cgi');

$classInstances= GetClassInstance('videoprofile');
$profileList	= $classInstances['VideoProfile'];
$imageSpecialConf = $classInstances['ImageSetting']->imageSpecial;
$isDIS = $imageSpecialConf->dataInfo["DIS"]["value"];
if ($GLOBALS['M_SPECIAL_TYPE'] == 1)
{
	$fixProfileCnt = 3;	// DEV_S1DEFAULTPROFILE
	if ($GLOBALS['M_SUPPORT_VIDEOCODEC'] & VIDEOCODEC_MASK_MPEG4) $fixProfileCnt = 4;
}
else
{
	$fixProfileCnt = 2;
	if ($GLOBALS['M_SUPPORT_VIDEOCODEC'] & VIDEOCODEC_MASK_MPEG4) $fixProfileCnt = 3;
}
$resolMode = $GLOBALS['M_MAX_RESOLUTION'];
$streamingDisconnection	= $classInstances['StreammingDisconnection'];
// DEV_S1WEBVIEWER Start
$userClassInstance = GetClassInstance('user');
$userConf	= $userClassInstance['UserConfiguration'];
// DEV_S1WEBVIEWER End

define('MIN_BITRATE_3M_CBR',			2 * 1024);
define('MAX_BITRATE_3M_CBR',			15 * 1024);
define('DEFAULT_BITRATE_3M_CBR',		10 * 1024);
define('DEFAULT_BITRATE_2M_CBR',		2.5 * 1024);
define('MIN_BITRATE_1M_CBR',			1024);
define('MAX_BITRATE_1M_CBR',			10 * 1024);
define('MAX_BITRATE_6M_CBR',			6 * 1024);
define('DEFAULT_BITRATE_1M_CBR',		2 * 1024); // for SNF-7010 only  5X1024 -> 2X1024 
define('MIN_BITRATE_D1_CBR',			512);
define('MAX_BITRATE_D1_CBR',			5 * 1024);
define('DEFAULT_BITRATE_D1_CBR',		1 * 1024);
define('MIN_BITRATE_CIF_CBR',			64);
define('MAX_BITRATE_CIF_CBR',			2 * 1024);
define('DEFAULT_BITRATE_CIF_CBR',	512);
define('MIN_BITRATE_QCIF_CBR',		32);
define('MAX_BITRATE_QCIF_CBR',		1024);
define('DEFAULT_BITRATE_QCIF_CBR', 	256);
define('MIN_BITRATE_VBR',				64);
define('MAX_BITRATE_VBR',				30 * 1024);
define('MAX_BITRATE_6M_VBR',			6 * 1024);
define('DEFAULT_BITRATE_VBR',			10 * 1024);
define('DEFAULT_BITRATE_VBR_H264',  10 * 512);
define('MIN_BITRATE_VGA_VBR',			64);
define('MAX_BITRATE_VGA_VBR',			15 * 1024);
define('DEFAULT_BITRATE_VGA_VBR',	1024);
define('DEFAULT_BITRATE_3M_VBR',		3*1024);
define('DEFAULT_BITRATE_5M',			5*1024);
define('DEFAULT_BITRATE_4M',			4*1024);
define('DEFAULT_BITRATE_2M',			2*1024);
define('DEFAULT_BITRATE_1M',			1024);
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="kr" xml:lang="kr">
<head>
	<title>iPOLiS NETWORK CAMERA WEBVIEWER</title>
	<meta http-equiv="X-UA-Compatible" content="IE=Edge; requiresActiveX=true" />
	<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
	<link rel="stylesheet" type="text/css" href="../css/techwin.css" />
	<style>
	#lnb-list {
		height:1450px;
	}
	#CGILoading {filter:alpha(opacity=60); opacity:0.6; -moz-opacity:0.6;}
	#mask {
	   position:absolute;
	   z-index:9000;
	   background-color:#000;
	   display:none;
	   left:0;
	   top:0;
	}
	.window{
	   display: none;
	   position:absolute;
	   left:50%;
	   top:350px;
	   margin-left: -500px;
	   width:700px;
	   <?php if($GLOBALS['M_MAX_RESOLUTION'] == MAX_2_MEGA || $GLOBALS['MEGAMODE'] == 2) { ?>
	   height:550px;
	   <?php } else { ?>
	   height:650px;
	   <?php } ?>
	   background-color:#40495a;
	   border:5px solid #1b2029;
	   z-index:10000;
	   padding:20px 5px 5px 5px;
	}
	</style>
	<script type="text/javascript" src="../js/jquery-1.9.1.js"></script>
	<script type="text/javascript" src="../js/lnb.js"></script>
	<script type="text/javascript" src="../js/jquery-ui.js"></script>
	<script type="text/javascript" src="../js/board.js"></script>
	<script type="text/javascript" src="../js/common_function.js"></script>
	<script type="text/javascript" src="../js/pluginCheck.js"></script>
	<script type="text/javascript" src="../js/pluginControl.js"></script>	
	<!--[if lt IE 9]><script type="text/javascript" src="../js/excanvas.js"></script><![endif]-->	
	<script type="text/javascript" src="../js/videoProfile.js"></script>
	<script type="text/javascript">
<?php
	if ($classInstances['Information']->dataInfo['PasswordCheck']['value'] == 1) {
?>
		window.location.href = '../pw_change.cgi';
<?php
	}
	else if ($classInstances['Information']->dataInfo['PasswordCheck']['value'] == 2) {
?>
		alert("<?php echo $msg_change_weak_password[$GLOBALS['LANGINDEX']]; ?>");
<?php
	}
?>
	$(document).ready(function(){
		lnbonoff("lnb_basic");
	});

	var browserName = "<?php echo GetBrowserName(); ?>";
	var ieVer = <?php echo ieversion(); ?>;

	var localSeq				= <?php echo $_SESSION['count']; ?>;
	var ajaxReqUrl				= "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq;
	var encName 				= "<?php echo $GLOBALS['USERINFO']['encname']; ?>";
	var encPW 					= "<?php echo $GLOBALS['USERINFO']['encpw']; ?>";
	var devicePort 			= <?php echo $classInstances['Information']->dataInfo['DevicePort']['value']; ?>;
	var previewProfileNo 	= <?php echo $classInstances['Information']->dataInfo['PreviewProfileNo']['value']; ?> + 1;
	var installMsg				= new Array();
	installMsg[0] 				= "<?php echo $msg_plugin_install[$GLOBALS['LANGINDEX']]; ?>";
	installMsg[1] 				= "<?php echo $msg_plugin_install2[$GLOBALS['LANGINDEX']]; ?>";
	installMsg[2] 				= "<?php echo $msg_notsupport_plugin[$GLOBALS['LANGINDEX']]; ?>";
	
	var viewerWidth 			= <?php echo $GLOBALS['VIEWER_RESOLUTION']['width']; ?>;
	var viewerHeight 			= <?php echo $GLOBALS['VIEWER_RESOLUTION']['height']; ?>;

	var videotype 		= "<?php echo $classInstances['Information']->dataInfo['VideoType']['value']; ?>";
	var sensorFrameMode = "<?php echo $classInstances['Information']->dataInfo['SensorFrameMode']['value']; ?>";
	var VIDEOTYPE_NTSC = 0;
	var VIDEOTYPE_PAL = 1;
	var CODEC_MJPEG 	= 0;
	var CODEC_MPEG4 	= 1;
	var CODEC_H264 	= 2;
	var oldSelNo;
	var profile_cnt = 0;

	var RESOL_MEGA 	= 0;
	var RESOL_3MEGA 	= 1;
	var RESOL_4CIF 	= 2;
	var RESOL_VGA 		= 3;
	var RESOL_2MEGA 	= 4;
	var resolMode = parseInt(<?php echo $resolMode; ?>);
	var profileFrmArr = new Array();
	var MEGA_MODE = <?php echo $classInstances['Information']->dataInfo['MegaMode']['value']; ?>;
	
	var profileNameArr = new Array();
	var gopISone = false;	
	var govMax = <?php echo $GLOBALS['M_MAX_GOV']; ?>;
	var mirror = <?php echo $classInstances['Information']->dataInfo['Mirror']['value']; ?>;
	var flip = <?php echo $classInstances['Information']->dataInfo['Flip']['value']; ?>;

	var maxResolution = {width: <?php echo $GLOBALS['MAX_RESOLUTION']['width'] ?>, height: <?php echo $GLOBALS['MAX_RESOLUTION']['height'] ?>};
	var crop_set, cropX, cropY, cropWidth, cropHeight, cropRatio;
	var crop_x = new Array();
	var crop_y = new Array();
	var crop_width = new Array();
	var crop_height = new Array();
	var crop_ratio = new Array();

<?php
	if($GLOBALS['M_SUPPORT_CROP_ENCODING']) {
		for($index = 0; $index<MAX_PROFILE; $index++) {
?>
		crop_x[<?php echo $index; ?>] = <?php echo $profileList->profile[$index]->dataInfo['CropXpos']['value']; ?>;
		crop_y[<?php echo $index; ?>] = <?php echo $profileList->profile[$index]->dataInfo['CropYpos']['value']; ?>;
		crop_width[<?php echo $index; ?>] = <?php echo $profileList->profile[$index]->dataInfo['CropWidth']['value']; ?>;
		crop_height[<?php echo $index; ?>] = <?php echo $profileList->profile[$index]->dataInfo['CropHeight']['value']; ?>;
		crop_ratio[<?php echo $index; ?>] = <?php echo $profileList->profile[$index]->dataInfo['CropRatio']['value']; ?>;
<?php
		}
	}
?>

	var record_mjpeg_bitrate = 6144;
	var record_h264_bitrate = 6144;
<?php 
	if ($GLOBALS['M_ISP_TYPE']  == ISP_TYPE_HISILICON) { 
?>
	record_h264_bitrate = 4096;
<?php
	}
?>
		
	function OnClickApply()
	{
		var selNo = $("input[name='profile_select']:checked").val();
		var codecType = parseInt($('#profile_'+selNo+'_codec').val());
		var codec = 'h264';
		var resolVal = $('#profile_'+selNo+'_resolution').val().split(" X ");
		var obj = 'profile_'+selNo+'_';

	  	if (!CheckProfile()) return;

		var actionName = "Set";
		if ($('div').hasClass('profile_'+selNo+'_add')) actionName = "Add";

		var msg = "<"+actionName+"VideoProfile>";
		msg += "<Name>"+$('#'+obj+'name').val()+"</Name>";
		msg += "<Index>"+selNo+"</Index>";
		msg += "<Default>"+($('#'+obj+'type_default').is(':checked') ? 1 : 0 )+"</Default>";
		msg += "<EventProfile>"+($('#'+obj+'type_event').is(':checked') ? 1 : 0 )+"</EventProfile>";
		msg += "<RecordProfile>"+($('#'+obj+'type_record').is(':checked') ? 1 : 0 )+"</RecordProfile>";
		msg += "<FixedRateProfile>0</FixedRateProfile>";
<?php
	if($GLOBALS['M_SUPPORT_AUDIO']) {
?>
		msg += "<UseAudioIn>"+($('#'+obj+'audioIn').is(':checked') ? 1 : 0 )+"</UseAudioIn>";
<?php
	}
?>
		msg += "<UseATC>"+$('#'+obj+'atc').val()+"</UseATC>";
		msg += "<ATC_Sensitivity>"+$('#'+obj+'atc_sensitivity').val()+"</ATC_Sensitivity>";
		if($('#'+obj+'atc_limit').val() >= 10 && $('#'+obj+'atc_limit').val() <= 50)
			msg += "<ATC_Limit>"+$('#'+obj+'atc_limit').val()+"</ATC_Limit>";
	<?php
		if($GLOBALS['M_SUPPORT_CROP_ENCODING']) {
	?>
			msg += "<UseCropEncoding>"+ ($('#'+obj+'cropencoding_use').is(':checked') ? 1 : 0)+"</UseCropEncoding>";
			if (crop_set ==1) {
				msg += "<CropXpos>"+cropX+"</CropXpos>";
				msg += "<CropYpos>"+cropY+"</CropYpos>";
				msg += "<CropWidth>"+cropWidth+"</CropWidth>";
				msg += "<CropHeight>"+cropHeight+"</CropHeight>";
				msg += "<CropRatio>"+cropRatio+"</CropRatio>";
			}
	<?php
		}
	?>
		msg += "<Encoding>"+codecType+"</Encoding>";
	  	msg += "<ResolWidth>"+resolVal[0]+"</ResolWidth>";
	  	msg += "<ResolHeight>"+resolVal[1] +"</ResolHeight>";
<?php
	if ($GLOBALS['M_SUPPORT_COMPRESSION']) {
?>
	  	msg += "<Compression>"+$('#'+obj+'compression').val()+"</Compression>";
<?php	  	
	}
?>
	  	msg += "<BitrateLimit>"+parseInt($('#'+obj+'bitrate').val(),10)+"</BitrateLimit>";
	  	msg += "<FrameRateLimit>"+$('#'+obj+'framerate').val()+"</FrameRateLimit>";

		if(codecType == CODEC_H264) {		
		  	msg += "<H264GovLength>"+$('#'+obj+'adv_gop').val()+"</H264GovLength>";
		  	<?php if ($GLOBALS['M_SUPPORT_ENTROPY']) { ?> 
		  	msg += "<H264Profile>"+$('#'+obj+'adv_profile').val()+"</H264Profile>";
		  	msg += "<H264Entropy>"+$('#'+obj+'adv_entropy').val()+"</H264Entropy>";
		  	<?php } ?>
		  	msg += "<H264Priority>"+$('#'+obj+'adv_priority').val()+"</H264Priority>";
			msg += "<ConstantBitrate>"+$('#'+obj+'adv_bitcontrol').val() +"</ConstantBitrate>";
			
	<?php
		if($GLOBALS['M_SUPPORT_SMARTCODEC']) {
	?> 	
			msg += "<UseSmartCodec>"+$('#'+obj+codec+'_adv_smart').val()+"</UseSmartCodec>";
	<?php
		}
	?> 	
		}
		else if(codecType == CODEC_MPEG4) {
			codec = 'mpeg4'
	  		msg += "<MPEG4GovLength>"+ $('#'+obj+'adv_gop').val() +"</MPEG4GovLength>";
		}
		msg += "<VNPEnabled>"+ ($('#'+obj+'multicast_svnp_use').is(':checked') ? 1 : 0)+"</VNPEnabled>";
		msg += "<VNPIPv4Addr>"+$('#'+obj+'multicast_svnp_ip').val()+"</VNPIPv4Addr>";
		msg += "<VNPPort>"+$('#'+obj+'multicast_svnp_port').val()+"</VNPPort>";
		msg += "<VNPTTL>"+$('#'+obj+'multicast_svnp_ttl').val()+"</VNPTTL>";
		msg += "<RTPEnabled>"+($('#'+obj+'multicast_rtp_use').is(':checked') ? 1 : 0)+"</RTPEnabled>";
		msg += "<RTPIPv4Addr>"+$('#'+obj+'multicast_rtp_ip').val()+"</RTPIPv4Addr>";
		msg += "<RTPPort>"+$('#'+obj+'multicast_rtp_port').val()+"</RTPPort>";
		msg += "<RTPTTL>"+$('#'+obj+'multicast_rtp_ttl').val()+"</RTPTTL>";
		msg += "</"+actionName+"VideoProfile>";
		RequestAjaxMsg(msg, "<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq);
	}

	function CheckProfile()
	{
		var selNo = parseInt($("input[name='profile_select']:checked").val());
		var obj = 'profile_'+selNo+'_';
		var profileName = $('#'+obj+'name').val();

		if (selNo >= parseInt(<?php echo $fixProfileCnt; ?>) ) {
			if (!TypeCheck(profileName, NUM+ALPHA) || CheckSpace(profileName)) {
				alert("<?php echo $msg_invalid_name[$GLOBALS['LANGINDEX']]; ?>");
				return false;
			}
		}

		profileNameArr[selNo] = profileName;
		<?php
		for ($index=0; $index<MAX_PROFILE; $index++) {
		?>
			if ((selNo != "<?php echo $index; ?>" && profileName == "<?php echo $profileList->profile[$index]->dataInfo['Name']['value']; ?>") || profileName == "profile<?php echo $index+1;?>") {
				alert("<?php echo $msg_invalid_name[$GLOBALS['LANGINDEX']]; ?>");
				return false;
			}
		<?php
		}?>

		if ($('#'+obj+'atc').val() > 0)
		{
			if ($('#'+obj+'atc_limit').val() < 10 || $('#'+obj+'atc_limit').val() > 50 || $('#'+obj+'atc_limit').val() == '' || !TypeCheck($('#'+obj+'atc_limit').val(), NUM))
			{
				alert("<?php echo $msg_invalid_profile_atc_limit[$GLOBALS['LANGINDEX']]; ?>");
				return false;
			}
		}

		if ($('#'+obj+'multicast_svnp_use').is(':checked')	&& !CheckMulticast($('#'+obj+'multicast_svnp_ip').val(), $('#'+obj+'multicast_svnp_port').val(), $('#'+obj+'multicast_svnp_ttl').val(), false)) 	return false;
		if ($('#'+obj+'multicast_rtp_use').is(':checked')	&& !CheckMulticast($('#'+obj+'multicast_rtp_ip').val(), $('#'+obj+'multicast_rtp_port').val(), $('#'+obj+'multicast_rtp_ttl').val(), true)) 		return false;
		if ($('#'+obj+'multicast_svnp_use').is(':checked') && $('#'+obj+'multicast_rtp_use').is(':checked')){
			if ($('#'+obj+'multicast_svnp_ip').val() == $('#'+obj+'multicast_rtp_ip').val() && $('#'+obj+'multicast_svnp_port').val() == $('#'+obj+'multicast_rtp_port').val()) {
				alert("<?php echo $msg_invalid_svnp_port[$GLOBALS['LANGINDEX']]; ?>");
				return false;
			}
		}
		var bitrateArr = GetBitrateRange('load');
		var minBitrate = parseInt(bitrateArr[0]);
		var maxBitrate = parseInt(bitrateArr[1]);
		var bitrateMsg = bitrateArr[3];
		var bitrateVal = parseInt($('#'+obj +'bitrate').val(), 10);

		if(parseInt($('#profile_'+selNo+'_codec').val()) != CODEC_MJPEG)
		{
			if ($('#profile_'+selNo+'_adv_gop').val() < 1 || $('#profile_'+selNo+'_adv_gop').val() > govMax) {
				alert("<?php echo $msg_check_gov[$GLOBALS['LANGINDEX']]; ?>");
				return false;
			}
		}

		if (!TypeCheck($('#'+obj +'bitrate').val(), NUM) || CheckSpace(new String(bitrateVal)) || bitrateVal<minBitrate || bitrateVal>maxBitrate) {
			alert(bitrateMsg);
			return false;
		}
	
		return true;
	}

	function CheckMulticast(ip, port, ttl, isRTP)
	{
		var ipPattern	= /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/;
		var mcastArray	= ip.match(ipPattern);

		if (mcastArray == null || !TypeCheck(ip, NUM+'.')) {
			alert( "<?php echo $msg_check_multicast[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}
		for (var index=2; index<5; index++){
			 if (mcastArray[index].length > 1) {
				if (mcastArray[index].charAt(0)  == '0'){
					alert( "<?php echo $msg_check_multicast[$GLOBALS['LANGINDEX']]; ?>");
					return false;
				}	
			}
		}
		thisSegment = mcastArray[1];
		if (thisSegment < 224 || thisSegment > 239) {
			alert( "<?php echo $msg_check_multicast[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}

		for(var index=2; index<4; ++index) {
			thisSegment = mcastArray[index];
			if(thisSegment > 255) {
				alert( "<?php echo $msg_check_multicast[$GLOBALS['LANGINDEX']]; ?>");
				return false;
			}
		}
		thisSegment = mcastArray[4];
		if (thisSegment > 254) {
			alert( "<?php echo $msg_check_multicast[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}

		if (isRTP == true) {
			if ((port % 2) != 0 ||port == 3702 || port < 1024 || port > 65535 || !TypeCheck(port, NUM)) {
				alert( "<?php echo $msg_error_multicast_rtp[$GLOBALS['LANGINDEX']]; ?>");
				return false;
			}
		}
		else {
			if (port == 3702 || port < 1024 || port > 65535 || !TypeCheck(port, NUM)) {
				alert( "<?php echo $msg_error_multicast_svnp[$GLOBALS['LANGINDEX']]; ?>");
				return false;
			}
		}

		if (ttl == "" || ttl<0 || ttl >255 || !TypeCheck(ttl, NUM)) {
			alert( "<?php echo $msg_check_ttl[$GLOBALS['LANGINDEX']]; ?>");
			return false;
		}

		return true;
	}

	function wrapWindowByMask()
	{
		var maskHeight = $(document).height();
		var maskWidth = $(document).width();
		$('#mask').css({'width':maskWidth,'height':maskHeight});
		$('#mask').fadeIn(0);
		$('#mask').fadeTo("slow",0.7);
		$('.window').css({'top':getScrollTop()+100});
		$('.window').show();
		SISOPlugin.init(installMsg, viewerWidth, viewerHeight);
		// DEV_S1WEBVIEWER start
		//SISOPlugin.startPluginPlay(devicePort,previewProfileNo,encName,encPW);
		<?php if ($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>
			SISOPlugin.startS1PluginPlay(devicePort,previewProfileNo,encName,encPW,<?php echo $userConf->dataInfo['IsEnableNoEncrypt']['value']; ?>);
		<?php } else { ?>
			SISOPlugin.startPluginPlay(devicePort,previewProfileNo,encName,encPW);
		<?php } ?>
		// DEV_S1WEBVIEWER end
		cropEncoding.drawing.init(viewerWidth,viewerHeight, maxResolution.width,maxResolution.height);
	}

	function getScrollTop() 
	{
		if (typeof window.pageYOffset != 'undefined')
		{
			return window.pageYOffset;
		}
		else if (typeof document.documentElement != 'undefined')
		{
			return document.documentElement.scrollTop;
		}
		else if (typeof document.body != 'undefined')
		{
			return document.body.scrollTop;
		}
		else
		{
			return 0;
		}
	}

	function GetBitrateRange(type)
	{
		var selNo = $("input[name='profile_select']:checked").val();
		var codecType = parseInt($('#profile_'+selNo+'_codec').val());
		var bitControlVal = $('#profile_'+selNo+'_adv_bitcontrol').val();
		var resolVal = $('#profile_'+selNo+'_resolution').val().split(" X ");
		var resol_temp = resolVal[1].split("(");
		var min_bitrate = 0;
		var max_bitrate = 0;
		var resol_width = resolVal[0];
		var resol_height = resol_temp[0];
		var defaultBitrate = 0;
		var bitrateMsg = '';

		if (codecType == CODEC_MJPEG) {
			DisplayMJPEG_BitrateRange(type);
			<?php for($i=0 ; $i<MAX_RESOLUTION_COUNT ; $i++) { ?>
				if(resol_width == <?php echo $classInstances['ResolutionInfo']->resolution[$i]->dataInfo['Width']['value']; ?> && resol_height == <?php echo $classInstances['ResolutionInfo']->resolution[$i]->dataInfo['Height']['value']; ?>){
					min_bitrate = <?php echo $classInstances['ResolutionInfo']->resolution[$i]->dataInfo['MJPEGVBRMinBitrate']['value']; ?>/1024;
					max_bitrate = <?php echo $classInstances['ResolutionInfo']->resolution[$i]->dataInfo['MJPEGVBRMaxBitrate']['value']; ?>/1024;
					defaultBitrate = <?php echo $classInstances['ResolutionInfo']->resolution[$i]->dataInfo['MJPEGVBRDefaultBitrate']['value']; ?>/1024;
					if ($('#profile_'+selNo+'_type_record').is(':checked') && max_bitrate > record_mjpeg_bitrate ) max_bitrate = record_mjpeg_bitrate;
					bitrateMsg = "<?php echo $msg_maximum_bitrate0[$GLOBALS['LANGINDEX']]; ?>"+min_bitrate+"<?php echo $msg_maximum_bitrate1[$GLOBALS['LANGINDEX']]; ?>"+max_bitrate+"<?php echo $msg_maximum_bitrate2[$GLOBALS['LANGINDEX']]; ?>";
				}
			<?php }?>
		}
		else {
			if (bitControlVal == 1) {	// BITCONTROL_CBR
			<?php for($i=0 ; $i<MAX_RESOLUTION_COUNT ; $i++) { ?>
				if(resol_width == <?php echo $classInstances['ResolutionInfo']->resolution[$i]->dataInfo['Width']['value']; ?> && resol_height == <?php echo $classInstances['ResolutionInfo']->resolution[$i]->dataInfo['Height']['value']; ?>){
					min_bitrate = <?php echo $classInstances['ResolutionInfo']->resolution[$i]->dataInfo['H264CBRMinBitrate']['value']; ?>/1024;
					max_bitrate = <?php echo $classInstances['ResolutionInfo']->resolution[$i]->dataInfo['H264CBRMaxBitrate']['value']; ?>/1024;
					defaultBitrate = <?php echo $classInstances['ResolutionInfo']->resolution[$i]->dataInfo['H264CBRDefaultBitrate']['value']; ?>/1024;
					if ($('#profile_'+selNo+'_type_record').is(':checked')) {
						if (max_bitrate > record_h264_bitrate)
							max_bitrate = record_h264_bitrate;
						if (defaultBitrate > record_h264_bitrate)
							defaultBitrate = record_h264_bitrate;
					}
					bitrateMsg = "<?php echo $msg_target_bitrate0[$GLOBALS['LANGINDEX']]; ?>"+min_bitrate+"<?php echo $msg_target_bitrate1[$GLOBALS['LANGINDEX']]; ?>"+max_bitrate+"<?php echo $msg_target_bitrate2[$GLOBALS['LANGINDEX']]; ?>";
				}
			<?php }?>

			}
			else {
				<?php for($i=0 ; $i<MAX_RESOLUTION_COUNT ; $i++) { ?>
					if(resol_width == <?php echo $classInstances['ResolutionInfo']->resolution[$i]->dataInfo['Width']['value']; ?> && resol_height == <?php echo $classInstances['ResolutionInfo']->resolution[$i]->dataInfo['Height']['value']; ?>){
						min_bitrate = <?php echo $classInstances['ResolutionInfo']->resolution[$i]->dataInfo['H264VBRMinBitrate']['value']; ?>/1024;
						max_bitrate = <?php echo $classInstances['ResolutionInfo']->resolution[$i]->dataInfo['H264VBRMaxBitrate']['value']; ?>/1024;
						defaultBitrate = <?php echo $classInstances['ResolutionInfo']->resolution[$i]->dataInfo['H264VBRDefaultBitrate']['value']; ?>/1024;
						if ($('#profile_'+selNo+'_type_record').is(':checked')) {
							if (max_bitrate > record_h264_bitrate)
								max_bitrate = record_h264_bitrate;
							if (defaultBitrate > record_h264_bitrate)
								defaultBitrate = record_h264_bitrate;
						}
						bitrateMsg = "<?php echo $msg_maximum_bitrate0[$GLOBALS['LANGINDEX']]; ?>"+min_bitrate+"<?php echo $msg_maximum_bitrate1[$GLOBALS['LANGINDEX']]; ?>"+max_bitrate+"<?php echo $msg_maximum_bitrate2[$GLOBALS['LANGINDEX']]; ?>";
					}
				<?php }?>
			}
		}
		var bitrateArr = [min_bitrate, max_bitrate, defaultBitrate, bitrateMsg];
		return bitrateArr;
	}


	function OnChangeResolution(type)
	{
		var selNo = $("input[name='profile_select']:checked").val();
		var bitrateArr = GetBitrateRange('load');
		var minBitrate = bitrateArr[0];
		var maxBitrate = bitrateArr[1];
		var defaultBitrate = bitrateArr[2];
		if ($('#profile_'+selNo+'_codec').val() != CODEC_MJPEG)
		{
			if(type == 'change')
			{
				if ($('#profile_'+selNo+'_bitrate').val() > parseInt(maxBitrate)) $('#profile_'+selNo+'_bitrate').val(maxBitrate);
				if ($('#profile_'+selNo+'_bitrate').val() < parseInt(minBitrate)) $('#profile_'+selNo+'_bitrate').val(minBitrate);
				$('#profile_'+selNo+'_bitrate').val(defaultBitrate);				
			}

			if($('#profile_'+selNo+'_codec').val() == CODEC_MPEG4 && $('#profile_'+selNo+'_adv_bitcontrol').val() == 0)
				$('#profile_'+selNo+'_bitrate_range').html('');
			else
				$('#profile_'+selNo+'_bitrate_range').html('('+minBitrate+' ~ '+maxBitrate+')');

		}
		OnClickProfileType(type);
		OnChangeFrate(type);
	}

	function DisplayMJPEG_BitrateRange(type)
	{
		var selNo = $("input[name='profile_select']:checked").val();
		var resolVal = $('#profile_'+selNo+'_resolution').val().split(" X ");
		var resol_temp = resolVal[1].split("(");
		var min_bitrate = 0;
		var max_bitrate = 0;
		var def_bitrate = 0;
		var resol_width = resolVal[0];
		var resol_height = resol_temp[0];
	
		<?php for($i=0 ; $i<MAX_RESOLUTION_COUNT ; $i++) { ?>
			if(resol_width == <?php echo $classInstances['ResolutionInfo']->resolution[$i]->dataInfo['Width']['value']; ?> && resol_height == <?php echo $classInstances['ResolutionInfo']->resolution[$i]->dataInfo['Height']['value']; ?>){
				min_bitrate = <?php echo $classInstances['ResolutionInfo']->resolution[$i]->dataInfo['MJPEGVBRMinBitrate']['value']; ?>/1024;
				max_bitrate = <?php echo $classInstances['ResolutionInfo']->resolution[$i]->dataInfo['MJPEGVBRMaxBitrate']['value']; ?>/1024;
				def_bitrate = <?php echo $classInstances['ResolutionInfo']->resolution[$i]->dataInfo['MJPEGVBRDefaultBitrate']['value']; ?>/1024;
			}
		<?php }?>
		
		if ($('#profile_'+selNo+'_type_record').is(':checked')) {

			if (max_bitrate > record_mjpeg_bitrate) max_bitrate = record_mjpeg_bitrate; 
			if(type == 'change' && $('#profile_'+selNo+'_bitrate').val() > max_bitrate) $('#profile_'+selNo+'_bitrate').val(max_bitrate);
			
		}
		else {
			if(type == 'change') $('#profile_'+selNo+'_bitrate').val(def_bitrate);
		}
		$('#profile_'+selNo+'_bitrate_range').html('('+min_bitrate+' ~ '+max_bitrate+')');
	}

	function GetCurrentProfile()
	{
		for (var index=1; index<=10; ++index) {
			if ($('#profileList'+index).is(':checked')) {
				return (index-1);
			}
		}
		return false;
	}

	function OnClickMulticastUse(protocol)
	{
		var selNo = $("input[name='profile_select']:checked").val();
		if ($('#profile_'+selNo+'_multicast_'+protocol+'_use').is(':checked')) {
			$('#profile_'+selNo+'_multicast_'+protocol+'_ip').removeAttr('disabled');
			$('#profile_'+selNo+'_multicast_'+protocol+'_port').removeAttr('disabled');
			$('#profile_'+selNo+'_multicast_'+protocol+'_ttl').removeAttr('disabled');
		}
		else {
			$('#profile_'+selNo+'_multicast_'+protocol+'_ip').attr('disabled', 'disabled');
			$('#profile_'+selNo+'_multicast_'+protocol+'_port').attr('disabled', 'disabled');
			$('#profile_'+selNo+'_multicast_'+protocol+'_ttl').attr('disabled', 'disabled');
		}
	}

	function OnChangeH264ProfileMode()
	{
		<?php if ($GLOBALS['M_SUPPORT_ENTROPY']) { ?>
		var selNo = $("input[name='profile_select']:checked").val();
		var oldProfile = $('#profile_'+selNo+'_adv_profile').val();
			if ($('#profile_'+selNo+'_type_record').is(':checked')) {
				$('#profile_'+selNo+'_adv_profile option:eq(0)').attr("disabled", "disabled");
				if (oldProfile == 0) $('#profile_'+selNo+'_adv_profile').val(1);
			}else {
				$('#profile_'+selNo+'_adv_profile option:eq(0)').removeAttr("disabled");
				if($('#profile_'+selNo+'_adv_profile').val() == 0) {     //BaseLine
					$('#profile_'+selNo+'_adv_entropy').val(0);
					$('#profile_'+selNo+'_adv_entropy').attr('disabled', 'disabled');
				}
				else {
					$('#profile_'+selNo+'_adv_entropy').removeAttr('disabled');
				}
			}
		<?php } ?>
	}

	function OnChangeBitcontrol(type)
	{

		var selNo = $("input[name='profile_select']:checked").val();
		var codecType = parseInt($('#profile_'+selNo+'_codec').val());
		var bitrateArr = GetBitrateRange('load');
		var minBitrate = bitrateArr[0];
		var maxBitrate = bitrateArr[1];
		var defaultBitrate = bitrateArr[2];

		if ($('#profile_'+selNo+'_codec').val() != CODEC_MJPEG)
		{
			if (type == 'change' || $('#profile_'+selNo+'_name').val() == '')
			{
				if ($('#profile_'+selNo+'_bitrate').val() > parseInt(maxBitrate)) $('#profile_'+selNo+'_bitrate').val(maxBitrate);
				if ($('#profile_'+selNo+'_bitrate').val() < parseInt(minBitrate)) $('#profile_'+selNo+'_bitrate').val(minBitrate);

				if ($('#profile_'+selNo+'_type_record').is(':checked')) {
					if(type == 'change' && $('#profile_'+selNo+'_bitrate').val() > record_h264_bitrate ) $('#profile_'+selNo+'_bitrate').val(record_h264_bitrate);
				}else
					$('#profile_'+selNo+'_bitrate').val(defaultBitrate);

			}
			if($('#profile_'+selNo+'_codec').val() == CODEC_MPEG4 && $('#profile_'+selNo+'_adv_bitcontrol').val() == 0)
				$('#profile_'+selNo+'_bitrate_range').html('');
			else
				$('#profile_'+selNo+'_bitrate_range').html('('+minBitrate+' ~ '+maxBitrate+')');

		}

		if (codecType == CODEC_MJPEG || $('#profile_'+selNo+'_adv_bitcontrol').val() == 0) {   // VBR

			if (codecType == CODEC_H264)
			{
				<?php if ($GLOBALS['M_SUPPORT_COMPRESSION']) { ?> 
				$('#profile_'+selNo+'_compression').removeAttr('disabled');
				<?php } ?>
				$('#profile_'+selNo+'_adv_priority').attr('disabled', 'disabled');
				<?php if($GLOBALS['M_SUPPORT_SMARTCODEC']) { ?>
				$('#profile_'+selNo+'_h264'+'_adv_smart').attr('disabled', 'disabled');
				<?php } ?>
				
				$('#profile_'+selNo+'_bitrate').removeAttr('disabled');
			}
			else if (codecType == CODEC_MPEG4)
			{
				<?php if ($GLOBALS['M_SUPPORT_COMPRESSION']) { ?> 
				$('#profile_'+selNo+'_compression').removeAttr('disabled');
				<?php } ?>
				$('#profile_'+selNo+'_adv_priority').attr('disabled', 'disabled');
				$('#profile_'+selNo+'_bitrate').attr('disabled', 'disabled');
				$('#profile_'+selNo+'_bitrate').val(10240);

			}
			else if (codecType == CODEC_MJPEG)
			{
				$('#profile_'+selNo+'_bitrate').removeAttr('disabled');
			}
			$('.target_bitrate').hide();
			$('.max_bitrate').show();
		}
		else {

			if (codecType == CODEC_H264)
			{
				<?php if ($GLOBALS['M_SUPPORT_COMPRESSION']) { ?> 
				$('#profile_'+selNo+'_compression').attr('disabled', 'disabled');
				<?php } ?>
				$('#profile_'+selNo+'_adv_priority').removeAttr('disabled');
				<?php if($GLOBALS['M_SUPPORT_SMARTCODEC']) { ?>
				$('#profile_'+selNo+'_h264'+'_adv_smart').removeAttr('disabled');
				<?php } ?>

			}
			else if (codecType == CODEC_MPEG4)
			{
				<?php if ($GLOBALS['M_SUPPORT_COMPRESSION']) { ?> 
				$('#profile_'+selNo+'_compression').attr('disabled', 'disabled');
				<?php } ?>
				$('#profile_'+selNo+'_adv_priority').removeAttr('disabled');
				$('#profile_'+selNo+'_bitrate').removeAttr('disabled');


			}

			$('.target_bitrate').show();
			$('.max_bitrate').hide();
		}

		if(codecType == CODEC_MJPEG) {
			$('.target_bitrate').hide();
			$('.max_bitrate').show();
			$('#profile_'+selNo+'_compression').removeAttr('disabled');
		}

		OnChangeATC();
	}
	
	function GetMaxFrameRate (selNo, encoding, width, height )
	{
		var maxframe = 30;
		<?php
		if ($resolMode == MAX_1_MEGA || $resolMode == MAX_2_MEGA || $resolMode == MAX_3_MEGA){
			if($GLOBALS['M_SUPPORT_SENSOR_FRAMEMODE']){
		?>
				if (encoding == 2) { //H264
					if (sensorFrameMode == 0) maxframe = 60;
					else if (sensorFrameMode == 1) maxframe = 50;
					else if (sensorFrameMode == 2) maxframe = 30;
					else if (sensorFrameMode == 3) maxframe = 25;
				
				}else if (encoding == 0) { //MJPEG
					if (sensorFrameMode == 3) maxframe = 25;
			<?php 
					if ($resolMode == MAX_1_MEGA || $resolMode == MAX_2_MEGA || $resolMode == MAX_3_MEGA) {
			?>
						if (width >= 1024) maxframe = 15;
					<?php 
						if ($resolMode == MAX_3_MEGA) {
					?>
						if (encoding == 0 && width == 2048) maxframe = 10;
					<?php 
						}
					?>
					<?php 
						if ($GLOBALS['M_ISP_TYPE']  == ISP_TYPE_HISILICON) {
					?>
						if (width >= 1024) {
							maxframe = 1;
						}else {
							if ($('#profile_'+selNo+'_type_record').is(':checked')) maxframe = 5;
							else maxframe = 15;						
						}
					<?php 
						}
					?>
					
			<?php
					}
			?>
				}
		<?php	
			}else {
				if ($resolMode == MAX_3_MEGA) {
			?>
				if(MEGA_MODE == 3)  maxframe = 20;
				else maxframe = 30;
				if (encoding == 0 && width == 2048) maxframe = 10;
				else if (encoding == 0 && width >= 1024) maxframe = 15;
			<?php 
				}
			}
			?>
			if (encoding == 1 && width == 1280 && height == 1024) maxframe = 25; //MPEG4
			<?php
				if($resolMode == MAX_1_MEGA && $GLOBALS['M_SUPPORT_PTZ']) {
			?>
				if (encoding == 0 && height > 600) maxframe = 15;
			<?php
				}
			?>
		<?php
		}else if ($resolMode == MAX_4CIF) {
		?>
			if (videotype == VIDEOTYPE_NTSC)  maxframe = 30;
			else maxframe = 25;
		<?php
		}
		?>
		
		if ($('#profile_'+selNo+'_type_event').is(':checked')) {						
			<?php 
				if ($GLOBALS['M_ISP_TYPE']  == ISP_TYPE_HISILICON) {
			?>
					if (encoding == 0 && width >= 1024) maxframe = 1;
					else maxframe = 5;
			<?php
				} else {
			?>				
				maxframe = 5;
			<?php
				}
			?>			
		}
		
		return maxframe;
	}
	
	function OnClickProfileType(type)
	{
		var selNo = $("input[name='profile_select']:checked").val();
		var resolVal = $('#profile_'+selNo+'_resolution').val().split(" X ")
		var height = resolVal[1].split("(");
		var maxframe = GetMaxFrameRate(selNo, parseInt($('#profile_'+selNo+'_codec').val()),resolVal[0], height[0]);
		ChangeFramerate(maxframe, 'load');
		OnChangeBitcontrol('load');
		GetBitrateRange(type);
		OnChangeH264ProfileMode();

 		var resolVal = $('#profile_'+selNo+'_resolution').val().split(" X ");
		var pixel = parseInt(resolVal[0])*parseInt(resolVal[1]);
		var gov_maxratio = <?php echo $GLOBALS['M_GOV_MAXRATIO']; ?>;
		if ($('#profile_'+selNo+'_framerate').val() / 1000 * gov_maxratio < govMax)
			govMax = $('#profile_'+selNo+'_framerate').val() / 1000 * gov_maxratio;
					
		$('#profile_'+selNo+'_gop_range').html('(1 ~ '+govMax+')');
		if ($('#profile_'+selNo+'_type_record').is(':checked')) {
			if (parseInt($('#profile_'+selNo+'_codec').val()) == CODEC_H264) {

				//for (var i=1; i<=15; i++)
				//	$('#profile_'+selNo+'_h264_adv_gop option:eq(i)').remove();
				$('#profile_'+selNo+'_adv_gop').empty();
				$('#profile_'+selNo+'_adv_gop').val(Math.round($('#profile_'+selNo+'_framerate').val()/2000));

				$('#profile_'+selNo+'_adv_gop').attr('disabled', 'disabled');
				$('#profile_'+selNo+'_gop_range').html('');

				//$('#profile_'+selNo+'_adv_gop').append("<option value="+Math.round($('#profile_'+selNo+'_framerate').val()/2000)+">"+Math.round($('#profile_'+selNo+'_framerate').val()/2000)+"</option>");


				if(type == 'change')
				{
					if($('#profile_'+selNo+'_adv_bitcontrol').val() == 0)//VBR
					{
						if ($('#profile_'+selNo+'_bitrate').val() > record_h264_bitrate)
							$('#profile_'+selNo+'_bitrate').val(record_h264_bitrate);
					}
					else //CBR
					{
						if (pixel > 1280 * 1024)
							if ($('#profile_'+selNo+'_bitrate').val() > record_h264_bitrate) $('#profile_'+selNo+'_bitrate').val(record_h264_bitrate);
					}
					<?php if ($GLOBALS['M_SUPPORT_ENTROPY']) { ?> 
					$('#profile_'+selNo+'_adv_entropy').val(1); //CABAC
					$('#profile_'+selNo+'_adv_entropy').attr('disabled', 'disabled');
					<?php } ?>

				}

			}
			// record profile does not support ATC
			$('#profile_'+selNo+'_atc').val(0);
			$('#profile_'+selNo+'_atc').attr('disabled', 'disabled');
			$('#profile_'+selNo+'_atc_sensitivity').attr('disabled', 'disabled');
			$('#profile_'+selNo+'_atc_limit').attr('disabled', 'disabled');
			//$('#profile_'+selNo+'_adv_gop').removeAttr('disabled');
		}
		else {
			//$('#profile_'+selNo+'_adv_bitcontrol').removeAttr('disabled');
			if(type=='change')
			{
				var oldGopSelectedIndex = $('#profile_'+selNo+'_adv_gop').val();

				$('#profile_'+selNo+'_adv_gop').empty();
				$('#profile_'+selNo+'_adv_gop').val(oldGopSelectedIndex);

				if (parseInt($('#profile_'+selNo+'_codec').val()) == CODEC_H264) {
					var bitrateArr = GetBitrateRange('load');
					var defaultBitrate = bitrateArr[2];
					$('#profile_'+selNo+'_bitrate').val(defaultBitrate);
				}
				
				<?php if ($GLOBALS['M_SUPPORT_ENTROPY']) { ?> 
				if (parseInt($('#profile_'+selNo+'_adv_profile').val()) == 0) {
					$('#profile_'+selNo+'_adv_entropy').attr('disabled', 'disabled');
				} else {
					$('#profile_'+selNo+'_adv_entropy').removeAttr('disabled');
				}
				<?php } ?>
			}

			$('#profile_'+selNo+'_atc').removeAttr('disabled');
			if($('#profile_'+selNo+'_atc').val() == 1)
			{
				$('#profile_'+selNo+'_atc_sensitivity').removeAttr('disabled');
				$('#profile_'+selNo+'_atc_limit').removeAttr('disabled');
			}

			if ($('#profile_'+selNo+'_framerate').val() == 1000)
			{
				$('#profile_'+selNo+'_adv_gop').val(1);
				$('#profile_'+selNo+'_adv_gop').attr('disabled', 'disabled');
				$('#profile_'+selNo+'_gop_range').html('');
			}
			else
			{
				//$('#profile_'+selNo+'_h264'+'_adv_gop').val(15);
				$('#profile_'+selNo+'_adv_gop').removeAttr('disabled');

			}
		}

	}

	function ChangeFramerate(maxFrm, type)
	{	
		var selNo = $("input[name='profile_select']:checked").val();
		var oldFramerateSelectedVal = $('#profile_'+selNo+'_framerate').val();
		$('#profile_'+selNo+'_framerate').empty();
		var msg = '';
		if (type == 'change') oldFramerateSelectedVal = maxFrm*1000;
		for (var index=maxFrm; index>=1; --index) {
			msg = '';
			if (oldFramerateSelectedVal == (index*1000)) msg = ' selected=\"selected\"';
			$('#profile_'+selNo+'_framerate').append("<option value="+(index*1000)+msg+">"+index+" fps </option>");
		}
		if (oldFramerateSelectedVal > (maxFrm*1000) ) $('#profile_'+selNo+'_framerate').val(maxFrm*1000);
	}

	function DisplayBitrateControl()
	{
		var selNo = $("input[name='profile_select']:checked").val();
		var codecType = parseInt($('#profile_'+selNo+'_codec').val());
		var bitrateControlMsg = ["VBR", "CBR", "Off"];

		$('#profile_'+selNo+'_adv_bitcontrol').empty()
		for (var index=0; index<2; ++index) {
			$('#profile_'+selNo+'_adv_bitcontrol').append("<option value="+index+">"+bitrateControlMsg[index]+"</option>");
		}
		if (codecType == CODEC_MJPEG) {
			$('#profile_'+selNo+'_adv_bitcontrol').append("<option value="+index+">"+bitrateControlMsg[2]+"</option>");
		}
	}

	function DisplayGopSize()
	{
		var selNo = $("input[name='profile_select']:checked").val();
		var codecType = parseInt($('#profile_'+selNo+'_codec').val());
		var framerateVal = parseInt($('#profile_'+selNo+'_framerate').val());
		var gopVal = parseInt(framerateVal/2);
		if (gopVal == 0) gopVal = 1;
		var maxGop = 15;
		if (framerateVal == 1) maxGop = 1;

/*
		$('#profile_'+selNo+'_adv_gop').empty()
		switch (codecType) {
			case CODEC_MPEG4:
				for (var index=maxGop; index>=1; --index) {
					$('#profile_'+selNo+'_adv_gop').append("option value="+index+">"+index+"</option>");
				}
				break;
			case CODEC_H264:
				for (var index=maxGop; index>=1; --index) {
					if ($('#profile_'+selNo+'_type_record').is(':checked') && index != gopVal) continue;
					$('#profile_'+selNo+'_adv_gop').append("option value="+index+">"+index+"</option>");
				}

				if ($('#profile_'+selNo+'_type_record').is(':checked')) {
					$('#profile_'+selNo+'_adv_gop').attr('disabled', 'disabled');
				}
				else {
					$('#profile_'+selNo+'_adv_gop').removeAttr('disabled');
				}
				break;
		}

		if (framerateVal == 1) {
			$('#profile_'+selNo+'_adv_gop').attr('disabled', 'disabled');
		}
		else {
			$('#profile_'+selNo+'_adv_gop').removeAttr('disabled');
		}*/
	}

	function OnClickCodec()
	{
		var selNo = $("input[name='profile_select']:checked").val();
		var codecType = parseInt($('#profile_'+selNo+'_codec').val());
		var maxFrm = 30;
		var bitrateArr = GetBitrateRange('load');
		var defaultBitrate = bitrateArr[2];
		
		switch(codecType) {
			case CODEC_MJPEG: {
				$('.profile_'+selNo+'_advanced_codec').hide();
				$('#profile_'+selNo+'_type_event').removeAttr('disabled');
				$('#profile_'+selNo+'_type_default').removeAttr('disabled');
				$('#profile_'+selNo+'_type_record').removeAttr('disabled');
				$('#profile_'+selNo+'_bitrate').val(defaultBitrate);
				<?php if ($GLOBALS['M_SUPPORT_ENTROPY']) { ?> 
				$('.profile_'+selNo+'_adv_profileMode').hide();
				$('.profile_'+selNo+'_adv_entropyCoding').hide();
				<?php } ?>
			} break;
			case CODEC_MPEG4: {
				if (videotype == VIDEOTYPE_NTSC)
					maxFrm = 30
				else
					maxFrm = 25;
				$('.profile_'+selNo+'_advanced_codec').show();
				$('#profile_'+selNo+'_type_event').attr('disabled', 'disabled');
				$('#profile_'+selNo+'_type_default').attr('disabled', 'disabled');
				$('#profile_'+selNo+'_type_record').attr('disabled', 'disabled');
				<?php if ($GLOBALS['M_SUPPORT_ENTROPY']) { ?> 
				$('.profile_'+selNo+'_adv_profileMode').hide();
				$('.profile_'+selNo+'_adv_entropyCoding').hide();
				<?php } ?>
			} break;
			case CODEC_H264: {
			  if(MEGA_MODE == 3) maxFrm = 20;
			  <?php  if ($GLOBALS['M_SUPPORT_SENSOR_FRAMEMODE']) { ?>
					if (sensorFrameMode	== 0)  maxFrm = 60;
					else if (sensorFrameMode	== 1)  maxFrm = 50;
					else if (sensorFrameMode	== 2)  maxFrm = 30;
					else if (sensorFrameMode	== 3)  maxFrm = 25;
				<?php } ?>
				$('.profile_'+selNo+'_advanced_codec').show();
				$('#profile_'+selNo+'_type_event').prop('checked',false);
				$('#profile_'+selNo+'_type_event').attr('disabled', 'disabled');
				$('#profile_'+selNo+'_type_default').removeAttr('disabled');
				$('#profile_'+selNo+'_type_record').removeAttr('disabled');
				$('#profile_'+selNo+'_bitrate').val(defaultBitrate);
				<?php if ($GLOBALS['M_SUPPORT_ENTROPY']) { ?> 
				$('.profile_'+selNo+'_adv_profileMode').show();
				$('.profile_'+selNo+'_adv_entropyCoding').show();
				<?php } ?>
			} break;
			default: break;
		}
		ChangeFramerate(maxFrm);
		OnChangeResolution('load');
		DisplayBitrateControl();
		if(codecType == CODEC_MJPEG)
			DisplayMJPEG_BitrateRange('change');
		else 
			DisplayGopSize();
	}

	function ChangeProfileState()
	{
		var selNo = $("input[name='profile_select']:checked").val();
		var codecType = parseInt($('#profile_'+selNo+'_codec').val());

		//var maxFrm = 30;
		switch(codecType) {
			case CODEC_MJPEG: {
				$('.profile_'+selNo+'_advanced_codec').hide();
				$('#profile_'+selNo+'_type_event').removeAttr('disabled');
				$('#profile_'+selNo+'_type_default').removeAttr('disabled');
				$('#profile_'+selNo+'_type_record').removeAttr('disabled');
			} break;
			case CODEC_MPEG4: {
				//maxFrm = 25;
				$('.profile_'+selNo+'_advanced_codec').show();
				$('#profile_'+selNo+'_type_event').attr('disabled', 'disabled');
				$('#profile_'+selNo+'_type_default').attr('disabled', 'disabled');
				$('#profile_'+selNo+'_type_record').attr('disabled', 'disabled');
			} break;
			case CODEC_H264: {
			  //if(MEGA_MODE == 3) maxFrm = 20;
				$('.profile_'+selNo+'_advanced_codec').show();
				$('#profile_'+selNo+'_type_event').attr('disabled', 'disabled');
				$('#profile_'+selNo+'_type_default').removeAttr('disabled');
				$('#profile_'+selNo+'_type_record').removeAttr('disabled');
			} break;
			default: break;
		}
		//ChangeFramerate(maxFrm);
	}

	function OnClickProfileList()
	{
		var selNo = $("input[name='profile_select']:checked").val();
				
		for (var i=0; i<10; i++) {
			if (i != selNo) $('.profile_'+i+'_setting').hide();
			else $('.profile_'+i+'_setting').show();
		}
		//$('.profile_'+oldSelNo+'_setting').hide();
		//$('.profile_'+selNo+'_setting').show();
		oldSelNo = selNo;
		ChangeProfileState();
		OnClickProfileType('load');

		var selNo = $("input[name='profile_select']:checked").val();
		if ($('#profile_'+selNo+'_type_record').is(':checked')) {
			if (parseInt($('#profile_'+selNo+'_codec').val()) == CODEC_H264) {
			}

			// record profile does not support ATC
			$('#profile_'+selNo+'_atc').val(0);
			$('#profile_'+selNo+'_atc').attr('disabled', 'disabled');
		}
		else {
			$('#profile_'+selNo+'_atc').removeAttr('disabled');
		}
		//DisplayMJPEG_BitrateRange('load');
		OnChangeFrate('load');
		OnChangeBitcontrol('load');
		OnChangeH264ProfileMode();

		//init();
		<?php if ($GLOBALS['M_SUPPORT_SENSOR_FRAMEMODE']) { ?>
		if(parseInt($('#profile_'+selNo+'_codec').val()) == CODEC_H264) {
			GetFramerate();
			if($('#profile_'+selNo+'_name').val() == '') {
				if (sensorFrameMode	== 0)  $('#profile_'+selNo+'_adv_gop').val(60);
				else if (sensorFrameMode	== 1)  $('#profile_'+selNo+'_adv_gop').val(50);
				else if (sensorFrameMode	== 2)  $('#profile_'+selNo+'_adv_gop').val(30);
				else if (sensorFrameMode	== 3)  $('#profile_'+selNo+'_adv_gop').val(25);
			}
		}
		<?php } ?>

		if(test ^ $(".show_advanced_profile").is(':visible'))
		{
	  		$(".show_advanced_profile").toggle();
		}

		cropX = crop_x[selNo];
		cropY = crop_y[selNo];
		cropWidth = crop_width[selNo];
		cropHeight = crop_height[selNo];
		cropRatio = crop_ratio[selNo];
		$('#profile_crop_ratio').val(cropRatio);

		if ($('#profile_'+selNo+'_cropencoding_use').is(':checked'))
		{
			$("#profile_cropencoding_areaset_" + selNo).attr('href', 'javascript:OnClickSetCropArea()');
			$("#profile_cropencoding_areaset_" + selNo).attr('class', 'btn_type01');
		}
		else
		{
			$("#profile_cropencoding_areaset_" + selNo).removeAttr('href');
			$("#profile_cropencoding_areaset_" + selNo).attr('class','btn_disable');
		}
		CheckSmartCodec();
	}

	function OnClickDelete()
	{
		var fixedProfileCnt = parseInt(<?php echo $fixProfileCnt; ?>);
		var selNo = $("input[name='profile_select']:checked").val();
		
		if (selNo < fixedProfileCnt) {
			alert("<?php echo $msg_cannot_delete_profile[$GLOBALS['LANGINDEX']]; ?>");
			return;
		}
		if (profileNameArr[selNo] != '') {
			if (confirm("<?php echo $msg_confirm_remove_profile[$GLOBALS['LANGINDEX']]; ?>")) {
				var msg = '';
				msg += "<RemoveVideoProfile>";
				msg += "<Index>"+selNo+"</Index>";
				msg += "</RemoveVideoProfile>";
				RequestAjaxMsg(msg, "<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, 'REFRESH');
				if (!CheckDeletedTarget('profile'))	return;
			}
		}
		
		//OnClickProfileList();
	}

	function OnChangeFrate(type, command)
	{
		if (typeof command == "undefined")	command = "nonselect";
		var selNo = $("input[name='profile_select']:checked").val();
		var codecType = parseInt($('#profile_'+selNo+'_codec').val());
		var gov_maxratio = <?php echo $GLOBALS['M_GOV_MAXRATIO']; ?>;
		govMax = <?php echo $GLOBALS['M_MAX_GOV']; ?>;
		if ($('#profile_'+selNo+'_framerate').val() /1000 * gov_maxratio < govMax)
			govMax = $('#profile_'+selNo+'_framerate').val() / 1000 * gov_maxratio;
		
		$('#profile_'+selNo+'_gop_range').html('(1 ~ '+govMax+')');
		if ($('#profile_'+selNo+'_adv_gop').val() > govMax) $('#profile_'+selNo+'_adv_gop').val(govMax);
		if(codecType == CODEC_H264)
		{
			if ($('#profile_'+selNo+'_framerate').val() == 1000)
			{
				gopISone = true;
				$('#profile_'+selNo+'_adv_gop').val(1);
				$('#profile_'+selNo+'_adv_gop').attr('disabled', 'disabled');
				$('#profile_'+selNo+'_gop_range').html('');
			}
			else
			{
				if(type == 'change' && gopISone) 
					$('#profile_'+selNo+'_adv_gop').val(govMax);
				$('#profile_'+selNo+'_adv_gop').removeAttr('disabled');
				gopISone = false;

			}

			if ($('#profile_'+selNo+'_type_record').is(':checked')) {

			$('#profile_'+selNo+'_adv_gop').empty();

			$('#profile_'+selNo+'_adv_gop').val(Math.round($('#profile_'+selNo+'_framerate').val()/2000));
			$('#profile_'+selNo+'_adv_gop').attr('disabled', 'disabled');
			$('#profile_'+selNo+'_gop_range').html('');

			<?php if ($GLOBALS['M_SUPPORT_ENTROPY']) { ?>
			$('#profile_'+selNo+'_adv_entropy').val(1); //CABAC
			$('#profile_'+selNo+'_adv_entropy').attr('disabled', 'disabled');
			<?php } ?>
		
			}
			else
			{
				if(command == 'select'){
					$('#profile_'+selNo+'_adv_gop').val($('#profile_'+selNo+'_framerate').val()/1000);
				}
			}
		}
		else if(codecType == CODEC_MPEG4)
		{
			if ($('#profile_'+selNo+'_framerate').val() == 1000)
			{
				$('#profile_'+selNo+'_adv_gop').val(1);
				$('#profile_'+selNo+'_adv_gop').attr('disabled', 'disabled');
			}
			else
			{
				//$('#profile_'+selNo+'_mpeg4'+'_adv_gop').val(15);
				$('#profile_'+selNo+'_adv_gop').removeAttr('disabled');
			}
		}

	}
	function OnChangeATC()
	{
		var selNo = $("input[name='profile_select']:checked").val();

		if ($('#profile_'+selNo+'_atc').val() == 0 || $('#profile_'+selNo+'_atc').val() == 3)
		{
			$('#profile_'+selNo+'_atc_sensitivity').attr('disabled', 'disabled');
			$('#profile_'+selNo+'_atc_limit').attr('disabled', 'disabled');
		}
		else
		{
			$('#profile_'+selNo+'_atc_sensitivity').removeAttr('disabled');
			$('#profile_'+selNo+'_atc_limit').removeAttr('disabled');
		}

		if($('#profile_'+selNo+'_adv_bitcontrol').val() == 1 )//CBR
		{
			if($('#profile_'+selNo+'_atc').val() == 1) //framerate
			{
				$('#profile_'+selNo+'_adv_priority').val(0);
				$('#profile_'+selNo+'_adv_priority').attr('disabled', 'disabled');

			}
			else if ($('#profile_'+selNo+'_atc').val() == 2) //compression
			{
				$('#profile_'+selNo+'_adv_priority').val(1);
				$('#profile_'+selNo+'_adv_priority').attr('disabled', 'disabled');
			}
			else
			{
				$('#profile_'+selNo+'_adv_priority').removeAttr('disabled');
			}
		}
	}
	function OnLoad()
	{
		$("#CGILoading").get(0).style.display = "block";
		oldSelNo = $("input[name='profile_select']:checked").val();
		<?php
		for ($i=0; $i<MAX_PROFILE; $i++)
		{
			if ($profileList->profile[$i]->dataInfo['Default']['value'] == 1)
			{
		?>
				$('#profile_select_<?php echo $i;?>').prop('checked',true);

		<?php
			}
		}
		?>

		OnChangeResolution('load');
		OnChangeH264ProfileMode();
		OnChangeFrate('load');
		OnChangeBitcontrol('load');
		ChangeProfileState();
		<?php if ($GLOBALS['M_SUPPORT_SENSOR_FRAMEMODE']) { ?>
		if(parseInt($('#profile_'+oldSelNo+'_codec').val()) == CODEC_H264)
			GetFramerate();
		<?php } ?>

		<?php if($resolMode == MAX_3_MEGA) { ?>
		if(MEGA_MODE == 2)
  	  $('#profile_megamode_2').prop('checked', true);
  	else
  	  $('#profile_megamode_3').prop('checked', true);
		<?php } ?>

		window.setTimeout("OnLoadComplete()", 1000);

		cropX = crop_x[oldSelNo];
		cropY = crop_y[oldSelNo];
		cropWidth = crop_width[oldSelNo];
		cropHeight = crop_height[oldSelNo];
		cropRatio = crop_ratio[oldSelNo];
		$('#profile_crop_ratio').val(cropRatio)

	<?php
		if($GLOBALS['M_SUPPORT_CROP_ENCODING']) {
	?>
			if ($('#profile_'+oldSelNo+'_cropencoding_use').is(':checked'))
			{
				ApplyCropResolutionList();
			}

			if ($('#profile_'+oldSelNo+'_cropencoding_use').is(':checked'))
			{
				$("#profile_cropencoding_areaset_" + oldSelNo).attr('href', 'javascript:OnClickSetCropArea()');
				$("#profile_cropencoding_areaset_" + oldSelNo).attr('class', 'btn_type01');
			}
			else
			{
				$("#profile_cropencoding_areaset_" + oldSelNo).removeAttr('href');
				$("#profile_cropencoding_areaset_" + oldSelNo).attr('class','btn_disable');
			}
	<?php
		}
	?>
		CheckSmartCodec();
	}

	function OnLoadComplete()
	{
		$("#CGILoading").get(0).style.display = "none";
	}

	function OnClickMegaMode(mode)
	{
	  	if (MEGA_MODE == mode) return;

	  	var msg = "";
	  	var val;
	  	if (mode == 2)
			val = confirm("<?php echo $msg_2megamode_change[$GLOBALS['LANGINDEX']]; ?>");
		else
  	  		val = confirm("<?php echo $msg_3megamode_change[$GLOBALS['LANGINDEX']]; ?>");

	  	if(val == true)
	  	{
	  		msg += "<SetVideoSourceSelection>";
	  		msg += "<VideoSource>" + mode + "</VideoSource>";
	  		msg += "</SetVideoSourceSelection>";
			RequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, 'NO_REFRESH', true, OnSuccessChangeMegaMode);
	  	}
	  	else
	  	{
	  	  if (mode == 2)
	  	  {
			  $("#profile_megamode_2").prop('checked', false);
			  $("#profile_megamode_3").prop('checked', true);
			}
			else
			{
			  $("#profile_megamode_3").prop('checked', false);
			  $("#profile_megamode_2").prop('checked', true);
			}
	  	}
	}

	function OnSuccessChangeMegaMode()
	{
		$("#profile_megamode_2").attr('disabled', 'disabled');
		$("#profile_megamode_3").attr('disabled', 'disabled');
		$("#CGILoading").get(0).style.display = "block";
		window.setTimeout('OnSuccessChangeMegaModeDone()', 10000);
	}

	function OnSuccessChangeMegaModeDone()
	{
		window.location.reload(true);
	}

	function OnClickConnectionPolicy()
	{
		if ($('#profile_rtpdisconnect').is(':checked'))
			popUpMsg = "<?php echo $msg_change_setting[$GLOBALS['LANGINDEX']]; ?>";
		else
			popUpMsg = "<?php echo $msg_change_connection_policy[$GLOBALS['LANGINDEX']]; ?>";

		var res = confirm(popUpMsg);
		if(res == true)
	  	{
	  		var msg = "";
			msg += "<SetStreammingDisconnection>";
	  		msg += "<Enabled>" + ($('#profile_rtpdisconnect').is(':checked') ? 0 : 1) + "</Enabled>";
	  		msg += "</SetStreammingDisconnection>";
	  		RequestAjaxMsg(msg, "", "<?php echo $GLOBALS['REQUEST_URI']; ?>" + "?seq=" + localSeq, 'REFRESH', true);
		}
		else
		{
			if ($('#profile_rtpdisconnect').is(':checked'))
				$('#profile_rtpdisconnect').prop('checked', false);
			else
				$('#profile_rtpdisconnect').prop('checked', true);
		}
	}

	function UnLoad()
	{
		var currProfile = $(".Profile_select:checked").val();
		$('#profile_select_'+currProfile).prop('checked',false);
	}

	// ---------------------------
	// CROP AREA SETTING FUNCTIONS
	// ---------------------------
	function CheckSmartCodec() 
	{
		var selNo = $("input[name='profile_select']:checked").val();
		if ($('#profile_'+selNo+'_adv_bitcontrol').val() == 1) { //CBR
			if ($('#profile_'+selNo+'_cropencoding_use').is(':checked'))
				$('#profile_'+selNo+'_h264_adv_smart').attr('disabled', 'disabled');
			else
				$('#profile_'+selNo+'_h264_adv_smart').removeAttr('disabled');
		}
	}
	
	function OnClickUseCrop()
	{
		if ($('#profile_'+oldSelNo+'_cropencoding_use').is(':checked'))
		{
			ApplyCropResolutionList();

			var selNo = $("input[name='profile_select']:checked").val();
			for(var i = 0 ; i < $('#profile_'+selNo+'_resolution option').size() ; i++)
			{
				if(!$('#profile_'+selNo+'_resolution option:eq('+i+')').is(':disabled'))
				{
					$('#profile_'+selNo+'_resolution option:eq('+i+')').prop('selected', true);
					break;
				}
			}
			OnClickProfileType('change');
		}
		else
		{
			var selNo = $("input[name='profile_select']:checked").val();
			var temp_option = 0;
			if (browserName == 'IE' && ieVer <= 7)
				temp_option = $('#profile_'+selNo+'_resolution option').size() + $('#profile_'+selNo+'_resolution optgroup').size();
			else
				temp_option = $('#profile_'+selNo+'_resolution option').size();
			
			for(var i = 0 ; i < temp_option ; i++) {
				ChangeOption('profile_'+selNo+'_resolution', i, 'Enable');
			}

			if (browserName == 'IE' && ieVer <= 7) {
				document.getElementById('profile_'+selNo+'_resolution').style.display ='none';
				document.getElementById('profile_'+selNo+'_resolution').style.display ='';
			}
		}
		
		// --- to do : get setting value. if use crop is on, enable set area button. Otherwise disable it.
		if ($('#profile_'+oldSelNo+'_cropencoding_use').is(':checked'))
		{
			$("#profile_cropencoding_areaset_" + oldSelNo).attr('href', 'javascript:OnClickSetCropArea()');
			$("#profile_cropencoding_areaset_" + oldSelNo).attr('class', 'btn_type01');
		}
		else
		{
			$("#profile_cropencoding_areaset_" + oldSelNo).removeAttr('href');
			$("#profile_cropencoding_areaset_" + oldSelNo).attr('class','btn_disable');
		}
		CheckSmartCodec();
	}

	function ApplyCropResolutionList()
	{
		var selNo = $("input[name='profile_select']:checked").val();
		cropRatio = $('#profile_crop_ratio').val();

<?php	if ($GLOBALS['M_MAX_RESOLUTION'] == MAX_1_MEGA) { ?>
			var widthArray = [1280, 1280, 1024, 800, 	640, 	320];
			var heightArray = [1024, 720, 	768, 	600, 	480, 	240];
<?php } else if ($GLOBALS['M_MAX_RESOLUTION'] == MAX_2_MEGA || ($GLOBALS['M_MAX_RESOLUTION'] == MAX_3_MEGA && $classInstances['Information']->dataInfo['MegaMode']['value'] == 2)) { ?>	
			var widthArray = [1920, 1280, 800, 640, 320, 1280, 1280, 1024, 800, 640, 320];
	<?php if($GLOBALS['M_SPECIAL_TYPE'] == 1) {   ?>
			var heightArray = [1080, 720, 450, 360, 180, 1024, 960, 768, 600, 360, 240];
	<?php } else {	?>
			var heightArray = [1080, 720, 450, 360, 180, 1024, 960, 768, 600, 480, 240];
	<?php } 	?>
<?php	} else if ($GLOBALS['M_MAX_RESOLUTION'] == MAX_3_MEGA) { ?>
			var widthArray = [2048, 1600, 1280, 1024, 800, 640, 320, 1280, 1920, 1280, 800, 640, 320];
			var heightArray = [1536, 1200, 960, 768, 600, 480, 240, 1024, 1080, 720, 450, 360, 180];
<?php } ?>
		
		if ($('#profile_'+selNo+'_cropencoding_use').is(':checked'))
		{				
			for(var i = 0 ; i < widthArray.length ; i++)
			{
				var optionValue = 'Enable';
				if(cropWidth < widthArray[i] || cropHeight < heightArray[i]) {
					optionValue = 'Disable';
				}
			
				if (MEGA_MODE > 1) {
					if (cropRatio == 0) {	// 16:9
						if ((MEGA_MODE == 3 && i < 8) || (MEGA_MODE != 3 && i > 4)) {
							optionValue = 'Disable';
						}	
					}
					else if (cropRatio == 1) {	// 4:3
						if ((MEGA_MODE == 3 && i > 6) || (MEGA_MODE != 3 && i < 5)) {
							optionValue = 'Disable';
						}
					}
				}
				ChangeOption('profile_'+selNo+'_resolution', i, optionValue);
			}
			
			if (browserName == 'IE' && ieVer <= 7) {
				document.getElementById('profile_'+selNo+'_resolution').style.display ='none';
				document.getElementById('profile_'+selNo+'_resolution').style.display ='';
			}
		}
	}

	function OnClickSetCropArea()
	{
		wrapWindowByMask();
		$('#profile_crop_ratio').val(cropRatio);
		DrawCropArea();
	}

	function DrawCropArea()
	{
		var selNo = $("input[name='profile_select']:checked").val();
		var previewProfileNo = <?php echo $classInstances['Information']->dataInfo['PreviewProfileNo']['value']; ?> + 1;		

		var devicePort = "<?php echo $classInstances['Information']->dataInfo['DevicePort']['value']; ?>";
		if (MEGA_MODE == 2) {
			var viewerWidth = 640;
			var viewerHeight = 360;
		}else {
			var viewerWidth = 640;
			var viewerHeight = 480;
		}

		if (cropX % 2 != 0) cropX--;
		if (cropY % 2 != 0) cropY--;
		if (cropWidth % 2 != 0) cropWidth--;
		if (cropHeight % 2 != 0) cropHeight--;

		// --- give current profile's crop area values to Silverlight
		if (MEGA_MODE == 2) {
			var halfX = 1920 / 2;
			var halfY = 1080 / 2;
		}else if (MEGA_MODE == 3) {
			var halfX = 2048 / 2;
			var halfY = 1536 / 2;
		}else {
			var halfX = 1280 / 2;
			var halfY = 1024 / 2;
		}

		var X1 = cropX;
		var Y1 = cropY;
		var X2 = cropX + cropWidth;
		var Y2 = cropY + cropHeight;
		if (mirror)
		{
			if (X1 >= halfX)
				X1 = halfX - (X1 - halfX);
			else
				X1 = halfX + (halfX - X1);

			if (X2 >= halfX)
				X2 = halfX - (X2 - halfX);
			else
				X2 = halfX + (halfX - X2);
		}
		if (flip)
		{
			if (Y1 >= halfY)
				Y1 = halfY - (Y1 - halfY);
			else
				Y1 = halfY + (halfY - Y1);

			if (Y2 >= halfY)
				Y2 = halfY - (Y2 - halfY);
			else
				Y2 = halfY + (halfY - Y2);
		}

		if (mirror)
		{
			var tmp = X1;
			X1 = X2;
			X2 = tmp;
		}
		if (flip)
		{
			var tmp = Y1;
			Y1 = Y2;
			Y2 = tmp;
		}
		var width = X2 - X1;
		var height = Y2 - Y1;

		cropEncoding.drawing.setArea(X1, Y1, width, height);
	}

	function OnClickCrop(mode)
	{
		SISOPlugin.stop();
		$('#mask, .window').hide();
		if (mode == 'Apply') {
			// --- to do : get crop encoding setting values
			// --- GetImageAreaValue(value) value param : 0:x, 1:y, 2:width, 3:height
			var cropArea = cropEncoding.drawing.getArea();
			
			cropX = parseInt(cropArea[0], 10);
			cropY = parseInt(cropArea[1], 10);
			cropWidth = parseInt(cropArea[2], 10);
			cropHeight = parseInt(cropArea[3], 10);

			if (cropX % 2 != 0) cropX--;
			if (cropY % 2 != 0) cropY--;
			if (cropWidth % 2 != 0) cropWidth--;
			if (cropHeight % 2 != 0) cropHeight--;

			if (parseInt(cropX) < 0 ) {
				cropX = 0;
			}
			if (parseInt(cropY) < 0) {
				cropY = 0;
			}
			if (parseInt(cropWidth) > 1280) {
				cropWidth = 1280;
			}
			if (parseInt(cropHeight) > 1024) {
				cropHeight = 1024;
			}			
			
			<?php if ($resolMode == MAX_2_MEGA || $classInstances['Information']->dataInfo['MegaMode']['value'] == 2) { ?>	
				var halfX = 1920 / 2;
				var halfY = 1080 / 2;
				<?php } else if ($resolMode == MAX_3_MEGA && $classInstances['Information']->dataInfo['MegaMode']['value'] == 3) { ?>
				var halfX = 2048 / 2;
				var halfY = 1536 / 2;
				<?php } else { ?>
				var halfX = 1280 / 2;
				var halfY = 1024 / 2;
			<?php } ?>
			
			var X1 = cropX;
			var Y1 = cropY;
			var X2 = cropX + cropWidth;
			var Y2 = cropY + cropHeight;

			if (mirror)
			{
				if (X1 >= halfX)
					X1 = halfX - (X1 - halfX);
				else
					X1 = halfX + (halfX - X1);

				if (X2 >= halfX)
					X2 = halfX - (X2 - halfX);
				else
					X2 = halfX + (halfX - X2);
			}
			if (flip)
			{
				if (Y1 >= halfY)
					Y1 = halfY - (Y1 - halfY);
				else
					Y1 = halfY + (halfY - Y1);

				if (Y2 >= halfY)
					Y2 = halfY - (Y2 - halfY);
				else
					Y2 = halfY + (halfY - Y2);
			}

			if (mirror)
			{
				var tmp = X1;
				X1 = X2;
				X2 = tmp;
			}
			if (flip)
			{
				var tmp = Y1;
				Y1 = Y2;
				Y2 = tmp;
			}
			var width = X2 - X1;
			var height = Y2 - Y1;

			cropX = X1;
			cropY = Y1;
			cropWidth = X2 - X1;
			cropHeight = Y2 - Y1;
			crop_set = 1;
		
			if ($('#profile_'+oldSelNo+'_cropencoding_use').is(':checked'))
			{
				ApplyCropResolutionList();

				var selNo = $("input[name='profile_select']:checked").val();
				for(var i = 0 ; i < $('#profile_'+selNo+'_resolution option').size() ; i++)
				{
					if(!$('#profile_'+selNo+'_resolution option:eq('+i+')').is(':disabled'))
					{
						$('#profile_'+selNo+'_resolution option:eq('+i+')').prop('selected', true);
						break;
					}
				}
				OnClickProfileType('change');
			}
		}
	}
	
	function OnChangeCropRatio()
	{
		var val = $('#profile_crop_ratio').val();
	<?php if ($GLOBALS['M_MAX_RESOLUTION'] == MAX_3_MEGA && $GLOBALS['MEGAMODE'] == 3) { ?>	
		cropX = 384;
      cropY = 256;
	<?php }else if(($GLOBALS['M_MAX_RESOLUTION'] == MAX_3_MEGA && $GLOBALS['MEGAMODE'] == 2) || $GLOBALS['M_MAX_RESOLUTION'] == MAX_2_MEGA) { ?>
		cropX = 320;
		cropY = 28;
	<?php } else if ($GLOBALS['M_MAX_RESOLUTION'] == MAX_1_MEGA) { ?>
		cropX = 128;
      cropY = 128;	
	<?php } else { ?>
		cropX = 0;
      cropY = 0;
	<?php } ?>
			
		if (val == 0)
		{
			cropWidth = 1280;
			cropHeight = 720;
		}
		else if (val == 1)
		{
		<?php if ($GLOBALS['M_MAX_RESOLUTION'] == MAX_2_MEGA || $GLOBALS['M_MAX_RESOLUTION'] == MAX_3_MEGA) { ?>	
			cropWidth = 1280;
			cropHeight = 960;
		<?php } else { ?>
			cropWidth = 1024;
			cropHeight = 768;
		<?php } ?>
		}
		else
		{
		<?php if ($GLOBALS['M_MAX_RESOLUTION'] == MAX_1_MEGA) { ?>
			cropWidth = 1024;
			cropHeight = 768;
		<?php } else { ?>
			cropWidth = 1280;
			cropHeight = 1024;
		<?php } ?>
		}
		cropRatio = val;
		cropEncoding.drawing.setArea(cropX, cropY, cropWidth, cropHeight);
	}

	function GetFramerate() { // sensorFramemode
		if (sensorFrameMode == 0) ChangeFramerate(60);
		else if (sensorFrameMode == 1) ChangeFramerate(50);
		else if (sensorFrameMode == 2) ChangeFramerate(30);
		else if (sensorFrameMode == 3) ChangeFramerate(25);
	}

	</script>
</head>
<body onload="OnLoad()" onunload="UnLoad()" onselectstart="return false">
	<div id="CGILoading" style="position:absolute; width:800px; height:1200px; left: 300px; top: 150px; background-color:#000000; display:block; z-index:1000">
		<p align="center">
			<br /> <br /> <br /> <br /> <br /> <br /> <br /> <br /> <br /> <br />
			<img src="../images/common/cgi_loading.gif" />
		</p>
	</div>

	<div id="mask">
	</div>
	<div class="window">
		<div id="window_crop_contents" style="width:650px;">
			<div class="h3_tit mgt0" >
				<h3 class="wid220"><?php echo $t_cropencoding[$GLOBALS['LANGINDEX']]; ?></h3>
			</div>
			<!-- Webviewer -->
			<table class="data_write" style="width:330px;margin-bottom:5px;">
				<tbody>
					<tr>
						<th class="top_txt" style="width:100px"><?php echo $t_ratio[$GLOBALS["LANGINDEX"]]; ?></th>
						<td>
							<select id="profile_crop_ratio" class="selectbox_style_wid260" onchange="OnChangeCropRatio()">
							  <?php if ($GLOBALS['M_MAX_RESOLUTION'] >= MAX_2_MEGA) { ?>
							  <option value="0">16:9</option>
							  <?php } ?>
							  <option value="1">4:3</option>
							  <option value="2"><?php echo $t_manual[$GLOBALS['LANGINDEX']]; ?></option>
							</select>
						</td>
					</tr>
				</tbody>
			</table>
			<?php if($GLOBALS['M_MAX_RESOLUTION'] == MAX_2_MEGA || $GLOBALS['MEGAMODE'] == 2) { ?>
			<div style="text-align:center; background-color:#2B313E; width:640px; height:360px; margin-left:10px; margin-bottom:10px" >
				<span id="pluginArea" style="position: absolute;left:15px; width: 640px; height: 360px;background-color:black"></span>				
				<div id="cropDraw" style="position: absolute;left:15px;">
					<canvas id="cropCanvas" width="640" height="360"></canvas>
					<?php if(GetBrowserName() == 'IE' && ieversion() <= 8) { ?>
					<span style="position: absolute;left:0px; width: 640px; height: 360px; background:#000;opacity:0;filter:alpha(opacity=0);"></span> 
					<?php } ?>						
					<canvas id="cropCanvasTemp" width="640" height="360" style="position: absolute;top:0px;left:0px;z-index:1000"></canvas>
				</div>
			<?php } else { ?>
			<div style="text-align:center; background-color:#2B313E; width:640px; height:480px; margin-left:10px; margin-bottom:10px" >
				<span id="pluginArea" style="position: absolute;left:15px; width: 640px; height: 480px;background-color:black"></span>				
				<div id="cropDraw" style="position: absolute;left:15px;">
					<canvas id="cropCanvas" width="640" height="480"></canvas>
					<?php if(GetBrowserName() == 'IE' && ieversion() <= 8) { ?>
					<span style="position: absolute;left:0px; width: 640px; height: 480px; background:#000;opacity:0;filter:alpha(opacity=0);"></span> 
					<?php } ?>						
					<canvas id="cropCanvasTemp" width="640" height="480" style="position: absolute;top:0px;left:0px;z-index:1000"></canvas>
				</div>
			
			<?php } ?>
			</div>
			<div style="color:#fff;margin-left:10px;"><span id="span_cropsize"></span></div>
			<!-- Button -->
			<div class="right_btn">
				<a id="window_crop_mid_ok_btn" class="btn_apply" href="javascript:OnClickCrop('Apply')"><?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?></a>&nbsp;
				<a id="window_crop_mid_cancel_btn" class="btn_apply" href="javascript:OnClickCrop('Cancel')"><?php echo $t_cancel[$GLOBALS['LANGINDEX']]; ?></a>
			</div>
		</div>
	</div>

	<div id="wrap">
		<?php
			require_once ('left_menu.cgi');
			require_once ('top_menu.cgi');
		?>
		<div id="container">
		<?php
			PrintLeftMenu($_SERVER['SCRIPT_NAME']);
		?>
			<div id="contents" >

		<?php
			if($GLOBALS['M_SUPPORT_MEGAMODE']) {
		?>
			<div class="h3_tit mgt0">
					<h3 class="wid320"><?php echo $t_megamode[$GLOBALS['LANGINDEX']]; ?></h3>
					<table class="data_write">
					<tr><td height="50px">
					<div class="input_box" >
						<label><input type="radio" name="profile_megamode" id="profile_megamode_2" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" onclick="javascript:OnClickMegaMode(2)" /><?php echo $t_2mega[$GLOBALS['LANGINDEX']]; ?></label>
						<label><input type="radio" name="profile_megamode" id="profile_megamode_3" onclick="javascript:OnClickMegaMode(3)"/><?php echo $t_3mega[$GLOBALS['LANGINDEX']]; ?></label>
					</div>
					</td></tr>
					</table>
				</div>

		<?php
			}
		?>

				<div class="h3_tit" style="<?php if($GLOBALS['M_SUPPORT_MEGAMODE']) echo 'padding-top:15px;'; else echo 'margin-top:0px;';?>" >
					<h3 class="wid320"><?php echo $t_rtpconnection[$GLOBALS['LANGINDEX']]; ?></h3>
					<table class="data_write">
					<tr><td height="50px">
					<div class="input_box" style="width:500px;">
						<label><input type="checkbox" id="profile_rtpdisconnect" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" onclick="javascript:OnClickConnectionPolicy()" <?php if ($streamingDisconnection->dataInfo['Enabled']['value']==0) echo "checked=\"checked\"";?> /><?php echo $t_rtpconnection_disconnect[$GLOBALS['LANGINDEX']]; ?></label>
					</div>
					</td></tr>
					</table>
				</div>
				<div class="h3_tit" style="<?php if($GLOBALS['M_SUPPORT_MEGAMODE']) echo 'padding-top:15px;'; else echo 'margin-top:65px;';?>" >
					<h3><?php echo $menu_videoprofile[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>
				<table id="profile_list" class="data_table2" style="width:680px">
					<colgroup>
						<col style="width:27px;" />
						<col style="width:123px;" />
						<col style="width:133px;" />
						<col />
					</colgroup>
					<thead>
						<tr>
							<th></th>
							<th><?php echo $t_name[$GLOBALS['LANGINDEX']]; ?></th>
							<th><?php echo $t_codec[$GLOBALS['LANGINDEX']]; ?></th>
							<th><?php echo $t_type[$GLOBALS['LANGINDEX']]; ?></th>
						</tr>
					</thead>
					<tbody>
				<?php
				    $profileCnt = 0;
				    $encodingStr = array('MJPEG', 'MPEG-4', 'H.264');						
				    $typeStr = array($t_default[$GLOBALS['LANGINDEX']], $t_event[$GLOBALS['LANGINDEX']], $t_record[$GLOBALS['LANGINDEX']]);
				    $addProfileNum = -1;
				    for ($index=0; $index<MAX_PROFILE; ++$index) {
				    	if ($profileList->profile[$index]->dataInfo['Name']['value'] == '') {
				    		if ($addProfileNum == -1)  		$addProfileNum = $index;
				    		$profileCnt++;
				    		continue;
				    	}
				    	$typeVals = array($profileList->profile[$index]->dataInfo['Default']['value'], $profileList->profile[$index]->dataInfo['EventProfile']['value'], $profileList->profile[$index]->dataInfo['RecordProfile']['value']);
						$profileType = '';
						for ($index2=0; $index2<count($typeStr); ++$index2) {
							if (!($GLOBALS['M_SUPPORT_SD'] || $GLOBALS['M_SUPPORT_NAS']) && $index2 == 2) continue;
							if ($typeVals[$index2] == 1) $profileType .= $typeStr[$index2].' / ';
						}
						if ($profileType != '') $profileType = substr($profileType, 0, -2);
        		?>
						<tr class="profile_list_<?php echo $profileCnt.$addProfileNum; ?>" >
							<td><input type="radio" class= "Profile_select" name="profile_select" id="profile_select_<?php echo $profileCnt; ?>" onClick="OnClickProfileList();ApplyCropResolutionList();" value="<?php echo $profileCnt; ?>" <?php if ($profileList->profile[$index]->dataInfo['Default']['value'] == 1) echo "checked=\"checked\""; ?> /></td>
      					<td><label for="profile_select_<?php echo $profileCnt; ?>"><?php echo $profileList->profile[$index]->dataInfo['Name']['value']; ?>&nbsp;</label></td>
							<td><?php echo $encodingStr[$profileList->profile[$index]->dataInfo['Encoding']['value']]; ?></td>
							<td><?php echo $profileType; ?></td>
						</tr>
				<?php
						$profileCnt++;
					}

					if ($addProfileNum != -1) {
				?>
						<tr class="profile_list_<?php echo $addProfileNum; ?>">
							<td><input type="radio" name="profile_select" id="profile_select_<?php echo $addProfileNum; ?>" onClick="OnClickProfileList();" value="<?php echo $addProfileNum; ?>"/></td>
      					<td></td>
							<td></td>
							<td></td>
						</tr>

				<?php
					}
				?>
					<script>profile_cnt = <?php echo $profileCnt; ?>;</script>
					</tbody>
				</table>
				<div class="btn_add_left">
					<a id="mid_del_btn" class="btn_type01" href="javascript:OnClickDelete()"><?php echo $t_delete[$GLOBALS['LANGINDEX']]; ?></a>
				</div>
				<br/>
			<?php
				$videoType = $classInstances['Information']->dataInfo['VideoType']['value'];
				$megaMode = $classInstances['Information']->dataInfo['MegaMode']['value'];
				$resolArr = array();
				$resolArr2 = array();
				if ($resolMode == MAX_3_MEGA) {
					if ($megaMode == 3) {
						$resolArr = array('2048 X 1536 (4:3)', '1600 X 1200 (4:3)', '1280 X 960 (4:3)', '1024 X 768 (4:3)', '800 X 600 (4:3)', '640 X 480 (4:3)', '320 X 240 (4:3)',
														'1280 X 1024 (5:4)', '1920 X 1080 (16:9)', '1280 X 720 (16:9)', '800 X 450 (16:9)', '640 X 360 (16:9)', '320 X 180 (16:9)');
						$resolArr2 = array('2048 X 1536', '1600 X 1200', '1280 X 960', '1024 X 768', '800 X 600', '640 X 480', '320 X 240',
													'1280 X 1024', '1920 X 1080', '1280 X 720', '800 X 450', '640 X 360', '320 X 180');
						if ($GLOBALS['M_MODEL_GROUP'] == MF_7010FE) {
							$resolArr = array('2048 X 1536 (4:3)', '1600 X 1200 (4:3)', '1280 X 960 (4:3)', '1024 X 768 (4:3)', '800 X 600 (4:3)', '640 X 480 (4:3)', '320 X 240 (4:3)');
							$resolArr2 = array('2048 X 1536', '1600 X 1200', '1280 X 960', '1024 X 768', '800 X 600', '640 X 480', '320 X 240');
						}
					}
					else {
						$resolArr = array('1920 X 1080 (16:9)', '1280 X 720 (16:9)', '800 X 450 (16:9)', '640 X 360 (16:9)', '320 X 180 (16:9)', '1280 X 1024 (5:4)',
														'1280 X 960 (4:3)', '1024 X 768 (4:3)', '800 X 600 (4:3)', '640 X 480 (4:3)', '320 X 240 (4:3)');
						$resolArr2 = array('1920 X 1080', '1280 X 720', '800 X 450', '640 X 360', '320 X 180', '1280 X 1024',
													'1280 X 960', '1024 X 768', '800 X 600', '640 X 480', '320 X 240');
					}
				}
				else if ($resolMode == MAX_2_MEGA) {
					if($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_HISILICON) {
						if($GLOBALS['M_SPECIAL_TYPE'] == 1) {
							$resolArr = array('1920 X 1080 (16:9)', '1280 X 960 (4:3)', '1280 X 720 (16:9)', '1024 X 768 (4:3)', 
						                  '800 X 600 (4:3)', '720 X 576 (5:4)', '640 X 360 (16:9)', '320 X 240 (4:3)');
						    	$resolArr2 = array('1920 X 1080', '1280 X 960', '1280 X 720', '1024 X 768', 
						                   '800 X 600', '720 X 576', '640 X 360', '320 X 240');           
						}
						else {
							$resolArr = array('1920 X 1080 (16:9)', '1280 X 960 (4:3)', '1280 X 720 (16:9)', '1024 X 768 (4:3)', 
						                  '800 X 600 (4:3)', '720 X 576 (5:4)', '640 X 480 (4:3)', '320 X 240 (4:3)');
						      	$resolArr2 = array('1920 X 1080', '1280 X 960', '1280 X 720', '1024 X 768', 
						                   '800 X 600', '720 X 576', '640 X 480', '320 X 240');      
						}

					}
					else if ($GLOBALS['M_MODEL_GROUP'] == MF_6321)
					{
						$resolArr = array('1920 X 1080 (16:9)', '1280 X 720 (16:9)', '800 X 450 (16:9)', '640 X 360 (16:9)', '320 X 180 (16:9)', '1280 X 1024 (5:4)', '720 X 576 (5:4)',
															'1280 X 960 (4:3)', '1024 X 768 (4:3)', '800 X 600 (4:3)', '640 X 480 (4:3)', '320 X 240 (4:3)');
						$resolArr2 = array('1920 X 1080', '1280 X 720', '800 X 450', '640 X 360', '320 X 180', '1280 X 1024', '720 X 576',
														'1280 X 960', '1024 X 768', '800 X 600', '640 X 480', '320 X 240');
					}
					else
					{
						$resolArr = array('1920 X 1080 (16:9)', '1280 X 720 (16:9)', '800 X 450 (16:9)', '640 X 360 (16:9)', '320 X 180 (16:9)', '1280 X 1024 (5:4)',
															'1280 X 960 (4:3)', '1024 X 768 (4:3)', '800 X 600 (4:3)', '640 X 480 (4:3)', '320 X 240 (4:3)');
						$resolArr2 = array('1920 X 1080', '1280 X 720', '800 X 450', '640 X 360', '320 X 180', '1280 X 1024',
														'1280 X 960', '1024 X 768', '800 X 600', '640 X 480', '320 X 240');
						
						if ($GLOBALS['M_MODEL_NAME'] == "SNP-6320RH") 
						{
							$resolArr = array('1920 X 1080 (16:9)', '1280 X 720 (16:9)', '640 X 360 (16:9)', '320 X 180 (16:9)', '1280 X 1024 (5:4)', '720 X 576 (5:4)',   
														'1280 X 960 (4:3)', '1024 X 768 (4:3)', '800 X 600 (4:3)', '640 X 480 (4:3)', '320 X 240 (4:3)');
							$resolArr2 = array('1920 X 1080', '1280 X 720', '640 X 360', '320 X 180', '1280 X 1024', '720 X 576',   
														'1280 X 960', '1024 X 768', '800 X 600', '640 X 480', '320 X 240');	
					 	} 
					}
				}
				else if ($resolMode == MAX_1_MEGA) {
					if($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_HISILICON) {
						$resolArr = array('1280 X 1024 (5:4)', '1280 X 960 (4:3)','1280 X 720 (16:9)', '1024 X 768 (4:3)', '800 X 600 (4:3)', '720 X 576 (5:4)', '640 X 480 (4:3)' ,'320 X 240 (4:3)');
						$resolArr2 = array('1280 X 1024', '1280 X 960', '1280 X 720', '1024 X 768', '800 X 600', '720 X 576', '640 X 480' ,'320 X 240');
					}else{
						$resolArr = array('1280 X 1024 (5:4)', '1280 X 720 (16:9)', '1024 X 768 (4:3)', '800 X 600 (4:3)', '640 X 480 (4:3)' ,'320 X 240 (4:3)');
						$resolArr2 = array('1280 X 1024', '1280 X 720', '1024 X 768', '800 X 600', '640 X 480' ,'320 X 240');
					}
				}
				else if ($resolMode == MAX_4CIF) {
					if ($videoType == VIDEOTYPE_NTSC) {
						$resolArr = array('704 X 480', '640 X 480', '352 X 240' ,'320 X 240');
					}
					else {
						$resolArr = array('704 X 576', '640 X 480', '352 X 288' ,'320 X 240');
					}
				}
				else if ($resolMode == MAX_VGA) {
					$resolArr = array('640 X 480', '320 X 240', '160 X 120');
				}
			?>

		<?php
			$profileCnt = 0;
			$addProfileArea = '';
			for ($index=0; $index<MAX_PROFILE; ++$index) {

				if ($profileList->profile[$index]->dataInfo['Name']['value'] == '') {
					if ($addProfileArea == '') 	$addProfileArea = 'profile_'.$profileCnt.'_add';
					else {
						$profileCnt++;
						continue;
					}
				}
				else {
					$addProfileArea = '';
				}

				$encoding = $profileList->profile[$index]->dataInfo['Encoding']['value'];
				if ($profileList->profile[$index]->dataInfo['Name']['value'] == '') $encoding = 2;
		?>
				<div class="profile_<?php echo $profileCnt; ?>_setting <?php echo $addProfileArea; ?>" <?php if ($profileList->profile[$index]->dataInfo['Default']['value']!=1) echo "style=\"display:none\""; ?> >
					<table class="data_write">
						<colgroup>
							<col style="width:225px;" />
							<col />
						</colgroup>
						<tbody>
							<tr>
								<th scope="row"><?php echo $t_name[$GLOBALS['LANGINDEX']]; ?></th>
								<td><input type="text" id="profile_<?php echo $profileCnt; ?>_name" class="text" value="<?php echo $profileList->profile[$index]->dataInfo['Name']['value'];?>" style="width:257px;"  onkeypress="IsNumChar(event);" onkeydown="CheckKorean(event);"   maxlength="15" <?php if ($index < $fixProfileCnt) echo "disabled=\"disabled\""; ?> /></td>
							</tr>
							<script>
								profileNameArr[<?php echo $profileCnt;?>] = "<?php echo $profileList->profile[$index]->dataInfo['Name']['value']; ?>";
							</script>
							<tr>
								<th scope="row"><?php echo $t_codec[$GLOBALS['LANGINDEX']]; ?></th>
								<td>
									<select id="profile_<?php echo $profileCnt; ?>_codec" class="selectbox_style_wid260" onchange="OnClickCodec()" <?php if ($index < $fixProfileCnt) echo "disabled=\"disabled\""; ?>>
									  <option value="0" <?php if ($encoding==0) echo "selected=\"selected\"";?> >MJPEG</option>
								<?php
									if ($GLOBALS['M_SUPPORT_VIDEOCODEC'] & VIDEOCODEC_MASK_MPEG4) {
								?>
									  <option value="1" <?php if ($encoding==1) echo "selected=\"selected\"";?> >MPEG-4</option>
								<?php
									}
								?>
									  <option value="2" <?php if ($encoding==2) echo "selected=\"selected\"";?> >H.264</option>
									</select>
								</td>
							</tr>
							<tr>
								<th scope="row" class="top_txt"><?php echo $t_profileType[$GLOBALS['LANGINDEX']]; ?></th>
								<td>
									<label><input type="checkbox" id="profile_<?php echo $profileCnt; ?>_type_default" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" <?php if ($profileList->profile[$index]->dataInfo['Default']['value']==1) echo "checked=\"checked\"";?> onclick="OnClickProfileType('load');"/><?php echo $t_defaultProfile[$GLOBALS['LANGINDEX']]; ?></label><br/>
									<label><input type="checkbox" id="profile_<?php echo $profileCnt; ?>_type_event" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" <?php if ($profileList->profile[$index]->dataInfo['EventProfile']['value']==1) echo "checked=\"checked\"";?> onclick="OnClickProfileType('change');"/><?php echo $t_emailFtpProfile[$GLOBALS['LANGINDEX']]; ?></label><br/>
							<?php
								if ( ($GLOBALS['M_SUPPORT_SD'] || $GLOBALS['M_SUPPORT_NAS'])) {
							?>
									<label><input type="checkbox" id="profile_<?php echo $profileCnt; ?>_type_record" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" <?php if ($profileList->profile[$index]->dataInfo['RecordProfile']['value']==1) echo "checked=\"checked\"";?> onclick="OnClickProfileType('change');"/><?php echo $t_recordProfile[$GLOBALS['LANGINDEX']]; ?></label>
							<?php
								}
							?>
								</td>
							</tr>
							<?php
								if($GLOBALS['M_SUPPORT_AUDIO']) {
							?>
							<tr>
								<th scope="row" class="top_txt"><?php echo  $t_audioIn[$GLOBALS['LANGINDEX']]; ?></th>
								<td>
									<label><input type="checkbox" id="profile_<?php echo $profileCnt; ?>_audioIn" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" <?php if ($profileList->profile[$index]->dataInfo['UseAudioIn']['value'] == 1 || $addProfileArea != '' ) echo "checked=\"checked\""; ?> /><?php echo $t_use[$GLOBALS['LANGINDEX']]; ?></label>
								</td>
							</tr>
							<?php
								}
							?>
							<tr>
								<th scope="row"><?php echo $t_atcmode[$GLOBALS['LANGINDEX']];?></th>
								<td>
									<select id="profile_<?php echo $profileCnt; ?>_atc" class="selectbox_style_wid260"  <?php if ($index < $fixProfileCnt) echo "disabled=\"disabled\""; ?> onChange="OnChangeATC()">
									  <option value="0" <?php if ($profileList->profile[$index]->dataInfo['UseATC']['value']==0) echo "selected=\"selected\"";?>><?php echo $t_off[$GLOBALS['LANGINDEX']];?></option>
									  <option value="1" <?php if ($profileList->profile[$index]->dataInfo['UseATC']['value']==1) echo "selected=\"selected\"";?>><?php echo $t_on[$GLOBALS['LANGINDEX']].$t_control_framerate[$GLOBALS['LANGINDEX']]; ?></option>
									  <option value="2" <?php if ($profileList->profile[$index]->dataInfo['UseATC']['value']==2) echo "selected=\"selected\"";?>><?php echo $t_on[$GLOBALS['LANGINDEX']].$t_control_compression[$GLOBALS['LANGINDEX']]; ?></option>
								<?php
									if($GLOBALS['M_SUPPORT_ATC_EVENTMODE']) {
								?>
									  <option value="3" <?php if ($profileList->profile[$index]->dataInfo['UseATC']['value']==3) echo "selected=\"selected\"";?>><?php echo $t_on[$GLOBALS['LANGINDEX']].$t_eventMD[$GLOBALS['LANGINDEX']]; ?></option>
								<?php
									}
								?>
									</select>
								</td>
							</tr>
							<tr>
								<th scope="row"><?php echo $t_atcSensitivity[$GLOBALS['LANGINDEX']];?></th>
								<td>
									<select id="profile_<?php echo $profileCnt; ?>_atc_sensitivity" class="selectbox_style_wid260"   >
									  <option value="0" <?php if ($profileList->profile[$index]->dataInfo['ATC_Sensitivity']['value']==0) echo "selected=\"selected\"";?>><?php echo $t_very_low[$GLOBALS['LANGINDEX']];?></option>
									  <option value="1" <?php if ($profileList->profile[$index]->dataInfo['ATC_Sensitivity']['value']==1) echo "selected=\"selected\"";?>><?php echo $t_low[$GLOBALS['LANGINDEX']]; ?></option>
									  <option value="2" <?php if ($profileList->profile[$index]->dataInfo['ATC_Sensitivity']['value']==2) echo "selected=\"selected\"";?>><?php echo $t_normal[$GLOBALS['LANGINDEX']]; ?></option>
									  <option value="3" <?php if ($profileList->profile[$index]->dataInfo['ATC_Sensitivity']['value']==3) echo "selected=\"selected\"";?>><?php echo $t_high[$GLOBALS['LANGINDEX']]; ?></option>
									  <option value="4" <?php if ($profileList->profile[$index]->dataInfo['ATC_Sensitivity']['value']==4) echo "selected=\"selected\"";?>><?php echo $t_very_high[$GLOBALS['LANGINDEX']]; ?></option>
									</select>
								</td>
							</tr>
							<tr>
								<th scope="row"><?php echo $t_atcLimit[$GLOBALS['LANGINDEX']];?></th>
								<td>
									<input id="profile_<?php echo $profileCnt; ?>_atc_limit" type="text" class="text" value="<?php echo $profileList->profile[$index]->dataInfo['ATC_Limit']['value']; ?>" style="width:62px;" maxlength="2" onkeypress="IsNum(event)" onkeydown="OnlyNUm(event);"/> % (10 ~ 50)
								</td>
							</tr>
						</tbody>
					</table>
			<?php
				if($GLOBALS['M_SUPPORT_CROP_ENCODING']) {
			?>
					<div class="h3_tit">
						<h3 class="wid320"><?php echo $t_cropencoding[$GLOBALS['LANGINDEX']]; ?></h3>
					</div>
					<table class="data_write">
						<colgroup>
	  						<col style="width:225px;" />
	  						<col />
						</colgroup>
						<tbody>
							<tr>
								<td>
									<label><input type="checkbox" id="profile_<?php echo $profileCnt; ?>_cropencoding_use" onclick="javascript:OnClickUseCrop()" <?php if ($profileList->profile[$index]->dataInfo['UseCropEncoding']['value'] == 1) echo "checked=\"checked\""; ?> /><?php echo $t_use[$GLOBALS['LANGINDEX']]; ?></label>
								</td>
								<td>
									<a id="profile_cropencoding_areaset_<?php echo $profileCnt; ?>" class="btn_type01" href="javascript:OnClickSetCropArea()" style="width:170px;"><?php echo $t_setArea[$GLOBALS['LANGINDEX']]; ?></a>
								</td>
							</tr>
						</tbody>
					</table>
			<?php
				}
			?>
					<div class="h3_tit">
						<h3 class="wid320"><?php echo $t_profileSetting[$GLOBALS['LANGINDEX']]; ?></h3>
					</div>
	  				<table class="data_write">
	  					<colgroup>
	  						<col style="width:225px;" />
	  						<col />
	  					</colgroup>
	  					<tbody>
	  						<tr>
	  							<th scope="row"><?php echo $t_resolution[$GLOBALS['LANGINDEX']]; ?></th>
	  							<td>
	  								<select id="profile_<?php echo $profileCnt; ?>_resolution" class="selectbox_style_wid260" onChange="OnChangeResolution('change')">

		  						<?php
		  							$resolVal = $profileList->profile[$index]->dataInfo['ResolWidth']['value'].' X '.$profileList->profile[$index]->dataInfo['ResolHeight']['value'];
									if($resolMode >= MAX_1_MEGA)
									{

									for ($index2=0; $index2<count($resolArr); ++$index2) {
		  						?>
										<option value="<?php echo $resolArr[$index2]; ?>" <?php if ($resolVal == $resolArr2[$index2]) echo "selected=\"selected\""; ?> ><?php echo $resolArr[$index2]; ?></option>
		  						<?php
		  								}
		  							}else{
		  							for ($index2=0; $index2<count($resolArr); ++$index2) {
		  						?>
		  								<option value="<?php echo $resolArr[$index2]; ?>" <?php if ($resolVal == $resolArr[$index2]) echo "selected=\"selected\""; ?> ><?php echo $resolArr[$index2]; ?></option>
		  						<?php
		  								}
		  							}?>
	  								</select>
	  							</td>
	  						</tr>
	  						<tr>
	  							<th scope="row"><?php echo $t_framerate[$GLOBALS['LANGINDEX']]; ?></th>
	  							<td>
	  								<select id="profile_<?php echo $profileCnt; ?>_framerate" class="selectbox_style_wid260" onChange="OnChangeFrate('change', 'select')">
								<?php
									$max = 30;
									if ($GLOBALS['M_SUPPORT_SENSOR_FRAMEMODE']) {
										if 		($classInstances['Information']->dataInfo['SensorFrameMode']['value'] == 0) $max = 60;
										else if 	($classInstances['Information']->dataInfo['SensorFrameMode']['value'] == 1) $max = 50;
										else if 	($classInstances['Information']->dataInfo['SensorFrameMode']['value'] == 2) $max = 30;
										else if 	($classInstances['Information']->dataInfo['SensorFrameMode']['value'] == 3) $max = 25;
									}

									if ($GLOBALS['M_MAX_RESOLUTION'] == MAX_4CIF & $videoType == VIDEOTYPE_PAL) $max = 25;
									else if ($GLOBALS['M_MAX_RESOLUTION'] == MAX_3_MEGA && $GLOBALS['M_MODEL_GROUP'] != MF_7004) $max = 20;
									switch ($encoding ) {
										case 0: //MJPEG
											if ($max > 30) $max = 30;
											if (($resolMode == MAX_2_MEGA || $resolMode == MAX_3_MEGA) && $profileList->profile[$index]->dataInfo['ResolHeight']['value'] >= 1024) $max = 15;
											if ($GLOBALS['M_MAX_RESOLUTION'] == MAX_3_MEGA && $profileList->profile[$index]->dataInfo['ResolHeight']['value'] >= 1536) $max = 10;
											if ($profileList->profile[$index]->dataInfo['EventProfile']['value'] == 1) $max = 5;
											if ($GLOBALS['M_MAX_RESOLUTION'] == MAX_1_MEGA && $GLOBALS['M_SUPPORT_PTZ'] && $profileList->profile[$index]->dataInfo['ResolHeight']['value'] > 600) $max = 15;
											if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_HISILICON){
												if($profileList->profile[$index]->dataInfo['ResolHeight']['value'] >= 1024) $max=5;
												else 15;
											}
											else	
											break;
										case 1:
											if ($GLOBALS['M_MAX_RESOLUTION'] == MAX_1_MEGA && $profileList->profile[$index]->dataInfo['ResolHeight']['value']==1024) $max = 25;
											//if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_HISILICON && $profileList->profile[$index]->dataInfo['RecordProfile']['value'] == 1) $max = 15;
											break;
									}
									
	  								for ($index2=$max; $index2>=1; --$index2) {
	  							?>
	  									<option value="<?php echo ($index2*1000) ?>" <?php if ($index2>=26) echo "class=\"no_mpeg4\"";?>><?php echo $index2.' fps'; ?></option>
	  							<?php
	  								}
	  							?>
	  								</select>
	  								<script>
										profileFrmArr[<?php echo $profileCnt; ?>] = <?php echo $profileList->profile[$index]->dataInfo['FrameRateLimit']['value']; ?>;
										$("#profile_<?php echo $profileCnt; ?>_framerate").val("<?php echo $profileList->profile[$index]->dataInfo['FrameRateLimit']['value']; ?>");
	  								</script>
	  							</td>
	  						</tr>
	  				<?php
	  					if ($GLOBALS['M_SUPPORT_COMPRESSION']) {
	  				?>
	  						<tr>
	  							<th scope="row"><?php echo $t_compression[$GLOBALS['LANGINDEX']]; ?></th>
	  							<td>
	  								<select id="profile_<?php echo $profileCnt; ?>_compression" class="selectbox_style_wid260">
	  									<option value="1"><?php echo $t_best[$GLOBALS['LANGINDEX']]; ?></option>
								<?php
	  								for ($index2=2; $index2<=19; ++$index2) {
	  							?>
	  									<option value="<?php echo $index2; ?>"><?php echo $index2; ?></option>
	  							<?php
	  								}
	  							?>
	  									<option value="20"><?php echo $t_worst[$GLOBALS['LANGINDEX']]; ?></option>
	  								</select>
	  								<script>
	  									$("#profile_<?php echo $profileCnt; ?>_compression").val("<?php echo $profileList->profile[$index]->dataInfo['Compression']['value']; ?>");
	  								</script>
	  							</td>
	  						</tr>
	  				<?php
	  					}
	  					else {
	  				?>
	  						<!-- tr>
	  							<th scope="row"><?php echo $t_bitrateControl[$GLOBALS['LANGINDEX']]; ?></th>
	  							<td >
	  							
	  								<select id="profile_<?php echo $profileCnt; ?>_adv_bitcontrol" class="selectbox_style_wid260" onChange="OnChangeBitcontrol('change')" >
	  									<option value="0" <?php if ($profileList->profile[$index]->dataInfo['ConstantBitrate']['value']==0) echo "selected=\"selected\""; ?> >VBR</option>
	  									<option value="1" <?php if ($profileList->profile[$index]->dataInfo['ConstantBitrate']['value']==1) echo "selected=\"selected\""; ?> >CBR</option>
	  								</select>
	  							</td>
	  						</tr
	  						<tr>
	  							<th scope="row"><?php echo $t_encodePriority[$GLOBALS['LANGINDEX']]; ?></th>
	  							<td>
	  								<select id="profile_<?php echo $profileCnt; ?>_adv_priority" class="selectbox_style_wid260">
	  									<option value ="0" <?php if ($priorityVal==0) echo "selected=\"selected\"";?> ><?php echo $t_framerate[$GLOBALS['LANGINDEX']]; ?></option>
	  									<option value ="1" <?php if ($priorityVal==1) echo "selected=\"selected\"";?> ><?php echo $t_compression[$GLOBALS['LANGINDEX']]; ?></option>
	  								</select>
	  							</td>
	  						</tr -->
	  				<?php
	  					}
	  				?>
	  					<tr>
  							<th scope="row" class="max_bitrate" <?php if ($profileList->profile[$index]->dataInfo['ConstantBitrate']['value']==1) echo "style=\"display:none\"";?> ><?php echo $t_max_bitrate[$GLOBALS['LANGINDEX']]; ?></th>
  							<th scope="row" class="target_bitrate" <?php if ($profileList->profile[$index]->dataInfo['ConstantBitrate']['value']==0) echo "style=\"display:none\"";?> ><?php echo $t_targetBitrate[$GLOBALS['LANGINDEX']]; ?></th>
  							<td><input id="profile_<?php echo $profileCnt; ?>_bitrate" type="text" class="text" value="<?php echo $profileList->profile[$index]->dataInfo['BitrateLimit']['value']/(1024*1024); ?>" style="width:62px;" maxlength="5" onkeypress="IsNum(event)" onkeydown="OnlyNUm(event);"/> Kbps
  							<span id="profile_<?php echo $profileCnt; ?>_bitrate_range"></span></td>
  						</tr>
	  					</tbody>
	  				</table>

					<div style="cursor:pointer;" class="advanced_profile" >
						<a  class="down"><?php echo $t_advanced[$GLOBALS['LANGINDEX']]; ?></a>
					</div>
					<div class="show_advanced_profile mgt30" style="display:none;margin-top:0px;">
					<?php
						if ($encoding == 1) { // MPEG4
							$codec = 'mpeg4';
							$gopVal = $profileList->profile[$index]->dataInfo['MPEG4GovLength']['value'];
							$priorityVal = $profileList->profile[$index]->dataInfo['MPEG4Priority']['value'];
						}
						else {	// H.264
							$codec = 'h264';
							$gopVal = $profileList->profile[$index]->dataInfo['H264GovLength']['value'];
							$priorityVal = $profileList->profile[$index]->dataInfo['H264Priority']['value'];
							$profileVal = $profileList->profile[$index]->dataInfo['H264Profile']['value'];
							$entropyVal = $profileList->profile[$index]->dataInfo['H264Entropy']['value'];
							$smartVal = $profileList->profile[$index]->dataInfo['UseSmartCodec']['value'];
						}
					?>
						<div class="profile_<?php echo $profileCnt; ?>_advanced_codec">
							<table class="data_write">
			  					<colgroup>
			  						<col style="width:225px;" />
			  						<col />
			  					</colgroup>
			  					<tbody>			  				
			  						<tr>
			  							<td colspan='2' height='20px'></td>
			  						</tr>
			  						<tr>
			  							<th scope="row"><?php echo $t_bitrateControl[$GLOBALS['LANGINDEX']]; ?></th>
			  							<td >
			  								<select id="profile_<?php echo $profileCnt; ?>_adv_bitcontrol" class="selectbox_style_wid260" onChange="OnChangeBitcontrol('change')" >
			  									<option value="0" <?php if ($profileList->profile[$index]->dataInfo['ConstantBitrate']['value']==0) echo "selected=\"selected\""; ?> >VBR</option>
			  									<option value="1" <?php if ($profileList->profile[$index]->dataInfo['ConstantBitrate']['value']==1) echo "selected=\"selected\""; ?> >CBR</option>
			  								</select>
			  							</td>
			  						</tr>
			  						<tr>
			  							<th scope="row"><?php echo $t_encodePriority[$GLOBALS['LANGINDEX']]; ?></th>
			  							<td>
			  								<select id="profile_<?php echo $profileCnt; ?>_adv_priority" class="selectbox_style_wid260">
			  									<option value ="0" <?php if ($priorityVal==0) echo "selected=\"selected\"";?> ><?php echo $t_framerate[$GLOBALS['LANGINDEX']]; ?></option>
			  									<option value ="1" <?php if ($priorityVal==1) echo "selected=\"selected\"";?> ><?php echo $t_compression[$GLOBALS['LANGINDEX']]; ?></option>
			  								</select>
			  							</td>
			  						</tr>
			  						<tr>
			  							<th scope="row"><?php echo $t_govlength[$GLOBALS['LANGINDEX']]; ?></th>
			  							<td>
			  								<input id="profile_<?php echo $profileCnt; ?>_adv_gop" type="text" class="text" value="<?php echo $gopVal; ?>" style="width:62px;" maxlength="3" onkeypress="IsNum(event)" onkeydown="OnlyNUm(event);"/>
			  								<span id="profile_<?php echo $profileCnt; ?>_gop_range"></span>
										</td>
									</tr>
									<?php
					  					if ($GLOBALS['M_SUPPORT_ENTROPY']) {
					  				?>
			  						<tr class="profile_<?php echo $profileCnt; ?>_adv_profileMode" <?php if ($codec != 'h264') echo "style=\"display:none\""; ?>>
			  							<th scope="row"><?php echo $t_profile[$GLOBALS['LANGINDEX']]; ?></th>
			  							<td>
			  								<select id="profile_<?php echo $profileCnt; ?>_adv_profile" class="selectbox_style_wid260" onChange="OnChangeH264ProfileMode()">
			  									<option value="0" <?php if ($profileVal==0) echo "selected=\"selected\"";?> >BaseLine</option>
			  									<option value="1" <?php if ($profileVal==1) echo "selected=\"selected\"";?> >Main</option>
												<?php
													if (!$GLOBALS['M_SUPPORT_HISILICON_2M_RES']) {
												?>
			  									<option value="3" <?php if ($profileVal==3) echo "selected=\"selected\"";?> >High</option>
												<?php } ?>
			  								</select>
			  							</td>
			  						</tr>
			  						<tr class="profile_<?php echo $profileCnt; ?>_adv_entropyCoding" <?php if ($codec != 'h264') echo "style=\"display:none\""; ?>>
			  							<th scope="row"><?php echo $t_entropyCoding[$GLOBALS['LANGINDEX']]; ?></th>
			  							<td>
			  								<select id="profile_<?php echo $profileCnt; ?>_adv_entropy" class="selectbox_style_wid260">
			  									<option value="0" <?php if ($entropyVal==0) echo "selected=\"selected\"";?> >CAVLC</option>
			  									<option value="1" <?php if ($entropyVal==1) echo "selected=\"selected\"";?> >CABAC</option>
			  								</select>
			  							</td>
			  						</tr>
			  						<?php
			  							}
			  							if($GLOBALS['M_SUPPORT_SMARTCODEC']) {
			  						?>
			  						<tr>
			  							<th scope="row"><?php echo $t_smartcodec[$GLOBALS['LANGINDEX']]; ?></th>
			  							<td>
			  								<select id="profile_<?php echo $profileCnt.'_'.$codec; ?>_adv_smart" class="selectbox_style_wid260">
			  									<option value="0" <?php if ($smartVal==0) echo "selected=\"selected\"";?> ><?php echo $t_off[$GLOBALS['LANGINDEX']];?></option>
			  									<option value="1" <?php if ($smartVal==1) echo "selected=\"selected\"";?> ><?php echo $t_on[$GLOBALS['LANGINDEX']];?></option>
			  								</select>
			  							</td>
			  						</tr>
				  				<?php } ?>
		  							</tbody>
		  						</table>
		  					</div>
							<table border="0" style="width:680px;">
							<tr><td style="height:40px;"></td></tr>
							<tr><td>
							<div class="h3_tit" style="width:680px;margin-top:0px;">
								<h3 style="width:225px;"><?php echo $t_multicast[$GLOBALS['LANGINDEX']];?> (SVNP)</h3>
								<div class="input_box" style="margin-left:<?php if(GetBrowserName()=='IE' && ieversion() < 8) {echo '2';}else {echo'-6';}?>px">
									<label><input id="profile_<?php echo $profileCnt; ?>_multicast_svnp_use" type="checkbox" onClick="OnClickMulticastUse('svnp')" <?php if ($profileList->profile[$index]->dataInfo['VNPEnabled']['value'] == 1) echo "checked=\"checked\""; ?> /><?php echo $t_use[$GLOBALS['LANGINDEX']];?></label>
								</div>
							</div>
							</td></tr>
							</table>
							<table class="data_write">
								<colgroup>
									<col style="width:225px;" />
									<col />
								</colgroup>
								<tbody>
									<tr>
										<th scope="row"><?php echo $t_IPAddress[$GLOBALS['LANGINDEX']]; ?></th>
										<td><input type="text" id="profile_<?php echo $profileCnt; ?>_multicast_svnp_ip" class="text" value="<?php echo $profileList->profile[$index]->dataInfo['VNPIPv4Addr']['value']; ?>" maxlength="15" style="width:257px;"  onkeypress='CheckIPv4(event)' onkeydown='CheckIPv4(event)' <?php if ($profileList->profile[$index]->dataInfo['VNPEnabled']['value'] == 0) echo "disabled=\"disabled\""; ?> /></td>
									</tr>
									<tr>
										<th scope="row"><?php echo $t_port[$GLOBALS['LANGINDEX']];?></th>
										<td><input type="text" id="profile_<?php echo $profileCnt; ?>_multicast_svnp_port" class="text" value="<?php echo $profileList->profile[$index]->dataInfo['VNPPort']['value']; ?>" maxLength="5" style="width:257px;" onkeypress="IsNum(event)" onkeydown="OnlyNUm(event);" <?php if ($profileList->profile[$index]->dataInfo['VNPEnabled']['value'] == 0) echo "disabled=\"disabled\""; ?> /></td>
									</tr>
									<tr>
										<th scope="row">TTL</th>
										<?php
											$ttlVal = $profileList->profile[$index]->dataInfo['VNPTTL']['value'];
											if ($ttlVal < 0) $ttlVal += 256;
										?>
										<td><input type="text" id="profile_<?php echo $profileCnt; ?>_multicast_svnp_ttl" class="text" value="<?php echo $ttlVal; ?>" style="width:257px;" maxLength="3" onkeypress="IsNum(event)" onkeydown="OnlyNUm(event);" <?php if ($profileList->profile[$index]->dataInfo['VNPEnabled']['value'] == 0) echo "disabled=\"disabled\""; ?> /></td>
									</tr>
								</tbody>
							</table>
							<div class="h3_tit">
								<h3 style="width:225px;"><?php echo $t_multicast[$GLOBALS['LANGINDEX']];?> (RTP)</h3>
								<div class="input_box" style="margin-left:<?php if(GetBrowserName()=='IE' && ieversion() < 8) {echo '2';}else {echo'-6';}?>px">
									<label><input id="profile_<?php echo $profileCnt; ?>_multicast_rtp_use" type="checkbox" onClick="OnClickMulticastUse('rtp')" <?php if ($profileList->profile[$index]->dataInfo['RTPEnabled']['value'] == 1) echo "checked=\"checked\""; ?> /><?php echo $t_use[$GLOBALS['LANGINDEX']];?></label>
								</div>
							</div>
							<table class="data_write">
								<colgroup>
									<col style="width:225px;" />
									<col />
								</colgroup>
								<tbody>
									<tr>
										<th scope="row"><?php echo $t_IPAddress[$GLOBALS['LANGINDEX']]; ?></th>
										<td><input type="text" id="profile_<?php echo $profileCnt; ?>_multicast_rtp_ip" class="text" value="<?php echo $profileList->profile[$index]->dataInfo['RTPIPv4Addr']['value']; ?>" style="width:257px;" maxlength="15"  onKeyPress='return IsIPv4Char(event)' onkeydown='CheckIPv4(event)' <?php if ($profileList->profile[$index]->dataInfo['RTPEnabled']['value'] == 0) echo "disabled=\"disabled\""; ?> /></td>
									</tr>
									<tr>
										<th scope="row"><?php echo $t_port[$GLOBALS['LANGINDEX']];?></th>
										<td><input type="text" id="profile_<?php echo $profileCnt; ?>_multicast_rtp_port" class="text" value="<?php echo $profileList->profile[$index]->dataInfo['RTPPort']['value']; ?>" style="width:257px;" maxLength="5" onkeypress="IsNum(event)" onkeydown="OnlyNUm(event);" <?php if ($profileList->profile[$index]->dataInfo['RTPEnabled']['value'] == 0) echo "disabled=\"disabled\""; ?> /></td>
									</tr>
									<tr>
										<th scope="row">TTL</th>
										<?php
											$ttlVal = $profileList->profile[$index]->dataInfo['RTPTTL']['value'];
											if ($ttlVal < 0) $ttlVal += 256;
										?>
										<td><input type="text" id="profile_<?php echo $profileCnt; ?>_multicast_rtp_ttl" class="text" value="<?php echo $ttlVal; ?>" style="width:257px;" maxLength="3" onkeypress="IsNum(event)" onkeydown="OnlyNUm(event);" <?php if ($profileList->profile[$index]->dataInfo['RTPEnabled']['value'] == 0) echo "disabled=\"disabled\""; ?> /></td>
									</tr>
									<tr>
										<th height="20px"></th>
									</tr>
								</tbody>
							</table>
						</div>

					</div>
			<?php
					$profileCnt++;
				}
			?>
			<table border="0" style="width:680px;">
			<tr><td style="height:30px;"></td></tr>
			<tr><td>
				<div class="btn_right_top" >
					<a  href="javascript:OnClickApply()" class="btn_apply"><?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?></a>
				</div>
			</td></tr>
			</table>
				</div>

			</div>
		</div>
</body>
</html>

