(function($) {
	$(document).ready(function() {
		$body = $("body");
		$(".sidebar").hover(function() {
			$body.css("padding-left", "300px");
		}, function() {
			$body.css("padding-left", "");
		});
	});
})(jQuery);