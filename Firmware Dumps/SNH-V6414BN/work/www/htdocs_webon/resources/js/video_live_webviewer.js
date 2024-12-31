var stun_host = "stun.samsungsmartcam.com";
var Webviewer = (function(){
	var Plugin = null;
	var style = null;
	var setting = null;
	var timer = null;
	var player = null;

	var object = {
		init : function( obj ){
			setting = obj;

			if(setting.type != "0"){
				Plugin = plugin;
			}
			else{
				Plugin = document.getElementById("plugin");
			}

			try{
				Plugin.Init(stun_host);

				var curVersion = Plugin.GetMajorVersion() + "." + Plugin.GetMinorVersion() + "." +
								 Plugin.GetPatchVersion() + "." + Plugin.GetBuildVersion();

				if (typeof (console) != "undefined") {
					console.info("Current version : "  + curVersion);
					console.info("Latest version : "  + lastVersion);
				}

				if (curVersion < lastVersion) {
					alert("Please check plugin or firmware version!");
				}

				return true;
			}
			catch(exc){
				return false;
			}

			style = $("#plugin");
			style.css("width", setting.width + "px");
			style.css("height", setting.height + "px");
		},

		play : function( obj ){
			player = obj;
			var ret = "";
			var rtpUrl = "rtsp://" + player.ip + "/profile4/media.smp";

			if(setting.type == 0){
				ret = Plugin.LivePlay(rtpUrl, player.camId, player.privateKey);
			}
			else{
				ret = Plugin.LivePlayLocal(rtpUrl, player.camId, player.privateKey);
			}

			return ret;
		},

		profileChange : function( profile ){
			var rtpUrl = "rtsp://" + player.ip + "/" + profile + "/media.smp";
			var ret = "";

			if(setting.type == 0){
				ret = Plugin.LivePlay(rtpUrl, player.camId, player.privateKey);
			}
			else{
				setTimeout(function(){
					ret = Plugin.LivePlayLocal(rtpUrl, player.camId, player.privateKey);
				}, 2000);
			}

			return ret;
		},

		stop : function(){
			Plugin.Stop();
		},

		soundOn : function(){
			Plugin.Unmute();
		},

		soundOff : function(){
			Plugin.Mute();
		},

		capture : function( filename ){
			Plugin.SaveSnapShot(filename);
		},

		irFlashOn : function(){
			Plugin.IRFlash();
		},

		statusCheck : function(){
			var res = Plugin.GetState();
			return res;
		}
	};
	return object;
})();