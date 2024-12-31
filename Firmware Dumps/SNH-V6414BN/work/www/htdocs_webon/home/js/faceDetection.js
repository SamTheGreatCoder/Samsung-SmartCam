//js

var G_vmlCanvasManager; // so non-IE won't freak out in canvasInit

FaceDetection={		
	getRectagnleXML:'',
	setRectangleXML:'',
	MAX_RESOLUTION_W: 1920,
	MAX_RESOLUTION_H: 1080,
	VIEWER_W:'',
	VIEWER_H:'',
	RATIO_W: this.MAX_RESOLUTION_W / this.VIEWER_W,
	RATIO_H: this.MAX_RESOLUTION_H / this.VIEWER_H,
	FLIP_MIRROR: 0,			//"0": Flip OFF / Mirror OFF,  "1": Flip ON /Mirror OFF,  "2": Flip OFF / Mirror ON, "3": Flip ON / Mirror ON	

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
FaceDetection.drawings={

	rectangle: function(){
				
				
					var x1, x2, y1, y2;
					var top, left, width, height;
					var isDragging = false;
					var index = 0,arrayCount=0;
					//var xPts=[[0,0,],[0,0],[0,0],[0,0]];
					//var yPts=[[0,0,],[0,0],[0,0],[0,0]];
					$("#FaceDetection_uri").mousedown(function(e) {
					
						
						if($("#FaceDetection .selected_area").length>4)  return; 
						
						isDragging = true;
						//$("#current").remove();
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
						
						var topVal=yVal+2
						var leftVal=xVal+2;
						
						box = $('<div class="selected_area" style="position: absolute;border:2px #18436b solid;z-index:999;"/>')
							.css("background-position-x","-"+leftVal+"px")
							.css("background-position-y","-"+topVal+"px")
							.hide();
						$("#FaceDetection #drawings").append(box);
						
						
						x1 = x1 = xVal;
						y1 = yVal;
						y1 = yVal;
						var currId = 'current' + index;
						box.attr({
							id : currId
						});
						
						
						
					});
					$("#FaceDetection_uri").mousemove(function(e) {
						
						if($("#FaceDetection .selected_area").length>4) return;
						
						
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
						
						if (isDragging) {
							if (yVal > y1) {
								top = y1
							} else {
								top = yVal;
							}
							if (xVal > x1) {
								left = x1
							} else {
								left = xVal
							}
							width = Math.abs(xVal - x1);
							if (width < 16)
								width = 16;
							height = Math.abs(yVal - y1)
							if (height < 16)
								height = 16;

							var currId = 'current' + index;
							$("#FaceDetection #" + currId).css({
								position : "absolute",
								left : left,
								top : top,
								width : width,
								height : height
							});

							$("#FaceDetection #" + currId).show();
							//$("#current").attr({ id: ''});
						}
					});
					
					$("#FaceDetection_uri").mouseup(function(e) {
					
						if($("#FaceDetection .selected_area").length>4) return;
					
						isDragging = false;
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
						
						var currId = 'current' + index;

						if (x1 == x2 && y1 == y2) {
							$("#FaceDetection #" + currId).css({
								position : "absolute",
								left : x1,
								top : y1,
								width : "16",
								height : "16"
							});
							$("#FaceDetection #" + currId).show();

						};
						index++;
						
					});
					
					

		

	}, 
	getRectangle: function(){
			var xml_data=$.parseXML(FaceDetection.getRectagnleXML);
			var i=0;
			$(xml_data).find("GetFDArea ObjectArea").each(function()
			{
				
				
					var x=$(this).find("X").text()/(FaceDetection.RATIO_W);
					var y=$(this).find("Y").text()/(FaceDetection.RATIO_H);
				
						
				
					var width=$(this).find("Width").text()/(FaceDetection.RATIO_W);
					var height=$(this).find("Height").text()/(FaceDetection.RATIO_H);
					var divElem="<div class='selected_area' style='position: absolute;border:2px #18436b solid;z-index:999;width:"+width+"px;height:"+height+"px;left:"+x+"px;top:"+y+"px;'></div>";
					$("#FaceDetection #drawings").append(divElem);
				
				var topVal=y+2
				var leftVal=x+2;
				$("#FaceDetection #drawings .selected_area").eq(i).css("background-position-x","-"+leftVal+"px");
				$("#FaceDetection #drawings .selected_area").eq(i).css("background-position-y","-"+topVal+"px");
					i++;
			});
		
	},
	setRectangle: function(){
		var i=0;
		var setXmlData='';
		$("#FaceDetection .selected_area").each(function()
		{
			var top=parseInt($(this).css("top"), 10);
			var left=parseInt($(this).css("left"), 10);
			var right=parseInt($(this).css("width"), 10)+left;
			var bottom=parseInt($(this).css("height"), 10)+top;
			
			left=left*(FaceDetection.RATIO_W);
			top=top*(FaceDetection.RATIO_H);
			right=right*(FaceDetection.RATIO_W);
			bottom=bottom*(FaceDetection.RATIO_H);

			if(left < 0){
				left = 0;
			}
			if(top < 0){
				top = 0;
			}
			if(right >= FaceDetection.MAX_RESOLUTION_W){
				right = FaceDetection.MAX_RESOLUTION_W-1;
			}
			if(bottom >= FaceDetection.MAX_RESOLUTION_H){
				bottom = FaceDetection.MAX_RESOLUTION_H-1;
			}
			
			setXmlData="<ObjectArea"+i+"><NumPoint>2</NumPoint><FDPoint0><PosX>"+left+"</PosX><PosY>"+top+"</PosY></FDPoint0><FDPoint1><PosX>"+right+"</PosX><PosY>"+bottom+"</PosY></FDPoint1></ObjectArea"+i+">";
			
			FaceDetection.setRectangleXML+=setXmlData;
			i++;
			
		});
		
		//FaceDetection.setRectangleXML="<SetSmartCodecConfiguration><Mode>1</Mode><QualityLevel>0</QualityLevel>"+setXmlData+"</SetSmartCodecConfiguration>";
	},
	polyCount:0,
	deleteClass:"",
	polygon:function(max_polyCount,width,height,maxWidth,maxheight,flip_mirror){
		FaceDetection.VIEWER_W = width;
		FaceDetection.VIEWER_H = height;
		FaceDetection.MAX_RESOLUTION_W = maxWidth;
		FaceDetection.MAX_RESOLUTION_H = maxheight;
		FaceDetection.RATIO_W = maxWidth / width;
		FaceDetection.RATIO_H = maxheight / height;
		FaceDetection.FLIP_MIRROR = flip_mirror;		
	
		var context;
		var c=document.getElementById("FDPoly");;
		if (G_vmlCanvasManager != undefined) { // ie IE
			G_vmlCanvasManager.initElement(c);
		}
		var c2=c.getContext("2d");
		c2.lineWidth = 2;
		c2.globalAlpha="1"; 
		
		var canvas=document.getElementById("FDPolyTemp");
		if (G_vmlCanvasManager != undefined) { // ie IE
			G_vmlCanvasManager.initElement(canvas);
		}
		var context=canvas.getContext("2d");
		context.lineWidth = 2;
		context.strokeStyle = "yellow";		
		context.globalAlpha="1";
		
		var Fx, Fy;
		var Ax=0, Ay=0, Bx=0, By=0, index=1;
		var isDragging = false;
		var x1=0,y1=0,x2=0,y2=0,x3=0,y3=0,x4=0,y4=0;
		pCount=0;
		
		$("#FDPolyTemp").click(function(e) {
			c2.strokeStyle = "blue";
			c2.globalCompositeOperation="source-over";
			
			//if(e.which!=1) return;			
			if($(".FDpolygonID").length >=max_polyCount) return;
			
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
		
			if(index != 1 && lineDistance(Ax,Ay,xVal,yVal)<20) { return; }
			
			if(index==1){
				isDragging=true;
				x1 = xVal,y1= yVal;
				Ax=xVal, Ay=yVal;// getting mouse move action
				index++;
				$("#DisableFDSelectLayer").css("display","block");
				// red
			}
			else if(index==2){
				x2 = xVal,y2= yVal;
				
				Ax=xVal, Ay=yVal;// getting mouse move action
				c2.beginPath();
				c2.moveTo(x1, y1);
				c2.lineTo(x2, y2);
				c2.stroke();
				c2.closePath();
				index++;
			}
			else if(index==3){
				x3 = xVal,y3= yVal;
			
				Ax=xVal, Ay=yVal;// getting mouse move action
				 c2.beginPath();
				 c2.moveTo(x2, y2);
				 c2.lineTo(x3, y3);
				 c2.stroke();
				 c2.closePath();	
				 index++;
			}
			else if(index==4){
				x4 = xVal,y4= yVal;
				
				var a={x:x1,y:y1},c={x:x3,y:y3},b={x:x2,y:y2};
				var d={x:x4,y:y4};
				
				
				var totAngle22=Math.floor(GetAngleABC22(a,b,c))+Math.floor(GetAngleABC22(b,c,d))+Math.floor(GetAngleABC22(c,d,a))+Math.floor(GetAngleABC22(d,a,b));
							
				if(Math.abs(totAngle22)<=1 || Math.abs(GetAngleABC22(d,a,b)) > 170 ){ return; }
				else if(distToSegment(a, d, c) <20) { return; }
				else { Ax=xVal, Ay=yVal;}
				
				if(x1 < 0) x1 = 0;
				if(x2 < 0) x2 = 0;
				if(x3 < 0) x3 = 0;
				if(x4 < 0) x4 = 0;
				
				if(y1 < 0) y1 = 0;
				if(y2 < 0) y2 = 0;
				if(y3 < 0) y3 = 0;
				if(y4 < 0) y4 = 0;
				
				var polygonPoints = [[x1,y1],[x2,y2],[x3,y3],[x4,y4]];
				c2.beginPath();
				c2.moveTo(x3, y3);
				c2.lineTo(x4, y4);
				c2.stroke();
				c2.moveTo(x4, y4);
				c2.lineTo(x1, y1);
				c2.stroke();
				c2.closePath(); 
				
				c2.strokeStyle = "#18436D";
				c2.fillStyle = "#18436D";
				
				c2.beginPath();	
				c2.moveTo(x1, y1);c2.lineTo(x2, y2);c2.stroke();
				c2.moveTo(x2, y2);c2.lineTo(x3, y3);c2.stroke();
				c2.moveTo(x3, y3);c2.lineTo(x4, y4);c2.stroke();
				c2.moveTo(x4, y4);c2.lineTo(x1, y1);c2.stroke();
				c2.closePath();
				
				
				c2.fillPolygon(polygonPoints, '#18436D','#18436D');
				$("#FDPolyDraw").append("<div style='display:none;' class='FDpolygonID' id='"+"FDpolygon"+FaceDetection.drawings.polyCount+"'>"+x1+","+y1+","+x2+","+y2+","+x3+","+y3+","+x4+","+y4+"</div>");
				context.clearRect(0, 0, canvas.width, canvas.height);
				FaceDetection.drawings.updatePolygon();
				isDragging=false;
				index=1;			
				FaceDetection.drawings.polyCount++;
				$("#DisableFDSelectLayer").css("display","none");
				return;
			}
		});
		
		$("#FDPolyTemp").mousemove(function(e) {
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
			
			if (isDragging) {
				context.clearRect(0, 0, canvas.width, canvas.height);
				context.beginPath();
				context.moveTo(Ax, Ay);
				context.lineTo(xVal, yVal);
				context.stroke();
				context.closePath();
			}
		});
		
		$("#FDPolyTemp").on("contextmenu",function(e){
			if(isDragging){
				context.clearRect(0, 0, canvas.width, canvas.height);
				isDragging=false;
				index = 1;
				FaceDetection.drawings.updatePolygon();
				$("#DisableFDSelectLayer").css("display","none");
				return false;
			}
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
			
			$(".FDpolygonID").each(function(e) {
				var cordinates=$(this).html().split(",");
				var x1=parseInt(cordinates[0]);
				var y1=parseInt(cordinates[1]);
				var x2=parseInt(cordinates[2]);
				var y2=parseInt(cordinates[3]);
				var x3=parseInt(cordinates[4]);
				var y3=parseInt(cordinates[5]);
				var x4=parseInt(cordinates[6]);
				var y4=parseInt(cordinates[7]);
				points = [
				{x: x1, y: y1},
				{x: x2, y: y2},
				{x: x3, y: y3},
				{x: x4, y: y4},
				{x: x1, y: y1}
				];

				if(isPointInPoly(points, {x: xVal, y: yVal})) { 
					c2.strokeStyle = "#00ffff";
					c2.beginPath();	
					c2.moveTo(x1, y1);c2.lineTo(x2, y2);c2.stroke();
					c2.moveTo(x2, y2);c2.lineTo(x3, y3);c2.stroke();
					c2.moveTo(x3, y3);c2.lineTo(x4, y4);c2.stroke();
					c2.moveTo(x4, y4);c2.lineTo(x1, y1);c2.stroke();
					c2.closePath();
					FaceDetection.drawings.deleteClass=$(this).attr("id");
					var input = confirm(deleteLang);
					if(input) {
						$("#FDPolyDraw div").remove("#"+FaceDetection.drawings.deleteClass);
						FaceDetection.drawings.updatePolygon();
						return false;
						}else {
						FaceDetection.drawings.updatePolygon(); 
					};
					return false;
				}
			});
			
			return false;
		});

	},
	setPolygonData:function(){
		var i=0;;
		var FDresponse='';
		var leftFD=0;
		
		$("#FDPolyDraw .FDpolygonID").each(function()
		{
			var cordinates=$(this).html().split(",");
			
			var x1=parseInt(cordinates[0],10);
			var y1=parseInt(cordinates[1],10);
			var x2=parseInt(cordinates[2],10);
			var y2=parseInt(cordinates[3],10);
			var x3=parseInt(cordinates[4],10);
			var y3=parseInt(cordinates[5],10);
			var x4=parseInt(cordinates[6],10);
			var y4=parseInt(cordinates[7],10);
			
			var xpos = [x1,x2,x3,x4];
			var ypos = [y1,y2,y3,y4];
			
			if(FaceDetection.FLIP_MIRROR == 1) {
				for(var j = 0; j < 4; j++){
					ypos[j]=FaceDetection.VIEWER_H - ypos[j];
				}
			}
			else if(FaceDetection.FLIP_MIRROR == 2) {
				for(var j = 0; j < 4; j++){
					xpos[j]=FaceDetection.VIEWER_W - xpos[j];
				}
			}
			else if(FaceDetection.FLIP_MIRROR == 3) { 
				for(var j = 0; j < 4; j++){
					ypos[j]=FaceDetection.VIEWER_H - ypos[j];
				}	
				for(var j = 0; j < 4; j++){
					xpos[j]=FaceDetection.VIEWER_W - xpos[j];
				}
			}
			
			var posXml = '';
			for(var j = 0; j < 4; j++){
				xpos[j] = xpos[j]*(FaceDetection.RATIO_W);
				ypos[j] = ypos[j]*(FaceDetection.RATIO_H);

				if(xpos[j] < 0){
					xpos[j] = 0;
				}
				if(ypos[j] < 0){
					ypos[j] = 0;
				}
				if(xpos[j] >= FaceDetection.MAX_RESOLUTION_W){
					xpos[j] = FaceDetection.MAX_RESOLUTION_W-1;
				}
				if(ypos[j] >= FaceDetection.MAX_RESOLUTION_H){
					ypos[j] = FaceDetection.MAX_RESOLUTION_H-1;
				}

				posXml += "<FDPoint"+j+"><PosX>"+xpos[j]+"</PosX><PosY>"+ypos[j]+"</PosY></FDPoint"+j+">";
			}

			
			FDresponse+="<ObjectArea"+i+"><NumPoint>4</NumPoint>"+posXml+"</ObjectArea"+i+">";
			
			i++;
			leftFD=$("#FDPolyDraw .FDpolygonID").length;
		});
		
		for(var j=leftFD;j<4;j++){
			var rect_xml_data=$.parseXML(FaceDetection.setFDXML);
			
			FDresponse+="<ObjectArea"+j+">\
								<NumPoint>0</NumPoint>\
								<FDPoint0><PosX>0</PosX><PosY>0</PosY></FDPoint0>\
								<FDPoint1><PosX>0</PosX><PosY>0</PosY></FDPoint1>\
								<FDPoint2><PosX>0</PosX><PosY>0</PosY></FDPoint2>\
								<FDPoint3><PosX>0</PosX><PosY>0</PosY></FDPoint3>\
							</ObjectArea"+j+">";
			
			
		}

		///////////////////////////////////////////////////////////////////////////////////////////////////////////////
		
		return FDresponse;
	},
	getPolygon:function(xmlData){
		var c=document.getElementById("FDPoly");
		if (G_vmlCanvasManager != undefined) { // ie IE
			G_vmlCanvasManager.initElement(c);
		}
		var c2=c.getContext("2d");
		c2.lineWidth = 2;
		c2.strokeStyle = "#18436D";
		c2.fillStyle = "#18436D";
		c2.globalAlpha="1"; 
		
		var xml_data=$.parseXML(xmlData);
		$(xml_data).find("ObjectArea").each(function()
		{
			var x1=0,y1=0,x2=0,y2=0,x3=0,y3=0,x4=0,y4=0;
			
			x1=$(this).find("Point0 X").text()/(FaceDetection.RATIO_W);
			y1=$(this).find("Point0 Y").text()/(FaceDetection.RATIO_H);
			x2=$(this).find("Point1 X").text()/(FaceDetection.RATIO_W);
			y2=$(this).find("Point1 Y").text()/(FaceDetection.RATIO_H);
			c2.beginPath();
			c2.moveTo(x1, y1);
			c2.lineTo(x2, y2);
			c2.stroke();	
			
			x3=$(this).find("Point2 X").text()/(FaceDetection.RATIO_W);
			y3=$(this).find("Point2 Y").text()/(FaceDetection.RATIO_H);
			c2.moveTo(x2, y2);
			c2.lineTo(x3, y3);
			c2.stroke();
			
			x4=$(this).find("Point3 X").text()/(FaceDetection.RATIO_W);
			y4=$(this).find("Point3 Y").text()/(FaceDetection.RATIO_H);
			
			c2.moveTo(x3, y3);
			c2.lineTo(x4, y4);
			c2.stroke();
			c2.moveTo(x4, y4);
			c2.lineTo(x1, y1);
			c2.stroke();
			c2.closePath();
			isDragging=false;
			var polygonPoints = [[x1,y1],[x2,y2],[x3,y3],[x4,y4]];
			
			c2.fillPolygon(polygonPoints, '#18436D','#18436D');
			
			
			$("#FDPolyDraw").append("<div style='display:none;' class='FDpolygonID' id='"+"FDpolygon"+FaceDetection.drawings.polyCount+"'>"+x1+","+y1+","+x2+","+y2+","+x3+","+y3+","+x4+","+y4+"</div>");
			
			FaceDetection.drawings.polyCount++;
		});
		FaceDetection.drawings.updatePolygon();
	},
	reDrawPolygon:function(isDetect){
		var canvasRect=document.getElementById("FDPoly");
		if (G_vmlCanvasManager != undefined) { // ie IE
			G_vmlCanvasManager.initElement(canvasRect);
		}
		var rect=canvasRect.getContext("2d");
		rect.clearRect(0, 0, canvasRect.width, canvasRect.height);
		//rect.globalCompositeOperation="source-over";
		if(isDetect){
			rect.strokeStyle = "#FF1800";
		}else{
			rect.strokeStyle = "#009CFF";
		}
		
		//rect.fillStyle = "#009CFF";
		rect.globalAlpha="1";
		$(".FDpolygonID").each(function(e) {
			
			var cordinates=$(this).html().split(",");

			var x1=parseInt(cordinates[0]);
			var y1=parseInt(cordinates[1]);
			var x2=parseInt(cordinates[2]);
			var y2=parseInt(cordinates[3]);
			var x3=parseInt(cordinates[4]);
			var y3=parseInt(cordinates[5]);
			var x4=parseInt(cordinates[6]);
			var y4=parseInt(cordinates[7]);
			var polygonPoints = [[x1,y1],[x2,y2],[x3,y3],[x4,y4]];
			rect.beginPath();	
			rect.moveTo(x1, y1);rect.lineTo(x2, y2);rect.stroke();
			rect.moveTo(x2, y2);rect.lineTo(x3, y3);rect.stroke();
			rect.moveTo(x3, y3);rect.lineTo(x4, y4);rect.stroke();
			rect.moveTo(x4, y4);rect.lineTo(x1, y1);rect.stroke();
			rect.closePath();
			rect.globalAlpha="0.35";
			if(isDetect){
				rect.fillPolygon(polygonPoints, '#FF1800','#FF1800');
			}else{
				rect.fillPolygon(polygonPoints, '#009CFF','#009CFF');
			}
			
		});
	},
	reDrawPolygonLine:function(){
		var canvasRect=document.getElementById("FDPoly");
		if (G_vmlCanvasManager != undefined) { // ie IE
			G_vmlCanvasManager.initElement(canvasRect);
		}
		var rect=canvasRect.getContext("2d");
		rect.globalCompositeOperation="source-over";
		rect.strokeStyle = "#173D64";
		rect.globalAlpha="1";
		$(".FDpolygonID").each(function(e) {
			
			var cordinates=$(this).html().split(",");

			var x1=parseInt(cordinates[0]);
			var y1=parseInt(cordinates[1]);
			var x2=parseInt(cordinates[2]);
			var y2=parseInt(cordinates[3]);
			var x3=parseInt(cordinates[4]);
			var y3=parseInt(cordinates[5]);
			var x4=parseInt(cordinates[6]);
			var y4=parseInt(cordinates[7]);
			var polygonPoints = [[x1,y1],[x2,y2],[x3,y3],[x4,y4]];
			rect.beginPath();	
			rect.moveTo(x1, y1);rect.lineTo(x2, y2);rect.stroke();
			rect.moveTo(x2, y2);rect.lineTo(x3, y3);rect.stroke();
			rect.moveTo(x3, y3);rect.lineTo(x4, y4);rect.stroke();
			rect.moveTo(x4, y4);rect.lineTo(x1, y1);rect.stroke();
			rect.closePath();
			
		});
	},
	updatePolygon:function(){
		var isDetect = $('#event_fd_detection_mode_on').is(':checked');
		
		FaceDetection.drawings.reDrawPolygon(isDetect);
	}
	/*
	nonDetectionArea:function(){
		FaceDetection.drawings.reDrawPolygon();
	},
	DetectionArea:function(){
		FaceDetection.drawings.reDrawPolygon();
		
		
		var canvasRect=document.getElementById("FDPoly");
		if (G_vmlCanvasManager != undefined) { // ie IE
			G_vmlCanvasManager.initElement(canvasRect);
		}
		var rect=canvasRect.getContext("2d");
		rect.lineWidth = 2;
		rect.globalAlpha="0.8";
		rect.fillStyle = "#173D64";
		rect.globalCompositeOperation="source-out";
		rect.fillRect(0,0,640,480);
		
		FaceDetection.drawings.reDrawPolygonLine();
		
	}
	*/
	
};
	function sqr(x) { return x * x }
function dist2(v, w) { return sqr(v.x - w.x) + sqr(v.y - w.y) }
function distToSegmentSquared(p, v, w) {
  var l2 = dist2(v, w);
  if (l2 == 0) return dist2(p, v);
  var t = ((p.x - v.x) * (w.x - v.x) + (p.y - v.y) * (w.y - v.y)) / l2;
  if (t < 0) return dist2(p, v);
  if (t > 1) return dist2(p, w);
  return dist2(p, { x: v.x + t * (w.x - v.x),
                    y: v.y + t * (w.y - v.y) });
}
function distToSegment(p, v, w) { return Math.sqrt(distToSegmentSquared(p, v, w)); }
function lineDistance(x1,y1,x2,y2)
{
  var xs = 0;
  var ys = 0;
 
  xs = x2 - x1;
  xs = xs * xs;
 
  ys = y2 - y1;
  ys = ys * ys;
 
  return Math.sqrt( xs + ys );
}

function GetAngleABC22( a,b,c)
{
	var ab = { x:b.x - a.x, y:b.y - a.y };
	var cb = { x:b.x - c.x, y:b.y - c.y };
	
	var dot = (ab.x * cb.x + ab.y * cb.y); // dot product
	var cross = (ab.x * cb.y - ab.y * cb.x); // cross product
	
	var alpha = Math.atan2(cross, dot);
	
	return Math.floor(alpha * 180 / 3.141592 + 0.5);
}

function isPointInPoly(poly, pt)
{
	for(var c = false, i = -1, l = poly.length, j = l - 1; ++i < l; j = i)
		((poly[i].y <= pt.y && pt.y < poly[j].y) || (poly[j].y <= pt.y && pt.y < poly[i].y))
		&& (pt.x < (poly[j].x - poly[i].x) * (pt.y - poly[i].y) / (poly[j].y - poly[i].y) + poly[i].x)
		&& (c = !c);
	return c;
};

$(document).ready(function() {

	CanvasRenderingContext2D.prototype.fillPolygon = function (pointsArray, fillColor, strokeColor) {
		if (pointsArray.length <= 0) return;
		this.moveTo(pointsArray[0][0], pointsArray[0][1]);
		for (var i = 0; i < pointsArray.length; i++) {
			this.lineTo(pointsArray[i][0], pointsArray[i][1]);
		}
		if (strokeColor != null && strokeColor != undefined)
		this.strokeStyle = strokeColor;
		this.globalAlpha="1";
		
		if (fillColor != null && fillColor != undefined) {
			this.fillStyle = fillColor;
			this.globalAlpha="0.5"; 
			this.fill();
		}
	}



	$("#apply").on("click",function() {
		
	});

});
