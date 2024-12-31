var test = false;
$(document).ready(function(){

	$(function () {
		$('.time_table tbody tr:odd td').css("background-color","#b4b9c5");
	});

	$(".advanced").click(function(){
		$(".show_advanced").toggle(300);
		$(".advanced a").toggleClass('up down');
	});

	$(".advanced_profile").click(function(){
		test = !test;
	  	$(".show_advanced_profile").toggle();
		$(".advanced_profile a").toggleClass('up down');
	});

	$(".box01").click(function(){
		$(".show_advanced").toggle(300);
		$(".box01 a img").toggleClass('up down');
	});
	$(".lnb-btn").click(function(){
		$('#lnb').css("display","none");
		$('#lnb2').css("display","block");
	});
	$(".lnb-open").click(function(){
		$('#lnb').css("display","block");
		$('#lnb2').css("display","none");
	});
	$(".next2").click(function(){
		$('.select_list').css("display","block");
	});

});

// added by sj0428.ko (for monitoring/playback left menu)
function openlnbMenu(val)
{
  $('#lnb').css("display","block");
	$('#lnb2').css("display","none");

/*	try
	{
  	if(val == 2){
  		$("#lnb02 > ul.two_depth").slideDown(200);
  		$("#lnb02 > div.hidden_box").slideDown(200);
  		$("#lnb02 > a > img").attr("src",$("#lnb02 > a > img").attr("src").replace("_off.","_on."));
  		$("#lnb01 > ul.two_depth").css("display","none");
  		$("#lnb01 > div.hidden_box").css("display","none");
  		$("#lnb01 > a > img").attr("src",$("#lnb01 > a > img").attr("src").replace("_on.","_off."));
  		$("#lnb03 > ul.two_depth").css("display","none");
  		$("#lnb03 > div.hidden_box").css("display","none");
  		$("#lnb03 > a > img").attr("src",$("#lnb03 > a > img").attr("src").replace("_on.","_off."));
  	}

  	else if(val == 3){
  		$("#lnb03 > ul.two_depth").slideDown(200);
  		$("#lnb03 > div.hidden_box").slideDown(200);
  		$("#lnb03 > a > img").attr("src",$("#lnb03 > a > img").attr("src").replace("_off.","_on."));
  		$("#lnb01 > ul.two_depth").css("display","none");
  		$("#lnb01 > div.hidden_box").css("display","none");
  		$("#lnb01 > a > img").attr("src",$("#lnb01 > a > img").attr("src").replace("_on.","_off."));
  		$("#lnb02 > ul.two_depth").css("display","none");
  		$("#lnb02 > div.hidden_box").css("display","none");
  		$("#lnb02 > a > img").attr("src",$("#lnb02 > a > img").attr("src").replace("_on.","_off."));
  	}

  	else {
  		$("#lnb01 > ul.two_depth").slideDown(200);
  		$("#lnb01 > div.hidden_box").slideDown(200);
  		$("#lnb01 > a > img").attr("src",$("#lnb01 > a > img").attr("src").replace("_off.","_on."));
  		$("#lnb02 > ul.two_depth").css("display","none");
  		$("#lnb02 > div.hidden_box").css("display","none");
  		$("#lnb02 > a > img").attr("src",$("#lnb02 > a > img").attr("src").replace("_on.","_off."));
  		$("#lnb03 > ul.two_depth").css("display","none");
  		$("#lnb03 > div.hidden_box").css("display","none");
  		$("#lnb03 > a > img").attr("src",$("#lnb03 > a > img").attr("src").replace("_on.","_off."));
  	}
	}
	catch (err)
	{

	}*/

	try
	{
  	if(val == 1){
  		$("#lnb01 > ul.two_depth").slideDown(200);
  		$("#lnb01 > div.hidden_box").slideDown(200);
  		$("#lnb01 > a > img").attr("src",$("#lnb01 > a > img").attr("src").replace("_off.","_on."));
  		$("#lnb02 > ul.two_depth").css("display","none");
  		$("#lnb02> div.hidden_box").css("display","none");
  		$("#lnb02 > a > img").attr("src",$("#lnb02 > a > img").attr("src").replace("_on.","_off."));
		$("#lnb03 > ul.two_depth").css("display","none");
  		$("#lnb03> div.hidden_box").css("display","none");
  		$("#lnb03 > a > img").attr("src",$("#lnb03 > a > img").attr("src").replace("_on.","_off."));
  	}

  	else if(val == 2){
  		$("#lnb02 > ul.two_depth").slideDown(200);
  		$("#lnb02 > div.hidden_box").slideDown(200);
  		$("#lnb02 > a > img").attr("src",$("#lnb02 > a > img").attr("src").replace("_off.","_on."));
  		$("#lnb01 > ul.two_depth").css("display","none");
  		$("#lnb01 > div.hidden_box").css("display","none");
  		$("#lnb01 > a > img").attr("src",$("#lnb01 > a > img").attr("src").replace("_on.","_off."));
		$("#lnb03 > ul.two_depth").css("display","none");
  		$("#lnb03> div.hidden_box").css("display","none");
  		$("#lnb03 > a > img").attr("src",$("#lnb03 > a > img").attr("src").replace("_on.","_off."));

  	}
	else {
  		$("#lnb01 > ul.two_depth").css("display","none");
  		$("#lnb01 > div.hidden_box").css("display","none");
  		$("#lnb01 > a > img").attr("src",$("#lnb01 > a > img").attr("src").replace("_on.","_off."));
  		$("#lnb02 > ul.two_depth").css("display","none");
  		$("#lnb02 > div.hidden_box").css("display","none");
  		$("#lnb02 > a > img").attr("src",$("#lnb02 > a > img").attr("src").replace("_on.","_off."));
		$("#lnb03 > ul.two_depth").slideDown(200);
  		$("#lnb03 > div.hidden_box").slideDown(200);
  		$("#lnb03 > a > img").attr("src",$("#lnb03 > a > img").attr("src").replace("_off.","_on."));
  	}
	}
	catch (err)
	{

	}
}
