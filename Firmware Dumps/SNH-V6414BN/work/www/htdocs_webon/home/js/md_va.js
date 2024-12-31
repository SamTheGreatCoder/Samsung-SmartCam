
//js
var G_vmlCanvasManager; // so non-IE won't freak out in canvas

var	isDrawDragging= false;
var	firstDrawClick= false;

var VIEW_MODE = {"NONE" : -1,
				  "MD" : 0,
				  "MD_OBJSIZE" : 1,
				  "VA_PASSING" : 2,
				  "VA_ENTERING" : 3,
				  "VA_APPEAR" : 4,
				  "VA_ENTIRE" : 5};



EventSetup={};
EventSetup={
	setVAXML:'<IVConfiguration><Sensitivity>2</Sensitivity><ObjectSize>5</ObjectSize><ManualSize><VSL>4</VSL><VSH>90</VSH><HSL>4</HSL><HSH>91</HSH></ManualSize><Overlay>0</Overlay><VABoxDisplay>0</VABoxDisplay><FullScreen><FullAppear>0</FullAppear><FullDisappear>0</FullDisappear><FullSceneChange>0</FullSceneChange></FullScreen><IVObject></IVObject><IVObject></IVObject><Schedule><Enabled>0</Enabled></Schedule></IVConfiguration>',
	setMDXML:'<MDConfiguration><ObjectMode>1</ObjectMode><Sensitivity>2</Sensitivity><ObjectSize>5</ObjectSize><ManualSize><VSL>4</VSL><VSH>90</VSH><HSL>4</HSL><HSH>91</HSH></ManualSize><Overlay>0</Overlay><VABoxDisplay>0</VABoxDisplay><Schedule><Enabled>0</Enabled></Schedule></MDConfiguration>',

	getLineXML:'<IVLineObject count="3"><LineObject index="0"><PointCount>2</PointCount><LineRule>1</LineRule><Point index ="0"><X>194</X><Y>151</Y></Point><Point index ="1"><X>542</X><Y>567</Y></Point></LineObject><LineObject index="1"><PointCount>2</PointCount><LineRule>2</LineRule><Point index ="0"><X>316</X><Y>785</Y></Point><Point index ="1"><X>958</X><Y>381</Y></Point></LineObject></IVLineObject>',
	getMDxml:'<GetMDArea count ="4"><ObjectArea index="0"><X>156</X><Y>260</Y><Width>262</Width><Height>226</Height></ObjectArea><ObjectArea index="1"><X>702</X><Y>194</Y><Width>242</Width><Height>187</Height></ObjectArea><ObjectArea index="2"><X>380</X><Y>633</Y><Width>262</Width><Height>173</Height></ObjectArea><ObjectArea index="3"><X>820</X><Y>548</Y><Width>136</Width><Height>173</Height></ObjectArea></GetMDArea>',
	getVAXML:'<IVAreaObject count="3"><LineObject index="0"><PointCount>4</PointCount><AreaEnter>1</AreaEnter><AreaExit>0</AreaExit><AreaAppear>0</AreaAppear><AreaDisappear>0</AreaDisappear><Point index ="0"><X>516</X><Y>149</Y></Point><Point index ="1"><X>1014</X><Y>115</Y></Point><Point index ="2"><X>1070</X><Y>900</Y></Point><Point index ="3"><X>346</X><Y>791</Y></Point></LineObject></IVAreaObject>',

	MAX_RESOLUTION_W: 1920,
	MAX_RESOLUTION_H: 1080,
	VIEWER_W: 640,
	VIEWER_H: 360,
	RATIO_W: this.MAX_RESOLUTION_W / this.VIEWER_W,
	RATIO_H: this.MAX_RESOLUTION_H / this.VIEWER_H,
	FLIP_MIRROR: 0,			//"0": Flip OFF / Mirror OFF,  "1": Flip ON /Mirror OFF,  "2": Flip OFF / Mirror ON, "3": Flip ON / Mirror ON	

	TYPE_RECT:1,
	TYPE_POLY:2,

	minMdObjX:0,
	minMdObjY:0,
	maxMdObjX:0,
	maxMdObjY:0,
	viewStatus: -1,
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
	},
	drawLine:function ( lineObjectHandle, Ax, Ay, Bx, By, lineImgPath )
	{
		/*
			*	lineObjectHandle = an IMG tag with position:absolute
		 */
		var
		xMin        = Math.min( Ax, Bx ),
		yMin        = Math.min( Ay, By ),
		xMax        = Math.max( Ax, Bx ),
		yMax        = Math.max( Ay, By ),
		boxWidth    = Math.max( xMax-xMin, 1 ),
		boxHeight   = Math.max( yMax-yMin, 1 ),
		tmp         = Math.min( boxWidth, boxHeight ),
		smallEdge   = 1,
		newSrc;
		
		
		while( tmp>>=1 )
		smallEdge<<=1;
		
		newSrc = lineImgPath+ smallEdge +( (Bx-Ax)*(By-Ay)<0?"up.png":"down.png" );
		if( lineObjectHandle.src.indexOf( newSrc )==-1 )
		lineObjectHandle.src = newSrc;
		
		with( lineObjectHandle.style )
		{
			width   = boxWidth	+"px";
			height  = boxHeight	+"px";
			left    = xMin		+"px";
			top     = yMin		+"px";
		}
	}
	
};

// MD
var mdPolyObj = null;
var mdPolyContext = null;
var mdPolyTempObj = null;
var mdPolyTempContext = null;

// VA
var vaPolyObj = null;
var vaPolyContext = null;
var vaPolyTempObj = null;
var vaPolyTempContext = null;

var vaAreaRectObj = null;
var vaAreaRectContext = null;
var vaAreaRectTempObj = null;
var vaAreaRectTempContext = null;
var vaLineObj = null;
var vaLineContext = null;
var vaLineTempObj = null;
var vaLineTempContext = null;

// Min&Max Object Size

