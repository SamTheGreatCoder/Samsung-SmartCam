<script type="text/javascript" language="javascript">

$(document).ready(function(){	
	var ConfMinHeight	= {min:32,max: <?php echo $GLOBALS['MAX_RESOLUTION']['height']; ?>};
	var ConfMinwidth 	= {min:32,max: <?php echo $GLOBALS['MAX_RESOLUTION']['width']; ?>};
	
	$("#va_tabs").tabs({
		activate:function(event){
			var tabIndex = parseInt($("#va_tabs").tabs("option", "active"),10);
			if(tabIndex == 2)		//analytics
				tabIndex = 3;		//chnage to analytics index
			OnChangeVaTabs(tabIndex);
		}
	});

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

function InitIVConfiguration(xml_data)
{	
	EventSetup.MD.init(viewerWidth,viewerHeight,maxResolution.width,maxResolution.height,EventSetup.TYPE_RECT,0, true); 						//MD Rectangle 
	EventSetup.MD.getMDPolygon(xml_data);

	var MaxVaCount = {passing:1, entering:1, appearing:1};
	EventSetup.VA.lineDraw(MaxVaCount.passing);								//passing
	EventSetup.VA.getLine(xml_data);
	EventSetup.VA.init(true,MaxVaCount.entering);						//Entering/Exiting
	EventSetup.VA.getPolygon(xml_data);
	EventSetup.VA.initRectangle(EventSetup.TYPE_RECT, MaxVaCount.appearing);		//Rectangle
	EventSetup.VA.getRectangle(xml_data);
	
	EventSetup.MD.minMaxRectangle(); //min max size

	window.setTimeout(function(){
		OnClickVaMode(currentVaMode);
	},500);
}

function MakeVideoAnalyticsXml()
{
	var msg = "";
	var mdvaMode = ($('#event_<?php echo $event_name; ?>_mode_md').is(':checked') ? 0 : ($('#event_<?php echo $event_name; ?>_mode_va').is(':checked') ? 1 : 2));
	msg += "<Mode>"+mdvaMode+"</Mode>";
	msg += "<MDConfiguration>";
	msg += "<Enabled>"+($("#event_<?php echo $event_name; ?>_use_on").is(':checked')? 1 : 0)+"</Enabled>";
	msg += "<ObjectMode>"+($('#event_<?php echo $event_name; ?>_detection_mode_on').is(':checked') ? 1 : 0)+"</ObjectMode>";
	msg += "<Sensitivity>"+$('#event_<?php echo $event_name; ?>_md_sensitivity').val()+"</Sensitivity>";
	msg += MakeManualSize('md');
	msg += "<VABoxDisplay>"+($('#event_<?php echo $event_name; ?>_overlay_motion').is(':checked') ? 1 : 0)+"</VABoxDisplay>";
	msg += EventSetup.VA.setMD_xml();
	
	if (currentMdVaSetupType == 'global') {
	<?php if($GLOBALS['M_SPECIAL_TYPE'] == 1) { ?>	
		msg += MakeScheduleAndActionSetupXML_S1("<?php echo $event_name; ?>");
	<?php } else { ?>
		msg += MakeScheduleAndActionSetupXML("<?php echo $event_name; ?>");
	<?php } ?>
	}
	msg += "</MDConfiguration>";
	msg += "<IVConfiguration>";
	msg += "<Enabled>"+($("#event_<?php echo $event_name; ?>_use_on").is(':checked')? 1 : 0)+"</Enabled>";
	msg += "<AnalyticsType>"+$('#event_<?php echo $event_name; ?>_analytics_type').val()+"</AnalyticsType>";
	msg += "<Sensitivity>"+$('#event_<?php echo $event_name; ?>_va_sensitivity').val()+"</Sensitivity>";
	<?php if($GLOBALS['M_ISP_TYPE'] != ISP_TYPE_WN3_PTZ) { ?>
	msg += "<Overlay>"+($('#event_<?php echo $event_name; ?>_overlay_rules').is(':checked') ? 1 : 0)+"</Overlay>";
	<?php } ?>
	msg += "<VABoxDisplay>"+($('#event_<?php echo $event_name; ?>_overlay_motion').is(':checked') ? 1 : 0)+"</VABoxDisplay>";
	msg += MakeManualSize('va');		
	msg += EventSetup.VA.setVA_xml();
	msg += "</IVConfiguration>";
	return msg;
}

function OnClickVaMode(mdvaMode)
{
	currentVaMode = mdvaMode;
	if (mdvaMode == 'md') {	// MD
		$("#md_tabs").show();
		$("#va_tabs").hide();	
	}
	else {		// VA		
		$("#md_tabs").hide();
		$("#va_tabs").show();
	}
	$("#"+currentVaMode+"_tabs .ui-tabs-panel").css("height", "140px");
	$("#"+currentVaMode+"_tabs").tabs("option", "active", 0);
	EventSetup.VA.view("");
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
			EventSetup.VA.view("rectangleDraw");
			EventSetup.VA.reDrawRectangle();
	}
}

function ParsingXML_VAConfiguration(xmlData)
{
	var modeVal = parseInt(xmlData.find('Mode').text());
	$('input:radio[name=event_<?php echo $event_name; ?>_mode]').filter('[value="'+modeVal+'"]').prop("checked", true);
	xmlData.find("MDConfiguration").each(function() {
		$('input:radio[name=event_<?php echo $event_name; ?>_use]').filter('[value="'+$(this).find('Enabled').text()+'"]').prop("checked", true);
		$('#event_<?php echo $event_name; ?>_md_sensitivity').val($(this).find('Sensitivity').text());	
		$("#md_min_width").val($(this).find('MinWidth').text());
		$("#md_min_height").val($(this).find('MinHeight').text());
		$("#md_max_width").val($(this).find('MaxWidth').text());
		$("#md_max_height").val($(this).find('MaxHeight').text());
	});
	xmlData.find("IVConfiguration").each(function() {
		$('input:radio[name=event_<?php echo $event_name; ?>_use]').filter('[value="'+$(this).find('Enabled').text()+'"]').prop("checked", true);
		$('#event_<?php echo $event_name; ?>_analytics_type').val($(this).find('AnalyticsType').text());	
		$('#event_<?php echo $event_name; ?>_va_sensitivity').val($(this).find('Sensitivity').text());	
		$('#event_<?php echo $event_name; ?>_overlay_motion').prop('checked', ($(this).find('VABoxDisplay').text()=='1'?true:false));
		<?php if($GLOBALS['M_ISP_TYPE'] != ISP_TYPE_WN3_PTZ) { ?>
		$('#event_<?php echo $event_name; ?>_overlay_rules').prop('checked', ($(this).find('Overlay').text()=='1'?true:false));
		<?php } ?>
		$("#va_min_width").val($(this).find('MinWidth').text());
		$("#va_min_height").val($(this).find('MinHeight').text());
		$("#va_max_width").val($(this).find('MaxWidth').text());
		$("#va_max_height").val($(this).find('MaxHeight').text());
	});
	
	$("#polyDraw div").remove();
	$("#fullScreen div").remove();
	$("#lineDraw div").remove();
	$("#rectangleDraw div").remove();
	$("#MDPolyDraw div").remove();

	currentVaMode = (modeVal == 0 ? 'md' : 'va');
	InitIVConfiguration(xmlData);
}

</script>
<div style="position:relative">
	<div id="DisableIVSelectLayer" style="position:absolute; width:680px; height:340px; left: 0px; top: -175px; background-color:#000000; display:none; z-index:1000; filter:alpha(opacity=0.3); opacity:0.3; -moz-opacity:0.3; -ms-filter: 'progid:DXImageTransform.Microsoft.Alpha(Opacity=30)';"></div>
	<div id="md_tabs" style="display:none; margin-top:20px; margin-bottom:10px; margin-left:9px">
		<ul>
			<li><a href="#md_tabs-1"><?php echo $t_sensitivity[$GLOBALS['LANGINDEX']]; ?></a></li>
			<li><a href="#md_tabs-2"><?php echo $t_size[$GLOBALS['LANGINDEX']]; ?></a></li>
			<li><a href="#md_tabs-3"><?php echo $t_area[$GLOBALS['LANGINDEX']]; ?></a></li>		
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
							<label><input type="radio" name="event_<?php echo $event_name; ?>_detection_mode" id="event_<?php echo $event_name; ?>_detection_mode_on" class="event_detection_mode_on" checked="checked" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_detectionArea[$GLOBALS['LANGINDEX']]; ?></label>
						</td>
					</tr>
				</tbody>
			</table>
		</div>
	</div>
	<div id="va_tabs" style="display:none; margin-top:20px; margin-bottom:10px; margin-left:9px">
		<ul>
			<li><a href="#va_tabs-1"><?php echo $t_sensitivity[$GLOBALS['LANGINDEX']]; ?></a></li>
			<li><a href="#va_tabs-2"><?php echo $t_size[$GLOBALS['LANGINDEX']]; ?></a></li>
			<li><a href="#va_tabs-3"><?php echo $t_analytics[$GLOBALS['LANGINDEX']]; ?></a></li>
		</ul>
		<div id="va_tabs-1">
			<table class="data_write mgt10 mgl-20 pdl15" style="width:670px;" border=0>
				<colgroup>
					<col style="width:162px;"/>
					<col />
				</colgroup>
				<tr>
					<th class="top_txt"><?php echo $t_sensitivity[$GLOBALS['LANGINDEX']]; ?></th> 					
					<td>
						<select id="event_<?php echo $event_name; ?>_va_sensitivity" class="selectbox_style">
							<option value="0" <?php if ($vaConf->ivConf->dataInfo['Sensitivity']['value']==0) echo "selected=\"selected\""; ?>><?php echo $t_very_low[$GLOBALS['LANGINDEX']]; ?></option>
							<option value="1" <?php if ($vaConf->ivConf->dataInfo['Sensitivity']['value']==1) echo "selected=\"selected\""; ?>><?php echo $t_low[$GLOBALS['LANGINDEX']]; ?></option>
							<option value="2" <?php if ($vaConf->ivConf->dataInfo['Sensitivity']['value']==2) echo "selected=\"selected\""; ?>><?php echo $t_normal[$GLOBALS['LANGINDEX']]; ?></option>
							<option value="3" <?php if ($vaConf->ivConf->dataInfo['Sensitivity']['value']==3) echo "selected=\"selected\""; ?>><?php echo $t_high[$GLOBALS['LANGINDEX']]; ?></option>
							<option value="4" <?php if ($vaConf->ivConf->dataInfo['Sensitivity']['value']==4) echo "selected=\"selected\""; ?>><?php echo $t_very_high[$GLOBALS['LANGINDEX']]; ?></option>
						</select>
					</td>
				</tr>
			</table> 					
		</div>
		<div id="va_tabs-2">
			<table class="data_write mgt10 mgl-20 pdl15" style="width:630px;" >
				<colgroup>
					<col style="width:162px;"/>
					<col />
				</colgroup>
				<tbody>
				<tr>
					<th class="top_txt"><?php echo $t_size[$GLOBALS['LANGINDEX']]; ?></th>
					<td>
						<label><input type="radio" name="event_<?php echo $event_name; ?>_va_object_size" id="event_<?php echo $event_name; ?>_va_object_size_min" class="va_event_object_size_min" checked="checked" onClick='OnChangeObjectSize()'	style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_minimumSize[$GLOBALS['LANGINDEX']]; ?> (<?php echo $t_pixel[$GLOBALS['LANGINDEX']]; ?>)</label>
					</td>
				</tr>
				<tr>
					<td></td>
					<td style="padding-left:26px">
						<label>
							<?php echo $t_width[$GLOBALS['LANGINDEX']]; ?>
							<input type="text" id="va_min_width" class="objectSizeSpinner text" style="width:60px;" value="<?php echo $vaConf->ivConf->manualSize->dataInfo['MinWidth']['value']; ?>" maxlength="4"  readonly="readonly" />
						</label>
						<label>
							<?php echo $t_height[$GLOBALS['LANGINDEX']]; ?>
							<input type="text" id="va_min_height" class="objectSizeSpinner text" style="width:60px;" value="<?php echo $vaConf->ivConf->manualSize->dataInfo['MinHeight']['value']; ?>" maxlength="4" readonly="readonly" />
						</label>
					</td>
				</tr>
				<tr></tr>
				<tr>
					<td></td>
					<td>
						<label><input type="radio" name="event_<?php echo $event_name; ?>_va_object_size" id="event_<?php echo $event_name; ?>_va_object_size_max" class="va_event_object_size_max" onClick='OnChangeObjectSize()' style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_maximumSize[$GLOBALS['LANGINDEX']]; ?> (<?php echo $t_pixel[$GLOBALS['LANGINDEX']]; ?>)</label>
					</td>
				</tr>
				<tr>
					<td></td>
					<td style="padding-left:26px">
						<label>
							<?php echo $t_width[$GLOBALS['LANGINDEX']]; ?>
							<input type="text" id="va_max_width" class="objectSizeSpinner text" style="width:60px;" value="<?php echo $vaConf->ivConf->manualSize->dataInfo['MaxWidth']['value']; ?>" maxlength="4"  readonly="readonly"/>
						</label>
						<label>
							<?php echo $t_height[$GLOBALS['LANGINDEX']]; ?>
							<input type="text" id="va_max_height" class="objectSizeSpinner text" style="width:60px;" value="<?php echo $vaConf->ivConf->manualSize->dataInfo['MaxHeight']['value']; ?>" maxlength="4" readonly="readonly"/>
						</label>
					</td>
				</tr>
				</tbody>
			</table>
		</div>
		<div id="va_tabs-3">
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
								<option value="0" <?php if ($vaConf->ivConf->dataInfo['AnalyticsType']['value']==0) echo "selected=\"selected\""; ?>><?php echo $t_passing[$GLOBALS['LANGINDEX']]; ?></option>
								<option value="1" <?php if ($vaConf->ivConf->dataInfo['AnalyticsType']['value']==1) echo "selected=\"selected\""; ?>><?php echo $t_entering_exiting[$GLOBALS['LANGINDEX']]; ?></option>
								<option value="2" <?php if ($vaConf->ivConf->dataInfo['AnalyticsType']['value']==2) echo "selected=\"selected\""; ?>><?php echo $t_appearing_disappearing[$GLOBALS['LANGINDEX']]; ?></option>							
							</select>	
						</td>
					</tr>
					<tr>
						<th><?php echo $t_overlay[$GLOBALS['LANGINDEX']]; ?></th>
						<td>
							<label><input type='checkbox' id='event_<?php echo $event_name; ?>_overlay_motion' <?php if ($vaConf->ivConf->dataInfo['VABoxDisplay']['value']==1) echo "checked=\"checked\""; ?> style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_detection_result_overlay[$GLOBALS['LANGINDEX']] ; ?></label>
						</td>
					</tr>
					<?php if($GLOBALS['M_ISP_TYPE'] != ISP_TYPE_WN3_PTZ) { ?>
					<tr>
						<td></td>
						<td>
							<label><input type="checkbox" id="event_<?php echo $event_name; ?>_overlay_rules" <?php if ($vaConf->ivConf->dataInfo['Overlay']['value']==1) echo "checked=\"checked\""; ?> style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_analytics_rule_overlay[$GLOBALS['LANGINDEX']]; ?></label>
						</td>
					</tr>
					<?php } ?>
				</tbody>
			</table>
		</div>	
	</div>
</div>
