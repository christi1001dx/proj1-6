
def formatData(post, comments):
    r = ""
    for x in comments:
        r += formatComment(x)

    post["comments"] = r
    return r



    

def authorLinksHTML():
    return '''
    <a href="#" class="btn btn-warning"><span class="glyphicon glyphicon-pencil"></span> Edit</a>
    <a href="#" class="btn btn-danger"><span class="glyphicon glyphicon-remove"></span> Delete</a>
    '''


def formatComment(data):
    # data:
    # username = username
    # content = comment content
    return '''
    	      <tr>
		<td><a href="#">%(username)s</a><br />%(content)s</td>
	      </tr>
'''%(data)

def formatPost(data):
    # data:
    # title = title
    # author = author username
    # content = post content
    # comments = HTML comments (run each comment through formatComment() and put into one variable)
    # authorLinksHTML = if user == author display edit/delete links, call function authorLinksHTML()
    return '''
      <table class="table post">
	<tr class="active"><td class="postHeader" colspan="2"><a class="postTitle" href="#">%(title)s</a><div class="postAuthor">Posted by <a href="#">%(author)s</a></div></td></tr>
	<tr class="active"><td colspan="2">%(content)s<br /><br />stuff</br /><br />stuff</td></tr>
	<tr class="active">
	  <td colspan="2" class="likes">
	    <span class="glyphicon glyphicon-thumbs-up"></span> <a href="#">User</a>, <a href="#">User 2</a>
	  </td>
	</tr>
	<tr class="active">
	  <td colspan="2">
	    <table class="table comments">
              %(comments)s
	    </table>
	  </td>
	</tr>
	<tr class="active">
	  <td class="links left">
	    <a href="#" class="btn btn-primary">Comment</a>
	    <a href="#" class="btn btn-primary"><span class="glyphicon glyphicon-thumbs-up"></span> Like</a>
	  </td>
	  <td class="links right">
            %(authorHTML)s
	  </td>
	</tr>
      </table>
'''%(data)


if __name__ == "__main__":
    post = {"title":"HELLO","author":"Andrew","content":"ME ME ME","authorLinksHTML":authorLinksHTML()}
    comment1 = {"username":"Andrew","content":"TEST COMMENT"}
    comment2 = {"username":"Z","content":"aaaaa"}
    
    k = formatData(post,[comment1,comment2])

    print(formatPost(k))