EventSetup.MD={
	xPts:[[0,0],[0,0],[0,0],[0,0]],
	yPts:[[0,0],[0,0],[0,0],[0,0]],
	mdDrawType: EventSetup.TYPE_RECT,
	polyCount:0,
	minMaxRectangle: function(){
		var x1, x2, y1, y2,px=0,py=0;
		var top, left, width, height;
		var index = 0,arrayCount=0;
		var xVal=0, yVal=0;

		//var xPts=[[0,0,],[0,0],[0,0],[0,0]];
		//var yPts=[[0,0,],[0,0],[0,0],[0,0]];
		$("#maxMinCover").mousedown(function(e) {
			var offset = $(this).offset();
			xVal=e.pageX - offset.left;
			yVal=e.pageY - offset.top;
			
			if (window.navigator.msPointerEnabled) {		//Detect IE10 or IE11
				if($(window).scrollLeft() != 0 && e.pageX == e.clientX){
					xVal= xVal + $(window).scrollLeft();
				}
				if($(window).scrollTop() != 0 && e.pageY == e.clientY){
					yVal= yVal + $(window).scrollTop();
				}
			}
			
			arrayCount++;
			firstDrawClick = true;
			isDrawDragging = false;
		
			x1 = xVal;
			y1 = yVal;
			
			return false;
		});
		$("#maxMinCover").mousemove(function(e) {
			var offset = $(this).offset();
			xVal=e.pageX - offset.left;
			yVal=e.pageY - offset.top;
			
			if (window.navigator.msPointerEnabled) {		//Detect IE10 or IE11
				if($(window).scrollLeft() != 0 && e.pageX == e.clientX){
					xVal= xVal + $(window).scrollLeft();
				}
				if($(window).scrollTop() != 0 && e.pageY == e.clientY){
					yVal= yVal + $(window).scrollTop();
				}
			}
			
			if (firstDrawClick) {
				if (yVal > y1) {
					top = y1;
				} else {
					top = yVal;
				}
				if (xVal > x1) {
					left = x1;
				} else {
					left = xVal;
				}

				width = Math.abs(xVal - x1);
				height = Math.abs(yVal - y1);
				
				$("#minMaxTemp").css("left",left).css("top",top).css("width",width).css("height",height);
				$("#minMaxTemp").css("display","block");
			
				px=xVal;py=yVal;
				isDrawDragging = true;
			}
		});
		
		$("#maxMinCover").mouseup(function(e) {
			firstDrawClick = false;				
			isDrawDragging = false;
			x1 = x1 - 1;
			y1 = y1 - 1;
			var width = xVal - x1-1;
			var height = yVal - y1-1;
			var widthAbs = Math.abs(width);
			var heightAbs = Math.abs(height);
			
			$("#minMaxTemp").css("display","none");
			if(parseInt(widthAbs*(EventSetup.RATIO_W)) < $("#md_min_width").spinner("option","min") || parseInt(heightAbs*(EventSetup.RATIO_H)) < $("#md_min_height").spinner("option","min")){
				return;
			}
			
			var rect;
			var vaMode = '';
			if (typeof currentVaMode != 'undefined') {
				vaMode = currentVaMode+'_';
			}

			if ($('.'+vaMode+'event_object_size_max').is(':checked')) {		//max obj
				rect="maxRect";
				var currMinWidth = parseInt($("#"+vaMode+"min_width").val())/(EventSetup.RATIO_W)-2;
				var currMinHeight = parseInt($("#"+vaMode+"min_height").val())/(EventSetup.RATIO_H)-2;
				
				if((widthAbs >= currMinWidth) && (heightAbs >= currMinHeight)){
					var tempWidth = parseInt((widthAbs+2)*(EventSetup.RATIO_W));
					var tempHeight = parseInt((heightAbs+2)*(EventSetup.RATIO_H));
					if(tempWidth > EventSetup.MAX_RESOLUTION_W)
						tempWidth = EventSetup.MAX_RESOLUTION_W;
					if(tempHeight > EventSetup.MAX_RESOLUTION_H)
						tempHeight = EventSetup.MAX_RESOLUTION_H;
						
					$("#"+vaMode+"max_width").val(tempWidth);
					$("#"+vaMode+"max_height").val(tempHeight);
					
					if(width >= 0){
						EventSetup.maxMdObjX = x1;
					}else{
						EventSetup.maxMdObjX = x1 + width;
					}
					if(height >= 0){
						EventSetup.maxMdObjY = y1;
					}else{
						EventSetup.maxMdObjY = y1 + height;
					}
					
					if(xVal < x1){
						x1 = xVal;
					}
					if(yVal < y1){
						y1 = yVal;
					}
					$("#"+rect).css("left",x1).css("top",y1).css("width",widthAbs).css("height",heightAbs);
				}
			}
			else if ($('.'+vaMode+'event_object_size_min').is(':checked')) {			//min obj
				rect="minRect";
				var currMaxWidth = parseInt($("#"+vaMode+"max_width").val())/(EventSetup.RATIO_W)-2;
				var currMaxHeight = parseInt($("#"+vaMode+"max_height").val())/(EventSetup.RATIO_H)-2;
				if((widthAbs <= currMaxWidth) && (heightAbs <= currMaxHeight)){
					var tempWidth = parseInt((widthAbs+2)*(EventSetup.RATIO_W));
					var tempHeight = parseInt((heightAbs+2)*(EventSetup.RATIO_H));
					if(tempWidth > EventSetup.MAX_RESOLUTION_W)
						tempWidth = EventSetup.MAX_RESOLUTION_W;
					if(tempHeight > EventSetup.MAX_RESOLUTION_H)
						tempHeight = EventSetup.MAX_RESOLUTION_H;
					
					$("#"+vaMode+"min_width").val(tempWidth);
					$("#"+vaMode+"min_height").val(tempHeight);

					if(width >= 0){
						EventSetup.minMdObjX = x1;		
					}else{
						EventSetup.minMdObjX = x1 + width;
					}
					if(height >= 0){
						EventSetup.minMdObjY = y1;
					}else{
						EventSetup.minMdObjY = y1 + height;
					}
					if(xVal < x1){
						x1 = xVal;
					}
					if(yVal < y1){
						y1 = yVal;
					}
					$("#"+rect).css("left",x1).css("top",y1).css("width",widthAbs).css("height",heightAbs);
				}
			}
			EventSetup.MD.updateMaxMinOption();
			
		});
	}, 
	setMaxMinArea:function(){
		var vaMode = '';
		if (typeof currentVaMode != 'undefined') {
			vaMode = currentVaMode+'_';
		}
		var currMaxWidth = parseInt($("#"+vaMode+"max_width").val())/(EventSetup.RATIO_W)-2;
		var currMaxHeight = parseInt($("#"+vaMode+"max_height").val())/(EventSetup.RATIO_H)-2;
		var currMinWidth = parseInt($("#"+vaMode+"min_width").val())/(EventSetup.RATIO_W)-2;
		var currMinHeight = parseInt($("#"+vaMode+"min_height").val())/(EventSetup.RATIO_H)-2;
		
		$("#minRect").css("left",EventSetup.minMdObjX).css("top",EventSetup.minMdObjY).css("width",currMinWidth).css("height",currMinHeight);
		$("#maxRect").css("left",EventSetup.maxMdObjX).css("top",EventSetup.maxMdObjY).css("width",currMaxWidth).css("height",currMaxHeight);
		EventSetup.MD.updateMaxMinOption();
	},
	updateMaxMinOption:function(){
		var vaMode = '';
		if (typeof currentVaMode != 'undefined') {
			vaMode = currentVaMode+'_';
		}
	
		var fullOffset = $("#max_min").offset();
		var minOffset = $("#minRect").offset();
		var minXVal = (minOffset.left - fullOffset.left);
		var minYVal = (minOffset.top - fullOffset.top);
		
		minXVal = (parseInt(minXVal*(EventSetup.RATIO_W)) + parseInt($("#"+vaMode+"max_width").val())) - EventSetup.MAX_RESOLUTION_W;
		minYVal = (parseInt(minYVal*(EventSetup.RATIO_H)) + parseInt($("#"+vaMode+"max_height").val())) - EventSetup.MAX_RESOLUTION_H;

		if(minXVal >= 0){
			minXVal = parseInt($("#"+vaMode+"max_width").val()) - minXVal;
		}else{
			minXVal = parseInt($("#"+vaMode+"max_width").val());
		}
		if(minYVal >= 0){
			minYVal = parseInt($("#"+vaMode+"max_height").val()) - minYVal;
		}else{
			minYVal = parseInt($("#"+vaMode+"max_height").val());
		}

		$("#"+vaMode+"min_width").spinner({max: minXVal});
		$("#"+vaMode+"min_height").spinner({max: minYVal});

		var maxOffset = $("#maxRect").offset();	
		var xVal = (maxOffset.left - fullOffset.left);
		var yVal = (maxOffset.top - fullOffset.top);
		
		xVal = EventSetup.MAX_RESOLUTION_W - parseInt(xVal*(EventSetup.RATIO_W));
		yVal = EventSetup.MAX_RESOLUTION_H - parseInt(yVal*(EventSetup.RATIO_H));
		if(xVal > EventSetup.MAX_RESOLUTION_W)
			xVal = EventSetup.MAX_RESOLUTION_W;
		if(yVal > EventSetup.MAX_RESOLUTION_H)
			yVal = EventSetup.MAX_RESOLUTION_H;
		
		$("#"+vaMode+"max_width").spinner({min:$("#"+vaMode+"min_width").val()},{max:xVal});
		$("#"+vaMode+"max_height").spinner({min:$("#"+vaMode+"min_height").val()},{max:yVal});
	},
	deleteClass:"",
	ROTATE: 0,
	init:function(width,height,maxWidth,maxheight,drawType,flip_mirror,support_ptz,rotate){
		EventSetup.VIEWER_W = width;
		EventSetup.VIEWER_H = height;
		this.ROTATE = rotate;
		if(this.ROTATE == 1 || this.ROTATE ==3){
			EventSetup.MAX_RESOLUTION_W = maxheight;
			EventSetup.MAX_RESOLUTION_H = maxWidth;
		}else{
			EventSetup.MAX_RESOLUTION_W = maxWidth;
			EventSetup.MAX_RESOLUTION_H = maxheight;
		}
		EventSetup.RATIO_W = EventSetup.MAX_RESOLUTION_W / EventSetup.VIEWER_W;
		EventSetup.RATIO_H = EventSetup.MAX_RESOLUTION_H / EventSetup.VIEWER_H;
		EventSetup.MD.mdDrawType = drawType;
		EventSetup.FLIP_MIRROR = flip_mirror;
		EventSetup.IS_PTZ_SUPPORT = support_ptz;

		EventSetup.MD.polyCount = 0;
		$("#MDPolyDraw canvas").remove();
		$("#MDPolyDraw span").remove();
		$("#MDPolyDraw").append("<canvas id=\"MDPoly\" width=\""+EventSetup.VIEWER_W+"\" height=\""+EventSetup.VIEWER_H+"\"></canvas>");
		if(BrowserDetect.browser == "Explorer" && getIEVersion() <= 8){
			$("#MDPolyDraw").append("<span class=\"drawArea-position\" style=\"left:0px;background:#000;opacity:0;filter:alpha(opacity=0);\"></span>");
		}
		$("#MDPolyDraw").append("<canvas id=\"MDPolyTemp\" width=\""+EventSetup.VIEWER_W+"\" height=\""+EventSetup.VIEWER_H+"\" style=\"position: absolute;top:0px;left:0px;z-index:1000;\" ></canvas>");

		if(EventSetup.MD.mdDrawType == EventSetup.TYPE_RECT){
			var Fx, Fy;
			var Ax=0, Ay=0, Bx=0, By=0, index=1;
			var once=false;
			var arrayCount=0;
			var x1=0,y1=0,x2=0,y2=0;
			var a1=0,b1=0,a2=0,b2=0,a3=0,b3=0,a4=0,b4=0;

			var rect = {};
			$("#MDPolyTemp").mousedown(function(e) {
				if(e.which != 1) {
					return;
				}	
				
				mdPolyContext.globalCompositeOperation="source-over";
				mdPolyContext.strokeStyle = "#18436D";
				mdPolyTempContext.strokeStyle = "yellow";

				if($(".MDpolygonID").length >=4) return;

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
				
				rect.startX = xVal;
				rect.startY = yVal;
				firstDrawClick = true;
				isDrawDragging = false;
				
			});
			
			$("#MDPolyTemp").mousemove(function(e) {
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
					rect.w = xVal - rect.startX;
				    rect.h = yVal - rect.startY;
					rect.endX = xVal;
					rect.endY = yVal;
					
					mdPolyTempContext.clearRect(0,0,mdPolyTempObj.width,mdPolyTempObj.height);
					
					mdPolyTempContext.strokeStyle = "yellow";
					mdPolyTempContext.lineWidth = 2;
					mdPolyTempContext.globalAlpha="1";
					mdPolyTempContext.strokeRect(rect.startX,rect.startY,rect.w,rect.h);
					isDrawDragging = true;
				}
			});
	 
			$("#MDPolyTemp").mouseup(function(e) {
				if($(".MDpolygonID").length >=4) return;
				
				firstDrawClick = false;
				if(isDrawDragging){
					if(rect.startX <= rect.endX){
						x1 = rect.startX;
						x2 = rect.endX;
					}
					else{
						x2 = rect.startX;
						x1 = rect.endX;
					}
					if(rect.startY <= rect.endY){
						y1 = rect.startY;
						y2 = rect.endY;
					}
					else{
						y2 = rect.startY;
						y1 = rect.endY;
					}
					var width = x2 - x1;
					var hegiht = y2 - y1;
					mdPolyTempContext.clearRect(0, 0, mdPolyTempObj.width, mdPolyTempObj.height);
					
					if(parseInt(width*(EventSetup.RATIO_W)) < 100 || parseInt(hegiht*(EventSetup.RATIO_H)) < 100){
						return;
					}
					$("#MDPolyDraw").append("<div style='display:none;' class='MDpolygonID' id='"+"MDpolygon"+EventSetup.MD.polyCount+"'>"+x1+","+y1+","+x2+","+y2+","+0+","+0+","+0+","+0+"</div>");
					
					EventSetup.MD.updatePolygon();
					EventSetup.MD.polyCount++;

					isDrawDragging = false;
				}
			});

			$("#MDPolyTemp").on("contextmenu",function(e){
				if(isDrawDragging) return false;
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
				
				if (mdPolyObj == null) {
					mdPolyObj = document.getElementById("MDPoly");
					if (G_vmlCanvasManager != undefined) { // ie IE
						G_vmlCanvasManager.initElement(mdPolyObj);
					}
					mdPolyContext = mdPolyObj.getContext("2d");
				}
				mdPolyContext.lineWidth = 2;
				mdPolyContext.globalAlpha="1"; 
				
				$(".MDpolygonID").each(function(e) {
					var cordinates=$(this).html().split(",");
					var x1=parseInt(cordinates[0]);
					var y1=parseInt(cordinates[1]);
					var x2=parseInt(cordinates[2]);
					var y2=parseInt(cordinates[3]);
					
					if(x1 <= xVal && xVal <= x2 && y1 <= yVal && yVal <= y2){
						mdPolyContext.strokeStyle = "#00ffff";
						mdPolyContext.strokeRect(x1,y1,x2-x1,y2-y1);
						var input = confirm(deleteLang);
						if(input){
							var thisID = $(this).attr("id");
							$("#MDPolyDraw div").remove("#"+thisID);
						}
						EventSetup.MD.updatePolygon();

						return false;
					}
				});
				
				return false;
			});
		}
		else{				//polygon type
			var Fx, Fy;
			var Ax=0, Ay=0, Bx=0, By=0, index=1;
			var x1=0,y1=0,x2=0,y2=0,x3=0,y3=0,x4=0,y4=0;
			
			$("#MDPolyTemp").click(function(e) {
				mdPolyContext.globalCompositeOperation="source-over";
				mdPolyContext.strokeStyle = "#18436D";
				mdPolyTempContext.strokeStyle = "yellow";
				mdPolyContext.lineWidth = 2;
				mdPolyContext.globalAlpha="1"; 				
				
				//if(e.which!=1) return;
				if($(".MDpolygonID").length >=4) return;
				
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
					isDrawDragging=true;
					x1 = xVal,y1= yVal;
					Ax=xVal, Ay=yVal;// getting mouse move action
					$("#DisableIVSelectLayer").css("display","block");
					// red
				}
				else if(index==2){
					x2 = xVal,y2= yVal;
					Ax=xVal, Ay=yVal;// getting mouse move action
					mdPolyContext.beginPath();
					mdPolyContext.moveTo(x1, y1);
					mdPolyContext.lineTo(x2, y2);
					mdPolyContext.stroke();
					mdPolyContext.closePath();	
				}
				else if(index==3){
					x3 = xVal,y3= yVal;
					Ax=xVal, Ay=yVal;// getting mouse move action
					mdPolyContext.beginPath();
					mdPolyContext.moveTo(x2, y2);
					mdPolyContext.lineTo(x3, y3);
					mdPolyContext.stroke();
					mdPolyContext.closePath();	
				}
				else if(index==4){
					x4 = xVal,y4= yVal;
					
					var a={x:x1,y:y1},c={x:x3,y:y3},b={x:x2,y:y2};
					var d={x:x4,y:y4};
					
					
					var totAngle22=Math.floor(GetAngleABC22(a,b,c))+Math.floor(GetAngleABC22(b,c,d))+Math.floor(GetAngleABC22(c,d,a))+Math.floor(GetAngleABC22(d,a,b));
								
					if(Math.abs(totAngle22)<=1 || Math.abs(GetAngleABC22(d,a,b)) > 170 ){ return; }
					else if(distToSegment(a, d, c) <20) { return; }
					else { Ax=xVal, Ay=yVal;}

					mdPolyContext.beginPath();
					mdPolyContext.moveTo(x3, y3);
					mdPolyContext.lineTo(x4, y4);
					mdPolyContext.stroke();
						
					mdPolyContext.moveTo(x4, y4);
					mdPolyContext.lineTo(x1, y1);
					mdPolyContext.stroke();
					mdPolyContext.closePath(); 
						
					mdPolyContext.strokeStyle = "#18436D";
					mdPolyContext.fillStyle = "#18436D";
					
					var polygonPoints = [[x1,y1],[x2,y2],[x3,y3],[x4,y4]];
					
					mdPolyContext.fillPolygon(polygonPoints, '#18436D','#18436D');
					$("#MDPolyDraw").append("<div style='display:none;' class='MDpolygonID' id='"+"MDpolygon"+EventSetup.MD.polyCount+"'>"+x1+","+y1+","+x2+","+y2+","+x3+","+y3+","+x4+","+y4+"</div>");
					mdPolyTempContext.clearRect(0, 0, mdPolyTempObj.width, mdPolyTempObj.height);
					EventSetup.MD.updatePolygon();
					isDrawDragging=false;
					index=1;	
					EventSetup.MD.polyCount++;
					$("#DisableIVSelectLayer").css("display","none");
					return;
				}
				
				index++;				
			});
			
				$("#MDPolyTemp").mousemove(function(e) {
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
					
					if (isDrawDragging) {
						mdPolyTempContext.clearRect(0, 0, mdPolyTempObj.width, mdPolyTempObj.height);
						mdPolyTempContext.beginPath();
						mdPolyTempContext.moveTo(Ax, Ay);
						mdPolyTempContext.lineTo(xVal, yVal);
						mdPolyTempContext.stroke();
						mdPolyTempContext.closePath();
					}
				});
				
			$("#MDPolyTemp").on("contextmenu",function(e){
				
				if(isDrawDragging){
					isDrawDragging=false;
					index = 1;
					EventSetup.MD.updatePolygon();
					$("#DisableIVSelectLayer").css("display","none");

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
					
				$(".MDpolygonID").each(function(e) {
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
						mdPolyContext.strokeStyle = "#00ffff";
						mdPolyContext.beginPath();	
						mdPolyContext.moveTo(x1, y1);mdPolyContext.lineTo(x2, y2);mdPolyContext.stroke();
						mdPolyContext.moveTo(x2, y2);mdPolyContext.lineTo(x3, y3);mdPolyContext.stroke();
						mdPolyContext.moveTo(x3, y3);mdPolyContext.lineTo(x4, y4);mdPolyContext.stroke();
						mdPolyContext.moveTo(x4, y4);mdPolyContext.lineTo(x1, y1);mdPolyContext.stroke();
						mdPolyContext.closePath();
						EventSetup.MD.deleteClass=$(this).attr("id");
						var input = confirm(deleteLang);
						if(input) {
							$("#MDPolyDraw div").remove("#"+EventSetup.MD.deleteClass);
							EventSetup.MD.updatePolygon();
							return false;
						}else {
							EventSetup.MD.updatePolygon();
						};
						
						return false;
					}
				});
				
				return false;
			});
		}
			
	},
	reDrawPolygon:function(isDetect){

		mdPolyObj = document.getElementById("MDPoly");
		if (G_vmlCanvasManager != undefined) { // ie IE
			G_vmlCanvasManager.initElement(mdPolyObj);
		}
		mdPolyContext = mdPolyObj.getContext("2d");
		mdPolyContext.lineWidth = 2;
		mdPolyContext.clearRect(0,0,mdPolyObj.width,mdPolyObj.height);

		mdPolyTempObj = document.getElementById("MDPolyTemp");
		if (G_vmlCanvasManager != undefined) { // ie IE
			G_vmlCanvasManager.initElement(mdPolyTempObj);
		}
		mdPolyTempContext = mdPolyTempObj.getContext("2d");
		mdPolyTempContext.lineWidth = 2;

		mdPolyTempContext.clearRect(0,0,mdPolyTempObj.width,mdPolyTempObj.height);

		$(".MDpolygonID").each(function(e) {
			
			var cordinates=$(this).html().split(",");

			var x1=parseInt(cordinates[0]);
			var y1=parseInt(cordinates[1]);
			var x2=parseInt(cordinates[2]);
			var y2=parseInt(cordinates[3]);
			var x3=parseInt(cordinates[4]);
			var y3=parseInt(cordinates[5]);
			var x4=parseInt(cordinates[6]);
			var y4=parseInt(cordinates[7]);

			if(EventSetup.MD.mdDrawType == EventSetup.TYPE_RECT){
				if(EventSetup.IS_PTZ_SUPPORT){
					mdPolyContext.strokeStyle = "#173D64";	
				}else{
					if(isDetect){
						mdPolyContext.strokeStyle = "#FF1800";
					}else{
						mdPolyContext.strokeStyle = "#009CFF";
					}					
				}
				
				mdPolyContext.globalAlpha="1";
				mdPolyContext.strokeRect(x1,y1,x2-x1,y2-y1);
				if(EventSetup.IS_PTZ_SUPPORT){
					mdPolyContext.fillStyle = "#173D64";
				}else{
					if(isDetect){
						mdPolyContext.fillStyle = "#FF1800";
					}else{
						mdPolyContext.fillStyle = "#009CFF";
					}
				}
				mdPolyContext.globalAlpha="0.5";
				mdPolyContext.fillRect(x1,y1,x2-x1,y2-y1);
				mdPolyContext.closePath();
			}
			else{
				var polygonPoints = [[x1,y1],[x2,y2],[x3,y3],[x4,y4]];
				if(isDetect){
					mdPolyContext.strokeStyle = "#FF1800";
				}else{
					mdPolyContext.strokeStyle = "#009CFF";
				}
				mdPolyContext.globalAlpha="1";
				mdPolyContext.beginPath();	
				mdPolyContext.moveTo(x1, y1);mdPolyContext.lineTo(x2, y2);mdPolyContext.stroke();
				mdPolyContext.moveTo(x2, y2);mdPolyContext.lineTo(x3, y3);mdPolyContext.stroke();
				mdPolyContext.moveTo(x3, y3);mdPolyContext.lineTo(x4, y4);mdPolyContext.stroke();
				mdPolyContext.moveTo(x4, y4);mdPolyContext.lineTo(x1, y1);mdPolyContext.stroke();
				mdPolyContext.closePath();
				mdPolyContext.globalAlpha="0.35";
				if(isDetect){
					mdPolyContext.fillPolygon(polygonPoints, '#FF1800','#FF1800');
				}else{
					mdPolyContext.fillPolygon(polygonPoints, '#009CFF','#009CFF');
				}
			}
		});
	},
	updatePolygon:function(){
		var isDetect = $('.event_detection_mode_on').is(':checked');

		EventSetup.MD.reDrawPolygon(isDetect);
	},
	
	getMDPolygon:function(xmlData){		
		//var xml_data=$.parseXML(xmlData);
		if(EventSetup.MD.mdDrawType == EventSetup.TYPE_RECT){
			xmlData.find("ObjectArea").each(function()
			{
				var x1=0,y1=0,x2=0,y2=0;
				x1=$(this).find("Point0 X").text()/(EventSetup.RATIO_W);
				y1=$(this).find("Point0 Y").text()/(EventSetup.RATIO_H);

				x2=$(this).find("Point1 X").text()/(EventSetup.RATIO_W);
				y2=$(this).find("Point1 Y").text()/(EventSetup.RATIO_H);

				if(EventSetup.FLIP_MIRROR == 1) {
					y1 = EventSetup.VIEWER_H -y1;
					y2 = EventSetup.VIEWER_H -y2;
				}else if(EventSetup.FLIP_MIRROR == 2) {
					x1=EventSetup.VIEWER_W - x1;
					x2=EventSetup.VIEWER_W - x2;
				}else if(EventSetup.FLIP_MIRROR == 3) { 
					x1=EventSetup.VIEWER_W - x1;
					x2=EventSetup.VIEWER_W - x2;
					y1 = EventSetup.VIEWER_H -y1;
					y2 = EventSetup.VIEWER_H -y2;
				}

				if (x2 < x1)
				{
					var temp;
					temp = x1;
					x1 = x2;
					x2 = temp;
				}
				if (y2 < y1)
				{
					var temp;
					temp = y1;
					y1 = y2;
					y2 = temp;
				}

				$("#MDPolyDraw").append("<div style='display:none;' class='MDpolygonID' id='"+"MDpolygon"+EventSetup.MD.polyCount+"'>"+x1+","+y1+","+x2+","+y2+","+0+","+0+","+0+","+0+"</div>");
				EventSetup.MD.polyCount++;
			});
		}
		else{
			xmlData.find("ObjectArea").each(function()
			{
				var x1=0,y1=0,x2=0,y2=0,x3=0,y3=0,x4=0,y4=0;
			
				x1=$(this).find("Point0 X").text()/(EventSetup.RATIO_W);
				y1=$(this).find("Point0 Y").text()/(EventSetup.RATIO_H);
			
				x2=$(this).find("Point1 X").text()/(EventSetup.RATIO_W);
				y2=$(this).find("Point1 Y").text()/(EventSetup.RATIO_H);
			
				x3=$(this).find("Point2 X").text()/(EventSetup.RATIO_W);
				y3=$(this).find("Point2 Y").text()/(EventSetup.RATIO_H);
			
				x4=$(this).find("Point3 X").text()/(EventSetup.RATIO_W);
				y4=$(this).find("Point3 Y").text()/(EventSetup.RATIO_H);

				var xpos = [x1,x2,x3,x4];
				var ypos = [y1,y2,y3,y4];

				if(EventSetup.FLIP_MIRROR == 1) {
					for(var j = 0; j < 4; j++){
						ypos[j]=EventSetup.VIEWER_H - ypos[j];
					}
				}
				else if(EventSetup.FLIP_MIRROR == 2) {
					for(var j = 0; j < 4; j++){
						xpos[j]=EventSetup.VIEWER_W - xpos[j];
					}
				}
				else if(EventSetup.FLIP_MIRROR == 3) { 
					for(var j = 0; j < 4; j++){
						ypos[j]=EventSetup.VIEWER_H - ypos[j];
					}	
					for(var j = 0; j < 4; j++){
						xpos[j]=EventSetup.VIEWER_W - xpos[j];
					}
				}
				
				var polygonPoints = [[x1,y1],[x2,y2],[x3,y3],[x4,y4]];
				
				$("#MDPolyDraw").append("<div style='display:none;' class='MDpolygonID' id='"+"MDpolygon"+EventSetup.MD.polyCount+"'>"+xpos[0]+","+ypos[0]+","+xpos[1]+","+ypos[1]+","+xpos[2]+","+ypos[2]+","+xpos[3]+","+ypos[3]+"</div>");
				EventSetup.MD.polyCount++;
			});
		}	
	}
};

