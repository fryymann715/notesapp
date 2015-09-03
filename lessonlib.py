__author__ = 'Ian'

import os
import noteclasses

# Library full of functions used to pull bits of data from the lesson notes text files.


# Function that finds the number of concepts in the lesson string by counting the amount of TITLE tasgs it finds
def get_num_of_concepts(text):
    number_concepts = 0
    while text.find('TITLE:') != -1:
        number_concepts += 1
        next_spot = text.find('TITLE:')
        text = text[next_spot+6:]
    return number_concepts


# pulls the lesson number from the lesson string and turns it into an integer
def get_lesson_id(text):
    start_location = text.find('LESSON: ')
    end_location = text.find('NAME: ')
    lesson_id = text[start_location+8:end_location]
    lesson_id = lesson_id.rstrip()
    lesson_id = lesson_id.lstrip()
    return lesson_id


# pulls the lesson name from the lesson string
def get_lesson_name(text):
    start_location = text.find('NAME: ') + 6
    end_location = text.find('TITLE: ')
    lesson_name = text[start_location:end_location-1]
    lesson_name = lesson_name.lstrip()
    lesson_name = lesson_name.rstrip()
    return lesson_name


# pulls an individual concept from a chunk of the lesson string
def get_title(concept):
    start_location = concept.find('TITLE: ') + 7
    end_location = concept.find('DESC: ')
    concept_title = concept[start_location:end_location-1]
    return concept_title


# grabs the description portion of the raw concept text
def get_desc(concept):
    start_location = concept.find('DESC: ') + 6
    end_location = concept.find('TITLE: ', start_location)
    concept_desc = concept[start_location:end_location]
    return concept_desc


# loops through all the concepts and fills a list containing all the concepts' info
def fill_concepts(text, number_of_concepts):
    # write_log('-- initializing fill_concepts() with %s concepts --' % str(number_of_concepts))
    counter = 0
    concept_list = []
    while counter < number_of_concepts:
        concept = {}
        this_concept_start = text.find('TITLE:')
        this_concept_end = text.find('TITLE:', this_concept_start + 1)
        raw_concept = text[this_concept_start:this_concept_end]
        concept['title'] = get_title(raw_concept)
        concept['description'] = get_desc(raw_concept)
        # write_log('- creating concept %s -' % concept['title'])
        concept_list.append(concept)
        text = text[this_concept_end:]
        counter += 1
    # write_log('-- finished creating concepts --')
    return concept_list

def get_lesson_text(lesson_number):
    file_name = 'lesson_notes/'+lesson_number+'.txt'
    lesson_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    lessonfile = open(lesson_path, 'r')
    lesson_text = lessonfile.read()
    lessonfile.close()
    return lesson_text

            # lesson = noteclasses.Lesson(file)
            # lesson_entry = noteclasses.Lesson_Entry()
            # lesson_entry.number = file
            # lesson_entry.lesson_obj = lesson
            # lesson_entry.put()


