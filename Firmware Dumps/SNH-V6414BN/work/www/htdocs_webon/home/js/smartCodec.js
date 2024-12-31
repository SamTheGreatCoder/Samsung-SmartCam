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

smartCodec={};
smartCodec={
	
	getAreaXML:'',
	
	MAX_RESOLUTION_W: 1920,
	MAX_RESOLUTION_H: 1080,
	VIEWER_W: 640,
	VIEWER_H: 360,
	RATIO_W: this.MAX_RESOLUTION_W / this.VIEWER_W,
	RATIO_H: this.MAX_RESOLUTION_H / this.VIEWER_H,
	FLIP_MIRROR: 0,			//"0": Flip OFF / Mirror OFF,  "1": Flip ON /Mirror OFF,  "2": Flip OFF / Mirror ON, "3": Flip ON / Mirror ON	
	IS_PTZ_SUPPORT: false,	

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
smartCodec.drawings={

	rectangle:function(width,height,maxWidth,maxheight,flip_mirror,support_ptz){
		smartCodec.VIEWER_W = width;
		smartCodec.VIEWER_H = height;
		smartCodec.MAX_RESOLUTION_W = maxWidth;
		smartCodec.MAX_RESOLUTION_H = maxheight;
		smartCodec.RATIO_W = maxWidth / width;
		smartCodec.RATIO_H = maxheight / height;
		smartCodec.FLIP_MIRROR = flip_mirror;
		smartCodec.IS_PTZ_SUPPORT = support_ptz;
		
		c=document.getElementById("myCanvas");
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
					
		var Fx, Fy;
		var Ax=0, Ay=0, Bx=0, By=0, index=1;
		var once=false;
		var arrayCount=0;
		var x1=0,y1=0,x2=0,y2=0,x3=0,y3=0,x4=0,y4=0;
		var a1=0,b1=0,a2=0,b2=0,a3=0,b3=0,a4=0,b4=0;
		pCount=0;

		var smartCodecRect = {};
		$("#imgTemp").mousedown(function(e) {			
			if(areaCount > 4 || $("#roi_area_fd").is(":checked"))
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

			smartCodecRect.startX = xVal;
			smartCodecRect.startY = yVal;
				
			firstDrawClick = true;
			isDrawDragging = false;

		});
		
		$("#imgTemp").mousemove(function(e) {
			if(areaCount > 4 || $("#roi_area_fd").is(":checked"))
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
				smartCodecRect.w = xVal - smartCodecRect.startX;
			    smartCodecRect.h = yVal - smartCodecRect.startY;
				smartCodecRect.endX = xVal;
				smartCodecRect.endY = yVal;
				
				context.clearRect(0,0,canvas.width,canvas.height);
				context.lineWidth = 2;
				context.strokeStyle = "#00008B";
				context.globalAlpha="1";
				context.strokeRect(smartCodecRect.startX,smartCodecRect.startY,smartCodecRect.w,smartCodecRect.h);
				
				/*
				c2.strokeStyle = "DeepSkyBlue";
				c2.lineWidth = 3;
				c2.globalAlpha="1";
				c2.strokeRect(smartCodecRect.startX,smartCodecRect.startY,smartCodecRect.w,smartCodecRect.h);
				*/
			}
			isDrawDragging = true;
			
		});
 
		$("#imgTemp").mouseup(function(e) {
			if(areaCount > 4 || $("#roi_area_fd").is(":checked"))
				return;
			
			firstDrawClick = false;
			if(isDrawDragging){
				if(smartCodecRect.startX <= smartCodecRect.endX){
					x1 = smartCodecRect.startX;
					x2 = smartCodecRect.endX;
				}
				else{
					x2 = smartCodecRect.startX;
					x1 = smartCodecRect.endX;
				}
				if(smartCodecRect.startY <= smartCodecRect.endY){
					y1 = smartCodecRect.startY;
					y2 = smartCodecRect.endY+2;
				}
				else{
					y2 = smartCodecRect.startY;
					y1 = smartCodecRect.endY;
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
						smartCodec.drawings.reDrawPolygon();
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
			var parentFound=$(xml_data).find("SmartCodecArea"+i);
			var tmpX1 = $(parentFound).find("AreaLeft").text();
			var tmpY1 = $(parentFound).find("AreaTop").text();
			var tmpX2 = $(parentFound).find("AreaRight").text();
			var tmpY2 = $(parentFound).find("AreaBottom").text();
			
			tmpX1=Math.ceil(parseInt(tmpX1)/(smartCodec.RATIO_W));
			tmpX2=Math.ceil(parseInt(tmpX2)/(smartCodec.RATIO_W));
			tmpY1=Math.ceil(parseInt(tmpY1)/(smartCodec.RATIO_H));
			tmpY2=Math.ceil(parseInt(tmpY2)/(smartCodec.RATIO_H));
			
			if(!smartCodec.IS_PTZ_SUPPORT){
				var tmpSwp = 0;
				if(smartCodec.FLIP_MIRROR == 1) {
					tmpY1=smartCodec.VIEWER_H - tmpY1;
					tmpY2=smartCodec.VIEWER_H - tmpY2;

					tmpSwp = tmpY1;
					tmpY1 = tmpY2;
					tmpY2 = tmpSwp;					
				}
				else if(smartCodec.FLIP_MIRROR == 2) {
					tmpX1=smartCodec.VIEWER_W - tmpX1;
					tmpX2=smartCodec.VIEWER_W - tmpX2;
					
					tmpSwp = tmpX1;
					tmpX1 = tmpX2;
					tmpX2 = tmpSwp;	
				}
				else if(smartCodec.FLIP_MIRROR == 3) {
					tmpY1=smartCodec.VIEWER_H - tmpY1;
					tmpY2=smartCodec.VIEWER_H - tmpY2;
					tmpX1=smartCodec.VIEWER_W - tmpX1;
					tmpX2=smartCodec.VIEWER_W - tmpX2;

					tmpSwp = tmpY1;
					tmpY1 = tmpY2;
					tmpY2 = tmpSwp;
					
					tmpSwp = tmpX1;
					tmpX1 = tmpX2;
					tmpX2 = tmpSwp;
				}
				
			}
						
			var divText="<div style='display:none;' class='SmartRectID'>"+tmpX1+","+tmpY1+","+tmpX2+","+tmpY2+"</div>"
						
			$("#polyDraw").append(divText);
			smartCodec.drawings.reDrawPolygon();
			areaCount++;
		};
		
		
	},
	clearArea:function(){
		areaCount = 0;
		
		$(".SmartRectID").remove();
		smartCodec.drawings.reDrawPolygon();
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

			if(!smartCodec.IS_PTZ_SUPPORT){
				var tmpSwp = 0;
				if(smartCodec.FLIP_MIRROR == 1) {
					y1=smartCodec.VIEWER_H - y1;
					y2=smartCodec.VIEWER_H - y2;
					tmpSwp = y1;
					y1 = y2;
					y2 = tmpSwp;
				}
				else if(smartCodec.FLIP_MIRROR == 2) {
					x1=smartCodec.VIEWER_W - x1;
					x2=smartCodec.VIEWER_W - x2;
					tmpSwp = x1;
					x1 = x2;
					x2 = tmpSwp;
				}
				else if(smartCodec.FLIP_MIRROR == 3) {
					y1=smartCodec.VIEWER_H - y1;
					y2=smartCodec.VIEWER_H - y2;
					x1=smartCodec.VIEWER_W - x1;
					x2=smartCodec.VIEWER_W - x2;
					tmpSwp = y1;
					y1 = y2;
					y2 = tmpSwp;
					
					tmpSwp = x1;
					x1 = x2;
					x2 = tmpSwp;
				}
			}

			x1=Math.ceil(x1*(smartCodec.RATIO_W));
			x2=Math.ceil(x2*(smartCodec.RATIO_W));
			y1=Math.ceil(y1*(smartCodec.RATIO_H));
			y2=Math.ceil(y2*(smartCodec.RATIO_H));

			if(x1 < 0){
				x1 = 0;
			}
			if(y1 < 0){
				y1 = 0;
			}
			if(x2 >= smartCodec.MAX_RESOLUTION_W){
				x2 = smartCodec.MAX_RESOLUTION_W-1;
			}
			if(y2 >= smartCodec.MAX_RESOLUTION_H){
				y2 = smartCodec.MAX_RESOLUTION_H-1;
			}

			data += "<SmartCodecArea"+ tmpCount +">\
						<Enabled>1</Enabled>\
						<AreaLeft>" + x1 + "</AreaLeft>\
						<AreaTop>" + y1 + "</AreaTop>\
						<AreaRight>" + x2 + "</AreaRight>\
						<AreaBottom>" + y2 + "</AreaBottom>\
					</SmartCodecArea"+ tmpCount +">";
				
			tmpCount++;
		});

		return data;
	    
	}	
	
};
