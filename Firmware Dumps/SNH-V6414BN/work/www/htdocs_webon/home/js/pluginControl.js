//var isClick = false;
//var areazoomStatus = false;
//var SISOPlugin = null;
var ptzSpeedVal = 3;
//var ptzSlideStatus = 0;

$(document).ready(function(){
	var sliderMouseDown = function (e) { // disable clicks on track
		 var sliderHandle = $('#ptzSpeed').find('.ui-slider-handle');
		 if (e.target != sliderHandle[0]) {
			  e.stopImmediatePropagation();
		 }
	};
	var isStartzoomSlider = false;
	$('#ptzSpeed')
		.on('mousedown', sliderMouseDown)
		.on('touchstart', sliderMouseDown)
		.slider({
			orientation: "vertical",
			min: -100,
			max: 100,
			value: 8,
			range: "min",
			slide: function( event, ui ) {
				if(isStartzoomSlider || BrowserDetect.browser != "Explorer"){
					ptzSpeedVal = ui.value;
					if(ptzSpeedVal > 0) {
						SISOPlugin.pluginObj.SetPTZExtension(1);
						SISOPlugin.pluginObj.ZoomIn(parseInt(ptzSpeedVal));
						this.isClick = true;
					} else if(ptzSpeedVal < 0) {
						SISOPlugin.pluginObj.SetPTZExtension(1);
						SISOPlugin.pluginObj.ZoomOut(parseInt(ptzSpeedVal*-1));
						this.isClick = true;
					} else if(ptzSpeedVal == 0) {
						if(this.isClick == true) {
							SISOPlugin.pluginObj.SetPTZExtension(1);
							SISOPlugin.pluginObj.PtzStop(0);
							this.isClick = false;
						}
					}
					$('#Plus-Btn').css('display', 'none');
					$('#Plus-Btn-Disable').css('display', 'block');
					$('#Minus-Btn').css('display', 'none');
					$('#Minus-Btn-Disable').css('display', 'block');
				}
				isStartzoomSlider = true;
			},
			stop: function( event, ui ) {
				isStartzoomSlider = false;
				if(this.isClick == true) {
					SISOPlugin.pluginObj.SetPTZExtension(1);
					SISOPlugin.pluginObj.PtzStop(0);
					this.isClick = false;
				}
				$('#ptzSpeed').slider("value", 8);		
				
				$('#Plus-Btn').css('display', 'block');
				$('#Plus-Btn-Disable').css('display', 'none');
				$('#Minus-Btn').css('display', 'block');
				$('#Minus-Btn-Disable').css('display', 'none');
			}
		});
		

	var isDrag = false; 
	var isMove = false;
	var countUp = 0;
	var countDown = 0;
	var animateDuration = 50;
	var PAN_RATIO = 1.205;
	var TILT_RATIO = 1.755;
	
	$('#Move-Btn').draggable({
		drag: function() {
			isDrag = true;
			isMove = false;
			countDown = 0;
			var offset = $(this).position();
			var xPos = (offset.left);
			var yPos = -(offset.top);
			xPos *= PAN_RATIO;
			yPos *= TILT_RATIO;
			if (-4 < yPos && yPos < 4) yPos = 0;
			if (-2 < xPos && xPos < 2) xPos = 0;
			SISOPlugin.ptzControl.setAreaZoom(xPos, yPos, 0, 2);
		},
		containment: "#MOVEArea",
		revert: false,
		revertDuration: animateDuration,
		stop: function(e){
			$('body').trigger("mouseup");
		}
	}).on("contextmenu",function(e){
		return false;
	});

	$('#MOVEArea').mousedown(function(e){
		if(isDrag || isMove || e.which != 1)
			return;
		if(countDown != 0 || countUp != 0)
			return;
		
		countDown++;
		isMove = true;
		var jogWidth = $('#Move-Btn').width()/2;									// 12

		var moveAreaPos = $('#MOVEArea').offset();												// top:483, left: 20
		var moveAreaWidth = $('#MOVEArea').width();											// 240
		var moveAreaHeight = $('#MOVEArea').height();											// 148
		
		var jogPos = $('#Move-Btn').offset();										// top:545, left: 128
		
		var jog_Left = jogPos.left + jogWidth;
		var jog_Top = jogPos.top + jogWidth;
		
		var xPos = e.pageX;
		var yPos = e.pageY;
		
		if (window.navigator.msPointerEnabled) {		//Detect IE10 or IE11
			if($(window).scrollLeft() != 0 && e.pageX == e.clientX){
				xPos = xPos + $(window).scrollLeft();
			}
			if($(window).scrollTop() != 0 && e.pageY == e.clientY){
				yPos = yPos + $(window).scrollTop();
			}
		}
		if(xPos <= (moveAreaPos.left + jogWidth))												// 32 = 20 + 12
			xPos = (moveAreaPos.left + jogWidth);
		else if(xPos >= (moveAreaWidth + moveAreaPos.left - jogWidth))					// 248 = 240 + 20 - 12
			xPos = moveAreaWidth + moveAreaPos.left - jogWidth;

		if(yPos <= (moveAreaPos.top + jogWidth)) 												// 495 = 483 + 12
			yPos = moveAreaPos.top + jogWidth; 
		else if(yPos >= (moveAreaPos.top + moveAreaHeight - jogWidth)) 					// 619 = 483 + 148  - 12
			yPos = moveAreaPos.top + moveAreaHeight - jogWidth;

		xPos = xPos- jog_Left;
		yPos = jog_Top - yPos;
		if (-4 <= xPos && xPos <= 4) xPos = 0;
		if (-2 <= yPos && yPos <= 2) yPos = 0;
		$('#Move-Btn').animate({
			top: -yPos,
			left: xPos
		}, animateDuration, function() {
			xPos *= PAN_RATIO;
			yPos *= TILT_RATIO;		
			SISOPlugin.ptzControl.setAreaZoom(xPos, yPos, 0, 2);
		});
		
		e.preventDefault();
		window.clearTimeout(window.downTimer);
    	window.downTimer = window.setTimeout(function(){
			$('#Move-Btn').trigger(e);
    	}, animateDuration);

		countDown = 0;
	}).on("contextmenu",function(e){
		return false;
	});

	$('body').mouseup(function(e) {
		if(countUp != 0 || countDown != 0)
			return;
		if(isDrag == false && isMove == false)
			return;

		window.clearTimeout(window.downTimer);
		countUp++;
		
		$('#Move-Btn').animate({
			top: 0,
			left: 0
		}, {complete: function(){
				isDrag = false;
				isMove = false;
				countUp = 0;
				SISOPlugin.ptzControl.ptzStop(1);
		}, duration:animateDuration});
		e.preventDefault();
	});


	if(BrowserDetect.browser == 'Chrome') {
		$(window).on('beforeunload', function(){
			SISOPlugin.onPluginUnload();
		});
	}
	else {
		$(window).on('unload', function() {
			SISOPlugin.onPluginUnload();
		});
	}
});


