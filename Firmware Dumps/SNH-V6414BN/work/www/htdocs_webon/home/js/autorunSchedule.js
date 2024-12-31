
function SetAutoRunScheduleDataToTable(startIndex,XmlData)
{
	var tableID = "autorun_timeschedule_table";
	xmlDoc = $.parseXML( XmlData );
	var i = startIndex[0];
	var j = startIndex[1];
	var prevI = startIndex[0];
	var prevJ = startIndex[1];
	var currStartIndex = new Array();	
	var currEndIndex = new Array();
	
	while(1){
		$(xmlDoc).find("AutorunSchedule").find("Day"+i+" H"+j).each(function(e){
			var isHead = parseInt($(this).find("Enable").text());
			var mode = parseInt($(this).find("Mode").text());
			var tmpDetailVal = '';
			switch (mode) {
				case 1:
					break;
				case 2: // preset
					tmpDetailVal = $(this).find("PresetNo").text();
					break;
				case 3:
					tmpDetailVal = $(this).find("SwingMode").text();
					break;
				case 4:
					tmpDetailVal = $(this).find("GroupNo").text();
					break;
				case 5:
					break;
				case 6:
					tmpDetailVal = $(this).find("TraceNo").text();
					break;
				case 7:
					tmpDetailVal = $(this).find("AutoPanSpeed").text()+","+$(this).find("AutoPanTiltangle").text();
					break;
			}
			$("table#"+tableID+" tbody tr:eq("+i+") td:eq("+(j+1)+")").addClass('set'+modeNameList[mode]);
			if(isHead == 1){
				$("table#"+tableID+" tbody tr:eq("+i+") td:eq("+(j+1)+")").addClass("headTime");
				currStartIndex[0] = i;
				currStartIndex[1] = j;
			}
			$("table#"+tableID+" tbody tr:eq("+i+") td:eq("+(j+1)+")").append("<span class=\"detailValue\" style=\"display:none\">"+tmpDetailVal+"</span>");
			$("table#"+tableID+" tbody tr:eq("+i+") td:eq("+(j+1)+")").append("<span class=\"startTime\" style=\"display:none\">"+currStartIndex[0]+","+currStartIndex[1]+"</span>");
		});

		var isHead = parseInt($(xmlDoc).find("AutorunSchedule").find("Day"+prevI+" H"+prevJ).find("Enable").text());
		if(isHead == 1){
			currEndIndex[0] = prevI;
			currEndIndex[1] = prevJ-1;
			if(currEndIndex[1] == -1){
				currEndIndex[1] = 23;
				currEndIndex[0]--;
			}
			if(currEndIndex[0] == -1){
				currEndIndex[0] = 6;
			}			
		}
		
		prevJ--;
		if(prevJ == -1){
			prevJ = 23;
			prevI--;
		}
		if(prevI == -1){
			prevI = 6;
		}

		$("table#"+tableID+" tbody tr:eq("+prevI+") td:eq("+(prevJ+1)+")").append("<span class=\"endTime\" style=\"display:none\">"+currEndIndex[0]+","+currEndIndex[1]+"</span>");			
		
		j++;
		if(j == 24){
			j = 0;
			i++;
		}
		if(i == 7){
			i = 0;
		}
		
		if(i == startIndex[0] && j == startIndex[1]){
			break;
		}
	}
}

function GetAutoRunScheduleData()
{
	var ScheduleData = "";
	var rowData = "";
	
	for (var index=0; index<7; ++index) {
		var cellData = "";
		
		for (var index2=1; index2<=24; ++index2) {  
			var tdObj = $("table.eventTable tbody tr:eq("+index+")").children(":eq("+index2+")");
			var tdDetail = tdObj.children(".detailValue").html().split(",");
			if(tdDetail.length < 2){
				tdDetail = tdObj.children(".detailValue").html();
			}

			cellData += "<AutorunDetailSchedule>\r\n";
			if(tdObj.hasClass("headTime")){
				cellData += "<Enable>1</Enable>\r\n";
			}else{
				cellData += "<Enable>0</Enable>\r\n";
			}
			cellData += "<StartMin>0</StartMin>\r\n";
			cellData += "<AutorunDetail>\r\n";
			
			if(tdObj.hasClass("setHome")){
				cellData += "<Mode>1</Mode>\r\n";
			}else if(tdObj.hasClass("setPreset")){
				cellData += "<Mode>2</Mode>\r\n";
				cellData += "<PresetNumber>"+tdDetail+"</PresetNumber>\r\n";
			}else if(tdObj.hasClass("setSwing")){
				cellData += "<Mode>3</Mode>\r\n";
				cellData += "<SwingMode>"+tdDetail+"</SwingMode>\r\n";
			}else if(tdObj.hasClass("setGroup")){
				cellData += "<Mode>4</Mode>\r\n";
				cellData += "<GroupNumber>"+tdDetail+"</GroupNumber>\r\n";
			}else if(tdObj.hasClass("setTour")){
				cellData += "<Mode>5</Mode>\r\n";			
			}else if(tdObj.hasClass("setTrace")){
				cellData += "<Mode>6</Mode>\r\n";
				cellData += "<TraceNumber>"+tdDetail+"</TraceNumber>\r\n";
			}else if(tdObj.hasClass("setAutopan")){
				cellData += "<Mode>7</Mode>\r\n";
				cellData += "<AutoPanSpeed>"+tdDetail[0]+"</AutoPanSpeed>\r\n";
				cellData += "<AutoPanTiltangle>"+tdDetail[1]+"</AutoPanTiltangle>\r\n";			
			}

			cellData += "</AutorunDetail>\r\n";
			cellData += "</AutorunDetailSchedule>\r\n";
		}
		rowData+="<AutorunSchedule>"+cellData+"</AutorunSchedule>\r\n";
	}
	return rowData;		
}

