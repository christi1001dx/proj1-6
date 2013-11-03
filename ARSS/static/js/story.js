(function($) {
	$.getSelection = function() {
		var t = '';
		if (window.getSelection) {
			t = window.getSelection();
		} else if (document.getSelection) {
			t = document.getSelection();
		} else if (document.selection) {
			t = document.selection.createRange().text;
		}
		return t.toString();
	};
	$(document).ready(function() {
		var $newline = $("#story-newline");
		var placeholder = $newline.data("placeholder");
		$newline.toggleEmpty = function(empty) {
			if (empty) {
				$newline.data("empty", true);
				$newline.text(placeholder);
				$newline.css("color", "gray");
			} else {
				$newline.data("empty", false);
				$newline.text("");
				$newline.css("color", "");
			}
			return empty;
		};
		$newline.toggleEmpty(true);
		$newline.on("keydown paste cut delete", function(e) {
			var text = $newline.text();
			var selection = $.getSelection();
			if (e.keyCode == 8 && (text.length <= 1 || selection.length == text.length)) {
				$newline.toggleEmpty(true);
			}
		}).on("keypress", function(e) {
			// if is letter or punctuation
			if (e.keyCode >= 32 && $newline.data("empty")) {
				$newline.toggleEmpty(false);
			}
			// if enter key
			else if (e.keyCode == 13) {
				e.preventDefault();
			}
		}).on("paste", function(e) {
			var clipboard = e.originalEvent.clipboardData.getData("Text");
			if (clipboard.length > 0 && $newline.data("empty")) {
				$newline.toggleEmpty(false);
			}
		});
	});
})(jQuery);