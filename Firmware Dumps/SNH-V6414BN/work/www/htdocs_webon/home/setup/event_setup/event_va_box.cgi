<script type="text/javascript" language="javascript">

$(document).ready(function(){	
	var ConfMinHeight	= {min:24,max:maxResolution.height};
	var ConfMinwidth	= {min:24,max:maxResolution.width};	
	
	$("#md_tabs").tabs({
		activate:function(event){
			var tabIndex = parseInt($("#md_tabs").tabs("option", "active"), 10);
			OnChangeVaTabs(tabIndex);
		}
	});
	//spinner config
	$(".objectSizeSpinner").spinner({
		min:ConfMinwidth.min,
		max:ConfMinwidth.max,
		spin: function(event, ui) {
			 OnChangeObjectSize();
		},
		stop: function(event, ui) {
			OnChangeObjectSize();
		}
	});
});

$(document).mouseup(function() {
	if(firstDrawClick && isDrawDragging){
		switch(EventSetup.viewStatus){
			case VIEW_MODE["MD"] : $("#MDPolyTemp").trigger("mouseup"); break;
			case VIEW_MODE["MD_OBJSIZE"] : $("#maxMinCover").trigger("mouseup"); break;
			case VIEW_MODE["VA_PASSING"] : ; break;
			case VIEW_MODE["VA_ENTERING"] : ; break;
			case VIEW_MODE["VA_APPEAR"] : $("#myCanvasRectTmp").trigger("mouseup"); break;
		}
		$("#imgTemp").trigger("mouseup");
	}
});

function InitIVConfiguration()
{
	var xml_data=$.parseXML(mdvaXmlMsg);
	<?php if($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_HISILICON) { ?>
		EventSetup.MD.init(viewerWidth,viewerHeight,maxResolution.width,maxResolution.height,EventSetup.TYPE_RECT,GetFilpMirrorStatus(), false, GetRotateStatus());		//MD Polygon	
	<?php }else{ ?>
		EventSetup.MD.init(viewerWidth,viewerHeight,maxResolution.width,maxResolution.height,EventSetup.TYPE_POLY,GetFilpMirrorStatus(), false,0);		//MD Polygon	
	<?php } ?>
	EventSetup.MD.getMDPolygon($(xml_data));

	<?php if ($GLOBALS['M_SUPPORT_EVENT_VA'] & IV_SUPPORT) { ?> 	//IV
		var MaxVaCount 	= {passing:3, entering:3, appearing:3};	
		EventSetup.VA.lineDraw(MaxVaCount.passing);			//passing
		EventSetup.VA.getLine($(xml_data));
		EventSetup.VA.init(false,MaxVaCount.entering);		//Entering/Exiting
		EventSetup.VA.getPolygon($(xml_data));
		EventSetup.VA.initRectangle(EventSetup.TYPE_POLY, MaxVaCount.appearing);		//Polygon		
		EventSetup.VA.getRectangle($(xml_data));
	<?php } ?>			
	
	EventSetup.MD.minMaxRectangle(); //min max size
	
	window.setTimeout(function(){
		OnClickVaMode();
	},500);
}

