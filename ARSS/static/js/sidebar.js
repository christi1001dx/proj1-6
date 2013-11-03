(function($) {
	function add(unit, a, b) {
		var s = 0;
		for (var i = 1; i < arguments.length; i++)
			s += parseInt(arguments[i], 10);
		return s + unit;
	}
	$(document).ready(function() {
		var $body = $("body"),
			$sidebar = $(".sidebar"),
			$label = $(".sidebar-label"),
			$labelText = $label.children("h1").first(),
			$bodyWrapper = $(".sidebar-body-wrapper"),
			$sidebarBody = $bodyWrapper.children(".sidebar-body").first();

		var labelWidth = $label.css("width"),
			bodyWidth = "250px",
			bodyPadding = "7px",
			bodyTotalWidth = add("px", bodyWidth, bodyPadding, bodyPadding);
			// total width
			sidebarWidth = add("px", labelWidth, bodyTotalWidth);

		function open() {
			$bodyWrapper.css({
				width: bodyTotalWidth,
				"padding-left": bodyPadding,
				"padding-right": bodyPadding
			});
			$body.css("padding-left", sidebarWidth);
			$sidebarBody.css("opacity", "1");
		}
		function close() {
			$bodyWrapper.css({
				width: "",
				"padding-left": "0",
				"padding-right": "0"
			});
			$body.css("padding-left", "");
			$sidebarBody.css("opacity", "0");
		}
		open();
		//$labelText.mouseenter(open);
		//$sidebar.mouseleave(close);
	});
})(jQuery);
