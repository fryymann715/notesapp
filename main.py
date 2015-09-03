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
import lessonlib

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
notes_dir = os.path.join(os.path.dirname(__file__), 'lesson_notes')
number_of_lessons = len(os.listdir(notes_dir))

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


NO_LESSON = 'None'
#
# def lesson_key(lesson_number):
#
#     return ndb.Key('Lesson', lesson_number)

def lesson_key(lesson_name=NO_LESSON):

    return ndb.Key('Lesson', lesson_name)

class Handler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

# validate_input is a function used to make sure the user input is a number
# and that the number is within the range of available lesson notes.

# I want to modify this function to check a global variable for the number
# of lessons there are rather than having it hard-coded here.
    def validate_input(self, input):
        if input and input.isdigit():
            input = int(input)
            if 1 <= input <= 9:
                return input
            else :
                return None

# This handler simply renders the base.html template and is only run the first time a user
# visits the webapp.
class MainHandler(Handler):
    def get(self):
        # lessonlib.build_lesson_entities()
        self.render("base.html")

# This handler grabs the value stored in the url, which has already been
# validated by InputHandler, and creates a Lesson object with the number
# provided by the user.
class LessonHandler(Handler):
    def get(self):
        # noteclasses.build_lesson_entries()
        lesson_number = self.request.get("lesson_input")
        query_string = noteclasses.Lesson_Entry.query(lesson_key(lesson_number))
        lesson_thing = query_string.fetch()
        # lesson = noteclasses.Lesson(lesson_number)
        self.render("lessons.html")

# This handler is initiated whenever the submit button in base.html is clicked. It takes the input
# passed into lesson_input, validates it, then based on the result of validate_input() it either
# redirects to the LessonHandler or it renders the error.html template.
class InputHandler(Handler):
    def get(self):
        input = self.request.get("lesson_input")
        lesson_number = self.validate_input(input)
        if lesson_number:
            redirect_string = "/lesson?lesson_input=%s" % lesson_number
            self.redirect(redirect_string)
        else:
            self.render("error.html", input=input)



app = webapp2.WSGIApplication([('/', MainHandler), ('/lesson', LessonHandler), ('/inputhandler', InputHandler)
], debug=True)
