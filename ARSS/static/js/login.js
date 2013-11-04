
// callback(success)
//   success = T/F
function login(user, pass, callback) {
	$.post("login", {
		username : user,
		password : pass
	}, function(d) {
		if (d.indexOf("success") > -1) callback(true);
		else callback(false);
	});
}

// callback(success, error)
//    success = T/F
//    error = whatever
function register(user, pass, pass2, callback) {
	$.post("register", {
		username : user,
		password : pass,
		password2 : pass2
	},function(d) {
		if (d.indexOf("success") > -1) callback(true);
		else callback(false, d);
	});
}

// callback(success)
//    success = T/F
//    if success is F it just means wasn't logged in in the first place
function logout(callback) {
	$.post("logout", {}, function(d) {
		if (d.indexOf("success") > -1) callback(true);
		else callback(false);
	});
}

// callback(status)
//    status = -1 not logged in
//              0 story already exists or some random other error
//              1 success
function make_story(title, callback) {
	$.post("makestory", {
		title : title
	}, function(d) {
		if (d.indexOf("success") > -1) callback(-1);
		else callback(eval(d.toLowerCase())?1:0);
	});
}

// callback(success)
//    success = T/F
function add_line(title, line, callback) {
	$.post("addline", {
		title : title,
		line : line
	}, function(d) {
		if (d.indexOf("success") > -1) callback(true);
		else callback(false);
	});
}

function get_all_stories() {
	$.get("allstories", function(d) {
    var allstories = JSON.parse(d);
	});
}



