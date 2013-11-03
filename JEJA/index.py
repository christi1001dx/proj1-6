import utils2




def getHeader(uid):
    if uid == -1:
        return '''
<nav class="navbar navbar-default">
<div class="navbar-header">
<a class="navbar-brand" href="/">Home</a>
<ul class="nav navbar-nav">
<li class="active"><a href="login">Login</a></li>
<li><a href="register">Register</a></li>
</ul>

</div>
</nav>
'''
    else:
        return '''
<nav class="navbar navbar-default">
<div class="navbar-header">
<a class="navbar-brand" href="/">Home</a>
<p class="navbar-text">Logged in as <strong>%s</strong></p>
<ul class="nav navbar-nav">
<li><a href="logout">Logout</a></li>
</ul>

</div>
</nav>
'''%(utils2.uidToUsername(uid))

def formatData(uid, post):
    com = utils2.getComments(post["id"])
    return formatData2(uid,post,com)


def formatData2(uid, post, comments):
    r = ""
    for x in comments:
        if x["uid"] == -1:
            x["username"] = "Guest"
        else:
            x["username"] = utils2.uidToUsername(x["uid"])
        r += formatComment(x)

        
    post["comments"] = r

    post["author"] = utils2.uidToUsername(post["uid"])

    if uid == post["uid"]:
        post["authorHTML"] = authorLinksHTML(post["id"])
    else:
        post["authorHTML"] = ""

    return formatPost(post,uid==-1)



def authorLinksHTML(pid):
    return '''
    <a href="edit?id=%d" class="btn btn-warning"><span class="glyphicon glyphicon-pencil"></span> Edit</a>
    <a href="delete?id=%d" class="btn btn-danger"><span class="glyphicon glyphicon-remove"></span> Delete</a>
    '''%(pid,pid)

def formatComments(data):
    r = ""
    for x in range(0,len(data)):
        r += formatComment(data[x])
        
    return r

def formatComment(data):
    # data:
    # username = username
    # content = comment content
    return '''              <tr>
                <td><a href="#">%(username)s</a><br />%(content)s</td>
              </tr>'''%(data)

def formatPost(data,guest):
    # data:
    # title = title
    # author = author username
    # content = post content
    # comments = HTML comments (run each comment through formatComment() and put into one variable)
    # authorLinksHTML = if user == author display edit/delete links, call function authorLinksHTML()
    r = '''
      <table class="table post">
	<tr class="active"><td class="postHeader" colspan="2"><a class="postTitle" href="post?id=%(id)s">%(title)s</a><div class="postAuthor">Posted by <a href="#">%(author)s</a></div></td></tr>
	<tr class="active"><td colspan="2">%(content)s</td></tr>
	<tr class="active">
	  <td colspan="2" class="likes">
	    <span class="glyphicon glyphicon-thumbs-up"></span> <a href="#">User</a>, <a href="#">User 2</a>
	  </td>
	</tr>
	<tr class="active">
	  <td colspan="2">
	    <table class="table comments">
              %(comments)s
              <tr class="active">
                <td><form action="comment" method="post"><input name="pid" type="hidden" value="%(id)s" /><input name="comment" class="form-control" placeholder="Add a comment!" /><input type="submit" value="Add" style="display:none" /></form></td>
              </tr>
	    </table>
	  </td>
	</tr>'''%(data)

    if not guest:
        r += '''
	<tr class="active">
	  <td class="links left">
	    <a href="#" class="btn btn-primary"><span class="glyphicon glyphicon-thumbs-up"></span> Like</a>
	  </td>
	  <td class="links right">
            %(authorHTML)s
	  </td>
	</tr>'''%(data)
    r += '</table>'
    return r


if __name__ == "__main__":
    post = {"title":"HELLO","author":"Andrew","content":"ME ME ME","authorLinksHTML":authorLinksHTML()}
    comment1 = {"username":"Andrew","content":"TEST COMMENT"}
    comment2 = {"username":"Z","content":"aaaaa"}
    
    k = formatData(post,[comment1,comment2])

    print(formatPost(k))