EventSetup.VA={
			xPts:[[0,0,0,0],[0,0,0,0],[0,0,0,0]],
			yPts:[[0,0,0,0],[0,0,0,0],[0,0,0,0]],
			deleteClass:'',
			MAX_PASSING_COUNT:0,
			MAX_ENTERING_COUNT:0,
			MAX_APPEARING_COUNT:0,
			enteringCount:0,
			appearingCount:0,
			passingCount:0,
			appearDrawType: EventSetup.TYPE_RECT,
			init:function(support_ptz, maxCount)
			{
				EventSetup.IS_PTZ_SUPPORT = support_ptz;
				EventSetup.VA.MAX_ENTERING_COUNT = maxCount;

				EventSetup.VA.enteringCount = 0;
				
				$("#polyDraw canvas").remove();
				$("#polyDraw span").remove();
				$("#polyDraw").append("<canvas id=\"myCanvas\" width=\""+EventSetup.VIEWER_W+"\" height=\""+EventSetup.VIEWER_H+"\"></canvas>");
				if(BrowserDetect.browser == "Explorer" && getIEVersion() <= 8){
					$("#polyDraw").append("<span class=\"drawArea-position\" style=\"left:0px;background:#000;opacity:0;filter:alpha(opacity=0);\"></span>");
				}
				$("#polyDraw").append("<canvas id=\"imgTemp\" width=\""+EventSetup.VIEWER_W+"\" height=\""+EventSetup.VIEWER_H+"\" style=\"position: absolute;top:0px;left:0px;z-index:1000;\" ></canvas>");

				///////////////////////////////////////////
					
				var Fx, Fy;
				var Ax=0, Ay=0, Bx=0, By=0, index=1;
				var polyCreate=false;
				var arrayCount=0;
				var x1=0,y1=0,x2=0,y2=0,x3=0,y3=0,x4=0,y4=0;
										
				$("#imgTemp").click(function(e) {
					if(EventSetup.IS_PTZ_SUPPORT){
						var vaCount = EventSetup.VA.enteringCount + EventSetup.VA.passingCount;
						if(vaCount == EventSetup.VA.MAX_ENTERING_COUNT) return;
					}else{
						var vaCount = EventSetup.VA.enteringCount + EventSetup.VA.appearingCount;
						if(vaCount == EventSetup.VA.MAX_ENTERING_COUNT) return;
					}
					
					vaPolyContext.globalCompositeOperation="source-over";
						
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
						isDrawDragging=true;
						x1 = xVal,y1= yVal;
						Ax=xVal, Ay=yVal;// getting mouse move action
						$("#DisableIVSelectLayer").css("display","block");
						 // red
					}
					else if(index==2){
						x2 = xVal,y2= yVal;
						Ax=xVal, Ay=yVal;// getting mouse move action
						
						vaPolyContext.beginPath();
						vaPolyContext.moveTo(x1, y1);
						vaPolyContext.lineTo(x2, y2);
						vaPolyContext.stroke();
						vaPolyContext.closePath();	
					}
					else if(index==3){
						x3 = xVal,y3= yVal;
						Ax=xVal, Ay=yVal;// getting mouse move action
						
						vaPolyContext.beginPath();
						vaPolyContext.moveTo(x2, y2);
						vaPolyContext.lineTo(x3, y3);
						vaPolyContext.stroke();
						vaPolyContext.closePath();
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
						vaPolyContext.beginPath();
						vaPolyContext.moveTo(x3, y3);
						vaPolyContext.lineTo(x4, y4);
						vaPolyContext.stroke();
						vaPolyContext.moveTo(x4, y4);
						vaPolyContext.lineTo(x1, y1);
						vaPolyContext.stroke();
						vaPolyContext.closePath(); 
						vaPolyContext.fillPolygon(polygonPoints, 'gray','green');
						$("#polyDraw").append("<div style='display:none;' class='polygonID' id='"+"polygon"+EventSetup.VA.enteringCount+"'>"+x1+","+y1+","+x2+","+y2+","+x3+","+y3+","+x4+","+y4+"</div>");

						vaPolyTempContext.clearRect(0, 0, vaPolyTempObj.width, vaPolyTempObj.height);
						
						EventSetup.VA.deleteClass="polygon"+EventSetup.VA.enteringCount;						
						
						isDrawDragging=false;
						EventSetup.VA.enteringCount++;
						polyCreate=true;
						EventSetup.VA.reDrawVaPolygon();
						
						$( "#poly-dialog" ).dialog("open"); 

						$(".ui-dialog #poly-dialog input").prop("checked", false);
						
						index=1	;
						$("#DisableIVSelectLayer").css("display","none");
						return;
					}
					
					index++;				
				});
											
				$("#imgTemp").mousemove(function(e) {
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
				
					if (isDrawDragging) {
						vaPolyTempContext.clearRect(0, 0, vaPolyTempObj.width, vaPolyTempObj.height);
						vaPolyTempContext.beginPath();
						vaPolyTempContext.moveTo(Ax, Ay);
						vaPolyTempContext.lineTo(xVal, yVal);
						vaPolyTempContext.strokeStyle="yellow";
						vaPolyTempContext.stroke();
						vaPolyTempContext.closePath();
					}
				});
					/////////////////////////////////////////////////////////////////////////////////////
				
				$("#imgTemp").on("contextmenu",function(e){
					if(isDrawDragging){
						isDrawDragging=false;
						index = 1;
						EventSetup.VA.reDrawVaPolygon();
						$("#DisableIVSelectLayer").css("display","none");
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
					
						$(".polygonID").each(function(e) {
							
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
								EventSetup.VA.deleteClass=$(this).attr("id");
								$('.ui-dialog input').prop('checked', false);	
								if($(this).attr("alt")=="AreaEnter"){ $(".ui-dialog #poly-dialog input#polyEntering").prop('checked', true); }
								if($(this).attr("alt")=="AreaExit"){ $(".ui-dialog #poly-dialog input#polyExiting").prop('checked', true); }
								if($(this).attr("alt")=="AreaEnter,AreaExit"){
									$(".ui-dialog #poly-dialog input#polyEntering").prop('checked', true);
									$(".ui-dialog #poly-dialog input#polyExiting").prop('checked', true);
								}
								$( "#poly-dialog" ).dialog("open");
								
								return;
							};
						});
					
					
					return false;
				});
					
				function deletePoly(){
					$("#polyDraw div").remove("#"+EventSetup.VA.deleteClass);
					EventSetup.VA.enteringCount--;


					if (vaPolyContext != null) {
						vaPolyContext.clearRect(0, 0, vaPolyObj.width, vaPolyObj.height);
					}

					var index = 0;
					$(".polygonID").each(function(e) {
						
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
						
						if (vaPolyContext != null) {
							vaPolyContext.beginPath();	
							vaPolyContext.moveTo(x1, y1);vaPolyContext.lineTo(x2, y2);vaPolyContext.stroke();
							vaPolyContext.moveTo(x2, y2);vaPolyContext.lineTo(x3, y3);vaPolyContext.stroke();
							vaPolyContext.moveTo(x3, y3);vaPolyContext.lineTo(x4, y4);vaPolyContext.stroke();
							vaPolyContext.moveTo(x4, y4);vaPolyContext.lineTo(x1, y1);vaPolyContext.stroke();
							vaPolyContext.closePath();
							vaPolyContext.fillPolygon(polygonPoints, 'gray','green');
						}
						$(this).attr("id","polygon"+index);
						index++;						
					});
				}
						
				$("#poly-dialog").dialog({
					autoOpen: false,
					modal: true,
				    draggable: false,
					position:{
						my: 'center',
						of: $("#pluginArea")
					},
				    title: titleLang[1],
					dialogClass: 'polygon-dialog-class',
					open:function() { 
						if($('#polyExiting').is(':checked') || $('#polyEntering').is(':checked'))
						{
							$("#button-ok-polyDail").button("enable");
						}
						else{
							$("#button-ok-polyDail").button("disable");
						}
					},
					beforeClose: function( event, ui ) { 
						if (polyCreate) {  
							deletePoly();
							polyCreate=false;
						}						
					},
					close: function(event, ui){
						$("#poly-dialog input[type=checkbox]").prop('checked',false);
					},	
					buttons: [
								{
									id: "button-ok-polyDail",
									text: okLang,
									click: function() {   
									
										var PolySpan="#"+EventSetup.VA.deleteClass;
										if ($('#polyEntering').is(':checked')) {
												$(PolySpan).attr("alt","AreaEnter");
										}
										if($('#polyExiting').is(':checked'))
										{
											$(PolySpan).attr("alt","AreaExit");
										}
										if($('#polyExiting').is(':checked') && $('#polyEntering').is(':checked'))
										{
											$(PolySpan).attr("alt","AreaEnter,AreaExit");
										}
										
										polyCreate=false;
									   $(this).dialog("close");
									}
								  
								},
								{
									id: "button-cancel-polyDail",
									text: cancelLang,
									click: function() {
									  	$("#poly-dialog").dialog("close");
									}
								},
								{
									id: "button-delete-polyDail",
									text: deleteLang,
									click:function(){
										polyCreate=true;
										$(this).dialog( "close" );
									}
								}
							]
				});
						
				
						
					$("#polyExiting, #polyEntering").on( "click", function() { 
						if($('#polyExiting').is(':checked') || $('#polyEntering').is(':checked'))
						{
							$("#button-ok-polyDail").button("enable");
						}
						else{
							$("#button-ok-polyDail").button("disable");
						}
					});
						
			},
			getPolygon:function(xmlData){
				var once=true;
				xmlData.find("AreaObject").each(function()
				{
					var thisObject=$(this);
					var x1=0, y1=0, x2=0, y2=0, x3=0, y3=0,x4=0,y4=0;
					var firstTime=true, count=1;

					if (typeof analyticsType != 'undefined') analyticsType = 1;
					
					var objectType=''; var ClassName='polygonID';
					if ($(this).find("AreaEnter").text()==1) {
						objectType="AreaEnter";
					}
					if ($(this).find("AreaExit").text()==1) {
						objectType="AreaExit";
					}
					if(($(this).find("AreaExit").text()==1) && ($(this).find("AreaEnter").text()==1))
					{
						objectType="AreaEnter,AreaExit";
						
					}
					/*
					if(($(this).find("AreaAppear").text()==1) && ($(this).find("AreaDisappear").text()==1))
					{
						objectType="AreaAppearDisappear";
						c2=c33;
						ClassName="appDiss";
						if (typeof analyticsType != 'undefined') analyticsType = 2;
					}
					*/
					
					if(!($(this).find("AreaAppear").text()==1))
					{
						$(this).find("Point").each(function()
						{
							if(count==1)
							{
								x1=parseInt($(this).find("X").text()/(EventSetup.RATIO_W));
								y1=parseInt($(this).find("Y").text()/(EventSetup.RATIO_H));
							}
							if(count==2)
							{
								x2=parseInt($(this).find("X").text()/(EventSetup.RATIO_W));
								y2=parseInt($(this).find("Y").text()/(EventSetup.RATIO_H));
								
							}
							if(count==3)
							{
								x3=parseInt($(this).find("X").text()/(EventSetup.RATIO_W));
								y3=parseInt($(this).find("Y").text()/(EventSetup.RATIO_H));
							}
							if(count==4)
							{
								x4=parseInt($(this).find("X").text()/(EventSetup.RATIO_W));
								y4=parseInt($(this).find("Y").text()/(EventSetup.RATIO_H));
								isDrawDragging=false;
						//		var polygonPoints = [[x1,y1],[x2,y2],[x3,y3],[x4,y4]];
						//		vaPolyContext.fillPolygon(polygonPoints, 'gray','green');

								var xpos = [x1,x2,x3,x4];
								var ypos = [y1,y2,y3,y4];
								
								if(!EventSetup.IS_PTZ_SUPPORT){
									if(EventSetup.FLIP_MIRROR == 1) {
										for(var j = 0; j < 4; j++){
											ypos[j]=EventSetup.VIEWER_H - ypos[j];
										}
									}
									else if(EventSetup.FLIP_MIRROR == 2) {
										for(var j = 0; j < 4; j++){
											xpos[j]=EventSetup.VIEWER_W - xpos[j];
										}
									}
									else if(EventSetup.FLIP_MIRROR == 3) { 
										for(var j = 0; j < 4; j++){
											ypos[j]=EventSetup.VIEWER_H - ypos[j];
										}	
										for(var j = 0; j < 4; j++){
											xpos[j]=EventSetup.VIEWER_W - xpos[j];
										}
									}
								}
						
								$("#polyDraw").append("<div style='display:none;' alt='"+objectType+"' class='"+ClassName+"' id='"+"polygon"+EventSetup.VA.enteringCount+"'>"+xpos[0]+","+ypos[0]+","+xpos[1]+","+ypos[1]+","+xpos[2]+","+ypos[2]+","+xpos[3]+","+ypos[3]+"</div>");
					
								count=1;
								
								EventSetup.VA.enteringCount++;
							}
							
							
							count++;
						});
					}
				});
				xmlData.find("FullScreen").each(function()
				{
					if ($(this).find("FullAppear").text()==1) {
						$('#app_disapp_entire').prop('checked',true);
					}
					else{
						$('#app_disapp_entire').prop('checked',false);
					}
				});
			},
			reDrawVaPolygon:function(){
				vaPolyObj = document.getElementById("myCanvas");
				if (G_vmlCanvasManager != undefined) { // ie IE
					G_vmlCanvasManager.initElement(vaPolyObj);
				}
				vaPolyContext = vaPolyObj.getContext("2d");
				vaPolyContext.lineWidth = 2;
				vaPolyContext.strokeStyle = "green";
				vaPolyContext.fillStyle = "gray";
				vaPolyContext.globalAlpha="1"; 
				
				vaPolyTempObj = document.getElementById("imgTemp");
				if (G_vmlCanvasManager != undefined) { // ie IE
					G_vmlCanvasManager.initElement(vaPolyTempObj);
				}
				vaPolyTempContext = vaPolyTempObj.getContext("2d");
				vaPolyTempContext.lineWidth = 2;
				vaPolyTempContext.strokeStyle = "yellow";

				vaPolyContext.clearRect(0,0,vaPolyObj.width,vaPolyObj.height);
				vaPolyTempContext.clearRect(0,0,vaPolyTempObj.width,vaPolyTempObj.height);

				var index = 0;
				$(".polygonID").each(function(e) {
					
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
					vaPolyContext.beginPath();	
					vaPolyContext.moveTo(x1, y1);vaPolyContext.lineTo(x2, y2);vaPolyContext.stroke();
					vaPolyContext.moveTo(x2, y2);vaPolyContext.lineTo(x3, y3);vaPolyContext.stroke();
					vaPolyContext.moveTo(x3, y3);vaPolyContext.lineTo(x4, y4);vaPolyContext.stroke();
					vaPolyContext.moveTo(x4, y4);vaPolyContext.lineTo(x1, y1);vaPolyContext.stroke();
					vaPolyContext.closePath();
					vaPolyContext.globalAlpha="0.5";
					vaPolyContext.fillPolygon(polygonPoints, 'gray','green');
					
					$(this).attr("id","polygon"+index);
					index++;					
				});
			},			
			initRectangle:function(drawType, maxCount){
				EventSetup.VA.appearDrawType = drawType;
				EventSetup.VA.MAX_APPEARING_COUNT = maxCount;
				
				EventSetup.VA.appearingCount = 0;
				
				$("#rectangleDraw canvas").remove();
				$("#rectangleDraw").append("<canvas id=\"myCanvasRect\" width=\""+EventSetup.VIEWER_W+"\" height=\""+EventSetup.VIEWER_H+"\"></canvas>");
				if(BrowserDetect.browser == "Explorer" && getIEVersion() <= 8){
					$("#rectangleDraw").append("<span class=\"drawArea-position\" style=\"left:0px;background:#000;opacity:0;filter:alpha(opacity=0);\"></span>");
				}				
				$("#rectangleDraw").append("<canvas id=\"myCanvasRectTmp\" width=\""+EventSetup.VIEWER_W+"\" height=\""+EventSetup.VIEWER_H+"\" style=\"position: absolute;top:0px;left:0px;z-index:1000;\" ></canvas>");
				
				var Fx, Fy;
				var Ax=0, Ay=0, Bx=0, By=0, index=1;
				var once=false;
				var arrayCount=0;
				var x1=0,y1=0,x2=0,y2=0,x3=0,y3=0,x4=0,y4=0;
				var isCreate=false;

				if(EventSetup.VA.appearDrawType == EventSetup.TYPE_RECT){
					var rect = {};

					$("#myCanvasRectTmp").mousedown(function(e) {
						if(EventSetup.IS_PTZ_SUPPORT){
							if(EventSetup.VA.appearingCount >= EventSetup.VA.MAX_APPEARING_COUNT) return;								
						}else{
							var vaCount = EventSetup.VA.appearingCount + EventSetup.VA.enteringCount;
							if(vaCount == EventSetup.VA.MAX_APPEARING_COUNT) return;
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
						
						rect.startX = xVal;
						rect.startY = yVal;
						firstDrawClick = true;
						isDrawDragging = false;
						
					});
				
					$("#myCanvasRectTmp").mousemove(function(e) {
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
							rect.w = xVal - rect.startX;
						    rect.h = yVal - rect.startY;
							rect.endX = xVal;
							rect.endY = yVal;
							
							vaAreaRectTempContext.clearRect(0,0,vaAreaRectTempObj.width,vaAreaRectTempObj.height);
							vaAreaRectTempContext.fillStyle = "gray";
							vaAreaRectTempContext.globalAlpha="0.5"; 
							vaAreaRectTempContext.fillRect(rect.startX,rect.startY,rect.w,rect.h);
							
							vaAreaRectTempContext.strokeStyle = "green";
							vaAreaRectTempContext.lineWidth = 2;
							vaAreaRectTempContext.globalAlpha="1";
							vaAreaRectTempContext.strokeRect(rect.startX,rect.startY,rect.w,rect.h);
							isDrawDragging = true;
						}
						
					});
		 
					$("#myCanvasRectTmp").mouseup(function(e) {
						if(EventSetup.IS_PTZ_SUPPORT){
							if(EventSetup.VA.appearingCount > EventSetup.VA.MAX_APPEARING_COUNT) return;								
						}else{
							var vaCount = EventSetup.VA.appearingCount + EventSetup.VA.enteringCount;
							if(vaCount == EventSetup.VA.MAX_APPEARING_COUNT) return;
						}
						
						firstDrawClick = false;
						if(isDrawDragging){
							if(rect.startX <= rect.endX){
								x1 = rect.startX;
								x2 = rect.endX;
							}
							else{
								x2 = rect.startX;
								x1 = rect.endX;
							}
							if(rect.startY <= rect.endY){
								y1 = rect.startY;
								y2 = rect.endY;
							}
							else{
								y2 = rect.startY;
								y1 = rect.endY;
							}
							
							if(x1 < 0) x1 = 0;
							if(x2 < 0) x2 = 0;
							if(y1 < 0) y1 = 0;
							if(y2 < 0) y2 = 0;

							var width = x2 - x1;
							var hegiht = y2 - y1;

							if(parseInt(width*(EventSetup.RATIO_W)) < 100 || parseInt(hegiht*(EventSetup.RATIO_H)) < 100){
								vaAreaRectTempContext.clearRect(0, 0, vaAreaRectObj.width, vaAreaRectObj.height);
								return;
							}							
							
							$("#rectangleDraw").append("<div style='display:none;' class='appDiss' id='"+"rect"+EventSetup.VA.appearingCount+"'>"+x1+","+y1+","+x2+","+y2+"</div>");
							
							EventSetup.VA.deleteClass="rect"+EventSetup.VA.appearingCount;
							
							EventSetup.VA.appearingCount++;
							EventSetup.VA.reDrawRectangle();

							isCreate=true;


							$( "#poly-dialog-appear" ).dialog("open");
							isDrawDragging = false;
						}
					});

					$("#myCanvasRectTmp").on("contextmenu",function(e){
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
						
							$(".appDiss").each(function(e) {
								
								var cordinates=$(this).html().split(",");
								var x1=parseInt(cordinates[0]);
								var y1=parseInt(cordinates[1]);
								var x2=parseInt(cordinates[2]);
								var y2=parseInt(cordinates[3]);
							
								if(x1 <= xVal && xVal <= x2 && y1 <= yVal && yVal <= y2){
									EventSetup.VA.deleteClass=$(this).attr("id");

									$('.ui-dialog input').prop('checked', false);								

									if($(this).attr("alt")=="AreaAppearDisappear"){ $(".ui-dialog #poly-dialog-appear input#app_disapp").prop('checked', true); }
									$( "#poly-dialog-appear" ).dialog("open");
									
									return;
								}	
							});
						
						
						return false;
					});
				}else{
				
					$("#myCanvasRectTmp").click(function(e) {
						if(EventSetup.IS_PTZ_SUPPORT){
							if(EventSetup.VA.appearingCount > EventSetup.VA.MAX_APPEARING_COUNT) return;								
						}else{
							var vaCount = EventSetup.VA.appearingCount + EventSetup.VA.enteringCount;
							if(vaCount == EventSetup.VA.MAX_APPEARING_COUNT) return;
						}

						vaAreaRectContext.globalCompositeOperation="source-over";
							
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
							isDrawDragging=true;
							x1 = xVal,y1= yVal;
							Ax=xVal, Ay=yVal;// getting mouse move action
							$("#DisableIVSelectLayer").css("display","block");
							 // red
						}
						else if(index==2){
							x2 = xVal,y2= yVal;
							Ax=xVal, Ay=yVal;// getting mouse move action
							
							vaAreaRectContext.beginPath();
							vaAreaRectContext.moveTo(x1, y1);
							vaAreaRectContext.lineTo(x2, y2);
							vaAreaRectContext.stroke();
							vaAreaRectContext.closePath();	
						}
						else if(index==3){
							x3 = xVal,y3= yVal;
							Ax=xVal, Ay=yVal;// getting mouse move action

							vaAreaRectContext.beginPath();
							vaAreaRectContext.moveTo(x2, y2);
							vaAreaRectContext.lineTo(x3, y3);
							vaAreaRectContext.stroke();
							vaAreaRectContext.closePath();
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
							vaAreaRectContext.beginPath();
							vaAreaRectContext.moveTo(x3, y3);
							vaAreaRectContext.lineTo(x4, y4);
							vaAreaRectContext.stroke();
							vaAreaRectContext.moveTo(x4, y4);
							vaAreaRectContext.lineTo(x1, y1);
							vaAreaRectContext.stroke();
							vaAreaRectContext.closePath(); 
							vaAreaRectContext.fillPolygon(polygonPoints, 'gray','green');
							$("#rectangleDraw").append("<div style='display:none;' class='appDiss' id='"+"rect"+EventSetup.VA.appearingCount+"'>"+x1+","+y1+","+x2+","+y2+","+x3+","+y3+","+x4+","+y4+"</div>");

							vaAreaRectTempContext.clearRect(0, 0, vaAreaRectTempObj.width, vaAreaRectTempObj.height);
							
							EventSetup.VA.deleteClass="rect"+EventSetup.VA.appearingCount;						
							
							isDrawDragging=false;
							EventSetup.VA.appearingCount++;
							EventSetup.VA.reDrawRectangle();
							
							isCreate=true;

							$(".ui-dialog #poly-dialog-appear input").prop("checked", false);
							$( "#poly-dialog-appear" ).dialog("open"); 
							
							index=1	;
							$("#DisableIVSelectLayer").css("display","none");
							return;
						}
						
						index++;				
					});
												
					$("#myCanvasRectTmp").mousemove(function(e) {
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
					
						if (isDrawDragging) {
							vaAreaRectTempContext.clearRect(0, 0, vaAreaRectTempObj.width, vaAreaRectTempObj.height);
							vaAreaRectTempContext.beginPath();
							vaAreaRectTempContext.moveTo(Ax, Ay);
							vaAreaRectTempContext.lineTo(xVal, yVal);
							vaAreaRectTempContext.strokeStyle="yellow";
							vaAreaRectTempContext.stroke();
							vaAreaRectTempContext.closePath();
						}
					});
						/////////////////////////////////////////////////////////////////////////////////////
					
					$("#myCanvasRectTmp").on("contextmenu",function(e){
						if(isDrawDragging){
							isDrawDragging=false;
							index = 1;
							EventSetup.VA.reDrawRectangle();							
							$("#DisableIVSelectLayer").css("display","none");
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
						
							$(".appDiss").each(function(e) {
								
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
									EventSetup.VA.deleteClass=$(this).attr("id");
									/*
									$('.ui-dialog input').prop('checked', false);	
									if($(this).attr("alt")=="AreaEnter"){ $(".ui-dialog #poly-dialog input#polyEntering").prop('checked', true); }
									if($(this).attr("alt")=="AreaExit"){ $(".ui-dialog #poly-dialog input#polyExiting").prop('checked', true); }
									if($(this).attr("alt")=="AreaEnter,AreaExit"){
										$(".ui-dialog #poly-dialog input#polyEntering").prop('checked', true);
										$(".ui-dialog #poly-dialog input#polyExiting").prop('checked', true);
									}
									*/
									$("#poly-dialog-appear input[type=checkbox]").prop('checked',true);
									$("#poly-dialog-appear").dialog("open");
									
									return;
								};
							});
						
						
						return false;
					});						
				}
				function deleteAppearingRect(){
					$("#rectangleDraw div").remove("#"+EventSetup.VA.deleteClass);
					EventSetup.VA.appearingCount--;
					
					vaAreaRectContext.clearRect(0, 0, vaAreaRectObj.width, vaAreaRectObj.height);
					vaAreaRectTempContext.clearRect(0, 0, vaAreaRectObj.width, vaAreaRectObj.height);

					var index = 0;
					$(".appDiss").each(function(e) {
						var cordinates=$(this).html().split(",");
						var x1=parseInt(cordinates[0]);
						var y1=parseInt(cordinates[1]);
						var x2=parseInt(cordinates[2]);
						var y2=parseInt(cordinates[3]);
						
						vaAreaRectContext.clearRect(0,0,vaAreaRectTempObj.width,vaAreaRectTempObj.height);
						vaAreaRectContext.fillStyle = "gray";
						vaAreaRectContext.globalAlpha="0.5"; 
						vaAreaRectContext.fillRect(x1,y1,x2-x1,y2-y1);
						
						vaAreaRectContext.strokeStyle = "green";
						vaAreaRectContext.lineWidth = 2;
						vaAreaRectContext.globalAlpha="1";
						vaAreaRectContext.strokeRect(x1,y1,x2-x1,y2-y1);
						$(this).attr("id","rect"+index);
						index++;
					});
				}
				
				function deleteAppearingPoly(){
					$("#rectangleDraw div").remove("#"+EventSetup.VA.deleteClass);
					EventSetup.VA.appearingCount--;

					if (vaAreaRectContext != null) {
						vaAreaRectContext.clearRect(0, 0, vaAreaRectObj.width, vaAreaRectObj.height);
					}
					
					var index = 0;
					$(".appDiss").each(function(e) {
						
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
						
						if (vaAreaRectContext != null) {
							vaAreaRectContext.beginPath();	
							vaAreaRectContext.moveTo(x1, y1);vaAreaRectContext.lineTo(x2, y2);vaAreaRectContext.stroke();
							vaAreaRectContext.moveTo(x2, y2);vaAreaRectContext.lineTo(x3, y3);vaAreaRectContext.stroke();
							vaAreaRectContext.moveTo(x3, y3);vaAreaRectContext.lineTo(x4, y4);vaAreaRectContext.stroke();
							vaAreaRectContext.moveTo(x4, y4);vaAreaRectContext.lineTo(x1, y1);vaAreaRectContext.stroke();
							vaAreaRectContext.closePath();
							vaAreaRectContext.fillPolygon(polygonPoints, 'gray','green');
						}
						$(this).attr("id","rect"+index);
						index++;
					});
				}
				$("#poly-dialog-appear").dialog({
					autoOpen: false,
					modal: true,
					dialogClass: 'polygon-dialog-class',
					draggable: false,
					title: titleLang[1],
					position:{
						my: 'center',
						of: $("#pluginArea")
					},
					open:function(){
						if($('#app_disapp').is(':checked')) 
							$("#button-ok-appear").button("enable");
						else 
							$("#button-ok-appear").button("disable");
					},
					beforeClose: function( event, ui ) {
						if (isCreate) {
							if(EventSetup.VA.appearDrawType == EventSetup.TYPE_RECT){
								deleteAppearingRect();
							}else{
								deleteAppearingPoly();
							}
							isCreate=false;
						}						
					},
					close: function(event, ui){
						$("#poly-dialog-appear input[type=checkbox]").prop('checked',false);
					},
					buttons: 
						[
							{
								id: "button-ok-appear",
								text: okLang,
								disabled:false,
								click: function() {
									var PolySpan="#"+EventSetup.VA.deleteClass;					
									if($('#app_disapp').is(':checked'))
									{
										$(PolySpan).attr("alt","AreaAppearDisappear")
									}
									isCreate=false;
									$(this).dialog( "close" );
								}
							},
							{
								id: "button-cancel-appear",
								text: cancelLang,
								click: function() {
									$(this).dialog("close");
								}
							},
							{
								id: "button-delete-appear",
								text: deleteLang,
								click: function() {
									isCreate=true;
									$(this).dialog( "close" );
								}
							}
								
						]
				});	

				$("#app_disapp").on( "click", function() { 
					if($('#app_disapp').is(':checked'))
					{
						$("#button-ok-appear").button("enable");
					}
					else{
						$("#button-ok-appear").button("disable");
					}
				});
				
				var fullScreenAppear = false;
				if(EventSetup.IS_PTZ_SUPPORT == false){
				$("#poly-dialog-entireArea").dialog({
					autoOpen: false,
					modal: true,
					dialogClass: 'polygon-dialog-class',
					draggable: false,
					title: titleLang[2],
					position:{
						my: 'center',
						of: $("#pluginArea")
					},
					open:function(){ 
						if($(".ui-dialog #poly-dialog-entireArea input#app_disapp_entire").is(':checked')){
							$("#button-ok-entire").button("enable");
						}else{
							$("#button-ok-entire").button("disable");
						}
						$("#fullCanvas").show();
					},
					beforeClose: function( event, ui ) { 
						if(!fullScreenAppear) {
							$(".ui-dialog #poly-dialog-entireArea input#app_disapp_entire").prop("checked", false);
							$("#fullCanvas").hide(); 
						}
						
					},
					buttons: [
					
					{
						id: "button-ok-entire",
						text: okLang,
						disabled:true,
						click: function() {
							fullScreenAppear=true;
							$(this).dialog( "close" );
						}
					},
					{
						id: "button-cancel-entire",
						text: cancelLang,
						click: function() {
							$(this).dialog("close");
						}
					},
					{
						id: "button-delete-entire",
						text: deleteLang,
						click: function() {
							fullScreenAppear=false;
							$(this).dialog("close");
						}
					}
					
					]
				});	
				}
				
				$("#app_disapp_entire").on( "click", function() { 
					if($('#app_disapp_entire').is(':checked'))
					{
						$("#button-ok-entire").button("enable");
					}
					else{
						$("#button-ok-entire").button("disable");
					}
				});
				
				$("#fullScreen").on("contextmenu",function(e){
					$( "#poly-dialog-entireArea" ).dialog("open");
					return false;
				});	
			},
			
			getRectangle:function(xmlData){

				//var xml_data=$.parseXML(xmlData);
				xmlData.find("AreaObject").each(function()
				{
					if(($(this).find("AreaAppear").text()==1) && ($(this).find("AreaDisappear").text()==1))
					{
						var count = 0;
						
						var x1,y1,x2,y2,x3,y3,x4,y4;
						
						$(this).find("Point").each(function()
						{
							if(count == 0){
								x1=$(this).find("X").text()/(EventSetup.RATIO_W);
								y1=$(this).find("Y").text()/(EventSetup.RATIO_H);
							}else if(count == 1){
								x2=$(this).find("X").text()/(EventSetup.RATIO_W);
								y2=$(this).find("Y").text()/(EventSetup.RATIO_H);
							}else if(count == 2){
								x3=$(this).find("X").text()/(EventSetup.RATIO_W);
								y3=$(this).find("Y").text()/(EventSetup.RATIO_H);
							}else if(count == 3){
								x4=$(this).find("X").text()/(EventSetup.RATIO_W);
								y4=$(this).find("Y").text()/(EventSetup.RATIO_H);
							}
							
							count++;
						});
						if(EventSetup.VA.appearDrawType == EventSetup.TYPE_RECT){
							$("#rectangleDraw").append("<div style='display:none;' class='appDiss' alt='AreaAppearDisappear' id='"+"rect"+EventSetup.VA.appearingCount+"'>"+x1+","+y1+","+x2+","+y2+"</div>");
						}else{
							var xpos = [x1,x2,x3,x4];
							var ypos = [y1,y2,y3,y4];
							
							if(!EventSetup.IS_PTZ_SUPPORT){
								if(EventSetup.FLIP_MIRROR == 1) {
									for(var j = 0; j < 4; j++){
										ypos[j]=EventSetup.VIEWER_H - ypos[j];
									}
								}
								else if(EventSetup.FLIP_MIRROR == 2) {
									for(var j = 0; j < 4; j++){
										xpos[j]=EventSetup.VIEWER_W - xpos[j];
									}
								}
								else if(EventSetup.FLIP_MIRROR == 3) { 
									for(var j = 0; j < 4; j++){
										ypos[j]=EventSetup.VIEWER_H - ypos[j];
									}	
									for(var j = 0; j < 4; j++){
										xpos[j]=EventSetup.VIEWER_W - xpos[j];
									}
								}
							}
						
							$("#rectangleDraw").append("<div style='display:none;' class='appDiss' alt='AreaAppearDisappear' id='"+"rect"+EventSetup.VA.appearingCount+"'>"+xpos[0]+","+ypos[0]+","+xpos[1]+","+ypos[1]+","+xpos[2]+","+ypos[2]+","+xpos[3]+","+ypos[3]+"</div>");
						}
						
						EventSetup.VA.appearingCount++;
					}
				});
				
					//EventSetup.MD.DetectionArea();
			
			},
			reDrawRectangle:function(){
				vaAreaRectObj = document.getElementById("myCanvasRect");
				if (G_vmlCanvasManager != undefined) { // ie IE
					G_vmlCanvasManager.initElement(vaAreaRectObj);
				}
				vaAreaRectContext = vaAreaRectObj.getContext("2d");
				vaAreaRectContext.lineWidth = 2;
				vaAreaRectContext.strokeStyle = "green";
				vaAreaRectContext.fillStyle = "gray";
				vaAreaRectContext.globalAlpha="1"; 
				
				vaAreaRectContext.clearRect(0,0,vaAreaRectObj.width,vaAreaRectObj.height);


				vaAreaRectTempObj = document.getElementById("myCanvasRectTmp");
				if (G_vmlCanvasManager != undefined) { // ie IE
					G_vmlCanvasManager.initElement(vaAreaRectTempObj);
				}
				
				vaAreaRectTempContext = vaAreaRectTempObj.getContext("2d");
				vaAreaRectTempContext.lineWidth = 2;
				vaAreaRectTempContext.strokeStyle = "yellow";

				vaAreaRectTempContext.clearRect(0,0,vaAreaRectTempObj.width,vaAreaRectTempObj.height);

				var index = 0;
				$(".appDiss").each(function(e) {
					var cordinates=$(this).html().split(",");
					var x1=parseInt(cordinates[0]);
					var y1=parseInt(cordinates[1]);
					var x2=parseInt(cordinates[2]);
					var y2=parseInt(cordinates[3]);
					
					var x3=parseInt(cordinates[4]);
					var y3=parseInt(cordinates[5]);
					var x4=parseInt(cordinates[6]);
					var y4=parseInt(cordinates[7]);					
					if(EventSetup.VA.appearDrawType == EventSetup.TYPE_RECT){
						vaAreaRectContext.strokeStyle = 'green';
						vaAreaRectContext.globalAlpha="1";
						vaAreaRectContext.strokeRect(x1,y1,x2-x1,y2-y1);
						vaAreaRectContext.fillStyle = 'gray';
						vaAreaRectContext.globalAlpha="0.5";
						vaAreaRectContext.fillRect(x1,y1,x2-x1,y2-y1);
						vaAreaRectContext.closePath();
					}else{
						var polygonPoints = [[x1,y1],[x2,y2],[x3,y3],[x4,y4]];
						vaAreaRectContext.beginPath();	
						vaAreaRectContext.moveTo(x1, y1);vaAreaRectContext.lineTo(x2, y2);vaAreaRectContext.stroke();
						vaAreaRectContext.moveTo(x2, y2);vaAreaRectContext.lineTo(x3, y3);vaAreaRectContext.stroke();
						vaAreaRectContext.moveTo(x3, y3);vaAreaRectContext.lineTo(x4, y4);vaAreaRectContext.stroke();
						vaAreaRectContext.moveTo(x4, y4);vaAreaRectContext.lineTo(x1, y1);vaAreaRectContext.stroke();
						vaAreaRectContext.closePath();
						vaAreaRectContext.globalAlpha="0.5";
						vaAreaRectContext.fillPolygon(polygonPoints, 'gray','green');
					}
					$(this).attr("id","rect"+index);
					index++;
				});
			},			
			drawDirection:function(Fx,Fy,Bx,By,dir){
				var x1,x2,x3,x4,y1,y2,y3,y4;
				x1=Fx;y1=Fy;x2=Bx;y2=By;

				if (vaLineObj == null) {
					vaLineObj = document.getElementById("LineCanvas");
					if (G_vmlCanvasManager != undefined) { // ie IE
						G_vmlCanvasManager.initElement(vaLineObj);
					}
					vaLineContext = vaLineObj.getContext("2d");
				}
				
				//finding midpointof line
				x3=(Fx+Bx)/2;
				y3=(Fy+By)/2;

				var m = (y1 - y2) / (x1 - x2);
				//drawing perpendicular line
				vx = x2-x1;
				vy = y2-y1;
				len = Math.sqrt( vx*vx + vy*vy )
				ux = -vy/len;
				uy = vx/len;
				
				nx3 = x3 + 50/2 * ux;
				ny3 = y3 + 50/2 * uy;
				
				nx4 = x3 - 50/2 * ux;
				ny4 = y3 - 50/2 * uy;
				vaLineContext.beginPath();
				vaLineContext.strokeStyle = "#00ffff";
				vaLineContext.moveTo(nx3, ny3);
				vaLineContext.lineTo(nx4, ny4);
				vaLineContext.stroke();
				vaLineContext.closePath();
				var arrow = [
				[ 5, 0 ],
				[ -10, -4 ],
				[ -10, 4]
				];
				function drawFilledPolygon(shape) {
					vaLineContext.beginPath();
					vaLineContext.moveTo(shape[0][0],shape[0][1]);
					
					for(p in shape)
					if (p > 0) vaLineContext.lineTo(shape[p][0],shape[p][1]);
					
					vaLineContext.lineTo(shape[0][0],shape[0][1]);
					vaLineContext.fill();
				};
				
				function translateShape(shape,x,y) {
					var rv = [];
					for(p in shape)
					rv.push([ shape[p][0] + x, shape[p][1] + y ]);
					return rv;
				};
				
				function rotateShape(shape,ang)
				{
					var rv = [];
					for(p in shape)
					rv.push(rotatePoint(ang,shape[p][0],shape[p][1]));
					return rv;
				};
				function rotatePoint(ang,x,y) {
					return [
					(x * Math.cos(ang)) - (y * Math.sin(ang)),
					(x * Math.sin(ang)) + (y * Math.cos(ang))
					];
				};
				
				function drawLineArrow(x1,y1,x2,y2) {
					var ang = Math.atan2(y2-y1,x2-x1);
					drawFilledPolygon(translateShape(rotateShape(arrow,ang),x2,y2));
				};
				
				vaLineContext.strokeStyle = "#00ffff";
				vaLineContext.fillStyle = "#00ffff";
				if(dir=="right"){
					if(nx3 > nx4)
						drawLineArrow(nx4,ny4,nx3,ny3);
					else
						drawLineArrow(nx3,ny3,nx4,ny4);
				}
				else if (dir=="left"){
					if(nx3 > nx4)
						drawLineArrow(nx3,ny3,nx4,ny4);
					else
						drawLineArrow(nx4,ny4,nx3,ny3);
				}
				else {drawLineArrow(nx3,ny3,nx4,ny4); drawLineArrow(nx4,ny4,nx3,ny3);}
			},
			lineDraw:function(maxCount){
				EventSetup.VA.MAX_PASSING_COUNT = maxCount;
				EventSetup.VA.passingCount = 0;
				
				$("#lineDraw canvas").remove();
				$("#lineDraw span").remove();
				$("#lineDraw").append("<canvas id=\"LineCanvas\" width=\""+EventSetup.VIEWER_W+"\" height=\""+EventSetup.VIEWER_H+"\"></canvas>");
				if(BrowserDetect.browser == "Explorer" && getIEVersion() <= 8){
					$("#lineDraw").append("<span class=\"drawArea-position\" style=\"left:0px;background:#000;opacity:0;filter:alpha(opacity=0);\"></span>");
				}
				$("#lineDraw").append("<canvas id=\"LineCanvasTmp\" width=\""+EventSetup.VIEWER_W+"\" height=\""+EventSetup.VIEWER_H+"\" style=\"position: absolute;top:0px;left:0px;z-index:1000;\" ></canvas>");

				///////////////////////////////////////////
				var Fx, Fy;
				var Ax=0, Ay=0, Bx=0, By=0, index=1,create=false;

				$("#LineCanvasTmp").click(function(e) {
					if(EventSetup.IS_PTZ_SUPPORT){
						var vaCount = EventSetup.VA.passingCount + EventSetup.VA.enteringCount;
						if(vaCount == EventSetup.VA.MAX_PASSING_COUNT) return;
					}else{
						if(EventSetup.VA.passingCount == EventSetup.VA.MAX_PASSING_COUNT) return;
					}
					
					var offset = $(this).offset();
					if(index==1){

						Ax = e.pageX-offset.left;
						Ay = e.pageY-offset.top;
															
						if (window.navigator.msPointerEnabled) {		//Detect IE10 or IE11
							if($(window).scrollLeft() != 0 && e.pageX == e.clientX){
								Ax= Ax + $(window).scrollLeft();
							}
							if($(window).scrollTop() != 0 && e.pageY == e.clientY){
								Ay= Ay + $(window).scrollTop();
							}							
						}
					
						isDrawDragging=true;
						index++;
						$("#DisableIVSelectLayer").css("display","block");
						return;
					}					

					/////////////////////////////////////////////////
					if(index==2){
						Bx = e.pageX-offset.left;
						By = e.pageY-offset.top;
						if (window.navigator.msPointerEnabled) {		//Detect IE10 or IE11
							if($(window).scrollLeft() != 0 && e.pageX == e.clientX){
								Bx= Bx + $(window).scrollLeft();
							}
							if($(window).scrollTop() != 0 && e.pageY == e.clientY){
								By= By + $(window).scrollTop();
							}
						}
						
						if(Ay > By){
							Fx = Ax;
							Fy = Ay;
							
							Ax = Bx;
							Ay = By;
							
							Bx = Fx;
							By = Fy;
						}else if(Ay == By && Ax > Bx){
							Fx = Ax;
							Fy = Ay;
							
							Ax = Bx;
							Ay = By;
							
							Bx = Fx;
							By = Fy;							
						}
						
							/*
						vaLineContext.strokeStyle = "green";	
						vaLineTempContext.clearRect(0, 0, vaLineTempObj.width, vaLineTempObj.height);
						vaLineContext.beginPath();
						vaLineContext.moveTo(Fx, Fy);
						vaLineContext.lineTo(Bx, By);
						vaLineContext.stroke();
						vaLineContext.closePath();*/
						//////////////////////////////////////////////////////////////// x1=Fx;y1=Fy;x2=Bx;y2=By;
						
						///////////////////////////////////////////////////////////////
							
							EventSetup.VA.deleteClass="line"+EventSetup.VA.passingCount;
							if(Ax < 0) Ax = 0;
							if(Bx < 0) Bx = 0;
							if(Ay < 0) Ay = 0;
							if(By < 0) By = 0;
							$("#lineDraw").append("<div style='display:none' class='lineID line"+EventSetup.VA.passingCount+"'>"+Ax+","+Ay+","+Bx+","+By+"</div>");
							EventSetup.VA.passingCount++;
							EventSetup.VA.popUp("create",Ax,Ay,Bx,By);
							isDrawDragging=false;
							index=1;	
							EventSetup.VA.reDrawLine();
							$("#DisableIVSelectLayer").css("display","none");
							return;
					}
					
				});
							
				$("#LineCanvasTmp").mousemove(function(e) {
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
					
					if (isDrawDragging) {
						vaLineTempContext.clearRect(0, 0, vaLineTempObj.width, vaLineTempObj.height);
						vaLineTempContext.beginPath();
						vaLineTempContext.moveTo(Ax, Ay);
						vaLineTempContext.lineTo(xVal, yVal);
						vaLineTempContext.strokeStyle="yellow";
						vaLineTempContext.stroke();
						vaLineTempContext.closePath();
					}
				});
					
				$("#lineDraw").on("contextmenu",function(e){
					if(isDrawDragging){
						isDrawDragging=false;
						index = 1;
						EventSetup.VA.reDrawLine();
						$("#DisableIVSelectLayer").css("display","none");
						return false;
					}
					
					var offset = $(this).offset();
					var Fx=e.pageX - offset.left;
					var Fy=e.pageY - offset.top;
					
					if (window.navigator.msPointerEnabled) {		//Detect IE10 or IE11
						if($(window).scrollLeft() != 0 && e.pageX == e.clientX){
							Fx= Fx + $(window).scrollLeft();
						}
						if($(window).scrollTop() != 0 && e.pageY == e.clientY){
							Fy= Fy + $(window).scrollTop();
						}
					}
					
					$("#line-dialog input").prop("checked", false);
					$(".lineID").each(function(e) {
						var cordinates=$(this).html().split(",");
						var x1=parseInt(cordinates[0]);
						var y1=parseInt(cordinates[1]);
						var x2=parseInt(cordinates[2]);
						var y2=parseInt(cordinates[3]);
						
						if(dotLineLength(Fx,Fy, x1,y1,x2,y2,0)<3){
							EventSetup.VA.deleteClass=$(this).attr("class").split(' ')[1];
							if(parseInt($(this).attr("alt"))==0){  $("#line-dialog input#right").prop("checked", true); }
							else if(parseInt($(this).attr("alt"))==1){  $("#line-dialog input#left").prop("checked", true); }
							else if(parseInt($(this).attr("alt"))==2){  $("#line-dialog input").prop("checked", true); }
							EventSetup.VA.popUp("delete",x1,y1,x2,y2);
						}
					});
					
					return false;
					
				}); 	
			},
			getLine:function(xmlData){
				var x1, y1, x2, y2,firstTime=true, count=0;
				//var xml_data=$.parseXML(xmlData);
				xmlData.find("LineObject").each(function()
				{
					var lineRule=$(this).find("LineRule").text();
					if (lineRule == 0 && EventSetup.FLIP_MIRROR >= 2 && EventSetup.IS_PTZ_SUPPORT == false)
					{
						lineRule = 1;
					}
					else if (lineRule == 1 && EventSetup.FLIP_MIRROR >= 2 && EventSetup.IS_PTZ_SUPPORT == false)
					{
						lineRule = 0;
					}
					if (typeof analyticsType != 'undefined') analyticsType = 0;
					$(this).find("Point").each(function()
					{
						if(firstTime)
						{
							x1=$(this).find("X").text()/(EventSetup.RATIO_W);
							y1=$(this).find("Y").text()/(EventSetup.RATIO_H);
							firstTime=false;
							count++;
						}
						else {
							if(x1==0&&y1==0) return;
							x2=$(this).find("X").text()/(EventSetup.RATIO_W);
							y2=$(this).find("Y").text()/(EventSetup.RATIO_H);
							firstTime=true;
							/*
							vaLineContext.strokeStyle = 'green';
							vaLineContext.beginPath();
							vaLineContext.moveTo(x1, y1);
							vaLineContext.lineTo(x2, y2);
							vaLineContext.stroke();
							vaLineContext.closePath();
							
							if(lineRule==0) {EventSetup.VA.drawDirection(x1,y1,x2,y2,"right");}
							if(lineRule==1) {EventSetup.VA.drawDirection(x1,y1,x2,y2,"left");}
							if(lineRule==2) {EventSetup.VA.drawDirection(x1,y1,x2,y2,"right");EventSetup.VA.drawDirection(x1,y1,x2,y2,"left");}
							*/
							if(!EventSetup.IS_PTZ_SUPPORT){
								if(EventSetup.FLIP_MIRROR == 1) {
									y1=EventSetup.VIEWER_H - y1;
									y2=EventSetup.VIEWER_H - y2;
								}
								else if(EventSetup.FLIP_MIRROR == 2) {
									x1=EventSetup.VIEWER_W - x1;
									x2=EventSetup.VIEWER_W - x2;
								}
								else if(EventSetup.FLIP_MIRROR == 3) {
									y1=EventSetup.VIEWER_H - y1;
									y2=EventSetup.VIEWER_H - y2;
									x1=EventSetup.VIEWER_W - x1;
									x2=EventSetup.VIEWER_W - x2;					
								}
							}
							
							$("#lineDraw").append("<div style='display:none' alt='"+lineRule+"' class='lineID line"+EventSetup.VA.passingCount+"'>"+x1+","+y1+","+x2+","+y2+"</div>");
							
							EventSetup.VA.passingCount++;
							x1=0; y1=0;
						}
					
					});
				});
			
			},
			
			reDrawLine:function(){
				vaLineObj = document.getElementById("LineCanvas");
				if (G_vmlCanvasManager != undefined) { // ie IE
					G_vmlCanvasManager.initElement(vaLineObj);
				}
				vaLineContext = vaLineObj.getContext("2d");
				vaLineContext.lineWidth = 2;
				vaLineContext.strokeStyle = 'green';	

				vaLineTempObj = document.getElementById("LineCanvasTmp");
				if (G_vmlCanvasManager != undefined) { // ie IE
					G_vmlCanvasManager.initElement(vaLineTempObj);
				}
				vaLineTempContext = vaLineTempObj.getContext("2d");
				vaLineTempContext.lineWidth = 2;
				vaLineTempContext.strokeStyle = "yellow";
				
				vaLineContext.clearRect(0,0,vaLineObj.width,vaLineObj.height);		
				vaLineTempContext.clearRect(0,0,vaLineTempObj.width,vaLineTempObj.height);
				var index = 0;
				$(".lineID").each(function(e) {
					var cordinates=$(this).html().split(",");
					var x1=parseInt(cordinates[0]);
					var y1=parseInt(cordinates[1]);
					var x2=parseInt(cordinates[2]);
					var y2=parseInt(cordinates[3]);
					var lineRule=$(this).attr("alt");

					if(lineRule==0) {EventSetup.VA.drawDirection(x1,y1,x2,y2,"right");}
					if(lineRule==1) {EventSetup.VA.drawDirection(x1,y1,x2,y2,"left");}
					if(lineRule==2) {EventSetup.VA.drawDirection(x1,y1,x2,y2,"right");EventSetup.VA.drawDirection(x1,y1,x2,y2,"left");}
					
					vaLineContext.strokeStyle = 'green';
					vaLineContext.beginPath();
					vaLineContext.moveTo(x1, y1);
					vaLineContext.lineTo(x2, y2);
					vaLineContext.stroke();
					vaLineContext.closePath();
					$(this).removeClass();
					$(this).attr("class", "lineID line"+index);
					index++;
				});
			},
			setMD_xml:function(){
				
						var i=0;
						var RectsetXmlData='';
						var leftMD=0;
						
						$("#MDPolyDraw .MDpolygonID").each(function()
						{
							var cordinates=$(this).html().split(",");
														
							if(EventSetup.MD.mdDrawType == EventSetup.TYPE_RECT){
								var x1=cordinates[0]*(EventSetup.RATIO_W);
								var y1=cordinates[1]*(EventSetup.RATIO_H);
								var x2=cordinates[2]*(EventSetup.RATIO_W);
								var y2=cordinates[3]*(EventSetup.RATIO_H);

								if(x1 < 0){
									x1 = 0;
								}
								if(y1 < 0){
									y1 = 0;
								}
								if(x2 < 0){
									x2 = 0;
								}
								if(y2 < 0){
									y2 = 0;
								}
								if(x1 >= EventSetup.MAX_RESOLUTION_W){
									x1 = EventSetup.MAX_RESOLUTION_W-1;
								}
								if(y1 >= EventSetup.MAX_RESOLUTION_H){
									y1 = EventSetup.MAX_RESOLUTION_H-1;
								}
								if(x2 >= EventSetup.MAX_RESOLUTION_W){
									x2 = EventSetup.MAX_RESOLUTION_W-1;
								}
								if(y2 >= EventSetup.MAX_RESOLUTION_H){
									y2 = EventSetup.MAX_RESOLUTION_H-1;
								}

								if(EventSetup.FLIP_MIRROR == 1) {
									y1 = EventSetup.MAX_RESOLUTION_H-1 -y1;
									y2 = EventSetup.MAX_RESOLUTION_H-1 -y2;
								}else if(EventSetup.FLIP_MIRROR == 2) {
									x1 = EventSetup.MAX_RESOLUTION_W-1 - x1;
									x2 = EventSetup.MAX_RESOLUTION_W-1 - x2;
								}else if(EventSetup.FLIP_MIRROR == 3) { 
									x1 = EventSetup.MAX_RESOLUTION_W-1 - x1;
									x2 = EventSetup.MAX_RESOLUTION_W-1 - x2;
									y1 = EventSetup.MAX_RESOLUTION_H-1 -y1;
									y2 = EventSetup.MAX_RESOLUTION_H-1 -y2;
								}

								if (x2 < x1)
								{
									var temp;
									temp = x1;
									x1 = x2;
									x2 = temp;
								}
								if (y2 < y1)
								{
									var temp;
									temp = y1;
									y1 = y2;
									y2 = temp;
								}
	
								RectsetXmlData+="<ObjectArea"+i+"><NumPoint>2</NumPoint><MDPoint0><PosX>"+x1+"</PosX><PosY>"+y1+"</PosY></MDPoint0><MDPoint1><PosX>"+x2+"</PosX><PosY>"+y2+"</PosY></MDPoint1><MDPoint2><PosX>"+x3+"</PosX><PosY>"+y3+"</PosY></MDPoint2><MDPoint3><PosX>"+x4+"</PosX><PosY>"+y4+"</PosY></MDPoint3></ObjectArea"+i+">";
							}else{
								var x1=cordinates[0];
								var y1=cordinates[1];
								var x2=cordinates[2];
								var y2=cordinates[3];
								var x3=cordinates[4];
								var y3=cordinates[5];
								var x4=cordinates[6];
								var y4=cordinates[7];
								var xpos = [x1,x2,x3,x4];
								var ypos = [y1,y2,y3,y4];

								if(EventSetup.FLIP_MIRROR == 1) {
									for(var j = 0; j < 4; j++){
										ypos[j]=EventSetup.VIEWER_H - ypos[j];
									}
								}
								else if(EventSetup.FLIP_MIRROR == 2) {
									for(var j = 0; j < 4; j++){
										xpos[j]=EventSetup.VIEWER_W - xpos[j];
									}
								}
								else if(EventSetup.FLIP_MIRROR == 3) { 
									for(var j = 0; j < 4; j++){
										ypos[j]=EventSetup.VIEWER_H - ypos[j];
									}	
									for(var j = 0; j < 4; j++){
										xpos[j]=EventSetup.VIEWER_W - xpos[j];
									}
								}
								
								var posXml = '';
								for(var j = 0; j < 4; j++){
									xpos[j] = xpos[j]*(EventSetup.RATIO_W);
									ypos[j] = ypos[j]*(EventSetup.RATIO_H);

									if(xpos[j] < 0){
										xpos[j] = 0;
									}
									if(ypos[j] < 0){
										ypos[j] = 0;
									}
									if(xpos[j] >= EventSetup.MAX_RESOLUTION_W){
										xpos[j] = EventSetup.MAX_RESOLUTION_W-1;
									}
									if(ypos[j] >= EventSetup.MAX_RESOLUTION_H){
										ypos[j] = EventSetup.MAX_RESOLUTION_H-1;
									}

									posXml += "<MDPoint"+j+"><PosX>"+xpos[j]+"</PosX><PosY>"+ypos[j]+"</PosY></MDPoint"+j+">";
								}
							
								RectsetXmlData+="<ObjectArea"+i+"><NumPoint>4</NumPoint>"+posXml+"</ObjectArea"+i+">";
							}							
							i++;
							leftMD=$("#MDPolyDraw .MDpolygonID").length
	
						});
						
						for(var j=leftMD;j<4;j++){
							var rect_xml_data=$.parseXML(EventSetup.setMDXML);							
							RectsetXmlData+="<ObjectArea"+j+"><NumPoint>0</NumPoint><MDPoint0><PosX>0</PosX><PosY>0</PosY></MDPoint0><MDPoint1><PosX>0</PosX><PosY>0</PosY></MDPoint1><MDPoint2><PosX>0</PosX><PosY>0</PosY></MDPoint2><MDPoint3><PosX>0</PosX><PosY>0</PosY></MDPoint3></ObjectArea"+j+">";
						}
							
					
					var Mdresponse="<MDConfiguration><ObjectMode>1</ObjectMode><Sensitivity>2</Sensitivity><ObjectSize>5</ObjectSize><ManualSize><VSL>4</VSL><VSH>90</VSH><HSL>4</HSL><HSH>91</HSH></ManualSize><Overlay>0</Overlay><VABoxDisplay>0</VABoxDisplay><Schedule><Enabled>0</Enabled></Schedule>"+RectsetXmlData+"</MDConfiguration>";
				///////////////////////////////////////////////////////////////////////////////////////////////////////////////
						
				return RectsetXmlData;
			},
	setVA_xml:function(){
		//setting polygon cordinates
		
		var PolyCount= parseInt($(".polygonID").length) + parseInt($(".appDiss").length);
		var loopPol=['polygonID','appDiss'];
		
		var objectRullData = new Array(6);
		for (var j=0; j<6; ++j) {
			if (j < 3) {
				objectRullData[j] = "<LineObject"+j+"><Type>0</Type></LineObject"+j+">";
			}
			else {
				objectRullData[j] = "<AreaObject"+j+"><Type>0</Type></AreaObject"+j+">";
			}
		}
		var firstTime=true;
		var objIndex=0;
		var setLineXML="";
		var lineRule=0;
		$(".lineID").each(function(){
			var cordinates=$(this).html().split(",");
			var x1=cordinates[0];
			var y1=cordinates[1];
			var x2=cordinates[2];
			var y2=cordinates[3];

			if(!EventSetup.IS_PTZ_SUPPORT){
				if(EventSetup.FLIP_MIRROR == 1) {
					y1=EventSetup.VIEWER_H - y1;
					y2=EventSetup.VIEWER_H - y2;
				}
				else if(EventSetup.FLIP_MIRROR == 2) {
					x1=EventSetup.VIEWER_W - x1;
					x2=EventSetup.VIEWER_W - x2;
				}
				else if(EventSetup.FLIP_MIRROR == 3) { 
					y1=EventSetup.VIEWER_H - y1;
					y2=EventSetup.VIEWER_H - y2;
					x1=EventSetup.VIEWER_W - x1;
					x2=EventSetup.VIEWER_W - x2;					
				}								
			}
			
			x1=x1*(EventSetup.RATIO_W);
			y1=y1*(EventSetup.RATIO_H);
			x2=x2*(EventSetup.RATIO_W);
			y2=y2*(EventSetup.RATIO_H);
			lineRule=$(this).attr("alt");
			if (lineRule == 0 && EventSetup.FLIP_MIRROR >= 2 && EventSetup.IS_PTZ_SUPPORT == false)
			{
				lineRule = 1;
			}
			else if (lineRule == 1 && EventSetup.FLIP_MIRROR >= 2 && EventSetup.IS_PTZ_SUPPORT == false)
			{
				lineRule = 0;
			}

			if(x1 < 0){
				x1 = 0;
			}
			if(y1 < 0){
				y1 = 0;
			}
			if(x2 < 0){
				x2 = 0;
			}
			if(y2 < 0){
				y2 = 0;
			}
			if(x1 >= EventSetup.MAX_RESOLUTION_W){
				x1 = EventSetup.MAX_RESOLUTION_W-1;
			}
			if(y1 >= EventSetup.MAX_RESOLUTION_H){
				y1 = EventSetup.MAX_RESOLUTION_H-1;
			}
			if(x2 >= EventSetup.MAX_RESOLUTION_W){
				x2 = EventSetup.MAX_RESOLUTION_W-1;
			}
			if(y2 >= EventSetup.MAX_RESOLUTION_H){
				y2 = EventSetup.MAX_RESOLUTION_H-1;
			}

			objectRullData[objIndex]="<LineObject"+objIndex+"><Type>1</Type><PointCount>2</PointCount><LineRule>"+lineRule+"</LineRule><Point0><Valid>1</Valid><PosX>"+x1+"</PosX><PosY>"+y1+"</PosY></Point0><Point1><Valid>1</Valid><PosX>"+x2+"</PosX><PosY>"+y2+"</PosY></Point1></LineObject"+objIndex+">";
			objIndex++;
		});

		objIndex = 3;
		for(var j=0; j < loopPol.length; j++){
			$("."+loopPol[j]).each(function(){
				var cordinates=$(this).html().split(",");
				var posX = new Array(cordinates.length);
				var posY = new Array(cordinates.length);
				posX[0]=cordinates[0];
				posY[0]=cordinates[1];
				posX[1]=cordinates[2];
				posY[1]=cordinates[3];
				if (cordinates.length > 4) {
					posX[2]=cordinates[4];
					posY[2]=cordinates[5];
					posX[3]=cordinates[6];
					posY[3]=cordinates[7];
				}

				if(EventSetup.FLIP_MIRROR == 1) {
					for(var j = 0; j < cordinates.length/2; j++){
						posY[j] = EventSetup.VIEWER_H - posY[j];
					}
				}
				else if(EventSetup.FLIP_MIRROR == 2) {
					for(var j = 0; j < cordinates.length/2; j++){
						posX[j] = EventSetup.VIEWER_W - posX[j];
					}
				}
				else if(EventSetup.FLIP_MIRROR == 3) { 
					for(var j = 0; j < cordinates.length/2; j++){
						posY[j] = EventSetup.VIEWER_H - posY[j];
					}	
					for(var j = 0; j < cordinates.length/2; j++){
						posX[j] = EventSetup.VIEWER_W - posX[j];
					}
				}

				var Aenter=0,Aexit=0,AappDisapp=0;
				
				if($(this).attr("alt")=="AreaAppearDisappear"){ 
					AappDisapp = 1;
					if(EventSetup.VA.MAX_APPEARING_COUNT == 1){		//Only for WN2_PTZ spec
						objIndex = 4;
					}
				}else if($(this).attr("alt")=="AreaEnter"){
					Aenter = 1;
				}else if($(this).attr("alt")=="AreaExit"){
					Aexit = 1;
				}else{
					Aenter = 1;
					Aexit = 1;
				}
				
				objectRullData[objIndex]="<AreaObject"+objIndex+">\
											<Type>2</Type>\
											<PointCount>"+(cordinates.length/2)+"</PointCount>\
											<AreaEnter>"+Aenter+"</AreaEnter>\
											<AreaExit>"+Aexit+"</AreaExit>\
											<AreaAppear>"+AappDisapp+"</AreaAppear>\
											<AreaDisappear>"+AappDisapp+"</AreaDisappear>\\";
				for (var k=0; k<(cordinates.length/2); ++k) {
					posX[k] = posX[k]*(EventSetup.RATIO_W);					
					posY[k] = posY[k]*(EventSetup.RATIO_H);
					
					if(posX[k] < 0){
						posX[k] = 0;
					}
					if(posY[k] < 0){
						posY[k] = 0;
					}
					if(posX[k] >= EventSetup.MAX_RESOLUTION_W){
						posX[k] = EventSetup.MAX_RESOLUTION_W-1;
					}
					if(posY[k] >= EventSetup.MAX_RESOLUTION_H){
						posY[k] = EventSetup.MAX_RESOLUTION_H-1;
					}

					objectRullData[objIndex]+="<Point"+k+"><Valid>1</Valid><PosX>"+posX[k]+"</PosX><PosY>"+posY[k]+"</PosY></Point"+k+">";
				}
				objectRullData[objIndex]+="</AreaObject"+objIndex+">";
				objIndex++;
			});
		}
		if(EventSetup.IS_PTZ_SUPPORT)
			objIndex = 5;
		else
			objIndex = 6;
		
		var VaRespone="<FullScreen><FullAppear>"+($('#app_disapp_entire').is(':checked')?1:0)+"</FullAppear><FullDisappear>0</FullDisappear><FullSceneChange>0</FullSceneChange></FullScreen>";
		for (var j=0; j<objIndex; ++j) {
			VaRespone+="<IVObject>"+objectRullData[j]+"</IVObject>";
		}
		return VaRespone;
	},
			popUp:function(type,Fx,Fy,Bx,By){
				var create=true;
				$("#line-dialog").dialog({
					autoOpen: false,
					modal: true,
					draggable: false,
					position:{
						my: 'center',
						of: $("#pluginArea")
					},
				  	dialogClass: 'polygon-dialog-class',
				 	title: function(){
				  		if(type == "delete")
							return titleLang[0];
						else
							return titleLang[0];
				  	},
				  	open: function(){
					 	if($("#line-dialog #right").is(":checked") || $("#line-dialog #left").is(":checked")){
							$("#button-ok-lineDialog").button("enable");
					 	}	
						else{
							$("#button-ok-lineDialog").button("disable");
						}
						
				  	},
				 	beforeClose: function( event, ui ) { 
				  		if(type == "create"){
						  	if(create) {
								$("#lineDraw div").remove("."+EventSetup.VA.deleteClass);
								EventSetup.VA.passingCount--;
								deleteLine();
								EventSetup.VA.reDrawLine();
							}
				  		}
				  	},
				  	close: function(){
						$("#line-dialog input[type=checkbox]").prop('checked', false);
				  	},
				  	buttons: [
					  	{
					  		id:"button-ok-lineDialog",
							text: okLang,
							click: function(){
								if(type=="delete"){
									if($('#line-dialog #right').is(':checked')){  $("."+EventSetup.VA.deleteClass).attr("alt","0"); deleteLine(); }
									if ($('#line-dialog #left').is(':checked')){  $("."+EventSetup.VA.deleteClass).attr("alt","1"); deleteLine();  }
									if ($('#line-dialog #right').is(':checked') && $('#line-dialog #left').is(':checked')){  $("."+EventSetup.VA.deleteClass).attr("alt","2"); deleteLine();}
									
								}else{
									create=false;
									if($('#line-dialog #right').is(':checked')){ EventSetup.VA.drawDirection(Fx,Fy,Bx,By,"right"); $("."+EventSetup.VA.deleteClass).attr("alt","0");}
									if ($('#line-dialog #left').is(':checked')){ EventSetup.VA.drawDirection(Fx,Fy,Bx,By,"left");$("."+EventSetup.VA.deleteClass).attr("alt","1"); }
									if ($('#line-dialog #right').is(':checked') && $('#line-dialog #left').is(':checked')){$("."+EventSetup.VA.deleteClass).attr("alt","2");}
								}
								$( this ).dialog( "close" );
							}
						},
						{
							id:"button-cancel-lineDialog",
							text: cancelLang,
							click: function() {
							  $( this ).dialog( "close" );
							}
						},
						{
							id:"button-delete-lineDialog",
							text: deleteLang,
							click:function(){
								if(type=="delete"){
									$("#lineDraw div").remove("."+EventSetup.VA.deleteClass);
									EventSetup.VA.passingCount--;
									deleteLine();
									EventSetup.VA.reDrawLine();
								}
								$( this ).dialog( "close" );
							}
						}	
				  	]
				});
				$( "#line-dialog" ).dialog("open");
	
				$("#line-dialog #right, #line-dialog #left").on("click", function(){
					if($("#line-dialog #right").is(":checked") || $("#line-dialog #left").is(":checked")){
						$("#button-ok-lineDialog").button("enable");
				 	}
					else{
						$("#button-ok-lineDialog").button("disable");
					}
				});
				
			},
			drawPolygonLine:function(Ax, Ay, Bx, By,index)
			{
				
					bla = "";
					var lineLength = Math.sqrt( (Ax-Bx)*(Ax-Bx)+(Ay-By)*(Ay-By) );
					for( var i=0; i<lineLength; i++ )
					{
						bla += "<div class='currentPoly polygon"+index+"' style='left:"+ Math.round( Ax+(Bx-Ax)*i/lineLength  ) +"px;top:"+ Math.round( Ay+(By-Ay)*i/lineLength  ) +"px;'></div>";
					}
					document.getElementById("polyDraw").innerHTML += bla;
								
					
			},
			drawLine:function(Ax, Ay, Bx, By,index,divID)
			{
				
					bla = "";
					var lineLength = Math.sqrt( (Ax-Bx)*(Ax-Bx)+(Ay-By)*(Ay-By) );
					for( var i=0; i<lineLength; i++ )
					{
						bla += "<div class='currentLine line"+index+"' style='left:"+ Math.round( Ax+(Bx-Ax)*i/lineLength  ) +"px;top:"+ Math.round( Ay+(By-Ay)*i/lineLength  ) +"px; '></div>";
					}
					//document.getElementById(divID).innerHTML += bla
					$("#"+divID).append(bla);
			},
			
			polygonArea:function(X, Y, numPoints) 
			{ 
				  area = 0;         // Accumulates area in the loop
				  j = numPoints-1;  // The last vertex is the 'previous' one to the first

				  for (i=0; i<numPoints; i++)
					{ area = area +  (X[j]+X[i]) * (Y[j]-Y[i]); 
					  j = i;  //j is previous vertex to i
					}
				  return area/2;
			},
			lineIntersect:function(x1,y1,x2,y2, x3,y3,x4,y4) {
				var x=((x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4));
				var y=((x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4));
				if (isNaN(x)||isNaN(y)) {
					return false;
				} else {
					if (x1>=x2) {
						if (!(x2<=x&&x<=x1)) {return false;}
					} else {
						if (!(x1<=x&&x<=x2)) {return false;}
					}
					if (y1>=y2) {
						if (!(y2<=y&&y<=y1)) {return false;}
					} else {
						if (!(y1<=y&&y<=y2)) {return false;}
					}
					if (x3>=x4) {
						if (!(x4<=x&&x<=x3)) {return false;}
					} else {
						if (!(x3<=x&&x<=x4)) {return false;}
					}
					if (y3>=y4) {
						if (!(y4<=y&&y<=y3)) {return false;}
					} else {
						if (!(y3<=y&&y<=y4)) {return false;}
					}
				}
				return true;
			},
			view:function(Sel_div){
				$("#polyDraw,#lineDraw,#rectangleDraw,#max_min,#fullScreen,#MDPolyDraw").css("display","none");
				$("#"+Sel_div).css("display","block");
				switch(Sel_div){
					case "MDPolyDraw" : EventSetup.viewStatus = VIEW_MODE["MD"]; break;
					case "max_min" : EventSetup.viewStatus = VIEW_MODE["MD_OBJSIZE"]; break;
					case "lineDraw" : EventSetup.viewStatus = VIEW_MODE["VA_PASSING"]; break;
					case "polyDraw" : EventSetup.viewStatus = VIEW_MODE["VA_ENTERING"]; break;
					case "rectangleDraw" : EventSetup.viewStatus = VIEW_MODE["VA_APPEAR"]; break;
					case "fullScreen" : EventSetup.viewStatus = VIEW_MODE["VA_ENTIRE"]; break;
					default : EventSetup.viewStatus = VIEW_MODE["NONE"];
				}
			}
};