SISOPlugin = {};

SISOPlugin = {
	MIN_PLUGIN_VER: 170, // for Windows plugin
	pluginObj: null,
	
	init: function(installMsg, viewerWidth, viewerHeight){
		if(!this.isBrowserSupportPlugin()){
			msg = "<label id=\"plugin\">"+installMsg[2]+"</label>"
			$('#pluginArea').html(msg);
			return;
		}
		// draw plugin area
		var msg="";
		if(BrowserDetect.browser == "Explorer") { // activex
			if (typeof plugins.sisoplugin == 'undefined'){
				if(getIEVersion() >= 11){
					var winWidth = window.innerWidth;
					var winHeight = window.innerHeight;
					$("body").css("overflow","hidden");
					$("body").append("<div style=\"position:absolute; top: 0px; left:0px; width:"+winWidth+"px; height:"+winHeight+"px; background-color:#000000; z-index:1000; filter:alpha(opacity=0.5); opacity:0.5; -moz-opacity:0.5; -ms-filter: 'progid:DXImageTransform.Microsoft.Alpha(Opacity=50)';\"></div>");

					var r = confirm(installMsg[1]);
					if(r){
						location.replace('/home/webviewerinstall.cgi');
					}
					return;
				}else{
					location.replace('/home/webviewerinstall.cgi');
					return;
				}
			}else{
				msg += "<object style=\'z-index:10\' id=\'plugin\' width=\""+viewerWidth+"\" height=\""+viewerHeight+"\"";
				msg += "classid=\"clsid:58930875-5F98-4151-B894-A7A3EA94ABC8\">";
				msg += "<a class='pluginInstall' href='./STWWebViewer.exe'>";
				msg += "<br />"+installMsg[0]+"</a>";
				msg += "</object>";
			}
		}
		else {		// npapi
			if(typeof plugins['webviewer'] == 'undefined'){
				location.replace('/home/webviewerinstall.cgi');
				return;
			}else{
				msg += "<object style=\'z-index:10\' type=\"application/WebViewer-plugin\" width=\""+viewerWidth+"\" height=\""+viewerHeight+"\" id='plugin'>";
				if(BrowserDetect.OS == "Mac")
					msg += "<a class='pluginInstall' href='./STWWebviewer.pkg'>";
				else
					msg += "<a class='pluginInstall' href='./STWWebViewer.exe'>";
				msg += "<br />"+installMsg[0]+"</a>";
				msg += "</object>";
			}
		}
		$('#pluginArea').html(msg);			//need to add  <span id="pluginArea"></span>
		
		// initialize plugin object instance
		try {
			this.pluginObj = document.getElementById("plugin");
		}
		catch (err) { alert(err); }

		if(BrowserDetect.OS == "Mac")
		{
			this.MIN_PLUGIN_VER = 145; // for Mac plugin
		}

		var version;
		try {
			version = this.pluginObj.GetCurrentVersion();
		}
		catch (err) {  }

		if(version < this.MIN_PLUGIN_VER)
		{
		  	location.replace('/home/webviewerinstall.cgi');
		}
	},
	isBrowserSupportPlugin: function()
	{
		var supported = null;
	   	var errorName = null;
	   	
		try {
			new ActiveXObject("");
		}
		catch (e) {
			// FF has ReferenceError here
			errorName = e.name; 
		}     
		try {
			supported = !!new ActiveXObject("htmlfile");
		} catch (e) {
			supported = false;
		}
		if(errorName != 'ReferenceError' && supported==false){
			supported = false;
		}else{
			supported =true;
		}
		return supported;
	},
	startPluginPlay: function(devicePort,previewProfileNo,encName,encPW)
	{
		this.setSecurityEnhancement();
		//this.setPTZExtension(1);
		this.livePlay(location.hostname, devicePort, previewProfileNo, encName, encPW);
		this.setResolution(viewerWidth, viewerHeight);
	},

	/* *********** DEV_S1WEBVIEWER start **************** */
	startS1PluginPlay: function(devicePort,previewProfileNo,encName,encPW,isNoEnc)
	{
		this.setSecurityEnhancement();
		this.setIsNoVideoEncrypt(isNoEnc);
		//this.setPTZExtension(1);
		this.livePlay(location.hostname, devicePort, previewProfileNo, encName, encPW);
		this.setResolution(viewerWidth, viewerHeight);
	},
	/* *********** DEV_S1WEBVIEWER END **************** */

	enableLowAudioBuffer: function()
	{
		this.pluginObj.EnableLowAudioBuffer();
	},
	setSecurityEnhancement: function()
	{
		this.pluginObj.SetSecurityEnhancement();
	},

	/* *********** DEV_S1WEBVIEWER start **************** */
	setIsNoVideoEncrypt: function(isNoEnc)
	{
		this.pluginObj.SetIsNoVideoEncrypt(isNoEnc);
	},
	/* *********** DEV_S1WEBVIEWER END **************** */

	livePlay: function(hostName, devicePort, currProfile, userName, userPW)
	{
		this.pluginObj.LivePlay(hostName, parseInt(devicePort), parseInt(currProfile), userName, userPW);
	},
	setPTZExtension: function(num)
	{
		this.pluginObj.SetPTZExtension(num);
	},
	setResolution: function(width, height)
	{
		var resolWidth = parseInt(width,10);
		var resolHeight = parseInt(height,10);
		this.pluginObj.SetResolution(resolWidth, resolHeight);
		this.pluginObj.width = resolWidth;
		this.pluginObj.height = resolHeight;
	},
	getRelayStatus: function(index)
	{
		return this.pluginObj.GetRelayStatus(index);
	},
	setRelayStatus: function(relayStatus)
	{
		this.pluginObj.SetRelayStatus(relayStatus[0], relayStatus[1], relayStatus[2], relayStatus[3]);
	},
	getVNPResCode: function()
	{
		return this.pluginObj.GetVNPResCode();
	},
	setVolume: function(volume)
	{
		this.pluginObj.SetVolume(volume)
	},
	makeBrowserFullScreen: function(isFullScreen)
	{
		this.pluginObj.MakeBrowserFullScreen(isFullScreen);
	},
	stop: function()
	{
		this.pluginObj.Stop();
	},
	changeProfile: function(profileNum)
	{
		this.pluginObj.ChangeProfile(profileNum);
	},
	stopAudio: function()
	{
		this.pluginObj.StopAudio();
	},
	saveSnapShot: function()
	{
		this.pluginObj.SaveSnapShot();
	},
	saveSnapShotNoDialog: function(fileName)
	{
		this.pluginObj.SaveSnapShotNoDialog(fileName);
	},
	startTalk: function()
	{
		this.pluginObj.StartTalk();
	},
	stopTalk: function()
	{
		this.pluginObj.StopTalk();
	},
	startAudio: function()
	{
		this.pluginObj.StartAudio();
	},
	stopAudio: function()
	{
		this.pluginObj.StopAudio();
	},
	doOverlay: function(num)
	{
		this.pluginObj.DoOverlay(num);
	},
	drawIVLine: function(x1,y1,x2,y2,left,right)
	{
		this.pluginObj.DrawIVLine(x1,y1,x2,y2,left,right)
	},
	drawIVArea: function(posX1, posY1, posX2, posY2, posX3, posY3, posX4, posY4)
	{
		this.pluginObj.DrawIVArea(parseInt(posX1), parseInt(posY1), parseInt(posX2), parseInt(posY2), parseInt(posX3), parseInt(posY3), parseInt(posX4), parseInt(posY4));
	},
	onPluginUnload: function()
	{
		if (typeof this.pluginObj == "undefined" || this.pluginObj == null) return;
		this.pluginObj.Stop();
		if(BrowserDetect.browser == "Explorer")
			this.pluginObj.Release();
	},
	browseFirmwareImage: function()
	{
		this.pluginObj.browseFirmwareImage();
	},
	firmwareUpgrade: function(hostName, devicePort, encName, encPW)
	{
		this.pluginObj.firmwareUpgrade(hostName, devicePort, encName, encPW);
	},
	onClickBackupConfiguration: function(hostName,encName, encPW)
	{
		var result = this.pluginObj.OnClickBackupConfiguration(hostName,encName, encPW);
		return result;
	},
	playbackBackup: function(hostName,encName, encPW,data)
	{
		var result = this.pluginObj.playbackBackup(hostName,encName, encPW,data);
		return result;	
	},
	startLocalRecording: function(fileName)
	{
		var result = this.pluginObj.StartLocalRecording(fileName);
		return result;
	},
	stopLocalRecording: function()
	{
		this.pluginObj.StopLocalRecording("aa"); // dummy param. don't care of that.
	}
}

