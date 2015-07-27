import webapp2
import jinja2
from google.appengine.api import users

env = jinja2.Environment(loader=jinja2.FileSystemLoader('template'))
"""
class Users(ndb.Model):
    username = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
"""
# '/login' page
class LoginHandler(webapp2.RequestHandler):
    def get(self): #copied from learn.co
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

"""
# '/profile'
class ProfileHandler(webapp2.RequestHandler):
    def get(self):

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

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/login', LoginHandler)
], debug=True)
