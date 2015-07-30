import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import urlfetch


env = jinja2.Environment(loader=jinja2.FileSystemLoader('template'))
# advice_key_urlsafe = self.request.get('key')
# advice_key = ndb.Key(urlsafe=advice_key_urlsafe)
# advice = advice_key.get()
# user_key = advice.user_key
# user = user_key.get()

# post = GiveAdvicePost(title=title,content=content)
# advice_post = GiveAdvicePost.query( post.advice_key == advice_key ).fetch()
#this is supposed to print the whole list of advice by using the keys
"""
#for posts on fawk
class Post(ndb.Model):
    content = ndb.StringProperty(required=True)
    username = ndb.StringProperty(required=True)


# '/fawk'
class FawkHandler(webapp2.RequestHandler):
    def get(self):
        posts = Post.query().fetch() #list of post objects from ndb model
        posts.sort()#by what though
        template = env.get_template('fawk.html')
        variables = {'posts': posts}
        self.response.write(template.render(variables))

    def post(self):
        content = self.request.get('content')
        username = self.request.get('username')
        fawk_post = Post(content=content,username=username)
        fawk_post.put()
        return self.redirect("/fawk")
"""

# '/' goes to main.html in template
class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('main.html')
        variables = {}
        self.response.write(template.render(variables))
        #self.response.write('Hello world!')

# '/login' page  #copied from learn.co
class LoginHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                        (user.nickname(), users.create_logout_url('/')))
                        #.nickname uses the gmails profile name
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' %
                        users.create_login_url('/'))

        self.response.out.write('<html><body>%s</body></html>' % greeting)
        template = env.get_template('login.html')
        variables = {}
        self.response.write(template.render(variables))

#opens /about us
class AboutHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('about.html')
        variables = {}
        self.response.write(template.render(variables))


#new database for a "give advice" post
class GiveAdvicePost(ndb.Model):
    title = ndb.StringProperty(required=True)
    content = ndb.TextProperty(required=True)
    category = ndb.StringProperty(required=True)
    user = ndb.UserProperty(required=True)
    userID = ndb.StringProperty(required=True)

#connects to /user
class UserHandler(webapp2.RequestHandler):
    def get(self):
        current_user = users.get_current_user()
        short_user = current_user.email().partition('@')[0].capitalize()
        # query all posts, for the logged in user by matching the user
        #id we saved when they created a post
        users_advice = GiveAdvicePost.query(GiveAdvicePost.userID==current_user.user_id()).fetch()

        template = env.get_template('user.html')
        variables = {'short_user':short_user,'users_advice':users_advice}
        self.response.write(template.render(variables))
        logout_url = users.create_logout_url('/')
        self.response.write('<a href ="%s" >Log Out</a>' % logout_url)

#handler for "giving advice"
class GiveAdviceHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('give_advice.html')
        variables = {}
        self.response.write(template.render(variables))

    def post(self):
        #1.
        title = self.request.get('title')
        content = self.request.get('content')
        category = self.request.get('category')
        user = users.get_current_user()
        userID = user.user_id()

        #2.
        post = GiveAdvicePost(title=title,content=content,category=category,user=user,userID=userID)
        post.put()
        #3.
        self.redirect( '/postoutline?key=' + post.key.urlsafe() )
        #return self.redirect('/advice')


class PostOutlineHandler(webapp2.RequestHandler):
    def get(self):
        post_key_urlsafe = self.request.get('key')
        post_key = ndb.Key(urlsafe=post_key_urlsafe)
        post = post_key.get()

        user = users.get_current_user()
        short_user = user.email().partition('@')[0].capitalize()
        #separated the email by @ and prints index 0 or everything before the @

        template = env.get_template('post_outline.html')
        variables = {'post': post,'short_user': short_user}
        self.response.write(template.render(variables))

# for the home page of advice posts
class AdviceHandler(webapp2.RequestHandler):
    def get(self):
        all_posts = GiveAdvicePost.query().fetch()
        categories = set() #different type of list where I can have multiple of the same title
        for post in all_posts:
            category_from_post = post.category
            categories.add(category_from_post)

        template = env.get_template('advice.html')
        variables = {'categories':sorted(categories)}
        self.response.write(template.render(variables))

class CategoryHandler(webapp2.RequestHandler):
    def get(self):
        url_category = self.request.get('tag')
        all_advice = GiveAdvicePost.query(GiveAdvicePost.category==url_category).fetch()
        categories = set() #different type of list where I can have multiple of the same title
        for post in all_advice:
            category_from_post = post.category
            categories.add(category_from_post)

        template = env.get_template('category.html')
        variables = {'all_advice': all_advice,
                     'categories':sorted(categories),
                     'category_from_post':category_from_post,
                     'url_category': url_category}
        self.response.write(template.render(variables))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/login', LoginHandler),
    ('/about', AboutHandler),
    ('/user', UserHandler),
    ('/giveadvice', GiveAdviceHandler),
    ('/advice', AdviceHandler),
    ('/category', CategoryHandler),
    ('/postoutline', PostOutlineHandler),
    #('/redirect', RedirectHandler)
    #('/fawk', FawkHandler)
], debug=True)
