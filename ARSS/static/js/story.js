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
	$.fn.toggleEmpty = function(empty) {
		var placeholder = this.data("placeholder");
		if (empty) {
			this.data("empty", true);
			this.text(placeholder);
			this.css("color", "gray");
		} else {
			this.data("empty", false);
			this.text("");
			this.css("color", "");
		}
		return empty;
	};
	$.fn.cleanAttrs = function() {
		this.removeAttr("id");
		this.removeAttr("contenteditable");
		this.removeAttr("style");
		this.removeAttr("data-placeholder");
	};
	/*** NEW LINE CODE ***/
	$(document).ready(function() {
		var $text = $(".story-text");
		$text.on("keydown paste cut delete", "#story-new-line", function(e) {
			var text = $(this).text();
			var selection = $.getSelection();
			if (e.keyCode == 8 && (text.length <= 1 || selection.length == text.length)) {
				$(this).toggleEmpty(true);
			}
		}).on("keypress", "#story-new-line", function(e) {
			$this = $(this);
			// if is letter or punctuation
			if (e.keyCode >= 32 && $this.data("empty")) {
				$this.toggleEmpty(false);
			}
			// if enter key
			else if (e.keyCode == 13) {
				e.preventDefault();
				var title = $(".story-container h1").first().text();
				var line = $this.text();
				add_line(title, line, function(success) {
					if (success) {
						$(".story-text .text").append(line + " ");
						$this.after('<span id="story-new-line" contenteditable=true data-placeholder="Continue the story!"></span>');
						$("#story-new-line").toggleEmpty(true);
					}
				});
			}
		}).on("paste", "#story-new-line", function(e) {
			var $this = $(this);
			var clipboard = e.originalEvent.clipboardData.getData("Text");
			if (clipboard.length > 0 && $this.data("empty")) {
				$this.toggleEmpty(false);
			}
		});
		$("#story-new-line").toggleEmpty(true);
	});
})(jQuery);