function MakeVideoAnalyticsXml()
{
	var msg = "";
	<?php if ($GLOBALS['M_SUPPORT_EVENT_VA'] & IV_SUPPORT) { ?>
	msg += "<Mode>"+$('#event_<?php echo $event_name; ?>_mode').val()+"</Mode>";
	<?php } ?>
	msg += "<MDConfiguration>";
	msg += "<Enabled>"+($("#event_<?php echo $event_name; ?>_use_on").is(':checked')? 1 : 0)+"</Enabled>";
	msg += "<ObjectMode>"+($('#event_<?php echo $event_name; ?>_detection_mode_on').is(':checked') ? 1 : 0)+"</ObjectMode>";
	msg += "<ObjectSize>5</ObjectSize>"; // always manual size
	msg += "<Sensitivity>"+$('#event_<?php echo $event_name; ?>_md_sensitivity').val()+"</Sensitivity>";
	msg += MakeManualSize('md');
	<?php if($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_HISILICON){ ?>
	<?php }else{ ?>
	msg += "<VABoxDisplay>"+($('#event_<?php echo $event_name; ?>_overlay_motion').is(':checked') ? 1 : 0)+"</VABoxDisplay>";
	<?php } ?>	
	msg += EventSetup.VA.setMD_xml();
	<?php if($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>	
	msg += MakeScheduleAndActionSetupXML_S1("<?php echo $event_name; ?>");
	<?php } else { ?>
	msg += MakeScheduleAndActionSetupXML("<?php echo $event_name; ?>");
	<?php } ?>
	msg += "</MDConfiguration>";
	<?php if ($GLOBALS['M_SUPPORT_EVENT_VA'] & IV_SUPPORT) { ?>
		msg += "<IVConfiguration>";
		msg += "<Enabled>"+($("#event_<?php echo $event_name; ?>_use_on").is(':checked')? 1 : 0)+"</Enabled>";
		msg += "<Sensitivity>"+$('#event_<?php echo $event_name; ?>_va_sensitivity').val()+"</Sensitivity>";
		msg += "<Overlay>"+($('#event_<?php echo $event_name; ?>_overlay_rules').is(':checked') ? 1 : 0)+"</Overlay>";
		msg += "<VABoxDisplay>"+($('#event_<?php echo $event_name; ?>_overlay_motion').is(':checked') ? 1 : 0)+"</VABoxDisplay>";
		msg += MakeManualSize('va');		
		msg += EventSetup.VA.setVA_xml();
		msg += "</IVConfiguration>";
	<?php } ?>
	return msg;
}

function OnClickVaMode()
{
	$("#md_tabs").show();
	currentVaMode = 'md';
	$("#md_tabs .ui-tabs-panel").css("height", "140px");
	$("#md_tabs").tabs("option", "active", 0);
	if ($('#event_<?php echo $event_name; ?>_mode').val() == 0) {		//MD
		$('#event_<?php echo $event_name; ?>_analytics_type').attr('disabled','disabled');
		$('#event_<?php echo $event_name; ?>_overlay_rules').attr('disabled','disabled');
		$("#md_tabs").tabs("disable", 3);
	}
	else if($('#event_<?php echo $event_name; ?>_mode').val() == 1){		//IV
		$('#event_<?php echo $event_name; ?>_analytics_type').removeAttr('disabled');
		$('#event_<?php echo $event_name; ?>_overlay_rules').removeAttr('disabled');
		$("#md_tabs").tabs("enable", 3);
	}
	else{		
		$('#event_<?php echo $event_name; ?>_analytics_type').removeAttr('disabled');
		$('#event_<?php echo $event_name; ?>_overlay_rules').removeAttr('disabled');
		$("#md_tabs").tabs("enable", 3);
	}
}

function OnChangeAnalyticsType()
{
	switch(parseInt($('#event_<?php echo $event_name; ?>_analytics_type').val())) {
		case 0:		// passing
			EventSetup.VA.view("lineDraw");
			EventSetup.VA.reDrawLine();
			break;
		case 1:		// Entering&Exiting
			EventSetup.VA.view("polyDraw");
			EventSetup.VA.reDrawVaPolygon();
			break;
		case 2:		// Appear(Disappear)
			if($("#event_<?php echo $event_name; ?>_appearing_rules_definedarea").is(":checked")){
				EventSetup.VA.view("rectangleDraw");
				EventSetup.VA.reDrawRectangle();
			}else{
				EventSetup.VA.view("fullScreen");
				$("#poly-dialog-entireArea").dialog("open");
			}
			break;
	}

	if(parseInt($('#event_<?php echo $event_name; ?>_analytics_type').val()) == 2){
		$('.event_<?php echo $event_name; ?>_appearing_rules').show();
	}else{
		$('.event_<?php echo $event_name; ?>_appearing_rules').hide();
	}
}

