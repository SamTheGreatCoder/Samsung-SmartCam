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
	
	$("#lnb01 > a > img").click(function(){
	  try
		{
  		$("#lnb01 > ul.two_depth").slideDown(slideDelay);
  		$("#lnb01 > div.hidden_box").slideDown(slideDelay);
  		$("#lnb01 > a > img").attr("src",$("#lnb01 > a > img").attr("src").replace("_off","_on"));
  		$("#lnb02 > ul.two_depth").css("display","none");
  		$("#lnb02 > div.hidden_box").css("display","none");
  		$("#lnb02 > a > img").attr("src",$("#lnb02 > a > img").attr("src").replace("_on","_off"));
		$("#lnb03 > ul.two_depth").css("display","none");
  		$("#lnb03 > div.hidden_box").css("display","none");
  		$("#lnb03 > a > img").attr("src",$("#lnb03 > a > img").attr("src").replace("_on","_off"));

		}
		catch (err)
		{
		}
		return false;
	});

	$("#lnb02 > a > img").click(function(){
	  try
		{
  		$("#lnb02 > ul.two_depth").slideDown(slideDelay);
  		$("#lnb02 > div.hidden_box").slideDown(slideDelay);
  		$("#lnb02 > a > img").attr("src",$("#lnb02 > a > img").attr("src").replace("_off","_on"));
  		$("#lnb01 > ul.two_depth").css("display","none");
  		$("#lnb01 > div.hidden_box").css("display","none");
  		$("#lnb01 > a > img").attr("src",$("#lnb01 > a > img").attr("src").replace("_on","_off"));
		$("#lnb03 > ul.two_depth").css("display","none");
  		$("#lnb03 > div.hidden_box").css("display","none");
  		$("#lnb03 > a > img").attr("src",$("#lnb03 > a > img").attr("src").replace("_on","_off"));

		}
		catch (err)
		{
		}
	});

	$("#lnb03 > a > img").click(function(){
	  try
		{
  		$("#lnb03 > ul.two_depth").slideDown(slideDelay);
  		$("#lnb03 > div.hidden_box").slideDown(slideDelay);
  		$("#lnb03 > a > img").attr("src",$("#lnb03 > a > img").attr("src").replace("_off","_on"));
  		$("#lnb01 > ul.two_depth").css("display","none");
  		$("#lnb01 > div.hidden_box").css("display","none");
  		$("#lnb01 > a > img").attr("src",$("#lnb01 > a > img").attr("src").replace("_on","_off"));
  		$("#lnb02 > ul.two_depth").css("display","none");
  		$("#lnb02 > div.hidden_box").css("display","none");
  		$("#lnb02 > a > img").attr("src",$("#lnb02 > a > img").attr("src").replace("_on","_off"));
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
	var thissrc = $(".lnb-list-in > li").eq(a).find("img").eq(0).attr("src");
	var thissrcin = $("li",$(".lnb-list-in > li").eq(a)).eq(b).find("img").attr("src");
	var inul = $("ul",$(".lnb-list-in > li").eq(a));
	if(inul != null)
	{
		inul.show();
	}
	if(thissrc)
	{
		$(".lnb-list-in > li").eq(a).find("img").eq(0).attr("src",thissrc.replace("_off","_on"));
		$(".lnb-list-in > li").eq(a).addClass("slc");
	}
	if(thissrcin)
	{
		$("li",$(".lnb-list-in > li").eq(a)).eq(b).find("img").attr("src",thissrcin.replace("_off","_on"));
		$("li",$(".lnb-list-in > li").eq(a)).eq(b).addClass("selected");
	}
}
