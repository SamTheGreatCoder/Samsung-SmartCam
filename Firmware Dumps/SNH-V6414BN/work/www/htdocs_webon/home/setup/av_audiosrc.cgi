<?php
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_menu.cgi');
require_once ('../language/language_av_audiosetup.cgi');

$classInstances= GetClassInstance('audio');
$audioInput 	= $classInstances['MediaConfiguration']->audioInput;
$audioOutput 	= $classInstances['MediaConfiguration']->audioOutput;
$audioDetail 	= $classInstances['MediaConfiguration']->audioDetail;
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="kr" xml:lang="kr">
<head>
	<title>iPOLiS NETWORK CAMERA WEBVIEWER</title>
	<meta http-equiv="X-UA-Compatible" content="IE=Edge; requiresActiveX=true">
	<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
	<link rel="stylesheet" type="text/css" href="../css/techwin.css" />
	<script type="text/javascript" src="../js/jquery-1.9.1.js"></script>
	<script type="text/javascript" src="../js/lnb.js"></script>
	<script type="text/javascript" src="../js/common_function.js"></script>
	<script type="text/javascript" language="javascript">
	<?php if (!$GLOBALS['M_SUPPORT_AUDIO']) { ?>
		document.location = "../../index.htm";
	<?php } ?>
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

	$(document).ready(function(){ lnbonoff("lnb_av"); });

	function OnClickApply()
	{
	  	var msg = "";
	  	msg += "<SetAudio>";
	  	msg += "<AudioInput>";
	  	msg += "<Enabled>1</Enabled>";
	  	msg += "<Gain>"+$('#audioInGain').val() + "</Gain>";
	  	<?php if($GLOBALS['M_SUPPORT_AUDIOCODEC'] & AUDIOCODEC_MASK_G726) { ?>
	  	msg += "<Encoding>"+$('#audioInCodec').val()+"</Encoding>";
	  	<?php } ?>
	  	msg += "</AudioInput>";
	  	<?php if($GLOBALS['M_SUPPORT_AUDIO_OUT'] != 0) {
		?>
	  	msg += "<AudioOutput>";
	  	msg += "<Enabled>" + ($('#audioOutEnable_enable').is(':checked')? 1 : 0) + "</Enabled>";
	  	msg += "<Gain>"+$('#audioOutGain').val()+"</Gain>";
	  	msg += "</AudioOutput>";
	  	<?php } ?>
	  	<?php if($GLOBALS['M_SUPPORT_AUDIOCODEC'] & AUDIOCODEC_MASK_G726) { ?>
	  	msg += "<AudioDetail>";

		msg += "<AudioInSource>"+$('#audioInSource').val()+"</AudioInSource>";
		msg += "<AudioInMicPowerEnable>"+($('#audioInBiasOn').is(':checked') ? 1 : 0)+"</AudioInMicPowerEnable>";

		if (parseInt($('#audioInCodec').val()) == 0)	{	// G.711
  			msg += "<AudioInBitrate>"+$('#audioInBitrate_G711').val()+"</AudioInBitrate>";
			msg += "<AudioInSamplingRate>"+8000+"</AudioInSamplingRate>";
  		}
  		else if (parseInt($('#audioInCodec').val()) == 1)	{	// G.726
  			msg += "<AudioInBitrate>"+$('#audioInBitrate_G726').val()+"</AudioInBitrate>";
			msg += "<AudioInSamplingRate>"+8000+"</AudioInSamplingRate>";
  		}
		else { // AAC
  			msg += "<AudioInBitrate>"+$('#audioInBitrate_AAC').val()+"</AudioInBitrate>";
			msg += "<AudioInSamplingRate>"+$('#audioInSamplingRate_AAC').val()+"</AudioInSamplingRate>";
  		}
		msg += "</AudioDetail>";
	  	<?php } ?>
	  	msg += "</SetAudio>";

		RequestAjaxMsg(msg, "<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>", "<?php echo $GLOBALS['REQUEST_URI'].'?seq='.$_SESSION['count'] ?>");
	}

	function AudioOutCheck()
	{
		if ($('#audioOutEnable_enable').is(':checked'))	$('#audioOutGain').removeAttr('disabled');
		else 															$('#audioOutGain').attr('disabled', 'disabled');
  	}

  	function OnChangeAudioInCodec()
  	{
  		var inCodec = parseInt($('#audioInCodec').val());
  		if (inCodec == 0)	{	// G.711
  			$('#audioInBitrate_G711').css('display', 'block');
  			$('#audioInBitrate_G726').css('display', 'none');
			$('#audioInBitrate_AAC').css('display', 'none');
			$('#audioInSamplingRate_G711_G726').css('display', 'block');
			$('#audioInSamplingRate_AAC').css('display', 'none');
  		}
		else if (inCodec == 1) { // G.726
  			$('#audioInBitrate_G711').css('display', 'none');
  			$('#audioInBitrate_G726').css('display', 'block');
			$('#audioInBitrate_AAC').css('display', 'none');
			$('#audioInSamplingRate_G711_G726').css('display', 'block');
			$('#audioInSamplingRate_AAC').css('display', 'none');
  		}
  		else { // AAC
  			$('#audioInBitrate_G711').css('display', 'none');
  			$('#audioInBitrate_G726').css('display', 'none');
			$('#audioInBitrate_AAC').css('display', 'block');
			$('#audioInSamplingRate_G711_G726').css('display', 'none');
			$('#audioInSamplingRate_AAC').css('display', 'block');

			OnChangeSamplingRate();
  		}
  	}

	function OnChangeAudioInSource()
	{
		var source = parseInt($('#audioInSource').val());
		if (source == 2)
		{
			$('#audioInBiasOn').removeAttr('disabled');
		}
		else
		{
			$('#audioInBiasOn').attr('disabled', 'disabled');
		}
	}

	function OnChangeSamplingRate() // AAC only
	{
		var samplingRate = parseInt($('#audioInSamplingRate_AAC').val());
		if (samplingRate == 16000) {
			if (parseInt($('#audioInBitrate_AAC').val()) == 128000) {
				$('#audioInBitrate_AAC').val(64000);
			}
			ChangeOption("audioInBitrate_AAC",  4, 'Disable');
		}
		else
		{
			ChangeOption("audioInBitrate_AAC",  4, 'Enable');
		}
	}

  	function OnLoad() {}

	</script>
