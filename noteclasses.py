__author__ = "ideans"

import lessonlib
import os

# class Entry():
#
#     def __init__(self, title, id_number):
#         self.title = title
#         self.id_number = id_number
#
#     def get_title(self):
#         return self.title
#
#     def get_id_number(self):
#         return self.id_number

# Defining the Lesson class that will hold all the data for each lesson to make accessing
# lesson data easier.

class Lesson():

    def __init__(self, lesson_number):

        file_name = str(lesson_number)+'.txt'
        # lesson_path = os.path.join(os.path.dirname(__file__), 'lesson_notes')
        lesson_path = os.path.join("C:\\Users\\Ian\Documents\\Intro to Programming\\notesapp\lesson_notes\\", file_name)
        # lessonlib.write_log("**** %s found in %s *****" % (file_name, lesson_path))

        lessonfile = open(lesson_path, 'r')
        # lessonlib.write_log("**** Opening %s ****" % file_name)

        lesson_text = lessonfile.read()
        # lessonlib.write_log("Reading %s" % file_name)

        lessonfile.close()
        # lessonlib.write_log("**** %s Closed *****\n" % file_name)

        self.name = lessonlib.get_lesson_name(lesson_text)
        self.concepts = lessonlib.fill_concepts(lesson_text, lessonlib.get_num_of_concepts(lesson_text))
        # lessonlib.write_log('** concepts filled **')

        # lessonlib.write_log(' --- Lesson %(number)s : %(name)s created with %(concepts)s concepts ---\n' %
        #                    {"number": lesson_number, "name": self.name, "concepts": str(len(self.concepts))})

    def get_concept(self, concept_number):
        return self.concepts[concept_number-1]


# lesson7 = Lesson(7)
# print lesson7.name
# print lesson7.concepts[4]['title']
# print lesson7.concepts[4]['description']