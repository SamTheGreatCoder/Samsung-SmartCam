<?php
require_once ('../cgi-bin/adv/_define.inc');
require_once ('./language/language_menu.cgi');
require_once ('./language/language_about.cgi');

$classInstances= GetClassInstance('profileaccess');
$accessInfo		= $classInstances['ProfileAccessInformation'];
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="kr" xml:lang="kr">
	<head>
		<meta http-equiv="X-UA-Compatible" content="IE=Edge; requiresActiveX=true">
		<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
		<title>iPOLiS NETWORK CAMERA WEBVIEWER</title>
		<link rel="stylesheet" type="text/css" href="./css/techwin.css" />
		<script type="text/javascript" src="./js/jquery-1.9.1.js"></script>
		<script type="text/javascript" src="./js/lnb.js"></script>
		<script type="text/javascript" src="./js/common_function.js"></script>
		<script type="text/javascript">	
<?php
	if ($classInstances['Information']->dataInfo['PasswordCheck']['value'] == 1) {
?>
		window.location.href = './pw_change.cgi';
<?php
	}
	else if ($classInstances['Information']->dataInfo['PasswordCheck']['value'] == 2) {
?>
		alert("<?php echo $msg_change_weak_password[$GLOBALS['LANGINDEX']]; ?>");
<?php
	}
?>	
		</script>
	</head>
	<body onselectstart="return false" class="ptz">
		<div style="margin:10px;">
			<div class="h3_tit mgt0" style="width:920px;">
				<h3 class="wid320"><?php echo $t_profileAccess[$GLOBALS['LANGINDEX']]; ?></h3>
			</div>
			<table class="data_table2" style="width:920px;table-layout:fixed;">
				<colgroup>
					<col style="width:160px;"/>
					<col style="width:180px;"/>
					<col style="width:180px;"/>
					<col style="width:100px;"/>
					<col style="width:300px;"/>
				</colgroup>
				<thead>
					<tr>
						<th><?php echo $t_profile[$GLOBALS['LANGINDEX']];?></th>
						<th><?php echo $t_bitrate[$GLOBALS['LANGINDEX']];?>(kbps)</th>
						<th><?php echo $t_framerate[$GLOBALS['LANGINDEX']];?>(fps)</th>
						<th>ATC(%)</th>
						<th><?php echo $t_accessNumber[$GLOBALS['LANGINDEX']];?></th>
					</tr>
				</thead>
				<tbody>
			<?php
				for($index=0; $index<MAX_PROFILE_COUNT; ++$index) {
					if ($accessInfo->profileAtcInfo[$index]['ProfileName']['value'] == '') continue;
			?>
					<tr>
						<td height="auto" style="word-break:break-all; padding-left:5px"><?php echo $accessInfo->profileAtcInfo[$index]['ProfileName']['value']; ?></td>
						<td><?php echo $accessInfo->profileAtcInfo[$index]['RealBitrate']['value'].'/'.$accessInfo->profileAtcInfo[$index]['SetBitrate']['value']; ?></td>
						<td><?php echo $accessInfo->profileAtcInfo[$index]['RealFramerate']['value'].'/'.$accessInfo->profileAtcInfo[$index]['SetFramerate']['value']; ?></td>
						<td><?php echo $accessInfo->profileAtcInfo[$index]['ATCRate']['value']; ?></td>
						<td><?php echo $accessInfo->profileAtcInfo[$index]['UserCnt']['value']; ?></td>
					</tr>
			<?php
				}
			?>
				</tbody>
			</table>
			
			<div class="h3_tit mgt20" style="width:920px;">
				<h3 class="wid320"><?php echo $t_currentUsers[$GLOBALS['LANGINDEX']]; ?></h3>
			</div>
			<table class="data_table2" style="width:920px;table-layout:fixed;">
				<colgroup>
					<col style="width:160px;"/>
					<col style="width:180px;"/>
					<col style="width:180px;"/>
					<col style="width:400px;"/>
				</colgroup>
				<thead>
					<tr>
						<th><?php echo $t_profile[$GLOBALS['LANGINDEX']];?></th>								
						<th><?php echo $t_bitrate[$GLOBALS['LANGINDEX']];?>(kbps)</th>
						<th><?php echo $t_networkConnectionStatus[$GLOBALS['LANGINDEX']];?></th>
						<th>IP</th>
					</tr>
				</thead>
				<tbody>
			<?php
				for($index=0; $index<MAX_STREAM_COUNT; ++$index) {
					if ($accessInfo->userAtcInfo[$index]['UsedProfile']['value'] == 0) continue;
					$connectedProfile = '';
					for ($index2=0; $index2<MAX_PROFILE_COUNT; ++$index2) {
						if (($accessInfo->userAtcInfo[$index]['UsedProfile']['value'] & (1 << $index2)) == 0) continue;
						if ($accessInfo->profileAtcInfo[$index2]['ProfileName']['value'] == '') continue;
						$connectedProfile .= $accessInfo->profileAtcInfo[$index2]['ProfileName']['value'].', ';
					}
					$connectedProfile = substr($connectedProfile, 0, -2);
					$networkState = $accessInfo->userAtcInfo[$index]['NetworkState']['value'];
			?>
					<tr>
						<td height="auto" style="word-break:break-all; padding-left:5px"><?php echo $connectedProfile; ?></td>								
						<td><?php echo $accessInfo->userAtcInfo[$index]['RealBitrate']['value']; ?></td>
						<td><?php echo ($networkState == 0 ? $t_bad[$GLOBALS['LANGINDEX']] : ($networkState == 1 ? $t_good[$GLOBALS['LANGINDEX']] : $t_optimized[$GLOBALS['LANGINDEX']])); ?></td>
						<td height="auto" style="word-break:break-all"><?php echo $accessInfo->userAtcInfo[$index]['IPAddress']['value']; ?></td>
					</tr>
			<?php
				}
			?>
				</tbody>
			</table>

			<div style="text-align:center; margin-top:40px; position:absolute; left:430px;">
				<a href="javascript:window.close()" class="btn_apply"><?php echo $t_close[$GLOBALS['LANGINDEX']];?></a>
			</div>
		</div>
	</body>
</html>
