function MakeManualSize(mode)
{
	var msg  = '';
	msg += "<ManualSize>";
	msg += "<MinWidth>" + $("#"+mode+"_min_width").val() + "</MinWidth>";
	msg += "<MinHeight>" + $("#"+mode+"_min_height").val() + "</MinHeight>";
	msg += "<MaxWidth>" + $("#"+mode+"_max_width").val() + "</MaxWidth>";
	msg += "<MaxHeight>" + $("#"+mode+"_max_height").val() + "</MaxHeight>";
	msg += "</ManualSize>";
	return msg;
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
	if ($('#event_'+event_name+'_'+currentVaMode+'_object_size_min').is(':checked')) {			//min obj
		$("#"+currentVaMode+"_min_width").spinner({ disabled: false }); 
		$("#"+currentVaMode+"_min_height").spinner({ disabled: false }); 
		$("#"+currentVaMode+"_max_width").spinner({ disabled: true }); 
		$("#"+currentVaMode+"_max_height").spinner({ disabled: true });
		
		$("#minRect").css("opacity","0.4");
		$("#maxRect").css("opacity","0.2");
		$("#minMaxTemp").css("border","1px solid blue");
	}
	else if ($('#event_'+event_name+'_'+currentVaMode+'_object_size_max').is(':checked')) {		//max obj
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

function OnClickDetectionModeImage(mode)
{
	if(mode == 'on'){
		$("#event_"+event_name+"_detection_mode_on").prop("checked", true);
	}
	else{
		$("#event_"+event_name+"_detection_mode_none").prop("checked", true);
	}
	OnClickDetectionMode();
}

function GetFilpMirrorStatus()
{	
	var flip_mirror = 0;
	if		(FLIP == 1 && MIRROR == 0) 	flip_mirror=1;
	else if	(FLIP == 0 && MIRROR == 1) 	flip_mirror=2;
	else if	(FLIP == 1 && MIRROR == 1) 	flip_mirror=3;
	else								flip_mirror=0;
	return flip_mirror;
}