//create and fill polygon
function GetAngleABC22( a,b,c)
{
	var ab = { x:b.x - a.x, y:b.y - a.y };
	var cb = { x:b.x - c.x, y:b.y - c.y };
	
	var dot = (ab.x * cb.x + ab.y * cb.y); // dot product
	var cross = (ab.x * cb.y - ab.y * cb.x); // cross product
	
	var alpha = Math.atan2(cross, dot);
	
	return Math.floor(alpha * 180 / 3.141592 + 0.5);
}		

var dotLineLength = function(x, y, x0, y0, x1, y1, o) {
  function lineLength(x, y, x0, y0){
    return Math.sqrt((x -= x0) * x + (y -= y0) * y);
  }
  if(o && !(o = function(x, y, x0, y0, x1, y1){
    if(!(x1 - x0)) return {x: x0, y: y};
    else if(!(y1 - y0)) return {x: x, y: y0};
    var left, tg = -1 / ((y1 - y0) / (x1 - x0));
    return {x: left = (x1 * (x * tg - y + y0) + x0 * (x * - tg + y - y1)) / (tg * (x1 - x0) + y0 - y1), y: tg * left - tg * x + y};
  }(x, y, x0, y0, x1, y1), o.x >= Math.min(x0, x1) && o.x <= Math.max(x0, x1) && o.y >= Math.min(y0, y1) && o.y <= Math.max(y0, y1))){
    var l1 = lineLength(x, y, x0, y0), l2 = lineLength(x, y, x1, y1);
    return l1 > l2 ? l2 : l1;
  }
  else {
    var a = y0 - y1, b = x1 - x0, c = x0 * y1 - y0 * x1;
    return Math.abs(a * x + b * y + c) / Math.sqrt(a * a + b * b);
  }
};

