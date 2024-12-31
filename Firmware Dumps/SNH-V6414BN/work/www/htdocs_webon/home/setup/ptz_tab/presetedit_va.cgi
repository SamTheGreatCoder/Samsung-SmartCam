<script type="text/javascript" language="javascript">

var currentVaTab = '';

var halfX = 640;
var halfY = 512;
var currentVaMode = '';
var analyticsType = 0;

$(document).ready(function(){
	var ConfMinHeight={min:32,max:maxResolution.height};
	var ConfMinwidth={min:32,max:maxResolution.width};

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

function MakeVideoAnalyticsXml()
{
	var msg = "";
	msg += "<Mode>"+($('#event_<?php echo $event_name; ?>_mode_md').is(':checked') ? 0 : 1)+"</Mode>";
	msg += "<MDConfiguration>";
	msg += "<Enabled>"+($("#event_<?php echo $event_name; ?>_use_on").is(':checked') ? 1 : 0 )+"</Enabled>";
	msg += "<Sensitivity>"+$('#event_<?php echo $event_name; ?>_md_sensitivity').val()+"</Sensitivity>";
	msg += MakeManualSize('md');
	msg += EventSetup.VA.setMD_xml();
	msg += "</MDConfiguration>";
	msg += "<IVConfiguration>";
	msg += "<Enabled>"+($("#event_<?php echo $event_name; ?>_use_on").is(':checked') ? 1 : 0 )+"</Enabled>";
	msg += "<AnalyticsType>"+$('#event_<?php echo $event_name; ?>_analytics_type').val()+"</AnalyticsType>";
	msg += "<Sensitivity>"+$('#event_<?php echo $event_name; ?>_va_sensitivity').val()+"</Sensitivity>";
	msg += "<Overlay>"+($('#event_<?php echo $event_name; ?>_overlay_rules').is(':checked') ? 1 : 0)+"</Overlay>";
	msg += "<VABoxDisplay>"+($('#event_<?php echo $event_name; ?>_overlay_motion').is(':checked') ? 1 : 0)+"</VABoxDisplay>";	
	msg += MakeManualSize('va');
	msg += EventSetup.VA.setVA_xml();
	msg += "</IVConfiguration>";

	return msg;
}

function ParsingXML_VAConfiguration(xmlData)
{	
	$('input:radio[name=event_<?php echo $event_name; ?>_mode]').filter('[value="'+xmlData.find('Mode').text()+'"]').prop("checked", true);
	xmlData.find("MDConfiguration").each(function() {
		$('input:radio[name=event_<?php echo $event_name; ?>_md_use]').filter('[value="'+$(this).find('Enabled').text()+'"]').prop("checked", true);
		$('#event_<?php echo $event_name; ?>_md_sensitivity').val($(this).find('Sensitivity').text());	
		$("#md_min_width").val($(this).find('MinWidth').text());
		$("#md_min_height").val($(this).find('MinHeight').text());
		$("#md_max_width").val($(this).find('MaxWidth').text());
		$("#md_max_height").val($(this).find('MaxHeight').text());
	});
	xmlData.find("IVConfiguration").each(function() {
		$('input:radio[name=event_<?php echo $event_name; ?>_va_use]').filter('[value="'+$(this).find('Enabled').text()+'"]').prop("checked", true);
		$('#event_<?php echo $event_name; ?>_analytics_type').val($(this).find('AnalyticsType').text());	
		$('#event_<?php echo $event_name; ?>_va_sensitivity').val($(this).find('Sensitivity').text());	
		$('#event_<?php echo $event_name; ?>_overlay_motion').prop('checked', ($(this).find('VABoxDisplay').text()=='1'?true:false));
		$('#event_<?php echo $event_name; ?>_overlay_rules').prop('checked', ($(this).find('Overlay').text()=='1'?true:false));
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

	var MaxVaCount = {passing:1, entering:1, appearing:1};
	
	//var msg = EventSetup.xmlToString(xmlData);
	EventSetup.MD.init(viewerWidth,viewerHeight,maxResolution.width,maxResolution.height,EventSetup.TYPE_RECT,0);
	EventSetup.MD.getMDPolygon(xmlData);

	EventSetup.VA.init(true, MaxVaCount.entering);
	EventSetup.VA.getPolygon(xmlData);

	EventSetup.VA.lineDraw(MaxVaCount.passing);	
	EventSetup.VA.getLine(xmlData);

	EventSetup.VA.initRectangle(EventSetup.TYPE_RECT,MaxVaCount.appearing);
	EventSetup.VA.getRectangle(xmlData);

	EventSetup.MD.minMaxRectangle(); //min max size
}

function MakeManualSize(mode)
{
	var msg  = '';
	var minWidth = parseInt($("#"+mode+"_min_width").val())/(1920/viewerWidth);
	var minHeight = parseInt($("#"+mode+"_min_height").val())/(1080/viewerHeight);
	var maxWidth = parseInt($("#"+mode+"_max_width").val())/(1920/viewerWidth);
	var maxHeight = parseInt($("#"+mode+"_max_height").val())/(1080/viewerHeight);
	msg += "<ManualSize>";/*
	var vsl = Math.ceil((minHeight/viewerHeight)*99);
	var vsh = Math.ceil((maxHeight/viewerHeight)*99);
	var hsl = Math.ceil((minWidth/640)*99);
	var hsh = Math.ceil((maxWidth/640)*99);
	if(vsl > 99) vsl = 99;
	if(vsh > 99) vsh = 99;
	if(hsl > 99) hsl = 99;
	if(hsh > 99) hsh = 99;
	msg += "<VSL>" + vsl + "</VSL>";
	msg += "<VSH>" + vsh + "</VSH>";
	msg += "<HSL>" + hsl + "</HSL>";
	msg += "<HSH>" + hsh + "</HSH>";*/
	msg += "<MinWidth>" + $("#"+mode+"_min_width").val() + "</MinWidth>";
	msg += "<MinHeight>" + $("#"+mode+"_min_height").val() + "</MinHeight>";
	msg += "<MaxWidth>" + $("#"+mode+"_max_width").val() + "</MaxWidth>";
	msg += "<MaxHeight>" + $("#"+mode+"_max_height").val() + "</MaxHeight>";
	msg += "</ManualSize>";
	return msg;
}

function OnClickVaMode()
{	
	$("#md_tabs").tabs();
	$("#va_tabs").tabs();
	if ($('#event_<?php echo $event_name; ?>_mode_md').is(':checked')) {	// MD
		currentVaMode = 'md';
		$('.md_area').show();
		$('.va_area').hide();	
		$("#md_tabs .ui-tabs-panel").css("height", "140px");
		$("#md_tabs").tabs("option", "active", 0);
	}
	else {		// IV
		currentVaMode = 'va';
		$('.md_area').hide();
		$('.va_area').show();
		$("#va_tabs .ui-tabs-panel").css("height", "140px");
		$("#va_tabs").tabs("option", "active", 0);
	}
	currentVaTab = 'sense';
	EventSetup.VA.view("");
}

function OnClickVaTabs(name)
{		
	currentVaTab = name;
	
	switch (name) {
		case 'size':	
			EventSetup.minMdObjX = -1;
			EventSetup.minMdObjY = -1;
			EventSetup.maxMdObjX = -1;
			EventSetup.maxMdObjY = -1;
			
			EventSetup.VA.view("max_min");
			OnChangeObjectSize();
			break;
		case 'area':
			EventSetup.VA.view("MDPolyDraw");	
			EventSetup.MD.updatePolygon();
			break;		
		case 'rule':		
			//$('#event_<?php echo $event_name; ?>_analytics_type').val(analyticsType);	
			OnChangeAnalyticsType();
			break;
		default: 		EventSetup.VA.view(""); 	break;
	}
}

function OnChangeObjectSize()
{
	if ($('#event_<?php echo $event_name; ?>_'+currentVaMode+'_object_size_min').is(':checked')) {			//min obj
		$("#"+currentVaMode+"_min_width").spinner({ disabled: false }); 
		$("#"+currentVaMode+"_min_height").spinner({ disabled: false }); 
		$("#"+currentVaMode+"_max_width").spinner({ disabled: true }); 
		$("#"+currentVaMode+"_max_height").spinner({ disabled: true });
		
		$("#minRect").css("opacity","0.4");
		$("#maxRect").css("opacity","0.2");
		$("#minMaxTemp").css("border","1px solid blue");		
	}
	else if ($('#event_<?php echo $event_name; ?>_'+currentVaMode+'_object_size_max').is(':checked')) {		//max obj
		$("#"+currentVaMode+"_max_width").spinner({ disabled: false }); 
		$("#"+currentVaMode+"_max_height").spinner({ disabled: false }); 
		$("#"+currentVaMode+"_min_width").spinner({ disabled: true }); 
		$("#"+currentVaMode+"_min_height").spinner({ disabled: true });

		$("#minRect").css("opacity","0.2");
		$("#maxRect").css("opacity","0.4");
		$("#minMaxTemp").css("border","1px solid red");		
	}
	EventSetup.MD.setMaxMinArea();	
}

function OnChangeAnalyticsType()
{
	switch(parseInt($('#event_<?php echo $event_name; ?>_analytics_type').val())) {
		case 0:	// passing
			EventSetup.VA.view("lineDraw");		// virtual line
			EventSetup.VA.reDrawLine();
			break;
		case 1:	// Entering&Exiting
			EventSetup.VA.view("polyDraw");
			EventSetup.VA.reDrawVaPolygon();
			break;
		case 2:	// Appear(Disappear)
			EventSetup.VA.view("rectangleDraw");
			EventSetup.VA.reDrawRectangle();
	}
}

</script>

<table class="data_write mgt20">
	<colgroup>
		<col style="width:150px;"/>
		<col style="width:150px;"/>
		<col />
	</colgroup>
	<tbody>
		<tr>
			<th scope="row"><?php echo $t_enable[$GLOBALS['LANGINDEX']]; ?></th>
			<td>
				<label><input type="radio" name="event_<?php echo $event_name; ?>_md_use" id="event_<?php echo $event_name; ?>_use_on"	value="1" <?php if ($vaConf->mdConf->dataInfo['Enabled']['value'] == 1 || $vaConf->ivConf->dataInfo['Enabled']['value'] == 1) echo "checked=\"checked\""; ?> style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_on[$GLOBALS['LANGINDEX']]; ?></label>
			</td>
			<td style="padding-left:3px;">
				<label><input type="radio" name="event_<?php echo $event_name; ?>_md_use" id="event_<?php echo $event_name; ?>_use_off" value="0" <?php if ($vaConf->mdConf->dataInfo['Enabled']['value'] == 0 && $vaConf->ivConf->dataInfo['Enabled']['value'] == 0) echo "checked=\"checked\""; ?> /><?php echo $t_off[$GLOBALS['LANGINDEX']]; ?></label>
			</td>
		</tr>	
		<tr>
			<th><?php echo $t_mode[$GLOBALS['LANGINDEX']] ?></th>
			<td>
				<label><input type="radio" name="event_<?php echo $event_name; ?>_mode" id="event_<?php echo $event_name; ?>_mode_md" value="0" <?php if($vaConf->dataInfo['Mode']['value'] == 0) echo "checked=\"checked\""; ?> onClick='OnClickVaMode()' style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_md[$GLOBALS['LANGINDEX']]; ?></label>
			</td>
			<td>
				<label><input type="radio" name="event_<?php echo $event_name; ?>_mode" id="event_<?php echo $event_name; ?>_mode_va" value="1" <?php if($vaConf->dataInfo['Mode']['value'] == 1) echo "checked=\"checked\""; ?> onClick='OnClickVaMode()' style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_videoAnalytics[$GLOBALS['LANGINDEX']]; ?></label>
			</td>
		</tr>
	</tbody>
</table>
<div id="md_tabs" class="md_area" style="margin-top:20px; margin-bottom:10px; margin-left:9px">
	<ul>
		<li><a href="#md_tabs-1" onClick="OnClickVaTabs('sense')"><?php echo $t_sensitivity[$GLOBALS['LANGINDEX']]; ?></a></li>
		<li><a href="#md_tabs-2" onClick="OnClickVaTabs('size')"><?php echo $t_size[$GLOBALS['LANGINDEX']]; ?></a></li>
		<li><a href="#md_tabs-3" onClick="OnClickVaTabs('area')"><?php echo $t_area[$GLOBALS['LANGINDEX']]; ?></a></li>
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
						<label><input type="radio" name="event_<?php echo $event_name; ?>_md_object_size" id="event_<?php echo $event_name; ?>_md_object_size_min" class="md_event_object_size_min" checked="checked" onClick='OnChangeObjectSize()'	style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_minimumSize[$GLOBALS['LANGINDEX']]; ?> (<?php echo $t_pixel[$GLOBALS['LANGINDEX']]; ?>)</label>
					</td>
				</tr>
				<tr>
					<td></td>
					<td style="padding-left:26px">
						<label>
							<?php echo $t_width[$GLOBALS['LANGINDEX']]; ?>
							<input type="text" id="md_min_width" class="objectSizeSpinner text" style="width:60px; margin-left:5px" value="<?php echo $vaConf->mdConf->manualSize->dataInfo['MinWidth']['value']; ?>" maxlength="4"  readonly="readonly" />
						</label>
						<label>
							<?php echo $t_height[$GLOBALS['LANGINDEX']]; ?>
							<input type="text" id="md_min_height" class="objectSizeSpinner text" style="width:60px; margin-left:5px" value="<?php echo $vaConf->mdConf->manualSize->dataInfo['MinHeight']['value']; ?>" maxlength="4"	readonly="readonly" />
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
							<input type="text" id="md_max_width" class="objectSizeSpinner text" style="width:60px; margin-left:5px" value="<?php echo $vaConf->mdConf->manualSize->dataInfo['MaxWidth']['value']; ?>" maxlength="4"  readonly="readonly"/>
						</label>
						<label>
							<?php echo $t_height[$GLOBALS['LANGINDEX']]; ?>
							<input type="text" id="md_max_height" class="objectSizeSpinner text" style="width:60px; margin-left:5px" value="<?php echo $vaConf->mdConf->manualSize->dataInfo['MaxHeight']['value']; ?>" maxlength="4" readonly="readonly"/>
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
						<label><input type="radio" name="event_<?php echo $event_name; ?>>_detection_mode" id="event_<?php echo $event_name; ?>>_detection_mode_on" class="event_detection_mode_on" checked="checked" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_detectionArea[$GLOBALS['LANGINDEX']]; ?></label>
					</td>
				</tr> 	
			</tbody>
		</table>
	</div>
</div>

<div id="va_tabs" class="va_area" style="margin-top:20px; margin-bottom:10px; margin-left:9px">
	<ul>
		<li><a href="#va_tabs-1" onClick="OnClickVaTabs('sense')"><?php echo $t_sensitivity[$GLOBALS['LANGINDEX']]; ?></a></li>
		<li><a href="#va_tabs-2" onClick="OnClickVaTabs('size')"><?php echo $t_size[$GLOBALS['LANGINDEX']]; ?></a></li>
		<li><a href="#va_tabs-4" onClick="OnClickVaTabs('rule')"><?php echo $t_analytics[$GLOBALS['LANGINDEX']]; ?></a></li>
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
						<label><input type="radio" name="event_<?php echo $event_name; ?>_va_object_size" id="event_<?php echo $event_name; ?>_va_object_size_min" class="va_event_object_size_min" checked="checked" onClick='OnChangeObjectSize()'  style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_minimumSize[$GLOBALS['LANGINDEX']]; ?> (<?php echo $t_pixel[$GLOBALS['LANGINDEX']]; ?>)</label>
					</td>
				</tr>
				<tr>
					<td></td>
					<td style="padding-left:26px">
						<label>
							<?php echo $t_width[$GLOBALS['LANGINDEX']]; ?>
							<input type="text" id="va_min_width" class="objectSizeSpinner text" style="width:60px; margin-left:5px" value="<?php echo $vaConf->ivConf->manualSize->dataInfo['MinWidth']['value']; ?>" maxlength="4"  readonly="readonly" />
						</label>
						<label>
							<?php echo $t_height[$GLOBALS['LANGINDEX']]; ?>
							<input type="text" id="va_min_height" class="objectSizeSpinner text" style="width:60px; margin-left:5px" value="<?php echo $vaConf->ivConf->manualSize->dataInfo['MinHeight']['value']; ?>" maxlength="4"  readonly="readonly" />
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
							<input type="text" id="va_max_width" class="objectSizeSpinner text" style="width:60px; margin-left:5px" value="<?php echo $vaConf->ivConf->manualSize->dataInfo['MaxWidth']['value']; ?>" maxlength="4"  readonly="readonly"/>
						</label>
						<label>
							<?php echo $t_height[$GLOBALS['LANGINDEX']]; ?>
							<input type="text" id="va_max_height" class="objectSizeSpinner text" style="width:60px; margin-left:5px" value="<?php echo $vaConf->ivConf->manualSize->dataInfo['MaxHeight']['value']; ?>" maxlength="4" readonly="readonly"/>
						</label>
					</td>
				</tr>
			</tbody>
		</table>
	</div>
	<div id="va_tabs-4">
		<table class="data_write mgt10 mgl-20 pdl15"  style='width:670px;table-layout:fixed;'>
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
					<th><?php echo $t_overlay[$GLOBALS['LANGINDEX']]; ?></th>
					<td>
						<label><input type='checkbox' id='event_<?php echo $event_name; ?>_overlay_motion' <?php if ($vaConf->ivConf->dataInfo['VABoxDisplay']['value']==1) echo "checked=\"checked\""; ?> style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_detection_result_overlay[$GLOBALS['LANGINDEX']] ; ?></label>
					</td>
				</tr>
				<tr>
					<td></td>
					<td>
						<label><input type="checkbox" id="event_<?php echo $event_name; ?>_overlay_rules" <?php if ($vaConf->ivConf->dataInfo['Overlay']['value']==1) echo "checked=\"checked\""; ?> style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_analytics_rule_overlay[$GLOBALS['LANGINDEX']]; ?></label>
					</td>
				</tr>
			</tbody>
		</table>
	</div>	
</div>
