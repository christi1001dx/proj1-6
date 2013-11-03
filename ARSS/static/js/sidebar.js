(function($) {
	$(document).ready(function() {
		$(".sidebar").hover(function() {
			$(this).animate({
				width: "500px"
			});
		}, function() {
			$(this).animate({
				width: ""
			});
		});
	});
})(jQuery);