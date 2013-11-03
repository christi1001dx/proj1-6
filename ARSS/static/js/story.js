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
	/*** NEW LINE CODE ***/
	$(document).ready(function() {
		var $newLine = $("#story-new-line");
		var placeholder = $newLine.data("placeholder");
		$newLine.toggleEmpty = function(empty) {
			if (empty) {
				$newLine.data("empty", true);
				$newLine.text(placeholder);
				$newLine.css("color", "gray");
			} else {
				$newLine.data("empty", false);
				$newLine.text("");
				$newLine.css("color", "");
			}
			return empty;
		};
		$newLine.toggleEmpty(true);
		$newLine.on("keydown paste cut delete", function(e) {
			var text = $newLine.text();
			var selection = $.getSelection();
			if (e.keyCode == 8 && (text.length <= 1 || selection.length == text.length)) {
				$newLine.toggleEmpty(true);
			}
		}).on("keypress", function(e) {
			// if is letter or punctuation
			if (e.keyCode >= 32 && $newLine.data("empty")) {
				$newLine.toggleEmpty(false);
			}
			// if enter key
			else if (e.keyCode == 13) {
				e.preventDefault();
			}
		}).on("paste", function(e) {
			var clipboard = e.originalEvent.clipboardData.getData("Text");
			if (clipboard.length > 0 && $newLine.data("empty")) {
				$newLine.toggleEmpty(false);
			}
		});
	});
})(jQuery);