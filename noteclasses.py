__author__ = "ideans"

import lessonlib
import os
from google.appengine.api import users
from google.appengine.ext import ndb

# The Lesson class builds a lesson object that holds the data for each lesson based
# on the note file in the lesson_notes directory.


class Lesson:

    def __init__(self, lesson_number):

        file_name = 'lesson_notes/'+lesson_number+'.txt'
        lesson_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
        lessonfile = open(lesson_path, 'r')
        lesson_text = lessonfile.read()
        lessonfile.close()

        self.name = lessonlib.get_lesson_name(lesson_text)
        self.concepts = lessonlib.fill_concepts(lesson_text, lessonlib.get_num_of_concepts(lesson_text))


