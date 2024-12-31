<?php
require_once $_SERVER["DOCUMENT_ROOT"] . "/resources/languages/Language.php";

$mGroup = $_SESSION["GROUP"];
$mPage = $_SESSION["PAGE"];

$pageLive = "moveToPage('pages/page_video_live.php');";
$pageVideo = "moveToPage('pages/page_setup_video.php');";
$pageWired = "moveToPage('pages/page_setup_wired_network.php');";
$pageWireless = "moveToPage('pages/page_setup_wireless_network.php');";
$pageTime = "moveToPage('pages/page_setup_time.php');";
$pagePrivatekey = "moveToPage('pages/page_admin_privatekey.php');";
$pageFirmware = "moveToPage('pages/page_admin_firmware.php');";
$pageClose = "moveToPage('pages/camera_login.php');";
?>

<!-- s:사이드바 -->
<div id="contDiv1">
<? if($mGroup == "Video"){ ?>	
	<ul id="snb" class="vd">
		<li class="sm1 on"><a href="#" onclick="<?=$pageLive?>" onmouseover="return parent.hidestatus();"><?=$Lang["Live"]?></a></li>
	</ul>
<? }else if($mGroup == "Setup"){ ?>
	<? if($mPage == "setup_video"){ ?>
		<ul id="snb" class="su">
			<li class="sm1 on"><a href="#" onclick="<?=$pageVideo?>" onmouseover="return parent.hidestatus();"><?=$Lang["General Setting"]?></a></li>
			<li class="sm2"><a href="#" onclick="<?=$pageWired?>" onmouseover="return parent.hidestatus();"><?=$Lang["Network Setting"]?></a></li>
			<li class="sm3"><a href="#" onclick="<?=$pageTime?>" onmouseover="return parent.hidestatus();"><?=$Lang["Time Setting"]?></a></li>
		</ul>
	<? }else if($mPage == "setup_wired_network"){ ?>
		<ul id="snb" class="su">
			<li class="sm1"><a href="#" onclick="<?=$pageVideo?>" onmouseover="return parent.hidestatus();"><?=$Lang["General Setting"]?></a></li>
			<li class="sm2 on"><a href="#" onclick="<?=$pageWired?>" onmouseover="return parent.hidestatus();"><?=$Lang["Network Setting"]?></a>
				<ul>
					<li class="on"><a href="#" onclick="<?=$pageWired?>" onmouseover="return parent.hidestatus();"><?=$Lang["Wired Network"]?></a></li>
					<li><a href="#" onclick="<?=$pageWireless?>" onmouseover="return parent.hidestatus();"><?=$Lang["Wireless Network"]?></a></li>
				</ul>
			</li>
			<li class="sm3"><a href="#" onclick="<?=$pageTime?>" onmouseover="return parent.hidestatus();"><?=$Lang["Time Setting"]?></a></li>
		</ul>
	<? }else if($mPage == "setup_wireless_network"){ ?>
		<ul id="snb" class="su">
			<li class="sm1"><a href="#" onclick="<?=$pageVideo?>" onmouseover="return parent.hidestatus();"><?=$Lang["General Setting"]?></a></li>
			<li class="sm2 on"><a href="#" onclick="<?=$pageWired?>" onmouseover="return parent.hidestatus();"><?=$Lang["Network Setting"]?></a>
				<ul>
					<li><a href="#" onclick="<?=$pageWired?>" onmouseover="return parent.hidestatus();"><?=$Lang["Wired Network"]?></a></li>
					<li class="on"><a href="#" onclick="<?=$pageWireless?>" onmouseover="return parent.hidestatus();"><?=$Lang["Wireless Network"]?></a></li>
				</ul>
			</li>
			<li class="sm3"><a href="#" onclick="<?=$pageTime?>" onmouseover="return parent.hidestatus();"><?=$Lang["Time Setting"]?></a></li>
		</ul>
	<? }else if($mPage == "setup_time"){ ?>
		<ul id="snb" class="su">
			<li class="sm1"><a href="#" onclick="<?=$pageVideo?>" onmouseover="return parent.hidestatus();"><?=$Lang["General Setting"]?></a></li>
			<li class="sm2"><a href="#" onclick="<?=$pageWired?>" onmouseover="return parent.hidestatus();"><?=$Lang["Network Setting"]?></a></li>
			<li class="sm3 on"><a href="#" onclick="<?=$pageTime?>" onmouseover="return parent.hidestatus();"><?=$Lang["Time Setting"]?></a></li>
		</ul>
	<? } ?>
<? }else if($mGroup == "Admin"){ ?>
	<? if($mPage == "admin_privatekey"){ ?>
		<ul id="snb" class="adm">
			<li class="m1 on"><a href="#" onclick="<?=$pagePrivatekey?>" onmouseover="return parent.hidestatus();"><?=$Lang["Private Key"]?></a></li>
			<li class="m2"><a href="#" onclick="<?=$pageFirmware?>" onmouseover="return parent.hidestatus();"><?=$Lang["Update Firmware"]?></a></li>
		</ul>
	<? }else if($mPage == "admin_firmware"){ ?>
		<ul id="snb" class="adm">
			<li class="m1"><a href="#" onclick="<?=$pagePrivatekey?>" onmouseover="return parent.hidestatus();"><?=$Lang["Private Key"]?></a></li>
			<li class="m2 on"><a href="#" onclick="<?=$pageFirmware?>" onmouseover="return parent.hidestatus();"><?=$Lang["Update Firmware"]?></a></li>
		</ul>
	<? } ?>
<? } ?>
</div>
<!-- e:사이드바 -->