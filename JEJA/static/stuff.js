/* JEJA */

// comment button
$(function(){
    $("tr.commentTr").children().hide();
    $("a.commentLink").click(function(){
	$(this).parent().parent().prev().find("tr.commentTr").children().slideDown();
    });
});