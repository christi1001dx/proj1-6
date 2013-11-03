
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


