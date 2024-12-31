
	var SDK_USER_DATA = {
		"UserName":"",
		"Password":"",
		"PTZ":"",
		"LangString":"",
		"DevicePort":""
		};
		
(function ($) {
///////////////////////////////////////////////////////////////////////////////////////////////////////////
/// getting User info like user name and pwd etc..
			

///////////////////////////////////////////////////////////////////////////////////////////////////////////


    var SDK_ERROR_CODES_MAP = {
        66: 'OPERATION TEMPORARILY UNAVAILABLE',
        100: 'APP ALREADY RUNNING',
        101: 'APP START FAILED',
        102: 'APP STOP FAILED',
        103: 'APP UPLOAD FAIL',
        104: 'NO ENOUGH SPACE LEFT ON DEVICE',
        105: 'INVALID APPLICATION PACKAGE',
        106: 'HIGHER OR SIMILAR VERSION IS ALREADY AVAILABLE',
        107: 'APP INSTALL FAIL',
        108: 'APP UNINSTALL FAIL',
        109: 'APP NOT FOUND',
        110: 'App Recording already Running',
        111: 'APP IS NOT RUNNING',
        112: 'Debug viewer is already running',
        113: 'Camera platform could not be recognised',
        114: 'Mismatch between package and camera platform',
        115: 'System recovered from an error! DB is reset to default.\nPlease try again.',
        116: 'Parallel install of the application is under progress.\nPlease reload and try again.',
        117: 'CPU limit reached.\nFresh start is prohibited.',
        118: 'Memory limit reached.\nFresh start is prohibited.',
        119: 'SDK Version is not supported for application.'
    };

    var reqUrl = window.location.protocol+"//" + window.location.host + "/cgi-bin/stw.cgi";
	if (BrowserDetect.browser == 'Explorer' || (BrowserDetect.browser == 'Safari') && reqUrl.search('.local') != -1) {
		//reqUrl = "../.."+reqUrl.substr(reqUrl.indexOf("/cgi"));
		reqUrl = reqUrl.substr(reqUrl.indexOf("/cgi"));
	}

    //pass a single JSON object
    $.fn.startApplication = function (params) {
        // function should define a set of default parameters then overwrite these with any user-defined values. 
        //The jQuery extend function can handle this for us:
        var defaults = {
            appname: "",
            datatype: "json"
        };

        params = $.extend(defaults, params);

        var appname = params.appname;
        var msg = "";
        msg += "<StartSDK>";
        msg += "<AppName>" + appname + "</AppName>";
        msg += "</StartSDK>";

        if (appname || appname != '') {
            //console.log("Value Passed::",appname);
            $.ajax({
                type: "POST",
                cache: false,
                url: reqUrl,
                dataType: "text",
                data: encodeURI(msg),
                success: function (response) {
                    var jsonResponse = $.xml2json(response);
                    //console.log(jsonResponse);
                    if (jsonResponse == "OK") {
                        // Make Call Back Optional && Make Sure the Callback is a Function
                        if (params.success && typeof params.success == 'function') {
                            if (params.datatype == 'json') {
                                params.success(jsonResponse);
                            } else {
                                params.success(response);
                            }
                        }
                    } else {
                        // Make Call Back Optional && Make Sure the Callback is a Function
                        if (params.error && typeof params.error == 'function') {
                            params.error(SDK_ERROR_CODES_MAP[jsonResponse]);
                        }
                    }
                }
            });
        }
        //return the jQuery object so other methods can be chained
        return this;
    };
    $.fn.stopApplication = function (params) {
        // function should define a set of default parameters then overwrite these with any user-defined values. 
        //The jQuery extend function can handle this for us:
        var defaults = {
            appname: "",
            datatype: "json"
        };

        params = $.extend(defaults, params);

        var appname = params.appname;
        var msg = "";
        msg += "<StopSDK>";
        msg += "<AppName>" + appname + "</AppName>";
        msg += "</StopSDK>";

        if (appname || appname != '') {
            //console.log("Value Passed::",appname);
            $.ajax({
                type: "POST",
                cache: false,
                url: reqUrl,
                dataType: "text",
                data: encodeURI(msg),
                success: function (response) {
                    var jsonResponse = $.xml2json(response);
                    //console.log(jsonResponse);
                    if (jsonResponse == "OK") {
                        // Make Call Back Optional && Make Sure the Callback is a Function
                        if (params.success && typeof params.success == 'function') {
                            if (params.datatype == 'json') {
                                params.success(jsonResponse);
                            } else {
                                params.success(response);
                            }
                        }
                    } else {
                        // Make Call Back Optional && Make Sure the Callback is a Function
                        if (params.error && typeof params.error == 'function') {
                            params.error(SDK_ERROR_CODES_MAP[jsonResponse]);
                        }
                    }
                }
            });
        }
        //return the jQuery object so other methods can be chained
        return this;
    };

    $.fn.getApplicationStatus = function (params) {
        // function should define a set of default parameters then overwrite these with any user-defined values. 
        //The jQuery extend function can handle this for us:
        var defaults = {
            appname: "",
            datatype: "json"
        };

        params = $.extend(defaults, params);

        var appname = params.appname;
        var msg = "";
        msg += "<GetSDK_APP_STATUS>";
        msg += "<AppName>" + appname + "</AppName>";
        msg += "</GetSDK_APP_STATUS>";

        if (appname || appname != '') {
            //console.log("Value Passed::",appname);
            $.ajax({
                type: "POST",
                cache: false,
                url: reqUrl,
                dataType: "text",
                data: encodeURI(msg),
                success: function (response) {
                    // Make Call Back Optional && Make Sure the Callback is a Function
                    if (params.success && typeof params.success == 'function') {
                        if (params.datatype == 'json') {
                            params.success($.xml2json(response));
                        } else {
                            params.success(response);
                        }
                    }
                }
            });
        }
        //return the jQuery object so other methods can be chained
        return this;
    };

    $.fn.getApplicationSettings = function (params) {
        // function should define a set of default parameters then overwrite these with any user-defined values. 
        //The jQuery extend function can handle this for us:
        var defaults = {
            appname: "",
            datatype: "json"
        };

        params = $.extend(defaults, params);

        var appname = params.appname;
        var msg = "";
        msg += "<GetSDK_APP>";
        msg += "<AppName>" + appname + "</AppName>";
        msg += "</GetSDK_APP>";

        if (appname || appname != '') {
            //console.log("Value Passed::",appname);
            $.ajax({
                type: "POST",
                cache: false,
                url: reqUrl,
                dataType: "text",
                data: encodeURI(msg),
                success: function (response) {
                    var jsonResponse = $.xml2json(response);
                    //console.log(jsonResponse);
                    if (params.success && typeof params.success == 'function') {
                        if (params.datatype == 'json') {
                            params.success(jsonResponse);
                        } else {
                            params.success(response);
                        }
                    }
                }
            });
        }
        //return the jQuery object so other methods can be chained
        return this;
    };

    $.fn.updateApplicationSettings = function (params) {
        // function should define a set of default parameters then overwrite these with any user-defined values. 
        //The jQuery extend function can handle this for us:
        var defaults = {
            appname: "",
            appconfig: null,
            datatype: "json"
        };

        params = $.extend(defaults, params);

        var appname = params.appname;
        var appconfig = params.appconfig
        var msg = "";
        msg += "<SetSDK_APP>";
        msg += "<AppName>" + appname + "</AppName>";

        if (appconfig) {
            msg += $.json2xml(appconfig);
        }
        msg += "</SetSDK_APP>";

        if (appname || appname != '') {
            //console.log("Value Passed::", msg);
            $.ajax({
                type: "POST",
                cache: false,
                url: reqUrl,
                dataType: "text",
                data: encodeURI(msg),
                success: function (response) {
                    var jsonResponse = $.xml2json(response);
                    //console.log(jsonResponse);
                    if (jsonResponse.Status == "OK") {
                        // Make Call Back Optional && Make Sure the Callback is a Function
                        if (params.success && typeof params.success == 'function') {
                            if (params.datatype == 'json') {
                                params.success(jsonResponse);
                            } else {
                                params.success(response);
                            }
                        }
                    } else {
                        // Make Call Back Optional && Make Sure the Callback is a Function
                        if (params.error && typeof params.error == 'function') {
                            params.error(SDK_ERROR_CODES_MAP[jsonResponse]);
                        }
                    }
                }
            });
        }
        //return the jQuery object so other methods can be chained
        return this;
    };
    $.fn.sendCommandToServer = function (params) {
        var defaults = {
            requestMessage: null,
            datatype: "json"
        };
        params = $.extend(defaults, params);
		var requestMessage = params.requestMessage;
		if(requestMessage){
			$.ajax({
				type: "POST",
				cache: false,
				url: reqUrl,
				dataType: "text",
				data: encodeURI(requestMessage),
				success: function (response) {
					var jsonResponse = $.xml2json(response);
					//console.log(jsonResponse);
					if (params.success && typeof params.success == 'function') {
						if(params.datatype == 'json') {
							params.success(jsonResponse);
						} else {
							params.success(response);
						}
					}
				},
				error: function( jqXHR, textStatus, errorThrow){
					if (params.error && typeof params.error == 'function') {
						params.error(jqXHR, textStatus, errorThrow);						
					}
				}
			});
		}
        
    };
	
	$.fn.pluginPlay = function (params) {
        // function should define a set of default parameters then overwrite these with any user-defined values. 
        //The jQuery extend function can handle this for us:
        var defaults = {
            width: "",
            height: ""
        };

        params = $.extend(defaults, params);
            //console.log("Value Passed::",appname);
            $.ajax({
                type: "POST",
                cache: false,
                url: "/home/setup/getUserInfo.cgi",
                dataType: "text",
                success: function (response) {
                    xmlDoc = $.parseXML( response );
					$xml = $( xmlDoc );
					
					  SDK_USER_DATA["DevicePort"]=$xml.find("DEVICEPORT").text();
					  SDK_USER_DATA["UserName"]=$xml.find("USERNAME").text();
					  SDK_USER_DATA["Password"]=$xml.find("PWD").text();
					  SDK_USER_DATA["PTZ"]=$xml.find("PTZ").text();
					  SDK_USER_DATA["LangString"]=$xml.find("LANGSTRING").text();
					 // console.log(SDK_USER_DATA);
					  SISOPlugin.init("please install plugin", params.width, params.height);
					SISOPlugin.startPluginPlay(SDK_USER_DATA["DevicePort"],1,SDK_USER_DATA["UserName"],SDK_USER_DATA["Password"]);
                }
            });
       
        //return the jQuery object so other methods can be chained
        return this;
    };
	
	
})(jQuery);
