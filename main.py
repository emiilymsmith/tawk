import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import urlfetch


env = jinja2.Environment(loader=jinja2.FileSystemLoader('template'))

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

"""
#tbd
class RatingHandler(webapp2.RequestHandler):
    def get(self):
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

#users database with username and passwords
# class User(ndb.Model):
#     username = ndb.StringProperty(required=True)
#     password = ndb.StringProperty(required=True)

#new database for a "give advice" post
class GiveAdvicePost(ndb.Model):
    title = ndb.StringProperty(required=True)
    content = ndb.TextProperty(required=True)
    category = ndb.StringProperty(required=True)
    user = ndb.UserProperty(required=True)

#connects to /user
class UserHandler(webapp2.RequestHandler):
    def get(self):
        # user_key_urlsafe = self.request.get('key')
        # user_key = ndb.Key(urlsafe=user_key_urlsafe)
        user = users.get_current_user()

        template = env.get_template('user.html')
        variables = {}
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

        #2.
        post = GiveAdvicePost(title=title,content=content,category=category,user=user)
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

        template = env.get_template('post_outline.html')
        variables = {'post': post,'user':user}
        self.response.write(template.render(variables))

# for the home page of advice posts
class AdviceHandler(webapp2.RequestHandler):
    def get(self):

        all_advice = GiveAdvicePost.query().fetch()


        template = env.get_template('advice.html')
        variables = {'all_advice': all_advice}
        self.response.write(template.render(variables))


# advice_key_urlsafe = self.request.get('key')
# advice_key = ndb.Key(urlsafe=advice_key_urlsafe)
# advice = advice_key.get()
# user_key = advice.user_key
# user = user_key.get()

# post = GiveAdvicePost(title=title,content=content)
# advice_post = GiveAdvicePost.query( post.advice_key == advice_key ).fetch()
#this is supposed to print the whole list of advice by using the keys


class Categories(ndb.Model):
    family = ndb.StringProperty(required=True)
    friends = ndb.StringProperty(required=True)
    strangers = ndb.StringProperty(required=True)
    date = ndb.StringProperty(required=True)
    general = ndb.StringProperty(required=True)

class CategoryHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('category.html')
        variables = {}
        self.response.write(template.render(variables))
    def post(self):
        pass



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
