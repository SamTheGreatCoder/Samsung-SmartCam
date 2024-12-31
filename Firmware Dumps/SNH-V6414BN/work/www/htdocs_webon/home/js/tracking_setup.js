//js

var G_vmlCanvasManager; // so non-IE won't freak out in canvasInit
var areaCount=0;

var c=null;
var c2=null;
var canvas=null;
var context=null;

var	isDrawDragging= false;
var	firstDrawClick= false;


$(function() {
	
});

trackingSetup={};
trackingSetup={
	
	getAreaXML:'',
	
	MAX_RESOLUTION_W: 1920,
	MAX_RESOLUTION_H: 1080,
	VIEWER_W: 640,
	VIEWER_H: 360,
	RATIO_W: this.MAX_RESOLUTION_W / this.VIEWER_W,
	RATIO_H: this.MAX_RESOLUTION_H / this.VIEWER_H,

	xmlToString:function(xmlData) 
	{
	    var xmlString;
	    //IE
	    if (window.ActiveXObject){
	        xmlString = xmlData.xml;
	    }
	    // code for Mozilla, Firefox, Opera, etc.
	    else{
	        xmlString = (new XMLSerializer()).serializeToString(xmlData[0]);
	    }
	    return xmlString;
	}
};
trackingSetup.drawings={

	rectangle:function(width,height,maxWidth,maxheight){
		trackingSetup.VIEWER_W = width;
		trackingSetup.VIEWER_H = height;
		trackingSetup.MAX_RESOLUTION_W = maxWidth;
		trackingSetup.MAX_RESOLUTION_H = maxheight;
		trackingSetup.RATIO_W = trackingSetup.MAX_RESOLUTION_W / trackingSetup.VIEWER_W;
		trackingSetup.RATIO_H = trackingSetup.MAX_RESOLUTION_H / trackingSetup.VIEWER_H;
		
		c=document.getElementById("myCanvas");;
		if (G_vmlCanvasManager != undefined) { // ie IE
			G_vmlCanvasManager.initElement(c);
		}
		
		c2=c.getContext("2d");
		c2.lineWidth = 2;
		c2.strokeStyle = "green";
		c2.globalAlpha="1"; 

		canvas=document.getElementById("imgTemp");
		if (G_vmlCanvasManager != undefined) { // ie IE
			G_vmlCanvasManager.initElement(canvas);
		}
		
		context=canvas.getContext("2d");
		context.lineWidth = 2;
		context.strokeStyle = "yellow";

		$("#AreaNames").bind("click",function(e) {
			trackingSetup.drawings.selectPolygon($(".selArea").attr("id"));
		});
		$("#DeleteArea").click(function(e) {
			if($("#AreaNames li a").hasClass("selArea")) {
			var deleteIndex=$(".selArea").attr("id");
			
			
			trackingSetup.drawings.deleteArea(deleteIndex);
			}
		});		
					
		var Fx, Fy;
		var Ax=0, Ay=0, Bx=0, By=0, index=1;
		var once=false;
		var arrayCount=0;
		var x1=0,y1=0,x2=0,y2=0,x3=0,y3=0,x4=0,y4=0;
		var a1=0,b1=0,a2=0,b2=0,a3=0,b3=0,a4=0,b4=0;
		pCount=0;

		var trackingRect = {};
		$("#imgTemp").mousedown(function(e) {
			if($("#DisableVideoSetup").is(":visible")){
				return;
			}
			
			if($("#AreaNames").children().length > 7) {			//Area count 8
				return;
			}
			if(e.which == 3){			//right click
				return;
			}
			$("ul#AreaNames li a").removeClass("selArea");
			
			var offset = $(this).offset();
			var xVal=e.pageX - offset.left;
			var yVal=e.pageY - offset.top;
			
			if (window.navigator.msPointerEnabled) {		//Detect IE10 or IE11
				if($(window).scrollLeft() != 0 && e.pageX == e.clientX){
					xVal= xVal + $(window).scrollLeft();
				}
				if($(window).scrollTop() != 0 && e.pageY == e.clientY){
					yVal= yVal + $(window).scrollTop();
				}
			}
			
			trackingRect.startX = xVal;
			trackingRect.startY = yVal;
			firstDrawClick = true;
			isDrawDragging = false;

		});
		
		$("#imgTemp").mousemove(function(e) {
			//console.log("mousemove : " + isDragging);
			var offset = $(this).offset();
			var xVal=e.pageX - offset.left;
			var yVal=e.pageY - offset.top;
			
			if (window.navigator.msPointerEnabled) {		//Detect IE10 or IE11
				if($(window).scrollLeft() != 0 && e.pageX == e.clientX){
					xVal= xVal + $(window).scrollLeft();
				}
				if($(window).scrollTop() != 0 && e.pageY == e.clientY){
					yVal= yVal + $(window).scrollTop();
				}
			}
			
			if(firstDrawClick){	
				trackingRect.w = xVal - trackingRect.startX;
			    trackingRect.h = yVal - trackingRect.startY;
				trackingRect.endX = xVal;
				trackingRect.endY = yVal;
				
				c2.clearRect(0,0,canvas.width,canvas.height);				
				c2.fillStyle = "gray";
				c2.globalAlpha="0.5"; 
				c2.fillRect(trackingRect.startX,trackingRect.startY,trackingRect.w,trackingRect.h);
				
				c2.strokeStyle = "green";
				c2.lineWidth = 2;
				c2.globalAlpha="1";
				c2.strokeRect(trackingRect.startX,trackingRect.startY,trackingRect.w,trackingRect.h);
			}
			isDrawDragging = true;
			
		});
 
		$("#imgTemp").mouseup(function(e) {
			if(!firstDrawClick) {
				return;
			}	
			
			firstDrawClick = false;
			if(isDrawDragging){
				if(trackingRect.startX <= trackingRect.endX){
					x1 = trackingRect.startX;
					x2 = trackingRect.endX;
				}
				else{
					x2 = trackingRect.startX;
					x1 = trackingRect.endX;
				}
				if(trackingRect.startY <= trackingRect.endY){
					y1 = trackingRect.startY;
					y2 = trackingRect.endY;
				}
				else{
					y2 = trackingRect.startY;
					y1 = trackingRect.endY;
				}

				x1=Math.ceil(x1*(trackingSetup.RATIO_W));
				x2=Math.ceil(x2*(trackingSetup.RATIO_W));
				y1=Math.ceil(y1*(trackingSetup.RATIO_H));
				y2=Math.ceil(y2*(trackingSetup.RATIO_H));

				if(x1 < 0){
					x1 = 0;
				}
				if(y1 < 0){
					y1 = 0;
				}
				if(x2 > trackingSetup.MAX_RESOLUTION_W){
					x2 = trackingSetup.MAX_RESOLUTION_W-1;
				}
				if(y2 > trackingSetup.MAX_RESOLUTION_H){
					y2 = trackingSetup.MAX_RESOLUTION_H-1;
				}
				if(x1 != x2 && y1 != y2){				
					var polyXml="<StartTrackingMaskArea><Name>Test</Name><NumPoint>2</NumPoint><Point><X>"+x1+"</X><Y>"+y1+"</Y></Point><Point><X>"+x2+"</X><Y>"+y2+"</Y></Point></StartTrackingMaskArea>";
					ApplyMaskPolygon(polyXml,true);
				}else{
					trackingSetup.drawings.cleanViewer();
				}
				

				isDrawDragging = false;
			}
		});
			//var titleText="Add : ["+areaCount+"]";
		$('#imgTemp').bind('contextmenu', function(e){		//right click
			var offset = $(this).offset();
			var xVal=e.pageX - offset.left;
			var yVal=e.pageY - offset.top;
			
			if (window.navigator.msPointerEnabled) {		//Detect IE10 or IE11
				if($(window).scrollLeft() != 0 && e.pageX == e.clientX){
					xVal= xVal + $(window).scrollLeft();
				}
				if($(window).scrollTop() != 0 && e.pageY == e.clientY){
					yVal= yVal + $(window).scrollTop();
				}
			}
		
			xVal=Math.ceil(xVal*(trackingSetup.RATIO_W));
			yVal=Math.ceil(yVal*(trackingSetup.RATIO_H));
			OnClickTargetLockOn(xVal,yVal);
		
		    return false;
		}); 	
		$("#polyName").attr('maxLength',10);
	},
	drawPolygonLine:function(Ax, Ay, Bx, By,index)
	{
		//console.log(Ax, Ay, Bx, By,index);
		bla = "";
		var lineLength = Math.sqrt( (Ax-Bx)*(Ax-Bx)+(Ay-By)*(Ay-By) );
		for( var i=0; i<lineLength; i++ )
		{
			bla += "<div class='currentPoly polygon"+index+"' style='left:"+ Math.round( Ax+(Bx-Ax)*i/lineLength  ) +"px;top:"+ Math.round( Ay+(By-Ay)*i/lineLength  ) +"px;'></div>";
		}
		document.getElementById("polyDraw").innerHTML += bla;
		
		
	},
	getArea:function(){
		var xml_data=$.parseXML(trackingSetup.getAreaXML);
		$("#AreaNames").empty();
		var i=0;
		var loopCount=$(xml_data).find("Name").length;
		var t=0;
		areaCount=0;
		for(i=0;i<loopCount;i++)
		{
			var parentFound=$(xml_data).find("TrackingMaskArea"+i);
			var liText="<li><a href='javascript:void(0);' id='"+$(parentFound).find("Index").text()+"'>"+t+"&nbsp;: &nbsp;"+$(parentFound).find("Name").text()+"["+$(parentFound).find("Index").text()+"]</a></li>";
			if($(parentFound).find("NumPoint").text()!=0){
				$("#AreaNames").append(liText);
				t++;
				areaCount++;
			}
			
		};
		
		$("ul#AreaNames li a").click(function(e) {
			$("ul#AreaNames li a").removeClass("selArea");
			$(this).addClass("selArea");
		});
		
		
	},
	setAreaPoly:function(x1,y1,x2,y2,x3,y3,x4,y4){
		x1=Math.ceil(x1/(trackingSetup.RATIO_W));
		x2=Math.ceil(x2/(trackingSetup.RATIO_W));
		y1=Math.ceil(y1/(trackingSetup.RATIO_H));
		y2=Math.ceil(y2/(trackingSetup.RATIO_H));

		c2.clearRect(0,0,canvas.width,canvas.height);
		c2.fillStyle = "gray";
		c2.globalAlpha="0.5"; 
		c2.fillRect(x1,y1,x2-x1,y2-y1);
		
		c2.strokeStyle = "green";
		c2.lineWidth = 2;
		c2.globalAlpha="1";
		c2.strokeRect(x1,y1,x2-x1,y2-y1);

		$("#poly-dialog").dialog({
				position:{
						my: "left+10 bottom",
						at: "left+10 bottom",
						of: "#VideoSetup"
				},			
				autoOpen: false,
				draggable: false,
				modal: true,
				title: title + " : ["+areaCount+"]",
				beforeClose: function( event, ui ) { c2.clearRect(0, 0, c.width, c.height);},
				close: function(){
					c2.clearRect(0, 0, c.width, c.height);
					$( this ).dialog( "close" );
					$(".DisableAreaList").css("display","none");
				},
				open: function(event, ui){
					$(".ui-widget-overlay").position({
						my: "top",
						at: "top",
						of: "#plugin_control_area"
					});
				},
				buttons: [{
					text: buttonLang[0],	//Ok
					click: function() {   
					//alert($("#polyName").val());
					var imgWidth=$("#imgTemp").width();
					var imgHeight=$("#imgTemp").height();

					var name = $("#polyName").val();	   	   
					var regexp = /^[-.\a-zA-Z0-9]+$/;
					if (name && name.search(regexp) == -1)
					{ 
						alert(nameCheck);
						return false;
					}

					x1=Math.ceil(x1*(trackingSetup.RATIO_W));
					x2=Math.ceil(x2*(trackingSetup.RATIO_W));
					y1=Math.ceil(y1*(trackingSetup.RATIO_H));
					y2=Math.ceil(y2*(trackingSetup.RATIO_H));
					
					if(x1 < 0){
						x1 = 0;
					}
					if(y1 < 0){
						y1 = 0;
					}
					if(x2 > trackingSetup.MAX_RESOLUTION_W){
						x2 = trackingSetup.MAX_RESOLUTION_W-1;
					}
					if(y2 > trackingSetup.MAX_RESOLUTION_H){
						y2 = trackingSetup.MAX_RESOLUTION_H-1;
					}

					var polyXml="<SetTrackingMaskArea><Name>"+$("#polyName").val()+"</Name><NumPoint>2</NumPoint><Point><X>"+x1+"</X><Y>"+y1+"</Y></Point><Point><X>"+x2+"</X><Y>"+y2+"</Y></Point></SetTrackingMaskArea>";
					//console.log(polyXml);
		
					ApplyMaskPolygon(polyXml,false);
					
					//removing once it is drwan
					c2.clearRect(0, 0, c.width, c.height);

					$(this).dialog("close");
					$(".DisableAreaList").css("display","none");
						}
				}, {
				text: buttonLang[1],	//Cancel
				click: function() {
					c2.clearRect(0, 0, c.width, c.height);
					$(this).dialog("close");
					$(".DisableAreaList").css("display","none");
				}
			}]
		});

	},
	selectPolygon:function(deleteIndex){
		
	
		//console.log("deleteIndex",deleteIndex);
		/*
		var c=document.getElementById("myCanvas");;
		if (G_vmlCanvasManager != undefined) { // ie IE
			G_vmlCanvasManager.initElement(c);
		}
		var c2=c.getContext("2d");
		c2.lineWidth = 2;
		c2.strokeStyle = "#00ffff";
		c2.clearRect(0, 0, c.width, c.height);
		*/
		
		var xml_data=$.parseXML(trackingSetup.getAreaXML);
		var i=0;
		
		var rectXml="<MoveTrackingMaskArea><Index>"+deleteIndex+"</Index></MoveTrackingMaskArea>";
		ApplyMove(rectXml);		
		
		$(xml_data).find("Index").each(function(e) {
			
					if($(this).text()==deleteIndex)
					{
						var xmlSel=$(this).parents("TrackingMaskArea"+i);
						var x1=xmlSel.find("Point0 X").text(),x2=xmlSel.find("Point1 X").text(),x3=xmlSel.find("Point2 X").text(),x4=xmlSel.find("Point3 X").text();
						var y1=xmlSel.find("Point0 Y").text(),y2=xmlSel.find("Point1 Y").text(),y3=xmlSel.find("Point2 Y").text(),y4=xmlSel.find("Point3 Y").text();
						
						x1=Math.ceil(x1/(trackingSetup.RATIO_W));
						x2=Math.ceil(x2/(trackingSetup.RATIO_W));
						y1=Math.ceil(y1/(trackingSetup.RATIO_H));
						y2=Math.ceil(y2/(trackingSetup.RATIO_H));
						x3=Math.ceil(x3/(trackingSetup.RATIO_W));
						x4=Math.ceil(x4/(trackingSetup.RATIO_W));
						y3=Math.ceil(y3/(trackingSetup.RATIO_H));
						y4=Math.ceil(y4/(trackingSetup.RATIO_H));

						//console.log("select: " + x1,y1,x2,y2);
						
						var imgWidth=$("#imgTemp").width();;
						var imgHeight=$("#imgTemp").height();
						
						//console.log(x1,y1,x2,y2,x3,y3,x4,y4);
						/*
						c2.beginPath();	
						c2.moveTo(x1, y1);c2.lineTo(x2, y2);c2.stroke();
						c2.moveTo(x2, y2);c2.lineTo(x3, y3);c2.stroke();
						c2.moveTo(x3, y3);c2.lineTo(x4, y4);c2.stroke();
						c2.moveTo(x4, y4);c2.lineTo(x1, y1);c2.stroke();
						c2.closePath();
						*/
						x2 = x2 - x1;
						y2 = y2 - y1;
						//c2.strokeRect(x1,y1,x2,y2);
						
						return false;
					}
					i++;
		});
		
	},
	deleteArea:function(index){
		c2.clearRect(0,0,canvas.width,canvas.height);	
		
		var rectXml="<RemoveTrackingMaskArea><Index>"+index+"</Index></RemoveTrackingMaskArea>";
		areaCount--;
		ApplyDelete(rectXml);	
		
		
	},
	cleanViewer:function(){
		c2.clearRect(0, 0, c.width, c.height);
		$("#DisableVideoSetup").css("display","none");
		$(".DisableAreaList").css("display","none");
		$("#polyDraw").css("display","");
	}

		
	
};
