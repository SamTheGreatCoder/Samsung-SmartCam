(function ($) {
	$.extend($.ui, { datetimepicker: {} });

	$.datepicker._base_updateDatepicker = $.datepicker._updateDatepicker;
	$.datepicker._updateDatepicker = function (inst) {
		$.datepicker._base_updateDatepicker(inst);
		var val = inst.input.val();
		var hourHTML = "<select class='datetimepicker-hour' onchange='$.datetimepicker.isDirty = true;'>";
		var hourHTML_time = "<select class='datetimepicker-hour' onfocus='setIntervalStatus();' onblur='clearIntervalStatus();' onchange='OnChangeSeekTime();'>";
		for (i = 0; i <= 23; i++) {
			if(i < 10)	{
				hourHTML += "<option>" + ('0'+i) + "</option>";
				hourHTML_time += "<option>" + ('0'+i) + "</option>";
			}
			else {
				hourHTML += "<option>" + i + "</option>";
				hourHTML_time += "<option>" + i + "</option>";
			}
		}
		hourHTML += "</select>" + " : ";
		hourHTML_time += "</select>" + " : ";
		
		var minutsHTML = "<select class='datetimepicker-minuts' onchange='$.datetimepicker.isDirty = true;'>";
		var minutsHTML_time = "<select class='datetimepicker-minuts' onfocus='setIntervalStatus();' onblur='clearIntervalStatus();' onchange='OnChangeSeekTime();'>";
		for (i = 0; i < 60; i++){
			if(i < 10)	{
				minutsHTML += "<option>" + ('0'+i) + "</option>";
				minutsHTML_time += "<option>" + ('0'+i) + "</option>";
			}
			else {
				minutsHTML += "<option>" + i + "</option>";
				minutsHTML_time += "<option>" + i + "</option>";
			}
		}
		minutsHTML += "</select>" + " : ";
		minutsHTML_time += "</select>" + " : ";

		var secondHTML = "<select class='datetimepicker-second' onchange='$.datetimepicker.isDirty = true;'>";
		var secondHTML_time = "<select class='datetimepicker-second' onfocus='setIntervalStatus();' onblur='clearIntervalStatus();' onchange='OnChangeSeekTime();'>";
		for (i = 0; i < 60; i++){
			if(i < 10) {
				secondHTML += "<option>" + ('0'+i) + "</option>";
				secondHTML_time += "<option>" + ('0'+i) + "</option>";
			}
			else {
				secondHTML += "<option>" + i + "</option>";
				secondHTML_time += "<option>" + i + "</option>";
			}
		} 
		secondHTML += "</select>";
		secondHTML_time += "</select>";

		if(inst.id=="eventFrom" || inst.id=="eventTo")
			$(".ui-datepicker-calendar tbody").append("<tr style='height:10px;'><td id='blank' colspan='7'></td></tr><tr><td colspan=7><div style='text-align:center' class='datetimepicker'>"+hourHTML+ minutsHTML+ secondHTML+"</div></td></tr>");
		else 
			$(".ui-datepicker-calendar tbody").append("<tr style='height:10px;'><td id='blank' colspan='7'></td></tr><tr><td colspan=7><div style='text-align:center' class='datetimepicker'>"+hourHTML_time+ minutsHTML_time+ secondHTML_time+"</div></td></tr>");

		$.datetimepicker.setTime(val, inst.input);
	};

	$.datepicker._selectDateOverload = $.datepicker._selectDate;
	$.datepicker._selectDate = function(id, dateStr) {
	    var target = $(id);
	    var inst = this._getInst(target[0]);

		var hour = $('.datetimepicker-hour').val();
		var minuts = $('.datetimepicker-minuts').val();
		var second = $('.datetimepicker-second').val();
		if(inst.id == "Timesearch") {
			hour	= "00";
			minuts	= "00";
			second	= "00";
		}

		var time = hour + ":" + minuts + ":" + second;

		dateStr += " " + time;
		
	    inst.inline = true;
	    $.datepicker._selectDateOverload(id, dateStr);
	    inst.inline = false;
	    this._updateDatepicker(inst);
		
		
	}
/*
	$.datepicker._base_gotoToday = $.datepicker._gotoToday;
	$.datepicker._gotoToday = function(id) {
    // now, optionally, call the original handler, making sure
    //  you use .apply() so the context reference will be correct

	 	var inst = this._getInst($(id)[0]),
 	    $dp = inst.dpDiv;
	//	this._base_gotoToday(id);
 	 	$('.ui-datepicker-today', $dp).click();
	};
*/
	function DateTimePicker(options) {
		this.defaultDateTimePicker =
			{
				showTimePicker: true,
				time_format: 'hh:mm:ss'
			};
	}

	$.fn.extend({
		datetimepicker: function (options) {
			$.datetimepicker._attach(this, options);
		}
	});

	DateTimePicker.prototype = {
		_initTimePicker: function () {
		},
		isDirty: false,
		innerOption: function ($this) {
			return {
				showOn: "button",
				buttonImageOnly: true,
				changeMonth: true,
				changeYear: true,
				autoSize: true,
				onClose: function (a, b) {
				//	if ($.datetimepicker.isDirty) {
					$this.val($.datepicker._formatDate(b));

					var hour = $('.ui-datepicker .datetimepicker-hour').val();
					var minuts = $('.ui-datepicker .datetimepicker-minuts').val();
					var second = $('.ui-datepicker .datetimepicker-second').val();

					var time = hour + ":" + minuts + ":" + second;
					$this.val($this.val() + " " + time);
				//	}
				
					if($this[0].id == "eventFrom") {
						var event = $('#eventTo').val();
						var result = event.match(":");
						if(result == null) {
							$('#eventTo').val($('#eventTo').val() + " 23:59:59"); 
						}
					}
					return true;
				}
			};
		},
		_attach: function ($this, options) {
			$this.datepicker($.fn.extend(this.innerOption($this), options))
				.addClass("datetimepicker");

			this.setTime($this.val(), $this);
		},
		reset: function () {
			this.isDirty = false;
		},
		setTime: function (format, $this) {
			var arrStr = format.split(' ');
			var id = $this[0].id;

			if(id=='eventFrom' || id=='Timesearch') {
				var hour = "00";
				var minuts = "00";
				var second = "00";
			} else if(id=="eventTo"){
				var hour = "23";
				var minuts = "59";
				var second = "59";
			}
			
			if (arrStr.length > 1) {
				var strTime = arrStr[1];
				var arr = strTime.split(':');
				if (arr.length > 0) {
					hour = arr[0];
					if (arr.length > 1) minuts = arr[1];
					if (arr.length > 2) second = arr[2];
				}
			}

				$('.ui-datepicker .datetimepicker-hour').val(hour);
				$('.ui-datepicker .datetimepicker-minuts').val(minuts);
				$('.ui-datepicker .datetimepicker-second').val(second);
			
		}
	};

	$.datetimepicker = new DateTimePicker();
	$.datetimepicker._initTimePicker();

} (jQuery));
