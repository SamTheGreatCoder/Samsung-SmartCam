function CheckImagePresetSchedule() {
	for(var index=0; index<5; index++) {
		var selMode = parseInt($("#imagepreset_mode_"+index).val());
	
		if(selMode != 0) { 
			var startHour = $("#from_hour_"+index).val();
			var startMin = $("#from_min_"+index).val();
			var toHour = $("#to_hour_"+index).val();
			var toMin = $("#to_min_"+index).val();
				
			var baseStartTime = new Date(2000, 1, 1, startHour, startMin, 0).valueOf();
			var baseEndTime = new Date(2000, 1, 1, toHour, toMin, 59).valueOf();

			if (baseStartTime > baseEndTime) {
				alert(alertList[0]);
				return false;
			}			

			for (var index2=0; index2 < 5; ++index2) {
				var nextSelMode = parseInt($("#imagepreset_mode_"+index2).val());
				if(index2 != index && nextSelMode != 0) {
					var tempStartHour 	= $("#from_hour_"+index2).val();
					var tempStartMin	= $("#from_min_"+index2).val();
					var tempEndHour	= $("#to_hour_"+index2).val();
					var tempEndMin		= $("#to_min_"+index2).val();
				
					var compareStartTime = new Date(2000,1,1,tempStartHour, tempStartMin, 0).valueOf();
					var compareEndTime = new Date(2000,1,1,tempEndHour, tempEndMin, 59).valueOf();

					if ((baseStartTime <= compareStartTime && compareStartTime <= baseEndTime) || (baseStartTime <= compareEndTime && compareEndTime <= baseEndTime)) {
						alert(alertList[1]);
						return false;
					}

					if ((compareStartTime <= baseStartTime && baseStartTime <= compareEndTime) || (compareStartTime <= baseEndTime && baseEndTime <= compareEndTime)) {
						alert(alertList[1]);
						return false;
					}
				}
			}
		}
	}
}

$(document).ready(function($){

	$("#imagepreset_timebar").children(" div").on("mouseover", function(e) {
		var msg="";
		var startTime = $(this).children(".startTime").html().split(",");
		var endTime = $(this).children(".endTime").html().split(",");

		if(startTime[0] < 10){
			startTime[0] = '0'+startTime[0];
		}
		if(startTime[1] < 10){
			startTime[1] = '0'+startTime[1];
		}
		if(endTime[0] < 10){
			endTime[0] = '0'+endTime[0];
		}
		if(endTime[1] < 10){
			endTime[1] = '0'+endTime[1];
		}

		if($(this).hasClass("setDefineFocus")){
			msg += tooltipInfo["Mode"]+" : "+modeLanguageList[1]+"<br>";
			msg += tooltipInfo["Time"]+" : "+startTime[0]+":"+startTime[1]+":00 ~ " +endTime[0]+":"+endTime[1]+":59<br>";
		}else if($(this).hasClass("setMotionFocus")){
			msg += tooltipInfo["Mode"]+" : "+modeLanguageList[2]+"<br>";
			msg += tooltipInfo["Time"]+" : "+startTime[0]+":"+startTime[1]+":00 ~ " +endTime[0]+":"+endTime[1]+":59<br>";
		}else if($(this).hasClass("setReduceNoise")){
			msg += tooltipInfo["Mode"]+" : "+modeLanguageList[3]+"<br>";
			msg += tooltipInfo["Time"]+" : "+startTime[0]+":"+startTime[1]+":00 ~ " +endTime[0]+":"+endTime[1]+":59<br>";
		}else if($(this).hasClass("setBrightVideo")){
			msg += tooltipInfo["Mode"]+" : "+modeLanguageList[4]+"<br>";
			msg += tooltipInfo["Time"]+" : "+startTime[0]+":"+startTime[1]+":00 ~ " +endTime[0]+":"+endTime[1]+":59<br>";
		}else if($(this).hasClass("setMotionFocus_ReduceNoise")){
			msg += tooltipInfo["Mode"]+" : "+modeLanguageList[5]+"<br>";
			msg += tooltipInfo["Time"]+" : "+startTime[0]+":"+startTime[1]+":00 ~ " +endTime[0]+":"+endTime[1]+":59<br>";
		}else if($(this).hasClass("setMotionFocus_BrightVideo")){
			msg += tooltipInfo["Mode"]+" : "+modeLanguageList[6]+"<br>";
			msg += tooltipInfo["Time"]+" : "+startTime[0]+":"+startTime[1]+":00 ~ " +endTime[0]+":"+endTime[1]+":59<br>";
		}else if($(this).hasClass("setUserPreset")){
			msg += tooltipInfo["Mode"]+" : "+modeLanguageList[7]+"<br>";
			msg += tooltipInfo["Time"]+" : "+startTime[0]+":"+startTime[1]+":00 ~ " +endTime[0]+":"+endTime[1]+":59<br>";
		}

		$(this).attr("title", msg);
	});
	
	$("#presetScheduleSet").dialog({
		autoOpen: false,
		modal: true,
		draggable: false,
		dialogClass: 'scheduleSetTable',
		buttons: [{
			text: buttonLang[0],		//Apply
			click: function() { 
				if(CheckImagePresetSchedule() == false) return;
				var strMode="";
				
				for(var index=0; index<5; index++) {
					var selMode = parseInt($("#imagepreset_mode_"+index+" option:selected").val());					
					mode[index] = selMode;
					fromHour[index] = parseInt($("#from_hour_"+index).val());
					fromMin[index]  = parseInt($("#from_min_"+index).val());
					toHour[index]  = parseInt($("#to_hour_"+index).val());
					toMin[index] = parseInt($("#to_min_"+index).val());
				}
				updatePresetScheduleTimeBar();

				$(this).dialog( "close" );
				}
			}, 
			{
				text: buttonLang[1],		// Cancel
				click: function() {
					$(this).dialog( "close" );
				}
			}]
	});

	
	//////////////////////////////////////		

	for(var index=0; index<6; index++) {
		for(var i=0;i<60;i++){
			var val = i;
			if (i < 10) val = '0'+i;
			$("#from_min_"+index).append("<option value=\""+i+"\">"+val+":00"+"</option>");
		}
		for(var i=0;i<24;i++){
			var val = i;
			if (i < 10) val = '0'+i;
			$("#from_hour_"+index).append("<option value=\""+i+"\">"+val+"</option>");
		}
		
		for(var i=0;i<60;i++){
			var val = i;
			if (i < 10) val = '0'+i;
			$("#to_min_"+index).append("<option value=\""+i+"\">"+val+":59"+"</option>");
		}
		for(var i=0;i<24;i++){
			var val = i;
			if (i < 10) val = '0'+i;
			$("#to_hour_"+index).append("<option value=\""+i+"\">"+val+"</option>");
		}
		
	//////////////////////////////////////		
		//$('#from_min_'+index).val(0);
		//$('#to_min_'+index).val(59);	
	}
});
