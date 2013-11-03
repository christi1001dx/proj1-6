var blockw = BLOCK = 300, PAD = 20, contw, bw, bh;
var HEADSIZE = [60, 400];
var s = [];

var sideneg = 30, sideopen = 0;

$(function() {
	$(window).resize(calcheader).scroll(calcheader).resize();
	
	$("#sidebar .label").mouseover(function() {
		if (!!sideopen) return;
		$(this).animate({
			opacity : 0
		},{
			duration : 500,
			complete : function() {
				sideopen = 1;
				$(this).css("display","none");
				calcheader();
				blocks();
			},
			step : function() {
				calcheader();
				blocks();
			}
		});
		var $side = $(this).parent();
		$side.animate({
			left: 0
		},500);
		$side.find(".stuff").animate({
			opacity:1
		},500);
		sideopen = 2;
	})
	$("#sidebar").mouseout(function() {
		if (sideopen != 1) return;
		$(this).find(".label").css("display","block").animate({
			opacity : 1
		},{
			duration : 500,
			complete : function() {
				sideopen = 0;
				calcheader();
				blocks();
			},
			step : function() {
				calcheader();
				blocks();
			}
		});
		$(this).animate({
			left:30-$(this).width()
		},500);
		$(this).find(".stuff").animate({
			opacity:0
		},500);
		sideopen = 2;
	});
});

function calcheader() {
	bw = $(window).width(); bh = $(window).height();
	var st = $(window).scrollTop();
	sideneg = $("#sidebar").width() + $("#sidebar").position().left;
	bw -= sideneg;
	
	var hh = Math.max(HEADSIZE[1] - st, HEADSIZE[0]);
	$("header").css("height", hh);
	var fsr = (hh - HEADSIZE[0]) / (HEADSIZE[1]-HEADSIZE[0]);
	$(".title h1").css("font-size", fsr * 130 + 45);
	$(".title .sub").css("font-size", fsr * 40)
		.css("opacity", (hh>HEADSIZE[1]/2)?1:0).css("display", (hh>HEADSIZE[1]/4)?"block":"none");
	
	$("header, .container").css({
		"width": bw,
		left : sideneg
	});
}

var pre = ["","-moz-","-o-","-webkit-","-ms-"];
$(function() {
	$.fn.extend({
		css3 : function(obj) {
			for(var i in obj) {
				for(var j in pre) {
					this.css(pre[j]+i,obj[i]);
				}
			}
			return this;
		}
	});
	for(var i=0;i<stories.length;i++) {
		stories[i].shown = false;
		s.push(i);
		$("#cards").append(
			$("<div></div>").attr("id","box"+i).addClass("box").css({
				//opacity : 0
			}).html(
				"<div class='title'><div class='text'>"+stories[i].title+"</div></div>"+
				"<div class='author'>by "+stories[i].author+"</div>"+
				"<div class='edits' title='"+stories[i].edits+" edits'><img src='"+dir+"img/edit.png' />"+stories[i].edits+"</div>"+
				"<div class='story'>"+stories[i].text+"</div>"+
				"<div class='goto'><div class='text' onclick='openStory("+i+")'>Go to Story &rarr;</div></div>"
			).css("opacity",0).css3({
				"transform-origin" : "50% 50%"
			})
		);
	}
	
	$(".back-button").click(hideStory);
	
	$(window).resize(blocks).scroll(blocks).resize();
	setInterval(showBlocks, 100);
});

function hideStory() {
	$("#story").animate({
		left:$(window).width()
	},500,function() {
		$(this).css("display","none");
	});
	$("#stories").css("display","block").css("left",-$(window).width()).animate({
		left : sideneg
	},500);
	$("header").animate({
		top : 0
	},500);
}
function openStory(i) {
	$("#story").css("display","block")
	.css("left", $(window).width())
	.animate({
		left : sideneg
	},500);
	$("#stories").animate({
		left : -bw
	},500,function() {
		$(this).css("display","none");
	});
	$("header").animate({
		top : -400
	},500);
	var s = stories[i];
	$(".story-author").html("by "+s.author);
	$(".story-container h1").html(s.title);
	$(".story-text .text").html(s.text);
}

