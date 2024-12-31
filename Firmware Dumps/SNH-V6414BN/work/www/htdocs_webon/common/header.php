<?php
require_once $_SERVER["DOCUMENT_ROOT"] . "/resources/languages/Language.php";

$mGroup = $_SESSION["GROUP"];
$pageVideo = "moveToPage('pages/page_video_live.php');";
$pageSetup = "moveToPage('pages/page_setup_video.php');";
$pageAdmin = "moveToPage('pages/page_admin_privatekey.php');";
$pageClose = "moveToPage('pages/camera_login.php');";
?>

<body>
	<div id="wrap_cl">
		<!-- s:Skip Navigation --><a class="hide" href="#contBox_cl">Skip Navigation</a> <!-- e:Skip Navigation -->
		<a id="win_close" href="#">
			<img src="/resources/images/btn_close.gif" width="22" height="21" alt="close" onclick="<?=$pageClose?>"/>
		</a>
		
		<!-- s:header_cl -->
		<div id="header_cl" class="floatClear">
			<div id="logo_cl"><img alt="Samsung SmartCam" src="/resources/images/smartcam_ci_white_small.png"></div>
			<div id="camera_name2"></div>
			<!-- s:gnb_cl -->
			<div id="gnb_cl">
				<ul class="floatClear">
					<? if($mGroup == "Video"){ ?>
						<li class="m1 on"><a href="#" onclick="<?=$pageVideo?>" onmouseover="return parent.hidestatus();"><?=$Lang["Video"]?></a></li>
						<li class="m2"><a href="#" onclick="<?=$pageSetup?>" onmouseover="return parent.hidestatus();"><?=$Lang["Setup"]?></a></li>
						<li class="m3"><a href="#" onclick="<?=$pageAdmin?>" onmouseover="return parent.hidestatus();"><?=$Lang["Admin"]?></a></li>
					<? }else if($mGroup == "Setup"){ ?>
						<li class="m1"><a href="#" onclick="<?=$pageVideo?>" onmouseover="return parent.hidestatus();"><?=$Lang["Video"]?></a></li>
						<li class="m2 on"><a href="#" onclick="<?=$pageSetup?>" onmouseover="return parent.hidestatus();"><?=$Lang["Setup"]?></a></li>
						<li class="m3"><a href="#" onclick="<?=$pageAdmin?>" onmouseover="return parent.hidestatus();"><?=$Lang["Admin"]?></a></li>
					<? }else{ ?>
						<li class="m1"><a href="#" onclick="<?=$pageVideo?>" onmouseover="return parent.hidestatus();"><?=$Lang["Video"]?></a></li>
						<li class="m2"><a href="#" onclick="<?=$pageSetup?>" onmouseover="return parent.hidestatus();"><?=$Lang["Setup"]?></a></li>
						<li class="m3 on"><a href="#" onclick="<?=$pageAdmin?>" onmouseover="return parent.hidestatus();"><?=$Lang["Admin"]?></a></li>
					<? } ?>					
				</ul>
			</div>
			<!-- e:gnb_cl -->
		</div>
		<!-- e:header_cl -->