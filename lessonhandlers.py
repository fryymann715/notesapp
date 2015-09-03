__author__ = 'Ian'

import webapp2
import jinja2
import os
import postclasses
import notedb

from google.appengine.api import users


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
notes_dir = os.path.join(os.path.dirname(__file__), 'lesson_notes')
number_of_lessons = len(os.listdir(notes_dir))

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


class Handler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def validate_input(self, arg):
        if arg and arg.isdigit():
            arg = int(arg)
            if 1 <= arg <= 9:
                return arg
        else:
            return None

# Function I use to fill the user dictionary when there is no current user.
    def build_no_user(self):
        user_dict = {'url': users.create_login_url(self.request.uri),
                     'url_linktext': "Login",
                     'user_name': 'Not Logged In',
                     'is_user': False}
        return user_dict


class LessonHandler(Handler):
    def get(self):
        lesson_number = self.request.get("lesson_input")
        if lesson_number and self.validate_input(lesson_number):
            lesson_wall = postclasses.lesson_key(lesson_number)
            lesson_query = notedb.Lesson_Note.query(ancestor=notedb.lesson_dir(lesson_number))
            concept_query = notedb.Concept.query(ancestor=notedb.lesson_db(lesson_number))

            lesson = lesson_query.fetch()
            concepts = concept_query.fetch()

            user = users.get_current_user()
            user_dict = {}
            if user:
                user_dict = {'url': users.create_logout_url(self.request.uri),
                             'url_linktext': "Logout",
                             'user_name': user.nickname(),
                             'is_user': True}
                post_query = postclasses.Post.query(ancestor=lesson_wall)\
                    .filter(postclasses.Post.author.identity == user.user_id()).order(-postclasses.Post.date)

                posts = post_query.fetch()
                self.render("lessons.html", lesson=lesson, concepts=concepts, user=user_dict, posts=posts, lesson_number=lesson_number)

        else:
            user_dict = self.build_no_user()
            self.render("error.html", user=user_dict)


class PostHandler(Handler):
    def post(self):
        content = self.request.get('content')
        lesson_number = self.request.get('lesson_number')
        post = postclasses.Post(parent=postclasses.lesson_key(lesson_number))

        if users.get_current_user():
            post.author = postclasses.Author(
                identity=users.get_current_user().user_id(),
                identity=users.get_current_user().user_id(),
                name=users.get_current_user().nickname(),
                email=users.get_current_user().email()
                )

        post.content = content
        post.put()
        redirect_string = "/lesson?lesson_input=%s" % lesson_number
        self.redirect(redirect_string)