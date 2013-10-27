var PAD = 10;
var HEADSIZE = [60, 400];



$(function() {
	$(window).resize(calcheader).scroll(calcheader).resize();
});

function calcheader() {
	var bw = $(window).width(), bh = $(window).height();
	var st = $(window).scrollTop();
	
	var hh = Math.max(HEADSIZE[1] - st, HEADSIZE[0]);
	$("header").css("height", hh);
	var fsr = (hh - HEADSIZE[0]) / (HEADSIZE[1]-HEADSIZE[0]);
	$(".title h1").css("font-size", fsr * 130 + 45);
	$(".title .sub").css("font-size", fsr * 40)
		.css("opacity", (hh>HEADSIZE[1]/2)?1:0).css("display", (hh>HEADSIZE[1]/4)?"block":"none");
	
	
}

