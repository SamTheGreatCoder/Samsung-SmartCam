<?php
require_once ('../language/language_menu.cgi');

$selectedSetup = "class=\"selected\"";
$selectedPlayback = "";
if (stristr($_SERVER['SCRIPT_NAME'], 'playback') != FALSE) {
	$selectedPlayback = "class=\"selected\"";
	$selectedSetup = "";
}
?>

<div id="head">
		<?php 
			
			if($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>
				<div class="head-top2">
				<h1><img src="../images/common/top_title_1.png" alt="S1" /></h1>
				<div class="logo"></div>
			<?php } 
				else { 
			?>
			<div class="head-top">
				<h1><img src="../images/common/top_title.gif" alt="iPOLiS NETWORK CAMERA WEBVIEWER" /></h1>
				<div class="logo"><img src="../images/common/top_logo.gif" alt="SAMSUNG TECHWIN" /></div>
			<?php } ?>

			</div>
			<div class="gnb-tab" style="width:560px;">
				<ul>
					<li><a href="../monitoring.cgi"><img src="../images/common/icon/icon_live.png" alt="live icon" class="fix" /><?php echo $GLOBALS['top_monitoring'][0]; ?></a></li>
			<?php
		  		if (($GLOBALS['M_SUPPORT_SD'] || $GLOBALS['M_SUPPORT_NAS']) && $GLOBALS['M_SPECIAL_TYPE'] != 1) {
		  	?>
  					<li <?php echo $selectedPlayback; ?>><a href="./playback.cgi"><img src="../images/common/icon/icon_search.png" alt="search icon" class="fix" /><?php echo $GLOBALS['top_playback'][0]; ?></a></li>
		  	<?php
		  		}
		  		else {
		  	?>
					<li class="disable" style="color:gray;"><img src="../images/common/icon/icon_search.png" alt="search icon" class="fix" style="vertical-align:middle;"/><?php echo $GLOBALS['top_playback'][0]; ?></li>
			<?php
  				}
  			?>
	  			<li <?php echo $selectedSetup; ?>><a href="./basic_videoprofile.cgi"><img src="../images/common/icon/icon_setup.png" alt="setup icon" class="fix" /><?php echo $GLOBALS['top_setup'][0]; ?></a></li>
				</ul>
				<div>
					<div style="position:absolute; top:54px;left:430px;">
						<img src="../images/common/icon/user_icon.png">
					</div>
					<div style="position:absolute; top:58px;left:450px">					
					<h2>
			<?php
				// NO NEED to transrate, ONLY ENGLISH
				if 		($GLOBALS['USERINFO']['name'] == 'admin') 	echo 'ADMIN';
				else if 	($GLOBALS['USERINFO']['name'] == 'guest') 	echo 'GUEST';
				else																echo 'USER';
			?>
					</h2>
					</div>
					<div style="position:absolute; top:58px;left:510px">
						<img src="../images/common/PTZ/bar.png">
					</div>
					<div style="position:absolute; top:60px;left:520px">
						<img class="profileAccess" src="../images/common/icon/profileaccess.png" style="cursor:pointer" />
					</div>
					<div style="position:absolute; top:58px;left:545px;cursor:pointer">
						<h2 class="profileAccess">Status</h2>
					</div>
				</div>
			</div>
		</div>
<script type="text/javascript">
	$( ".profileAccess" ).mouseup(function() {
		window.open('../monitoring_info.cgi', 'popup', 'top=150, left=420, width=960, height=500, location=no, status=no, scrollbars=yes, resizable=no');
	});
</script>