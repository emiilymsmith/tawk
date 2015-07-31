import webapp2
import jinja2
import time
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import urlfetch

def shorter_name(user):
    return user.email().partition('@')[0].capitalize()

env = jinja2.Environment(loader=jinja2.FileSystemLoader('template'))
env.globals['shorter_name'] = shorter_name

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
        users_fawks = FawkPost.query(FawkPost.userID==current_user.user_id()).fetch()

        logout_url = users.create_logout_url('/')
        template = env.get_template('user.html')
        variables = {'short_user':short_user,'users_advice':users_advice,'logout_url':logout_url,'users_fawks':users_fawks}
        self.response.write(template.render(variables))

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

        current_user = users.get_current_user()
        short_user = current_user.email().partition('@')[0].capitalize()

        categories = set() #different type of list where I can have multiple of the same title
        category_from_post = url_category
        for post in all_advice:
            categories.add(category_from_post)

        template = env.get_template('category.html')
        variables = {'all_advice': all_advice,
                     'categories':sorted(categories),
                     'category_from_post':category_from_post,
                     'url_category': url_category,
                     'short_user':short_user}
        self.response.write(template.render(variables))

#for posts on fawk
class FawkPost(ndb.Model):
    content = ndb.StringProperty(required=True)
    user = ndb.UserProperty(required=True)
    userID = ndb.StringProperty(required=True)

# this lists all of the fawks '/fawk'
class FawkHandler(webapp2.RequestHandler):
    def get(self):
        current_user = users.get_current_user()
        short_user = current_user.email().partition('@')[0].capitalize()

        posts = FawkPost.query().fetch() #list of post objects from ndb model

        template = env.get_template('fawk.html')
        variables = {'posts': posts,'short_user':short_user}
        self.response.write(template.render(variables))

    def post(self):
        user = users.get_current_user()
        userID = user.user_id()
        content = self.request.get('content')

        fawk_post = FawkPost(content=content,user=user,userID=userID)
        fawk_post.put()
        time.sleep(.5)
        self.redirect('/fawk')


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/login', LoginHandler),
    ('/about', AboutHandler),
    ('/user', UserHandler),
    ('/giveadvice', GiveAdviceHandler),
    ('/advice', AdviceHandler),
    ('/category', CategoryHandler),
    ('/postoutline', PostOutlineHandler),
    ('/fawk', FawkHandler)
], debug=True)
