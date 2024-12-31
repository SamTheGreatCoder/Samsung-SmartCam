
function isSupportedBrowser(){
	//console.log("Detecting Browser Agent");  //throws error on IE8
	var supportedBrowser = ["Chrome","Safari","Explorer","Firefox","default"];
	var currentBrowser = BrowserDetect.browser;
	//console.log("currentBrowser: ",currentBrowser);
	var isSupported = false;
	for(var index = 0; index < supportedBrowser.length; index++){
		if(currentBrowser == supportedBrowser[index]){
			isSupported = true;
		}
	}
	if(!isSupported){
		alert("The application does not support this browser.");
	}
}