SISOPlugin.ptzControl = {
	isClick: false,
	areazoomStatus: false,
	ptzSlideStatus: 0,
	
	setAreaZoom: function(xPos, yPos)
	{
		SISOPlugin.pluginObj.SetPTZExtension(1);
		SISOPlugin.pluginObj.SetAreaZoom(parseInt(xPos), parseInt(yPos), 0, 2);
	},
	ptzStop: function(num)
	{
		SISOPlugin.pluginObj.SetPTZExtension(1);
		SISOPlugin.pluginObj.PtzStop(num);
	},
	onClickPtzStop: function(mode) 
	{
		SISOPlugin.pluginObj.SetPTZExtension(1);
		var PTZSPEED = parseInt($("#ptzSpeed").slider("option","value"));
		
		if(typeof mode != 'undefined' || this.isClick == true){
			SISOPlugin.pluginObj.PtzStop(PTZSPEED);
			this.isClick = false;
		}
	},
	onClickPresetMove: function() 
	{
		var presetnum = parseInt($("#ptzPresetNo").get(0).value);
		
		SISOPlugin.pluginObj.SetPTZExtension(1);
		SISOPlugin.pluginObj.MovePreset(presetnum, "aaa");

	},
	onClickZoom: function(mode, type) 
	{
		SISOPlugin.pluginObj.SetPTZExtension(1);
		var PTZSPEED;

		if(type=='btn'){
			PTZSPEED = 50;
		}
		else if(type=='slider') {
			PTZSPEED = parseInt($("#ptzSpeed").slider("option", "value"));
			if(PTZSPEED < 0) {PTZSPEED = -(PTZSPEED);}
		}
	
		eval("SISOPlugin.pluginObj.Zoom"+mode+"(parseInt(PTZSPEED));");
		this.isClick = true;
	},
	onClickFocus: function(mode) 
	{
		SISOPlugin.pluginObj.SetPTZExtension(1);
		var PTZSPEED = parseInt($("#ptzSpeed").slider("option","value"));
				
		eval("SISOPlugin.pluginObj.SetFocus"+mode+"(parseInt(PTZSPEED));");
		
		this.isClick = true;
	},
	btnPtzAreazoomPreview: function()
	{
		if (this.areazoomStatus == true)
		{
			SISOPlugin.pluginObj.SetAreaZoom(0, 0, 0, 10);
		}
		else
		{
			//do nothing
		}
	},
	btnPtzAreazoomForward: function()
	{
		if (this.areazoomStatus == true)
		{
			SISOPlugin.pluginObj.SetAreaZoom(0, 0, 0, 11);
		}
		else
		{
			//do nothing
		}
	},
	btnPtzAreazoomActive: function()
	{
		if (this.areazoomStatus == true)
		{
			SISOPlugin.pluginObj.SetAreaZoom(0, 0, 0, 0);
			this.areazoomStatus = false;
		}
		else
		{
			SISOPlugin.pluginObj.SetAreaZoom(0, 0, 0, 1);
			this.areazoomStatus = true;
		}
	},
	btnPixelCounter: function(val)
	{
		if (val == 1)
		{
			SISOPlugin.pluginObj.SetAreaZoom(0, 0, 0, 20);
		}
		else
		{
			SISOPlugin.pluginObj.SetAreaZoom(0, 0, 0, 0);
		}
	},

	btnPtzAreazoomGoto1x: function()
	{
		if (this.areazoomStatus == true)
		{
			SISOPlugin.pluginObj.SetAreaZoom(0, 0, 0, 12);
		}
		else
		{
			//do nothing
		}
	},
	manualRecordingBtnColorChange: function(status) 
	{
		if (status)
		{	
			ChangeImage('btnManualRecording', './images/common/VIEW/rec_press.png');
		}
		else 
		{
			ChangeImage('btnManualRecording', './images/common/VIEW/rec_normal.png');
		}
		
	},
	areazoomBtnColorChange: function(param)
	{
		var path = '../';
		if (typeof param != "undefined") path = './';
							
		if(this.areazoomStatus)
		{
			ChangeImage('btnAreaZoom', path+'images/common/PTZ/areazoom_press.png');
			this.areazoomStatus = 1;
		}
		else
		{
			ChangeImage('btnAreaZoom',path+'images/common/PTZ/areazoom_normal.png');
			this.areazoomStatus = 0;
		}
	},
	onClickBLCStatus: function(){
		if (this.ptzSlideStatus == 1 && $("#blc_mode").val() == 1) {	
			$('#blcbox').show();
			
		} else {
			$('#blcbox').hide();
		}
	},
	onClickPTZSlide: function()
	{
		if (this.ptzSlideStatus == 0) {	
			$('.ptzControl').show();
			$('#showBtn').hide();
			$('#hideBtn').show();
			if($("#blc_mode").val() == 1)	$('#blcbox').show();
			else						 	$('#blcbox').hide();
			ChangeImage('imgSlidePTZ', '../images/common/PTZ/hide.png');
		}
		else {							
			$('.ptzControl').hide();
			$('#showBtn').show();
			$('#hideBtn').hide();
			$('#blcbox').hide();
			ChangeImage('imgSlidePTZ', '../images/common/PTZ/show.png');
		}
		this.ptzSlideStatus = (this.ptzSlideStatus ? 0 : 1);
	}
}

