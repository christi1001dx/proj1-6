(function($) {
	$(document).ready(function() {
		var $body = $("body");
		var sidebarWidth = "300px";
		$(".sidebar").hover(function() {
			$(this).css("width", sidebarWidth)
			$body.css("padding-left", sidebarWidth);
		}, function() {
			$(this).css("width", "")
			$body.css("padding-left", "");
		});
	});
})(jQuery);