(function($) {
	$(document).ready(function() {
		var $body = $("body");
		var sidebarWidth = "250px";
		$(".sidebar").hover(function() {
			$(".sidebar-body-wrapper").css("width", sidebarWidth)
			$body.css("padding-left", "285px");
		}, function() {
			$(".sidebar-body-wrapper").css("width", "")
			$body.css("padding-left", "");
		});
	});
})(jQuery);