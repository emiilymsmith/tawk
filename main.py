import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users

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

"""
class Users(ndb.Model):
    username = ndb.StringProperty(required=True)
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


#connects to /user
class UserHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('user.html')
        variables = {}
        self.response.write(template.render(variables))



#new database for a "give advice" post
class GiveAdvicePost(ndb.Model):
    title = ndb.StringProperty(required=True)
    content = ndb.TextProperty(required=True)


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
        #2.
        post = GiveAdvicePost(title=title,content=content)
        post.put()
        #3.
        #self.redirect( '/advice?key=' + advice.key.urlsafe() )
        return self.redirect('/advice')



# for the home page of advice posts
class AdviceHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('advice.html')
        variables = {}
        self.response.write(template.render(variables))

    def post(self):
        advice = GiveAdvicePost.query().fetch()



class PostOutlineHandler(webapp2.RequestHandler):
    def get(self):


        template = env.get_template('post_outline.html')
        variables = {}
        self.response.write(template.render(variables))


class Categories(ndb.Model):
    family = ndb.StringProperty(required=True)
    friends = ndb.StringProperty(required=True)
    strangers = ndb.StringProperty(required=True)
    date = ndb.StringProperty(required=True)
    strangers = ndb.StringProperty(required=True)
    general = ndb.StringProperty(required=True)



class CategoryHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('tag.html')
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
    ('/postoutile', PostOutlineHandler),
    #('/redirect', RedirectHandler)
    #('/fawk', FawkHandler)
], debug=True)
