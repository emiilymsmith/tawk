import webapp2
import jinja2

env = jinja2.Environment(loader=jinja2.FileSystemLoader('template'))

# '/login'
class LoginHandler(webapp2.RequestHandler):
    def get(self):
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
