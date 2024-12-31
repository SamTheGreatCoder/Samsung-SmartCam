$(document).ready(function(){
	var ieversion = parseInt($.browser.version);
	
//Bring back the browser object 
jQuery.browser = {}; 
//Rest all is self explanatory. 
jQuery.browser.mozilla = /mozilla/.test(navigator.userAgent.toLowerCase())&& !/webkit/.test(navigator.userAgent.toLowerCase()); 
jQuery.browser.webkit = /webkit/.test(navigator.userAgent.toLowerCase()); 
jQuery.browser.opera = /opera/.test(navigator.userAgent.toLowerCase()); 
jQuery.browser.msie = /msie/.test(navigator.userAgent.toLowerCase());  
jQuery.browser.version = /version/.test(navigator.userAgent.toLowerCase()); 

	var slideDelay = 200;
	if ($.browser.msie && ieversion < 8)
	{
		slideDelay = 0;
	}
	
	$(".lnb-list-in > li > ul.two_depth").hide();
	$(".lnb-list-in > li > div.hidden_box").hide();


	$("#lnb_ptz > a > img").click(function(){
	  try
		{
		$("#lnb_basic > img").attr("src",$("#lnb_basic > img").attr("src").replace("_on","_off"));
  		$("#lnb_ptz > ul.two_depth").slideDown(slideDelay);
  		$("#lnb_ptz > div.hidden_box").slideDown(slideDelay);
  		$("#lnb_ptz > a > img").attr("src",$("#lnb_ptz > a > img").attr("src").replace("_off","_on")); 
  		$("#lnb_av > ul.two_depth").css("display","none");
  		$("#lnb_av > div.hidden_box").css("display","none");
  		$("#lnb_av > a > img").attr("src",$("#lnb_av > a > img").attr("src").replace("_on","_off"));
  		$("#lnb_network > ul.two_depth").css("display","none");
  		$("#lnb_network > div.hidden_box").css("display","none");
  		$("#lnb_network > a > img").attr("src",$("#lnb_network > a > img").attr("src").replace("_on","_off"));
		$("#lnb_event > ul.two_depth").css("display","none");
		$("#lnb_event > div.hidden_box").css("display","none");
		$("#lnb_event > a > img").attr("src",$("#lnb_event > a > img").attr("src").replace("_on","_off"));
		$("#lnb_system > ul.two_depth").css("display","none");
		$("#lnb_system > div.hidden_box").css("display","none");
		$("#lnb_system > a > img").attr("src",$("#lnb_system > a > img").attr("src").replace("_on","_off"));
		}
		catch (err)
		{
		}
		return false;
	});

	$("#lnb_av > a > img").click(function(){
	  try
		{
		$("#lnb_basic > img").attr("src",$("#lnb_basic > img").attr("src").replace("_on","_off"));
  		$("#lnb_av > ul.two_depth").slideDown(slideDelay);
  		$("#lnb_av > div.hidden_box").slideDown(slideDelay);
  		$("#lnb_av > a > img").attr("src",$("#lnb_av > a > img").attr("src").replace("_off","_on"));
		if($("#lnb_ptz").length > 0){
	  		$("#lnb_ptz > ul.two_depth").css("display","none");
	  		$("#lnb_ptz > div.hidden_box").css("display","none");
	  		$("#lnb_ptz > a > img").attr("src",$("#lnb_ptz > a > img").attr("src").replace("_on","_off"));
		}
  		$("#lnb_network > ul.two_depth").css("display","none");
  		$("#lnb_network > div.hidden_box").css("display","none");
  		$("#lnb_network > a > img").attr("src",$("#lnb_network > a > img").attr("src").replace("_on","_off"));
	  	$("#lnb_event > ul.two_depth").css("display","none");
	  	$("#lnb_event > div.hidden_box").css("display","none");
	  	$("#lnb_event > a > img").attr("src",$("#lnb_event > a > img").attr("src").replace("_on","_off"));
		$("#lnb_system > ul.two_depth").css("display","none");
		$("#lnb_system > div.hidden_box").css("display","none");
		$("#lnb_system > a > img").attr("src",$("#lnb_system > a > img").attr("src").replace("_on","_off"));
		}
		catch (err)
		{
		}
	});

	$("#lnb_network > a > img").click(function(){
	  try
		{
		$("#lnb_basic > img").attr("src",$("#lnb_basic > img").attr("src").replace("_on","_off"));
  		$("#lnb_network > ul.two_depth").slideDown(slideDelay);
  		$("#lnb_network > div.hidden_box").slideDown(slideDelay);
  		$("#lnb_network > a > img").attr("src",$("#lnb_network > a > img").attr("src").replace("_off","_on"));
		if($("#lnb_ptz").length > 0){
	  		$("#lnb_ptz > ul.two_depth").css("display","none");
	  		$("#lnb_ptz > div.hidden_box").css("display","none");
	  		$("#lnb_ptz > a > img").attr("src",$("#lnb_ptz > a > img").attr("src").replace("_on","_off"));
		}
  		$("#lnb_av > ul.two_depth").css("display","none");
  		$("#lnb_av > div.hidden_box").css("display","none");
  		$("#lnb_av > a > img").attr("src",$("#lnb_av > a > img").attr("src").replace("_on","_off"));
		$("#lnb_event > ul.two_depth").css("display","none");
		$("#lnb_event > div.hidden_box").css("display","none");
		$("#lnb_event > a > img").attr("src",$("#lnb_event > a > img").attr("src").replace("_on","_off"));
		$("#lnb_system > ul.two_depth").css("display","none");
		$("#lnb_system > div.hidden_box").css("display","none");
		$("#lnb_system > a > img").attr("src",$("#lnb_system > a > img").attr("src").replace("_on","_off"));
		}
		catch (err)
		{
		}
	});

	$("#lnb_event > a > img").click(function(){
	  try
		{
		$("#lnb_basic > img").attr("src",$("#lnb_basic > img").attr("src").replace("_on","_off"));
  		$("#lnb_event > ul.two_depth").slideDown(slideDelay);
  		$("#lnb_event > div.hidden_box").slideDown(slideDelay);
  		$("#lnb_event > a > img").attr("src",$("#lnb_event > a > img").attr("src").replace("_off","_on"));
		if($("#lnb_ptz").length > 0){
	  		$("#lnb_ptz > ul.two_depth").css("display","none");
	  		$("#lnb_ptz > div.hidden_box").css("display","none");
	  		$("#lnb_ptz > a > img").attr("src",$("#lnb_ptz > a > img").attr("src").replace("_on","_off"));
		}
  		$("#lnb_av > ul.two_depth").css("display","none");
  		$("#lnb_av > div.hidden_box").css("display","none");
  		$("#lnb_av > a > img").attr("src",$("#lnb_av > a > img").attr("src").replace("_on","_off"));
  		$("#lnb_network > ul.two_depth").css("display","none");
  		$("#lnb_network > div.hidden_box").css("display","none");
  		$("#lnb_network > a > img").attr("src",$("#lnb_network > a > img").attr("src").replace("_on","_off"));
		$("#lnb_system > ul.two_depth").css("display","none");
		$("#lnb_system > div.hidden_box").css("display","none");
		$("#lnb_system > a > img").attr("src",$("#lnb_system > a > img").attr("src").replace("_on","_off"));
		}
		catch (err)
		{
		}
	});

	$("#lnb_system > a > img").click(function(){
	  try
		{
		$("#lnb_basic > img").attr("src",$("#lnb_basic > img").attr("src").replace("_on","_off"));
  		$("#lnb_system > ul.two_depth").slideDown(slideDelay);
  		$("#lnb_system > div.hidden_box").slideDown(slideDelay);
  		$("#lnb_system > a > img").attr("src",$("#lnb_system > a > img").attr("src").replace("_off","_on"));
		if($("#lnb_ptz").length > 0){
	  		$("#lnb_ptz > ul.two_depth").css("display","none");
	  		$("#lnb_ptz > div.hidden_box").css("display","none");
	  		$("#lnb_ptz > a > img").attr("src",$("#lnb_ptz > a > img").attr("src").replace("_on","_off"));
		}
  		$("#lnb_av > ul.two_depth").css("display","none");
  		$("#lnb_av > div.hidden_box").css("display","none");
  		$("#lnb_av > a > img").attr("src",$("#lnb_av > a > img").attr("src").replace("_on","_off"));
  		$("#lnb_network > ul.two_depth").css("display","none");
  		$("#lnb_network > div.hidden_box").css("display","none");
  		$("#lnb_network > a > img").attr("src",$("#lnb_network > a > img").attr("src").replace("_on","_off"));
		$("#lnb_event > ul.two_depth").css("display","none");
		$("#lnb_event > div.hidden_box").css("display","none");
		$("#lnb_event > a > img").attr("src",$("#lnb_event > a > img").attr("src").replace("_on","_off"));
		}
		catch (err)
		{
		}
	});

	$(".two_depth > li").mouseenter(function(){
		$(this).addClass("on");
	});
	$(".two_depth > li").mouseleave(function(){
		$(this).removeClass("on");
	});

});

function lnbonoff(a,b){
	var thissrc = $("#"+ a).find("img").eq(0).attr("src");
	var thissrcin = $("li",$(".lnb-list-in > li").eq(a)).eq(b).find("img").attr("src");
	var inul = $("ul",$("#"+ a));
	if(inul != null)
	{
		inul.show();
	}
	if(thissrc)
	{
		$("#"+ a).find("img").eq(0).attr("src",thissrc.replace("_off","_on"));
		$("#"+ a).addClass("slc");
	}
	if(thissrcin)
	{
		$("#"+ a).eq(b).find("img").attr("src",thissrcin.replace("_off","_on"));
		$("#"+ a).eq(b).addClass("selected");
	}
}
