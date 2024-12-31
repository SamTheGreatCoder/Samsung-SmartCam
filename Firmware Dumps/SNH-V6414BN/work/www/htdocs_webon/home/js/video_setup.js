//js

var G_vmlCanvasManager; // so non-IE won't freak out in canvasInit
var c=null;
var c2=null;
var canvas=null;
var context=null;

videoSetup={};
videoSetup={
	TYPE_RECT:0,
	TYPE_POLY:1,
	MAX_RESOLUTION_W: 1920,
	MAX_RESOLUTION_H: 1080,
	VIEWER_W: 640,
	VIEWER_H: 360,
	RATIO_W: this.MAX_RESOLUTION_W / this.VIEWER_W,
	RATIO_H: this.MAX_RESOLUTION_H / this.VIEWER_H,
	FLIP_MIRROR: 0,			//"0": Flip OFF / Mirror OFF,  "1": Flip ON /Mirror OFF,  "2": Flip OFF / Mirror ON, "3": Flip ON / Mirror ON
	IS_PTZ_SUPPORT: false,

	ROTATE: 0,

	areaCount:0,
	isDrawDragging:false,
	firstDrawClick:false,
	
	getAreaXML:'',
	AddPARectagnleXML:'<AddPrivacyArea><Name>area4</Name><NumPoint>2</NumPoint><Point><X>883.2</X><Y>84</Y></Point><Point><X>1785.6</X><Y>336</Y></Point></AddPrivacyArea>',
	AddPAPolygonXML:'<AddPrivacyArea><Name>area16</Name><NumPoint>4</NumPoint><Point><X>1094.4</X><Y>630</Y></Point><Point><X>1472</X><Y>552</Y></Point><Point><X>1529.6</X><Y>738</Y></Point><Point><X>1171.2</X><Y>810</Y></Point></AddPrivacyArea>',
	msg_max_Privacyarea:'',

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

	drawType:this.TYPE_RECT,
	init:function(width,height,maxWidth,maxheight,areaNum, drawType, flip_mirror, isPtzSupport, rotate){
		this.drawType = drawType;
		this.VIEWER_W = width;
		this.VIEWER_H = height;
		this.ROTATE = rotate;
		if(this.ROTATE == 1 || this.ROTATE ==3){
			this.MAX_RESOLUTION_W = maxheight;
			this.MAX_RESOLUTION_H = maxWidth;
		}else{
			this.MAX_RESOLUTION_W = maxWidth;
			this.MAX_RESOLUTION_H = maxheight;
		}
		this.RATIO_W = this.MAX_RESOLUTION_W / this.VIEWER_W;
		this.RATIO_H = this.MAX_RESOLUTION_H / this.VIEWER_H;
		this.FLIP_MIRROR = flip_mirror;
		this.IS_PTZ_SUPPORT = isPtzSupport;

		c=document.getElementById("myCanvas");
		if (G_vmlCanvasManager != undefined) { // ie IE
			G_vmlCanvasManager.initElement(c);
		}
		
		canvas=document.getElementById("imgTemp");
		if (G_vmlCanvasManager != undefined) { // ie IE
			G_vmlCanvasManager.initElement(canvas);
		}
		
		c2=c.getContext("2d");
		c2.lineWidth = 2;
		c2.strokeStyle = "green";
		c2.globalAlpha="1"; 
		
		context=canvas.getContext("2d");
		context.lineWidth = 2;
		context.strokeStyle = "yellow";
		context.globalAlpha="1";
		
		$("#AreaNames").bind("click",function(e) {
			videoSetup.selectPolygon($(".selArea").attr("id"));
		});
		$("#DeleteArea").click(function(e) {
			if($("#AreaNames li a").hasClass("selArea")) {
			var deleteIndex=$(".selArea").attr("id");
			
			videoSetup.deleteArea(deleteIndex);
			
			//videoSetup.selectPolygon();
			}
		});
		
		var Ax=0, Ay=0, Bx=0, By=0;
		var x1=0,y1=0,x2=0,y2=0,x3=0,y3=0,x4=0,y4=0;
		var a1=0,b1=0,a2=0,b2=0,a3=0,b3=0,a4=0,b4=0;

		if(this.drawType == this.TYPE_RECT){
			var privacyRect = {};
			$("#imgTemp").mousedown(function(e) {
				if($("#DisableVideoSetup").is(":visible")){
					return;
				}
				
				if(e.which != 1 || $("#AreaNames").children().length >= areaNum) {			//right click or Maximum Area count
					if($("#AreaNames").children().length >= areaNum){
						alert(videoSetup.msg_max_Privacyarea);
					}
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
				
				privacyRect.startX = xVal;
				privacyRect.startY = yVal;
				videoSetup.firstDrawClick = true;
				videoSetup.isDrawDragging = false;

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
				
				if(videoSetup.firstDrawClick){	
					privacyRect.w = xVal - privacyRect.startX;
				    privacyRect.h = yVal - privacyRect.startY;
					privacyRect.endX = xVal;
					privacyRect.endY = yVal;
					
					c2.clearRect(0,0,canvas.width,canvas.height);

					c2.strokeStyle = "green";
					c2.lineWidth = 2;
					c2.globalAlpha="1";
					c2.strokeRect(privacyRect.startX,privacyRect.startY,privacyRect.w,privacyRect.h);
				}
				videoSetup.isDrawDragging = true;
				
				/*
				if (isDragging) {
					context.clearRect(0, 0, canvas.width, canvas.height);
					context.beginPath();
					context.moveTo(Ax, Ay);
					context.lineTo(xVal, yVal);
					context.stroke();
					context.closePath();
				}
				*/
			});
	 
			$("#imgTemp").mouseup(function(e) {
				if(!videoSetup.firstDrawClick) {
					return;
				}	
				videoSetup.firstDrawClick = false;
				if(videoSetup.isDrawDragging){
					if(privacyRect.startX <= privacyRect.endX){
						x1 = privacyRect.startX;
						x2 = privacyRect.endX;
					}
					else{
						x2 = privacyRect.startX;
						x1 = privacyRect.endX;
					}
					if(privacyRect.startY <= privacyRect.endY){
						y1 = privacyRect.startY;
						y2 = privacyRect.endY;
					}
					else{
						y2 = privacyRect.startY;
						y1 = privacyRect.endY;
					}

					x1=Math.ceil(x1*(videoSetup.RATIO_W));
					x2=Math.ceil(x2*(videoSetup.RATIO_W));
					y1=Math.ceil(y1*(videoSetup.RATIO_H));
					y2=Math.ceil(y2*(videoSetup.RATIO_H));
					//x3=Math.ceil(x3*(videoSetup.RATIO_W));
					//x4=Math.ceil(x4*(videoSetup.RATIO_W));
					//y3=Math.ceil(y3*(videoSetup.RATIO_H));
					//y4=Math.ceil(y4*(videoSetup.RATIO_H));
					if(x1 < 0){
						x1 = 0;
					}
					if(y1 < 0){
						y1 = 0;
					}
					if(x2 >= videoSetup.MAX_RESOLUTION_W){
						x2 = videoSetup.MAX_RESOLUTION_W-1;
					}
					if(y2 >= videoSetup.MAX_RESOLUTION_H){
						y2 = videoSetup.MAX_RESOLUTION_H-1;
					}
					if(videoSetup.IS_PTZ_SUPPORT){
						if(x1 != x2 && y1 != y2){						
							var polyXml="<StartPrivacyArea><Name>Test</Name><NumPoint>2</NumPoint><Point><X>"+x1+"</X><Y>"+y1+"</Y></Point><Point><X>"+x2+"</X><Y>"+y2+"</Y></Point></StartPrivacyArea>";
							ApplyMaskPolygon(polyXml,true);
						}else{
							videoSetup.cleanViewer();
						}						
					}else{
						videoSetup.setAreaPoly(x1,y1,x2,y2,x3,y3,x4,y4);
						$(".DisableAreaList" ).css("display","block");
						$("#poly-dialog").dialog("open");	
					}

					videoSetup.isDrawDragging = false;
				}
			});
			
			$('#imgTemp').bind('contextmenu', function(e){
				return false;
			});

			var isZoomSet = false;
			$('#zoomThreshold-dialog').dialog({
					position:{
						my: "right+10 bottom",
						at: "right+10 bottom",
						of: "#VideoSetup"
					},
					autoOpen: false,
					draggable: false,
					modal: true,
					close: function(){
						if(!isZoomSet){
							var tmpIndex =  $("#currentIndex").html();
							videoSetup.deleteArea(tmpIndex);
						}
						
						$(".DisableAreaList").css("display","none");
						$("input[name='privacyMaskStatus']").removeAttr("disabled");
						$("#privacy_color").removeAttr("disabled");
						$("#privacy_pattern").removeAttr("disabled");
					},
					open: function(event, ui){
						isZoomSet = false;
						$(".ui-widget-overlay").position({
							my: "top",
							at: "top",
							of: "#plugin_control_area"
						});
					},
					buttons: [{
						text: buttonLang[0],	//Ok
						click: function(event) {
							var rectXml="<ThresholdPrivacyArea><Index>"+$("#currentIndex").html()+"</Index><ZoomThreshold>1</ZoomThreshold></ThresholdPrivacyArea>";
							isZoomSet = true;
							ApplyPrivacyIndex(rectXml);

							$(this).dialog("close");
							$(".DisableAreaList").css("display","none");
						}
					}, {
					text: buttonLang[1],	//Cancel
					click: function() {
							isZoomSet = false;
							$(this).dialog("close");
							$(".DisableAreaList").css("display","none");
							$("input[name='privacyMaskStatus']").removeAttr("disabled");
							$("#privacy_color").removeAttr("disabled");
							$("#privacy_pattern").removeAttr("disabled");
						}
					}]
			});
		}
		else{
			var index=1;

			$("#imgTemp").click(function(e) {
				if($("#DisableVideoSetup").is(":visible")){
					return;
				}

				if($("#AreaNames").children().length >= areaNum){
					alert(videoSetup.msg_max_Privacyarea);
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
				
				if(index != 1 && lineDistance(Ax,Ay,xVal,yVal)<20) { return; }
				
				$(".DisableAreaList" ).css("display","block");
				
				if(index==1){
					c2.clearRect(0,0,canvas.width,canvas.height);
					c2.lineWidth = 2;
					c2.strokeStyle = "green";
					c2.globalAlpha="1"; 

					videoSetup.isDrawDragging=true;
					x1 = xVal,y1= yVal;
					Ax=xVal, Ay=yVal;// getting mouse move action
					index++;
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
					
					var polygonPoints = [[x1,y1],[x2,y2],[x3,y3],[x4,y4]];
						c2.moveTo(x3, y3);
						c2.lineTo(x4, y4);
						c2.stroke();
						c2.moveTo(x4, y4);
						c2.lineTo(x1, y1);
						c2.stroke();
						c2.closePath(); 
						
						c2.fillPolygon(polygonPoints, 'gray','green');
					
					context.clearRect(0, 0, canvas.width, canvas.height);
					videoSetup.isDrawDragging = false;
					$('#polyColor').prop('selectedIndex',0);
					videoSetup.setAreaPoly(x1,y1,x2,y2,x3,y3,x4,y4);
					//$("#poly-dialog").dialog('option', 'title', "Add : ["+videoSetup.areaCount+"]");
					$( "#poly-dialog" ).dialog("open");
					
					index=1;
					return;
				}
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

				if (videoSetup.isDrawDragging) {
					context.clearRect(0, 0, canvas.width, canvas.height);
					context.beginPath();
					context.moveTo(Ax, Ay);
					context.lineTo(xVal, yVal);
					context.stroke();
					context.closePath();
				}
			});

			$('#imgTemp').bind('contextmenu', function(e){
				if(videoSetup.isDrawDragging == true){
					context.clearRect(0, 0, canvas.width, canvas.height);
					videoSetup.cleanViewer();
					videoSetup.isDrawDragging = false;
					index = 1;
				}
			    return false;
			}); 	
			
		}
			
		$("#polyName").attr('maxLength',10);


		function GetAngleABC( a, b, c )
		{
			var ab={x:0,y:0};
			var ac={x:0,y:0};
			ab.x = b.x - a.x;
			ab.y = b.y - a.y;
			ac.x = b.x - c.x;
			ac.y = b.y - c.y;
			
			var dotabac = (ab.x * ab.y + ac.x * ac.y);
			var lenab = Math.sqrt(ab.x * ab.x + ab.y * ab.y);
			var lenac = Math.sqrt(ac.x * ac.x + ac.y * ac.y);
			
			var dacos = dotabac/lenab/lenac;

			var rslt = Math.acos(dacos);
			var rs = (rslt * 180) / 3.141592;
			return rs;
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
	},
	drawPolygonLine:function(Ax, Ay, Bx, By,index){
		bla = "";
		var lineLength = Math.sqrt( (Ax-Bx)*(Ax-Bx)+(Ay-By)*(Ay-By) );
		for( var i=0; i<lineLength; i++ )
		{
			bla += "<div class='currentPoly polygon"+index+"' style='left:"+ Math.round( Ax+(Bx-Ax)*i/lineLength  ) +"px;top:"+ Math.round( Ay+(By-Ay)*i/lineLength  ) +"px;'></div>";
		}
		document.getElementById("polyDraw").innerHTML += bla;
		
	},
	getArea:function(){
		
		var xml_data=$.parseXML(videoSetup.getAreaXML);
		$("#AreaNames").empty();
		var i=0;
		var loopCount=$(xml_data).find("Name").length;
		var t=0;
		this.areaCount=0;
		for(i=0;i<loopCount;i++)
		{
			var parentFound=$(xml_data).find("PrivacyArea"+i);
			var text = t+"&nbsp;: &nbsp;"+$(parentFound).find("Name").text()+"["+$(parentFound).find("Index").text()+"]";
			if($(parentFound).find("ZoomThreshold").text() == "1"){
				text += "<span style=\"color:black;font-weight:bold;\">[zoom]</span>";
			}
			var liText="<li><a href='javascript:void(0);' id='"+$(parentFound).find("Index").text()+"'>"+text+"</a></li>";
			
			if($(parentFound).find("NumPoint").text()!=0){
				$("#AreaNames").append(liText);
				t++;
				videoSetup.areaCount++;
			}
			
		};
		
		$("ul#AreaNames li a").click(function(e) {
			$("ul#AreaNames li a").removeClass("selArea");
			$(this).addClass("selArea");
		});	
	},
	setAreaPoly:function(x1,y1,x2,y2,x3,y3,x4,y4){
		if(this.drawType == this.TYPE_RECT){
			x1=Math.ceil(x1/(videoSetup.RATIO_W));
			x2=Math.ceil(x2/(videoSetup.RATIO_W));
			
			y1=Math.ceil(y1/(videoSetup.RATIO_H));
			y2=Math.ceil(y2/(videoSetup.RATIO_H));
										
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
						my: "right+10 bottom",
						at: "right+10 bottom",
						of: "#VideoSetup"
					},
					autoOpen: false,
					draggable: false,
					modal: true,
					title: title + " : ["+videoSetup.areaCount+"]",
					beforeClose: function( event, ui ) { c2.clearRect(0, 0, c.width, c.height);},
					close: function(){
						c2.clearRect(0, 0, c.width, c.height);
						$( this ).dialog( "close" );
						$("input[name='privacyMaskStatus']").removeAttr("disabled");
						$("#privacy_color").removeAttr("disabled");
						$("#privacy_pattern").removeAttr("disabled");
					},
					open: function(event, ui){
						$('#polyName').val("");
						$('#zoom_threshold_off').prop("checked", true);
						$(".ui-widget-overlay").position({
							my: "top",
							at: "top",
							of: "#plugin_control_area"
						});
					},
					buttons: [{
						text: buttonLang[0],	//Ok
						click: function(event) {   
							var name = $("#polyName").val();	   	   
							var regexp = /^[-.\a-zA-Z0-9]+$/;
							if (name && name.search(regexp) == -1)
							{ 
								alert(nameCheck);
								return false;
							}
							
							if(videoSetup.FLIP_MIRROR==1) { 
								y1=videoSetup.VIEWER_H-y1;
								y2=videoSetup.VIEWER_H-y2;
							}
							else if(videoSetup.FLIP_MIRROR==2) {
								x1=videoSetup.VIEWER_W-x1;
								x2=videoSetup.VIEWER_W-x2;
							}
							else if(videoSetup.FLIP_MIRROR==3) { 
								y1=videoSetup.VIEWER_H-y1;
								y2=videoSetup.VIEWER_H-y2;
								
								x1=videoSetup.VIEWER_W-x1;
								x2=videoSetup.VIEWER_W-x2;
							}

							if(videoSetup.ROTATE == 1)
							{
								var temp;
								temp = x1;
								x1 = y1;
								y1 = videoSetup.VIEWER_W -temp;
								temp = x2;
								x2 = y2;
								y2 = videoSetup.VIEWER_W -temp;							
							}
							else if(videoSetup.ROTATE == 3)
							{
								var temp;
								temp = y1;
								y1 = x1;
								x1 = videoSetup.VIEWER_H -temp;
								temp = y2;
								y2 = x2;
								x2 = videoSetup.VIEWER_H -temp;							
							}		

							if(x2 < x1){
								var temp;
								temp = x1;
								x1 = x2;
								x2 = temp;
							}
							if(y2 < y1){
								var temp;
								temp = y1;
								y1 = y2;
								y2 = temp;
							}
							
							x1=Math.ceil(x1*(videoSetup.RATIO_W));
							x2=Math.ceil(x2*(videoSetup.RATIO_W));
							y1=Math.ceil(y1*(videoSetup.RATIO_H));
							y2=Math.ceil(y2*(videoSetup.RATIO_H));

							if(x1 < 0){
								x1 = 0;
							}
							if(y1 < 0){
								y1 = 0;
							}
							if(videoSetup.ROTATE == 1 || videoSetup.ROTATE == 3){
								if(y2 >= videoSetup.MAX_RESOLUTION_W){
									y2 = videoSetup.MAX_RESOLUTION_W-1;
								}
								if(x2 >= videoSetup.MAX_RESOLUTION_H){
									x2 = videoSetup.MAX_RESOLUTION_H-1;
								}
							}else{
								if(x2 >= videoSetup.MAX_RESOLUTION_W){
									x2 = videoSetup.MAX_RESOLUTION_W-1;
								}
								if(y2 >= videoSetup.MAX_RESOLUTION_H){
									y2 = videoSetup.MAX_RESOLUTION_H-1;
								}
							}
							
							var polyXml = "";
							if(videoSetup.IS_PTZ_SUPPORT){
								polyXml="<SetPrivacyArea><Name>"+$("#polyName").val()+"</Name><NumPoint>2</NumPoint>";
								/*
								if($("#zoom_threshold_on").length > 0){		//detect zoom_threshold_on obj
									polyXml += "<ZoomThreshold>"+($("#zoom_threshold_on").is(":checked")? 1:0)+"</ZoomThreshold>";
								}
								*/
								polyXml +="<Point><X>"+x1+"</X><Y>"+y1+"</Y></Point><Point><X>"+x2+"</X><Y>"+y2+"</Y></Point></SetPrivacyArea>";
							}else{
								polyXml="<AddPrivacyArea>\
											<Name>"+$("#polyName").val()+"</Name>\
											<Color>"+$("#polyColor").val()+"</Color>\
											<NumPoint>2</NumPoint>\
											<Point><X>"+x1+"</X><Y>"+y1+"</Y></Point>\
											<Point><X>"+x2+"</X><Y>"+y2+"</Y></Point>\
										</AddPrivacyArea>";
							}
							ApplyMaskPolygon(polyXml,false);
							
							//removing once it is drwan
							c2.clearRect(0, 0, c.width, c.height);
							$(this).dialog("close");
						}
					}, {
					text: buttonLang[1],	//Cancel
					click: function() {
							c2.clearRect(0, 0, c.width, c.height);
							$(this).dialog("close");
							$('#zoom_threshold_off').prop("checked", true);
							$(".DisableAreaList").css("display","none");
							$("input[name='privacyMaskStatus']").removeAttr("disabled");
							$("#privacy_color").removeAttr("disabled");
							$("#privacy_pattern").removeAttr("disabled");
						}
					}]
			});

			if(videoSetup.ROTATE == 0){
				$("#poly-dialog").dialog({ position: { my: "right+10 bottom", at: "right+10 bottom", of: "#VideoSetup"} }); 
			}else{
				$("#poly-dialog").dialog({ position: { my: "right+150 bottom", at: "right+10 bottom", of: "#VideoSetup"} }); 
			}

		}
		else{
			$("#poly-dialog").dialog({
					autoOpen: false,
					draggable: false,
					modal: true,
					title: title + " : ["+videoSetup.areaCount+"]",
					beforeClose: function( event, ui ) { c2.clearRect(0, 0, c.width, c.height);},
					close: function(){
						c2.clearRect(0, 0, c.width, c.height);
						$( this ).dialog( "close" );
						$(".DisableAreaList").css("display","none");
						$("input[name='privacyMaskStatus']").removeAttr("disabled");
						$("#privacy_color").removeAttr("disabled");
						$("#privacy_pattern").removeAttr("disabled");	
					},
					open: function(event, ui){
						$('#polyName').val("");
						$(".ui-widget-overlay").position({
							my: "top",
							at: "top",
							of: "#plugin_control_area"
						});
	        			$(event.target).parent().position({
							my: "right+10 bottom",
							at: "right+10 bottom",
							of: "#VideoSetup"
						});
						$(".ui-dialog-titlebar-close").hide();						
					},
					buttons: [{
						text: buttonLang[0],	//Ok
						click: function(event) {   
							//alert($("#polyName").val());

							if(videoSetup.FLIP_MIRROR == 1) { 
								y1=videoSetup.VIEWER_H-y1;
								y2=videoSetup.VIEWER_H-y2;
								y3=videoSetup.VIEWER_H-y3;
								y4=videoSetup.VIEWER_H-y4;
							}
							else if(videoSetup.FLIP_MIRROR == 2) {
								x1=videoSetup.VIEWER_W-x1;
								x2=videoSetup.VIEWER_W-x2;
								x3=videoSetup.VIEWER_W-x3;
								x4=videoSetup.VIEWER_W-x4;
							}
							else if(videoSetup.FLIP_MIRROR == 3) { 
								y1=videoSetup.VIEWER_H-y1;
								y2=videoSetup.VIEWER_H-y2;
								y3=videoSetup.VIEWER_H-y3;
								y4=videoSetup.VIEWER_H-y4;
								
								x1=videoSetup.VIEWER_W-x1;
								x2=videoSetup.VIEWER_W-x2;
								x3=videoSetup.VIEWER_W-x3;
								x4=videoSetup.VIEWER_W-x4;
							}

							var name = $("#polyName").val();	   	   
							var regexp = /^[-.\a-zA-Z0-9]+$/;
							if (name && name.search(regexp) == -1)
							{ 
								alert(nameCheck);
								return false;
							}
							
							//videoSetup.setAreaPoly(x1,y1,x2,y2,x3,y3,x4,y4,$("#polyName").val(),$("#polyColor").val());
							
							//videoSetup.setAreaPoly(x1, y1, x2, y2,0,0,0,0,$("#polyName").val(),$("#polyColor").val());
						
							x1=Math.ceil(x1*(videoSetup.RATIO_W));
							x2=Math.ceil(x2*(videoSetup.RATIO_W));
							x3=Math.ceil(x3*(videoSetup.RATIO_W));
							x4=Math.ceil(x4*(videoSetup.RATIO_W));
							
							y1=Math.ceil(y1*(videoSetup.RATIO_H));
							y2=Math.ceil(y2*(videoSetup.RATIO_H));
							y3=Math.ceil(y3*(videoSetup.RATIO_H));
							y4=Math.ceil(y4*(videoSetup.RATIO_H));

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
							if(x3 < 0){
								x3 = 0;
							}
							if(y3 < 0){
								y3 = 0;
							}
							if(x4 < 0){
								x4 = 0;
							}
							if(y4 < 0){
								y4 = 0;
							}
							if(x1 >= videoSetup.MAX_RESOLUTION_W){
								x1 = videoSetup.MAX_RESOLUTION_W-1;
							}
							if(y1 >= videoSetup.MAX_RESOLUTION_H){
								y1 = videoSetup.MAX_RESOLUTION_H-1;
							}
							if(x2 >= videoSetup.MAX_RESOLUTION_W){
								x2 = videoSetup.MAX_RESOLUTION_W-1;
							}
							if(y2 >= videoSetup.MAX_RESOLUTION_H){
								y2 = videoSetup.MAX_RESOLUTION_H-1;
							}
							if(x3 >= videoSetup.MAX_RESOLUTION_W){
								x3 = videoSetup.MAX_RESOLUTION_W-1;
							}
							if(y3 >= videoSetup.MAX_RESOLUTION_H){
								y3 = videoSetup.MAX_RESOLUTION_H-1;
							}
							if(x4 >= videoSetup.MAX_RESOLUTION_W){
								x4 = videoSetup.MAX_RESOLUTION_W-1;
							}
							if(y4 >= videoSetup.MAX_RESOLUTION_H){
								y4 = videoSetup.MAX_RESOLUTION_H-1;
							}

							var polyXml="<AddPrivacyArea>\
											<Name>"+$("#polyName").val()+"</Name>\
											<Color>"+$("#polyColor").val()+"</Color>\
											<NumPoint>4</NumPoint>\
											<Point><X>"+x1+"</X><Y>"+y1+"</Y></Point>\
											<Point><X>"+x2+"</X><Y>"+y2+"</Y></Point>\
											<Point><X>"+x3+"</X><Y>"+y3+"</Y></Point>\
											<Point><X>"+x4+"</X><Y>"+y4+"</Y></Point>\
										</AddPrivacyArea>";
				
							ApplyMaskPolygon(polyXml,false);
							
							//removing once it is drwan

							$(this).dialog("close");
						}
					}, {
					text: buttonLang[1],	//Cancel
					click: function() {
							c2.clearRect(0, 0, c.width, c.height);
							$(this).dialog("close");
							$(".DisableAreaList").css("display","none");
							$("input[name='privacyMaskStatus']").removeAttr("disabled");
							$("#privacy_color").removeAttr("disabled");
							$("#privacy_pattern").removeAttr("disabled");
						}
					}]
			});
		}

	},
	selectPolygon:function(deleteIndex){
		if(this.drawType == this.TYPE_RECT){
			if(this.IS_PTZ_SUPPORT){
				var rectXml="<MovePrivacyArea><Index>"+deleteIndex+"</Index></MovePrivacyArea>";
				ApplyMove(rectXml);
			}else{
				var xml_data=$.parseXML(videoSetup.getAreaXML);
				var i=0;
				
				$(xml_data).find("Index").each(function(e) {
					if($(this).text()==deleteIndex)
					{
						var xmlSel=$(this).parents("PrivacyArea"+i);
						var x1=xmlSel.find("Point0 X").text(),x2=xmlSel.find("Point1 X").text();
						var y1=xmlSel.find("Point0 Y").text(),y2=xmlSel.find("Point1 Y").text();
						
						x1=Math.ceil(x1/(videoSetup.RATIO_W));
						x2=Math.ceil(x2/(videoSetup.RATIO_W));
						
						y1=Math.ceil(y1/(videoSetup.RATIO_H));
						y2=Math.ceil(y2/(videoSetup.RATIO_H));

						if(videoSetup.ROTATE == 1)
						{
							var temp;
							temp = y1;
							y1 = x1;
							x1 = videoSetup.VIEWER_W -temp;
							temp = y2;
							y2 = x2;
							x2 = videoSetup.VIEWER_W -temp;							
						}
						else if(videoSetup.ROTATE == 3)
						{
							var temp;
							temp = x1;
							x1 = y1;
							y1 = videoSetup.VIEWER_H -temp;
							temp = x2;
							x2 = y2;
							y2 = videoSetup.VIEWER_H -temp;							
						}						
						
						if(videoSetup.FLIP_MIRROR==1) { 
							y1=videoSetup.VIEWER_H-y1;
							y2=videoSetup.VIEWER_H-y2;
						}
						else if(videoSetup.FLIP_MIRROR==2) {
							x1=videoSetup.VIEWER_W-x1;
							x2=videoSetup.VIEWER_W-x2;
						}
						else if(videoSetup.FLIP_MIRROR==3) { 
							y1=videoSetup.VIEWER_H-y1;
							y2=videoSetup.VIEWER_H-y2;
							
							x1=videoSetup.VIEWER_W-x1;
							x2=videoSetup.VIEWER_W-x2;
						}

						c2.clearRect(0,0,canvas.width,canvas.height);
						c2.strokeStyle = "#00ffff";
						c2.lineWidth = 2;
						c2.globalAlpha="1";
						c2.strokeRect(x1,y1,x2-x1,y2-y1);

						/*	rectangle
						x2 = x2 - x1;
						y2 = y2 - y1;
						c2.strokeRect(x1,y1,x2,y2);
						*/
						return false;
					}
					i++;
				});
			}
		}else{			//poly type
			c2.clearRect(0, 0, c.width, c.height);
			c2.lineWidth = 2;
			c2.strokeStyle = "#00ffff";
		
			var xml_data=$.parseXML(videoSetup.getAreaXML);
			var i=0;
			
			$(xml_data).find("Index").each(function(e) {
				if($(this).text()==deleteIndex)
				{
					var xmlSel=$(this).parents("PrivacyArea"+i);
					var x1=xmlSel.find("Point0 X").text(),x2=xmlSel.find("Point1 X").text(),x3=xmlSel.find("Point2 X").text(),x4=xmlSel.find("Point3 X").text();
					var y1=xmlSel.find("Point0 Y").text(),y2=xmlSel.find("Point1 Y").text(),y3=xmlSel.find("Point2 Y").text(),y4=xmlSel.find("Point3 Y").text();
					
					x1=Math.ceil(x1/(videoSetup.RATIO_W));
					x2=Math.ceil(x2/(videoSetup.RATIO_W));
					x3=Math.ceil(x3/(videoSetup.RATIO_W));
					x4=Math.ceil(x4/(videoSetup.RATIO_W));
					
					y1=Math.ceil(y1/(videoSetup.RATIO_H));
					y2=Math.ceil(y2/(videoSetup.RATIO_H));
					y3=Math.ceil(y3/(videoSetup.RATIO_H));
					y4=Math.ceil(y4/(videoSetup.RATIO_H));
					

					if(videoSetup.FLIP_MIRROR==1) { 
						y1=videoSetup.VIEWER_H-y1;
						y2=videoSetup.VIEWER_H-y2;
						y3=videoSetup.VIEWER_H-y3;
						y4=videoSetup.VIEWER_H-y4;
					}
					else if(videoSetup.FLIP_MIRROR==2) {
						x1=videoSetup.VIEWER_W-x1;
						x2=videoSetup.VIEWER_W-x2;
						x3=videoSetup.VIEWER_W-x3;
						x4=videoSetup.VIEWER_W-x4;
					}
					else if(videoSetup.FLIP_MIRROR==3) { 
						y1=videoSetup.VIEWER_H-y1;
						y2=videoSetup.VIEWER_H-y2;
						y3=videoSetup.VIEWER_H-y3;
						y4=videoSetup.VIEWER_H-y4;
						
						x1=videoSetup.VIEWER_W-x1;
						x2=videoSetup.VIEWER_W-x2;
						x3=videoSetup.VIEWER_W-x3;
						x4=videoSetup.VIEWER_W-x4;
					}

					c2.beginPath();	
					c2.moveTo(x1, y1);c2.lineTo(x2, y2);c2.stroke();
					c2.moveTo(x2, y2);c2.lineTo(x3, y3);c2.stroke();
					c2.moveTo(x3, y3);c2.lineTo(x4, y4);c2.stroke();
					c2.moveTo(x4, y4);c2.lineTo(x1, y1);c2.stroke();
					c2.closePath();

					/*	rectangle
					x2 = x2 - x1;
					y2 = y2 - y1;
					c2.strokeRect(x1,y1,x2,y2);
					*/
					return false;
				}
				i++;
			});
		}
	},
	deleteArea:function(index){
		
		var rectXml="<RemovePrivacyArea><Index>"+index+"</Index></RemovePrivacyArea>";
		this.areaCount--;
		ApplyPrivacyIndex(rectXml);
	},
	cleanViewer:function(){
		c2.clearRect(0, 0, c.width, c.height);
		$("#DisableVideoSetup").css("display","none");
		$(".DisableAreaList").css("display","none");

	}
	
};

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

function lineIntersect(x1,y1,x2,y2, x3,y3,x4,y4) {
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
		
