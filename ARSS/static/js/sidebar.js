(function($) {
	function add(a, b) {
		return parseInt(a, 10) + parseInt(b, 10) + "px";
	}
	$(document).ready(function() {
		var $body = $("body");
		var sidebarLabelWidth = $(".sidebar-label").css("width");
		var sidebarBodyWidth = "250px";
		// total width
		var sidebarWidth = add(sidebarLabelWidth, sidebarBodyWidth);

		$(".sidebar").hover(function() {
			$(".sidebar-body-wrapper").css("width", sidebarBodyWidth)
			$body.css("padding-left", sidebarWidth);
		}, function() {
			$(".sidebar-body-wrapper").css("width", "")
			$body.css("padding-left", "");
		});
	});
})(jQuery);