var G_vmlCanvasManager; // so non-IE won't freak out in canvasInit

var c=null;
var c2=null;
var canvas=null;
var context=null;

$(function() {
	$(document).mouseup(function() {		
		if(cropEncoding.firstDrawClick && cropEncoding.isDrawDragging){
			$("#cropCanvasTemp").trigger("mouseup");
		}
	});

});

cropEncoding={};
cropEncoding={
	getAreaXML:'',	
	MAX_RESOLUTION_W: 1920,
	MAX_RESOLUTION_H: 1080,
	viewerW:'',
	viewerH:'',
	isDrawDragging: false,
	firstDrawClick: false,
	
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
cropEncoding.drawing={
	init:function(width,height,maxWidth,maxheight){
		cropEncoding.viewerW = width;
		cropEncoding.viewerH = height;
		cropEncoding.MAX_RESOLUTION_W = maxWidth;
		cropEncoding.MAX_RESOLUTION_H = maxheight;
		
		c=document.getElementById("cropCanvas");;
		if (G_vmlCanvasManager != undefined) { // ie IE
			G_vmlCanvasManager.initElement(c);
		}
		
		c2=c.getContext("2d");
		c2.fillStyle = "#00BFFF";
		c2.globalAlpha="0.5";
		
		canvas=document.getElementById("cropCanvasTemp");
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

		var cropEncodingRect = {};
		$("#cropCanvasTemp").mousedown(function(e) {
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

			cropEncodingRect.startX = xVal;
			cropEncodingRect.startY = yVal;
				
			cropEncoding.firstDrawClick = true;
			cropEncoding.isDrawDragging = false;

		});
		
		$("#cropCanvasTemp").mousemove(function(e) {
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
			
			if(cropEncoding.firstDrawClick){	
				cropEncodingRect.w = xVal - cropEncodingRect.startX;
			    cropEncodingRect.h = yVal - cropEncodingRect.startY;
				cropEncodingRect.endX = xVal;
				cropEncodingRect.endY = yVal;
				
				context.clearRect(0,0,canvas.width,canvas.height);
				context.lineWidth = 2;
				context.strokeStyle = "#00008B";
				context.globalAlpha="1";
				context.strokeRect(cropEncodingRect.startX,cropEncodingRect.startY,cropEncodingRect.w,cropEncodingRect.h);
			}
			cropEncoding.isDrawDragging = true;
			
		});
 
		$("#cropCanvasTemp").mouseup(function(e) {
			cropEncoding.firstDrawClick = false;
			if(cropEncoding.isDrawDragging){
				if(cropEncodingRect.startX <= cropEncodingRect.endX){
					x1 = cropEncodingRect.startX;
					x2 = cropEncodingRect.endX;
				}
				else{
					x2 = cropEncodingRect.startX;
					x1 = cropEncodingRect.endX;
				}
				if(cropEncodingRect.startY <= cropEncodingRect.endY){
					y1 = cropEncodingRect.startY;
					y2 = cropEncodingRect.endY+2;
				}
				else{
					y2 = cropEncodingRect.startY;
					y1 = cropEncodingRect.endY;
				}

				var	cX=Math.ceil(x1*(cropEncoding.MAX_RESOLUTION_W/cropEncoding.viewerW));
				var	cY=Math.ceil(y1*(cropEncoding.MAX_RESOLUTION_H/cropEncoding.viewerH));
				var	cW=Math.ceil(Math.abs(cropEncodingRect.w)*(cropEncoding.MAX_RESOLUTION_W/cropEncoding.viewerW));
				var	cH=Math.ceil(Math.abs(cropEncodingRect.h)*(cropEncoding.MAX_RESOLUTION_H/cropEncoding.viewerH));

				if($("#profile_crop_ratio").val() == 0){		//16:9
					cH = Math.ceil(cW * (9/16));
				}else if($("#profile_crop_ratio").val() == 1){		//4:3
					cH = Math.ceil(cW * (3/4));
				}

				if (parseInt(cY) + parseInt(cH) >= cropEncoding.MAX_RESOLUTION_H)
				{
					var changeY = cropEncoding.MAX_RESOLUTION_H - parseInt(cH);
					cY = changeY;
					if (parseInt(cY) + parseInt(cH) >= cropEncoding.MAX_RESOLUTION_H)
					{
						cY -= 2;
						cH -= 2;
					}
				}

				if(cW < 320){
					context.clearRect(0,0,canvas.width,canvas.height);
					return;	
				}
				if(cH < 240){
					context.clearRect(0,0,canvas.width,canvas.height);
					return;	
				}
				
				if (parseInt(cX) < 0 ) {
					cX = 0;
				}
				if (parseInt(cY) < 0) {
					cY = 0;
				}

				if (cropEncoding.MAX_RESOLUTION_W == 1280 && cropEncoding.MAX_RESOLUTION_H == 1024)
				{
					if (parseInt(cW) > 1024) {
						cW = 1024;
					}
					if (parseInt(cH) > 768) {
						cH = 768;
					}
				}
				else
				{
					if($("#profile_crop_ratio").val() == 0){		//16:9
						if (parseInt(cW) > 1280) {
							cW = 1280;
						}
						if (parseInt(cH) > 720) {
							cH = 720;
						}
					}
					else if($("#profile_crop_ratio").val() == 1){		//4:3
						if (parseInt(cW) > 1280) {
							cW = 1280;
						}
						if (parseInt(cH) > 960) {
							cH = 960;
						}
					} 
					else // 5:4
					{
						if (parseInt(cW) > 1280) {
							cW = 1280;
						}
						if (parseInt(cH) > 1024) {
							cH = 1024;
						}
					}
				}

				if(cX % 2 == 1){
					cX += 1;
				}
				if(cY % 2 == 1){
					cY += 1;
				}
				if(cW % 2 == 1){
					cW += 1;
				}
				if(cH % 2 == 1){
					cH += 1;
				}

				
				if(!(typeof cX == "undefined" || typeof cY == "undefined" || typeof cW == "undefined" || typeof cH == "undefined")){
					$(".CropID").remove();
					$("#cropDraw").append("<div style='display:none;' class='CropID'>"+cX+","+cY+","+cW+","+cH+"</div>");
					cropEncoding.drawing.reDraw();
				}
				context.clearRect(0,0,canvas.width,canvas.height);

				cropEncoding.isDrawDragging = false;
			}
		});
	},
	reDraw:function(){
		var canvasRect=document.getElementById("cropCanvas");
		if (G_vmlCanvasManager != undefined) { // ie IE
			G_vmlCanvasManager.initElement(canvasRect);
		}
		$(".CropID").each(function(e) {
			var cordinates=$(this).html().split(",");

			var msg = "X : " + cordinates[0] + "  Y : " + cordinates[1] + "  W : " + cordinates[2] + "  H : " + cordinates[3];
			$("#span_cropsize").text(msg);
			
			var tmpCx=Math.ceil(parseInt(cordinates[0])/(cropEncoding.MAX_RESOLUTION_W/cropEncoding.viewerW));
			var tmpCy=Math.ceil(parseInt(cordinates[1])/(cropEncoding.MAX_RESOLUTION_H/cropEncoding.viewerH));
			var tmpCw=Math.ceil(parseInt(cordinates[2])/(cropEncoding.MAX_RESOLUTION_W/cropEncoding.viewerW));
			var tmpCh=Math.ceil(parseInt(cordinates[3])/(cropEncoding.MAX_RESOLUTION_H/cropEncoding.viewerH));

			var rect=canvasRect.getContext("2d");
			rect.clearRect(0, 0, canvasRect.width, canvasRect.height);
			rect.fillStyle = "#00BFFF";
			rect.globalAlpha="0.5";
			rect.fillRect(tmpCx,tmpCy,tmpCw,tmpCh);
		});

	},
	setArea:function(cX, cY, cW, cH){
		var tmpCx=cX;
		var tmpCy=cY;
		var tmpCw=cW;
		var tmpCh=cH;

		if (parseInt(tmpCx) < 0 ) {
			tmpCx = 0;
		}
		if (parseInt(tmpCy) < 0) {
			tmpCy = 0;
		}

		if (cropEncoding.MAX_RESOLUTION_W == 1280 && cropEncoding.MAX_RESOLUTION_H == 1024)
		{
			if (parseInt(tmpCw) > 1024) {
				tmpCw = 1024;
			}
			if (parseInt(tmpCh) > 768) {
				tmpCh = 768;
			}
		}
		else
		{
			if (parseInt(tmpCw) > 1280) {
				tmpCw = 1280;
			}
			if (parseInt(tmpCh) > 1024) {
				tmpCh = 1024;
			}
		}
		
		var divText="<div style='display:none;' class='CropID'>"+tmpCx+","+tmpCy+","+tmpCw+","+tmpCh+"</div>"
		$(".CropID").remove();
		$("#cropDraw").append(divText);
		cropEncoding.drawing.reDraw();
	},
	getArea:function(){
		var cordinates = $(".CropID").html().split(",");
		return cordinates;
	},
	clearArea:function(){
		$(".CropID").remove();
		cropEncoding.drawing.reDraw();
	}
	
};

