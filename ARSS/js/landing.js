var PAD = 20;

$(document).ready(function() {
	var bw = $(window).width(), bh = $(window).height();
	bh -= 3 * PAD;
	$(".top").css("top", PAD);
	$(".top, .left").css("left", PAD);
	
	$(window).trigger("resize");
	
	$(".login .sub").click(function() {
		fadeLR($(".login"), $(".register"));
	});
	$(".register .sub").click(function() {
		fadeLR($(".register"), $(".login"));
	});
	
});

function fadeLR(a, b) {
	a.css({
		marginLeft : -150,
		opacity : 0,
		zIndex : 1
	});
	b.css({
		marginLeft : 0,
		opacity : 1,
		zIndex : 2
	});
}

function resize() {
	var bw = $(window).width(), bh = $(window).height();
	bh -= 3 * PAD;
	$(".top").css({
		width: bw - PAD * 2,
		height : bh * 2 / 5
	});
	$(".left, .right").css("height", bh * 3 / 5);
	$(".left, .right").css({
		width : (bw - PAD * 3) / 2,
		top : bh * 2 / 5 + 2 * PAD
	});
	$(".right").css("left", (bw - PAD * 3) / 2 + 2 * PAD);
}
$(window).resize(resize);
setInterval(resize, 2000);

