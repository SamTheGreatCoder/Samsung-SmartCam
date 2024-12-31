$(document).ready(function(){
	$(".lnb-list-in > li > ul.two_depth").hide();
	$(".lnb-list-in > li > div.hidden_box").hide();
	
	$("#lnb01 > img").click(function(){
	
		  if (mode == 0)
		  {
			return;
		  }
	
		  OriginalStatus = 1;
		  FittStatus = 0;
		  isDaySelected = 0;
		  try{
			SISOPlugin.Stop();
		  } catch(err) { }
		  mode = 0;
		  
		  $("#timeBar").html("");
		  $("#timebarHtml").hide();
		  $("#lnb02_timeCal").html("");
		  $('#lnb01_span').html("");
		  $("#event_box").show();

		  $(".timeLineDiv").empty();

		 try{
		  SISOPlugin.SetResolution(1, 1);
		  } catch(err) { }
		 document.getElementById('plugin').width = 1;
		 document.getElementById('plugin').height = 1;

		  playSpeed = 1;
		 $('#speed_ff').html("<font color='#2A303C'>1x</font>");
		 $('#speed_prev').html("<font color='#2A303C'>-1x</font>");

		 $("#rewind_btn").html("<img src=\"../images/search/common/btn/02.jpg\" />");
		 $("#stepbackward_btn").html("<img src=\"../images/search/common/btn/btn_stepbackward_disable.jpg\" />");
		 $("#ff_btn").html("<img src=\"../images/search/common/btn/05.jpg\" />");
		 $("#stepforward_btn").html("<img src=\"../images/search/common/btn/btn_stepforward_disable.jpg\" />");
		 if (isEventSearchSuccess == 0)
		 {
			$("#stop_btn").html("<img src=\"../images/search/common/btn/03_disable.jpg\" />");
			$("#play_btn").html("<img src=\"../images/search/common/btn/04_disable.jpg\" />");
		 }

  		$("#lnb01 > ul.two_depth").slideDown(200);
  		$("#lnb01 > div.hidden_box").slideDown(200);
  		$("#lnb01 > img").attr("src",$("#lnb01 > img").attr("src").replace("_off.","_on."));
  		$("#lnb02 > ul.two_depth").css("display","none");
  		$("#lnb02 > div.hidden_box").css("display","none");
  		$("#lnb02 > img").attr("src",$("#lnb02 > img").attr("src").replace("_on.","_off."));
		StopRecordedVideo();
		return false;
	});

	$("#lnb02 > img").click(function(){
		  if (mode == 1)
		  {
			return;
		  }
		  OriginalStatus = 1;
		  FittStatus = 0;
		  isDaySelected = 0;
		  try {
		  SISOPlugin.Stop();
		  } catch(err) { }
		  //window.setTimeout('DrawTimeline()', 5000);
		 
		  mode = 1;
		  DrawTimeline();
		  if(recordingEnable == 0) {
		  	mode = 0;
			return;
		  }
		  
		 try{
		 SISOPlugin.SetResolution(1, 1);
		 } catch(err) { }
		 document.getElementById('plugin').width = 1;
		 document.getElementById('plugin').height = 1;
		 
		 $('#timeBar').show();
		 $('#timebarHtml').show();
		 $('#lnb01_span').html("");
		 $("#event_box").hide();

		 $(".timeLineDiv").empty();

		  playSpeed = 1;
		 $('#speed_ff').html(playSpeed + "x");
		 $('#speed_prev').html("<font color='#2A303C'>-1x</font>");

		 //$("#rewind_btn").html("<a href=\"javascript:Rewind()\"><img src=\"../images/search/common/btn/btn_prevspeed.jpg\" /></a>");
		 $("#stepbackward_btn").html("<a href=\"javascript:StepBackward()\"><img src=\"../images/search/common/btn/btn_stepbackward.jpg\" /></a>");
		 //$("#ff_btn").html("<a href=\"javascript:FastForward()\"><img src=\"../images/search/common/btn/btn_ffspeed.jpg\" /></a>");
		 $("#stepforward_btn").html("<a href=\"javascript:StepForward()\"><img src=\"../images/search/common/btn/btn_stepforward.jpg\" /></a>");
		 $("#stop_btn").html("<a href=\"javascript:OnClickStop()\"><img src=\"../images/search/common/btn/03_normal.jpg\" /></a>");
		 $("#play_btn").html("<a href=\"javascript:OnClickPlay()\"><img src=\"../images/search/common/btn/04_normal.jpg\" /></a>");

  		$("#lnb02 > ul.two_depth").slideDown(200);
  		$("#lnb02 > div.hidden_box").slideDown(200);
  		$("#lnb02 > img").attr("src",$("#lnb02 > img").attr("src").replace("_off.","_on."));
  		$("#lnb01 > ul.two_depth").css("display","none");
  		$("#lnb01 > div.hidden_box").css("display","none");
  		$("#lnb01 > img").attr("src",$("#lnb01 > img").attr("src").replace("_on.","_off."));
		StopRecordedVideo();
	});
	
	$(".two_depth > li").mouseenter(function(){
		$(this).addClass("on");
	});
	$(".two_depth > li").mouseleave(function(){
		$(this).removeClass("on");
	});
	
	$(function () {
		$('.time_table tbody tr:odd td').css("background-color","#b4b9c5");
	});

	$(".advanced").click(function(){
		$(".show_advanced").toggle(300);
		$(".advanced a").toggleClass('up down'); 
	});
	$(".advanced_profile").click(function(){
		$(".show_advanced_profile").toggle(300);
		$(".advanced_profile a").toggleClass('up down'); 
	});
	$(".box01").click(function(){
		$(".show_advanced").toggle(300);
		$(".box01 a img").toggleClass('up down');
	});
	$(".lnb-btn").click(function(){
		$('#lnb').css("display","none");
		$('#lnb2').css("display","block");

		if($('#timebarHtml').get(0) != null)
			$('#timebarHtml').get(0).style.left='80px';
	});
	$(".lnb-open").click(function(){
		$('#lnb').css("display","block");
		$('#lnb2').css("display","none");

		if($('#timebarHtml').get(0) != null)
			$('#timebarHtml').get(0).style.left='305px';
	});
	$(".next2").click(function(){
		$('.select_list').css("display","block");
	});

});

