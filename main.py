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
import lessonhandlers
import lessonlib

from google.appengine.api import users


class MainHandler(lessonhandlers.Handler):



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


app = webapp2.WSGIApplication([('/', MainHandler), ('/lesson', lessonhandlers.LessonHandler),
                               ('/lessonswitch', lessonhandlers.LessonHandler),
                               ('/sign', lessonhandlers.PostHandler)], debug=True)
