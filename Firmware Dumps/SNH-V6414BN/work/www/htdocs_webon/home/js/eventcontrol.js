function OnClickActivationTime(eventName)
{
	if($("#event_"+eventName+"_act_always").is(':checked'))	
		$("#event_"+eventName+"_timeschedule_overlay").show();
	else 
		$("#event_"+eventName+"_timeschedule_overlay").hide();
}

function MakeScheduleAndActionSetupXML(eventName)
{
	var msg = "";
	msg += "<Schedule>";
	msg += "<Enabled>"+($("#event_"+eventName+"_act_always").is(':checked') ? 0 : 1 )+"</Enabled>";
	msg += GetScheduleData("event_"+eventName+"_timeschedule_table");
	msg += "</Schedule>";

	if (eventName != 'storage') {
		var actionVal = 0;	
		var actionInfo = {	"output_1":"AlarmOutput0",
							"output_2":"AlarmOutput1",
							"ftp":"FTPSending",
							"email":"SMTPSending",
							"record":"Record",
							"preset":"GotoPreset"};
		msg += "<Action>";
		for (var actionType in actionInfo) {
			if(actionType.substring(0, 6) == "output" || actionType == 'preset') {
				actionVal = $("#event_"+eventName+"_"+actionType).val();
			}
			else {
				actionVal = $("#event_"+eventName+"_"+actionType).is(':checked') ? 1 : 0;
			}
			msg += "<"+actionInfo[actionType]+">"+actionVal+"</"+actionInfo[actionType]+">";
		}
		msg += "</Action>";
	}
	return msg;
}

function MakeScheduleAndActionSetupXML_S1(eventName)
{
	var msg = "";
	msg += "<Schedule>";
	msg += "<Enabled>"+($("#event_"+eventName+"_act_always").is(':checked') ? 0 : 1 )+"</Enabled>";
	msg += GetScheduleData("event_"+eventName+"_timeschedule_table");
	msg += "</Schedule>";

	if (eventName != 'storage') {
		var actionVal = 0;	
		var actionInfo = {	"output_1":"AlarmOutput0",
							"output_2":"AlarmOutput1",
							"ftp":"FTPSending",
							"email":"SMTPSending",
							"sms":"SMSSending",
							"record":"Record",
							"preset":"GotoPreset"};
		msg += "<Action>";
		for (var actionType in actionInfo) {
			if(actionType.substring(0, 6) == "output" || actionType == 'preset') {
				actionVal = $("#event_"+eventName+"_"+actionType).val();
			}
			else {
				actionVal = $("#event_"+eventName+"_"+actionType).is(':checked') ? 1 : 0;
			}
			msg += "<"+actionInfo[actionType]+">"+actionVal+"</"+actionInfo[actionType]+">";
		}
		msg += "</Action>";
	}
	return msg;
}

function CheckScheduleSetting(eventName)
{
	if($("#event_"+eventName+"_act_timesched").is(':checked') && $("table#event_"+eventName+"_timeschedule_table tr td.selTime").length == 0)
		return 0;
	return 1;	
}

function ScheduleClear(eventName)
{
	var tableID = "event_"+eventName+"_timeschedule_table";
	$("table#"+tableID+" tr td").removeClass("selTime");
	$("table#"+tableID+" tr td").removeClass("selHour");
	$("table#"+tableID+" tr td").remove("span");
}