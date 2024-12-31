<div class="h3_tit">
	<h3 class="wid220"><?php echo $t_fd[$GLOBALS['LANGINDEX']]; ?></h3>
</div>
<?php
	require_once('plugin_ui.cgi');
?>
<script>
	AddPluginObject("<?php echo $msg_plugin_install[$GLOBALS['LANGINDEX']]; ?>", viewerWidth, viewerHeight, "<?php echo '_'.$eventType; ?>");
</script>

<div id="DisableFDSelectLayer" style="position:absolute; width:800px; height:300px; left: 300px; top: 940px; background-color:#000000; display:none; z-index:1000; filter:alpha(opacity=0); opacity:0.0; -moz-opacity:0.0;">
</div>
<div id="fd_tabs" style="margin-top:40px; margin-bottom:10px; margin-left:9px">
	<ul>
		<li><a href="#fd_tabs-1" onClick="OnClickFdTabs('sense')"><?php echo $t_sensitivity[$GLOBALS['LANGINDEX']]; ?></a></li>
		<li><a href="#fd_tabs-2" onClick="OnClickFdTabs('area')"><?php echo $t_area[$GLOBALS['LANGINDEX']]; ?></a></li>
	</ul>
	<div id="fd_tabs-1">
		<table class="data_write mgt10 mgl-20 pdl15" style="width:670px;" border=0>
			<colgroup>
				<col style="width:162px;"/>
				<col />
			</colgroup>
			<tr>
				<th class="top_txt"><?php echo $t_sensitivity[$GLOBALS['LANGINDEX']]; ?></th> 					
				<td>
					<select id="event_<?php echo $eventType; ?>_sensitivity" class="selectbox_style">					
						<option value="1" <?php if ($event_class[$eventType]->dataInfo['Sensitivity']['value'] == 1) echo "selected=\"selected\""; ?> ><?php echo '1('.$t_very_low[$GLOBALS['LANGINDEX']].')'; ?></option>
						<?php
							$sens_list = '';
							for($i=2; $i<10; $i++) {
								$sens_list .= '<option value='.$i;
								if ($event_class[$eventType]->dataInfo['Sensitivity']['value'] == $i) $sens_list .= " selected=\"selected\"";
								$sens_list .= '>'.$i.'</option>'."\r\n";

							}
							echo $sens_list;
						?>
						<option value="10" <?php if ($event_class[$eventType]->dataInfo['Sensitivity']['value'] == 10) echo "selected=\"selected\""; ?> ><?php echo '10('.$t_very_high[$GLOBALS['LANGINDEX']].')'; ?></option>
					</select>
				</td>
			</tr>
		</table> 					
	</div>
	<div id="fd_tabs-2">
		<table class="data_write mgt10 mgl-20 pdl15" style='width:670px;'>
			<colgroup>
				<col style="width:162px;"/>
				<col />
			</colgroup>
			<tbody>
				<tr>
					<th class="top_txt"><?php echo $t_area[$GLOBALS['LANGINDEX']]; ?></th>
					<td>
						<label><input type="radio" name="event_<?php echo $eventType; ?>_detection_mode" id="event_<?php echo $eventType; ?>_detection_mode_on" onClick='OnClickDetectionMode()' <?php if($event_class[$eventType]->dataInfo['ObjectMode']['value'] == 1) echo "checked=\"checked\""; ?> style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_detectionArea[$GLOBALS['LANGINDEX']]; ?></label>
					</td>
				</tr>
				<tr>
					<td></td>
					<td>
						<label><input type="radio" name="event_<?php echo $eventType; ?>_detection_mode" id="event_<?php echo $eventType; ?>_detection_mode_none" onClick='OnClickDetectionMode()' <?php if($event_class[$eventType]->dataInfo['ObjectMode']['value'] == 0) echo "checked=\"checked\""; ?> style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_nondetectionArea[$GLOBALS['LANGINDEX']]; ?></label>
					</td>
				</tr>	
			</tbody>
		</table>
	</div>
</div>
<table class="data_write">
	<tbody>
		<tr>
			<td>
				<label><input type='checkbox' id='event_<?php echo $eventType; ?>_overlay_motion' <?php if ($event_class[$eventType]->dataInfo['FDBoxDisplay']['value']==1) echo "checked=\"checked\""; ?> style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_detection_result_overlay[$GLOBALS['LANGINDEX']] ; ?></label>
			</td>
		</tr> 
	</tbody>
</table>
