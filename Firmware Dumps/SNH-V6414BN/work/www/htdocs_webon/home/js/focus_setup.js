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

focusSetup={};
focusSetup={
	
	getAreaXML:'',
	
	OW:1920,
	OH:1080,
	viewerW:'',
	viewerH:'',

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
	},

init:function(maxWidth,maxHeight)
	{
		this.OW = maxWidth;
		this.OH = maxHeight;
	}
};

focusSetup.drawings={

	rectangle:function(width,height){
		c=document.getElementById("myCanvas");;
		if (G_vmlCanvasManager != undefined) { // ie IE
			G_vmlCanvasManager.initElement(c);
		}
		
		c2=c.getContext("2d");
		c2.fillStyle = "#00BFFF";
		c2.globalAlpha="0.5";
		
		canvas=document.getElementById("imgTemp");
		if (G_vmlCanvasManager != undefined) { // ie IE
			G_vmlCanvasManager.initElement(canvas);
		}
		
		context=canvas.getContext("2d");
		context.lineWidth = 2;
		context.strokeStyle = "#00008B";

		focusSetup.viewerW = width;
		focusSetup.viewerH = height;
		
					
		var Fx, Fy;
		var Ax=0, Ay=0, Bx=0, By=0, index=1;
		var once=false;
		var arrayCount=0;
		var x1=0,y1=0,x2=0,y2=0,x3=0,y3=0,x4=0,y4=0;
		var a1=0,b1=0,a2=0,b2=0,a3=0,b3=0,a4=0,b4=0;
		pCount=0;

		var focusSetupRect = {};
		$("#imgTemp").mousedown(function(e) {			
			if(areaCount > 0 || $("#roi_area_fd").is(":checked"))
			{
				// delete current area
				areaCount = 0;
				$(".SmartRectID").remove();
				//return;
			}
		
			var offset = $(this).offset();
			var xVal=e.pageX - offset.left;
			var yVal=e.pageY - offset.top;
			
			if (window.navigator.msPointerEnabled) {	//Detect IE10 or IE11
				if($(window).scrollLeft() != 0 && e.pageX == e.clientX){
					xVal= xVal + $(window).scrollLeft();
				}
				if($(window).scrollTop() != 0 && e.pageY == e.clientY){
					yVal= yVal + $(window).scrollTop();
				}
			}

			focusSetupRect.startX = xVal;
			focusSetupRect.startY = yVal;
				
			firstDrawClick = true;
			isDrawDragging = false;

		});
		
		$("#imgTemp").mousemove(function(e) {
			if(areaCount > 0 || $("#roi_area_fd").is(":checked"))
				return;
			
			var offset = $(this).offset();
			var xVal=e.pageX - offset.left;
			var yVal=e.pageY - offset.top;
			
			if (window.navigator.msPointerEnabled) {	//Detect IE10 or IE11
				if($(window).scrollLeft() != 0 && e.pageX == e.clientX){
					xVal= xVal + $(window).scrollLeft();
				}
				if($(window).scrollTop() != 0 && e.pageY == e.clientY){
					yVal= yVal + $(window).scrollTop();
				}
			}
			
			if(firstDrawClick){	
				focusSetupRect.w = xVal - focusSetupRect.startX;
			    focusSetupRect.h = yVal - focusSetupRect.startY;
				focusSetupRect.endX = xVal;
				focusSetupRect.endY = yVal;
				
				context.clearRect(0,0,canvas.width,canvas.height);
				context.lineWidth = 2;
				context.strokeStyle = "#00008B";
				context.globalAlpha="1";
				context.strokeRect(focusSetupRect.startX,focusSetupRect.startY,focusSetupRect.w,focusSetupRect.h);
				
				/*
				c2.strokeStyle = "DeepSkyBlue";
				c2.lineWidth = 3;
				c2.globalAlpha="1";
				c2.strokeRect(focusSetupRect.startX,focusSetupRect.startY,focusSetupRect.w,focusSetupRect.h);
				*/
			}
			isDrawDragging = true;
			
		});
 
		$("#imgTemp").mouseup(function(e) {
			if(areaCount > 0 || $("#roi_area_fd").is(":checked"))
				return;
			
			firstDrawClick = false;
			if(isDrawDragging){
				if(focusSetupRect.startX <= focusSetupRect.endX){
					x1 = focusSetupRect.startX;
					x2 = focusSetupRect.endX;
				}
				else{
					x2 = focusSetupRect.startX;
					x1 = focusSetupRect.endX;
				}
				if(focusSetupRect.startY <= focusSetupRect.endY){
					y1 = focusSetupRect.startY;
					y2 = focusSetupRect.endY+2;
				}
				else{
					y2 = focusSetupRect.startY;
					y1 = focusSetupRect.endY;
				}

				var isDuplicateArea = false;
				
				$(".SmartRectID").each(function(e) {
					var cordinates=$(this).html().split(",");

					var tempX1=parseInt(cordinates[0]);
					var tempY1=parseInt(cordinates[1]);
					var tempX2=parseInt(cordinates[2]);
					var tempY2=parseInt(cordinates[3]);

					if(x1 <= tempX2 && tempX1 <= x2 && y1 <= tempY2 && tempY1 <= y2){
						isDuplicateArea = true;
					}
									
				});
				
				if(!isDuplicateArea){
					if(!(typeof x1 == "undefined" || typeof y1 == "undefined" || typeof x2 == "undefined" || typeof y2 == "undefined")){
						$("#polyDraw").append("<div style='display:none;' class='SmartRectID'>"+x1+","+y1+","+x2+","+y2+"</div>");
						focusSetup.drawings.reDrawPolygon();
						areaCount++;				
					}
				}
				
				context.clearRect(0,0,canvas.width,canvas.height);

				isDrawDragging = false;
			}
		});
	},
	reDrawPolygon:function(){
		var canvasRect=document.getElementById("myCanvas");
		if (G_vmlCanvasManager != undefined) { // ie IE
			G_vmlCanvasManager.initElement(canvasRect);
		}
		var rect=canvasRect.getContext("2d");
		rect.clearRect(0, 0, canvasRect.width, canvasRect.height);
		rect.fillStyle = "#00BFFF";
		rect.globalAlpha="0.5"; 
		rect.clearRect(0,0,640,360);
		
		$(".SmartRectID").each(function(e) {
			var cordinates=$(this).html().split(",");

			var x1=parseInt(cordinates[0]);
			var y1=parseInt(cordinates[1]);
			var x2=parseInt(cordinates[2]);
			var y2=parseInt(cordinates[3]);
			
			rect.fillRect(x1,y1,x2-x1,y2-y1);
		});
	},
	getArea:function(xmlData){
		
		var xml_data=$.parseXML(xmlData);

		var i=0;
		var loopCount=$(xml_data).find("Enabled").length;
		
		areaCount=0;
		for(i=0;i<loopCount;i++)
		{
			var parentFound=$(xml_data).find("FocusSetupArea"+i);
			var tmpX1 = $(parentFound).find("AreaLeft").text();
			var tmpY1 = $(parentFound).find("AreaTop").text();
			var tmpX2 = $(parentFound).find("AreaRight").text();
			var tmpY2 = $(parentFound).find("AreaBottom").text();
			
			tmpX1=Math.ceil(parseInt(tmpX1)/(focusSetup.OW/focusSetup.viewerW));
			tmpX2=Math.ceil(parseInt(tmpX2)/(focusSetup.OW/focusSetup.viewerW));
			tmpY1=Math.ceil(parseInt(tmpY1)/(focusSetup.OH/focusSetup.viewerH));
			tmpY2=Math.ceil(parseInt(tmpY2)/(focusSetup.OH/focusSetup.viewerH));

			var divText="<div style='display:none;' class='SmartRectID'>"+tmpX1+","+tmpY1+","+tmpX2+","+tmpY2+"</div>"
						
			$("#polyDraw").append(divText);
			focusSetup.drawings.reDrawPolygon();
			areaCount++;
		};
		
		
	},
	clearArea:function(){
		areaCount = 0;
		
		$(".SmartRectID").remove();
		focusSetup.drawings.reDrawPolygon();
	},
	setArea_xml:function(){
		var tmpCount = 0;
		var data = '';
		
		$(".SmartRectID").each(function(e) {
			var cordinates=$(this).html().split(",");

			var x1=parseInt(cordinates[0]);
			var y1=parseInt(cordinates[1]);
			var x2=parseInt(cordinates[2]);
			var y2=parseInt(cordinates[3]);

			x1=Math.ceil(x1*(focusSetup.OW/focusSetup.viewerW));
			x2=Math.ceil(x2*(focusSetup.OW/focusSetup.viewerW));
			y1=Math.ceil(y1*(focusSetup.OH/focusSetup.viewerH));
			y2=Math.ceil(y2*(focusSetup.OH/focusSetup.viewerH));

			if(x1 < 0){
				x1 = 0;
			}
			if(y1 < 0){
				y1 = 0;
			}
			if(x2 > focusSetup.OW){
				x2 = focusSetup.OW-1;
			}
			if(y2 > focusSetup.OH){
				y2 = focusSetup.OH-1;
			}

			data += "<AreaLeft>" + x1 + "</AreaLeft>\
						<AreaTop>" + y1 + "</AreaTop>\
						<AreaRight>" + x2 + "</AreaRight>\
						<AreaBottom>" + y2 + "</AreaBottom>";
				
			tmpCount++;
		});

		return data;
	    
	},
	getWidth:function(index){
		var tmpCount = 0;
		var data = '';
		var width = 0;
		
		$(".SmartRectID").each(function(e) {
			var cordinates=$(this).html().split(",");

			var x1=parseInt(cordinates[0]);
			var y1=parseInt(cordinates[1]);
			var x2=parseInt(cordinates[2]);
			var y2=parseInt(cordinates[3]);

			x1=Math.ceil(x1*(focusSetup.OW/focusSetup.viewerW));
			x2=Math.ceil(x2*(focusSetup.OW/focusSetup.viewerW));
			y1=Math.ceil(y1*(focusSetup.OH/focusSetup.viewerH));
			y2=Math.ceil(y2*(focusSetup.OH/focusSetup.viewerH));

			if(x1 < 0){
				x1 = 0;
			}
			if(y1 < 0){
				y1 = 0;
			}
			if(x2 > focusSetup.OW){
				x2 = focusSetup.OW-1;
			}
			if(y2 > focusSetup.OH){
				y2 = focusSetup.OH-1;
			}

			width = x2 - x1;

			if (index == tmpCount)
			{
				return width;
			}
				
			tmpCount++;
		});
		return width;
	},
	getHeight:function(index){
		var tmpCount = 0;
		var data = '';
		var height = 0;
		
		$(".SmartRectID").each(function(e) {
			var cordinates=$(this).html().split(",");

			var x1=parseInt(cordinates[0]);
			var y1=parseInt(cordinates[1]);
			var x2=parseInt(cordinates[2]);
			var y2=parseInt(cordinates[3]);

			x1=Math.ceil(x1*(focusSetup.OW/focusSetup.viewerW));
			x2=Math.ceil(x2*(focusSetup.OW/focusSetup.viewerW));
			y1=Math.ceil(y1*(focusSetup.OH/focusSetup.viewerH));
			y2=Math.ceil(y2*(focusSetup.OH/focusSetup.viewerH));

			if(x1 < 0){
				x1 = 0;
			}
			if(y1 < 0){
				y1 = 0;
			}
			if(x2 > focusSetup.OW){
				x2 = focusSetup.OW-1;
			}
			if(y2 > focusSetup.OH){
				y2 = focusSetup.OH-1;
			}

			height = y2 - y1;

			if (index == tmpCount)
			{
				return height;
			}
				
			tmpCount++;
		});
		return height;
	}
	
};