SISOPlugin.externalPtz = {
	isClick: false,
	ptzCmd : {"stop":0, "up":1, "down":2, "left":3, "right":4, "upLeft":5, "upRight":6, "downLeft":7, "downRight":8, "zoomIn":9, "zoomOut":10, "near":11, "far":12},
	control : function(ptzSpeed, cmd){
		var val = parseInt(ptzSpeed, 10);
		switch(cmd){
			case this.ptzCmd.stop: {
				if(this.isClick){
					SISOPlugin.pluginObj.PtzStop(val);
					this.isClick = false;
				}
				break;
			}			
			case this.ptzCmd.up: SISOPlugin.pluginObj.PtzUp(val); this.isClick = true; break;
			case this.ptzCmd.down: SISOPlugin.pluginObj.PtzDown(val); this.isClick = true; break;
			case this.ptzCmd.left: SISOPlugin.pluginObj.PtzLeft(val); this.isClick = true; break;
			case this.ptzCmd.right: SISOPlugin.pluginObj.PtzRight(val); this.isClick = true; break;
			case this.ptzCmd.upLeft: SISOPlugin.pluginObj.PtzUpLeft(val); this.isClick = true; break;
			case this.ptzCmd.upRight: SISOPlugin.pluginObj.PtzUpRight(val); this.isClick = true; break;
			case this.ptzCmd.downLeft: SISOPlugin.pluginObj.PtzDownLeft(val); this.isClick = true; break;
			case this.ptzCmd.downRight: SISOPlugin.pluginObj.PtzDownRight(val); this.isClick = true; break;
			case this.ptzCmd.zoomIn: SISOPlugin.pluginObj.ZoomIn(val); this.isClick = true; break;
			case this.ptzCmd.zoomOut: SISOPlugin.pluginObj.ZoomOut(val); this.isClick = true; break;
			case this.ptzCmd.near: SISOPlugin.pluginObj.SetFocusNear(val); this.isClick = true; break;
			case this.ptzCmd.far: SISOPlugin.pluginObj.SetFocusFar(val); this.isClick = true; break;
		}
	}
}
/*
function OnClickPtzMoveButton(direction)
{
	var PTZSPEED = parseInt($("#ptzSpeed").slider("option","value"));
	if(typeof SISOPlugin == 'undefined')
	{
		var control = document.getElementById("viewer");
		eval("control.content.ViewerControl.Ptz"+direction+"(PTZSPEED);");
	}
	else
	{
		eval("SISOPlugin.Ptz"+direction+"(PTZSPEED);");
	}
	isClick = true;
}
*/

function AuxBtnColorChange(param)
{
	var path = '../';
	if (typeof param != "undefined") path = './';

	if(auxStatus == 0)
	{
//		ChangeImage('btnAux', path+'images/common/PTZ/aux.png');
	}
	else
	{
//		ChangeImage('btnAux', path+'images/common/PTZ/aux_blue.png');
	}
}


function OnClickAutoTracking(mode)
{
	var msg = "";
	msg += "<StartTrackingTargetlock>";
	msg += "<AutoTrack>"+mode+"</AutoTrack>";
	msg += "</StartTrackingTargetlock>";
	RequestAjaxMsg(msg, '', ajaxReqUrl, 'NO_REFRESH');
}

function OnClickAutoFocus()
{
	var msg = "";
	msg += "<StartPTZInstantAF>";
	msg += "<Index>0</Index>";
	msg += "</StartPTZInstantAF>";
	RequestAjaxMsg(msg, '', ajaxReqUrl, 'NO_REFRESH');
}