function showBlocks() {
	bw = $(window).width() - sideneg; bh = $(window).height();
	var st = $(window).scrollTop(), ct = $("#cards").position().top;
	var x=0, y=0;
	for(var i=0;i<s.length;i++) {
		var b = stories[s[i]];
		if (!b.shown && ct + PAD + (PAD+blockw)*y + blockw / 3 < st + bh) {
			b.shown = true;
			$("#box"+s[i]).css3({
				transform : "rotateY(180deg)"
			}).css("opacity",0).animate({
				opacity : 1
			}, {
				step:function(now, fx) {
					$(this).css3({transform:"rotateY("+(220+140*now)+"deg) scale("+(0.5+0.5*now)+")"});
				},
				duration : 1000
			});
			break;
		}
		if (++x >= coln) y += (x=0)+1;
	}
}
function blocks() {
	bw = $(window).width() - sideneg; bh = $(window).height();
	var st = $(window).scrollTop(), ct = $("#cards").position().top;
	
	coln = 10;
	while ((contw = coln*BLOCK + (coln+1)*PAD) > bw) coln--;
	blockw = (bw - (coln+1)*PAD) / coln;
	
	var x=0, y=0;
	for(var i=0;i<s.length;i++) {
		var b = stories[s[i]];
		$("#box"+s[i]).css({
			left : PAD + (PAD+blockw)*x,
			top : PAD + (PAD+blockw)*y,
			width : blockw,
			height : blockw
		});
		if (++x >= coln) y += (x=0)+1;
	}
	
}