</script>
<div style="position:relative">
<?php if ($GLOBALS['M_SUPPORT_EVENT_VA'] & IV_SUPPORT) { ?>
<div id="DisableIVSelectLayer" style="position:absolute; width:680px; height:215px; left: 0px; top: 0px; background-color:#000000; display:none; z-index:1000; filter:alpha(opacity=0.3); opacity:0.3; -moz-opacity:0.3; -ms-filter: 'progid:DXImageTransform.Microsoft.Alpha(Opacity=30)';"></div>
<?php }else{ ?>
<div id="DisableIVSelectLayer" style="position:absolute; width:680px; height:165px; left: 0px; top: 0px; background-color:#000000; display:none; z-index:1000; filter:alpha(opacity=0.3); opacity:0.3; -moz-opacity:0.3; -ms-filter: 'progid:DXImageTransform.Microsoft.Alpha(Opacity=30)';"></div>
<?php } ?>
<?php
if($GLOBALS['M_SUPPORT_EVENT_VA'] & IV_SUPPORT) {
?>
	<table class="data_write mgt20">
		<colgroup>
			<col style="width:150px;"/>
			<col />
		</colgroup>
		<tbody>
			<tr>
				<th><?php echo $t_mode[$GLOBALS['LANGINDEX']] ?></th>
				<td>
					<select id="event_<?php echo $event_name; ?>_mode" class="selectbox_style" style="width:303px" onChange='OnClickVaMode()'>
						<option value="0" <?php if ($vaConf->dataInfo['Mode']['value']==0) echo "selected=\"selected\""; ?>><?php echo $t_md[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="1" <?php if ($vaConf->dataInfo['Mode']['value']==1) echo "selected=\"selected\""; ?>><?php echo $t_videoAnalytics[$GLOBALS['LANGINDEX']]; ?></option>
						<option value="2" <?php if ($vaConf->dataInfo['Mode']['value']==2) echo "selected=\"selected\""; ?>><?php echo $t_md_va[$GLOBALS['LANGINDEX']]; ?></option>
					</select>
				</td>
			</tr>
		</tbody>
	</table>
<?php
}
?>
	<div id="md_tabs" style="display:none; margin-top:20px; margin-bottom:10px; margin-left:9px">
		<ul>
			<li><a href="#md_tabs-1"><?php echo $t_sensitivity[$GLOBALS['LANGINDEX']]; ?></a></li>
			<li><a href="#md_tabs-2"><?php echo $t_size[$GLOBALS['LANGINDEX']]; ?></a></li>
			<li><a href="#md_tabs-3"><?php echo $t_area[$GLOBALS['LANGINDEX']]; ?></a></li>
			<?php if($GLOBALS['M_SUPPORT_EVENT_VA'] & IV_SUPPORT) { ?>
			<li><a href="#md_tabs-4"><?php echo $t_analytics[$GLOBALS['LANGINDEX']]; ?></a></li>
			<?php } ?>
		</ul>
		<div id="md_tabs-1">
			<table class="data_write mgt10 mgl-20 pdl15" style="width:670px;">
				<colgroup>
					<col style="width:162px;"/>
					<col />
				</colgroup>
				<tr>
					<th class="top_txt"><?php echo $t_sensitivity[$GLOBALS['LANGINDEX']]; ?></th>						
					<td>
						<select id="event_<?php echo $event_name; ?>_md_sensitivity" class="selectbox_style">
							<option value="0" <?php if ($vaConf->mdConf->dataInfo['Sensitivity']['value']==0) echo "selected=\"selected\""; ?>><?php echo $t_very_low[$GLOBALS['LANGINDEX']]; ?></option>
							<option value="1" <?php if ($vaConf->mdConf->dataInfo['Sensitivity']['value']==1) echo "selected=\"selected\""; ?>><?php echo $t_low[$GLOBALS['LANGINDEX']]; ?></option>
							<option value="2" <?php if ($vaConf->mdConf->dataInfo['Sensitivity']['value']==2) echo "selected=\"selected\""; ?>><?php echo $t_normal[$GLOBALS['LANGINDEX']]; ?></option>
							<option value="3" <?php if ($vaConf->mdConf->dataInfo['Sensitivity']['value']==3) echo "selected=\"selected\""; ?>><?php echo $t_high[$GLOBALS['LANGINDEX']]; ?></option>
							<option value="4" <?php if ($vaConf->mdConf->dataInfo['Sensitivity']['value']==4) echo "selected=\"selected\""; ?>><?php echo $t_very_high[$GLOBALS['LANGINDEX']]; ?></option>
						</select>
					</td>
				</tr>
			</table>						
		</div>
		<div id="md_tabs-2">
			<table class="data_write mgt10 mgl-20 pdl15" style="width:630px;" >
				<colgroup>
					<col style="width:162px;"/>
					<col />
				</colgroup>
				<tbody>
				<tr>
					<th class="top_txt"><?php echo $t_size[$GLOBALS['LANGINDEX']]; ?></th>
					<td>
						<label><input type="radio" name="event_<?php echo $event_name; ?>_md_object_size" id="event_<?php echo $event_name; ?>_md_object_size_min" class="md_event_object_size_min" checked="checked" onClick='OnChangeObjectSize()'  style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_minimumSize[$GLOBALS['LANGINDEX']]; ?> (<?php echo $t_pixel[$GLOBALS['LANGINDEX']]; ?>)</label>
					</td>
				</tr>
				<tr>
					<td></td>
					<td style="padding-left:26px">
						<label>
							<?php echo $t_width[$GLOBALS['LANGINDEX']]; ?>
							<input type="text" id="md_min_width" class="objectSizeSpinner text" style="width:60px;" value="<?php echo $vaConf->mdConf->manualSize->dataInfo['MinWidth']['value']; ?>" maxlength="4"  readonly="readonly" />
						</label>
						<label>
							<?php echo $t_height[$GLOBALS['LANGINDEX']]; ?>
							<input type="text" id="md_min_height" class="objectSizeSpinner text" style="width:60px;" value="<?php echo $vaConf->mdConf->manualSize->dataInfo['MinHeight']['value']; ?>" maxlength="4"  readonly="readonly" />
						</label>
					</td>
				</tr>
				<tr></tr>
				<tr>
					<td></td>
					<td>
						<label><input type="radio" name="event_<?php echo $event_name; ?>_md_object_size" id="event_<?php echo $event_name; ?>_md_object_size_max" class="md_event_object_size_max" onClick='OnChangeObjectSize()' style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_maximumSize[$GLOBALS['LANGINDEX']]; ?> (<?php echo $t_pixel[$GLOBALS['LANGINDEX']]; ?>)</label>
					</td>
				</tr>
				<tr>
					<td></td>
					<td style="padding-left:26px">
						<label>
							<?php echo $t_width[$GLOBALS['LANGINDEX']]; ?>
							<input type="text" id="md_max_width" class="objectSizeSpinner text" style="width:60px;" value="<?php echo $vaConf->mdConf->manualSize->dataInfo['MaxWidth']['value']; ?>" maxlength="4"  readonly="readonly"/>
						</label>
						<label>
							<?php echo $t_height[$GLOBALS['LANGINDEX']]; ?>
							<input type="text" id="md_max_height" class="objectSizeSpinner text" style="width:60px;" value="<?php echo $vaConf->mdConf->manualSize->dataInfo['MaxHeight']['value']; ?>" maxlength="4" readonly="readonly"/>
						</label>
					</td>
				</tr>
				</tbody>
			</table>
		</div>
		<div id="md_tabs-3">
			<table class="data_write mgt10 mgl-20 pdl15" style='width:670px;'>
				<colgroup>
					<col style="width:162px;"/>
					<col />
				</colgroup>
				<tbody>
					<tr>
						<th class="top_txt"><?php echo $t_area[$GLOBALS['LANGINDEX']]; ?></th>
						<td>
							<input type="radio" name="event_<?php echo $event_name; ?>_detection_mode" value="1" id="event_<?php echo $event_name; ?>_detection_mode_on" class="event_detection_mode_on" <?php if($vaConf->mdConf->dataInfo['ObjectMode']['value'] == 1) echo "checked=\"checked\""; ?> onClick='OnClickDetectionMode()' style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><img id="detect_img" src="../images/common/detection.png" onclick="OnClickDetectionModeImage('on')" /><label style="vertical-align: top;" > <?php echo $t_detectionArea[$GLOBALS['LANGINDEX']]; ?></label>
						</td>
					</tr>
					<tr>
						<td></td>
						<td>
							<input type="radio" name="event_<?php echo $event_name; ?>_detection_mode" value="0" id="event_<?php echo $event_name; ?>_detection_mode_none" class="event_detection_mode_none" <?php if($vaConf->mdConf->dataInfo['ObjectMode']['value'] == 0) echo "checked=\"checked\""; ?> onClick='OnClickDetectionMode()' style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><img id="nonDetect_img" src="../images/common/non_detection.png" onclick="OnClickDetectionModeImage('none')" /><label style="vertical-align: top;" > <?php echo $t_nondetectionArea[$GLOBALS['LANGINDEX']]; ?></label>
						</td>
					</tr>
				</tbody>
			</table>
		</div>
		<?php if($GLOBALS['M_SUPPORT_EVENT_VA'] & IV_SUPPORT) { ?>
		<div id="md_tabs-4">
			<table class="data_write mgt10 mgl-20 pdl15"  style='width:670px;table-layout:fixed;' border="0">
				<colgroup>
					<col style="width:162px;"/>
					<col />
				</colgroup>
				<tbody>
					<tr>
						<th><?php echo $t_type[$GLOBALS['LANGINDEX']]; ?></th>
						<td colspan="2">
							<select id="event_<?php echo $event_name; ?>_analytics_type" class="selectbox_style" style="width:290px" onChange='OnChangeAnalyticsType()'>
								<option value="0"><?php echo $t_passing[$GLOBALS['LANGINDEX']]; ?></option>
								<option value="1"><?php echo $t_entering_exiting[$GLOBALS['LANGINDEX']]; ?></option>
								<option value="2"><?php echo $t_appearing_disappearing[$GLOBALS['LANGINDEX']]; ?></option>							
							</select>	
						</td>
					</tr>
					<tr>
						<th></th>
						<td colspan="2" height="19px">
							&nbsp;<label class="event_<?php echo $event_name; ?>_appearing_rules"><input type="radio" name="event_<?php echo $event_name; ?>_appearing_rules" id="event_<?php echo $event_name; ?>_appearing_rules_definedarea" onClick='OnChangeAnalyticsType()' style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-9';} else { echo '-6'; } ?>px" checked="checked"/><?php echo $t_defined_area[$GLOBALS['LANGINDEX']];  ?></label>
						</td>
					</tr>
					<tr>
						<th></th>
						<td colspan="2" height="19px">
							&nbsp;<label class="event_<?php echo $event_name; ?>_appearing_rules"><input type="radio" name="event_<?php echo $event_name; ?>_appearing_rules" id="event_<?php echo $event_name; ?>_appearing_rules_entirearea" onClick='OnChangeAnalyticsType()' style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-9';} else { echo '-6'; } ?>px"/><?php echo $t_entire_area[$GLOBALS['LANGINDEX']]; ?></label>
						</td>
					</tr>
				</tbody>
			</table>
		</div>
		<?php } ?>
	</div>
	<?php if($GLOBALS['M_ISP_TYPE'] != ISP_TYPE_HISILICON) { ?>
	<table class="data_write mgb25">
		<tbody>
			<tr>
				<th colspan="2"><?php echo $t_overlay[$GLOBALS['LANGINDEX']]; ?></th>
			</tr>
			<tr>
				<td style="padding-left:20px" colspan="2">
					<label><input type='checkbox' id='event_<?php echo $event_name; ?>_overlay_motion' <?php if ($vaConf->ivConf->dataInfo['VABoxDisplay']['value']==1) echo "checked=\"checked\""; ?> style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_detection_result_overlay[$GLOBALS['LANGINDEX']] ; ?></label>
				</td>
			</tr>
	<?php
		if($GLOBALS['M_SUPPORT_EVENT_VA'] & IV_SUPPORT) {
	?>
			<tr>
				<td style="padding-left:20px" colspan="2">										
					<label><input type="checkbox" id="event_<?php echo $event_name; ?>_overlay_rules" <?php if ($vaConf->ivConf->dataInfo['Overlay']['value']==1) echo "checked=\"checked\""; ?> style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_analytics_rule_overlay[$GLOBALS['LANGINDEX']]; ?></label>
				</td>
			</tr>
	<?php
		}
	?>
		</tbody>
	</table>
	<?php } ?>
</div>
