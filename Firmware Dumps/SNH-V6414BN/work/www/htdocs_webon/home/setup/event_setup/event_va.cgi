<script type="text/javascript" language="javascript">

var currentVaMode = '';

$(document).ready(function(){	
	var ConfMinHeight={min:24,max:maxResolution.height};
	var ConfMinwidth={min:24,max:maxResolution.width};	
	
	<?php if($GLOBALS['M_SUPPORT_PTZ'] == PTZ_SUPPORT){?>
		ConfMinHeight.min = 32;
		ConfMinwidth.min = 32;
	
		$("#va_tabs").tabs({
			activate:function(event){
				var tabIndex = parseInt($("#va_tabs").tabs("option", "active"),10);
				if(tabIndex == 2)		//analytics
					tabIndex = 3;		//chnage to analytics index
				OnChangeVaTabs(tabIndex);
			}
		});
	<?php } ?>

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

function InitIVConfiguration(){
	var xmlData = "<?php echo $event_class->GetXMLData(); ?>";
	var xml_data=$.parseXML(xmlData);
		
	<?php if($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_HISILICON || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3){ ?>
		EventSetup.MD.init(viewerWidth,viewerHeight,maxResolution.width,maxResolution.height,EventSetup.TYPE_POLY,GetFilpMirrorStatus());		//MD Polygon	
		EventSetup.MD.getMDPolygon($(xml_data));
	<?php } else{ ?>
		EventSetup.MD.init(viewerWidth,viewerHeight,maxResolution.width,maxResolution.height,EventSetup.TYPE_RECT,0); 						//MD Rectangle 
		EventSetup.MD.getMDPolygon($(xml_data));
	<?php } ?>
	<?php if ($GLOBALS['M_SUPPORT_EVENT_VA'] & IV_SUPPORT) { ?> 	//IV
		var MaxVaCount = {passing:3, entering:3, appearing:3};
		<?php if($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ){ ?>
			MaxVaCount = {passing:1, entering:1, appearing:1};
		<?php }else if($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3){ ?>
			MaxVaCount = {passing:3, entering:3, appearing:3};
		<?php }?>
	
		EventSetup.VA.lineDraw(MaxVaCount.passing);								//passing
		EventSetup.VA.getLine($(xml_data));
		<?php if($GLOBALS['M_SUPPORT_PTZ'] == PTZ_SUPPORT){?>
			EventSetup.VA.init(true,MaxVaCount.entering);						//Entering/Exiting
		<?php }else{ ?>
			EventSetup.VA.init(false,MaxVaCount.entering);						//Entering/Exiting
		<?php } ?>
		EventSetup.VA.getPolygon($(xml_data));

		<?php if($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ){ ?>		 	//Appearing/Disappearing
			EventSetup.VA.initRectangle(EventSetup.TYPE_RECT, MaxVaCount.appearing);		//Rectangle
		<?php }else if($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3){ ?>
			EventSetup.VA.initRectangle(EventSetup.TYPE_POLY, MaxVaCount.appearing);		//Polygon
		<?php } ?>
		
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
	<?php if (($GLOBALS['M_SUPPORT_EVENT_VA'] & IV_SUPPORT) && ($GLOBALS['M_SUPPORT_EVENT_VA'] & MD_SUPPORT)) { ?>
	msg += "<Mode>"+$('#event_<?php echo $event_name; ?>_mode').val()+"</Mode>";
	<?php } ?>
	msg += "<MDConfiguration>";
	msg += "<Enabled>"+($("#event_<?php echo $event_name; ?>_use_on").is(':checked')? 1 : 0)+"</Enabled>";
	
	<?php if(!($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ)){ ?>
	msg += "<ObjectMode>"+($('#event_<?php echo $event_name; ?>_detection_mode_on').is(':checked') ? 1 : 0)+"</ObjectMode>";
	msg += "<ObjectSize>5</ObjectSize>"; // always manual size
	<?php } ?>
	msg += "<Sensitivity>"+$('#event_<?php echo $event_name; ?>_md_sensitivity').val()+"</Sensitivity>";
	msg += MakeManualSize('md');
	
	<?php if($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_HISILICON || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ){ ?>
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
		<?php if($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ){ ?>
		msg += "<AnalyticsType>"+$('#event_<?php echo $event_name; ?>_analytics_type').val()+"</AnalyticsType>";
		<?php } ?>
		msg += "<Sensitivity>"+$('#event_<?php echo $event_name; ?>_va_sensitivity').val()+"</Sensitivity>";
		msg += "<Overlay>"+($('#event_<?php echo $event_name; ?>_overlay_rules').is(':checked') ? 1 : 0)+"</Overlay>";
		msg += "<VABoxDisplay>"+($('#event_<?php echo $event_name; ?>_overlay_motion').is(':checked') ? 1 : 0)+"</VABoxDisplay>";
		msg += MakeManualSize('va');		
		msg += EventSetup.VA.setVA_xml();
		msg += "</IVConfiguration>";
	<?php } ?>
	return msg;
}

function MakeManualSize(mode)
{
	var msg  = '';
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
	<?php if($GLOBALS['M_SUPPORT_PTZ'] == PTZ_SUPPORT){?>
		if ($('#event_<?php echo $event_name; ?>_mode').val() == 0) {	// MD
			currentVaMode = 'md';
			$("#md_tabs").show();
			$("#va_tabs").hide();	
			$("#md_tabs .ui-tabs-panel").css("height", "140px");
			$("#md_tabs").tabs("option", "active", 0);
		}
		else {		// IV
			currentVaMode = 'va';
			$("#md_tabs").hide();
			$("#va_tabs").show();
			$("#va_tabs .ui-tabs-panel").css("height", "140px");
			$("#va_tabs").tabs("option", "active", 0);
		}
		EventSetup.VA.view("");
	<?php }else{ ?>
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
	<?php } ?>
}

function OnChangeVaTabs(index)
{		
	switch (index) {
		case 1:			//size
			EventSetup.minMdObjX = -1;
			EventSetup.minMdObjY = -1;
			EventSetup.maxMdObjX = -1;
			EventSetup.maxMdObjY = -1;
			
			EventSetup.VA.view("max_min");
			OnChangeObjectSize();
			break;
		case 2:			//area
			EventSetup.VA.view("MDPolyDraw");	
			OnClickDetectionMode();
			break;		
		case 3:			//rule
			OnChangeAnalyticsType();
			break;
		default:
			EventSetup.VA.view(""); 	
			break;
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

function OnClickDetectionMode()
{	
	EventSetup.MD.updatePolygon();
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
			<?php if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3) { ?>
				if($("#event_<?php echo $event_name; ?>_appearing_rules_definedarea").is(":checked")){
					EventSetup.VA.view("rectangleDraw");
					EventSetup.VA.reDrawRectangle();
				}else{
					EventSetup.VA.view("fullScreen");
					$("#poly-dialog-entireArea").dialog("open");
				}
			<?php }else{ ?>
				EventSetup.VA.view("rectangleDraw");
				EventSetup.VA.reDrawRectangle();
			<?php } ?>
	}

	<?php if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3) { ?>
		if(parseInt($('#event_<?php echo $event_name; ?>_analytics_type').val()) == 2){
			$('.event_<?php echo $event_name; ?>_appearing_rules').show();
		}else{
			$('.event_<?php echo $event_name; ?>_appearing_rules').hide();
		}
	<?php } ?>
}

function OnClickDetectionModeImage(mode)
{
	if(mode == 'on'){
		$("#event_<?php echo $event_name; ?>_detection_mode_on").prop("checked", true);
	}
	else{
		$("#event_<?php echo $event_name; ?>_detection_mode_none").prop("checked", true);
	}
	OnClickDetectionMode();
}

</script>
<div style="position:relative">
<div id="DisableIVSelectLayer" style="position:absolute; width:680px; height:215px; left: 0px; top: 0px; background-color:#000000; display:none; z-index:1000; filter:alpha(opacity=0.3); opacity:0.3; -moz-opacity:0.3; -ms-filter: 'progid:DXImageTransform.Microsoft.Alpha(Opacity=30)';"></div>
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
				<?php 
					if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3) { 
				?>
						<option value="2" <?php if ($vaConf->dataInfo['Mode']['value']==2) echo "selected=\"selected\""; ?>><?php echo $t_md_va[$GLOBALS['LANGINDEX']]; ?></option>
				<?php
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
<div id="md_tabs" style="display:none; margin-top:20px; margin-bottom:10px; margin-left:9px">
	<ul>
		<li><a href="#md_tabs-1"><?php echo $t_sensitivity[$GLOBALS['LANGINDEX']]; ?></a></li>
		<li><a href="#md_tabs-2"><?php echo $t_size[$GLOBALS['LANGINDEX']]; ?></a></li>
		<li><a href="#md_tabs-3"><?php echo $t_area[$GLOBALS['LANGINDEX']]; ?></a></li>		
		<?php if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3 && $GLOBALS['M_SUPPORT_EVENT_VA'] & IV_SUPPORT) { ?>
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
				<?php if($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ){?>
				<tr>
					<th class="top_txt"><?php echo $t_area[$GLOBALS['LANGINDEX']]; ?></th>
					<td>
						<label><input type="radio" name="event_<?php echo $event_name; ?>>_detection_mode" id="event_<?php echo $event_name; ?>>_detection_mode_on" class="event_detection_mode_on" checked="checked" style="margin-left:<?php if (GetBrowserName()=='IE') {echo '-4';} else { echo '-1'; } ?>px"/><?php echo $t_detectionArea[$GLOBALS['LANGINDEX']]; ?></label>
					</td>
				</tr>
				<?php }else{?>
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
				<?php } ?>
			</tbody>
		</table>
	</div>
	<?php if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3 && $GLOBALS['M_SUPPORT_EVENT_VA'] & IV_SUPPORT) { ?>
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
<?php if($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ){?>
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
<?php } ?>
<?php if($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_HISILICON || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN2_PTZ || $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ){ ?>
<br/>
<?php }else{ ?>
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
