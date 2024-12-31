function SetScheduleDataToTable(XmlData,TableId)
{
	//console.log(XmlData)
	xmlDoc = $.parseXML( XmlData );
	var i=0;
		/*$(xmlDoc).find("Schedule").children().each(function() 
		{
					//alert($(this)[0].nodeName);
					var rowName=$(this)[0].nodeName;
					
					if(rowName=="Enabled"){ }
					else
					{
						var j=1;
						$(this).children().each(function(){
							//alert($(this)[0].nodeName);
							var CellName=$(this)[0].nodeName;
								if($(this).text()==1)
								{
									$("table#"+TableId+" tbody tr:eq("+i+") td:eq("+j+")").addClass("selTime");
									//alert("Row ID"+(i-1)+"-> Cell ID"+(j));
								}
							j++;
						});
						i++;
					}
				
				
		});
		*/
	for(var i=0;i<7;i++){
		for(var j=0;j<24;j++){
			if($(xmlDoc).find("Schedule").find("Day"+i+" H"+j).text()==1)
			{
					//console.log(i,j);
				$("table#"+TableId+" tbody tr:eq("+i+") td:eq("+(j+1)+")").addClass("selTime");
				if($(xmlDoc).find("Schedule").find("Day"+i+" IsEnabled"+j).text()==1){
					//console.log("having minutes",i,j);
					var frMin=$(xmlDoc).find("Schedule").find("Day"+i+" From"+j).text();
					var toMin=$(xmlDoc).find("Schedule").find("Day"+i+" To"+j).text();
					
					$("table#"+TableId+" tbody tr:eq("+i+") td:eq("+(j+1)+")").addClass("selHour");
					$("table#"+TableId+" tbody tr:eq("+i+") td:eq("+(j+1)+")").html("<span style='display:none'>"+frMin+","+toMin+"</span>");
				}
			}
		}	
	}
}

function GetScheduleData(tableId)
{
	//console.log("GetScheduleData called");
	var ScheduleData="";
	var currEventType = $(".event_select:checked").val();
	
	var rowData='';
	var rowCount=0;

	$("table#"+tableId+" tbody tr").each(function() {		
		var rowIndex=$(this).parents("tbody").index();
		var cellData="";
		$(this).children("td.selTime").each(function() { 
			var isEn=0,frMin=0,tomin=59;
			if($(this).children().length > 0){
				var minuteData=$(this).children("span").html().split(",");
				isEn=1,frMin=minuteData[0],tomin=minuteData[1];
			}
					
			var cellIndex=$(this).parent("tr").children().index($(this));
			var cInd=cellIndex-1;
			cellData+="<H"+cInd+">1</H"+cInd+"><IsEnabled"+cInd+">"+isEn+"</IsEnabled"+cInd+"><From"+cInd+">"+frMin+"</From"+cInd+"><To"+cInd+">"+tomin+"</To"+cInd+">";
		});
			rowData+="<Day"+rowCount+">"+cellData+"</Day"+rowCount+">";
			rowCount++;
	});
			//console.log(rowData)
		ScheduleData=rowData;
	return ScheduleData;		
};

function OnChangeMinutes(isStartMin){
	var fromMin = parseInt($("#fromMinutes").val(),10);
	var toMin = parseInt($("#toMinutes").val(),10);

	if(isStartMin){
		if(fromMin >= toMin){
			$("#toMinutes").val(fromMin);
		}
	}else{
		if(fromMin >= toMin){
			$("#fromMinutes").val(toMin);
		}
	}
}