var dotLineLength = function(x, y, x0, y0, x1, y1, o) {
  function lineLength(x, y, x0, y0){
    return Math.sqrt((x -= x0) * x + (y -= y0) * y);
  }
  if(o && !(o = function(x, y, x0, y0, x1, y1){
    if(!(x1 - x0)) return {x: x0, y: y};
    else if(!(y1 - y0)) return {x: x, y: y0};
    var left, tg = -1 / ((y1 - y0) / (x1 - x0));
    return {x: left = (x1 * (x * tg - y + y0) + x0 * (x * - tg + y - y1)) / (tg * (x1 - x0) + y0 - y1), y: tg * left - tg * x + y};
  }(x, y, x0, y0, x1, y1), o.x >= Math.min(x0, x1) && o.x <= Math.max(x0, x1) && o.y >= Math.min(y0, y1) && o.y <= Math.max(y0, y1))){
    var l1 = lineLength(x, y, x0, y0), l2 = lineLength(x, y, x1, y1);
    return l1 > l2 ? l2 : l1;
  }
  else {
    var a = y0 - y1, b = x1 - x0, c = x0 * y1 - y0 * x1;
    return Math.abs(a * x + b * y + c) / Math.sqrt(a * a + b * b);
  }
}

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
	
function sqr(x) { return x * x }

