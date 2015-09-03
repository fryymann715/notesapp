__author__ = 'Ian'

from google.appengine.ext import ndb
import lessonhandlers

LESSON_DIR = "lesson_dir"
DEFAULT_LESSON = '1'


def lesson_dir(lesson_note=LESSON_DIR):
    return ndb.Key('Lesson_Number', lesson_note)


def lesson_db(lesson_number=DEFAULT_LESSON):
    return ndb.Key('Concepts_in_Lesson', lesson_number)


class Concept(ndb.Model):
    title = ndb.StringProperty(indexed=False)
    description = ndb.StringProperty(indexed=False)


class Lesson_Note(ndb.Model):
    name = ndb.StringProperty(indexed=False)
    concepts = ndb.KeyProperty(indexed=True)


