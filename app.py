import tornado.ioloop
import tornado.web
import tornado.log
import queries
import psycopg2
import os
import sqlalchemy
from sqlalchemy import create_engine

from jinja2 import \
  Environment, PackageLoader, select_autoescape
  
ENV = Environment(
  loader=PackageLoader('appfiles', 'templates'),
  autoescape=select_autoescape(['html', 'xml'])
)

engine = create_engine('postgresql+psycopg2://postgres@localhost:5432/codeemp')

class TemplateHandler(tornado.web.RequestHandler):
  def render_template (self, tpl, context=None):
    if context is None:
      context = {}
      
    template = ENV.get_template(tpl)
    self.write(template.render(context))

class MainHandler(TemplateHandler):
  def get(self):
    self.set_header(
      'Cache-Control',
      'no-store, no-cache, must-revalidate, max-age=0')
    
    self.render_template("index.html")
    

class DeveloperBlogHandler(TemplateHandler):
  def get(self):
    self.set_header(
      'Cache-Control',
      'no-store, no-cache, must-revalidate, max-age=0')
    
    self.render_template("developerblog.html")
    
    
class HobbyBlogHandler(TemplateHandler):
  def get(self):
    self.set_header(
      'Cache-Control',
      'no-store, no-cache, must-revalidate, max-age=0')
    
    self.render_template("hobbyblog.html")
    
    
class PostHandler(TemplateHandler):
  def get (self, slug):
    self.set_header(
      'Cache-Control',
      'no-store, no-cache, must-revalidate, max-age=0')
      
    self.render_template("post.html")
    
    
def make_app():
  return tornado.web.Application([
    (r"/", MainHandler),
    (r"/developerblog", DeveloperBlogHandler),
    (r"/hobbyblog", HobbyBlogHandler),
    (r"/post/(.*)", PostHandler),
    (
      r"/static/(.*)",
      tornado.web.StaticFileHandler,
      {'path': 'static'}
    ),
  ], autoreload=True)
  
if __name__ == "__main__":
  tornado.log.enable_pretty_logging()
  PORT = int(os.environ.get('PORT', '8080'))
  app = make_app()
  app.listen(PORT)
  tornado.ioloop.IOLoop.current().start()