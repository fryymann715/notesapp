__author__ = 'Ian'

import webapp2
import jinja2
import os
import postclasses
import notedb
import lessonlib
import noteclasses


from google.appengine.api import users


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
notes_dir = os.path.join(os.path.dirname(__file__), 'lesson_notes')
number_of_lessons = len(os.listdir(notes_dir))

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

build_lesson_syntax = "-<!Build Lesson %s!>-"
build_all_lessons_syntax = "-<!Build All Lessons!>-"

def build_lessons(arg):
    if arg == build_lesson_syntax % arg:
        lessonlib.build_lesson_table(arg)
        return None
    elif arg == build_all_lessons_syntax:
        a = 1
        while a <= 9:
            lessonlib.build_lesson_table(str(a))
            a += 1
        return None


class Handler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def validate_input(self, arg):
        if arg == build_lesson_syntax or arg == build_all_lessons_syntax:
            build_lessons(arg)
            return None
        elif arg and arg.isdigit():
            if 1 <= int(arg) <= 9:
                return arg
        else:
            return None


class LessonHandler(Handler):
    def get(self):
        lesson_number = self.request.get("lesson_input")
        if lesson_number and self.validate_input(lesson_number):
            dgoods = noteclasses.Dgoods(lesson_number)
            self.render("lessons.html", dgoods=dgoods)
        else:
            dgoods = noteclasses.Dgoods()
            self.render("error.html", dgoods=dgoods)


class PostHandler(Handler):
    def post(self):
        content = self.request.get('content')
        lesson_number = self.request.get('lesson_number')
        post = postclasses.Post(parent=postclasses.lesson_key(lesson_number))

        if users.get_current_user():
            post.author = postclasses.Author(
                identity=users.get_current_user().user_id(),
                name=users.get_current_user().nickname(),
                email=users.get_current_user().email()
                )

        post.content = content
        post.put()
        redirect_string = "/lesson?lesson_input=%s" % lesson_number
        self.redirect(redirect_string)