function lnbonoff(a,b){
	var thissrc = $(".lnb-list-in > li").eq(a).find("img").eq(0).attr("src");
	var thissrcin = $("li",$(".lnb-list-in > li").eq(a)).eq(b).find("img").attr("src");
	var inul = $("ul",$(".lnb-list-in > li").eq(a));
	if(inul != null)
	{
		inul.show();
	}
	if(thissrc)
	{
		$(".lnb-list-in > li").eq(a).find("img").eq(0).attr("src",thissrc.replace("_off.","_on."));
		$(".lnb-list-in > li").eq(a).addClass("slc");
	}
	if(thissrcin)
	{
		$("li",$(".lnb-list-in > li").eq(a)).eq(b).find("img").attr("src",thissrcin.replace("_off.","_on."));
		$("li",$(".lnb-list-in > li").eq(a)).eq(b).addClass("selected");
	}
}

// added by sj0428.ko (for monitoring/playback left menu)
function openlnbMenu(val)
{
  $('#lnb').css("display","block");
	$('#lnb2').css("display","none");
	
  	if(val == 2){
		if(mode == 0)
		{
			OriginalStatus = 1;
			  FittStatus = 0;
			  isDaySelected = 0;
			  try{
			  SISOPlugin.Stop();
			  } catch(err) { }
			  //window.setTimeout('DrawTimeline()', 5000);
			  DrawTimeline();
			  if(recordingEnable == 0)
				  return;
			  mode = 1;
			 if (SISOPlugin != null)
			 {
				  try{
				  SISOPlugin.SetResolution(1, 1);
				  } catch(err) { }
				 document.getElementById('plugin').width = 1;
				 document.getElementById('plugin').height = 1;
			 }
			 $('#lnb02').click();
			 $('#timeBar').show();
			 $('#timebarHtml').show();

			  playSpeed = 1;
			 $('#speed_ff').html(playSpeed + "x");
			 $('#speed_prev').html("<font color='#2A303C'>-1x</font>");

			 //$("#rewind_btn").html("<a href=\"javascript:Rewind()\"><img src=\"../images/search/common/btn/btn_prevspeed.jpg\" /></a>");
			 $("#stepbackward_btn").html("<a href=\"javascript:StepBackward()\"><img src=\"../images/search/common/btn/btn_stepbackward.jpg\" /></a>");
			 //$("#ff_btn").html("<a href=\"javascript:FastForward()\"><img src=\"../images/search/common/btn/btn_ffspeed.jpg\" /></a>");
			 $("#stepforward_btn").html("<a href=\"javascript:StepForward()\"><img src=\"../images/search/common/btn/btn_stepforward.jpg\" /></a>");
			 $("#stop_btn").html("<a href=\"javascript:OnClickStop()\"><img src=\"../images/search/common/btn/03_normal.jpg\" /></a>");
			 $("#play_btn").html("<a href=\"javascript:OnClickPlay()\"><img src=\"../images/search/common/btn/04_normal.jpg\" /></a>");
		}

		 if($('#timebarHtml').get(0) != null)
			$('#timebarHtml').get(0).style.left='305px';

  		$("#lnb02 > ul.two_depth").slideDown(200);
  		$("#lnb02 > div.hidden_box").slideDown(200);
  		$("#lnb02 > img").attr("src",$("#lnb02 > img").attr("src").replace("_off.","_on."));
  		$("#lnb01 > ul.two_depth").css("display","none");
  		$("#lnb01 > div.hidden_box").css("display","none");
  		$("#lnb01 > img").attr("src",$("#lnb01 > img").attr("src").replace("_on.","_off."));
  	}
  	
  	else {
		if(mode == 1)
		{
			OriginalStatus = 1;
			  FittStatus = 0;
			  isDaySelected = 0;
			  try{
			  SISOPlugin.Stop();
			  } catch(err) { }
			  mode = 0;
			  if (SISOPlugin != null)
			 {
				  try{
				  SISOPlugin.SetResolution(1, 1);
				  } catch(err) { }
				 document.getElementById('plugin').width = 1;
				 document.getElementById('plugin').height = 1;
			 }
			
			 $('#event_box').show();
			 $('#timeBar').hide();
			 $('#timebarHtml').hide();
			 $("#timeBar").html("");
			 $("#lnb02_timeCal").html("");

			  playSpeed = 1;
			 $('#speed_ff').html("<font color='#2A303C'>1x</font>");
			 $('#speed_prev').html("<font color='#2A303C'>-1x</font>");

			 $("#rewind_btn").html("<img src=\"../images/search/common/btn/02.jpg\" />");
			 $("#stepbackward_btn").html("<img src=\"../images/search/common/btn/btn_stepbackward_disable.jpg\" />");
			 $("#ff_btn").html("<img src=\"../images/search/common/btn/05.jpg\" />");
			 $("#stepforward_btn").html("<img src=\"../images/search/common/btn/btn_stepforward_disable.jpg\" />");
			 if (isEventSearchSuccess == 0)
			 {
				$("#stop_btn").html("<img src=\"../images/search/common/btn/03_disable.jpg\" />");
				$("#play_btn").html("<img src=\"../images/search/common/btn/04_disable.jpg\" />");
			 }
		}

		if($('#timebarHtml').get(0) != null)
			$('#timebarHtml').get(0).style.left='305px';


  		$("#lnb01 > ul.two_depth").slideDown(200);
  		$("#lnb01 > div.hidden_box").slideDown(200);
  		$("#lnb01 > img").attr("src",$("#lnb01 > img").attr("src").replace("_off.","_on."));
  		$("#lnb02 > ul.two_depth").css("display","none");
  		$("#lnb02 > div.hidden_box").css("display","none");
  		$("#lnb02 > img").attr("src",$("#lnb02 > img").attr("src").replace("_on.","_off."));
  	}
}