function dist2(v, w) { return sqr(v.x - w.x) + sqr(v.y - w.y) }

function distToSegmentSquared(p, v, w) 
{
	var l2 = dist2(v, w);
	if (l2 == 0) return dist2(p, v);
	var t = ((p.x - v.x) * (w.x - v.x) + (p.y - v.y) * (w.y - v.y)) / l2;
	if (t < 0) return dist2(p, v);
	if (t > 1) return dist2(p, w);
	return dist2(p, { x: v.x + t * (w.x - v.x),
	                y: v.y + t * (w.y - v.y) });
}

function distToSegment(p, v, w) 
{
	return Math.sqrt(distToSegmentSquared(p, v, w)); 
}

function deleteLine()
{	
	if (vaLineObj == null) {
		vaLineObj = document.getElementById("LineCanvas");
		if (G_vmlCanvasManager != undefined) { // ie IE
			G_vmlCanvasManager.initElement(vaLineObj);
		}
		vaLineContext = vaLineObj.getContext("2d");
	}

	vaLineContext.lineWidth = 2;
	vaLineContext.strokeStyle = 'green';
	vaLineContext.clearRect(0, 0, vaLineObj.width, vaLineObj.height);
	
	$(".lineID").each(function(e) {
		var cordinates=$(this).html().split(",");

		var x1=parseInt(cordinates[0]);
		var y1=parseInt(cordinates[1]);
		var x2=parseInt(cordinates[2]);
		var y2=parseInt(cordinates[3]);
		var lineRule=$(this).attr("alt");
		if(lineRule==0) {EventSetup.VA.drawDirection(x1,y1,x2,y2,"right");}
		if(lineRule==1) {EventSetup.VA.drawDirection(x1,y1,x2,y2,"left");}
		if(lineRule==2) {EventSetup.VA.drawDirection(x1,y1,x2,y2,"right");EventSetup.VA.drawDirection(x1,y1,x2,y2,"left");}
		vaLineContext.strokeStyle = 'green';
		vaLineContext.beginPath();	
		vaLineContext.moveTo(x1, y1);vaLineContext.lineTo(x2, y2);vaLineContext.stroke();
		vaLineContext.closePath();

	});
};