</head>
<body onload="OnLoad()" onselectstart="return false">
	<div id="wrap" >
		<?php
			require_once ('left_menu.cgi');
			require_once ('top_menu.cgi');
		?>
		<div id="container" >
		<?php
			PrintLeftMenu($_SERVER['SCRIPT_NAME']);
		?>
			<div id="contents">
				<div class="h3_tit mgt0" >
					<h3 class="wid220"><?php echo $t_audioIn[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>
				<table class="data_write">
					<colgroup>
						<col style="width:115px;" />
						<?php if($GLOBALS['M_SUPPORT_AUDIOSOURCE'] & AUDIOSOURCE_MASK_EXTERAL_MIC) { ?>
						<col style="width:150px;" />
						<?php } ?>
						<col />
					</colgroup>
					<tbody>
					<?php
						if($GLOBALS['M_SUPPORT_AUDIOCODEC'] & AUDIOCODEC_MASK_G726) {
					?>
						<tr>
							<th scope="row"><?php echo $t_source[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<select name="select" id="audioInSource" class="selectbox_style_width165" onclick="javascript:OnChangeAudioInSource();" onChange="javascript:OnChangeAudioInSource();">
								<?php if($GLOBALS['M_SUPPORT_AUDIOSOURCE'] & AUDIOSOURCE_MASK_LINEIN) { ?>
									<option value="0" <?php if ($audioDetail->dataInfo['AudioInSource']['value'] == 0) echo "selected=\"selected\""; ?>><?php echo $t_line[$GLOBALS['LANGINDEX']]; ?></option>
								<?php } ?>
								<?php if($GLOBALS['M_SUPPORT_AUDIOSOURCE'] & AUDIOSOURCE_MASK_INTERAL_MIC) { ?>
									<option value="1" <?php if ($audioDetail->dataInfo['AudioInSource']['value'] == 1) echo "selected=\"selected\""; ?>><?php echo $t_microphone[$GLOBALS['LANGINDEX']]; ?></option>
								<?php } ?>
								<?php if($GLOBALS['M_SUPPORT_AUDIOSOURCE'] & AUDIOSOURCE_MASK_EXTERAL_MIC) { ?>
									<option value="2" <?php if ($audioDetail->dataInfo['AudioInSource']['value'] == 2) echo "selected=\"selected\""; ?>><?php echo $t_ext_mic[$GLOBALS['LANGINDEX']]; ?></option>
								<?php } ?>
								</select>
							</td>
							<?php if($GLOBALS['M_SUPPORT_AUDIOSOURCE'] & AUDIOSOURCE_MASK_EXTERAL_MIC) { ?>
							<td>	
								<label>
									<input type="checkbox" id="audioInBiasOn" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" <?php if ($audioDetail->dataInfo['AudioInMicPowerEnable']['value'] == 1) echo "checked=\"checked\""; ?>
									<?php if ($audioDetail->dataInfo['AudioInSource']['value'] != 2) echo "disabled=\"disabled\""; ?> /><?php echo $t_bias_on[$GLOBALS['LANGINDEX']]; ?>
								</label>
							</td>
							<?php } ?>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_codec[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<select name="select" id="audioInCodec" class="selectbox_style_width165" onChange="OnChangeAudioInCodec()">
									<option value="0" <?php if ($audioInput->dataInfo['Encoding']['value'] == 0) echo "selected=\"selected\""; ?> >G.711</option>
									<option value="1" <?php if ($audioInput->dataInfo['Encoding']['value'] == 1) echo "selected=\"selected\""; ?> >G.726</option>
									<?php
										if($GLOBALS['M_SUPPORT_AUDIOCODEC'] & AUDIOCODEC_MASK_AAC) {
									?>
									<option value="2" <?php if ($audioInput->dataInfo['Encoding']['value'] == 2) echo "selected=\"selected\""; ?> >AAC</option>
									<?php } ?>
								</select>
							</td>
						</tr>
						<?php
							if($GLOBALS['M_SUPPORT_AUDIOCODEC'] & AUDIOCODEC_MASK_AAC) {
						?>
						<tr>
							<th scope="row"><?php echo $t_samplingrate[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<select name="select" id="audioInSamplingRate_G711_G726" class="selectbox_style_width165" <?php if ($audioInput->dataInfo['Encoding']['value'] < 2) echo "style=\"display:block\""; else echo "style=\"display:none\""; ?> disabled="disabled">
									<option value="8000" <?php if ($audioDetail->dataInfo['AudioInSamplingRate']['value'] == 8000) echo "selected=\"selected\""; ?>>8KHz</option>
								</select>
								<select name="select" id="audioInSamplingRate_AAC" class="selectbox_style_width165" <?php if ($audioInput->dataInfo['Encoding']['value'] == 2) echo "style=\"display:block\""; else echo "style=\"display:none\""; ?> onChange="javascript:OnChangeSamplingRate();">
									<option value="16000" <?php if ($audioDetail->dataInfo['AudioInSamplingRate']['value'] == 16000) echo "selected=\"selected\""; ?>>16KHz</option>
									<option value="48000" <?php if ($audioDetail->dataInfo['AudioInSamplingRate']['value'] == 48000) echo "selected=\"selected\""; ?>>48KHz</option>
								</select>
							</td>
						</tr>
						<?php
							}
						?>
						<tr>
							<th scope="row"><?php echo $t_bitrate[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<select name="select" id="audioInBitrate_G711" class="selectbox_style_width165" <?php if ($audioInput->dataInfo['Encoding']['value'] == 0) echo "style=\"display:block\""; else echo "style=\"display:none\""; ?> disabled="disabled">
									<option value="64000" selected="selected">64K</option>
								</select>
								<select name="select" id="audioInBitrate_G726" class="selectbox_style_width165" <?php if ($audioInput->dataInfo['Encoding']['value'] == 1) echo "style=\"display:block\""; else echo "style=\"display:none\""; ?> >
									<option value="16000" <?php if ($audioDetail->dataInfo['AudioInBitrate']['value'] == 16000) echo "selected=\"selected\""; ?>>16K</option>
									<option value="24000" <?php if ($audioDetail->dataInfo['AudioInBitrate']['value'] == 24000) echo "selected=\"selected\""; ?>>24K</option>
									<option value="32000" <?php if ($audioDetail->dataInfo['AudioInBitrate']['value'] == 32000) echo "selected=\"selected\""; ?>>32K</option>
									<option value="40000" <?php if ($audioDetail->dataInfo['AudioInBitrate']['value'] == 40000) echo "selected=\"selected\""; ?>>40K</option>
								</select>
								<select name="select" id="audioInBitrate_AAC" class="selectbox_style_width165" <?php if ($audioInput->dataInfo['Encoding']['value'] == 2) echo "style=\"display:block\""; else echo "style=\"display:none\""; ?> >
									<option value="8000" <?php if ($audioDetail->dataInfo['AudioInBitrate']['value'] == 8000) echo "selected=\"selected\""; ?>>8K</option>
									<option value="16000" <?php if ($audioDetail->dataInfo['AudioInBitrate']['value'] == 16000) echo "selected=\"selected\""; ?>>16K</option>
									<option value="32000" <?php if ($audioDetail->dataInfo['AudioInBitrate']['value'] == 32000) echo "selected=\"selected\""; ?>>32K</option>
									<option value="64000" <?php if ($audioDetail->dataInfo['AudioInBitrate']['value'] == 64000) echo "selected=\"selected\""; ?>>64K</option>
									<option value="128000" <?php if ($audioDetail->dataInfo['AudioInBitrate']['value'] == 128000) echo "selected=\"selected\""; ?> <?php if ($audioDetail->dataInfo['AudioInSamplingRate']['value'] == 16000) echo "disabled=\"disabled\""; ?>>128K</option>
								</select>
								<script>
									<?php
										if ($audioInput->dataInfo['Encoding']['value'] == 0) {
									?>
											$('#audioInBitrate_G726').val(32000);
											$('#audioInBitrate_AAC').val(32000);
									<?php
										} else if ($audioInput->dataInfo['Encoding']['value'] == 1) {
									?>
											$('#audioInBitrate_G711').val(64000);
											$('#audioInBitrate_AAC').val(32000);
									<?php
										} else if ($audioInput->dataInfo['Encoding']['value'] == 2) {
									?>
											$('#audioInBitrate_G711').val(64000);
											$('#audioInBitrate_G726').val(32000);
									<?php
										}
									?>
								</script>
							</td>
						</tr>
					<?php
						}
					?>
						<tr>
							<th scope="row"><?php echo $t_gain[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<select name="select" id="audioInGain" class="selectbox_style_width165">
						<?php
                  	for ($index=1; $index<11; ++$index) {
               			if ($audioInput->dataInfo['Gain']['value'] == $index) {
               	?>
                  	      <option value="<?php echo $index; ?>" selected="selected"> <?php echo $index; ?></option>
                	<?php	}
                			else {
                	?>
                				<option value="<?php echo $index; ?>"> <?php echo $index; ?></option>
                	<?php
                			}
                		}
               	?>
                			</select>
							</td>
						</tr>
					</tbody>
				</table>
				<?php
					if($GLOBALS['M_SUPPORT_AUDIO_OUT'] != 0) {
				?>
				<div class="h3_tit">
					<h3 class="wid220"><?php echo $t_audioOut[$GLOBALS['LANGINDEX']]; ?></h3>
				</div>
				<table class="data_write" style="table-layout: fixed;">
					<colgroup>
						<col style="width:115px;" />
						<col />
					</colgroup>
					<tbody>
						<tr>
							<th scope="row"><?php echo $t_enable[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<label><input type="radio" name="audioOutEnable" id="audioOutEnable_enable" value="Enable" onClick="AudioOutCheck()" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px" <?php if($audioOutput->dataInfo['Enabled']['value'] == 1) echo "checked=\"checked\"" ?> /><?php echo $t_on[$GLOBALS["LANGINDEX"]]; ?></label>
								<label><input type="radio" name="audioOutEnable" id="audioOutEnable_disable" value="Disable" onClick="AudioOutCheck()" <?php if($audioOutput->dataInfo['Enabled']['value'] == 0) echo "checked=\"checked\"" ?> /><?php echo $t_off[$GLOBALS["LANGINDEX"]]; ?></label>
							</td>
						</tr>
						<tr>
							<th scope="row"><?php echo $t_gain[$GLOBALS['LANGINDEX']]; ?></th>
							<td>
								<select name="select" id="audioOutGain" class="selectbox_style_width165" <?php if ($audioOutput->dataInfo['Enabled']['value'] == 0) echo "disabled=\"disabled\""; ?> >
						  <?php
                  		for ($index=1; $index<11; ++$index)
                  		{
                  			if ($audioOutput->dataInfo['Gain']['value'] == $index)
                  			{
                  	?>
                  	      <option value="<?php echo $index; ?>" selected="selected"><?php echo $index; ?></option>
                	<?php
                			}
                			else
                			{
                	?>
                				  <option value="<?php echo $index; ?>"><?php echo $index; ?></option>
                	<?php
                			}
                		}
                	?>
								</select>
							</td>
						</tr>
					</tbody>
				</table>
				<?php
					}
				?>
				<div class="btn_right">
					<a id="mid_ok_btn" class="btn_apply" href="javascript:OnClickApply()"><?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?></a>
				</div>
			</div>
		</div>
	</div>
</body>
</html>
