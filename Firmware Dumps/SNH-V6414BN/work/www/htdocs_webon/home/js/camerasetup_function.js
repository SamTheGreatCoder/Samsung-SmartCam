var keyCode = "";
var TEST = 1;
var SAVE = 0;
var timer;
var setupState = 1;
var isApplying = 0;
var isOnloading = false;
var selNo = 0;
var oldSelNo = 0;

var blc_top = 0;
var blc_bottom = 0;
var blc_right = 0;
var blc_left = 0;

function ControlSlider(name,cmd)
{
	var id = "#" + name;
	var value;
	var max;
	var min;
	
	value = parseInt($(id).slider( "option", "value" ));
	if(name.substr(0, 3) == "blc"){
		max =  $(id).slider( "option", "limitMax" );
		min = $(id).slider( "option", "limitMin" );
	}
	else{
		max =  $(id).slider( "option", "max" );
		min = $(id).slider( "option", "min" );
	}

	if(cmd == "left"){
		if(name == "iris_piris_pos" && value > 2){
			value = parseInt($("#iris_piris_pos_value").text(),10) - 2;
		}
		else
		{
			value -= 1;
		}
	}
	else {
		if(name == "iris_piris_pos" && value > 1){
			value = parseInt($("#iris_piris_pos_value").text(),10) + 2;
		}
		else
		{
			value += 1;
		}
	}
	if(value >= min && value <= max){
		if(name == "iris_piris_pos"){
			pirisVal = value;
			DrawPIrisValue();		//exposure_tab.cgi
			$(id).slider("option","value",value);
			$(id + "_value").html($(id).slider( "option", "value" ));
			SetPIris_Fno(parseInt($("#iris_piris_pos_value").text(),10));		//exposure_tab.cgi
		}
		else
		{
			$(id).slider("option","value",value);
			$(id + "_value").html($(id).slider( "option", "value" ));
		}
	}
	
	if(name.substr(0, 3) == "blc"){
		SetBlcRange(name,$(id).slider("option","value"));	//backlight_tab.cgi
	}
}

function MoveTapLink(tapId)
{		
	switch(tapId){
		case "imagepreset" :
			$("#camera_tabs").tabs("option","active", "0");
			break;
		case "daynight" :		
			$("#camera_tabs").tabs("option","active", "5");
			break;
	};
}

function SetTimeOut()
{
	if(!isOnloading){
  		if(setupState == 1){
  			OnClickApply(TEST);
  			setupState = 2;
  		} else if(setupState == 2){
  			setupState = 3;
  		}
  	}
}

function OnChangeCamTitle() 
{
	var val = 0;
	if ((keyCode == 8) || (keyCode == 45) || (keyCode == 46) 
			|| (keyCode > 47 && keyCode < 58)
			|| (keyCode > 64 && keyCode < 91)
			|| (keyCode > 96 && keyCode < 123)) {
	}
	else{
		return;
	}
	OnChangeTitleTimeMode('title');
}

function OnCheckValue(event)
{
	if(window.event){ 	//ie,crome, safari
		keyCode = event.keyCode;
	} else { 				//firefox	
		keyCode = event.which;
	}
	if ((keyCode == 8) || (keyCode == 45) || (keyCode == 46) 
			|| (keyCode > 47 && keyCode < 58)
			|| (keyCode > 64 && keyCode < 91)
			|| (keyCode > 96 && keyCode < 123)) {
	}
	else {
		if(window.event){ //ie
			event.returnValue = false; 
			try{
				event.preventDefault();
			}catch(err){
			
			}
		}
		else{
			event.preventDefault();
		}
	}
}

function OnCamTitleKeydown(event)
{
	if(window.event){ 	//ie,crome, safari
		keyCode = event.keyCode;
	} else { 				//firefox
		keyCode = event.which;
	}
}

function SetPtzBLcButtonHoverFunction(isDisable, name)
{
	var splitValue = name.split('_');
	var direction = splitValue[splitValue.length-1];
	var path1='', path2='';
	var targetName = name.substring(0, (name.lenght-direction.lenght+2));
	var path = '../images/common/btn/backlight_'+direction+'_';
	
	if (isDisable == false) {
		path1 = path+'press.png';
		path2 = path+'normal.png';
		$("#"+name).hover(function(){ ChangeImage(name,path1); }, function(){ ChangeImage(name,path2); }).click(function(){ OnClickBLCRange(targetName,direction); });	
	}
	else {
		path1 = path+'normal.png';
		path2 = path+'normal.png';
		$("#"+name).hover(function(){ ChangeImage(name,path1); }, function(){ ChangeImage(name,path2); }).unbind('click');
	}
}

function InitCameraSetupSlider(name, minVal, maxVal, val)
{
	$("#"+name).slider({
		orientation: "horizontal",
		min: minVal,
		max: maxVal,
		value: val,
		range: "min",
		slide: function( event, ui ) {
			$("#"+name+"_value").html(ui.value);
		},
		change: function(event, ui) {
			SetTimeOut();
		},
		stop: function(event, ui) {

		}
	});
	$("#"+name+"_value").html($("#"+name).slider("value"));
}