function lineIntersect(x1,y1,x2,y2, x3,y3,x4,y4) 
{
	var x=((x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4));
	var y=((x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4));
	if (isNaN(x)||isNaN(y)) {
		return false;
	} else {
		if (x1>=x2) {
			if (!(x2<=x&&x<=x1)) {return false;}
		} else {
			if (!(x1<=x&&x<=x2)) {return false;}
		}
		if (y1>=y2) {
			if (!(y2<=y&&y<=y1)) {return false;}
		} else {
			if (!(y1<=y&&y<=y2)) {return false;}
		}
		if (x3>=x4) {
			if (!(x4<=x&&x<=x3)) {return false;}
		} else {
			if (!(x3<=x&&x<=x4)) {return false;}
		}
		if (y3>=y4) {
			if (!(y4<=y&&y<=y3)) {return false;}
		} else {
			if (!(y3<=y&&y<=y4)) {return false;}
		}
	}
	return true;
};

function isPointInPoly(poly, pt)
{
	for(var c = false, i = -1, l = poly.length, j = l - 1; ++i < l; j = i)
		((poly[i].y <= pt.y && pt.y < poly[j].y) || (poly[j].y <= pt.y && pt.y < poly[i].y))
		&& (pt.x < (poly[j].x - poly[i].x) * (pt.y - poly[i].y) / (poly[j].y - poly[i].y) + poly[i].x)
		&& (c = !c);
	return c;
}


$(function() {
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
});
