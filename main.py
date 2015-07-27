import webapp2

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('home.html')
        variables = {}
        self.response.write(template.render(variables))
        #self.response.write('Hello world!')

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