function AutoRunScheduleClear()
{
	var tableID = "autorun_timeschedule_table";
	for(var i = 0; i < 7; i++)
	{
		for(var j = 1; j < 25; j++)
		{
			$("table#"+tableID+" tbody tr:eq("+i+")").children(":eq("+j+")").removeClass();
			$("table#"+tableID+" tbody tr:eq("+i+")").children(":eq("+j+")").addClass("setHome");
			if(i == 0 && j == 1){
				$("table#"+tableID+" tbody tr:eq("+i+")").children(":eq("+j+")").addClass("headTime");
			}
			$("table#"+tableID+" tbody tr:eq("+i+") td:eq("+j+")").html("");
			$("table#"+tableID+" tbody tr:eq("+i+") td:eq("+j+")").append("<span class=\"detailValue\" style=\"display:none\"></span>");			
			$("table#"+tableID+" tbody tr:eq("+i+") td:eq("+j+")").append("<span class=\"startTime\" style=\"display:none\">0,0</span>");
			$("table#"+tableID+" tbody tr:eq("+i+") td:eq("+j+")").append("<span class=\"endTime\" style=\"display:none\">6,23</span>");	
		}
	}
}

$(document).ready(function($){
	$("table.eventTable tbody tr td").on("mouseover", function(e) {
		if(!$(this).hasClass("dayHead")){
			var tdDetail = $(this).children(".detailValue").html().split(",");

			if(tdDetail.length < 2){
				tdDetail = $(this).children(".detailValue").html();
			}
			var startTime = $(this).children(".startTime").html().split(",");
			var endTime = $(this).children(".endTime").html().split(",");
			var msg="";

			if($(this).hasClass("setHome")){
				msg += tooltipInfo["Mode"]+" : "+modeLanguageList[1]+"<br>";
			}else if($(this).hasClass("setPreset")){
				msg += tooltipInfo["Mode"]+" : "+modeLanguageList[2]+"<br>";
				msg += tooltipInfo["PresetNumber"]+" : "+tdDetail+"<br>";			
			}else if($(this).hasClass("setSwing")){
				msg += tooltipInfo["Mode"]+" : "+modeLanguageList[3]+"<br>";
				var swingIndex = parseInt(tdDetail);
				msg += tooltipInfo["SwingMode"]+" : "+swingModeList[swingIndex].replace("&amp;","&")+"<br>";			
			}else if($(this).hasClass("setGroup")){
				msg += tooltipInfo["Mode"]+" : "+modeLanguageList[4]+"<br>";
				msg += tooltipInfo["GroupNumber"]+" : "+tdDetail+"<br>";
			}else if($(this).hasClass("setTour")){
				msg += tooltipInfo["Mode"]+" : "+modeLanguageList[5]+"<br>";
			}else if($(this).hasClass("setTrace")){
				msg += tooltipInfo["Mode"]+" : "+modeLanguageList[6]+"<br>";
				msg += tooltipInfo["TraceNumber"]+" : "+tdDetail+"<br>";			
			}else if($(this).hasClass("setAutopan")){
				msg += tooltipInfo["Mode"]+" : "+modeLanguageList[7]+"<br>";
				msg += tooltipInfo["AutoPanSpeed"]+" : "+tdDetail[0]+"<br>";
				msg += tooltipInfo["AutoPanTiltangle"]+" : "+tdDetail[1]+"<br>";			
			}
			var startDay = parseInt(startTime[0]);
			var endDay = parseInt(endTime[0]);
			if(startTime[1] < 10){
				startTime[1] = '0'+startTime[1];
			}
			if(endTime[1] < 10){
				endTime[1] = '0'+endTime[1];
			}
			msg += daysList[startDay]+" "+startTime[1]+":00 ~ "+daysList[endDay]+" "+endTime[1]+":59";
			$(this).attr("title", msg);
		}
	});

	$("table.eventTable tbody tr td").on("click",function(e){
		if($(this).parents("thead").length==1){
			return false;
		}
		if($(this).parent("tr").children().index($(this))==0){
			return false;
		}	
		
		var Othis=this;

		jQuery("#tmMinute").dialog({
			autoOpen: false,
			modal: true,
			draggable: false,
			dialogClass: 'scheduleTable',
			buttons: [{
				text: buttonLang[0],		//Apply
				click: function() { 
					var selMode = parseInt($("#ScheduleAutoRunMode").val());
					var fromTime = new Array();
					var toTime = new Array();
					
					fromTime['d'] = parseInt($("#from_days").val());
					fromTime['h'] = parseInt($("#from_hour").val())+1;

					toTime['d'] = parseInt($("#to_days").val());
					toTime['h'] = parseInt($("#to_hour").val())+1;

					var selClass = 'set'+modeNameList[selMode];

					if(modeNameList[selMode] == "Preset") {
						if (CheckValueRange($("#AutoRunPresetNumber").val(), 1, 255, presetNumberAlert)) return;
						if(!TypeCheck($('#AutoRunPresetNumber').val(), NUM+ALPHA)) {
							alert(presetNumberAlert);
							return;
						}
					}
					if(modeNameList[selMode] == "Group") {
						if (CheckValueRange($("#ScheduleAutoRunGroupNo").val(), 1, 6, groupNumberAlert)) return;
						if(!TypeCheck($('#ScheduleAutoRunGroupNo').val(), NUM+ALPHA)) {
							alert(groupNumberAlert);
							return;
						}
					}
					if(modeNameList[selMode] == "Trace") {
						if (CheckValueRange($("#ScheduleAutoRunTraceNumber").val(), 1, 4, traceNumberAlert)) return;
						if(!TypeCheck($('#ScheduleAutoRunTraceNumber').val(), NUM+ALPHA)) {
							alert(traceNumberAlert);
							return;
						}
					}
					if(modeNameList[selMode] == "Autopan") {
						if (CheckValueRange($("#ScheduleAutoPanSpeed").val(), 1, 50, autoPanSpeedAlert)) return;
						if(!TypeCheck($('#ScheduleAutoPanSpeed').val(), NUM+ALPHA)) {
							alert(autoPanSpeedAlert);
							return;
						}

						if (CheckValueRange($("#ScheduleAutoPanTiltangle").val(), 0, 85, autoPanTiltangleAlert)) return;
						if(!TypeCheck($('#ScheduleAutoPanTiltangle').val(), NUM+ALPHA)) {
							alert(autoPanTiltangleAlert);
							return;
						}
					}

					var i = fromTime['d'];
					var j = fromTime['h'];
					var prevI = i;
					var prevJ = j-1;

					if(prevJ == 0){
						prevJ = 24;
						prevI--;
					}
					if(prevI == -1){
						prevI = 6;
					}
					while(1){		//Set back endTime
						var currObj = $("table.eventTable tbody tr:eq("+prevI+")").children(":eq("+prevJ+")");
						
						if(currObj.children().length > 0){
							var tempI = fromTime['d'];
							var tempJ = fromTime['h']-2;
							
							if(tempJ == -1){
								tempJ = 23;
								tempI--;
							}
							if(tempI == -1){
								tempI = 6;
							}
							
							currObj.children(".endTime").html(tempI+","+tempJ)
						}
						if($("table.eventTable tbody tr:eq("+prevI+")").children(":eq("+prevJ+")").hasClass("headTime")){
							break;
						}

						prevJ--;
						if(prevJ == 0){
							prevJ = 24;
							prevI--;
						}
						if(prevI == -1){
							prevI = 6;
						}
					}

					while(1){
						var currObj = $("table.eventTable tbody tr:eq("+i+")").children(":eq("+j+")");
						var tmpDetailVal = '';
						
						switch (selMode) {
							case 1:
								break;
							case 2: // preset
								tmpDetailVal = $("#AutoRunPresetNumber").val();
								break;
							case 3:
								tmpDetailVal = $("#ScheduleAutoRunSwingMode").val();
								break;
							case 4:
								tmpDetailVal = $("#ScheduleAutoRunGroupNo").val();
								break;
							case 5:
								break;
							case 6:
								tmpDetailVal = $("#ScheduleAutoRunTraceNumber").val();
								break;
							case 7:
								tmpDetailVal = $("#ScheduleAutoPanSpeed").val()+","+$("#ScheduleAutoPanTiltangle").val();
								break;
						}
						currObj.removeClass();
						currObj.addClass(selClass);
						if(i == fromTime['d'] && j == fromTime['h']){
							currObj.addClass("headTime");
						}
						
						currObj.html("");
						currObj.append("<span class=\"detailValue\" style=\"display:none\">"+tmpDetailVal+"</span>")
						currObj.append("<span class=\"startTime\" style=\"display:none\">"+fromTime['d']+","+(fromTime['h']-1)+"</span>");
						currObj.append("<span class=\"endTime\" style=\"display:none\">"+toTime['d']+","+(toTime['h']-1)+"</span>");
						
						if((i == toTime['d'] && j == toTime['h'])){
							break;
						}
						
						j++;
						if(j == 25){
							j = 1;
							i++;
						}
						if(i == 7){
							i = 0;
						}
					}
					
					var nextI = i;
					var nextJ = j+1;
						
					if(nextJ == 25){
						nextJ = 1;
						nextI++;
					}
					if(nextI == 7){
						nextI = 0;
					}
					
					$("table.eventTable tbody tr:eq("+nextI+")").children(":eq("+nextJ+")").addClass("headTime");
					while(1){		////Set next startTime
						var currObj = $("table.eventTable tbody tr:eq("+nextI+")").children(":eq("+nextJ+")");
						if(currObj.children().length > 0){
							var tempI = toTime['d'];
							var tempJ = toTime['h'];
							
							if(tempJ == 24){
								tempJ = 0;
								tempI++;
							}
							if(tempI == 7){
								tempI = 0;
							}
							
							currObj.children(".startTime").html(tempI+","+tempJ)
						}
						nextJ++;
						if(nextJ == 25){
							nextJ= 1;
							nextI++;
						}
						if(nextI == 7){
							nextI = 0;
						}
						if($("table.eventTable tbody tr:eq("+nextI+")").children(":eq("+nextJ+")").hasClass("headTime")){
							break;
						}
					}
					//////////////////////////////////////////////////////////////////					
					
					$(this).dialog( "close" );
					}
				}, {
					text: buttonLang[1],		// Cancel
					click: function() {
						$(this).dialog( "close" );
					}
				}]
		});
		
		////////////////////////////////////////
		jQuery("#tmMinute").dialog("open");

		var target = $("table.eventTable");
				
		$("#tmMinute").dialog("widget").position({
			my: 'center',
			of: target
		});

		var tdDetail = $(Othis).children(".detailValue").html().split(",");
		if(tdDetail.length < 2){
			tdDetail = $(Othis).children(".detailValue").html();
		}
		if($(Othis).hasClass("setHome")){
			$("#ScheduleAutoRunMode").val(1);
		}else if($(Othis).hasClass("setPreset")){
			$("#ScheduleAutoRunMode").val(2);
			$("#AutoRunPresetNumber").val(tdDetail);
		}else if($(Othis).hasClass("setSwing")){
			$("#ScheduleAutoRunMode").val(3);
			$("#ScheduleAutoRunSwingMode").val(parseInt(tdDetail));
		}else if($(Othis).hasClass("setGroup")){
			$("#ScheduleAutoRunMode").val(4);
			$("#ScheduleAutoRunGroupNo").val(tdDetail);
		}else if($(Othis).hasClass("setTour")){
			$("#ScheduleAutoRunMode").val(5);
		}else if($(Othis).hasClass("setTrace")){
			$("#ScheduleAutoRunMode").val(6);
			$("#ScheduleAutoRunTraceNumber").val(tdDetail);
		}else if($(Othis).hasClass("setAutopan")){
			$("#ScheduleAutoRunMode").val(7);
			$("#ScheduleAutoPanSpeed").val(tdDetail[0]);
			$("#ScheduleAutoPanTiltangle").val(tdDetail[1]);
		}

		$("#ScheduleAutoRunMode").trigger("onchange");
		var dayIndex = $(Othis).parent("tr").index();
		var hourIndex = $(Othis).parent("tr").children().index($(Othis)) -1;

		$("#from_days").val(dayIndex).attr("disabled","disabled");
		$("#from_hour").val(hourIndex).attr("disabled","disabled");

		$("#to_days").val(dayIndex);
		$("#to_hour").val(hourIndex);

		/////////////////////////////////////////////////////////////////////
	});
	/////////////////////////////////////
	for(var i=0;i<24;i++){
		var val = i;
		if (i < 10) val = '0'+i;
		$("#from_hour").append("<option value=\""+i+"\">"+val+":00</option>");
	}
	for(var i=0;i<daysList.length;i++){
		$("#from_days").append("<option value=\""+i+"\">"+daysList[i]+"</option>");
	}
	
	for(var i=0;i<24;i++){
		var val = i;
		if (i < 10) val = '0'+i;
		$("#to_hour").append("<option value=\""+i+"\">"+val+":59</option>");
	}
	for(var i=0;i<daysList.length;i++){
		$("#to_days").append("<option value=\""+i+"\">"+daysList[i]+"</option>");
	}
	
//////////////////////////////////////		
	
});
