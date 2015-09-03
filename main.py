#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os
import noteclasses
import postclasses

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import db

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

    def build_no_user(self):
        user_dict = {'url': users.create_login_url(self.request.uri),
                     'url_linktext': "Login",
                     'user_name': 'Not Logged In',
                     'is_user': False}
        return user_dict


class MainHandler(Handler):
    def get(self):
        user = users.get_current_user()
        if user:
            user_dict = {'url': users.create_logout_url(self.request.uri),
                         'url_linktext': "Logout",
                         'user_name': user.nickname(),
                         'is_user': True}
        else:
            user_dict = self.build_no_user()

        self.render("base.html", user=user_dict)


# This handler grabs the value stored in the url, which has already been
# validated by InputHandler, and creates a Lesson object with the number
# provided by the user.

class LessonHandler(Handler):
    def get(self):
        lesson_number = self.request.get("lesson_input")
        lesson_wall = postclasses.lesson_key(lesson_number)
        lesson = noteclasses.Lesson(lesson_number)

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
            self.render("lessons.html", lesson=lesson, user=user_dict, posts=posts, lesson_number=lesson_number)

        else:
            user_dict = self.build_no_user()
            self.render("lessons.html", lesson=lesson, user=user_dict, lesson_number=lesson_number)


# This handler is initiated whenever the submit button in base.html is clicked. It takes the input
# passed into lesson_input, validates it, then based on the result of validate_input() it either
# redirects to the LessonHandler or it renders the error.html template.


# validate_input is a function used to make sure the user input is a number
# and that the number is within the range of available lesson notes.

# I want to modify this function to check a global variable for the number
# of lessons there are rather than having it hard-coded here.
class LessonSwitch(Handler):

    def validate_input(self, arg):
        if arg and arg.isdigit():
            arg = int(arg)
            if 1 <= arg <= 9:
                return arg
        else:
                return None

    def post(self):
        input = self.request.get("lesson_input")
        lesson_number = self.validate_input(input)
        if lesson_number:
            redirect_string = "/lesson?lesson_input=%s" % lesson_number
            self.redirect(redirect_string)
        else:
            self.render("error.html", input=input)


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
        else:
            post.author = postclasses.Author(
                name="Anonymous",
                email="Anonymous"
                )

        post.content = content
        post.put()
        redirect_string = "/lesson?lesson_input=%s" % lesson_number
        self.redirect(redirect_string)


app = webapp2.WSGIApplication([('/', MainHandler), ('/lesson', LessonHandler),
                               ('/lessonswitch', LessonSwitch),
                               ('/sign', PostHandler)], debug=True)
