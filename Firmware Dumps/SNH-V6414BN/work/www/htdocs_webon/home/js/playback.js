var widthPerMin=0.555;
var distPerHrour=33.3;
var incLevel=false;
var eventDays=new Array();

// struct for timeline block
function TimelineBlock(starthour, startmin, startsec, endhour, endmin, endsec, rectype, dbindex, fileindex, doubleindex)
{
	this.startHour = starthour;
	this.startMin = startmin;
	this.startSec = startsec;
	this.endHour = endhour;
	this.endMin = endmin;
	this.endSec = endsec;
	this.nRecType = rectype;
	this.dbIndex = dbindex;
	this.fileIndex = fileindex;
	this.doubleIndex = doubleindex;
}

// timeline array
var timelineBlockArray = new Array();
var duplicateBlockArray = new Array();
var isDuplicateBlockStarts = false;
var isDuplicatePlay = false;
var timelineBlockCount = 0;
var duplicateBlockCount = 0;

playback={};
playback.timeline={
	init:function(){
					var x1, x2, y1, y2,px=0,py=0;
					var isDragging = false;

					// for IE 8
					//$(".scrollCover").mousemove(function(e) {
					//	$(".timeLineDiv").trigger(e);
					//});

					$(".timeLineSeek").mousedown(function(e) {
						
						var offset = $(this).offset();
						var xVal=(e.pageX - offset.left);
						var yVal=(e.pageY - offset.top);
						
						//console.log(xPts + " , " + yPts);
						isDragging = true;
						
						x1= xVal;
						y1 =yVal;
						$(".timeLineSeek").css("opacity","0.4");
						return false;
						
					});
					
					$(".timeLineDiv").mousemove(function(e) {
						//console.log("mousemove : " + isDragging);
						
						var offset = $(this).offset();
						var xVal=(e.pageX - offset.left);
						var yVal=(e.pageY - offset.top);
						
						if (isDragging) {
							
							//if(xVal>802) xVal=802;
							
							$(".timeLineSeek").css("left",xVal+"px");
							$(".timeLineSeek").css("opacity","0.4");
							stopInterval();
						}
					});

					$(document).mouseup(function(e) {
						if (isDragging) {
							isDragging = false;
						//console.log("raleased");
						//console.log("seek Left Val",$(".timeLineSeek").css("left"));
						$(".timeLineSeek").css("opacity","1");
							startInterval();
						}
					});
					$(".timeLineSeek").mouseup(function(e) {
						if (isDragging) {
							isDragging = false;

							$(".timeLineSeek").css("opacity","1");

							var SeekYear=searchYear-1900;
							var SeekMonth=searchMonth-1;

							var offset = $(".timeLineDiv").offset();
							var xVal=(e.pageX - offset.left);
							var yVal=(e.pageY - offset.top);
							$(".timeLineSeek").css("left",xVal+"px");
							
							var distHr=parseInt(xVal/distPerHrour);
							
							var distMin=parseInt((xVal/distPerHrour - parseInt(xVal/distPerHrour))*0.6*100);
							//console.log("x " + xVal + "  y " + yVal);
							//console.log("Hr-->",distHr,"min-->",distMin);

							// Seek starts...

							isDuplicatePlay = false;
							if (yVal > 25)
							{
								isDuplicatePlay = true;
							}
							//console.log("yVal " + yVal);

							var dup = false;

							var checkstartVal, checkendVal;
							var dbIndex, startHour, startMin, startSec;
							var timeVal = distHr * 60 * 60 + distMin * 60 + 0;
							//console.log("timeVal " + timeVal);
							for (var i = 0; i < duplicateBlockCount; i++)
							{
								checkstartVal = duplicateBlockArray[i].startHour * 60 * 60 + duplicateBlockArray[i].startMin * 60 + duplicateBlockArray[i].startSec;
								checkendVal = duplicateBlockArray[i].endHour * 60 * 60 + duplicateBlockArray[i].endMin * 60 + duplicateBlockArray[i].endSec;
								//console.log(checkstartVal + ":::" + checkendVal + " " + duplicateBlockArray[i].startHour + ":" + duplicateBlockArray[i].startMin + ":" + duplicateBlockArray[i].startSec + " " + duplicateBlockArray[i].endHour + ":" + duplicateBlockArray[i].endMin + ":" + duplicateBlockArray[i].endSec);
								if (timeVal >= checkstartVal && timeVal <= checkendVal && isDuplicatePlay)
								{
									//console.log("Try to play duplicatetime " + duplicateBlockArray[i].dbIndex);
									dbIndex = duplicateBlockArray[i].dbIndex; //-1;
									startHour = distHr;
									startMin = distMin;
									startSec = 0;
									dup = true;
									break;
								}
								else if (timeVal < checkstartVal && isDuplicatePlay)
								{
									//console.log("Try to play duplicatetime.. " + duplicateBlockArray[i].dbIndex);
									dbIndex = duplicateBlockArray[i].dbIndex; //-1;
									startHour = duplicateBlockArray[i].startHour;
									startMin = duplicateBlockArray[i].startMin;
									startSec = duplicateBlockArray[i].startSec;
									dup = true;
									break;
								}
							}
							//--
							if (!dup)
							{
								for (var i = 0; i < timelineBlockCount; i++)
								{
									checkstartVal = timelineBlockArray[i].startHour * 60 * 60 + timelineBlockArray[i].startMin * 60 + timelineBlockArray[i].startSec;
									checkendVal = timelineBlockArray[i].endHour * 60 * 60 + timelineBlockArray[i].endMin * 60 + timelineBlockArray[i].endSec;
									//console.log(checkstartVal + "::" + checkendVal + " " + timelineBlockArray[i].startHour + ":" + timelineBlockArray[i].startMin + ":" + timelineBlockArray[i].startSec + " " + timelineBlockArray[i].endHour + ":" + timelineBlockArray[i].endMin + ":" + timelineBlockArray[i].endSec);
									if (timeVal >= checkstartVal && timeVal <= checkendVal)
									{
										//console.log("Normal DBindex is " + timelineBlockArray[i].dbIndex);
										dbIndex = timelineBlockArray[i].dbIndex; //-1;
										startHour = distHr;
										startMin = distMin;
										startSec = 0;
										break;
									}
									else if (timeVal < checkstartVal) // normal timeline also detects dbindex automatically 2012.6.25
									{
										//console.log("Normal DBindex is " + timelineBlockArray[i].dbIndex);
										dbIndex = timelineBlockArray[i].dbIndex; //-1;
										startHour = timelineBlockArray[i].startHour;
										startMin = timelineBlockArray[i].startMin;
										startSec = timelineBlockArray[i].startSec;
										break;
									}
								}
							}
							// --

							if (timeVal > checkendVal)
							{
								startInterval();
								return;
							}

							
							Seek(parseInt(searchYear),parseInt(searchMonth),parseInt(searchDayVal),parseInt(startHour),parseInt(startMin),parseInt(startSec),parseInt(dbIndex));

						}
					});

					$(".timeLineSeek").mousemove(function(e) {
						if (isDragging) {
						
							var offset = $(".timeLineDiv").offset();
							var xVal=(e.pageX - offset.left);
							var yVal=(e.pageY - offset.top);
							
							//if(xVal>802) xVal=802;
							
							$(".timeLineSeek").css("left",xVal+"px");
							$(".timeLineSeek").css("opacity","0.4");
							stopInterval();
						}
					});
			//////////////////////////////////////////////////////		
				
				/*$(".timeLineDiv div").click(function(e) {
					console.log(e.target);
					
				});*/
				$(".timeLineDiv").click(function(e) {
					//console.log($(e.target).attr("class"));
					var SeekYear=searchYear-1900;
					var SeekMonth=searchMonth-1;
					
					if($(e.target).attr("class")=="timeLineDiv" || $(e.target).hasClass("tmRed")|| $(e.target).hasClass("tmBlue")){
						
						var offset = $(this).offset();
						var xVal=(e.pageX - offset.left);
						var yVal=(e.pageY - offset.top);
						$(".timeLineSeek").css("left",xVal+"px");
						
						var distHr=parseInt(xVal/distPerHrour);
						
						var distMin=parseInt((xVal/distPerHrour - parseInt(xVal/distPerHrour))*0.6*100);
						//console.log("x " + xVal + "  y " + yVal);
						//console.log("Hr-->",distHr,"min-->",distMin);

						// Seek starts...

						isDuplicatePlay = false;
						if (yVal > 25)
						{
							isDuplicatePlay = true;
						}
						//console.log("yVal " + yVal);

						var dup = false;

						var checkstartVal, checkendVal;
						var dbIndex, startHour, startMin, startSec;
						var timeVal = distHr * 60 * 60 + distMin * 60 + 0;
						//console.log("timeVal " + timeVal);
						for (var i = 0; i < duplicateBlockCount; i++)
						{
							checkstartVal = duplicateBlockArray[i].startHour * 60 * 60 + duplicateBlockArray[i].startMin * 60 + duplicateBlockArray[i].startSec;
							checkendVal = duplicateBlockArray[i].endHour * 60 * 60 + duplicateBlockArray[i].endMin * 60 + duplicateBlockArray[i].endSec;
							//console.log(checkstartVal + ":::" + checkendVal + " " + duplicateBlockArray[i].startHour + ":" + duplicateBlockArray[i].startMin + ":" + duplicateBlockArray[i].startSec + " " + duplicateBlockArray[i].endHour + ":" + duplicateBlockArray[i].endMin + ":" + duplicateBlockArray[i].endSec);
							if (timeVal >= checkstartVal && timeVal <= checkendVal && isDuplicatePlay)
							{
								//console.log("Try to play duplicatetime " + duplicateBlockArray[i].dbIndex);
								dbIndex = duplicateBlockArray[i].dbIndex; //-1;
								startHour = distHr;
								startMin = distMin;
								startSec = 0;
								dup = true;
								break;
							}
							else if (timeVal < checkstartVal && isDuplicatePlay)
							{
								//console.log("Try to play duplicatetime.. " + duplicateBlockArray[i].dbIndex);
								dbIndex = duplicateBlockArray[i].dbIndex; //-1;
								startHour = duplicateBlockArray[i].startHour;
								startMin = duplicateBlockArray[i].startMin;
								startSec = duplicateBlockArray[i].startSec;
								dup = true;
								break;
							}
						}
						//--
						if (!dup)
						{
							for (var i = 0; i < timelineBlockCount; i++)
							{
								checkstartVal = timelineBlockArray[i].startHour * 60 * 60 + timelineBlockArray[i].startMin * 60 + timelineBlockArray[i].startSec;
								checkendVal = timelineBlockArray[i].endHour * 60 * 60 + timelineBlockArray[i].endMin * 60 + timelineBlockArray[i].endSec;
								//console.log(checkstartVal + "::" + checkendVal + " " + timelineBlockArray[i].startHour + ":" + timelineBlockArray[i].startMin + ":" + timelineBlockArray[i].startSec + " " + timelineBlockArray[i].endHour + ":" + timelineBlockArray[i].endMin + ":" + timelineBlockArray[i].endSec);
								if (timeVal >= checkstartVal && timeVal <= checkendVal)
								{
									//console.log("Normal DBindex is " + timelineBlockArray[i].dbIndex);
									dbIndex = timelineBlockArray[i].dbIndex; //-1;
									startHour = distHr;
									startMin = distMin;
									startSec = 0;
									break;
								}
								else if (timeVal < checkstartVal) // normal timeline also detects dbindex automatically 2012.6.25
								{
									//console.log("Normal DBindex is " + timelineBlockArray[i].dbIndex);
									dbIndex = timelineBlockArray[i].dbIndex; //-1;
									startHour = timelineBlockArray[i].startHour;
									startMin = timelineBlockArray[i].startMin;
									startSec = timelineBlockArray[i].startSec;
									break;
								}
							}
						}
						// --

						if (timeVal > checkendVal)
						{
							return;
						}

						
						Seek(parseInt(searchYear),parseInt(searchMonth),parseInt(searchDayVal),parseInt(startHour),parseInt(startMin),parseInt(startSec),parseInt(dbIndex));
					}
						
				});
					
					//////////////////////////////////////////////////////
					var IncDecOnce=true;
		$(".timebarInc").click(function(e) {
			
			if(!IncDecOnce) return;
			
			IncDecOnce=false;
			
			$("#timelineBar ul").removeClass("timeLabel").addClass("timeLabel2");
			$(".scrollCover").addClass("timebartype2");
			$(".scrollCover").css("width", "1595");
			$("#timelineRightBlank").css("z-index", "500");
			//$("#timelineRightBlank").css("left", "1595");

			$(".timeLineDiv").css("width", "1595px");
			incLevel=true;
			widthPerMin=1.108;
			distPerHrour=66.5;
			playback.timeline.resetTimeLineData();
		});
		$(".timebarDec").click(function(e) {
			
			if(IncDecOnce) return;
			
			IncDecOnce=true;
			
			incLevel=false;
			$("#timelineBar ul").removeClass("timeLabel2").addClass("timeLabel");;
			$(".scrollCover").removeClass("timebartype2");
			$("#timelineBar ul").css("margin-left","0");
			$(".scrollCover").css("left","0");
			$(".scrollCover").css("width", "797");
			$("#timelineRightBlank").css("z-index", "0");
			//$("#timelineRightBlank").css("left", "797");

			$(".timeLineDiv").css("width", "797px");
			widthPerMin=0.555;
			distPerHrour=33.3;
			playback.timeline.resetTimeLineData();
		});
		
		$(".timebarRight").click(function(e) {
			if(!incLevel) return ;
			$("#timelineBar ul").css("margin-left","-802px");
			$(".scrollCover").css("left","-802px");
			$("#timelineRightBlank").css("left", "1595");
			$("#timelineRightBlank").css("z-index", "0");

			$(".timeLineDiv").css("width", "1595px");
		});
		$(".timebarLeft").click(function(e) {
			if(!incLevel) return ;
			$("#timelineBar ul").css("margin-left","0");
			$(".scrollCover").css("left","0");
			$("#timelineRightBlank").css("left", "797");
			$("#timelineRightBlank").css("z-index", "500");

			$(".timeLineDiv").css("width", "797px");
		});
	},
	
	setTimeLineData:function(tmStartHr,tmStartMin,tmStartSec,tmEndHr,tmEndMin,tmEndSec,nRecType,dbIndex, fileIndex, doubleIndex){

		var hrDiff=tmEndHr-tmStartHr;
		var MinDiff;
		if (tmEndMin >= tmStartMin && tmEndHr == tmStartHr)
		{
			MinDiff=tmEndMin-tmStartMin;
		}
		else
		{
			MinDiff=(tmEndMin+(60*hrDiff))-tmStartMin;
		}
		
		var defaultWidth = 0.6;
		if (incLevel)
		{
			defaultWidth = 1.108;
		}
		var timeWidth=MinDiff*widthPerMin+defaultWidth;
		if(timeWidth<2) timeWidth=2;
		
		var leftVal=(widthPerMin*((tmStartHr*60)+tmStartMin)) - (((tmStartHr*60)+tmStartMin)/1499 * 3);

		if (leftVal < 0) leftVal = 0;
		
		var content="";
		var botAtt="";
		if(doubleIndex==1) botAtt="bottomAttch";
		
		//console.log("nRecType-->",nRecType);
		if(nRecType==524288) // normal recording
		{
			content="<div alt='"+tmStartHr+","+tmStartMin+","+tmStartSec+","+tmEndHr+","+tmEndMin+","+tmEndSec+","+nRecType+","+dbIndex+","+ fileIndex+","+doubleIndex+"' class='tmBlue "+botAtt+"'' style='width:"+timeWidth+"px;left:"+leftVal+"px;'></div>";
		}
		else // event recording
		{
			content="<div alt='"+tmStartHr+","+tmStartMin+","+tmStartSec+","+tmEndHr+","+tmEndMin+","+tmEndSec+","+nRecType+","+dbIndex+","+ fileIndex+","+doubleIndex+"' class='tmRed "+botAtt+"' style='width:"+timeWidth+"px;left:"+leftVal+"px;'></div>";
		}
	
			$(".timeLineDiv").append(content);
			$(".timeLineSeek").css("left","0");
			
		
		
	},
	moveTime:function(hour,min,sec){
		
		var hrDist=hour*distPerHrour;
		var minDist=min*widthPerMin;
		
		
		$(".timeLineSeek").css("left",hrDist+minDist+"px");
		
	},
	resetTimeLineData:function(){
		$(".timeLineDiv div").each(function()
		{
			var paramVal=$(this).attr("alt").split(",");
			
			var tmStartHr=paramVal[0],tmStartMin=paramVal[1],tmStartSec=paramVal[2],tmEndHr=paramVal[3],tmEndMin=paramVal[4],tmEndSec=paramVal[5];
			var nRecType=paramVal[6],dbIndex=paramVal[7], fileIndex=paramVal[8], doubleIndex=paramVal[9];
			
			var hrDiff=parseInt(tmEndHr)-parseInt(tmStartHr);
			var MinDiff;
			if (parseInt(tmEndMin) >= parseInt(tmStartMin) && parseInt(tmEndHr) == parseInt(tmStartHr))
			{
				MinDiff=parseInt(tmEndMin)-parseInt(tmStartMin);
			}
			else
			{
				MinDiff=(parseInt(tmEndMin)+(60*hrDiff))-parseInt(tmStartMin);
			}
			
			var defaultWidth = 0.6;
			if (incLevel)
			{
				defaultWidth = 1.108;
			}
			var timeWidth=MinDiff*widthPerMin+defaultWidth;
			if(timeWidth<2) timeWidth=2;
			
			//console.log("hour -->",tmStartHr,"min --> ",tmStartMin);
			
			var leftVal=(widthPerMin*( (parseInt(tmStartHr)*60) + parseInt(tmStartMin) ) ) - ( ( (parseInt(tmStartHr)*60) + parseInt(tmStartMin))/1499 * 3);

			if(leftVal < 0)
				leftVal = 0;
			
			//console.log("left -->",leftVal,"width --> ",timeWidth);
			
			$(this).css("width",timeWidth+"px").css("left",leftVal+"px");
			
			//playback.timeline.setTimeLineData(paramVal[0],paramVal[1],paramVal[2],paramVal[3],paramVal[4],paramVal[5],paramVal[6],paramVal[7],paramVal[8],paramVal[9]);
		});
	},
	displaySearchDay:function(dateData){
		//var dateData=262144;
		var isRecordDay=new Array();
		eventDays=new Array();
		var firstAccessCalend=false;;
		for (var i = 31; i >= 0; --i)
		{
			isRecordDay[i] = (dateData >> i) & 0x01;
			if (i <= 30 /*Because MSB is always 0*/ && isRecordDay[i] == 0)
			{
				//console.log(isRecordDay[i],i);
			}
			else{
				eventDays.push(i+1);
			}
		};
		
		//console.log("Event days",eventDays);
		
		//$( "#datepicker" ).datepicker("destroy");
		$( "#datepicker" ).datepicker({
			showOtherMonths: true,
			onSelect: function( selectedDate ) {
				//console.log(selectedDate);
				var datArr=selectedDate.split("/");
				//console.log(datArr[2], datArr[0], datArr[1]);
				SearchDay(parseInt(datArr[2]), parseInt(datArr[0]), parseInt(datArr[1]));
			},
			onChangeMonthYear: function(year, month, inst) 
			{ 
				
				
				if(cameraYear!=parseInt(year) || cameraMonth!=parseInt(month))
				{
					cameraYear=parseInt(year); cameraMonth=parseInt(month);
					SearchCalendar(cameraYear, cameraMonth);
				}
				
			},
			beforeShowDay: function(eachDate) {
				
				//console.log(cameraYear, cameraMonth);
				//console.log(eachDate.getFullYear(), eachDate.getMonth()+1, eachDate.getDate());
				//console.log(eachDate.getDate(),eventDays);
				//jQuery.inArray(parseInt(eachDate.getDate()), eventDays)==-1) && (eachDate.getMonth()+1)==cameraMonth &&  eachDate.getFullYear()==cameraYear
				if (jQuery.inArray(parseInt(eachDate.getDate()), eventDays)>=0 && (eachDate.getMonth()+1)==cameraMonth &&  eachDate.getFullYear()==cameraYear) { 
					//console.log("event found",eachDate.getDate());
					return [true, 'eventDay', ''];
				}
				else  return [false, '', ''];
			}
		});
	}
}
