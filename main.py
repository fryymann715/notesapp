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

    def validate_input(self, input):
        if input and input.isdigit():
            input = int(input)
            if 1 <= input <= 7:
                return input


class MainHandler(Handler):
    def get(self):
        lesson_number = self.response.get("lesson_input")
        if lesson_number:

        else:
            self.render("base.html")

        # if selected_lesson:
        #     lesson_number = self.validate_input(selected_lesson)
        #     if not lesson_number:
        #         invalid = True
        #         self.render("base.html", invalid=invalid, )
        #     else:
        #         redirect_string = "/lesson?lesson_input=%s" % selected_lesson
        #         self.redirect(redirect_string)
        # else:
        #     self.render("base.html", number_of_lessons=number_of_lessons, css_file=css_file)


class LessonHandler(Handler):
    def get(self):
        selected_lesson = self.request.get("lesson_input")
        if selected_lesson:
            lesson_number = self.validate_input(selected_lesson)
            if not lesson_number:
                invalid = True
                self.render("base.html", invalid=invalid, css_file=css_file)
            else:
                lesson = noteclasses.Lesson(lesson_number)
                self.render("lessons.html", lesson=lesson, number_of_lessons=number_of_lessons, css_file=css_file)




app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/lesson', LessonHandler)
], debug=True)
