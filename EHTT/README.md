#Project: Bloginator

##Leader: Helen Lin
##Front End: Timothy Ong and Helen Lin
##Flask-y stuff: Eli Cohen
##Back End (MongoDB): Tyrone Ye

##Timeline:
Basic website skeleton/layout done by Oct 28th
Empty website done by Nov 1st
Finishing touches by Nov 4th

##How it will work:

*  So for the project, we plan on having one main page that has links to the other pages as well as maybe titles of the posts with links to the post. 
*  Each post will generate its own page using the generalized 'post' template. 
*  Each post will have its own ID and will be stored in the posts collection.
*  The comments to the post will be stored in the comments collection and will have an ID that will be the same as the one that the post has.
*  When logged in as the admin, it will automatically redirect to the posting page
*  Only when logged in will there be a comment field
*  There will obviously be another collection just for users
*  Main page will have links to register and login pages