var authors = "Snoop Dogg,Dr. Dre,Eminem,50 Cent,Lil Wayne,Tupac,Kanye West,Jay Z,Biggie".split(",");
var loremipsum = "Lorizzle ipsizzle dolizzle sit fizzle, boofron adipiscing elizzle. Nullam sapien velit, shizzlin dizzle bow wow wow, fizzle izzle, crunk doggy, fo shizzle mah nizzle fo rizzle, mah home g-dizzle. Pellentesque eget mofo. Dope fizzle. Own yo' things my shizz dapibizzle the bizzle tempizzle i'm in the shizzle. Maurizzle pellentesque nibh phat check out this. Yippiyo i'm in the shizzle tortizzle. Pellentesque eleifend rhoncizzle rizzle. In hizzle habitasse platea break yo neck, yall. bow wow wow. Curabitur mah nizzle dawg, pretizzle da bomb, bow wow wow ac, eleifend vitae, nunc. Dang suscipit. Bling bling sempizzle velit sizzle uhuh ... yih!.\n\nCurabitizzle sure diam quizzle nisi that's the shizzle mollis. Fo potenti. Morbi odio. Fo neque. Crizzle orci. Crizzle maurizzle mauris, interdum a, own yo' mah nizzle amizzle, go to hizzle izzle, pede. Sure gravida. We gonna chung ass black, volutpat izzle, sagittis sizzle, adipiscing mammasay mammasa mamma oo sa, velit. Crizzle in ipsum. Shit volutpizzle felis vizzle gangsta. Crizzle mammasay mammasa mamma oo sa justo in purizzle pot ornare. We gonna chung venenatizzle crunk for sure phat. Crunk crackalackin. Suspendisse boom shackalack placerat lacizzle. Curabitizzle doggy ante. Nunc its fo rizzle, shut the shizzle up eu dapibus hendrerizzle, dizzle daahng dawg elementizzle sem, in aliquizzle yo mamma felis bling bling shit. Dawg shiznit nisl. Class pizzle taciti yo mamma ad litora torquent fo nizzle stuff, pizzle fo shizzle hymenizzle. Aliquam i saw beyonces tizzles and my pizzle went crizzle, boofron nec elementum nonummy, da bomb orci viverra leo, bling bling break it down risus stuff uhuh ... yih! sem.\n\nPraesent non mi mauris posuere mah nizzle. Aliquizzle lacinia viverra crackalackin. Crizzle izzle uhuh ... yih! break yo neck, yall leo phat euismizzle. Aliquam lobortizzle, maurizzle vitae dapibus daahng dawg, sure boom shackalack bow wow wow metus, dawg venenatizzle for sure dui fo shizzle arcu. Vivamus gravida crazy id ass. Ass cool magna, phat sizzle amizzle, faucibizzle fo, placerizzle daahng dawg, maurizzle. Dizzle vehicula shit pot. Vestibulum fo diam, hendrerizzle gangster, condimentizzle izzle, malesuada break it down, arcu. Morbi aliquizzle placerat nulla. Maecenizzle malesuada break yo neck, yall shizznit erizzle. Phat you son of a bizzle sizzle, ma nizzle eu, accumsizzle quis, elementizzle egizzle, neque. Nulla iaculizzle dizzle a orci hizzle sodalizzle. Fusce sagittizzle, nulla eget we gonna chung mollizzle, lacizzle quizzle bow wow wow erat, shiznit vehicula fizzle purus vitae arcu. I saw beyonces tizzles and my pizzle went crizzle fo hizzle. Nunc break it down black. Duis eu yo. Vestibulum a magna. Gangsta turpizzle doggy, consectetizzle i saw beyonces tizzles and my pizzle went crizzle, dawg, facilisizzle daahng dawg, pede. Fizzle tellizzle. Sure nisi eros, tristique doggy amizzle, black izzle, tincidunt non, augue.\n\nVivamizzle ghetto mofo eget nisi check it out pretizzle. Ma nizzle sizzle that's the shizzle . Nizzle eu break yo neck, yall egizzle lacizzle auctor i'm in the shizzle. Praesent fo shizzle viverra shiznit. Curabitizzle in arcu. Shizzlin dizzle enizzle that's the shizzle, auctor sizzle, dang gizzle, dignissizzle gangster, libero. Dizzle vitae shiz non erizzle posuere pharetra. Quisque pede tortizzle, gangster pizzle, auctizzle a, black i saw beyonces tizzles and my pizzle went crizzle amet, erat. Go to hizzle izzle dui. Aliquizzle shiznit purus, elementizzle consectetizzle, gangster in, consequizzle imperdiet, yippiyo. Quisque fo shizzle ipsizzle fo shizzle mah nizzle fo rizzle, mah home g-dizzle you son of a bizzle check it out vehicula. Fo shizzle mah nizzle fo rizzle, mah home g-dizzle accumsizzle rizzle ipsum. Pellentesque habitant fo shizzle tristique gangster yippiyo netus izzle fizzle fames ac away you son of a bizzle. In est. Doggy elementum. Ut eros its fo rizzle, rizzle quizzle, suscipizzle ac, porta pulvinizzle, gangsta. Nulla brizzle gravida daahng dawg.\n\nBlack izzle ligula. Aliquam yo dizzle tellizzle. Dope viverra, check out this uhuh ... yih! vulputate hendrerizzle, i'm in the shizzle hizzle hendrerizzle check out this, non condimentum shizzle my nizzle crocodizzle sapizzle izzle nunc. Donizzle eu its fo rizzle. Vestibulum pizzle felis. Sed elementizzle faucibus erizzle. Tellivizzle that's the shizzle i saw beyonces tizzles and my pizzle went crizzle, volutpizzle bizzle, volutpat egizzle, auctizzle pot, nunc. The bizzle mammasay mammasa mamma oo sa. Gangsta yippiyo. Curabitur sizzle check it out leo nizzle ante shit dignissizzle. Quisque laorizzle tellus sit amizzle enizzle. Black tempus nizzle cool.\n\nVivamus tempizzle my shizz izzle phat. Pellentesque izzle shut the shizzle up mofo ligula dapibus interdum. Etizzle crazy pharetra dui. Aliquam luctizzle feugizzle neque. Doggy erat volutpat. In sit amizzle nisl. Pellentesque that's the shizzle funky fresh that's the shizzle nunc. Aenean phat gangsta. Quisque lorizzle justo, owned dapibizzle, check it out izzle, phat nizzle, dang. Nulla go to hizzle felizzle izzle sapizzle owned consequat. Integer nizzle erizzle. Crizzle interdum. Morbi nisi tortizzle, pizzle get down get down, pharetra a, fo shizzle mah nizzle fo rizzle, mah home g-dizzle sure, nibh. Pellentesque dapibus cool mi. Yo mamma nisl orci, i saw beyonces tizzles and my pizzle went crizzle quizzle, vehicula id, shizznit pizzle, sheezy. Nullizzle leo. Check out this crazy sapizzle in get down get down semper mattizzle. Nizzle lectus go to hizzle, facilisizzle go to hizzle, mammasay mammasa mamma oo sa shizzle my nizzle crocodizzle, adipiscing in, ante.";
loremipsum = loremipsum.split("\n\n");