jQuery(document).ready(function(){
	var isDragging = false;
	var firstTimeSel = false;
	var FirstCell="";
	var mouseMove=false;
	$(document).tooltip({
		open: function (event, ui) {
			setTimeout(function () {
				$(ui.tooltip).hide();
			}, 3000);
		}
	});
	
	$("table.eventTable tbody tr td").mousedown(function(e){	
		if($(this).parent("tr").children().index($(this))==0){
			return false;
		}
		FirstCell=this;
		isDragging=true;
		firstTimeSel = true;
	});
	
	$("table.eventTable tbody tr td").on("mouseover", function(e) {
		if($(this).hasClass("selHour")){
			var tdDetail = $(this).children("span").html().split(",");
			var day = $(this).parents("tr").children(":first").html();
			var hour = parseInt($(this).parent("tr").children().index($(this)),10) -1;
			if(hour < 10)
				hour = "0"+hour;
			if(parseInt(tdDetail[0],10) < 10)
				tdDetail[0] = "0"+tdDetail[0];
			if(parseInt(tdDetail[1],10) < 10)
				tdDetail[1] = "0"+tdDetail[1];

			var msg = "("+day+") " + hour + ":" + tdDetail[0] + " ~ " + hour + ":" + tdDetail[1];
			$(this).attr("title", msg);
		}else{
			$(this).removeAttr("title");
		}
	});
	
	$("table.eventTable tbody tr td").mouseenter(function(e){
		if(isDragging){
			mouseMove=true;
			//console.log("mouse enter");
			if($(this).hasClass("selTime")) {
				$(this).removeClass("selTime");
				if($(this).hasClass("selHour")){
						$(this).removeClass("selHour");
						$(this).html("");
				}
			}
			else{	$(this).addClass("selTime");} 			

			if(firstTimeSel){
			//	console.log("mouse enter first click move");
				if($(FirstCell).hasClass("selTime")) {
					$(FirstCell).removeClass("selTime");
					if($(FirstCell).hasClass("selHour")){
						$(FirstCell).removeClass("selHour");
						$(FirstCell).html("");
					}
				}
				else{	$(FirstCell).addClass("selTime");} 		
				
				firstTimeSel=false;
						
			}
		}
	});

	$(document).mouseup(function(e){	
		if(isDragging){
			//console.log("mouse up");
			isDragging=false;
		}
	});
	
	$("table.eventTable").on("mouseleave",function(e){	
		if(isDragging){
			//console.log("mouse leave");
			isDragging=false;
		}
	});

	$("table.eventTable tbody tr td").on("click",function(e){				
		if(mouseMove){
			mouseMove=false;
			//return;
		}					
				
		if($(this).parents("thead").length==1){
			return false;
		}
		
		if($(this).parent("tr").children().index($(this))==0){
			return false;
		}				
				
		var Othis=this;
		var titleText=$(Othis).parent("tr").children(":first").html();
		var dayText=$(this).parent("tr").children().index($(this));
			dayText=dayText-1; //first colunm for heading						
					
	jQuery("#tmMinute").dialog({
		autoOpen: false,
		modal: true,
		title:titleText,
		draggable: false,
		dialogClass: 'scheduleTable',
		buttons: [{
			text: buttonLang[0],	//Ok
			click: function() { 
				$(Othis).addClass("selTime");
			
				if($('#toMinutes').val()!=59 || $('#fromMinutes').val()!=0){
					$(Othis).addClass("selHour");
					$(Othis).html("<span style='display:none;'>"+$("#fromMinutes").val()+","+$("#toMinutes").val()+"</span>"); 
				}
				else {  $(Othis).removeClass("selHour"); $(Othis).html(""); }									
				$(this).dialog( "close" );
				}
			}, {
			text: buttonLang[1],	//Cancel
			click: function() {								
				$(this).dialog( "close");
				}
			}, {
			text: buttonLang[2],	//Delete
			click: function () {
				$(Othis).html("");
				$(Othis).removeClass("selTime");
				$(Othis).removeClass("selHour");
				$(this).dialog( "close");
				}
			}]
	});		
			////////////////////////////////////////
			//setTimeout($( "#tmMinute" ).dialog("open"),2000);
			//console.log("here");
			jQuery("#tmMinute").dialog("open");
			
			//////////////////////////////////////
			if($(Othis).children().length > 0){

				var minuteData=$(Othis).children("span").html().split(",");
				
				$('#toMinutes').val(minuteData[1]);
				$('#fromMinutes').val(minuteData[0]);
			}
			else{
				$('#toMinutes').val(59);
				$('#fromMinutes').val(0);
			}
			
			//////////////////////////////////////
			
			var target = $("table.eventTable");
			$("#tmMinute").dialog("widget").position({
				my: "center",
				of: target
			});
			if(dayText < 10) {
				$("#fromMinutesHr,#toMinutesHr").html("<option>"+"0"+dayText+"</option>").attr("disabled","disabled");
			} else {
				$("#fromMinutesHr,#toMinutesHr").html("<option>"+dayText+"</option>").attr("disabled","disabled");
			}
			/////////////////////////////////////////////////////////////////////
	});
/////////////////////////////////////
	for(var i=0;i<60;i++){
		var val = i;
		if(i<10) val = '0'+i;
		$("#toMinutes,#fromMinutes").append("<option value=\""+i+"\">"+val+"</option>");
	}
	$('#toMinutes').val(59);
	$('#fromMinutes').val(0);
//////////////////////////////////////		
});
